---
name: Rule Format Guide
description: Complete specification for rule file format, fields, and guidelines for writing effective rules
---

# Rule Format Guide

Rule files are markdown documents in `docs/rules/` with structured
frontmatter and three required body sections. They define conventions
that Claude evaluates semantically — patterns too nuanced for
traditional linters.

## File Naming

`docs/rules/<slug>.rule.md`

Derive the slug from the rule name: lowercase, hyphens, no dates.
Example: "Staging Layer Purity" → `staging-layer-purity.rule.md`

## Frontmatter

```yaml
---
name: Staging layer purity
description: Staging models must only cast, rename, and deduplicate — no business logic
type: rule
scope: "models/staging/**/*.sql"
severity: warn
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

### Scope Patterns

Scope determines which files the rule applies to. Use glob patterns.

**Single pattern:**
```yaml
scope: "models/staging/**/*.sql"
```

**Multiple patterns (list):**
```yaml
scope:
  - "src/api/**/*.py"
  - "src/handlers/**/*.py"
```

**Guidelines:**
- Be as specific as possible. `**/*.py` fires on every Python file —
  almost always too broad.
- Use directory prefixes to target architectural layers:
  `models/staging/`, `src/repositories/`, `tests/unit/`
- Test the scope: mentally list which files would match and whether
  the rule makes sense for ALL of them.

### Severity

| Level | Meaning | When to use |
|-------|---------|-------------|
| `warn` | Advisory — reported but doesn't block | Default. Use for conventions, preferences, guidelines |
| `fail` | Blocking — treated as an error | Hard constraints. Use for security, data integrity, architectural boundaries |

Default to `warn`. False positives from `fail` rules erode trust
faster than missed violations from `warn` rules.

## Body Sections

### Intent (Required)

1-2 sentences explaining WHY this rule exists. Not what it checks —
why it matters. Rules without intent get bypassed because developers
don't understand their purpose.

```markdown
## Intent

Staging models exist to provide a clean interface over raw source data.
Business logic in staging creates coupling between source schema changes
and business definitions, making both harder to maintain independently.
```

### Non-Compliant Example (Required, Listed First)

Show what a violation looks like. Place this BEFORE the compliant
example — research shows listing exclusions first improves
classification accuracy.

````markdown
## Non-Compliant Example

```sql
-- models/staging/stg_orders.sql
-- VIOLATION: contains business logic (revenue calculation, customer segmentation)
select
    id,
    cast(order_date as date) as order_date,
    quantity * unit_price * (1 - discount) as revenue,  -- business logic
    case
        when lifetime_value > 1000 then 'high'          -- business logic
        else 'standard'
    end as customer_tier
from {{ source('raw', 'orders') }}
```
````

### Compliant Example (Required)

Show what correct code looks like.

````markdown
## Compliant Example

```sql
-- models/staging/stg_orders.sql
-- COMPLIANT: only casts, renames, and deduplicates
select
    id as order_id,
    cast(order_date as date) as order_date,
    cast(quantity as integer) as quantity,
    cast(unit_price as numeric(10,2)) as unit_price,
    cast(discount as numeric(5,2)) as discount_rate
from {{ source('raw', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```
````

## Writing Effective Rules

**Be specific, not aspirational.** A rule should produce a clear pass/fail
judgment on a single file. "Code should be clean" is not a rule.
"Repository classes must not import from the presentation layer" is.

**One convention per rule.** If you're writing "and" in the description,
it's probably two rules. Split them.

**Examples from real code.** When extracting from exemplary files, use
actual code snippets. Synthetic examples are less effective anchors.

**Test the ambiguity.** Ask: would two experienced developers independently
agree on whether a given file passes or fails this rule? If not, the rule
needs more specific examples or a narrower scope.

## Complete Example

````markdown
---
name: Staging layer purity
description: Staging models must only cast, rename, and deduplicate — no business logic
type: rule
scope: "models/staging/**/*.sql"
severity: warn
---

## Intent

Staging models exist to provide a clean interface over raw source data.
Business logic in staging creates coupling between source schema changes
and business definitions, making both harder to maintain independently.

## Non-Compliant Example

```sql
select
    id,
    quantity * unit_price * (1 - discount) as revenue,
    case when lifetime_value > 1000 then 'high' else 'standard' end as customer_tier
from {{ source('raw', 'orders') }}
```

Violations: revenue calculation and customer segmentation are business
logic that belongs in the marts layer.

## Compliant Example

```sql
select
    id as order_id,
    cast(order_date as date) as order_date,
    cast(quantity as integer) as quantity,
    cast(unit_price as numeric(10,2)) as unit_price,
    cast(discount as numeric(5,2)) as discount_rate
from {{ source('raw', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

Only casts, renames, and deduplication. Business logic lives in
downstream marts models.
````
