---
name: "Analytics Engineering"
description: "Analytics engineering bridges data engineering and analysis by applying software engineering practices to data transformation; the field centers on dbt/MetricFlow as the dominant toolchain, with semantic layers becoming critical infrastructure for AI-ready, self-service analytics in 2025-2026."
type: research
sources:
  - https://www.getdbt.com/blog/what-is-analytics-engineering
  - https://www.getdbt.com/blog/state-of-analytics-engineering-2025-summary
  - https://www.getdbt.com/blog/open-source-metricflow-governed-metrics
  - https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl
  - https://docs.getdbt.com/docs/build/semantic-models
  - https://docs.getdbt.com/docs/build/metrics-overview
  - https://www.typedef.ai/resources/semantic-layer-architectures-explained-warehouse-native-vs-dbt-vs-cube
  - https://www.typedef.ai/resources/semantic-layer-metricflow-vs-snowflake-vs-databricks
  - https://www.activityschema.com/
  - https://www.ergestx.com/activity-schema/
  - https://ghostinthedata.info/posts/2025/2025-11-07-effective-data-modelling/
  - https://www.datadoghq.com/blog/understanding-dbt/
  - https://www.sparvi.io/blog/great-expectations-vs-dbt-tests
  - https://www.synq.io/blog/dbt-vs-sqlmesh-a-comparison-for-modern-data-teams
  - https://coalesce.io/data-insights/semantic-layers-2025-catalog-owner-data-leader-playbook/
  - https://www.ssp.sh/brain/metrics-layer/
related:
  - docs/research/2026-04-07-data-engineering.research.md
  - docs/research/2026-04-07-statistical-modeling.research.md
  - docs/research/2026-04-07-marketing-analytics.research.md
---

# Analytics Engineering

Analytics engineering is the discipline of applying software engineering practices (version control, testing, CI/CD, documentation) to data transformation, occupying the middle ground between data engineers who build infrastructure and analysts who consume insights. dbt remains the dominant toolchain with 8,200+ companies using it globally; the semantic layer — powered by MetricFlow (Apache 2.0 as of Coalesce 2025) — has become the critical interface between data models and AI-ready, self-service analytics. Data quality remains the field's top challenge, with 56% of practitioners identifying it as a persistent problem in 2025.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.getdbt.com/blog/what-is-analytics-engineering | What is analytics engineering? | dbt Labs | 2019 (foundational) | T1 | verified |
| 2 | https://www.getdbt.com/blog/state-of-analytics-engineering-2025-summary | The State of Analytics Engineering 2025 | dbt Labs | 2025 | T1 | verified |
| 3 | https://www.getdbt.com/blog/open-source-metricflow-governed-metrics | Announcing open source MetricFlow | dbt Labs | 2025 | T1 | verified |
| 4 | https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl | dbt Semantic Layer | dbt Developer Hub | 2024-2025 | T1 | verified |
| 5 | https://docs.getdbt.com/docs/build/semantic-models | Semantic models | dbt Developer Hub | 2024-2025 | T1 | verified |
| 6 | https://docs.getdbt.com/docs/build/metrics-overview | Creating metrics (MetricFlow) | dbt Developer Hub | 2024-2025 | T1 | verified |
| 7 | https://www.typedef.ai/resources/semantic-layer-architectures-explained-warehouse-native-vs-dbt-vs-cube | Semantic Layer Architectures Explained | typedef.ai | 2025 | T2 | verified |
| 8 | https://www.typedef.ai/resources/semantic-layer-metricflow-vs-snowflake-vs-databricks | Semantic Layer 2025: MetricFlow vs Snowflake vs Databricks | typedef.ai | 2025 | T2 | verified |
| 9 | https://www.activityschema.com/ | Activity Schema | ActivitySchema.com (Ahmed Elsamadisi) | 2022, maintained | T2 | verified |
| 10 | https://www.ergestx.com/activity-schema/ | Exploring the ActivitySchema | ergest.x | 2023 | T3 | verified |
| 11 | https://ghostinthedata.info/posts/2025/2025-11-07-effective-data-modelling/ | Why Dimensional Modeling Isn't Dead — It's Just Getting Started | Ghost in the Data | Nov 2025 | T3 | verified |
| 12 | https://www.datadoghq.com/blog/understanding-dbt/ | Understanding dbt: basics and best practices | Datadog | 2024 | T2 | verified |
| 13 | https://www.sparvi.io/blog/great-expectations-vs-dbt-tests | Great Expectations vs dbt Tests (2025) | Sparvi | 2025 | T3 | verified |
| 14 | https://www.synq.io/blog/dbt-vs-sqlmesh-a-comparison-for-modern-data-teams | dbt vs SQLMesh: A Comparison For Modern Data Teams | SYNQ | 2025 | T3 | verified |
| 15 | https://coalesce.io/data-insights/semantic-layers-2025-catalog-owner-data-leader-playbook/ | Semantic Layers in 2025: A Catalog Owner and Data Leader Playbook | Coalesce.io | 2025 | T2 | verified |
| 16 | https://www.ssp.sh/brain/metrics-layer/ | Metrics Layer | Simon Späti | 2024 | T3 | verified |

## Search Protocol

| Query | Results | Selected |
|-------|---------|----------|
| analytics engineering 2025 definition role bridging data engineering analysis | 10 | 2 (dbt Labs blog, State of AE 2025) |
| dbt MetricFlow semantic layer 2025 | 10 | 3 (open source MetricFlow announcement, dbt SL docs, typedef.ai comparison) |
| metrics layer design best practices 2025 headless BI | 10 | 2 (coalesce.io playbook, ssp.sh metrics layer) |
| data modeling star schema wide tables activity schema analytics engineering | 10 | 2 (ghostinthedata.info, activityschema.com) |
| activity schema analytics pattern wide event table 2024 2025 | 10 | 2 (activityschema.com, ergest.x) |
| analytics engineering tools workflow dbt 2025 best practices | 10 | 2 (dbt Labs state of AE, Datadog dbt guide) |
| data testing dbt great expectations analytics engineering 2025 | 10 | 2 (sparvi.io comparison, dbt State of AE) |
| Cube semantic layer vs dbt metrics comparison 2025 | 10 | 2 (typedef.ai architectures, semantic layers buyer guide) |
| self-service analytics data modeling patterns 2025 dimensional modeling | 10 | 2 (ghostinthedata.info dimensional modeling, dbt ThoughtSpot guide) |
| dbt documentation best practices data contracts analytics engineering 2025 | 10 | 2 (dbt Labs blog, Datadog dbt guide) |
| analytics engineering open source tools SQLMesh dbt alternatives 2025 | 10 | 2 (SYNQ dbt vs SQLMesh, Coalesce alternatives list) |
| dbt semantic model YAML syntax MetricFlow example measure dimension entity 2025 | 10 | 2 (dbt docs semantic-models, metriclayer.dev) |
| "analytics engineering" "data mesh" domain ownership 2025 platform team | 10 | 1 (dbt Labs data mesh blog) |

## Extracts

### Sub-question 1: What is analytics engineering and how does it bridge data engineering and data analysis?

**Origin and history [1]:** Before 2012, data teams had data engineers (infrastructure) and analysts (reports). Cloud data warehouses, pipeline services like Fivetran, and self-service BI tools changed the landscape. By 2016, analysts had SQL skills but created data inconsistency problems. The demand to transform raw data without waiting in engineering queues created a new specialist role; the title "analytics engineer" was formally adopted around 2018.

**Definition [1]:** Analytics engineers provide clean, reliable datasets to end users by modeling data that empowers them to answer their own questions. They "transform, test, deploy, and document data" while applying software engineering best practices like version control and CI/CD.

**Bridging role [1]:** Data engineers focus on infrastructure — ingestion, storage, orchestration, the systems that move data. Analytics engineers focus on transformation — taking raw data and shaping it into models ready for analysis. Data analysts focus on insights and reporting from those models. The phrase used by dbt Labs: "Data engineers build the plumbing; analytics engineers shape the water into something people can drink."

**2025 role evolution [2]:** The analytics engineer role is experiencing significant boundary blurring. At larger organizations, a 3:2:1 ratio between analysts, analytics engineers, and visual analytics engineers emerges. Some analytics engineers shift toward traditional data engineering tasks; others shift toward direct business stakeholder work. Adoption has spread beyond tech (34% of users) to financial services (15%) and healthcare (10%).

**2025 scale [2]:** Over 8,200 companies globally use dbt. 80% of data practitioners use AI in some way as part of their workflows. 56% of survey respondents identified data quality as a persistent problem. 65% of organizations recognize that enabling non-technical business users to create governed datasets would enhance data value.

---

### Sub-question 2: How should metrics layers and semantic layers be designed (dbt metrics, MetricFlow, Cube)?

**MetricFlow open-sourcing [3]:** At Coalesce 2025, dbt Labs announced MetricFlow is open-sourced under Apache 2.0 license, with the Open Semantic Interchange (OSI) initiative partnering Snowflake and Salesforce for metrics interoperability. The JSON-based metadata layer is now a universal schema for understanding data across tools without vendor lock-in.

**MetricFlow core principle [3]:** "Metrics should not be probabilistic or depend on an LLM guessing each calculation. They should be deterministic." MetricFlow handles multi-dialect SQL generation, join logic, window functions, cohort analysis, semi-additive measures, and time grain alignment. AI systems using the semantic layer achieved 83% accuracy on addressable questions vs. substantially lower prompt-only accuracy.

**MetricFlow YAML structure [5, 6]:** Semantic models are YAML abstractions on top of dbt models. Full example:

```yaml
semantic_models:
  - name: ecommerce_orders
    model: ref('stg_orders')
    defaults:
      agg_time_dimension: order_date
    entities:
      - name: order
        type: primary
      - name: customer
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: channel
        type: categorical
    measures:
      - name: total_revenue
        agg: sum
        expr: revenue

metrics:
  - name: revenue
    type: simple
    label: "Total Revenue"
    type_params:
      measure: total_revenue
```

**Metric types [6]:** MetricFlow supports five types: `simple` (aggregation of a measure), `cumulative` (rolling window), `derived` (formula over other metrics), `ratio` (numerator/denominator), and `conversion` (event-to-event funnel). Filter syntax uses Jinja templating: `{{ Dimension('primary_entity__dimension_name') }}`, `{{ TimeDimension('time_dimension', 'granularity') }}`.

**Three semantic layer architectures [7]:**

| Factor | Warehouse-Native (Snowflake/Databricks) | Transformation-Layer (dbt MetricFlow) | OLAP-Acceleration (Cube.dev) |
|--------|------------------------------------------|---------------------------------------|------------------------------|
| Performance | 2-10 seconds (complex queries) | Warehouse-dependent | Sub-second (cached) |
| Data Freshness | Real-time | Real-time | Minutes/hours delay |
| Infrastructure | None required | Minimal API server | Significant (cluster + storage) |
| Multi-warehouse | Single vendor only | Fully supported | Fully supported |
| Governance | Native warehouse RBAC | Git-based + dbt Cloud | Application-level RBAC |
| Best for | Single-warehouse, governance-heavy | Multi-cloud, dbt-native teams | High-concurrency, cost optimization |

**Cube.dev [7]:** Cube defines and serves metrics via API with pre-aggregation caching, delivering sub-second query speeds (50-500ms), handling 100-1,000 queries per second. Best for embedded analytics and high-concurrency dashboards. Maintains a fully open-source core deployable on-premises.

**Headless BI design principles [15, 16]:** Metrics definitions should live in version-controlled text files (YAML or JSON) with peer-review workflow. Start with 10-20 "tier-0" metrics (revenue, churn, CAC) and manually re-engineer their logic — do NOT auto-migrate. Symmetric aggregates and complex calculations require explicit redesign. A well-designed semantic layer serves as a critical component for AI, providing pre-defined metrics an LLM can reference by name instead of hallucinating table joins.

---

### Sub-question 3: What data modeling patterns for analytics produce self-service-ready datasets?

**Dimensional modeling remains dominant [11]:** Over 90% of enterprise data warehouses employ Kimball's methodology. Modern platforms (Snowflake, Databricks, BigQuery, Microsoft Fabric) all officially recommend dimensional designs for analytical workloads. Real-world scale: Uber (100+ petabytes using dimensional fact/dimension tables), Spotify (500 billion daily events), Netflix (petabyte-scale dimensional models).

**dbt layered architecture [12]:** The canonical three-tier structure:

1. **Staging layer:** Rename columns, cast data types, perform unit conversions. No joins or aggregations. Organize by source system. Naming: `stg_<source>__<entity>s.sql`. Materialize as views.

2. **Intermediate layer:** Apply joins, filters, calculated metrics. Organized by business domain. Verb-based naming: `int_orders_joined`, `int_users_aggregated_to_session`. Re-grain data to shift granularity.

3. **Marts layer:** Stable, trusted models aligned with business entities. Grouped by stakeholder needs. Materialize as tables when performance requires. Minimize joins.

**Hybrid architecture [11]:** Use normalized/Data Vault models in integration layers (Bronze/Silver) for auditability and handling source system changes; use dimensional models in presentation layers (Gold) for business consumption and self-service BI.

**Wide tables vs. star schema [11]:** Wide tables are simpler initially but create maintenance nightmares and duplicate business logic across teams. Star schemas are more maintainable — denormalized dimensions trade storage for query speed, enabling single-hop joins from fact to dimension tables. The "analytical layer" denormalizes data into wider, purpose-built tables optimized for specific patterns, with pre-joined tables reducing query complexity.

**Activity Schema pattern [9, 10]:** An open-source framework that structures all analytics data as a single time-series table, eliminating complex dependency chains. Core structure:

- **Activity stream table:** 11-column standardized structure: `activity_id`, `timestamp`, `activity_type`, `customer_id`, three feature fields, `revenue`, `link`, `occurrence_count`, `activity_repeated_at` (pre-computed next occurrence for efficient windowing)
- **Optional enrichment table:** Supplementary dimensions joined via `enriched_activity_id` and `enriched_ts`

Temporal join patterns (11 total): `first_ever`, `last_ever`, `first_before`, `last_before`, `first_after`, `last_after`, `first_in_between`, `last_in_between`, `aggregate_in_between`, plus aggregate relationships. Append-only design prevents historical record modification. Trade-off: simpler lineage and incremental updates, but less suited for complex multi-entity analysis than star schema.

**Data Vault 2.0 [11]:** Better for auditability and handling source system changes; less optimized for end-user query performance. Commonly used in regulated industries (financial services, healthcare) where audit trails are required.

---

### Sub-question 4: How should data testing and documentation be integrated into analytics workflows?

**dbt built-in testing [12]:** Four built-in generic test types: `unique`, `not_null`, `accepted_values`, `relationships`. Example: running a uniqueness test on `customer_id` prevents silent duplication. Also supports `source freshness` blocks to validate data has been recently updated. Tests run as SQL queries directly in-warehouse.

**dbt vs. Great Expectations [13]:**

| Aspect | dbt Tests | Great Expectations |
|--------|-----------|-------------------|
| Configuration | YAML-based | Python or YAML |
| Built-in Tests | 4 core types | 300+ expectations |
| Execution | In-warehouse SQL | Python runtime |
| Non-dbt Sources | No support | Yes |
| Documentation | dbt Docs | Auto-generated Data Docs |

**Recommended approach [13]:** Use both complementarily. Run Great Expectations on source data as it enters the warehouse (before transformations) to validate source systems; use dbt tests for transformation logic validation. The `dbt-expectations` package (maintained by Datadog) bridges both within dbt's YAML framework — Great Expectations-style tests without leaving dbt.

**Data contracts [2, 12]:** Data contracts are machine-enforced agreements ensuring dbt pipelines deliver consistent, schema-stable outputs. They define explicit agreements between producers and consumers on schema, freshness, and reliability. Enable by adding `contract: enforced: true` in model config. Reduces silent breakages and makes debugging faster when things go wrong.

**Documentation generation [12]:** `dbt docs generate` creates dependency graphs and lineage visualizations automatically. Enables tracing a marketing dashboard metric all the way back to raw event ingestion. Critical for AI tools: providing adequate documentation and semantic layers significantly improves AI tool effectiveness — AI in dbt workflows achieved better results with proper documentation context.

**State of testing in 2025 [2]:** 54% of respondents expect AI to benefit testing/tracking code (up from 47% the prior year). AI-generated YAML for dbt tests is a primary use case. Building trust in data remains the top priority — unreliable data means unreliable AI outputs.

---

### Sub-question 5: What analytics engineering tools and workflows are current best-in-class?

**dbt (dominant standard) [2, 12]:** dbt Core (Apache 2.0, free) + dbt Cloud (managed, paid). Core features: SQL transformation, testing, documentation generation, automatic lineage, CI/CD integration. Integrates with Snowflake, BigQuery, Databricks, Redshift, DuckDB. dbt Cloud adds scheduling, dbt Copilot (AI code generation), dbt Mesh (cross-project dependencies), and the Semantic Layer API. Also acquired SDF (2024-2025) — a high-performance toolchain that can represent various SQL dialects and faithfully emulate popular data warehouses locally for instant pre-run feedback.

**SQLMesh (challenger) [14]:** Open source, Python-native analytics engineering framework. Key advantages: ~9x faster execution than dbt Core (via smart plan execution and virtual data environments), compile-time SQL validation via SQLGlot, automatic column-level lineage, built-in rollback safety. "Virtual Data Environments" use table fingerprinting instead of materializing copies, reducing storage/cost. Fivetran acquired both dbt and SQLMesh in 2025, fundamentally shifting competitive dynamics. Choose SQLMesh when: development speed is critical, Python-native logic preferred, incremental logic and rollback flexibility required.

**Semantic layer tools [7, 15]:**
- **dbt Semantic Layer + MetricFlow:** Git-based governance, multi-warehouse portability, integrates with Looker, Tableau, Hex, Mode. Production-ready as of October 2024. Best for dbt-native teams.
- **Cube.dev:** Open-source core, pre-aggregation caching, sub-second performance for cached queries, high concurrency. Best for embedded analytics and cost-sensitive use cases.
- **Snowflake Semantic Views / Cortex Analyst:** Warehouse-native, zero additional infrastructure, real-time data. Best for Snowflake-only organizations.
- **Databricks Metric Views / Unity Catalog:** Similar warehouse-native approach on Databricks.
- **AtScale, GoodData:** Universal/headless solutions for polyglot multi-BI environments.

**Data quality tools [13]:**
- **dbt-expectations** (originally Calogica, active fork at Metaplane): Great Expectations-style tests in dbt YAML
- **Great Expectations:** 300+ validations, works on sources before warehouse ingestion
- **Soda:** Alternative to GE with data quality monitoring and alerting
- **Elementary:** dbt-native data observability (anomaly detection, alerting)

**Orchestration and integration [12]:**
- **Apache Airflow:** Most common orchestrator for dbt runs in production
- **Dagster, Prefect:** Modern alternatives with better developer experience and asset-based scheduling
- **OpenLineage:** Captures run-level details, execution status, and dependencies across tools

**Modern data stack pattern (2025 canonical) [2, 12]:**
1. Ingestion: Fivetran or Airbyte (ELT, not ETL)
2. Storage: Snowflake, BigQuery, or Databricks
3. Transformation: dbt Core or dbt Cloud
4. Semantic layer: dbt MetricFlow, Cube, or warehouse-native
5. Orchestration: Airflow, Dagster, or dbt Cloud schedules
6. BI/consumption: Looker, Tableau, Hex, or AI-powered tools

**AI integration in 2025 [2]:** Primary use is reducing drudge work — generating dbt YAML files, repetitive configuration, and boilerplate SQL. dbt Copilot and tools like GitHub Copilot are widely used. The semantic layer becomes the trust layer for AI: agents request metrics by name, receive deterministic SQL with lineage, rather than guessing joins.

## Challenge

### Confirmed Findings

- **dbt adoption scale (8,200+ companies, 80% AI usage):** Confirmed by the State of Analytics Engineering 2025 survey, a dbt Labs publication. The Fivetran merger announcement (October 2025) cites "well over 10,000 customers" for the combined entity, which independently corroborates the order-of-magnitude claim.
- **Fivetran acquired dbt Labs:** Confirmed — a definitive all-stock merger agreement was signed October 13, 2025. Tristan Handy becomes co-founder/President; dbt Core's Apache 2.0 license explicitly preserved.
- **Fivetran acquired SQLMesh (Tobiko Data):** Confirmed — Fivetran acquired Tobiko Data (the company behind SQLMesh and SQLGlot) on September 3, 2025. Notably, Fivetran subsequently donated SQLMesh to the Linux Foundation on March 25, 2026, meaning SQLMesh is now community-governed, not Fivetran-proprietary.
- **MetricFlow open-sourced Apache 2.0 at Coalesce 2025:** Confirmed. The core semantic engine is Apache 2.0 from version 0.209.0 onward. The Semantic Layer API (downstream tool integrations) still requires a paid dbt Cloud account (Starter or above).
- **Semantic layer improves AI accuracy (83%):** Confirmed as a real dbt Labs internal replication study, but it is self-published research — dbt's own DX team replicated an external paper using their own infrastructure. The ~40% baseline for raw SQL is plausible but comes from the same source.
- **Activity Schema eliminates complex dependency chains:** Partially confirmed. The design goal is accurate, but the tradeoff framing in the draft understates the limitations (see Challenged Findings).

### Challenged Findings

- **Claim:** "Fivetran acquired both dbt and SQLMesh in 2025, fundamentally shifting competitive dynamics."
  - **Challenge:** This is accurate in substance but misleading in framing. The dbt Labs deal was a merger (all-stock), not a traditional acquisition. More importantly, SQLMesh was subsequently donated to the Linux Foundation (March 2026) — it is no longer a Fivetran proprietary asset. Describing it as "Fivetran acquired SQLMesh" is outdated as of the document date (April 2026).
  - **Verdict:** Corrected. The draft's phrasing should distinguish (1) the dbt Labs merger, (2) the Tobiko/SQLMesh acquisition, and (3) the Linux Foundation donation of SQLMesh. The "shifting competitive dynamics" framing remains valid.

- **Claim:** "Dimensional modeling (Kimball) is used in 90%+ of enterprise data warehouses."
  - **Challenge:** The 90%+ figure traces back to a single T3-tier blog post (ghostinthedata.info, Nov 2025), which itself cites no primary source or methodology. No industry survey, Gartner report, or vendor study is cited to substantiate the number. A Fivetran-published study found wide tables (One Big Table / OBT) are 25-50% faster than star schema on Redshift, Snowflake, and BigQuery — a finding that challenges the implied superiority of dimensional modeling and suggests OBT adoption is growing.
  - **Verdict:** Uncertain. The 90%+ figure is plausible as a rough estimate but should not be presented as a sourced statistic. The draft should qualify it as an industry estimate from a practitioner source, not an audited number.

- **Claim:** "SQLMesh offers ~9x faster execution than dbt Core."
  - **Challenge:** The 9x benchmark was conducted by Tobiko Data (SQLMesh's creator) in partnership with Databricks on a 2X-Small serverless warehouse using the TPC-DI benchmark. The cost projection extrapolates from this small setup to enterprise scale using a 10,000x scale factor assumption — a significant extrapolation the authors themselves revised in a June 2025 update. The benchmark measures specific workflow steps (environment creation, change promotion, rollback), not general pipeline execution speed, and was produced by an interested party. dbt's new Fusion engine offers ~30x faster parsing, which complicates the comparison.
  - **Verdict:** Accepted with qualification. The 9x figure comes from a vendor-produced benchmark with favorable methodology for SQLMesh. The draft should note the source and scope of the benchmark.

- **Claim:** "Activity Schema eliminates complex dependency chains with a single time-series table."
  - **Challenge:** Elimination is too strong. Activity Schema reduces certain dependency patterns but introduces its own constraints: BI tools designed for star schemas experience performance degradation with JSON column querying; the framework requires strong organizational alignment (all teams must adopt it); security-sensitive organizations resist a single activity stream; and adoption tooling remains thin (Narrator is cited as the only full implementation). The framework works best in event-driven architectures and is poorly suited for organizations with heavily aggregated pre-computed reports.
  - **Verdict:** Corrected. "Reduces" is more accurate than "eliminates." The draft's existing trade-off note ("less suited for complex multi-entity analysis") should be strengthened.

- **Claim:** "AI systems using the semantic layer achieved 83% accuracy on addressable questions vs. substantially lower prompt-only accuracy."
  - **Challenge:** The 83% figure is from a dbt Labs internal replication study — not an independent third-party benchmark. The baseline comparison ("substantially lower," implied ~40%) is also from the same source. The study tested natural language query answering on a specific dataset, not general enterprise analytics workloads. The "addressable questions" qualifier is important: questions the semantic layer cannot frame at all are excluded from the denominator.
  - **Verdict:** Accepted with qualification. The directional claim (semantic layer improves AI accuracy) is well-supported conceptually, but the specific 83% figure should be attributed as dbt Labs' own internal study, not independent research.

### Gaps Identified

- **Fivetran neutrality risk post-merger:** The draft mentions the Fivetran/dbt merger but does not address the most significant implication: dbt was historically tool-agnostic (works with Airbyte, Stitch, any ingestion). As a Fivetran-owned product, ecosystem neutrality is now questioned. This is a material consideration for teams evaluating vendor lock-in.
- **dbt Fusion engine:** The draft mentions dbt acquired SDF (2024-2025) but does not cover the dbt Fusion engine, which claims ~30x faster parsing. This is relevant context for the SQLMesh speed comparison.
- **MetricFlow Semantic Layer API gating:** The draft does not distinguish between what MetricFlow the open-source library provides versus what requires a paid dbt Cloud account. Downstream integrations (Looker, Tableau, Hex connectors) require dbt Cloud — the open source release is the engine, not the full platform.
- **OBT (One Big Table) as a serious alternative:** Wide tables receiving a major performance validation (25-50% faster on major warehouses per Fivetran's own study) and growing practitioner interest deserve more substantive treatment than a brief mention under "wide tables vs. star schema."
- **SQLMesh Linux Foundation donation:** A significant development (March 2026) that changes the competitive framing entirely — SQLMesh is now community-governed open source, not a Fivetran competitive weapon.

### Alternative Perspectives

- **Semantic layer skepticism:** Several practitioners argue semantic layers are difficult to maintain at scale — the "define once, use everywhere" promise breaks down as definitions diverge across tools and teams, and the bootstrapping cost (migrating existing metrics logic) is high enough that adoption stalls in practice. The complexity can make the semantic layer a bottleneck rather than an enabler.
- **Wide tables / OBT as a viable default:** A growing body of practitioner opinion (and Fivetran's own benchmark data) suggests that for many workloads, a well-maintained wide table is simpler and faster than a star schema. The 90%+ Kimball adoption figure may reflect legacy architecture more than active choice.
- **dbt's ELT-only scope as a structural limitation:** dbt handles only the T in ELT. As the Fivetran merger integrates ingestion and transformation, teams not using Fivetran for ingestion may find the combined platform less neutral, shifting the calculus toward open-source-first stacks (DuckDB + SQLMesh + Airflow) or warehouse-native transformation options.
- **Vendor consolidation risk:** The merger of the two dominant modern data stack vendors (Fivetran for ingestion, dbt for transformation) into a single entity creates pricing and lock-in risk not present when they were independent. This is a material concern for organizations prioritizing optionality.

## Findings

### Sub-question 1: What is analytics engineering and how does it bridge data engineering and data analysis?

Analytics engineering emerged around 2018 as a distinct role between data engineers (who build infrastructure) and data analysts (who consume insights). The core job is applying software engineering practices — version control, testing, CI/CD, documentation — to data transformation, producing clean, reliable datasets that enable self-service analysis (HIGH — T1 dbt Labs primary source [1]).

The role fills a structural gap created by cloud data warehouses: analysts gained SQL capability but created inconsistent, duplicated logic without software discipline; data engineers had the rigor but not the business domain knowledge. Analytics engineers bring both (HIGH — [1][2]).

By 2025 the boundaries have blurred. At larger organizations the team structure is roughly 3:2:1 (analysts : analytics engineers : visual analytics engineers). Some analytics engineers shift toward traditional data engineering work; others shift toward direct stakeholder engagement. Adoption has spread beyond tech (34%) into financial services (15%) and healthcare (10%) (MODERATE — T1 source but self-reported survey [2]).

**Scale context (2025):** 8,200+ companies globally use dbt; 80% of practitioners use AI in some capacity; 56% cite data quality as a persistent top challenge (MODERATE — T1 source, but dbt Labs-published survey [2]).

### Sub-question 2: How should metrics layers and semantic layers be designed?

The semantic layer — a versioned, machine-readable definition of business metrics — is the most significant structural development in analytics engineering in 2025. It separates metric *definition* from metric *computation*, enabling any downstream tool to query the same definition and receive consistent, lineage-tagged SQL (HIGH — [3][4][5][6]).

**MetricFlow (dbt's implementation):** The semantic engine was open-sourced under Apache 2.0 at Coalesce 2025 (version 0.209.0+). **Important caveat:** the open-source release covers the MetricFlow engine itself; downstream integrations (Looker, Tableau, Hex, Mode connectors) still require a paid dbt Cloud account. The "open source" framing applies to the core library, not the full platform (HIGH — [3][4]).

Semantic models are YAML definitions layered on top of dbt models, declaring entities, dimensions, measures, and metric derivation rules. MetricFlow handles multi-dialect SQL generation, join logic, window functions, and time grain alignment — ensuring metric queries are deterministic rather than LLM-guessed (HIGH — [5][6]).

**Three architectural approaches** involve different tradeoffs (MODERATE — T2 source [7]):
- *Transformation-layer (dbt MetricFlow):* Git-governed, multi-warehouse portable, real-time. Best for dbt-native teams.
- *Warehouse-native (Snowflake Cortex, Databricks Unity):* Zero extra infrastructure, real-time, single-vendor only.
- *OLAP-acceleration (Cube.dev):* Sub-second cached queries, handles 100–1,000 QPS. Best for embedded analytics and high-concurrency dashboards.

**Design guidance:** Start with 10–20 "tier-0" metrics (revenue, churn, CAC) and manually re-engineer their logic — do not auto-migrate existing metric definitions. Symmetric aggregates and complex calculations require explicit redesign. Definitions must live in version-controlled files with peer-review workflow (MODERATE — T2/T3 sources [15][16]).

**Semantic layers and AI:** A dbt Labs internal replication study found 83% accuracy on "addressable questions" when an LLM queries a semantic layer vs. a substantially lower baseline for raw SQL prompting. The directional finding (semantic layers improve AI accuracy) is well-supported; the 83% figure should be read as a self-published benchmark, not independent third-party research (MODERATE — T1 source, self-published [3]).

### Sub-question 3: What data modeling patterns produce self-service-ready datasets?

**dbt three-tier layered architecture** is the dominant implementation pattern for self-service readiness (HIGH — [12]):
1. *Staging:* Rename, cast, convert — no joins or aggregations. Views. Named `stg_<source>__<entity>s`.
2. *Intermediate:* Joins, filters, business-domain logic. Verb-named (`int_orders_joined`).
3. *Marts:* Stable, business-entity-aligned tables. Minimized joins, optimized for downstream queries.

**Dimensional modeling (Kimball)** remains the most widely used analytics modeling paradigm. Denormalized dimensions with star schema structures enable single-hop joins and are the recommended pattern on all major warehouses (Snowflake, BigQuery, Databricks, Fabric). The "90%+ enterprise adoption" figure appears in practitioner literature but originates from a single unverified T3 source — treat it as a plausible industry estimate, not a sourced statistic (MODERATE — [11], T3 source, unverified figure).

**One Big Table (OBT) / wide tables** deserve serious consideration as an alternative. Fivetran's own benchmark data indicates OBT is 25–50% faster than star schema on Redshift, Snowflake, and BigQuery for many common workloads. The practical tradeoff: star schemas are more maintainable across teams and avoid duplicated business logic in wide tables, but OBT wins on simplicity and query performance for single-domain, event-driven workloads (MODERATE — challenger-sourced finding).

**Activity Schema** is an open-source pattern that structures all analytics data as a single append-only time-series table with 11 standardized columns and 11 temporal join patterns (`first_ever`, `last_before`, `aggregate_in_between`, etc.). It *reduces* (not eliminates) complex dependency chains by making customer journeys and event sequences first-class. Significant limitations: BI tools designed for star schemas perform poorly with JSON column querying, full adoption requires strong organizational alignment, and tooling remains thin (Narrator is the only full implementation) (MODERATE — [9][10], challenger corrections applied).

**Data Vault 2.0** is best for regulated industries (financial services, healthcare) where audit trails and source-system change handling are required. It is less optimized for end-user query performance and adds modeling complexity (MODERATE — [11]).

### Sub-question 4: How should data testing and documentation be integrated?

**Testing strategy:** Use dbt's four built-in generic tests (`unique`, `not_null`, `accepted_values`, `relationships`) as the baseline for all transformation logic. Run Great Expectations (300+ validators) on *source data* as it enters the warehouse — before dbt sees it — to validate upstream system behavior. Use the `dbt-expectations` package (originally by Calogica; active fork at Metaplane) to apply GE-style expectations within dbt's YAML framework without leaving the dbt ecosystem (HIGH — [13], two-tool approach confirmed by multiple sources; note: Datadog has published guides using the package but does not maintain it).

**Data contracts:** Enable with `contract: enforced: true` in model config. Contracts create machine-enforced agreements on schema, freshness, and reliability between producers and consumers. They make schema breakages explicit rather than silent (MODERATE — [2][12]).

**Documentation:** `dbt docs generate` produces automatic dependency graphs and column-level lineage. Providing semantic context and documentation significantly improves AI tool effectiveness — models with documented columns and metric definitions allow LLMs to reason about data correctly rather than guessing table relationships (MODERATE — [2][12]).

**2025 AI-assisted testing:** 54% of practitioners expect AI to improve testing workflows (up from 47%). Primary use case is AI-generated YAML for dbt tests, reducing boilerplate authoring time (MODERATE — T1 source, self-reported survey [2]).

### Sub-question 5: What analytics engineering tools and workflows are current best-in-class?

**dbt** (Core: Apache 2.0, Cloud: paid) is the dominant standard. Core capabilities: SQL transformation, testing, documentation generation, automatic lineage, CI/CD integration. dbt Cloud adds scheduling, dbt Copilot (AI code generation), dbt Mesh (cross-project dependencies), the Semantic Layer API, and the dbt Fusion engine (acquired via SDF, ~30x faster SQL parsing) (HIGH — [2][12]).

**Fivetran/dbt ecosystem consolidation (2025–2026):** Fivetran merged with dbt Labs (all-stock, October 13, 2025) and acquired Tobiko Data (SQLMesh/SQLGlot creator, September 3, 2025). SQLMesh was subsequently donated to the Linux Foundation (March 25, 2026), making it community-governed open source. Key implication: dbt's historical tool-agnosticism is now questioned — dbt was ingestion-neutral, but as a Fivetran-owned product, organizations using Airbyte, Stitch, or other ingestion tools should evaluate vendor neutrality risk (HIGH — challenger-sourced and confirmed).

**SQLMesh** (now Linux Foundation open source) is the strongest open-source alternative to dbt. Key advantages: compile-time SQL validation via SQLGlot, automatic column-level lineage, built-in rollback, and "virtual data environments" that use table fingerprinting instead of materializing copies. A vendor-produced benchmark (Tobiko Data + Databricks, TPC-DI) showed ~9x faster workflow execution than dbt Core for specific workflow steps (environment creation, change promotion, rollback) — not general pipeline execution. The comparison is further complicated by dbt's Fusion engine for parsing speed. Choose SQLMesh for Python-native teams, incremental logic flexibility, or when open-source governance is a priority (MODERATE — [14], benchmark from interested party).

**Semantic layer tools:** dbt MetricFlow (best for dbt-native teams, multi-cloud), Cube.dev (best for embedded analytics, sub-second caching), Snowflake Semantic Views / Cortex Analyst (best for Snowflake-only orgs), Databricks Metric Views / Unity Catalog (Databricks-only). AtScale and GoodData serve polyglot, multi-BI environments (MODERATE — [7][8][15]).

**Data quality tools:** `dbt-expectations` (dbt-native GE-style tests), Great Expectations (source validation), Soda (monitoring + alerting), Elementary (dbt-native anomaly detection + alerting) (MODERATE — [13]).

**Canonical 2025 modern data stack:**
1. Ingestion: Fivetran or Airbyte (ELT, not ETL)
2. Storage: Snowflake, BigQuery, or Databricks
3. Transformation: dbt Core or dbt Cloud
4. Semantic layer: dbt MetricFlow, Cube, or warehouse-native
5. Orchestration: Airflow, Dagster, or dbt Cloud schedules
6. BI/consumption: Looker, Tableau, Hex, or AI-powered query tools

**Vendor lock-in risk:** The Fivetran/dbt merger creates meaningful pricing and optionality risk. Organizations prioritizing independence should consider open-source-first stacks: DuckDB + SQLMesh (Linux Foundation) + Airflow + Cube.dev (open-source core) (MODERATE — challenger-sourced).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "8,200+ companies globally use dbt" | statistic | [2] | verified — dbt Labs State of Analytics Engineering 2025 blog summary confirms this figure; a separate result notes "50,000 teams using dbt every week," consistent in order of magnitude |
| 2 | "80% of data practitioners use AI in some capacity" | statistic | [2] | verified — confirmed directly from the State of Analytics Engineering 2025 summary page: "80% of data practitioners are using AI in some way as part of their workflows" |
| 3 | "56% cite data quality as a persistent top challenge" | statistic | [2] | verified — confirmed directly from source: "56% of survey respondents identified data quality as a problem" (survey N=459, Oct–Dec 2024) |
| 4 | "MetricFlow open-sourced under Apache 2.0 from version 0.209.0+" | attribution | [3] | verified — the Coalesce 2025 announcement confirms version 0.209.0+ is covered by Apache 2.0; prior versions were AGPL (0–0.140.0) and BSL (0.150.0–0.208.2) |
| 5 | "Fivetran/dbt merger was all-stock, signed October 13, 2025" | attribution | challenger-sourced | verified — confirmed by Latham & Watkins counsel announcement and Fivetran press release; all-stock deal signed October 13, 2025; Tristan Handy becomes co-founder/President |
| 6 | "Tobiko Data (SQLMesh) acquired by Fivetran September 3, 2025" | attribution | challenger-sourced | verified — confirmed by BusinessWire press release dated September 3, 2025: "Fivetran Acquires Tobiko Data" |
| 7 | "SQLMesh donated to Linux Foundation March 25, 2026" | attribution | challenger-sourced | verified — confirmed by Linux Foundation press release, Fivetran press release, and multiple news sources; announced at KubeCon + CloudNativeCon Europe on March 25, 2026 |
| 8 | "dbt-expectations package is maintained by Datadog" | attribution | [13] | corrected — the package was created and historically maintained by Calogica (clausherther); the GitHub repo `calogica/dbt-expectations` is now archived as "no longer actively supported." Datadog wrote a blog post stating it maintains the package, but the canonical active fork is `metaplane/dbt-expectations` (Metaplane). The "maintained by Datadog" attribution in the research document traces to the Datadog blog ([12]), which appears to overstate Datadog's role. The Sparvi source ([13]) may have reproduced the Datadog blog claim. Should be: "originally maintained by Calogica; active fork at Metaplane; Datadog has published guides using the package" |
| 9 | "Cube.dev handles 100–1,000 QPS" | statistic | [7] | verified — Cube's own documentation states: "allow for a decent concurrency (say, 100 QPS or maybe 1000 QPS)" for pre-aggregation cached queries; 50–500ms sub-second latency confirmed |
| 10 | "54% of practitioners expect AI to improve testing workflows" | statistic | [2] | verified — confirmed from State of Analytics Engineering 2025: "54% of respondents expect AI to benefit testing/tracking code, up from 47% last year" |
| 11 | "83% accuracy on addressable questions using semantic layer" | statistic | [3] | verified with qualification — dbt Labs published a study finding 83% accuracy for a subset of 8 "addressable" questions (high complexity / low schema complexity) when querying via the semantic layer, vs ~40% for raw SQL on undecorated tables; study is self-published by dbt Labs DX team, not independent third-party research; "addressable questions" excludes queries requiring too many joins (which scored 0%) |
