---
name: Microservices Sizing, DDD Boundaries, and the Default Monolith
description: Start with a modular monolith; extract microservices only when team scaling or independent deployment requirements explicitly justify the operational cost.
type: context
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-domain-driven-design
  - https://microservices.io/patterns/data/event-driven-architecture.html
  - https://microservices.io/post/architecture/2025/04/25/microservices-authn-authz-part-1-introduction.html
related:
  - docs/context/api-protocol-selection-rest-grpc-graphql.context.md
  - docs/context/api-backwards-compatibility-and-deprecation-protocol.context.md
  - docs/context/saga-orchestration-vs-choreography-default.context.md
  - docs/context/distributed-resilience-stack-circuit-breaker-retry-jitter.context.md
---

# Microservices Sizing, DDD Boundaries, and the Default Monolith

The most common microservices mistake is adopting them too early. A 2025 CNCF survey found 42% of microservices adopters have consolidated services back into larger units, reflecting the real operational cost differential. The correct default is a modular monolith with clear internal boundaries; extract services when team scaling or independent deployment requirements explicitly justify it.

## The Default: Modular Monolith

A modular monolith has clear internal boundaries between domains, deployable as a single unit. It provides the organizational benefits of clear ownership and separation of concerns without the operational costs of distributed systems:
- No inter-service network latency (microservices add 10–50ms per hop)
- No distributed transaction complexity
- No separate deployment pipelines per service
- Fewer moving pieces to monitor and debug

Extract a service when one of these conditions is genuinely met:
- A specific capability needs to scale independently due to resource profile divergence
- Team growth creates coordination overhead that a deployment boundary would eliminate
- An independent release cadence is required for regulatory, partner, or operational reasons

Do not extract services to "follow microservices best practices," to match an org chart, or to achieve perceived technical purity.

## When Microservices Are Warranted: DDD Boundaries

When microservices are appropriate, use DDD tactical patterns to size them correctly. Microsoft's guidance is the clearest formulation: **no smaller than an aggregate, no larger than a bounded context.**

Key DDD tactical patterns:
- **Aggregates** define transactional consistency boundaries. Keep them small — include only data that must remain consistent in a single transaction. Reference other aggregates by ID only (a `Delivery` service stores `DroneId`, not a reference to the full `Drone` object).
- **Bounded contexts** are the natural service boundary — a cohesive area where the domain model is internally consistent and shared with a specific team.
- Design microservices around business capabilities, not horizontal layers. Do not create a "Data Access Service."
- Each service owns its database. No shared schema between services. Two services needing the same data maintain their own projections.

## Communication Patterns

**Synchronous (REST/gRPC):** Use for real-time queries where the caller needs a response to proceed. Vulnerable to cascading failure — downstream service degradation propagates upstream. Use circuit breakers and timeouts as baseline safeguards.

**Asynchronous (event-driven):** Use for write-heavy workflows, cross-service state changes, and scenarios tolerating eventual consistency. Kafka for high-throughput streaming; RabbitMQ for message queuing with reliability guarantees.

**The atomicity problem.** A service that updates its database and publishes an event cannot do both atomically without infrastructure support. The Transactional Outbox pattern solves this at moderate throughput: write the event to an outbox table in the same DB transaction, then a separate process publishes to the broker. For high throughput, Change Data Capture (Debezium) is superior: lower latency, no application-layer relay, no outbox maintenance.

## Avoiding Common Pitfalls

- **Nano-services**: Services smaller than a single aggregate create distributed monolith problems without service benefits
- **Shared databases**: Multiple services sharing a schema creates hidden coupling that defeats service independence
- **Synchronous chains**: Long chains of synchronous service calls accumulate latency and amplify failure probability
- **Premature extraction**: Extracting before load characteristics are understood produces services sized for imagined, not actual, scaling needs

## Takeaway

Default to a modular monolith. Extract services against explicit, measurable criteria. When services are warranted, use DDD boundaries (aggregate → bounded context) as the sizing constraint, and favor asynchronous communication for cross-service state changes.
