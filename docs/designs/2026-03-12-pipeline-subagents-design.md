---
name: Pipeline Subagent Definitions
description: Unify research and distill execution through named agents — skills handle interaction, agents handle execution, one way to run
type: design
status: draft
related:
  - docs/designs/2026-03-12-research-pipeline-gates-design.md
  - skills/execute-plan/references/research-distill-pipeline.md
  - skills/research/SKILL.md
  - skills/distill/SKILL.md
  - docs/research/agent-directory-conventions.md
---

## Purpose

Unify research and distill execution through named Claude Code agents.
Today there are two execution paths: interactive skills do everything
in the foreground, and execute-plan embeds anonymous prompt templates for
background dispatch. This creates duplicated logic, assembly burden, and
no enforced identity for subagents.

The fix follows "one obvious way to run": skills own interaction, agents
own execution. Whether the user invokes `/wos:research` directly or
execute-plan runs the pipeline, the same skill handles interaction and
the same agents handle execution. Every discrete capability is isolated
in its own agent for independent evaluation, with controlled context
pressure at each phase.

**Problems addressed:**
1. Two execution paths — skills do Phases 2-9 inline; pipeline assembles
   anonymous subagents that do the same work differently
2. Assembly burden — execute-plan reads 10+ reference files to construct
   subagent prompts at dispatch time
3. No agent identity — subagent behavior is defined inline, not as a
   discoverable, testable agent
4. No tool or isolation guarantees — the pipeline describes desired
   behavior but cannot enforce restrictions
5. Duplicated orchestration — pipeline reimplements framing and mapping
   logic that already exists in the skills
6. No evaluation boundaries — framing, execution, mapping, and writing
   are interleaved in monolithic skill runs with no isolated units to test
7. Context pressure degrades verification — by Phase 7-8, the context
   is packed with search results and extracts, weakening CoVe accuracy

**Mechanism:** Claude Code's agent convention — markdown files with YAML
frontmatter in `agents/`. Each agent's body contains the full
methodology for its phase(s), inlined from the corresponding shared
reference files. No `skills` injection — agents are self-contained.
Skills remain the orchestrators that dispatch agents, validate handoff
gates, and manage user interaction.

## Behavior

### Architecture: One Way to Run

Both skills follow the same pattern: dispatch agents sequentially,
using the persistent DRAFT file on disk as the state handoff mechanism.
Each agent starts with a fresh context, reads the document, does its
work, writes it back. User gates live in the skill foreground between
agent dispatches.

```
User invokes              execute-plan invokes
/wos:research             /wos:research per task
      │                         │
      └────────┐   ┌────────────┘
               ▼   ▼
         ┌──────────────┐
         │ research     │  Accept question
         │ SKILL.md     │
         └──────┬───────┘
                │ dispatch
                ▼
         ┌──────────────┐
         │ research-    │  Phase 1: Frame the question
         │ framer       │  → returns structured brief
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research     │  Present brief → user approves
         │ SKILL.md     │
         └──────┬───────┘
                │ dispatch chain (each writes to DRAFT on disk)
                ▼
         ┌──────────────┐
         │ research-    │  Phases 2-3: Search, extract, verify URLs
         │ gatherer     │  → DRAFT with extracts + verified sources
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research-    │  Phase 4: SIFT tier assignment
         │ evaluator    │  → DRAFT with tiered sources
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research-    │  Phase 5: Counter-evidence, assumptions
         │ challenger   │  → DRAFT with challenge section
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research-    │  Phase 6: Produce findings
         │ synthesizer  │  → DRAFT with findings section
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research-    │  Phases 7-8: CoVe + citation re-verify
         │ verifier     │  → DRAFT with verified claims (fresh context)
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ research-    │  Phase 9: Structure, format, finalize
         │ finalizer    │  → final research doc
         └──────────────┘

User invokes              execute-plan invokes
/wos:distill              /wos:distill per batch
      │                         │
      └────────┐   ┌────────────┘
               ▼   ▼
         ┌──────────────┐
         │ distill      │  Accept research path(s)
         │ SKILL.md     │
         └──────┬───────┘
                │ dispatch
                ▼
         ┌──────────────┐
         │ distill-     │  Analyze research, propose N:M mapping
         │ mapper       │  → returns mapping table
         └──────┬───────┘
                ▼
         ┌──────────────┐
         │ distill      │  Present mapping → user approves
         │ SKILL.md     │
         └──────┬───────┘
                │ dispatch
                ▼
         ┌──────────────┐
         │ distill-     │  Generate context files + integrate
         │ worker       │
         └──────────────┘
```

The path is identical regardless of entry point. Execute-plan invokes
the skills; skills dispatch the agents. The pipeline document becomes
pure orchestration: phase ordering, validation gates, and dispatch
parameters — no research or distill logic of its own.

### State model and contracts

**Shared state via persistent file.** The DRAFT research document on
disk is the handoff mechanism between research agents. Each agent reads
the current document state, performs its phase, and writes the updated
document back.

**Contracts live in two places:**

1. **Agent body (self-contained).** Each agent defines its input
   expectations and output guarantees. The agent knows what state it
   needs to start and what state it must produce. This is the
   authoritative contract — the agent enforces it during execution.

2. **Skill orchestrator (Phase Gates table).** The research skill's
   Phase Gates table documents the full handoff chain. The skill
   validates the gate condition after each agent completes and before
   dispatching the next. If a gate fails, the skill can re-dispatch
   the agent or escalate to the user.

**Contract chain (research):**

| Handoff | Gate condition (what's on disk) |
|---------|--------------------------------|
| Framer → Gatherer | Approved brief (passed via dispatch prompt) |
| Gatherer → Evaluator | DRAFT with extracts for all sub-questions, sources table with verified URLs |
| Evaluator → Challenger | Sources table has Tier + Status columns for all sources |
| Challenger → Synthesizer | `## Challenge` section exists |
| Synthesizer → Verifier | `## Findings` section exists |
| Verifier → Finalizer | `## Claims` table populated, no `unverified` entries |
| Finalizer → Done | `<!-- DRAFT -->` removed, audit passes |

**Contract chain (distill):**

| Handoff | Gate condition |
|---------|---------------|
| Mapper → Skill | Mapping table returned to dispatcher |
| Skill → Worker | User-approved mapping passed via dispatch prompt |
| Worker → Done | Context files written, reindex + audit pass |

### Entry validation (deterministic gate checks)

**Principle: structure in code, quality in skills.** Gate conditions
are structural facts — section exists, column present, no marker found.
These are deterministic checks that belong in Python, not LLM judgment.

A `check_gates` function extends the existing `assess_research.py`
module. It reads a DRAFT document and returns which gates pass/fail:

```python
check_gates(path) → {
    "gatherer_exit": {  # = evaluator entry
        "pass": True,
        "checks": {
            "draft_exists": True,
            "sources_table_present": True,
            "sources_have_urls": True,
            "extracts_present": True
        }
    },
    "evaluator_exit": {  # = challenger entry
        "pass": False,
        "checks": {
            "sources_have_tier": False,
            "sources_have_status": True
        }
    },
    ...
}
```

**Three consumers, same checks:**

1. **Agent entry.** Each agent's body includes: "Run
   `research_assess.py --file <path> --gate <phase>` before starting.
   If the gate fails, STOP and return the error — do not attempt the
   work." The agent gets a clear diagnostic instead of silently
   producing garbage from bad input.

2. **Skill orchestrator.** Between dispatches, the skill runs the
   same gate check. If the previous agent's exit gate fails, the
   skill re-dispatches or escalates — before wasting a fresh context
   on the next agent.

3. **Evaluation harness (future).** To test an agent in isolation,
   feed it a DRAFT at a known state and verify the exit gate passes.
   The gate check is the assertion.

**Gate checks by phase:**

| Gate | Deterministic checks |
|------|---------------------|
| Gatherer exit | DRAFT file exists; sources table present with URL column; extracts present for sub-questions |
| Evaluator exit | Sources table has `Tier` column; all sources have tier values |
| Challenger exit | `## Challenge` heading exists |
| Synthesizer exit | `## Findings` heading exists |
| Verifier exit | `## Claims` heading exists; claims table has rows; no cell contains `unverified` |
| Finalizer exit | `<!-- DRAFT -->` marker absent; frontmatter has `type: research` and non-empty `sources` |

Each check is a string match or table parse — no LLM judgment needed.
The existing `_detect_sections` function in `assess_research.py`
already handles heading detection; gate checks extend this with table
column detection and cell value scanning.

**Fresh context per agent.** Each agent starts with a clean context
window containing only its system prompt (from the agent definition)
and the dispatch prompt. It then reads the DRAFT file from disk. No
accumulated search results, extracts, or findings from prior phases
pollute the context.

**Context isolation for verification.** The research-verifier is the
primary beneficiary: it receives a fresh context with just the research
document (findings + sources). Full attention budget is available for
CoVe claim verification and citation re-verification, with no leftover
search noise competing for attention.

### Self-contained agents (no skills injection)

Agents do NOT use the `skills` frontmatter field. Each agent's markdown
body contains the full methodology for its phase(s), inlined from the
corresponding shared reference file(s). This ensures:

- **Minimal context** — the agent gets only what it needs, not 12
  reference files when it uses 1-2
- **Self-contained execution** — the agent works identically regardless
  of skill loading behavior
- **Evaluation isolation** — each agent can be tested with just its
  body + a dispatch prompt, no dependency chain

The shared reference files (`skills/_shared/references/`) remain on
disk as the source of truth for methodology. They continue to serve:
- The interactive skills (loaded as skill references)
- Human readers reviewing the process
- Agent body content (derived from references during implementation)

**Methodology mapping:**

| Agent | Inlines content from | ~Lines |
|-------|---------------------|--------|
| research-framer | `frame.md` + `research-modes.md` | ~85 |
| research-gatherer | `gather-and-extract.md` + `verify-sources.md` + cli commands | ~140 |
| research-evaluator | `evaluate-sources-sift.md` | ~80 |
| research-challenger | `challenge.md` | ~70 |
| research-synthesizer | `synthesize.md` | ~50 |
| research-verifier | `self-verify-claims.md` + `citation-reverify.md` | ~115 |
| research-finalizer | `finalize.md` + cli commands | ~70 |
| distill-mapper | `mapping-guide.md` + `distillation-guidelines.md` | ~195 |
| distill-worker | `distillation-guidelines.md` + cli commands | ~80 |

### Symmetric skill pattern

Both skills follow the same three-phase pattern:

| Phase | Research skill | Distill skill |
|-------|---------------|---------------|
| 1. Analyze | Dispatch `research-framer` (read-only) | Dispatch `distill-mapper` (read-only) |
| 2. Approve | Present brief → user approves/rejects | Present mapping → user approves/rejects |
| 3. Execute | Dispatch research chain (gatherer → evaluator → challenger → synthesizer → verifier → finalizer) | Dispatch `distill-worker` |

On rejection in phase 2, re-dispatch the analysis agent with user
feedback. Skills are thin orchestrators: accept input, dispatch agents,
manage user gates, present results.

### Dispatch-time parameters

Agents define capabilities. Dispatchers control execution mode.

**Platform constraint: no subagent nesting.** Claude Code subagents
cannot dispatch other subagents — the Agent tool is not available to
them. This means a background agent cannot run a skill that dispatches
further agents. All agent dispatch must originate from the foreground
conversation.

This constraint shapes the execution model: both the interactive skill
and the pipeline dispatch agents from the foreground. Research agents
in the chain (gatherer through finalizer) always run sequentially in
the foreground — each reads the DRAFT file written by the previous
agent.

| Context | Dispatcher | Agent | Execution |
|---------|-----------|-------|-----------|
| `/wos:research` (direct) | research skill | research-framer | foreground |
| `/wos:research` (direct) | research skill | chain (gatherer → finalizer) | foreground, sequential |
| `/wos:distill` (direct) | distill skill | distill-mapper | foreground |
| `/wos:distill` (direct) | distill skill | distill-worker | foreground |
| pipeline (research) | execute-plan via `/wos:research` | all agents | foreground, sequential per task |
| pipeline (distill) | execute-plan via `/wos:distill` | all agents | foreground, sequential per batch |

Agents do NOT have `background` or `isolation` in their frontmatter.
All dispatch happens from the foreground conversation.

**Parallelism (future).** The current model runs research tasks
sequentially. Parallel dispatch across tasks would require one of:
- A monolithic background research agent per task that inlines all
  phases 2-9 (loses decomposition and context isolation)
- Wave-based dispatch: all gatherers in parallel, wait, all evaluators
  in parallel, etc. (complex worktree state management between waves)
- Relaxation of the no-nesting constraint by Claude Code

These are future enhancements if sequential execution proves too slow.
The agent definitions and contracts are unchanged — only the dispatch
pattern differs.

### Research agents

Each agent's body contains: input contract, inlined phase methodology,
output contract (phase gate), and autonomy rules.

#### research-framer

**File:** `agents/research-framer.md`

| Field | Value |
|-------|-------|
| `name` | `research-framer` |
| `description` | Analyzes a research question and produces a structured brief with mode, sub-questions, and search strategy |
| `tools` | `[Read, Glob, Grep]` |

**Input contract:** Research question/topic, stated constraints, project
root path.

**Body inlines:** `frame.md` (Phase 1 methodology) + `research-modes.md`
(mode table and SIFT rigor levels).

**Output contract:** Returns structured brief (restated question, mode,
SIFT rigor, sub-questions, search strategy, suggested output path).

**Autonomy rules:** Read-only. No file writes. No web searches. No user
prompts. Return brief to dispatcher.

#### research-gatherer

**File:** `agents/research-gatherer.md`

| Field | Value |
|-------|-------|
| `name` | `research-gatherer` |
| `description` | Searches for sources, extracts content verbatim, and verifies URLs for a research investigation |
| `tools` | `[Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]` |

**Input contract:** Approved brief fields (question, sub-questions, mode,
search strategy, output path).

**Body inlines:** `gather-and-extract.md` (Phase 2 methodology) +
`verify-sources.md` (Phase 3 methodology) + relevant cli commands
(url_checker).

**Output contract (phase gate):** DRAFT exists on disk with structured
extracts for all sub-questions, sources table with verified URLs.

#### research-evaluator

**File:** `agents/research-evaluator.md`

| Field | Value |
|-------|-------|
| `name` | `research-evaluator` |
| `description` | Assigns SIFT tier classifications (T1-T5) to research sources based on authority, methodology, and corroboration |
| `tools` | `[Read, Write, Edit, Glob, Grep]` |

**Input contract:** Path to DRAFT document with gathered sources.

**Body inlines:** `evaluate-sources-sift.md` (Phase 4 methodology —
SIFT framework, tier hierarchy T1-T6, intensity by mode, red flags).

**Output contract (phase gate):** All sources have Tier assignments in
the sources table.

#### research-challenger

**File:** `agents/research-challenger.md`

| Field | Value |
|-------|-------|
| `name` | `research-challenger` |
| `description` | Tests assumptions and finds counter-evidence for research findings to prevent confirmation bias |
| `tools` | `[Read, Write, Edit, Glob, Grep, WebSearch, WebFetch]` |

**Input contract:** Path to DRAFT document with evaluated sources.

**Body inlines:** `challenge.md` (Phase 5 methodology — assumptions
check, analysis of competing hypotheses, premortem).

**Output contract (phase gate):** `## Challenge` section exists on disk.

#### research-synthesizer

**File:** `agents/research-synthesizer.md`

| Field | Value |
|-------|-------|
| `name` | `research-synthesizer` |
| `description` | Synthesizes research extracts into structured findings with confidence levels and evidence attribution |
| `tools` | `[Read, Write, Edit, Glob, Grep]` |

**Input contract:** Path to DRAFT document with challenge section.

**Body inlines:** `synthesize.md` (Phase 6 methodology — confidence
level criteria, writing constraints, source attribution rules).

**Output contract (phase gate):** `## Findings` section exists on disk.

#### research-verifier

**File:** `agents/research-verifier.md`

| Field | Value |
|-------|-------|
| `name` | `research-verifier` |
| `description` | Verifies research claims using Chain of Verification (CoVe) and re-verifies all citations against source material |
| `tools` | `[Read, Write, Edit, Glob, Grep, WebFetch]` |

**Input contract:** Path to DRAFT document with findings section.

**Body inlines:** `self-verify-claims.md` (Phase 7 — CoVe procedure,
claim types, contradiction resolution) + `citation-reverify.md`
(Phase 8 — re-fetch sources, resolution statuses, human-review triggers).

**Context isolation:** This agent is the primary beneficiary of the
per-agent context model. It starts with a fresh context and reads only
the DRAFT document. Full attention budget is available for claim-by-claim
verification without accumulated search noise from Phases 2-4.

**Output contract (phase gate):** `## Claims` table populated, no
`unverified` entries.

#### research-finalizer

**File:** `agents/research-finalizer.md`

| Field | Value |
|-------|-------|
| `name` | `research-finalizer` |
| `description` | Restructures verified research documents for optimal readability, formats search protocol, and runs validation |
| `tools` | `[Read, Write, Edit, Glob, Grep, Bash]` |

**Input contract:** Path to DRAFT document with verified claims.

**Body inlines:** `finalize.md` (Phase 9 — restructuring convention,
search protocol formatting, quality checklist) + relevant cli commands
(reindex, audit).

**Output contract (phase gate):** DRAFT marker removed, audit passes.

### Distill agents

#### distill-mapper

**File:** `agents/distill-mapper.md`

| Field | Value |
|-------|-------|
| `name` | `distill-mapper` |
| `description` | Analyzes completed research documents and proposes N:M finding-to-context-file mappings with boundary rationale |
| `tools` | `[Read, Glob, Grep]` |

**Input contract:** Research document paths, target area root, user
constraints.

**Body inlines:** `mapping-guide.md` (boundary heuristics, splitting/
merging rules, one-concept test, proposal table format) +
`distillation-guidelines.md` (quality criteria, confidence mapping,
completeness constraint).

**Output contract:** Mapping table with Finding, Source Research Doc,
Target Context File, Target Area, Words (est.) columns. Includes
confidence carry-forward and one-concept test results.

**Autonomy rules:** Read-only. No file writes. Return proposal to
dispatcher.

#### distill-worker

**File:** `agents/distill-worker.md`

| Field | Value |
|-------|-------|
| `name` | `distill-worker` |
| `description` | Writes context files from approved research-to-context mappings with bidirectional linking |
| `tools` | `[Read, Write, Edit, Glob, Grep, Bash]` |

**Input contract:** Assigned findings, source research doc paths, target
context file paths + areas, estimated word counts.

**Body inlines:** `distillation-guidelines.md` (quality criteria,
splitting heuristics, confidence mapping, completeness constraint) +
relevant cli commands (reindex, audit).

**Output contract:** Context files written with frontmatter, bidirectional
links, confidence annotations. Reindex + audit pass.

### Research skill changes

**File:** `skills/research/SKILL.md`

The research skill becomes a thin orchestrator that provides context
about the agent chain and manages user interaction. Each agent is the
expert for its phase — the skill describes what each does but does not
duplicate methodology.

**Current flow:**
1. Frame (interactive) → user approves brief
2. Gather and Extract (skill does it)
3. ... Phases 3-9 (skill does them all)

**New flow:**
1. Accept research question from user
2. Dispatch `research-framer` — the framing expert. It analyzes the
   question, identifies the research mode, breaks into sub-questions,
   and produces a structured brief.
3. Present brief to user → approve or reject with feedback
4. If rejected, re-dispatch framer with feedback
5. Dispatch research chain, validating each phase gate before
   dispatching the next agent:
   - `research-gatherer` — the source discovery expert. Searches,
     extracts content verbatim, verifies URLs.
     **Gate:** DRAFT with extracts + verified sources.
   - `research-evaluator` — the source quality expert. Assigns SIFT
     tiers (T1-T5) to every source.
     **Gate:** All sources have Tier assignments.
   - `research-challenger` — the critical thinking expert. Tests
     assumptions, finds counter-evidence, runs premortem.
     **Gate:** `## Challenge` section exists.
   - `research-synthesizer` — the findings expert. Produces structured
     findings with confidence levels and source attribution.
     **Gate:** `## Findings` section exists.
   - `research-verifier` — the verification expert. Runs CoVe on every
     claim, re-verifies citations against live sources.
     **Gate:** `## Claims` table complete, no `unverified` entries.
   - `research-finalizer` — the quality expert. Restructures for
     readability, formats protocol, runs audit.
     **Gate:** DRAFT marker removed, audit passes.
6. Present completion status to user

Dispatch mode for the chain is context-dependent: foreground when the
user invokes `/wos:research` directly, background with worktree
isolation when execute-plan directs parallel dispatch.

The skill retains Phase Gates table, Common Deviations, and Output
Document Format sections as methodology documentation. These remain
the canonical reference for the process even though agents now contain
inlined methodology in their bodies.

### Distill skill changes

**File:** `skills/distill/SKILL.md`

Same thin orchestrator pattern as research.

**Current flow:**
1. Input — accept research path
2. Analyze — identify findings (skill does it)
3. Propose — present mapping table, user approves
4. Generate — write context files (skill does it)
5. Integrate — reindex, audit (skill does it)

**New flow:**
1. Input — accept research path(s)
2. Dispatch `distill-mapper` — the mapping expert. Analyzes research,
   identifies findings, applies boundary heuristics, proposes N:M
   mapping.
3. Present mapping to user → approve/edit/reject
4. If rejected, re-dispatch mapper with feedback
5. Dispatch `distill-worker` — the context writing expert. Writes
   files with frontmatter, bidirectional links, confidence annotations.
   Runs reindex + audit.
   **Gate:** Context files written, audit passes.
6. Present completion status to user

### Pipeline document changes

**File:** `skills/execute-plan/references/research-distill-pipeline.md`

The pipeline becomes pure orchestration. It invokes skills; skills
dispatch agents. The 7-phase structure simplifies because skills now
handle framing, approval, and agent dispatch internally.

**Current 7 phases → New 5 phases:**

| Phase | What execute-plan does |
|-------|----------------------|
| 1. Research | For each research task in the plan, invoke `/wos:research` with the research question. The skill handles everything: framer dispatch → brief approval → chain dispatch (gatherer → evaluator → challenger → synthesizer → verifier → finalizer). Sequential per task. |
| 2. Validate Research | Run audit on all research outputs. Check: frontmatter present, sources non-empty, DRAFT marker removed, Findings and Claims sections exist. Unchanged from current Phase 3. |
| 3. Review | Present research batch summaries to user. User approves before distillation begins. Unchanged from current Phase 4. |
| 4. Distill | For each research batch, invoke `/wos:distill` with the research document paths. The skill handles everything: mapper dispatch → mapping approval → worker dispatch. Sequential per batch. |
| 5. Validate Distill | Run audit + verify bidirectional links + index sync. Unchanged from current Phase 7. |

**What execute-plan needs to know about skill invocation:**

```
For each research task:
  1. Invoke /wos:research with the research question from the plan task
  2. The skill will:
     a. Dispatch research-framer → present brief → get user approval
     b. Dispatch gatherer → evaluator → challenger → synthesizer →
        verifier → finalizer (sequential, gate-checked)
     c. Return completion status
  3. On success, mark the plan task checkbox
  4. On failure, apply recovery patterns (retry, then escalate)

After all research tasks complete:
  5. Run validation (Phase 2 above)
  6. Present for user review (Phase 3 above)

For each distill batch:
  7. Invoke /wos:distill with research document paths
  8. The skill will:
     a. Dispatch distill-mapper → present mapping → get user approval
     b. Dispatch distill-worker with approved mapping
     c. Return completion status
  9. On success, mark the plan task checkbox

After all distill batches complete:
  10. Run validation (Phase 5 above)
```

**Removed from pipeline:**
- Inline prompt templates (current Phase 2 and Phase 6 templates)
- Reference file assembly instructions (no reading 10+ files to
  build subagent prompts)
- Direct subagent dispatch logic (skills handle this now)
- Separate framing phase (each `/wos:research` invocation handles
  its own framing)
- Separate mapping phase (each `/wos:distill` invocation handles
  its own mapping)

**Retained unchanged:**
- Validation phases (structural checks, audit, link verification)
- Review phase (user reviews research batch before distillation)
- Key Rules: user-facing gates in foreground, feedback before
  progression, partial execution acceptable

## Components

### Research agents (7)
1. `agents/research-framer.md` — framing expert (~85 lines)
2. `agents/research-gatherer.md` — source discovery expert (~140 lines)
3. `agents/research-evaluator.md` — source quality expert (~80 lines)
4. `agents/research-challenger.md` — critical thinking expert (~70 lines)
5. `agents/research-synthesizer.md` — findings expert (~50 lines)
6. `agents/research-verifier.md` — verification expert (~115 lines)
7. `agents/research-finalizer.md` — quality expert (~70 lines)

### Distill agents (2)
8. `agents/distill-mapper.md` — mapping expert (~195 lines)
9. `agents/distill-worker.md` — context writing expert (~80 lines)

### Gate check script (1)
10. `wos/research/assess_research.py` — extend with `check_gates()`
    function for deterministic phase gate validation
11. `skills/research/scripts/research_assess.py` — expose `--gate`
    flag for agent and skill invocation

### Skill updates (2)
12. `skills/research/SKILL.md` — thin orchestrator with agent chain,
    gate validation between dispatches, and agent descriptions
13. `skills/distill/SKILL.md` — thin orchestrator with mapper + worker

### Pipeline update (1)
14. `research-distill-pipeline.md` — pure orchestration, invokes skills

## Constraints

- No `skills` field in agent frontmatter — agents are self-contained
  with inlined methodology
- Shared reference files remain on disk as source of truth for skills
  and humans
- Agent body content is derived from shared references during
  implementation — methodology updates require updating the agent body
- No new skills
- No changes to `execute-plan/SKILL.md` — it already defers to the
  pipeline document
- Agents do not set `background` or `isolation` in frontmatter —
  dispatchers control execution mode
- No subagent nesting — Claude Code subagents cannot dispatch other
  subagents (Agent tool unavailable). All agent dispatch originates
  from the foreground conversation. This means the pipeline invokes
  skills (foreground), which dispatch agents (foreground). No
  background agent chains.
- User-facing gates remain in the skill foreground — agents never
  prompt the user
- One way to run — execute-plan invokes the same skills as the user;
  skills dispatch the same agents regardless of caller
- Sequential execution — research tasks and distill batches run one
  at a time. Parallel dispatch is a future enhancement blocked by
  the no-nesting constraint.
- Shared state via persistent file — agents hand off state through
  the DRAFT document on disk
- Fresh context per agent — each agent starts clean, reads state from
  disk, maximizing attention for its specific task

## Acceptance Criteria

1. All 9 agent files exist in `agents/` with no `skills`, `background`,
   or `isolation` in frontmatter
2. Each agent body contains inlined methodology from the corresponding
   shared reference file(s) — self-contained, no runtime dependencies
3. Each agent body includes explicit input contract and output contract
   (phase gate condition)
4. Each agent runs deterministic gate check on entry — fails fast with
   diagnostic if preconditions not met
5. `check_gates()` function validates all 6 research phase gates with
   deterministic structural checks (no LLM judgment)
6. Research skill runs gate checks between dispatches — same checks
   agents run on entry
7. Research skill describes the full agent chain with gate validation
   between each dispatch, framing each agent as the expert for its phase
8. `/wos:research` dispatches the full agent chain — same path whether
   invoked by user or by execute-plan
9. `/wos:distill` dispatches mapper then worker — same path whether
   invoked by user or by execute-plan
10. Pipeline invokes `/wos:research` and `/wos:distill` rather than
    reimplementing their logic
11. Inline prompt templates removed from pipeline document
12. Pipeline validation and review phases unchanged in substance
13. No subagent nesting — all agent dispatch from foreground conversation
14. Each agent is independently evaluable — dispatch with a test input,
    verify output matches contract, gate check passes
15. research-verifier starts with fresh context — no accumulated search
    results from earlier phases
