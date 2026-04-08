---
name: Challenge Skill Simplification
description: Remove Python discovery module from /wos:challenge — let the LLM use AGENTS.md + indexes instead of keyword matching
type: plan
status: complete
related:
  - docs/plans/2026-03-23-challenge-skill.plan.md
  - docs/designs/2026-03-23-challenge-skill.design.md
---

# /wos:challenge Simplification Plan

**Goal:** Remove the Python discovery module (`wos/challenge/`, `scripts/discover_context.py`, and tests) from the challenge skill. Replace the script-based Phase 2 with LLM-driven document search using AGENTS.md and indexes. The skill becomes a pure SKILL.md + reference docs skill with no Python code.

**Rationale:** The LLM reading AGENTS.md indexes outperforms keyword-overlap scoring — it understands synonyms, context, and intent. The Python module adds 543 lines of code and tests for capability the LLM handles natively.

**Branch:** `refactor/challenge-simplification`

---

## Scope

**Must:**
- Remove `wos/challenge/` subpackage
- Remove `scripts/discover_context.py`
- Remove `tests/test_challenge_discover.py` and `tests/test_discover_context_script.py`
- Rewrite SKILL.md Phase 2 to use AGENTS.md + Read/Grep
- Update CLAUDE.md architecture section (subpackage count)
- Update CHANGELOG.md under [Unreleased]

**Won't:**
- Change the four-phase workflow structure
- Modify reference docs (assumption-quality.md, gap-analysis-guide.md)
- Bump version (this is a simplification, version bump happens at release)

---

## Tasks

### Task 1: Create branch and remove Python files

- [x] Create branch `refactor/challenge-simplification`
- [x] Delete `wos/challenge/__init__.py`
- [x] Delete `wos/challenge/discover.py`
- [x] Delete `scripts/discover_context.py`
- [x] Delete `tests/test_challenge_discover.py`
- [x] Delete `tests/test_discover_context_script.py`
- [x] Verify: `find wos/challenge -type f` returns nothing; `ls scripts/discover_context.py tests/test_challenge_discover.py tests/test_discover_context_script.py` all fail

### Task 2: Update SKILL.md Phase 2

Replace the script invocation with LLM-driven search instructions. Keep all other phases unchanged.

- [x] Rewrite Phase 2 in `skills/challenge/SKILL.md`
- [x] Verify: SKILL.md contains no references to `discover_context.py`, `<plugin-scripts-dir>`, or `wos/challenge`

### Task 3: Update CLAUDE.md architecture

- [x] Change `12 modules + 2 subpackages` to `12 modules + 2 subpackages` → correct count after removal (12 modules + 2 subpackages — challenge was the 3rd)
- [x] Remove `discover_context.py` from the scripts list if present
- [x] Verify: no references to `wos/challenge` or `discover_context` in CLAUDE.md

### Task 4: Update CHANGELOG

- [x] Add entry under `[Unreleased]` documenting the simplification
- [x] Verify: changelog entry accurately describes what was removed and why

### Task 5: Run validation

- [x] `python -m pytest tests/ -v` — all tests pass (removed tests should not cause failures)
- [x] `ruff check wos/ tests/ scripts/` — no lint errors
- [x] `python scripts/audit.py --root . --no-urls` — no new fail-severity issues
- [x] Verify skill structure: `ls skills/challenge/` shows SKILL.md and references/ only

---

## Validation

1. `python -m pytest tests/ -v` passes with no failures
2. `ruff check wos/ tests/ scripts/` passes
3. `python scripts/audit.py --root . --no-urls` shows no new fail-severity issues
4. `wos/challenge/` directory does not exist
5. `scripts/discover_context.py` does not exist
6. `skills/challenge/SKILL.md` contains no script invocations
7. CLAUDE.md architecture section reflects correct module/subpackage count
