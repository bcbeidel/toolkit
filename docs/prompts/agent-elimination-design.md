---
name: Agent Elimination Design
description: Prompt for designing the removal of static agent definitions in favor of dynamic prompt composition from enriched reference files
---

You are a software architect specializing in LLM agent orchestration and prompt composition.

## Context

We have a research pipeline in a Claude Code plugin (wos) with 9 static agent definitions (`agents/*.md`) across two pipelines:

**Research pipeline** (7 agents, sequential with gate checks):
framer → gatherer → evaluator → challenger → synthesizer → verifier → finalizer

**Distill pipeline** (2 agents):
mapper → worker

We recently implemented a **composable pipeline** where the orchestrator (`skills/research/SKILL.md`, `skills/distill/SKILL.md`) decides at runtime whether to run each stage **inline** (execute methodology directly) or **delegate** (dispatch a subagent). This created a duplication problem: **70-90% of agent file content is verbatim from shared reference files** in `skills/_shared/references/`. The methodology lives in two places.

### What exists today

**Reference files** (`skills/_shared/references/research/*.md`, `distill/*.md`):
- Stage methodology (SIFT evaluation, CoVe, ACH, search budgets, etc.)
- Recently standardized with frontmatter (`name`, `description`, `stage`, `pipeline`)
- Recently added contract sections: Purpose, Input, Output, Gate
- Mapped to stages via `MANIFEST.md`

**Agent files** (`agents/*.md`) contain methodology copied from references plus these unique elements:
1. **Frontmatter `tools:` list** — which tools the agent can use (e.g., gatherer gets WebSearch+WebFetch; mapper gets Read+Glob+Grep only)
2. **Autonomy rules** — behavioral constraints (e.g., "Do not search for new sources", "Do not prompt the user", "Do not modify findings")
3. **Input contracts** — structured dispatch format (e.g., "You receive: Path to DRAFT document with evaluated sources")
4. **Output contracts** — explicit post-conditions (e.g., "Claims table populated, no unverified cells")
5. **Entry validation** — gate check commands (e.g., `research_assess.py --gate synthesizer_exit`)
6. **Role framing** — "You are the verification expert..." statements
7. **Context isolation notes** — verifier-specific: "You start with a fresh context... your full attention budget is available for claim-by-claim verification"
8. **Stage-specific behavioral guidance** not in references:
   - Challenger: "Anti-anchoring: ask 'What would someone who disagrees propose?'"
   - Challenger: "Absence of counter-evidence is a valid finding, not a failure"
   - Verifier: "Use WebFetch only for re-verification, not discovering new sources"
   - Finalizer: "Ensure unverifiable and human-review entries are annotated in the body"

**SKILL.md files** already contain:
- Execution Mode section with inline/delegate decision heuristics
- Mode defaults table (which stages inline vs delegate per research mode)
- Per-stage override conditions
- Gate check commands in the workflow
- The full dispatch sequence

**MANIFEST.md** maps stages to reference files with a Purpose column.

### Decisions already made

1. **Reference files become the complete single source** — add Constraints, Input Contract, and Output Contract sections so all stage knowledge lives in one place
2. **Orchestrator composes the full prompt at dispatch time** — assembles role framing + tools + contracts + methodology + constraints from reference files
3. **Delete `agents/` directory entirely** — no static agent files, no generated artifacts

### Stage-gate checks (unchanged)

Deterministic Python validation (`wos/research/assess_research.py`):
- `gatherer_exit` — DRAFT exists, sources table has URL column, extracts present
- `evaluator_exit` — sources table has Tier and Status columns
- `challenger_exit` — Challenge section exists
- `synthesizer_exit` — Findings section exists
- `verifier_exit` — Claims table with rows, no unverified cells
- `finalizer_exit` — DRAFT marker removed, type: research, non-empty sources

## Task

Design how to eliminate the `agents/` directory by enriching reference files and updating the orchestrator's dispatch logic, ensuring zero information loss.

Address these specific concerns:

### 1. Reference file enrichment

The reference files already have Purpose, Input, Output, and Gate sections (added in the composable pipeline work). They need to absorb the remaining agent-unique content. Design the exact sections to add and their format. Consider:

- **Constraints section** — autonomy rules vary per stage (mapper can't write; verifier can't WebSearch; challenger CAN WebSearch). How should these be structured?
- **Tools declaration** — currently in agent frontmatter. Should this go in reference file frontmatter, the Constraints section, or MANIFEST.md?
- **Stage-specific behavioral guidance** — the anti-anchoring prompt, context isolation note, absence-as-valid-finding note. These aren't methodology but they're not constraints either. Where do they belong?
- **Multi-reference stages** — gatherer uses 3 reference files, verifier uses 2, finalizer uses 2. When the orchestrator composes a prompt, it concatenates multiple files. Which file in a multi-reference stage holds the Constraints and Input/Output Contract? The primary file? A dedicated file? All files?

### 2. Prompt composition template

Design the exact template the orchestrator uses to compose a subagent prompt at dispatch time. The template must:

- Produce prompts functionally equivalent to the current agent definitions
- Use only information from reference files + MANIFEST.md + SKILL.md
- Handle single-reference stages (evaluator: 1 file) and multi-reference stages (gatherer: 3 files)
- Include role framing generated from stage name + description
- Include the entry gate check command
- Include the tools declaration
- Preserve the verifier's context isolation note

Show the template with placeholder variables and one concrete example (the verifier, since it's the most complex case with context isolation + 2 reference files + specific tool restrictions).

### 3. MANIFEST.md evolution

MANIFEST.md currently has: Stage, Files, Purpose columns. It may need to expand to support prompt composition. Design what additional columns or metadata MANIFEST.md needs (if any). Consider:

- Tools per stage
- Entry gate name
- Role description (one-line)
- Primary reference file (for multi-reference stages — which file has the contracts?)
- Whether MANIFEST.md should remain a markdown table or evolve into something more structured

### 4. Information preservation audit

For each of the 9 agents, specify exactly where each piece of unique content migrates:

| Agent | Unique Content | Destination |
|-------|---------------|-------------|
| research-framer | ... | ... |
| ... | ... | ... |

Flag anything that has no clear destination — these are design decisions to make.

### 5. SKILL.md updates

The SKILL.md workflow currently says "Dispatch the named agent (e.g., `research-gatherer`)". With no agent files, describe what changes in SKILL.md:

- How does Step 4 (Execute Research Chain) change for the delegate path?
- Does the orchestrator need new instructions for prompt composition, or is it implicit from reading MANIFEST.md + reference files?
- How does the distill SKILL.md change for worker dispatch?

### 6. Migration steps

Ordered list of changes with rollback strategy. The constraint: at no point during migration should existing functionality break. The composable pipeline (inline execution) must keep working throughout.

### 7. Trade-off analysis

Compare before (static agents + references) vs after (references only + dynamic composition):

- Maintenance burden (how many files to update when methodology changes)
- Prompt fidelity (is the composed prompt as good as the hand-crafted agent?)
- Debugging (how do you inspect what prompt a subagent actually received?)
- Token efficiency (does composing from parts cost more or less than static files?)
- Copilot compatibility (can GitHub Copilot use enriched reference files without Claude Code's dispatch layer?)

## Constraints

- Stdlib-only Python (no external dependencies)
- Must work within Claude Code's agent/subagent dispatch model
- Stage-gate checks (`assess_research.py`) unchanged
- All methodology preserved at full fidelity
- Reference files must remain model-agnostic (no XML tags or model-specific syntax)
- MANIFEST.md must remain human-readable (it's documentation too)
- The inline execution path (orchestrator reads references directly) must not be degraded by changes made to support delegation

## Output Format

Produce a design document with these sections:

1. **Reference file contract** — updated template with all new sections, showing how a single-reference stage and a multi-reference stage differ
2. **MANIFEST.md schema** — updated table structure with any new columns
3. **Prompt composition template** — the exact assembly pattern with a concrete verifier example
4. **Information migration table** — per-agent audit showing where every unique piece goes
5. **SKILL.md changes** — specific updates to research and distill orchestrator workflows
6. **Migration plan** — ordered steps with rollback points
7. **Trade-off analysis** — before vs after comparison on the five dimensions above

Prioritize zero information loss over elegance. If something doesn't have a clean home, call it out explicitly rather than dropping it.
