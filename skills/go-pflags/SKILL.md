---
name: go-pflags
description: Apply these standards when using github.com/spf13/pflag for Go command-line flags.
---

# pflag

- Use pflag with Cobra commands instead of creating a second flag parser.
- Define each flag on the narrowest command that needs it.
- Use persistent flags only when descendant commands need the flag.
- Give each flag a descriptive long name, a useful default, and help text.
- Use short names only when they are common and unambiguous.
- Validate flag combinations after parsing and return an error.
- Bind a flag to a variable only when direct access is needed.
