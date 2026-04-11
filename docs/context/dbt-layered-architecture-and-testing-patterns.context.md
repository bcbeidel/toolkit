---
name: "dbt Layered Architecture and Testing Patterns"
description: "dbt's three-tier architecture (staging → intermediate → mart) is the canonical transformation pattern. Use dbt tests for schema contracts, Great Expectations for complex source quality. Dimensional modeling remains dominant in 90%+ of enterprise warehouses."
type: entity
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.datadoghq.com/blog/understanding-dbt/
  - https://www.sparvi.io/blog/great-expectations-vs-dbt-tests
  - https://ghostinthedata.info/posts/2025/2025-11-07-effective-data-modelling/
  - https://www.getdbt.com/blog/state-of-analytics-engineering-2025-summary
related:
  - docs/context/semantic-layer-as-ai-analytics-infrastructure.context.md
  - docs/context/data-governance-failure-modes-and-federated-model.context.md
---
# dbt Layered Architecture and Testing Patterns

dbt's three-tier architecture (staging → intermediate → mart) is the canonical transformation pattern for analytics engineering, used in 8,200+ companies globally. dbt tests handle lightweight schema contracts; Great Expectations handles complex source data quality. Dimensional modeling remains the dominant paradigm in enterprise data warehouses, though wide-table patterns are gaining ground.

## The Three-Tier Architecture

**Staging layer** — one model per source system entity. Responsibilities: rename columns to consistent conventions, cast data types, apply unit conversions. No joins, no aggregations. Materialize as views (no storage cost, always fresh). Naming: `stg_<source>__<entity>s.sql`.

**Intermediate layer** — apply joins, filters, and calculated metrics. Organized by business domain (orders, customers, sessions). Re-grain data where needed (shift granularity from events to sessions, sessions to users). Verb-based naming: `int_orders_joined`, `int_users_aggregated_to_session`. Materialize as views or ephemeral models.

**Marts layer** — stable, trusted models aligned with business entities. Grouped by stakeholder teams (marketing mart, finance mart, product mart). Minimize joins at this layer — pre-join where query performance requires it. Materialize as tables. These are the models that BI tools and semantic layer definitions reference.

The three tiers enforce a discipline that prevents the most common analytics engineering failure: business logic accumulating in BI tools or ad-hoc scripts rather than in version-controlled, tested, documented SQL models.

## Testing Strategy: dbt vs. Great Expectations

**dbt built-in tests** (four generic types): `unique`, `not_null`, `accepted_values`, `relationships`. Run as SQL queries in-warehouse. Fast, version-controlled, part of the CI/CD pipeline. Appropriate for transformation logic validation: uniqueness constraints, referential integrity, enumeration validation.

**Great Expectations** (300+ expectations): Python-based, runs outside the warehouse. Supports non-dbt data sources. Auto-generates Data Docs (HTML data quality reports). Appropriate for source data quality validation as data enters the warehouse — before transformations have run.

**Recommended approach**: run Great Expectations on source data at ingestion; run dbt tests on transformed models. The `dbt-expectations` package (originally Calogica, maintained by Metaplane) bridges both within dbt's YAML framework, enabling Great Expectations-style assertions without leaving the dbt toolchain.

**Data contracts**: enable `contract: enforced: true` in dbt model config to machine-enforce schema stability agreements between model producers and downstream consumers. Reduces silent breakages and makes root cause analysis faster when contracts are violated.

## Data Modeling Patterns

**Dimensional modeling (Kimball methodology)** remains the standard in over 90% of enterprise data warehouses — a practitioner estimate from Ghost in the Data (Nov 2025), consistent with official recommendations from Snowflake, Databricks, BigQuery, and Microsoft Fabric. Real-world scale: Uber, Spotify, and Netflix all use dimensional models at petabyte scale.

Key dimensional modeling principles:
- Fact tables: immutable business events (transactions, sessions, orders) with foreign keys to dimension tables
- Dimension tables: business entities (customers, products, geographies) with rich descriptive attributes
- Star schema: fact table at center, single-hop joins to dimensions — optimized for analytical query patterns

**Wide tables (One Big Table)**: pre-join fact and dimension data into a single denormalized table. Simpler for analysts initially, but creates maintenance problems as business logic changes: updates require modifying a single large model that many downstream consumers depend on. A Fivetran study found wide tables are 25–50% faster on some cloud warehouses — the tradeoff between performance and maintainability is real.

**Hybrid approach**: use normalized Data Vault or integration-layer models (Bronze/Silver) for auditability and handling source system changes; use dimensional models in the presentation layer (Gold) for business consumption and self-service BI.

## 2025 Context

56% of analytics engineering practitioners identify data quality as a persistent problem (State of Analytics Engineering 2025, dbt Labs). AI use in dbt workflows has reached 80% of practitioners — primarily for generating boilerplate YAML, dbt tests, and documentation. The semantic layer becomes critical infrastructure as AI tools in BI require pre-defined, deterministic metric definitions rather than inferred table join logic.

## Bottom Line

Apply the three-tier architecture consistently — staging cleans, intermediate joins and re-grains, marts serve business entities. Use both dbt tests and Great Expectations: each covers a different quality layer. Dimensional modeling is the safe default for enterprise warehouse design; validate against wide-table alternatives empirically when query performance is a constraint.
