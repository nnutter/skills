---
name: fracture
description: Improve commit reviewability by splitting one commit into a series of simpler commits while preserving its exact patch. Use when asked to fracture or split a commit, separate refactoring from functional changes, or simplify a complex commit history.
---

# Fracture

## Input

Treat the first skill argument as `$1`.
`$1` is the source commit and defaults to `HEAD` when it is not supplied.

## Instructions

Load and use the refactoring skill if it is available.
Review the source commit and split it into several simpler commits.
Separate refactoring changes from functional changes, and break complex changes into a clear series of commits.
The combined diff of the commits you produce MUST be identical to the source commit's patch.
