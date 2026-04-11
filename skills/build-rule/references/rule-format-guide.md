---
name: Rule Format Guide (build-rule)
description: Complete specification for rule file formats across WOS, Cursor, and Claude Code — fields, structure, and detection heuristics
---

# Rule Format Guide

Rules are semantic enforcement documents evaluated by an LLM — they capture
patterns too nuanced for traditional linters. Three formats are in common use
depending on project tooling. This guide covers all three.

## Format Detection

Detect the project's rule format automatically before drafting:

| Signal | Format |
|--------|--------|
| `.cursor/` directory exists | Cursor (`.mdc`) |
| `CLAUDE.md` exists AND no `docs/rules/` directory | Claude Code (CLAUDE.md section) |
| `docs/rules/` exists OR neither signal present | WOS (`.rule.md`) |

Always report the detected format to the user and allow override.

---

## Format 1: WOS Rule (`.rule.md`)

Used in WOS-managed projects. Stored at `docs/rules/<slug>.rule.md`.

### File Naming

Derive the slug from the rule name: lowercase, hyphens, no dates.
Example: "Staging Layer Purity" → `staging-layer-purity.rule.md`

### Frontmatter

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

### Required Fields

| Field | Type | Purpose |
|-------|------|---------|
| `name` | string | Human-readable rule name |
| `description` | string | One-sentence summary of what the rule enforces |
| `type` | literal | Always `rule` |
| `scope` | string or list | Glob pattern(s) matching files this rule applies to |
| `severity` | string | `warn` (advisory) or `fail` (blocks) |
| `fix-safety` | string | `auto-remediable` or `requires-review` (see Fix-Safety Classification) |

### Body Sections (all required)

**`## Intent`** — 1-2 sentences explaining WHY this rule exists. Not what it checks — why it matters.

**`## Non-Compliant Example`** — shown FIRST. What a violation looks like. Use actual code snippets from the codebase, not synthetic examples.

**`## Compliant Example`** — what correct code looks like.

Non-compliant before compliant: listing exclusions first improves LLM classification accuracy.

### Scope Patterns

```yaml
# Single pattern
scope: "models/staging/**/*.sql"

# Multiple patterns
scope:
  - "src/api/**/*.py"
  - "src/handlers/**/*.py"
```

- Be as specific as possible. `**/*.py` fires on every Python file — almost always too broad.
- Use directory prefixes to target architectural layers.
- Test the scope mentally: list which files match and whether the rule applies to ALL of them.

---

## Format 2: Cursor Rule (`.mdc`)

Used in Cursor-based projects. Stored at `.cursor/rules/<slug>.mdc`.

### Frontmatter

```yaml
---
description: One-sentence trigger description for the AI
globs: models/staging/**/*.sql
alwaysApply: false
---
```

### Fields

| Field | Type | Purpose |
|-------|------|---------|
| `description` | string | Shown to the AI as the trigger condition |
| `globs` | string or list | File patterns this rule applies to |
| `alwaysApply` | boolean | `true` = always loaded; `false` = loaded when files match |

### Body

Same three sections as WOS format: **Intent**, **Non-Compliant Example**, **Compliant Example**.

Add a `fix-safety` line in the body under Intent (no frontmatter field in `.mdc`):

```markdown
## Intent

Staging models exist to provide a clean interface over raw source data.

**Fix-safety:** requires-review — violations involve architectural decisions.
```

### Example

````markdown
---
description: Staging models must only cast, rename, and deduplicate — no business logic
globs: models/staging/**/*.sql
alwaysApply: false
---

## Intent

Staging models exist to provide a clean interface over raw source data.
Business logic in staging creates coupling between source schema changes
and business definitions.

**Fix-safety:** requires-review

## Non-Compliant Example

```sql
select id, quantity * unit_price as revenue from {{ source('raw', 'orders') }}
```

Violation: revenue calculation is business logic.

## Compliant Example

```sql
select id as order_id, cast(order_date as date) as order_date from {{ source('raw', 'orders') }}
```
````

---

## Format 3: Claude Code Rule (CLAUDE.md section)

Used in Claude Code projects without a dedicated rules directory. Rules are
embedded directly in `CLAUDE.md` as named sections.

### Section Structure

```markdown
## Rule: <Name>

**Scope:** `<glob pattern>`
**Severity:** warn | fail
**Fix-safety:** auto-remediable | requires-review

### Intent

1-2 sentences explaining why this rule exists.

### Non-Compliant Example

[code block showing a violation]

### Compliant Example

[code block showing correct code]
```

### Placement

Add new rules at the end of `CLAUDE.md`. Keep each rule self-contained —
do not split a rule across sections.

---

## Fix-Safety Classification

Every rule must declare whether its findings can be automatically remediated
or require human judgment. This classification comes from Ruff's fix-safety
model and prevents automated tools from applying unsafe changes.

| Value | Meaning | When to use |
|-------|---------|-------------|
| `auto-remediable` | The fix preserves behavior and can be applied automatically | Formatting, import ordering, pure renames with no semantic change |
| `requires-review` | The fix may alter behavior, remove logic, or require design judgment | Business logic violations, architectural boundary crossings, security issues |

**Default to `requires-review`.** Only use `auto-remediable` when you can guarantee the fix preserves all observable behavior.

---

## Writing Effective Rules

**Start narrow, add exclusions.** Draft the rule to match your known failure case. Broaden only after validating against known negative examples. A rule that fires twice with 100% accuracy is more valuable than one that fires 200 times with 50%.

**One convention per rule.** If the description contains "and", it's probably two rules. Split them.

**Examples from real code.** When extracting from exemplary files, use actual code snippets. Synthetic examples are weaker anchors.

**Default-closed stance.** Every rule must define how uncertain or borderline cases resolve. "When evidence is borderline, surface as WARN rather than PASS." If this isn't specified, models default to PASS, hiding real violations.

**Test the ambiguity.** Ask: would two experienced developers independently agree whether a given file passes or fails? If not, the rule needs more specific examples or a narrower scope.
