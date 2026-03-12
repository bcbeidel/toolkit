---
name: Research-Distill Pipeline
description: Seven-phase orchestration pattern for plans with parallel research and distillation workstreams
---

# Research-Distill Pipeline

Orchestration pattern for executing plans that contain research and
distillation workstreams. All user-facing gates run in execute-plan's
foreground conversation. Subagents are autonomous workers that receive
approved inputs and inlined instructions.

## When to Apply

Use this pattern when a plan includes tasks that:
- Investigate multiple topics via research
- Follow research with distillation to convert findings into context files
- Can benefit from parallel execution within each phase

## Seven-Phase Pipeline

| Phase | Location | Mode | Gate |
|-------|----------|------|------|
| 1. Frame | execute-plan | Foreground | User approves all research briefs |
| 2. Research | subagents | Background (parallel) | All subagents complete |
| 3. Validate Research | execute-plan | Foreground | All research docs pass audit |
| 4. Review | execute-plan | Foreground | User approves research batch |
| 5. Map | distill agent | Foreground | User approves N:M mapping |
| 6. Distill | subagents | Background (parallel) | All subagents complete |
| 7. Validate Distill | execute-plan | Foreground | Audit + index sync pass |

---

### Phase 1: Frame

Generate research briefs and get user approval before any dispatch.

**Entry:** Plan has research tasks pending. Execute-plan is in
research-distill execution mode.

**Actions:**

For each research task in the current chunk:

1. Extract the research question from the plan task description.
2. Identify the research mode from the question framing:
   - "What do we know about X?" → deep-dive
   - "What's the landscape for X?" → landscape
   - "How does X work technically?" → technical
   - "Can we do X with our constraints?" → feasibility
   - "How does X compare to competitors?" → competitive
   - "Should we use A or B?" → options
   - "How did X evolve?" → historical
   - "What open source options exist for X?" → open-source
3. Break into 2-4 sub-questions that structure the investigation.
4. Declare search strategy: initial search terms and source types.
5. Write a 1-paragraph research brief:
   - State the question
   - List all stated constraints (time period, domain, stack, etc.)
   - Mark unstated dimensions as explicitly open-ended
   - Specify preferred source types

Present all briefs to the user as a batch. For each brief, the user
can **approve** or **reject with feedback**. Rejected briefs are revised
based on feedback and re-presented.

**Gate:** All briefs approved. Do not dispatch any research subagent
until every brief in the batch is approved.

---

### Phase 2: Research

Dispatch research tasks as parallel background subagents.

**Entry:** All research briefs approved in Phase 1.

**Actions:**

Dispatch one subagent per approved brief. Each subagent receives its
instructions **inlined in the prompt** — subagents do NOT invoke
`/wos:research` or read plugin cache files.

**Subagent prompt template:**

> You are executing a research investigation autonomously.
>
> **Research question:** [question from approved brief]
> **Sub-questions:** [sub-questions from approved brief]
> **Research mode:** [mode]
> **Search strategy:** [search terms and source types]
> **Output path:** docs/research/[target filename]
>
> **Research brief:**
> [full brief paragraph from Phase 1]
>
> Execute the research following the instructions below. Save the
> completed research document to the output path.
>
> ---
>
> [Full content of research-agent-payload.md inlined here]

All research subagents must complete before proceeding to Phase 3.
Failed agents are re-dispatched with the same inlined payload. After
3 total failures for the same task, escalate to user.

**Gate:** All research subagents returned (DONE, NEEDS_HELP, or BLOCKED).
All NEEDS_HELP and BLOCKED resolved.

---

### Phase 3: Validate Research

Verify research outputs are well-formed before user review.

**Entry:** All research subagents completed successfully.

**Actions:**

1. Run `uv run <plugin-scripts-dir>/audit.py --root . --no-urls` to
   check structural validity of new research documents.
2. For each research document, verify:
   - Frontmatter present with `type: research`
   - `sources:` non-empty
   - `<!-- DRAFT -->` marker removed
   - `## Findings` section exists
   - `## Claims` section exists with no `unverified` entries
3. Report any failures to the user with the specific document and issue.

**Gate:** All research documents pass validation. Failures are fixed
(by re-dispatch or manual intervention) before proceeding.

---

### Phase 4: Review

Present research results for user review.

**Entry:** All research documents validated in Phase 3.

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
gate — do not begin mapping or distillation without explicit approval.

---

### Phase 5: Map

Propose how research findings map to context files.

**Entry:** Research batch approved by user in Phase 4.

**Actions:**

Dispatch a **foreground** distill agent that reads all completed
research documents from the batch. The agent:

1. Identifies discrete findings across the full research corpus
2. Applies boundary heuristics from
   [distill-mapping-guide.md](distill-mapping-guide.md) to determine
   concept boundaries
3. Proposes an N:M mapping as a table:

| # | Finding | Source Research Doc | Target Context File | Target Area | Words (est.) |
|---|---------|-------------------|-------------------|-------------|-------------|
| 1 | [finding] | [research doc] | [filename] | docs/context/[area]/ | ~[N] |

4. Notes confidence level for each finding (carried from research)
5. Identifies cross-document merges where findings from multiple
   research docs should combine into one context file

Present the mapping to the user. The user can approve, edit, or reject
individual rows.

**Gate:** User approves the mapping. Rejected rows are revised based on
feedback. Approved mapping becomes the dispatch plan for Phase 6.

---

### Phase 6: Distill

Dispatch distillation tasks as parallel background subagents.

**Entry:** Mapping approved by user in Phase 5.

**Actions:**

Dispatch one subagent per target context file (or small group of related
files). Each subagent receives its instructions **inlined in the prompt**
— subagents do NOT invoke `/wos:distill` or read plugin cache files.

**Subagent prompt template:**

> You are writing context files from research findings.
>
> **Assigned findings:**
> [list of findings from approved mapping, with source research doc paths]
>
> **Target files:**
> [list of target context file paths and areas from approved mapping]
>
> **Instructions:**
>
> For each target file, write a 200-800 word context file with this
> frontmatter:
>
> ```yaml
> ---
> name: [Concise title]
> description: [One-sentence summary]
> type: reference
> sources:
>   - [Carry forward relevant URLs from source research]
> related:
>   - [Path to source research artifact]
>   - [Path to sibling context files from this batch]
>   - [Path to existing context files in the same area]
> ---
> ```
>
> **Structure:** Key insights first, detailed explanation in the middle,
> takeaways at the bottom (U-shape for retrieval).
>
> **Completeness constraint:** Verified findings must not be dropped or
> diluted to achieve U-shape structure. Accuracy and completeness are
> the constraints; U-shape is the goal.
>
> **Confidence mapping:**
> - HIGH — state directly: "X works because Y"
> - MODERATE — qualify: "Evidence suggests X, based on Y"
> - LOW — flag: "Early evidence indicates X, but Z remains uncertain"
>
> **Bidirectional linking:** Every context file must link to its source
> research doc via `related:`. Include cross-references to sibling
> context files from this batch.
>
> After writing all files, run:
> ```bash
> uv run <plugin-scripts-dir>/reindex.py --root .
> uv run <plugin-scripts-dir>/audit.py --root . --no-urls
> ```

All distill subagents must complete before proceeding to Phase 7.
Failed agents are re-dispatched. After 3 total failures, escalate.

**Gate:** All distill subagents returned successfully.

---

### Phase 7: Validate Distill

Verify distillation outputs are well-formed and properly linked.

**Entry:** All distill subagents completed successfully.

**Actions:**

1. Run `uv run <plugin-scripts-dir>/reindex.py --root .` to regenerate
   indexes.
2. Run `uv run <plugin-scripts-dir>/audit.py --root . --no-urls` to
   check structural validity.
3. Verify bidirectional links:
   - Each context file links to its source research doc via `related:`
   - Source research docs link to generated context files via `related:`
4. Verify index sync: `_index.md` files match directory contents.
5. Report results to the user.

**Gate:** All validation passes. Failures are fixed before proceeding
to the next chunk or plan completion.

---

## Key Rules

- **All user-facing gates run in the foreground.** Subagents are
  autonomous workers — they do not prompt the user for input.
- **Subagents receive inlined instructions.** Never have subagents
  invoke `/wos:research` or `/wos:distill` as skills. Never have
  subagents read from the plugin cache. Inline all instructions in
  the subagent prompt.
- **Never chain research and distill in a single subagent.** Multiple
  hard gates separate the phases. Each phase is a separate wave.
- **Feedback before progression.** At every user-facing gate (Phases 1,
  4, 5), corrections are applied before moving to the next phase.
- **Partial execution is acceptable.** If some research tasks fail or
  produce insufficient findings, the user may approve continuing with
  only the successful documents. Do not block the entire pipeline on
  a single failure.
- **Distill subagents are independent.** Each works from its assigned
  findings. They do not need to coordinate with each other.
