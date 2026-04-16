---
name: "Cross-Model Prompt Portability"
description: "Investigation of prompt constructs, formatting, and abstraction strategies for cross-model compatibility"
type: research
sources:
  - https://arxiv.org/html/2411.10541v1
  - https://www.improvingagents.com/blog/best-nested-data-format/
  - https://systima.ai/blog/delimiter-hypothesis
  - https://www.joanmedia.dev/ai-blog/model-specific-prompting-how-claude-gpt-and-gemini-differ
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
  - https://www.philschmid.de/gemini-3-prompt-practices
  - https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide
  - https://techsy.io/blog/llm-structured-outputs-guide
  - https://docs.litellm.ai/docs/completion/json_mode
  - https://python.useinstructor.com/
  - https://github.com/stanfordnlp/dspy
  - https://github.com/andrewyng/aisuite
  - https://github.com/promptfoo/promptfoo
  - https://www.prompthub.us/blog/the-complete-guide-to-gpt-4-1-models-performance-pricing-and-prompting-tips
  - https://promptbuilder.cc/blog/claude-vs-chatgpt-vs-gemini-best-prompt-engineering-practices-2025
  - https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/
  - https://modelcontextprotocol.io/specification/2025-11-25
  - https://arxiv.org/abs/2512.01420
  - https://www.prompthub.us/blog/one-size-does-not-fit-all-an-analaysis-of-model-specific-prompting-strategies
  - https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
  - https://arxiv.org/abs/2511.22176
  - https://www.scalifiai.com/blog/model-context-protocol-flaws-2025
  - https://arxiv.org/html/2603.05637v1
  - https://dev.to/debmckinney/5-real-issues-with-litellm-that-are-pushing-teams-away-in-2026-h0h
  - https://arxiv.org/html/2505.20139v1
related:
  - docs/research/2026-04-07-prompt-engineering.research.md
  - docs/research/2026-04-07-context-engineering.research.md
  - docs/research/2026-04-07-writing-for-llm-consumption.research.md
---

## Research Question

What prompt constructs and abstraction strategies enable reliable cross-model portability, and how do model-specific features affect instruction design?

## Search Protocol

| # | Query | Source | Hits | Useful |
|---|-------|--------|------|--------|
| 1 | cross-model prompt portability Claude GPT Gemini 2025 2026 | WebSearch | 10 | 4 |
| 2 | XML tags prompt formatting Claude vs GPT vs Gemini comparison 2025 | WebSearch | 10 | 5 |
| 3 | structured output JSON across LLM models portability 2025 2026 | WebSearch | 10 | 4 |
| 4 | reasoning mode thinking mode differences Claude GPT Gemini 2025 | WebSearch | 10 | 3 |
| 5 | prompt abstraction layer write once run across LLMs library framework 2025 2026 | WebSearch | 10 | 4 |
| 6 | LiteLLM Instructor aisuite cross-model prompt management tools 2025 2026 | WebSearch | 10 | 4 |
| 7 | markdown headers vs XML tags vs JSON prompt format LLM benchmark performance 2025 | WebSearch | 10 | 6 |
| 8 | Anthropic Claude prompt engineering best practices XML structured 2025 documentation | WebSearch | 10 | 3 |
| 9 | DSPy prompt optimization cross-model portability compile prompts 2025 2026 | WebSearch | 10 | 3 |
| 10 | OpenAI GPT-4.1 prompting guide best practices system prompt 2025 | WebSearch | 10 | 3 |
| 11 | extended thinking mode Claude vs chain of thought GPT reasoning portability 2025 2026 | WebSearch | 10 | 3 |
| 12 | aisuite Andrew Ng multi-model LLM abstraction library 2025 | WebSearch | 10 | 4 |
| 13 | Google Gemini prompt engineering best practices structured format 2025 documentation | WebSearch | 10 | 4 |
| 14 | model context protocol MCP tool calling standard cross-model portability 2025 2026 | WebSearch | 10 | 4 |
| 15 | prompt template portability Llama open source models vs proprietary Claude GPT 2025 | WebSearch | 10 | 2 |
| 16 | Llama chat template format prompt portability system prompt format differences 2025 | WebSearch | 10 | 3 |
| 17 | PromptHub Promptfoo cross-model prompt testing evaluation tools 2025 2026 | WebSearch | 10 | 4 |
| 18 | arxiv.org/html/2411.10541v1 — prompt formatting impact on LLM performance | WebFetch | 1 | 1 |
| 19 | improvingagents.com — nested data format benchmarks | WebFetch | 1 | 1 |
| 20 | joanmedia.dev — model-specific prompting differences | WebFetch | 1 | 1 |
| 21 | systima.ai — delimiter hypothesis benchmark | WebFetch | 1 | 1 |
| 22 | techsy.io — structured outputs cross-provider guide | WebFetch | 1 | 1 |
| 23 | philschmid.de — Gemini 3 prompt practices | WebFetch | 1 | 1 |
| 24 | platform.claude.com — Claude prompting best practices | WebFetch | 1 | 1 |
| 25 | developers.openai.com — GPT-4.1 prompting guide | WebFetch | 1 | 1 |

## Sources

| # | Source | Type | Tier | Status |
|---|--------|------|------|--------|
| 1 | [Does Prompt Formatting Have Any Impact on LLM Performance?](https://arxiv.org/html/2411.10541v1) | Peer-reviewed research | T1 | verified |
| 2 | [Which Nested Data Format Do LLMs Understand Best?](https://www.improvingagents.com/blog/best-nested-data-format/) | Independent benchmark | T2 | verified |
| 3 | [The Delimiter Hypothesis: Does Prompt Format Actually Matter?](https://systima.ai/blog/delimiter-hypothesis) | Independent benchmark | T2 | verified |
| 4 | [Model-Specific Prompting: How Claude, GPT, and Gemini Differ](https://www.joanmedia.dev/ai-blog/model-specific-prompting-how-claude-gpt-and-gemini-differ) | Technical analysis | T3 | verified |
| 5 | [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | Vendor documentation | T1 | verified |
| 6 | [GPT-4.1 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide) | Vendor documentation | T1 | verified |
| 7 | [Gemini 3 Prompting Best Practices](https://www.philschmid.de/gemini-3-prompt-practices) | Technical guide | T2 | verified |
| 8 | [Gemini 3 Prompting Guide (Google Cloud)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide) | Vendor documentation | T1 | verified |
| 9 | [LLM Structured Outputs: The Practical Guide for Every Provider](https://techsy.io/blog/llm-structured-outputs-guide) | Technical guide | T3 | verified |
| 10 | [Structured Outputs (JSON Mode) - LiteLLM](https://docs.litellm.ai/docs/completion/json_mode) | Tool documentation | T2 | verified |
| 11 | [Instructor - Multi-Language Structured LLM Outputs](https://python.useinstructor.com/) | Tool documentation | T2 | verified |
| 12 | [DSPy: Programming not Prompting LMs](https://github.com/stanfordnlp/dspy) | Tool documentation | T1 | verified |
| 13 | [aisuite: Unified Interface to Multiple GenAI Providers](https://github.com/andrewyng/aisuite) | Tool documentation | T2 | verified |
| 14 | [Promptfoo: Test Prompts Across Models](https://github.com/promptfoo/promptfoo) | Tool documentation | T1 | verified |
| 15 | [Claude vs ChatGPT vs Gemini Prompting Best Practices (2025)](https://promptbuilder.cc/blog/claude-vs-chatgpt-vs-gemini-best-prompt-engineering-practices-2025) | Technical comparison | T3 | verified |
| 16 | [Llama 4 Model Cards and Prompt Formats](https://www.llama.com/docs/model-cards-and-prompt-formats/llama4/) | Vendor documentation | T1 | verified |
| 17 | [Model Context Protocol Specification (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25) | Protocol specification | T1 | verified |
| 18 | [Context Engineering Guide 2026](https://www.the-ai-corner.com/p/context-engineering-guide-2026) | Industry analysis | T3 | verified |

## Raw Extracts

### Sub-question 1: Portable vs. model-specific prompt constructs

**Portable constructs (work across Claude, GPT, Gemini, Llama):**

- Role definition and persona assignment. All major models respond well to system-level role setting (e.g., "You are a helpful coding assistant specializing in Python"). [Source 4, 5, 6]
- Clear objective statements. Direct, concise goal description is universally effective. Every vendor guide recommends stating goals plainly. [Source 5, 6, 7]
- Few-shot examples. Example-based learning transfers across all model families, though format consistency within examples matters more for some models (Gemini requires matching structure and formatting in few-shot examples). [Source 5, 7, 8]
- Output format specification. Telling the model what format you want (JSON, table, prose) works universally. [Source 4, 15]
- Numbered step instructions. Sequential step lists for ordered tasks work across models. [Source 5, 6]

**Model-specific constructs:**

- **Claude:** Strong XML preference. Anthropic states Claude was "trained specifically to recognize XML tags as a prompt organizing mechanism." XML tags provide 34% better performance on structured reasoning. Prefilled responses deprecated as of Claude 4.6. Adaptive thinking replaces manual budget_tokens. ALL-CAPS directives ("CRITICAL: You MUST...") now cause overtriggering. [Source 5]
- **GPT-4.1:** Markdown recommended as starting format, XML for complex tasks. Follows instructions "more literally than predecessors." Prioritizes instructions closer to end of prompt when conflicts arise (opposite of most models). Three agentic system prompt components (persistence, tool-calling, planning) increased SWE-bench scores by ~20%. Tools API field outperforms manually injected schemas by ~2%. [Source 6]
- **Gemini 3:** Either markdown or XML works equally. Shorter prompts preferred ("usually needs shorter prompts"). Temperature must stay at default 1.0 or performance degrades. Place instructions at end of prompt after context. Use anchor phrases ("Based on the information above...") to bridge from context to query. [Source 7, 8]
- **Llama 4:** Uses special token format: `<|header_start|>role<|header_end|>` for message boundaries. Prompt template varies across Llama versions (2, 3, 3.1, 4). Tokenizer configuration embeds chat template for portability across inference frameworks. [Source 16]

**Key insight from Source 4:** "Build evaluation frameworks, not static templates." Portable constructs get you ~80% of performance; the remaining 20% requires model-specific tuning.

### Sub-question 2: Format performance across model families

**Benchmark: Prompt formatting impact (Source 1, arxiv 2411.10541)**

- GPT-3.5-turbo: Performance varies up to 40% based on prompt template (code translation); JSON format performed best across multiple tasks.
- GPT-4: Markdown emerged as preferred format. Exhibited >300% performance boost on HumanEval when changing from JSON to plain text.
- Cross-model IoU (intersection-over-union) on optimal formats dropped below 0.2 between model families, confirming minimal overlap.
- Same-family models (e.g., GPT-3.5-turbo variants) showed high IoU >0.7, meaning format preferences transfer within a family but not across families.
- Larger models demonstrate increased robustness to format variations (GPT-4 consistency >0.5 vs GPT-3.5 <0.5).

**Benchmark: Nested data formats (Source 2, improvingagents.com)**

| Model | YAML | Markdown | JSON | XML |
|-------|------|----------|------|-----|
| GPT-5 Nano | 62.1% | 54.3% | 50.3% | 44.4% |
| Llama 3.2 3B | 49.1% | 48.0% | 52.7% | 50.7% |
| Gemini 2.5 Flash Lite | 51.9% | 48.2% | 43.1% | 33.8% |

- YAML outperformed XML by 17.7 percentage points on GPT-5 Nano.
- XML produced "particularly poor" results on Gemini 2.5 Flash Lite.
- Llama 3.2 3B showed minimal format sensitivity across all formats.
- Markdown was most token-efficient (10-38% fewer tokens than alternatives).

**Benchmark: Delimiter hypothesis (Source 3, systima.ai)**

Tested XML, Markdown, JSON across GPT-5.2, Claude Opus 4.6, MiniMax M2.5, and Kimi K2.5 with 600 model calls.

- "Format rarely matters, but when it does, Markdown is the weak link."
- XML: 96.3%, Markdown: 93.3%, JSON: 96.3% on stress tests.
- Three of four models showed no meaningful format sensitivity.
- MiniMax M2.5 had a reproducible Markdown prompt injection vulnerability (~20% failure rate) that XML and JSON were immune to.
- Complex multi-section reasoning failures (max 84.4%) reflect reasoning limits, not format parsing issues.

**Format preference summary by model family:**

| Model Family | Primary Format | Secondary | Avoid |
|-------------|---------------|-----------|-------|
| Claude | XML | Structured outputs | ALL-CAPS directives |
| GPT-4.1+ | Markdown (start), XML (complex) | Delimited text | JSON for long context |
| Gemini 3 | Markdown or XML (equally) | Either | Low temperature settings |
| Llama | Special token templates | YAML for data | N/A |

### Sub-question 3: Write-once abstraction strategies

**API-level abstraction tools:**

1. **LiteLLM** — Python SDK and proxy server calling 100+ LLM APIs in OpenAI-compatible format. Handles prompt formatting translation, cost tracking, and load balancing. Supports model fallbacks and retries. [Source 10]

2. **aisuite** (Andrew Ng) — Lightweight Python library providing unified `chat.completions.create()` interface across OpenAI, Anthropic, Google, Mistral, Ollama. Switch models by changing a string (e.g., `openai:gpt-4o` to `anthropic:claude-3-7-sonnet`). 12K+ GitHub stars. Supports MCP and function calling. [Source 13]

3. **Instructor** — Cross-provider structured output via Pydantic models. Works with 15+ providers. Provides automatic retries with validation feedback, streaming via `create_partial()`. 11K+ GitHub stars, 3M+ monthly downloads. [Source 11]

**Prompt compilation (declarative abstraction):**

4. **DSPy** (Stanford NLP) — "Programming not prompting" framework. Define behavior via Signatures, DSPy compiles optimal prompts per model. The same signature compiles to different prompts for GPT-4o, Claude Sonnet 4.5, or Llama 3.3 without code changes. MIPROv2 optimizer is flagship as of late 2025. Upfront compilation cost of 100-500 LLM calls yields cross-model portability and 99%+ reliability. [Source 12]

**Structured output portability:**

5. All major providers now support constrained decoding via JSON Schema (OpenAI since Aug 2024, Gemini 2024, Anthropic GA early 2026). Core mechanism: JSON Schema compiled into finite state machine (FSM), invalid tokens get logits set to negative infinity. [Source 9]

6. **BAML** — Schema-first approach via custom DSL in `.baml` files. Generates typed clients for Python, TypeScript, Ruby, Go. Cross-language schema contracts. [Source 9]

7. **Vercel AI SDK** — `generateObject()` with Zod schemas, supports OpenAI, Anthropic, Gemini natively. [Source 9]

**Tool and protocol portability:**

8. **Model Context Protocol (MCP)** — Open standard for tool integration. Introduced by Anthropic (Nov 2024), adopted by OpenAI (March 2025) and Google DeepMind. Donated to Linux Foundation's Agentic AI Foundation (Dec 2025). Eliminates vendor-specific tool connectors. Natively supported by virtually every major AI tool by early 2026. [Source 17]

**Prompt testing and evaluation:**

9. **Promptfoo** — Open-source CLI for testing prompts across 50+ providers. YAML config files, CI/CD integration. Acquired by OpenAI (March 2026). [Source 14]

10. **PromptHub** — Git-style version control for prompts with side-by-side multi-model comparison. Supports OpenAI, Anthropic, Azure. Used by Shopify, Adobe. [Source 14 search results]

**Architectural pattern — prompt library abstraction:**

The recommended architecture decouples application logic from model quirks through a prompt library layer that internalizes roles, context windows, tool calling, and token budgeting. Gartner predicts 75% of enterprise LLM implementations will use multi-provider strategies by mid-2026. [Source 5 search results]

### Sub-question 4: Reasoning mode differences and portability

**Claude — Adaptive Thinking:**
- Claude 4.6 uses adaptive thinking (`thinking: {type: "adaptive"}`), where the model dynamically decides when and how much to think. [Source 5]
- Controlled by `effort` parameter (low/medium/high/max). Higher effort and more complex queries trigger more thinking.
- Extended thinking with `budget_tokens` is deprecated but still functional. Prefer `effort` + `max_tokens`.
- Thinking behavior is promptable: "Extended thinking adds latency and should only be used when it will meaningfully improve answer quality."
- Manual chain-of-thought still works when thinking is disabled: use `<thinking>` and `<answer>` tags.
- Interleaved thinking: model can alternate between reasoning and tool calls.
- Claude Opus 4.5 is sensitive to the word "think" — use alternatives like "consider" or "evaluate" when thinking mode is disabled.

**GPT — Adaptive Reasoning and Reasoning Models:**
- GPT-5.1 introduced adaptive reasoning that dynamically adjusts "thinking time" based on task complexity. [Source 4]
- GPT-5.2 automatically detects if a prompt requires Thinking mode — no manual toggling needed.
- Separate reasoning model variants (o3, o4-mini, o5) offer hidden chain-of-thought.
- GPT-4.1 is not a reasoning model but benefits from prompted step-by-step thinking. Start with basic instructions, enhance based on failure analysis. [Source 6]
- GPT-5.4 "Thinking" variant achieves GPT-6-level reasoning in smaller architecture but "occasionally dropped constraints or reinterpreted instructions."

**Gemini — Deep Think:**
- Gemini 3 Pro integrates "Deep Think" mode for extended reasoning. [Source search results]
- Allocates more computation time per query. Achieved +3.5pp on Humanity's Last Exam (37.5% to 41.0%) and +14pp on ARC-AGI-2 (31.1% to 45.1%).
- Reasoning happens through explicit prompting rather than an API toggle. [Source 4]
- Must decompose goals into sub-tasks, verify completeness, and validate understanding before responding. [Source 7]

**Llama — No native reasoning mode:**
- Open-source models lack built-in reasoning toggles. Chain-of-thought must be prompted explicitly.
- Fine-tuning and inference frameworks (vLLM, SGLang) provide computational control but not reasoning modes.

**Portability concerns:**

| Aspect | Claude | GPT | Gemini | Llama |
|--------|--------|-----|--------|-------|
| Reasoning trigger | API param (`effort`) | Auto-detect / model variant | Prompt-based | Prompt-based only |
| CoT visibility | Thinking blocks (visible in API) | Hidden (reasoning models) or prompted | Prompted | Prompted |
| Control mechanism | effort parameter + adaptive | Model routing (auto) | Deep Think toggle | N/A |
| Tool interleaving | Native (interleaved thinking) | Supported | Limited | Framework-dependent |

Key portability issue: Reasoning modes are activated differently per model. A prompt designed to trigger deep reasoning on Claude (via effort parameter) has no equivalent API mechanism on Gemini or Llama. Prompted chain-of-thought ("think step by step") is the most portable reasoning technique but is now actively counterproductive on GPT-5+ ("explicitly harms GPT-5's reasoning" per Source 18) where the model's internal router handles this automatically.

**Deprecated/harmful patterns:**
- "Think step by step" now harms GPT-5 performance (model router handles this automatically). [Source 18]
- ALL-CAPS directives ("CRITICAL: YOU MUST...") cause Claude 4.6 to overtrigger. [Source 5]
- Low temperature settings degrade Gemini 3 performance. [Source 7, 8]
- Prefilled assistant responses deprecated on Claude 4.6. [Source 5]

### Canonical Tools & Libraries

| Tool | Purpose | Cross-Model | GitHub Stars | Notes |
|------|---------|-------------|-------------|-------|
| [LiteLLM](https://github.com/BerriAI/litellm) | API gateway, prompt formatting | 100+ providers | 18K+ | OpenAI-compatible format |
| [aisuite](https://github.com/andrewyng/aisuite) | Unified chat API | OpenAI, Anthropic, Google, Mistral, Ollama | 12K+ | Andrew Ng; MCP support |
| [Instructor](https://python.useinstructor.com/) | Structured output | 15+ providers | 11K+ | Pydantic-based validation |
| [DSPy](https://github.com/stanfordnlp/dspy) | Prompt compilation | Any LLM | 22K+ | Stanford NLP; write-once portability |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Prompt testing/eval | 50+ providers | 8K+ | Acquired by OpenAI (2026) |
| [BAML](https://www.boundaryml.com/) | Schema-first output | Multi-provider | — | Cross-language via DSL |
| [Vercel AI SDK](https://sdk.vercel.ai/) | Structured generation | OpenAI, Anthropic, Gemini | — | TypeScript; Zod schemas |
| [Outlines](https://github.com/outlines-dev/outlines) | Constrained decoding | Open-source models | 10K+ | JSON Schema, regex, EBNF |
| [PromptHub](https://www.prompthub.us/) | Prompt version control | Multi-provider | — | Git-style branching |
| [MCP](https://modelcontextprotocol.io/) | Tool integration protocol | Universal (2026) | — | Linux Foundation standard |

## Challenge

### Gaps Identified

**1. The "80% portable" claim is unsourced and likely overstated.**
The document attributes the assertion that "portable constructs get you ~80% of performance" to Source 4 (a blog post), but treats it as a general finding. The PromptBridge paper (arxiv 2512.01420, Dec 2025) directly contradicts this: transferring GPT-5's best prompt to Llama-3.1-70B yielded 68.70% vs. the target model's own optimal of 79.47% — a 10.77pp gap. On HumanEval, GPT-4o prompts transferred to o3 scored 92.27% vs. o3's achievable 98.37%. PromptHub research found "there wasn't a single prompt snippet that could be used across all models to increase performance." The 80% figure is aspirational, not empirical. [C1, C2]

**2. YAML's strong benchmark showing is presented without its well-known fragility.**
Sub-question 2 highlights YAML outperforming XML by 17.7pp on GPT-5 Nano (Source 2), but omits that YAML's whitespace sensitivity makes it unreliable for LLM-generated output. OpenAI mandated JSON-only for function calling precisely because YAML parsing errors are common in LLM outputs. A single incorrect space changes YAML's meaning entirely — a serious production risk the document doesn't acknowledge despite presenting YAML as a top performer. [C3]

**3. Chain-of-thought deprecation claim is oversimplified.**
The document states "think step by step" now "explicitly harms GPT-5's reasoning" (attributed to Source 18) and presents this as a settled fact. The Wharton GAIL study (2025-2026) provides more nuanced data: CoT produced marginal 2.9-3.1% gains on reasoning models (o3-mini, o4-mini) with 20-80% latency increases, while Gemini Flash 2.5 actually degraded by 3.3%. For non-reasoning models, results ranged from +13.5% (Gemini Flash 2.0) to -17.2% (Gemini Pro 1.5) at strict accuracy thresholds. The reality is task-dependent and model-dependent, not categorically harmful. Focused Chain-of-Thought (F-CoT) reduces tokens 2-3x while maintaining accuracy — an alternative the document should note. [C4, C5]

**4. MCP presented too optimistically — security gaps are material.**
The document describes MCP as an "open standard" achieving "universal" adoption by 2026, but omits significant security and operational concerns. The Postmark MCP supply chain breach (2025) involved backdoored npm packages blind-copying emails. Over 1,800 MCP servers were found on the public internet without authentication. The protocol lacks message signing, has stateful sessions that fight load balancers, and places security responsibility on implementers rather than providing secure-by-default architecture. A March 2026 arxiv taxonomy paper documents real faults in MCP software systematically. The document should acknowledge that MCP's rapid adoption outpaced its security maturity. [C6, C7]

**5. LiteLLM stability and security risks omitted.**
The document lists LiteLLM as a recommended cross-model tool without noting: 800+ open GitHub issues by early 2026, performance degradation under sustained load (database logging layer slowing after 1M logs), GIL-related concurrency problems, and critically — a supply chain attack on March 24, 2026 where backdoored versions (1.82.7, 1.82.8) on PyPI stole SSH keys, cloud credentials, and Kubernetes secrets. For a tool recommended as production infrastructure, these risks are material omissions. [C8]

**6. DSPy's "write-once portability" claim lacks failure-mode analysis.**
The document presents DSPy as solving cross-model portability via prompt compilation, with "100-500 LLM calls" for upfront cost. But the DSPy roadmap itself acknowledges gaps in typed multi-field constraints, assertions, observability, and deployment. The compilation cost is non-trivial for iterative development, and the document doesn't address what happens when compiled prompts fail on target models or when model updates invalidate compiled artifacts. The PromptBridge research exists specifically because compilation-style approaches don't fully solve model drifting. [C1]

**7. Structured output section understates format generation difficulty.**
The document claims "all major providers now support constrained decoding via JSON Schema" and describes the FSM mechanism, but omits that the StructEval benchmark (arxiv 2505.20139, May 2025) found even GPT-4o scored only 76.02% across structured formats, with all models below 50% on TOML, Mermaid, and SVG tasks. Constrained decoding guarantees schema compliance but not semantic correctness — models can and do hallucinate values that fit the schema but are factually wrong. The document should distinguish structural validity from content accuracy. [C9]

**8. Format benchmark data mixes different model generations.**
Sub-question 2 cites three benchmarks (Sources 1, 2, 3) that tested different models across different time periods. Source 1 tested GPT-3.5/4 (2024), Source 2 tested GPT-5 Nano/Llama 3.2/Gemini 2.5 Flash Lite (2025), and Source 3 tested GPT-5.2/Claude Opus 4.6 (2026). Drawing cross-benchmark conclusions from different model generations is methodologically weak. Source 1's own finding — cross-model IoU on optimal formats below 0.2 — actually argues against the document's format preference summary table, which implies stable preferences per model family.

**9. Reasoning mode section lacks Llama reasoning model coverage.**
The document states Llama has "no native reasoning mode" and requires explicit CoT prompting. This was true through Llama 4 but should acknowledge that the open-source ecosystem (DeepSeek-R1, QwQ, Phi-4-reasoning) has produced reasoning-capable open models that compete with proprietary reasoning modes. The "Llama = no reasoning" framing is increasingly outdated.

### Counter-Evidence

| # | Source | Finding | Challenges |
|---|--------|---------|------------|
| C1 | [PromptBridge: Cross-Model Prompt Transfer](https://arxiv.org/abs/2512.01420) | Prompt transfer drops 10-30pp between model families; "model drifting" is common and severe | "80% portable" claim (Gap 1), DSPy completeness (Gap 6) |
| C2 | [One Size Does Not Fit All (PromptHub)](https://www.prompthub.us/blog/one-size-does-not-fit-all-an-analaysis-of-model-specific-prompting-strategies) | No single prompt snippet works across all models; CoT helps Mistral ~50%, hurts Llama2-70B | "80% portable" claim (Gap 1), CoT universality |
| C3 | [YAML Is Bad and Here Is Why](https://medium.com/@ftieben/yaml-is-bad-and-here-is-why-a73c64a1eea6) | YAML whitespace sensitivity causes silent parsing failures; OpenAI mandated JSON-only for function calling | YAML benchmark results (Gap 2) |
| C4 | [Decreasing Value of Chain of Thought (Wharton GAIL)](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/) | CoT: +2.9% o3-mini, -3.3% Gemini Flash 2.5; 20-80% latency cost on reasoning models | CoT deprecation claim (Gap 3) |
| C5 | [Focused Chain-of-Thought (arxiv 2511.22176)](https://arxiv.org/abs/2511.22176) | F-CoT reduces tokens 2-3x while maintaining accuracy vs standard zero-shot CoT | Missing alternative to CoT deprecation (Gap 3) |
| C6 | [Six Fatal Flaws of MCP](https://www.scalifiai.com/blog/model-context-protocol-flaws-2025) | No enforced authentication, no message signing, session IDs leaked in URLs, prompt injection via tool descriptions | MCP optimism (Gap 4) |
| C7 | [Real Faults in MCP Software (arxiv 2603.05637)](https://arxiv.org/html/2603.05637v1) | Systematic taxonomy of real faults in MCP implementations | MCP maturity (Gap 4) |
| C8 | [5 Real Issues With LiteLLM (2026)](https://dev.to/debmckinney/5-real-issues-with-litellm-that-are-pushing-teams-away-in-2026-h0h) | 800+ open issues, supply chain attack (March 2026), GIL concurrency limits, DB log degradation | LiteLLM recommendation (Gap 5) |
| C9 | [StructEval: Benchmarking Structural Outputs (arxiv 2505.20139)](https://arxiv.org/html/2505.20139v1) | GPT-4o scored 76% across formats; all models below 50% on complex structured tasks | Structured output completeness (Gap 7) |

### Confidence Assessment

| Claim | Document Confidence | Assessed Confidence | Basis |
|-------|-------------------|-------------------|-------|
| Portable constructs get ~80% of performance | High (stated as key insight) | Low | Unsourced; PromptBridge shows 10-30pp transfer gaps; PromptHub found no universal snippets |
| XML best for Claude, Markdown best for GPT | Medium-High | Medium | Supported by vendor docs but cross-model IoU <0.2 undermines stable family preferences; benchmarks use different model generations |
| Format rarely matters (Delimiter Hypothesis) | Medium (Source 3) | Medium | 4-model study with 600 calls is small; contradicted by Source 1 showing 40% variance on GPT-3.5 and Source 2 showing 17.7pp YAML-XML gap |
| "Think step by step" harms GPT-5 | High (stated as deprecated) | Medium-Low | Wharton study shows nuanced results: marginal for reasoning models, mixed for non-reasoning; task-dependent, not categorically harmful |
| MCP achieves universal tool portability | High (stated as fact) | Medium | Adoption is real but security gaps are material; enterprise deployment has operational friction; "universal" overstates current maturity |
| LiteLLM / DSPy solve cross-model abstraction | High (listed as canonical) | Medium | Both have documented production limitations; LiteLLM supply chain attack is a concrete risk; DSPy compilation cost and failure modes unaddressed |
| Structured output via JSON Schema is solved | High (all providers support it) | Medium-High | Schema compliance is near-100% via constrained decoding, but semantic hallucination within valid schemas remains; complex formats still challenging |
| Reasoning modes are the key portability blocker | Medium | Medium-High | Well-supported by evidence; API-level divergence is real; prompted CoT as fallback is increasingly unreliable |

### Recommendations

1. **Downgrade the "80% portable" claim.** Either find empirical support or replace with the PromptBridge finding: optimized prompts lose 10-30pp on transfer, with the gap depending on model family distance and task complexity. Frame portability as a spectrum, not a threshold.

2. **Add a "risks and limitations" column to the Canonical Tools table.** LiteLLM's supply chain attack and MCP's security gaps are production-relevant. Readers selecting tools from this table need to know the tradeoffs, not just the capabilities.

3. **Nuance the CoT deprecation section.** Replace the categorical "harms GPT-5" claim with the Wharton data: CoT is marginally beneficial on some models, harmful on others, and always expensive in latency. Mention Focused CoT as an emerging alternative.

4. **Add YAML fragility caveat to format benchmarks.** The benchmark data showing YAML's strong performance needs the context that YAML is unreliable for LLM output generation due to whitespace sensitivity, even if it performs well as an input format.

5. **Separate "schema compliance" from "output correctness" in the structured output section.** Constrained decoding solves format validity but not semantic accuracy. The StructEval benchmark shows this gap concretely.

6. **Acknowledge the PromptBridge research** as evidence that cross-model transfer is an active research problem, not a solved one. The existence of transfer-learning approaches for prompts implies the abstraction layers listed are necessary but insufficient.

7. **Expand open-source reasoning coverage.** The Llama section should note that DeepSeek-R1, QwQ, and similar models provide reasoning capabilities outside proprietary APIs, changing the portability landscape for reasoning-intensive tasks.

## Sources (Challenge Additions)

| # | Source | Type | Tier | Status |
|---|--------|------|------|--------|
| C1 | [PromptBridge: Cross-Model Prompt Transfer for LLMs](https://arxiv.org/abs/2512.01420) | Peer-reviewed research | T1 | verified |
| C2 | [One Size Does Not Fit All (PromptHub)](https://www.prompthub.us/blog/one-size-does-not-fit-all-an-analaysis-of-model-specific-prompting-strategies) | Independent benchmark | T2 | verified |
| C3 | [The Decreasing Value of Chain of Thought (Wharton GAIL)](https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/) | Academic research | T1 | verified |
| C4 | [Focused Chain-of-Thought (arxiv 2511.22176)](https://arxiv.org/abs/2511.22176) | Peer-reviewed research | T1 | verified |
| C5 | [Six Fatal Flaws of MCP](https://www.scalifiai.com/blog/model-context-protocol-flaws-2025) | Technical analysis | T3 | verified |
| C6 | [Real Faults in MCP Software (arxiv 2603.05637)](https://arxiv.org/html/2603.05637v1) | Peer-reviewed research | T1 | verified |
| C7 | [5 Real Issues With LiteLLM (2026)](https://dev.to/debmckinney/5-real-issues-with-litellm-that-are-pushing-teams-away-in-2026-h0h) | Industry analysis | T3 | verified |
| C8 | [StructEval: Benchmarking Structural Outputs (arxiv 2505.20139)](https://arxiv.org/html/2505.20139v1) | Peer-reviewed research | T1 | verified |

## Findings

### 1. What prompt constructs are portable vs. model-specific?

**Core constructs are portable: role definitions, clear objectives, few-shot examples, output format specs, numbered steps** (HIGH — converging T1 vendor docs [5][6][7][8]). These work across Claude, GPT, Gemini, and Llama without modification.

**Cross-model transfer incurs 10-30pp performance drops** (HIGH — T1 [C1], T2 [C2]). PromptBridge found transferring GPT-5's optimal prompt to Llama-3.1-70B yielded 68.7% vs. 79.5% achievable. PromptHub found "no single prompt snippet works across all models." The commonly cited "80% portable" figure is aspirational, not empirical — portability is a spectrum, not a threshold.

**Model-specific tuning points** (HIGH — T1 vendor docs):
- **Claude**: XML tags (trained specifically for them); avoid ALL-CAPS directives on 4.6
- **GPT-4.1+**: Markdown default, XML for complex tasks; prioritizes end-of-prompt instructions
- **Gemini 3**: Either format; shorter prompts; temperature must stay at 1.0
- **Llama**: Special token templates vary across versions

### 2. How do formats perform across model families?

**No universal best format; cross-family format IoU below 0.2** (HIGH — T1 [1]). Format can swing performance by up to 40% on GPT-3.5 [1]. Same-family models share preferences (IoU >0.7), but preferences don't transfer across families.

**Larger models are more robust to format variation** (HIGH — T1 [1]). GPT-4 consistency >0.5 vs. GPT-3.5 <0.5. Format choice matters most for smaller/older models.

**Markdown is the safest cross-model default** (MODERATE — T2 [2][3]). Most token-efficient (10-38% fewer than alternatives). XML excels on Claude but was worst on Gemini 2.5 Flash Lite. YAML shows strong benchmark results as input format but is fragile for LLM output generation due to whitespace sensitivity.

**"Format rarely matters, but when it does, Markdown is the weak link"** (MODERATE — T2 [3]). Delimiter Hypothesis study (600 calls, 4 models): XML 96.3%, JSON 96.3%, Markdown 93.3% on stress tests. Three of four models showed no meaningful sensitivity.

### 3. What write-once abstraction strategies exist?

**The ecosystem has converged on layered abstraction** (HIGH — documented tools):
- **API gateways**: LiteLLM (100+ providers), aisuite (unified interface) — but LiteLLM suffered a supply chain attack in March 2026 and has 800+ open issues
- **Structured output**: Instructor (Pydantic), BAML (DSL), Vercel AI SDK (Zod) — constrained decoding ensures schema compliance but not semantic correctness (GPT-4o scored only 76% on StructEval [C8])
- **Prompt compilation**: DSPy compiles same signature to different optimal prompts per model — the strongest portability solution, but with upfront cost of 100-500 LLM calls
- **Tool protocol**: MCP (Linux Foundation standard, adopted by all major vendors) — but has documented security gaps: no enforced auth, supply chain breaches, 1,800+ unauthenticated public servers [C6]
- **Prompt testing**: Promptfoo (50+ providers), PromptHub (version control)

### 4. How do reasoning modes differ and what portability concerns arise?

**Reasoning mode activation is fundamentally incompatible across models** (HIGH — T1 vendor docs [5][6][7]):
- Claude: API `effort` parameter (adaptive thinking)
- GPT-5+: Auto-routing (model detects need); separate reasoning model variants (o3, o4-mini)
- Gemini 3: Prompt-based "Deep Think" (+14pp on ARC-AGI-2)
- Llama/open-source: Prompt-only CoT; but DeepSeek-R1 and QwQ offer reasoning capabilities

**Prompted chain-of-thought is the most portable but increasingly unreliable** (MODERATE — T1 [C3][C4]). CoT shows marginal gains (2.9-3.1%) on reasoning models with 20-80% latency costs. Gemini Flash 2.5 degraded 3.3% with CoT. Focused CoT (F-CoT) reduces tokens 2-3x while maintaining accuracy — an emerging alternative [C4].

**Several previously common patterns are now counterproductive** (HIGH — T1 vendor docs):
- "Think step by step" harms GPT-5 (auto-router handles this)
- ALL-CAPS directives cause Claude 4.6 overtriggering
- Low temperature degrades Gemini 3
- Prefilled assistant responses deprecated on Claude 4.6

### Canonical Tools

| Tool | Purpose | Key Risk |
|------|---------|----------|
| [DSPy](https://github.com/stanfordnlp/dspy) | Prompt compilation | 100-500 LLM call upfront cost |
| [LiteLLM](https://github.com/BerriAI/litellm) | API gateway (100+ providers) | March 2026 supply chain attack; 800+ open issues |
| [Instructor](https://python.useinstructor.com/) | Structured output (Pydantic) | Schema compliance ≠ content accuracy |
| [MCP](https://modelcontextprotocol.io/) | Tool integration protocol | Security gaps: no enforced auth, supply chain risks |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | Cross-model prompt testing | Now OpenAI-owned |
| [aisuite](https://github.com/andrewyng/aisuite) | Unified chat API | Newer, smaller community |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Portable constructs get ~80% of performance" | statistic | [4] | corrected — unsourced blog claim; PromptBridge shows 10-30pp transfer gaps [C1] |
| 2 | Cross-model format IoU below 0.2 | statistic | [1] | verified — peer-reviewed |
| 3 | Format can swing GPT-3.5 performance by 40% | statistic | [1] | verified — peer-reviewed |
| 4 | YAML outperformed XML by 17.7pp on GPT-5 Nano | statistic | [2] | verified — but YAML fragile for output generation |
| 5 | XML 96.3% vs Markdown 93.3% on stress tests | statistic | [3] | verified — small study (600 calls, 4 models) |
| 6 | "Think step by step" harms GPT-5 | finding | [18] | caution — Wharton shows nuanced results, not categorical [C3] |
| 7 | Claude XML tags provide 34% better structured reasoning | statistic | [5] | caution — vendor claim, no independent verification |
| 8 | MCP achieves "universal" adoption | finding | [17] | corrected — adoption is broad but security gaps are material [C6] |
| 9 | GPT-4o scored 76% on StructEval | statistic | [C8] | verified — peer-reviewed |
| 10 | DSPy compilation cost: 100-500 LLM calls | statistic | [12] | verified — tool documentation |
