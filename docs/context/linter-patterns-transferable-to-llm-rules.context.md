---
name: Linter Patterns Transferable to LLM Rules
description: "Five structural patterns from ESLint, Semgrep, OPA, and Ruff that directly transfer to LLM rule design — meta/create separation, start-narrow, default-closed, fix-safety classification, and concern-prefix organization."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://eslint.org/docs/latest/extend/custom-rules
  - https://semgrep.dev/blog/2020/writing-semgrep-rules-a-methodology/
  - https://www.openpolicyagent.org/docs/latest/policy-language/
  - https://deepwiki.com/astral-sh/ruff/3-ruff-linter
related:
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
  - docs/context/rule-library-operational-practices.context.md
---
# Linter Patterns Transferable to LLM Rules

## Key Insight

ESLint, Semgrep, OPA, and Ruff have independently solved the rule-design problem in code enforcement. Their structural patterns transfer directly to LLM evaluation rules — not as inspiration, but as tested engineering solutions to the same underlying problem.

## The Five Transferable Patterns

**1. Meta/create separation (from ESLint)**

ESLint separates `meta` (what the rule is — type, description, schema, messages) from `create` (how it fires — the evaluation logic). Applied to LLM rules: define the criterion (what you're measuring, scoring scale, anchors) separately from the evaluation prompt (how the LLM scores it). This separation makes rules auditable, versionable, and composable.

Rule types carry semantic priority: "problem" (causes errors, highest priority), "suggestion" (better approach, no breakage), "layout" (style only). LLM rules should similarly declare their severity level before evaluating.

**2. Start-narrow, add exclusions (from Semgrep)**

"Write rules that match the exact pattern you observed in a real bug or vulnerability." Start with the minimal pattern that matches your known failure case. Then add `pattern-not` clauses for false-positive cases, and `pattern-either` for legitimate variations. "A rule that fires twice with 100% accuracy is more valuable than one fires 200 times with 50% accuracy."

Applied to LLM rules: draft conservative criteria that match observed failures first. Broaden only after validating against known negative examples.

**3. Default-closed stance (from OPA)**

OPA's `default allow := false` prevents undefined results — unknown cases fail closed. Applied to LLM rules: every rule should declare its default stance. If the LLM cannot determine whether a criterion is met, the result should surface as "uncertain" or fail, never silently pass.

**4. Fix-safety classification (from Ruff)**

Ruff classifies rules by fix safety: "safe" fixes preserve behavior; "unsafe" fixes may alter runtime behavior or remove comments. Users can override via `extend-safe-fixes` and `extend-unsafe-fixes`. Applied to LLM rules: explicitly distinguish rules that can be auto-remediated from rules that require human judgment. Label LLM evaluation outputs with the same dimension — auto-remediable vs. requires-review.

**5. Concern-prefix organization (from Ruff)**

Ruff organizes 800+ rules by prefix: F (Pyflakes), E/W (pycodestyle), B (bugbear), PL (Pylint), RUF (Ruff-specific). This enables selective rule enabling by concern category without requiring individual rule enumeration. Applied to LLM rule libraries: prefix rules by domain (safety-, quality-, compliance-, style-) so teams can enable/disable entire concern areas without managing each rule individually.

## Why This Matters

These patterns emerged from engineering teams managing thousands of rules at scale. Each one addresses a failure mode that also occurs in LLM evaluation systems: undefined handling (default-closed), false-positive cascade (start-narrow), tangled criterion/logic (meta/create), undifferentiated remediation (fix-safety), and unmanageable rule sprawl (concern-prefix).

## Takeaway

Before designing a new LLM rule, map it against these five patterns: Is the criterion defined separately from the prompt? Is it starting narrow? Does it define a default stance for uncertain cases? Is its remediability classified? Is it organized within a concern-prefix taxonomy? Rules that satisfy all five are significantly easier to maintain, debug, and calibrate.
