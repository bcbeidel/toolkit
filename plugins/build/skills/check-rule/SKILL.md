---
name: check-rule
description: Check a Claude Code rule library under `.claude/rules/` for path-glob validity, vague phrasing, contradictions, and oversize files. Use when the user wants to "audit rules", "check rule quality", "find conflicting rules", "review my rules", or "are my rules well-formed".
argument-hint: "[path to rule file or directory — scans .claude/rules/ if omitted]"
user-invocable: true
references:
  - ../../_shared/references/rules-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
---

# /build:check-rule

Evaluate the quality of an existing Claude Code rule library. Three tiers,
in order: deterministic format checks (no LLM), per-rule semantic checks
(eight always-on dimensions in a single locked-rubric call), then
cross-rule conflict detection.

This skill evaluates the rules themselves — not files against rules.

The audit rubric mirrors the authoring principles in
[rules-best-practices.md](../../_shared/references/rules-best-practices.md).
Each Tier-2 dimension cites its source principle. When the principles doc
changes, the dimensions should follow.

## Workflow

### 1. Discover Rules

Rule files live under `.claude/rules/**/*.md` (recursive). When `$ARGUMENTS`
resolves to a path, scope discovery to that file or directory. When
`$ARGUMENTS` is empty, scan `.claude/rules/` and (if the user maintains
personal rules) `~/.claude/rules/`.

Report: "Found N rules. Auditing..."

### 2. Tier 1 — Deterministic Format Checks

For each rule file, parse frontmatter and check structural facts. No
LLM call. See [audit-dimensions.md](references/audit-dimensions.md) for
the full table. The checks:

- **Location** — file is under `.claude/rules/` (or `~/.claude/rules/`); files
  at other paths are not loaded by Claude Code as rules
- **Extension** — file uses `.md` (not `.rule.md` or `.mdx`)
- **`paths:` glob validity** — when `paths:` is present, every glob
  parses (no unmatched brackets, valid wildcards, non-empty)
- **File size** — WARN at >200 non-blank lines, FAIL at >500 non-blank lines
- **Frontmatter shape** — only `paths:` is documented by Anthropic;
  flag unknown top-level keys as informational
- **Shape hints** — scan for keywords that signal a judgment-based rule
  (`compliant`, `non-compliant`, `violation`, `exception`, `failure`,
  fenced code blocks). These do not produce findings; they inform the
  Tier-2 prompt so the evaluator knows to weigh Why Adequacy and Example
  Realism more closely

Emit findings immediately. Rules with FAIL-severity findings (location,
extension, malformed `paths:`, oversize) are reported and excluded from
Tier 2 — malformed rules don't reach the LLM step.

### 3. Tier 2 — Per-Rule Semantic Checks (One LLM Call per Rule)

For each structurally valid rule, one locked-rubric LLM call assesses
the eight always-on dimensions in
[audit-dimensions.md](references/audit-dimensions.md):

1. **Framing** — positive statement of what to do; no hedged phrasing
2. **Specificity** — directive is concrete and falsifiable
3. **Single Concern** — body covers one topic
4. **Why Adequacy** — reasoning present; judgment-based rules name failure cost + legitimate exception
5. **Scope Tightness** — `paths:` matches the rule's actual reach; unscoped rules that name a specific directory get flagged
6. **Staleness** — globs resolve to real paths; examples look current
7. **Judgment-Not-Linter** — rule doesn't restate what a formatter or type-checker already catches
8. **Example Realism** — if examples present, they use domain-specific identifiers from the codebase, not synthetic `foo`/`bar`

Include the full rule file verbatim — never summarize. Present all
eight dimensions in one call (per-dimension calls degrade agreement
by ~11.5 points per RULERS, Hong et al. 2026). Dimensions that don't
apply to the specific rule return PASS silently — e.g., Example Realism
PASSes on a rule with no examples.

Output format per dimension: `evidence (quoted from rule) → reasoning →
verdict (WARN or PASS) → recommendation`. Default-closed: borderline
evidence surfaces as WARN, not PASS — this is evaluator policy; rules
themselves don't declare it.

### 4. Tier 3 — Cross-Rule Conflict Detection

After per-rule evaluation, compare rule pairs that could fire on the
same file. Two rules can conflict when:
- Both are always-on (no `paths:`), OR
- Their `paths:` globs overlap

For each candidate pair:
1. Present both rule files verbatim
2. Ask: "If a developer follows Rule A's guidance exactly, does Rule B
   contradict?"
3. Ask the reverse
4. If either answer is yes → FAIL finding citing both rule names and the
   specific contradiction

Anthropic's warning is the basis: *"if two rules contradict each other,
Claude may pick one arbitrarily."*

### 5. Report Findings

Output all findings in `scripts/lint.py` format (file, issue, severity).
Sort within each severity tier: Tier-1 deterministic first, then Tier-2
in dimension order (Framing → Specificity → Single Concern → Why
Adequacy → Scope Tightness → Staleness → Judgment-Not-Linter → Example
Realism), then Tier-3 conflicts; ties break alphabetically by file path.
FAIL precedes WARN overall.

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
WARN  .claude/rules/api-errors.md — Framing: rule states only what to avoid, no positive action named
  Recommendation: Restate as a positive directive (e.g., "Return structured error responses via `ApiError`") instead of "Don't throw raw errors"
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

- Run Tier-1 deterministic checks first; gate LLM evaluation on structural validity so malformed rules surface as findings, not as expensive LLM calls
- Include the Tier-1 shape-hints keyword sniff as context in the Tier-2 prompt — it informs the evaluator, not the dimension set (all eight dimensions always run)
- Present all eight Tier-2 dimensions as a single locked-rubric call per rule — per-dimension calls degrade agreement by ~11.5 points (RULERS, Hong et al. 2026)
- Include the full rule file verbatim in every LLM evaluation so the evaluator sees the same anchors a human reviewer would
- Limit conflict comparison to rule pairs that could co-fire (both always-on, or overlapping `paths:` globs) — non-overlapping scoped rules cannot contradict and the comparison is wasted budget
- Surface borderline evidence as WARN (default-closed) so ambiguous cases enter the report rather than silently passing — this is evaluator policy, not a per-rule requirement

## Anti-Pattern Guards

1. **Per-dimension LLM call** — collapse into one locked-rubric call per rule (per-dimension splits degrade agreement by 11.5 points, RULERS)
2. **LLM-evaluating format compliance** — handle frontmatter / glob syntax with deterministic parse (Tier 1); send only structurally valid rules to the LLM
3. **Ambiguous compliance reported as PASS** — surface as WARN (default-closed) so the user sees the borderline case
4. **Vague finding text** — cite the specific rule file and the exact phrasing or field that triggered the finding
5. **Conflict-comparing non-overlapping rules** — gate Tier 3 on co-fire potential (always-on pair, or overlapping `paths:`)
6. **Generic repair text** ("fix this", "improve specificity") — every Recommendation names the specific change, drawn from `repair-playbook.md`
7. **Trigger-gating Tier-2 dimensions** — don't skip dimensions based on whether the rule "opts into" a shape; run all eight always. Dimensions that don't apply return PASS silently

## Example

<example>
User: `/build:check-rule .claude/rules/`

Step 1 — Discovers 3 rules: code-style.md, api-design.md, testing.md

Step 2 — Tier 1 deterministic check:
- code-style.md: 47 lines, no frontmatter (always-on) — passes to Tier 2
- api-design.md: `paths: "src/api/**/*.{ts"` — unclosed brace → FAIL (excluded from Tier 2)
- testing.md: 287 lines → WARN (proceeds to Tier 2 anyway; below 500-line FAIL threshold)

Step 3 — Tier 2 semantic on 2 rules:
- code-style.md: contains "format code properly" → WARN (Specificity). Rule is entirely positive → PASS (Framing). Covers only code style → PASS (Single Concern). No examples → PASS (Example Realism, N/A).
- testing.md: covers unit, integration, AND e2e → WARN (Single Concern). Has compliant/non-compliant examples using `foo`/`bar` → WARN (Example Realism). Rule phrased as "Don't write flaky tests" with no positive counterpart → WARN (Framing).

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
WARN  .claude/rules/testing.md — Single Concern: covers three distinct topics (unit, integration, e2e)
  Recommendation: Same split as above resolves both findings
WARN  .claude/rules/testing.md — Framing: "Don't write flaky tests" states only what to avoid
  Recommendation: Restate positively (e.g., "Write tests that produce the same result given the same inputs")
WARN  .claude/rules/testing.md — Example Realism: examples use `foo`/`bar` placeholders
  Recommendation: Replace with real code from the codebase

3 rules audited, 6 findings (1 fail, 5 warn)
```
</example>

## Handoff

**Receives:** Path to a `.md` rule file or directory under `.claude/rules/`, or no argument (scans `.claude/rules/`)
**Produces:** Structured findings report in file/issue/severity format
**Chainable to:** build-rule (to fix flagged issues and rebuild non-compliant rules)
