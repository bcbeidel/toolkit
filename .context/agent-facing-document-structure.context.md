---
name: "Agent-Facing Document Structure"
description: "Documents for LLM consumption: key insights at start and end, answer-first structure, explicit paths/commands over prose"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/html/2406.15981
  - https://daplab.cs.columbia.edu/general/2026/03/31/your-ai-agent-doesnt-care-about-your-readme.html
  - https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
related:
  - docs/context/context-rot-and-window-degradation.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
---
The structural rules for agent-facing documents differ fundamentally from human-facing documentation. The core principle: place key insights at the beginning and end; treat the middle as a dead zone for anything critical.

## Answer-First Structure

State the answer in the first 1-2 sentences of each section before any exposition. AI tools pull the first sentence as the core summary — if it is vague or buried, content will not be selected or used correctly. The same principle applies to context files: bottom-line-up-front makes content retrievable under the U-shaped attention curve.

Serial position effects are consistent across model families (Wu et al., ACL Findings 2025). The recency effect reinforces the primacy effect: beginning and end receive the highest attention regardless of relevance. This is caused by Rotary Position Embedding (RoPE), used in most modern transformers.

## Explicit Over Descriptive

Agent documentation is fundamentally different from human documentation. Agents need "insight into where things live, what rules to follow, and how to implement changes" — not narratives. Traditional README files fail agents because they contain "fluff" irrelevant to programmatic task execution (Columbia DAPLab, 2026).

Prefer:
- Explicit file paths over descriptions of where things might be
- Concrete commands with specific flags over tool names
- One real code snippet over three paragraphs describing conventions
- Three-tier boundaries (Always do / Ask first / Never do) over aspirational guidance
- Single-concept sections over multi-topic narratives

## Structural Markers Help

Use headings that mirror real queries rather than vague labels. Descriptive headings act as semantic markers — "How to run tests" beats "Testing." Use XML tags or Markdown headers to create section boundaries that help models parse structure.

Anthropic's ordering recommendation: put longform data at the top of prompts, above queries and instructions. Questions at the end. For multi-document input, use `<document>` wrappers with `<source>` and `<document_content>` subtags.

## Manus Agent Practice

Manus agents maintain a `todo.md` file updated step-by-step, keeping current objectives at the tail of context — exploiting the recency effect. This is an architectural application of the primacy/recency principle: stable background goes first, current objectives go last.

## What to Avoid

- Narrative overviews that humans can infer but provide no programmatic value
- Instructions buried in the middle of long documents
- Aspirational or motivational framing — constraints and boundaries over goals
- Deep nesting — flat structure is more reliably parsed
- Redundant context that dilutes signal-to-noise ratio
