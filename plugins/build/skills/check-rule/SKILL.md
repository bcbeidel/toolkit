---
name: check-rule
description: Check a rule library for quality issues — conflicts, specificity, staleness, fix-safety, rubric instability, and Intent completeness. Use when the user wants to "audit rules", "check rule quality", "find conflicting rules", "review my rules", or "are my rules well-formed".
argument-hint: "[path to rule file or directory — scans project if omitted]"
user-invocable: true
references:
  - references/audit-dimensions.md
  - references/repair-playbook.md
---

# /build:check-rule

Evaluate the quality of an existing rule library. Checks format validity
deterministically, then evaluates six semantic quality dimensions per rule
using a locked rubric, then detects cross-rule conflicts.

This skill evaluates the rules themselves — not files against rules.

## Workflow

### 1. Discover Rules

Find all rule files in scope:

| Format | Location |
|--------|----------|
| Toolkit | `docs/rules/*.rule.md` |
| Cursor | `.cursor/rules/*.mdc` |
| Claude Code | `## Rule:` sections in `CLAUDE.md` |

When `$ARGUMENTS` resolves to a path, scope discovery to that file or
directory. When `$ARGUMENTS` is empty, scan the project for all three
formats.

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

For each structurally valid rule, construct one LLM evaluation call with all six required elements (evaluating six semantic dimensions simultaneously):

1. **Criterion statement** — for each dimension, a single precise behavioral definition of what is being evaluated (drawn from the locked rubric in [audit-dimensions.md](references/audit-dimensions.md), not generated per-audit)
2. **PASS/FAIL scale declaration** — binary with behavioral definitions of what PASS and WARN mean in observable terms; no 1–5 or percentage scales
3. **Anchor examples** — one PASS anchor and one FAIL anchor per dimension demonstrating the criterion; without these the evaluator defaults to PASS on ambiguous cases
4. **CoT requirement** — explicit instruction: "Explain your reasoning and cite the specific text from the rule before stating your verdict"
5. **Structured output format** — constrain output to: `Dimension | Evidence (quoted from rule) | Reasoning | Verdict (WARN or PASS) | Recommendation`; evidence must appear before verdict
6. **Default-closed instruction** — "When evidence is borderline, surface as WARN, not PASS"

Include the full rule file verbatim (never summarize). Present all six dimension rubrics simultaneously — never split into per-dimension calls. Per-criterion separate calls score 11.5 points lower on average.

The output format enforces evidence-before-verdict ordering: `evidence → reasoning → verdict → recommendation`. If the LLM emits a verdict in the first sentence, the prompt is not enforcing evidence-first ordering — revise the output schema.

Repair recommendations are a separate concern from evaluation. The evaluation call produces evidence and verdict per dimension. The `Recommendation:` field in Step 5 is populated from [repair-playbook.md](references/repair-playbook.md) based on the verdict — it is not generated within the evaluation reasoning itself.

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
Sort within each severity tier: Tier-1 deterministic findings first, then
Tier-2 dimensions in numerical order (Dim 1 → Dim 6), then Tier-3
conflicts; ties break alphabetically by file path. FAIL findings precede
WARN findings overall. This mirrors check-skill's structural-before-content
ordering so the most actionable findings (frontmatter / sections) lead.

Each FAIL or WARN finding must include a `Recommendation:` line with a specific,
actionable repair drawn from [repair-playbook.md](references/repair-playbook.md).
Generic suggestions ("fix this") are not acceptable — name the exact change.

```
FAIL  docs/rules/staging-layer-purity.rule.md — Missing required field: severity
  Recommendation: Add `severity: warn` to frontmatter (default for new rules)
WARN  docs/rules/api-handler.rule.md — Specificity: scope "**/*.py" has no directory prefix
  Recommendation: Narrow scope to target architectural layer (e.g., `src/api/**/*.py`)
WARN  docs/rules/naming.rule.md — Fix-safety classification missing
  Recommendation: Add `fix-safety: requires-review` to frontmatter (default for convention rules)
```

Close with a summary line:
- Findings present: `N rules audited, M findings (X fail, Y warn)`
- No findings: `N rules audited — no findings`

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding, draw the canonical repair from
[repair-playbook.md](references/repair-playbook.md) — the playbook is
indexed by dimension and failure signal, so each finding maps to a
specific repair recipe. Then:

1. Read the relevant section of the rule file
2. Apply the canonical repair from the playbook (if the finding has no
   playbook entry, skip and flag for manual review — do not improvise)
3. Show the diff
4. Write the change only on user confirmation
5. Re-run Tier-1 deterministic checks after each applied fix to confirm
   the repair didn't break a different check

Per-change confirmation is required — bulk application removes the
user's ability to review individual repairs and conflicts with the
playbook's intent-preservation gate.

## Key Instructions

- Run Tier-1 deterministic checks first; gate LLM evaluation on structural validity so malformed rules surface as findings, not as expensive LLM calls
- Present all six semantic dimensions as a locked rubric in a single call per rule — per-dimension calls degrade agreement by ~11.5 points (RULERS, Hong et al. 2026)
- Include the full rule file verbatim in every LLM evaluation so the evaluator sees the same anchors a human reviewer would
- Limit conflict comparison to rule pairs with overlapping `scope` globs — non-overlapping rules cannot contradict and the comparison is wasted budget
- Surface borderline evidence as WARN (default-closed) so ambiguous cases enter the report rather than silently passing

## Anti-Pattern Guards

1. **Per-dimension LLM call** — collapse into one locked-rubric call per rule (per-dimension splits degrade agreement by 11.5 points, RULERS)
2. **LLM-evaluating format compliance** — handle frontmatter / section presence with deterministic parse (Tier 1); send only structurally valid rules to the LLM
3. **Ambiguous compliance reported as PASS** — surface as WARN (default-closed) so the user sees the borderline case
4. **Vague finding text** — cite the specific rule file and the exact criterion that failed; every finding names a file path and a rubric line
5. **Conflict-comparing non-overlapping rules** — gate Tier 3 on `scope`-glob overlap so the comparison budget goes to pairs that can actually contradict
6. **Generic repair text** ("fix this", "improve specificity") — every Recommendation names the specific change (what to add, remove, or replace, and what with) drawn from `repair-playbook.md`
7. **Evaluation prompt missing the criterion statement** — this is the highest-leverage element (its removal drops human-correlation from 0.666 → 0.487); include the behavioral definition from `audit-dimensions.md` verbatim in every Tier-2 call

## Example

<example>
User: `/build:check-rule docs/rules/`

Step 1 — Discovers 3 rules: staging-layer-purity.rule.md, api-input-validation.rule.md, naming-conventions.rule.md

Step 2 — Deterministic check:
- staging-layer-purity.rule.md: all fields present, all sections present → passes to LLM
- api-input-validation.rule.md: missing `fix-safety` field → WARN (proceeds to LLM anyway)
- naming-conventions.rule.md: missing `## Intent` → FAIL (excluded from LLM step)

Step 3 — Semantic audit on 2 rules:
- staging-layer-purity.rule.md: all 6 dimensions PASS
- api-input-validation.rule.md: Dimension 4 WARN (fix-safety missing), Dimension 6 WARN (Intent lacks failure cost and exception policy)

Step 4 — Conflict detection: staging-layer-purity and api-input-validation have non-overlapping scopes → no comparison needed

Output:
```
FAIL  docs/rules/naming-conventions.rule.md — Missing required section: ## Intent
  Recommendation: Add ## Intent section covering all five components: violation, failure cost, principle, exception policy, fix-safety signal
WARN  docs/rules/api-input-validation.rule.md — Fix-safety classification missing
  Recommendation: Add `fix-safety: requires-review` to frontmatter (default for security rules)
WARN  docs/rules/api-input-validation.rule.md — Intent completeness: missing failure cost and exception policy
  Recommendation: Add sentence naming what breaks and who bears the cost; add "Exception: [case]" line

2 rules audited (1 excluded — structural failure), 3 findings (1 fail, 2 warn)
```
</example>

## Handoff

**Receives:** Path to a rules file or directory, or no argument (scans project for all rule formats)
**Produces:** Structured findings report in file/issue/severity format
**Chainable to:** build-rule (to fix flagged issues and rebuild non-compliant rules)
