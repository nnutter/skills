---
name: go-skill-loader
description: Documents the go-skill-loader pi extension. Use when adding auto-load metadata to a SKILL.md, or when debugging why a skill did or did not auto-load after reading a Go file. Covers the metadata.go-module / metadata.go-package frontmatter format and the /go-skills status command.
---

# go-skill-loader

The `go-skill-loader` pi extension (`~/.pi/agent/extensions/go-skill-loader.ts`) auto-loads skills when Go code using them is read.
It watches `read` tool results for `.go` files, extracts import paths, resolves each import to its
Go module with `go list`, and appends the full bodies of matching skills to that tool result (once per skill per session).

## Skill metadata format

Declare auto-load matching in the skill's frontmatter under `metadata`:

```yaml
---
name: my-skill
description: ...
metadata:
  go-module:
    - github.com/foo/bar
  go-package:
    - github.com/foo/bar/baz
---
```

Rules:

- Each key accepts a scalar string, a flow list (`[a, b]`), or a block list
  (`- a`). `go_module` / `go_package` (underscore) spellings also work.
- `go-package` matches an **exact import path** from the file's imports.
- `go-module` matches the **module path** owning an import, as reported by `go list -e`.
  Standard library packages resolve to the module name `std`.
- List **both sides**: the packages/modules providing the modern API *and* the ones they supersede, so the skill loads whether the file already uses the new API or still uses the old one.
  Example: a `slices`-based skill lists `go-package: [slices, sort]`.
- **Stdlib skills must use `go-package` only.** Declaring `go-module: std` would match every file with any stdlib import.
- **Third-party skills use both**: e.g. `go-module: [github.com/google/uuid]` plus `go-package: [uuid, github.com/google/uuid]`, so any package under that module also matches.
- Skills whose guideline involves no importable package (pure builtins or language semantics such as `any`, `clear`, `min`/`max`) get **no metadata**: there is no import signal to match on, and the loader ignores skills without metadata.

## Matching details

- Single-line imports, import blocks, and aliased / blank (`_`) / dot (`.`) imports are all recognized.
  The cgo pseudo-package `C` is skipped, as are commented-out imports.
- Module resolution runs `go list` per import with caching; results are cached for the session.
  When `go` is unavailable, exact `go-package` matching still works and module matching is skipped.
- Partial reads (offset/limit) are parsed best-effort from the returned text.

## Indexing

Skills are indexed exactly once per session: `session_start` kicks off a background build (startup never waits on it) that lists skills via `pi.getCommands()`, re-reads each `SKILL.md`, and keeps those with loader metadata. `tool_result` handlers await that single index instead of re-scanning on every read.

## /go-skills command

```text
/go-skills
```

Reports the loader status for the current session: how many skills were indexed with their `go-module` / `go-package` entries, and which have been loaded so far.
Each load is also announced with a `go-skill-loader: loaded <names>` notice, and the injected text carries a
`Go skill auto-loader:` marker in its host tool result.
