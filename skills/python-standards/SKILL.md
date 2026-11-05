---
name: python-standards
description: Apply these standards when writing Python code.
---

# Python Standards

## General Coding

- Use tabs for indentation.
- Use the `functools` module from the Python standard library.
- Use `polars` instead of `pandas`.
- Always use type hints.
- Prefer the `|` operator over `Union`.
- Prefer `| None` over `Optional`.

## Package-specific Skills

- Use `py-dataclasses` for guidance about Python data classes.
- Use `py-collections` for guidance about Python collections.
- Use `py-requests` for guidance about HTTP requests.
- Use `py-pendulum` for guidance about date and time handling.
- Use `py-argparse` for guidance about Python command-line interfaces.

## Testing

- Use `pytest` for tests.

## Tooling

- If you need a CLI tool, first see if the project uses `mise`.
- If the project uses `mise`, install the tool with `mise`.
- If the project uses `uv`, run commands with `uv` so that the tools and dependencies are correct.
- If the project uses `invoke`, run format, lint, and test tasks with `invoke`.
