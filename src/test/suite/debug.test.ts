import * as assert from 'assert';
import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

/**
 * End-to-end: launch a real debugpy session on `fixture/script.py`, stop at a
 * breakpoint and read the DAP `variables` response that backs the Variables view.
 */

interface Stop {
    session: vscode.DebugSession;
    threadId: number;
}

interface DapVariable {
    name: string;
    value: string;
}

const DEBUG_TYPE = 'debugpy';
const DEBUG_TIMEOUT_MS = 45_000;

suite('dims in the Variables view', () => {
    const workspace = vscode.workspace.workspaceFolders![0];
    const script = path.join(workspace.uri.fsPath, 'script.py');

    suiteSetup(() => {
        const lines = fs.readFileSync(script, 'utf-8').split(/\r?\n/);
        const line = lines.findIndex((text) => text.startsWith('print('));
        const location = new vscode.Location(vscode.Uri.file(script), new vscode.Position(line, 0));
        vscode.debug.addBreakpoints([new vscode.SourceBreakpoint(location)]);
    });

    suiteTeardown(async () => {
        vscode.debug.removeBreakpoints(vscode.debug.breakpoints);
        await setEnabled(undefined);
    });

    test('shapes and lengths are prepended', async () => {
        const variables = await debugAndReadLocals(workspace, script);
        assert.match(variables['matrix'], /^\{\[2, 3\]\}, array\(/);
        assert.strictEqual(variables['items'], '{3}, [1, 2, 3]');
        assert.strictEqual(variables['name'], "'dims'");
    });

    test('dims.enabled = false leaves values untouched', async () => {
        await setEnabled(false);
        const variables = await debugAndReadLocals(workspace, script);
        assert.match(variables['matrix'], /^array\(/);
        assert.strictEqual(variables['items'], '[1, 2, 3]');
    });
});

async function setEnabled(value: boolean | undefined): Promise<void> {
    await vscode.workspace.getConfiguration('dims').update('enabled', value, vscode.ConfigurationTarget.Global);
}

async function debugAndReadLocals(folder: vscode.WorkspaceFolder, program: string): Promise<Record<string, string>> {
    const stopped = waitForStop();
    const started = await vscode.debug.startDebugging(folder, {
        type: DEBUG_TYPE,
        request: 'launch',
        name: 'dims e2e',
        program,
        python: pythonInterpreter(),
        console: 'internalConsole',
        justMyCode: true,
    });
    assert.ok(started, 'debug session did not start');

    const { session, threadId } = await withTimeout(stopped, DEBUG_TIMEOUT_MS, 'breakpoint was not hit');
    try {
        return await readLocals(session, threadId);
    } finally {
        await stopSession(session);
    }
}

function pythonInterpreter(): string {
    return process.env['DIMS_E2E_PYTHON'] ?? (process.platform === 'win32' ? 'python' : 'python3');
}

function waitForStop(): Promise<Stop> {
    return new Promise((resolve) => {
        const registration = vscode.debug.registerDebugAdapterTrackerFactory(DEBUG_TYPE, {
            createDebugAdapterTracker: (session) => ({
                onDidSendMessage: (message) => {
                    if (message.type === 'event' && message.event === 'stopped') {
                        registration.dispose();
                        resolve({ session, threadId: message.body.threadId });
                    }
                },
            }),
        });
    });
}

async function readLocals(session: vscode.DebugSession, threadId: number): Promise<Record<string, string>> {
    const { stackFrames } = await session.customRequest('stackTrace', { threadId, startFrame: 0, levels: 1 });
    const { scopes } = await session.customRequest('scopes', { frameId: stackFrames[0].id });
    const { variables } = await session.customRequest('variables', {
        variablesReference: scopes[0].variablesReference,
    });
    return Object.fromEntries((variables as DapVariable[]).map((v) => [v.name, v.value]));
}

async function stopSession(session: vscode.DebugSession): Promise<void> {
    const terminated = new Promise<void>((resolve) => {
        const registration = vscode.debug.onDidTerminateDebugSession((ended) => {
            if (ended.id === session.id) {
                registration.dispose();
                resolve();
            }
        });
    });
    await vscode.debug.stopDebugging(session);
    await withTimeout(terminated, DEBUG_TIMEOUT_MS, 'debug session did not terminate');
}

function withTimeout<T>(promise: Promise<T>, ms: number, message: string): Promise<T> {
    let timer: NodeJS.Timeout;
    const timeout = new Promise<never>((_, reject) => {
        timer = setTimeout(() => reject(new Error(message)), ms);
    });
    return Promise.race([promise, timeout]).finally(() => clearTimeout(timer));
}
