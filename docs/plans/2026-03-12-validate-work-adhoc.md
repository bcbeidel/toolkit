---
name: Validate Work Ad-Hoc Mode
description: Add plan-free validation path to validate-work using git diff and project conventions
type: plan
status: completed
related:
  - docs/plans/2026-03-12-validate-work-adhoc-design.md
  - skills/validate-work/SKILL.md
---

# Validate Work Ad-Hoc Mode

**Goal:** Users can call `/wos:validate-work` without a plan and get a
useful, scoped validation based on their actual changes and project setup.
This makes the skill accessible to anyone doing work outside the WOS
planning workflow.

**Scope:**

Must have:
- Mode branching at Step 1 (plan vs ad-hoc)
- Git diff analysis (branch + working tree)
- Config file convention detection
- Project doc scanning (CLAUDE.md, AGENTS.md, README, CONTRIBUTING)
- Hypothesis presentation with user confirmation gate
- Lighter failure handling for ad-hoc mode (suggestions, not plan tasks)

Won't have:
- New Python scripts or tooling
- Changes to the existing plan-based validation path
- Persistent storage of ad-hoc validation results
- Auto-detection of CI pipeline config (GitHub Actions, etc.)

**Approach:** Add a mode branch at the top of the SKILL.md workflow. When
no plan is provided, a new "Build Hypothesis" section gathers signals from
git diff, config files, and project docs. A new reference file
(`adhoc-validation.md`) contains the convention detection table and
hypothesis building protocol. The existing automated-validation and
human-validation references are reused unchanged. Failure handling is
conditioned on mode.

**File Changes:**
- Modify: `skills/validate-work/SKILL.md` (add mode branching, ad-hoc
  workflow steps, conditioned failure handling)
- Create: `skills/validate-work/references/adhoc-validation.md` (convention
  detection table, hypothesis protocol, project doc scanning)

**Branch:** `feat/validate-work-adhoc`
**PR:** TBD

---

### Task 1: Create ad-hoc validation reference

**Files:**
- Create: `skills/validate-work/references/adhoc-validation.md`

- [x] Write the reference file with three sections: git diff analysis
  protocol, config-file-to-check mapping table, and project doc scanning
  guidance. Include the convention detection table from the design doc.
  Add guidance on scoping checks to changed files. <!-- sha:be3de2b -->
- [x] Verify: `wc -l skills/validate-work/references/adhoc-validation.md`
  is under 120 lines. Content covers all three signal sources. <!-- sha:be3de2b -->
- [x] Commit <!-- sha:be3de2b -->

---

### Task 2: Add mode branching to SKILL.md

**Files:**
- Modify: `skills/validate-work/SKILL.md`

**Depends on:** Task 1

- [x] Replace Step 1 ("Load Plan") with "Determine Mode" that branches
  between plan path and ad-hoc path. Plan path loads existing Steps 2-7
  unchanged. Ad-hoc path flows into a new "Build Hypothesis" step. <!-- sha:e0de6b3 -->
- [x] Add Step 1b "Build Hypothesis" for ad-hoc mode: gather git diff
  signals, scan config files, read project docs. Reference
  `adhoc-validation.md` for the detection table and protocol. <!-- sha:e0de6b3 -->
- [x] Add Step 1c "Present and Confirm" for ad-hoc mode: show changes
  detected, proposed checks with classification ([auto]/[human]),
  and user confirmation gate. <!-- sha:e0de6b3 -->
- [x] Verify: SKILL.md reads coherently end-to-end. Both paths are clear.
  354 instruction lines, under 500 threshold. <!-- sha:e0de6b3 -->
- [x] Commit <!-- sha:e0de6b3 -->

---

### Task 3: Condition failure handling on mode

**Files:**
- Modify: `skills/validate-work/SKILL.md`

**Depends on:** Task 2

- [x] Update Step 6 (Handle Failures) to branch on mode. Plan mode:
  existing behavior (diagnose gap, suggest plan tasks, keep plan in
  executing). Ad-hoc mode: report diagnosis with evidence, suggest
  fixes as actionable next steps (not plan tasks), offer to re-run
  after fixes. <!-- sha:bd0899d -->
- [x] Update Step 7 (On Success) to branch on mode. Plan mode: update
  plan status to completed. Ad-hoc mode: report results summary,
  no status to update. <!-- sha:bd0899d -->
- [x] Verify: re-read SKILL.md. Both modes have complete failure and
  success paths. No plan-specific language leaks into ad-hoc path. <!-- sha:bd0899d -->
- [x] Commit <!-- sha:bd0899d -->

---

### Task 4: Update description triggers

**Files:**
- Modify: `skills/validate-work/SKILL.md`

**Depends on:** Task 3

- [x] Update the frontmatter `description` to include ad-hoc triggers:
  "check my work", "verify my changes", "does this look right",
  "run checks". Keep existing plan-related triggers. <!-- sha:3ca2957 -->
- [x] Verify: description is 427 characters. No XML tags,
  no second-person voice. No meta issues. <!-- sha:3ca2957 -->
- [x] Commit <!-- sha:3ca2957 -->

---

## Validation

- [ ] `uv run python -m pytest tests/ -v` — all existing tests pass (no
  regressions)
- [ ] Skill instruction density for validate-work stays under 500 lines
- [ ] Read SKILL.md end-to-end: both plan and ad-hoc paths are coherent,
  complete, and clearly separated
- [ ] SKILL.md frontmatter passes `check_skill_meta` with no issues
