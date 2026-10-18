# TODO

- [x] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [ ] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [ ] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [x] **Marketplace publisher**: `provaznik` created at <https://marketplace.visualstudio.com/manage>.
- [ ] **Marketplace auth for CI**: use Microsoft Entra ID (GitHub OIDC federated credential + `vsce publish --azure-credential`) instead of a `VSCE_PAT` secret; global Azure DevOps PATs stop working on 2026-12-01.
- [ ] **Open VSX** (Cursor, Windsurf): create an account/namespace and store `OVSX_PAT`.
- [ ] **Publish from CI**: extend `.github/workflows/release.yml` with `vsce publish` / `ovsx publish` once Entra ID auth and `OVSX_PAT` exist.
- [x] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
