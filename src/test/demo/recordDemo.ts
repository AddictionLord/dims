import * as cp from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { downloadAndUnzipVSCode, resolveCliArgsFromVSCodeExecutablePath, runTests } from '@vscode/test-electron';

/**
 * Records `images/demo.gif`: runs `suite.ts` in VS Code with remote debugging
 * enabled, screenshots the workbench over the Chrome DevTools Protocol while
 * the suite debugs `train.py` with dims off and on, then encodes with ffmpeg.
 */

const CDP_PORT = 9339;
const WIDTH = 1280;
const HEIGHT = 720;
const FRAME_INTERVAL_MS = 100;
const FPS = 1000 / FRAME_INTERVAL_MS;
const SETTINGS = {
    'workbench.startupEditor': 'none',
    'workbench.tips.enabled': false,
    'workbench.secondarySideBar.defaultVisibility': 'hidden',
    'workbench.colorTheme': 'Default Dark Modern',
    'window.commandCenter': false,
    'window.zoomLevel': 0,
    'editor.minimap.enabled': false,
    'editor.fontSize': 16,
    'debug.internalConsoleOptions': 'neverOpen',
    'debug.toolBarLocation': 'hidden',
    'chat.commandCenter.enabled': false,
    'chat.disableAIFeatures': true,
    'problems.visibility': false,
    'git.openRepositoryInParentFolders': 'never',
    'telemetry.telemetryLevel': 'off',
    'update.mode': 'none',
};

const SIDEBAR_RIGHT = 500;
const SIDEBAR_SASH_SCRIPT = `(() => {
    const sidebar = document.getElementById('workbench.parts.sidebar').getBoundingClientRect();
    const sash = [...document.querySelectorAll('.monaco-sash.vertical')]
        .map((el) => el.getBoundingClientRect())
        .map((r) => [r.left + r.width / 2, r.top + r.height / 2])
        .find(([x, y]) => Math.abs(x - sidebar.right) < 6 && y > 0);
    return JSON.stringify(sash ?? null);
})()`;

type Point = [number, number];

interface CdpTarget {
    type: string;
    url: string;
    webSocketDebuggerUrl: string;
}

async function main(): Promise<void> {
    const root = path.resolve(__dirname, '../../../');
    const output = path.join(root, 'images', 'demo.gif');
    const workDir = fs.mkdtempSync(path.join(os.tmpdir(), 'dims-demo-'));
    const framesDir = path.join(workDir, 'frames');
    const userDataDir = path.join(workDir, 'user-data');
    const phaseFile = path.join(workDir, 'phase');
    fs.mkdirSync(framesDir);
    fs.mkdirSync(path.join(userDataDir, 'User'), { recursive: true });
    fs.writeFileSync(path.join(userDataDir, 'User', 'settings.json'), JSON.stringify(SETTINGS, null, 4));
    process.env['DIMS_DEMO_PHASE_FILE'] = phaseFile;

    const vscodeExecutablePath = await downloadAndUnzipVSCode('stable');
    const [cli, ...cliArgs] = resolveCliArgsFromVSCodeExecutablePath(vscodeExecutablePath);
    cp.spawnSync(cli, [...cliArgs, '--install-extension', 'ms-python.debugpy'], { stdio: 'inherit' });

    const recording = record(framesDir, phaseFile);
    await runTests({
        vscodeExecutablePath,
        extensionDevelopmentPath: root,
        extensionTestsPath: path.join(__dirname, 'suite'),
        launchArgs: [
            path.join(root, 'src', 'test', 'demo', 'workspace'),
            '--disable-workspace-trust',
            `--user-data-dir=${userDataDir}`,
            `--remote-debugging-port=${CDP_PORT}`,
        ],
    });
    const frames = await recording;

    encodeGif(framesDir, frames, output);
    console.log(`Wrote ${output} (${frames} frames)`);
}

async function record(framesDir: string, phaseFile: string): Promise<number> {
    const target = await waitForWorkbench();
    const cdp = await Cdp.connect(target.webSocketDebuggerUrl);
    await cdp.send('Emulation.setDeviceMetricsOverride', {
        width: WIDTH,
        height: HEIGHT,
        deviceScaleFactor: 1,
        mobile: false,
    });

    let frame = 0;
    let caption = '';
    for (;;) {
        const phase = fs.existsSync(phaseFile) ? fs.readFileSync(phaseFile, 'utf-8') : '';
        if (phase === 'done') {
            break;
        }
        if (phase === 'layout' && caption !== 'layout') {
            caption = phase;
            await layout(cdp);
        } else if (phase && phase !== caption) {
            caption = phase;
            await cdp.send('Runtime.evaluate', { expression: captionScript(caption) });
        }
        const started = Date.now();
        if (caption && caption !== 'layout') {
            const { data } = await cdp.send('Page.captureScreenshot', { format: 'png' });
            fs.writeFileSync(path.join(framesDir, `${String(frame++).padStart(5, '0')}.png`), Buffer.from(data, 'base64'));
        }
        await sleep(Math.max(0, FRAME_INTERVAL_MS - (Date.now() - started)));
    }
    cdp.close();
    return frame;
}

async function layout(cdp: Cdp): Promise<void> {
    const { result } = await cdp.send('Runtime.evaluate', { expression: SIDEBAR_SASH_SCRIPT, returnByValue: true });
    const sidebar: Point | null = JSON.parse(result.value);
    if (sidebar) {
        await drag(cdp, sidebar, [SIDEBAR_RIGHT, sidebar[1]]);
    }
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: WIDTH - 40, y: HEIGHT - 80 });
}

async function drag(cdp: Cdp, from: Point, to: Point): Promise<void> {
    const steps = 10;
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: from[0], y: from[1] });
    await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: from[0], y: from[1], button: 'left', clickCount: 1 });
    for (let i = 1; i <= steps; i++) {
        const x = from[0] + ((to[0] - from[0]) * i) / steps;
        const y = from[1] + ((to[1] - from[1]) * i) / steps;
        await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y, button: 'left', buttons: 1 });
        await sleep(20);
    }
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: to[0], y: to[1], button: 'left', clickCount: 1 });
}

function captionScript(text: string): string {
    const color = text === 'with dims' ? '#2ea043' : '#8b949e';
    return `(() => {
        let el = document.getElementById('dims-demo-caption');
        if (!el) {
            el = document.createElement('div');
            el.id = 'dims-demo-caption';
            Object.assign(el.style, {
                position: 'fixed', top: '10px', right: '16px', zIndex: '100000',
                padding: '6px 14px', borderRadius: '6px', color: '#fff',
                font: '600 18px system-ui, sans-serif', pointerEvents: 'none',
            });
            document.body.appendChild(el);
        }
        el.textContent = ${JSON.stringify(text)};
        el.style.background = ${JSON.stringify(color)};
    })()`;
}

async function waitForWorkbench(): Promise<CdpTarget> {
    for (;;) {
        try {
            const response = await fetch(`http://127.0.0.1:${CDP_PORT}/json/list`);
            const targets = (await response.json()) as CdpTarget[];
            const workbench = targets.find((t) => t.type === 'page' && t.url.includes('workbench'));
            if (workbench) {
                return workbench;
            }
        } catch {
            await sleep(250);
            continue;
        }
        await sleep(250);
    }
}

function encodeGif(framesDir: string, frames: number, output: string): void {
    if (frames === 0) {
        throw new Error('No frames captured');
    }
    const input = path.join(framesDir, '%05d.png');
    const filters = `fps=${FPS},scale=${WIDTH}:-1:flags=lanczos,split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle`;
    const result = cp.spawnSync(
        'ffmpeg',
        ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', input, '-filter_complex', filters, output],
        { stdio: 'inherit' },
    );
    if (result.status !== 0) {
        throw new Error('ffmpeg failed');
    }
}

class Cdp {
    private nextId = 1;
    private readonly pending = new Map<number, (result: any) => void>();

    private constructor(private readonly socket: WebSocket) {
        socket.addEventListener('message', (event) => {
            const message = JSON.parse(String(event.data));
            this.pending.get(message.id)?.(message.result ?? {});
            this.pending.delete(message.id);
        });
    }

    static connect(url: string): Promise<Cdp> {
        return new Promise((resolve, reject) => {
            const socket = new WebSocket(url);
            socket.addEventListener('open', () => resolve(new Cdp(socket)));
            socket.addEventListener('error', reject);
        });
    }

    send(method: string, params: Record<string, unknown> = {}): Promise<any> {
        const id = this.nextId++;
        return new Promise((resolve) => {
            this.pending.set(id, resolve);
            this.socket.send(JSON.stringify({ id, method, params }));
        });
    }

    close(): void {
        this.socket.close();
    }
}

function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
