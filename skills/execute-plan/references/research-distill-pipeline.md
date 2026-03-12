---
name: Research-Distill Pipeline
description: Orchestration pattern for plans with parallel research and distillation workstreams
---

# Research-Distill Pipeline

Guidance for executing plans that contain both `/wos:research` and
`/wos:distill` tasks on related topics.

## When to Apply

Use this pattern when a plan includes tasks that:
- Invoke `/wos:research` to investigate multiple topics
- Follow research with `/wos:distill` to convert findings into context files
- Can benefit from parallel execution within each phase

## Three-Phase Pattern

### Phase 1: Parallel Research

Dispatch research tasks as parallel subagents. Each subagent invokes
`/wos:research` and produces a research document in `docs/research/`.

**Subagent prompt template:**

> You are executing a research task from an implementation plan.
>
> **Research question:** [question from plan task]
> **Output path:** docs/research/[target filename]
>
> Invoke `/wos:research` to investigate this question. Follow the full
> research workflow including source verification. Save the completed
> research document to the output path.

All research subagents must complete before proceeding to Phase 2.

### Phase 2: Human Review Checkpoint

This is a hard gate. Do not begin distillation without user approval.

When all research subagents return:

1. Present a summary of each research document — title, key findings,
   source count, and any limitations or gaps noted.
2. Ask the user to review the research findings.
3. If the user provides feedback, update the affected research documents
   before proceeding.
4. Get explicit approval: "Research reviewed. Ready to invoke `/wos:distill`
   on each document — proceed?"

### Phase 3: Parallel Distill

Dispatch distill tasks as parallel subagents. Each subagent invokes
`/wos:distill` with the path to a reviewed research document.

**Subagent prompt template:**

> You are executing a distillation task from an implementation plan.
>
> **Research document:** [path to reviewed research doc]
>
> Invoke `/wos:distill` with this research document path. Follow the full
> distillation workflow — analyze findings, propose context files, generate
> with proper frontmatter, and run reindex + audit.

## Key Rules

- **Never chain research and distill in a single subagent.** The human
  review gate between Phase 2 and Phase 3 must be honored. Each phase
  is a separate wave of subagent dispatches.
- **Feedback before distillation.** If the user identifies gaps or
  corrections during review, update the research documents before
  dispatching distill subagents.
- **Partial distillation is acceptable.** If some research tasks fail
  or produce insufficient findings, the user may approve distilling
  only the successful research documents. Do not block the entire
  pipeline on a single failure.
- **Distill subagents are independent.** Each distill subagent works
  from a single research document. They do not need to coordinate
  with each other.
