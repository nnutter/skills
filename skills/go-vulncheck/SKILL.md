---
name: go-vulncheck
description: Address govulncheck findings with only the required dependency or Go toolchain updates. Use when fixing Go vulnerabilities or CVEs without unnecessary module upgrades.
---

# Fix Go Vulnerabilities with Minimal Updates

A module can contain vulnerable packages that the project never imports.
An imported package can contain vulnerable symbols that the project never calls.
Neither finding alone requires an update for this task.
Go updates dependencies at module granularity, not individual packages.

## Workflow

1. Run the repository's govulncheck command before making changes.
   If none exists, run `govulncheck ./...` from each relevant module root.
   Use the project's supported build tags, platforms, and test scope.
1. Classify each finding using source analysis and reported call traces.
   Update only for vulnerable symbols reachable from the scanned code.
   Do not update a module only because a module-level scan reports a CVE.
   Do not update for vulnerable packages that are not imported or vulnerable symbols that are not called.
   Treat missing analysis or unsupported configurations as unknown, not proof that the code is unaffected.
1. For each reachable finding, identify the owning module and its applicable fixed version.
   Select the smallest compatible upgrade that fixes all reachable findings in that module.
   Use an explicit version: `go get example.com/module@vX.Y.Z`.
   For standard-library findings, update the Go toolchain to an applicable fixed release instead.
1. Do not run broad upgrades such as `go get -u ./...` or select `@latest` by default.
   Keep transitive updates only when the required fix needs them.
   Review `go.mod` and `go.sum` for unrelated changes.
   If no compatible fix exists, report the blocker instead of making unrelated upgrades.
1. Repeat the same scans after the update.
   Run the repository's tests and required checks.
   Report fixed findings, skipped findings with reachability evidence, and any remaining unknowns or blockers.

A clean scan applies only to the configurations that it analyzed.
Do not suppress findings or reduce scan coverage to obtain a clean result.
