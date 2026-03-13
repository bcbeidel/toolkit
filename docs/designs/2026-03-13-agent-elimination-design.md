---
name: Agent Elimination Design
description: Design for removing static agent definitions in favor of dynamic prompt composition from enriched reference files and MANIFEST.md
type: design
status: draft
related:
  - docs/designs/2026-03-13-composable-pipeline-design.md
  - skills/_shared/references/MANIFEST.md
  - skills/research/SKILL.md
  - skills/distill/SKILL.md
---

# Agent Elimination Design

**Goal:** Remove all 9 static agent definitions (`agents/`) and compose
equivalent subagent prompts dynamically from enriched reference files +
MANIFEST.md. Zero information loss, single source of truth for all stage
knowledge.

**Key decisions:**
- Reference files become the complete single source per stage
- Orchestrator composes the full prompt at dispatch time
- `agents/` directory deleted entirely

## 1. Reference File Contract (Updated)

### Single-Reference Stage Template

```markdown
---
name: "Stage Name Reference"
description: "One-line description"
stage: evaluate
pipeline: research
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

## Purpose

One paragraph: what this stage does and why.

## Input

What the stage receives:
- **Path to DRAFT document** with [prerequisite state description]

## Methodology

[Existing methodology content — unchanged]

## Output

What must be on disk after this stage completes:
- [Specific structural requirements]
- [Column/section/marker expectations]

## Gate

Gate name: `<stage>_exit`

```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py \
  --file <path> --gate <stage>_exit
```

## Constraints

- [Behavioral boundaries — what the stage must NOT do]
- [Tool restrictions — e.g., "Do not use WebSearch"]
- [Scope limits — e.g., "Do not modify findings structure"]
```

### Multi-Reference Stage Convention

For stages that span multiple reference files (gatherer: 3 files, verifier:
2 files, finalizer: 2 files), the **primary file** holds the contracts and
constraints. Secondary files hold methodology only.

**Primary file:** The first file listed in MANIFEST.md for that stage.

| Stage | Primary File | Secondary Files |
|-------|-------------|-----------------|
| gather | gather-and-extract.md | verify-sources.md, cli-commands.md |
| verify | self-verify-claims.md | citation-reverify.md |
| finalize | finalize.md | cli-commands.md |
| map | mapping-guide.md | distillation-guidelines.md |

Primary file contains: Purpose, Input, full Methodology for its phase,
Output (covering the combined stage output), Gate, Constraints.

Secondary files contain: Purpose, Methodology only. No Input, Output, Gate,
or Constraints sections (those belong to the primary).

**cli-commands.md** is a supporting reference, not a stage methodology. It
has no contracts — it's included in composed prompts as a utility reference
when the stage uses CLI tools.

### What Changes in Each Reference File

**Files that need new sections added:**

| File | Add | Content Source |
|------|-----|---------------|
| frame.md | `tools:` frontmatter, Constraints | framer agent frontmatter + autonomy rules |
| gather-and-extract.md | `tools:` frontmatter, Output (combined with verify), Constraints | gatherer agent frontmatter + output contract + autonomy rules |
| verify-sources.md | (secondary — no contracts needed) | — |
| evaluate-sources-sift.md | `tools:` frontmatter, Constraints | evaluator agent frontmatter + autonomy rules |
| challenge.md | `tools:` frontmatter, Constraints | challenger agent frontmatter + autonomy rules |
| synthesize.md | `tools:` frontmatter, Constraints | synthesizer agent frontmatter + autonomy rules |
| self-verify-claims.md | `tools:` frontmatter, Output (combined with citation-reverify), Constraints, Context Isolation note | verifier agent frontmatter + output contract + autonomy rules + context isolation paragraph |
| citation-reverify.md | (secondary — no contracts needed) | — |
| finalize.md | `tools:` frontmatter, Constraints | finalizer agent frontmatter + autonomy rules |
| mapping-guide.md | `tools:` frontmatter, Output (combined with guidelines), Constraints | mapper agent frontmatter + output contract + autonomy rules |
| distillation-guidelines.md | `tools:` frontmatter, Constraints | worker agent frontmatter + autonomy rules |

**Files that need no changes:**
- research-modes.md (supporting reference, no stage contracts)
- cli-commands.md (utility reference)
- resumption.md (supporting reference)

### Handling Stage-Specific Behavioral Guidance

Content that isn't methodology or constraints but adds behavioral context:

| Content | Current Location | Destination |
|---------|-----------------|-------------|
| Context isolation note | verifier agent line 21-25 | self-verify-claims.md — new `## Context Model` section before Methodology |
| Anti-anchoring prompt | challenger agent line 64-65 | challenge.md — inline in ACH procedure (it's methodology) |
| Absence-as-valid-finding | challenger agent line 103-105 | challenge.md — add to Output section |
| WebFetch-only restriction | verifier agent line 127-128 | self-verify-claims.md — Constraints section |
| Annotate unverifiable/human-review in body | finalizer agent line 63-64 | finalize.md — inline in Final Verification step |
| Summary search count format | finalizer agent line 53 | finalize.md — inline in Format Search Protocol step |
| Deferred sources comment format | gatherer agent line 93-95 | gather-and-extract.md — inline in methodology |

**Principle:** If it's _how to do the work_, it goes in Methodology.
If it's _what not to do_, it goes in Constraints. If it's _why this stage
is structured this way_, it goes in a Context Model note (verifier only).

## 2. MANIFEST.md Schema (Updated)

Current columns: Stage, Files, Purpose.

New columns: **Tools**, **Entry Gate**, **Role**.

```markdown
## Research Pipeline References

| Stage | Role | Files | Tools | Entry Gate | Purpose |
|-------|------|-------|-------|------------|---------|
| frame | Framing expert — analyzes questions, decomposes into sub-questions | research/frame.md, research/research-modes.md | Read, Glob, Grep | — | Question analysis, mode detection, sub-question decomposition |
| gather | Source discovery expert — finds, extracts, and verifies sources | research/gather-and-extract.md, research/verify-sources.md, research/cli-commands.md | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch | — | Source discovery, verbatim extraction, URL verification |
| evaluate | Source evaluation expert — applies SIFT framework to assess source quality | research/evaluate-sources-sift.md | Read, Write, Edit, Glob, Grep, Bash | gatherer_exit | SIFT tier assignment (T1-T5), red flag detection |
| challenge | Critical thinking expert — tests assumptions and finds counter-evidence | research/challenge.md | Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch | evaluator_exit | Assumptions check, ACH, premortem |
| synthesize | Synthesis expert — organizes findings with confidence calibration | research/synthesize.md | Read, Write, Edit, Glob, Grep, Bash | challenger_exit | Confidence-annotated findings with source attribution |
| verify | Verification expert — verifies claims via CoVe and citation re-verification | research/self-verify-claims.md, research/citation-reverify.md | Read, Write, Edit, Glob, Grep, Bash, WebFetch | synthesizer_exit | Chain of Verification (CoVe), citation re-verification |
| finalize | Finalization expert — restructures, validates, and publishes | research/finalize.md, research/cli-commands.md | Read, Write, Edit, Glob, Grep, Bash | verifier_exit | Lost-in-the-middle restructuring, search protocol formatting, validation |

## Distill Pipeline References

| Stage | Role | Files | Tools | Entry Gate | Purpose |
|-------|------|-------|-------|------------|---------|
| map | Mapping expert — analyzes research and proposes finding-to-context-file mappings | distill/mapping-guide.md, distill/distillation-guidelines.md | Read, Glob, Grep | — | Finding boundaries, N:M mapping, one-concept test |
| write | Context file writer — distills findings into focused reference documents | distill/distillation-guidelines.md | Read, Write, Edit, Glob, Grep, Bash | — | Context file quality criteria, confidence carry-forward |
```

**Design notes:**
- **Role** column provides the "You are the..." framing for composed prompts. One sentence, generated into the prompt header.
- **Tools** column is the authoritative tool list. Reference file `tools:` frontmatter mirrors this (MANIFEST.md is the registry; reference frontmatter is for standalone use).
- **Entry Gate** of `—` means no prerequisite gate (framer and gatherer are first stages; distill stages use SKILL.md-level checks).
- MANIFEST.md stays human-readable markdown tables. No YAML, no JSON.
- The first file in the Files column is the **primary** reference (holds contracts and constraints).

## 3. Prompt Composition Template

When the orchestrator delegates a stage, it composes the prompt from
MANIFEST.md metadata + reference file contents.

### Template

```
# {Stage Title}

You are the {role} for the {pipeline} pipeline. Your job is to
{purpose}. You execute this stage of the {pipeline} process.

{context_model_note — only if present in primary reference file}

## Entry Validation

Before starting work, run the gate check:
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py \
  --file <path> --gate {entry_gate}
```
If the gate fails, STOP and return the error.

## Input Contract

You receive via dispatch prompt:
{input section from primary reference file}

## Methodology

{methodology from primary reference file}

{methodology from secondary reference file(s), if any}

## Output Contract

{output section from primary reference file}

## Constraints

{constraints section from primary reference file}
- Do not prompt the user for input.
```

### Assembly Rules

1. **Role framing** — generated from MANIFEST.md `Role` and `Purpose` columns.
2. **Entry validation** — generated from MANIFEST.md `Entry Gate` column.
   Omitted entirely if entry gate is `—`.
3. **Context model note** — included only if the primary reference file has
   a `## Context Model` section (currently only self-verify-claims.md).
4. **Input** — read from primary reference file's `## Input` section.
5. **Methodology** — concatenate from all reference files listed in
   MANIFEST.md `Files` column, in order. Primary file methodology first,
   then secondary files. Each file's methodology is included under its
   own heading.
6. **Output** — read from primary reference file's `## Output` section.
7. **Constraints** — read from primary reference file's `## Constraints`
   section. Always append "Do not prompt the user for input." (universal
   constraint).
8. **Tools** — not in the prompt body. Passed as dispatch metadata from
   MANIFEST.md `Tools` column. The orchestrator uses this to configure
   the subagent's tool access.

### Concrete Example: Research Verifier

MANIFEST.md row:
- Stage: verify
- Role: Verification expert — verifies claims via CoVe and citation re-verification
- Files: research/self-verify-claims.md, research/citation-reverify.md
- Tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
- Entry Gate: synthesizer_exit

Composed prompt:

```markdown
# Research Verifier

You are the verification expert for the research pipeline. Your job is to
verify claims via Chain of Verification (CoVe) and citation re-verification.
You execute this stage of the research process.

**Context isolation.** You are the primary beneficiary of the per-agent
context model. You start with a fresh context containing only this
system prompt and the dispatch prompt. Your full attention budget is
available for claim-by-claim verification, with no accumulated search
results from earlier phases competing for attention.

## Entry Validation

Before starting work, run the gate check:
```bash
uv run <plugin-skills-dir>/research/scripts/research_assess.py \
  --file <path> --gate synthesizer_exit
```
If the gate fails, STOP and return the error. Do not attempt
verification on a document without completed findings.

## Input Contract

You receive via dispatch prompt:
- **Path to DRAFT document** with findings section completed

## Methodology

### Phase 7: Self-Verify Claims (CoVe)

[Full content from self-verify-claims.md methodology section]

### Phase 8: Citation Re-Verify

[Full content from citation-reverify.md methodology section]

## Output Contract

The DRAFT document must have:
- `## Claims` table populated with all extracted claims
- No cells containing `unverified` in the Status column
- All claims resolved to: verified, corrected, removed, unverifiable,
  or human-review

## Constraints

- Use WebFetch only for re-verification of existing citations, not for
  discovering new sources (no WebSearch).
- Do not modify findings structure — only update claim statuses and
  correct factual errors.
- Do not prompt the user for input.
```

**This prompt is functionally equivalent to the current
`agents/research-verifier.md`** — same tools, same methodology, same
constraints, same context isolation note, same output contract.

## 4. Information Migration Table

### research-framer

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Glob, Grep]` | Agent frontmatter | MANIFEST.md Tools column + frame.md `tools:` frontmatter |
| Role: "framing expert... do not search, write, or interact" | Agent line 12-15 | MANIFEST.md Role column (role part) + frame.md Constraints (restrictions) |
| Input contract (question, constraints, project root) | Agent lines 17-22 | frame.md Input section (already partially there, needs structured format) |
| Step 7: Suggest output path | Agent lines 96-98 | frame.md methodology — add as step |
| Output contract (7 structured items) | Agent lines 100-110 | frame.md Output section (expand existing) |
| Autonomy: read-only, no web searches, no user prompts | Agent lines 112-120 | frame.md Constraints section |
| Full mode matrix with Intensity column | Agent lines 36-44 | Already in research-modes.md — no migration needed |
| Full/partial challenge definitions | Agent lines 60-61 | Already in research-modes.md challenge sub-steps table |

### research-gatherer

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]` | Agent frontmatter | MANIFEST.md Tools column + gather-and-extract.md `tools:` frontmatter |
| Role: "source discovery expert" | Agent line 17-20 | MANIFEST.md Role column |
| Input contract (6 bullet points) | Agent lines 22-30 | gather-and-extract.md Input section (expand) |
| Deferred sources comment format | Agent lines 93-95 | gather-and-extract.md — inline in methodology |
| Output contract (4 requirements) | Agent lines 117-125 | gather-and-extract.md Output section (expand to cover combined gather+verify) |
| Autonomy: 3 rules | Agent lines 127-131 | gather-and-extract.md Constraints section |
| Phase 3 verify content | Agent lines 101-115 | Already in verify-sources.md — no migration needed |

### research-evaluator

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash]` | Agent frontmatter | MANIFEST.md Tools column + evaluate-sources-sift.md `tools:` frontmatter |
| Role: "source evaluation expert" | Agent line 14-16 | MANIFEST.md Role column |
| Entry gate: `gatherer_exit` | Agent lines 19-26 | MANIFEST.md Entry Gate column (already planned) |
| Input contract | Agent lines 29-32 | evaluate-sources-sift.md Input section (expand) |
| Output contract (3 requirements) | Agent lines 89-94 | evaluate-sources-sift.md Output section (expand) |
| Autonomy: no new sources, no synthesize, no prompt | Agent lines 96-100 | evaluate-sources-sift.md Constraints section |

### research-challenger

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch]` | Agent frontmatter | MANIFEST.md Tools column + challenge.md `tools:` frontmatter |
| Role: "critical thinking expert" | Agent line 17-19 | MANIFEST.md Role column |
| Entry gate: `evaluator_exit` | Agent lines 21-29 | MANIFEST.md Entry Gate column |
| Input contract | Agent lines 31-34 | challenge.md Input section (expand) |
| Anti-anchoring: "What would someone who disagrees propose?" | Agent line 64-65 | challenge.md — inline in ACH procedure (it's methodology guidance) |
| WebSearch/WebFetch authorization | Agent lines 95-96 | challenge.md — move to end of Methodology ("You may use WebSearch and WebFetch...") |
| Absence-as-valid-finding note | Agent lines 103-105 | challenge.md Output section |
| Output contract | Agent lines 98-105 | challenge.md Output section (expand) |
| Autonomy: challenge only, no prompt | Agent lines 107-110 | challenge.md Constraints section |

### research-synthesizer

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash]` | Agent frontmatter | MANIFEST.md Tools column + synthesize.md `tools:` frontmatter |
| Role: "synthesis expert" | Agent line 14-16 | MANIFEST.md Role column |
| Entry gate: `challenger_exit` | Agent lines 20-28 | MANIFEST.md Entry Gate column |
| Input contract | Agent lines 30-33 | synthesize.md Input section (expand) |
| Output contract (3 requirements) | Agent lines 63-68 | synthesize.md Output section (expand) |
| Autonomy: no new sources, no modify prior sections, no prompt | Agent lines 70-74 | synthesize.md Constraints section |

### research-verifier

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash, WebFetch]` | Agent frontmatter | MANIFEST.md Tools column + self-verify-claims.md `tools:` frontmatter |
| Role: "verification expert" | Agent line 16-19 | MANIFEST.md Role column |
| Context isolation paragraph | Agent lines 21-25 | self-verify-claims.md — new `## Context Model` section before Methodology |
| Entry gate: `synthesizer_exit` | Agent lines 27-35 | MANIFEST.md Entry Gate column |
| Input contract | Agent lines 37-40 | self-verify-claims.md Input section (expand) |
| WebFetch-only restriction (no WebSearch) | Agent line 127-128 | self-verify-claims.md Constraints section |
| Output contract (3 requirements) | Agent lines 117-123 | self-verify-claims.md Output section (expand to cover combined Phase 7+8) |
| Autonomy: no modify findings, no prompt | Agent lines 129-131 | self-verify-claims.md Constraints section |
| Phase 8 content | Agent lines 88-115 | Already in citation-reverify.md — no migration needed |
| human-review triggers list | Agent lines 107-113 | Already in citation-reverify.md — verify parity |

### research-finalizer

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash]` | Agent frontmatter | MANIFEST.md Tools column + finalize.md `tools:` frontmatter |
| Role: "finalization expert" | Agent line 14-16 | MANIFEST.md Role column |
| Entry gate: `verifier_exit` | Agent lines 20-28 | MANIFEST.md Entry Gate column |
| Input contract | Agent lines 30-33 | finalize.md Input section (expand) |
| Annotate unverifiable/human-review in body | Agent line 63-64 | finalize.md — inline in Final Verification step |
| Search protocol summary line format | Agent line 53 | finalize.md — inline in Format Search Protocol step |
| Output contract (4 requirements) | Agent lines 85-91 | finalize.md Output section (expand) |
| Autonomy: no new content, no modify claims, no prompt | Agent lines 93-97 | finalize.md Constraints section |

### distill-mapper

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Glob, Grep]` | Agent frontmatter | MANIFEST.md Tools column + mapping-guide.md `tools:` frontmatter |
| Role: "mapping expert" | Agent line 12-14 | MANIFEST.md Role column |
| Input contract (3 items) | Agent lines 16-22 | mapping-guide.md Input section (expand) |
| Output contract (7 items) | Agent lines 132-141 | mapping-guide.md Output section (expand) |
| Autonomy: no write, no modify research, no prompt | Agent lines 143-148 | mapping-guide.md Constraints section |

### distill-worker

| Unique Content | Current Location | Destination |
|---------------|-----------------|-------------|
| `tools: [Read, Write, Edit, Glob, Grep, Bash]` | Agent frontmatter | MANIFEST.md Tools column + distillation-guidelines.md `tools:` frontmatter |
| Role: "context file writer" | Agent line 15-17 | MANIFEST.md Role column |
| Input contract (4 items) | Agent lines 19-26 | distillation-guidelines.md Input section (expand) |
| Frontmatter template (YAML) | Agent lines 47-60 | distillation-guidelines.md — inline in methodology |
| Bidirectional linking step | Agent lines 84-90 | distillation-guidelines.md — add as methodology step |
| Reindex and validate step | Agent lines 91-98 | distillation-guidelines.md — add as methodology step |
| Output contract (4 items) | Agent lines 100-106 | distillation-guidelines.md Output section (expand) |
| Autonomy: 3 rules | Agent lines 108-112 | distillation-guidelines.md Constraints section |

### Unresolved Items

**None.** Every piece of unique agent content has a clear destination.
The verifier's context isolation note is the only piece that required a
new section type (`## Context Model`), and it's specific to that one stage.

## 5. SKILL.md Changes

### Research SKILL.md

**Step 2 (Dispatch Framer):** Currently says "Dispatch `research-framer`".
Change to describe composing the framer prompt from reference files:

```
### Step 2: Compose and Dispatch Framer

Read the framer stage's reference files (per MANIFEST.md: frame.md,
research-modes.md). Compose the dispatch prompt using the prompt
composition template:
- Role from MANIFEST.md
- Input: research question, detected mode, project root
- Methodology from reference files
- Output contract and constraints from frame.md

Dispatch with tools: Read, Glob, Grep (per MANIFEST.md).
```

**Step 4 (Execute Research Chain) — Delegate path:** Currently says
"Dispatch the named agent (e.g., `research-gatherer`)". Change to:

```
- **Delegate:** Read the stage's reference files (per MANIFEST.md).
  Compose the dispatch prompt using the prompt composition template
  (role + entry gate + input + methodology + output + constraints).
  Dispatch with the tools listed in MANIFEST.md for that stage.
  The subagent starts with a fresh context.
```

The inline path is unchanged — it already reads reference files directly.

**No structural changes needed.** The mode defaults table, decision rules,
override conditions, error handling, and gate checks all remain identical.
Only the _mechanism_ of delegation changes (compose from references instead
of dispatch a named agent file).

### Distill SKILL.md

**Step 2 (Dispatch Mapper):** Change from "Dispatch `distill-mapper`" to
compose from mapping-guide.md + distillation-guidelines.md.

**Step 4 (Execute Worker) — Delegate path:** Change from "Dispatch
`distill-worker`" to compose from distillation-guidelines.md.

Same pattern as research — compose prompt from reference files per
MANIFEST.md, dispatch with the stage's tools.

## 6. Migration Plan

### Phase 1: Enrich reference files (no deletions)

Add `tools:` frontmatter, Constraints sections, expanded Input/Output
sections, and stage-specific behavioral guidance to all primary reference
files. Add Context Model section to self-verify-claims.md.

**Verify:** Each enriched reference file contains all content from its
corresponding agent file. Diff the agent against the reference to confirm
zero content loss.

**Rollback:** Revert reference file changes. Agents still work.

### Phase 2: Update MANIFEST.md

Add Tools, Entry Gate, and Role columns. Designate primary files for
multi-reference stages.

**Verify:** MANIFEST.md columns are complete for all 9 stages. Cross-check
tools against agent frontmatter.

**Rollback:** Revert MANIFEST.md. Old format still works for inline
execution.

### Phase 3: Update SKILL.md dispatch instructions

Change delegate path in research SKILL.md Step 2 and Step 4, and distill
SKILL.md Steps 2 and 4 to use prompt composition from reference files
instead of named agent dispatch.

**Verify:** Run a research pipeline end-to-end using the updated SKILL.md
dispatch instructions. All gates pass.

**Rollback:** Revert SKILL.md changes. Agent files still exist.

### Phase 4: Delete agents/ directory

Remove all 9 agent files and the `agents/` directory.

**Verify:**
- `ls agents/` returns "No such file or directory"
- `uv run python -m pytest tests/ -v` — all tests pass
- `uv run scripts/audit.py --root .` — no new failures
- MANIFEST.md + reference files contain all former agent content

**Rollback:** `git checkout -- agents/` restores all agent files.

### Phase 5: Update AGENTS.md and documentation

Remove any references to the `agents/` directory from AGENTS.md,
CLAUDE.md, or other documentation. Update the composable pipeline design
doc's appendix ("What Does NOT Change" section said agent definitions
unchanged — that's now outdated).

**Verify:** `grep -r "agents/" docs/ AGENTS.md CLAUDE.md` returns no
stale references to the deleted directory.

### Phase 6: Clean up and validate

Run full test suite, audit, and manual review.

**Verify:**
- All tests pass
- Audit clean
- No references to `agents/` directory remain
- MANIFEST.md has complete stage metadata
- Every reference file for a stage has tools + contracts + constraints

## 7. Trade-off Analysis

### Maintenance burden

| Scenario | Before (agents + references) | After (references only) |
|----------|------------------------------|------------------------|
| Change SIFT methodology | Update evaluate-sources-sift.md AND research-evaluator.md | Update evaluate-sources-sift.md only |
| Change verifier tools | Update research-verifier.md frontmatter | Update self-verify-claims.md frontmatter + MANIFEST.md |
| Add a new stage | Create agent file + reference file + MANIFEST.md row | Create reference file + MANIFEST.md row |
| Change stage constraints | Update agent autonomy rules | Update reference Constraints section |

**Verdict:** Net improvement. Methodology changes (most common) go from
2 files to 1. Tool/constraint changes stay at ~2 files but move from
agent+reference to reference+MANIFEST (same count, better cohesion).

### Prompt fidelity

| Dimension | Before | After |
|-----------|--------|-------|
| Methodology content | Hand-copied from reference (drift risk) | Read directly from reference (zero drift) |
| Role framing | Hand-written per agent | Generated from MANIFEST.md Role column |
| Tool declarations | Agent frontmatter | MANIFEST.md (authoritative) + reference frontmatter (backup) |
| Constraints | Hand-written per agent | Read from reference Constraints section |

**Verdict:** Higher fidelity. The composed prompt assembles from the
source-of-truth files, eliminating copy drift. Role framing is slightly
more formulaic but functionally equivalent.

### Debugging

| Scenario | Before | After |
|----------|--------|-------|
| Inspect what a subagent receives | Read the agent file | Compose the prompt mentally from reference files + MANIFEST.md |
| Trace a methodology issue | Check both agent and reference, determine which diverged | Check reference file only |
| Verify tool access | Read agent frontmatter | Read MANIFEST.md Tools column |

**Verdict:** Mixed. Debugging dispatch prompts is slightly harder (mental
composition vs. reading one file). But tracing methodology issues is
simpler (one source of truth). A future script could render the composed
prompt for inspection if needed.

### Token efficiency

| Path | Before | After |
|------|--------|-------|
| Inline execution | Orchestrator reads reference files (~50-100 lines) | Identical — no change |
| Delegate execution | Agent file loaded as system prompt (~75-150 lines) | Composed prompt loaded (~75-150 lines, same content) |

**Verdict:** Neutral. The composed prompt is the same size as the agent
file because it contains the same content. No token savings or cost on
the delegation path. The win is in maintenance, not token count.

### Copilot compatibility

| Dimension | Before | After |
|-----------|--------|-------|
| Reference files | Usable by Copilot for inline methodology | Same, plus contracts and constraints |
| Agent files | Claude Code-specific (frontmatter format) | Eliminated — no platform lock-in |
| MANIFEST.md | Discovery index (stage → files) | Richer discovery (stage → files + tools + role + gates) |
| Stage knowledge | Split across 2 file types | Consolidated in reference files + MANIFEST.md |

**Verdict:** Improvement. Copilot (or any LLM agent framework) can read
MANIFEST.md to discover stages, read reference files for complete stage
knowledge, and compose its own dispatch prompts. No Claude Code-specific
agent format dependency.
