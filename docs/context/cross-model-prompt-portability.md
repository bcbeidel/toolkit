---
name: "Cross-Model Prompt Portability"
description: "What transfers across LLM families (XML structure, clear instructions) vs. what requires per-model adaptation (API parameters, reasoning modes, token templates), with measured transfer costs"
metadata:
  type: reference
  sources:
    - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
    - https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
    - https://ai.google.dev/gemini-api/docs/prompting-strategies
    - https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/
    - https://arxiv.org/abs/2411.10541
    - https://arxiv.org/html/2512.01420v1
  related:
    - docs/research/cross-model-prompt-portability.md
    - docs/context/prompt-engineering.md
    - docs/context/reasoning-mode-divergence.md
    - docs/context/writing-for-llm-consumption.md
    - docs/context/llm-capabilities-limitations.md
---

## Key Insight

XML tags work everywhere that matters. The truly non-portable layer is API
parameters (system vs. developer messages, reasoning controls, token templates),
not prompt-level formatting. Budget for per-model API integration code, not
per-model prompt rewrites.

## The Portable Layer

Six techniques transfer reliably across Claude, GPT, Gemini, and Llama:

1. **Clear, specific instructions** with explicit success criteria
2. **Role/persona setting** via system messages
3. **Structured delimiters** separating instructions from data (delimiter type varies, principle is universal)
4. **Step-by-step decomposition** for complex tasks
5. **Output format specification**
6. **Context-first, query-last ordering** for long documents

All four model families' official documentation recommends these patterns.

## XML Convergence

XML tags were once considered Claude-specific. That framing is now incorrect.
Anthropic recommends XML natively. OpenAI's GPT-5 guide endorses XML specs,
citing Cursor's validation that "structured XML specs improved instruction
adherence." Gemini accepts XML alongside Markdown. The convergence is documented
but its permanence is uncertain — it may reflect Claude's market influence rather
than a durable architectural advantage.

For cross-model prompts, XML is the safest default structuring format today.

## The Non-Portable Layer

API-level parameters differ completely and require per-model code:

- **Claude:** Adaptive thinking, XML tag nesting with attributes, `<thinking>`/`<answer>` separation
- **GPT:** Developer messages (replacing system messages for reasoning models), `reasoning_effort` parameter, "Formatting re-enabled" string for Markdown output, Markdown refresh every 3-5 messages
- **Gemini:** Negative constraints must go at end of prompt (may be dropped if placed early), temperature locked at 1.0 for Gemini 3, system instruction vs. user prompt distinction
- **Llama:** Strict special token templates (`<|begin_of_text|>`, `<|start_header_id|>`), exact newline placement required, Meta built Prompt Ops specifically for cross-model transformation

## Transfer Costs Are Measured

Cross-model transfer has a quantified penalty. PromptBridge found a GPT-5-optimized
prompt drops from 99.39% to 68.70% accuracy on Llama-3.1-70B — a 30.69 percentage
point loss. Even within OpenAI's family, GPT-4o prompts transferred to o3 yield
92.27% vs. o3's achievable 98.37%.

Format sensitivity scales inversely with model size. GPT-3.5 showed 40-300%
performance variation depending on format. GPT-4 was more consistent. No study
has tested current frontier models (GPT-5, Claude 4.x, Gemini 3), but the trend
suggests format matters less for larger models — content quality matters more.

## Practical Implications

**For single-model deployments:** Optimize for the target model's conventions.
The performance ceiling is higher with model-specific tuning.

**For multi-model deployments:** Use XML structure as the common layer. Isolate
model-specific elements (reasoning parameters, message types, token templates)
in API integration code rather than prompt text. Accept a 6-30pp accuracy gap
or invest in per-model prompt variants.

**For prompt maintenance:** Re-evaluate prompts on every model upgrade. IoU scores
between GPT versions were often below 0.2, indicating optimizations do not
transfer even within the same model family across generations.
