---
name: Timestamps and Date Prefix Removal
description: Add created_at/updated_at frontmatter fields and remove date prefixes from filenames
type: plan
status: completed
related:
  - https://github.com/bcbeidel/wos/issues/199
  - https://github.com/bcbeidel/wos/issues/200
---

# Timestamps and Date Prefix Removal

**Goal:** Move date information from filenames into frontmatter. Documents get
`created_at` and `updated_at` fields (ISO 8601 strings), and the `YYYY-MM-DD-`
filename prefix convention is removed. This pairs the two changes so dates
aren't lost during the rename.

**Scope:**

Must have:
- `created_at` and `updated_at` as Optional[str] fields on Document dataclass
- ISO 8601 date format validation in validators
- All date-prefixed filenames renamed (prefix stripped)
- `related` frontmatter cross-references updated to match new filenames
- Indexes regenerated
- All tests pass after changes

Won't have:
- Auto-population of timestamps (future tooling concern)
- Migration script for external repos using WOS
- `updated_at` auto-update on file save (hook concern)

**Approach:** Two chunks. First, add the timestamp fields to the data model
and validator — this is additive and backward-compatible. Second, rename all
date-prefixed files, update cross-references, fix test fixtures, and
regenerate indexes. Order matters: timestamps exist before renames so we can
backfill `created_at` during the rename step.

**File Changes:**
- Modify: `wos/document.py` (add fields to dataclass and `_KNOWN_FIELDS`)
- Modify: `wos/validators.py` (add ISO 8601 format check)
- Modify: `tests/test_document.py` (timestamp parsing tests)
- Modify: `tests/test_validators.py` (timestamp validation tests)
- Modify: `tests/test_suffix.py` (remove date prefixes from test paths)
- Modify: `tests/test_index.py` (remove date prefix from test fixture)
- Modify: `tests/test_research_assess.py` (remove date prefixes from test fixtures)
- Rename: `docs/designs/2026-03-13-cross-platform-deploy-design.md` → `cross-platform-deploy-design.md`
- Rename: `docs/plans/2026-03-13-cross-platform-deploy.md` → `cross-platform-deploy.plan.md`
- Modify: `docs/plans/cross-platform-deploy.plan.md` (update related paths, add timestamps)
- Modify: `docs/designs/cross-platform-deploy-design.md` (update related paths, add timestamps)
- Regenerate: `docs/plans/_index.md`, `docs/designs/_index.md`, `docs/research/_index.md`

**Branch:** `cross-platform-deploy` (current)
**PR:** TBD

---

## Chunk 1: Timestamp Fields

### Task 1: Add created_at and updated_at to Document model

**Files:**
- Modify: `wos/document.py`
- Test: `tests/test_document.py`

- [x] **Step 1:** Add `created_at` and `updated_at` to `_KNOWN_FIELDS` set in `document.py` <!-- sha:779659d -->
- [x] **Step 2:** Add `created_at: Optional[str] = None` and `updated_at: Optional[str] = None` fields to the `Document` dataclass <!-- sha:779659d -->
- [x] **Step 3:** Extract `created_at` and `updated_at` from frontmatter in `parse_document()`, same pattern as `status` <!-- sha:779659d -->
- [x] **Step 4:** Add tests: parsing documents with timestamps, without timestamps (backward compat), timestamps appear in Document fields <!-- sha:779659d -->
- [x] **Step 5:** Verify: `python -m pytest tests/test_document.py -v` — all pass <!-- sha:779659d -->
- [x] **Step 6:** Commit <!-- sha:779659d -->

---

### Task 2: Add ISO 8601 date validation

**Files:**
- Modify: `wos/validators.py`
- Test: `tests/test_validators.py`

- [x] **Step 1:** Add `check_timestamps()` function in `validators.py` that validates `created_at` and `updated_at` are valid ISO 8601 date strings (YYYY-MM-DD) when present. Severity: `warn` for invalid format. <!-- sha:7c104cc -->
- [x] **Step 2:** Wire `check_timestamps()` into `validate_file()` alongside other checks <!-- sha:7c104cc -->
- [x] **Step 3:** Add tests: valid dates pass, invalid dates warn, missing dates are fine, `updated_at` before `created_at` warns <!-- sha:7c104cc -->
- [x] **Step 4:** Verify: `python -m pytest tests/test_validators.py -v` — all pass <!-- sha:7c104cc -->
- [x] **Step 5:** Commit <!-- sha:7c104cc -->

---

## Chunk 2: Remove Date Prefixes

### Task 3: Rename date-prefixed files and update cross-references

**Files:**
- Rename: `docs/designs/2026-03-13-cross-platform-deploy-design.md`
- Rename: `docs/plans/2026-03-13-cross-platform-deploy.md`
- Modify: renamed files' `related` frontmatter

- [x] **Step 1:** Rename `docs/designs/2026-03-13-cross-platform-deploy-design.md` → `docs/designs/cross-platform-deploy-design.md` <!-- sha:35ee18d -->
- [x] **Step 2:** Rename `docs/plans/2026-03-13-cross-platform-deploy.md` → `docs/plans/cross-platform-deploy.plan.md` <!-- sha:35ee18d -->
- [x] **Step 3:** Add `created_at: 2026-03-13` to both renamed files' frontmatter <!-- sha:35ee18d -->
- [x] **Step 4:** Update `related` fields in both files — remove `2026-03-13-` prefix from all cross-references. Remove references to missing research files if they no longer exist. <!-- sha:35ee18d -->
- [x] **Step 5:** Verify: `ls docs/designs/ docs/plans/` — no date-prefixed files remain <!-- sha:35ee18d -->
- [x] **Step 6:** Commit <!-- sha:35ee18d -->

---

### Task 4: Update test fixtures

**Files:**
- Modify: `tests/test_suffix.py`
- Modify: `tests/test_document.py`
- Modify: `tests/test_index.py`
- Modify: `tests/test_validators.py`
- Modify: `tests/test_research_assess.py`

- [x] **Step 1:** In `test_suffix.py`: change `2026-03-13-deploy.plan.md` → `deploy.plan.md`, `2026-03-13-cross-platform.design.md` → `cross-platform.design.md`, update expected stem_name outputs accordingly <!-- sha:72d4f46 -->
- [x] **Step 2:** In `test_document.py`: change `2026-02-20-api-review.md` → `api-review.md`, `2026-03-13-deploy.plan.md` → `deploy.plan.md`, `2026-03-13-feature.design.md` → `feature.design.md` <!-- sha:72d4f46 -->
- [x] **Step 3:** In `test_index.py`: change `2026-03-13-api.research.md` → `api.research.md` <!-- sha:72d4f46 -->
- [x] **Step 4:** In `test_validators.py`: change `2026-03-13-api.research.md` → `api.research.md` in compound suffix tests <!-- sha:72d4f46 -->
- [x] **Step 5:** In `test_research_assess.py`: change any `2026-03-` prefixed filenames to unprefixed versions <!-- sha:72d4f46 -->
- [x] **Step 6:** Verify: `python -m pytest tests/ -v` — all tests pass <!-- sha:72d4f46 -->
- [x] **Step 7:** Commit <!-- sha:72d4f46 -->

---

### Task 5: Regenerate indexes and clean up

**Files:**
- Regenerate: `docs/plans/_index.md`, `docs/designs/_index.md`, `docs/research/_index.md`

- [x] **Step 1:** Run `python scripts/reindex.py` to regenerate all `_index.md` files <!-- sha:8aec4dd -->
- [x] **Step 2:** Verify: `python scripts/audit.py --no-urls` — no index sync failures <!-- sha:8aec4dd -->
- [x] **Step 3:** Commit <!-- sha:8aec4dd -->

---

## Validation

- [x] `python -m pytest tests/ -v` — 370 passed
- [x] `python scripts/audit.py --no-urls` — no fail-severity issues from our changes (pre-existing prompts index desync only)
- [x] `git diff --name-only main` — no files with `YYYY-MM-DD-` prefix pattern remain in docs/
- [x] `grep -r "2026-03-13-" tests/` — zero matches
