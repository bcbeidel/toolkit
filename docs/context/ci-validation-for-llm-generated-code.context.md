---
name: CI Validation for LLM-Generated Code
description: "LLM-generated code requires non-functional CI checks beyond unit tests — CodeQL at repo scope, runtime/memory tracking (patches avg 64% slower, 89% higher peak memory), and weighted severity scoring."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2511.10271v1
  - https://docs.github.com/en/code-security/code-scanning/integrating-with-code-scanning/sarif-support-for-code-scanning
  - https://github.com/github/codeql-action
related:
  - docs/context/precommit-hooks-vs-ci-enforcement-boundary.context.md
  - docs/context/quality-ratchet-pattern-for-gradual-enforcement.context.md
  - docs/context/agent-driven-ci-guardrails-and-confidence-routing.context.md
  - docs/context/agent-generated-code-security-patterns.context.md
---
# CI Validation for LLM-Generated Code

## Key Insight

Functional tests pass for LLM output that contains security vulnerabilities and performance regressions. Standard CI pipelines treating LLM output like human output accumulate technical debt faster. Three additional checks are required: CodeQL at repository scope, runtime and peak memory tracking, and weighted severity scoring (MODERATE — core concern is valid; headline statistics are from narrow benchmarks).

## The Quality Gap

A November 2025 arXiv study evaluated LLM-generated patches across functional correctness, security, and performance dimensions. Functionally correct patches from LLMs still triggered substantial CodeQL violations: 7–9 error-level violations and 58–64 recommendation-level violations per model evaluated (GPT-4o: 8 error, 64 recommendation; DeepSeek: 9 error, 59 recommendation; Claude Sonnet: 7 error, 58 recommendation).

Performance efficiency is also degraded: LLM patches averaged 23.27s runtime and 44.54 MB peak memory versus 14.26s and 23.50 MB for human-written reference patches. That is ~64% longer runtime and ~89% higher peak memory. Standard unit tests pass — the regressions are non-functional.

## The Three Required Additions

**1. CodeQL at repository scope (not just PR-incremental)**

LLM-generated changes often introduce vulnerabilities in their interaction with existing code rather than in isolation. PR-targeted incremental scans miss this. Repository-level CodeQL scans (scheduled, not just on PR) catch interactions that narrow PR-scope analysis does not surface.

Results should upload as SARIF to GitHub Code Scanning to surface findings in the Security tab and as PR annotations, not just in log output.

**2. Runtime and peak memory tracking**

Execute tests inside a monitoring harness that records both runtime and peak memory consumption. Compare against a baseline from human-written reference patches or previous runs. Flag regressions that exceed threshold (e.g., >20% runtime increase, >50% memory increase).

This adds negligible overhead to test execution and catches the category of non-functional regressions that are invisible to functional test suites.

**3. Weighted severity scoring**

Treat CodeQL findings differently by severity: Error-level findings are blocking; Warning and Recommendation are informational. Do not treat all findings equally — a uniform block-on-any threshold creates excessive noise and alert fatigue for recommendation-level findings, while missing the signal of error-level findings if thresholds are set too permissively.

Recommended weights from the study: Error: 1.0, Warning: 0.6, Recommendation: 0.2, using precision-based rule weighting.

## The Multi-Dimensional Gate Problem

Prompting LLMs to optimize for security degrades performance, and vice versa. CI gates that check only security tend to accumulate performance debt; gates that check only performance create security gaps. Multi-dimensional CI evaluation (security + performance + correctness simultaneously) is more reliable than sequential single-dimension gates.

This is a structural property of LLM output, not an implementation limitation. It will not improve with model capability alone.

## Takeaway

Do not run the same CI configuration for LLM-generated PRs as for human-written PRs. Add CodeQL at repository scope, runtime/memory tracking, and weighted severity scoring. Evaluate all three quality dimensions simultaneously — security optimization degrades performance and vice versa. The quality gap is measurable and the checks are well-established; the gap between knowing and implementing these checks is an organizational risk.
