---
name: Agentic Fault Taxonomy and Interface Mismatch Pattern
description: "A 2026 empirical study of 13,602 issues across 40 repos identifies 37 fault types in 5 dimensions; the root cause pattern is probabilistic model outputs conflicting with deterministic interface constraints."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2603.06847
  - https://arxiv.org/abs/2512.07497
  - https://arxiv.org/abs/2503.13657
  - https://www.anthropic.com/research/building-effective-agents
related:
  - docs/context/multi-agent-shared-state-failure-mechanisms.context.md
  - docs/context/agentic-resilience-infrastructure-primitives.context.md
  - docs/context/agentic-failure-recovery-classify-retry-replan-abandon.context.md
---
# Agentic Fault Taxonomy and Interface Mismatch Pattern

**The most rigorous empirical grounding is the March 2026 arXiv fault taxonomy: 37 fault types across 5 dimensions, from 13,602 issues across 40 open-source agentic repositories, with 83.8% practitioner validation.** The core insight: "Many failures originate from mismatches between probabilistically generated artifacts and deterministic interface constraints."

## The Five Fault Dimensions (with fault counts)

| Dimension | Faults | Representative Types |
|-----------|--------|----------------------|
| Runtime & Environment Grounding | 87 | Dependency errors, environment misconfiguration, platform/API compatibility |
| Agent Cognition & Orchestration | 83 | LLM misconfiguration, token handling, agent termination failure, state inconsistency |
| Perception, Context & Memory | 72 | Memory persistence failure, type handling, validation omissions, encoding errors |
| System Reliability & Observability | 67 | Swallowed exceptions, missing error reporting, implementation defects |
| Tooling, Integration & Actuation | 66 | API misuse, parameter mismatch, auth failure, synchronization errors |

**Environmental/runtime failures are the most common category** — a non-obvious finding. This challenges the assumption that model reasoning failures dominate agentic production issues.

## Most Common Observable Symptom: Data Validation Errors

Data and validation errors represent 20% of observable symptoms — the highest of the 13 symptom classes. Schema validation at tool call boundaries is the highest-leverage prevention point. Every LLM output that crosses a tool boundary should be validated against a schema before execution routes it further.

## LLM-Specific Failure Archetypes

Four recurring patterns from a separate arXiv study (T3, December 2025):

1. **Premature action without grounding** — acting before verifying available context
2. **Over-helpfulness substitution** — fabricating missing data rather than acknowledging gaps
3. **Context pollution vulnerability** — distractor information interferes with decision-making
4. **Fragile execution under load** — performance degradation under complexity or volume

Critically: a 400B-parameter model only marginally outperformed a 32B model on uncertainty-driven tasks. Model scale is not a reliable reliability proxy.

## Multi-Agent Amplification

The MAST study (ICLR 2025, UC Berkeley — T2, 1,600+ annotated traces, kappa=0.88): 14 failure modes in three categories — system design issues, inter-agent misalignment, and task verification failures. Error amplification reaches 17.2x in poorly coordinated networks; centralized coordination contains this to approximately 4.4x.

## The Architectural Prescription

The interface mismatch pattern drives a clear structural response: **move interface constraints to deterministic layers** rather than trusting the model to honor them. This means:

- Schema validation on all LLM outputs before tool execution (not after)
- Typed tool interfaces with Pydantic or equivalent — catch mismatches structurally, not behaviorally
- Stopping conditions (iteration caps, cost caps) in infrastructure code, not prompt instructions
- Error classification at tool boundaries to route to retry/replan/abandon without model judgment

Prompts cannot enforce structural constraints reliably. The runtime can.

## Scope Limitation

The taxonomy was derived from open-source repositories, which skew toward developer tooling. Proprietary, enterprise, and multimodal agent failure modes may be underrepresented. Apply the taxonomy as a comprehensive starting checklist, not as a guaranteed exhaustive set.

## Takeaway

Data/validation errors are the most frequent observable symptom. Instrument every tool call boundary with schema validation. Treat runtime and environmental failures as the primary reliability target — not model reasoning quality, which is harder to control structurally.
