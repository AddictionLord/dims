import * as cp from 'child_process';
import * as path from 'path';
import { downloadAndUnzipVSCode, resolveCliArgsFromVSCodeExecutablePath, runTests } from '@vscode/test-electron';

/**
 * Downloads VS Code, installs the Python Debugger extension into the isolated
 * test profile and runs the suite in `suite/` against `src/test/fixture`.
 */

const PYTHON_DEBUGGER_EXTENSION = 'ms-python.debugpy';

async function main(): Promise<void> {
    const extensionDevelopmentPath = path.resolve(__dirname, '../../');
    const extensionTestsPath = path.resolve(__dirname, './suite/index');
    const workspacePath = path.resolve(extensionDevelopmentPath, 'src/test/fixture');

    const vscodeExecutablePath = await downloadAndUnzipVSCode(process.env['DIMS_E2E_VSCODE_VERSION'] ?? 'stable');
    const [cli, ...cliArgs] = resolveCliArgsFromVSCodeExecutablePath(vscodeExecutablePath);
    const install = cp.spawnSync(cli, [...cliArgs, '--install-extension', PYTHON_DEBUGGER_EXTENSION], {
        encoding: 'utf-8',
        stdio: 'inherit',
        shell: process.platform === 'win32',
    });
    if (install.status !== 0) {
        throw new Error(`Failed to install ${PYTHON_DEBUGGER_EXTENSION}`);
    }

    await runTests({
        vscodeExecutablePath,
        extensionDevelopmentPath,
        extensionTestsPath,
        launchArgs: [workspacePath, '--disable-workspace-trust'],
    });
}

main().catch((err) => {
    console.error(err);
    process.exit(1);
});
