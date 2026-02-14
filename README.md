# dims

See array shapes instantly in the debug variables view.

## Before → After

**Before:** You see `tensor([[2, 3]...` and have to type `.shape` in the console.

**After:** You see `{[2, 3]}, tensor([[2, 3]...` — the shape is right there.

```
# Before dims
n: ndarray = [[1 2 3]]
t: Tensor = tensor([1, 2, 3])
l: list = [1, 2, 3]

# After dims
n: ndarray = {[2, 3]}, [[1 2 3]]
t: Tensor = {[2, 3]}, tensor([1, 2, 3])
l: list = {3}, [1, 2, 3]
```

Works with **NumPy**, **PyTorch**, **TensorFlow**, **pandas**, and any object with a `.shape` attribute or `len()`.

## Install

1. Install from the [VSCode Marketplace](https://marketplace.visualstudio.com/items?itemName=dims.dims)
2. Start debugging Python — shapes appear automatically

No configuration needed. Just install and debug.

## How it works

dims uses debugpy's official [pydevd extension plugin API](https://github.com/microsoft/debugpy/tree/main/src/debugpy/_vendored/pydevd/pydevd_plugins/extensions) to customize variable display at the debugger level. When you start a debug session, dims injects a lightweight Python plugin via `PYTHONPATH` that:

1. Detects objects implementing `collections.abc.Sized`
2. For objects with `.shape` (arrays, tensors): displays `{[dim1, dim2, ...]}`
3. For other sized objects (lists, dicts, sets): displays `{length}`
4. Excludes strings to reduce noise

The plugin adds **zero overhead** — it runs inline during variable serialization, no extra debug requests needed.

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
| pandas DataFrame | Shape | `{[100, 5]}, ...` |
| list | Length | `{3}, [1, 2, 3]` |
| dict | Length | `{2}, {1: 2, 3: 4}` |
| set | Length | `{3}, {1, 2, 3}` |
| tuple | Length | `{3}, (1, 2, 3)` |
| str | Unchanged | `"hello"` |

## Requirements

- VSCode 1.85+
- Python extension with debugpy

## License

MIT
