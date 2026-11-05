---
name: go-cli
description: Start or review a Go command-line application with the standard stack - Cobra for commands, Fang as the execution entry point, pflag for flags, and Charm libraries for logging, styling, and terminal UI. Use when creating a new Go CLI, adding subcommands, or wiring a CLI client to a server.
---

# Go CLI Standard Stack

Use this skill to start a Go command-line application or to check one.
Use the keywords MUST, SHOULD, and MAY as defined in RFC 2119.
Only packages specific to a CLI are covered.

## Stack

| Concern | Choice | Level |
| --- | --- | --- |
| Language | Go, latest stable version | MUST |
| Command framework | `github.com/spf13/cobra` | MUST |
| Execution entry point, help, version, completions, error output | `github.com/charmbracelet/fang` | MUST |
| Flags | `github.com/spf13/pflag`, through Cobra | MUST (no second parser) |
| Application logs | Charm Log (`github.com/charmbracelet/log`) | MUST |
| Styling | Lip Gloss | MUST when the CLI emits its own output |
| Interactive terminal UI | Bubble Tea and Bubbles | MUST when the CLI has user interactions or is a full TUI |

Add Bubble Tea, Bubbles, and Lip Gloss only when the application needs interactive UI or custom styling.

## Project Layout

- SHOULD put `main` in `cmd/<app>/main.go`.
  It MUST only build the root command and call the entry point.
  `version` should be specified at build time for this package and passed into entry point.
- Give each subcommand its own Go package, for example, `internal/cmd/<app>/<sub>`.
  Keep command wiring there.
- Keep application logic out of Cobra handlers so that it can be tested without a command tree.
- Create one package per subcommand even when the command is small.
  This keeps wiring separate and makes later growth cheap.

## Cobra

- Build a root command with focused children.
- Set `Use`, `Short`, and `Args` on each command.
- Use `RunE`, not `Run`, so errors return to the caller.
- Use validators such as `cobra.NoArgs` and `cobra.ExactArgs(n)`.
- Define each flag on the narrowest command that needs it.
- Use `PersistentFlags` only when descendant commands need the flag.
- Bind a flag to a variable only when direct access is needed.
  Read flags with `cmd.Flags().GetString(...)` or a typed accessor otherwise.
- Validate flag combinations after parsing and return an error.
- Give every flag a long name, a useful default, and help text.
  Use a short name only when it is common and does not conflict.

## Fang

- Use `fang.Execute` as the only call that starts command execution.
- Build the root command first, then pass the application context.
- Let Fang provide help, version, completion, man pages, and error presentation.
  Do not replace these with custom code unless the CLI has a specific requirement.
- Return errors from commands and handle the final error once, in `main`.
  Fang prints it, `main` sets the exit status.
- Keep application logic independent of Fang so tests do not need it.
- Verify option names and signatures against the pinned Fang version before writing code.
  Fang's API has changed between releases.

## Logging and Output

- Use Charm Log for application logs.
  Write logs to stderr.
  Keep command results on stdout so that output can be piped.
- Put logs and diagnostics in one place, set up in the root command.
- Do not log an error and also return it.
  Return it, and let the top level log it once.

## Context and Shutdown

- Create a cancellable context in `main` for the process lifetime.
  Including binding to standard OS signals.
- Pass that context into every command that does I/O or long work.
- Cancel the context on interrupt.
- Do not store contexts in structs.
- Use `context.WithCancelCause` or `context.WithTimeoutCause` when the caller needs to know why work stopped.

## Errors

- Wrap errors with context when they cross a package boundary, using `fmt.Errorf("...: %w", err)`.
- Check errors with `errors.Is` and `errors.AsType[T]`.
- Use typed error values only when callers need to branch on them.

## Testing

- Test commands through the Cobra command object with set output and input buffers.
  Test application behavior through its own package.
- Use table-driven tests with a slice of a named struct.
- Use `t.Context()` in tests that need a context.
- Use `t.TempDir()` for temporary files.
- Use testify assertions when the project uses them (see the go-testify skill).
- Test the public contract of each command: arguments, flags, output, exit status, and error messages.
- If application uses Git be sure to shield tests from Git environment variables that are set during interactive rebase.

## Tooling and Process

Keep them unless the new project chooses otherwise.

- Pin tool versions in `mise.toml` (or the project's equivalent).
- Provide a `mise run linters` task that runs at least:
  - `go vet`
  - `staticcheck`
  - `golangci-lint` with the analyzers it supports
  - `nilaway`
  - `go-check-sumtype` for sealed sum types
  - `errorlint`
  - `modernize`
- Format with `gofumpt`.
- Every commit MUST pass the tests.
- Run `mise run linters` before each commit.
- Run `mise run install-hooks` in every new worktree.
- Use `//sumtype:decl` on sealed interfaces that model enums.

## Starter Checklist

1. Create the module and pin Go, Cobra, Fang, and Charm versions.
1. Add `cmd/<app>/main.go` that calls the root command and `fang.Execute`.
1. Add the root command with `Use`, `Short`, and `Version`.
1. Add one subcommand package with `RunE` and argument validation.
1. Add Charm Log to the root command and send logs to stderr.
1. Add the test for the subcommand's behavior and exit status.
1. Add `mise.toml` tasks for lint, format, test, and install-hooks.
1. Confirm `mise run linters` passes before the first commit.

## Anti-Patterns

- A second flag parser next to pflag.
- Business logic in `cmd/` packages.
- `Run` instead of `RunE`, errors are part of UX.
- Logging to stdout, breaks piping to other commands.
- Calling `os.Exit` outside `main`.
