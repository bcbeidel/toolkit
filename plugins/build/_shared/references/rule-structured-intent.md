---
name: Rule Structured Intent (Toolkit Opinion)
description: Toolkit-opinion body shape for Claude Code enforcement rules — when to use, template, rationale, and the trigger that opts a rule into structured-Intent auditing. Layered on top of the canonical spec in rule-canonical-form.md; adds no frontmatter fields and no required Anthropic headings.
---

# Rule Structured Intent

This document is **toolkit opinion**, layered on top of Anthropic's
canonical spec (see [rule-canonical-form.md](rule-canonical-form.md)).
It does not add frontmatter fields, change file location, or require any
heading Anthropic disallows. It opts the rule into a body shape that
helps the LLM evaluator stay consistent when the rule asks Claude to
*judge* a file's compliance.

## When to use this pattern

Use the structured-Intent shape when the rule is an **enforcement
rule** — Claude reads the file, applies the rule, and produces a
PASS/FAIL verdict. Skip it for:

- Procedural rules ("run X before Y") — bullet list is enough
- Style rules ("use 2-space indentation") — single line is enough
- Reference rules ("API handlers live in `src/api/handlers/`") —
  Anthropic's canonical body pattern handles them cleanly

## Body shape

````markdown
---
paths:
  - "models/staging/**/*.sql"
---

# <Rule Name>

## Why

<VIOLATION — what pattern does this rule catch?>
<FAILURE COST — what specifically goes wrong, and who bears it?>
<PRINCIPLE — what underlying value does this enforce?>
Exception: <name at least one legitimate bypass case>.

When evidence is borderline, prefer WARN over PASS.

## Compliant

```<lang>
// real code from the codebase, with file path comment
```

## Non-compliant

```<lang>
// real code that violates the rule
```
````

## Why each piece earns its place

| Piece | Why it helps |
|-------|--------------|
| **`## Why` lead-in** | Names the rule's purpose so a reader (human or Claude) understands the *why*, not just the *what*. Anthropic's specificity guidance applies — the Why section should be concrete, not "this rule keeps things clean". |
| **Failure cost** (load-bearing) | Without it, developers weigh the rule as bureaucratic overhead. Naming what breaks and who bears the cost drives adherence over disable behavior. |
| **Exception policy** (load-bearing) | Rules that admit no exception get disabled wholesale when the legitimate edge case appears. Naming one case keeps the rule alive. |
| **Principle** | Anchors the rule to a value (type safety, security, maintainability). When the rule's specifics don't quite fit a new situation, the principle still guides. |
| **`## Compliant` and `## Non-compliant` examples** | Anchor the evaluation to concrete cases. Research-grounded: evidence-anchored rubrics deliver +0.17 QWK over inference-only (per `.research/rule-best-practices.md`). |
| **Real code with file path comments** | Synthetic `foo`/`bar` examples produce weaker anchors than domain-specific identifiers from the actual codebase. |
| **Default-closed declaration** | Without it, evaluators silently default to PASS on ambiguous cases. The line keeps borderline cases visible. |

## Trigger — how a rule opts in

A rule opts into structured-Intent auditing when its body contains:

- `## Compliant` AND `## Non-compliant` (or `## Non-Compliant`) sections, **OR**
- `## Why` (or `## Intent`) section.

Rules that don't meet the trigger stay in the canonical-spec lane and
are audited only against always-on dimensions. Flagging a plain
Anthropic-shape rule against structured-Intent dimensions would penalize
it for not adopting toolkit opinion, which is not the rubric's intent.
