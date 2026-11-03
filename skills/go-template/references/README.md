# Reference files

For a new project, copy the applicable files to the matching paths.
For an existing project, inspect its configuration and merge the applicable examples without overwriting unrelated settings or changes.
Replace these placeholders before you use the files:

- `MODULE_PATH`: the Go module path.
- `GO_VERSION`: the minimum Go version, such as `1.27.3`.
- `COPYRIGHT_YEAR`: the copyright year.
- `COPYRIGHT_HOLDER`: the copyright holder.

`hk.pkl` imports 2 packages: hk's own builtins and the extra builtins from `nnutter/hk-config`.
The hk version in both imports must equal the `hk` pin in `mise.toml`, and the `hk-config` version is that hk version plus a revision.
Every other tool takes the latest release.
`references/tools.md` lists the recommended tool for each language and format.

Copy `.github/workflows/update-tap.yaml` only when the project publishes a Homebrew formula.
Replace `FORMULA_NAME_PLACEHOLDER`, `TAP_OWNER_PLACEHOLDER`, and `TAP_REPOSITORY_PLACEHOLDER` with the formula name, tap owner, and tap repository.
The tap must provide `bin/update-formula`.
Configure the `APP_CLIENT_ID` repository variable and `APP_PRIVATE_KEY` secret for a GitHub App that can write to the tap and open pull requests.

Keep GitHub Actions expressions such as `${{ github.ref }}` and hk placeholders such as `{{files}}` unchanged.
Run `mise upgrade` to install the tools at the versions the pins name, and run `go mod tidy` to resolve the project's Go dependencies.
Use `mise run check` for non-writing checks and `mise run fix` to apply fixes.
A fix can change files across a Go module, because hk's `go fix` and `go mod tidy` steps run at the module workspace; inspect the changes before committing.
Before running `mise run setup`, follow the Git hook migration procedure in `SKILL.md`.
Inspect existing hooks and managers, preserve nonduplicate behavior, and obtain approval before removing or replacing them.
