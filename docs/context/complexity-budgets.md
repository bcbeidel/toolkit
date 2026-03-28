---
name: "Complexity Budgets for Agent Systems"
description: "Treating total system complexity as a finite, measurable resource — tool-count cliffs, context-complexity degradation, token budgeting per tool, and periodic pruning as a first-class engineering activity"
metadata:
  type: reference
  sources:
    - https://arxiv.org/html/2511.22729v1
    - https://arxiv.org/html/2601.06112v1
    - https://www.anthropic.com/research/building-effective-agents
    - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  related:
    - docs/research/scope-management-yagni.md
    - docs/context/yagni-agent-tooling.md
    - docs/context/tool-vs-framework-spectrum.md
    - docs/context/context-window-management.md
    - docs/context/tool-design-for-llms.md
---

A complexity budget is the total cognitive and computational overhead a system can bear before incremental additions degrade overall performance. In agent tooling, this budget is not abstract — it is measurable in tokens, tool counts, and conversation turns.

## Context Complexity, Not Context Length

The binding constraint on agent performance is context complexity, not context length. When researchers gave a quantized Llama 3.1 8B model access to 46 tools from the GeoEngine benchmark, it failed completely — even though the context was within its 16K window. With 19 tools, it succeeded. The failure was not a token-length problem but a tool-selection problem: too many descriptions overwhelmed the model's ability to reason about the right tool.

This distinction matters for design decisions. Adding a tool that fits within the token budget can still degrade performance if it pushes past the model's effective reasoning capacity for tool selection.

## The Degradation Curve

ReliabilityBench tested agents under production-like conditions and found consistent degradation patterns. Beyond 12 conversation turns, agents increasingly invoke redundant operations: re-reading unchanged files, repeating failed tool calls with minimal adjustments, generating verbose summaries that consume tokens without adding information. A 50% increase in conversation length yields 3-5% efficiency losses, with compounding effects as context accumulates.

Simpler ReAct agents outperformed more complex Reflexion architectures under stress conditions. Nearly all models suffered an average accuracy drop of 20.8% under realistic conditions (ambiguous instructions, noisy tool outputs, context overflow). The systems with lower inherent complexity degraded more gracefully.

## Practical Budgeting Principles

**Token cost per tool.** Every tool description has an amortized cost across all invocations. A tool description that adds 200 tokens is not a one-time cost — it is a per-invocation tax. If the tool is relevant to 5% of sessions, 95% of sessions pay 200 tokens for zero benefit. Across 10 such tools, that is 2000 tokens of reasoning capacity consumed for marginal utility.

**Feature justification threshold.** Every feature must demonstrate that its value exceeds its context cost. A rarely-used parameter adding 50 tokens to a tool description must justify those 50 tokens against the reasoning degradation they cause in every invocation where the parameter is irrelevant.

**Periodic pruning.** Just as teams allocate sprint capacity for technical debt, agent tooling projects should periodically audit tool sets and remove unused or low-value tools. Feature removal is a feature. This is not cleanup — it is a first-class engineering activity that directly improves system performance.

**Minimum viable tool set.** The optimal strategy is enough tools to cover required capabilities, no more. The empirical evidence consistently shows that more tools beyond the necessary set makes agents worse, not better. The goal is coverage with minimum surface area.

## Budget Allocation in Practice

Treat the project's total complexity as a finite resource shared by all features. When considering a new tool or parameter, the question is not just "is this useful?" but "is this more useful than the reasoning capacity it displaces?" Every addition draws from the same budget as every existing feature. The budget metaphor makes the tradeoff concrete: adding one thing means every other thing gets slightly less effective.
