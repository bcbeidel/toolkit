---
name: "Skill Behavioral Testing — Layer 2–3 Gap"
description: "Layer 2–3 of the eval stack (deterministic behavioral assertions + embedding similarity classifiers) is the highest-value unoccupied gap for WOS skill testing — cheap to run, catches failures structural linting misses, avoids LLM-as-judge's second non-determinism layer."
type: context
sources:
  - https://developers.openai.com/blog/eval-skills
  - https://www.evidentlyai.com/blog/llm-regression-testing-tutorial
  - https://arxiv.org/html/2508.13144v1
  - https://arxiv.org/html/2508.20737v1
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
related:
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
  - docs/context/skill-success-criteria-four-axes.context.md
  - docs/context/structural-gates-llm-quality-checks.context.md
  - docs/context/behavioral-testing-roi-and-investment-threshold.context.md
  - docs/context/skill-golden-dataset-perishability.context.md
---
# Skill Behavioral Testing — Layer 2–3 Gap

The highest-value unoccupied testing layer for WOS skills is Layer 2–3: deterministic behavioral assertions and embedding similarity classifiers. WOS currently has Layer 1 (structural linting). Layer 4 (LLM-as-judge) adds a second non-determinism layer and is expensive. Layer 2–3 fills the gap at low cost.

## The Four-Layer Eval Stack

| Layer | Check type | Cost | Catches |
|-------|-----------|------|---------|
| 1 | Structural linting (syntax, format, schema) | Cheap | Format failures, schema violations, instruction bloat |
| 2 | Code-based behavioral assertions (regex, keyword, JSON parse) | Cheap | Deterministic behavioral properties |
| 3 | Embedding similarity / classifier-based | Medium | Semantic drift, tone, toxicity |
| 4 | LLM-as-judge | Expensive | Nuanced quality (helpfulness, reasoning, style) |

Run Layer 1–2 on every change; Layer 3 on every PR; Layer 4 selectively before release on high-stakes skills.

## WOS Current State

WOS implements Layer 1: `wos/validators.py` checks frontmatter, word count, draft markers, URL reachability, related paths, index sync, project files, and skill quality metrics (ALL-CAPS density, instruction line count, SKILL.md body length, name format, description length). This catches structural failures reliably.

WOS has no Layer 2–3 coverage. A `test-skill` primitive that runs regex matching for required patterns and embedding similarity against golden outputs would occupy this gap.

## Why Layer 2–3 Over Layer 4

Layer 4 (LLM-as-judge) has two problems specific to skill evaluation:

1. **Second non-determinism layer.** Evaluating a non-deterministic artifact (a skill's outputs) with a non-deterministic evaluator (an LLM judge) compounds uncertainty. The same skill change can pass on one evaluation run and fail on the next — eroding confidence in the signal.

2. **Perishability.** WOS skills define behavior for Claude. LLM-as-judge scores against a golden dataset are calibrated against one model version. When Claude's model updates, the scores shift — not because the skill regressed, but because the judge's calibration shifted.

Layer 2–3 avoids both problems. Pre-trained classifiers (toxicity, sentiment, tone) and embedding cosine similarity provide deterministic-enough behavioral evaluation without invoking an LLM. A cosine similarity threshold of ≥0.9 against golden outputs detects meaningful semantic drift without LLM API calls. These checks are idempotent across model updates.

## Takeaway

The actionable recommendation: before investing in LLM-as-judge skill evaluation, implement Layer 2–3. Regex assertions on required structural patterns (does the output contain a ## Findings section? Does it reference at least one source?), word-count bounds, and embedding similarity against a small golden set of high-quality outputs provide substantial regression coverage at near-zero marginal cost per run.
