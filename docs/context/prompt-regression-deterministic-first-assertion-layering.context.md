---
name: Prompt Regression — Deterministic-First Assertion Layering
description: "Regression pipelines should layer deterministic assertions (schema, regex, structure) before LLM-as-judge; judges have position bias, rubric order effects, and 100% instability on ambiguous items."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
  - https://github.com/promptfoo/promptfoo
  - https://www.traceloop.com/blog/automated-prompt-regression-testing-with-llm-as-a-judge-and-ci-cd
  - https://www.kinde.com/learn/ai-for-software-engineering/ai-devops/ci-cd-for-evals-running-prompt-and-agent-regression-tests-in-github-actions/
  - https://www.braintrust.dev/articles/what-is-prompt-management
related:
  - docs/context/prompt-immutable-versioning-and-attribution.context.md
  - docs/context/prompt-drift-types-and-detection-hierarchy.context.md
  - docs/context/llm-as-judge-biases-and-mitigations.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
---
# Prompt Regression — Deterministic-First Assertion Layering

Prompt regression pipelines should run deterministic checks before semantic checks. This is not a preference — it is a reliability requirement. LLM-as-judge has documented systematic biases that make it unsafe as the foundation of a regression system.

## LLM-as-Judge Failure Modes

Multiple independent sources document quantified unreliability:

- **Position bias**: LLMs select "Response B" 60–69% of the time in pairwise comparisons, far from the random 50% baseline
- **Rubric order effects**: A criterion evaluated last scores ~3.5% lower than when evaluated first; the same item scored 5.0/5 in isolation but 4.0/5 in holistic evaluation
- **Classification instability**: For ambiguous items, some models show 100% sensitivity to prompt template or category order changes — the same input classified differently every time the prompt changes
- **Fleiss' Kappa ~0.3** across multilingual tasks (ACL 2025 "Rating Roulette") vs. ~0.78 claimed in single-practitioner benchmarks

EvidentlyAI's practical guidance: "you will also need to check in on it regularly" as evaluator alignment drifts. LLM-as-judge is a practical tool when rubrics are carefully calibrated against human ground truth — it is not reliable infrastructure used naively.

## The Assertion Layering Pattern

Promptfoo implements this as four assertion types in order:

1. **Deterministic** — JSON schema validation, regex matching, structural invariants, required field presence. These are binary and reliable. Run first, block on failure.
2. **Semantic (LLM-as-judge)** — for outputs where deterministic checks are insufficient (tone, coherence, relevance). Use calibrated rubrics with human ground truth. Treat as soft signal, not hard gate.
3. **Safety** — content policy checks; often deterministic (keyword lists) combined with classifier models.
4. **Cost/latency** — token count thresholds, response time; track as regression signals independent of quality scores.

The key discipline: deterministic checks block the build; LLM-as-judge informs review but does not automatically block.

## CI/CD Integration Pattern

GitHub Actions trigger on path-filtered PRs (`prompts/**` or `promptfoo.config.yaml`). Failure conditions: any deterministic assertion failure or pass rate below threshold (≥95%) blocks the build gate. Braintrust posts score distributions as PR comments for human review before merge.

A curated golden dataset of 10–20 production examples covering critical cases and edge cases is the minimum viable evaluation corpus. Include cases that have regressed before — production failures are the highest-signal test cases.

**Latency and cost as regression signals (MODERATE):** Track both alongside quality scores. A prompt that produces higher-quality output at 3x the tokens may not be acceptable for production. Regression is not only quality degradation.

**The takeaway:** Deterministic assertions first, always. Build the evaluation pyramid the same way you build a testing pyramid: fast and reliable at the base, judgment-based at the top. LLM-as-judge is a complement to deterministic checks, not a replacement for them.
