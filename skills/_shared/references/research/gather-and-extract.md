---
name: Gather and Extract
description: Phase 2 — search for sources, extract content verbatim, write to disk per sub-question
metadata:
  stage: gather
  pipeline: research
  tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]
---

## Purpose

Search for sources across sub-questions, extract content verbatim, and verify URLs. Produces a DRAFT document with structured extracts and a verified sources table.

## Input

- **Research question** (restated, precise)
- **Sub-questions** (2-4, from the approved brief)
- **Research mode** (deep-dive, landscape, technical, etc.)
- **Search strategy** (initial terms, source types)
- **Output path** (e.g., `docs/research/YYYY-MM-DD-slug.research.md`)
- **Constraints** (time period, domain, technology stack)

# Phase 2: Gather and Extract

### Search Budgets by SIFT Rigor

| SIFT Rigor | Searches per sub-question | Total budget |
|------------|---------------------------|--------------|
| Low        | 2-3                       | 5-10         |
| Medium     | 3-5                       | 10-15        |
| High       | 5-8                       | 15-25        |

Process one sub-question at a time. For each sub-question, complete the
full gather-and-extract cycle before moving to the next:

### Per sub-question:

**Gather.** Repeat until coverage is sufficient or budget is exhausted:

1. Execute a search. Aim for 10-20 candidates total across all sub-questions.
2. For each candidate: record URL, title, publication date, author/org. Flag as **unverified**.
3. Log the search:

```json
{"query": "terms", "source": "google", "date_range": "2024-2026", "results_found": 12, "results_used": 3}
```

4. **Reflect.** After every 2-3 searches, assess: does this sub-question have
   coverage? Are results converging? Continue or stop.

> **Source diversity:** `WebSearch` routes through a single engine. Vary
> query terms to surface different source types. Fetch known database URLs
> directly when relevant. Log `"google"` as the source honestly.

> **Fetch failures:** Retry failed `WebFetch` calls individually. Retry
> 3xx with redirect URL. Keep 403 if from published venue. Retry timeouts
> once, then skip. Do not drop sources solely because fetching failed.

**Extract.** For each fetched source, extract relevant content verbatim and
discard boilerplate (navigation, ads, sidebars, unrelated content). This is
**lossless extraction**, not summarization — Phases 7-8 need original
source content for claim verification.

Format per source:

```markdown
### Source [1]: asyncio — Asynchronous I/O
- **URL:** https://docs.python.org/3/library/asyncio.html
- **Author/Org:** Python Software Foundation | **Date:** 2024

**Re: How does asyncio handle concurrency?**
> "The library provides a foundation for writing single-threaded concurrent
> code using coroutines, multiplexing I/O access over sockets and other
> resources, running network clients and servers, and other related
> primitives." (Introduction, para 1)
```

Each extract links to its sub-question, preserves exact wording, and
notes location within the source for later verification.

**Write to disk.** After extracting for the current sub-question, update
the DRAFT document on disk with the new sources and structured extracts.
This ensures fetched content from completed sub-questions is eligible for
context compression before starting the next sub-question.

**Deferred sources.** If a search for the current sub-question surfaces a
source relevant to a different sub-question, note it in a
`<!-- deferred-sources -->` comment in the DRAFT document with the URL and
which sub-question it applies to. Pick up deferred sources when processing
that sub-question.

### After all sub-questions:

5. Record skipped sources in `not_searched` with reasons.
6. **Verify DRAFT state.** The document should have `type: research`
   frontmatter, a `<!-- DRAFT -->` marker, a sources table
   (# | URL | Title | Author/Org | Date | Status), structured extracts
   for every sub-question, and a `<!-- search-protocol ... -->` comment
   containing the accumulated JSON.

## Output

The DRAFT document on disk must have:
- `type: research` frontmatter with `<!-- DRAFT -->` marker
- Sources table with `# | URL | Title | Author/Org | Date | Status` columns
- Structured extracts for every sub-question
- `<!-- search-protocol ... -->` comment with accumulated search JSON
- Verified URLs (404s removed, 403s noted)

### Phase Gate: Phase 2 → Phase 3

DRAFT file exists on disk with structured extracts for all sub-questions.

## Constraints

- Do not evaluate sources (no tier assignment — that's the evaluator's job).
- Do not synthesize findings — extract verbatim only.
- Do not prompt the user for input.
