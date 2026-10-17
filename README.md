# dims

See array shapes instantly in the debug variables view.

## Before → After

**Before:** You see `tensor([[0., 0., 0.], ...` and have to type `.shape` in the console.

**After:** You see `{[2, 3]}, tensor([[0., 0., 0.], ...` — the shape is right there.

```
# Before dims
n = array([[0., 0., 0.], [0., 0., 0.]])
t = tensor([[0., 0., 0.], [0., 0., 0.]])
l = [1, 2, 3]

# After dims
n = {[2, 3]}, array([[0., 0., 0.], [0., 0., 0.]])
t = {[2, 3]}, tensor([[0., 0., 0.], [0., 0., 0.]])
l = {3}, [1, 2, 3]
```

Works with **NumPy**, **PyTorch**, **TensorFlow**, **pandas**, and any object with a `.shape` attribute or `len()`.

## Install

1. Install from the [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=addictionlord.dims)
2. Start debugging Python — shapes appear automatically

No configuration needed. Just install and debug.

## How it works

dims uses debugpy's official [pydevd extension plugin API](https://github.com/microsoft/debugpy/tree/main/src/debugpy/_vendored/pydevd/pydevd_plugins/extensions) to customize variable display at the debugger level. When you launch a Python debug session, dims prepends its bundled `python/` directory to the debuggee's `PYTHONPATH`; pydevd discovers `pydevd_plugins/extensions/pydevd_plugin_dims.py` there. The plugin:

1. Handles objects implementing `collections.abc.Sized`, except `str`, `bytes` and `bytearray`
2. For objects with `.shape` (arrays, tensors, DataFrames): prepends `{[dim1, dim2, ...]}`
3. For other sized objects (lists, dicts, sets): prepends `{length}`
4. Renders the value with pydevd's own size-bounded `SafeRepr`, so a 5M-element list stays cheap
5. Wraps debugpy's bundled pandas presenters so DataFrames and Series get a shape too

*Copy Value* yields the plain value, without the prefix. Attach sessions are not covered: the plugin can only be injected into processes the debugger launches.

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `dims.enabled` | `true` | Enable/disable shape display |

## Supported types

| Type | Display | Example |
|------|---------|---------|
| NumPy ndarray | Shape | `{[2, 3]}, array(...)` |
| PyTorch Tensor | Shape | `{[2, 3]}, tensor(...)` |
| TensorFlow Tensor | Shape | `{[2, 3]}, tf.Tensor(...)` |
| pandas DataFrame / Series | Shape | `{[100, 5]}, ...` |
| list | Length | `{3}, [1, 2, 3]` |
| dict | Length | `{2}, {1: 2, 3: 4}` |
| set | Length | `{3}, {1, 2, 3}` |
| tuple | Length | `{3}, (1, 2, 3)` |
| str, bytes | Unchanged | `'hello'` |

## Requirements

- VSCode 1.85+
- Python Debugger extension (debugpy)

## Development

```bash
npm install && npm run compile && npx vsce package
pip install -r requirements-dev.txt && python -m pytest tests
```

## License

MIT
