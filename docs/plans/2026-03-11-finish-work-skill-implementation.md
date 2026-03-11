---
name: "finish-work skill implementation"
description: "Implementation plan for wos:finish-work skill — SKILL.md, 2 reference files, CLAUDE.md registration"
type: plan
status: completed
related:
  - docs/plans/2026-03-11-finish-work-skill-design.md
---

# finish-work Skill Implementation

## Goal

Create the `wos:finish-work` skill with SKILL.md and 2 reference files, register
it in CLAUDE.md, and verify with audit. This is the terminal step in the plan
lifecycle pipeline (issue #162).

## Scope

**Must have:**
- `skills/finish-work/SKILL.md` — 6-step workflow, under 500 lines
- `skills/finish-work/references/option-execution.md` — per-option git commands
- `skills/finish-work/references/retrospective-format.md` — retrospective section format
- CLAUDE.md updated with finish-work in skills table
- Indexes regenerated
- Audit passes

**Won't have:**
- Python scripts (no automated assessment needed for this skill)
- Changes to existing planning skills
- Superpowers deprecation (that's issue #164)

## Approach

Create the 3 markdown files following the patterns established by sibling
planning skills (validate-plan, execute-plan). Register in CLAUDE.md skills
table. Run audit to validate.

## File Changes

- **Create:** `skills/finish-work/SKILL.md`
- **Create:** `skills/finish-work/references/option-execution.md`
- **Create:** `skills/finish-work/references/retrospective-format.md`
- **Modify:** `CLAUDE.md` — add finish-work to skills table
- **Regenerate:** `skills/_index.md` (via reindex script)

## Tasks

### Task 1: Create SKILL.md

**Files:**
- Create: `skills/finish-work/SKILL.md`

- [x] Create `skills/finish-work/` directory and `SKILL.md` with frontmatter
  matching the design spec metadata (name, description, argument-hint,
  user-invocable, references list including shared refs).

- [x] Write the SKILL.md body with the 6-step workflow:
  1. Verify Readiness — run tests, hard gate on failure
  2. Locate Plan — optional, use `plan_assess.py --scan`, handle 0/1/many
  3. Determine Base Branch — `git merge-base`, confirm with user
  4. Present 4 Options — exact text block, no explanation
  5. Execute Chosen Option — delegate to `option-execution.md`
  6. Optional Retrospective — offer only if plan found

- [x] Add Key Instructions section (5 items: test gate, plan-optional,
  discard safety, worktree rules, status accuracy).

- [x] Add Anti-Pattern Guards section (5 guards from design spec).

- [x] Verify SKILL.md body is under 500 lines:
  ```bash
  wc -l skills/finish-work/SKILL.md
  ```

### Task 2: Create option-execution.md reference

**Files:**
- Create: `skills/finish-work/references/option-execution.md`

- [x] Write the reference with 4 sections (one per option), each containing:
  - Preconditions and behavior summary
  - Git command sequence (platform-agnostic descriptions with example commands)
  - Worktree handling (cleanup on merge/discard, preserve on PR/keep)
  - Quick reference table matching the superpowers pattern

- [x] Include PR body format: plan-derived (Goal section) as default, git log
  as fallback. Include suggestion to return to main worktree after PR creation.

- [x] Include discard confirmation format: show what will be lost (branch name,
  commit list, worktree path), require typed "discard", update plan status to
  `abandoned` if plan exists.

### Task 3: Create retrospective-format.md reference

**Files:**
- Create: `skills/finish-work/references/retrospective-format.md`

- [x] Write the reference covering:
  - When to offer (only when plan file exists)
  - Retrospective section format (3 subsections: Completed, Deviations, Lessons)
  - Where to insert in plan file (after Validation section)
  - Example retrospective section
  - Keep it concise — this is a simple reference

### Task 4: Register in CLAUDE.md and reindex

**Files:**
- Modify: `CLAUDE.md`
- Regenerate: indexes

- [x] Add `finish-work` to the skills table in CLAUDE.md:
  ```
  | `/wos:finish-work` | Structured work integration (merge/PR/keep/discard) |
  ```
  Update skill count from 8 to 9.

- [x] Run reindex:
  ```bash
  uv run scripts/reindex.py
  ```

- [x] Run audit to verify:
  ```bash
  uv run python -m pytest tests/ -v
  uv run scripts/audit.py --root .
  ```

### Task 5: Update design doc status

**Files:**
- Modify: `docs/plans/2026-03-11-finish-work-skill-design.md`

- [x] Update design doc frontmatter `status: draft` → `status: completed`.

## Validation

1. `uv run python -m pytest tests/ -v` — all tests pass
2. `uv run scripts/audit.py --root .` — no fail-severity issues
3. `wc -l skills/finish-work/SKILL.md` — under 500 lines
4. SKILL.md contains all 6 workflow steps, 5 key instructions, 5 anti-pattern guards
5. All 4 options documented in option-execution.md with git commands and worktree rules
6. Retrospective format documented with example
7. CLAUDE.md lists `/wos:finish-work` in skills table with count updated to 9
