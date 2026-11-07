---
name: go-template
description: Set up or adopt the Go repository tooling baseline, mise tasks, Git hooks, and GitHub CI. Use when creating a Go repository or bringing an existing one onto this baseline. Configure Homebrew publishing only when requested.
---

# Go repository tooling

Use this skill to apply the repository tooling baseline.
This skill does not define Go package or application defaults.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when, and only when, they appear in all capitals, as shown here.

[RFC2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC8174]: https://www.rfc-editor.org/rfc/rfc8174

## Workflow

1. Inspect the target repository, its instructions, existing configuration, and working tree.
   Identify conflicts before changing files.
   Preserve unrelated changes and merge the baseline into existing files rather than overwriting them.
1. Determine the module path and minimum Go version from the project or ask the user.
   Do not replace an existing module path or Go version without approval.
   Determine whether Homebrew publishing is requested.
1. Read the relevant files in `references/` relative to this skill.
   Adapt their project-specific values and merge their configurations into the target.
   Do not leave template directives or unresolved placeholders in the target.
1. Remove the `git-tpl` template layer.
   Delete `.config/git.tpl.toml` and every task that runs `git tpl`, such as a template refresh task.
   Do not add a template remote or create `refs/tpl` merges.
1. Configure the required tools, tasks, hooks, and CI below.
1. Install or resolve dependencies as appropriate, then verify the result.
   Report any blocked setup or failed check and its cause.

If a required reference is unavailable, the agent MUST report the missing file and MUST NOT claim that the baseline is complete.

## Tool versions

Every development tool MUST use `latest`, except `hk`.
A repository whose own code is Python MAY pin `python` and `uv`, because the supported range belongs to that code.
When Python only runs repository scripts, `python` MUST use `latest`.
`hk` MUST be pinned, because `hk.pkl` imports an exact hk release and the step types of 2 releases do not match.
The `hk-config` package that `hk.pkl` amends MUST target the `hk` pin in `mise.toml`:

- its version is `<hk-version>-<revision>`, such as `v2.11.1-6/hk-config@2.11.1-6`, and `<hk-version>` MUST equal the pin;
- a config that also imports hk's own builtins MUST import `v<hk-version>/hk@<hk-version>`, such as `v2.11.1/hk@2.11.1`.

The agent MUST take the highest revision that is released for the pinned hk version, because each revision adds builtins and hook templates for that release.

The agent MUST run `mise upgrade` after it writes the pins.
The agent MUST track `mise.lock`, which records the release that each `latest` pin resolved to, so a run has the same versions on every machine and in CI.
The agent MUST run `mise lock` after it changes a pin and MUST NOT add the lock file to `.gitignore`.
A lock entry for a Python tool points at a sidecar directory under `.mise/locks/`, so the agent MUST track that directory and MAY ignore the rest of `.mise/`; a checkout without the sidecar cannot install the tool.
A repository that installs a Python tool MUST also install `uv`, because the `pypi` backend builds the lock with it and a host without a recent `uv` fails the install.
`mise install` keeps an existing `latest` installation and does not refresh it, so a stale installation can run an older tool than the pin names.
`hk` runs its steps in the environment that `mise` provides, so use the `mise` tasks such as `mise run fix` and `mise run check`.
A bare `hk` command runs whatever tools the shell resolves, which is not necessarily the pinned ones.

## Required baseline

The agent MUST configure `mise` to install the required tools and `hk` to run formatters and linters.
The agent MUST install a tool from its published release with the `github:` backend when that release covers Linux and macOS on both amd64 and arm64, because the `go:` backend compiles the tool on every machine and every CI run.
`github:nnutter/constable` is such a tool.
A released binary is built with one Go toolchain and reads the build artifacts of that toolchain, so the agent MUST run the binary of a Go analyzer before it prefers the binary over the compile: gohawk v0.7.2 was built with Go 1.27.0, so it panics on a module that Go 1.27.3 compiles.
The agent MUST keep the `go:` backend for a tool whose binary cannot read the code, and MUST record the reason in `mise.toml`.
When the repository contains skills, the agent MUST name the `agentskills` group, which supplies the `skills_ref` step, and MUST install its `agentskills` command from `pypi:agentskills-tools`.
The agent MUST use suitable `hk` built-ins when available and MUST use custom `hk` steps for the remaining required tools.
`hk` supersedes `lefthook` as the hook manager, and the baseline MUST NOT add `lefthook`.
`hk` installs config-based Git hooks on Git 2.54 or later and writes script shims on an older Git.
Both work, but the Git version then picks the mechanism on each machine.
When a repository needs the same mechanism everywhere, the agent SHOULD install Git through `mise` with `conda:git`, a prebuilt package of about 260 MB that every repository on the machine shares.
The `commit-msg` hook MUST run `timber review commit-msg`, which `Hooks.all` supplies as its `change-id` step.
That hook supersedes the `git-review commit-msg` hook, and every `github.com/nnutter` repository uses it.
Use `references/mise.toml` and `references/hk.pkl` as the configuration references.
`references/hk.pkl` builds every hook with `Hooks.all` from `hk-config`, and that template owns the step order:

- in a hook that fixes, the steps that rewrite files run in the order their edits must land;
- every step that only reads waits for the last fixer and for no other reader, so the readers run together;
- the check hook sets no order, so every step runs at once.

The agent MUST pass the groups that the repository needs, and MUST NOT list the steps of a group itself.
Use `go` for Go; `toml`, `yaml`, `json`, `shell`, `python`, `rust`, and `buf` for their languages and formats; `ts-backend` and `ts-frontend` for TypeScript; and `agentskills` for skill front matter.
The agent MUST NOT write `depends` for a step that the template supplies.
A step that the agent replaces or adds is its own step, so the agent MUST set that step's `depends` to keep its place in the order.

The agent MUST treat the fix hook as a superset of the check hook.
By the definition in `hk-config`, `hk fix` runs every step that `hk check` runs and also applies the fix that each step offers, so a local run starts with `mise run fix`.
`mise run check` reports what no fix can change, and it is the read-only run for CI.

The `mise` tasks MUST use the `fix`, `check`, and `test` names.
The `fix` and `check` tasks MUST delegate to `hk`, so that `hk.pkl` is the only place that names a tool, a command, or a file pattern.

- Configure the recommended tool for each language and format in `references/tools.md`.
- Configure the hooks from `Hooks.all` in the same reference, with the groups that the repository needs.
- Preserve the existing `testifylint`, `go-check-sumtype`, `errcheck`, `constable`, `betterleaks`, `nilaway`, Markdown linting, and Change-Id capabilities.
- Configure GitHub CI from `references/.github/workflows/ci.yaml` and run the same checks in CI as in the local workflow.
  Preserve its least-privilege permissions.
  Pin each action to a full commit SHA and keep its release tag in a comment.
  The tag MUST be the latest release of that action that is at least 24 hours old.
  The agent MUST confirm the tag, its date, and its SHA in the action's GitHub repository, and MUST NOT pin a release published within 24 hours.
  Run `scripts/pin-action OWNER/REPO` to get the pin; it applies the 24-hour rule and reports a newer version that it skipped.
- Configure the release workflow from `references/.github/workflows/release.yaml` when the repository is a Go application.
  A `v*` tag MUST build macOS and Linux binaries for arm64 and amd64 and attach them to the GitHub release.
  A Go library MUST NOT add the release workflow.

A custom step MUST carry a comment that states why no built-in fits.
If a built-in needs a different command in more than 1 repository, the agent SHOULD add the built-in to `hk-config` instead of copying the override.

The agent MUST preserve tests, coverage, setup, and the `on-start` and `on-stop` hooks.
The pre-commit hook MUST scan the staged files for secrets.
For an existing repository, adapt commands to its structure without removing these capabilities.
hk's `go_fix` and `gomod_tidy` steps run at the module workspace, so a fix of 1 Go file can rewrite other files in that module.
The `pre-commit` hook therefore stashes unstaged changes.
The agent MUST inspect the diff after a fix instead of assuming that it touches only the named files.
The `go-fix` built-in requires Go 1.26 or later; use a compatible toolchain without silently changing an existing module's minimum Go version.

## Git hook migration

Before installing `hk`, the agent MUST inspect the effective hooks directory and any configured `core.hooksPath`:

```sh
git config --show-origin --show-scope --get-all core.hooksPath
git config --show-origin --show-scope --get-regexp '^hook\.'
git rev-parse --git-path hooks
```

The first 2 commands can exit with status 1 when no matching configuration exists.
Inspect active hooks, symlinks and their targets, and repository configuration and dependencies for existing managers such as Lefthook, Husky, pre-commit, and `hk`.
The agent MUST identify existing hook behavior and preserve nonduplicate behavior in `hk` before removing its previous implementation.
The agent MUST treat hooks as duplicates only when their behavior is demonstrably equivalent.
If equivalence or preservation is uncertain, the agent MUST ask the user before removing either implementation.
The agent MUST obtain approval before removing or replacing hooks or uninstalling a hook manager.

For each manager to remove, consult the uninstall instructions for the installed version and inspect their effects before running them.
For Lefthook, consult `lefthook uninstall --help` or its documentation and use its documented uninstall process after approval.
`hk migrate pre-commit` reads a pre-commit or prek configuration, so inspect its output instead of trusting it.
Do not assume a manager's uninstall command affects only its own files or handles every hooks directory.
After uninstalling, inspect the effective hooks directory again, resolve remaining conflicts, install `hk`, and verify that the preserved behavior runs.
A `git-review commit-msg` hook MUST become the `timber` hook, and the agent MUST remove the `git-review` dependency when nothing else uses it.
Report any behavior that could not be preserved.

## Conditional Homebrew publishing

If the user requests Homebrew publishing, the agent MUST configure `.github/workflows/update-tap.yaml` from `references/.github/workflows/update-tap.yaml` using the agreed formula name, tap owner, and tap repository.
The agent MUST identify the required GitHub App client ID and private key, tap access, existing formula, and `bin/update-formula` dependency.
The agent MUST report any unmet prerequisite rather than claim publishing is ready.
Preserve GitHub Actions expressions when adapting the reference.

If Homebrew publishing is not requested, the agent MUST NOT add the publishing workflow.
The agent MUST NOT remove an existing publishing workflow without approval.

## Verification

For a repository with Go packages, run `mise upgrade`, `mise run setup`, `mise run fix`, `mise run test`, `mise run check`, and `mise run ci-test` when their prerequisites are available. `mise run setup` changes Git hooks; follow the Git hook migration procedure before running it.
`mise run fix` is a superset of `mise run check`, so read its output for the problems that no fix can change, and use `mise run check` for the read-only result.
Inspect changes produced by fix tasks.
If the repository has no Go packages or a required tool or service is unavailable, report the commands not run and why.
Do not claim CI or Homebrew publishing has been verified without exercising it.
