---
name: py-dataclasses
description: Apply these standards when using Python's dataclasses module.
---

# Python dataclasses

- Use `@dataclass` for classes whose main purpose is to store data.
- Add type annotations to every data field.
- Use `field(default_factory=...)` for mutable default values.
- Use `frozen=True` for value objects that must not change after creation.
- Use `__post_init__` for validation and derived values that need field data.
