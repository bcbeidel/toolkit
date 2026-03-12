---
name: Distill Mapping Guide
description: Boundary heuristics for the foreground distill agent that proposes N:M research-to-context-file mappings
---

# Distill Mapping Guide

Guidance for analyzing completed research documents and proposing how
findings map to context files. Used during Phase 5 (Map) of the
research-distill pipeline by a foreground agent before dispatching
distill subagents.

## Your Task

Read all completed research documents from the current batch. Identify
discrete findings across the full corpus, then propose which findings
become which context files. Present the mapping as a table for user
approval.

## Finding Concept Boundaries

A **finding** is a self-contained insight that can inform a decision or
action without requiring other findings for context. To identify
boundaries:

1. **State the finding in one sentence.** If you need "and" to connect
   two distinct ideas, you're looking at two findings.
2. **Check audience independence.** Would different people need these
   insights for different purposes? If yes, separate them.
3. **Check actionability independence.** Can someone act on this finding
   without the other? If yes, separate them.
4. **Check concept independence.** Does this finding introduce a distinct
   concept, framework, or recommendation? If yes, it's its own unit.

## Splitting Heuristics

Split a research document into multiple context files when:

- It covers more than one distinct concept (most common — research
  questions naturally span multiple sub-topics)
- Different findings serve different audiences or use cases
- The document has both "what" and "how" components that are
  independently useful
- The document exceeds 800 words of distillable content — retrieval
  precision degrades in longer files
- Sub-questions in the research produced findings that are logically
  independent

## Merging Heuristics

Merge findings across research documents into one context file when:

- Multiple research documents investigated the same concept from
  different angles and produced convergent findings
- The findings are tightly coupled and don't make sense independently
- Combined content stays under 800 words
- The findings serve the same audience with the same purpose

**Merging is less common than splitting.** Default to splitting unless
there's a clear reason to merge.

## The One-Concept Test

Every proposed context file must pass this test:

> Can you describe what this file is about in one sentence without
> using "and"?

- **Pass:** "How asyncio's event loop achieves concurrency through
  cooperative multitasking"
- **Fail:** "How asyncio works and when to use threading instead"
  (two concepts — split into separate files)

## Granularity Preference

**Prefer more granular files over fewer large ones.** Retrieval precision
matters more than reducing file count. A user searching for a specific
concept should find a focused 300-word file, not wade through an 800-word
file where their answer is buried in paragraph 4.

## Proposal Table Format

Present the mapping as a table:

| # | Finding | Source Research Doc | Target Context File | Target Area | Words (est.) |
|---|---------|-------------------|-------------------|-------------|-------------|
| 1 | Event loops use cooperative multitasking | 2026-03-12-asyncio.md | event-loop-model.md | docs/context/async/ | ~350 |
| 2 | CPU-bound work blocks the event loop | 2026-03-12-asyncio.md | cpu-bound-workarounds.md | docs/context/async/ | ~250 |
| 3 | Task scheduling patterns converge across frameworks | 2026-03-12-asyncio.md, 2026-03-12-trio.md | task-scheduling-patterns.md | docs/context/async/ | ~400 |

Note that row 3 shows a **cross-document merge** — findings from two
research documents combined into one context file.

## Confidence Carry-Forward

Each finding should note the confidence level from the source research:

- **HIGH** — state directly in the context file
- **MODERATE** — qualify with evidence basis
- **LOW** — flag uncertainty explicitly

See the distillation guidelines for how confidence maps to framing.

## Context File Requirements

Each proposed context file must have:

- A target area under `docs/context/`
- Estimated word count between 200-800 (advisory — note exceptions)
- At least one `related:` link to its source research document
- At least one `related:` link to a sibling context file from the batch
- `sources:` URLs carried forward from the source research
