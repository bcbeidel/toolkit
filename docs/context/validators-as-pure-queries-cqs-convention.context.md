---
name: "Validators as Pure Queries: CQS Convention"
description: "Validators should be pure query functions — observe and return issue lists, never mutate — while fix operations are separate explicit commands. CQS maps cleanly onto validation design as a code-level convention, not a structural constraint."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://martinfowler.com/bliki/CQRS.html
  - https://khalilstemmler.com/articles/oop-design-principles/command-query-separation/
  - https://openai.github.io/openai-agents-python/guardrails/
  - https://arxiv.org/html/2601.18827
related:
  - docs/context/composable-validators-stateless-accumulator-pattern.context.md
  - docs/context/structural-gates-llm-quality-checks.context.md
---
## Key Insight

Command-Query Separation (CQS) maps directly onto validation design. Validators are pure query functions: they observe state and return issue lists without mutating anything. Fix operations are separate explicit commands. This separation makes validators safe to run in CI, enables memoization and parallelization, and prevents accidental mutations during audit passes.

## The Mapping

Bertrand Meyer's original CQS principle: "every method should either be a command that performs an action, or a query that returns data to the caller, but not both."

In validation:
- **Validators (queries):** observe documents/artifacts, return `list[dict]` with keys `file`, `issue`, `severity`. No writes, no mutations, no side effects on the artifact under validation.
- **Fix operations (commands):** receive an artifact and explicit instruction to mutate it. Separate invocation path. Separate audit trail.

The OpenAI Agents SDK implements this cleanly: `GuardrailFunctionOutput` observes input/output and reports a `tripwire_triggered` boolean. The guardrail never mutates agent state — the orchestrator handles the mutation (halting execution) when the tripwire fires.

## Scope and Limits

The CQS mapping holds as design vocabulary and as an organizational convention. It breaks at two real-world boundaries:

**Audit log side effects:** Validators that write audit records technically violate pure CQS. The pragmatic rule (Ploeh 2015): validators should not mutate the artifact under validation, but may emit observability data. The client does not care about audit log side effects; what matters is that the artifact remains unchanged.

**Python provides no structural enforcement:** Nothing in Python prevents a "query" function from mutating state. CQS is a naming and code-review convention in this context, not a language-level constraint. The discipline must be maintained through review, not enforced by the type system.

For single-process developer tools (the common case for validators), full CQRS with separate read/write stores is unnecessary overhead. The value is the design vocabulary and the convention, not the infrastructure separation.

## Practical Application

- Name validators as observers: `check_frontmatter()`, `validate_urls()`, `audit_index_sync()` — not `fix_frontmatter()`.
- Name fix operations as commands: `reindex()`, `fix_frontmatter()` — functions that take an artifact and change it.
- Never mix validation logic with mutation logic in the same function.
- Validator return types should be consistent: `list[dict]` with `file`, `issue`, `severity` keys enables composability across the pipeline.

For agent-level validation via OpenTelemetry traces, the CQS principle is inherent: trace assertions observe span data and assert against it without modifying agent behavior. The test framework is a pure query on the trace record.

## Takeaway

Design validators as read-only reporters. They should be safe to run anywhere, at any time, without fear of side effects on the artifacts they examine. Fix operations earn a separate invocation path. The convention is worth enforcing through code review even without language-level guarantees.
