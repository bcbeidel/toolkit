---
name: distill
description: >
  Converts research artifacts into focused context documents. Use when the
  user wants to "distill research", "extract findings", "create context
  from research", "summarize research into context files", or
  "operationalize research".
argument-hint: "[path to research artifact]"
user-invocable: true
references:
  - ../_shared/references/distill/distillation-guidelines.md
  - ../_shared/references/distill/mapping-guide.md
  - ../_shared/references/preflight.md
---

# Distill

Convert research artifacts into focused context files.

**Prerequisite:** Before running any `uv run` command below, follow the preflight check in the [preflight reference](../_shared/references/preflight.md).

## Workflow

The skill dispatches two agents sequentially. All dispatch is foreground
(no-nesting constraint).

### Step 1: Input

Accept a research artifact path from the user. If none provided, scan
`docs/research/` for the most recently modified `.md` file and confirm.

### Step 2: Dispatch Mapper

Dispatch `distill-mapper` with the research document path(s), target
area root, and any user constraints. The mapper returns a proposed
finding-to-context-file mapping table.

### Step 3: Mapping Approval

Present the mapping table to the user. User approves, edits, or rejects
individual rows.

**Target Area must be under `docs/context/`.** If the user requests a
different location, write to `docs/context/` first (the canonical
location), then offer to copy files to the additional location.

If rejected, re-dispatch `distill-mapper` with the user's feedback.
Do not proceed without approval.

### Step 4: Dispatch Worker

Dispatch `distill-worker` with the approved mapping (assigned findings,
source research paths, target file paths, estimated word counts).

### Step 5: Completion

Present completion status to the user. Show which context files were
created, word counts, and any audit issues.

## Examples

<example>
**Distillation proposal table (Phase 3):**

| # | Finding | Target Area | Filename | Words (est.) |
|---|---------|-------------|----------|--------------|
| 1 | Event loops use cooperative multitasking, not preemptive threading | docs/context/async/ | event-loop-model.md | ~350 |
| 2 | `asyncio.gather()` vs `TaskGroup` tradeoffs for concurrent I/O | docs/context/async/ | concurrency-patterns.md | ~400 |
| 3 | CPU-bound work blocks the event loop; use `run_in_executor()` | docs/context/async/ | cpu-bound-workarounds.md | ~250 |
</example>

<example>
**Distilled context file (Phase 4):**

```yaml
---
name: "Event Loop Model"
description: "How asyncio's single-threaded event loop achieves concurrency through cooperative multitasking"
type: reference
sources:
  - https://docs.python.org/3/library/asyncio-eventloop.html
related:
  - docs/research/2026-02-10-asyncio-deep-dive.md
  - docs/context/async/concurrency-patterns.md
---
```

Tasks yield control at `await` points, allowing other tasks to run on the
same thread. This differs from threading...
</example>

## Key Constraints

- **User controls granularity.** They pick which findings become standalone
  files vs. which get folded into existing files. Propose, don't decide.
- **Context files target 200-800 words.** This is advisory. If a finding
  needs more space, note it and proceed.
- **Carry forward sources.** Each context file should trace back to the
  original evidence via `sources:` URLs.
- **Bidirectional linking.** New files link to research via `related:`.
  Research links to new files via `related:`. Ask before modifying.
