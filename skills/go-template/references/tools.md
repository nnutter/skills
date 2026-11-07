# Recommended tools

Each row names the `hk` step, the group that supplies it, and the tool that the step runs.
`Hooks.all` in `nnutter/hk-config` adds the steps of every group it is given and orders them, so a project config names groups and no steps.
Take a step from a group first, then from hk's own builtins, and add a custom step only when neither fits.
When more than 1 repository needs the same custom step, add it to `hk-config` instead.
Install the tool with `mise`; the step only supplies the command, the file patterns, and the fix command.

Install a tool from its published release with the `github:` backend when that release covers Linux and macOS on both amd64 and arm64, because the `go:` backend compiles the tool on every machine and every CI run.
`github:nnutter/constable` is such a tool, and a new tool SHOULD join it.

A Go analyzer reads the build artifacts of the toolchain that compiles the module, so its binary must be built with a Go at least as new as the repository's.
`gohawk` v0.7.2 was built with Go 1.27.0 and panics on a module that Go 1.27.3 compiles, and `testifylint` v0.0.1 was built with Go 1.26 and cannot analyze such a module.
These tools therefore keep the `go:` backend: `gohawk`, `testifylint`, and `errcheck`, `nilaway`, `goimports`, and `govulncheck`, which publish no release for both platforms.

`default` is a step that every hook runs, so no group adds it.
Add the group of each language and format that the repository contains.

## Go

| Step | Group | Tool | Notes |
| --- | --- | --- | --- |
| `go_imports` | go | `goimports` | Groups this module's own packages as a separate import group. |
| `go_fumpt` | go | `gofumpt` | Runs before the steps that need formatted code. |
| `go_fix` | go | `go fix` | Needs Go 1.26 or later. |
| `testifylint` | go | `testifylint` |  |
| `constable` | go | `constable` | Contracts, method order, complexity, and predicates. |
| `gomod_tidy` | go | `go mod tidy` | Runs in the module workspace and stages `go.mod` and `go.sum`. |
| `go_vet` | go | `go vet` |  |
| `staticcheck` | go | `staticcheck` |  |
| `go_vuln_check` | go | `govulncheck` |  |
| `err_check` | go | `errcheck` |  |
| `go_check_sumtype` | go | `go-check-sumtype` | Requires an exhaustive switch over a sum type. |
| `nilaway` | go | `nilaway` | Checks this module's packages only. |
| `go_sec` | go | `gosec` | High-severity findings only. |
| `gohawk` | go | `gohawk` | Resource lifetime and concurrency bugs. |
| `golangci_lint` | none | `golangci-lint` | Custom step. Use when 1 run must cover many analyzers. |

## Markdown, YAML, TOML, Pkl, and shell

| Step | Group | Tool | Notes |
| --- | --- | --- | --- |
| `mdlint` | default | `mdlint` | Install `github:nnutter/mdlint`. |
| `yamlfmt` | yaml | `yamlfmt` | Formats YAML, including workflows. |
| `tombi_format`, `tombi` | toml | `tombi` | Formats, then lints, TOML. |
| `pkl_format`, `pkl` | default | `pkl` | Formats, then evaluates, Pkl. |
| `shellcheck` | shell | `shellcheck` |  |
| `shfmt` | shell | `shfmt` | Formats shell. |
| `skills_ref` | agentskills | `agentskills` | Validates the front matter of each `SKILL.md` and needs `pypi:agentskills-tools`. |

## Python

| Step | Group | Tool | Notes |
| --- | --- | --- | --- |
| `ruff_format`, `ruff` | python | `ruff` | Formats, then lints. |
| `ty` | python | `ty` | Type checks. |

Install the project environment with `uv`, and run the tests through it.

`conda:git` exports `CONDA_PREFIX` to every child process, and a Python tool then looks for `site-packages` inside the Git package, which fails the step.
A repository that installs Git with `conda:git` and also runs Python tools MUST remove the variable in `[env]`, unless it has a conda environment:

```toml
[env]
CONDA_PREFIX = false
```

## GitHub Actions

| Step | Group | Tool | Notes |
| --- | --- | --- | --- |
| `jactionlint` | default | `jactionlint` | A maintained `actionlint` fork. It also reads composite actions and Dependabot configuration, and it rewrites a workflow in the hooks that fix. The step skips a repository that has no workflow. |

## Every file

| Step | Group | Tool | Notes |
| --- | --- | --- | --- |
| `betterleaks` | default | `betterleaks` | The step scans the files the hook selects, so `pre-commit` scans the staged files and every other hook scans the worktree. |
| `mise` | default | `mise` | Checks the format of the `mise` configuration. |
| `newlines` | default | `hk util end-of-file-fixer` |  |
| `trailing_whitespace` | default | `hk util trailing-whitespace` |  |
| `typos` | none | `typos` | Custom step. Spelling. |

`betterleaks` is the maintained successor to `gitleaks`, from the same authors.
It loads `.gitleaks.toml` only with `--unsafe-auto-load-config`, and the builtin of hk does not set the flag, so a repository with that file sets the flag in its own step.

## Other languages and formats

Use these only when the repository already uses the language or format.

| Language or format | Steps |
| --- | --- |
| Dockerfile | `hadolint` |
| JavaScript, TypeScript | `oxfmt` and `ox_lint` in `ts-backend` or `ts-frontend`, `tsc` in `ts-backend`, `oxfmt` in `json` |
| Kotlin, Java | `ktlint`, `google_java_format` |
| Ruby | `rubocop` |
| Rust | `cargo_fmt`, `cargo_check`, and `cargo_clippy` in `rust`, `cargo_deny` |
| Terraform, OpenTofu | `terraform_validate`, `tf_lint`, `tofu_validate` |
