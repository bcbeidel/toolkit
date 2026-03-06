---
name: LLM Prompt Structuring Format Preferences by Vendor
description: >
  Which prompt structuring formats (XML, YAML, Markdown, JSON) perform best
  for each major LLM vendor, based on vendor documentation and independent
  benchmarks.
type: research
sources:
  - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/use-xml-tags
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
  - https://ai.google.dev/gemini-api/docs/prompting-strategies
  - https://www.llama.com/docs/how-to-guides/prompting/
  - https://www.improvingagents.com/blog/best-nested-data-format/
  - https://arxiv.org/abs/2411.10541
related:
  - skills/refine-prompt/references/technique-registry.md
---

# LLM Prompt Structuring Format Preferences by Vendor

## Bottom Line

Format choice affects LLM accuracy by up to 17.7 percentage points depending
on model and task. No single format is universally best. The mapping below
reflects vendor documentation and independent benchmarks.

| Vendor | Recommended format | Fallback | Avoid | Confidence |
|--------|-------------------|----------|-------|------------|
| Anthropic (Claude) | XML tags | Markdown headers | — | HIGH |
| OpenAI (GPT) | Markdown headers | XML tags | JSON for documents | HIGH |
| Google (Gemini) | XML tags or Markdown | Either works | — | MODERATE |
| Meta (Llama) | Markdown + XML | Markdown headers | — | MODERATE |
| Multi-model | Markdown headers | YAML in code fences | XML tags | HIGH |

## Findings

### 1. Anthropic (Claude): XML tags preferred

Claude was specifically trained to recognize XML tags as prompt organizing
boundaries. Anthropic's official documentation recommends wrapping distinct
sections in descriptive XML tags (`<instructions>`, `<context>`, `<input>`)
and nesting tags when content has natural hierarchy.

**Key claims:**
- XML tags provide "up to 40% quality improvement on complex prompts"
  (Anthropic Tier 1 documentation)
- Examples should be wrapped in `<example>` / `<examples>` tags
- Documents should use `<document>` with `<document_content>` and `<source>`
  subtags

**Source tier:** Tier 1 (vendor documentation) — HIGH confidence.

### 2. OpenAI (GPT): Markdown preferred, XML acceptable

OpenAI's GPT-4.1 prompting guide recommends starting with Markdown:
"markdown titles for major sections and subsections (including deeper
hierarchy, to H4+)." XML is noted as performing well too, particularly for
precisely wrapping sections with start/end boundaries.

JSON "performed particularly poorly" for document collections in OpenAI's
long-context testing.

**Benchmark data (He et al., arXiv:2411.10541):**
- GPT-4: Markdown 81.2% vs JSON 73.9% on MMLU
- GPT-3.5: JSON 59.7% vs Markdown 50.0% on MMLU
- Conclusion: "no universally optimal format, even within the same
  generational lineage"

**Source tier:** Tier 1 (vendor cookbook) + Tier 2 (peer-reviewed) — HIGH
confidence.

### 3. Google (Gemini): Format-agnostic, consistency matters

Google's Gemini documentation recommends both XML-style tags and Markdown
headings equally. The key principle is consistency: "Choose one format and
use it consistently within a single prompt."

No comparative performance metrics between formats are provided. Google
emphasizes structural clarity over format superiority.

**Source tier:** Tier 1 (vendor documentation) — MODERATE confidence (no
comparative data).

### 4. Meta (Llama): Markdown + XML hybrid

Meta's documentation recommends "Markdown + XML for structure" with system
prompt as the primary control mechanism. Llama models support prefilled
output structure (starting responses with opening characters).

**Benchmark data (ImprovingAgents, Llama 3.2 3B Instruct):**
- JSON: 52.7%, XML: 50.7%, YAML: 49.1%, Markdown: 48.0%
- Formats performed similarly, with slight JSON edge

**Source tier:** Tier 1 (vendor docs) + Tier 3 (industry benchmark) —
MODERATE confidence.

### 5. Independent benchmarks

**ImprovingAgents Nested Data Format Benchmark (2024):**

| Model | YAML | Markdown | JSON | XML |
|-------|------|----------|------|-----|
| GPT-5 Nano | 62.1% | 54.3% | 50.3% | 44.4% |
| Llama 3.2 3B | 49.1% | 48.0% | 52.7% | 50.7% |
| Gemini 2.5 Flash Lite | 51.9% | 48.2% | 43.1% | 33.8% |

Key takeaway: XML consistently underperformed on non-Claude models. YAML
performed best on GPT and Gemini. Llama showed minimal format sensitivity.

**He et al. "Does Prompt Formatting Have Any Impact on LLM Performance?"
(arXiv:2411.10541, Nov 2024):**

Tested Plain Text, Markdown, YAML, JSON across six benchmarks on GPT-3.5
and GPT-4. Found up to 40% performance variation on code translation tasks
depending on format. Larger models (GPT-4) showed greater robustness to
format variation but still measurable differences.

### 6. Token efficiency

Markdown requires approximately 34-38% fewer tokens than JSON across
models (ImprovingAgents). XML requires approximately 80% more tokens than
Markdown for equivalent data. YAML falls between Markdown and JSON.

For cost-sensitive applications, Markdown is the most token-efficient
structured format.

## Multi-model recommendation

When a prompt will be used across multiple models or the target model is
unknown:

1. **Use Markdown headers** (`#`, `##`) for section boundaries
2. **Use fenced code blocks** for structured data (YAML preferred over JSON)
3. **Avoid XML tags** — they are Claude-optimized but underperform on GPT
   and Gemini

This sacrifices some Claude-specific optimization for broad compatibility.

## Challenge

**Assumptions tested:**
- "XML is always best for Claude" — True per vendor docs, but the margin
  depends on prompt complexity. Simple prompts see no benefit.
- "One format fits all" — False. Format preference varies by vendor, model
  size, and task type.
- "Format doesn't matter for large models" — Partially true. GPT-4 is more
  robust than GPT-3.5, but still shows measurable differences.

**Limitations:**
- ImprovingAgents benchmark tested nested data retrieval, not prompt
  structuring specifically. Results may not transfer directly.
- He et al. tested GPT-3.5 and GPT-4 (older models). Current GPT-5 family
  may behave differently.
- No direct Claude benchmark data in either study — Claude recommendation
  relies on vendor documentation only.
- Gemini lacks published format comparison data.

## Search Protocol

| # | Query | Source | Result |
|---|-------|--------|--------|
| 1 | Anthropic Claude XML tags prompt structuring best practices | WebSearch | Vendor docs confirming XML preference |
| 2 | OpenAI GPT prompt structuring format best practices markdown JSON | WebSearch | GPT-4.1 guide recommending Markdown |
| 3 | Google Gemini prompt structuring format recommendations | WebSearch | Format-agnostic, consistency-focused |
| 4 | Meta Llama prompt format structuring best practices | WebSearch | Markdown + XML hybrid recommended |
| 5 | ImprovingAgents nested data format benchmark | WebSearch + WebFetch | Full accuracy table by model/format |
| 6 | Prompt formatting impact LLM performance arxiv | WebSearch + WebFetch | He et al. benchmark data |
