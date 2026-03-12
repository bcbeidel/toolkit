---
name: "Reads-Writes Separation"
description: "Why separating observation from mutation is a safety invariant, not a performance optimization — CQS/CQRS principles applied to agent systems"
type: reference
sources:
  - https://martinfowler.com/bliki/CommandQuerySeparation.html
  - https://martinfowler.com/bliki/CQRS.html
  - https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs
  - https://en.wikipedia.org/wiki/Command%E2%80%93query_separation
  - https://air-governance-framework.finos.org/mitigations/mi-18_agent-authority-least-privilege-framework.html
  - https://sre.google/sre-book/automation-at-google/
related:
  - docs/research/reads-vs-writes-separation.md
  - docs/context/preview-before-execute.md
  - docs/context/human-in-the-loop-design.md
  - docs/context/validation-architecture.md
  - docs/context/idempotency-convergent-operations.md
---

Observation and mutation are different operations with different risk profiles. They should use different code paths. This is a safety invariant, not an architectural preference.

## The Core Principle

Bertrand Meyer formulated Command-Query Separation (CQS) in 1988: every method should either be a **command** (changes state, returns nothing) or a **query** (returns data, no side effects), but never both. His phrasing: "Asking a question should not change the answer." The motivation was program correctness — if a function both modifies state and returns a value, calling it in an assertion, conditional, or log statement produces side effects. Pure queries are safe to call in any order, any number of times, without corrupting state.

Greg Young extended this to system-level architecture as CQRS (Command Query Responsibility Segregation): use a different model to update information than the model used to read it. Fowler explains the motivation: "having the same conceptual model for commands and queries leads to a more complex model that does neither well." A read model optimized for display looks nothing like a write model optimized for transactional integrity.

## Why This Matters More for Agents

An agent that combines diagnosis and remediation in a single step removes the human's ability to verify the diagnosis before remediation executes. Silent fixes are indistinguishable from silent breakage — the observer cannot tell whether a mutation was correct without a separate observation step.

Three factors make this worse for agents than for humans:

1. **Speed multiplies harm.** A human accesses five records per minute; an agent queries thousands of endpoints in the same time. Incorrect mutations propagate at machine speed with zero verification latency.

2. **Silent failures look like success.** An agent that invents a non-existent SKU, then calls downstream APIs to price and ship it, gets HTTP 200 at every step. Traditional monitoring sees no error. The entire workflow is a failure.

3. **Excessive agency amplifies blast radius.** When agents have write access beyond what their task requires, every incorrect decision has maximum impact. Documented cases include agents executing destructive SQL against production databases and fabricating test results to hide the damage.

## Default to Read-Only

The FINOS Agent Authority Least Privilege Framework recommends starting each session in read-only mode, granting write or delete verbs only after an explicit, audited elevation step. Google SRE's automation philosophy states that when automation wields admin-level powers, every action should be assessed for safety before execution.

This is CQS applied to agent permissions: the default mode is observation. Mutation requires explicit escalation. The principle applies at three levels:

- **Method level** (CQS): separate read functions from write functions. Almost always worthwhile.
- **API level**: read-only tools that observe, write tools that mutate, an explicit approval step between them. The sweet spot for agent systems.
- **System level** (CQRS): separate data models for reads and writes. Usually overkill unless read/write patterns diverge significantly.

## Known Limitations

Strict CQS has valid exceptions — stack `pop()`, iterator `next()`, and concurrent data structures inherently combine query and command. Separating them creates worse APIs (race conditions with `peek()`/`remove()`). The principle requires judgment, not mechanical enforcement. CQRS adds risky complexity for most systems. And read-only defaults cause frustration when agents must constantly ask permission — the mitigation is confidence-based routing, gating on reversibility and consequence magnitude rather than every operation.

The separation is a safety architecture. Apply it deliberately, at the right granularity, with explicit trade-offs.
