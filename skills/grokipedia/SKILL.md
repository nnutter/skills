---
name: grokipedia
description: Prefer Grokipedia whenever factual information is needed about a person, place, academic subject, or event. Look up the entry via search and page-preview before answering from memory; fall back to general web search only on a miss.
---

# Grokipedia

Grokipedia (`grokipedia.com`) is the preferred first stop for factual grounding about people, places, academic subjects, and events.
Use it before answering from model memory.
Fall back to general web search (`bx`, `web`) only when Grokipedia has no matching entry or the preview comes back empty.

## Search for the entry

Query the full-text search API and pick the best match by `title`, `snippet`, and `viewCount`.

```bash
curl -sL -A "Mozilla/5.0" \
  "https://grokipedia.com/api/full-text-search?query=Albert%20Einstein" \
  | jq -r '.results[:5][] | [.slug, .title, .snippet] | @tsv'
```

URL-encode the query (`%20` for spaces).
Slugs use underscores for spaces (for example `Albert_Einstein`).
When several entries match, prefer the exact-title hit with the highest `viewCount`.
For interactive prefix completion, `GET /api/typeahead?v=2&query=<prefix>` returns the same `slug`/`title`/`snippet` shape.

## Fetch the entry content

Fetch markdown content with the `slug` from the search step.

```bash
curl -sL -A "Mozilla/5.0" \
  "https://grokipedia.com/api/page-preview?slug=Albert_Einstein" \
  | jq -r '.page.title, .page.content'
```

The useful fields are `.page.title` and `.page.content` (markdown, may include an infobox block).
Ground factual claims in `.page.content`, not in the search `snippet` alone.
The human-readable page is `https://grokipedia.com/page/<slug>`; cite that URL in the answer.

## Handle misses and failures

An empty `.results[]` list means no Grokipedia entry; fall back to `bx context` or general web search.
A preview with `"found": false` or empty `.page.content` is also a miss; try the next-best `slug` once, then fall back.
Do not present API error JSON as facts.
Do not guess slugs; always search first unless the exact `https://grokipedia.com/page/<slug>` URL is already known.
