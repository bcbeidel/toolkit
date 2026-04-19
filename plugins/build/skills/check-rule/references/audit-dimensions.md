---
name: Audit Rule Dimensions
description: Evaluation criteria for auditing rule library quality — deterministic format checks and six semantic dimensions evaluated as a complete locked rubric
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
| Test file present | Co-located `<slug>.tests.md` does not exist alongside the rule file | warn |
| Concern prefix | Rule `name` field has no domain prefix (e.g., `quality-`, `style-`, `security-`, `compliance-`) when the rule library contains >5 rules | warn |

For Toolkit `.rule.md` files: parse frontmatter between `---` delimiters and check body headings.
For Cursor `.mdc` files: check `description`, `globs`, `alwaysApply` fields and body headings.
For CLAUDE.md sections: check that each `## Rule: <name>` block contains Intent, Non-Compliant, and Compliant subsections.

**Test file check:** derive the slug from the rule filename (strip `.rule.md` suffix), then check for `<slug>.tests.md` in the same directory. Example: `docs/rules/staging-layer-purity.rule.md` → look for `docs/rules/staging-layer-purity.tests.md`.

**Concern prefix check:** count all rule files in the library. Apply only when count >5. Domain prefixes are project-specific — accept any consistent prefix pattern; flag only if the `name` field contains no hyphen-delimited prefix at all (e.g., `name: staging layer purity` fails; `name: style-staging-layer-purity` passes).

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

**Canonical Repair:**
- *Broad scope:* Replace `**/*.ext` with `<directory>/**/*.ext` where `<directory>` is the specific architectural layer named in the Intent section. If uncertain, use the directory where the known failure occurred.
- *Vague criterion:* Replace each anchor-free term with a behavioral definition. Example: instead of "well-structured Intent section" → "Intent section contains all five required components: violation, failure cost, principle, exception policy, fix-safety signal."

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

**Canonical Repair:**
- *Wrong example order:* Swap Non-Compliant and Compliant Example sections — non-compliant must appear first.
- *Missing default-closed stance:* Add to Intent section: "When evidence is borderline, prefer WARN over PASS."
- *Multiple dimensions:* Split into two rules — one criterion per rule. If the description contains "and," it encodes two rules.

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

**Canonical Repair (staleness decision tree, in preference order):**
1. **Update examples** — if the convention still applies but code has changed: replace examples with current code, update file path comments.
2. **Archive** — if the convention still applies but the specific implementation it targets is gone: add `status: archived` to frontmatter with a reason note.
3. **Delete** — if the convention itself is definitively retired: remove the file and document the reason in the commit message.

Do not delete unless the convention is definitively retired — archive preserves the historical record.

### Dimension 4: Fix-Safety Classification

**What it checks:** Whether the rule declares whether its findings are
auto-remediable or require human judgment.

**Fail signals (→ WARN):**
- Toolkit `.rule.md` frontmatter has no `fix-safety` field
- Cursor `.mdc` body has no `**Fix-safety:**` line under Intent
- CLAUDE.md section has no `**Fix-safety:**` line
- `fix-safety` value is not `auto-remediable` or `requires-review`

**Pass signals:**
- `fix-safety` is declared as `auto-remediable` or `requires-review`

**Canonical Repair:** Mechanical — no intent-preservation risk.
- Add `fix-safety: requires-review` to frontmatter (default when uncertain).
- Downgrade to `auto-remediable` only when the fix provably preserves all observable behavior (formatting, pure renames, import ordering).

### Dimension 5: Rubric Instability Risk

**What it checks:** Whether the rule's examples and phrasing are stable enough
to produce consistent evaluations over time.

**Fail signals (→ WARN):**
- Non-compliant or compliant examples are synthetic (no file path comment, generic variable names like `foo`, `bar`, `myFunction`) — synthetic examples produce weaker anchors than real code
- Examples are absent (already caught by Tier 1, but flag here too if present but trivially minimal)
- Multiple examples present in a single section — risks introducing conflicting behavioral signals; a single canonical example anchors more reliably
- Intent section uses hedging language that creates a moving threshold: "might", "usually", "could", "generally"
- Rule has no "When evidence is borderline" declaration — without this, models default to PASS on ambiguous cases

**Pass signals:**
- Examples include file path comments indicating origin in real code
- Each section contains exactly one canonical example
- Language is categorical and unambiguous
- Borderline case handling is explicitly specified

**Canonical Repair:**
- *Synthetic examples:* Replace with real codebase code. Add file path comment (`// path/to/actual-file.ext`). Use domain-specific identifiers, not `foo`/`bar`.
- *Multiple examples:* Choose the single most canonical instance. Move secondary examples to the co-located `.tests.md` as additional FAIL or PASS cases.
- *Hedging language:* Replace "usually should" → "must"; "might cause" → "causes". If "usually" was intentional (acknowledging exceptions), move the exception to the Intent section's exception policy and use categorical language in the criterion.
- *Missing borderline declaration:* Add to Intent section: "When evidence is borderline, prefer WARN over PASS."

---

### Dimension 6: Intent Completeness

**What it checks:** Whether the Intent section contains all five required components
that prevent enforcement-without-education failure mode.

**The five required components:**
1. **Violation** — what pattern does this rule catch?
2. **Failure cost** — what specifically goes wrong when this pattern occurs, and who bears it? (load-bearing)
3. **Principle** — what underlying value does this enforce (type safety, security, maintainability)?
4. **Exception policy** — when is disabling this rule legitimate? Name at least one case. (load-bearing)
5. **Fix-safety signal** — is the auto-fix always safe, or does it require human review?

Components 2 (failure cost) and 4 (exception policy) are load-bearing: their absence produces enforcement-without-education behavior where developers disable rules rather than fix code.

**Fail signals (→ WARN):**
- Intent names the violation only ("Avoid using `console.log` in production") with no failure cost — what goes wrong? Who is affected?
- Intent contains hedging language ("might", "could") where the failure cost should be stated categorically
- No exception policy ("Exception: …") present — the rule appears to have no legitimate bypass
- Fix-safety signal missing from Intent section (separate from Tier 1 frontmatter check — this checks whether Intent *explains* the fix-safety decision, not just that the field exists)
- Intent section is fewer than 2 sentences — insufficient to contain all five components

**Pass signals:**
- Intent explicitly states what goes wrong when the pattern occurs and who bears the cost
- At least one named exception case ("Exception: …" or equivalent)
- Fix-safety reasoning explained ("Fix-safety: requires-review — violations involve architectural decisions")
- Default-closed stance declared ("When evidence is borderline, prefer WARN over PASS")

**Canonical Repair:**
- *Missing failure cost:* Add a sentence naming the specific consequence and who bears it. Example: instead of "Avoid X" → "X causes [specific failure] in [specific context], requiring [specific cost]."
- *Missing exception policy:* Add "Exception: [name at least one case where disabling is legitimate]." Even a narrow exception (e.g., "Exception: test files") satisfies this requirement.
- *Missing fix-safety explanation:* Add "Fix-safety: [auto-remediable | requires-review] — [brief reason]." to the Intent section.
- *Intent too short:* Expand — a compliant Intent section typically runs 3–6 sentences covering all five components.

---

## Evaluation Prompt Template

Use this skeleton for every Tier 2 LLM evaluation call. The criterion statement and anchor examples must come from the locked rubric above — do not generate them per-audit.

```
You are auditing a rule file for quality. Evaluate all six dimensions below in a single response.

For each dimension:
1. Quote the specific text from the rule that is most relevant (evidence)
2. Explain your reasoning
3. State your verdict: WARN or PASS
4. Give a specific Recommendation if WARN (name the exact change)

When evidence is borderline, surface as WARN, not PASS.

---

## Dimension 1: Specificity
Criterion: Does the scope glob include a directory prefix targeting a specific architectural
layer rather than matching all files of an extension? Do all criterion terms have observable
behavioral definitions (no anchor-free terms: "good", "clean", "clear", "appropriate")?

PASS anchor: scope is `models/staging/**/*.sql`; criterion says "no SQL expressions that multiply, divide, or aggregate column values"
FAIL anchor: scope is `**/*.py`; criterion says "handlers should be well-structured and clear"

## Dimension 2: Research Grounding
Criterion: Does the rule have exactly one criterion? Does non-compliant appear before compliant?
Is a default-closed stance explicitly declared? Is language categorical (no "might", "usually", "generally")?

PASS anchor: one criterion, non-compliant first, contains "When evidence is borderline, prefer WARN over PASS"
FAIL anchor: description contains "and"; compliant example appears before non-compliant; uses "usually should avoid"

## Dimension 3: Staleness
Criterion: Do the scope glob paths exist in the current codebase? Do examples reference
functions, imports, or modules present in the current codebase? Does Intent reference
dependencies present in the project manifest?

PASS anchor: scope path `src/api/` exists, examples use current framework imports
FAIL anchor: scope references `app/legacy/` which does not exist; examples use deprecated import

## Dimension 4: Fix-Safety Classification
Criterion: Is `fix-safety` declared as `auto-remediable` or `requires-review`?
For Toolkit: frontmatter field. For Cursor: `**Fix-safety:**` line in body. For CLAUDE.md: `**Fix-safety:**` line.

PASS anchor: frontmatter contains `fix-safety: requires-review`
FAIL anchor: no `fix-safety` field anywhere in the rule

## Dimension 5: Rubric Instability Risk
Criterion: Do examples have file path comments or domain-specific identifiers (not foo/bar)?
Does each example section contain exactly one canonical example (not multiple)?
Does Intent use categorical language? Is borderline case handling explicitly specified?

PASS anchor: example has `// src/api/handlers/users.py`, uses `user_id`/`order_total`; one example per section; Intent says "When evidence is borderline, prefer WARN over PASS"
FAIL anchor: examples use `foo`/`bar`, no file path comment; three non-compliant examples listed; Intent says "might cause issues"

## Dimension 6: Intent Completeness
Criterion: Does the Intent section contain all five required components: (1) violation — what pattern does the rule catch?; (2) failure cost — what specifically goes wrong and who bears it?; (3) principle — what underlying value does this enforce?; (4) exception policy — when is disabling legitimate?; (5) fix-safety signal — is the auto-fix always safe?

PASS anchor: "X causes [specific failure] in [specific context] (failure cost). This enforces [principle]. Exception: [named case]. Fix-safety: requires-review — [reason]. When evidence is borderline, prefer WARN over PASS."
FAIL anchor: "Avoid using console.log in production code. It creates noise." — names violation only; no failure cost, no principle, no exception policy, no fix-safety signal

---

<rule file verbatim>

---

Output format (one block per dimension):
## Dimension N: [Name]
Evidence: "[quoted text from rule]"
Reasoning: [your reasoning]
Verdict: WARN | PASS
Recommendation: [specific change if WARN, else "None"]
```

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
