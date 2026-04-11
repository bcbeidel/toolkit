---
name: "Prompt Repetition Technique"
description: "Prompt repetition: 47 wins vs. 0 losses across 70 benchmarks, no latency cost"
type: concept
confidence: medium
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2512.14982
related:
  - docs/context/cot-and-self-consistency-tradeoffs.context.md
  - docs/context/prompt-design-principles-framing-and-emphasis.context.md
---
Repeating the input query improves LLM performance with the strongest signal-to-noise ratio of any tested prompting technique: 47 statistically significant wins across 70 model-benchmark combinations with zero losses and no increase in latency.

## The Finding

Leviathan et al. (Google, 2025) tested a minimal transformation: repeating the input query at the end of the prompt. Transforming `<QUERY>` to `<QUERY><QUERY>` produced consistent improvements across Gemini, GPT-4o, Claude, and DeepSeek models.

Key results:
- 47 statistically significant improvements, 0 losses across 70 model-benchmark combinations
- Gemini 2.0 Flash-Lite on NameIndex: accuracy jumped from 21.33% to 97.33%
- No increase in generated tokens or latency — extra processing is in the parallelizable prefill stage
- Prompt Repetition x3 sometimes substantially outperforms x2 on specific tasks

## Why It Works

The mechanism: each token in the second copy can attend to every token in both copies, improving contextual integration. The model gets two "looks" at the query, which is particularly valuable when the query is embedded in a large context that may dilute its signal.

## Applicability Constraints

Most effective for non-reasoning tasks. Diminishing returns when combined with step-by-step reasoning (CoT). If the model is already performing well on a task, repetition adds less value.

This technique is the complement to CoT: CoT helps tasks requiring deliberate multi-step reasoning, while prompt repetition helps tasks where the model needs to keep the query salient relative to large surrounding context.

## Practical Use

The transformation is trivial to implement: append the query a second time at the end of the prompt, after any context. For context files, this corresponds to restating the core question or objective at the end of the instruction block.

The x3 variant (repeat three times) outperforms x2 on some specific tasks but should be tested rather than assumed to always be better. The gains are not uniform across all tasks.
