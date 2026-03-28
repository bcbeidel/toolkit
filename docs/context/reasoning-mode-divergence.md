---
name: "Reasoning Mode Divergence"
description: "How chain-of-thought and reasoning capabilities differ across LLM families — each has incompatible built-in reasoning mechanisms while explicit CoT prompting remains the only portable technique"
metadata:
  type: reference
  sources:
    - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
    - https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
    - https://ai.google.dev/gemini-api/docs/prompting-strategies
    - https://simonwillison.net/2025/Feb/2/openai-reasoning-models-advice-on-prompting/
    - https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide
  related:
    - docs/research/cross-model-prompt-portability.md
    - docs/context/cross-model-prompt-portability.md
    - docs/context/prompt-engineering.md
    - docs/context/llm-capabilities-limitations.md
---

## Key Insight

Every major model family has built a different reasoning mechanism with
incompatible API parameters. Explicit chain-of-thought prompting is the only
reasoning technique that works across all models. Built-in reasoning modes
are more capable but lock you into a specific family.

## Four Incompatible Approaches

**Claude (Anthropic):** Uses adaptive thinking where the model dynamically
decides when and how much to reason. Extended thinking outputs `<thinking>`
tags. General directives ("think thoroughly") produce better results than
prescriptive step-by-step plans. Claude is sensitive to the word "think"
when extended thinking is disabled.

**GPT (OpenAI):** Reasoning models (o1, o3, o4-mini) generate chain-of-thought
internally. GPT-5 supports a `reasoning_effort` parameter (minimal/medium/high).
Few-shot examples are less necessary — OpenAI recommends trying prompts without
examples first. Contradictory instructions are especially damaging because the
model spends reasoning tokens trying to reconcile them.

**Gemini (Google):** Gemini 2.5 Pro introduced "Deep Think" for internal
chain-of-thought. Gemini 3 reasons internally before answering by default.
Google recommends direct prompts: the model "favors directness over persuasion
and logic over verbosity."

**Llama (Meta):** No built-in reasoning mode. Chain-of-thought must be explicitly
prompted. Performance is highly sensitive to prompt template and formatting.

## The Portability Problem

These mechanisms differ in three dimensions:

1. **Activation:** Adaptive (Claude), parameter-controlled (GPT), default-on (Gemini 3), manual (Llama)
2. **Visibility:** Some expose reasoning traces (`<thinking>` tags), others reason opaquely
3. **Control:** Different API parameters (`reasoning_effort`, thinking budget) with no cross-model equivalent

There is no abstraction layer that maps between these. Code that configures
reasoning for one model must be rewritten for another.

## Explicit CoT as the Portable Fallback

Traditional chain-of-thought prompting — asking the model to "think step by
step" or "show your reasoning" — works on every model. But it is less effective
than built-in reasoning modes on models that have them. The tradeoff:

- **Built-in reasoning:** Higher ceiling, model-specific API, no portability
- **Explicit CoT prompting:** Lower ceiling, works everywhere, portable

For multi-model deployments, use explicit CoT as the baseline. Layer
model-specific reasoning parameters in API integration code when targeting a
single family.

## Implications for Prompt Design

The rise of built-in reasoning modes changes two established prompt engineering
practices:

**Few-shot examples become less critical.** Reasoning models already decompose
problems internally. OpenAI's guidance is explicit: try without examples first.
This contradicts the traditional "always include few-shot examples" advice,
which remains valid for models without built-in reasoning (Llama, older GPT).

**Step-by-step scaffolding can hurt.** Prescriptive reasoning plans constrain
models that reason better on their own. Claude performs better with general
directives than hand-written step lists. Reserve explicit scaffolding for tasks
where models consistently fail without it.
