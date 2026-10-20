# Changelog

## 0.1.6 (2026-10-20)

- Fix: Set Value in the Variables and Watch views evaluated the shown dims prefix, raising `TypeError: unhashable type: 'list'` for arrays and silently replacing lists with a tuple ([#13](https://github.com/marekprovaznik/dims/issues/13)). The prefix is now stripped before pydevd evaluates the new value.
- End-to-end test for Set Value; manual *Verify publishing* workflow that checks Marketplace and Open VSX credentials without publishing.

## 0.1.5 (2026-10-18)

- README: static before/after screenshot instead of the demo GIF.

## 0.1.4 (2026-10-18)

- README: demo GIF, Marketplace badges, known limitations (attach, notebooks) with a manual workaround.
- End-to-end test covers `PYTHONPATH` from `envFile` surviving next to the plugin path.
- CI: PyTorch tests on Linux, actions on Node 24; releases publish to the Marketplace and Open VSX once credentials are configured.

## 0.1.3 (2026-10-18)

- Published on the VS Code Marketplace as `provaznik.dims`.
- End-to-end test: a real debugpy session in VS Code checks the values shown in the Variables view.

## 0.1.2 (2026-10-18)

- Marketplace publisher `provaznik`; repository moved to github.com/marekprovaznik/dims.

## 0.1.1 (2026-10-17)

- Extension icon.

## 0.1.0 (2026-10-17)

- First buildable release: VS Code extension + pydevd plugin.
- Shapes for `.shape` objects, lengths for sized containers; `str`/`bytes` unchanged.
- Values rendered through pydevd's `SafeRepr` (bounded on huge objects).
- Shapes on pandas DataFrame/Series via debugpy's bundled presenters.
- Copy Value returns the plain value.
