# TODO

- [x] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [x] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [x] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [x] **Marketplace publisher**: `provaznik` created at <https://marketplace.visualstudio.com/manage>.
- [x] **Marketplace auth for CI** (Microsoft Entra ID; global Azure DevOps PATs stop working on 2026-12-01): app registration `dims-publisher` in the personal Default Directory, federated credentials for `master`, added to publisher `provaznik` as *Contributor*, `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables set.
- [ ] **Delete the unused Entra credential** `github-dims-master-legacy`: GitHub already sends the ID-based subject (`repo:marekprovaznik@74077046/dims@1157953275:ref:refs/heads/master`, seen in the first *Verify publishing* run), which `github-dims-master` matches.
- [ ] **Open VSX token for CI**: namespace `provaznik` claimed (EclipseFdn/open-vsx.org#14392) and 0.1.5 published. Remaining: generate a token at <https://open-vsx.org/user-settings/tokens> and store it as the `OVSX_PAT` repo *secret*.
- [ ] **Verify CI publishing**: run the *Verify publishing* workflow (Actions tab) to check credentials without publishing; the Marketplace side passed on 2026-10-20. Then confirm with the next version bump: the release run must show both publish steps executed (they are skipped silently when the variables/secret are missing), and both stores must list the new version.
- [x] **Publish from CI**: `release.yml` publishes to the Marketplace when the `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables exist and to Open VSX when the `OVSX_PAT` secret exists.
- [x] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
- [ ] **Promotion**: short posts with the before/after screenshot on r/vscode, r/Python, r/MachineLearning (Project flair) and r/learnmachinelearning; consider a Show HN. Track Marketplace *installs* (not Open VSX downloads, which are mostly crawlers) before and after.
