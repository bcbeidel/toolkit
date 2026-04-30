---
name: ingest
description: >
  Ingest any source into wiki pages. Use when the user says "ingest this",
  "add to wiki", "process this source", "update wiki with", or provides a
  URL, file path, or pasted text for knowledge capture.
argument-hint: "[URL | file path | pasted content]"
user-invocable: true
license: MIT
---

# Ingest

Update wiki pages from any source: URL, file path, pasted text, or research document.

## Input Handling

Accept the source in any of these forms:

- **URL** — fetch the page content before proceeding
- **File path** — read the file (`.md`, `.txt`, `.pdf`, transcript, etc.)
- **Pasted text** — use as-is
- **Research document** (`.research.md`) — read; see [High-Rigor Path](#high-rigor-path) for an opt-in verification step

Resolve the source to readable text before any further steps.

If no source is provided, ask: "What source should I ingest? (URL, file path, or paste content directly)"

## Pre-Ingest

Before editing any files, resolve **where pages live** and **what vocabulary
applies** by deferring to the project's `RESOLVER.md`. Ingest does not assume
a fixed `wiki/` directory or hard-coded schema path.

1. **Read `RESOLVER.md`** at the project root if it exists.

   - **Filing target** — find the row in the filing table that covers
     ingest output (typical content types: "wiki page", "knowledge page",
     "source summary", or whatever the project uses). The location column
     is the directory where new pages go; the naming column is the file
     pattern. If multiple rows apply (e.g., separate rows for source
     summaries vs. concept pages), use them all.
   - **Vocabulary / schema** — find the context-table entry for "ingesting
     a source" (or the closest equivalent). It bundles the doc(s) that
     define valid `type:` values, `confidence:` tiers, and relationship
     types. Read the bundled doc(s) before assigning frontmatter.
   - **Inventory** — scan the resolved filing directory, glob the naming
     pattern, and read each file's frontmatter `description` to understand
     existing pages. This replaces a hand-maintained index file.

2. **If `RESOLVER.md` is missing or has no relevant rows**, ingest runs in
   degraded mode:

   - Ask the user where new pages should go and what naming pattern to use
   - Skip schema enforcement (frontmatter `type:` / `confidence:` are
     written but not validated against a vocabulary)
   - Recommend running `/build:build-resolver` to add filing + context
     entries so future ingests are deterministic. Do not block on it.

3. **If a `wiki/SCHEMA.md` exists at the legacy path** but RESOLVER.md
   does not point at it, treat its presence as an implicit schema and
   read it. Recommend the user add an "ingesting a source" context-table
   entry so the dependency is explicit.

The output of Pre-Ingest is: **filing target(s)**, **schema content (or
none)**, and **existing-page inventory**. The rest of the protocol uses
these resolved values, not hard-coded paths.

## Ingest Protocol

With the source content and wiki context in hand:

### Step 0: Discuss Key Takeaways (opt-in)

When `--discuss` is passed, present your reading of the source to the user
and invite correction before proposing the page list. Otherwise, skip
straight to Step 1.

**Single source:**

```
Here are the key takeaways from [Source Title]:
- ...
- ...

Does this capture the important ideas? Anything missing or worth
emphasizing differently before I propose the page list?
```

**Multiple sources (bulk mode):** Present takeaways for all sources in a single
consolidated discussion — one list per source, one round of feedback for all.
Do not run a separate round-trip per source.

### Step 1: Identify Affected Pages

Identify the wiki pages this source meaningfully informs — both:
- **Existing pages** that should be updated with new information or connections
- **New pages** to create for topics the source covers that have no existing page

**Emergent path selection for new pages:** Based on the filing target(s)
resolved in Pre-Ingest and the inventory scan, propose a subdirectory
path that fits contextually — place the new page alongside existing
pages on related topics. Example: if `<filing-target>/llm-patterns/`
already has caching pages, a new page on cache invalidation belongs
under `<filing-target>/llm-patterns/cache-invalidation.md`, not at the
top level. If no relevant subdirectory exists, propose a new one whose
name reflects the topic cluster. The user can override any proposed
path at Step 1b.

**Source summary page (conditional):** If the project's RESOLVER.md
filing table defines a row for "source summary" pages — or the schema
loaded in Pre-Ingest defines a `source-summary` `type:` value —
include one source summary page for the ingested source (see
[Step 3a](#step-3a-create-source-summary-page)). Idempotency: if a
source summary page already exists for this URL (matched by URL in
the `sources:` frontmatter field), update it rather than creating a
duplicate — append new claims, never remove existing ones.

If the project does not define a source-summary convention, skip the
summary page. Concept and entity pages are sufficient.

### Step 1b: Confirm Before Writing

Present the proposed changes to the user before modifying any file. Use
the filing target resolved in Pre-Ingest as the path prefix:

```
Ready to ingest into N pages:
- UPDATE <filing-target>/existing-page.md — adding [summary of additions]
- CREATE <filing-target>/llm-patterns/new-topic.md — [description of new page]
...

Proceed? (yes / edit list / cancel)
```

Paths for new pages include the proposed subdirectory. The user can edit any path before confirming.

Wait for explicit confirmation. If the user edits the list, revise accordingly. Do not modify any wiki files until confirmed.

### Step 2: Update Each Page

For each affected page, apply all changes that are warranted:

**Content (append-only):** Add new information, examples, or elaboration at the appropriate location in the page. Never remove or rewrite existing prose — only add. If existing content conflicts with the source, flag it (see Contradiction Handling below) rather than overwriting it.

**Frontmatter updates:**
- `sources:` — append the source URL or file path (deduplicate if already present)
- `updated:` — set to today's date (YYYY-MM-DD)
- `type:` — assign or confirm the page type per the project schema loaded
  in Pre-Ingest (or the user's preference, in degraded mode)
- `confidence:` — assign or update the confidence tier per the project
  schema, reflecting the source's authority and corroboration with
  existing pages
- `related:` — add cross-references to other pages that this source connects

### Step 3: Create New Pages

For topics the source covers with no existing page, create a new page:

- Path: `<filing-target>/<slug>.md` using the filing target and naming
  pattern resolved in Pre-Ingest
- Include full frontmatter: `name`, `description`, `type`, `confidence`,
  `sources`, `created`, `updated`
- Write an initial page body from the source content — follow the
  structure of existing pages in the same filing target
- Add `related:` links to existing pages that connect

### Step 3a: Create Source Summary Page (conditional)

When the project defines a source-summary convention (see Step 1),
create or update a source summary page in addition to the concept and
entity pages. Skip this step if the convention is not defined.

**Structure:**

```markdown
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

## Summary

[Structured summary of what the source says]
```

**Factual-only constraint:** Source summary pages record what the source says.
No interpretation, synthesis, or evaluation. Those belong in concept and
synthesis pages.

**Idempotency:** Match an existing source summary page by URL in its `sources:`
frontmatter. If found, append new claims — do not create a duplicate, do not
remove existing claims.

### Step 4: Contradiction Handling

If source content contradicts information in an existing page, do **not** overwrite the existing claim. Instead, append a contradiction marker immediately after the conflicting passage:

```
<!-- CONTRADICTION: [source] states "[new claim]". Existing content says "[current claim]". Verify which is correct. -->
```

Report all contradiction markers to the user at the end of ingest.

## Append-Only Constraint

Existing prose in pages is never removed or overwritten. Every `git diff`
after an ingest should show only additions (new lines, frontmatter field
updates, appended content). If you find yourself deleting or rewriting
existing text, stop — append instead or flag a contradiction.

## Post-Ingest

After all page updates and creations, run lint:

```bash
python3 <plugin-scripts-dir>/lint.py --root <project-root>
```

Report results to the user:
- If lint produces new issues, list them with severity

Do not block on lint issues — report and continue.

## High-Rigor Path

When the source is a research document (`.research.md` file), offer the user an opt-in SIFT verification step before ingest:

> "This source is a research document. Would you like to run SIFT verification before ingesting? (default: skip)"

- **Skip (default):** Proceed directly to the Ingest Protocol
- **Verify:** Invoke `/wiki:research` with the document to validate sources, then ingest the verified findings

The high-rigor path is never required. It is appropriate when the user wants to confirm source credibility before committing findings to the wiki.

## Examples

**URL ingest:**
> "Ingest this article: https://example.com/llm-caching"
→ Fetch content → resolve filing/schema via RESOLVER.md → identify affected pages → update/create pages → lint

**File ingest:**
> "Add to wiki: .research/2026-04-10-caching-patterns.research.md"
→ Read file → offer SIFT opt-in → resolve filing/schema → identify pages → update/create → lint

**Pasted text:**
> "Ingest this: [user pastes a block of notes]"
→ Use pasted text as source → resolve filing/schema → proceed

## Key Instructions

- **Won't overwrite existing prose** — ingest is append-only; every `git diff` should show only additions
- **Won't write until confirmed** — Step 1b gate is non-negotiable; present the full list and wait for approval
- **Won't ingest without resolving filing target** — Pre-Ingest reads RESOLVER.md (or asks the user in degraded mode) before any page identification
- **Recovery:** if an ingest produces unwanted changes, use `git diff` to review; writes are isolated to the filing target(s) resolved in Pre-Ingest, so `git checkout -- <filing-target>/` reverts cleanly

## Anti-Pattern Guards

1. **Separate discussion round per source in bulk mode** — when ingesting multiple sources, running one discussion round per source creates unnecessary back-and-forth. Consolidate all sources into a single takeaways discussion before moving to the page list.
2. **Overwriting existing prose** — every `git diff` after ingest should show only additions. Rewriting existing content destroys the provenance trail and may silently lose validated information. If existing content is wrong, flag a contradiction marker instead.
3. **Writing interpretation into source summary pages** — source summary pages record what the source says, not what you conclude from it. Synthesis and evaluation belong in concept or synthesis pages, not in `type: source-summary` pages.
4. **Skipping Pre-Ingest resolution** — proceeding without resolving filing target and schema (via RESOLVER.md or user prompt) causes pages to land in the wrong directory and frontmatter to misalign with project vocabulary. Pre-Ingest is required, not optional context.
5. **Silent contradiction** — when source content conflicts with an existing page, the anti-pattern is choosing one version silently. The correct action is the contradiction marker. Unresolved conflicts belong to the user, not the ingest operation.

## Handoff

**Receives:** URL, file path, or pasted text representing an external source
**Produces:** One or more pages added or updated under the filing target(s) resolved from `RESOLVER.md` (or user-confirmed paths in degraded mode)
**Chainable to:** `/wiki:lint`; `/build:build-resolver` (when RESOLVER.md is missing or lacks an "ingesting a source" context bundle)
