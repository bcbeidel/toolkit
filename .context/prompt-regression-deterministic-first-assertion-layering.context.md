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
  - https://www.evidentlyai.com/blog/llm-regression-testing-tutorial
  - https://arxiv.org/abs/2601.22025
related:
  - docs/context/prompt-immutable-versioning-and-attribution.context.md
  - docs/context/prompt-drift-types-and-detection-hierarchy.context.md
  - docs/context/llm-as-judge-biases-and-mitigations.context.md
  - docs/context/rubric-specificity-and-deterministic-first-evaluation.context.md
  - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
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

## Handling Non-Determinism in Assertions

Exact-match testing is not viable for LLM outputs. No framework uses it. The consensus approach has three components:

1. **Statistical aggregation** — run multiple samples, aggregate, apply threshold (e.g., "95% pass rate across N runs") rather than binary per-run pass/fail. A single failing run is not a regression signal; a sustained rate drop is.
2. **Semantic similarity** — cosine similarity on embeddings (threshold ≥ 0.9) replaces string equality for output comparison. Pre-trained classifiers (toxicity, sentiment, tone) handle specific behavioral properties without LLM overhead — avoiding the second non-determinism layer.
3. **Acceptable failure tolerance** — define expected score ranges rather than requiring zero failures. Statistical drift detection over time is more reliable than single-run pass/fail.

Temperature=0 is insufficient alone — it reduces variance but does not eliminate it, and produces artificially narrow test coverage. Treat temperature control as a noise-reduction measure, not a determinism guarantee.

## The Eval-Overfitting Failure Mode

Eval-driven prompt iteration can improve aggregate scores while masking category-specific regressions — a failure mode structurally identical to what behavioral testing is meant to prevent.

The "When Better Prompts Hurt" paper (arxiv 2601.22025) demonstrated this concretely: replacing task-specific prompts with generic rules on Llama 3 8B degraded extraction accuracy by 10% and RAG compliance by 13%, while appearing as an aggregate improvement against the tested golden set. The aggregate score improved; the targeted task regressed. This is eval overfitting: the optimization pressure from iterating on a fixed test suite causes the prompt to fit the test distribution rather than the real use distribution.

The practical implication: rotating golden datasets, maintaining holdout sets, and auditing the eval suite itself are necessary governance mechanisms for any sustained eval-driven prompt development workflow. Treating eval scores as the sole quality signal creates the silent regression problem it was designed to prevent.
