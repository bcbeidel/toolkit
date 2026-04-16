---
name: Rule Testing Guide (build-rule)
description: How to write a co-located rule test file — two-polarity structure, minimum sample sizes, acceptance criteria gates, and what makes a good test case. Every rule produced by build-rule requires a companion .tests.md file.
---

# Rule Testing Guide

Every rule written by build-rule requires a co-located test file. Test cases verify
that the rule generalizes beyond its own examples. A rule without test cases cannot
be validated before deployment.

## File Naming and Location

```
docs/rules/staging-layer-purity.rule.md      ← rule file
docs/rules/staging-layer-purity.tests.md     ← test file (same directory, same slug)
```

The test file lives in the same directory as the rule file. Naming convention:
`<slug>.tests.md` where `<slug>` matches the rule filename without the `.rule.md` suffix.

---

## Test File Structure

```markdown
# Tests: <Rule Name>

## FAIL Cases
Cases that must trigger the rule (violations).

### FAIL 1 — <brief description>
**Rationale:** <what makes this a violation>
```<language>
<code snippet>
```

### FAIL 2 — <brief description>
...

---

## PASS Cases
Cases that must NOT trigger the rule (compliant code).

### PASS 1 — <brief description>
**Rationale:** <what makes this compliant despite superficial resemblance to violations>
```<language>
<code snippet>
```

### PASS 2 — <brief description>
...
```

Use `# todo: <description>` to document known coverage gaps — patterns the rule
should catch but doesn't yet — without adding test failures for unimplemented coverage.

---

## Minimum Viable Test Set

| Phase | Cases | Gate |
|-------|-------|------|
| Warn-mode launch (Gate 1) | 3 FAIL + 3 PASS | Required before deployment |
| Fail-mode promotion (Gate 2) | 8–10 FAIL + 8–10 PASS | Required before fail-severity |

The minimum of 3+3 covers obvious cases. Gate 2 adds borderline and known FP/FN candidates.

---

## What Makes a Good Test Case

Include one case from each category at Gate 1:

**FAIL cases:**
- **Obvious violation** — unambiguous, exactly what the rule is designed to catch
- **Borderline violation** — clearly violates but might be misclassified by a lenient evaluator
- **Common false-negative candidate** — a pattern that looks compliant but isn't

**PASS cases:**
- **Obvious compliance** — unambiguous, clearly correct
- **Near-miss** — code that superficially resembles a violation but is actually compliant
- **Edge case** — a legitimate pattern at the boundary of the rule's scope

---

## Independence from Rule Examples

Test cases must use **different code** than the rule's own Non-Compliant and Compliant
examples. The rule examples anchor the evaluation criterion; test cases verify generalization.

If a test case uses the same code as a rule example, it is verifying recall of the anchor,
not generalization. This produces false confidence in rule quality.

---

## Acceptance Criteria

**Gate 1 (warn mode):** TP ≥90%, TN ≥85%, consistency ≥80% across 3 runs at temperature=0

**Gate 2 (fail mode):** TP ≥95%, TN ≥90%, consistency ≥90% + human CoT spot-check of 5 cases

**Post-deployment trigger for revision:** production FP rate >20% (regardless of test results)

---

## Example

For `docs/rules/staging-layer-purity.rule.md`:

```markdown
# Tests: Staging Layer Purity

## FAIL Cases

### FAIL 1 — Revenue calculation in staging
**Rationale:** `quantity * unit_price` is a business logic calculation, not a cast or rename.
```sql
-- models/staging/stg_line_items.sql
select
  id,
  quantity * unit_price as line_total,
  cast(order_date as date) as order_date
from {{ source('raw', 'line_items') }}
```

### FAIL 2 — Conditional classification
**Rationale:** `CASE WHEN` that derives a category is business logic, not a rename.
```sql
-- models/staging/stg_customers.sql
select
  id,
  case when total_spend > 5000 then 'vip' else 'standard' end as customer_tier
from {{ source('raw', 'customers') }}
```

### FAIL 3 — Filtered staging model (borderline)
**Rationale:** Filtering rows based on a business condition is business logic, not deduplication.
```sql
-- models/staging/stg_orders.sql
select id, cast(order_date as date) as order_date
from {{ source('raw', 'orders') }}
where status != 'cancelled'
```

---

## PASS Cases

### PASS 1 — Pure casts and renames
**Rationale:** Only type casts and column renames; no derived values.
```sql
-- models/staging/stg_products.sql
select
  product_id as id,
  cast(price as numeric) as price,
  cast(created_at as timestamp) as created_at
from {{ source('raw', 'products') }}
```

### PASS 2 — Deduplication via window function
**Rationale:** `QUALIFY ROW_NUMBER()` deduplicates; this is an explicit exception in the rule.
```sql
-- models/staging/stg_events.sql
select id, cast(event_at as timestamp) as event_at
from {{ source('raw', 'events') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

### PASS 3 — Date parsing (near-miss: looks like calculation but is normalization)
**Rationale:** Parsing a string to a date type is pure type normalization, not business logic.
```sql
-- models/staging/stg_sessions.sql
select id, cast(started_at_str as date) as started_at
from {{ source('raw', 'sessions') }}
```
```
