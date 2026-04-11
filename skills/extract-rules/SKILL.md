---
name: extract-rules
description: Surfaces and captures codebase conventions as structured rule files. Use when the user wants to "create a rule", "extract a rule", "capture this convention", "enforce this pattern", or describes a convention they want enforced.
argument-hint: A description of the convention, file paths to exemplary code, or a link to an external style guide
user-invocable: true
references:
  - references/rule-format-guide.md
---

> **Deprecated.** This skill is replaced by `/wos:build-rule`.
> `/wos:build-rule` provides all extract-rules functionality plus multi-format support
> (WOS `.rule.md`, Cursor `.mdc`, Claude Code CLAUDE.md), conflict detection, and
> structural validation against LLM rule research (fix-safety, default-closed, start-narrow).
>
> Proceed with extract-rules anyway? (y/n) — if not, invoke `/wos:build-rule` instead.

# /wos:extract-rules

Extract codebase conventions into structured rule files in `docs/rules/`.
Rules are evaluated by Claude for semantic compliance — they capture
patterns too nuanced for traditional linters.

Every rule MUST have both a non-compliant and compliant example.
Do not write a rule without examples.

## Workflow

### 1. Detect Mode

Determine the extraction mode from the user's input:

| Input | Mode |
|-------|------|
| User describes a convention in words | **conversation** |
| User points to files or code examples | **from-code** |
| User provides a style guide, RFC, or external doc | **from-source** |

If ambiguous, ask: "Would you like to describe the rule, point me at
exemplary code, or provide a reference document?"

### 2. Elicit Rule Details

**Conversation mode:**
- Ask clarifying questions one at a time, multiple-choice preferred
- Establish: what the rule enforces, which files it applies to (scope),
  how strict it is (severity), and why it exists (intent)
- Default severity to `warn` unless the user specifies `fail`

**From-code mode:**
- Read the exemplary files the user identified
- Identify the shared pattern: what convention do these files follow?
- Propose the rule with examples drawn directly from the actual code
- Ask the user to confirm or refine the inferred convention

**From-source mode:**
- Read the provided document (style guide, RFC, wiki page)
- Identify enforceable conventions — statements that produce a
  clear pass/fail judgment on a single file
- Present candidate rules as a numbered list
- User selects which to keep

**Edge cases:**
- If exemplary code has no discernible shared pattern, say so and ask
  the user to describe the convention they see
- If an external source contains no enforceable statements, report
  this and suggest conversation mode instead
- If the user describes something a traditional linter handles
  (syntax, formatting, import ordering), recommend the appropriate
  linter tool instead

### 3. Draft the Rule

Compose a rule file following the [Rule Format Guide](references/rule-format-guide.md).

Required elements:
- **Frontmatter:** name, description, type (`rule`), scope (glob pattern),
  severity (`warn` or `fail`)
- **Intent:** 1-2 sentences explaining WHY this rule exists
- **Non-compliant example:** shown FIRST — what a violation looks like
- **Compliant example:** what correct code looks like

Non-compliant examples placed before compliant examples improve
classification accuracy. Both examples serve as concrete anchors
that disambiguate intent far more effectively than additional prose.

### 4. Check for Duplicates

Before writing, read existing rules in `docs/rules/`:
- Check for rules with overlapping scope globs
- Check for rules with similar names or descriptions
- If overlap found, present to user: "This overlaps with [existing rule].
  Merge, replace, or keep both?"

### 5. Self-Check

Before presenting the rule to the user, verify:
- Frontmatter contains all required fields (name, description, type, scope, severity)
- Body contains an `## Intent` section
- Body contains a `## Non-Compliant Example` section with a code block
- Body contains a `## Compliant Example` section with a code block
- Scope glob is specific (not `**/*` or `**/*.py` without a directory prefix)
- Severity is `warn` or `fail`

If any check fails, fix it before presenting.

### 6. Present for Approval

Show the complete rule file to the user. Do not write until approved.

### 7. Write the Rule

- Create `docs/rules/` directory if it doesn't exist
- Write the rule file as `docs/rules/<slug>.rule.md`
- Derive the slug from the rule name (lowercase, hyphens)

## Example

<example>
User: "I want staging models to only do casts, renames, and deduplication"

Assistant asks: "Which files should this apply to?"
User: "models/staging/**/*.sql"

Assistant asks: "Should violations block (fail) or just warn?"
User: "warn for now"

Assistant drafts and presents:

```yaml
---
name: Staging layer purity
description: Staging models must only cast, rename, and deduplicate — no business logic
type: rule
scope: "models/staging/**/*.sql"
severity: warn
---
```

```markdown
## Intent

Staging models provide a clean interface over raw source data. Business
logic here couples source schema changes to business definitions.

## Non-Compliant Example
[code showing revenue calculation in staging]

## Compliant Example
[code showing only casts, renames, deduplication]
```

User approves → file written to `docs/rules/staging-layer-purity.rule.md`
</example>

## Key Instructions

- Every rule MUST have both a non-compliant and compliant example.
  Rules without examples produce unreliable enforcement.
- Default severity is `warn`. Only use `fail` when the user explicitly
  requests it or the convention is a hard constraint.
- Scope patterns must be as specific as possible. Broad scopes
  (e.g., `**/*.py`) cause rules to fire on irrelevant files,
  increasing false positives and eroding trust.
- Target semantic conventions that traditional linters cannot catch —
  layer boundaries, architectural constraints, naming intent,
  documentation quality.
- One convention per rule. If a user describes multiple conventions,
  create separate rule files.
- Do not write a rule file without both examples. This is non-negotiable.

## Anti-Pattern Guards

1. **Rules without examples** — refuse to write. Examples improve
   enforcement reliability by 4x.
2. **Overly broad scope** — flag and suggest narrowing. `**/*` is almost
   never correct.
3. **Rules that a linter handles better** — recommend the appropriate
   linter instead. LLM-based rules are for semantic understanding.
4. **Multiple conventions in one rule** — split into separate rules.
   One rule, one convention.
5. **Vague criterion language** — terms like "good structure", "appropriate
   naming", or "clear intent" without behavioral anchors produce variable
   evaluation results. Require concrete, observable behaviors that distinguish
   compliant from non-compliant. Question-specific rubrics with explicit
   anchors outperform vague ones ~4× on inter-evaluator agreement.
6. **Missing default-closed stance** — a rule that doesn't specify how
   to handle borderline cases will default to PASS, hiding real violations.
   Add a note in the rule's Intent section describing how uncertain cases
   should resolve (e.g., "When evidence is borderline, prefer WARN over PASS").

## Handoff

**Receives:** Convention description, code examples, or style-guide text to formalize
**Produces:** Structured rule files saved to `docs/rules/`
**Chainable to:** check-rules
