---
name: "Structured Thinking and Decision Frameworks"
description: "How to convert classical mental models into executable agent procedures — trigger conditions, structured steps, verification criteria, and the reasoning substrate that makes them work"
type: reference
sources:
  - https://arxiv.org/abs/2201.11903
  - https://arxiv.org/abs/2305.10601
  - https://arxiv.org/abs/2210.03629
  - https://arxiv.org/html/2602.16512
  - https://fs.blog/mental-models/
related:
  - docs/research/structured-thinking-decision-frameworks.md
  - docs/context/agentic-planning-execution.md
  - docs/context/prompt-engineering.md
  - docs/context/tool-design-for-llms.md
---

# Structured Thinking and Decision Frameworks

Mental models are not useful to agents as reference material. They become operational only when converted from descriptive frameworks into executable procedures with defined inputs, outputs, trigger conditions, and verification criteria. The gap between knowing a framework and applying it mirrors the gap between naive chain-of-thought prompting and structured agentic reasoning.

## The Operationalization Gap

Three properties distinguish an executable framework from inert description:

**Trigger conditions** — the agent knows *when* to apply the framework. First principles triggers when assumptions are unexamined. Inversion triggers before committing to a plan. Eisenhower triggers when task volume exceeds capacity. Without triggers, models sit unused in context.

**Structured procedure** — the framework specifies discrete steps with inputs and outputs. "Consider second-order effects" is a vague instruction. "For each proposed action, list 3 immediate consequences, then for each list 2 further consequences, then rate each as beneficial/neutral/harmful" is an executable procedure.

**Verification criteria** — the agent can check whether it applied the framework correctly. Did the inversion pass enumerate failure modes? Did the Pareto analysis produce a ranked list with a cutoff? Without verification, the agent cannot self-correct.

## Five Classical Models as Agent Operations

Each follows the same meta-pattern: decompose, evaluate, select, verify.

**First principles** — recursive decomposition with assumption auditing. Input: problem + assumptions. Process: list assumptions, challenge each, identify irreducible facts, rebuild from facts only. Verification: each base fact independently confirmable.

**Inversion (pre-mortem)** — failure-mode enumeration before plan execution. Assume the plan failed, enumerate causes ranked by likelihood and impact, check whether mitigations exist. Unaddressed high-risk failure modes flag the plan for revision.

**Eisenhower matrix** — urgency/importance classification. Score tasks on both dimensions, classify into quadrants, apply routing rules. Key constraint: Quadrant 2 (important, not urgent) tasks must not be displaced by Quadrant 3 (urgent, not important) without explicit override.

**Pareto (80/20)** — impact-weighted ranking with diminishing returns detection. Compute impact/effort ratio, sort descending, find the knee where cumulative impact crosses ~80%. Focus on above-knee items.

**Second-order effects** — consequence chain tracing to configurable depth. Trace immediate consequences, then consequences of consequences (typically 2-3 levels). Any undesirable second-order effect with high probability triggers plan revision.

## Structured Reasoning as Execution Substrate

The LLM reasoning literature provides the architectural patterns for executing these frameworks:

**Chain-of-Thought** makes reasoning explicit through intermediate steps — the baseline requirement for any operationalized model. **Tree-of-Thought** adds branching exploration with self-evaluation at each node, producing dramatic gains (GPT-4 went from 4% to 74% on Game of 24). Inversion and second-order effects are inherently tree-structured. **ReAct** interleaves reasoning with tool calls and observations, grounding frameworks in external data rather than hallucinated assumptions. **Framework of Thoughts (FoT)** models reasoning as dynamic execution graphs with explicit input/output contracts between nodes, enabling composition and parallelization (10.7x speedup, 64-91% cost reduction).

These are not alternative techniques but a progressive stack: CoT makes reasoning explicit, ToT adds exploration, ReAct adds grounding, FoT adds composition.

## Practical Integration Patterns

**Framework as tool** — define each model as a callable tool with a schema (inputs, outputs, verification). Makes frameworks composable and auditable in reasoning traces.

**Framework as gate** — use frameworks as decision checkpoints. A plan must pass an inversion gate and a second-order effects gate before execution.

**Composed pipeline** — chain frameworks in sequence: first principles (decompose) then Pareto (rank) then inversion (risk-check) then Eisenhower (prioritize) then second-order effects (validate). Each stage's output feeds the next, with verification at each step.

The universal pattern across all operationalized frameworks: make reasoning structure explicit and evaluable. Vague instructions to "think carefully" underperform structured procedures with defined steps, intermediate outputs, and self-evaluation checkpoints.
