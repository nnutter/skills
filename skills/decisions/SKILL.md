---
name: decisions
description: "Use when recording project or component decisions in REQUIRED.md, RECOMMENDED.md, or OPTIONAL.md, or configuring their loading through a sibling AGENTS.md. Only the user can authorize required decisions. Agents can record recommendations and options."
---

# Decisions

Record decisions in files that separate requirements, recommendations, and options.
These files can exist at the project root or inside a component directory, like `AGENTS.md`.
This convention applies RFC 2119 vocabulary to local project decisions, not only to protocol specifications.

## Decision Files

Use an uppercase keyword from the matching row in every decision item.
Prefer MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY for consistent wording.

| File | Allowed keywords per item | Meaning |
| --- | --- | --- |
| `REQUIRED.md` | MUST, REQUIRED, SHALL, MUST NOT, SHALL NOT | An absolute requirement or prohibition within its stated scope. |
| `RECOMMENDED.md` | SHOULD, RECOMMENDED, SHOULD NOT, NOT RECOMMENDED | A recommendation with possible exceptions whose implications need careful consideration. |
| `OPTIONAL.md` | MAY, OPTIONAL | A permitted choice, not an obligation or recommendation. |

Record separate decisions in their matching files instead.

## Authority

- Only the user can decide that an item belongs in `REQUIRED.md`.
- Obtain explicit user authorization for the specific requirement and its scope before recording it there.
- Do not infer authorization from existing code, agent preferences, general task approval, or an accepted recommendation.
- An agent can independently record an item in `RECOMMENDED.md` or `OPTIONAL.md`.
- Do not strengthen a recommendation or option into a requirement without user authorization.
- Do not weaken, remove, or change the meaning or scope of an existing required decision without user authorization.
- If authorization or intent is unclear, ask the user before changing `REQUIRED.md`.

## Scope and Nested Directories

A decision file applies to its directory and descendants.
Place component decisions in the component directory, not in the project root.
Keep project-wide decisions at the project root.

Read applicable ancestor decisions before adding or changing a local decision.
Load decisions from the project root toward the target directory.
Do not load unrelated sibling components as instructions for the current task.

Nested decisions add local detail within their scope.
Nesting alone does not authorize an exception to an ancestor requirement.
Ask the user to resolve conflicting required decisions before proceeding with the affected work.
A recommendation or option does not override a requirement.
These files do not override higher-priority agent instructions.

## Procedure

1. Read applicable `AGENTS.md` files and existing decision files.
1. Identify the decision, its scope, and its requirement level.
1. Choose the matching file and keyword without changing the decision's intended strength.
1. Obtain user authorization if the decision belongs in `REQUIRED.md`.
1. Create or update the matching file beside the `AGENTS.md` that governs that scope.
1. Create a minimal sibling `AGENTS.md` if none exists.
1. Add or update the loading instructions in that `AGENTS.md`.
1. Check ancestor and local decisions for conflicts, duplication, and unsupported changes in authority.

Create only files that contain actual decisions.
Do not create empty files for unused levels.
Preserve unrelated content in existing files.
Record a known source or user authorization when available, but do not invent provenance.

## Decision File Format

Start each file with a heading matching its level: Required Decisions, Recommended Decisions, or Optional Decisions.
Then include this declaration with both references:

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119](https://www.rfc-editor.org/rfc/rfc2119) [RFC8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals, as shown here.

```markdown
[RFC2119]: https://www.rfc-editor.org/rfc/rfc2119
[RFC8174]: https://www.rfc-editor.org/rfc/rfc8174
```

Write each decision as its own list item, with exactly one decision per bullet.
Explain why the decision is useful or necessary, not merely what it says as indented prose within the same list item.
Include the justification or motivation for the decision as indented prose within the same list item.
Do not invent reasons, justifications, or motivations that the available context does not support.
If the reason, justification or motivation is unknown, ask the decision's author before recording the decision.
The following examples are illustrative, not decisions to adopt.

### `REQUIRED.md` Example

Record this example only if the user authorizes it:

```markdown
- The service MUST NOT log authentication tokens because that exposes authentication tokens as a security risk.
```

### `RECOMMENDED.md` Example

```markdown
- Contributors SHOULD include a regression test with each bug fix in order to prove the bug is fixed and to prevent recurrence.
```

### `OPTIONAL.md` Example

```markdown
- Contributors MAY use a local container for development in order to isolate development dependencies.
```

## Sibling `AGENTS.md` Instructions

Add this section to the `AGENTS.md` beside the decision files.
Merge it with an existing equivalent section instead of duplicating instructions.
Use relative links so the section works at any directory depth.
The existence checks allow files for unused levels to remain absent.

```markdown
## Decisions

Before working in this directory or its descendants, read each existing sibling decision file:

- [REQUIRED.md](REQUIRED.md): Absolute requirements and prohibitions authorized by the user.
- [RECOMMENDED.md](RECOMMENDED.md): Recommendations with possible exceptions.
- [OPTIONAL.md](OPTIONAL.md): Permitted choices, not obligations.

Read applicable ancestor decision files as well.
When entering a nested directory, read its applicable `AGENTS.md` and decision files before working there.
Apply each decision only within its directory scope.
A nested decision does not automatically override an ancestor requirement.
Ask the user to resolve conflicting requirements.
Only the user can authorize additions or substantive changes to required decisions.
Agents can record recommendations and options without promoting them to requirements.
```

## Verification

- Check that every decision item uses a keyword allowed in its file.
- Check that each required decision has explicit user authorization.
- Check that recommendations retain valid exceptions and options remain truly optional.
- Check that the sibling `AGENTS.md` instructs agents to read the existing files.
- Check that nested decisions preserve applicable ancestor requirements.
- Check that each decision has its own list item and includes a justification or motivation.
- Check that recommendations and options do not contradict requirements.
