---
name: Saga — Orchestration vs Choreography Default
description: Default to orchestration for sagas with more than 3 steps or conditional branching — choreography's implicit distributed state makes debugging partially compensated sagas substantially harder.
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://microservices.io/patterns/data/saga.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
  - https://temporal.io/blog/mastering-saga-patterns-for-distributed-transactions-in-microservices
related:
  - docs/context/raft-consensus-and-event-sourcing-adoption-constraints.context.md
  - docs/context/distributed-resilience-stack-circuit-breaker-retry-jitter.context.md
  - docs/context/microservices-sizing-ddd-boundaries-and-default-monolith.context.md
---
# Saga — Orchestration vs Choreography Default

The Saga pattern manages cross-service distributed transactions where each service owns its own database and two-phase commit is not viable. Choreography fits simple, stable workflows. Orchestration is structurally superior for anything with more than 3 steps or conditional branching. Default to orchestration.

## The Problem Sagas Solve

In a microservices architecture, a business transaction may span multiple services (order service, payment service, inventory service). No shared database means no distributed ACID transaction. The Saga pattern decomposes a distributed transaction into a sequence of local transactions, each updating its own database and publishing an event or message. If any step fails, compensating transactions undo the preceding steps.

## Orchestration vs Choreography

**Choreography — no central controller:**
- Each service publishes domain events that trigger reactions in other services
- Workflow state is implicit: it exists only in the aggregate position across multiple services' event logs
- Benefits: no single point of failure, lower infrastructure complexity for very simple workflows
- Drawbacks:
  - Debugging a stuck or partially compensated saga requires reconstructing full event history across all services
  - Adding a new workflow step requires modifying event consumers across multiple services
  - Risk of cyclic event dependencies as workflow complexity grows
  - Integration testing requires all participating services running simultaneously
  - End-to-end workflow monitoring and reporting require dedicated correlation tooling

**Orchestration — central coordinator:**
- A central orchestrator explicitly directs each participant what to do and tracks state
- Workflow state is explicit in the orchestrator's storage
- Benefits:
  - Stuck sagas are visible: the orchestrator knows which step failed and what compensation is pending
  - Conditional branching is expressed in the orchestrator, not scattered across consumers
  - Monitoring shows workflow progress in one place
  - "Single point of failure" concern is addressable via high-availability orchestrator deployment
- Drawbacks:
  - Orchestrator is a coordination dependency all participants must interact with
  - Additional infrastructure (orchestrator service or durable workflow engine)

## When to Use Each

**Use choreography for:** simple workflows with 2–3 fixed, linear steps; workflows unlikely to evolve; teams already invested in event-driven architecture where simplicity of infrastructure is a priority.

**Use orchestration for:** workflows with more than 3 steps; any workflow with conditional branching; business-critical transactions requiring compensating transaction tracking; workflows that must be monitored end-to-end; workflows that teams maintain over time and that will evolve.

The threshold is lower than most teams expect. Choreography's complexity compounds nonlinearly with workflow steps. A 3-step linear saga is manageable in choreography; a 5-step saga with one conditional branch is significantly harder; a 7-step saga with business-rule branching becomes operationally opaque.

## Key Saga Concepts

- **Compensable transactions**: steps that can be undone via an opposite-effect compensating action
- **Pivot transactions**: the "point of no return" — once this step commits, all subsequent steps must complete or their compensations must run
- **Retryable transactions**: steps following the pivot; must be idempotent so they can be safely retried

All saga steps should be idempotent: event delivery in distributed systems is at-least-once. A step receiving the same event twice must produce the same outcome as receiving it once.

## Data Anomalies to Guard Against

Cross-service saga execution creates consistency windows where partial state is visible:
- **Lost updates**: one saga overwrites another saga's uncommitted changes
- **Dirty reads**: a service reads another saga's intermediate (uncommitted) state
- **Fuzzy reads**: a saga reads inconsistent data due to a concurrent update mid-execution

Countermeasures: semantic locks on in-progress entities; commutative updates where possible; pessimistic view sequencing for read-heavy coordination.

## Takeaway

Default to orchestration for any saga beyond a simple 2–3 step linear flow. The "single point of failure" concern for orchestrators is solvable with high availability; the observability and debuggability problems of choreography at scale are structural. Build compensating transactions for every compensable step, ensure idempotency throughout, and monitor saga state from the orchestrator as the canonical source of workflow truth.
