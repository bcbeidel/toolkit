---
name: "Portable vs. Model-Specific Prompt Constructs"
description: "Portable constructs: clear objectives, few-shot examples, numbered steps; model-specific tuning stays separate"
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2512.01420
  - https://www.prompthub.us/blog/one-size-does-not-fit-all-an-analaysis-of-model-specific-prompting-strategies
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
  - https://www.philschmid.de/gemini-3-prompt-practices
  - https://arxiv.org/html/2411.10541v1
related:
  - docs/context/format-sensitivity-and-cross-model-defaults.context.md
  - docs/context/cot-and-self-consistency-tradeoffs.context.md
  - docs/context/prompt-design-principles-framing-and-emphasis.context.md
---
Cross-model prompt transfer incurs a 10-30 percentage point performance drop between model families. PromptBridge (2025) found that transferring GPT-5's optimal prompt to Llama-3.1-70B yielded 68.7% versus the target model's own optimal of 79.5%. PromptHub confirmed "there wasn't a single prompt snippet that could be used across all models to increase performance." Portability is a spectrum, not a threshold.

## What Is Portable

These constructs work across Claude, GPT, Gemini, and Llama without significant modification:

- **Role definitions and persona assignment** — all major models respond well to system-level role setting
- **Clear objective statements** — direct, concise goal description is universally effective; every vendor guide converges on stating goals plainly
- **Few-shot examples** — example-based learning transfers across all model families (though format consistency matters more for some models)
- **Output format specification** — telling the model what format you want (JSON, table, prose) works universally
- **Numbered step instructions** — sequential step lists for ordered tasks work across models

These give approximately 80% of achievable performance. The remaining 20% requires model-specific tuning.

## What Is Model-Specific

**Claude (Anthropic):** XML tags are optimal — Claude was specifically trained to recognize XML as a prompt organizing mechanism. Adaptive thinking via `effort` parameter replaces manual chain-of-thought budget control. Avoid ALL-CAPS directives ("CRITICAL: YOU MUST...") as they cause overtriggering in Claude 4.6.

**GPT-4.1+:** Markdown is the recommended starting format; XML works for complex tasks. Follows instructions "more literally" than predecessors — a single clarifying sentence suffices. Prioritizes instructions near the end of prompt when conflicts arise (opposite of most models). Explicit planning between tool calls improved SWE-bench by ~4%.

**Gemini 3:** Either Markdown or XML works equally. Shorter prompts preferred. Temperature must stay at default 1.0 or performance degrades. Place instructions at end of prompt after context. Use anchor phrases ("Based on the information above...") to bridge context to query.

**Llama:** Special token templates vary across versions. Open-source reasoning models (DeepSeek-R1, QwQ) provide reasoning capabilities outside proprietary APIs.

## Deprecated Patterns

Several previously common patterns are now counterproductive on specific models:
- "Think step by step" harms GPT-5 (the model's internal router handles this automatically)
- ALL-CAPS directives cause Claude 4.6 overtriggering
- Low temperature settings degrade Gemini 3 performance
- Prefilled assistant responses are deprecated on Claude 4.6
- Few-shot examples can degrade performance on frontier reasoning models (DeepSeek-R1 explicitly recommends zero-shot)

## Architecture Pattern

The recommended architecture decouples application logic from model quirks through a prompt library layer that internalizes model-specific formatting, context windows, and tool calling. Start with portable constructs for the base, apply model-specific tuning in a separate layer tested per deployment. DSPy's compilation approach — defining behavior via input/output signatures and compiling to model-specific prompts — is the strongest portability solution at the cost of 100-500 LLM calls upfront.
