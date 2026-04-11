---
name: "Validation Severity Tiers and Confidence Decoupling"
description: "Mature validation tools converge on three severity tiers (fail/warn/info), require active warn enforcement to prevent fatigue, and treat severity and confidence as separate dimensions — a conflation that causes fail-tier erosion."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://rustc-dev-guide.rust-lang.org/diagnostics.html
  - https://docs.greatexpectations.io/docs/reference/api/core/expectationsuitevalidationresult_class/
  - https://semgrep.dev/docs/kb/rules/understand-severities
  - https://www.hebbia.com/blog/evaluating-ai-agents-a-hybrid-deterministic-and-rubric-based-framework
  - https://arxiv.org/abs/2503.05965
related:
  - docs/context/structural-gates-llm-quality-checks.context.md
  - docs/context/composable-validators-stateless-accumulator-pattern.context.md
  - docs/context/validators-as-pure-queries-cqs-convention.context.md
---
## Key Insight

Mature developer tools converge on three severity tiers: **fail** (blocks execution), **warn** (accumulates for report), **info/note** (context-only, no action required). The minimum viable model is fail + warn. A critical design distinction separates severity (how bad is this?) from confidence (how certain are we?) — conflating them is a documented cause of fail-tier erosion and trust loss.

## The Three-Tier Convergence

**Rust diagnostics (T1):** Error (blocks compilation), Warning (informational but actionable), Note (contextual support), Help (actionable fix suggestions). The lint subsystem adds a configurable enforcement layer — Forbid/Deny/Warn/Allow — separating policy from hard errors. The design goal: reserve warnings for situations "where the user should take action" or code that is "very likely to be incorrect."

**Great Expectations (T1):** Critical > Warning > Info with explicit ordering. Execution failures always escalate to Critical regardless of configured severity. The `get_max_severity_failure()` method enables threshold-based gating: block on Critical, report on Warning, log Info.

**Semgrep (T1):** Critical, High, Medium, Low. A **separate confidence dimension** (distinct from severity) captures the rule's accuracy and false-positive characteristics. This explicitly prevents conflating "how bad is this?" with "how certain are we?" — the most important design choice Semgrep makes.

## The Warn Tier Trap

The warn level is the intended escape valve for alert fatigue. In practice, it is itself a documented source of fatigue if not actively enforced. Thomas Junghans's widely-cited ESLint analysis finds warnings are routinely ignored, recommending `error` or `off` only — never unmanaged `warn`.

The mitigation is active enforcement:
- ESLint: `--max-warnings 0` (zero warning tolerance in CI)
- Rust: `#[deny(warnings)]` (promotes all warnings to errors)
- dbt: `warn_if` / `error_if` thresholds (graduated enforcement)

Without an enforcement gate, warn becomes a category developers are conditioned to ignore. The tier's value depends entirely on the enforcement policy around it.

## Severity vs. Confidence: The Critical Distinction

Semgrep explicitly separates these dimensions. The failure mode of conflation: a high-severity but low-confidence finding that blocks CI. A check that fires often when it is wrong erodes trust in the entire system, leading teams to disable or ignore the blocking tier.

For deterministic validators, severity and confidence are correlated (if the check fires, it is certain). For LLM-based checks, they decouple sharply — an LLM judge may assess high severity while the assessment itself is unreliable.

Research evidence (arXiv 2503.05965) finds that forcing LLM judges to assign fixed severity labels is systematically biased — selecting judge systems that perform up to 31% worse than alternatives. For LLM-based quality checks, the appropriate model is either: (1) Hebbia's required/additional binary (required = SLA, additional = aspirational quality); or (2) confidence-threshold scoring rather than severity tiers.

## Practical Design Recommendations

For deterministic validators: use 3 tiers (fail / warn / info). Set an explicit warn enforcement gate in CI. Never let warns accumulate without a threshold.

For LLM-based quality checks: do not apply traditional severity tiers. Use required/additional binary or confidence-threshold scoring. The non-determinism of LLM evaluators makes fixed severity assignment unreliable.

## Takeaway

Three tiers is the right structure for deterministic validation. Keep severity and confidence as separate fields — never combine them into a single score. Enforce warn tiers or they become noise. LLM-based checks need a different severity model entirely: binary (required/additional) or threshold-based, not tiered.
