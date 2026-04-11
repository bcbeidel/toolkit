---
name: Audit Rule Dimensions
description: Evaluation criteria for auditing rule library quality — deterministic format checks and five semantic dimensions evaluated as a complete locked rubric
---

# Audit Rule Dimensions

Rule auditing uses the three-tier grading hierarchy: deterministic checks first
(no LLM), then semantic evaluation (one LLM call per rule, full rubric in one pass),
then cross-rule conflict detection (separate LLM pass over rule pairs).

**Do not use LLM evaluation for deterministic checks.** Parsing required fields
and sections is faster, cheaper, and more reliable with code-style grep/read.

---

## Tier 1: Deterministic Format Checks

Run for every rule file before any LLM evaluation. Emit findings immediately.
Do not pass structurally invalid rules to the LLM step.

| Check | Condition | Severity |
|-------|-----------|----------|
| Required frontmatter fields | Missing any of: `name`, `description`, `type`, `scope`, `severity` | fail |
| `## Intent` section | Body does not contain `## Intent` heading | fail |
| Non-compliant example | Body does not contain `## Non-Compliant Example` heading | warn |
| Compliant example | Body does not contain `## Compliant Example` heading | warn |
| Severity value | `severity` field is not `warn` or `fail` | fail |

For WOS `.rule.md` files: parse frontmatter between `---` delimiters and check body headings.
For Cursor `.mdc` files: check `description`, `globs`, `alwaysApply` fields and body headings.
For CLAUDE.md sections: check that each `## Rule: <name>` block contains Intent, Non-Compliant, and Compliant subsections.

---

## Tier 2: Semantic Dimensions (One LLM Call per Rule)

Present all five dimensions as a locked rubric in a single call per rule.
Include the full rule file verbatim — never summarize.

**Evaluating dimensions one at a time is an anti-pattern.** Per-criterion separate
calls score 11.5 points lower on average and are excessively stringent (Hong et al.,
2026, RULERS study). Present all five simultaneously; score each independently
within the same call.

For each dimension, produce: **verdict** (WARN or PASS), **evidence** (specific
text from the rule that triggered the verdict), and **recommendation** (what to
change). Default-closed: when evidence is borderline, surface as WARN, not PASS.

### Dimension 1: Specificity

**What it checks:** Whether the rule's criterion is defined precisely enough to
produce consistent verdicts across evaluators.

**Fail signals (→ WARN):**
- Scope glob is `**/*` or `**/*.ext` without a directory prefix (e.g., `**/*.py` with no path component)
- Description or Intent uses anchor-free terms: "good", "clean", "clear", "appropriate", "well-structured", "properly formatted" without a behavioral definition
- Scope matches >3 unrelated directory trees, making the rule fire on conceptually different files

**Pass signals:**
- Scope is directory-prefixed (e.g., `models/staging/**/*.sql`)
- All terms in the criterion have observable behavioral definitions
- The compliant and non-compliant examples unambiguously illustrate the criterion

### Dimension 2: Research Grounding

**What it checks:** Whether the rule's design violates known best practices for
LLM evaluation rules.

**Fail signals (→ WARN):**
- Rule combines multiple evaluation dimensions in one criterion (scope isolation violation — `llm-rule-structural-characteristics.context.md`)
- Non-compliant example is absent or placed after the compliant example (listing exclusions first improves accuracy)
- Rule has no declaration of how uncertain/borderline cases should resolve (missing default-closed stance — `linter-patterns-transferable-to-llm-rules.context.md`)
- Rubric contains hedging language ("might", "usually", "generally", "often") without clarifying when exceptions apply

**Pass signals:**
- One criterion, one dimension
- Non-compliant example appears before compliant
- Default-closed stance is explicitly declared
- Language is categorical, not probabilistic

### Dimension 3: Staleness

**What it checks:** Whether the rule references tools, APIs, patterns, or file
structures that are no longer present in the codebase.

**Evidence to read:** Scan the rule's scope glob, examples, and Intent section for
tool names, file paths, framework APIs, and pattern names. Then check the codebase:
do those paths exist? Do those tools appear in dependencies?

**Fail signals (→ WARN):**
- Scope glob references a directory that does not exist in the project
- Examples reference functions, imports, or modules not found in the codebase
- Intent references a dependency or framework not in the project's manifest
- Rule mentions a deprecated internal convention that has since been replaced

**Pass signals:**
- All referenced paths exist
- All referenced tools are present in dependencies
- Examples match current code patterns

### Dimension 4: Fix-Safety Classification

**What it checks:** Whether the rule declares whether its findings are
auto-remediable or require human judgment.

**Fail signals (→ WARN):**
- WOS `.rule.md` frontmatter has no `fix-safety` field
- Cursor `.mdc` body has no `**Fix-safety:**` line under Intent
- CLAUDE.md section has no `**Fix-safety:**` line
- `fix-safety` value is not `auto-remediable` or `requires-review`

**Pass signals:**
- `fix-safety` is declared as `auto-remediable` or `requires-review`

### Dimension 5: Rubric Instability Risk

**What it checks:** Whether the rule's examples and phrasing are stable enough
to produce consistent evaluations over time.

**Fail signals (→ WARN):**
- Non-compliant or compliant examples are synthetic (no file path comment, generic variable names like `foo`, `bar`, `myFunction`) — synthetic examples produce weaker anchors than real code
- Examples are absent (already caught by Tier 1, but flag here too if present but trivially minimal)
- Intent section uses hedging language that creates a moving threshold: "might", "usually", "could", "generally"
- Rule has no "When evidence is borderline" declaration — without this, models default to PASS on ambiguous cases

**Pass signals:**
- Examples include file path comments indicating origin in real code
- Language is categorical and unambiguous
- Borderline case handling is explicitly specified

---

## Tier 3: Cross-Rule Conflict Detection (Separate LLM Pass)

Run after per-rule semantic evaluation. Compare rule pairs.

**A conflict exists when:** following one rule's compliant example as written would cause the other rule to produce a FAIL verdict on the same file.

**Evaluation prompt for each rule pair:**
1. Present Rule A verbatim
2. Present Rule B verbatim
3. Ask: "If a file follows Rule A's Compliant Example exactly, would Rule B FAIL that file?"
4. Ask the reverse: "If a file follows Rule B's Compliant Example exactly, would Rule A FAIL that file?"
5. If either answer is yes → FAIL finding for both rules

**Output format for conflicts:**
```
FAIL  docs/rules/rule-a.rule.md — Conflicts with rule-b.rule.md
  "Rule A requires X; Rule B's compliant example does not-X"
FAIL  docs/rules/rule-b.rule.md — Conflicts with rule-a.rule.md
  "Rule B requires not-X; Rule A's compliant example does X"
```

---

## Output Format

All findings use the `scripts/lint.py` format:

```
FAIL  docs/rules/staging-layer-purity.rule.md — Missing required frontmatter field: severity
WARN  docs/rules/api-input-validation.rule.md — Specificity: scope glob "**/*.py" has no directory prefix
WARN  docs/rules/naming-conventions.rule.md — Fix-safety classification missing
```

Sort order: FAIL findings first, WARN findings second, within each severity sort alphabetically by file path.

Final summary line: `N rules audited, M findings (X fail, Y warn)` or `N rules audited — no findings`.
