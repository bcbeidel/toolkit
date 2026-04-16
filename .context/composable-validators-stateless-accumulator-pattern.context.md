---
name: "Composable Validators: Stateless Check Functions and Shared Accumulator"
description: "The canonical validation pipeline pattern uses stateless check functions that return issue lists, composed via a shared result accumulator — not fail-fast chaining."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://eslint.org/docs/latest/contribute/architecture/
  - https://fsharpforfunandprofit.com/rop/
  - https://arxiv.org/html/2603.07019
  - https://oneuptime.com/blog/post/2026-01-25-data-validation-framework-python/view
related:
  - docs/context/structural-gates-llm-quality-checks.context.md
  - docs/context/validators-as-pure-queries-cqs-convention.context.md
  - docs/context/validation-severity-tiers-and-confidence-decoupling.context.md
---
## Key Insight

Composable validation pipelines share a single design pattern across every mature tool: stateless check functions that return issue lists, merged into a shared result accumulator. This collects all errors rather than stopping at the first failure. ESLint, Railway Oriented Programming, and AutoChecklist (arXiv 2026) all independently converge on this pattern.

## The Pattern

Each check function:
- Takes input and context
- Returns zero or more issue objects (never mutates input)
- Is independently testable in isolation

A pipeline composes checks by running each function and merging results:

```python
result = ValidationResult()
for check in checks:
    result = result.merge(check.validate(value, context))
```

This produces a complete issue list from a single pass rather than a partial list truncated at the first failure.

## Three Convergent Implementations

**ESLint rule model (T1 official docs):** Rules are stateless. They attach to AST traversal events and emit issues into a shared result list. No direct file system access or async operations are permitted. The CLI, CLIEngine, and Linter are layered — CLI handles I/O; Linter performs verification with no side effects. This makes the core independently testable and programmatically embeddable.

**Railway Oriented Programming (ROP):** Provides the theoretical foundation for collecting all errors rather than failing fast. The `Sequence` method accumulates all individual failures. The `&&&` operator applies multiple validators logically in parallel on the same input, checking multiple fields simultaneously without coupling their failure modes. ROP's constraint — one uniform composition pattern — enforces consistency across a pipeline at scale.

**AutoChecklist (arXiv Mar 2026, U. Chicago):** Applies the same composability to LLM-based quality checks: Generator → Refiner → Scorer, where any generator pairs with any scorer, and refiners compose in sequence. New configurations register via Markdown prompt templates without modifying library code. This demonstrates that quality-check pipelines can be as composable as structural-check pipelines.

## Design Constraints That Make It Work

For composability to hold, each check function must:
1. Be stateless — no internal state carried between invocations
2. Accept context explicitly as a parameter (not via global state)
3. Return structured issue objects (file, issue, severity) — not raise exceptions
4. Not modify the artifact under validation

ESLint enforces these constraints architecturally: rules cannot access the file system or perform async operations. In Python, the constraints are conventions — code review is the enforcement mechanism.

## When to Fail Fast

The composable accumulator pattern applies within a severity tier. Structural failures (Tier 1) should still short-circuit LLM-quality checks (Tier 2) — see the structural gates pattern. Within a single tier, accumulate all issues rather than stopping at the first one. This gives callers a complete picture of what needs fixing rather than requiring iterative reruns.

## Takeaway

Write each validator as a pure function returning a list. Compose by merging lists. The ESLint rule model is the canonical reference. ROP provides the theoretical grounding for why accumulation is superior to fail-fast for validation use cases. Never mix validation logic with mutation logic in the same function.
