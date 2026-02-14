import * as vscode from 'vscode';
import * as path from 'path';

/**
 * dims - Display array shapes in the debug variables view
 *
 * Architecture:
 * 1. This extension registers a DebugConfigurationProvider for debugpy/python
 * 2. On each debug session start, resolveDebugConfiguration injects our
 *    bundled pydevd plugin directory into PYTHONPATH
 * 3. debugpy's pydevd discovers our plugin via namespace packages
 * 4. The plugin's StrPresentationProvider prepends shape info to variable display
 *
 * The actual shape logic lives in python/pydevd_plugins/extensions/types/
 */

const SUPPORTED_DEBUG_TYPES = ['debugpy', 'python'];

class DimsDebugConfigProvider implements vscode.DebugConfigurationProvider {
    private pluginPath: string;

    constructor(extensionPath: string) {
        // Points to the `python` dir which contains the pydevd_plugins namespace package
        this.pluginPath = path.join(extensionPath, 'python');
    }

    resolveDebugConfiguration(
        _folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
        _token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration> {

        const enabled = vscode.workspace.getConfiguration('dims').get<boolean>('enabled', true);
        if (!enabled) {
            return config;
        }

        // Only inject for Python debug sessions
        if (!config.type || !SUPPORTED_DEBUG_TYPES.includes(config.type)) {
            return config;
        }

        // Ensure env object exists
        if (!config.env) {
            config.env = {};
        }

        // Inject our plugin path into PYTHONPATH
        // Respect existing PYTHONPATH — prepend ours with platform separator
        const sep = process.platform === 'win32' ? ';' : ':';
        const existing = config.env['PYTHONPATH'] || '';

        if (existing) {
            // Don't double-inject
            if (!existing.includes(this.pluginPath)) {
                config.env['PYTHONPATH'] = this.pluginPath + sep + existing;
            }
        } else {
            config.env['PYTHONPATH'] = this.pluginPath;
        }

        return config;
    }

    resolveDebugConfigurationWithSubstitutedVariables(
        _folder: vscode.WorkspaceFolder | undefined,
        config: vscode.DebugConfiguration,
        _token?: vscode.CancellationToken
    ): vscode.ProviderResult<vscode.DebugConfiguration> {
        // Second pass: handle case where PYTHONPATH was set via variable substitution
        // e.g. "${env:PYTHONPATH}" which wouldn't be available in first pass
        const enabled = vscode.workspace.getConfiguration('dims').get<boolean>('enabled', true);
        if (!enabled || !config.type || !SUPPORTED_DEBUG_TYPES.includes(config.type)) {
            return config;
        }

        if (!config.env) {
            config.env = {};
        }

        const sep = process.platform === 'win32' ? ';' : ':';
        const existing = config.env['PYTHONPATH'] || '';

        if (!existing.includes(this.pluginPath)) {
            config.env['PYTHONPATH'] = existing
                ? this.pluginPath + sep + existing
                : this.pluginPath;
        }

        return config;
    }
}

export function activate(context: vscode.ExtensionContext) {
    const provider = new DimsDebugConfigProvider(context.extensionPath);

    for (const debugType of SUPPORTED_DEBUG_TYPES) {
        context.subscriptions.push(
            vscode.debug.registerDebugConfigurationProvider(debugType, provider)
        );
    }

    // Log activation for debugging
    const outputChannel = vscode.window.createOutputChannel('dims');
    outputChannel.appendLine(`dims activated. Plugin path: ${path.join(context.extensionPath, 'python')}`);
    context.subscriptions.push(outputChannel);
}

export function deactivate() {}
