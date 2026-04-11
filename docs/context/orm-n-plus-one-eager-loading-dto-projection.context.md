---
name: ORM N+1, Eager Loading, and DTO Projection
description: N+1 is the primary ORM anti-pattern; eager loading solves it for full object graphs; DTO projection is the superior alternative for narrow field selection.
type: context
sources:
  - https://www.prisma.io/docs/orm/more/best-practices
  - https://blog.appsignal.com/2020/06/09/n-plus-one-queries-explained.html
related:
  - docs/context/database-workload-selection-and-polyglot-cost.context.md
  - docs/context/composite-index-ordering-equality-first-rule.context.md
  - docs/context/schema-evolution-expand-contract-pattern.context.md
---

# ORM N+1, Eager Loading, and DTO Projection

N+1 queries are the default failure mode of lazy-loading ORMs. At scale, the difference between an N+1 query and a properly structured query is the difference between a working app and an unusable one. Eager loading solves N+1 for full object graphs; DTO projection is superior when only a subset of fields is needed.

## The N+1 Pattern

N+1 occurs when:
1. A query retrieves N records: `SELECT * FROM posts` (1 query)
2. For each record, a separate query fetches related data: `SELECT * FROM comments WHERE post_id = ?` × N (N queries)

Total: 1 + N queries. At 1,000 records, this is 1,001 database round-trips for what should be 1 or 2. Controlled benchmarks show 80% query time reduction (290ms → 58ms at 1,000 records) when N+1 is eliminated — though these numbers are from specific test conditions and should not be used as general guarantees without measurement on your workload.

N+1 is the default behavior of lazy-loading ORMs (ActiveRecord is the highest-risk ORM for this; Rails developers must explicitly use `includes` or `eager_load`). It is silent in development at low data volumes and becomes a production crisis at scale.

## Eager Loading: The Standard Fix

Use the ORM's `include` (Prisma), `preload`/`eager_load` (ActiveRecord), `select_related`/`prefetch_related` (Django ORM) to load related data in a single query using IN filters:

Instead of N queries: `SELECT * FROM comments WHERE post_id = 1` ... `SELECT * FROM comments WHERE post_id = N`

One query: `SELECT * FROM comments WHERE post_id IN (1, 2, ..., N)`

This reduces N+1 to 2 queries regardless of dataset size.

**When eager loading underperforms:** Loading a full `User + Profile + Orders + Preferences` object graph when only `username` is required wastes memory and bandwidth. Eager loading can increase data transferred when relationship depth is deep and field selection is narrow. In some ORMs, eager loading can actually increase query count when used incorrectly.

## DTO Projection: Superior for Read-Heavy Endpoints

DTO (Data Transfer Object) projection fetches only the specific fields required, directly into a typed transfer object, in a single query. This bypasses both the N+1 problem and the over-fetching that eager loading introduces:

```sql
-- Instead of loading full User + Profile objects:
SELECT u.id, u.name, p.avatar_url 
FROM users u JOIN profiles p ON p.user_id = u.id
WHERE u.id IN (...)
```

Use DTO projection for:
- Read-heavy endpoints where field selection is narrow
- APIs returning large result sets where serialization overhead matters
- Endpoints where relationship depth is deep but consumers need few fields

Use eager loading for:
- Endpoints that return full domain objects
- CRUD operations where the full entity graph is needed

## ORM Best Practices (Prisma / General)

- Create one global ORM client instance — multiple instances exhaust connection pool limits
- Index all fields used in `WHERE`, `ORDER BY`, and join predicates — ORMs do not add indexes automatically
- Use cursor-based pagination for large datasets; offset pagination only for small datasets
- Use batch operations (`createMany`, `updateMany`, `deleteMany`) — they run as transactions
- In production: use `migrate deploy`, never `migrate dev` — the dev command risks data loss
- In serverless: instantiate ORM client outside handler functions to reuse connections

## Takeaway

Identify N+1 during development with query logging enabled — it is invisible in small datasets and catastrophic at scale. Eager loading is the standard fix for full object graph fetching. Prefer DTO projection for read-heavy endpoints with narrow field selection. Assess hot paths before committing to an ORM abstraction level, not after performance problems surface.
