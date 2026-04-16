---
name: Rule Example Construction Methodology
description: How to construct non-compliant and compliant examples for LLM semantic enforcement rules. Single canonical example from real failures outperforms multiple synthetic examples; evidence-anchored rubrics outperform pure-inference by +0.17 QWK. Non-compliant before compliant is required, not stylistic.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://arxiv.org/abs/2601.08654
  - https://arxiv.org/abs/2410.02185
  - https://arxiv.org/html/2503.23989v1
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://www.montecarlodata.com/blog-llm-as-judge/
  - https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/
related:
  - docs/research/2026-04-13-rule-example-construction.research.md
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/rule-testing-and-validation-methodology.context.md
---

# Rule Example Construction Methodology

## Key Insight

Examples are the primary anchor for LLM rule enforcement — not the criterion text. Without concrete examples, LLMs default to "pass: true," marking inadequate code as compliant. Evidence-anchored rubrics (examples that cite specific observable properties) outperform pure-inference rubrics by +0.17 QWK. A single well-constructed canonical example from a real failure outperforms multiple synthetic examples, which risk introducing conflicting signals.

## Non-Compliant Before Compliant (Required)

Listing the non-compliant (violation) example before the compliant (correct) example is a structural requirement, not a style preference. It exploits the primacy effect for the rejection case: the model evaluates what a violation looks like before seeing what correct code looks like. Reversing the order biases the model toward compliance by default. The research basis is the RULERS evidence-anchoring finding: establishing the negative case first improves evaluation accuracy.

## What Makes an Example "Real Enough"

Synthetic examples — those generated to illustrate a rule rather than extracted from actual failures — are weaker anchors. Real examples are stronger because they:
- Demonstrate failure modes that only appear in production code (not reasoned-up hypotheticals)
- Carry authentic identifier names, file paths, and surrounding context
- Have demonstrated coverage of the actual failure pattern

Signals that an example is "real enough" even if constructed:
- File path comment (`// src/api/handlers/user.ts`) identifying a plausible origin
- Non-generic identifiers (actual function names, real column names, domain-specific terminology)
- Surrounding context at realistic density (imports, function signatures, adjacent logic)

Signals that an example is weakly synthetic (flag for revision):
- Generic identifiers: `foo`, `bar`, `myFunction`, `data`, `result`
- No file path context
- Minimal surrounding code that couldn't realistically appear in a codebase

## When No Real Violating Code Exists Yet

For new conventions with no prior violations in the codebase, construct the non-compliant example to realistic density:
1. Use actual identifiers and structure from the codebase (copy from real files, then modify to introduce the violation)
2. Add a file path comment anchoring the example to a plausible location
3. Ensure the violation is the *only* difference from the compliant version — isolate the criterion

## Single Canonical Example Preferred

Research on few-shot prompting (Monte Carlo, POSIX arXiv 2410.02185) shows a single well-constructed example often outperforms multiple examples. Multiple examples can decrease consistency by introducing conflicting signals — especially if the examples illustrate different facets of the same violation. The goal is one maximally informative example per case, not comprehensive coverage of all violation patterns.

Exception: add a second non-compliant example only if a confirmed false positive has exposed a gap in the boundary definition. Each new false positive becomes a candidate for expanding the negative example set — do not pre-emptively add examples without evidence of a coverage gap.

## Example Independence from Test Cases

Rule examples (in the Non-Compliant and Compliant Example sections) anchor the evaluation criterion. Rule test cases (in co-located `.tests.md` files) verify the rule works. These must be different code snippets. Re-using the same code for examples and tests means the test is verifying recall of the anchors, not generalization of the criterion.

## Takeaway

Source the non-compliant example from a real failure or construct it to realistic density with a file path comment and domain identifiers. Pair it with a maximally similar compliant version that differs only on the criterion being tested. Lead with non-compliant. Use one canonical example; add a second only when a false positive exposes a coverage gap.
