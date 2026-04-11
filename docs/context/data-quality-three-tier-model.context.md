---
name: Data Quality Three-Tier Model
description: Data quality requires three distinct tiers — build-time tests, scheduled monitoring, and runtime observability — but most teams operate only the first.
type: context
sources:
  - https://www.sparvi.io/blog/great-expectations-vs-dbt-tests
  - https://www.elementary-data.com/post/data-contracts
  - https://www.startdataengineering.com/post/de_best_practices/
related:
  - docs/context/dbt-three-layer-transformation-model.context.md
  - docs/context/data-contracts-scope-and-incentive-alignment.context.md
  - docs/context/elt-vs-etl-workload-boundary.context.md
---

# Data Quality Three-Tier Model

Most teams treat data quality as a testing problem: validate at build time and move on. Production pipelines require two additional tiers — scheduled monitoring and runtime observability — that test-time validation cannot cover.

## The Three Tiers

**Tier 1 — Build-time testing (most teams have this).**
Tests embedded in the transformation layer, run during CI/CD or on schedule:
- Every model: primary key uniqueness + not_null at minimum (this is the floor, not the target)
- Beyond minimum: `accepted_values` for categoricals, `relationships` for foreign key integrity
- Tools: native dbt tests, `dbt-expectations`, `dbt-utils`
- Use `result:<status>` selectors to re-run only failing tests in CI without re-running the full suite
- Great Expectations (GX) is capable but adoption friction is severe — most teams find dbt-native packages sufficient for 80–90% of use cases without GX's operational overhead

**Tier 2 — Scheduled monitoring (few teams have this).**
Periodic checks against live production data:
- Freshness SLAs: is this table updated within its expected window?
- Row count anomaly detection: did this pipeline produce significantly fewer rows than expected?
- Schema change alerting: did an upstream source change its column names or types?
- Tools: Elementary (dbt package), Monte Carlo, Metaplane, SYNQ
- Tier 2 catches failures that only manifest in production data, not in transformation logic

**Tier 3 — Runtime observability (almost no teams have this).**
Continuous anomaly detection on production data patterns:
- Statistical distribution drift: are value distributions shifting unexpectedly?
- Volume anomalies: sudden drops in pipeline throughput
- Cross-table consistency: metrics that should agree across joins diverging over time
- Tools: Monte Carlo, SYNQ (commercial platforms), purpose-built ML monitoring
- This tier catches the class of failures that neither testing nor scheduled checks anticipate

## Why Most Teams Stop at Tier 1

Build-time tests are the natural starting point: they're integrated into the development workflow, produce immediate CI feedback, and require no additional infrastructure. The missing tiers require investment in monitoring tooling, alerting infrastructure, and operational runbooks — overhead that teams defer until a production incident makes the gap visible.

The risk: a pipeline can pass all Tier 1 tests and still deliver wrong answers to stakeholders. Schema changes from upstream application engineers, volume drops from source system issues, and freshness SLA violations all fall outside what build-time tests can catch.

## Practical Upgrade Path

1. **Establish Tier 1 baseline first.** Every model must pass PK uniqueness and not_null before adding monitoring complexity.
2. **Add freshness and row-count checks for critical tables.** These are the highest-value Tier 2 additions and often built into dbt's native `freshness` block or Elementary.
3. **Evaluate Tier 3 tooling only for business-critical pipelines.** Commercial observability platforms have real cost; apply selectively, not wholesale.

## Takeaway

Build-time testing is necessary but not sufficient for production data quality. Design your data quality strategy across all three tiers, even if only Tier 1 is implemented initially. The absence of Tier 2 and Tier 3 is a known gap in most teams' quality posture, not a validated decision.
