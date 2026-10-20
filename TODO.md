# TODO

- [x] **End-to-end check in VS Code**: run a real launch session (ideally automated with `@vscode/test-electron`) and confirm shapes show in the Variables view.
- [x] **`envFile` PYTHONPATH**: verify that a `PYTHONPATH` set in `.env` survives alongside the injected plugin path, rather than being overwritten.
- [x] **Demo GIF** for the README and Marketplace page (before/after, ~10 s).
- [x] **Marketplace publisher**: `provaznik` created at <https://marketplace.visualstudio.com/manage>.
- [ ] **Marketplace auth for CI** (Microsoft Entra ID; global Azure DevOps PATs stop working on 2026-12-01). No Azure subscription or Azure DevOps organization needed:
    1. Azure portal → Microsoft Entra ID → App registrations → New registration (`dims-publisher`, single tenant).
    2. Certificates & secrets → Federated credentials → *GitHub Actions deploying Azure resources*: org `marekprovaznik`, repo `dims`, entity *Branch* `master`.
    3. Get the app's Azure DevOps profile ID with a temporary client secret (delete it afterwards): token from `https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token` with scope `499b84ac-1321-427f-aa17-267ca6975798/.default`, then `GET https://app.vssps.visualstudio.com/_apis/profile/profiles/me`; the `id` field is what the Marketplace accepts (not the client or object ID).
    4. Marketplace → publisher `provaznik` → Members → Add that `id` as *Contributor*.
    5. GitHub → Settings → Secrets and variables → Actions → *Variables* (not Secrets): `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`.
- [ ] **Open VSX token for CI**: namespace `provaznik` claimed (EclipseFdn/open-vsx.org#14392) and 0.1.5 published. Remaining: generate a token at <https://open-vsx.org/user-settings/tokens> and store it as the `OVSX_PAT` repo *secret*.
- [ ] **Verify CI publishing** with the next version bump: the release run must show both publish steps executed (they are skipped silently when the variables/secret are missing), and both stores must list the new version.
- [x] **Publish from CI**: `release.yml` publishes to the Marketplace when the `AZURE_CLIENT_ID` / `AZURE_TENANT_ID` repo variables exist and to Open VSX when the `OVSX_PAT` secret exists.
- [x] Retire `/fix-dims` and the manual debugpy patch once dims is installed from the Marketplace.
- [ ] **Promotion**: short posts with the before/after screenshot on r/vscode, r/Python, r/MachineLearning (Project flair) and r/learnmachinelearning; consider a Show HN. Track Marketplace *installs* (not Open VSX downloads, which are mostly crawlers) before and after.
