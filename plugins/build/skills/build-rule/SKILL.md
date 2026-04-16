---
name: build-rule
description: Create a correctly-structured rule for LLM-based semantic enforcement. Use when the user wants to "create a rule", "build a rule", "add a rule", "capture this convention", or "enforce this pattern".
argument-hint: A code pattern, behavior description, or existing rule draft to formalize
user-invocable: true
references:
  - references/rule-format-guide.md
  - references/rule-testing-guide.md
  - ../../_shared/references/primitive-routing.md
---

# /build:build-rule

Create semantic enforcement rules that Claude evaluates for compliance.
Rules capture conventions too nuanced for traditional linters — architectural
boundaries, naming intent, layer purity, documentation quality.

Every rule requires both a non-compliant and compliant example from real code.
Every rule requires a fix-safety declaration. Do not write a rule without these.

## Workflow

### 0. Verify Primitive

Before proceeding, confirm a rule is the right mechanism. Full decision matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

**Not right — redirect instead:**
- Check is shell-expressible (grep, file existence, regex) → recommend a hook or linter
- Enforcement must fire at a lifecycle event (pre-commit, pre-tool-use) → redirect to `/build:build-hook`
- Convention is procedural (multi-step workflow Claude should follow) → redirect to CLAUDE.md or `/build:build-skill`

**A rule is right when:** enforcement requires LLM judgment on static file content and the convention is too nuanced for grep or an AST linter. Proceed only when this holds.

### 1. Detect Format

Check the project structure to determine rule format:

- `.cursor/` exists → **Cursor** (`.mdc` in `.cursor/rules/`)
- `CLAUDE.md` exists and no `docs/rules/` → **Claude Code** (CLAUDE.md section)
- Otherwise → **WOS** (`docs/rules/<slug>.rule.md`)

Report the detected format: "Detected format: **[format]** — proceed with this
or override?" Wait for confirmation before drafting.

### 2. Classify Rule Type

Before eliciting the pattern, determine the rule category. Present the eight categories and ask which best describes the rule:

| Category | What it enforces |
|----------|-----------------|
| **Correctness** | Code that will behave incorrectly or produce errors |
| **Suspicious** | Code that is probably wrong but not guaranteed |
| **Security** | Code that creates vulnerabilities or exposes sensitive data |
| **Complexity** | Code that is too complex to maintain safely |
| **Performance** | Code patterns with measurable performance cost |
| **Convention/Style** | Project-specific naming, structure, or formatting conventions |
| **Accessibility** | Code that creates accessibility barriers |
| **LLM Directive** | AI response-generation behavior (not code correctness) |

Use the category to set structural defaults before drafting:
- **Fix-safety default:** `auto-remediable` for Correctness and Convention/Style only; `requires-review` for all others
- **Framing:** binary PASS/FAIL for Correctness, Suspicious, Security, Accessibility, LLM Directive; warn-first (default severity `warn`) for Complexity, Performance, Convention/Style
- **Severity default:** `fail` is appropriate only for Correctness and Security; use `warn` for all others unless the user explicitly requests fail

### 3. Elicit Pattern

Determine the intake mode from the user's input:

| Input | Mode |
|-------|------|
| User describes a convention | **conversation** |
| User points to files or code | **from-code** |
| User provides style guide or RFC | **from-source** |

**Conversation mode:**
- Ask clarifying questions one at a time, multiple-choice preferred
- Establish: what the rule enforces, which files (scope), how strict (severity), and why (intent)
- Default severity to `warn`

**From-code mode:**
- Read the exemplary files the user identified
- Identify the shared pattern; propose with examples from actual code
- Ask the user to confirm or refine

**From-source mode:**
- Read the provided document; identify enforceable statements
- Present candidate rules as a numbered list; user selects

If the user describes something a traditional linter handles (syntax, formatting,
import ordering), recommend the appropriate linter tool instead.

### 4. Check for Conflicts

Before drafting, read existing rules in the project:
- Check for rules with overlapping scope globs
- Check for rules with similar names or descriptions
- If overlap found: "This overlaps with [existing rule]. Merge, replace, or keep both?"

Do not skip this step. Undetected conflicts create contradiction in the rule
library and degrade enforcement reliability.

### 5. Draft Rule

Compose the rule following the [Rule Format Guide](references/rule-format-guide.md)
for the detected format.

Required in all formats:
- **Intent** — WHY this rule exists; must contain all five components (see below)
- **Non-compliant example** — shown FIRST; drawn from actual codebase code
- **Compliant example** — what correct code looks like
- **Fix-safety** — use the category default from Step 2

**Intent five-component requirement.** The Intent section must contain:
1. **Violation** — what pattern does this rule catch?
2. **Failure cost** — what specifically goes wrong, and who bears it? (load-bearing — do not omit)
3. **Principle** — what underlying value does this enforce (type safety, security, maintainability)?
4. **Exception policy** — when is disabling legitimate? Name at least one case. (load-bearing — do not omit)
5. **Fix-safety signal** — is the auto-fix always safe, or does it require human review?

Non-compliant before compliant: listing exclusions first improves classification
accuracy. Use actual code snippets with file path comments — synthetic examples
with generic identifiers (foo, bar, myFunction) produce weaker anchors.

Default severity: `warn`. Use `fail` only when the category is Correctness or Security,
or the user explicitly requests it.

### 6. Validate Structure

Before presenting, self-check against all twelve criteria. Fix any gap before presenting.

**Four structural requirements** (`llm-rule-structural-characteristics.context.md`):
1. **Specificity** — all key terms have explicit behavioral definitions; no vague words like "good", "clean", "clear", "appropriate"
2. **Scale matching** — binary PASS/FAIL for this rule type (not 1-5 or percentage)
3. **Scope isolation** — exactly one convention; no "and" in the description
4. **Behavioral anchoring** — both examples demonstrate observable, citable behaviors

**Five linter patterns** (`linter-patterns-transferable-to-llm-rules.context.md`):
5. **Meta/create separation** — criterion defined separately from evaluation context (Intent section exists and explains the criterion, not the enforcement mechanism)
6. **Start-narrow** — scope targets the specific file pattern where the known failure occurs; not `**/*` or `**/*.ext` without directory prefix
7. **Default-closed** — rule declares how uncertain cases resolve (WARN, not PASS)
8. **Fix-safety classification** — `fix-safety` field is set to `auto-remediable` or `requires-review`
9. **Concern-prefix** (if library has >5 rules) — rule name prefixed by domain (e.g., `quality-`, `safety-`, `compliance-`, `style-`)

**Three new quality checks** (from this session's research):
10. **Intent completeness** — Intent section contains all five components: violation, failure cost, principle, exception policy, fix-safety signal; no weak signals present (hedging language, prohibition-without-consequence, no exception policy)
11. **Single canonical example** — primary example is one canonical instance; flag if multiple examples risk introducing conflicting signals
12. **Example realism** — examples have file path comments or domain-specific identifiers; flag if synthetic (generic `foo`/`bar` identifiers, no file path context)

### 7. Present for Approval

Show the complete rule file to the user. Iterate on feedback. Do not write until approved.

### 8. Write the Rule

- Create the parent directory if it doesn't exist
- Write the rule file at the correct path for the detected format
- Write the test file at the format-specific location:

  | Format | Test file location |
  |--------|--------------------|
  | WOS | `docs/rules/<slug>.tests.md` |
  | Cursor | `.cursor/rules/<slug>.tests.md` |
  | Claude Code | `docs/rules/<slug>.tests.md` (create directory if needed) |

  Include at minimum 3 PASS cases and 3 FAIL cases, each with a rationale note. Reference the [Rule Testing Guide](references/rule-testing-guide.md) for format. Test cases must use different code than the rule's own examples.
- Report both file paths

## Example

<example>
User: "I want staging models to only do casts, renames, and deduplication"

Assistant detects WOS format (docs/rules/ exists). Classifies rule type: Convention/Style
(enforcing architectural layer purity). Fix-safety default: requires-review. Framing: warn-first.
Asks: "Which files should this apply to?"
User: "models/staging/**/*.sql". Asks: "Should violations block (fail) or just warn?"
User: "warn". Checks existing rules — no overlap found.

Drafts:

```yaml
---
name: Staging layer purity
description: Staging models must only cast, rename, and deduplicate — no business logic
type: rule
scope: "models/staging/**/*.sql"
severity: warn
fix-safety: requires-review
---
```

```markdown
## Intent

Staging models that include business logic (revenue calculations, tier
classifications) couple source schema changes to business definitions,
requiring coordinated updates across both layers when either changes.
This enforces the principle that staging models are a clean interface
over raw sources — not a transformation layer. Exception: calculated
fields that are pure data-type normalization (e.g., parsing a date
string to a date type) are permitted. Fix-safety: requires-review —
violations involve architectural decisions. When evidence is borderline,
prefer WARN over PASS.

## Non-Compliant Example

```sql
-- models/staging/stg_orders.sql
select id, quantity * unit_price as revenue,
  case when lifetime_value > 1000 then 'high' else 'standard' end as tier
from {{ source('raw', 'orders') }}
```

Violations: revenue calculation and tier classification are business logic.

## Compliant Example

```sql
-- models/staging/stg_orders.sql
select id as order_id, cast(order_date as date) as order_date,
  cast(quantity as integer) as quantity
from {{ source('raw', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

Only casts, renames, and deduplication.
```

Validates all 12 criteria — passes. Presents for approval. On approval, writes rule to
`docs/rules/staging-layer-purity.rule.md` and test file to
`docs/rules/staging-layer-purity.tests.md`.
</example>

## Key Instructions

- Every rule MUST have both a non-compliant and compliant example. Refuse to write without both.
- Won't replace a traditional linter: if the user's request is syntax, formatting, import ordering, or naming case, recommend the appropriate linter tool instead and stop.
- Intent must contain all five components. Missing failure cost (component 2) or exception policy (component 4) — stop and require them before drafting.
- Default severity is `warn`. False positives from `fail` rules erode trust faster than missed violations from `warn` rules.
- Start narrow: scope targets the specific known-failure pattern. Broaden only after validating negative examples.
- Default-closed: every rule declares how uncertain cases resolve. Rules without this default to PASS, hiding violations.
- Fix-safety is mandatory: always declare `auto-remediable` or `requires-review`.
- Never skip the conflict check. Undetected contradictions degrade the entire rule library.
- Do not write the file until the user approves the drafted rule.
- Always write the co-located test file. A rule without test cases cannot be validated before deployment.

## Anti-Pattern Guards

1. **Rules without both examples** — refuse to write; examples improve enforcement reliability 4×
2. **Overly broad scope** — `**/*` or `**/*.ext` without directory prefix fires on unrelated files; flag and require narrowing
3. **Multiple conventions in one rule** — any "and" in the description is a split signal
4. **Linter-appropriate checks** — syntax, formatting, import ordering belong in a linter, not here
5. **Missing default-closed stance** — rules without uncertainty handling default to PASS; always require a declaration
6. **Skipping conflict check** — contradictions in the rule library produce unpredictable enforcement
7. **Missing fix-safety** — without this, automated tools cannot safely apply fixes
8. **Incomplete Intent section** — an Intent that states only what the rule catches (not why it matters, not when to disable it) produces enforcement-without-education and workaround behavior
9. **Missing test file** — a rule without a co-located `.tests.md` file cannot be validated before deployment; this is a delivery failure, not optional polish

## Handoff

**Receives:** Code pattern, behavior description, or existing rule draft to formalize
**Produces:** Rule file written to the correct location for the detected project format
**Chainable to:** check-rule (verify the new rule fits the existing library without conflicts)