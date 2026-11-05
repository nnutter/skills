# Reference files

For a new project, copy the applicable files to the matching paths.
For an existing project, inspect its configuration and merge the applicable examples without overwriting unrelated settings or changes.
Replace these placeholders before you use the files:

- `MODULE_PATH`: the Go module path.
- `GO_VERSION`: the minimum Go version, such as `1.27.3`.
- `COPYRIGHT_YEAR`: the copyright year.
- `COPYRIGHT_HOLDER`: the copyright holder.

`hk.pkl` amends the `Config.pkl` of `nnutter/hk-config` and imports its `Hooks.pkl`, so hk's own builtins arrive through that package.
The hk-config version is the `hk` pin in `mise.toml` plus the highest revision released for it, and both package paths name that version.
`Hooks.all(List(...))` builds the check, fix, pre-commit, and commit-msg hooks from the groups that it names, and the template owns the step order: the fixers run in sequence, every reader waits for the last fixer, and the check hook runs every step at once.
Name the groups the project needs instead of listing steps.
Every other tool takes the latest release, and `mise.lock` is tracked so that a `latest` pin resolves to the same release on every machine.
Track `.mise/locks/` with it and ignore the rest of `.mise/`: a lock entry for a Python tool points at a sidecar directory there, and a checkout without it cannot install the tool.
Install `uv` when a Python tool is in the list; the pypi backend needs it to build the lock.
`references/tools.md` lists the recommended tool for each language and format, and the group that supplies its step.

Copy `.github/workflows/release.yaml` when the repository is a Go application; a library does not publish binaries and does not need it.
Replace `BINARY_PLACEHOLDER` with the binary name and `MAIN_PACKAGE_PLACEHOLDER` with the package to build, such as `.` or `./cmd/name`.
The workflow builds macOS and Linux binaries for arm64 and amd64 on a `v*` tag and publishes them with checksums.

Copy `.github/workflows/update-tap.yaml` only when the project publishes a Homebrew formula.
Replace `FORMULA_NAME_PLACEHOLDER`, `TAP_OWNER_PLACEHOLDER`, and `TAP_REPOSITORY_PLACEHOLDER` with the formula name, tap owner, and tap repository.
The tap must provide `bin/update-formula`.
Configure the `APP_CLIENT_ID` repository variable and `APP_PRIVATE_KEY` secret for a GitHub App that can write to the tap and open pull requests.

Keep GitHub Actions expressions such as `${{ github.ref }}` and hk placeholders such as `{{files}}` unchanged.
Every action is pinned to a commit SHA with its release tag in a comment; pin the latest tag that is at least 24 hours old and confirm it in the action's repository.
Run `scripts/pin-action OWNER/REPO` for the tag and SHA, and confirm the result in the action's repository.
Run `mise upgrade` to install the tools at the versions the pins name, run `mise lock` to record them, and run `go mod tidy` to resolve the project's Go dependencies.
Use `mise run fix` for the local run: by the definition in `hk-config` it is a superset of `mise run check`, because it runs the same steps and applies every fix that they offer.
Read its output for the problems that no fix can change, and use `mise run check` for the read-only run in CI.
A fix can change files across a Go module, because hk's `go fix` and `go mod tidy` steps run at the module workspace; inspect the changes before committing.
Before running `mise run setup`, follow the Git hook migration procedure in `SKILL.md`.
Inspect existing hooks and managers, preserve nonduplicate behavior, and obtain approval before removing or replacing them.
