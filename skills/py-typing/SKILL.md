---
name: py-typing
description: Use this skill to provide guidance related to Python's type hints and the typing package.
---

# py-typing

- Use `typing.Self` instead of a string literal class name for the return type of a constructor.

  ```python
  from typing import Self
  @classmethod
  def create(cls) -> Self: ...
  ```
