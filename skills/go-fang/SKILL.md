---
name: go-fang
description: Apply these standards when using github.com/charmbracelet/fang with Cobra.
---

# Fang

- Use Fang as the entry point for Cobra command execution.
- Build the root Cobra command before calling `fang.Execute`.
- Pass the application context to `fang.Execute`.
- Return errors from Cobra commands and handle the final error once in `main`.
- Let Fang provide its standard help, version, completion, man page, and error presentation.
- Keep application logic independent of Fang so that it remains easy to test.
