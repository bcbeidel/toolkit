---
name: plan-work
description: >
  Use when the user has a spec or requirements for a multi-step task,
  before touching code. Creates structured implementation plans with
  explicit lifecycle management and verification criteria. Use when
  the user wants to "plan", "make an implementation plan", "break
  this down into tasks", or needs to turn a design into actionable
  work items.
argument-hint: "[design doc path or feature description]"
user-invocable: true
references:
  - references/format-guide.md
  - references/plan-template.md
  - references/examples/small-plan.md
  - references/examples/medium-plan.md
---

# Plan Work

Convert approved designs or requirements into structured implementation plans.
The output is a plan document — not code, not a design.

## Workflow

### 1. Gather Context

- Read the design doc (if invoked from scope-work, check the `related` field).
- Explore the codebase: identify files to create, modify, or delete.
- Check `docs/plans/` for overlapping or related plans.
- If no design doc exists, gather requirements from the user before proceeding.

### 2. Scope Check

If the plan would require >20 tasks or span >3 independent subsystems,
suggest splitting into separate plans. Each plan should produce working,
testable software on its own.

> "This looks like [N] independent pieces: [list]. I'd suggest separate
> plans — they can be built in any order. Which should we start with?"

### 3. Write the Plan

Save location depends on the project's layout hint (read from AGENTS.md
`<!-- wos:layout: ... -->` comment):
- **separated**: `docs/plans/YYYY-MM-DD-<feature-name>.plan.md`
- **co-located**: same directory as the related design doc
- **flat**: `docs/YYYY-MM-DD-<feature-name>.plan.md`
- **none** or missing: ask the user where to save
- User can always override the suggested location.

Use the [Plan Document Format](../../_shared/references/plan-format.md).

See [Format Guide](references/format-guide.md) for how to write each section
effectively. Use the [Plan Template](references/plan-template.md) as a
starting skeleton.

All 6 required sections: Goal, Scope, Approach, File Changes, Tasks,
Validation. At least one concrete validation criterion — not "verify it
works" but a specific command with expected output.

### 4. Infeasibility Check

If plan creation reveals the design cannot be implemented as specified,
do not silently modify scope. Instead, produce structured feedback:

    ## Feedback

    **Infeasible:** [specific design element that cannot be implemented]
    **Why:** [files checked, APIs tested, dependencies missing]
    **Impact:** [which plan tasks are affected and how]
    **Alternatives:** [suggested modifications, if any]

See [Feedback Loop](../../_shared/references/feedback-loop.md) for the
full format, user options, and revision-vs-supersede decision tree.

Present the user with three options:

1. **Return to scope-work** — invoke `wos:scope-work` with this feedback
   to revise the design. Follow the "supersede, don't edit" pattern.
2. **Proceed with modified scope** — revise the plan in-place: update
   Must/Won't boundaries, adjust or remove affected tasks, and document
   what changed and why in the Approach section. Appropriate when the
   design is sound but a specific task or constraint is impractical.
3. **Abandon** — set `status: abandoned` with a reason in the plan.

### 5. Review with User

Before presenting, confirm all required sections are present:

```bash
bash <plugin-skills-dir>/start-work/scripts/validate_plan.sh <plan-file>
```

If the script exits 1, fix the missing sections before presenting.

Present a summary:
- Goal (1 sentence)
- Task count and estimated file changes
- Key scope boundaries (Must/Won't highlights)
- Validation criteria

Do not proceed until the user approves.

### 6. Update Status

When the user approves, set `status: approved` in the plan's frontmatter.

### 7. Hand Off

Present to user: "Plan approved. Ready to invoke `/wos:start-work` to
begin implementation — proceed?"

Wait for user confirmation before invoking the skill. The plan should be
ready for execution by an agent with zero prior context.

## Key Instructions

- **Won't write code, modify files, or invoke execution skills** — the plan is the
  deliverable; implementation is `start-work`'s job.
- **Plans are files, not chat.** Save to disk with frontmatter. Plans that
  exist only in conversation are lost on context reset.
- **Plans survive context resets.** A new session resumes by reading
  the plan file — completed tasks are `[x]`, remaining are `[ ]`.
  Write each task so it can be started from the current git state
  without requiring conversation history.
- **Every task gets a verification command.** If you can't verify it, you
  can't know it's done.
- **Commit per task creates rollback boundaries.** Each completed
  task gets its own git commit. On failure, the agent can diff
  against the last passing commit and roll back cleanly. This is
  why every task ends with a commit step.
- **Middle altitude.** Observable outcomes, not implementation prescriptions.
  Too abstract: "Implement auth." Too granular: "Write if-statement on
  line 47." Right: "Add login endpoint. Verify: `curl POST /login`
  returns 200 with token."
- **One plan per feature.** Multi-system changes get separate plans.
- **Link to design docs.** Use the `related` field to connect plans to
  their design specs, establishing traceability.
- **Scope boundaries are load-bearing.** Won't-have items prevent scope
  creep during execution. Be explicit about what's excluded.
- **Dependencies between tasks are explicit.** If task B requires task A,
  state the dependency. Default is sequential execution.
- **Intermediates go to disk, not just context.** During execution,
  write discovered information (decisions, edge cases, API findings)
  to the plan file or a companion notes file. Context resets;
  files persist.
- **Chunk large plans.** Use `## Chunk N: <name>` headers for plans with
  10+ tasks, grouping by logical dependency.

## Anti-Pattern Guards

1. **Premature implementation** — writing code or invoking execution skills
   before the plan is approved. The plan is the deliverable.
2. **Vague validation** — "verify it works" is not a criterion. Every
   validation item needs a concrete command or observable check.
3. **Task granularity extremes** — tasks should be independently verifiable
   outcomes. Neither "implement the feature" nor "add import statement."
4. **Scope creep during planning** — if the plan grows beyond the design,
   something is wrong. Check whether the design needs revision (step 4)
   or the plan needs splitting (step 2).
5. **Skipping the infeasibility check** — even if everything seems fine,
   confirm the design's assumptions against the actual codebase before
   presenting for review.
6. **Session-dependent task descriptions** — tasks that reference conversation context ("as discussed", "the approach we agreed on") cannot be resumed in a new session. Plans are procedural memory, not session notes. Every task must be startable with zero conversation history and no access to this chat.
7. **Missing branch in frontmatter** — the `branch:` field is load-bearing for multi-session execution. An executor resuming in a new session cannot determine where to work without it. Always set it before handing off to start-work.

## Output Format

Plan documents use WOS frontmatter:

    ---
    name: Feature Name
    description: One-sentence summary
    type: plan
    status: draft
    related:
      - docs/designs/YYYY-MM-DD-<name>.design.md
    ---

Save location follows the project's layout hint (see step 3 above).
The `related` field links to design docs, context files, or other plans.

## Handoff

**Receives:** Design doc path or feature description; optional issue number and roadmap context
**Produces:** Implementation plan document saved to `docs/plans/` with tasks, file changes, and validation criteria
**Chainable to:** start-work
