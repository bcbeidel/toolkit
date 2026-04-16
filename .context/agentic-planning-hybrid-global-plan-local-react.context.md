---
name: Agentic Planning — Hybrid Global-Plan / Local ReAct
description: "Production systems converge on a \"plan globally, act locally\" hybrid combining structured upfront plans with ReAct-style adaptive execution; dynamic replanning after each executor step is the architectural direction of current research."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://arxiv.org/abs/2305.18323
  - https://arxiv.org/html/2503.09572v3
  - https://blog.langchain.com/planning-agents/
  - https://byaiteam.com/blog/2025/12/09/ai-agent-planning-react-vs-plan-and-execute-for-reliability/
  - https://arxiv.org/abs/2402.11534
related:
  - docs/context/agentic-failure-recovery-classify-retry-replan-abandon.context.md
  - docs/context/multi-agent-orchestration-patterns-and-selection-criteria.context.md
  - docs/context/agentic-resilience-infrastructure-primitives.context.md
  - docs/context/agent-memory-tier-taxonomy-and-implementation-gaps.context.md
---
# Agentic Planning — Hybrid Global-Plan / Local ReAct

**Production systems converge on "plan globally, act locally"**: structure major stages upfront, use ReAct-style adaptive execution within each stage. This combines planning's strategic coherence with ReAct's tactical flexibility.

## The Core Planning Patterns

**ReAct (Reasoning + Acting)** is the most widely deployed production pattern (confirmed by Anthropic, LangGraph, Claude tool-use, AutoGen). The Thought → Action → Observation loop grounds reasoning in real retrieved evidence, reducing hallucination versus standalone chain-of-thought. Weaknesses: myopic step-by-step optimization, error cascade when a misleading observation propagates, full-context overhead at every step.

**Plan-and-Execute** separates a comprehensive planning phase from a distinct execution phase. A stronger model plans; cheaper specialized models execute. Wins when: multi-step workflows have known structure, human review is required before execution begins, cost optimization matters, or auditability is required. Validated by T2 ICML 2025 research (Plan-and-Act: 57.58% success vs. 49.1% prior SOTA on WebArena-Lite).

**ReWOO** (Reasoning Without Observations) decouples the full plan from tool execution via variable placeholders — the Planner emits the entire dependency-annotated plan upfront, the Worker fills in evidence, the Solver synthesizes. Token savings: 5× on HotpotQA, 64% average reduction across 6 benchmarks, +4.4% accuracy (T3 arXiv). Brittle: if any tool call returns unexpected output, the pre-committed plan has no adaptation hook.

**Tree-of-Thought / Graph-of-Thought** explore branching paths with scoring and pruning. Best for combinatorial problems and creative tasks. Multiple forward passes per node make them computationally prohibitive for latency-sensitive production agents.

## The Hybrid Consensus

Anthropic explicitly states: "the phases in agentic AI workflows do not always occur in a strict step-by-step linear fashion — they are frequently interleaved or iterative, depending on task nature and environment complexity."

The practitioner recommendation for production long-horizon tasks: use a high-level Planner that structures major stages, and a ReAct-style Executor that handles fine-grained adaptive execution within each stage. Plan-and-Act (ICML 2025) implements this with dynamic replanning — the Planner updates the plan after each Executor step, preserving long-range structure while allowing tactical adaptation.

## Task Decomposition

Three phases: (1) Task Analysis — classify intent, match to available tools; (2) Task Decomposition — generate ordered or parallel subtasks with explicit dependency links; (3) Plan Control — progress tracking, variable management, next-action selection, termination.

Explicit dependency encoding is required for correctness. ReWOO formalizes this with `#E1`/`#E2` variable placeholders. LangGraph implements it as conditional edges in a directed acyclic graph. Subtasks with no data dependency can run in parallel; dependent subtasks must be sequenced.

**Dynamic decomposition** (decompose only on failure, not upfront) avoids overhead on simple cases. Relevant when task complexity is uncertain at start.

## Pattern Selection Summary

| Pattern | When to Use |
|---------|-------------|
| ReAct | High uncertainty, interactive tasks, short horizon, real-time latency |
| Plan-and-Execute | Known structure, human review required, cost optimization, auditability |
| ReWOO | Predictable multi-hop with stable tool responses; token budget constrained |
| Hybrid | Long-horizon production tasks with both known structure and uncertain local execution |

## Takeaway

ReAct is the safe default. Add upfront planning when task structure is predictable and strategic coherence matters more than per-step adaptability. Use dynamic replanning to avoid brittle pre-committed plans. Checkpointing at subtask boundaries is architecturally required for efficient replanning — without it, failures force full restarts.
