---
name: audit-rule
description: Audit a rule library for quality issues — conflicts, specificity, staleness, fix-safety, and rubric instability. Use when the user wants to "audit rules", "check rule quality", "find conflicting rules", "review my rules", or "are my rules well-formed".
argument-hint: "[path to rule file or directory — scans project if omitted]"
user-invocable: true
references:
  - references/audit-dimensions.md
---

# /wos:audit-rule

Evaluate the quality of an existing rule library. Checks format validity
deterministically, then evaluates five semantic quality dimensions per rule
using a locked rubric, then detects cross-rule conflicts.

This skill evaluates the rules themselves — not files against rules.

## Workflow

### 1. Discover Rules

Find all rule files in scope:

| Format | Location |
|--------|----------|
| WOS | `docs/rules/*.rule.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Code | `## Rule:` sections in `CLAUDE.md` |

If a path argument is provided, scope discovery to that file or directory.
If no argument, scan the project for all three formats.

Report: "Found N rules across [formats]. Auditing..."

### 2. Deterministic Format Check

For each rule, parse frontmatter and body sections without LLM involvement.
Check against the **Tier 1: Deterministic Format Checks** table in
[audit-dimensions.md](references/audit-dimensions.md).

Emit findings immediately. Rules with FAIL-severity format issues are reported
and excluded from the LLM evaluation step — do not send malformed rules to the
LLM. Rules with only WARN-severity format issues proceed to LLM evaluation.

This step requires no LLM call. Use grep and read operations only.

### 3. Semantic Audit (One LLM Call per Rule)

For each structurally valid rule, make one LLM evaluation call containing:

1. The full rule file verbatim (never summarize)
2. All five semantic dimension rubrics from [audit-dimensions.md](references/audit-dimensions.md) presented simultaneously as a locked rubric

Score all five dimensions in one pass. Never split into per-dimension calls —
per-criterion separate calls score 11.5 points lower on average and are
excessively stringent (Hong et al., 2026).

For each dimension, produce: verdict (WARN or PASS), evidence (specific text
that triggered the verdict), and recommendation (what to change).

### 4. Conflict Detection (Separate LLM Pass)

After per-rule evaluation, compare rule pairs for contradictions. For each pair:

1. Present both rule files verbatim
2. Ask: "Would following Rule A's compliant example cause Rule B to FAIL?"
3. Ask the reverse
4. If either answer is yes → FAIL finding citing both rule names and the specific contradiction

Only compare rules whose scope globs overlap — rules with non-overlapping scopes
cannot conflict. This reduces the number of comparisons for large libraries.

### 5. Report Findings

Output all findings in `scripts/lint.py` format (file, issue, severity).
Sort: FAIL findings first, WARN findings second, alphabetically by file within
each severity tier.

```
FAIL  docs/rules/staging-layer-purity.rule.md — Missing required field: severity
WARN  docs/rules/api-handler.rule.md — Specificity: scope "**/*.py" has no directory prefix
WARN  docs/rules/naming.rule.md — Fix-safety classification missing
```

Close with a summary line:
- Findings present: `N rules audited, M findings (X fail, Y warn)`
- No findings: `N rules audited — no findings`

## Key Instructions

- Run deterministic checks before invoking the LLM — do not send malformed rules to LLM evaluation
- Present all five semantic dimensions as a locked rubric in one call per rule; never make per-dimension calls
- Include the full rule file verbatim in every LLM evaluation — never summarize
- Only compare rules with overlapping scope globs for conflict detection
- Default-closed: borderline evidence surfaces as WARN, never silently PASS

## Anti-Pattern Guards

1. **Per-dimension LLM calls** — degrades accuracy by 11.5 points; always use complete rubric in one call
2. **LLM-evaluating format compliance** — deterministic parse is faster, cheaper, and more reliable
3. **Treating ambiguous compliance as PASS** — default-closed; surface as WARN
4. **Reporting vague findings** — every FAIL/WARN must cite the specific rule file and the exact criterion that failed
5. **Comparing non-overlapping rules for conflicts** — only rules whose scope globs overlap can contradict each other

## Example

<example>
User: `/wos:audit-rule docs/rules/`

Step 1 — Discovers 3 rules: staging-layer-purity.rule.md, api-input-validation.rule.md, naming-conventions.rule.md

Step 2 — Deterministic check:
- staging-layer-purity.rule.md: all fields present, all sections present → passes to LLM
- api-input-validation.rule.md: missing `fix-safety` field → WARN (proceeds to LLM anyway)
- naming-conventions.rule.md: missing `## Intent` → FAIL (excluded from LLM step)

Step 3 — Semantic audit on 2 rules:
- staging-layer-purity.rule.md: all 5 dimensions PASS
- api-input-validation.rule.md: Dimension 4 WARN (fix-safety missing, confirmed by LLM too)

Step 4 — Conflict detection: staging-layer-purity and api-input-validation have non-overlapping scopes → no comparison needed

Output:
```
FAIL  docs/rules/naming-conventions.rule.md — Missing required section: ## Intent
WARN  docs/rules/api-input-validation.rule.md — Fix-safety classification missing
  "Add fix-safety: requires-review to frontmatter"

2 rules audited (1 excluded — structural failure), 2 findings (1 fail, 1 warn)
```
</example>

## Handoff

**Receives:** Path to a rules file or directory, or no argument (scans project for all rule formats)
**Produces:** Structured findings report in file/issue/severity format
**Chainable to:** build-rule (to fix flagged issues and rebuild non-compliant rules)
