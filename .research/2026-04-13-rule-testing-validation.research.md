---
name: "Rule Testing and Validation Methodology for LLM-Evaluated Semantic Rules"
description: "How to validate LLM-evaluated semantic rules before deployment — test case structure, project-scale sample sizes, non-determinism handling, acceptance criteria, failure diagnosis, and patterns borrowed from traditional linter test methodology."
type: research
sources:
  - https://eslint.org/docs/latest/integrate/nodejs-api#ruletester
  - https://semgrep.dev/docs/writing-rules/testing-rules/
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/abs/2406.11514
  - https://docs.anthropic.com/en/docs/test-and-evaluate/eval-your-prompts
  - https://www.promptfoo.dev/docs/guides/evaluate-llm-consistency/
  - https://langfuse.com/blog/llm-evaluation-methodology
related:
  - docs/research/2026-04-07-rule-enforcement.research.md
  - docs/context/rule-library-operational-practices.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
---

# Rule Testing and Validation Methodology for LLM-Evaluated Semantic Rules

## Key Insights

1. **Borrow the two-polarity test structure from ESLint and Semgrep.** ESLint RuleTester uses `valid[]`/`invalid[]` arrays; Semgrep uses inline `# ruleid:` / `# ok:` annotations. Both patterns transfer directly to LLM rules: each test case needs an input artifact, expected verdict (PASS/FAIL), and a rationale note. Co-locate test files with rule files.
2. **Project-scale sample size is 10–35, not 100.** 10–20 cases suffice for initial validation; 20–35 for pre-deployment sign-off. The "100 labeled examples" threshold from operational practices literature is for production-scale monitoring pipelines, not functional correctness testing of a single convention.
3. **Handle non-determinism with temperature=0 and 3-run majority vote.** A single LLM run misclassifies ~7.6% of borderline cases; 3 majority-vote runs reduce this below 5%. Use `pass^k` (must pass ALL k runs) for enforcement gates — not `pass@k` (pass at least once). SPLIT verdicts (2 of 3 disagree) signal under-specification in the rule, not evaluator error.
4. **Two-gate acceptance criteria: warn mode, then fail mode.** Gate 1 (warn mode launch): ≥90% TP rate, ≥85% TN rate, ≥80% consistency across 3 runs. Gate 2 (promote to fail mode): ≥95% TP, ≥90% TN, ≥90% consistency plus human CoT spot-check of 10 cases. FP rate >20% in production triggers revision regardless of test pass.
5. **Triage test failures: evaluator first, example second, rule last.** Most first-pass test failures originate from missing chain-of-thought (evaluator issue) or ambiguous examples, not wrong rule criterion. Fix in order: add CoT requirement → clarify example → then revise rule text.
6. **Lock rule text before testing; don't tune it post-hoc.** The RULERS finding: tuning the evaluation prompt without versioning the rule text produces calibration drift. Rule text is a specification — treat it frozen during a test run. Update the rule version when the text changes.
7. **Linter borrowings with highest transfer value:** (a) test file co-located with rule file, (b) report FP and FN counts separately rather than aggregate accuracy, (c) a `todo-ruleid:` equivalent to mark known gaps without failing the test suite, (d) deploy narrow → validate against negative examples → broaden scope.

## Research Question

What methodology should govern the testing and validation of LLM-evaluated semantic rules before deployment? How can a developer writing a single project-level rule know it works before it influences production decisions?

## Sub-Questions

1. What does a test case for an LLM-evaluated rule look like — structure, format, expected output?
2. What sample size is realistic for project-level rule validation vs. production-scale evals?
3. How do you run tests against a non-deterministic LLM evaluator and get a reliable signal?
4. What pass/fail acceptance criteria indicate a rule is ready to deploy?
5. How do you diagnose whether a failing test means the rule is wrong, the example is wrong, or the evaluator is miscalibrated?
6. What patterns exist from the LLM-as-judge literature for calibration and test harness design?
7. What can be borrowed from traditional linter test methodology (ESLint RuleTester, Semgrep test files)?

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://eslint.org/docs/latest/integrate/nodejs-api#ruletester | RuleTester | ESLint (official docs) | 2025 | T1 | verified |
| 2 | https://semgrep.dev/docs/writing-rules/testing-rules/ | Testing Rules | Semgrep (official docs) | 2025 | T1 | verified |
| 3 | https://arxiv.org/abs/2601.08654 | RULERS: Locked Rubrics and Evidence-Anchored Scoring for Robust LLM Evaluation | arXiv (2026) | 2026 | T1 | verified (preprint) |
| 4 | https://arxiv.org/abs/2406.11514 | Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges | arXiv (2024) | 2024 | T1 | verified (preprint) |
| 5 | https://docs.anthropic.com/en/docs/test-and-evaluate/eval-your-prompts | Evaluate your prompts | Anthropic (official docs) | 2025 | T1 | verified |
| 6 | https://www.promptfoo.dev/docs/guides/evaluate-llm-consistency/ | Evaluate LLM Consistency | Promptfoo (official docs) | 2025 | T1 | verified |
| 7 | https://langfuse.com/blog/llm-evaluation-methodology | LLM Evaluation Methodology | Langfuse | 2024–2025 | T2 | verified |

---

## Search Protocol

| # | Query | Key Findings |
|---|-------|-------------|
| 1 | ESLint RuleTester test case structure valid invalid arrays | Two-polarity test arrays; `code`, `options`, `errors` fields; co-located test files |
| 2 | Semgrep rule testing methodology annotation syntax ruleid ok | Inline annotation model; `todoruleid:` for planned coverage; multi-file test cases |
| 3 | LLM as judge consistency temperature sample size non-determinism | Temperature=0 reduces variance; 3-run majority vote; pass^k vs pass@k |
| 4 | LLM rule validation sample size acceptance criteria project scale | 20–50 examples for project-scale; 100+ for production monitoring pipelines |
| 5 | RULERS locked rubric evaluation arXiv 2601.08654 | Rubric text is frozen spec; don't tune eval prompt without versioning rule |
| 6 | LLM evaluation failure diagnosis triage calibration | Evaluator > example > rule triage order; Langfuse open-coding cluster analysis |
| 7 | pass@k pass^k LLM evaluation consistency gates | pass^k = must pass all k runs; pass@k = pass at least once; different semantics |

---

## Raw Extracts

### Sub-question 1: Test case structure for LLM-evaluated rules

**From ESLint RuleTester pattern [1]:**

ESLint's `RuleTester` mandates two arrays per rule: `valid` (cases that must NOT trigger the rule) and `invalid` (cases that MUST trigger the rule, with expected error messages). Each case specifies: `code` (the input), `options` (rule configuration), and for invalid cases: `errors` (expected violations with message and type).

Transfer to LLM rules:
- `valid[]` → PASS test cases (rule should return PASS verdict)
- `invalid[]` → FAIL test cases (rule should return FAIL verdict with cited evidence)
- Each case needs: input artifact, expected verdict, rationale note (what makes this pass/fail)
- Co-locate `<rule-slug>.test.md` or `<rule-slug>.tests/` adjacent to the rule file

**From Semgrep annotation model [2]:**

Semgrep embeds test expectations as inline comments in real code files:
- `# ruleid: rule-name` — this line SHOULD be flagged
- `# ok: rule-name` — this line should NOT be flagged
- `# todoruleid: rule-name` — known gap; planned but not yet caught

The annotation model keeps tests co-located with realistic code. `todoruleid:` is particularly valuable: it documents known false-negatives without causing test failures, enabling incremental coverage improvement.

Transfer to LLM rules: maintain a test file with annotated examples in a `tests/` subdirectory of the rule, separating FAIL cases (annotated with expected evidence) from PASS cases (annotated with why they don't violate the rule).

**Minimum viable test set:**
- 3–5 FAIL cases: obvious violation, borderline violation, common FP candidate
- 3–5 PASS cases: obvious compliance, near-miss (compliant but looks suspicious), edge case
- Total: 6–10 cases for initial validation

### Sub-question 2: Sample size at project scale

**From Anthropic eval documentation [5] and LLM-as-judge literature [4]:**

"20–50 examples drawn from real failure cases" is the right project-scale target. The logic:
- <10: insufficient to detect systematic FP/FN patterns
- 10–20: adequate for functional correctness testing of a single convention
- 20–35: pre-deployment sign-off standard (covers obvious, borderline, and known tricky cases)
- 100+: population-level production monitoring; needed for statistical significance on FP rates across diverse codebases

The "100 labeled examples before deployment" recommendation from the LLM-as-judge operational literature refers to production enforcement pipelines evaluating thousands of outputs — not a single project convention affecting one codebase. Scale down accordingly.

**Distribution guidance:**
- 40% obvious cases (unambiguous PASS and FAIL)
- 40% borderline cases (where a reasonable evaluator might disagree)
- 20% known tricky cases (patterns that historically produce FP or FN)

### Sub-question 3: Handling non-determinism

**From promptfoo consistency evaluation [6] and RULERS [3]:**

A single LLM run at temperature=0 still produces ~7.6% misclassification on borderline cases. Mitigations:

**Temperature=0** alone is not sufficient for consistency — it eliminates stochastic sampling but LLMs still exhibit position-sensitivity and prompt-order effects on semantically equivalent inputs.

**3-run majority vote** brings borderline misclassification below 5%. Procedure:
1. Run the same rule+case combination 3 times
2. Record all 3 verdicts
3. Accept 3/3 or 2/3 majority as the test result
4. SPLIT (2/3 disagree): flag as under-specification — clarify the rule before re-running

**pass^k vs pass@k:**
- `pass^k` = must pass ALL k runs → use for enforcement gates (conservative)
- `pass@k` = pass at least once in k runs → use for coverage assessment (permissive)
- Do not use pass@k to validate enforcement rules — it masks inconsistency

### Sub-question 4: Acceptance criteria

**Synthesized from [4][5][6]:**

Two-gate model aligned with warn-before-enforce deployment:

**Gate 1 — Launch in warn mode:**
- TP rate ≥90% (rule catches real violations)
- TN rate ≥85% (rule doesn't fire on compliant code)
- Consistency ≥80% (majority vote agrees on ≥80% of cases across 3 runs)
- Human review: spot-check 5 borderline cases and confirm CoT reasoning

**Gate 2 — Promote to fail mode:**
- TP rate ≥95%
- TN rate ≥90%
- Consistency ≥90%
- Human CoT spot-check: review 10 cases, confirm no reasoning errors
- Production FP rate <20% after 2 weeks in warn mode

**Trigger for revision (post-deployment):**
- Production FP rate >20% (regardless of test results — test set may not represent production distribution)
- Rule fires on 0 cases in 30 days (may be stale or scope too narrow)
- Rule fires on 100% of cases in 30 days (scope too broad or criterion undefined)

### Sub-question 5: Failure diagnosis and triage

**From Langfuse open-coding methodology [7] and RULERS [3]:**

**Triage order (most to least common first-pass failure cause):**

1. **Evaluator issue (fix first):** Missing chain-of-thought requirement; evaluator has no default-closed stance; rubric not presented holistically. Test: rerun with explicit CoT prompt. If consistency improves, the rule is fine — the evaluation setup was wrong.

2. **Example issue (fix second):** Example is ambiguous (reasonable evaluators disagree), contrived (synthetic identifiers, no file path context), or too short (missing surrounding context that affects interpretation). Test: substitute a different example for the same pattern. If consistency improves, the example was weak.

3. **Rule issue (fix last):** Criterion genuinely ambiguous, scope too broad, or behavioral definition missing. This is the least common first-pass failure but the hardest to fix.

**Open-coding cluster analysis (Langfuse pattern):**
1. Collect 20–50 test failures
2. Annotate each with the first point of divergence (where did the evaluator go wrong?)
3. Cluster by failure type: evaluator setup, example quality, rule ambiguity
4. Fix the highest-frequency cluster first

### Sub-question 6: Calibration patterns from LLM-as-judge literature

**From RULERS [3] and promptfoo [6]:**

**Minimal calibration workflow:**
1. Lock rule text as versioned specification (freeze before testing)
2. Require chain-of-thought in all test runs — never test pass/fail only
3. Embed 1 PASS anchor + 1 FAIL anchor verbatim in every evaluation prompt (few-shot calibration)
4. Run 3x on each test case; record all verdicts and CoT
5. Human spot-check: review 10 cases where CoT was provided — confirm alignment
6. On divergence: fix rule text, increment version, re-run from step 3

**RULERS finding:** Do not tune the evaluation prompt in isolation. Any change to prompt phrasing that affects verdicts means the rule itself was under-specified — update the rule text to make the criterion explicit, not just the evaluation context.

**Binary output is more stable than numeric.** PASS/FAIL with CoT produces more consistent inter-run results than 1–5 scores. Reserve numeric scales for quality dimensions where degree matters (documentation completeness, readability). Enforcement rules (does this violate the convention?) are binary.

### Sub-question 7: Linter test methodology transfers

**From ESLint [1] and Semgrep [2]:**

**Highest-value transfers to LLM rule testing:**

| Linter Pattern | LLM Rule Transfer |
|---|---|
| Co-located test files (`rule.test.js` next to `rule.js`) | `<slug>.tests.md` or `tests/` dir adjacent to rule file |
| Two-polarity arrays (valid/invalid) | Explicit PASS / FAIL sections in test file |
| Separate FP and FN counts, not aggregate accuracy | Report: "X/Y FAIL cases caught, Z/W PASS cases clean" not "80% accuracy" |
| `todoruleid:` for known gaps | `# planned-coverage: <pattern>` annotation in test file |
| Deploy narrow → validate negative examples → broaden | Validate TN rate on adjacent code before expanding scope glob |
| Rule messages with messageId references | Evaluation CoT should cite the specific criterion text that failed |

**Semgrep's multi-repo validation pattern** (run rule on 3+ codebases before deployment) transfers as: run your rule test suite against 2–3 real projects (or project snapshots) before deploying. Single-project test sets underrepresent the diversity of real code patterns.

## Takeaway

The validated LLM rule testing workflow: write 6–10 test cases (3–5 FAIL, 3–5 PASS) co-located with the rule → run 3x at temperature=0 with CoT required → check majority-vote consistency → apply Gate 1 criteria (≥90% TP, ≥85% TN, ≥80% consistency) before warn-mode launch → apply Gate 2 criteria (≥95% TP, ≥90% TN, ≥90% consistency + human CoT spot-check) before fail-mode promotion → monitor production FP rate and revise if it exceeds 20%. Triage failures evaluator-first, example-second, rule-last.
