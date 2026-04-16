---
name: Wiki Group C Enhancements
description: Emergent wiki nesting, source summary pages, operation log, and collaborative ingest (#275–#278)
type: design
status: draft
related:
  - docs/context/plugin-distribution-and-versioning-patterns.context.md
---

## Purpose

Four enhancements that make the wiki plugin more structurally expressive,
auditable, and collaborative. They share a common dependency: #277
(emergent nesting) gates the output-path behavior of #276 (source summary
pages), so they are designed together.

---

## #277 — Emergent wiki nesting

**Problem:** The flat `wiki/` layout becomes hard to navigate as page count
grows. Type is only visible by reading frontmatter.

**Decision:** Option A — fully emergent, LLM-determined nesting. No fixed
directory taxonomy. The LLM reads the existing `wiki/` structure and places
new pages into topic-based subdirectories it infers from content. The user
can override any path at the Step 1b confirmation.

### Behavior

**Ingest:** Before proposing new pages, the LLM reads the current `wiki/`
directory tree (not just `_index.md`) to understand existing groupings.
For each new page, it proposes a path that fits contextually — e.g.
`wiki/llm-caching/consistency-tradeoffs.md` alongside related existing
pages. The path is included in the Step 1b confirmation list and is
editable by the user.

**Existing pages:** Never moved. Nesting applies only to pages created by
future ingests.

**Reindex:** `reindex.py` is updated to walk the full `wiki/` subtree
recursively, generating a `_index.md` in each subdirectory as well as
refreshing the root `wiki/_index.md` with a tree view (directory headings,
then pages under each).

**Lint:** Validates index sync for all `wiki/` subdirectories. Does not
enforce or validate page placement — path is advisory, not enforced.

### Constraints

- Must not: enforce any fixed directory names
- Must not: add a SCHEMA.md directory-mapping section
- Must not: move or rename existing wiki pages
- Won't have: lint placement enforcement

---

## #276 — Source summary page per ingest

**Problem:** Sources are cited in frontmatter but never get their own page.
No way to trace a claim back to a structured summary of the source.

**Behavior:** On every ingest, in addition to updating concept/entity pages,
create (or update) a source summary page. The page path is LLM-determined
following the same emergent nesting logic as #277 — the LLM decides where
it fits contextually (e.g., alongside other pages from the same domain).

**Source summary page structure:**

```
---
name: <Source Title>
description: One-sentence summary of the source
type: source-summary
sources: [<URL or file path>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Source Title>

**Author:** ...  **Date:** ...  **URL:** ...

## Key Claims

- Claim 1
- Claim 2
...

## Summary

[Structured summary of what the source says]
```

**Factual-only constraint:** Source summary pages record what the source
says. No interpretation, synthesis, or evaluation. Interpretation belongs
in concept and synthesis pages.

**Idempotency:** If a source summary page for this source already exists
(matched by URL in `sources:` frontmatter), update it rather than creating
a duplicate. Append new claims; do not remove existing ones.

**Step 1b:** The source summary page appears in the confirmation list like
any other page — `CREATE wiki/<path>/source-name.md` — and can be edited
or removed by the user before writing.

### Constraints

- Must not: write interpretation or synthesis into source summary pages
- Must not: create a fixed `wiki/sources/` directory
- Must not: create a source summary page if the user removes it from the
  Step 1b list

---

## #275 — Append-only operation log

**Problem:** No audit trail for wiki operations. Hard to understand what
changed and when without reading git history.

**Behavior:** After each ingest or lint operation, append an entry to
`wiki/log.md`. Created on first operation if missing.

**Entry format:**

```markdown
## [YYYY-MM-DD] ingest | <Source Title>
<N> pages updated, <M> created. Pages: wiki/path/a.md, wiki/path/b.md.

## [YYYY-MM-DD] lint | <summary>
<N> issues found: <brief description>. (or: No issues.)
```

**Rules:**
- Append-only — existing entries are never modified or removed
- `wiki/log.md` is excluded from lint orphan checks and index requirements
- Reindex skips `log.md` when building `_index.md` page inventories

### Constraints

- Must not: modify existing log entries
- Must not: appear in `wiki/_index.md` page inventory
- Must not: be flagged as orphan by lint
- Won't have: structured data format (JSON, YAML) — plain markdown only
- Won't have: log entries for research or query operations (ingest and lint
  only)

---

## #278 — Discuss-before-write (collaborative ingest)

**Problem:** The Step 1b gate confirms *which pages* to write but not
*whether the LLM understood the source correctly*. Misinterpretations
compound across multiple pages.

**Behavior:** By default, ingest inserts a discussion step before the
page list:

1. Fetch and fully read the source
2. Present key takeaways and ask the user to confirm understanding
3. Incorporate feedback
4. Present the page list (existing Step 1b gate)
5. Write

**Bulk mode:** When multiple sources are ingested in one command, the
discussion covers all sources in a single pass — present takeaways from
each source, accept consolidated feedback, then proceed to the page list.
This avoids N sequential round-trips for N sources.

**Opt-out:** Pass `--no-discuss` to skip the discussion step entirely.
Appropriate for automated or batch ingests where the user trusts the LLM's
reading.

**Discussion prompt template:**

```
Here are the key takeaways from [Source Title]:
- ...
- ...

Does this capture the important ideas? Anything missing or worth
emphasizing differently before I propose the page list?
```

### Constraints

- Must not: skip discussion unless `--no-discuss` is passed
- Must not: run a separate discussion round per source in bulk mode
- Won't have: per-project SCHEMA.md opt-out setting (flag only)

---

## Components affected

| Component | Change |
|-----------|--------|
| `plugins/wiki/skills/ingest/SKILL.md` | Add emergent path selection, source summary page step, discuss step, log append |
| `plugins/wiki/scripts/reindex.py` | Walk `wiki/` subtree recursively; per-dir `_index.md`; root index with directory headings |
| `plugins/wiki/scripts/lint.py` | Index sync across `wiki/` subdirs; exclude `log.md` from orphan and index checks |
| `plugins/wiki/skills/lint/SKILL.md` | Document that log append happens after lint |

---

## Acceptance criteria

1. **Emergent nesting:** A new ingest proposes page paths with topic-based
   subdirectories derived from existing wiki structure. User can edit any
   path at Step 1b. Reindex produces per-directory `_index.md` files.
   Lint passes with no placement errors.

2. **Source summary page:** Every ingest produces one source summary page
   (create or update). The page contains only factual content — no
   interpretation. A second ingest of the same source updates the existing
   page rather than creating a duplicate.

3. **Operation log:** After ingest, `wiki/log.md` has a new entry. After
   lint, `wiki/log.md` has a new entry. Existing entries are unchanged.
   Lint does not flag `log.md` as an orphan or missing from index.

4. **Collaborative ingest:** Single-source ingest shows a takeaways
   discussion step before the page list. Multi-source ingest shows one
   consolidated discussion for all sources. `--no-discuss` skips discussion
   entirely and goes directly to page list.
