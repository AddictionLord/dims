# TODO

- [x] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [x] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [x] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [x] **Marketplace publisher**: `provaznik` created at <https://marketplace.visualstudio.com/manage>.
- [ ] **Marketplace auth for CI** (Microsoft Entra ID; global Azure DevOps PATs stop working on 2026-12-01):
    1. Azure portal → Entra ID → App registrations → New registration (`dims-publisher`).
    2. Certificates & secrets → Federated credentials → GitHub Actions: org `marekprovaznik`, repo `dims`, entity *Branch* `master`.
    3. Sign in to <https://dev.azure.com> once with the same tenant so the service principal gets an Azure DevOps identity, then add it as a *Contributor* member of publisher `provaznik` (Marketplace → Members).
    4. GitHub → Settings → Secrets and variables → Actions → *Variables*: `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.
- [ ] **Open VSX** (Cursor, Windsurf, VSCodium): log in at <https://open-vsx.org> with GitHub, sign the Eclipse publisher agreement, create a token, run `npx ovsx create-namespace provaznik -p <token>`, store the token as the `OVSX_PAT` repo secret. The next version bump publishes there automatically; for 0.1.4 run `npx ovsx publish dims-0.1.4.vsix -p <token>` once.
- [x] **Publish from CI**: `release.yml` publishes to the Marketplace when the `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables exist and to Open VSX when the `OVSX_PAT` secret exists.
- [x] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
