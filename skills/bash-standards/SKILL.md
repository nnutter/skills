---
name: bash-standards
description: >-
  Apply Bash scripting standards and ShellCheck linting.
  Use when writing or reviewing Bash scripts or adding Git-based option parsing.
---

# Bash Standards

## Scope and compatibility

- Use Bash for scripts that require Bash features.
- Start executable Bash scripts with `#!/usr/bin/env bash`.
- If compatibility affects the implementation, document the minimum supported Bash version.
- If the project has a style, preserve it.
- Otherwise, indent with two spaces.

## Script structure

- Enable strict error handling near the start of an executable script.

  ```bash
  set -euo pipefail
  ```

- Do not depend on `set -e` to handle an expected failure.

- Put a command that can fail normally in an `if` condition or handle its status explicitly.

- Define focused functions before the top-level flow.

- Put the top-level flow in `main` for a nontrivial executable script.

- Pass all command arguments to `main` without changing their boundaries.

  ```bash
  main() {
    run_task "$@"
  }
  main "$@"
  ```

- Do not call `main` from a file that other scripts source.

- A sourced file must not change the caller's state unexpectedly.

- Preserve the caller's shell options, working directory, traps, and `IFS`.

## Names and variables

- Use descriptive `lower_snake_case` names for functions and local variables.

- Use `UPPER_SNAKE_CASE` for exported variables and constants.

- Declare function variables with `local`.

- Mark constants with `readonly`.

- Separate a declaration from a command substitution.

- A declaration must not hide the command status.

  ```bash
  capture_output() {
    local command_output
    command_output=$(run_command)
    printf '%s\n' "$command_output"
  }
  ```

- Use arrays to store multiple arguments.

- Do not store a command and its arguments in one string.

  ```bash
  create_commit() {
    local message=$1
    local -a command=(git commit --message "$message")
    "${command[@]}"
  }
  ```

## Expansions and input

- Quote variable expansions and command substitutions.
- Use arrays instead of intentional word splitting.
- Use `"$@"` to forward arguments.
- Do not use unquoted `$@` or `$*`.
- Use `[[ ... ]]` for string and file tests.
- Use `(( ... ))` for arithmetic tests and updates.
- Use `read -r` so that backslashes remain unchanged.
- Use `printf` instead of `echo` for controlled output.
- If a command supports `--`, put it before user-controlled path arguments.
- Do not parse the output of `ls`.
- Do not use `eval` to construct commands.

## Option parsing

If a script parses command options, define `OPTIONS_SPEC` and use Git's option parser.
If the script can run outside a Git work tree, set `NONGIT_OK=Yes` before the source command.
Use this source command exactly:

```bash
#shellcheck disable=1090
source "$(git --exec-path)/git-sh-setup"
```

Process the normalized arguments with a `while` and `case` statement.
Accept `--` as the end of the options.
Reject unknown options and missing required values with a nonzero status.

## Functions and command status

- Make each function perform one task.

- Return status codes from functions.

- Write result data to standard output only for an interface that uses command substitution.

- Write diagnostics to standard error.

- Preserve meaningful failures instead of replacing them with an unconditional success status.

- If failure controls the flow, use `if command; then` or `if ! command; then`.

- Use a subshell for temporary directory or environment changes.

  ```bash
  (
    cd -- "$work_directory"
    run_task
  )
  ```

## Files, cleanup, and safety

- Create temporary files and directories with `mktemp`.
- Install a trap immediately after creating a temporary resource.
- Quote paths in cleanup commands.
- Validate external input before using it in paths, commands, or arithmetic expressions.
- Use `command -v` to test whether a required command is available.
- Do not enable `set -x` by default because traces can expose secrets.
- Use a safer input method instead of command-line arguments for secrets.

## ShellCheck

- Run [ShellCheck](https://www.shellcheck.net/) on every changed Bash script.
- Pass extensionless Bash executables to ShellCheck explicitly.
- Resolve every ShellCheck finding before completion.
- Do not add broad or file-wide disables.
- Put a required disable on the smallest applicable scope.
- Keep the option-parser disable and source command exactly as specified above.

```bash
shellcheck -x -P "$(git --exec-path)" path/to/script
```

ShellCheck is static analysis, not a behavior test.
Run the script's automated tests after ShellCheck passes.
