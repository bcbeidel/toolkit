---
name: Wiki Group C Enhancements
description: Emergent wiki nesting, source summary pages, operation log, and collaborative ingest (#275–#278)
type: plan
status: completed
branch: feat/wiki-group-c-enhancements
related:
  - docs/designs/2026-04-15-wiki-group-c-enhancements.design.md
---

# Wiki Group C Enhancements

## Goal

Four features that make the wiki plugin structurally expressive, auditable,
and collaborative. The wiki directory now supports emergent LLM-determined
subdirectory nesting (#277); every ingest produces a factual-only source
summary page (#276) and appends to an operation log (#275); and ingest now
opens a discuss-before-write dialogue by default (#278).

## Scope

Must have:
- `wiki.py`: `validate_wiki()` and `check_wiki_orphans()` walk the wiki
  subtree recursively; `log.md` excluded from page and orphan checks
- `reindex.py`: wiki reindex mode activated when `wiki/SCHEMA.md` is
  present; generates per-subdirectory `_index.md` and a tree-view root
  `wiki/_index.md`; skips `log.md`
- `ingest/SKILL.md`: reads wiki directory tree before proposing page
  paths; discuss-before-write step (default on, `--no-discuss` to skip);
  source summary page creation per ingest; log append after each ingest
- `lint/SKILL.md`: log append after each lint run

Won't have:
- Fixed directory taxonomy or lint enforcement on page placement
- `log.md` entries for research or query operations
- Per-project SCHEMA.md opt-out for discuss step (flag only)
- Migration of existing flat-wiki pages to subdirectories

## Approach

All changes are in the `plugins/wiki/` directory. Python changes come first
(Chunk 1) so they can be verified with `pytest` before touching the skill
files (Chunk 2). Chunk 1 has two parts: `wiki.py` (validation) and
`reindex.py` (index generation), each with their own tests.

For `validate_wiki()`: replace `wiki_dir.iterdir()` with `wiki_dir.rglob(
"*.md")` and filter out `log.md`, `SCHEMA.md`, `_index.md`. Call
`check_wiki_orphans()` for the root and every subdirectory that contains
a `_index.md`. Update `check_wiki_orphans()` to skip `log.md` and to
reference the specific directory's `_index.md` in error messages.

For `reindex.py`: auto-detect `wiki/SCHEMA.md` at the project root. When
found, walk `wiki/` recursively — for each subdirectory with `.md` files
(excluding `log.md`, `SCHEMA.md`, `_index.md`), write a flat `_index.md`;
then write a tree-view root `wiki/_index.md` with a `## DirName` heading per
subdirectory followed by a file table, and a flat table for root-level pages.
The existing `TestReindexDoesNotTouchWikiInventory` test must be updated:
it tested the old invariant (wiki not touched); the new invariant is
"reindex manages wiki indices when SCHEMA.md is present."

The four ingest SKILL.md changes are additive and committed separately to
keep rollback boundaries clean.

## File Changes

- Modify: `plugins/wiki/src/wiki/wiki.py` (recursive walk, log.md exclusion)
- Modify: `plugins/wiki/scripts/reindex.py` (wiki reindex mode)
- Modify: `plugins/wiki/tests/test_wiki.py` (new tests + log.md exclusion)
- Modify: `plugins/wiki/tests/test_reindex.py` (wiki reindex tests; update
  `TestReindexDoesNotTouchWikiInventory`)
- Modify: `plugins/wiki/skills/ingest/SKILL.md` (four behavioural additions)
- Modify: `plugins/wiki/skills/lint/SKILL.md` (log append)

## Tasks

---

### Chunk 1: Python — recursive validation and wiki reindex

---

### Task 1: Update `wiki.py` for recursive walk and log.md exclusion

**Files:**
- Modify: `plugins/wiki/src/wiki/wiki.py`

- [x] In `check_wiki_orphans()`: add `"log.md"` to the skip set alongside
  `"_index.md"` and `"SCHEMA.md"`. Update the error message from the
  hardcoded `wiki/_index.md` reference to `f"{wiki_dir.name}/_index.md"` so
  subdirectory error messages are accurate.
- [x] In `validate_wiki()`: replace `wiki_dir.iterdir()` with
  `wiki_dir.rglob("*.md")`. Add a skip guard for filenames `_index.md`,
  `SCHEMA.md`, and `log.md`. For each `.md` in subdirectories, the
  `wiki_dir` argument passed to `doc.issues()` is still the wiki root
  (SCHEMA.md lives at the root, not in subdirs).
- [x] In `validate_wiki()`: after the per-file loop, replace the single
  `check_wiki_orphans(wiki_dir)` call with a loop over `wiki_dir` and all
  subdirectories (`wiki_dir.rglob("*/")`) that call `check_wiki_orphans()`
  for each directory that has a `_index.md`.
- [x] Verify: `python -m pytest plugins/wiki/tests/test_wiki.py -v` — passes
  with no regressions on existing tests.
- [x] Commit: `fix(wiki): recursive validate_wiki and log.md exclusion (#277, #275)` <!-- sha:c12d900 -->

---

### Task 2: Update `reindex.py` with wiki reindex mode

**Files:**
- Modify: `plugins/wiki/scripts/reindex.py`

- [x] After the existing areas-based reindex block in `main()`, add wiki
  detection: `wiki_dir = root / "wiki"`. If `(wiki_dir / "SCHEMA.md").is_file()`,
  call a new helper `_reindex_wiki(wiki_dir, root)`.
- [x] Implement `_reindex_wiki(wiki_dir, root)`:
  - Walk `wiki_dir` recursively with `os.walk`.
  - Skip `log.md`, `SCHEMA.md`, `_index.md` when collecting files.
  - For each subdirectory with `.md` files: call `_write_index(subdir, root)`
    (existing helper — reuses unchanged).
  - For root `wiki/` itself: write a tree-view `wiki/_index.md` — one
    `## <dirname>` heading per subdirectory (sorted), followed by a file
    table for pages in that subdir; then a flat table for root-level `.md`
    pages (excluding `log.md`, `SCHEMA.md`, `_index.md`).
  - Print count: `f"Wiki: reindexed {n} subdirector{'y' if n==1 else 'ies'}"`
- [x] Verify: `python -m pytest plugins/wiki/tests/test_reindex.py -v` —
  existing tests pass (the wiki-isolation test will fail until Task 4 updates
  it; that is expected and acceptable).
- [x] Commit: `feat(wiki): reindex.py wiki subtree mode (#277)` <!-- sha:33791d9 -->

---

### Chunk 2: Tests

---

### Task 3: Tests for recursive wiki validation

**Files:**
- Modify: `plugins/wiki/tests/test_wiki.py`

- [x] Add `TestValidateWikiRecursive`: create a wiki dir with a subdir
  containing a valid page and a `_index.md` listing it. Call
  `validate_wiki()` — assert no failures. Assert the page in the subdir
  was validated (e.g., a deliberate type violation surfaces as a fail).
- [x] Add `TestCheckWikiOrphansSkipsLogMd`: create `wiki/log.md` alongside
  a `_index.md` that does not list `log.md`. Call `check_wiki_orphans()` —
  assert `log.md` is not reported as an orphan.
- [x] Add `TestCheckWikiOrphansSubdirMessage`: create a subdir with an
  unlisted `.md`. Assert the issue message references `<subdir>/_index.md`,
  not `wiki/_index.md`.
- [x] Verify: `python -m pytest plugins/wiki/tests/test_wiki.py -v` — all
  tests pass including new ones.
- [x] Commit: `test(wiki): recursive validation and log.md exclusion tests (#277, #275)` <!-- sha:73a2a97 -->

---

### Task 4: Tests for wiki reindex mode

**Files:**
- Modify: `plugins/wiki/tests/test_reindex.py`

- [x] Update `TestReindexDoesNotTouchWikiInventory`: rename to
  `TestReindexWikiMode`. Replace the "wiki not touched" assertion with:
  when `wiki/SCHEMA.md` is present, reindex DOES generate `wiki/_index.md`
  and per-subdir `_index.md` files.
- [x] Add test: `wiki/` with one subdirectory produces `wiki/<subdir>/_index.md`
  and `wiki/_index.md` with a `## <subdir>` heading.
- [x] Add test: `wiki/log.md` is not listed in any generated `_index.md`.
- [x] Add test: when `wiki/SCHEMA.md` is absent, `wiki/` is not touched.
- [x] Verify: `python -m pytest plugins/wiki/tests/test_reindex.py -v` — all
  tests pass.
- [x] Commit: `test(wiki): reindex wiki subtree mode tests (#277, #275)` <!-- sha:73971b3 -->

---

### Chunk 2: Ingest SKILL.md — four behavioural additions

All four tasks modify the same file: `plugins/wiki/skills/ingest/SKILL.md`.
Execute sequentially. Each commit is independently verifiable by reading the file.

---

### Task 5: Ingest — read wiki directory tree and propose emergent paths (#277)

**Files:**
- Modify: `plugins/wiki/skills/ingest/SKILL.md`

- [x] In "Pre-Ingest", extend step 1 ("Read `wiki/_index.md`") to also list
  the `wiki/` directory tree (e.g., `ls -R wiki/` or equivalent) so the LLM
  understands existing subdirectory groupings before proposing new page paths.
- [x] In "Step 1: Identify Affected Pages", add: for new pages, propose a
  path that fits contextually within the existing `wiki/` structure —
  `wiki/<topic-dir>/<slug>.md`. Explain that the path is editable by the
  user at Step 1b.
- [x] In "Step 1b: Confirm Before Writing", update the example to show a
  subdirectory path (`CREATE wiki/llm-patterns/consistency-tradeoffs.md`).
- [x] Verify: read `plugins/wiki/skills/ingest/SKILL.md` — confirm the three
  edits are present and coherent.
- [x] Commit: `feat(wiki): ingest proposes emergent subdirectory paths (#277)` <!-- sha:38b4498 -->

---

### Task 6: Ingest — discuss-before-write by default (#278)

**Files:**
- Modify: `plugins/wiki/skills/ingest/SKILL.md`

- [x] In "Ingest Protocol", insert a new **Step 0: Discuss Key Takeaways**
  before Step 1. Default behaviour (no flag): after reading the source(s),
  present key takeaways and ask the user to confirm. Bulk mode (multiple
  sources): one consolidated discussion for all sources, not one per source.
  Opt-out: `--no-discuss` flag skips this step and jumps directly to Step 1.
- [x] Add the discussion prompt template from the design:
  ```
  Here are the key takeaways from [Source Title]:
  - ...
  Does this capture the important ideas? Anything missing or worth
  emphasizing differently before I propose the page list?
  ```
- [x] Add an "Anti-Pattern Guard" entry: running a separate discussion round
  per source in bulk mode is wrong — consolidate into one pass.
- [x] Verify: read `plugins/wiki/skills/ingest/SKILL.md` — confirm Step 0
  appears before Step 1, bulk and `--no-discuss` behaviour documented.
- [x] Commit: `feat(wiki): discuss-before-write by default (#278)` <!-- sha:798f6a3 -->

---

### Task 7: Ingest — source summary page per ingest (#276)

**Files:**
- Modify: `plugins/wiki/skills/ingest/SKILL.md`

- [x] In "Step 1: Identify Affected Pages", add: always include one
  source summary page for the ingested source (create or update). Idempotency
  rule: if a source summary page already exists for this URL (matched by
  `sources:` frontmatter), update it rather than creating a duplicate —
  append new claims, never remove existing ones.
- [x] In "Step 3: Create New Pages" (or a new "Step 3a: Create Source Summary
  Page"), document the source summary page format from the design: frontmatter
  fields (`name`, `description`, `type: source-summary`, `sources`, `created`,
  `updated`) plus body sections (Author/Date/URL metadata, Key Claims,
  Summary). State the factual-only constraint explicitly: no interpretation,
  synthesis, or evaluation.
- [x] Add an "Anti-Pattern Guard": writing interpretation or synthesis into
  a source summary page (those belong in concept/synthesis pages).
- [x] Verify: read `plugins/wiki/skills/ingest/SKILL.md` — confirm source
  summary page step is present, factual-only constraint stated, idempotency
  rule documented.
- [x] Commit: `feat(wiki): source summary page per ingest (#276)` <!-- sha:76fc13f -->

---

### Task 8: Ingest — operation log append (#275)

**Files:**
- Modify: `plugins/wiki/skills/ingest/SKILL.md`

- [x] In "Post-Ingest", after the `lint.py` and `reindex.py` commands, add a
  step: append an entry to `wiki/log.md`. Create the file if it doesn't exist.
  Document the entry format:
  ```
  ## [YYYY-MM-DD] ingest | <Source Title>
  <N> pages updated, <M> created. Pages: wiki/path/a.md, wiki/path/b.md.
  ```
- [x] State the append-only constraint: existing entries are never modified.
- [x] Verify: read `plugins/wiki/skills/ingest/SKILL.md` — confirm log append
  step and format are present in Post-Ingest.
- [x] Commit: `feat(wiki): operation log append in ingest (#275)` <!-- sha:29e1346 -->

---

### Chunk 3: Lint SKILL.md — log append

---

### Task 9: Lint — operation log append (#275)

**Files:**
- Modify: `plugins/wiki/skills/lint/SKILL.md`

- [x] In "How to Run" or a new "Post-Lint" section, add: after reporting
  results, append an entry to `wiki/log.md` (create if missing). Format:
  ```
  ## [YYYY-MM-DD] lint | <summary>
  <N> issues found: <brief description>. (or: No issues.)
  ```
  Append-only: existing entries are never modified.
- [x] Verify: read `plugins/wiki/skills/lint/SKILL.md` — confirm log append
  step is present with correct format.
- [x] Commit: `feat(wiki): operation log append in lint (#275)` <!-- sha:c704491 -->

---

## Validation

- [x] `python -m pytest plugins/wiki/tests/ -v` — all tests pass, including
  new recursive validation and reindex wiki mode tests
- [x] `python -m pytest plugins/wiki/tests/test_wiki.py -k "log"` — at least
  one test verifies `log.md` is excluded from orphan checks
- [x] `python -m pytest plugins/wiki/tests/test_reindex.py -k "wiki"` — at
  least one test verifies wiki subtree reindex produces per-subdir `_index.md`
- [x] Read `plugins/wiki/skills/ingest/SKILL.md` — confirm four additions
  present: (1) wiki dir tree read + emergent paths, (2) discuss step with
  bulk mode and `--no-discuss`, (3) source summary page with factual-only
  constraint, (4) log append
- [x] Read `plugins/wiki/skills/lint/SKILL.md` — confirm log append step
  present with correct format
- [x] `ruff check plugins/wiki/src/ plugins/wiki/scripts/` — no errors
