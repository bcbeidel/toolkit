---
name: ingest
description: >
  Ingest any source into wiki pages. Use when the user says "ingest this",
  "add to wiki", "process this source", "update wiki with", or provides a
  URL, file path, or pasted text for knowledge capture.
argument-hint: "[URL | file path | pasted content]"
user-invocable: true
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

Before editing any files, read the project's wiki context:

1. **Read `wiki/_index.md`** — understand the existing page inventory (titles, descriptions, file paths)
2. **Read `wiki/SCHEMA.md`** — learn the valid `type` values, `confidence` tiers, and relationship types for this project

If either file is missing, stop and report: "wiki/_index.md not found" or "wiki/SCHEMA.md not found. Run `/wos:setup` to initialize wiki infrastructure."

## Ingest Protocol

With the source content and wiki context in hand:

### Step 1: Identify Affected Pages

Identify **5–15 wiki pages** that this source meaningfully informs — both:
- **Existing pages** that should be updated with new information or connections
- **New pages** to create for topics the source covers that have no existing page

If the source is narrow and fewer than 5 pages genuinely apply, proceed with what applies. Do not pad.

### Step 1b: Confirm Before Writing

Present the proposed changes to the user before modifying any file:

```
Ready to ingest into N pages:
- UPDATE wiki/existing-page.md — adding [summary of additions]
- CREATE wiki/new-topic.md — [description of new page]
...

Proceed? (yes / edit list / cancel)
```

Wait for explicit confirmation. If the user edits the list, revise accordingly. Do not modify any wiki files until confirmed.

### Step 2: Update Each Page

For each affected page, apply all changes that are warranted:

**Content (append-only):** Add new information, examples, or elaboration at the appropriate location in the page. Never remove or rewrite existing prose — only add. If existing content conflicts with the source, flag it (see Contradiction Handling below) rather than overwriting it.

**Frontmatter updates:**
- `sources:` — append the source URL or file path (deduplicate if already present)
- `updated:` — set to today's date (YYYY-MM-DD)
- `type:` — assign or confirm the page type per `wiki/SCHEMA.md`
- `confidence:` — assign or update the confidence tier per `wiki/SCHEMA.md`, reflecting the source's authority and corroboration with existing pages
- `related:` — add cross-references to other wiki pages that this source connects

### Step 3: Create New Pages

For topics the source covers with no existing wiki page, create a new page:

- Path: `wiki/<slug>.md` (derive slug from topic name)
- Include full frontmatter: `name`, `description`, `type`, `confidence`, `sources`, `created`, `updated`
- Write an initial page body from the source content — follow the structure of existing wiki pages
- Add `related:` links to existing pages that connect

### Step 4: Contradiction Handling

If source content contradicts information in an existing page, do **not** overwrite the existing claim. Instead, append a contradiction marker immediately after the conflicting passage:

```
<!-- CONTRADICTION: [source] states "[new claim]". Existing content says "[current claim]". Verify which is correct. -->
```

Report all contradiction markers to the user at the end of ingest.

## Append-Only Constraint

Existing prose in wiki pages is never removed or overwritten. Every `git diff` after an ingest should show only additions (new lines, frontmatter field updates, appended content). If you find yourself deleting or rewriting existing text, stop — append instead or flag a contradiction.

## Post-Ingest

After all page updates and creations, run both commands unconditionally:

```bash
python scripts/lint.py --root <project-root> --no-urls
python scripts/reindex.py --root <project-root>
```

Report results to the user:
- If lint produces new issues, list them with severity
- Confirm that `wiki/_index.md` was regenerated

Do not block on lint issues — report and continue.

## High-Rigor Path

When the source is a research document (`.research.md` file), offer the user an opt-in SIFT verification step before ingest:

> "This source is a research document. Would you like to run SIFT verification before ingesting? (default: skip)"

- **Skip (default):** Proceed directly to the Ingest Protocol
- **Verify:** Invoke `/wos:research` with the document to validate sources, then ingest the verified findings

The high-rigor path is never required. It is appropriate when the user wants to confirm source credibility before committing findings to the wiki.

## Examples

**URL ingest:**
> "Ingest this article: https://example.com/llm-caching"
→ Fetch content → read wiki context → identify 5–15 pages → update/create pages → lint + reindex

**File ingest:**
> "Add to wiki: docs/research/2026-04-10-caching-patterns.research.md"
→ Read file → offer SIFT opt-in → read wiki context → identify pages → update/create → lint + reindex

**Pasted text:**
> "Ingest this: [user pastes a block of notes]"
→ Use pasted text as source → read wiki context → proceed

## Key Instructions

- **Won't overwrite existing prose** — ingest is append-only; every `git diff` should show only additions
- **Won't write until confirmed** — Step 1b gate is non-negotiable; present the full list and wait for approval
- **Won't ingest without reading wiki context first** — `wiki/_index.md` and `wiki/SCHEMA.md` must be read before any changes
- **Recovery:** if an ingest produces unwanted changes, use `git diff` to review and `git checkout -- wiki/` to revert; all writes are isolated to the `wiki/` directory

## Anti-Pattern Guards

1. **Overwriting existing prose** — every `git diff` after ingest should show only additions. Rewriting existing content destroys the provenance trail and may silently lose validated information. If existing content is wrong, flag a contradiction marker instead.
2. **Skipping Pre-Ingest reads** — proceeding without reading `wiki/_index.md` and `wiki/SCHEMA.md` causes type/confidence misassignment and duplicate page creation. These are required reads, not optional context.
3. **Silent contradiction** — when source content conflicts with an existing page, the anti-pattern is choosing one version silently. The correct action is the contradiction marker. Unresolved conflicts belong to the user, not the ingest operation.
4. **Padding to hit the 5-page minimum** — if a narrow source genuinely affects fewer than 5 pages, proceed with what applies. Forcing connections to reach a target count produces low-quality updates that degrade the wiki.
5. **Assigning confidence without cross-referencing** — confidence tier should reflect corroboration across pages, not just the source's claimed authority. A single primary source warrants `medium` at best until cross-referenced with existing wiki content.

## Handoff

**Receives:** URL, file path, or pasted text representing an external source
**Produces:** One or more wiki pages added or updated under `wiki/`
**Chainable to:** lint
