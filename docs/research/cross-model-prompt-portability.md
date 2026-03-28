---
name: "Cross-Model Prompt Portability"
description: "Format choice measurably affects LLM performance (40-300% variation on smaller models), but XML tags are converging as a cross-model standard while model-specific API parameters and reasoning modes remain the key non-portable elements"
metadata:
  type: research
  sources:
    - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
    - https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
    - https://ai.google.dev/gemini-api/docs/prompting-strategies
    - https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/
    - https://arxiv.org/abs/2411.10541
    - https://arxiv.org/html/2502.04295v3
    - https://arxiv.org/html/2512.01420v1
    - https://github.com/meta-llama/prompt-ops
    - https://platform.openai.com/docs/guides/prompt-engineering
    - https://simonwillison.net/2025/Feb/2/openai-reasoning-models-advice-on-prompting/
    - https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide
    - https://blog.promptlayer.com/model-agnostic/
  related:
    - docs/context/cross-model-prompt-portability.md
    - docs/context/reasoning-mode-divergence.md
---

## Summary

Prompt formatting conventions differ across Claude, GPT, Gemini, and Llama model families, but the gap is narrowing. XML tags, once considered Claude-specific, are now recommended by OpenAI (GPT-5 guide) and accepted by Gemini. The truly non-portable elements are API-level parameters (reasoning modes, developer messages, token templates) rather than prompt-level formatting.

**Key findings:**

- **Format affects performance measurably.** Zhu et al. (2024) found 40-300% performance variation depending on prompt format, with p-values below 0.01 [5]. However, larger models show greater format resilience, and no study has tested current frontier models (HIGH).
- **XML tags are converging as a cross-model standard.** Claude recommends XML natively [1], OpenAI's GPT-5 guide endorses XML specs citing Cursor's validation [2], and Gemini accepts XML alongside Markdown [3] (MODERATE).
- **Cross-model prompt transfer is costly.** PromptBridge found a GPT-5-optimized prompt drops from 99.39% to 68.70% accuracy on Llama-3.1-70B [7]. Even GPT-4o-to-o3 transfer loses 6pp (HIGH).
- **Reasoning modes are the biggest divergence.** Claude uses adaptive thinking, GPT has reasoning models with developer messages, Gemini has Deep Think, and Llama has no built-in reasoning. The API parameters are completely incompatible (HIGH).

15 searches across Google, 12 sources used (7 T1, 3 T3, 1 T4, 1 T5).

## Findings

### Model-Specific Formatting Conventions

Each model family has documented formatting preferences, but these have been converging more than diverging in 2024-2025 (HIGH -- 6 T1 sources converge on this pattern).

**Claude (Anthropic):** XML tags are the primary structuring mechanism. Anthropic's documentation explicitly recommends wrapping prompt components in descriptive XML tags like `<instructions>`, `<context>`, `<input>`, `<example>`, and `<documents>` [1]. For long-context prompts, placing documents at the top and queries at the bottom improves response quality by up to 30% [1]. Claude 4.6 introduced adaptive thinking and deprecated prefilled responses, shifting toward system-prompt-driven control (MODERATE -- single vendor claim about 30% improvement).

**GPT/OpenAI:** The GPT family has evolved from Markdown-centric to XML-accepting. GPT-5 does not format responses in Markdown by default [2]. OpenAI's GPT-5 guide explicitly endorses structured XML specs, citing Cursor's testing that "structured XML specs like <[instruction]_spec> improved instruction adherence" [2]. Reasoning models (o1, o3) introduced developer messages replacing system messages and require "Formatting re-enabled" on the first line to output Markdown [10]. GPT-5 is notably sensitive to contradictory instructions, expending reasoning tokens trying to reconcile them [2] (HIGH -- T1 + T4 sources converge).

**Gemini (Google):** Gemini takes a format-agnostic approach, accepting both XML tags and Markdown headings but requiring consistency within a single prompt [3]. A distinctive finding: Gemini may drop negative constraints or formatting constraints that appear too early in complex prompts, so critical constraints should be placed at the end [3][11]. Gemini 3 favors shorter, more direct prompts than its predecessors and recommends keeping temperature at the default 1.0 [11] (HIGH -- T1 sources from both Google AI and Google Cloud converge).

**Llama/Open-source (Meta):** Llama models use strict special token formatting (`<|begin_of_text|>`, `<|start_header_id|>`, `<|eot_id|>`) and are highly sensitive to template deviations [4]. Meta built Llama Prompt Ops specifically to transform prompts from GPT, Claude, and Gemini formats into Llama-compatible formats [8], demonstrating that cross-model portability is a recognized problem requiring tooling. The tokenizer handles special tokens, but newlines must be present exactly as specified [4] (HIGH -- T1 official documentation).

### Empirical Format Effects

Format choice measurably affects LLM performance, though the magnitude depends heavily on model size and generation (HIGH -- T3 sources with empirical methodology).

**Quantified variations:** Zhu et al. (2024) found GPT-3.5-turbo showed up to 40% performance variation in code translation depending on prompt template, and a 200% improvement switching from Markdown to plain text on the FIND dataset [5]. GPT-4-32k showed over 300% performance boost changing from JSON to plain text on HumanEval [5]. P-values were mostly below 0.01, demonstrating statistical significance [5].

**No universal optimal format:** The same study found "no universally optimal format exists, even within the same generational lineage" [5]. GPT-3.5 performed best with JSON formatting while GPT-4 performed best with Markdown [5]. IoU scores between different GPT versions were often below 0.2, indicating prompt optimizations do not transfer even within the same model family [5] (HIGH -- peer-reviewed empirical evidence).

**Content-format interaction:** CFPO research demonstrated that optimal formatting depends on prompt content, not just the model [6]. Joint content-format optimization achieved 90-94% on Big-Bench Classification vs 56-78% for content-only optimization across Mistral-7B, LLaMA-3.1-8B, and Phi-3 [6] (MODERATE -- tested only on smaller open-source models).

**Model size reduces sensitivity:** Larger models demonstrate greater resilience to format changes. GPT-4's consistency score exceeded 0.5 on MMLU while GPT-3.5's was below 0.5 [5]. This suggests frontier models may be less format-sensitive, though no study has tested this on GPT-5, Claude 4.x, or Gemini 3 specifically (MODERATE -- trend observed but not confirmed for current frontier models).

### Universal vs Model-Specific Patterns

**Universal techniques** (work across all model families):
- Clear, specific instructions with explicit success criteria [1][2][3][9]
- Role/persona setting via system messages [1][2][3]
- Structured delimiters to separate instructions from data (the delimiter type varies, but the principle is universal) [1][2][3][9]
- Step-by-step decomposition for complex tasks [1][9]
- Output format specification [1][2][3][12]
- Context-first, query-last ordering for long documents [1][3]

(HIGH -- all four T1 official docs recommend these patterns)

**Converging techniques** (increasingly accepted across families):
- XML tags for prompt structuring -- originally associated with Claude, now recommended by OpenAI (GPT-5 guide) and accepted by Gemini [1][2][3]
- JSON/structured output specification [1][2][12]
- Temperature and generation parameter control [2][11]

(MODERATE -- convergence is documented but its permanence is uncertain)

**Model-specific techniques:**
- Claude: XML tag nesting with attributes (`<document index="n">`), `<thinking>`/`<answer>` tag patterns for CoT separation, adaptive thinking API parameter [1]
- GPT: Developer messages for reasoning models, "Formatting re-enabled" string, `reasoning_effort` and `verbosity` parameters, markdown instruction refresh every 3-5 messages [2][10]
- Gemini: Negative constraint placement at end of prompt, temperature locked at 1.0 for Gemini 3, system instruction vs user prompt distinction for constraint anchoring [3][11]
- Llama: Strict special token templates, format-sensitive tokenization requiring exact newline placement, need for Prompt Ops transformation from other model formats [4][8]

(HIGH -- documented in T1 official sources)

**Cross-model transfer is costly:** PromptBridge research quantified that a prompt optimized for GPT-5 (99.39% accuracy) drops to 68.70% on Llama-3.1-70B, a 30.69 percentage point loss and 10.69pp below Llama's own optimal [7]. Even within OpenAI's family, GPT-4o prompts transferred to o3 yielded 92.27% vs o3's achievable 98.37% [7] (HIGH -- empirical evidence across 7 models).

### Reasoning and Chain-of-Thought Differences

Models diverge significantly in how they handle reasoning prompts (MODERATE -- comparison based on T1 docs from different vendors, limited cross-model empirical studies).

**Claude:** Uses adaptive thinking (Claude 4.6) where the model dynamically decides when and how much to think. Extended thinking with `<thinking>` tags in output. General instructions ("think thoroughly") often produce better reasoning than prescriptive step-by-step plans. Claude is sensitive to the word "think" when extended thinking is disabled [1].

**GPT/OpenAI:** Reasoning models (o1, o3, o4-mini) generate explicit chain-of-thought internally. GPT-5 supports `reasoning_effort` parameter (minimal/medium/high). Few-shot examples are less necessary for reasoning models -- "try to write prompts without examples first" [10]. Contradictory instructions are particularly damaging because the model spends reasoning tokens reconciling them [2].

**Gemini:** Gemini 2.5 Pro introduced "Deep Think" mode for internal chain-of-thought. Gemini 3 performs internal reasoning before answering by default. Google recommends direct prompts over verbose ones -- the model "favors directness over persuasion and logic over verbosity" [11].

**Llama/Open-source:** No built-in reasoning mode. Chain-of-thought must be explicitly prompted. Performance is highly sensitive to prompt template and formatting [4][6].

**Counter-evidence:** The emerging pattern of built-in reasoning modes (Claude's adaptive thinking, GPT's reasoning models, Gemini's Deep Think) suggests that explicit CoT prompting may become less important for frontier models. However, this creates a new divergence: some models reason internally by default while others still require prompting, and the API parameters to control reasoning depth differ completely across families [1][2][11].

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| XML tags are Claude-specific and not recommended for other models | Anthropic docs explicitly recommend XML [1]; GPT-5 guide also recommends XML specs [2]; Gemini accepts XML or Markdown [3] | GPT-5 guide shows Cursor found XML improved instruction adherence [2]; Gemini docs explicitly support XML tags [3] | HIGH -- the core "XML = Claude only" framing is already false. XML is converging as a cross-model structuring format. |
| Prompt format effects are significant enough to matter in practice | Research shows 40-300% variation in some tasks [5]; PromptBridge shows 10-30pp transfer gaps [7] | These dramatic numbers come from smaller/older models (GPT-3.5, GPT-4-32k); larger models show more resilience [5] | MODERATE -- format sensitivity may be overstated for current-gen frontier models |
| Official documentation accurately reflects optimal usage | T1 sources from model creators [1-4, 8-9, 11] | Docs may lag behind model capabilities; community discovers optimizations ahead of official guidance | LOW -- official docs are the most reliable guide, even if not exhaustive |
| Few-shot prompting universally improves performance | General consensus across model families | OpenAI reasoning models documentation says "try to write prompts without examples first" [10] | MODERATE -- reasoning models represent a genuine exception to this pattern |
| Larger models are more robust to format variations | Zhu et al. show GPT-4 more consistent than GPT-3.5 [5] | No evidence for frontier models (GPT-5, Claude 4.x, Gemini 3); study only tested GPT family | MODERATE -- the trend may not hold across families |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Format sensitivity research is already outdated -- frontier models (GPT-5, Claude 4.6, Gemini 3) may have largely eliminated format sensitivity through better training | High | Core finding about "format matters" would need qualification: it matters for smaller/open-source models but decreasingly for frontier models |
| The convergence toward XML across model families may be a temporary trend driven by Claude's popularity rather than a genuine architectural advantage | Medium | Would weaken the "XML as universal format" recommendation |
| Open-source model landscape changes rapidly -- Llama 4 and other models may have already reduced the format sensitivity gap that drove Meta to build prompt-ops | Medium | Would narrow the scope of SQ3 findings about model-specific adaptation needs |

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags | Prompting best practices | Anthropic | 2025 | verified | T1 |
| 2 | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | GPT-5 prompting guide | OpenAI | 2025 | verified | T1 |
| 3 | https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt design strategies | Google | 2025 | verified | T1 |
| 4 | https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/ | Llama 3.1 Model Cards and Prompt formats | Meta | 2024 | verified | T1 |
| 5 | https://arxiv.org/abs/2411.10541 | Does Prompt Formatting Have Any Impact on LLM Performance? | Zhu et al. | 2024 | verified | T3 |
| 6 | https://arxiv.org/html/2502.04295v3 | Beyond Prompt Content: Content-Format Integrated Prompt Optimization | Research paper | 2025 | verified | T3 |
| 7 | https://arxiv.org/html/2512.01420v1 | PromptBridge: Cross-Model Prompt Transfer for LLMs | Research paper | 2025 | verified | T3 |
| 8 | https://github.com/meta-llama/prompt-ops | Llama Prompt Ops | Meta | 2025 | verified | T1 |
| 9 | https://platform.openai.com/docs/guides/prompt-engineering | Prompt engineering guide | OpenAI | 2025 | verified | T1 |
| 10 | https://simonwillison.net/2025/Feb/2/openai-reasoning-models-advice-on-prompting/ | OpenAI reasoning models: Advice on prompting | Simon Willison | 2025 | verified | T4 |
| 11 | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide | Gemini 3 prompting guide | Google Cloud | 2025 | verified | T1 |
| 12 | https://blog.promptlayer.com/model-agnostic/ | Model Agnostic Prompts | PromptLayer | 2025 | verified | T5 |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "placing documents at top and queries at bottom improves response quality by up to 30%" | statistic | [1] | verified |
| 2 | "structured XML specs like <[instruction]_spec> improved instruction adherence" (Cursor testing) | quote | [2] | verified |
| 3 | GPT-5 does not format responses in Markdown by default | attribution | [2] | verified |
| 4 | Reasoning models require "Formatting re-enabled" string for Markdown output | attribution | [2],[10] | verified |
| 5 | "Gemini may drop negative constraints or formatting constraints that appear too early in complex prompts" | quote | [3] | verified |
| 6 | GPT-3.5-turbo showed "up to 40% performance variation in code translation tasks" | statistic | [5] | verified |
| 7 | "200% improvement when switching from Markdown to plain text" on FIND dataset | statistic | [5] | verified |
| 8 | GPT-4-32k showed "over 300% performance boost when changing from JSON to plain text" on HumanEval | statistic | [5] | verified |
| 9 | "No universally optimal format exists, even within the same generational lineage" | quote | [5] | verified |
| 10 | IoU scores between GPT versions "often below 0.2" | statistic | [5] | verified |
| 11 | CFPO achieved 90-94% on Big-Bench Classification vs 56-78% for baselines | statistic | [6] | verified |
| 12 | GPT-5 optimized prompt achieves 99.39% on GPT-5, drops to 68.70% on Llama-3.1-70B | statistic | [7] | verified |
| 13 | Llama-3.1-70B optimal performance is 79.47% | statistic | [7] | verified |
| 14 | GPT-4o to o3 transfer yields 92.27% vs o3's achievable 98.37% | statistic | [7] | verified |
| 15 | PromptBridge achieved 27.39% improvement on SWE-Bench and 39.44% on Terminal-Bench | statistic | [7] | verified |
| 16 | "Reasoning models often don't need few-shot examples" | quote | [10] | verified |
| 17 | GPT-5 achieves 69.6% on Scale MultiChallenge instruction following | statistic | OpenAI GPT-5 announcement | corrected (source is OpenAI announcement, not prompting guide) |
| 18 | GPT-5 achieves 96.7% on tau2-bench telecom for tool calling | statistic | OpenAI GPT-5 announcement | corrected (source is OpenAI announcement, not prompting guide) |

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| Anthropic Claude prompt engineering XML tags formatting best practices 2025 | google | 2024-2026 | 10 | 2 |
| OpenAI GPT prompt formatting system messages markdown best practices 2025 | google | 2024-2026 | 10 | 3 |
| Google Gemini prompt engineering formatting guidelines 2025 | google | 2024-2026 | 10 | 2 |
| Llama Meta open source LLM prompt template sensitivity formatting 2025 | google | 2024-2026 | 10 | 3 |
| prompt format effect LLM performance benchmark XML markdown structured 2024 2025 | google | 2024-2025 | 10 | 3 |
| chain of thought prompting differences across models GPT Claude Gemini comparison 2025 | google | 2024-2025 | 10 | 1 |
| universal prompt engineering techniques work all LLMs model-agnostic portable 2025 | google | 2024-2026 | 10 | 1 |
| prompt engineering cross-model portability model-specific formatting comparison study 2024 2025 | google | 2024-2025 | 10 | 1 |
| Llama 3 prompt template special tokens BOS EOS format sensitivity performance impact | google | 2024-2025 | 10 | 1 |
| Gemini 3 prompt format XML markdown system instruction negative constraints end of prompt 2025 | google | 2024-2025 | 10 | 0 |
| few-shot prompting chain-of-thought reasoning performance comparison GPT Claude Gemini Llama benchmark 2025 | google | 2024-2025 | 10 | 0 |
| simonwillison OpenAI reasoning models prompting advice developer message 2025 | google | 2025 | 8 | 1 |
| Cursor structured XML prompt instruction adherence GPT-5 improvement 2025 | google | 2025 | 10 | 0 |
| OpenAI GPT-5 developer message system message structured prompts XML tags formatting 2025 | google | 2025 | 10 | 0 |
| meta llama prompt-ops prompt optimization transformation heuristics cross-model 2025 | google | 2025 | 10 | 1 |

15 searches across Google, 148 results found, 19 used. Not searched: arxiv direct search, Google Scholar, Hugging Face community forums.

## Limitations and Follow-ups

**Limitations:**
- Empirical format studies [5][6] tested older/smaller models (GPT-3.5, GPT-4, Mistral-7B, LLaMA-8B). No published benchmarks test format sensitivity on GPT-5, Claude 4.x, or Gemini 3.
- PromptBridge [7] is the only study measuring cross-model transfer quantitatively; its task coverage is limited to coding benchmarks.
- Official documentation [1-4, 8-9, 11] represents vendor recommendations, which may be optimistic about their own models' capabilities.
- This analysis does not cover DeepSeek, Qwen, or other model families gaining traction in 2025-2026.

**Follow-up questions:**
- Do format sensitivity findings hold for frontier models (GPT-5, Claude 4.6, Gemini 3)?
- Is XML convergence a durable trend or a temporary artifact of Claude's market influence?
- How do prompt portability challenges change when using tool-use and function-calling APIs?
- What is the performance impact of Llama Prompt Ops transformations on specific task types?

## Key Takeaways

1. **XML tags work everywhere that matters.** Claude recommends them natively, GPT-5 endorses them (validated by Cursor), and Gemini accepts them. Use XML as the default structuring format for cross-model prompts.

2. **The non-portable layer is API parameters, not prompt content.** System messages vs developer messages, reasoning_effort vs adaptive thinking, special token templates -- these require per-model code, not per-model prompts.

3. **Format sensitivity scales inversely with model size.** Smaller models (GPT-3.5, Llama-8B) show dramatic format sensitivity (40-300%). Larger models are more resilient. For frontier models, getting the content right matters more than getting the format right.

4. **Cross-model transfer has a measured cost.** Expect 6-30pp accuracy loss when transferring optimized prompts between model families without adaptation [7]. Budget for per-model prompt tuning or use tools like Llama Prompt Ops [8] / PromptBridge [7].

5. **Reasoning modes are diverging, not converging.** Each family has a different mechanism (adaptive thinking, reasoning models, Deep Think) with incompatible API parameters. Explicit CoT prompting remains the only portable reasoning technique.
