---
name: Agent Skills Metadata Superset Alignment
description: Move WOS document fields (except name/description) into a metadata map, as a superset of the Agent Skills spec
metadata:
  type: plan
  status: completed
  related:
    - docs/context/instruction-file-conventions.md
    - docs/context/agents-md-standard.md
---

# Agent Skills Metadata Superset Alignment

**Goal:** Adopt the Agent Skills frontmatter convention — `name` and `description` top-level, everything else under `metadata` — across all WOS documents. WOS extends the spec by allowing lists and nested values in `metadata` (Agent Skills restricts to `dict[str, str]`). The Document dataclass flattens `metadata` fields into attributes so downstream code (validators, assessors, index) is unchanged.

**Scope:**

Must have:
- Parser support for nested `metadata` map in `frontmatter.py`
- `parse_document()` resolves fields from `metadata.*` with fallback to top-level (backward compat)
- All existing tests pass with both flat and nested frontmatter formats
- New tests for the `metadata` format
- Migration script to rewrite existing docs from flat to nested format
- Updated reference docs (plan-format, plan-template, AGENTS.md metadata format)

Won't have:
- Strict Agent Skills validation (rejecting unknown top-level fields) — WOS remains lenient
- Changes to `skill_audit.py`'s regex-based parser — it only reads `name`/`description`, which stay top-level
- Removal of flat-format support — both formats work indefinitely
- Changes to downstream consumers (`validators.py`, `assess_research.py`, `assess_plan.py`, `index.py`) — the flattening in `document.py` shields them

**Approach:** Two-layer change. First, teach the YAML subset parser to recognize one level of nesting (the `metadata` key only — not arbitrary nested dicts). Second, update `parse_document()` to check `metadata.*` before top-level for each known field. The Document dataclass doesn't change. Downstream code accesses `doc.type`, `doc.sources`, etc. as before — the nesting is a serialization concern hidden by the parser. A migration script rewrites existing frontmatter in-place. Reference docs update to show the new canonical format.

**File Changes:**
- Modify: `wos/frontmatter.py` — add nested dict support for `metadata` key
- Modify: `wos/document.py` — resolve fields from `metadata` with top-level fallback
- Modify: `tests/test_frontmatter.py` — add tests for `metadata` nested parsing
- Modify: `tests/test_document.py` — add tests for metadata-format documents, verify backward compat
- Create: `scripts/migrate_frontmatter.py` — rewrite flat frontmatter to metadata format
- Modify: `skills/_shared/references/plan-format.md` — update frontmatter schema examples
- Modify: `skills/write-plan/references/plan-template.md` — update template
- Modify: `AGENTS.md` — update File Metadata Format section

**Branch:** `feat/211-metadata-superset`
**PR:** TBD

---

### Task 1: Add nested dict parsing to frontmatter.py

**Files:**
- Modify: `wos/frontmatter.py`
- Modify: `tests/test_frontmatter.py`

The parser currently handles scalars, lists, and null — no nested dicts. Add support for a single nesting level: when a key's value is empty (like `metadata:`) and the following lines are indented key-value pairs or key-list pairs, collect them into a dict.

The detection logic: after seeing `metadata:` (null value), if the next non-blank line is indented and contains a colon, treat subsequent indented lines as a nested map. List items (`- value`) within the nested map attach to the most recent nested key, same as top-level lists.

- [ ] **Step 1:** Modify `_parse_yaml_subset()` to detect indented key-value pairs following a null-valued key. Collect them into a nested dict. Support scalars, lists, and null values inside the nested dict. Only support one level of nesting — this is not a general YAML parser.
- [ ] **Step 2:** Add tests to `test_frontmatter.py`:
  - `metadata` with scalar values parses to `{"metadata": {"type": "plan", "status": "draft"}}`
  - `metadata` with list values parses to `{"metadata": {"sources": ["url1", "url2"]}}`
  - `metadata` with mixed scalar and list values
  - `metadata` with null values inside
  - Non-metadata nested keys also work (parser is general, not metadata-specific)
  - Existing flat-format tests still pass
- [ ] **Step 3:** Verify: `python -m pytest tests/test_frontmatter.py -v` — all pass
- [ ] **Step 4:** Commit

---

### Task 2: Resolve metadata fields in parse_document()

**Files:**
- Modify: `wos/document.py`
- Modify: `tests/test_document.py`

Update `parse_document()` to check `fm.get("metadata", {})` first, then fall back to top-level `fm.get()` for each known field (`type`, `sources`, `related`, `status`, `created_at`, `updated_at`). The Document dataclass stays unchanged — same attributes, same types.

Resolution order for each field: `metadata.{field}` → top-level `{field}` → default.

- [ ] **Step 1:** Extract a helper `_resolve(fm, key, default=None)` that checks `fm.get("metadata", {}).get(key)` then `fm.get(key)` then returns default. Use it for all optional field lookups.
- [ ] **Step 2:** Add tests to `test_document.py`:
  - Document with all fields in `metadata` parses correctly
  - Document with flat format still parses correctly (backward compat)
  - Document with mixed (some flat, some in metadata) works — metadata wins
  - `name` and `description` are always top-level (not resolved from metadata)
  - Null `metadata` key with no nested content doesn't break anything
- [ ] **Step 3:** Verify: `python -m pytest tests/test_document.py -v` — all pass
- [ ] **Step 4:** Verify: `python -m pytest tests/ -v` — full suite passes (validators, index, etc. unchanged)
- [ ] **Step 5:** Commit

---

### Task 3: Create migration script

**Files:**
- Create: `scripts/migrate_frontmatter.py`

Script reads all WOS-managed `.md` files, rewrites frontmatter from flat to metadata format. `name` and `description` stay top-level. Everything else moves under `metadata`. Body content is preserved exactly. Idempotent — running twice produces the same output.

- [ ] **Step 1:** Implement `migrate_frontmatter.py` with:
  - `--root` flag (default CWD)
  - `--dry-run` flag (print changes without writing)
  - `--check` flag (exit 1 if any files need migration, for CI)
  - Plugin root discovery pattern (same as other scripts)
  - For each `.md` file with frontmatter: parse, restructure, re-serialize, write
  - Skip files that already use `metadata` format
  - Skip `_index.md`, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `README.md`
- [ ] **Step 2:** Run with `--dry-run` on the WOS repo itself to verify output looks correct
- [ ] **Step 3:** Commit

---

### Task 4: Migrate existing WOS docs

**Depends on:** Task 3

- [ ] **Step 1:** Run `python scripts/migrate_frontmatter.py --root .` on the WOS repo
- [ ] **Step 2:** Verify: `python -m pytest tests/ -v` — full suite still passes (backward compat in parser means migrated docs parse identically)
- [ ] **Step 3:** Verify: `python scripts/audit.py --root . --no-urls` — no new issues
- [ ] **Step 4:** Spot-check 3-4 migrated files manually — `name`/`description` top-level, everything else under `metadata`, body untouched
- [ ] **Step 5:** Commit

---

### Task 5: Update reference docs and templates

**Files:**
- Modify: `skills/_shared/references/plan-format.md`
- Modify: `skills/write-plan/references/plan-template.md`
- Modify: `AGENTS.md` (File Metadata Format section)

Update all examples and templates to show the new canonical format with `metadata`.

- [ ] **Step 1:** Update `plan-format.md` frontmatter schema example and field descriptions
- [ ] **Step 2:** Update `plan-template.md` copyable skeleton
- [ ] **Step 3:** Update AGENTS.md `### File Metadata Format` code block
- [ ] **Step 4:** Verify no other reference docs show frontmatter examples (search for `type: plan`, `type: research`, `sources:` in skills/ references)
- [ ] **Step 5:** Commit

---

## Validation

- [ ] `python -m pytest tests/ -v` — all tests pass
- [ ] `python scripts/audit.py --root . --no-urls` — no new issues from migration
- [ ] `python scripts/migrate_frontmatter.py --root . --check` — exit 0 (all docs already migrated)
- [ ] Parse a flat-format document — still works (backward compat)
- [ ] Parse a metadata-format document — fields resolve correctly
- [ ] Grep for top-level `type:`, `sources:`, `related:`, `status:` in `docs/` — only appears inside `metadata` block (migration complete)
