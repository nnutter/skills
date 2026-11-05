---
name: py-argparse
description: Apply these standards when building Python command-line interfaces with argparse.
---

# Python argparse

- Build the parser in a function so command-line configuration stays separate from application logic.
- Pass an explicit argument list to `parse_args` when code needs tests.
- Use `type`, `choices`, `required`, and `default` to declare valid input.
- Use subparsers for commands with different arguments.
- Return parsed values or a typed configuration object to application code.
- Let `argparse` format usage errors instead of duplicating parser validation.
