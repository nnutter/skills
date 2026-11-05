---
name: audit-commits
description: Audit Git commit messages for body quality. Use when reviewing commit messages, checking commit bodies, or verifying messages follow purpose-focused, plain-language standards.
---

# Audit Commits

Audit commit message bodies against four checks.
Applies to each non-fixup commit in range.
Fixup commits (`fixup! <subject>`, `amend! <subject>`, and `reword! <subject>`) are exempt.
Audit their target instead.

## Scope

Treat invocation of this skill as a request to audit and correct commit messages.
Use the specified commit or range when provided.
Otherwise, audit the current feature branch's commits since its merge base with the upstream branch.
If the upstream branch is unknown, ask which base to use.

## Checks

1. **Line-wrapped**: every body line is at or below 72 characters.
1. **Purpose, not what**: body explains why the change is necessary, not what changed (the patch already shows the what).
   When behavior must be named to explain the why, name the outermost observable behavior.
   For a change in application behavior, describe what the end user would experience, not how inner functions changed.
   For a change with no application behavior change, the outermost level is the caller-visible behavior of the affected function or API.
   Describe what only when needed to understand the why.
1. **No jargon**: plain words, no unexplained acronyms, internal codenames, or implementation shorthand.
1. **Simple and brief**: shortest body that conveys the purpose.
   Omit filler, restatement of the subject, and per-commit detail that belongs to other commits.

Skip missing body only when the subject plus patch make the purpose obvious.
Otherwise flag it.

## Procedure

For each commit oldest-first:

```bash
sha=<sha>
git log -1 --format=%B --end-of-options "$sha"
git log -1 --format=%B --end-of-options "$sha" | awk '{ if (length > 72) print NR": "length" chars: "$0 }'
```

Blank line must separate subject from body.
Check the body lines only (after the blank line) for the 72-char limit.

## Report

One verdict per commit: `pass` or `fail`.
For each failure, name the failed check(s), quote the offending line(s), and propose a rewrite that is wrapped, purpose-focused, jargon-free, and brief.

## Corrections

For each failed commit, create a message-only `--fixup=amend` commit with the complete corrected message.
Use the Git commit tool's `amend` mode when that tool is available.
Keep the original commits unchanged so the user can review the corrections with `timber review`.
Follow the repository's feedback workflow to place each fixup immediately after its target commit stack.
Do not include file changes in these fixups.
Do not squash or apply the fixups.
