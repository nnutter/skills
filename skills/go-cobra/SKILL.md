---
name: go-cobra
description: Apply these standards when building Go command-line interfaces with github.com/spf13/cobra.
---

# Cobra

- Build a command tree with a root command and focused child commands.
- Set `Use`, `Short`, and `Args` on each command.
- Prefer `RunE` so commands return errors to the caller.
- Use Cobra argument validators such as `cobra.NoArgs` and `cobra.ExactArgs`.
- Define flags on the narrowest command that needs them.
- Use `PersistentFlags` only for flags inherited by descendants.
- Keep application logic outside command construction and handlers when possible.
