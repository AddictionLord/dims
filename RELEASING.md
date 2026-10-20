# Releasing

Every push to `master` runs [`release.yml`](.github/workflows/release.yml). When the tag `v<version from package.json>` does not exist yet, it tags the commit, creates a GitHub release with the packaged `.vsix`, and publishes it to the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=provaznik.dims) and [Open VSX](https://open-vsx.org/extension/provaznik/dims).

## Steps

1. Bump the version (this also updates `package-lock.json`):

   ```bash
   npm version X.Y.Z --no-git-tag-version
   ```

2. Add an entry for `X.Y.Z` at the top of [`CHANGELOG.md`](CHANGELOG.md). The GitHub release notes use the whole file.
3. Merge to `master`.
4. In the *Release* run, check that both `vsce publish` and `ovsx publish` actually ran. Each one is **skipped without failing** when its credentials are missing. Then check that both store pages show the new version.

Re-running a release does not republish: the job skips when the tag already exists. Fix forward with a new version instead.

The Marketplace page shows the README packaged in the `.vsix`. README changes, badges included, reach the Marketplace only with the next release.

## Credentials

| Store | Authentication | Repository configuration |
|---|---|---|
| VS Code Marketplace | Microsoft Entra ID app with a GitHub OIDC federated credential for `master`, added to publisher `provaznik` as *Contributor* | Variables `AZURE_CLIENT_ID`, `AZURE_TENANT_ID` |
| Open VSX | Access token for namespace `provaznik` | Secret `OVSX_PAT` |

To check both without publishing, run **Actions → Verify publishing → Run workflow** ([`verify-publishing.yml`](.github/workflows/verify-publishing.yml)). The failing step names the side that is misconfigured.
