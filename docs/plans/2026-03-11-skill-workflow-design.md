---
name: Skill Workflow Improvements
description: Explicit handoff templates, branch creation in execute-plan, and research→distill pipeline guidance
type: design
status: approved
related:
  - skills/brainstorm/SKILL.md
  - skills/write-plan/SKILL.md
  - skills/execute-plan/SKILL.md
---

## Purpose

Improve the WOS skill lifecycle by making transitions between skills explicit,
ensuring work happens on branches, and documenting the research→distill
orchestration pattern. Addresses issues #183, #181, and #174.

## Component 1: Explicit Handoff Templates (#183)

Update the Hand Off section in 3 SKILL.md files to name the exact `/wos:`
command and pause for user confirmation.

**brainstorm/SKILL.md** Step 6 (Hand Off):
> Present to user: "Design approved. Ready to invoke `/wos:write-plan` to
> turn this into an implementation plan — proceed?"
> Wait for confirmation before invoking.

**write-plan/SKILL.md** Step 7 (Hand Off):
> Present to user: "Plan approved. Ready to invoke `/wos:execute-plan` to
> begin implementation — proceed?"
> Wait for confirmation before invoking.

**execute-plan/SKILL.md** Step 6 (Finish):
> Present to user: "All tasks complete. Ready to invoke `/wos:validate-work`
> to verify the plan succeeded — proceed?"
> After validation passes: "Validation passed. Ready to invoke
> `/wos:finish-work` to integrate — proceed?"

## Component 2: Branch Creation in execute-plan (#181)

New step inserted after the approval gate, before task execution begins.

**Step 3: Branch Setup**

1. Check if currently on the default branch (`main` or `master`).
2. If on default branch:
   - Derive branch name from plan filename: strip `docs/plans/` and date
     prefix. E.g., `docs/plans/2026-03-11-skill-workflow.md` → `skill-workflow`.
   - Present to user: "This plan should be implemented on a branch.
     Suggested: `skill-workflow` — use this, or provide a different name?"
   - Create and checkout the branch.
   - Write the branch name to the plan's `branch:` frontmatter field.
3. If already on a feature branch:
   - Present to user: "Currently on branch `<name>` — use this for the plan?"
   - On confirmation, write branch name to plan's `branch:` field if not
     already set.

Subsequent steps renumber accordingly.

## Component 3: Research→Distill Pipeline Reference (#174)

New file: `skills/execute-plan/references/research-distill-pipeline.md`

**When to apply:** Plans containing tasks that invoke both `/wos:research`
and `/wos:distill` on related topics.

**Three-phase pattern:**

1. **Phase 1 — Parallel research:** Dispatch research tasks as parallel
   subagents. Each invokes `/wos:research` and produces a doc in
   `docs/research/`.
2. **Phase 2 — Human review checkpoint:** All research subagents complete
   and return to the main agent. Present findings to user for review.
   Hard gate — do not begin distillation without user approval.
3. **Phase 3 — Parallel distill:** Dispatch distill tasks as parallel
   subagents. Each invokes `/wos:distill` with the reviewed research doc path.

**Subagent prompt templates:** Include research question/target path for
research subagents; research doc path for distill subagents.

**Key rules:**
- Never chain research→distill in a single subagent (human review gate
  must intervene)
- If user provides feedback on research findings, update the research doc
  before dispatching distill
- If only some research tasks complete, user may approve partial distillation

**execute-plan/SKILL.md update:** Add reference link with note: "Consult
when plans contain research→distill workstreams."

## Constraints

- No new Python code or scripts — all changes are SKILL.md and reference markdown
- No changes to skill interfaces or frontmatter schemas
- Handoff templates are guidance for the agent, not enforced programmatically
- Branch creation is best-effort — if git operations fail, surface error to user

## Acceptance Criteria

1. Each of brainstorm, write-plan, and execute-plan SKILL.md files contains
   a handoff prompt naming the exact `/wos:` command with confirmation pause
2. execute-plan SKILL.md has a Branch Setup step after the approval gate that
   creates a branch, confirms with user, and writes to plan `branch:` field
3. `skills/execute-plan/references/research-distill-pipeline.md` exists with
   three-phase pattern, subagent prompt templates, and key rules
4. execute-plan SKILL.md references the pipeline doc

## Won't Have

- Shared handoff reference doc
- Plan-format.md updates for `branch:` field lifecycle
- Auto-detection of research/distill tasks in plans
- Programmatic enforcement of any of these patterns
