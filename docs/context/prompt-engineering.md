---
name: "Prompt Engineering for Skill Authors"
description: "Practical patterns for writing reliable system-level LLM instructions: layered structure, selective specification, few-shot examples, and anti-pattern avoidance"
type: reference
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://developers.openai.com/api/docs/guides/prompt-engineering/
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide/
  - https://arxiv.org/html/2505.13360v1
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
related:
  - docs/research/prompt-engineering.md
  - docs/context/context-window-management.md
  - docs/context/llm-capabilities-limitations.md
---

## Key Insight

Structure and selectivity matter more than clever phrasing. Both major model
providers converge on the same organizational pattern and warn against the same
failure modes. The central tension — underspecification causes regression,
overspecification degrades accuracy — resolves through selective specification
of only critical, unstable requirements.

## Prompt Architecture

Organize system prompts as layered specifications in this order:

1. **Role/identity** — who the model is and what it does
2. **Constraints** — behavioral boundaries and requirements
3. **Examples** — 3-5 diverse demonstrations wrapped in `<example>` tags
4. **Context** — reference material and background information

Use XML tags (`<instructions>`, `<example>`, `<context>`) to delimit sections.
Both Anthropic and OpenAI found XML outperforms JSON as a structural delimiter.

## The Specificity Paradox

Underspecified prompts are 2x more likely to regress during model updates, with
accuracy drops exceeding 20%. But specifying 19+ requirements simultaneously
degrades accuracy by 15-20% as competing constraints interfere.

**Resolution: specify selectively.** Identify requirements that are critical and
unstable — likely to regress across model versions — and specify those explicitly.
Let model defaults handle stable, predictable behaviors. Bayesian optimization
of this approach achieved 3.8% accuracy improvement while reducing prompt tokens
by 41-45%.

Conditional requirements deserve special attention. They appear in only 14.3% of
developer prompts but represent 40% of systematically curated requirements. Models
guess unspecified requirements correctly only 41.1% of the time.

## Steering Techniques

**Few-shot examples** are the most reliable steering mechanism. Use 3-5 examples
that cover edge cases and demonstrate the full expected workflow. Diversity across
examples matters more than quantity — repetitive examples cause the model to pick
up unintended patterns.

**Positive constraints** outperform negative ones. "Write in flowing prose" works
better than "Don't use markdown." Tell the model what to produce, not what to avoid.

**Explain the why.** Providing motivation behind constraints enables the model to
generalize beyond the literal rule. A model that understands *why* ellipses are
prohibited (text-to-speech output) will also avoid other TTS-unfriendly constructs.

**General reasoning directives** often beat prescriptive step lists. "Think
thoroughly" produces better reasoning than a hand-written step-by-step plan.
Reserve explicit chain-of-thought scaffolding for tasks where models consistently
fail without it.

## Anti-Patterns

| Anti-Pattern | Risk | Fix |
|---|---|---|
| Task overloading | Hallucination, missed tasks | Decompose into focused prompts |
| Unconditional tool mandates | Hallucinated inputs | Add conditions: "if you don't have enough information, ask" |
| ALL-CAPS escalation | Diminishing returns, overtriggering | Start without emphasis, add only when empirically necessary |
| Implicit assumptions | 41% guess rate on unspecified requirements | Make requirements explicit, especially conditional ones |
| Stale calibration | Newer models overtrigger on aggressive language | Re-evaluate prompts on every model upgrade |

## Calibration Warning

Newer models follow instructions more literally. Prompts tuned for older models —
especially those using aggressive emphasis to compensate for weaker instruction
following — will overtrigger on current models. Re-evaluate prompts on every model
upgrade. Hidden model updates caused a 48% reduction in producing expected output
formats in one study.
