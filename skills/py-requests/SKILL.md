---
name: py-requests
description: Apply these standards when making HTTP requests with Python requests.
---

# Python requests

- Use a `requests.Session` for related requests so connections and shared settings can be reused.
- Set an explicit `timeout` on every request.
- Call `response.raise_for_status()` before using response data.
- Pass query parameters through `params` and JSON payloads through `json`.
- Close sessions with a context manager when their lifetime ends.
- Catch `requests.RequestException` at the boundary where the application can handle it.
- Do not log credentials, tokens, or other sensitive request data.
