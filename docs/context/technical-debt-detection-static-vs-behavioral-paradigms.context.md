---
name: Technical Debt Detection — Static vs. Behavioral Paradigms
description: Static analysis (SonarQube) finds theoretical debt comprehensively; behavioral hotspot analysis (CodeScene) finds active debt by actual maintenance cost; a complete stack combines both.
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.sonarsource.com/resources/library/measuring-and-identifying-code-level-technical-debt-a-practical-guide/
  - https://codescene.com/blog/measure-code-health-of-your-codebase
  - https://codegen.com/blog/ai-tools-for-technical-debt/
  - https://conf.researchr.org/details/fse-2025/ai-ide-2025-papers/2/ACE-Automated-Technical-Debt-Remediation-with-Validated-Large-Language-Model-Refacto
related:
  - docs/context/technical-debt-prevention-fitness-functions-and-quality-gates.context.md
  - docs/context/quality-ratchet-pattern-for-gradual-enforcement.context.md
  - docs/context/deterministic-vs-advisory-principle-enforcement.context.md
---
# Technical Debt Detection — Static vs. Behavioral Paradigms

Two detection paradigms dominate technical debt identification, and they measure fundamentally different things. Using only one leaves a significant blind spot.

## Pattern-Based Static Analysis

SonarQube and equivalent tools (Codacy, CodeClimate) scan source code for known anti-patterns: cyclomatic complexity, test coverage gaps, code smells, duplication, security vulnerabilities. Technical debt is quantified using SQALE methodology: estimated remediation time weighted by probability-adjusted interest cost.

**What it gives you:** A consistent, objective debt score across the entire codebase. Comprehensive coverage of detectable code quality issues in 30+ languages. CI/CD integration as a deployment blocker on new code.

**What it misses:** Dormant debt — code with high measured complexity that is never touched and never causes problems. Static analysis cannot distinguish debt that costs you real maintenance time from debt that is theoretically problematic but operationally irrelevant. It identifies theoretical debt, not active debt.

## Behavioral Hotspot Analysis

CodeScene overlays commit frequency and authorship patterns on top of complexity metrics. The intersection of high-complexity + high-churn identifies "active" technical debt — code that both hurts structurally and is constantly being modified. This reveals actual business friction rather than theoretical quality scores.

Key insight: a stable 6/10 Code Health score is less alarming than a declining 8/10. Trends over absolute scores are the signal. Priorities are set based on product lifecycle: 8–9 for active feature development areas, 5+ acceptable for maintenance-phase components.

**What it gives you:** Prioritization signal grounded in actual maintenance cost. The 20% of the codebase causing 80% of development pain — the active debt that your team actually touches and suffers from.

**What it misses:** Dormant vulnerabilities, security patterns, and new code quality issues that have not yet generated churn. Behavioral analysis requires commit history to generate signal.

## AI-Assisted Detection: The Validated Layer

LLM-based Self-Admitted Technical Debt (SATD) detection — scanning code comments and commit messages for self-admitted debt — shows consistent improvement over prior NLP methods. Fine-tuned LLMs outperform CNN baselines by 4.4–7.2% F1-score improvement (Flan-T5-XL achieves F1 of 0.839). This is a modest but consistent and peer-reviewed gain.

The ACE paper (FSE 2025, the only peer-reviewed source on AI debt remediation) finds that "program understanding consumes approximately 70% of developers' time," and AI-assisted refactoring helps mitigate code-level debt that otherwise rarely gets acted upon. ACE requires validation, not autonomous operation — correctness checking is part of the system design.

**Autonomous AI remediation is not validated.** GitClear's 2024 analysis of 211 million lines found AI coding assistants increased duplicate block frequency ~8x and dropped refactoring from 25% to under 10% of code changes. Stack Overflow (Jan 2026) and InfoQ (Nov 2025) document that AI-generated code can accelerate debt creation if unreviewed. Use AI for detection and suggestion; require human validation for remediation.

## Complete Identification Stack

1. **Static analysis** — for comprehensive coverage and consistent scoring across the full codebase
2. **Behavioral hotspot analysis** — for prioritization signal grounded in actual maintenance cost
3. **LLM-based SATD detection** — for surfacing self-admitted debt in comments and commit messages
4. **Architectural fitness functions** — for prevention and structural compliance (see sibling file)

No single tool provides the full picture. Each layer answers a different question.

**The takeaway:** Run both static analysis for coverage and behavioral analysis for prioritization. Invest in fixing high-complexity + high-churn hotspots first — they represent debt that is actively costing you. Use AI for detection assistance, but require human review gates on any automated remediation.
