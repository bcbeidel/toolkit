---
name: Rule Testing and Validation Methodology
description: How to validate an LLM-evaluated rule before deploying it — two-polarity test structure, project-scale sample sizes (10–35), non-determinism handling via 3-run majority vote, two-gate acceptance criteria (warn then fail), and evaluator-first failure triage.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://eslint.org/docs/latest/integrate/nodejs-api#ruletester
  - https://semgrep.dev/docs/writing-rules/testing-rules/
  - https://arxiv.org/abs/2601.08654
  - https://docs.anthropic.com/en/docs/test-and-evaluate/eval-your-prompts
  - https://www.promptfoo.dev/docs/guides/evaluate-llm-consistency/
related:
  - docs/research/2026-04-13-rule-testing-validation.research.md
  - docs/context/rule-example-construction-methodology.context.md
  - docs/context/rule-library-operational-practices.context.md
---

# Rule Testing and Validation Methodology

## Key Insight

A rule without test cases cannot be verified before deployment. The two-polarity test structure (PASS cases + FAIL cases, borrowed from ESLint RuleTester and Semgrep's annotation model) is the minimum viable validation. Project-scale sample size is 10–35 cases — not the 100+ referenced in production monitoring literature. Non-determinism is handled by 3-run majority vote at temperature=0; SPLIT verdicts indicate under-specification in the rule, not evaluator error.

## Two-Polarity Test Structure

Each rule requires a co-located test file (`<slug>.tests.md`) with two sections:

**FAIL cases** — code that must trigger the rule. Each case needs:
- The code snippet
- Expected verdict: FAIL
- Rationale note: what specific element makes this a violation

**PASS cases** — code that must not trigger the rule. Each case needs:
- The code snippet
- Expected verdict: PASS
- Rationale note: what makes this compliant despite superficial similarity to a violation

Borrow from Semgrep's annotation pattern: use `# ruleid: <slug>` to mark lines that should be flagged, and `# ok: <slug>` to mark lines that should not. Use `# todo-ruleid: <slug>` to document known gaps without failing the test suite — planned coverage that the rule doesn't catch yet.

Test cases must be independent from the rule's own examples. The examples anchor the criterion; the test cases verify generalization.

## Project-Scale Sample Size

| Phase | Sample size | Gate |
|-------|-------------|------|
| Initial validation | 6–10 (3 PASS + 3 FAIL minimum) | Before warn-mode launch |
| Pre-deployment | 20–35 | Before fail-mode promotion |
| Production monitoring | 100+ | Ongoing; not a validation gate |

The "100 labeled examples" recommendation in LLM-as-judge operational literature targets production enforcement pipelines evaluating thousands of outputs — not a single project convention. Scale down accordingly. The minimum of 3+3 covers obvious cases; 20–35 adds borderline and known FP/FN candidates.

Distribution for 20–35 cases: 40% obvious (unambiguous PASS and FAIL), 40% borderline (reasonable disagreement possible), 20% known tricky (patterns that historically produce FP or FN).

## Handling Non-Determinism

**Temperature=0 + 3-run majority vote.** A single run misclassifies ~7.6% of borderline cases. Three majority-vote runs bring this below 5%.

**pass^k vs pass@k:**
- `pass^k` = must pass ALL k runs → use for enforcement gates (conservative)
- `pass@k` = pass at least once in k runs → use for coverage assessment (permissive)
- Never use pass@k to validate enforcement rules — it masks inconsistency

**SPLIT verdict (2 of 3 disagree):** flag as rule under-specification. Do not re-run. Clarify the criterion or add a borderline-case declaration before re-testing.

## Two-Gate Acceptance Criteria

**Gate 1 — Launch in warn mode:**
- TP rate ≥90% (rule catches real violations)
- TN rate ≥85% (rule doesn't fire on compliant code)
- Consistency ≥80% (majority vote agrees on ≥80% of cases)
- Human spot-check: review 5 borderline cases and confirm CoT reasoning is correct

**Gate 2 — Promote to fail mode:**
- TP rate ≥95%
- TN rate ≥90%
- Consistency ≥90%
- Human CoT spot-check: review 10 cases, confirm no reasoning errors
- Production FP rate <20% after ≥2 weeks in warn mode

**Post-deployment revision triggers:**
- Production FP rate >20% (regardless of test results — test distribution may not represent production)
- Rule fires on 0 cases in 30 days (stale or scope too narrow)
- Rule fires on 100% of cases in 30 days (scope too broad or criterion undefined)

## Failure Triage: Evaluator First

Most first-pass test failures come from evaluation setup issues, not wrong rules. Triage in this order:

1. **Evaluator issue (fix first):** Missing CoT requirement, no default-closed stance, rubric not presented holistically. Rerun with explicit CoT prompt — if consistency improves, the rule is fine.
2. **Example issue (fix second):** Ambiguous example, synthetic identifiers, too short. Substitute a different example for the same pattern — if consistency improves, the example was weak.
3. **Rule issue (fix last):** Criterion genuinely ambiguous, scope too broad, behavioral definition missing. Least common first-pass failure but hardest to fix.

## Takeaway

Write 6–10 co-located test cases (3 PASS + 3 FAIL) before launching a rule in warn mode. Run 3x at temperature=0; require majority-vote consistency. Apply Gate 1 before warn launch, Gate 2 before fail promotion. Triage failures evaluator-first — most are evaluation setup issues, not rule errors.
