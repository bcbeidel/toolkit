---
name: Rule Type Taxonomy and Structural Properties
description: Eight rule categories derived from mature linting ecosystems and empirical LLM tool research, with structural properties (binary vs. ordinal, fix-safety default, scope strategy) that differ by category. Use when classifying a new rule to determine the right structure before drafting.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://arxiv.org/abs/2512.18925
  - https://eslint.org/docs/latest/extend/custom-rules
  - https://biomejs.dev/linter/
  - https://semgrep.dev/docs/semgrep-code/policies
related:
  - docs/research/2026-04-13-rule-taxonomy-intent-quality.research.md
  - docs/context/rule-intent-section-quality.context.md
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
---

# Rule Type Taxonomy and Structural Properties

## Key Insight

Rule type determines structure. Eight categories derived from ESLint, Biome, Semgrep, and an empirical study of 401 Cursor rule repositories (Jiang & Nam, MSR 2026) converge on a taxonomy where each category has different structural defaults. Classifying a rule before drafting it prevents common structural errors: ordinal framing on binary decisions, auto-remediable defaults on rules that require judgment, global scope on rules that only apply to one layer.

## The Eight Categories

| Category | ESLint analog | Biome analog | Binary/Ordinal | Fix-safety default |
|----------|--------------|-------------|----------------|-------------------|
| **Correctness** | problem | correctness | Binary | auto-remediable |
| **Suspicious** | problem | suspicious | Binary | requires-review |
| **Security** | problem | security | Binary | requires-review |
| **Complexity** | suggestion | complexity | Ordinal (warn-first) | requires-review |
| **Performance** | suggestion | performance | Ordinal (warn-first) | requires-review |
| **Convention/Style** | layout + suggestion | style | Ordinal (warn-first) | auto-remediable |
| **Accessibility** | problem | a11y | Binary | requires-review |
| **LLM Directive** | — | — | Binary | n/a (behavioral) |

**LLM Directive** is the category unique to AI tools — it targets the AI's response-generation behavior, not the code itself. It cannot be verified mechanically. Cursor rule repositories show 50% include LLM directives; post-2024 repositories have proportionally more.

## Structural Properties by Category

**Binary categories** (correctness, suspicious, security, accessibility): the violation either exists or it does not. Ordinal framing ("this is a 3/5 problem") is meaningless for these — use binary PASS/FAIL.

**Ordinal categories** (complexity, performance, style): degree matters. A function of 300 lines is more complex than one of 100 lines; both may warrant different severity responses. Launch in warn mode; graduate to fail only after team consensus.

**Fix-safety defaults:**
- `auto-remediable` for correctness and style rules where the fix preserves all observable behavior (pure renames, formatting, import ordering)
- `requires-review` for security, suspicious, accessibility, complexity, and performance where the fix may alter behavior, remove logic, or require design judgment
- Not applicable for LLM directive rules — they govern behavior, not code

**Scope strategies:**
- Correctness and security: enforce file-wide, no directory prefix restriction
- Convention/style: directory-scoped to the architectural layer where the convention applies
- LLM directives: scope to trigger mode (always-apply competes for attention budget; agent-requested or glob-scoped loads on demand with higher effective weight per token)

## Calibration Note

No empirical study has measured whether rule categorization improves LLM compliance rates. The compliance benefits of categorization observed in human linting systems (ESLint's `--fix-type` filtering, Semgrep's Monitor → Comment → Block graduation, Biome's nursery system) are documented for human developers; transfer to LLMs is an authoring-clarity benefit, not a proven LLM adherence improvement.

## Takeaway

Classify the rule category before drafting. Use the table to set fix-safety default, binary/ordinal framing, and scope strategy. The most common structural errors — wrong fix-safety, wrong framing, global scope on a layer-specific rule — are prevented by choosing the right category first.
