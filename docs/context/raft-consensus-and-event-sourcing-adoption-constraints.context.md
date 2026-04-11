---
name: Raft Consensus and Event Sourcing Adoption Constraints
description: Raft is the de facto industrial consensus standard; event sourcing and CRDTs deliver real benefits but require strong justification before adoption due to operational complexity.
type: context
sources:
  - https://raft.github.io/
  - https://martinfowler.com/eaaDev/EventSourcing.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
  - https://redis.io/blog/diving-into-crdts/
related:
  - docs/context/saga-orchestration-vs-choreography-default.context.md
  - docs/context/distributed-resilience-stack-circuit-breaker-retry-jitter.context.md
  - docs/context/opentelemetry-overhead-and-sampling-strategy-timing.context.md
---

# Raft Consensus and Event Sourcing Adoption Constraints

Raft is the correct consensus algorithm for new distributed systems — industrially deployed, well-understood, and designed for understandability. Event sourcing and CRDTs are operationally expensive patterns that are more constrained than their reputations suggest. Both require explicit justification before adoption.

## Raft: The De Facto Standard

Raft was designed to be understandable, achieving equivalent fault tolerance and performance to Paxos while decomposing the problem into three comprehensible subproblems: leader election, log replication, and safety.

**Key safety property:** A majority of servers must agree before any command is committed. A 5-node cluster tolerates 2 simultaneous failures. The system halts rather than producing incorrect results when a quorum is unavailable — the correct failure mode for systems where data integrity outweighs availability.

**Production adoption:** etcd (Kubernetes metadata store), Consul (service mesh), CockroachDB, and Apache Kafka KRaft (replacing ZooKeeper) all use Raft. This breadth of adoption makes Raft the safe default for new systems requiring consensus.

Raft vs. Paxos: Raft only allows servers with up-to-date logs to become leaders; Paxos allows any server and updates the log after election. Both achieve the same safety guarantees; Raft's design constraint makes it easier to implement and reason about correctly.

## Event Sourcing: Adopt in Bounded Contexts, Not System-Wide

Event sourcing stores every state change as an immutable event, making current state derivable by replaying the event log. The Azure Architecture Center (T2, updated 2026) states the governing constraint directly: "For most systems, traditional data management is sufficient."

**Genuine advantages:**
- Append-only writes avoid row-level lock contention, improving write throughput
- Automatic audit trail via the immutable event log
- State reconstruction to any point in time
- CQRS pairing for independent read/write scaling

**Real costs that teams underestimate:**
- Schema evolution under blue-green deployments requires version upcasters maintained indefinitely
- GDPR right-to-be-forgotten conflicts with append-only immutability; crypto-shredding partially mitigates this
- "Explanation tax": every new engineer must learn the event sourcing model and replay semantics
- CQRS pairing doubles query surface area and introduces consistency windows
- Teams applying ES to the full system typically report unsustainable complexity within 18–24 months

**Adopt event sourcing when:** audit trail, temporal reconstruction, or write throughput justify it in a specific bounded context. Do not apply system-wide.

**Do not use when:** simple CRUD systems without auditability requirements, prototypes or MVPs, teams without event-driven architecture experience, or mostly-static reference data.

## CRDTs: Mathematically Sound, Operationally Narrow

CRDTs (Conflict-free Replicated Data Types) guarantee convergence without coordination via commutativity, idempotence, and associativity. Implementations exist for counters (G-Counter, PN-Counter) and sets (OR-Set). They are used in production in Redis Enterprise, Azure CosmosDB, and Figma.

**The practical constraints:**
- CRDTs work for specific data types and their defined merge functions. Business logic requiring domain-specific conflict resolution (e.g., account balances, inventory counts with minimum constraints) cannot be expressed in general-purpose CRDT merges.
- Tombstone accumulation in sequence CRDTs (document editing) requires garbage collection coordination that reintroduces consensus-like coordination — the problem CRDTs were meant to avoid.
- Vector clock metadata scales poorly with replica count; memory and bandwidth costs grow with each node.
- "Strong eventual consistency" means replicas converge to the same byte sequence; it does not mean they agree on business-level semantics.

**Adopt CRDTs when:** collaborative apps (shared documents, presence indicators, distributed counters) where merge semantics align with defined CRDT types and conflict-free merging is acceptable.

## Takeaway

Default to Raft for any new distributed system requiring consensus. Evaluate event sourcing and CRDTs against explicit business requirements — not as default architectural patterns. Both patterns deliver real value in the right context; both create serious operational debt when adopted broadly without justification.
