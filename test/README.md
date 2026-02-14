# dims Tests

Automated tests for the dims VSCode extension.

## Running Tests

Install test dependencies:
```bash
pip install -r requirements.txt
```

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest test/test_dims_plugin.py
```

## Test Coverage

- **Core functionality**: NumPy arrays, Python collections (list, dict, set, tuple)
- **String exclusion**: Verifies strings don't show length (to avoid noise)
- **Exception handling**: Ensures plugin doesn't break debugger on errors
- **Optional libraries**: PyTorch and pandas tests (skipped if not installed)

## Manual Testing

For manual debugging/demo, see the `examples/` directory:
- `examples/debug_demo.py` - NumPy arrays and Python collections
- `examples/pytorch_demo.py` - PyTorch tensors

Set breakpoints in these files and debug to visually verify shape display.
