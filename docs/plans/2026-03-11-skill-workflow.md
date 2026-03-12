---
name: Skill Workflow Improvements
description: Explicit handoff templates, branch creation in execute-plan, and research-distill pipeline guidance
type: plan
status: completed
branch: skill-workflow
related:
  - docs/plans/2026-03-11-skill-workflow-design.md
---

## Goal

Make skill lifecycle transitions explicit and reliable: handoffs name the
exact next command, execute-plan creates a branch before committing work,
and research→distill orchestration is documented. Addresses #183, #181, #174.

## Scope

**Must have:**
- Explicit handoff prompt templates in brainstorm, write-plan, execute-plan
- Branch Setup step in execute-plan after approval gate
- Research→distill pipeline reference document
- Pipeline reference linked from execute-plan SKILL.md

**Won't have:**
- Shared handoff reference document
- Plan-format.md updates for `branch:` field lifecycle
- Auto-detection of research/distill tasks
- Programmatic enforcement of any patterns
- Python code or script changes

## Approach

All changes are markdown edits to SKILL.md files and one new reference doc.
Tasks 1-3 are independent (different files). Task 4 consolidates all
execute-plan SKILL.md changes (branch setup, handoff updates, pipeline
reference link) into a single task to avoid edit conflicts. Task 5 creates
the new reference doc.

## File Changes

| File | Action |
|------|--------|
| `skills/brainstorm/SKILL.md` | Modify — update Hand Off (Step 6) |
| `skills/write-plan/SKILL.md` | Modify — update Hand Off (Step 7) |
| `skills/execute-plan/SKILL.md` | Modify — add Branch Setup step, update Finish/handoff, add pipeline reference |
| `skills/execute-plan/references/research-distill-pipeline.md` | Create — new reference doc |

## Tasks

- [x] Task 1: Update brainstorm handoff to name exact command (#183) <!-- sha:dfe63ce -->
  Replace Step 6 (Hand Off) content in `skills/brainstorm/SKILL.md` with
  explicit prompt template that names `/wos:write-plan` and waits for
  confirmation.
  Verify: `grep -c "wos:write-plan" skills/brainstorm/SKILL.md` returns 2+
  (backtick reference + prompt template). Read Step 6 and confirm it includes
  a user-facing prompt string and confirmation pause.

- [x] Task 2: Update write-plan handoff to name exact command (#183) <!-- sha:b367cad -->
  Replace Step 7 (Hand Off) content in `skills/write-plan/SKILL.md` with
  explicit prompt template that names `/wos:execute-plan` and waits for
  confirmation.
  Verify: `grep -c "wos:execute-plan" skills/write-plan/SKILL.md` returns 2+.
  Read Step 7 and confirm prompt template and confirmation pause.

- [x] Task 3: Create research-distill pipeline reference (#174) <!-- sha:9d7f004 -->
  Create `skills/execute-plan/references/research-distill-pipeline.md` with
  WOS frontmatter. Content: when to apply, three-phase pattern (parallel
  research → human review checkpoint → parallel distill), subagent prompt
  templates for both phases, key rules (no chaining in single subagent,
  feedback handling, partial distillation).
  Verify: file exists, has valid frontmatter, covers all three phases,
  includes prompt templates, includes key rules section.

- [x] Task 4: Update execute-plan SKILL.md — branch setup, handoffs, pipeline ref (#181, #183, #174) <!-- sha:4939248 -->
  Three changes to `skills/execute-plan/SKILL.md`:
  (a) Insert new Step 3 (Branch Setup) after Approval Gate. Check if on
      default branch; derive name from plan filename; confirm with user;
      create branch; write to plan `branch:` field. If already on feature
      branch, confirm and write. Renumber subsequent steps (current 3→4,
      4→5, 5→6, 6→7).
  (b) Update Step 6 (formerly Step 5, Validate) to use explicit handoff:
      "All tasks complete. Ready to invoke `/wos:validate-work`..."
  (c) Update Step 7 (formerly Step 6, Finish) to use explicit handoff:
      "Validation passed. Ready to invoke `/wos:finish-work`..."
  (d) Add `research-distill-pipeline.md` to the references list in
      frontmatter and add a note in Choose Execution Mode or a new
      subsection referencing it for research→distill workstreams.
  Verify: Step numbering is sequential 1-7. `grep "Branch Setup"` finds
  the new step. `grep "wos:validate-work"` and `grep "wos:finish-work"`
  each appear in explicit prompt templates. `grep "research-distill"`
  confirms pipeline reference is linked. Frontmatter `references:` list
  includes the new file.

## Validation

1. **Automated:** `uv run python -m pytest tests/ -v` — all tests pass
   (no behavioral changes, but confirms nothing broke)
2. **Structural:** Each of the 3 SKILL.md files contains an explicit
   handoff prompt that names the exact `/wos:` command with a confirmation
   pause
3. **Structural:** execute-plan SKILL.md has 7 numbered steps with Branch
   Setup as Step 3
4. **Structural:** `skills/execute-plan/references/research-distill-pipeline.md`
   exists with three-phase pattern and prompt templates
5. **Structural:** execute-plan frontmatter `references:` includes
   `references/research-distill-pipeline.md`
