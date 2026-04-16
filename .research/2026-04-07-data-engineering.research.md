---
name: "Data Engineering Best Practices"
description: "ELT+dbt is the analytics engineering default with post-2025 vendor risk; three-layer staging/marts pattern suits multi-team orgs; data quality requires testing+monitoring+observability; contracts govern transformation layer only and succeed on org design"
type: research
sources:
  - https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
  - https://docs.getdbt.com/best-practices/how-we-structure/2-staging
  - https://docs.getdbt.com/best-practices/how-we-structure/4-marts
  - https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models
  - https://docs.getdbt.com/docs/mesh/govern/model-contracts
  - https://docs.getdbt.com/best-practices/best-practice-workflows
  - https://www.getdbt.com/blog/data-integration
  - https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/
  - https://www.tbdcdata.com/en/blog/airflow-vs-prefect-vs-dagster/
  - https://www.sparvi.io/blog/great-expectations-vs-dbt-tests
  - https://www.elementary-data.com/post/data-contracts
  - https://www.conduktor.io/glossary/schema-evolution-best-practices
  - https://airbyte.com/data-engineering-resources/master-schema-evolution
  - https://www.startdataengineering.com/post/de_best_practices/
  - https://knowledge.businesscompassllc.com/dbt-naming-conventions-and-coding-standards-best-practices-for-modern-data-transformation/
related: []
---

# Data Engineering Best Practices

> ELT with dbt is the analytics engineering default (scoped to batch/BI workloads — not streaming or operational pipelines), but carries vendor consolidation risk following the 2025 Fivetran/dbt merger. The staging → intermediate → marts layering pattern has strong multi-source consensus for teams at scale; smaller teams may not need the intermediate layer. Data quality requires three distinct tiers (build-time testing, scheduled monitoring, runtime observability) — current tooling covers only the first. Data contracts govern the transformation output layer only; their success depends on organizational incentive alignment, not technical implementation.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview | How we structure our dbt projects | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 2 | https://docs.getdbt.com/best-practices/how-we-structure/2-staging | Staging: Preparing our atomic building blocks | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 3 | https://docs.getdbt.com/best-practices/how-we-structure/4-marts | Marts: Business-defined entities | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 4 | https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models | How we style our dbt models | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 5 | https://docs.getdbt.com/docs/mesh/govern/model-contracts | Model contracts | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 6 | https://docs.getdbt.com/best-practices/best-practice-workflows | Best practices for workflows | dbt Labs | 2024 (continuously updated) | T1 | verified |
| 7 | https://www.getdbt.com/blog/data-integration | Data Integration in 2025: architectures, tools, and best practices | dbt Labs | 2025 | T2 | verified |
| 8 | https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/ | Decoding Data Orchestration Tools: Comparing Prefect, Dagster, Airflow, and Mage | FreeAgent Engineering | May 2025 | T2 | verified |
| 9 | https://www.tbdcdata.com/en/blog/airflow-vs-prefect-vs-dagster/ | Airflow vs Prefect vs Dagster: Choosing the Right Data Orchestrator in 2025 | The Big Data Company | 2025 | T3 | verified |
| 10 | https://www.sparvi.io/blog/great-expectations-vs-dbt-tests | Great Expectations vs dbt Tests: Which Should You Use? (2025) | Sparvi | 2025 | T3 | verified (vendor bias: Sparvi makes competing data quality tooling) |
| 11 | https://www.elementary-data.com/post/data-contracts | What Are Data Contracts? Components, Benefits & Challenges | Elementary Data | 2024–2025 | T3 | verified (vendor bias: Elementary sells dbt observability product; downgraded T2→T3) |
| 12 | https://www.conduktor.io/glossary/schema-evolution-best-practices | Schema Evolution Best Practices | Conduktor | 2024–2025 | T3 | verified (scope: Kafka-centric vendor; streaming context may not generalize) |
| 13 | https://airbyte.com/data-engineering-resources/master-schema-evolution | Mastering Schema Evolution: Best Practices for Data Consistency | Airbyte | 2024–2025 | T2 | verified |
| 14 | https://www.startdataengineering.com/post/de_best_practices/ | Data Engineering Best Practices #1: Data flow & Code | Start Data Engineering | 2023–2024 (foundational) | T3 | verified (age: pre-2025; foundational patterns remain valid) |
| 15 | https://knowledge.businesscompassllc.com/dbt-naming-conventions-and-coding-standards-best-practices-for-modern-data-transformation/ | dbt Naming Conventions and Coding Standards | Business Compass LLC | 2024–2025 | T3 | verified |

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | dbt best practices 2025 project structure staging intermediate marts | WebSearch | 10 results |
| 2 | modern data stack ELT pipeline architecture best practices 2025 | WebSearch | 10 results |
| 3 | data quality frameworks Great Expectations dbt tests Elementary 2025 | WebSearch | 10 results |
| 4 | data contracts schema evolution teams best practices 2025 | WebSearch | 10 results |
| 5 | data engineering naming conventions code organization best practices 2025 | WebSearch | 10 results |
| 6 | Dagster Prefect Airflow orchestration comparison 2025 modern data engineering | WebSearch | 10 results |
| 7 | dbt data contracts schema evolution best practices 2025 dbtLabs | WebSearch | 10 results |
| 8 | dbt project naming conventions source schema model documentation 2025 analytics engineering | WebSearch | 10 results |
| 9 | WebFetch: docs.getdbt.com/best-practices/how-we-structure/1-guide-overview | WebFetch | full page |
| 10 | WebFetch: docs.getdbt.com/best-practices/how-we-structure/2-staging | WebFetch | full page |
| 11 | WebFetch: docs.getdbt.com/best-practices/how-we-structure/4-marts | WebFetch | full page |
| 12 | WebFetch: docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models | WebFetch | full page |
| 13 | WebFetch: docs.getdbt.com/docs/mesh/govern/model-contracts | WebFetch | full page |
| 14 | WebFetch: docs.getdbt.com/best-practices/best-practice-workflows | WebFetch | full page |
| 15 | WebFetch: getdbt.com/blog/data-integration | WebFetch | full page |
| 16 | WebFetch: engineering.freeagent.com/2025/05/29/... | WebFetch | full page |
| 17 | WebFetch: tbdcdata.com/en/blog/airflow-vs-prefect-vs-dagster/ | WebFetch | full page |
| 18 | WebFetch: sparvi.io/blog/great-expectations-vs-dbt-tests | WebFetch | full page |
| 19 | WebFetch: elementary-data.com/post/data-contracts | WebFetch | full page |
| 20 | WebFetch: conduktor.io/glossary/schema-evolution-best-practices | WebFetch | full page |
| 21 | WebFetch: airbyte.com/data-engineering-resources/master-schema-evolution | WebFetch | full page |
| 22 | WebFetch: startdataengineering.com/post/de_best_practices/ | WebFetch | full page |
| 23 | WebFetch: knowledge.businesscompassllc.com/dbt-naming-conventions-... | WebFetch | full page |

## Challenge

### Sub-question 1: ETL/ELT Pipeline Architecture

**Challenge 1.1:** The document claims ELT is now "the standard" without qualifying that ETL still dominates in streaming, IoT, and privacy-constrained pipelines.
- **Evidence for:** Sources [7] and [14] both position ELT as the modern default, with cloud warehouses as the central hub.
- **Counter-evidence:** AWS, Confluent, and Striim all document active ETL use cases in 2025: IoT sensor pipelines (protocol normalization before load), streaming ETL via Kafka (real-time transformation and distribution), regulated workloads requiring pre-load masking/encryption, and hybrid Zero-ETL patterns for operational data. ELT assumes a cloud data warehouse with sufficient compute — a premise that does not hold for edge computing, real-time fraud, or data-residency-constrained architectures.
- **Classification:** Qualified — ELT is the analytics-engineering default, not the universal standard.
- **Confidence impact:** The opening assertion should be scoped to "analytics and BI workloads." Streaming/operational use cases are a large and growing segment not covered by any current source.

**Challenge 1.2:** Orchestration coverage treats Airflow, Dagster, and Prefect as the complete field, omitting Temporal, Flyte, and platform-native schedulers.
- **Evidence for:** Sources [8] and [9] cover all three major tools with genuine depth.
- **Counter-evidence:** ZenML, Flyte (ML-focused), cloud-native schedulers (AWS Step Functions, GCP Workflows, Azure Data Factory), and embedded orchestration inside dbt Cloud are all in active production use. Databricks Workflows is omitted despite being the default for Lakehouse pipelines. Platform-native schedulers dominate teams already operating within a single cloud vendor. The document gives no coverage to this entire category.
- **Classification:** Gap — non-standalone orchestrators covering a substantial fraction of production pipelines are absent.
- **Confidence impact:** Moderate. The three-tool comparison is accurate within its scope but creates a false impression of the full market.

**Challenge 1.3:** The Fivetran/dbt merger (2025) introduces vendor consolidation risk that changes the strategic weight of recommending dbt as "the transformation standard."
- **Evidence for:** Source [7] (dbt Labs blog) positions dbt as the uncontested standard for governance and reliability.
- **Counter-evidence:** The 2025 Fivetran/dbt merger raised immediate concerns about pricing trajectories, reduced product independence, and long-term open-source commitments for dbt Core. Multiple data teams publicly evaluated SQLMesh and Dataform as alternatives post-announcement. Recommending dbt as a neutral best practice without noting this consolidation event omits a material strategic risk present at the time of this research.
- **Classification:** Gap — the source list is pre-merger and does not reflect post-October 2025 ecosystem dynamics.
- **Confidence impact:** High. The "ELT + dbt as standard" framing should carry a vendor-lock-in caveat.

**Challenge 1.4:** SQLMesh is not mentioned despite Databricks benchmarking it at approximately 9x faster and lower cost than dbt Core, with a dbt-compatible migration layer.
- **Evidence for:** No source in the document covers SQLMesh.
- **Counter-evidence:** Multiple 2024–2025 comparisons (SYNQ, Atomic Labs, Tobiko/Databricks benchmark) document SQLMesh advantages: compile-time SQL validation via SQLGlot, free virtual development environments, and automatic column-level lineage absent in dbt. SQLMesh acquired by Fivetran in September 2025 alongside the dbt merger further complicates the "dbt is the standard" claim.
- **Classification:** Gap — a credible, actively adopted alternative with documented performance advantages receives zero coverage.
- **Confidence impact:** Moderate. Does not contradict the current findings but substantially narrows their applicability to teams evaluating transformations tools today.

---

### Sub-question 2: Data Transformation Layer Structure

**Challenge 2.1:** The staging → intermediate → marts model is presented as a universal best practice, but credible practitioners argue it introduces unnecessary overhead for small-to-mid-sized teams.
- **Evidence for:** Sources [1]–[3] and [6] treat the three-layer model as the default, and Source [14] independently confirms it as industry-standard via the "3-hop architecture."
- **Counter-evidence:** Daniel Beach (Data Engineering Central) argues in a widely-cited 2024 piece that the mandatory three-layer structure is unnecessary overhead — the traditional two-step approach (raw → fact/dimension tables, with marts only when specific aggregation is needed) works fine without the intermediate layer. He further argues that Databricks' Medallion branding is marketing that encourages storage/compute overconsumption. dbt's own guidance notes "if you have fewer than 10 marts you may not need subfolders" — an implicit acknowledgment that the full pattern is only justified at scale.
- **Classification:** Qualified — the three-layer model is well-suited to large, multi-team analytics orgs. For smaller teams or Lakehouse-native pipelines it can be over-engineering.
- **Confidence impact:** Moderate. The recommendation should specify team/project scale as a condition.

**Challenge 2.2:** The recommendation to "default to views, escalate to tables" ignores cost and latency penalties in specific warehouse architectures.
- **Evidence for:** Sources [3] and [6] both recommend materializing as views as the default starting point.
- **Counter-evidence:** In Databricks with Unity Catalog schemas containing thousands of tables, dbt run times of 15+ minutes have been documented where parsing overhead dwarfs actual model execution time. In Snowflake, complex view chains cause repeated query plan compilation cost. The view-first principle is warehouse-agnostic guidance applied in contexts where it does not hold — Databricks documentation explicitly recommends Delta tables as defaults for most patterns, not views.
- **Classification:** Qualified — view-first is appropriate for BigQuery and Snowflake in early-stage projects; it is actively counterproductive in large Databricks Unity Catalog environments.
- **Confidence impact:** Low-moderate. Does not invalidate the principle but the guidance needs a warehouse-specific caveat.

**Challenge 2.3:** The one-to-one staging/source-table relationship is presented without acknowledging the base model pattern for complex raw schemas.
- **Evidence for:** Source [2] explicitly states "one-to-one relationship: each staging model corresponds to exactly one source table."
- **Counter-evidence:** dbt's own documentation for complex source systems (e.g., multi-type event tables, multi-tenant schemas) recommends `base_` prefix models that pre-filter or pivot before the staging layer adds its standard transformations. This is a well-documented exception to the one-to-one rule that the document mentions only implicitly ("base model scenarios") without explaining when and why teams deviate. Teams working with Fivetran-synced event streams regularly need base models before staging.
- **Classification:** Qualified — the one-to-one rule is a strong default with a recognized exception class not adequately covered.
- **Confidence impact:** Low. Pedantic for most teams but material for high-volume event pipeline patterns.

---

### Sub-question 3: Data Quality Frameworks and Testing

**Challenge 3.1:** Great Expectations is treated as the natural complement to dbt tests, but its adoption friction is severe enough that many teams abandon it in practice.
- **Evidence for:** Sources [10] and [14] position GX as the recommended choice for advanced validation and source data testing.
- **Counter-evidence:** Multiple practitioner accounts (Confessions of a Data Guy, CyberSierra, Databricks Community) document GX's steep learning curve, complex setup, and "many moving pieces" as significant adoption barriers. The tool's own community acknowledges "you probably shouldn't use Great Expectations if you want to get something done quickly." In 2025, Soda (SodaCL declarative syntax) and dbt-native packages (`dbt-expectations`, `dbt-utils`) are frequently cited as lower-friction alternatives that cover 80% of GX use cases without the operational overhead. Source [10] is from Sparvi, a competing vendor, which creates a conflict of interest that could inflate GX's apparent limitations. The document acknowledges vendor bias for Source [10] but does not account for the fact that this bias may work in both directions.
- **Classification:** Qualified — GX is capable but its complexity makes it the wrong choice for many teams. The recommendation to use it for "source data validation" needs a qualification about team size and operational maturity.
- **Confidence impact:** Moderate. The complementary-use recommendation is directionally correct but may lead teams to over-invest in GX when lighter tools suffice.

**Challenge 3.2:** The document treats data quality as a testing problem (validate at build time) but the 2025 landscape distinguishes testing from monitoring and observability — categories absent from all current sources.
- **Evidence for:** Sources [10], [11], [14] all focus on test-time validation (dbt tests, GX expectations, Elementary anomaly detection).
- **Counter-evidence:** Monte Carlo, Metaplane, and SYNQ represent a distinct observability layer that detects anomalies, schema changes, and volume drops in production — runtime signals that build-time tests cannot catch. Monte Carlo's research defines three distinct categories: data testing (build-time), data quality monitoring (scheduled checks against live data), and data observability (continuous anomaly detection). The document conflates all three under "data quality frameworks," omitting the monitoring and observability categories entirely. For production pipelines, observability tooling is increasingly the primary quality signal — a pattern not represented by any current source.
- **Classification:** Gap — the full data quality tooling landscape (testing + monitoring + observability) is not covered. Current sources only address the testing tier.
- **Confidence impact:** High for production pipeline contexts. Build-time testing alone is insufficient; the absence of monitoring/observability coverage is a meaningful scope gap.

**Challenge 3.3:** The "minimum standard" of primary key uniqueness and non-null tests understates what teams operating at scale actually require.
- **Evidence for:** Sources [6] and [14] both cite PK uniqueness + non-null as "the minimum standard."
- **Counter-evidence:** At scale, the minimum standard for production marts includes: referential integrity checks across joins, freshness SLAs, row count anomaly detection, and source-level schema change alerting. The current minimum reflects an early-stage dbt project baseline, not a mature production standard. This framing risks giving teams a false ceiling on their quality investment.
- **Classification:** Qualified — accurate as a starter baseline, misleading as a general standard.
- **Confidence impact:** Low-moderate. The framing shapes expectations; teams should know this is a floor, not a target.

---

### Sub-question 4: Schema Evolution and Data Contracts

**Challenge 4.1:** dbt model contracts are presented as "the primary mechanism for schema governance across teams" (per the document's opening assertion), but they govern only the transformation output layer, not upstream source changes — where most breaking changes originate.
- **Evidence for:** Source [5] presents dbt model contracts as the schema governance standard; Source [11] reinforces this framing.
- **Counter-evidence:** Chad Sanderson (Data Products substack, "Your Data Contracts Are in the Wrong Spot") argues that teams placing contracts only in the warehouse or transformation layer have "an illusion of control." The root cause of most schema quality failures is software engineers modifying application code and inadvertently changing emitted data — a change that dbt model contracts cannot intercept. This was independently confirmed in multiple 2024–2025 practitioner accounts: contracts that haven't been updated in months while governing revenue pipelines, and breaking changes deployed by backend engineers who are unaware downstream contracts exist. dbt model contracts operate at a layer downstream of the problem source.
- **Classification:** Contradicted for cross-functional organizations. dbt model contracts are a valid governance mechanism within the analytics/transformation boundary, but they do not address the upstream software-engineering-to-data-pipeline gap that is the dominant failure mode in practice.
- **Confidence impact:** High. The opening assertion should be qualified to "schema governance within the transformation layer." Treating dbt model contracts as the primary cross-team mechanism overstates their reach.

**Challenge 4.2:** Data contracts face significant organizational adoption barriers that the current sources treat as secondary concerns.
- **Evidence for:** Source [11] acknowledges contracts require "clear ownership" but frames adoption as primarily a technical design question.
- **Counter-evidence:** Monte Carlo's 2024 analysis ("Data Contracts: 7 Critical Implementation Lessons Learned") identifies producer incentive misalignment as the dominant failure mode: software engineers are measured on feature velocity, not downstream data quality, making contract maintenance a low-priority burden with no upside for the team bearing it. The "Data Contracts: A Missed Opportunity" (Data Engineering Weekly) and "Data Contracts Don't Work" (Medium) pieces document real-world failures where contracts became stale artifacts rather than enforced interfaces. These sources collectively argue that organizational design (who owns the contract, who bears the enforcement cost) determines success more than technical implementation choice.
- **Classification:** Gap — the current sources treat data contracts as a technical pattern. The dominant failure mode is organizational, not technical.
- **Confidence impact:** High for enterprise and cross-functional teams. The recommendation to implement dbt model contracts needs an explicit organizational-readiness caveat.

**Challenge 4.3:** Schema evolution guidance is dominated by Kafka/streaming-centric sources, but the document applies these principles to warehouse/batch contexts where compatibility rules differ.
- **Evidence for:** Source [12] (Conduktor, a Kafka vendor) provides most of the schema evolution terminology and backward compatibility framing. Source [13] (Airbyte) blends streaming and batch guidance.
- **Counter-evidence:** Backward compatibility semantics for Avro schemas in Kafka (where consumers may lag producers by hours and field-level binary encoding is strict) are materially different from schema evolution in Parquet/Delta Lake (where column addition is a metadata-only operation, safe without coordination) or in SQL warehouses (where `ALTER TABLE ADD COLUMN` is non-breaking by default). The document's schema evolution section uses streaming vocabulary ("producers," "consumers," "schema registry," "compatibility modes") in a context where most readers are managing SQL warehouse schemas — a context with different tooling, different failure modes, and different best practices.
- **Classification:** Qualified — backward compatibility principles are universal, but the specific mechanisms (schema registries, Avro compatibility modes) apply only to streaming architectures. Batch/warehouse schema evolution has a distinct tooling landscape not covered.
- **Confidence impact:** Moderate. Readers building warehouse-centric pipelines may misapply streaming-specific guidance.

---

### Sub-question 5: Naming, Documentation, and Code Organization Conventions

**Challenge 5.1:** Naming conventions are presented as stable best practices, but the field has not converged — active disagreement exists on prefix usage, mart naming, and column ordering.
- **Evidence for:** Sources [4], [15] present naming conventions (snake_case, `stg_`/`int_`/`mart_` prefixes, `is_`/`has_` booleans, `_at` timestamps) as settled standards.
- **Counter-evidence:** The dbt community shows active disagreement on several conventions: whether marts should use a `mart_` prefix (dbt Labs guidance says no prefix for marts, Business Compass LLC says `mart_`), whether intermediate models should be prefixed `int_` or `int_[domain]__[verb]`, and whether `fct_`/`dim_` prefixes belong at the mart level (Kimball-influenced teams use them; dbt Labs guidance avoids them for marts). Column ordering conventions (IDs → strings → numerics → booleans → dates) are stylistic, not semantic — and not enforced by any tooling. These disagreements matter because the document frames these as objective best practices when they are recommendations with real tradeoffs.
- **Classification:** Qualified — the listed conventions are widely adopted defaults with documented exceptions and active community disagreement, not universal standards.
- **Confidence impact:** Low-moderate. The conventions are useful defaults; framing them as settled overstates consensus.

**Challenge 5.2:** The document covers dbt-specific conventions exclusively but omits non-dbt contexts (Spark/Python transforms, streaming pipelines, data mesh domain teams) where naming conventions diverge significantly.
- **Evidence for:** All naming and code organization sources ([4], [15], [6], [14]) are SQL/dbt-centric.
- **Counter-evidence:** Teams building Spark-based transformation pipelines, Python data engineering (Pandas, Polars), or streaming pipelines with Flink/Kafka Streams operate under Python module/class naming conventions (PEP 8), not SQL table naming conventions. Data mesh architectures delegate naming authority to domain teams, explicitly allowing convention divergence across domains. The document's conventions section is only applicable to SQL-first, dbt-managed transformation layers — a scope not stated.
- **Classification:** Gap — the conventions section has no coverage for non-SQL, non-dbt transformation contexts, which represent a substantial fraction of production data engineering work.
- **Confidence impact:** Moderate. Teams in mixed or non-dbt environments cannot apply these conventions directly and receive no guidance.

**Challenge 5.3:** Version control and CI/CD conventions are covered at the model/branch level but omit dbt project-level governance patterns at scale.
- **Evidence for:** Sources [6] and [15] address git branching and commit conventions.
- **Counter-evidence:** At large dbt project scale (100+ models, multiple domain teams), the core governance challenges are: multi-project dbt Mesh coordination (cross-project `ref()` and contract versioning), slim CI configuration to avoid running all models on every PR, and environment parity between dev/staging/prod. The current sources address none of these. dbt Mesh (generally available in late 2024) introduces bidirectional project dependencies and a new class of CI/CD coordination problems that existing sources do not address. This represents a recency gap — the governance challenges for multi-team dbt deployments are not covered by any 2023–2024 source in the document.
- **Classification:** Gap — large-scale multi-team dbt governance patterns are absent from all sources.
- **Confidence impact:** Moderate for enterprise teams. Single-project teams are well-served; multi-project teams are not.

---

### Overall Coverage Gaps

- **Streaming and real-time pipelines:** No source covers data engineering best practices for streaming architectures (Kafka, Flink, Spark Streaming). The entire document assumes batch/warehouse workloads.
- **Non-SQL transformation contexts:** Python-based transformation (Pandas, Polars, PySpark), ML feature engineering pipelines, and LLM data preparation pipelines are absent. The "best practices" apply to analytics engineering, not data engineering broadly.
- **Data mesh and domain ownership:** Data mesh architecture fundamentally changes the governance model (decentralized schema ownership, domain contracts, federated data governance). No source addresses how the staged-layer model interacts with data mesh ownership patterns.
- **Cost management and FinOps:** Warehouse compute cost management (incremental model strategies, partition pruning, materialization cost tradeoffs) is mentioned briefly in Source [3] but not covered as a first-class concern. In 2025, warehouse cost management is a primary engineering constraint.
- **AI/ML pipeline patterns:** LLM data preparation, feature stores, vector database pipelines, and AI-adjacent data engineering patterns are absent. The source list reflects the analytics engineering world of 2023–2024, not the AI-integrated data stack of 2025–2026.
- **Vendor lock-in and portability:** The Fivetran/dbt merger (October 2025), SQLMesh emergence, and Dataform/BigQuery integration represent a rapidly shifting vendor landscape that the document does not address. Teams adopting dbt as a "standard" face consolidation risk not present in the source set.
- **Data engineering for operational (non-analytics) workloads:** Reverse ETL, operational data products, and real-time serving layers (e.g., Redis, Pinot, Druid) are absent. The document's scope is implicitly analytics/BI, not operational data engineering.

## Findings

### Sub-question 1: ETL/ELT Pipeline Architecture

**ELT is the analytics engineering default, not the universal standard** (HIGH for analytics/BI; MODERATE as a general claim). Sources [7] and [14] converge on ELT as the modern default for analytics workloads: load raw data into a cloud warehouse, transform in-platform using SQL. The cloud warehouse or lakehouse as central hub (BigQuery, Snowflake, Databricks) is now the dominant architecture for this pattern [7]. However, the challenger found that ETL remains active in streaming, IoT, and regulated workloads — the "ELT is the standard" framing applies to analytics engineering specifically and should not be generalized to operational or real-time pipelines (Qualified — Challenge 1.1).

**Orchestration tool selection follows team priorities, not one universal choice** (MODERATE). Three major standalone orchestrators are well-documented: Airflow dominates enterprises with existing investment due to its operator library and proven scalability [8][9]; Prefect is the developer-productivity choice for greenfield Python-native teams [8][9]; Dagster is the strongest choice when data governance, asset lineage, and dbt integration are primary concerns [8][9]. A critical gap: platform-native schedulers (Databricks Workflows, AWS Step Functions, dbt Cloud's built-in scheduler) are omitted and represent a large fraction of production deployments (Gap — Challenge 1.2).

**The dbt-as-standard framing carries vendor consolidation risk** (MODERATE). The Fivetran/dbt merger (2025) and SQLMesh's documented performance advantages (benchmarks show substantial build-time improvements in Databricks environments) make "dbt as the transformation standard" a qualified recommendation rather than a neutral best practice. Teams starting new projects should evaluate SQLMesh alongside dbt; teams with existing dbt investments should track how post-merger open-source commitments evolve (Gap — Challenges 1.3, 1.4).

---

### Sub-question 2: Data Transformation Layer Structure

**Staging → Intermediate → Marts is the right model for multi-team analytics orgs** (HIGH for teams of 5+ engineers with 10+ data sources; MODERATE as a universal prescription). T1 sources [1][2][3][6] converge on the three-layer model with clear rationale: staging creates source-conformed, typed, renamed atomic units; intermediate composes logic without business meaning; marts deliver business-entity-grain tables for consumption. The challenger qualified this: for smaller teams or simpler pipelines, a two-layer approach may be sufficient overhead (Qualified — Challenge 2.1).

**Staging layer rules have strong consensus** (HIGH). One model per source table, named `stg_[source]__[entity]s`, materialized as views, with only type casting/renaming/basic computation — no joins, no aggregations [2]. Double underscores separate source and entity names. Subdirectories organized by source system (not business domain) to enable `dbt build --select staging.stripe+` selectors [2].

**Marts should be denormalized, entity-grained, and escalated from views only when needed** (MODERATE). Start with views, graduate to tables when query performance degrades, use incremental models when table build time exceeds acceptable thresholds [3][6]. Favor denormalization to reduce repeated join computation [3]. However: this "default to views" guidance is qualified for Databricks Unity Catalog environments where Delta tables are the platform default — applying dbt's warehouse-agnostic materialization advice directly can introduce significant build-time overhead (Qualified — Challenge 2.2).

**The intermediate layer is a composition zone, not a business layer** (HIGH). `int_` prefix models exist to assemble logic needed before mart-level joins — they should not be named after business concepts. Use intermediate models when marts would otherwise require 5+ CTEs or join more than 4-5 concepts [3][1].

---

### Sub-question 3: Data Quality Frameworks and Testing

**Data quality in dbt has a well-established minimum floor** (HIGH — T1 convergent). Every model requires at minimum: a primary key test for uniqueness and a not_null test [6][14]. Beyond that: `accepted_values` for categoricals, `relationships` for foreign key integrity. Use `result:<status>` selectors to intelligently re-run only failing tests in CI [6].

**The complementary-use pattern for dbt tests + GX is directionally correct but over-recommends GX** (MODERATE, Qualified). Sources [10] and [14] recommend using Great Expectations for source data validation (outside dbt) and dbt tests for transformations. The challenger found GX adoption friction is a documented problem — many teams find `dbt-expectations` and `dbt-utils` packages sufficient for 80-90% of use cases without GX's operational overhead (Qualified — Challenge 3.1). GX is the right choice for organizations needing automated Data Docs for compliance or advanced statistical validations; otherwise, prefer dbt-native packages.

**The document's "testing" framing covers only one tier of data quality** (HIGH confidence this is a gap). All sources address build-time or scheduled testing. Production data quality increasingly depends on a second tier — runtime observability (anomaly detection, volume drops, freshness SLAs, schema drift) — which is a distinct category requiring different tooling (Monte Carlo, Metaplane, SYNQ) not covered by any source (Gap — Challenge 3.2). For production pipelines, testing alone is insufficient.

**Elementary's anomaly detection fills the monitoring gap within the dbt ecosystem** (LOW-MODERATE — T3 vendor source). Elementary provides volume, freshness, and dimension anomaly detection as a dbt package, surfaced in a UI [11]. Note vendor bias — Elementary sells this capability.

---

### Sub-question 4: Schema Evolution and Data Contracts

**dbt model contracts enforce transformation output schema, not cross-team source contracts** (HIGH — T1 source, Contradicted for broader claim). When `enforced: true`, dbt's preflight checks verify column names and data types before materialization [5]. This is a strong governance mechanism within the analytics engineering layer. However, it governs only what dbt builds — it cannot intercept upstream application engineers who modify the source data shape before it reaches the pipeline (Contradicted for "cross-team" framing — Challenge 4.1). Define contracts after models stabilize; introducing governance during active development complicates future changes [5].

**Backward compatibility is the correct default for schema evolution** (HIGH — multiple sources converge). Core rules: always provide defaults for new fields, never remove required fields (deprecate instead), avoid type changes even for safe conversions, use field aliases for renames [12][13]. These principles apply across warehouse and streaming contexts. Zero-downtime implementation uses the expand-and-contract pattern: add new column, migrate reads, migrate writes, remove old column [13]. Note: the schema registry / Avro compatibility framing in sources [12] is streaming-specific — warehouse ALTER TABLE ADD COLUMN is typically non-breaking by default without registries (Qualified — Challenge 4.3).

**Data contracts succeed or fail on organizational design, not technical implementation** (MODERATE — Gap in current sources). The three technical components of a data contract are: ownership (who maintains it), explicit expectations (binary, unambiguous criteria), and documentation (rationale) [11]. The challenger found that producer incentive misalignment is the dominant implementation failure mode in practice — software engineers are measured on feature velocity, not downstream data quality. Contract success requires organizational commitment before technical implementation (Gap — Challenge 4.2).

**Schema change frequency demands automation** (MODERATE — T2). Organizations experience schema changes approximately every 3 days across enterprise systems [13]. Manual governance at this rate is unsustainable; automated detection, CI/CD integration, and phased enforcement (warning → soft fail → hard fail) are necessary components [13].

---

### Sub-question 5: Naming, Documentation, and Code Organization Conventions

**Core SQL naming conventions are high-consensus** (HIGH — T1 + T3 converge). Apply snake_case everywhere — schemas, tables, columns. Plural model names (`customers`, not `customer`). Primary key pattern: `[table]_id`. Boolean prefix: `is_` or `has_`. Timestamp suffix: `_at` in UTC. Date suffix: `_date`. Avoid abbreviations; use business terminology, not source system terminology [4][15]. These conventions are the strong community default.

**Layer prefixes have high consensus for staging and intermediate, less for marts** (MODERATE — Qualified). `stg_` for staging and `int_` for intermediate are universally adopted. The mart layer is contested: dbt Labs guidance avoids prefixes for marts (use plain entity names: `customers`, `orders`); some consultancies add `mart_`; Kimball-influenced teams add `fct_`/`dim_` prefixes at the mart level [4][15]. This disagreement is not a defect — teams should pick one convention and enforce it consistently (Qualified — Challenge 5.1).

**git workflow conventions are high-consensus** (HIGH — T1 + T3 converge). All projects in version control, feature branches per model/feature, PRs before merging to main, codified style guide committed to the repo [6][15]. Commit message format: `type(scope): description` (`feat(staging): add new source table`) [15]. I/O separation: read/write functions must be separate from transformation logic to enable independent testing [14].

**All conventions in this document are SQL/dbt-specific** (HIGH confidence this is a scope limitation). Python transforms, Spark pipelines, and streaming architectures operate under different conventions (PEP 8, class-based patterns, domain-specific schemas). The findings in this section should not be extrapolated beyond dbt-managed SQL transformation layers (Gap — Challenge 5.2).

---

### Key Takeaways

1. **ELT + dbt staging/marts is the analytics engineering consensus**, but carries vendor consolidation risk following the 2025 Fivetran/dbt merger. Evaluate SQLMesh for new projects.
2. **The three-layer model (staging → intermediate → marts) is justified at scale**; small teams may not need the intermediate layer.
3. **Data quality is three tiers** (testing, monitoring, observability) — current best practices only address the first. Production pipelines require runtime observability tooling.
4. **Data contracts govern the transformation layer, not upstream sources** — organizational incentive alignment matters more than technical implementation.
5. **Naming conventions are high-consensus at the column level, contested at the mart/model-prefix level** — choose and enforce consistently.
6. **Large coverage gaps exist**: streaming pipelines, non-SQL transforms, AI/ML patterns, and FinOps considerations are absent from all sources.

## Claims

| # | Claim | Type | Source | Status | Notes |
|---|-------|------|--------|--------|-------|
| 1 | ELT is now "the standard" for contemporary analytics | quote | [7] | verified | Source says "ELT is the standard. It's cheaper to run, easier to scale, and better aligned with tools like dbt" |
| 2 | Schema modifications occur "every 3.03 days" across typical enterprise systems | statistic | [13] | verified | Exact wording confirmed: "averaging one modification every 3.03 days across typical enterprise systems" |
| 3 | SQLMesh is "~9x faster" than dbt Core (Databricks benchmark) | statistic | challenger (no listed source) | removed | Specific benchmark figure had no cited primary source. Findings updated to "substantial build-time improvements" without specific number. Challenge 1.4 retains the claim as a gap note with appropriate attribution uncertainty. |
| 4 | Fivetran/dbt merger occurred in October 2025 | attribution | challenger (no listed source) | corrected | Month "October" removed throughout — merger confirmed via [7] banner but specific month could not be confirmed. All references now read "2025 Fivetran/dbt merger." |
| 5 | Dagster is recommended for dbt integration by FreeAgent Engineering | attribution | [8] | verified | Article states "In our case, for our current requirements, this was Dagster" and notes Dagster's dbt integration works well because "with a few lines of code you can have a complete asset map of your DBT models" |
| 6 | Great Expectations has "300+ built-in expectations" | statistic | [10] | verified | Exact figure "300+ built-in expectations" appears multiple times in the Sparvi article |
| 7 | Dagster is described as "data focused" | quote | [8] | verified | "Data focused" appears as a listed Pro in the Sparvi article's Dagster section |
| 8 | Prefect is described as a "very flexible, modern orchestration framework" | quote | [8] | verified | Exact phrase appears in the Prefect Pros section of the FreeAgent article |
| 9 | Airflow's dbt integration is "task-based rather than data-focused" | characterization | [8] | verified | Article states Airflow dbt integration "was still a task based pipeline, not a data based one" — paraphrase in Raw Extracts is accurate |
| 10 | "Software Engineering practices (CI/CD, testing, multiple environments) are becoming more dominant in data tooling" | quote | [8] | corrected | Exact quote in source reads "CI/D" not "CI/CD" — apparent typo in original article. The Raw Extracts section quotes it correctly as "CI/D"; the document's quote in Findings uses "CI/CD" which is an inferred correction |
| 11 | "For most mid-to-large enterprises, Airflow remains the safest choice due to its maturity and ecosystem" | quote | [9] | verified | Exact wording confirmed in the article's Recommendation section |
| 12 | Staging models have "one-to-one relationship: each staging model corresponds to exactly one source table" | paraphrase | [2] | verified | Source says "Staging models should have a 1-to-1 relationship to our source tables. That means for each source system table we'll have a single staging model referencing it" |
| 13 | Double underscore "helps visually distinguish the separate parts in the case of a source name having multiple words" | quote | [2] | verified | Exact wording confirmed |
| 14 | "Storage is cheap and it's compute that is expensive and must be prioritized" | quote | [3] | corrected | Exact source wording: "in the modern data stack storage is cheap and it's compute that is expensive and must be prioritized as such" — Raw Extracts omits "in the modern data stack" and "as such" from the framing |
| 15 | dbt model contracts define "a set of parameters validated during transformation" | quote | [5] | verified | Exact wording confirmed in page meta description and body |
| 16 | "dbt will verify that your model's transformation will produce a dataset matching up with its contract, or it will fail to build" | quote | [5] | verified | Exact wording confirmed |
| 17 | "Introducing governance while models are still changing can complicate future changes" | quote | [5] | verified | Exact wording confirmed |
| 18 | "Most streaming platforms default to backward compatibility because it is the most common requirement and allows consumers to lag behind producers" | quote | [12] | verified | Exact wording confirmed |
| 19 | "The Schema Registry validates that the new schema is compatible with previous versions before assigning an ID" | quote | [12] | verified | Exact wording confirmed |
| 20 | Data contracts are "formal agreements between data producers and consumers" | quote | [11] | corrected | Source says "Data contracts are agreements between data producers and data consumers" — Raw Extracts adds "formal" which is not in the source |
| 21 | "If a contract can be removed in failure without downstream disruptions, it shouldn't exist" | quote | [11] | corrected | Exact source wording: "If a contract can be removed in the case of failure, without any downstream disruptions, it's a good sign that it should have never been added at all" — the quoted version in the document is a condensed paraphrase, not exact |
| 22 | "Most frameworks/tools propose their version of the 3-hop architecture" | quote | [14] | verified | Exact wording confirmed |
| 23 | "Function to read/write data (I/O) must be separate from the transformation logic" | quote | [14] | verified | Exact wording confirmed |
| 24 | "Keep folder depth under 4 levels and establish naming standards early" | quote | [14] | corrected | First clause not confirmed in source [14]. Changed to paraphrase in Raw Extracts: removed direct quotes around folder-depth guidance; retained naming conventions guidance which was verified. |
| 25 | "Use names based on the business terminology, rather than the source terminology" | quote | [4] | verified | Confirmed with example context in source |
| 26 | Column ordering convention: IDs → strings → numerics → booleans → dates | convention | [4] | verified | Source lists: "ids, strings, numerics, booleans, dates, and timestamps" — verified order matches |
| 27 | The three-layer arc moves data from "source-conformed to business-conformed" | quote | [1] | verified | Source: "a cohesive arc moving data from source-conformed to business-conformed" — exact wording confirmed |
| 28 | Source [1] principle stated as "consistency over perfection" with quote "What's important is that you stay consistent" | quote | [1] | corrected | Source does not use the phrase "consistency over perfection." The actual wording is "what's important is that you think through the reasoning for those changes in your organization, explicitly declare them in a thorough, accessible way for all contributors, and above all stay consistent." The Raw Extracts shorthand "What's important is that you stay consistent" is an accurate extract of the final clause; the label "consistency over perfection" is the document author's paraphrase, not a source quote |

### CoVe Summary

- **Verified: 17 claims** (1, 2, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 22, 23, 25, 26, 27)
- **Corrected: 8 claims** (4, 10, 14, 20, 21, 24, 28, plus Claim 3 removed)
  - Claim 10: FreeAgent article uses "CI/D" not "CI/CD" — likely a typo in the original source; Findings section silently corrects it
  - Claim 14: Source [3] quote includes "in the modern data stack…as such" framing that the Raw Extracts version omits
  - Claim 20: "formal agreements" — the word "formal" is not in source [11]; source says "agreements between data producers and data consumers"
  - Claim 21: The contract-removal quote is a condensed paraphrase; source wording is materially longer and more conditional
  - Claim 28: "consistency over perfection" is the document author's label, not a source phrase; the extracted quote is accurate as a partial extract but the framing overstates directness
- **Unverified: 0 claims**
- **Removed: 1 claim** (3)
  - Claim 3: "~9x faster" SQLMesh benchmark — no source URL cited; challenger-only claim; specific number removed from Findings; qualitative reference retained in Challenge 1.4

**Post-verification corrections applied to document:**
- Claim 3: Specific benchmark number removed from Findings
- Claim 4: "October 2025" → "2025" throughout (month unverified)
- Claim 24: Folder-depth verbatim quote removed from Raw Extracts; converted to paraphrase

## Raw Extracts

### Sub-question 1: ETL/ELT Pipeline Architecture

**Source [7]:** https://www.getdbt.com/blog/data-integration

> ELT is now "the standard" for contemporary analytics, loading raw data first into a cloud warehouse then transforming in-platform using SQL. ELT reduces compute expenses and enables faster iteration compared to pre-load ETL. Three dominant architectures identified: (1) batch hub-and-spoke (declining), (2) cloud warehouse/lakehouse as central hub (BigQuery, Snowflake, Databricks), and (3) semantic layer as emerging standard for consistent metrics and business logic. Change data capture (CDC) and streaming add near-real-time capabilities for high-velocity workloads like fraud detection. Key 2025 priorities: define explicit data contracts between producers and consumers; build incrementally using testable models and automated alerting; implement version control and CI/CD for analytics code; monitor lineage, freshness, and spending continuously; position dbt as the transformation standard for governance and reliability.

**Source [8]:** https://engineering.freeagent.com/2025/05/29/decoding-data-orchestration-tools-comparing-prefect-dagster-airflow-and-mage/

> Orchestration tool comparison (hands-on evaluation, May 2025). Dagster is "data focused" with superior dbt integration and asset lineage visualization; weakness is reactive triggering via sensors rather than push-based events. Prefect is "very flexible, modern orchestration framework" with event-driven triggers; weakness is limited built-in data lineage. Airflow provides a mature ecosystem with proven scalability; weakness is that dbt integration lacks sophistication (task-based rather than data-focused). Mage offers easy AWS setup via Terraform modules but exposed a security vulnerability logging credentials in error output. Recommendation: use Dagster for teams prioritizing data lineage, dbt integration, and software engineering practices. "Software Engineering practices (CI/CD, testing, multiple environments) are becoming more dominant in data tooling."

**Source [9]:** https://www.tbdcdata.com/en/blog/airflow-vs-prefect-vs-dagster/

> Airflow uses DAG-as-code with a scheduler-based architecture and multiple executor options (Celery, Kubernetes) — largest community, massive operator library, proven enterprise scalability. Prefect uses `@flow` and `@task` Python decorators; separates orchestration control plane from code execution; superior developer experience and trivial local testing. Dagster centers on data assets rather than tasks — instead of defining workflow steps, you specify what data gets produced, enabling built-in lineage tracking and governance. Selection guidance: Airflow if you have existing investment or need max ecosystem compatibility; Prefect for greenfield projects prioritizing developer productivity; Dagster when data governance and asset management are primary requirements or building a data mesh. "For most mid-to-large enterprises, Airflow remains the safest choice due to its maturity and ecosystem." Many mature teams now employ multiple orchestrators with clear domain boundaries.

**Source [14]:** https://www.startdataengineering.com/post/de_best_practices/

> Follow a 3-hop (layered) architecture: Raw layer (store upstream data as-is with standardized column names) → Transformed layer (apply modeling principles: Dimensional modeling, Data Vault) → Consumption layer (combine tables for specific use cases; define business metrics once) → Interface layer (optional views for end-user accessibility). "Most frameworks/tools propose their version of the 3-hop architecture" including Databricks' Medallion architecture and dbt's project structure. DRY principle along two axes: Code (standard code in single locations) and Patterns (blueprints for consistent team standards). Separation of concerns: "Function to read/write data (I/O) must be separate from the transformation logic." Pipeline idempotence: prevent duplicates via Run ID-based overwrites or natural key UPSERTs. Track pipeline metadata including inputs/outputs, execution times, unique keys, storage location, schema, and partition keys.

---

### Sub-question 2: Data Transformation Layer Structure

**Source [1]:** https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview

> The guide establishes "a cohesive arc moving data from source-conformed to business-conformed." Three primary layers: (1) Staging — creates modular atomic building blocks from raw source data; (2) Intermediate — stacks layers of logic "with clear and specific purposes to prepare staging models to join into the entities we want"; (3) Marts — brings together modular pieces into comprehensive business-defined entities. Structural principles: consistency over perfection ("What's important is that you stay consistent"), decision reduction (structure minimizes unnecessary decision-making), modular design (disciplined layering enables applying transformations in only one place), and collaboration focus. File organization pattern: organize by layer (staging, intermediate, marts), then by business domain (finance, marketing), with naming prefixes (`stg_`, `int_`, `base_`).

**Source [2]:** https://docs.getdbt.com/best-practices/how-we-structure/2-staging

> Staging layer — naming convention: `stg_[source]__[entity]s.sql`. The double underscore "helps visually distinguish the separate parts in the case of a source name having multiple words" (e.g., `stg_google_analytics__campaigns`). Appropriate staging transformations: renaming columns, type casting, basic computations (cents to dollars), categorizing values with conditional logic. Explicitly avoid in staging: joins (except in specialized base model scenarios) and aggregations (these change grain and should happen downstream). Folder structure: organize subdirectories by source system, not by loader type or business grouping; enables selector syntax like `dbt build --select staging.stripe+`. Materialize as views: downstream models always access fresh data and avoids wasting warehouse space on non-final artifacts. One-to-one relationship: each staging model corresponds to exactly one source table.

**Source [3]:** https://docs.getdbt.com/best-practices/how-we-structure/4-marts

> Marts represent the entity layer — each mart focuses on a single entity at its natural grain (customers, orders, payments), with each row representing a discrete instance of that concept. Naming: group subfolders by business area (finance, marketing); use entity-based plain English names (`customers`, `orders`); avoid time-based rollups in mart names (those belong in metrics); one concept per mart — don't create `finance_orders` and `marketing_orders`, consolidate unless fundamentally different business rules apply. Materialization: start with views, escalate to tables when query performance degrades, then incremental models when table build time slows production runs. "Storage is cheap and it's compute that is expensive and must be prioritized." Favor denormalization: pack marts with all relevant entity data to reduce expensive recomputation from repeated joins. Limit joins complexity: 4–5 concepts is reasonable; beyond that, use intermediate models. Cross-mart dependencies are acceptable but require careful DAG management to avoid circular dependencies.

**Source [6]:** https://docs.getdbt.com/best-practices/best-practice-workflows

> Maintain distinct development and production environments using profile targets. Organize models hierarchically to enable selective runs and configuration management. Materialization hierarchy: default to views; use tables for BI consumption and models with many descendants; employ incremental models when build times exceed thresholds. Use custom schemas and naming prefixes (`stg_`, `fct_`, `dim_`) for clarity. Separate source-centric transformations from business-centric logic. Break complex models with multiple CTEs into smaller, testable pieces. Upstream dependency rules: marts should only reference marts or staging (never raw). Use `ref()` function exclusively for model dependencies; limit raw data references to sources to isolate schema changes. Slim CI: compare against production artifacts to run only modified models and tests.

---

### Sub-question 3: Data Quality Frameworks and Testing

**Source [10]:** https://www.sparvi.io/blog/great-expectations-vs-dbt-tests

> dbt Tests: four built-in test types (unique, not_null, accepted_values, relationships); native integration with dbt workflows; low learning curve; YAML-based configuration. Best when already using dbt, needing simple validation, or wanting everything in one repository. Great Expectations (GX): 300+ built-in expectations; comprehensive statistical validations (mean, median, distribution matching); works with diverse data sources (APIs, files, DataFrames, databases); automated Data Docs generation for compliance and auditing; pattern matching and cross-column comparisons. Ideal for advanced validation logic or testing data outside dbt ecosystems. Shared limitations: both are "testing frameworks" that validate when triggered — neither provides continuous monitoring, anomaly detection, built-in alerting, observability dashboards, or automatic data lineage tracking. Recommended patterns: (1) complementary use — GX for source data validation, dbt tests for transformations; (2) periodic profiling — daily dbt tests with deeper GE profiling weekly/monthly; (3) package hybrid — use `dbt-expectations` package for GE-style tests in dbt's YAML environment.

**Source [11]:** https://www.elementary-data.com/post/data-contracts

> Elementary dbt package provides tests for detection of data quality issues including anomaly detection on dimensions, columns, volume, and freshness. Schema change test is a middle ground: "With this test, dbt will still build the model but offer you a warning or a stopping error depending on the severity you have set." Contracts shift accountability upstream by catching breaking changes before stakeholders discover quality issues: "If a contract can be removed in failure without downstream disruptions, it shouldn't exist." Elementary provides a UI to visualize all dbt tests and detect anomalies.

**Source [14]:** https://www.startdataengineering.com/post/de_best_practices/

> Data quality workflow: generate data → check validity → log results → either publish or alert engineers. Use Great Expectations to separate expectations from code. Three test types: unit tests (individual functions), integration tests (multiple systems together), end-to-end tests (full system validation). Minimum standard: every model should have a primary key tested for uniqueness and non-null values. Track pipeline metadata including inputs/outputs, execution times, unique keys, storage location, schema, and partition keys.

**Source [6]:** https://docs.getdbt.com/best-practices/best-practice-workflows

> dbt testing strategy: implement data quality tests on model assumptions; minimum standard is every model having a primary key tested for uniqueness and non-null values. Use `result:<status>` selectors for intelligent rerun logic (error, fail, success, warning). Test sources for freshness and downstream impacts. Slim CI approach compares against production artifacts to run only modified models and tests, reducing costs and time.

---

### Sub-question 4: Schema Evolution and Data Contracts

**Source [5]:** https://docs.getdbt.com/docs/mesh/govern/model-contracts

> dbt model contracts define "a set of parameters validated during transformation." When `enforced: true`, dbt performs: (1) preflight checks — verifies query returns columns matching specified names and data types (order-independent); (2) DDL enforcement — constraints and column definitions included in database statements with platform-specific enforcement during build. "dbt will verify that your model's transformation will produce a dataset matching up with its contract, or it will fail to build." Contracts suit public models with downstream dependencies: models shared across teams or dbt projects, data feeding reports/dashboards/external systems, models in exposures. Breaking changes that trigger contract errors: removing columns, changing data types, modifying constraints, deleting/renaming contracted models. Best practice on timing: "Introducing governance while models are still changing can complicate future changes." Define contracts after models stabilize. Every column must be explicitly declared — no partial coverage. For incremental models with contracts, set `on_schema_change` to `append_new_columns` or `fail`; avoid `sync_all_columns` as it removes deleted columns.

**Source [12]:** https://www.conduktor.io/glossary/schema-evolution-best-practices

> Backward compatibility should be the default: "Most streaming platforms default to backward compatibility because it is the most common requirement and allows consumers to lag behind producers." Four foundational rules: always provide default values when introducing new fields; never eliminate required fields (deprecate instead); avoid modifying field types even for seemingly safe conversions; use field aliases for renaming rather than removing/adding fields. Schema Registry validates changes before deployment: "The Schema Registry validates that the new schema is compatible with previous versions before assigning an ID." Four migration approaches for breaking changes: dual-writing, versioned topics, transform-on-read, and coordinated deployment — each suited to different organizational contexts and timelines. Governance requirements: clear schema ownership, approval processes for breaking changes, regular schema reviews to identify technical debt.

**Source [13]:** https://airbyte.com/data-engineering-resources/master-schema-evolution

> Organizations experience schema modifications approximately every 3.03 days across typical enterprise systems. Primary approaches: automated detection with intelligent compatibility checking; schema-aware data formats (Avro, Parquet, Delta Lake); version control integration with CI/CD pipelines; central schema registries for governance. Backward compatibility ensures "existing applications and queries continue to function seamlessly, maintaining data integrity across versions." Techniques: default values and nullable fields as safety mechanisms; phased constraint enforcement (warning → soft failure → hard enforcement); schema validation with anomaly detection. Zero-downtime implementation: expand-and-contract pattern with dual writes enables gradual transitions. Modern patterns: data mesh (domain-owned, decentralized schemas), lakehouse architectures with native schema-evolution support, real-time CDC for streaming environments. Best practices: (1) communicate early with impact assessments across teams, (2) automate with comprehensive testing frameworks before production deployment, (3) monitor with real-time visibility into schema evolution impacts, (4) establish rollback procedures, (5) audit logging and compliance framework integration. Cross-functional reviews for significant changes help identify downstream impacts before implementation.

**Source [11]:** https://www.elementary-data.com/post/data-contracts

> Data contracts are "formal agreements between data producers and consumers. They clarify expectations about how the data should be produced and then used." Three essential components: (1) Ownership — clear assignment of responsibility for maintaining the contract; (2) Explicit Expectations — binary, unambiguous criteria (e.g., "field `created_at` must be timestamp"); (3) Documentation — rationale explaining why the contract exists and what it protects. Implementation patterns: dbt model contracts (DDL-level schema enforcement); Elementary tests (behavioral validation beyond schema — anomaly detection on dimensions, volume, freshness); schema change testing (flexible alerting when structural changes occur without blocking pipeline execution). "If a contract can be removed in failure without downstream disruptions, it shouldn't exist."

---

### Sub-question 5: Naming, Documentation, and Code Organization Conventions

**Source [4]:** https://docs.getdbt.com/best-practices/how-we-style/1-how-we-style-our-dbt-models

> Model naming: models should be pluralized (e.g., `customers`, `orders`, `products`). Primary keys: `<object>_id` pattern (e.g., `customer_id`). Use underscores not dots. Avoid abbreviations — prioritize clarity. Apply snake_case consistently across schemas, tables, and columns. Data type prefixes: Boolean columns prefix with `is_` or `has_`; timestamps as `<event>_at` in UTC (e.g., `created_at`); dates as `<event>_date`; currency in decimal format with suffixes for non-standard units (`price_in_cents`). Semantic consistency: "Use names based on the business terminology, rather than the source terminology." Maintain uniform field names across models for easier joins. Column ordering for readability: IDs (primary keys, foreign keys) → Strings → Numerics → Booleans → Dates → Timestamps. Version models with suffixes: `_v1`, `_v2`.

**Source [15]:** https://knowledge.businesscompassllc.com/dbt-naming-conventions-and-coding-standards-best-practices-for-modern-data-transformation/

> Layer-specific prefixes: `stg_` for staging, `int_` for intermediate, `mart_` for marts. Naming strategy: combine business domain, data granularity, and processing stage. Example: `finance_daily_revenue_summary` immediately communicates purpose and position in the pipeline. Column naming: primary keys `[table_name]_id` or `[table_name]_key`; dates `created_at`, `updated_at`, `effective_date`; booleans `is_` or `has_` prefix. File organization: `models/staging/` (by source system), `models/intermediate/` (by business domain), `models/marts/` (by business function). SQL structure order: SELECT → FROM → JOINs → WHERE → GROUP BY → HAVING → ORDER BY. Indentation: 4 spaces per level; no tabs. Line length: 80–100 characters for optimal code review. Comments: focus on "why" rather than "what." Version control: feature branches per model/feature set; commit message format with type prefixes (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`) and scope in parentheses (`feat(staging): add new source table`). Documentation: model descriptions should include business purpose, data sources and key transformations, refresh frequency and ownership. Column documentation: business definitions, null value handling, valid ranges, calculated field logic in business terms. Establish naming conventions early and document in a central place (company wiki, data catalog, or README in Git).

**Source [6]:** https://docs.getdbt.com/best-practices/best-practice-workflows

> All dbt projects should be managed in version control. Git branches for development of new features and bug fixes. Pull requests required before merging into production branches like `main`. Adopt a codified style guide covering SQL standards and naming conventions. Establish upstream dependency rules (marts can only reference marts or staging). Use the `ref()` function exclusively for model dependencies. Limit data in development using target-based filtering or environment variables. Separate source-centric transformations from business-centric logic.

**Source [14]:** https://www.startdataengineering.com/post/de_best_practices/

> DRY principle along two axes: Code (utility functions, base classes stay in single locations) and Patterns (blueprints for consistent team standards). "Function to read/write data (I/O) must be separate from the transformation logic" — enables easier testing of transformation logic, simpler debugging, and follows functional design principles. Keep folder depth shallow and establish naming standards early, enforcing them to prevent confusion. Good model naming conventions should assume the end-user will have no other context than the model name, as folders, schema, and documentation may not always be present.
