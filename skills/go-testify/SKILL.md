---
name: go-testify
description: Apply these standards when testing Go code with github.com/stretchr/testify.
---

# Testify

- Use `assert` for checks that can continue after a failure.
- Use `require` for preconditions that make the rest of a test invalid.
- Use `require.NoError` when a test expects no error, not `assert.NoError`.
- Put the expected value before the actual value in equality assertions.
- Call `t.Helper()` in custom assertion helpers.
- Run `testifylint` with the other Go analyzers.
