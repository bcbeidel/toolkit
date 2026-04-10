---
name: "BLUF and Progressive Disclosure as Document Architecture"
description: "BLUF governs ordering within a document; progressive disclosure governs depth across tiers — complementary patterns that solve different problems"
type: context
sources:
  - https://arxiv.org/abs/2307.03172
  - https://semanticinfrastructurelab.org/essays/progressive-disclosure-for-ai-agents
  - https://www.honra.io/articles/progressive-disclosure-for-ai-agents
  - https://alexop.dev/posts/stop-bloating-your-claude-md-progressive-disclosure-ai-coding-tools/
  - https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
  - https://www.animalz.co/blog/bottom-line-up-front
  - https://mintcopy.com/content-marketing-blog/content-strategy-for-ai-attention-put-the-bluf-first/
related:
  - docs/context/agent-facing-document-structure.context.md
  - docs/context/context-rot-and-window-degradation.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/atomic-file-granularity-and-frontmatter-navigation.context.md
---

BLUF (Bottom Line Up Front) and progressive disclosure are complementary patterns that operate at different levels of document architecture. Conflating them leads to misapplication of both.

**BLUF governs ordering within a single document.** Place the conclusion, decision, or key finding in the first 1-2 sentences. Supporting evidence, examples, and alternatives follow. This applies at the document level (BLUF opening + takeaway closing) and at the section level.

**Progressive disclosure governs depth-of-detail across tiers.** Not how to order content within a file, but how much to reveal at each level of a hierarchy. The two patterns compose: apply BLUF ordering inside each tier, and progressive disclosure between tiers.

## Why BLUF Works for Agents

LLMs exhibit a U-shaped performance curve for long-context retrieval (Liu et al., TACL 2024). Performance peaks when relevant information appears at the beginning or end of input; critical information in the middle of the context window degrades retrieval reliability. BLUF is not just a human-readability convention — it directly aligns with this empirical attention pattern.

LLMs are trained heavily on journalism and technical documentation that follows BLUF structure. Models learn to weight content at the top. Agents that truncate or summarize long documents retain the conclusion even if middle content is lost. The BLUF pattern makes documents robust to truncation.

Caveat: the >30% accuracy drop from Liu et al. was measured on 2022-2023 era models. Modern frontier models with long-context training show reduced degradation. The design principle holds; the magnitude of penalty is smaller for current models. BLUF remains sound practice regardless of the specific magnitude.

## Progressive Disclosure Architecture

The three-layer pattern (T3 practitioner convergence, no controlled benchmarks):

1. **Index tier** — lightweight metadata for routing (~50 tokens per entry). File name, description, and type. No content. An agent reads the index to determine which files are relevant.
2. **Detail tier** — full content loaded when relevance is determined. Atomic files in the 200-800 word range. BLUF-ordered internally.
3. **Deep-dive tier** — supporting reference accessed on demand. Linked via `related:` or external sources.

Limit to 2-3 levels. More levels increase fragmentation risk: agents that receive only an index and fail to fetch the detail layer will have routing decisions based on metadata alone, which degrades to description quality as the single source of truth.

Investment in description quality directly controls routing accuracy. The index tier is the highest-leverage part of the architecture — it is what agents read before deciding what to read next.

## Practical Application

Keep the main instruction file minimal. Delegate enforcement to tooling, not prose. Include a trigger instruction: "Before starting any task, identify which docs are relevant and read them first" — agents do not automatically fetch supporting documentation without an explicit trigger.

Architecture decisions:
- Universal context in the main instruction file (AGENTS.md/CLAUDE.md)
- Domain-specific documentation on demand in `/docs`
- Specialized agents with focused context windows for complex sub-tasks

The index file is a BLUF of the entire corpus. Each document is a BLUF of its topic. The pattern is fractal: apply BLUF at every level, and use progressive disclosure to control how many levels exist.

## What BLUF Does Not Apply To

BLUF should be avoided when delivering sensitive or bad news (context-first softens impact), when foundational explanation is required before conclusions make sense, or in narrative contexts where tension matters. These are human communication exceptions; they rarely apply to agent-facing technical context files, where BLUF is almost always the right default.
