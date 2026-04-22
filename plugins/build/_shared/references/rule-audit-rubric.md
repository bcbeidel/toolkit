---
name: Rule Audit Rubric
description: Six-dimension locked rubric used by check-rule to audit Claude Code rule files. Cross-references invariants in rule-canonical-form.md and rule-structured-intent.md; evidence signals and canonical repairs stay here.
---

# Rule Audit Rubric

Six semantic dimensions scored in a single locked-rubric LLM call per
rule. This document is the source of truth for the dimensions,
evidence signals, and canonical repairs. Each dimension cross-references
the underlying invariant in
[rule-canonical-form.md](rule-canonical-form.md) or
[rule-structured-intent.md](rule-structured-intent.md) — this file does
not restate those invariants.

Evaluation process (tiering, prompt skeleton, cross-rule conflict,
output format) lives in each consumer skill's local
`references/evaluation-mechanics.md`.

## Table of Contents

- [Category Tiers](#category-tiers)
- [Always-on dimensions (every rule)](#always-on-dimensions-every-rule)
  - [Dimension 1: Specificity](#dimension-1-specificity)
  - [Dimension 2: Single Concern](#dimension-2-single-concern)
  - [Dimension 3: Staleness](#dimension-3-staleness)
- [Trigger-gated dimensions (structured-Intent rules only)](#trigger-gated-dimensions-structured-intent-rules-only)
  - [Dimension 4: Intent Completeness](#dimension-4-intent-completeness)
  - [Dimension 5: Example Pair Quality](#dimension-5-example-pair-quality)
  - [Dimension 6: Default-Closed Declaration](#dimension-6-default-closed-declaration)

---

## Category Tiers

Every dimension carries a category tier so users can distinguish
spec-backed findings from house-style guidance.

| Tier | Meaning |
|------|---------|
| **canonical** | Enforces a documented Anthropic invariant (see [rule-canonical-form.md](rule-canonical-form.md)) |
| **research-grounded** | Toolkit-opinion check whose design is supported by published research (cited in `.research/rule-best-practices.md`) |
| **toolkit-opinion** | Recommended by this toolkit; no upstream spec |

The tier appears in parentheses after each dimension heading.

Each dimension produces, per rule: **verdict** (WARN or PASS),
**evidence** (specific text from the rule that triggered the verdict),
and **recommendation** (what to change). Default-closed: when evidence
is borderline, surface as WARN, not PASS.

---

## Always-on dimensions (every rule)

Dimensions 1–3 apply to every rule. Anthropic-spec compliance plus
single-topic discipline plus drift detection apply regardless of body
shape.

### Dimension 1: Specificity

*(canonical — anchors Anthropic's "Specific over vague" body convention; see [rule-canonical-form.md → Body Conventions](rule-canonical-form.md#body-conventions))*

**What it checks:** Whether the rule's directives are concrete enough
that a developer (or Claude) can verify compliance unambiguously.

**Fail signals (→ WARN):**
- Anchor-free terms used as the directive: "good", "clean", "clear",
  "appropriate", "well-structured", "properly", "nice", "consistent"
  without a behavioral definition
- Directives that defer the decision back to the reader ("use your
  judgment", "as appropriate") without a fallback rule

**Pass signals:**
- Directives are verifiable: a numeric threshold, a named tool to run,
  a specific file path or command, a quoted code pattern
- Anchor-free terms appear only when paired with a verifiable
  definition ("clean code: no functions over 50 lines, no nested
  ternaries")

**Canonical Repair:** Replace each anchor-free term with a verifiable
directive. Examples:
- "Format code properly" → "Use 2-space indentation; run `prettier --check`"
- "Test your changes" → "Run `npm test` before committing"
- "Keep files organized" → "API handlers live in `src/api/handlers/`"

### Dimension 2: Single Concern

*(toolkit-opinion — anchors the "one topic per file" convention in [rule-canonical-form.md → Body Conventions](rule-canonical-form.md#body-conventions))*

**What it checks:** Whether the rule covers a single topic. A file that
mixes unrelated conventions is two rules, not one.

**Fail signals (→ WARN):**
- Multiple top-level `##` sections covering distinct topics that
  wouldn't naturally co-evolve (e.g., "API conventions" and
  "Test conventions" in the same file)
- Filename describes one topic but body covers another in addition
- Two unrelated `paths:` patterns where each `##` section applies to
  only one (split signal)

**Pass signals:**
- All `##` sections relate to the topic named in the filename
- `paths:` globs all target files where every directive in the body
  applies

**Canonical Repair:** Split into separate topic files. Move each
unrelated section to its own `<topic>.md` under `.claude/rules/`.
Update `paths:` if the original was a union covering multiple file
types — each split file gets the subset that actually applies.

### Dimension 3: Staleness

*(toolkit-opinion — drift detection against the codebase the rule was authored in; anchors the `paths:` glob semantics in [rule-canonical-form.md → Frontmatter](rule-canonical-form.md#frontmatter))*

**What it checks:** Whether the rule references file paths, commands,
or code patterns that no longer exist in the codebase.

**Evidence to read:** Scan `paths:` globs, code-block examples, and
prose for file paths, command names, framework imports, and pattern
names. Then check the codebase: do those paths exist? Do those commands
and imports still appear?

**Fail signals (→ WARN):**
- `paths:` glob references a directory that does not exist in the project
- Code-block examples reference functions, imports, or modules not found in the codebase
- Prose references a dependency or framework not in the project's manifest
- Rule mentions a deprecated convention that has since been replaced

**Pass signals:**
- All referenced paths exist
- Commands referenced are still in use (e.g., `npm test` is in `package.json`)
- Examples match current code patterns

**Canonical Repair (decision tree, in preference order):**
1. **Update** — convention still applies; the referenced code has changed. Replace examples with current code, update file paths.
2. **Delete** — the convention is retired (architectural pattern abandoned, framework replaced). Remove the rule file and document the reason in the commit message.

Anthropic doesn't define an `archived:` status for rules; deletion is
the canonical retirement.

---

## Trigger-gated dimensions (structured-Intent rules only)

Apply Dimensions 4–6 only when the rule opts into the toolkit-opinion
structured-Intent shape. Trigger criteria are defined in
[rule-structured-intent.md → Trigger](rule-structured-intent.md#trigger--how-a-rule-opts-in).

### Dimension 4: Intent Completeness

*(toolkit-opinion — enforces the four-component `## Why` shape in [rule-structured-intent.md → Why each piece earns its place](rule-structured-intent.md#why-each-piece-earns-its-place))*

**What it checks:** Whether the `## Why` (or `## Intent`) section
contains all four toolkit-opinion components: violation, failure cost,
principle, exception policy.

**Fail signals (→ WARN):**
- Why section names the violation only ("Avoid X") with no failure cost
- Why section uses hedging language ("might", "could") where failure
  cost should be categorical
- No exception policy ("Exception: …") present
- Why section is fewer than 2 sentences — insufficient to carry all
  four components

**Pass signals:**
- Why explicitly states what goes wrong and who bears the cost
- At least one named exception case ("Exception: …")
- Principle named (type safety, security, maintainability, etc.)

**Canonical Repair:** See local `repair-playbook.md` → Dimension 4 for
the consumer skill's repair procedure.

### Dimension 5: Example Pair Quality

*(research-grounded — enforces the compliant/non-compliant pairing convention in [rule-structured-intent.md → Body shape](rule-structured-intent.md#body-shape); evidence-anchored rubrics deliver +0.17 QWK over inference-only)*

**What it checks:** Whether the rule's example pair anchors evaluation
to concrete, real cases.

**Fail signals (→ WARN):**
- Examples use synthetic identifiers (`foo`, `bar`, `myFunction`) without file path comments
- Compliant example appears before non-compliant (listing exclusions first improves accuracy)
- Multiple code snippets in a single section (encodes conflicting behavioral signals)
- One section is missing entirely (compliant present without non-compliant or vice versa)

**Pass signals:**
- Both sections present; non-compliant first
- Each example uses real codebase code with `// path/to/file.ext` comment
- Each section has exactly one canonical example

**Canonical Repair:** See local `repair-playbook.md` → Dimension 5.

### Dimension 6: Default-Closed Declaration

*(toolkit-opinion — enforces the default-closed line in [rule-structured-intent.md → Body shape](rule-structured-intent.md#body-shape))*

**What it checks:** Whether the Why section declares how borderline /
uncertain cases should resolve.

**Fail signals (→ WARN):**
- No "When evidence is borderline…" line (or equivalent default-closed declaration)
- Declaration is reversed ("when borderline, prefer PASS over WARN")

**Pass signals:**
- Why contains: "When evidence is borderline, prefer WARN over PASS" (or close paraphrase)

**Canonical Repair:** Append to Why section: `"When evidence is borderline, prefer WARN over PASS."`
