import * as fs from 'fs';
import * as path from 'path';
import * as vscode from 'vscode';

/**
 * Drives VS Code for the README demo: debug `train.py` to a breakpoint once
 * without dims and once with it. `recordDemo.ts` captures the window and reads
 * the phase file this suite writes to know what to caption and when to stop.
 */

const HOLD_MS = 3_500;
const LAYOUT_MS = 3_000;
const RELEASE_MS = 500;
const SECONDARY_DEBUG_VIEWS = [
    'workbench.debug.watchExpressionsView',
    'workbench.debug.callStackView',
    'workbench.debug.breakPointsView',
];

export async function run(): Promise<void> {
    const workspace = vscode.workspace.workspaceFolders![0];
    const program = path.join(workspace.uri.fsPath, 'train.py');
    const phaseFile = process.env['DIMS_DEMO_PHASE_FILE']!;

    const document = await vscode.workspace.openTextDocument(program);
    await vscode.window.showTextDocument(document);
    const line = document.getText().split(/\r?\n/).findIndex((text) => text.trim().startsWith('print('));
    const location = new vscode.Location(document.uri, new vscode.Position(line, 0));
    vscode.debug.addBreakpoints([new vscode.SourceBreakpoint(location)]);

    await vscode.commands.executeCommand('vscode.moveViews', {
        viewIds: SECONDARY_DEBUG_VIEWS,
        destinationId: 'workbench.view.explorer',
    });
    await vscode.commands.executeCommand('workbench.view.debug');
    const setPhase = (phase: string) => () => fs.writeFileSync(phaseFile, phase);
    await debugAndHold(workspace, program, LAYOUT_MS, setPhase('layout'), setPhase('idle'));

    for (const enabled of [false, true]) {
        await vscode.workspace.getConfiguration('dims').update('enabled', enabled, vscode.ConfigurationTarget.Global);
        await debugAndHold(workspace, program, HOLD_MS, setPhase(enabled ? 'with dims' : 'without dims'), setPhase('idle'));
    }

    fs.writeFileSync(phaseFile, 'done');
    await vscode.workspace.getConfiguration('dims').update('enabled', undefined, vscode.ConfigurationTarget.Global);
}

async function debugAndHold(
    folder: vscode.WorkspaceFolder,
    program: string,
    holdMs: number,
    onStopped: () => void,
    onRelease: () => void,
): Promise<void> {
    const stopped = new Promise<vscode.DebugSession>((resolve) => {
        const registration = vscode.debug.registerDebugAdapterTrackerFactory('debugpy', {
            createDebugAdapterTracker: (session) => ({
                onDidSendMessage: (message) => {
                    if (message.type === 'event' && message.event === 'stopped') {
                        registration.dispose();
                        resolve(session);
                    }
                },
            }),
        });
    });

    await vscode.debug.startDebugging(folder, {
        type: 'debugpy',
        request: 'launch',
        name: 'train.py',
        program,
        python: process.env['DIMS_E2E_PYTHON'] ?? 'python3',
        console: 'internalConsole',
        justMyCode: true,
    });
    const session = await stopped;
    onStopped();
    await sleep(holdMs);
    onRelease();
    await sleep(RELEASE_MS);

    const terminated = new Promise<void>((resolve) => {
        const registration = vscode.debug.onDidTerminateDebugSession((ended) => {
            if (ended.id === session.id) {
                registration.dispose();
                resolve();
            }
        });
    });
    await vscode.debug.stopDebugging(session);
    await terminated;
}

function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
