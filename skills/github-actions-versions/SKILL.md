---
name: github-actions-versions
description: Look up the latest release of a GitHub Action before pinning or updating it in workflows. Use when adding, updating, or reviewing any `uses:` pin in `.github/workflows`.
---

# GitHub Action Versions

Never use an action's latest version from training data, always look it up using GitHub's API.
Upgrade each GitHub Actions action to the latest version by looking up the latest tag on that is at least 7 days old,

```bash
gh api "repos/<owner>/<repo>/releases?per_page=5" --jq '.[] | pick(.tag_name, .published_at)'
```

Pin the commit hash and use a comment, Python-style, two spaces then `# <tag>`.
