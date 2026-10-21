# TODO

- [x] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [x] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [x] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [x] **Marketplace publisher**: `provaznik` created at <https://marketplace.visualstudio.com/manage>.
- [x] **Marketplace auth for CI** (Microsoft Entra ID; global Azure DevOps PATs stop working on 2026-12-01): app registration `dims-publisher` in the personal Default Directory, federated credentials for `master`, added to publisher `provaznik` as *Contributor*, `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables set.
- [x] **Unused Entra credential** `github-dims-master-legacy` deleted: GitHub sends the ID-based OIDC subject, which `github-dims-master` matches.
- [x] **Open VSX token for CI**: namespace `provaznik` claimed (EclipseFdn/open-vsx.org#14392); token stored as the `OVSX_PAT` repo secret.
- [x] **CI publishing verified**: 0.1.6 was published to both stores by `release.yml` on 2026-10-20. See [RELEASING.md](RELEASING.md).
- [ ] **After 2026-11-19**: run *Verify publishing* once. The Azure free-trial subscription expires then; publishing should not depend on it, so confirm that it still works.
- [x] **Publish from CI**: `release.yml` publishes to the Marketplace when the `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables exist and to Open VSX when the `OVSX_PAT` secret exists.
- [x] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
- [ ] **Buy Me a Coffee**: create the page `buymeacoffee.com/provaznik` (handle must match the links in README, `package.json` and `.github/FUNDING.yml`) and connect Stripe before releasing 0.1.7.
- [ ] **Promotion**: short posts with the before/after screenshot on r/vscode, r/Python, r/MachineLearning (Project flair) and r/learnmachinelearning; consider a Show HN. Track Marketplace *installs* (not Open VSX downloads, which are mostly crawlers) before and after.
