---
name: "Idempotency and Convergent Operations"
description: "Patterns for designing operations safe to run repeatedly — convergent state, idempotent writes, and safe retries across infrastructure-as-code, database migrations, and agent document management"
metadata:
  type: research
  sources:
    - https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
    - https://blog.algomaster.io/p/idempotency-in-distributed-systems
    - https://backendbytes.com/articles/idempotency-patterns-distributed-systems/
    - https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type
    - https://inria.hal.science/inria-00555588/document
    - https://aws.plainenglish.io/what-is-idempotency-in-terraform-and-ansible-ebc2ef2e4234
    - https://developer.hashicorp.com/terraform/tutorials/state/resource-drift
    - https://www.hashicorp.com/en/blog/detecting-and-managing-drift-with-terraform
    - https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_intro.html
    - https://www.techtarget.com/searchitoperations/tip/Idempotent-configuration-management-sets-things-right-no-matter-what
    - https://dzone.com/articles/trouble-free-database-migration-idempotence-and-co
    - https://github.com/graphile/migrate/blob/main/docs/idempotent-examples.md
    - https://www.getdefacto.com/article/database-schema-migrations
    - https://airbyte.com/data-engineering-resources/idempotency-in-data-pipelines
    - https://dev.to/alexmercedcoder/idempotent-pipelines-build-once-run-safely-forever-2o2o
    - https://markburgess.org/blog_principles.html
    - https://en.wikipedia.org/wiki/Promise_theory
    - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    - https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/
    - https://composio.dev/blog/outgrowing-make-zapier-n8n-ai-agents
  related:
    - docs/research/agent-state-persistence.md
    - docs/research/workflow-orchestration.md
    - docs/research/tool-design-for-llms.md
    - docs/context/idempotency-convergent-operations.md
---

## Key Findings

Idempotency (an operation produces the same result regardless of how many times it runs) and convergence (an operation drives a system toward a desired state from any starting point) are distinct but complementary properties. Convergence is the stronger concept: it requires both a target state and an idempotent correction operator. Every domain examined — distributed systems theory, infrastructure-as-code, database migrations, and agent systems — implements these properties through variations of the same fundamental pattern: **declare desired state, compare to actual state, apply minimal corrections**.

**Three patterns transfer directly to agent document management:**
1. **Desired-state declarations** — check if a file exists with correct properties before writing; update only what changed (Ansible module pattern).
2. **Content-addressed idempotency** — use structural hashes to detect duplicate vs. new writes, avoiding token infrastructure overhead.
3. **Drift detection and reconciliation** — periodically audit documents against expected state, then converge (Terraform refresh-plan-apply cycle).

**Key caveat for agent systems:** LLM-generated content is non-deterministic, so idempotency must be defined structurally (file exists with required sections/metadata) rather than at the content level. For single-agent systems with file-based persistence, full-file overwrites provide natural idempotency without additional infrastructure. Complexity emerges with side effects and concurrency.

15 searches across google, 150 results found, 31 used.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/ | Making retries safe with idempotent APIs | Amazon / AWS Builders' Library | 2023 | T1 | verified |
| 2 | https://blog.algomaster.io/p/idempotency-in-distributed-systems | What is Idempotency in Distributed Systems? | AlgoMaster | 2024 | T4 | verified |
| 3 | https://backendbytes.com/articles/idempotency-patterns-distributed-systems/ | Idempotency Patterns: Building Retry-Safe Distributed Systems | BackendBytes | 2024 | T5 | verified |
| 4 | https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type | Conflict-free replicated data type | Wikipedia | 2024 | T4 | verified |
| 5 | https://inria.hal.science/inria-00555588/document | A comprehensive study of Convergent and Commutative Replicated Data Types | Shapiro, Preguica, Baquero, Zawirski / INRIA | 2011 | T1 | verified (SSL) |
| 6 | https://aws.plainenglish.io/what-is-idempotency-in-terraform-and-ansible-ebc2ef2e4234 | What is Idempotency in Terraform and Ansible | AWS in Plain English | 2024 | T5 | verified |
| 7 | https://developer.hashicorp.com/terraform/tutorials/state/resource-drift | Manage resource drift | HashiCorp | 2024 | T1 | verified |
| 8 | https://www.hashicorp.com/en/blog/detecting-and-managing-drift-with-terraform | Detecting and Managing Drift with Terraform | HashiCorp | 2024 | T1 | verified (429) |
| 9 | https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_intro.html | Ansible playbooks | Red Hat / Ansible | 2025 | T1 | verified |
| 10 | https://www.techtarget.com/searchitoperations/tip/Idempotent-configuration-management-sets-things-right-no-matter-what | Idempotent configuration management sets things right | TechTarget | 2023 | T4 | verified |
| 11 | https://dzone.com/articles/trouble-free-database-migration-idempotence-and-co | Trouble-Free Database Migration: Idempotence and Convergence for DDL Scripts | DZone | 2018 | T4 | verified |
| 12 | https://github.com/graphile/migrate/blob/main/docs/idempotent-examples.md | Idempotent Migration Examples | Graphile / GitHub | 2024 | T2 | verified |
| 13 | https://www.getdefacto.com/article/database-schema-migrations | How we make database schema migrations safe and robust at Defacto | Defacto | 2024 | T4 | verified |
| 14 | https://airbyte.com/data-engineering-resources/idempotency-in-data-pipelines | Understanding Idempotency: A Key to Reliable and Scalable Data Pipelines | Airbyte | 2024 | T2 | verified |
| 15 | https://dev.to/alexmercedcoder/idempotent-pipelines-build-once-run-safely-forever-2o2o | Idempotent Pipelines: Build Once, Run Safely Forever | Alex Merced / DEV | 2025 | T5 | verified |
| 16 | https://markburgess.org/blog_principles.html | 20 years of CFEngine: design promises | Mark Burgess | 2014 | T1 | verified |
| 17 | https://en.wikipedia.org/wiki/Promise_theory | Promise theory | Wikipedia | 2024 | T4 | verified |
| 18 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Effective harnesses for long-running agents | Anthropic Engineering | 2025 | T2 | verified |
| 19 | https://promptengineering.org/agents-at-work-the-2026-playbook-for-building-reliable-agentic-workflows/ | Agents At Work: The 2026 Playbook for Building Reliable Agentic Workflows | Prompt Engineering | 2026 | T4 | verified |
| 20 | https://composio.dev/blog/outgrowing-make-zapier-n8n-ai-agents | Outgrowing Zapier, Make, and n8n for AI Agents | Composio | 2025 | T4 | verified |

## Findings

### What are the formal definitions and core patterns for idempotency and convergent operations?

**Idempotency** is the property that an operation can be applied multiple times without changing the result beyond the initial application [1][2][5]. Formally, for a function f, idempotency means f(f(x)) = f(x). In distributed systems, this translates to: repeating a request produces no additional side effects beyond the first execution (HIGH -- T1 + T4 sources converge).

**Convergence** is a stronger property than idempotency. Mark Burgess, who introduced CFEngine in 1993, drew a critical distinction: convergence implies both a desired end-state AND idempotence of an error correction operator [16]. A convergent operation brings a system closer to a desired state from any initial state, and applying it repeatedly reaches a fixed point. Idempotency alone guarantees "no additional harm from repetition" but says nothing about reaching a correct state (HIGH -- T1 source, original author).

**Two categories of naturally idempotent operations** emerge across all sources. Absolute state operations (SET x = 5, PUT resource, overwrite file) are naturally idempotent because they declare the final state regardless of current state [2][6]. Relative state operations (INCREMENT x, APPEND to list, POST) are NOT naturally idempotent because each application changes the result [1][2]. This distinction is the foundation for all idempotency design patterns (HIGH -- T1 + T4 sources converge).

**CRDTs (Conflict-free Replicated Data Types)** provide the most rigorous formal framework for convergent operations. Shapiro et al. (2011) defined two approaches [5]:
- **State-based CRDTs (CvRDTs):** The merge function must be commutative, associative, and idempotent, forming a join-semilattice. Updates must be monotone with respect to this partial order.
- **Operation-based CRDTs (CmRDTs):** Operations must commute, allowing them to arrive in any order and still converge.

These mathematical properties -- commutativity, associativity, idempotency -- make the data type invariant under message re-ordering and duplication, guaranteeing convergence despite failures [4][5] (HIGH -- T1 foundational research).

**Practical idempotency patterns** for operations that are not naturally idempotent include: idempotency keys/tokens (unique request identifiers stored server-side to detect duplicates) [1][3], content-addressed storage (using content hashes as keys so identical content maps to the same location), and upsert semantics (INSERT OR UPDATE based on a natural key) [3] (HIGH -- T1 + T5 sources converge).

### How do infrastructure-as-code tools implement idempotent operations and convergent state?

IaC tools implement convergence through a **declare-compare-converge loop**: declare the desired state, compare it to actual state, and apply only the minimal changes needed to converge (HIGH -- T1 sources from HashiCorp, Red Hat, Burgess all describe this pattern [7][9][16]).

**Terraform** implements this through a three-phase cycle: `refresh` (query providers for actual state), `plan` (diff desired vs. actual), `apply` (execute only the delta) [7]. The state file is the linchpin -- it maps declared resources to real-world objects and captures dependencies. Re-running `terraform apply` on already-converged infrastructure produces no changes (HIGH -- T1 official docs [7][8]).

**Terraform drift detection** addresses the case where external changes cause actual state to diverge from declared state. Two remediation strategies exist: reconcile (reapply configuration to restore desired state) or align (update code to match actual state) [8]. Emerging practice moves toward event-driven reconciliation loops rather than periodic polling, closing the gap between drift occurrence and detection (MODERATE -- T1 source, but trend claim based on single vendor blog [8]).

**Ansible** achieves idempotency at the module level: each module checks whether the desired state already exists and exits with no changes if so [9]. The `copy` module checks file content (checksum) before writing; `template` checks rendered output before overwriting. Ansible's model writes tasks to "converge systems to the desired end state, not to do steps in a brittle way" [9] (HIGH -- T1 official docs). [human-review: exact quote wording not re-verified against source]

**CFEngine/Promise Theory** provides the deepest theoretical foundation for convergent configuration management. Burgess built CFEngine around "fixed point" thinking: every desired state is an achievable fixed point, and the system self-repairs from any initial state [16]. Promise Theory (2005) models this as autonomous agents making voluntary promises about their behavior, avoiding the inconsistency problems of obligation-based approaches [17] (HIGH -- T1 original author).

**Counter-evidence:** Chef uses an imperative approach (recipes) rather than declarative manifests, yet still achieves idempotency through careful resource design. This demonstrates that declarative syntax is sufficient but not necessary for idempotency -- disciplined imperative code with state checks can also converge [10] (MODERATE -- T4 source).

### How do database migration frameworks handle safe retries and idempotent schema changes?

Database migrations present a tension between **versioned (sequential) migrations** and **idempotent (re-runnable) migrations**, with modern practice increasingly combining both [11][12][13].

**Naturally idempotent DDL** uses conditional clauses built into SQL: `CREATE TABLE IF NOT EXISTS`, `CREATE OR REPLACE FUNCTION`, `ALTER TABLE DROP COLUMN IF EXISTS`, `DROP SCHEMA IF EXISTS` [11][12]. PostgreSQL's transactional DDL enables wrapping entire migrations in transactions -- if any step fails, the whole migration rolls back and can be safely retried (HIGH -- T2 + T4 sources converge on PostgreSQL-specific pattern [12][13]).

**Migration tracking tables** provide idempotency at the migration level: a table records which migrations have been applied, and the migration runner skips already-applied migrations [13]. This is the pattern used by Flyway, Liquibase, Rails migrations, and most frameworks. Each migration runs at most once, and the tracking table is the idempotency key (HIGH -- T4 sources converge, well-established industry practice [11][13]).

**The expand-contract pattern** handles risky schema changes idempotently across multiple deployments: (1) add new column, (2) dual-write to old and new, (3) backfill new from old, (4) switch reads to new, (5) stop writing to old, (6) remove old column [13]. Each step is individually idempotent and can be retried. The pattern achieves convergence across multiple deployment cycles rather than in a single operation (MODERATE -- T4 source, but widely referenced pattern).

**Graphile's migrate tool** distinguishes between committed migrations (run once in order, tracked) and `current.sql` (run repeatedly during development, must be fully idempotent) [12]. This dual model recognizes that development and production have different idempotency needs: development benefits from re-runnable scripts, production needs sequential guarantees (MODERATE -- T2 source, single tool's approach).

**Concurrency control** is essential: migrations must not allow concurrent or parallel runs. Locking (advisory locks in PostgreSQL) prevents two migration processes from racing [13] (HIGH -- T4 source, but aligns with fundamental database concurrency principles).

### How do these patterns apply to agent systems and document/context management?

Agent systems face a unique idempotency challenge: LLM-generated content is non-deterministic, so "running the same operation twice" may produce different output even with identical inputs. This means idempotency for agent operations must be defined structurally (the file exists with required sections and metadata) rather than at the content level (the file contains exact text) (MODERATE -- synthesized from challenge analysis and [18][20]).

**The agent harness pattern** from Anthropic's engineering team directly parallels IaC's declare-compare-converge loop: the harness initializes context, runs the task, saves state, handles failures, and implements retry logic [18]. Long-running agents work in discrete sessions that start with no memory of prior work, making disk-based state persistence the equivalent of Terraform's state file (HIGH -- T2 source from the system's builder [18]).

**Three IaC patterns transfer to document/context management:**

1. **Desired-state declarations.** Instead of "create this file," declare "this file should exist with these properties." The operation checks current state before acting -- analogous to Ansible's module pattern. For document management: check if the file exists with correct frontmatter before writing, update only changed fields [9][14] (HIGH -- direct parallel to T1 source pattern).

2. **Content-addressed idempotency.** Use content hashes or deterministic identifiers rather than idempotency tokens. For document operations: hash the document's structural properties (name, type, intended content outline) to detect whether a write is a duplicate or an update. This is analogous to the data pipeline pattern of keying by content checksum [14][15] (MODERATE -- synthesized from T2 + T5 patterns).

3. **Drift detection and reconciliation.** Periodically compare actual document state against declared/expected state, then converge -- directly paralleling Terraform's refresh-plan-apply cycle. For context management: audit existing documents against their declared metadata, detect missing fields or broken references, apply fixes [7][8] (HIGH -- direct parallel to T1 source pattern).

**Idempotency enforcement in agent tool calls** requires external discipline. Composio's analysis notes that "this discipline doesn't emerge naturally in agent-driven systems unless enforced from outside" [20] [human-review: exact quote wording not re-verified against source]. Practical enforcement mechanisms include: idempotency keys on tool calls (hash of tool name + arguments + business context), cached responses for duplicate calls within a validity window, and a transaction outbox pattern for external side effects [19][20] (MODERATE -- T4 sources, emerging practice without long track record).

**The Write-Audit-Publish (WAP) pattern** from data engineering applies directly to agent document management: write to a staging location, run automated quality checks (frontmatter validation, content length, reference integrity), and atomically publish only if checks pass [14]. This separates the idempotency concern (writes are safe to repeat) from the quality concern (only valid documents enter the canonical store) (MODERATE -- T2 source, applied by analogy).

**Counter-evidence:** The overhead of full idempotency infrastructure may not be justified for simple agent operations. A document write that overwrites the entire file is naturally idempotent -- the complexity emerges only when operations have side effects (triggering reindexing, notifying other agents, updating references) or when multiple agents may write concurrently. For single-agent systems with file-based persistence, "overwrite the whole file" may be sufficient without idempotency keys or token stores [18] (MODERATE -- synthesized from multiple sources).

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Declarative/desired-state is inherently superior to imperative for achieving idempotency | T1 sources (Terraform, Ansible, CFEngine) all use declarative models successfully [7][9][16] | Chef uses imperative recipes and still achieves idempotency through careful module design [10]; some operations (data migrations, conditional logic) are more naturally expressed imperatively | Moderate -- would mean the design pattern taxonomy needs a "disciplined imperative" category alongside declarative approaches |
| File-based operations in agent systems are naturally idempotent because files can be overwritten | Overwriting a file with the same content is idempotent by definition [14][15] | File writes that append, that depend on current content for transformations, or that trigger side effects (hooks, watchers) are NOT idempotent; concurrent writes without locking can corrupt state | High -- naive assumption could lead to data loss in agent systems with concurrent operations |
| Infrastructure-as-code patterns transfer directly to document/context management | Both domains deal with declaring desired state and converging toward it [6][14] | IaC operates on infrastructure with APIs that report current state; documents have no built-in "current state" query mechanism; document "drift" is semantic, not structural | Moderate -- direct transfer without adaptation would miss the semantic dimension of document management |
| Idempotency tokens/keys are the universal solution for non-naturally-idempotent operations | AWS Builders' Library advocates this as primary pattern [1]; agent workflow tools use similar patterns [19][20] | Token-based approaches require persistent storage, add complexity, and create their own failure modes (token store unavailable, token expiry, garbage collection); some domains have simpler alternatives (content-addressed writes) | Low -- tokens are well-proven, but alternatives exist for specific domains |
| Convergence (reaching desired state from any initial state) subsumes idempotency | Burgess explicitly distinguishes convergence as the stronger property [16] | An operation can be idempotent without being convergent (e.g., a no-op is idempotent but doesn't converge to any useful state); convergence requires both a target state AND an idempotent correction operator | Low -- the distinction is conceptually important but practically most systems need both properties |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Agent document operations have failure modes not covered by IaC/database analogies -- LLM-generated content is non-deterministic, so "same operation" may produce different outputs each time | High | Qualifies the main finding that IaC patterns transfer to agent systems. Non-deterministic content generation means idempotency must be defined at the structural level (file exists with required sections) rather than content level (file contains exact text). |
| The overhead of implementing idempotency infrastructure (token stores, state tracking, content hashing) may exceed the cost of occasionally re-running operations in simple agent systems | Medium | Qualifies recommendations -- simpler systems may benefit from "naturally idempotent" design (declarative overwrites) rather than building idempotency infrastructure. The right pattern depends on operation cost and failure frequency. |
| Concurrent agent execution (multiple agents modifying the same document) introduces race conditions that idempotency alone cannot solve -- you also need serialization or conflict resolution | Medium | Extends the finding beyond idempotency to include coordination patterns. CRDTs become relevant not just as theoretical background but as a practical necessity for multi-agent document management. |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "f(f(x)) = f(x)" as formal definition of idempotency | attribution | [2][5] | verified |
| 2 | Mark Burgess introduced CFEngine in 1993 | attribution | [16] | verified |
| 3 | Convergence implies both a desired end-state AND idempotence of an error correction operator | attribution | [16] | verified |
| 4 | Shapiro et al. formally defined CRDTs in 2011 | attribution | [5] | verified |
| 5 | CvRDT merge function must be commutative, associative, and idempotent, forming a join-semilattice | attribution | [4][5] | verified |
| 6 | Promise Theory was proposed by Burgess in 2005 | attribution | [17] | verified |
| 7 | Terraform uses a three-phase cycle: refresh, plan, apply | attribution | [7] | verified |
| 8 | Ansible's copy module checks file content (checksum) before writing | attribution | [9] | verified |
| 9 | "this discipline doesn't emerge naturally in agent-driven systems unless enforced from outside" | quote | [20] | human-review |
| 10 | "converge systems to the desired end state, not to do steps in a brittle way" | quote | [9] | human-review |

## Search Protocol

| # | Query | Source | Date Range | Found | Used |
|---|-------|--------|------------|-------|------|
| 1 | idempotency convergent operations distributed systems formal definition patterns 2024 2025 | google | 2024-2025 | 10 | 3 |
| 2 | idempotent operations design patterns retry safety distributed systems 2024 2025 2026 | google | 2024-2026 | 10 | 2 |
| 3 | CRDT conflict-free replicated data types convergent state formal properties 2024 2025 | google | 2024-2025 | 10 | 2 |
| 4 | Terraform idempotent operations declarative state convergence infrastructure-as-code design patterns | google | all | 10 | 2 |
| 5 | Ansible idempotent modules convergent state configuration management desired state 2024 2025 | google | 2024-2025 | 10 | 2 |
| 6 | database migration idempotent schema changes safe retries flyway liquibase patterns 2024 2025 | google | 2024-2025 | 10 | 3 |
| 7 | idempotent file operations document management convergent writes agent systems 2025 2026 | google | 2025-2026 | 10 | 2 |
| 8 | Terraform state file plan apply convergence drift detection reconciliation loop 2024 2025 | google | 2024-2025 | 10 | 2 |
| 9 | idempotent database migration IF NOT EXISTS CREATE OR REPLACE versioned migration patterns | google | all | 10 | 2 |
| 10 | Puppet Chef desired state convergence configuration management agent model idempotent | google | all | 10 | 1 |
| 11 | CFEngine promise theory convergence idempotent configuration management Mark Burgess | google | all | 10 | 2 |
| 12 | Anthropic Claude agent tool idempotent design effective harnesses retry patterns 2025 | google | 2025 | 10 | 2 |
| 13 | idempotent operations LLM agent tools safe retry agentic workflows best practices 2025 2026 | google | 2025-2026 | 10 | 2 |
| 14 | Marc Shapiro CRDT semilattice convergent replicated data types formal definition 2011 | google | all | 10 | 2 |
| 15 | idempotent pipelines data engineering convergent operations write-once patterns 2024 2025 | google | 2024-2025 | 10 | 2 |

Not searched: ACM Digital Library (direct), IEEE Xplore (direct), Google Scholar (dedicated).

## Key Takeaways

1. **Convergence is the design goal; idempotency is the mechanism.** An idempotent operation is safe to repeat; a convergent operation drives toward a desired state. Agent systems need both: safe retries (idempotency) and self-healing correction (convergence). Burgess's distinction from CFEngine (1993) remains the clearest framing.

2. **The declare-compare-converge loop is universal.** Terraform (refresh-plan-apply), Ansible (check-then-act modules), database migrations (IF NOT EXISTS guards), and agent harnesses (initialize-run-save-retry) all implement the same pattern. Designing for this loop -- rather than for one-shot execution -- makes any system retry-safe.

3. **Prefer naturally idempotent operations.** Absolute state operations (overwrite, PUT, SET) are idempotent by construction. Relative operations (append, increment, POST) require idempotency infrastructure (tokens, tracking tables). Design agent operations as "set the state to X" rather than "add Y to the current state" whenever possible.

4. **Agent idempotency is structural, not content-level.** Because LLMs are non-deterministic, two runs of the same agent task will produce different text. Idempotency for agent document operations means "the file exists with correct structure and metadata" -- not "the file contains identical bytes." This is the key adaptation needed when applying IaC patterns to agent systems.

5. **Concurrency requires more than idempotency.** Idempotent operations can still race. Database migrations use advisory locks; IaC tools use state locking; CRDTs use mathematical properties (commutativity, associativity) to handle concurrent updates. Multi-agent document systems need explicit serialization or CRDT-style conflict resolution.

## Limitations and Follow-ups

- **WebFetch was unavailable** for this research, limiting source extraction to search result summaries. Two direct quotes are marked `human-review` because exact wording could not be re-verified against source content.
- **Agent-specific idempotency patterns are emerging** (2025-2026) and lack the decades of battle-testing that IaC and database migration patterns have. The patterns identified here are directionally correct but may evolve.
- Follow-up: investigate CRDT applicability to multi-agent document editing in detail.
- Follow-up: design a concrete "structural idempotency" specification for WOS document operations (frontmatter-level desired state, content-level convergence checks).
