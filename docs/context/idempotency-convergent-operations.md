---
name: "Idempotency and Convergent Operations"
description: "Patterns for operations safe to run repeatedly — convergence as the design goal, idempotency as the mechanism, and the declare-compare-converge loop that unifies IaC, migrations, and agent systems"
metadata:
  type: reference
  sources:
    - https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
    - https://inria.hal.science/inria-00555588/document
    - https://developer.hashicorp.com/terraform/tutorials/state/resource-drift
    - https://markburgess.org/blog_principles.html
    - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
  related:
    - docs/research/idempotency-convergent-operations.md
    - docs/context/agent-state-persistence.md
    - docs/context/workflow-orchestration.md
    - docs/context/tool-design-for-llms.md
---

Convergence is the design goal; idempotency is the mechanism. An idempotent operation produces the same result regardless of how many times it runs (f(f(x)) = f(x)). A convergent operation goes further: it drives a system toward a desired state from any starting point and stays there. Every system that needs retry safety — infrastructure-as-code, database migrations, agent document management — implements convergence through variations of the same fundamental pattern.

## The Declare-Compare-Converge Loop

The universal pattern across all domains examined:

1. **Declare** the desired state (not the steps to get there)
2. **Compare** desired state against actual state
3. **Apply** only the minimal corrections needed to converge

Terraform implements this as refresh-plan-apply: query providers for actual state, diff against declared configuration, execute only the delta. Ansible checks whether desired state already exists at the module level before acting — the `copy` module checksums file content before writing. CFEngine formalized this as "fixed point" thinking: every desired state is an achievable fixed point, and the system self-repairs from any initial state.

Database migrations use the same pattern with different primitives: `CREATE TABLE IF NOT EXISTS`, `CREATE OR REPLACE FUNCTION`, and migration tracking tables that record which migrations have applied (skipping already-applied ones).

## Two Categories of Operations

**Naturally idempotent (absolute state):** SET x = 5, PUT resource, overwrite file. These declare the final state regardless of current state — safe to repeat by construction.

**Not naturally idempotent (relative state):** INCREMENT x, APPEND to list, POST. Each application changes the result. These require idempotency infrastructure: unique request tokens, content-addressed storage, or upsert semantics.

Design agent operations as "set the state to X" rather than "add Y to the current state" whenever possible. The fewer relative operations in a system, the less idempotency infrastructure it needs.

## Agent-Specific Adaptation

LLM-generated content is non-deterministic — two runs of the same agent task produce different text. This means idempotency for agent operations must be defined structurally rather than at the content level. A document operation is idempotent when "the file exists with required sections and metadata," not when "the file contains identical bytes."

Three IaC patterns transfer directly to agent document management:

**Desired-state declarations.** Check if a file exists with correct frontmatter before writing; update only changed fields. Analogous to Ansible's module pattern.

**Content-addressed idempotency.** Hash structural properties (name, type, content outline) to detect whether a write is a duplicate or an update. Avoids the overhead of idempotency token infrastructure.

**Drift detection and reconciliation.** Periodically audit documents against expected state, detect missing fields or broken references, apply fixes. Directly parallels Terraform's refresh-plan-apply cycle.

## When Full Idempotency Infrastructure Is Not Justified

For single-agent systems with file-based persistence, full-file overwrites provide natural idempotency without additional infrastructure. Complexity emerges only with side effects (triggering reindexing, notifying other agents, updating references) or concurrent writes. The overhead of idempotency tokens and state tracking should be proportional to the cost of duplicate operations.

Concurrency requires more than idempotency. Idempotent operations can still race. Database migrations use advisory locks; IaC tools use state locking; CRDTs use mathematical properties (commutativity, associativity) to handle concurrent updates. Multi-agent document systems need explicit serialization or conflict resolution beyond idempotency alone.
