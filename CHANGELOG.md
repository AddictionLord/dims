# Changelog

## 0.1.0 (2026-10-17)

- First buildable release: VS Code extension + pydevd plugin.
- Shapes for `.shape` objects, lengths for sized containers; `str`/`bytes` unchanged.
- Values rendered through pydevd's `SafeRepr` (bounded on huge objects).
- Shapes on pandas DataFrame/Series via debugpy's bundled presenters.
- Copy Value returns the plain value.
