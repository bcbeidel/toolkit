---
name: Pipeline Subagent Definitions
description: Create 9 self-contained agent definitions with deterministic gate checks, update skills to dispatch them, simplify pipeline to pure orchestration
type: plan
status: completed
branch: pipeline-subagents
related:
  - docs/designs/2026-03-12-pipeline-subagents-design.md
  - docs/plans/2026-03-12-research-pipeline-gates.md
  - docs/plans/2026-03-12-shared-research-references.md
---

# Pipeline Subagent Definitions

**Goal:** Unify research and distill execution through named agents with
discrete, evaluable capabilities. Skills own interaction, agents own
execution, one way to run. Each research phase gets its own agent with
a fresh context window — especially critical for CoVe verification
(Phases 7-8) where context pressure degrades claim accuracy. Deterministic
gate checks validate handoffs between agents.

**Scope:**

Must have:
- 7 research agents: framer, gatherer, evaluator, challenger, synthesizer,
  verifier, finalizer
- 2 distill agents: mapper, worker
- Self-contained agents — each body inlines methodology from shared
  reference files. No `skills`, `background`, or `isolation` in frontmatter.
- Deterministic gate check function (`check_gates`) validating all 6
  research phase gates
- Each agent runs gate check on entry and fails fast if preconditions
  not met
- `skills/research/SKILL.md` updated to dispatch agent chain with gate
  validation between dispatches
- `skills/distill/SKILL.md` updated to dispatch mapper + worker
- Pipeline becomes pure orchestration: invokes skills, manages validation
- Each agent has defined input/output contracts for independent evaluation

Won't have:
- Changes to shared reference files (content unchanged; agents derive
  from them)
- Changes to `execute-plan/SKILL.md`
- New skills
- Background or worktree dispatch (blocked by no-nesting constraint)
- Batch approval logic — approvals happen sequentially per skill
  invocation

**Approach:** Create 9 agent definitions in `agents/` using Claude Code's
native convention. Each agent body inlines the methodology from its
corresponding shared reference file(s) — no `skills` injection, agents
are self-contained. Agent bodies define input contracts, entry validation
(deterministic gate check), phase methodology, and output contracts.
Research agents form a sequential chain, handing off state through the
DRAFT document on disk. Each agent starts with a fresh context, reads
the document, does its phase, writes it back. Skills become thin
orchestrators that dispatch agents, run gate checks between dispatches,
and manage user approval gates. The pipeline simplifies to invoking
skills sequentially — no inline templates, no reference file assembly.

### Error classification and recovery

The skill orchestrator classifies agent failures using the two-axis
taxonomy from `error-classification-agent-systems.md`: retryability
(transient / correctable / structural) × origin phase (reasoning /
execution / verification).

**Recovery protocol per failure type:**

| Failure type | Example | Recovery | Budget |
|-------------|---------|----------|--------|
| Transient + execution | WebSearch 429, timeout, API 503 | Re-dispatch same agent, no mutation | 2 retries (3 total) |
| Correctable + execution | Gate check fails on exit (missing section, incomplete table) | Re-dispatch with gate check output as context mutation | 2 retries (3 total) |
| Correctable + reasoning | Agent misinterprets phase scope (e.g., evaluator searches for new sources) | Re-dispatch with explicit correction in dispatch prompt | 1 retry (2 total) |
| Structural + reasoning | Agent returns but file unmodified, or agent reports it cannot proceed | Escalate to user immediately, no retry | 0 retries |
| Structural + execution | Entry gate fails (previous agent didn't complete) | Do not dispatch — escalate to user with gate check output | 0 retries |

**Key rules:**
- Entry gate failure is always structural — the predecessor didn't
  finish. Never retry the current agent; fix the predecessor first.
- Exit gate failure is correctable — the agent did work but missed
  something. Re-dispatch with the gate check JSON as context.
- File-unmodified is structural — the agent didn't understand its task.
  Retrying won't help; escalate.
- Budget cap: 3 total attempts per agent per research task. On
  exhaustion, escalate to user with: agent name, attempt history,
  gate check output, and suggested next steps.

**Agent-specific failure patterns:**

| Agent | Common failure | Classification | Notes |
|-------|---------------|----------------|-------|
| Gatherer | No relevant search results | Correctable (widen terms) then structural (topic has no sources) | Retry with broader search strategy, then escalate |
| Gatherer | URL verification failures | Transient | Retry; URLs may be temporarily unreachable |
| Evaluator | Missing tier for some sources | Correctable | Re-dispatch with list of untiered sources |
| Challenger | No counter-evidence found | Not a failure — document absence in Challenge section | Agent should note "no disconfirming evidence found" |
| Verifier | URL fetch failures during re-verify | Transient | Retry individual URLs; mark persistently unavailable as `human-review` |
| Finalizer | Audit failures | Correctable | Re-dispatch with audit output |

### Observability

Agent execution is traced through three mechanisms, all lightweight
and fitting the existing CLI model. No external tracing infrastructure
required.

**1. Gate check JSON (deterministic, structured).**
Each gate check produces machine-readable JSON with pass/fail per
check. This is the primary trace artifact — it captures the state of
the DRAFT at each handoff. The skill logs gate check results between
dispatches, and agents log them on entry.

**2. Skill dispatch log (conversation-visible).**
The research skill announces each dispatch and gate result to the
user as it progresses through the chain:

```
Dispatching research-gatherer...
  → gatherer_exit gate: PASS (4/4 checks)
Dispatching research-evaluator...
  → evaluator_exit gate: FAIL (sources_have_tier: false)
  Re-dispatching research-evaluator (attempt 2/3)...
  → evaluator_exit gate: PASS (2/2 checks)
Dispatching research-challenger...
```

This gives the user (and any future evaluation harness) a real-time
trace of chain execution without infrastructure.

**3. Plan checkpoint annotations (persistent).**
When the pipeline invokes `/wos:research`, the plan task checkbox
records the outcome:

```markdown
- [x] Task N: Research topic X <!-- sha:abc1234 agents:7/7 retries:1 -->
```

The `agents:7/7` count and `retries:N` annotation persist across
sessions, giving resumption context about how cleanly the task ran.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `agents/research-framer.md` | Create | Read-only, frames research briefs (~85 lines) |
| `agents/research-gatherer.md` | Create | Phases 2-3: search, extract, URL verify (~140 lines) |
| `agents/research-evaluator.md` | Create | Phase 4: SIFT tier assignment (~80 lines) |
| `agents/research-challenger.md` | Create | Phase 5: counter-evidence (~70 lines) |
| `agents/research-synthesizer.md` | Create | Phase 6: findings construction (~50 lines) |
| `agents/research-verifier.md` | Create | Phases 7-8: CoVe + citation re-verify (~115 lines) |
| `agents/research-finalizer.md` | Create | Phase 9: structure + finalize (~70 lines) |
| `agents/distill-mapper.md` | Create | Read-only, proposes N:M mappings (~195 lines) |
| `agents/distill-worker.md` | Create | Writes context files from approved mappings (~80 lines) |
| `wos/research/assess_research.py` | Modify | Add `check_gates()` function |
| `skills/research/scripts/research_assess.py` | Modify | Add `--gate` CLI flag |
| `tests/test_assess_research.py` | Modify | Add gate check tests |
| `skills/research/SKILL.md` | Modify | Thin orchestrator dispatching agent chain |
| `skills/distill/SKILL.md` | Modify | Thin orchestrator dispatching mapper + worker |
| `skills/execute-plan/references/research-distill-pipeline.md` | Modify | Pure orchestration, invokes skills |

## Tasks

### Chunk 1: Deterministic Gate Checks

- [x] Task 1: Add `check_gates` function to assess_research.py <!-- sha:8f4a526 -->

  Extend `wos/research/assess_research.py` with a `check_gates(path)`
  function. It reads a research document and returns which phase gates
  pass or fail.

  **Return structure:**
  ```python
  {
      "file": path,
      "gates": {
          "gatherer_exit": {
              "pass": True/False,
              "checks": {
                  "draft_exists": bool,
                  "sources_table_present": bool,
                  "sources_have_urls": bool,
                  "extracts_present": bool
              }
          },
          "evaluator_exit": {
              "pass": True/False,
              "checks": {
                  "sources_have_tier": bool,
                  "sources_have_status": bool
              }
          },
          "challenger_exit": {
              "pass": True/False,
              "checks": {"challenge_section_exists": bool}
          },
          "synthesizer_exit": {
              "pass": True/False,
              "checks": {"findings_section_exists": bool}
          },
          "verifier_exit": {
              "pass": True/False,
              "checks": {
                  "claims_section_exists": bool,
                  "claims_table_has_rows": bool,
                  "no_unverified_claims": bool
              }
          },
          "finalizer_exit": {
              "pass": True/False,
              "checks": {
                  "draft_marker_absent": bool,
                  "type_is_research": bool,
                  "sources_non_empty": bool
              }
          }
      },
      "current_phase": "evaluator"  # highest passing gate + 1
  }
  ```

  Implementation notes:
  - Extend `_detect_sections` to also detect `challenge` heading
  - Add `_detect_table_columns(content, heading)` helper — finds a
    markdown table under a heading and checks column names
  - Add `_check_table_cells(content, heading, column, forbidden_value)`
    helper — scans cells in a column for forbidden values
  - All checks are string/regex matches — no LLM judgment
  - A gate "passes" when ALL its checks are True
  - `current_phase` is derived: the phase after the highest passing gate

  **Verify:**
  ```bash
  uv run python -m pytest tests/test_assess_research.py -v -k gate
  ```

- [x] Task 2: Add `--gate` flag to research_assess.py CLI <!-- sha:5bd4f93 -->

  Extend `skills/research/scripts/research_assess.py` to accept
  `--gate <phase>` alongside `--file`. When provided, run `check_gates`
  and output only the specified gate's result.

  Usage:
  ```bash
  # Check all gates
  uv run <plugin-skills-dir>/research/scripts/research_assess.py \
    --file docs/research/DRAFT-topic.md --gate all

  # Check specific gate
  uv run <plugin-skills-dir>/research/scripts/research_assess.py \
    --file docs/research/DRAFT-topic.md --gate evaluator_exit
  ```

  **Verify:** Run with `--gate all` on an existing research document
  and confirm JSON output with gate results.

- [x] Task 3: Add gate check tests <!-- sha:b7cf018 -->

  Add tests to `tests/test_assess_research.py` (or new file
  `tests/test_research_gates.py` if cleaner):

  - Test each gate with a DRAFT document that passes
  - Test each gate with a DRAFT document that fails (missing section,
    missing column, unverified claim)
  - Test `current_phase` derivation
  - Test on non-existent file returns all gates failed
  - Use inline markdown strings and `tmp_path` fixtures per conventions

  **Verify:**
  ```bash
  uv run python -m pytest tests/ -v -k gate
  ```

### Chunk 2: Research Agents

Each agent is self-contained: frontmatter defines identity and tools,
body inlines methodology from corresponding shared reference files,
includes input contract, entry validation, and output contract.

- [x] Task 4: Create research-framer agent <!-- sha:29ce175 -->

  Create `agents/research-framer.md`:
  - Frontmatter: `name: research-framer`,
    `description: Analyzes a research question and produces a structured
    brief with mode, sub-questions, and search strategy`,
    `tools: [Read, Glob, Grep]`
  - No `skills`, `background`, or `isolation`
  - Input contract: research question/topic, constraints, project root
  - Body inlines methodology from `frame.md` + `research-modes.md`
  - Output contract: structured brief (question, mode, SIFT rigor,
    sub-questions, search strategy, suggested output path)
  - Autonomy rules: read-only, no file writes, no web searches, no user
    prompts, return brief to dispatcher
  - No entry validation (first agent in chain, no DRAFT to check)

  **Verify:** `grep 'tools:' agents/research-framer.md` shows only
  Read, Glob, Grep. No `skills:`, `background:`, or `isolation:` in
  frontmatter. Body contains mode detection table from research-modes.md.

- [x] Task 5: Create research-gatherer agent <!-- sha:29ce175 -->

  Create `agents/research-gatherer.md`:
  - Frontmatter: `name: research-gatherer`,
    `description: Searches for sources, extracts content verbatim, and
    verifies URLs for a research investigation`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]`
  - No `skills`, `background`, or `isolation`
  - Input contract: approved brief fields (question, sub-questions, mode,
    search strategy, output path)
  - Body inlines methodology from `gather-and-extract.md` +
    `verify-sources.md` + relevant cli commands (url_checker)
  - Entry validation: none (first agent writing to disk, brief comes
    via dispatch prompt)
  - Output contract (phase gate): DRAFT exists with extracts for all
    sub-questions, sources table with verified URLs

  **Verify:** File exists. Tools include WebSearch and WebFetch.
  No `skills:` in frontmatter. Body contains verbatim extraction rules
  from gather-and-extract.md.

- [x] Task 6: Create research-evaluator agent <!-- sha:29ce175 -->

  Create `agents/research-evaluator.md`:
  - Frontmatter: `name: research-evaluator`,
    `description: Assigns SIFT tier classifications (T1-T5) to research
    sources based on authority, methodology, and corroboration`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash]`
  - No `skills`, `background`, or `isolation`
  - No WebSearch or WebFetch
  - Input contract: path to DRAFT document with gathered sources
  - Entry validation: run `research_assess.py --file <path> --gate
    gatherer_exit`. If fails, STOP and return error.
  - Body inlines methodology from `evaluate-sources-sift.md`
  - Output contract (phase gate): all sources have Tier assignments
  - Bash tool needed for running gate check script

  **Verify:** `grep -c 'WebSearch' agents/research-evaluator.md`
  returns 0. Body contains SIFT tier hierarchy from
  evaluate-sources-sift.md. Entry validation references
  `gatherer_exit` gate.

- [x] Task 7: Create research-challenger agent <!-- sha:29ce175 -->

  Create `agents/research-challenger.md`:
  - Frontmatter: `name: research-challenger`,
    `description: Tests assumptions and finds counter-evidence for
    research findings to prevent confirmation bias`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]`
  - No `skills`, `background`, or `isolation`
  - Includes WebSearch/WebFetch — may need to search for counter-evidence
  - Input contract: path to DRAFT with evaluated sources
  - Entry validation: run `research_assess.py --file <path> --gate
    evaluator_exit`. If fails, STOP and return error.
  - Body inlines methodology from `challenge.md`
  - Output contract (phase gate): `## Challenge` section exists on disk

  **Verify:** File exists. Tools include WebSearch. Entry validation
  references `evaluator_exit` gate.

- [x] Task 8: Create research-synthesizer agent <!-- sha:29ce175 -->

  Create `agents/research-synthesizer.md`:
  - Frontmatter: `name: research-synthesizer`,
    `description: Synthesizes research extracts into structured findings
    with confidence levels and evidence attribution`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash]`
  - No `skills`, `background`, or `isolation`
  - No WebSearch or WebFetch
  - Input contract: path to DRAFT with challenge section
  - Entry validation: run `research_assess.py --file <path> --gate
    challenger_exit`. If fails, STOP and return error.
  - Body inlines methodology from `synthesize.md`
  - Output contract (phase gate): `## Findings` section exists on disk

  **Verify:** `grep -c 'WebSearch' agents/research-synthesizer.md`
  returns 0. Entry validation references `challenger_exit` gate.

- [x] Task 9: Create research-verifier agent <!-- sha:29ce175 -->

  Create `agents/research-verifier.md`:
  - Frontmatter: `name: research-verifier`,
    `description: Verifies research claims using Chain of Verification
    (CoVe) and re-verifies all citations against source material`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]`
  - No `skills`, `background`, or `isolation`
  - Includes WebFetch (re-verify citations against live sources) but
    NOT WebSearch (verification, not discovery)
  - Input contract: path to DRAFT with findings section
  - Entry validation: run `research_assess.py --file <path> --gate
    synthesizer_exit`. If fails, STOP and return error.
  - Body inlines methodology from `self-verify-claims.md` +
    `citation-reverify.md`
  - Note in body: this agent benefits from context isolation — fresh
    context with full attention budget for claim-by-claim verification
  - Output contract (phase gate): `## Claims` table populated, no
    `unverified` entries

  **Verify:** Tools include WebFetch but NOT WebSearch. Entry validation
  references `synthesizer_exit` gate.

- [x] Task 10: Create research-finalizer agent <!-- sha:29ce175 -->

  Create `agents/research-finalizer.md`:
  - Frontmatter: `name: research-finalizer`,
    `description: Restructures verified research documents for optimal
    readability, formats search protocol, and runs validation`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash]`
  - No `skills`, `background`, or `isolation`
  - No web tools
  - Input contract: path to DRAFT with verified claims
  - Entry validation: run `research_assess.py --file <path> --gate
    verifier_exit`. If fails, STOP and return error.
  - Body inlines methodology from `finalize.md` + relevant cli commands
    (reindex, audit)
  - Output contract (phase gate): DRAFT marker removed, audit passes

  **Verify:** `grep -c 'WebSearch\|WebFetch' agents/research-finalizer.md`
  returns 0. Tools include Bash. Entry validation references
  `verifier_exit` gate.

### Chunk 3: Distill Agents

- [x] Task 11: Create distill-mapper agent <!-- sha:21647fd -->

  Create `agents/distill-mapper.md`:
  - Frontmatter: `name: distill-mapper`,
    `description: Analyzes completed research documents and proposes N:M
    finding-to-context-file mappings with boundary rationale`,
    `tools: [Read, Glob, Grep]`
  - No `skills`, `background`, or `isolation`
  - Read-only tools — no Write, Edit, Bash, or web tools
  - Input contract: research document paths, target area root, user
    constraints
  - Body inlines methodology from `mapping-guide.md` +
    `distillation-guidelines.md`
  - Output contract: mapping table (Finding, Source Research Doc,
    Target Context File, Target Area, Words est.) with confidence
    carry-forward and one-concept test results
  - Autonomy rules: no file writes, return proposal to dispatcher

  **Verify:** `grep 'tools:' agents/distill-mapper.md` shows only
  Read, Glob, Grep. No `skills:` in frontmatter. Body contains
  boundary heuristics from mapping-guide.md.

- [x] Task 12: Create distill-worker agent <!-- sha:21647fd -->

  Create `agents/distill-worker.md`:
  - Frontmatter: `name: distill-worker`,
    `description: Writes context files from approved research-to-context
    mappings with bidirectional linking`,
    `tools: [Read, Write, Edit, Glob, Grep, Bash]`
  - No `skills`, `background`, or `isolation`
  - No web tools
  - Input contract: assigned findings, source research doc paths,
    target context file paths + areas, estimated word counts
  - Body inlines methodology from `distillation-guidelines.md` +
    relevant cli commands (reindex, audit)
  - Autonomy rules: no re-analysis of mapping, no user prompts

  **Verify:** `grep -c 'WebSearch' agents/distill-worker.md` returns 0.
  No `skills:` in frontmatter. Body contains quality criteria from
  distillation-guidelines.md.

### Chunk 4: Skill Updates

- [x] Task 13: Update research skill to dispatch agent chain <!-- sha:b192059 -->

  Modify `skills/research/SKILL.md` Workflow section:

  **Current:** Workflow says "All modes follow the same 9-phase
  workflow" and defers to shared references. The skill executes all
  9 phases inline.

  **New:** Workflow becomes a thin orchestrator:
  1. Accept research question from user
  2. Dispatch `research-framer` → returns structured brief
  3. Present brief to user → approve or reject with feedback
  4. If rejected, re-dispatch framer with feedback
  5. Dispatch research chain with gate validation between each:
     - `research-gatherer` — source discovery expert
       **Gate check:** `research_assess.py --file <path> --gate gatherer_exit`
     - `research-evaluator` — source quality expert
       **Gate check:** `research_assess.py --file <path> --gate evaluator_exit`
     - `research-challenger` — critical thinking expert
       **Gate check:** `research_assess.py --file <path> --gate challenger_exit`
     - `research-synthesizer` — findings expert
       **Gate check:** `research_assess.py --file <path> --gate synthesizer_exit`
     - `research-verifier` — verification expert
       **Gate check:** `research_assess.py --file <path> --gate verifier_exit`
     - `research-finalizer` — quality expert
       **Gate check:** `research_assess.py --file <path> --gate finalizer_exit`
  6. Present completion status to user

  **Error handling between dispatches (per Approach section):**
  After each agent completes, the skill runs the exit gate check and
  classifies the result:
  - Gate PASS → dispatch next agent
  - Gate FAIL → correctable. Re-dispatch with gate check JSON as
    context mutation (max 2 retries, 3 total attempts)
  - File unmodified → structural. Escalate to user immediately
  - Agent returned error → retry once without mutation (transient),
    then with error context (correctable), then escalate

  On exhaustion (3 attempts), present to user:
  - Agent name and phase
  - Gate check output (which checks failed)
  - Attempt history (what was tried)
  - Suggested action: "Re-dispatch with guidance" or "skip and
    complete manually"

  **Dispatch log (observability):**
  Announce each dispatch and gate result as the chain progresses:
  ```
  Dispatching research-gatherer...
    → gatherer_exit gate: PASS (4/4 checks)
  Dispatching research-evaluator...
    → evaluator_exit gate: FAIL (sources_have_tier: false)
    Re-dispatching research-evaluator (attempt 2/3)...
  ```

  All dispatch is foreground, sequential. No background or worktree
  parameters (no-nesting constraint).

  **Retain unchanged:** Mode Detection, Resumption Assessment, Phase
  Gates table, Common Deviations, Output Document Format, Examples,
  Key Rules.

  **Verify:** `grep -c 'research-framer' skills/research/SKILL.md`
  returns at least 1. `grep -c 'research-gatherer' skills/research/SKILL.md`
  returns at least 1. `grep -c 'research-verifier' skills/research/SKILL.md`
  returns at least 1. `grep -c 'gate' skills/research/SKILL.md`
  returns at least 1. Phase Gates table still present.

- [x] Task 14: Update distill skill to dispatch mapper + worker <!-- sha:1140f8e -->

  Modify `skills/distill/SKILL.md` Workflow section:

  **Current:** 5-step workflow (Input → Analyze → Propose → Generate →
  Integrate), skill does everything.

  **New:** Thin orchestrator:
  1. Input — accept research path(s) (unchanged)
  2. Dispatch `distill-mapper` → returns proposed mapping
  3. Present mapping to user → approve/edit/reject
  4. If rejected, re-dispatch mapper with feedback
  5. Dispatch `distill-worker` with approved mapping
  6. Present completion status to user

  All dispatch is foreground, sequential.

  **Retain unchanged:** Examples, Key Constraints.

  **Verify:** `grep -c 'distill-mapper' skills/distill/SKILL.md`
  returns at least 1. `grep -c 'distill-worker' skills/distill/SKILL.md`
  returns at least 1. Key Constraints section still present.

### Chunk 5: Pipeline Simplification

- [x] Task 15: Simplify pipeline to pure orchestration <!-- sha:fcabeaa -->

  Rewrite `skills/execute-plan/references/research-distill-pipeline.md`:

  **Current 7 phases → New 5 phases:**

  Phase 1 (Research): For each research task in the plan, invoke
  `/wos:research` with the research question. The skill handles
  everything: framer dispatch → brief approval → chain dispatch with
  gate validation. Sequential per task.

  Phase 2 (Validate Research): Run audit on all research outputs.
  Verify: frontmatter present, sources non-empty, DRAFT marker
  removed, Findings and Claims sections exist. Unchanged from
  current Phase 3.

  Phase 3 (Review): Present research batch summaries to user. User
  approves before distillation begins. Unchanged from current Phase 4.

  Phase 4 (Distill): For each research batch, invoke `/wos:distill`
  with the research document paths. The skill handles everything:
  mapper dispatch → mapping approval → worker dispatch. Sequential
  per batch.

  Phase 5 (Validate Distill): Run audit + verify bidirectional links
  + index sync. Unchanged from current Phase 7.

  **Remove:**
  - Inline prompt templates (current Phase 2 and Phase 6 templates)
  - Reference file assembly instructions
  - Direct subagent dispatch logic
  - Separate framing phase (skill handles)
  - Separate mapping phase (skill handles)

  **Checkpoint annotations:**
  When marking plan task checkboxes after skill invocation, include
  agent execution metadata:
  ```markdown
  - [x] Task N: Research topic X <!-- sha:abc1234 agents:7/7 retries:1 -->
  ```
  The `agents:N/M` count shows how many agents completed out of the
  chain. The `retries:N` count shows total re-dispatches across all
  agents. This gives resumption context about execution quality.

  **Error escalation from skills:**
  If a skill invocation fails (agent exhausts retry budget), the
  pipeline records partial progress:
  ```markdown
  - [ ] Task N: Research topic X <!-- blocked:research-evaluator attempt:3/3 -->
  ```
  The pipeline presents the failure to the user with the skill's
  error report (agent name, gate check output, attempt history) and
  offers: retry the task, skip it, or abort the pipeline.

  **Key Rules update:**
  - Pipeline invokes skills; skills dispatch agents
  - No inline prompt templates or reference file assembly
  - Agents are self-contained with inlined methodology
  - One way to run regardless of entry point
  - Sequential execution (no-nesting constraint)
  - Checkpoint annotations include agent execution metadata
  - Partial failure doesn't block the entire pipeline — user decides

  **Verify:**
  `grep -c 'Subagent prompt template' skills/execute-plan/references/research-distill-pipeline.md`
  returns 0.
  `grep -c '/wos:research' skills/execute-plan/references/research-distill-pipeline.md`
  returns at least 1.
  `grep -c '/wos:distill' skills/execute-plan/references/research-distill-pipeline.md`
  returns at least 1.
  `grep -c 'gather-and-extract.md' skills/execute-plan/references/research-distill-pipeline.md`
  returns 0 (no direct reference file assembly).

## Validation

1. All 9 agent files exist:
   ```bash
   ls agents/research-framer.md agents/research-gatherer.md \
      agents/research-evaluator.md agents/research-challenger.md \
      agents/research-synthesizer.md agents/research-verifier.md \
      agents/research-finalizer.md agents/distill-mapper.md \
      agents/distill-worker.md
   ```

2. No agent has `skills`, `background`, or `isolation` in frontmatter:
   ```bash
   for f in agents/*.md; do echo "=== $f ==="; head -15 "$f"; done
   ```
   Confirm no `skills:`, `background:`, or `isolation:` lines.

3. Read-only agents have no write tools:
   ```bash
   grep 'tools:' agents/research-framer.md agents/distill-mapper.md
   ```
   Shows only `[Read, Glob, Grep]`.

4. Verifier has WebFetch but NOT WebSearch:
   ```bash
   grep 'tools:' agents/research-verifier.md
   ```

5. Agents with entry validation reference the correct gate:
   ```bash
   grep -n 'gate' agents/research-evaluator.md agents/research-challenger.md \
     agents/research-synthesizer.md agents/research-verifier.md \
     agents/research-finalizer.md
   ```
   Each references its predecessor's exit gate.

6. Gate check tests pass:
   ```bash
   uv run python -m pytest tests/ -v -k gate
   ```

7. Research skill dispatches full chain with gate validation:
   ```bash
   grep -E 'research-framer|research-gatherer|research-verifier|research-finalizer' skills/research/SKILL.md
   ```
   Returns at least 4 matches.
   ```bash
   grep -c 'gate' skills/research/SKILL.md
   ```
   Returns at least 1.

8. Distill skill dispatches both agents:
   ```bash
   grep -E 'distill-mapper|distill-worker' skills/distill/SKILL.md
   ```
   Returns at least 2 matches.

9. Pipeline invokes skills, no inline templates:
   ```bash
   grep -c 'Subagent prompt template' skills/execute-plan/references/research-distill-pipeline.md
   ```
   Returns 0.

10. Shared reference files unchanged:
    ```bash
    git diff skills/_shared/
    ```

11. Full project audit passes:
    ```bash
    uv run scripts/audit.py --root . --no-urls
    ```
