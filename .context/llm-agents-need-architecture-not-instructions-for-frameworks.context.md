---
name: "LLM Agents Need Architecture, Not Instructions, for Decision Frameworks"
description: "Standard chain-of-thought reasoning is structurally greedy and cannot reliably apply multi-step decision frameworks — Tree of Thoughts, process-reward models, and multi-agent verification provide the architectural mechanisms required."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2601.22311
  - https://arxiv.org/abs/2508.17692
  - https://medium.com/@anicomanesh/how-llm-reasoning-powers-the-agentic-ai-revolution-cbefd10ebf3f
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
related:
  - docs/context/mental-models-software-decisions-practitioner-vs-empirical.context.md
  - docs/context/cot-traces-debugging-vs-stakeholder-trust.context.md
---
## Key Insight

LLM agents can produce framework-shaped outputs via pattern matching. Producing outputs formatted as Richardson's seven steps or an ADR template does not mean the agent reasoned within those frameworks' logic. Standard chain-of-thought is structurally greedy — it creates myopic commitments at each step and cannot perform lookahead. Reliable systematic framework application requires architectural mechanisms (Tree of Thoughts, process-based reward models, multi-agent verification), not prompting alone.

## The Greedy Step-Wise Problem

Wang et al. 2026 (arXiv 2601.22311, T2) establishes formally: "step-wise reasoning induces a form of step-wise greedy policy" that creates "myopic commitments that are systematically amplified over time and difficult to recover from."

In practical terms: when an agent is instructed to apply a seven-step decision framework, standard chain-of-thought generates each step by conditioning on prior tokens — not on evaluation of future steps. Each commitment is greedy relative to prior context. This means by step 4, the agent cannot backtrack to revise a problematic step 2, even if later steps reveal the step 2 decision was wrong.

This is the same structural failure mode that makes CoT unreliable for long-horizon planning tasks. Instructing an agent to apply a framework more carefully does not fix the architectural constraint.

## Framework-Shaped Outputs vs. Framework-Grounded Reasoning

An agent prompted with Richardson's seven-step pattern analysis will produce outputs that superficially follow the seven-step structure. The underlying generation process is still greedy: step 3 is generated conditioned on steps 1–2 without evaluating whether step 3 is consistent with what step 6 would require.

Research on CoT consistency confirms: CoT outputs often reflect pattern retrieval or rationalization rather than genuine stepwise inference. The model recognizes the template and fills it — reasoning quality within the template is not guaranteed.

## Architectural Solutions

**Tree of Thoughts (ToT):** Generates multiple candidate reasoning branches at each node, evaluates them with value functions, and backtracks using BFS/DFS/Monte Carlo Tree Search. Achieves genuine systematic search rather than greedy forward traversal. Architecturally different from CoT — requires implementing the search procedure, not just prompting.

**Process-based Reward Models (PRMs):** Provide feedback on the validity of intermediate reasoning steps during generation, training agents to catch errors mid-chain rather than only rewarding final answers. Requires a trained PRM separate from the base model.

**Multi-agent verification:** Distributes deliberation across specialized agents that critique and verify each other's outputs. Enables collective mode reasoning where no single agent's greedy commitment goes unchallenged.

## What Works with Standard Prompting

Two approaches make framework application more reliable without full architectural changes:

**Structure-as-constraint over instruction-as-constraint:** ADR format as a required output schema is more reliable than telling an agent to "reason systematically." Requiring agents to populate `context`, `rationale`, `alternatives`, and `consequences` as explicit structured fields creates structural pressure on each field — it cannot be skipped. Fowler: "The act of writing helps clarify thinking." Structure that forces each field is more reliable than free-text instruction.

**Step-as-tool-call sequence:** Enforcing each framework step as a required tool call (rather than free-form generation) makes framework adherence verifiable. The orchestrator can confirm each step was populated before proceeding.

**Confidence level:** LOW that standard instruction-based agents apply multi-step frameworks systematically. MODERATE that ToT/PRM architectures can do so. HIGH that structure-as-constraint and step-as-tool-call improve reliability over unstructured instruction.

## Takeaway

Do not expect standard CoT prompting to reliably apply multi-step decision frameworks. Use ADR-style structured output schemas to impose step coverage. For high-stakes systematic reasoning, invest in ToT architecture or multi-agent verification — these are the mechanisms that provide genuine lookahead and error recovery, which prompting alone cannot supply.
