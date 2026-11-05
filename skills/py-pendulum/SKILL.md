---
name: py-pendulum
description: Apply these standards when using Pendulum for date and time handling in Python.
---

# Python Pendulum

- Use Pendulum instead of Python's `datetime` module for date and time values.
- Create timezone-aware values with `pendulum.now("UTC")` or an explicit timezone.
- Parse external date and time text with `pendulum.parse`.
- Convert time zones with `in_timezone` instead of manual offset arithmetic.
- Use `add` and `subtract` for calendar-aware arithmetic.
- Serialize API values as ISO 8601 with an explicit timezone.
