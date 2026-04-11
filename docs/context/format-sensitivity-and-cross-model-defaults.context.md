---
name: "Format Sensitivity and Cross-Model Defaults"
description: "Format sensitivity is real (up to 40% swing); XML optimal for Claude, Markdown safest cross-model default"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2411.10541v1
  - https://www.improvingagents.com/blog/best-nested-data-format/
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
  - https://arxiv.org/html/2502.04295v3
  - https://systima.ai/blog/delimiter-hypothesis
related:
  - docs/context/portable-vs-model-specific-prompt-constructs.context.md
  - docs/context/prompt-design-principles-framing-and-emphasis.context.md
---
Format choice is not cosmetic. Prompt format can swing GPT-3.5 performance by up to 40% (Agrawal et al., NAACL 2025). Only 16% of responses were identical between Markdown and JSON formatting on MMLU with GPT-3.5. No universal best format exists — optimal format depends on both model and task.

## The Core Finding

Cross-model format preferences have near-zero overlap. Same-family models (e.g., GPT-3.5 variants) share format preferences with IoU > 0.7. Cross-series models drop below IoU 0.2 — format preferences do not transfer across model families. A format optimized for Claude will often hurt GPT or Gemini performance.

Larger models are more robust to format variation: GPT-4 shows consistency > 0.5 versus GPT-3.5's < 0.5. Format choice matters most for smaller or older models.

## XML: Optimal for Claude, Risky Elsewhere

Claude was specifically trained with XML tags as a prompt organizing mechanism. XML provides multi-line certainty with explicit open/close delimiters, better control for structured nested content, and unambiguous section boundaries. Claude parsing reliability for XML is the highest of any format.

However, XML is the worst-performing format on Gemini 2.5 Flash Lite and was outperformed by YAML by 17.7 percentage points on GPT-5 Nano. XML also uses approximately 80% more tokens than equivalent Markdown representations. The XML recommendation is Claude-specific and may actively harm performance on other models.

## Markdown: Safest Cross-Model Default

Markdown is the safest format for cross-model content:
- Most token-efficient: 10-38% fewer tokens than XML for equivalent content
- Broadest acceptable performance across model families
- For stress tests across four frontier models, format rarely mattered — and when it did, Markdown was the weak link (93.3% vs XML/JSON at 96.3%), but the gap is small for well-specified content

For Claude-specific deployments, use XML. For content deployed across multiple models, use Markdown.

## YAML: Strong Input, Fragile Output

YAML outperforms XML by 17.7 percentage points on GPT-5 Nano as an input format. But YAML is unreliable for LLM-generated output due to whitespace sensitivity — a single incorrect space changes meaning entirely. OpenAI mandated JSON-only for function calling precisely because YAML parsing errors are common in LLM outputs. YAML's strong benchmark numbers as an input format should not be extended to output generation.

## Format-Content Interaction

Different LLMs have distinct format preferences. Formats performing well on one model sometimes fail on another. Even within a single LLM, the optimal format varies by prompt content (Chen et al., 2025). One-size-fits-all formatting is unlikely to succeed at the margins.

Practically: test formats per model family, not per task type alone. The underlying model matters more than the task category for format selection.

## Prompt Brittleness

LLMs are sensitive to meaning-preserving changes — extra spaces, colon variations, and few-shot example ordering all affect output. This "prompt brittleness" is underappreciated and affects all formats. Statistical tests confirm format sensitivity is significant (p < 0.05) across tested models.
