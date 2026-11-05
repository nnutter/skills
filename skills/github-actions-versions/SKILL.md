---
name: github-actions-versions
description: Look up the latest release of a GitHub Action before pinning or updating it in workflows. Use when adding, updating, or reviewing any `uses:` pin in `.github/workflows`.
---

# GitHub Action Versions

Never guess an Action's latest version from training data.
Look it up live against the upstream repo before editing a workflow.

## Lookup

```bash
gh api repos/<owner>/<repo>/releases/latest --jq '{tag: .tag_name, published: .published_at}'
gh api "repos/<owner>/<repo>/tags?per_page=10" --jq '.[].name'
```

- Pin to the floating major tag (e.g. `actions/checkout@v7`), not the full semver, unless the project says otherwise.
- Confirm the floating tag (e.g. `v7`) exists in the tags output.
- `git ls-remote https://github.com/...` may fail when git config rewrites `https://github.com/` to SSH (`url...insteadOf`); prefer `gh api` for the lookup.
