---
name: Metadata Correctness and Lint Accuracy Batch Fix
description: Fix five open bugs causing skill enumeration failures, false-positive lint results, a broken skill chain reference, and unusable static-check tooling.
type: design
status: approved
related:
  - docs/context/
---

# Metadata Correctness and Lint Accuracy Batch Fix

## Purpose

Fix five open bugs that cause skill enumeration failures, false-positive lint results, a broken skill chain reference, and unusable static-check tooling. All fixes are surgical — no new abstractions or tooling.

## Fixes in Scope

### #291 — build:check-skill references non-existent scripts/lint.py

**File:** `plugins/build/skills/check-skill/SKILL.md`

- Replace hardcoded `scripts/lint.py` with `<plugin-scripts-dir>/../../src/check/lint.py`
- Replace `python` with `python3`
- Add install prerequisite note (`pip install -e plugins/build`)

### #292 — wiki:lint false positives on test fixtures

**File:** `plugins/wiki/src/wiki/document.py`

- Add `"tests"` to the `_SKIP` frozenset in `Document.scan()`

### #293 — consider plugin: all 17 skills missing required frontmatter fields

**Files:** `plugins/consider/skills/*/SKILL.md` (all 17 files)

- Add `name: <directory-name>` frontmatter field to each skill
- Add `user-invocable: true` frontmatter field to each skill

### #294 — work plugin: verify-work name mismatch

**Files:**
- `plugins/work/skills/verify-work/SKILL.md` — change `name: check-work` → `name: verify-work`
- `plugins/work/skills/start-work/SKILL.md` — change `Chainable to: check-work` → `Chainable to: verify-work`

### #295 — build:build-rule test file placement ambiguous for Claude Code format

**File:** `plugins/build/skills/build-rule/SKILL.md`

Replace the single co-located test file instruction in Step 8 with a format-specific path table:

| Format | Test file location |
|--------|--------------------|
| WOS | `docs/rules/<slug>.tests.md` |
| Cursor | `.cursor/rules/<slug>.tests.md` |
| Claude Code | `docs/rules/<slug>.tests.md` |

## Won't Do

- No new entry points, wrappers, or scripts
- No regression tests (separate concern, separate issue)
- No renaming of the verify-work directory

## Acceptance Criteria

- `/wiki:lint` on the toolkit root reports 0 findings from `tests/fixtures/`
- `Document.parse()` succeeds on all consider `SKILL.md` files
- `/work:verify-work` is reachable via its registered name; start-work Handoff references `verify-work`
- `check-skill` SKILL.md references a valid, `python3`-compatible script path with install prerequisite documented
- `build-rule` Step 8 unambiguously defines test file location for all three formats
