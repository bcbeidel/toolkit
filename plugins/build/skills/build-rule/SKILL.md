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
- Otherwise → **Toolkit** (`docs/rules/<slug>.rule.md`)

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

Treat `$ARGUMENTS` as the user's initial input — a code pattern, behavior
description, or existing rule draft. If `$ARGUMENTS` is empty, prompt for
one of those three intake modes. Determine the intake mode from
`$ARGUMENTS`:

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

**Four structural requirements** (see [rule-format-guide.md](references/rule-format-guide.md) — *Writing Effective Rules*):
1. **Specificity** — all key terms have explicit behavioral definitions; no vague words like "good", "clean", "clear", "appropriate"
2. **Scale matching** — binary PASS/FAIL for this rule type (not 1-5 or percentage). *Drafting-time only — the rule file itself does not record its scale, so check-rule cannot independently verify it.*
3. **Scope isolation** — exactly one convention; no "and" in the description
4. **Behavioral anchoring** — both examples demonstrate observable, citable behaviors

**Five linter patterns** (audited by check-rule — see [audit-dimensions.md](../check-rule/references/audit-dimensions.md)):
5. **Meta/create separation** — criterion defined separately from evaluation context (Intent section exists and explains the criterion, not the enforcement mechanism)
6. **Start-narrow** — scope targets the specific file pattern where the known failure occurs; not `**/*` or `**/*.ext` without directory prefix
7. **Default-closed** — rule declares how uncertain cases resolve (WARN, not PASS)
8. **Fix-safety classification** — `fix-safety` field is set to `auto-remediable` or `requires-review`
9. **Concern-prefix** (if library has >5 rules) — rule name prefixed by domain (e.g., `quality-`, `safety-`, `compliance-`, `style-`)

**Three Intent / example quality checks** (audited by check-rule Dim 5–6; research grounding in [.research/rule-best-practices.md](../../../../.research/rule-best-practices.md)):
10. **Intent completeness** — Intent section contains all five components: violation, failure cost, principle, exception policy, fix-safety signal; no weak signals present (hedging language, prohibition-without-consequence, no exception policy)
11. **Single canonical example** — primary example is one canonical instance; flag if multiple examples risk introducing conflicting signals
12. **Example realism** — examples have file path comments or domain-specific identifiers; flag if synthetic (generic `foo`/`bar` identifiers, no file path context)

### 7. Present for Approval

Before showing the complete file, narrate the design choices in 3–6
bullets so the user can disagree with any structural decision before it
gets written:

- **Category and severity defaults** — name the category picked in Step 2
  and the severity / fix-safety defaults it triggered.
- **Scope choice** — which directory the glob targets and why (start-narrow
  rationale).
- **Intent components** — confirm all five are present; call out which
  exception case was named.
- **Example sourcing** — real codebase code or constructed; file path
  comments included.
- **What was skipped and why** — patterns considered but rejected (e.g.,
  "did not split into two rules — single criterion holds even though
  description mentions 'X and Y'; the 'and' is descriptive, not a second
  criterion").

Then show the complete rule file. Iterate on feedback. Hold the write
until the user approves.

### 8. Write the Rule

- Create the parent directory if it doesn't exist
- Write the rule file at the correct path for the detected format
- Write the test file at the format-specific location:

  | Format | Test file location |
  |--------|--------------------|
  | Toolkit | `docs/rules/<slug>.tests.md` |
  | Cursor | `.cursor/rules/<slug>.tests.md` |
  | Claude Code | `docs/rules/<slug>.tests.md` (create directory if needed) |

  Include at minimum 3 PASS cases and 3 FAIL cases, each with a rationale note. Reference the [Rule Testing Guide](references/rule-testing-guide.md) for format. Test cases must use different code than the rule's own examples.
- Report both file paths

## Example

<example>
User: "I want staging models to only do casts, renames, and deduplication"

Assistant detects Toolkit format (docs/rules/ exists). Classifies rule type: Convention/Style
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

- Won't write a rule that lacks both a non-compliant and a compliant example — examples improve enforcement reliability ~4×, so the gate is hard. *(scope boundary)*
- Won't replace a traditional linter — if the request is syntax, formatting, import ordering, or naming case, redirect to the appropriate linter and stop. *(scope boundary)*
- Require all five Intent components before drafting (violation, failure cost, principle, exception policy, fix-safety signal) — failure cost (#2) and exception policy (#4) are load-bearing because their absence drives developers to disable rules rather than fix code.
- Default severity to `warn` — false positives from `fail` rules erode trust faster than missed violations from `warn` rules.
- Start narrow on scope — target the specific known-failure pattern; broaden only after validating against negative examples.
- Declare a default-closed stance ("prefer WARN over PASS when borderline") in every Intent — without it, evaluators silently default to PASS and hide violations.
- Set `fix-safety` on every rule (`auto-remediable` or `requires-review`) so automated tools can decide safely.
- Run the conflict check (Step 4) before drafting — undetected contradictions degrade the entire rule library.
- Hold the write until the user approves the drafted rule (Step 7 gate).
- Write the co-located test file alongside the rule — a rule without test cases cannot be validated before deployment.

## Anti-Pattern Guards

1. **Rule with only one example side** — refuse to write; require both non-compliant and compliant examples (improves enforcement reliability ~4×)
2. **Glob without a directory prefix** (`**/*` or `**/*.ext`) — narrow to the architectural layer named in Intent before accepting the rule
3. **Multiple conventions packed into one rule** — any "and" in the description is a split signal; produce two rules instead
4. **Convention enforceable by a traditional linter** (syntax, formatting, import ordering) — redirect to the linter and stop
5. **Intent without a default-closed declaration** — append "When evidence is borderline, prefer WARN over PASS" so uncertain cases surface as WARN, not silently PASS
6. **Conflict check skipped** — run Step 4 before drafting; undetected contradictions in the rule library produce unpredictable enforcement
7. **Frontmatter without `fix-safety`** — set `auto-remediable` or `requires-review` so automated tools can decide safely
8. **Intent that states only what the rule catches** — add failure cost, principle, exception policy, and fix-safety signal so the rule educates rather than mandates blindly
9. **Rule shipped without a co-located `.tests.md`** — write the test file before reporting completion; an unvalidated rule is a delivery failure, not optional polish

## Handoff

**Receives:** Code pattern, behavior description, or existing rule draft to formalize
**Produces:** Rule file written to the correct location for the detected project format
**Chainable to:** check-rule (verify the new rule fits the existing library without conflicts)