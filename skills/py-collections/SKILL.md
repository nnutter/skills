---
name: py-collections
description: Apply these standards when using Python's collections and collections.abc modules.
---

# Python collections

- Choose a collection type that matches the operation.
- Use `deque` for queues and bounded histories.
- Use `defaultdict` for grouped values that need a default factory.
- Use `Counter` to count hashable values.
- Use types from `collections.abc` for abstract collection annotations.
