# Recommended tools

Each row names the `hk` step and the tool that the step runs.
Take the step from `nnutter/hk-config` when it has one, then from hk's own builtins, and add a custom step only when neither fits.
Install the tool with `mise`; the step only supplies the command, the file patterns, and the fix command.

Install from a published release when one covers macOS and Linux on arm64 and amd64, such as `github:nnutter/constable`.
The `go:` backend compiles the tool on every machine and every CI run, so use it only for a tool that publishes no release for both platforms.

## Go

| Step | Source | Tool | Notes |
| --- | --- | --- | --- |
| `go_imports` | hk-config | `goimports` | Groups this module's own packages as a separate import group. |
| `go_fumpt` | hk | `gofumpt` | Runs before the steps that need formatted code. |
| `go_fix` | hk | `go fix` | Needs Go 1.26 or later. |
| `gomod_tidy` | hk | `go mod tidy` | Runs in the module workspace and stages `go.mod` and `go.sum`. |
| `go_vet` | hk | `go vet` |  |
| `staticcheck` | hk | `staticcheck` |  |
| `errcheck` | hk | `errcheck` |  |
| `go_sec` | hk-config | `gosec` | High-severity findings only. |
| `go_vuln_check` | hk | `govulncheck` |  |
| `nilaway` | hk-config | `nilaway` | Checks this module's packages only. |
| `constable` | hk-config | `constable` | Non-mutating contracts, complexity, and predicates. |
| `go_check_sumtype` | hk-config | `go-check-sumtype` | Requires an exhaustive switch over a sum type. |
| `testifylint` | hk-config | `testifylint` | Install `github.com/nnutter/testifylint` with the `go:` backend; the 1.6 release cannot load packages from a current Go toolchain and it publishes no binary release. |
| `gohawk` | hk-config | `gohawk` | Optional: resource lifetime and concurrency bugs. |
| `golangci_lint` | hk | `golangci-lint` | Use when 1 run must cover many analyzers. |

## Markdown, YAML, TOML, Pkl, and shell

| Step | Source | Tool | Notes |
| --- | --- | --- | --- |
| `mdlint` | hk-config | `mdlint` | Install `github:nnutter/mdlint`. |
| `skills_ref` | hk-config | `agentskills` | Use only when the repository contains skills. Validates the front matter of each `SKILL.md` and needs `pypi:agentskills-tools`. |
| `yamlfmt` | hk | `yamlfmt` | Formats YAML, including workflows. |
| `tombi_format`, `tombi` | hk | `tombi` | Formats, then lints, TOML. |
| `pkl_format`, `pkl` | hk | `pkl` | Formats, then evaluates, Pkl. |
| `shellcheck` | hk | `shellcheck` | Give it `glob = "**/*.sh"` and `match_any = null`. |
| `shfmt` | hk | `shfmt` | Optional: shell formatting. |

## Python

| Step | Source | Tool | Notes |
| --- | --- | --- | --- |
| `ruff_format`, `ruff` | hk | `ruff` | Formats, then lints. |
| `ty` | hk | `ty` | Type checks. |

Install the project environment with `uv`, and run the tests through it.

## GitHub Actions

| Step | Source | Tool | Notes |
| --- | --- | --- | --- |
| `jactionlint` | hk | `jactionlint` | Lints workflows. |
| `actionlint` | hk | `actionlint` | Alternative to `jactionlint`. |

## Every file

| Step | Source | Tool | Notes |
| --- | --- | --- | --- |
| `gitleaks` | hk | `gitleaks` | The `pre-commit` hook needs the staged scan that also reads binary bytes. |
| `newlines` | hk | `hk util end-of-file-fixer` |  |
| `trailing_whitespace` | hk | `hk util trailing-whitespace` |  |
| `typos` | hk | `typos` | Optional: spelling. |

## Other languages and formats

Use these only when the repository already uses the language or format.

| Language or format | Steps |
| --- | --- |
| Dockerfile | `hadolint` |
| JavaScript, TypeScript | `biome`, `prettier`, `eslint`, `tsc` |
| Kotlin, Java | `ktlint`, `google_java_format` |
| Ruby | `rubocop` |
| Rust | `rustfmt`, `cargo_check`, `cargo_clippy`, `cargo_deny` |
| Terraform, OpenTofu | `terraform_validate`, `tf_lint`, `tofu_validate` |
