---
name: "Prompt Design Principles: Framing and Emphasis"
description: "Affirmative framing, context/motivation for rules, avoid ALL-CAPS on Claude 4.6 — most transferable prompt design principles"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://arxiv.org/html/2312.16171v1
  - https://gail.wharton.upenn.edu/research-and-insights/tech-report-prompt-engineering-is-complicated-and-contingent/
  - https://openai.com/index/the-instruction-hierarchy/
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
related:
  - docs/context/portable-vs-model-specific-prompt-constructs.context.md
  - docs/context/instruction-capacity-and-context-file-length.context.md
  - docs/context/format-sensitivity-and-cross-model-defaults.context.md
---
A small set of prompt design principles shows reliable, transferable effects across model families. These are distinct from model-specific optimizations — they apply broadly enough to be worth applying as defaults.

## Affirmative Framing Outperforms Prohibitions

State what the model should do rather than what it should not do. "Do not use markdown in your response" is less effective than "Your response should be composed of smoothly flowing prose paragraphs." The positive directive specifies the target behavior; the negative constraint leaves the behavior undefined.

This transfers across Claude, GPT, and Gemini vendor guidance. When prohibitions are being ignored, rephrasing as "Prefer X over Y" improves compliance — particularly in long-context sessions where negative constraints attenuate faster than affirmative ones.

Exception: negative constraints remain appropriate for hard safety boundaries where the behavior must never occur and there is no desirable positive alternative to specify.

## Context and Motivation for Instructions

Explaining why an instruction exists helps models generalize to edge cases. Rather than "NEVER use ellipses," say "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the TTS engine will not know how to pronounce them."

The motivation enables the model to handle novel situations consistent with the rule's intent, rather than pattern-matching on the rule's surface form. Anthropic confirms this as a reliability improvement; it is consistent with what the RLHF training process rewards — helpful behavior toward an understood goal.

## Avoid ALL-CAPS on Claude 4.6

Claude 4.6 is substantially more responsive to system prompts than prior versions. Aggressive emphasis language causes overtriggering — tools that undertriggered before now trigger on inappropriate inputs.

Replace: "CRITICAL: You MUST use this tool when..."
With: "Use this tool when..."

The information content is the same; the aggressive framing adds noise. This is a Claude 4.6-specific calibration — earlier Claude models and other model families may respond differently to emphasis markers.

## Instruction Hierarchy

Training LLMs to treat system prompts as higher priority than user prompts drastically improves resistance to prompt injection — even for attack types not seen during training (Wallace et al., OpenAI, 2024). This is a structural design principle: privileged instructions from the system layer should always dominate user-layer input when conflicts arise. The instruction hierarchy is not a prompting technique but an architectural constraint.

GPT-4.1 explicitly prioritizes instructions near the end of the prompt when conflicts arise — the opposite of most models. This is model-specific and should be tested rather than assumed.

## The Colleague Test

Show the prompt to a colleague with minimal context on the task and ask them to follow it. If they would be confused, the model will be too. This heuristic resolves the majority of real-world prompt issues before any advanced technique is needed.

## What Does Not Transfer

Several techniques have weak or conditional evidence:

**Role assignment**: "Playing Pretend" (Wharton GAIL, 2025) found expert personas provide no consistent benefit for factual accuracy across 6 LLMs. 80% of sociodemographic personas caused statistically significant performance drops. Role assignment may help with tone and style but should not be relied upon for accuracy gains.

**Universal principles**: The Wharton "complicated and contingent" finding applies broadly — prompt engineering effects depend on model, task, and question. The same technique can help or harm depending on these factors. No principle is universally effective; test per-deployment.

**Fixed quantitative claims**: "30% improvement from query placement" and "57.7% quality boost from 26 principles" are vendor claims or self-referential benchmarks without independent replication. Use them as directional guidance, not targets.
