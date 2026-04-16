---
name: Metadata Correctness and Lint Accuracy Batch Fix
description: Fix five open bugs causing skill enumeration failures, false-positive lint results, a broken skill chain reference, and unusable static-check tooling.
type: plan
status: executing
branch: fix/metadata-correctness-lint-accuracy
related:
  - docs/designs/2026-04-16-metadata-correctness-lint-accuracy.design.md
---

# Metadata Correctness and Lint Accuracy Batch Fix

## Goal

Fix five open bugs (#291–#295) that cause skill enumeration failures, false-positive lint output, a broken skill chain reference, and an unusable static-check step. All changes are surgical edits to existing files — no new files, no new abstractions.

## Scope

Must have:
- Add `"tests"` to `_SKIP` in `Document.scan()` so `wiki:lint` ignores test fixtures (#292)
- Add `name:` and `user-invocable: true` to all 17 consider skill SKILL.md files (#293)
- Fix `name: check-work` → `name: verify-work` in verify-work frontmatter; fix `Chainable to: check-work` → `Chainable to: verify-work` in start-work Handoff (#294)
- Replace single co-located test file instruction in build-rule Step 8 with a format-specific path table (#295)
- Fix check-skill SKILL.md: correct script path to `<plugin-scripts-dir>/../../src/check/lint.py`, `python` → `python3`, add install prerequisite (#291)

Won't have:
- New entry points, wrappers, or scripts
- Regression tests for frontmatter completeness
- Renaming the verify-work directory

## Approach

Five independent fixes, ordered from Python source (safest to verify with existing tests) to SKILL.md text edits. No cross-task dependencies — each task is a standalone commit. Task 1 is the only Python change; tasks 2–5 are Markdown-only.

## File Changes

- Modify: `plugins/wiki/src/wiki/document.py` (add `"tests"` to `_SKIP`)
- Modify: `plugins/consider/skills/10-10-10/SKILL.md`
- Modify: `plugins/consider/skills/5-whys/SKILL.md`
- Modify: `plugins/consider/skills/circle-of-competence/SKILL.md`
- Modify: `plugins/consider/skills/consider/SKILL.md`
- Modify: `plugins/consider/skills/eisenhower-matrix/SKILL.md`
- Modify: `plugins/consider/skills/first-principles/SKILL.md`
- Modify: `plugins/consider/skills/hanlons-razor/SKILL.md`
- Modify: `plugins/consider/skills/inversion/SKILL.md`
- Modify: `plugins/consider/skills/map-vs-territory/SKILL.md`
- Modify: `plugins/consider/skills/occams-razor/SKILL.md`
- Modify: `plugins/consider/skills/one-thing/SKILL.md`
- Modify: `plugins/consider/skills/opportunity-cost/SKILL.md`
- Modify: `plugins/consider/skills/pareto/SKILL.md`
- Modify: `plugins/consider/skills/reversibility/SKILL.md`
- Modify: `plugins/consider/skills/second-order/SKILL.md`
- Modify: `plugins/consider/skills/swot/SKILL.md`
- Modify: `plugins/consider/skills/via-negativa/SKILL.md`
- Modify: `plugins/work/skills/verify-work/SKILL.md`
- Modify: `plugins/work/skills/start-work/SKILL.md`
- Modify: `plugins/build/skills/build-rule/SKILL.md`
- Modify: `plugins/build/skills/check-skill/SKILL.md`

**Branch:** `fix/metadata-correctness-lint-accuracy`
**PR:** closes #291, #292, #293, #294, #295

## Tasks

---

### Task 1: Fix wiki:lint false positives on test fixtures (#292)

- [x] Add `"tests"` to `_SKIP` in `Document.scan()`, verify tests pass and lint produces no fixtures output, commit <!-- sha:c783d2f -->

In `plugins/wiki/src/wiki/document.py`, locate the `_SKIP` frozenset inside `Document.scan()` (around line 266) and add `"tests"` to it:

```python
_SKIP = frozenset({
    "node_modules", "__pycache__", "venv", ".venv",
    "dist", "build", ".tox", ".mypy_cache", ".pytest_cache",
    "tests",
})
```

**Verify:**
```bash
python3 -m pytest plugins/wiki/tests/ -v -x
python3 plugins/wiki/scripts/lint.py --root . 2>&1 | grep "tests/fixtures"
# second command should produce no output
```

Commit: `fix(wiki): exclude tests/ from Document.scan skip list (#292)`

---

### Task 2: Add required frontmatter to all 17 consider skills (#293)

- [x] Add `name:` and `user-invocable: true` to all 17 consider SKILL.md files, verify no files missing fields, commit <!-- sha:37919e7 -->

For each skill directory under `plugins/consider/skills/`, open its `SKILL.md` and insert `name: <directory-name>` and `user-invocable: true` into the frontmatter block. The directory names are:

`10-10-10`, `5-whys`, `circle-of-competence`, `consider`, `eisenhower-matrix`, `first-principles`, `hanlons-razor`, `inversion`, `map-vs-territory`, `occams-razor`, `one-thing`, `opportunity-cost`, `pareto`, `reversibility`, `second-order`, `swot`, `via-negativa`

Each frontmatter should look like (example for `pareto`):
```yaml
---
name: pareto
description: Apply the 80/20 rule...
argument-hint: "[area where effort and results feel misaligned]"
user-invocable: true
---
```

**Verify:**
```bash
grep -rL "^name:" plugins/consider/skills/*/SKILL.md
# should produce no output (all files have name:)
grep -rL "user-invocable:" plugins/consider/skills/*/SKILL.md
# should produce no output (all files have user-invocable:)
```

Commit: `fix(consider): add name and user-invocable frontmatter to all 17 skills (#293)`

---

### Task 3: Fix verify-work name mismatch and start-work chain reference (#294)

- [x] Fix `name: check-work` → `name: verify-work` in verify-work SKILL.md and `Chainable to: check-work` → `verify-work` in start-work Handoff, verify, commit <!-- sha:5f2b5c3 -->

**File 1:** `plugins/work/skills/verify-work/SKILL.md`
- Change frontmatter `name: check-work` → `name: verify-work`

**File 2:** `plugins/work/skills/start-work/SKILL.md`
- In the `## Handoff` section, change `**Chainable to:** check-work` → `**Chainable to:** verify-work`

**Verify:**
```bash
grep "^name:" plugins/work/skills/verify-work/SKILL.md
# → name: verify-work
grep "Chainable to:" plugins/work/skills/start-work/SKILL.md
# → **Chainable to:** verify-work
```

Commit: `fix(work): correct verify-work name and start-work chain reference (#294)`

---

### Task 4: Fix build-rule test file placement for Claude Code format (#295)

- [x] Replace single co-located test file instruction in build-rule Step 8 with format-specific path table, verify table present, commit <!-- sha:9427c66 -->

In `plugins/build/skills/build-rule/SKILL.md`, locate Step 8 "Write the Rule". Replace the single co-located test file instruction:

> `Write a co-located test file at <same-dir>/<slug>.tests.md ...`

with a format-specific path table prepended before the existing instruction text:

```
Write the test file at the format-specific location:

| Format | Test file location |
|--------|--------------------|
| WOS | `docs/rules/<slug>.tests.md` |
| Cursor | `.cursor/rules/<slug>.tests.md` |
| Claude Code | `docs/rules/<slug>.tests.md` (create directory if needed) |
```

Keep the existing instruction about minimum 3 PASS / 3 FAIL cases and the Rule Testing Guide reference — only the path specification changes.

**Verify:**
```bash
grep -A6 "Test file location" plugins/build/skills/build-rule/SKILL.md
# should show the three-row table with WOS, Cursor, Claude Code rows
```

Commit: `fix(build): add format-specific test file path table to build-rule Step 8 (#295)`

---

### Task 5: Fix check-skill static-check script reference (#291)

- [x] Fix script path to `<plugin-scripts-dir>/../../src/check/lint.py`, `python` → `python3`, add install prerequisite in check-skill SKILL.md, verify, commit <!-- sha:716423f -->

In `plugins/build/skills/check-skill/SKILL.md`, locate Step 2 "Run Static Checks". Replace the broken command block:

```bash
python scripts/lint.py --root <project-root> --no-urls
```

with:

```bash
# Prerequisite: pip install -e plugins/build
python3 <plugin-scripts-dir>/../../src/check/lint.py --root <project-root> --no-urls
```

**Verify:**
```bash
grep "plugin-scripts-dir" plugins/build/skills/check-skill/SKILL.md
# → python3 <plugin-scripts-dir>/../../src/check/lint.py
grep "pip install" plugins/build/skills/check-skill/SKILL.md
# → # Prerequisite: pip install -e plugins/build
grep "python3" plugins/build/skills/check-skill/SKILL.md
# → python3 (not bare `python`)
```

Commit: `fix(build): correct check-skill static-check script path and add prerequisite (#291)`

---

## Validation

All five criteria from the design must hold before the PR is opened:

1. `python3 plugins/wiki/scripts/lint.py --root . 2>&1 | grep "tests/fixtures"` → no output
2. `grep -rL "^name:" plugins/consider/skills/*/SKILL.md` → no output
3. `grep "^name:" plugins/work/skills/verify-work/SKILL.md` → `name: verify-work`
4. `grep "Chainable to:" plugins/work/skills/start-work/SKILL.md` → `verify-work`
5. `grep "Test file location" plugins/build/skills/build-rule/SKILL.md` → table header present
6. `grep "plugin-scripts-dir" plugins/build/skills/check-skill/SKILL.md` → path present
7. `python3 -m pytest plugins/wiki/tests/ -v` → all tests pass
