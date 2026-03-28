---
name: "Context Window Management"
description: "Strategies for maximizing LLM performance within token limits: position-aware formatting, compression, structured markup, and budget allocation"
metadata:
  type: reference
  sources:
    - https://arxiv.org/abs/2307.03172
    - https://arxiv.org/abs/2310.06839
    - https://arxiv.org/abs/2404.02060
    - https://arxiv.org/abs/2309.17453
    - https://arxiv.org/abs/2404.06654
    - https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
    - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/long-context-tips
  related:
    - docs/research/context-window-management.md
    - docs/research/prompt-engineering.md
    - docs/context/writing-for-llm-consumption.md
    - docs/context/prompt-engineering.md
    - docs/context/llm-capabilities-limitations.md
    - docs/context/agent-state-persistence.md
    - docs/context/context-engineering.md
---

Context window management determines what enters an LLM's working memory and how it is structured. Performance degrades predictably as context grows — not from capacity limits alone but from attention distribution patterns that favor boundary positions. Three coordinated strategies address this: strategic positioning, compression, and structured formatting.

## The Attention Curve

LLMs exhibit a U-shaped attention pattern: information at the beginning and end of context receives stronger attention than information in the middle. This "lost in the middle" effect produces measurable performance degradation on retrieval and QA tasks across model architectures (Liu et al., 2023). The root cause appears to be training data distribution rather than architectural limitation — targeted training approaches like FILM-7B largely eliminate the bias.

Newer models show improvement. Claude achieves state-of-the-art results on long-context retrieval benchmarks, but the effect persists to varying degrees. For practical purposes, assume effective context is 50-70% of the stated maximum for complex tasks. RULER benchmarks found only half of models claiming 32K+ tokens maintain satisfactory performance at that length (Hsieh et al., 2024).

## Position Strategy

Exploit the U-shaped curve deliberately:

- **Beginning (system prompt):** Critical instructions, constraints, role definitions, structural metadata that establishes the parsing framework.
- **Middle (acceptable degradation zone):** Reference material, supporting data, retrieved documents. This is where compression pays the highest dividend.
- **End (user turn):** The query, specific task instructions, and examples. Placing queries at the end improves response quality by up to 30% on complex multi-document inputs (Anthropic docs).

## Compression

Three compression paradigms have demonstrated effectiveness:

1. **Token-level pruning** removes predictable tokens based on self-information metrics. Fast and structure-preserving.
2. **Extractive compression** selects the most relevant sentences. RECOMP achieves 6% compression rate with minimal performance loss on specific benchmarks.
3. **Proposition-level retrieval** decomposes documents into atomic factual statements. Highest information density per token but requires preprocessing.

LongLLMLingua achieves 2-6x compression with up to 21.4% performance improvement on some benchmarks because it simultaneously reduces tokens and mitigates position bias (Jiang et al., 2023). Compress the middle zone most aggressively — that is where attention is weakest and compression cost-benefit is highest.

## Structured Formatting

XML tags create parseable landmarks that help models navigate large contexts. Anthropic recommends `<document>`, `<source>`, and `<document_content>` tags for multi-document inputs. Quote grounding — asking models to extract relevant quotes before answering — forces explicit attention to source material and reduces hallucination risk.

## Budget Allocation

No single empirically validated distribution exists, but practical guidance converges:

- **System instructions:** 5-15% of budget
- **Retrieved context:** 40-60% of budget
- **Examples:** 10-20% of budget
- **User input + query:** 10-20% of budget
- **Output reserve:** 10-25% of budget (newer models error on overflow, not truncate)

Track remaining budget using context awareness features. In long-running conversations, use server-side compaction, strip previous thinking blocks, and clear old tool results. Design state artifacts for fast context recovery when starting new sessions.
