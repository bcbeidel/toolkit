---
name: Skill and Script Renames (v0.36.0)
description: Rename audit-wos→lint, init-wos→setup, audit.py→lint.py, and update all cross-references
type: plan
status: completed
branch: feat/wiki-schema-infrastructure
pr: ~
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# Skill and Script Renames (v0.36.0)

Rename two skills and one script to cleaner, more universally-understood names,
then sweep all cross-references to leave zero old names in the codebase.

## Goal

Replace `audit-wos` → `lint`, `init-wos` → `setup`, `scripts/audit.py` →
`scripts/lint.py` across all code, docs, and skill files so no old names remain.
Update root documentation and add a v0.36.0 CHANGELOG entry.

## Scope

**Must have:**
- `skills/audit-wos/` → `skills/lint/` (git mv)
- `skills/init-wos/` → `skills/setup/` (git mv)
- `scripts/audit.py` → `scripts/lint.py` (git mv)
- `tests/test_audit.py` → `tests/test_lint.py` (git mv + import update)
- All `audit-wos`, `init-wos`, `audit.py` references replaced in 26 files
- `README.md`, `OVERVIEW.md`, `CHANGELOG.md` updated to reflect new names
- Full test suite green; `python scripts/lint.py --help` shows same flags

**Won't have:**
- Any functional changes to skill logic or script behavior
- Renaming other skills or scripts not in the issue
- Wiki schema work (separate issue #218)

## Approach

Sequential tasks: rename skills first (Tasks 1 and 3 are independent of each other
but both must precede the reference sweep). Rename the script and its test file
together (Task 2) to avoid an intermediate broken state. Sweep cross-references
last (Task 4) once both skills and the script are in final positions. Root doc
updates happen as part of Task 4.

Each task ends with a focused `pytest` run so failures surface close to their
cause; Task 4 ends with the full suite.

## File Changes

**Created:**
- `skills/lint/` — renamed from `skills/audit-wos/`
- `skills/setup/` — renamed from `skills/init-wos/`
- `scripts/lint.py` — renamed from `scripts/audit.py`
- `tests/test_lint.py` — renamed from `tests/test_audit.py`

**Deleted:**
- `skills/audit-wos/` (via git mv)
- `skills/init-wos/` (via git mv)
- `scripts/audit.py` (via git mv)
- `tests/test_audit.py` (via git mv)

**Modified** (cross-reference sweep — 26 files confirmed by grep):
- `skills/lint/SKILL.md` — name, description, trigger phrases, `audit.py` → `lint.py` command references
- `skills/setup/SKILL.md` — name field
- `tests/test_lint.py` — `from scripts.audit import` → `from scripts.lint import`, `"audit.py"` argv → `"lint.py"`
- `tests/test_script_syspath.py` — `audit.py` path references → `lint.py`
- `tests/test_deploy.py` — any `audit-wos`/`init-wos` skill name references
- `tests/test_skill_audit.py` — any `audit-wos`/`init-wos` skill name references
- `wos/validators.py` — any hardcoded skill name references
- `README.md` — skill list, invocation examples, skill ecosystem table
- `OVERVIEW.md` — skill list, skill ecosystem table, invocation examples
- `CHANGELOG.md` — add v0.36.0 entry documenting the renames
- `CLAUDE.md` — skill name references in Architecture section
- `PRINCIPLES.md` — any skill name references
- `DEPLOYING.md` — any `audit.py` / `audit-wos` references
- `skills/_shared/references/` — `audit.py` / `audit-wos` references in shared reference docs
- `skills/write-plan/references/` — `audit-wos`/`audit.py` references
- `skills/execute-plan/references/` — `audit-wos`/`audit.py` references
- Remaining files surfaced by the pre-sweep grep

## Tasks

### Task 1 — Rename `audit-wos` skill to `lint`

- [x] `git mv skills/audit-wos skills/lint` <!-- sha:25952f0 -->
- [x] Edit `skills/lint/SKILL.md`: set `name: lint`, update description to use "lint"/"lint checks" terminology, update trigger phrases (add "lint", "run lint", "check lint"), replace all `audit.py` command references with `lint.py` <!-- sha:25952f0 -->
- [x] Verify: `ls skills/lint/SKILL.md && ! ls skills/audit-wos 2>/dev/null && echo ok` <!-- sha:25952f0 -->
- [x] `python -m pytest tests/ -v --ignore=tests/test_audit.py --ignore=tests/test_script_syspath.py -k "not audit"` — existing tests pass <!-- sha:25952f0 -->
- [x] Commit: `rename: audit-wos skill → lint` <!-- sha:25952f0 -->

### Task 2 — Rename `scripts/audit.py` and its test to `lint.py`

- [x] `git mv scripts/audit.py scripts/lint.py` <!-- sha:54fbeb6 -->
- [x] `git mv tests/test_audit.py tests/test_lint.py` <!-- sha:54fbeb6 -->
- [x] Edit `tests/test_lint.py`: replace all `from scripts.audit import` with `from scripts.lint import`; replace all `"audit.py"` argv references with `"lint.py"` <!-- sha:54fbeb6 -->
- [x] Edit `tests/test_script_syspath.py`: rename class `TestAuditSysPath` → `TestLintSysPath`, update test method name, replace `"audit.py"` path reference with `"lint.py"` <!-- sha:54fbeb6 -->
- [x] Verify: `python scripts/lint.py --help` — shows flags `--root`, `--no-urls`, `--json`, `--fix`, `--strict`, `--context-max-words`, `--context-min-words`, `--skill-max-lines` <!-- sha:54fbeb6 -->
- [x] `python -m pytest tests/test_lint.py tests/test_script_syspath.py -v` — all tests pass <!-- sha:54fbeb6 -->
- [x] Commit: `rename: scripts/audit.py → scripts/lint.py, test_audit.py → test_lint.py` <!-- sha:54fbeb6 -->

### Task 3 — Rename `init-wos` skill to `setup`

- [x] `git mv skills/init-wos skills/setup` <!-- sha:afaeaf0 -->
- [x] Edit `skills/setup/SKILL.md`: set `name: setup` <!-- sha:afaeaf0 -->
- [x] Verify: `ls skills/setup/SKILL.md && ! ls skills/init-wos 2>/dev/null && echo ok` <!-- sha:afaeaf0 -->
- [x] `python -m pytest tests/ -v -k "not audit"` — existing tests pass <!-- sha:afaeaf0 -->
- [x] Commit: `rename: init-wos skill → setup` <!-- sha:afaeaf0 -->

### Task 4 — Sweep all remaining cross-references and update root docs

- [x] Run `grep -r "audit-wos\|init-wos\|audit\.py" --include="*.md" --include="*.py" . --exclude-dir=".git" -l` — enumerate all remaining files <!-- sha:5591a89 -->
- [x] Replace `audit-wos` → `lint`, `init-wos` → `setup`, `audit.py` → `lint.py` in every file returned, verifying each replacement is contextually correct <!-- sha:5591a89 -->
- [x] In `README.md` and `OVERVIEW.md`: update skill list, invocation examples, and skill ecosystem tables <!-- sha:5591a89 -->
- [x] In `CHANGELOG.md`: add v0.36.0 entry — "Renamed `audit-wos` → `lint`, `init-wos` → `setup`, `scripts/audit.py` → `scripts/lint.py`" <!-- sha:5591a89 -->
- [x] `python -m pytest tests/ -v` — full suite passes (399 passed, zero failures) <!-- sha:5591a89 -->
- [x] `python scripts/lint.py --root . --no-urls` — clean pass (no new failures introduced) <!-- sha:5591a89 -->
- [x] Commit: `chore: update all audit-wos/init-wos/audit.py references to lint/setup/lint.py` <!-- sha:5591a89 -->

## Validation

```bash
# Zero old names remaining
grep -r "audit-wos\|init-wos\|audit\.py" --include="*.md" --include="*.py" . --exclude-dir=".git"
# Expected: zero matches

# New skill directories exist
ls skills/lint/SKILL.md skills/setup/SKILL.md
# Expected: both files present

# lint.py has identical flags to old audit.py
python scripts/lint.py --help
# Expected: --root, --no-urls, --json, --fix, --strict, --context-max-words,
#           --context-min-words, --skill-max-lines all present

# Full test suite clean
python -m pytest tests/ -v
# Expected: zero failures

# Self-lint passes
python scripts/lint.py --root . --no-urls
# Expected: no new failures
```
