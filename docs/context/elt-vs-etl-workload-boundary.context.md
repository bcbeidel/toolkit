---
name: ELT vs ETL Workload Boundary
description: ELT is the analytics default; ETL remains correct for streaming, IoT, and regulated workloads — the two are not interchangeable.
type: context
sources:
  - https://www.getdbt.com/blog/data-integration
  - https://www.startdataengineering.com/post/de_best_practices/
related:
  - docs/context/dbt-three-layer-transformation-model.context.md
  - docs/context/data-quality-three-tier-model.context.md
  - docs/context/schema-evolution-expand-contract-pattern.context.md
---

# ELT vs ETL Workload Boundary

ELT is the analytics engineering default for batch and BI workloads. ETL remains the correct choice for streaming, IoT, and regulated pipelines. Treating "ELT is the standard" as a universal claim overstates the consensus and leads teams astray on real-time or compliance-constrained projects.

## ELT: Where It Applies

ELT (Extract → Load → Transform) works because modern cloud warehouses (BigQuery, Snowflake, Databricks) have sufficient compute to run transformations in-platform. Load raw data first, then transform using SQL. This pattern is cheaper, faster to iterate, and better-aligned with tools like dbt. It is the dominant architecture for analytics and BI workloads.

ELT assumes:
- A cloud warehouse or lakehouse as the central hub
- Batch or near-batch data ingestion
- Transformations are SQL-expressible and run downstream of loading

## ETL: Where It Remains Correct

ETL (Extract → Transform → Load) is still the appropriate default in three classes of workloads:

**Streaming and IoT pipelines.** Real-time sensor data often requires protocol normalization or schema coercion before load. Kafka-based pipelines (Kafka Streams, Flink) commonly perform in-stream transformation — ETL semantics — not ELT.

**Regulated workloads.** Industries with data-residency requirements or pre-load masking/encryption mandates (healthcare, finance) cannot write raw PII to a warehouse and transform after. Transformation before load is the compliance-correct sequence.

**Operational pipelines.** Fraud detection, feature engineering for real-time inference, and reverse ETL (pushing data back to operational systems) do not fit the warehouse-centric ELT model.

## The Distinction Matters in Practice

Selecting the wrong model introduces real problems:
- Applying ELT to a streaming IoT workload yields latency and ordering issues not present in a purpose-built ETL pipeline.
- Applying ETL patterns to analytics workloads adds unnecessary pre-load complexity and loses the iterability benefit of in-warehouse transformation.

Zero-ETL architectures (direct operational DB → warehouse CDC feeds) blur this further, but they are a narrow integration pattern, not a replacement for either paradigm.

## Takeaway

Scope "ELT is the standard" to analytics and BI workloads specifically. If the workload is real-time, involves edge/IoT devices, or has pre-load compliance requirements, evaluate ETL-first or hybrid architectures. The correct framing: **ELT is the analytics engineering default, not the universal default.**
