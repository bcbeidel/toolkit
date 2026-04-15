---
name: Spec Format Guide
description: How to write effective design specifications — behavior-focused, observable, bounded
---

# Spec Format Guide

Design specifications define WHAT the system does externally, not HOW it
works internally. Architecture decisions belong in the plan.

## Required Frontmatter

    ---
    name: Feature Name
    description: One-sentence summary
    type: design
    status: draft
    related:
      - docs/context/relevant-file.md
    ---

Use unquoted values. The WOS frontmatter parser does not strip quotes.

## Spec Sections

Scale each section to the complexity of the task. A simple task may need
only Purpose and Acceptance Criteria. A multi-system change needs all
sections.

| Section | Purpose | When to Include |
|---------|---------|-----------------|
| **Purpose** | What this achieves and why. State the user-visible outcome. | Always |
| **User Journeys** | Who uses this and how. Scenarios, not implementation. | Multi-user or workflow changes |
| **Behavior** | Observable input/output mappings, preconditions, postconditions. | API or data model changes |
| **Scope** | Must have / Won't have. Explicit exclusions prevent scope creep. | Always |
| **Constraints** | Technical, organizational, or timeline constraints. | When constraints affect design |
| **Acceptance Criteria** | Observable behaviors that prove success. Verifiable from outside. | Always |

## Writing Principles

1. **Behavior over implementation** — describe what the user sees, not what
   the code does. "Users can filter by date range" not "Add a SQL WHERE
   clause on created_at."
2. **Observable outcomes** — every requirement should be verifiable without
   reading source code. If you can't test it from the outside, it's an
   implementation detail.
3. **Explicit boundaries** — state what's excluded alongside what's included.
   "Won't have" is as important as "Must have."
4. **Structured over freeform** — use tables, lists, and Given/When/Then
   where they add clarity. Avoid long prose paragraphs.
5. **Minimum viable specification** — match effort to stakes. A config
   change needs a sentence. A new subsystem needs structured sections.

## Depth Calibration

| Task Complexity | Spec Depth | Example |
|----------------|------------|---------|
| Trivial (config, typo) | 1-2 sentences — purpose and acceptance criteria | "Change timeout from 30s to 60s. Verify with integration test." |
| Simple (single component) | Short paragraph per section, 2-3 sections | New validation rule, API endpoint |
| Moderate (multi-component) | Full sections, acceptance criteria per component | Feature spanning frontend + backend |
| Complex (multi-system) | Decompose into sub-projects first, then full spec per sub-project | Platform-level changes |
