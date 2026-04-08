---
name: Effective Rule Anatomy
description: What structural characteristics make rules effective for LLM-based enforcement — specificity, examples, scope precision, and instruction limits
type: context
sources:
  - https://arxiv.org/html/2407.08440v1
  - https://arxiv.org/html/2503.23989v1
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/
  - https://www.techpolicy.press/using-llms-for-policy-driven-content-classification/
  - https://semgrep.dev/docs/writing-rules/rule-syntax
related:
  - docs/research/2026-04-07-effective-rules-for-llm-enforcement.research.md
  - docs/context/rule-system-pitfalls.context.md
  - docs/context/llm-rule-evaluation-reliability.context.md
---

Rules evaluated by LLMs succeed or fail based on four structural
characteristics. Getting these right improves enforcement reliability
by 4x; getting them wrong produces noise that erodes trust.

## Specificity Over Generality

Context-specific rules massively outperform generic ones. Cohen's Kappa
jumps from 0.156 to 0.646 when switching from generic to context-specific
rubrics for code evaluation. Repository-specific rules achieve up to
10.87% accuracy improvement compared to 5.19% for generic rules. A rule
scoped to `models/staging/**/*.sql` will produce far more reliable
judgments than one scoped to `**/*.sql`.

## Examples Are the Highest-Leverage Addition

3-5 few-shot examples dramatically improve classification accuracy.
Defining both compliant and non-compliant examples — with non-compliant
listed first — significantly reduces misclassification. Examples serve as
concrete anchors that disambiguate intent far more effectively than
additional prose. Semgrep enforces this: every contributed rule must
include at least one true positive and one true negative test case.

## Scope Precision Prevents Triggering Errors

LLM rule-following failures decompose into two types: triggering errors
(selecting the wrong rule for a context) and execution errors (correct
rule, wrong conclusion). Scope precision directly addresses triggering
errors by reducing the number of irrelevant rules the LLM must filter
through. Natural language rules outperform formal logic equivalents, but
performance degrades as irrelevant rules increase.

## Instruction Count Has Hard Limits

Frontier LLMs reliably follow approximately 150-200 instructions, with
performance declining uniformly as count increases. Claude Code's system
prompt already consumes roughly 50 instruction slots. This means rule
systems must avoid loading all rules into a single prompt. Scope-based
matching — evaluating only rules whose scope matches the target file —
is essential, not optional.

## Template Design Follows the Same Principles

Effective rule template libraries start small and conservative (Ruff
defaults to only two rule categories). Templates use the same format as
custom rules (dominant pattern across ESLint, Semgrep, OPA, ast-grep).
Organization follows flat categories by concern (naming, boundaries,
tests, docs), not deep hierarchies. Templates must be self-documenting:
intent explains why, examples show what, scope makes applicability
explicit.
