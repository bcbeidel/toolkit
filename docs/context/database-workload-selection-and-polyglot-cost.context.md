---
name: Database Workload Selection and Polyglot Persistence Cost
description: Database selection is workload-driven; polyglot persistence is correct at scale for divergent access patterns but adds significant operational burden that small teams consistently underestimate.
type: context
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/understand-data-store-models
  - https://www.influxdata.com/blog/database-ecosystem-guide-2025/
  - https://mactores.com/blog/right-use-cases-for-relational-db-document-db-graph-db-time-series-db-and-in-memory-db
  - https://blog.bytebytego.com/p/database-schema-design-simplified
related:
  - docs/context/orm-n-plus-one-eager-loading-dto-projection.context.md
  - docs/context/composite-index-ordering-equality-first-rule.context.md
  - docs/context/schema-evolution-expand-contract-pattern.context.md
---

# Database Workload Selection and Polyglot Persistence Cost

Choose the database engine based on the actual access pattern and consistency requirements of the workload, not based on familiarity or recency. Polyglot persistence is correct when access patterns genuinely diverge, but each additional engine adds operational overhead — expertise, monitoring, backups, governance — that most teams underestimate.

## Workload-Based Selection Table

| Need | Prefer |
|------|--------|
| Strict multi-entity transactions | Relational (PostgreSQL, MySQL) |
| Evolving aggregate shape, JSON-centric APIs | Document (MongoDB, DynamoDB) |
| Extreme low-latency key lookups or caching | Key-value (Redis, DynamoDB in KV mode) |
| Wide, sparse, write-heavy telemetry | Column-family (Cassandra) or time-series |
| Deep relationship traversal | Graph (Neo4j, Amazon Neptune) |
| Massive historical analytical scans | OLAP / analytics warehouse |
| Full-text relevance and filtering | Search index (Elasticsearch, OpenSearch) |
| High-ingest timestamp metrics with window queries | Time-series (InfluxDB, TimescaleDB) |
| Rapid similarity search (semantic, vector) | Vector search (Pinecone, Qdrant, pgvector) |

Do not select a database by familiarity or by matching a technology trend. Re-evaluate when workload characteristics change.

## Normalization vs. Denormalization

Schema design is a spectrum, not a binary:
- **Normalize for correctness** — eliminates redundancy, enforces referential integrity, simplifies writes
- **Denormalize for measured performance** — reduces join depth for read-heavy workloads where join cost compounds at scale

At millions of rows, a fully normalized schema requiring 6+ joins per query can degrade in ways that indexing alone cannot offset. The counterpoint: denormalization complicates write paths and creates consistency obligations. The correct approach: design with normalization initially, measure actual query patterns, denormalize where specific queries have documented performance problems.

## The Polyglot Persistence Tradeoff

Using multiple database engines for different workloads (polyglot persistence) is technically correct at scale when access patterns genuinely diverge — a relational DB for transactional records, a time-series DB for metrics, Redis for session caching. Most large production systems at scale adopt polyglot persistence.

The operational cost is real and significant:
- Each engine requires dedicated expertise for deployment, scaling, tuning, and backup
- Cross-database consistency is not achievable via ACID transactions — polyglot architectures require saga patterns, event sourcing, or outbox integration for cross-store writes
- Monitoring, alerting, and observability must be configured per engine
- Developer experience degrades as teams context-switch between query languages and data models

The most common failure mode: a team adds a second database engine without operational maturity (no monitoring, no backup strategy, no documented runbook), creating a reliability liability, not a reliability improvement.

## Re-Evaluation Signals

These patterns indicate it's time to consider adding a database engine:
- Increasing ad-hoc joins on a document store → introduce a relational read model
- Large denormalized documents with high partial-update contention → reshape aggregates or split to relational
- Time-window aggregate queries slowing on column-family store → adopt a purpose-built time-series database
- Repeated full-text search on a relational DB → introduce a search index as a read replica

## 2025 Ecosystem Trend

Leading databases (PostgreSQL, MongoDB) are adding multi-modal capabilities: analytics queries, vector search, and semi-structured data support in a single engine. Open formats (Parquet, Arrow, Iceberg) reduce lock-in across engine choices. This trend means the threshold for introducing a specialized engine is rising — PostgreSQL with pgvector can handle many vector workloads that previously required Pinecone.

## Takeaway

Single-engine architectures are operationally simpler and should be the default for teams without deep database operations expertise. Introduce additional engines only when a specific workload pattern cannot be served acceptably by the existing engine, and when the team has operational capacity to manage the additional complexity. Polyglot persistence is a capability boundary, not a best-practice default.
