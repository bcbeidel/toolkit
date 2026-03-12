---
name: Init Onboarding Enhancement
description: Extend wos:init SKILL.md with empty-repo onboarding steps
type: plan
status: approved
related:
  - docs/plans/2026-03-11-init-onboarding-design.md
  - skills/init/SKILL.md
---

# Init Onboarding Enhancement

**Issue:** #172
**Branch:** `172-init-onboarding`

## Goal

Extend `wos:init` to detect empty repos and offer three optional onboarding
steps: `.gitignore` with Python defaults, `README.md` stub, and guided
first-action suggestion.

## Scope

**Must have:**
- Empty-repo detection in step 1 (no README.md, no .gitignore, no source files beyond WOS scaffolding)
- Step 2.5: offer `.gitignore` with Python defaults
- Step 2.6: offer `README.md` stub from one-question project-intent prompt
- Step 2.7: guided first-action suggesting WOS skill sequences
- All three steps skippable
- Report step updated to reflect new items

**Won't have:**
- New scripts or reference files
- Changes to behavior for non-empty repos
- Language detection (always Python defaults)

## Approach

Single file edit to `skills/init/SKILL.md`:

1. Extend step 1 (Check current state) to also check for empty-repo indicators
2. Insert steps 2.5, 2.6, 2.7 between "Create missing directories" and "Reindex"
3. Update step 7 (Report) to include onboarding items

Steps are numbered 2.5/2.6/2.7 to slot cleanly between existing steps 2 and 3
without renumbering the entire workflow.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `skills/init/SKILL.md` | modify | Add empty-repo detection and three onboarding steps |

## Tasks

- [x] **Task 1: Update SKILL.md with onboarding steps**
  - Add `.gitignore`, `README.md`, `.env` to step 1 checklist
  - Add empty-repo detection note after step 1 checklist
  - Insert step 2.5 (`.gitignore` with Python defaults)
  - Insert step 2.6 (`README.md` stub)
  - Insert step 2.7 (guided first action)
  - Update step 7 (Report) to include onboarding items
  - Verify: `wc -l skills/init/SKILL.md` stays under 200 lines

- [x] **Task 2: Validate**
  - Run `uv run python -m pytest tests/ -v` — all tests pass
  - Run `uv run scripts/audit.py --root .` — no new failures
  - Verify SKILL.md is well-formed (frontmatter intact, step numbering consistent)

## Validation

1. `uv run python -m pytest tests/ -v` — all tests pass
2. `uv run scripts/audit.py --root .` — no new warn/fail on init skill
3. SKILL.md instruction body stays under 200 lines
