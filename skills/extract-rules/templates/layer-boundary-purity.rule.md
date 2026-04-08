---
name: Layer boundary purity
description: Data transformation layers must not contain logic belonging to other layers
type: rule
scope: "models/staging/**/*.sql"
severity: warn
---

## Intent

Each data transformation layer has a specific responsibility. When logic
bleeds across layers, changes in one layer cascade unpredictably to others.
Keeping layers pure makes each independently testable and maintainable.

## Non-Compliant Example

```sql
-- models/staging/stg_orders.sql
select
    id as order_id,
    cast(order_date as date) as order_date,
    quantity * unit_price * (1 - discount) as revenue,  -- business logic
    case
        when total_spent > 1000 then 'premium'          -- business logic
        else 'standard'
    end as customer_tier
from {{ source('raw', 'orders') }}
```

Violations: revenue calculation and customer segmentation are business
logic. Staging should only cast, rename, and deduplicate.

## Compliant Example

```sql
-- models/staging/stg_orders.sql
select
    id as order_id,
    cast(order_date as date) as order_date,
    cast(quantity as integer) as quantity,
    cast(unit_price as numeric(10,2)) as unit_price,
    cast(discount as numeric(5,2)) as discount_rate
from {{ source('raw', 'orders') }}
qualify row_number() over (partition by id order by _loaded_at desc) = 1
```

Only casts, renames, and deduplication. Business logic belongs in
downstream transformation layers.
