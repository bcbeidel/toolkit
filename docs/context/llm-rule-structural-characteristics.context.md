---
name: LLM Rule Structural Characteristics
description: "Four structural requirements for reliable LLM rules — specificity, scale matching, scope isolation, and behavioral anchoring — and why a full rubric outperforms sequential evaluation."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://aclanthology.org/2025.coling-main.710.pdf
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/html/2503.23989v1
  - https://arxiv.org/html/2501.00274v1
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
related:
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/rule-library-operational-practices.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
---
# LLM Rule Structural Characteristics

## Key Insight

Single holistic LLM judgment is near-unusable (RMSE 0.856–0.901 — worse than random guessing). Every effective LLM rule depends on four structural properties: specificity, scale matching, scope isolation, and behavioral anchoring. Rules that lack any one of these degrade to noise.

## The Four Structural Requirements

**1. Specificity — define terms explicitly**

Vague instructions produce variable interpretations. "Don't just ask the LLM to label something as 'toxic' or 'not toxic' — clearly define what 'toxic' means." More granular criteria directly predict inter-evaluator agreement. Question-specific rubrics outperform question-agnostic ones by ~4× on Cohen's Kappa (QS = 0.646 vs. QA = 0.156).

**2. Scale matching — match the scale to the distinction type**

- Binary for categorical distinctions (toxic/not-toxic, pass/fail). Binary scales are the most reliable and consistent.
- Ordinal 1–5 for quality dimensions. Easier to build rubric anchors around than 1–100.
- Float/continuous only for benchmarking generation tasks.
- Never use 1–100 for LLM evaluation. "If you can't easily explain these distinctions, simplify the scale."

**3. Scope isolation — one dimension per evaluator**

"If you have several aspects to evaluate — completeness, accuracy, relevance — split them into separate evaluators." Do not combine multiple evaluation dimensions into one prompt. Decomposing a holistic judgment into 8 specific dimensions improves performance 2× (RMSE improved from 0.86 to 0.39–0.42 in controlled study).

**4. Behavioral anchoring — concrete examples at each scale point**

Rubric text must anchor each scale point with observable behavior. Example: "Score 0.1: Only a slight smile. Score 0.5: Laughing out loud. Score 1.0: Rolling on the floor laughing." Without anchors, models default to assuming pass:true, marking inadequate responses as passing.

## Why Full Rubric Outperforms Sequential Evaluation

When evaluating a complete rubric simultaneously (vs. criterion-by-criterion), human-aligned results improve. Presenting evaluation points one at a time makes the model "remarkably strict" (leniency score −0.329). Presenting the full rubric simultaneously yields more calibrated evaluations. Granularity of presentation matters, not just criterion count.

The RULERS framework — compiling natural language rubrics into versioned, immutable bundles with deterministic evidence verification — outperforms pure inference prompts by +0.17 QWK. Rule-compiling enables smaller models to rival larger proprietary judges, suggesting that rubric structure matters more than model size.

## Takeaway

Design rules as versioned specifications with four properties: explicit term definitions (specificity), matched scale types (scale matching), one criterion per evaluator (scope isolation), and anchored score points (behavioral anchoring). Present the full rubric simultaneously. Treat rubric text as a frozen artifact — minor phrasing changes produce meaningfully different evaluation results.
