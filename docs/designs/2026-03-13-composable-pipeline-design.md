---
name: Composable Pipeline Design
description: Architecture for runtime inline/delegate decisions in research and distill pipelines, with dual-use reference files, preserved gate checks, and cross-platform discovery
type: design
status: draft
related:
  - docs/designs/2026-03-12-pipeline-subagents-design.md
  - skills/research/SKILL.md
  - skills/distill/SKILL.md
  - wos/research/assess_research.py
  - skills/execute-plan/references/research-distill-pipeline.md
---

## Purpose

Reduce token overhead and latency in the research and distill pipelines by
allowing the orchestrator to run stages inline (in its own thread) or delegate
to subagents at runtime — while preserving gate checks, instruction fidelity,
and evaluation capability.

The current design (implemented in the pipeline-subagents-design) enforces
"always subagent" — every stage runs as a fresh subagent. This is correct for
context isolation but expensive: each subagent invocation pays ~2-4K tokens in
dispatch overhead (system prompt loading, agent definition, dispatch prompt
construction) and adds latency for agent startup. For lightweight stages or
stages that benefit from shared context, inline execution can save both.

**This design does NOT replace the subagent architecture.** It extends it with
a runtime decision layer. The agent definitions, gate checks, and skill
orchestration remain unchanged. What changes is whether the orchestrator
executes a stage's methodology directly (inline) or dispatches the
corresponding agent (delegate).

---

## 1. Architecture Overview

```
                    ┌─────────────────────────────────┐
                    │        Skill Orchestrator        │
                    │  (research SKILL.md / distill)   │
                    └──────────────┬──────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │  Decision Engine   │
                         │  (per-stage rule)  │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
             ┌──────▼──────┐              ┌──────▼──────┐
             │   INLINE    │              │  DELEGATE   │
             │             │              │             │
             │ Orchestrator│              │ Subagent    │
             │ reads ref   │              │ loads agent │
             │ files, runs │              │ definition, │
             │ methodology │              │ fresh ctx   │
             │ in-thread   │              │ per stage   │
             └──────┬──────┘              └──────┬──────┘
                    │                             │
                    └──────────────┬──────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │    Gate Check      │
                         │ assess_research.py │
                         │  (deterministic)   │
                         └─────────┬─────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   Next Stage or   │
                         │     Complete      │
                         └───────────────────┘
```

**Key invariant:** Gate checks run between every stage transition regardless of
execution mode. The gate check code (`assess_research.py`) is the same binary
in both paths. It reads the DRAFT file from disk and validates structural
conditions. The execution mode is invisible to the gate.

**Research pipeline with decision points:**

```
User question
  │
  ▼
FRAMER ──────────── [always delegate: read-only, cheap, clean separation]
  │
  ▼ (user approves brief)
  │
GATHERER ────────── [always delegate: WebSearch/WebFetch, heavy I/O, large output]
  │ gate: gatherer_exit
  ▼
EVALUATOR ───────── [prefer inline: reads existing sources table, no I/O,
  │                  benefits from gatherer's context about source quality]
  │ gate: evaluator_exit
  ▼
CHALLENGER ──────── [conditional: inline for partial challenge (landscape,
  │                  historical), delegate for full challenge (deep-dive,
  │                  options) which needs WebSearch for counter-evidence]
  │ gate: challenger_exit
  ▼
SYNTHESIZER ─────── [prefer inline: reads challenge + extracts already in
  │                  context, no I/O, benefits from evaluator + challenger
  │                  context for better confidence calibration]
  │ gate: synthesizer_exit
  ▼
VERIFIER ────────── [conditional on mode: delegate for high-stakes modes
  │                  (deep-dive, options, technical, feasibility) where CoVe
  │                  accuracy justifies fresh context. Inline for low-stakes
  │                  modes (historical, open-source, landscape) where the
  │                  source count is small and effort should match stakes.]
  │ gate: verifier_exit
  ▼
FINALIZER ───────── [prefer inline: structural reformatting, no I/O,
  │                  light methodology]
  │ gate: finalizer_exit
  ▼
Done
```

**Distill pipeline:**

```
Research doc(s)
  │
  ▼
MAPPER ──────────── [always delegate: read-only, clean separation for
  │                  user approval loop]
  │ (user approves mapping)
  ▼
WORKER ──────────── [conditional: delegate for large mappings (>3 context
                     files) where the write volume benefits from fresh
                     context. Inline for small mappings (1-3 files) where
                     the mapper's context carries useful understanding of
                     the research material and the overhead of delegation
                     exceeds the work itself.]
```

---

## 2. Decision Heuristics

### Default assignments

| Stage | Default Mode | Override Condition |
|-------|-------------|-------------------|
| framer | delegate | — (always delegate) |
| gatherer | delegate | — (always delegate: I/O heavy) |
| evaluator | **inline** | delegate if >15 sources (large table = high token pressure) |
| challenger | **conditional** | inline if partial challenge mode (landscape, historical, open-source); delegate if full challenge (deep-dive, options, technical, feasibility, competitive) which requires WebSearch |
| synthesizer | **inline** | delegate if >8 sub-questions (unusual, signals high complexity) |
| verifier | **conditional** | delegate for high-stakes modes (deep-dive, options, technical, feasibility, competitive) where CoVe accuracy justifies fresh context; inline for low-stakes modes (historical, open-source, landscape) where source count is small and effort matches stakes |
| finalizer | **inline** | delegate if context window utilization >50% after prior inline stages |
| distill-mapper | delegate | — (always delegate: read-only, user approval gate) |
| distill-worker | **conditional** | inline for small mappings (1-3 context files) where mapper context carries useful research understanding; delegate for large mappings (>3 files) where write volume benefits from fresh context |

### Decision rules (ordered by priority)

1. **Effort matches stakes → mode-conditional.** High-stakes modes (deep-dive,
   options, technical, feasibility, competitive) justify the overhead of
   delegation for accuracy-sensitive stages like the verifier. Low-stakes
   modes (historical, open-source, landscape) should inline more aggressively
   — the source count is smaller, verification is simpler, and the token
   savings are proportionally larger.

2. **External I/O (WebSearch, WebFetch) → delegate.** Stages that make web
   requests (gatherer, full-mode challenger) benefit from dedicated context
   because search results expand the context window unpredictably.

3. **User approval gate → delegate.** Stages that produce output for user
   review (framer, mapper) should delegate so the skill orchestrator can
   cleanly present results without interleaved methodology context.

4. **Context dependency benefit → inline.** Stages where the orchestrator's
   accumulated context from prior stages improves output quality (evaluator
   knows source content from gatherer, synthesizer knows challenge results)
   should run inline unless overridden by rules 1-3.

5. **Token budget pressure → delegate.** If the orchestrator's context
   utilization exceeds ~50% after inline stages, switch remaining stages
   to delegate mode. This is a conservative threshold — quality degrades
   gradually, and catching it early preserves headroom for the remaining
   stages.

6. **Parallelization opportunity → delegate.** If future parallel dispatch
   becomes available (relaxed no-nesting constraint, wave-based execution),
   stages that could run concurrently with other work should prefer
   delegation. A delegated stage can run in a worktree or background
   context while the orchestrator handles other tasks. The orchestrator
   should note this as an acceptable reason to delegate even when inline
   would otherwise be preferred.

7. **Methodology weight → inline for light, delegate for heavy.** Stages
   with <80 lines of methodology (evaluator, synthesizer, finalizer) are
   good inline candidates. Stages with >100 lines (gatherer, verifier
   in high-stakes modes, challenger-full) are better as delegates.

### Practical defaults for common modes

| Research Mode | Inline Stages | Delegated Stages |
|--------------|---------------|------------------|
| deep-dive | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| landscape | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |
| technical | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| feasibility | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| competitive | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| options | evaluator, synthesizer, finalizer | framer, gatherer, challenger, verifier |
| historical | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |
| open-source | evaluator, challenger, synthesizer, verifier, finalizer | framer, gatherer |

In the best case (historical/open-source), 5 of 7 stages run inline — only
framer and gatherer delegate. This saves ~10-16K tokens in dispatch overhead
and eliminates 5 agent startup latencies. Effort matches stakes: simple
investigations don't pay for the full subagent chain.

---

## 3. Reference File Placement

### Recommendation: keep in `skills/_shared/references/`, add a discovery manifest

**Do not move the files.** The current location works for Claude Code
(skill references are loaded via `references:` frontmatter in SKILL.md).
Moving them to `docs/` or a top-level `references/` would break the existing
skill loading convention and gain nothing for Claude Code users.

**For cross-platform discovery (GitHub Copilot, other agents), add a manifest:**

```
skills/_shared/references/
├── MANIFEST.md                    ← NEW: discovery index
├── preflight.md
├── feedback-loop.md
├── plan-format.md
├── research/
│   ├── frame.md
│   ├── gather-and-extract.md
│   ├── verify-sources.md
│   ├── evaluate-sources-sift.md
│   ├── challenge.md
│   ├── synthesize.md
│   ├── self-verify-claims.md
│   ├── citation-reverify.md
│   ├── finalize.md
│   ├── research-modes.md
│   ├── resumption.md
│   └── cli-commands.md
└── distill/
    ├── distillation-guidelines.md
    └── mapping-guide.md
```

**`MANIFEST.md` structure:**

```markdown
# Reference File Manifest

Machine-readable index for cross-platform agent discovery.

## Research Pipeline References

| Stage | Files | Purpose |
|-------|-------|---------|
| frame | research/frame.md, research/research-modes.md | Question analysis, mode detection, sub-question decomposition |
| gather | research/gather-and-extract.md, research/verify-sources.md, research/cli-commands.md | Source discovery, extraction, URL verification |
| evaluate | research/evaluate-sources-sift.md | SIFT tier assignment (T1-T5) |
| challenge | research/challenge.md | Assumptions, ACH, premortem |
| synthesize | research/synthesize.md | Confidence-annotated findings |
| verify | research/self-verify-claims.md, research/citation-reverify.md | CoVe, citation re-verification |
| finalize | research/finalize.md, research/cli-commands.md | Restructuring, formatting, validation |

## Distill Pipeline References

| Stage | Files | Purpose |
|-------|-------|---------|
| map | distill/mapping-guide.md, distill/distillation-guidelines.md | Finding boundaries, N:M mapping |
| write | distill/distillation-guidelines.md, distill/cli-commands.md (future) | Context file writing, integration |
```

### Skill reference to MANIFEST.md

Add MANIFEST.md to the `references:` list in both `skills/research/SKILL.md`
and `skills/distill/SKILL.md`. This ensures:
- Claude Code loads the manifest alongside other references
- Any agent (Claude, Copilot, or future platforms) that reads the skill
  definition discovers the manifest and can follow the file paths
- The manifest is the single entry point for understanding which reference
  files exist and how they compose into pipeline stages

### Rationale

1. **Claude Code native:** `skills/_shared/references/` is the convention.
   The `references:` frontmatter in SKILL.md auto-loads them. Zero config.
   Adding MANIFEST.md to the references list makes it discoverable through
   the same mechanism.

2. **GitHub Copilot discovery:** Copilot agent mode reads `.github/copilot-instructions.md`
   or project documentation. The MANIFEST.md file can be referenced from
   Copilot's instruction files to provide the same stage-to-file mapping.
   Copilot doesn't have Claude Code's auto-loading, but it can read files
   by path — the manifest provides those paths. This is a key requirement.

3. **No duplication:** A single copy of each reference file. Agent definitions
   inline from these (at implementation time, not runtime). Skills load them
   via frontmatter. Copilot reads them via manifest paths. One source of truth.

4. **Minimal change:** No file moves, no broken paths, no migration risk.

---

## 4. Reference File Contract

### Template for dual-use reference files

Every reference file MUST follow this structure for use as both an inline
instruction set (when the orchestrator runs a stage) and a subagent prompt
component (inlined into agent definitions):

```markdown
---
name: [Stage Name] Reference
description: [One-line description of what methodology this covers]
stage: [stage identifier: frame|gather|evaluate|challenge|synthesize|verify|finalize|map|write]
pipeline: [research|distill]
---

## Purpose

[1-2 sentences: what this stage accomplishes and why it exists in the pipeline]

## Input

[What this stage expects to find on disk or receive as parameters]

## Methodology

[Full detailed instructions — SIFT framework, CoVe procedure, confidence
calibration, search budgets, etc. This is the methodology that MUST be
preserved at full fidelity. No summarization.]

## Output

[What this stage must produce — sections, tables, markers, frontmatter changes]

## Gate

[The exit gate condition that must be satisfied before the next stage can begin.
References the specific gate name in assess_research.py]
```

### Contract rules

1. **No model-specific syntax.** No XML tags (`<thinking>`), no
   `[INST]` markers, no system/user/assistant role annotations. Plain
   markdown only. Both Claude and Copilot parse markdown natively.

2. **Self-contained methodology.** Each reference file contains the full
   instructions for its stage. An agent or orchestrator reading only this
   file (plus the dispatch prompt) has everything needed to execute the stage.

3. **Composable multi-file stages.** Some stages combine multiple references
   (gatherer = gather-and-extract + verify-sources + cli-commands). The
   composition order is documented in MANIFEST.md. When running inline,
   the orchestrator reads and concatenates them. When delegating, the agent
   definition already contains the inlined composite.

4. **Gate section is documentation, not enforcement.** The reference file
   documents what gate condition applies. Enforcement is always in Python
   (`assess_research.py`), never in the reference file or agent definition.

### Multi-reference composition for inline execution

When the orchestrator runs a multi-reference stage inline, it reads the
files in the order specified by MANIFEST.md and treats them as a single
instruction set:

```
# Inline execution of gatherer stage
orchestrator reads:
  1. research/gather-and-extract.md  → search and extraction methodology
  2. research/verify-sources.md      → URL verification methodology
  3. research/cli-commands.md        → utility command reference

# These are concatenated in-context as the methodology for the stage.
# The orchestrator then executes the methodology directly.
```

When the same stage runs as a subagent, `agents/research-gatherer.md` already
contains the composite methodology (inlined during implementation). No runtime
file reading needed — the agent definition IS the prompt.

### Fidelity guarantee

The agent definition body and the reference file(s) for the same stage must
contain identical methodology. This is enforced by convention and verified
during migration:

- Reference files are the source of truth
- Agent definitions are derived from reference files during implementation
- Any methodology update goes to the reference file first, then propagates
  to the agent definition
- An evaluation harness (Section 5) can diff the outputs of inline vs.
  delegate execution to detect fidelity drift

---

## 5. Evaluation Framework

### Per-reference isolation testing

Each reference file can be tested independently by constructing a minimal
test harness:

```
Test input: DRAFT document at the expected entry state for the stage
Expected output: DRAFT document that passes the exit gate
Assertion: assess_research.py --gate <stage>_exit returns pass
```

**Test fixture pattern:**

```
tests/fixtures/research/
├── gatherer_entry.md     ← DRAFT with approved brief, no extracts
├── gatherer_exit.md      ← DRAFT with extracts + sources table (expected)
├── evaluator_entry.md    ← = gatherer_exit.md
├── evaluator_exit.md     ← sources table has Tier + Status columns
├── challenger_entry.md   ← = evaluator_exit.md
├── challenger_exit.md    ← Challenge section added
├── synthesizer_entry.md  ← = challenger_exit.md
├── synthesizer_exit.md   ← Findings section added
├── verifier_entry.md     ← = synthesizer_exit.md
├── verifier_exit.md      ← Claims table populated, no unverified
├── finalizer_entry.md    ← = verifier_exit.md
└── finalizer_exit.md     ← DRAFT marker removed, passes audit
```

Each fixture pair defines the contract boundary for one stage. The entry
fixture is the exit fixture of the previous stage.

### Evaluation dimensions

| Dimension | Metric | How to measure |
|-----------|--------|----------------|
| **Gate pass rate** | % of runs where exit gate passes on first attempt | Run stage N times against entry fixture, check gate |
| **Instruction fidelity** | Methodology steps executed vs. specified | Compare output sections against reference file step list |
| **Inline/delegate parity** | Output structural equivalence | Run same stage inline and delegated against same input, diff outputs, verify both pass gate |
| **Token efficiency** | Tokens consumed per stage | Measure prompt + completion tokens for inline vs. delegate |
| **Latency** | Wall-clock time per stage | Measure from dispatch to gate check completion |

### Gate integration with evaluation

The gate checks serve as the primary evaluation assertion:

1. **Structural correctness.** If the gate passes, the stage produced the
   required structural elements (sections, tables, columns, values).

2. **No false passes.** Gates check necessary conditions, not sufficient
   conditions. A stage could pass the gate with low-quality content. Quality
   evaluation requires human review or a separate LLM judge — but structural
   correctness is the minimum bar.

3. **Regression detection.** If a methodology change causes a previously-passing
   fixture to fail its gate, the regression is caught before deployment.

### Inline vs. delegate parity test

The critical evaluation for the composable design:

```
For each stage that can run inline:
  1. Prepare entry fixture
  2. Run stage INLINE (orchestrator reads reference files, executes methodology)
  3. Capture output, verify gate passes
  4. Reset to entry fixture
  5. Run stage DELEGATED (dispatch agent with same input)
  6. Capture output, verify gate passes
  7. Compare: both outputs must pass gate, structural sections must match
  8. Diff: content differences are acceptable (LLM non-determinism),
     structural differences are not (missing sections, wrong columns)
```

---

## 6. Trade-off Analysis

### Token cost

| | Current (always delegate) | Composable (inline where beneficial) |
|---|---|---|
| **Dispatch overhead per stage** | ~2-4K tokens (agent def + system prompt + dispatch prompt) | 0 tokens for inline stages |
| **Reference loading per inline stage** | N/A | ~1-3K tokens (reading reference files into context) |
| **Net per inline stage** | 2-4K overhead | 1-3K reference loading (saves 1-2K net) |
| **Pipeline total (deep-dive, 3 inline)** | ~18-28K dispatch overhead (7 agents) | ~12-20K (4 delegates + 3 inline reference loads) |
| **Pipeline total (landscape, 4 inline)** | ~18-28K dispatch overhead (7 agents) | ~10-16K (3 delegates + 4 inline reference loads) |
| **Estimated savings** | baseline | 25-40% reduction in dispatch overhead |

The savings come from eliminating system prompt + agent definition loading for
inline stages. Reference file loading is cheaper because it's only the
methodology, not the full agent scaffolding.

### Latency

| | Current | Composable |
|---|---|---|
| **Agent startup per stage** | ~2-5s (context initialization) | 0 for inline stages |
| **Pipeline total (7 stages)** | 7 startups = ~14-35s overhead | 3-4 startups = ~6-20s overhead |
| **Estimated savings** | baseline | 40-60% reduction in startup latency |

Inline stages execute immediately in the orchestrator's thread with no
startup delay. The methodology is already in context (loaded from reference
files or accumulated from prior stages).

### Context quality

| | Current | Composable |
|---|---|---|
| **Inter-stage knowledge** | Lost between stages (fresh context) | Preserved for inline stages (evaluator sees gatherer's source assessments) |
| **Verifier isolation** | Guaranteed (fresh context) | Mode-conditional: fresh context for high-stakes modes (deep-dive, options, technical, feasibility, competitive); inline for low-stakes modes where effort matches stakes |
| **Context pressure** | Low per stage (fresh start) | Accumulates across inline stages — mitigated by delegate override at ~50% utilization |
| **Attention allocation** | Full budget per stage | Shared across inline stages — heavier stages should delegate |

The context quality trade-off is the core tension. Inline execution preserves
inter-stage knowledge (good for evaluator, synthesizer) but increases context
pressure. The decision heuristics in Section 2 balance this with the principle
that effort should match stakes — high-stakes modes pay for isolation where it
matters (verifier), low-stakes modes inline aggressively to save overhead.

### Instruction fidelity

| | Current | Composable |
|---|---|---|
| **Source of truth** | Reference files → inlined in agent defs | Reference files → read inline OR inlined in agent defs |
| **Drift risk** | Agent def may diverge from reference file | Same drift risk + inline execution reads reference directly (lower drift) |
| **Fidelity guarantee** | Convention + manual review | Convention + parity test (Section 5) |

Composable execution actually *improves* fidelity for inline stages because
the orchestrator reads reference files directly at runtime, rather than
relying on a manually-inlined copy in the agent definition. The parity test
catches any divergence between the two execution paths.

### Complexity

| | Current | Composable |
|---|---|---|
| **Decision logic** | None (always delegate) | Per-stage rules with overrides (Section 2) |
| **Orchestrator responsibility** | Dispatch + gate check | Dispatch OR execute + gate check |
| **Debugging** | Clear boundary per stage (agent = stage) | Inline stages blur boundaries |
| **Evaluation** | Test each agent in isolation | Test each agent + test inline execution + parity test |

The primary cost of composability is orchestrator complexity. The decision
engine adds branching logic, and inline execution means the orchestrator
must understand methodology it previously delegated. This is mitigated by
keeping the decision rules simple (static defaults per mode, not dynamic
heuristics) and preserving the ability to fall back to always-delegate.

---

## 7. Migration Steps

### Phase 0: Prerequisites (no code changes)

- [ ] Verify all 9 agent definitions exist and match reference file content
- [ ] Verify all 6 gate checks pass for existing test fixtures
- [ ] Baseline token usage and latency for 2-3 research runs (for comparison)

### Phase 1: Add MANIFEST.md (low risk, no behavior change)

- [ ] Create `skills/_shared/references/MANIFEST.md` with stage-to-file mapping
- [ ] Add `stage` and `pipeline` frontmatter fields to each reference file
- [ ] Verify no existing behavior changes (reference files are additive)
- [ ] **Rollback:** Delete MANIFEST.md, revert frontmatter additions

### Phase 2: Add reference file contract enforcement (low risk)

- [ ] Add `Purpose`, `Input`, `Methodology`, `Output`, `Gate` sections to
      any reference files missing them (most already have this structure
      implicitly)
- [ ] Create test fixtures (`tests/fixtures/research/`) for entry/exit states
- [ ] Write gate-based assertions: for each fixture pair, verify
      `assess_research.py --gate <stage>_exit` passes on the exit fixture
- [ ] **Rollback:** Remove fixtures and test file

### Phase 3: Implement inline execution for evaluator (smallest inline candidate)

- [ ] Add inline execution path to research skill orchestrator:
      when mode decision says "inline", read reference files and execute
      methodology in-thread instead of dispatching agent
- [ ] Gate check runs identically in both paths
- [ ] Run parity test: same input → inline vs. delegate → both pass gate
- [ ] Measure token savings and latency improvement
- [ ] **Rollback:** Set evaluator decision to "always delegate"

### Phase 4: Extend inline to synthesizer and finalizer

- [ ] Enable inline execution for synthesizer (same pattern as evaluator)
- [ ] Enable inline execution for finalizer
- [ ] Run parity tests for both
- [ ] Measure cumulative token savings
- [ ] **Rollback:** Set any failing stage to "always delegate"

### Phase 5: Implement conditional challenger inline

- [ ] Add mode-conditional logic: partial challenge modes run inline,
      full challenge modes delegate
- [ ] Run parity test for both paths
- [ ] **Rollback:** Set challenger to "always delegate"

### Phase 5b: Implement mode-conditional verifier inline

- [ ] Add mode-conditional logic: low-stakes modes (historical, open-source,
      landscape) run verifier inline; high-stakes modes (deep-dive, options,
      technical, feasibility, competitive) delegate for context isolation
- [ ] Run parity test for both paths across representative modes
- [ ] Verify CoVe claim accuracy does not regress for inline path on
      low-stakes fixtures (fewer sources, simpler claims)
- [ ] **Rollback:** Set verifier to "always delegate"

### Phase 6: Add context pressure monitoring and parallelization heuristic

- [ ] Implement context utilization estimation (approximate from token count)
- [ ] Add override rule: if utilization >50% after inline stages, switch
      remaining stages to delegate
- [ ] Add parallelization hint: when the orchestrator detects an opportunity
      for concurrent work (e.g., multiple research tasks in a plan), prefer
      delegation for stages that could benefit from parallel execution
- [ ] Document the parallelization heuristic in the skill so orchestrators
      know it's an acceptable reason to delegate over inline
- [ ] Test with deliberately large research inputs
- [ ] **Rollback:** Remove monitoring, use static defaults only

### Phase 7: Cross-platform testing

- [ ] Test MANIFEST.md discovery from GitHub Copilot agent mode
- [ ] Verify Copilot can read reference files and follow methodology
- [ ] Document any Copilot-specific configuration needed
- [ ] **Rollback:** N/A (Copilot support is additive)

### Rollback strategy

Every phase has independent rollback. The composable design degrades
gracefully to the current always-delegate model by setting all stage
decisions to "delegate". Agent definitions, gate checks, and skill
orchestration remain unchanged — the inline execution path is additive,
not a replacement.

The kill switch is a single configuration change: set the decision engine
to always return "delegate". This can be done per-stage or globally.

---

## Appendix: What Does NOT Change

Preserving these is a hard constraint, not a goal:

1. **Gate checks** — `assess_research.py` functions, gate names, check logic:
   unchanged. Gates run between every stage transition regardless of mode.

2. **Agent definitions** — ~~All 9 agent files in `agents/` remain as-is.~~
   *Superseded: agent definitions were subsequently eliminated. Stage
   knowledge now lives in enriched reference files + MANIFEST.md.
   See `docs/designs/2026-03-13-agent-elimination-design.md`.*

3. **Skill orchestration pattern** — Skills dispatch agents (delegate) or
   execute methodology (inline). The sequential chain with gate validation
   between each stage is identical.

4. **DRAFT file as shared state** — The persistent file on disk is still
   the handoff mechanism. Inline stages write to the same file.

5. **No subagent nesting** — All dispatch originates from foreground.
   Inline execution is NOT nesting — it's the orchestrator doing the work
   itself instead of delegating.

6. **User-facing gates** — Framer brief approval and mapper table approval
   remain in the skill foreground, between agent dispatches.

7. **One way to run** — Whether invoked by user or by execute-plan, the
   same skill handles orchestration, the same decision rules apply, the
   same agents are used for delegated stages.

8. **Effort matches stakes** — The guiding principle for all inline/delegate
   decisions. High-stakes investigations (deep-dive, options, technical)
   pay for context isolation where it matters. Low-stakes investigations
   (historical, open-source, landscape) inline aggressively. This isn't
   a cost optimization — it's a design principle that runs through every
   decision in Section 2.
