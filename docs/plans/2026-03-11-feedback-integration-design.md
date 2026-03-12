---
name: Write-Plan to Brainstorm Feedback Integration
description: >
  Design for bidirectional feedback between wos:write-plan and wos:brainstorm
  when plan creation reveals design infeasibility (issue #163).
type: design
status: draft
---

# Write-Plan to Brainstorm Feedback Integration

## Purpose

When write-plan discovers a design is infeasible during plan creation,
there is no structured path back to brainstorm. The current skills have
placeholder support but lack the detailed workflow, shared format contract,
and revision-vs-supersede guidance needed for the feedback loop to work.

## Behavior

### Shared Reference: feedback-loop.md

A new file at `skills/_shared/references/feedback-loop.md` referenced by
both skills. It documents three things:

**Feedback format** — four categorical fields under a `## Feedback` heading
in the plan document:

    ## Feedback

    **Infeasible:** [specific design element that cannot be implemented]
    **Why:** [files checked, APIs tested, dependencies missing]
    **Impact:** [which plan tasks are affected and how]
    **Alternatives:** [suggested modifications, if any]

**User options** — three choices when infeasibility is detected:

1. **Return to brainstorm** — invoke `wos:brainstorm` with the plan file
   path. Brainstorm reads the Feedback section and revises the design.
   Recommended for design-level problems.
2. **Proceed with modified scope** — revise the plan in-place: update
   Must/Won't boundaries, adjust or remove affected tasks, document what
   changed and why in the Approach section. Recommended for task-level
   adjustments where the design is sound.
3. **Abandon** — set `status: abandoned` with a reason.

**Revision-vs-supersede decision tree:**

- Problem with the **design** (wrong approach, missing capability,
  incorrect assumptions) → return to brainstorm → new design doc with
  `related:` link to original (supersede, don't edit)
- Problem with the **plan** (impractical task, scope too wide, missed
  dependency) → revise plan in-place → update affected sections, document
  change in Approach

Rationale: design docs are records of decision (immutable after approval);
plans are execution guides (mutable during execution). Follows the ADR/KEP
pattern documented in `docs/research/2026-03-11-immutable-design-mutable-plan.md`.

### Changes to write-plan

Three targeted edits to Step 4 (Infeasibility Check):

1. Rename feedback field `**Evidence:**` → `**Why:**` for clarity.
2. Add reference link to `feedback-loop.md`.
3. Elaborate option 2 ("proceed with modified scope") to describe the
   in-place revision workflow: update Must/Won't, adjust affected tasks,
   document changes in Approach.

No other changes. The existing Step 4 structure, anti-pattern guard #5,
and three-option flow remain intact.

### Changes to brainstorm

Replace the thin "Receiving Feedback from Write-Plan" section (lines 90-99)
with a five-step intake workflow:

1. Read the feedback artifact (plan's Feedback section)
2. Identify which design decisions are affected
3. Present feedback to user with assessment of what needs to change
4. Revise affected sections through normal brainstorm dialogue (steps 2-5)
5. Create new design doc with `related:` link to original (supersede pattern)

Remove the placeholder note referencing issues #159 and #163.
Add reference link to `feedback-loop.md`.

No other changes. The workflow, hard gate, anti-patterns, and output
format remain intact.

## Scope

Must have:
- Shared feedback format reference usable by both skills
- Revision-vs-supersede decision tree with rationale
- write-plan field rename and option 2 elaboration
- brainstorm five-step feedback intake workflow
- Placeholder note removal

Won't have:
- New skill or command for the feedback flow
- Python code, validators, or document model changes
- Changes to execute-plan, validate-plan, or finish-work
- Automated detection of design-vs-plan problems (user decides)

## Constraints

- Both SKILL.md files must stay under 500 body lines
- Shared reference goes in `skills/_shared/references/` (existing pattern)
- Field naming follows categorical convention per feedback-field-naming research
- Supersede-vs-revise follows immutable-design/mutable-plan research

## Acceptance Criteria

- write-plan Step 4 uses `Infeasible/Why/Impact/Alternatives` field names
- write-plan Step 4 option 2 describes in-place plan revision workflow
- brainstorm has five-step feedback intake replacing placeholder section
- Placeholder note referencing #163 is removed
- Shared `feedback-loop.md` exists and is referenced by both skills
- Decision tree distinguishes design problems (supersede) from plan problems (revise)
- All tests pass, audit clean for modified skills
