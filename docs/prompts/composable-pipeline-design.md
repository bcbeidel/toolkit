---
name: Composable Pipeline Design
description: Prompt for designing a composable research pipeline where stages can run inline or as subagents, with gate preservation and cross-platform reference placement
---

You are a software architect specializing in LLM agent orchestration and prompt composition.

## Context

We are building a research pipeline in a Claude Code plugin (wos). The current design uses 9 dedicated subagents across two pipelines:

**Research pipeline** (7 agents, sequential with gate checks):
framer → gatherer → evaluator → challenger → synthesizer → verifier → finalizer

**Distill pipeline** (2 agents):
mapper → worker

Each agent definition (`agents/*.md`) contains substantial inlined methodology — not just dispatch logic, but detailed instructions for SIFT source evaluation, Chain of Verification, Analysis of Competing Hypotheses, confidence calibration, search budgets by rigor level, and more. These instructions were derived from shared reference files in `skills/_shared/references/research/` and `skills/_shared/references/distill/`, but the agent bodies contain the full inlined version.

The current architecture enforces "one obvious way to run" — each stage always runs as a subagent. This creates overhead: each subagent invocation costs context window tokens for the handoff, adds latency for agent startup, and prevents the orchestrator from using information gathered in one stage to inform the next without passing it through structured outputs.

**Stage-gate checks** are deterministic Python validation (`wos/research/assess_research.py`) that run between agents:
- `gatherer_exit` — DRAFT file exists, sources table has URL column, extracts present for all sub-questions
- `evaluator_exit` — sources table has Tier and Status columns
- `challenger_exit` — Challenge section exists
- `synthesizer_exit` — Findings section exists
- `verifier_exit` — Claims table exists with rows, no unverified cells
- `finalizer_exit` — DRAFT marker removed, type: research and non-empty sources in frontmatter

These gates are structural checks (section exists, column present, cell values) with no LLM judgment. They must be preserved exactly as-is in any redesign.

## Task

Design a composable research pipeline where:

1. The research orchestrator decides at runtime whether to run a stage inline (in its own thread) or delegate to a subagent
2. All existing methodology detail (SIFT, CoVe, ACH, search budgets, confidence calibration, etc.) is preserved — no lossy compression of instructions
3. Stage-gate checks continue to run between every stage transition, regardless of whether the stage ran inline or as a subagent
4. Reference files serve dual purpose: direct instructions when run inline, or subagent prompts when delegated

Address these specific concerns:

- **Performance trade-offs:** When should the orchestrator run inline vs. delegate? What heuristics should guide this decision? (Consider: token budget remaining, task complexity, context dependency between stages, the verifier's deliberate context isolation)
- **Reference file placement:** The current references live in `skills/_shared/references/`. Should they stay there (Claude Code convention), move to a platform-agnostic shared directory (e.g., `docs/` or a top-level `references/`), or somewhere else? Optimize for cross-platform capability — both Claude Code and GitHub Copilot must be able to discover and load them. Make a concrete recommendation with rationale.
- **Instruction fidelity:** Each agent currently inlines 50-200 lines of methodology. How does the composable design ensure no detail is lost when the orchestrator runs a stage inline vs. when a subagent loads the same reference? Account for the fact that some agents combine multiple reference files (e.g., gatherer uses gather-and-extract.md + verify-sources.md + cli-commands.md).
- **Evaluation strategy:** Design an approach where each reference file can be evaluated in isolation as a standalone prompt, independent of the orchestration layer
- **Migration path:** How do we move from the current always-subagent design (9 agent definitions in `agents/`) to composable without breaking existing functionality or losing methodology detail?

## Constraints

- Stdlib-only Python (no external dependencies)
- Must work within Claude Code's agent/subagent model AND GitHub Copilot's agent mode
- Stage-gate checks (`wos/research/assess_research.py`) must remain deterministic Python — no changes to gate logic
- All existing methodology must be preserved at full fidelity — no summarization or simplification of instructions
- Minimize total token usage across the pipeline
- Design must be model-agnostic — no XML tags or model-specific prompt syntax in reference files
- Shared state between stages is the DRAFT research document on disk (not in-memory)

## Output Format

Produce a design document with these sections:

1. **Architecture overview** — text-based diagram of the composable pipeline showing inline/delegate decision points and where gate checks execute
2. **Decision heuristics** — concrete rules for when to inline vs. delegate, with specific attention to the verifier (which benefits from context isolation)
3. **Reference file placement** — recommended location, directory structure, and rationale for cross-platform discovery
4. **Reference file contract** — template/structure that reference files must follow for dual-use across both Claude Code and Copilot, including how multi-reference stages (gatherer, verifier, finalizer) compose their instructions
5. **Evaluation framework** — how to test each reference file in isolation, what metrics to measure, how gate checks integrate with evaluation
6. **Trade-off analysis** — explicit comparison of current (always-subagent) vs. proposed (composable) on token cost, latency, context quality, and instruction fidelity
7. **Migration steps** — ordered list of changes from current to proposed, with rollback strategy

Prioritize practical, implementable design over theoretical elegance. The primary goal is reducing token overhead and latency while preserving gate checks, instruction fidelity, and evaluation capability.
