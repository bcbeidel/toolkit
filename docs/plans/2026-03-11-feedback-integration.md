---
name: Feedback Integration Implementation
description: >
  Implement bidirectional feedback between wos:write-plan and wos:brainstorm
  when plan creation reveals design infeasibility (issue #163).
type: plan
status: completed
related:
  - docs/plans/2026-03-11-feedback-integration-design.md
  - docs/research/2026-03-11-feedback-field-naming-conventions.md
  - docs/research/2026-03-11-immutable-design-mutable-plan.md
---

# Feedback Integration Implementation

**Goal:** Complete the feedback loop between wos:write-plan and wos:brainstorm
so that infeasibility detected during planning flows back to design revision
through a structured, research-backed process. Addresses all 7 acceptance
criteria of issue #163.

**Scope:**

Must have:
- Shared `feedback-loop.md` reference with format, options, and decision tree
- write-plan Step 4 field rename (`Evidence` → `Why`) and option 2 elaboration
- brainstorm five-step feedback intake workflow replacing placeholder
- Placeholder note removal from brainstorm

Won't have:
- New skills, Python code, or validator changes
- Changes to execute-plan, validate-plan, or finish-work
- Automated design-vs-plan problem detection

**Approach:** Create one new shared reference file, then make targeted edits
to two existing SKILL.md files. All changes are markdown-only. The shared
reference establishes a contract between the two skills; each skill's SKILL.md
references it for the full format and decision tree while keeping inline
guidance minimal.

**File Changes:**

- Create: `skills/_shared/references/feedback-loop.md`
- Modify: `skills/write-plan/SKILL.md` (Step 4, lines 55-73)
- Modify: `skills/brainstorm/SKILL.md` (lines 90-99)

**Branch:** `feat/163-feedback-integration`
**PR:** TBD

---

### Task 1: Create shared feedback-loop reference

**Files:**
- Create: `skills/_shared/references/feedback-loop.md`

- [x] **Step 1:** Create `skills/_shared/references/feedback-loop.md` with WOS
  frontmatter (`name`, `description`) and three sections:
  1. **Feedback Format** — the four categorical fields (`Infeasible`, `Why`,
     `Impact`, `Alternatives`) under a `## Feedback` heading, with
     one-line descriptions of what goes in each field.
  2. **User Options** — the three choices (return to brainstorm, proceed
     with modified scope, abandon) with guidance on when each applies.
     Bias toward "return to brainstorm" for design-level problems and
     "proceed with modified scope" for task-level adjustments.
  3. **Revision vs Supersede** — decision tree distinguishing design
     problems (supersede: new doc with `related:` link) from plan
     problems (revise in-place: update sections, document in Approach).
     Include one-sentence rationale citing the immutable-design/mutable-plan
     research pattern.

- [x] **Step 2:** Verify: read the file and confirm it has frontmatter with
  `name` and `description`, and all three sections are present.

- [x] **Step 3:** Verify: `uv run scripts/audit.py --root . --no-urls 2>&1 | grep feedback-loop`
  produces no output (clean audit).

- [x] **Step 4:** Commit.

---

### Task 2: Update write-plan Step 4

**Files:**
- Modify: `skills/write-plan/SKILL.md` (lines 55-73)

**Depends on:** Task 1

- [x] **Step 1:** In Step 4 (Infeasibility Check), rename the feedback field
  `**Evidence:**` to `**Why:**` on line 63.

- [x] **Step 2:** Add a reference link after the feedback format block (after
  line 65). Text:
  `See [Feedback Loop](../../_shared/references/feedback-loop.md) for the full format, user options, and revision-vs-supersede decision tree.`

- [x] **Step 3:** Replace option 2 (line 71-72) with the elaborated version:
  `2. **Proceed with modified scope** — revise the plan in-place: update Must/Won't boundaries, adjust or remove affected tasks, and document what changed and why in the Approach section. Appropriate when the design is sound but a specific task or constraint is impractical.`

- [x] **Step 4:** Verify: read `skills/write-plan/SKILL.md` and confirm:
  - Line with `**Evidence:**` is gone, replaced by `**Why:**`
  - Reference link to `feedback-loop.md` is present
  - Option 2 describes in-place revision workflow

- [x] **Step 5:** Verify: `uv run scripts/audit.py --root . --no-urls 2>&1 | grep write-plan`
  shows no new failures. Check body line count stays under 500.

- [x] **Step 6:** Commit.

---

### Task 3: Update brainstorm feedback section

**Files:**
- Modify: `skills/brainstorm/SKILL.md` (lines 90-99)

**Depends on:** Task 1

- [x] **Step 1:** Replace the entire "Receiving Feedback from Write-Plan"
  section (lines 90-99, including the placeholder note) with:

  ```
  ## Receiving Feedback from Write-Plan

  When invoked with a plan file path containing a `## Feedback` section:

  1. Read the feedback artifact (the plan's `## Feedback` section).
  2. Identify which design decisions are affected by the infeasibility.
  3. Present the feedback to the user with your assessment of what needs
     to change in the design.
  4. Revise the affected sections through the normal brainstorm dialogue
     (steps 2-5 of the workflow above).
  5. For the revised design, follow the "supersede, don't edit" pattern:
     create a new design doc with a `related:` link to the original.
     Do not modify the approved original.

  See [Feedback Loop](../_shared/references/feedback-loop.md) for the
  feedback format and revision-vs-supersede decision tree.
  ```

- [x] **Step 2:** Verify: read `skills/brainstorm/SKILL.md` and confirm:
  - The placeholder note referencing #159 and #163 is gone
  - Five numbered steps are present in the section
  - Reference link to `feedback-loop.md` is present
  - The "supersede, don't edit" pattern is mentioned

- [x] **Step 3:** Verify: `uv run scripts/audit.py --root . --no-urls 2>&1 | grep brainstorm`
  shows no new failures. Check body line count stays under 500.

- [x] **Step 4:** Commit.

---

## Validation

- [x] `uv run python -m pytest tests/ -v` — all tests pass
- [x] `uv run scripts/audit.py --root . --no-urls` — no new failures for
  brainstorm, write-plan, or feedback-loop
- [x] `skills/_shared/references/feedback-loop.md` exists with format,
  options, and decision tree sections
- [x] `skills/write-plan/SKILL.md` Step 4 uses `Infeasible/Why/Impact/Alternatives`
- [x] `skills/brainstorm/SKILL.md` has five-step feedback intake, no placeholder note
- [x] Both SKILL.md files reference `feedback-loop.md`
- [x] Both SKILL.md body line counts under 500
