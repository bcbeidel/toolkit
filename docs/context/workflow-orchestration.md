---
name: "Workflow Orchestration for Agent Systems"
description: "State machine models, durable execution engines, phase gates, and resumability patterns for managing multi-phase agent workflows — from FSMs to Temporal and LangGraph"
metadata:
  type: reference
  sources:
    - https://www.sciencedirect.com/science/article/pii/0167642387900359
    - https://users.cs.northwestern.edu/~robby/courses/395-495-2017-winter/Van%20Der%20Aalst%201998%20The%20Application%20of%20Petri%20Nets%20to%20Workflow%20Management.pdf
    - https://temporal.io/blog/temporal-replaces-state-machines-for-distributed-applications
    - https://docs.langchain.com/oss/python/langgraph/durable-execution
    - https://stately.ai/docs/xstate
    - https://www.restate.dev/what-is-durable-execution
  related:
    - docs/research/workflow-orchestration.md
    - docs/context/agent-state-persistence.md
    - docs/context/agentic-planning-execution.md
    - docs/context/multi-agent-coordination.md
---

Agent workflows that span multiple phases — research, synthesis, review, revision — need orchestration models that handle branching, failure recovery, and auditability. The choice of model depends on workflow complexity, and the options form a clear spectrum.

## The Model Spectrum

**Finite State Machines (FSMs)** work for linear 3-5 state processes but suffer state explosion with concurrency: N independent binary properties require 2^N states. Most non-trivial agent workflows outgrow flat FSMs quickly.

**Harel Statecharts** (1987) solve this through three extensions: hierarchy (substates), orthogonality (concurrent regions), and broadcast communication. Two orthogonal regions of 4 states each need only 8 states instead of 16. XState implements statecharts in JavaScript/TypeScript, making the formal model practical. Agent systems typically need at least statechart-level expressiveness.

**Petri Nets** (specifically van der Aalst's Workflow Nets) model concurrency through tokens flowing through a bipartite graph. Their unique contribution is the soundness property — a formal guarantee that every execution reaches completion without deadlocks. Valuable for verification, but few production agent systems use them directly.

## Durable Execution Engines

Modern engines have shifted from explicit state machines to "durable execution," where the engine automatically captures and restores state.

**Temporal** records every action in an immutable Event History via event sourcing. On failure, Workers replay events to reconstruct exact pre-failure state, then resume. Developers write sequential code; the engine handles persistence. Temporal also supports the Saga pattern for compensating transactions when multi-step processes fail partway through.

**LangGraph** brings this specifically to LLM agents. Workflows are graphs with State (shared data), Nodes (agent logic), and Edges (conditional transitions). Three durability modes trade performance for recovery guarantees: "exit" (fastest, no intermediate recovery), "async" (balanced), "sync" (full durability). Its Time Travel feature enables checkpoint-based replay for debugging non-deterministic agent behavior.

**XState + Restate** combines formal statechart implementation with durable event loops. Each state transition is a separate Restate invocation with persisted state. Virtual Objects provide isolated state per workflow execution with single-writer guarantees.

## Phase Gates and Transition Rules

Phase gates are decision checkpoints that prevent premature advancement. Guard conditions — boolean predicates on transitions — make rules explicit, testable, and auditable. Four transition patterns matter for agent workflows:

- **Sequential:** Phase N completes before N+1 begins. Use when phases are inherently dependent.
- **Conditional:** Different next phases based on evaluation. If research quality is below threshold, return to gathering rather than advancing to synthesis.
- **Parallel convergence:** Multiple concurrent sub-processes must all complete before the parent advances (Petri net join semantics).
- **Escalation:** After N failed gate attempts, escalate to a different handler (human review, alternative strategy).

Gates should be forward-looking: early phases permissive (don't kill weak signals), late phases demanding (don't waste resources).

## Resumability Patterns

Three patterns dominate crash recovery. **Event sourcing** persists every state change as an immutable event; current state is reconstructed by replay. Complete audit trail but event logs grow and need periodic snapshots. **Checkpointing** saves periodic state snapshots (LangGraph's approach) — simpler but loses intermediate replay ability. **Deterministic replay** (Temporal) records results of non-deterministic operations; on replay, workflow code re-executes but external calls return recorded results. This requires workflow code itself to be deterministic.

## DAGs vs. State Machines

DAGs are completion-driven (transition when work finishes) and suit batch processing. State machines are event-driven (transition on external events) and suit interactive, long-running processes. The critical distinction: DAGs prohibit cycles, so "go back to research if synthesis fails" cannot be expressed as a DAG. However, simple linear pipelines gain nothing from state machine overhead. LangGraph and Temporal represent convergence — graph models that allow cycles, or sequential code with automatic state management — moving beyond the strict dichotomy.
