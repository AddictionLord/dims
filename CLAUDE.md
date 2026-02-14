# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**dims** is a VSCode extension that displays array/tensor shapes inline in the debug variables view for Python. It eliminates the need to manually check `.shape` in the console during debugging sessions.

**Core mechanism:** The extension injects a pydevd plugin via PYTHONPATH during debug session initialization. The plugin uses debugpy's `StrPresentationProvider` API to prepend shape information to variable displays.

## Architecture

### Extension Flow (TypeScript)
1. **extension.ts**: Registers a `DebugConfigurationProvider` for `debugpy` and `python` debug types
2. On debug session start, `resolveDebugConfiguration()` injects the Python plugin directory into `PYTHONPATH`
3. The plugin is discovered by debugpy's pydevd via namespace packages

### Python Plugin
**pydevd_plugin_dims.py**: Implements `StrPresentationProvider` from `_pydevd_bundle.pydevd_extension_api`
- Detects objects implementing `collections.abc.Sized`
- For objects with `.shape` attribute (NumPy, PyTorch, TensorFlow): displays `{[dim1, dim2, ...]}`
- For other sized objects (list, dict, set, tuple): displays `{length}`
- Explicitly excludes strings to reduce noise

### Key Technical Details
- Plugin runs inline during variable serialization (zero overhead)
- PYTHONPATH injection happens in two phases:
  1. `resolveDebugConfiguration`: Before variable substitution
  2. `resolveDebugConfigurationWithSubstitutedVariables`: After variable substitution
- Platform-aware path separator handling (`:` for Unix, `;` for Windows)
- Graceful degradation: if plugin fails, falls back to default string representation

## Development Commands

### Build
```bash
npm run compile          # Compile TypeScript to JavaScript
npm run watch           # Watch mode for development
```

### Packaging & Publishing
```bash
npm run package         # Create .vsix package (vsce package)
npm run publish         # Publish to VSCode Marketplace (vsce publish)
```

### Linting
```bash
npm run lint            # Run ESLint on TypeScript source
```

## Project Structure

```
dims/
├── extension.ts                 # Main TypeScript extension code
├── pydevd_plugin_dims.py        # Python debugger plugin (StrPresentationProvider)
├── package.json                 # VSCode extension manifest + npm scripts
├── README.md                    # User-facing documentation
└── DIMS_PROJECT_PLAN.md         # Project planning document
```

**Note:** The actual directory structure for a published extension should be:
```
dims/
├── out/
│   └── extension.js            # Compiled TypeScript
└── python/
    └── pydevd_plugins/
        └── extensions/
            └── types/
                └── pydevd_plugin_dims.py
```

The Python plugin must be in the correct pydevd namespace package structure for discovery.

## Configuration

Extension exposes one setting:
- `dims.enabled` (boolean, default: true) - Enable/disable shape display

## Supported Types

Works with any object implementing `collections.abc.Sized`:
- **Shape display** (.shape attribute): NumPy ndarray, PyTorch Tensor, TensorFlow Tensor, pandas DataFrame
- **Length display** (no .shape): list, dict, set, tuple
- **Excluded**: str (to avoid noise)

## Development Notes

- The extension activates on `onDebugResolve:debugpy` and `onDebugResolve:python` events
- PYTHONPATH injection must not double-inject if already present
- The plugin must handle all edge cases gracefully (use try/except in `get_str()`)
- Platform differences: Windows uses `;` as path separator, Unix uses `:`

## Publishing Checklist

Before publishing to VSCode Marketplace:
1. Update version in package.json
2. Update repository URL (currently placeholder)
3. Add icon.png to images/
4. Run `npm run compile` to verify build
5. Test on all platforms (Linux, macOS, Windows)
6. Package with `npm run package`
7. Publish with `npm run publish`
