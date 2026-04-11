---
name: dbt Three-Layer Transformation Model
description: The staging → intermediate → marts model gives each layer a clear, non-overlapping responsibility; best suited to multi-team analytics orgs with 10+ data sources.
type: context
sources:
  - https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
  - https://docs.getdbt.com/best-practices/how-we-structure/2-staging
  - https://docs.getdbt.com/best-practices/how-we-structure/4-marts
  - https://docs.getdbt.com/best-practices/best-practice-workflows
related:
  - docs/context/elt-vs-etl-workload-boundary.context.md
  - docs/context/data-quality-three-tier-model.context.md
  - docs/context/data-contracts-scope-and-incentive-alignment.context.md
  - docs/context/schema-evolution-expand-contract-pattern.context.md
---

# dbt Three-Layer Transformation Model

The three-layer model — staging → intermediate → marts — gives each layer a distinct, non-overlapping responsibility and is the consensus structure for multi-team analytics orgs. Smaller teams may not need the intermediate layer; the pattern is overhead-justified at scale.

## Layer Responsibilities

**Staging layer** — source-conformed atomic units.
- One model per source table, named `stg_[source]__[entity]s` (double underscore separates source system from entity)
- Materialized as views (cheap to maintain, no incremental complexity)
- Only type casting, renaming, and basic computation — no joins, no aggregations
- Subdirectories organized by source system, not business domain (enables `dbt build --select staging.stripe+`)
- This layer is the only place raw source names appear; everything downstream uses business terminology

**Intermediate layer** — composition without business meaning.
- `int_` prefix models assemble multi-source logic needed before mart-level joins
- Named for the transformation being performed, not a business concept
- Use this layer when a mart would otherwise require 5+ CTEs or join more than 4–5 concepts
- Materialized as views or ephemeral — escalate to tables only when build time demands it

**Marts layer** — business-entity-grain tables for consumption.
- Named after business entities (`customers`, `orders`), not technical concepts
- Denormalized: repeated join computation moved here so analysts don't repeat it
- Start as views; graduate to tables when query performance degrades; use incremental models when table build time exceeds acceptable thresholds
- dbt Labs guidance: avoid model-name prefixes at the mart level; Kimball-influenced teams add `fct_`/`dim_` — choose one convention and enforce it consistently

## When to Use (and When Not To)

The three-layer model pays off at scale: teams of 5+ engineers, 10+ data sources, multiple consuming teams. dbt's own guidance notes "if you have fewer than 10 marts you may not need subfolders" — an implicit acknowledgment that full pattern adherence is only justified above a size threshold.

For smaller teams or simpler pipelines, a two-layer approach (raw → consumption) is often sufficient. The intermediate layer adds overhead that is only justified when marts would otherwise accumulate complex multi-source join logic.

**Materialization caveat for Databricks users.** The default-to-views guidance is appropriate for BigQuery and Snowflake. In large Databricks Unity Catalog environments, Delta tables are the platform default — applying dbt's warehouse-agnostic view-first guidance introduces significant build-time overhead not present in other warehouses.

## Key Naming Rules

- snake_case everywhere: schemas, tables, columns
- Plural model names (`customers`, not `customer`)
- Primary key pattern: `[table]_id`
- Boolean prefix: `is_` or `has_`
- Timestamps: `_at` suffix in UTC; dates: `_date` suffix
- Avoid abbreviations; use business terminology, not source system terminology

## Takeaway

The three-layer model moves data from source-conformed to business-conformed through clearly bounded layers. The staging layer is the boundary between raw and governed; the intermediate layer contains composition; the marts layer contains business definitions. Apply the full model at scale, simplify for smaller projects, and always validate the materialization strategy against your specific warehouse.
