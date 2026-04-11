---
name: Distributed Resilience Stack — Circuit Breaker, Retry, Jitter
description: The resilience stack is bulkhead → circuit breaker → retry+jitter → DLQ; retry and circuit breaker must be tuned together or they create the retry storms they're meant to prevent.
type: context
sources:
  - https://calmops.com/software-engineering/circuit-breaker-pattern-resilience/
  - https://dev.to/andreparis/queue-based-exponential-backoff-a-resilient-retry-pattern-for-distributed-systems-37f3
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/saga
related:
  - docs/context/raft-consensus-and-event-sourcing-adoption-constraints.context.md
  - docs/context/saga-orchestration-vs-choreography-default.context.md
  - docs/context/opentelemetry-overhead-and-sampling-strategy-timing.context.md
  - docs/context/microservices-sizing-ddd-boundaries-and-default-monolith.context.md
---

# Distributed Resilience Stack — Circuit Breaker, Retry, Jitter

Four patterns form the distributed resilience stack. They are designed to compose, but the composition requires explicit tuning. Retry + circuit breaker without coordination creates retry storms — the exact failure mode the patterns exist to prevent.

## The Four-Pattern Stack

**1. Bulkhead** — isolate failure domains by limiting concurrent connections per downstream dependency. If one downstream service absorbs all available threads, healthy services remain unaffected. Cell-based architecture applies the bulkhead pattern at infrastructure scale.

**2. Circuit Breaker** — monitor calls to a remote service; stop requests when failure rate exceeds a threshold; fail fast instead of waiting for timeouts.

Three states:
- **CLOSED**: requests pass through normally; failures counted toward threshold
- **OPEN**: requests fail immediately with fallback response; no calls to the failing service
- **HALF-OPEN**: after recovery timeout, allow limited test requests; transition to CLOSED on success, back to OPEN on failure

Configuration parameters that require tuning: failure threshold (count to trigger OPEN), recovery timeout, success threshold to close, slow call timeout. Per-instance state is a known operational challenge: in a 10-instance deployment, each instance holds independent circuit state. Coarse-grained circuit breakers wrapping entire service endpoints misfire on partial shard failures.

**3. Retry with Exponential Backoff + Jitter** — retry transient failures with increasing delay; add randomness to prevent synchronized retry waves.

Formula: `delay = baseDelay × (multiplier ^ retryCount) + random(jitterRange)`

Jitter is not optional. Without it, multiple clients recovering from the same failure retry at identical intervals — the "thundering herd" problem recreates the original load spike on the recovering service at precisely the wrong moment.

Error-type configuration:
- Rate-limited errors: 60–300 second delays
- Temporary errors: 2–60 second delays
- Quota exceeded: 120–600 second delays
- Global cap: 60-second maximum per retry, 500-second maximum total

Non-retryable errors (4xx validation failures, business rule violations) must be detected and routed directly to DLQ. Retrying non-transient errors wastes resources and delays the inevitable DLQ routing.

**4. Dead Letter Queue (DLQ)** — capture messages that exhaust all retry attempts without processing; preserve for analysis and reprocessing without blocking healthy message flow.

DLQ implementation requirements:
- Detailed error metadata per captured message
- Monitoring and alerting on DLQ ingress rate — a rising rate is a leading indicator of systemic failure
- Automated reprocessing workflows after root-cause resolution
- 14-day minimum retention for post-incident investigation and compliance
- AWS SQS: native DLQ support; Apache Kafka: implement via error topics in consumer handlers

## The Composition Problem

Combining circuit breakers and retry without coordination creates a failure amplification loop:
- Retry logic fires on a failing service
- The circuit breaker is too slow to open (threshold too high or recovery timeout too long)
- Multiple clients retry at full speed against a recovering service, prolonging the outage

Coordination requirements:
- Circuit breaker failure threshold should be below retry `maxAttempts` so the circuit opens before retries are exhausted
- Retry `maxElapsedTime` should be shorter than circuit breaker recovery timeout to avoid retrying through an OPEN circuit
- Non-transient errors classified as non-retryable must route to DLQ immediately — not cycle through retry + breaker

## Implementation Libraries

Resilience4j (Java), Polly (.NET), pybreaker (Python), gobreaker (Go), opossum (Node.js) all implement the circuit breaker pattern with configurable thresholds. Most include retry policies. Check that the composition model (retry wrapping breaker, or breaker wrapping retry) matches your intended behavior before configuring.

## Takeaway

Implement all four patterns as a composed unit. Tune retry and circuit breaker together: align thresholds so the breaker opens before retries are exhausted. Classify error types explicitly — non-transient errors skip retry entirely. Monitor DLQ ingress rate as the primary signal that your resilience configuration needs adjustment.
