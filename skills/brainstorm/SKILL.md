---
name: brainstorm
description: >
  Use before creating implementation plans. Explores user intent,
  requirements, and design through structured divergent-then-convergent
  thinking. Produces a design document, not code. Use when the user
  wants to "brainstorm", "explore", "design", "figure out what to build",
  or needs to think through a problem before planning.
argument-hint: "[topic or problem to explore]"
user-invocable: true
references:
  - references/spec-format-guide.md
  - references/exploration-patterns.md
---

# Brainstorm

Explore ideas and turn them into design specifications through structured
dialogue. The output is a design document — not a plan, not code.

<HARD-GATE>
Do NOT invoke any planning or implementation skill, write any code, or take
any implementation action until you have presented a design and the user has
approved it. This applies to EVERY task regardless of perceived simplicity.
</HARD-GATE>

## Workflow

### 1. Understand Intent

- Explore project context — read relevant files, docs, recent commits.
- Assess scope: if the request describes multiple independent subsystems,
  flag this immediately. Don't refine details of a project that needs
  decomposition first. Each sub-project gets its own brainstorm → plan cycle.
- Ask clarifying questions one at a time, multiple-choice preferred.
  Establish what and why before how.

### 2. Diverge

- Propose 2-3 approaches with tradeoffs.
- Lead with your recommendation and reasoning.
- Do not converge prematurely — if only one approach is proposed,
  divergence was skipped.

See [Exploration Patterns](references/exploration-patterns.md) for question
templates and approach comparison format.

### 3. Converge

- Narrow to a recommended approach based on user input and constraints.
- Confirm scope boundaries (must have / won't have).

### 4. Write the Spec

- Present design section by section. Ask after each whether it looks right.
  Cover: purpose, behavior, components, constraints, acceptance criteria.
- Calibrate depth to task complexity — a paragraph for simple tasks, full
  structured spec for multi-system changes.
- Save location depends on the project's layout hint (read from AGENTS.md
  `<!-- wos:layout: ... -->` comment):
  - **separated**: `docs/designs/YYYY-MM-DD-<name>.design.md`
  - **co-located**: same directory as related documents
  - **flat**: `docs/YYYY-MM-DD-<name>.design.md`
  - **none** or missing: ask the user where to save
  - User can always override the suggested location.

See [Spec Format Guide](references/spec-format-guide.md) for format
conventions and examples.

### 5. Review with User

- Present a summary of the complete design.
- Hard gate: do not proceed until the user approves.

### 6. Hand Off

- Present to user: "Design approved. Ready to invoke `/wos:write-plan`
  to turn this into an implementation plan — proceed?"
- Wait for user confirmation before invoking the skill.
- The plan should reference this design doc via its `related` field,
  establishing traceability between design and plan.

## Key Instructions

- **Specs define WHAT and WHY, not HOW.** Architecture decisions belong
  in the plan, not the spec. If the spec reads like pseudo-code, it has
  crossed into implementation.
- **Calibrate depth to complexity.** A paragraph for simple tasks, full
  structured spec for multi-system changes.
- **One question at a time.** Prefer multiple-choice over open-ended.
- **Design for isolation and clarity.** Break systems into units with one
  clear purpose, well-defined interfaces, testable independently.
- **Follow existing patterns.** Explore the current codebase structure
  before proposing changes. Work with conventions, not against them.
- **YAGNI.** Remove unnecessary features from all designs. Every element
  must justify its presence.

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

## Anti-Pattern Guards

1. **Premature convergence** — jumping to solutions before exploring the
   problem space. If only one approach is proposed, divergence was skipped.
2. **Over-specification** — if the spec reads like pseudo-code, it has
   crossed into implementation. Specs should be verifiable from the outside.
3. **Skipping exploration** — even "simple" tasks benefit from clarification.
   The calibration instruction handles truly trivial changes, not anything
   involving design decisions.
4. **Scope blindness** — not flagging projects that need decomposition
   before deep-diving into details.
5. **False confidence from spec compliance** — a confident-sounding but
   incorrect specification is worse than no specification. The spec must
   be verified by the user (Step 5), not just by the agent that produced it.

## Output Format

Design docs use WOS frontmatter:

    ---
    name: Feature Name
    description: One-sentence summary
    metadata:
      type: design
      status: draft
      related:
        - docs/context/relevant-file.md
    ---

Save location follows the project's layout hint (see step 4 above).
The `metadata.related` field links to context files, research docs, or other
design docs.
