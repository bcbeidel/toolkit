---
name: check-rule
description: Check a Claude Code rule library under `.claude/rules/` for path-glob validity, vague phrasing, contradictions, and oversize files. Use when the user wants to "audit rules", "check rule quality", "find conflicting rules", "review my rules", or "are my rules well-formed".
argument-hint: "[path to rule file or directory — scans .claude/rules/ if omitted]"
user-invocable: true
references:
  - ../../_shared/references/rule-canonical-form.md
  - ../../_shared/references/rule-structured-intent.md
  - ../../_shared/references/rule-audit-rubric.md
  - references/evaluation-mechanics.md
  - references/repair-playbook.md
---

# /build:check-rule

Evaluate the quality of an existing Claude Code rule library. Three tiers,
in order: deterministic format checks (no LLM), per-rule semantic checks
(specificity + vague phrasing), then cross-rule conflict detection.

This skill evaluates the rules themselves — not files against rules.

## Workflow

### 1. Discover Rules

Rule files live under `.claude/rules/**/*.md` (recursive). When `$ARGUMENTS`
resolves to a path, scope discovery to that file or directory. When
`$ARGUMENTS` is empty, scan `.claude/rules/` and (if the user maintains
personal rules) `~/.claude/rules/`.

Report: "Found N rules. Auditing..."

### 2. Tier 1 — Deterministic Format Checks

Parse frontmatter and check structural facts — no LLM call. Full check
table and notes: [evaluation-mechanics.md → Tier 1](references/evaluation-mechanics.md#tier-1-deterministic-format-checks).

Emit findings immediately. Rules with FAIL-severity findings (location,
extension, malformed `paths:`) are reported and excluded from Tier 2 —
malformed rules don't reach the LLM step.

### 3. Tier 2 — Per-Rule Semantic Checks (One LLM Call per Rule)

For each structurally valid rule, one locked-rubric LLM call. See
[rule-audit-rubric.md](../../_shared/references/rule-audit-rubric.md)
for the six dimensions and their criteria (3 always-on, 3 trigger-gated
on structured-Intent shape). The prompt skeleton is in
[evaluation-mechanics.md → Tier 2](references/evaluation-mechanics.md#tier-2-evaluation-prompt-skeleton).

Include the full rule file verbatim — never summarize. Present all
applicable dimensions in one call (per-dimension calls degrade agreement
by ~11.5 points per RULERS, Hong et al. 2026).

### 4. Tier 3 — Cross-Rule Conflict Detection

After per-rule evaluation, compare rule pairs that could co-fire. Pair
selection, the evaluation prompt, and canonical repair options live in
[evaluation-mechanics.md → Tier 3](references/evaluation-mechanics.md#tier-3-cross-rule-conflict-detection).

### 5. Report Findings

Output all findings in `scripts/lint.py` format (file, issue, severity).
Sort within each severity tier: Tier-1 deterministic first, then Tier-2
in dimension order (Specificity → Single Concern → Staleness → Intent
Completeness → Example Pair Quality → Default-Closed Declaration), then
Tier-3 conflicts; ties break alphabetically by file path. FAIL precedes
WARN overall.

Each FAIL or WARN finding must include a `Recommendation:` line with a
specific, actionable repair drawn from
[repair-playbook.md](references/repair-playbook.md). Generic suggestions
("fix this") are not acceptable — name the exact change.

```
FAIL  .claude/rules/api-handlers.md — Malformed paths glob: "src/api/**/*.{ts" — unclosed brace
  Recommendation: Close the brace: `"src/api/**/*.{ts,tsx}"`
WARN  .claude/rules/code-style.md — Specificity: "format code properly" is anchor-free
  Recommendation: Replace with a verifiable directive (e.g., "Use 2-space indentation; run prettier --check")
WARN  .claude/rules/testing.md — File length 287 lines exceeds 200-line guidance
  Recommendation: Split into topic files (e.g., testing-unit.md + testing-integration.md)
```

Close with a summary line:
- Findings present: `N rules audited, M findings (X fail, Y warn)`
- No findings: `N rules audited — no findings`

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding, draw the canonical repair from
[repair-playbook.md](references/repair-playbook.md). Then:

1. Read the relevant section of the rule file
2. Apply the canonical repair (if no playbook entry exists, skip and
   flag for manual review — do not improvise)
3. Show the diff
4. Write the change only on user confirmation
5. Re-run Tier-1 deterministic checks after each applied fix

Per-change confirmation is required — bulk application removes the
user's ability to review individual repairs.

## Key Instructions

- **Tier gating.** Run Tier-1 deterministic checks first; rules with FAIL-severity findings are excluded from Tier 2 so malformed rules never reach an LLM.
- **One locked-rubric call per rule.** Present every applicable Tier-2 dimension in a single call — per-dimension splits degrade agreement by ~11.5 points (RULERS, Hong et al. 2026).
- **Default-closed surfacing.** Borderline evidence → WARN, never silently PASS.
- **Per-change confirmation in the repair loop.** Show each diff and wait for user approval before writing; bulk application removes the review gate.

## Anti-Pattern Guards

1. **Per-dimension LLM call** — collapse into one locked-rubric call per rule.
2. **LLM-evaluating format compliance** — handle frontmatter / glob syntax with deterministic parse (Tier 1); send only structurally valid rules to the LLM.
3. **Ambiguous compliance reported as PASS** — default-closed surfaces borderline cases as WARN.
4. **Vague finding text** — cite the specific rule file and the exact phrasing or field that triggered the finding.
5. **Conflict-comparing non-overlapping rules** — gate Tier 3 on co-fire potential.
6. **Generic repair text** — every Recommendation names the specific change, drawn from `repair-playbook.md`.

## Example

<example>
User: `/build:check-rule .claude/rules/`

Step 1 — Discovers 3 rules: code-style.md, api-design.md, testing.md

Step 2 — Tier 1 deterministic check:
- code-style.md: 47 lines, no frontmatter (always-on) — passes to Tier 2
- api-design.md: `paths: "src/api/**/*.{ts"` — unclosed brace → FAIL (excluded from Tier 2)
- testing.md: 287 lines → WARN (proceeds to Tier 2 anyway)

Step 3 — Tier 2 semantic on 2 rules:
- code-style.md: directive pattern only (no `## Compliant` / `## Non-compliant` sections) — applies always-on dimensions only. Contains "format code properly" → WARN (specificity)
- testing.md: covers unit, integration, AND e2e — three distinct topics → WARN (single concern). Has `## Compliant` and `## Non-compliant` sections → trigger-gated dimensions also fire. Examples use `foo`/`bar` with no file path comment → WARN (example pair quality)

Step 4 — Tier 3 conflict detection: code-style.md (always-on) and
testing.md (always-on) both fire on every session. No directive
contradiction found.

Output:
```
FAIL  .claude/rules/api-design.md — Malformed paths glob: unclosed brace
  Recommendation: Close the brace: `"src/api/**/*.{ts,tsx}"`
WARN  .claude/rules/code-style.md — Specificity: "format code properly" is anchor-free
  Recommendation: Replace with a verifiable directive (e.g., "Use 2-space indentation; run prettier --check")
WARN  .claude/rules/testing.md — File length 287 lines exceeds 200-line guidance
  Recommendation: Split into testing-unit.md + testing-integration.md + testing-e2e.md
WARN  .claude/rules/testing.md — Single concern: covers three distinct topics (unit, integration, e2e)
  Recommendation: Same split as above resolves both findings
WARN  .claude/rules/testing.md — Example pair quality: examples use `foo`/`bar` without file path comments
  Recommendation: Replace with real codebase code; add `// path/to/file.ext` comment

3 rules audited, 5 findings (1 fail, 4 warn)
```
</example>

## Handoff

**Receives:** Path to a `.md` rule file or directory under `.claude/rules/`, or no argument (scans `.claude/rules/`)
**Produces:** Structured findings report in file/issue/severity format
**Chainable to:** build-rule (to fix flagged issues and rebuild non-compliant rules)
