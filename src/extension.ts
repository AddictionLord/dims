import * as path from 'path';
import * as vscode from 'vscode';

/**
 * dims - Display array shapes in the debug variables view
 *
 * Before each Python launch, the bundled `python/` directory is prepended to
 * the debuggee's PYTHONPATH. pydevd (inside debugpy) discovers
 * `python/pydevd_plugins/extensions/pydevd_plugin_dims.py` through its
 * `pydevd_plugins.extensions` namespace package and uses it to format values.
 */

const SUPPORTED_DEBUG_TYPES = ['debugpy', 'python'];

export function prependPythonPath(env: Record<string, string | null | undefined>, pluginPath: string, sep: string): void {
    const existing = env['PYTHONPATH'] ?? '';
    if (existing.split(sep).includes(pluginPath)) {
        return;
    }
    env['PYTHONPATH'] = existing ? pluginPath + sep + existing : pluginPath;
}

class DimsDebugConfigProvider implements vscode.DebugConfigurationProvider {
    constructor(private readonly pluginPath: string) {}

    resolveDebugConfigurationWithSubstitutedVariables(
        _folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
    ): vscode.ProviderResult<vscode.DebugConfiguration> {
        const enabled = vscode.workspace.getConfiguration('dims').get<boolean>('enabled', true);
        if (!enabled || !SUPPORTED_DEBUG_TYPES.includes(config.type) || config.request !== 'launch') {
            return config;
        }

        config.env = config.env ?? {};
        prependPythonPath(config.env, this.pluginPath, path.delimiter);
        return config;
    }
}

export function activate(context: vscode.ExtensionContext): void {
    const pluginPath = path.join(context.extensionPath, 'python');
    const provider = new DimsDebugConfigProvider(pluginPath);

    for (const debugType of SUPPORTED_DEBUG_TYPES) {
        context.subscriptions.push(vscode.debug.registerDebugConfigurationProvider(debugType, provider));
    }

    const outputChannel = vscode.window.createOutputChannel('dims');
    outputChannel.appendLine(`dims activated. Plugin path: ${pluginPath}`);
    context.subscriptions.push(outputChannel);
}

export function deactivate(): void {}
