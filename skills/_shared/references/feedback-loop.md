---
name: Feedback Loop
description: >
  Shared contract between write-plan and brainstorm for structured
  infeasibility feedback — format, user options, and revision-vs-supersede
  decision tree.
---

# Feedback Loop

When write-plan discovers that a design cannot be implemented as specified,
it produces structured feedback rather than silently modifying scope. This
reference defines the feedback format, user options, and the decision tree
for how to proceed.

## Feedback Format

Embed a `## Feedback` section in the plan document with four fields:

    ## Feedback

    **Infeasible:** [specific design element that cannot be implemented]
    **Why:** [files checked, APIs tested, dependencies missing]
    **Impact:** [which plan tasks are affected and how]
    **Alternatives:** [suggested modifications, if any]

Field naming follows the categorical convention used by ADRs and KEPs.
Each field appears under the `## Feedback` heading, which provides
sufficient context for unambiguous interpretation.

## User Options

Present three choices when infeasibility is detected:

1. **Return to brainstorm** — invoke `wos:brainstorm` with the plan file
   path as input. Brainstorm reads the `## Feedback` section and revises
   the design through its normal workflow. **Recommend this for
   design-level problems** (wrong approach, missing capability, incorrect
   assumptions about the system).

2. **Proceed with modified scope** — revise the plan in-place: update
   Must/Won't boundaries, adjust or remove affected tasks, and document
   what changed and why in the Approach section. **Recommend this for
   task-level adjustments** where the overall design is sound but a
   specific task or constraint is impractical.

3. **Abandon** — set `status: abandoned` in the plan frontmatter with a
   reason. Link to the `## Feedback` section as rationale.

## Revision vs Supersede

The change mechanism depends on which artifact type has the problem:

- **Design problem** → return to brainstorm → create a **new** design
  doc with a `related:` link to the original. Do not modify the approved
  original. This is the "supersede, don't edit" pattern.

- **Plan problem** → revise the plan **in-place**. Update affected
  sections and document the change in the Approach section.

Rationale: design docs are records of decision (immutable after approval);
plans are execution guides (mutable during execution). This follows the
ADR/KEP pattern where architectural decisions are superseded while
implementation plans are living documents.
