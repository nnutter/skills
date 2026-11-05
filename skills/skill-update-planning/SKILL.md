---
name: skill-update-planning
description: Plan an update to an existing agent skill. Use for any request to add, change, or remove guidance in an existing agent skill, including direct implementation requests.
---

# Plan a Skill Update

Use this skill to identify the best existing skill for new guidance.
Then create a precise update plan.
If the user requests implementation, first complete the selection and update-planning workflow.
Then apply the planned change.
Do not modify a skill unless the user also asks you to implement the plan.

## Workflow

1. Extract the guidance that the user wants to add, change, or remove.
1. Inspect the available skill names and descriptions.
1. Load the candidate `SKILL.md` files that match the guidance.
1. Select the narrowest skill whose stated purpose includes the guidance.
1. If no existing skill fits, recommend a new skill instead of an extension of an unrelated skill.
1. Identify the exact section to change.
1. Describe the smallest change that records the guidance without a duplicate of existing instructions.
1. State any related skills that need a cross-reference or do not need a change.

## Selection Rules

- Prefer a skill that governs the action, artifact, or decision in the requested guidance.
- Prefer an existing explicit workflow section over a general introduction.
- Keep a skill focused on one capability.
- Do not add project-specific instructions to a general skill unless the user requests a global rule.
- Do not create duplicate instructions when the existing wording already implies the guidance.
- If two skills apply, name one primary skill and explain the boundary of the other skill.

## Required Response Format

Use this format:

```markdown
## Recommended Skill

`<skill-name>` — `<path-to-SKILL.md>`

## Why

<One or two sentences that connect the requested guidance to the skill purpose.>

## Update Plan

1. In `<section name>`, <specific edit>.
2. <Additional specific edit, if needed.>

## Proposed Wording

> <The exact new or replacement instruction.>

## Related Skills

- `<skill-name>`: <why it does or does not need a change.>
```

If no skill fits, replace **Recommended Skill** with **Recommended New Skill**.
State its name, location, description, and the sections that it needs.

## Verification

Before you respond, make sure that:

- The selected skill exists and its description supports the recommendation.
- The target section exists, or the plan says where to add it.
- The proposed wording is actionable and does not conflict with existing instructions.
- The plan does not propose an edit when no edit is necessary.
