---
name: "Structural Gates on LLM Quality Checks"
description: "Deterministic structural checks should run first and short-circuit expensive LLM-quality checks on structural failure, saving cost and preventing garbage input from reaching LLM evaluators."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.hebbia.com/blog/evaluating-ai-agents-a-hybrid-deterministic-and-rubric-based-framework
  - https://github.com/mlflow/mlflow/issues/20827
  - https://arxiv.org/html/2601.18827
  - https://openai.github.io/openai-agents-python/guardrails/
related:
  - docs/context/composable-validators-stateless-accumulator-pattern.context.md
  - docs/context/validation-severity-tiers-and-confidence-decoupling.context.md
  - docs/context/validators-as-pure-queries-cqs-convention.context.md
---
## Key Insight

Structural checks should run before LLM-quality checks in validation pipelines. When structural validation fails, there is no point invoking an LLM evaluator — the output is malformed and the semantic judgment would be meaningless. Gating on structural failure eliminates a significant portion of LLM API calls at zero quality cost.

## How It Works

A two-tier pipeline separates concerns by cost and determinism:

**Tier 1 — Structural (deterministic):** Schema validation, required field presence, data type correctness, format compliance. These run in microseconds, produce identical results on every run, and require no LLM API calls. Canonical implementations include Pydantic BaseModel enforcement (Guardrails AI), regex matching, length bounds, and JSON validity checks.

**Tier 2 — Quality (LLM-driven):** Semantic properties like coherence, completeness, and domain-appropriateness. These are expensive, non-deterministic, and produce meaningful results only when given structurally valid input.

The `gate=True` mechanism proposed in MLflow's Tier 1 scorer design short-circuits Tier 2 evaluation on any Tier 1 failure. The cost argument is concrete: at 1,000 evaluation rows with five LLM judges, even a modest structural failure rate eliminates a meaningful fraction of API calls per run.

For agent testing, the same separation applies at the trace level. Structural assertions via OpenTelemetry spans verify tool invocations, parameter passing, and execution sequences without touching semantic content. "No need to test the agent's text response, since we test if right tools were invoked" (arXiv structural testing paper).

## Where the Ordering Inverts

The structural-first rule holds for single-schema output validation. It inverts in multi-schema routing contexts: when a lightweight LLM classifier must first determine which schema applies before any structural check can run, the LLM call necessarily precedes structural validation. The two-tier model holds; only the execution order flips for that routing step.

## Canonical Implementations

- **Guardrails AI**: Pydantic BaseModel for structural validation; installable validators for semantic checks. Guard composes both and surfaces a `validation_passed` boolean.
- **OpenAI Agents SDK**: Input guardrails gate output guardrails. Structural checks prevent downstream semantic evaluators from running on invalid inputs.
- **ESLint**: Parse errors short-circuit rule-level checks. If the AST cannot be built, no linting rules run.

## Takeaway

Design validation pipelines as two tiers with an explicit gate. Invest in complete Tier 1 coverage before adding LLM evaluators. A 20% structural failure rate caught before LLM evaluation reduces both cost and noise in quality signals. The gate is a correctness mechanism as much as a cost mechanism — LLM judges on malformed output produce unreliable results regardless of their calibration.
