---
name: Research-Distill Pipeline
description: Five-phase orchestration pattern for plans with research and distillation workstreams, dispatching via skills
---

# Research-Distill Pipeline

Orchestration pattern for executing plans that contain research and
distillation workstreams. The pipeline invokes skills; skills dispatch
agents. All execution is sequential (no-nesting constraint — subagents
cannot dispatch other subagents).

## When to Apply

Use this pattern when a plan includes tasks that:
- Investigate multiple topics via research
- Follow research with distillation to convert findings into context files

## Five-Phase Pipeline

| Phase | Action | Gate |
|-------|--------|------|
| 1. Research | Invoke `/wos:research` per task | All research docs pass audit |
| 2. Validate Research | Run audit on research outputs | No structural failures |
| 3. Review | Present research summaries to user | User approves research batch |
| 4. Distill | Invoke `/wos:distill` per batch | All context files pass audit |
| 5. Validate Distill | Run audit + verify links + index sync | All validation passes |

---

### Phase 1: Research

For each research task in the plan, invoke `/wos:research` with the
research question. The skill handles the full chain internally:

1. Dispatches `research-framer` → returns structured brief
2. Presents brief to user → approval gate
3. Dispatches 6-agent research chain with gate validation between each:
   gatherer → evaluator → challenger → synthesizer → verifier → finalizer
4. Runs exit gate check after each agent

The skill manages error handling and retries per its own protocol
(see research skill for details). Execute-plan treats the skill
invocation as atomic — it either succeeds or reports failure.

Execute research tasks sequentially. Each `/wos:research` invocation
completes before the next begins.

---

### Phase 2: Validate Research

Verify research outputs are well-formed before user review.

**Entry:** All research skill invocations completed.

**Actions:**

1. Run `python <plugin-scripts-dir>/audit.py --root . --no-urls` to
   check structural validity of new research documents.
2. For each research document, verify:
   - Frontmatter present with `type: research`
   - `sources:` non-empty
   - `<!-- DRAFT -->` marker removed
   - `## Findings` section exists
   - `## Claims` section exists with no `unverified` entries
3. Report any failures to the user with the specific document and issue.

**Gate:** All research documents pass validation. Failures are fixed
(by re-invoking the research skill or manual intervention) before
proceeding.

---

### Phase 3: Review

Present research results for user review.

**Entry:** All research documents validated in Phase 2.

**Actions:**

1. Present a summary of each research document:
   - Title and research question
   - Key findings (with confidence levels: HIGH, MODERATE, LOW)
   - Source count and tier distribution
   - Limitations or gaps noted
2. Ask the user to review the research quality and completeness.
3. If the user provides feedback on specific documents, apply
   corrections before proceeding.

**Gate:** User explicitly approves the research batch. This is a hard
gate — do not begin distillation without explicit approval.

---

### Phase 4: Distill

For each research batch, invoke `/wos:distill` with the research
document paths. The skill handles the full process internally:

1. Dispatches `distill-mapper` → returns proposed mapping
2. Presents mapping to user → approval gate
3. Dispatches `distill-worker` with approved mapping
4. Worker writes context files, runs reindex and audit

Execute distillation tasks sequentially. Each `/wos:distill` invocation
completes before the next begins.

---

### Phase 5: Validate Distill

Verify distillation outputs are well-formed and properly linked.

**Entry:** All distill skill invocations completed.

**Actions:**

1. Run `python <plugin-scripts-dir>/reindex.py --root .` to regenerate
   indexes.
2. Run `python <plugin-scripts-dir>/audit.py --root . --no-urls` to
   check structural validity.
3. Verify bidirectional links:
   - Each context file links to its source research doc via `related:`
   - Source research docs link to generated context files via `related:`
4. Verify index sync: `_index.md` files match directory contents.
5. Report results to the user.

**Gate:** All validation passes. Failures are fixed before proceeding
to the next chunk or plan completion.

---

## Checkpoint Annotations

When marking plan task checkboxes after skill invocation, include
agent execution metadata:

```markdown
- [x] Task N: Research topic X <!-- sha:abc1234 agents:7/7 retries:1 -->
```

The `agents:N/M` count shows how many agents completed out of the
chain. The `retries:N` count shows total re-dispatches across all
agents. This gives resumption context about execution quality.

## Error Escalation from Skills

If a skill invocation fails (agent exhausts retry budget), the
pipeline records partial progress:

```markdown
- [ ] Task N: Research topic X <!-- blocked:research-evaluator attempt:3/3 -->
```

The pipeline presents the failure to the user with the skill's
error report (agent name, gate check output, attempt history) and
offers: retry the task, skip it, or abort the pipeline.

## Key Rules

- **Pipeline invokes skills; skills dispatch agents.** No inline
  prompt templates or reference file assembly at the pipeline level.
- **Agents are self-contained.** Each agent has its methodology inlined
  in its definition. No reference file reading at dispatch time.
- **One way to run.** The same skills and agents execute whether invoked
  directly by the user or via this pipeline.
- **Sequential execution.** No-nesting constraint means all agent
  dispatch is foreground, sequential. Parallelism is not available.
- **Never chain research and distill in a single invocation.** Multiple
  hard gates separate the phases.
- **Feedback before progression.** At every user-facing gate (brief
  approval, research review, mapping approval), corrections are applied
  before moving to the next phase.
- **Partial execution is acceptable.** If some research tasks fail or
  produce insufficient findings, the user may approve continuing with
  only the successful documents. Do not block the entire pipeline on
  a single failure.
- **Checkpoint annotations include agent execution metadata.** This
  persists execution quality across sessions.
