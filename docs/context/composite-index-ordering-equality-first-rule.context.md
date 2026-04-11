---
name: Composite Index Ordering — Equality First Rule
description: Place equality conditions first and range conditions last in composite indexes — the common "most selective column first" heuristic is wrong and can produce useless indexes.
type: context
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide?view=sql-server-ver17
related:
  - docs/context/orm-n-plus-one-eager-loading-dto-projection.context.md
  - docs/context/database-workload-selection-and-polyglot-cost.context.md
---

# Composite Index Ordering — Equality First Rule

The most commonly repeated composite index heuristic — "put the most selective column first" — is wrong. The correct rule is: equality conditions first, range conditions last. A highly selective column placed first that is not in the query's WHERE clause produces an index the query cannot use at all.

## The Correct Rule

**Equality conditions first, range conditions last.**

Given a query like:
```sql
WHERE status = 'active' AND created_at > '2025-01-01'
```

The correct index column order is `(status, created_at)`:
- `status` is an equality condition (`=`) — it pins the index scan to a specific value
- `created_at` is a range condition (`>`) — it scans from that position forward

If the index were `(created_at, status)`, queries filtering only on `status` cannot use the index at all (leftmost prefix rule).

## The Leftmost Prefix Rule

An index on `(A, B, C)` can serve queries filtering on:
- `A` alone
- `A + B`
- `A + B + C`

It cannot serve queries filtering on `B` alone or `C` alone. This is non-negotiable — it is how B-tree indexes are physically organized.

## Why "Most Selective First" Is Wrong

"Most selective first" means placing the column with the highest cardinality (most unique values) at the leading position. This is explicitly identified as a myth by use-the-index-luke.com: "The myth that you should always put the most selective column to the first position is just wrong."

The selectivity rule applies only in one narrow, specific scenario: when you have two independent range conditions and need to choose which comes first — in that case, the more selective column narrows the scan faster. This exception does not generalize to composite index design.

A highly selective column in position 1 is useless for any query that doesn't filter on that column. The index must match query access patterns, not statistical properties of the data.

## Covering Indexes: The Performance Ceiling

A covering index contains every column a query needs — predicates, order-by columns, and selected columns — allowing the database to serve the entire query from the index without touching the underlying table.

A single well-placed covering index can reduce query latency by an order of magnitude on high-frequency queries. Reserve covering indexes for:
- High-frequency queries on large tables
- Queries where every eliminated table access matters

## Practical Index Design Checklist

1. Identify the query's WHERE clause predicates and ORDER BY columns
2. Place equality conditions in the index first (in any order among themselves)
3. Place range conditions last
4. Add ORDER BY columns after range conditions if they match the sort direction
5. Consider adding SELECT columns last to create a covering index for critical queries
6. Verify with EXPLAIN/EXPLAIN ANALYZE that the query uses the index; unused indexes waste disk space and slow writes

## Takeaway

Design composite indexes by query access pattern, not column selectivity. Equality conditions come first; range conditions come last; covering index additions come after that. The leftmost prefix rule determines whether an index is usable at all — column ordering that violates it produces an index the query optimizer will ignore.
