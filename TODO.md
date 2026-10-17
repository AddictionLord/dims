# TODO

- [ ] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [ ] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [ ] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [ ] **Marketplace publisher**: create the `addictionlord` publisher at <https://marketplace.visualstudio.com/manage>, generate a PAT, and store it as the `VSCE_PAT` repo secret.
- [ ] **Open VSX** (Cursor, Windsurf): create an account/namespace and store `OVSX_PAT`.
- [ ] **Publish from CI**: extend `.github/workflows/release.yml` with `vsce publish` / `ovsx publish` once the tokens exist.
- [ ] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
