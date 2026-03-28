---
name: "Multi-Agent Coordination Patterns"
description: "Dispatch, context sharing, conflict prevention, and isolation patterns that have converged across major LLM agent frameworks (2024-2026)"
metadata:
  type: reference
  sources:
    - https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
    - https://arxiv.org/html/2503.03505v1
    - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/concurrent
    - https://docs.crewai.com/en/learn/sequential-process
    - https://code.claude.com/docs/en/sub-agents
    - https://openai.github.io/openai-agents-python/
    - https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
  related:
    - docs/research/multi-agent-coordination.md
    - docs/context/llm-capabilities-limitations.md
---

Multi-agent coordination has converged on a small set of patterns across all
major frameworks. The differences between frameworks are in abstraction level,
not in which patterns are available. Understanding these patterns matters more
than choosing a specific framework.

## Dispatch Patterns

Five dispatch patterns recur across Google ADK, LangGraph, CrewAI, Microsoft
Agent Framework, OpenAI Agents SDK, and Claude Code:

**Sequential pipeline.** Tasks execute in order, each receiving the prior
task's output. Best for workflows with strict ordering dependencies. Every
framework supports this.

**Fan-out / fan-in.** Independent tasks execute concurrently; results merge at
a synchronization point. LangGraph enforces merge semantics through typed state
reducers -- without a reducer, parallel writes to the same key raise an error.
Google ADK, Microsoft, and Claude Code all provide native parallel dispatch.

**Hierarchical delegation.** A coordinator routes work to specialist agents.
CrewAI models this as a corporate hierarchy with an auto-generated manager.
Google ADK uses a central coordinator with specialized sub-agents. OpenAI
Agents SDK supports an "agent as tool" approach where a planner calls other
agents as tools.

**DAG-based execution.** Tasks form a directed acyclic graph with prerequisite
edges. This subsumes sequential (linear DAG) and fan-out/fan-in (single-level
DAG). LangGraph's Send API enables dynamic map-reduce based on runtime
conditions.

**Dual-thread planning-acting.** A research-stage pattern separating planning
from execution into concurrent threads, with priority-based interruption. Shown
to reduce latency by overlapping plan and act phases, but demonstrated only in
game environments, not production coding tasks.

## Context Sharing

No framework has a universal answer for context sharing. Four mechanisms
dominate, each with distinct tradeoffs:

- **State reducers** (LangGraph): typed state dictionaries with merge
  functions. Most explicit and type-safe, but requires upfront schema design.
- **Task-output chaining** (CrewAI): each task's output becomes the next
  task's input. Simple but limited to sequential workflows without explicit
  configuration.
- **Conversation handoff** (OpenAI): full conversation history transfers
  between agents. Preserves chat context but lacks structured data sharing.
- **Centralized memory** (research/community): knowledge graphs or shared
  memory updated each timestep. Scales to many agents but requires access
  control.

Claude Code combines parent-child context isolation (subagents get focused
tasks, return results) with optional team-level communication where agents
stay aware of each other's changes.

## Conflict Prevention

The consensus approach is prevention over detection. Runtime conflict
detection is expensive and unreliable; the strongest systems prevent conflicts
by construction.

**Exclusive resource ownership** is the primary strategy: each file, endpoint,
or resource belongs to exactly one agent. This eliminates runtime conflict
detection entirely. Google ADK enforces it through coordinator routing; CrewAI
through role-based task assignment.

**State reducers** handle concurrent writes by defining merge semantics at
design time. Without a reducer, concurrent writes fail explicitly, forcing
developers to resolve conflicts before they occur.

**Pre-execution overlap analysis** is an emerging pattern where tools analyze
whether tasks risk touching the same files before parallel execution begins.
Not yet in major frameworks.

## Workspace Isolation

Three isolation strategies dominate for coding agents:

**Git worktrees** are the de facto standard. Each agent gets its own worktree
with a separate branch sharing the same repository history. Claude Code
provides built-in worktree support. Worktrees with no changes auto-clean;
those with changes persist for review. Effective for batched migrations where
multiple agents each handle a subset of files in parallel.

**Container isolation** provides stronger guarantees (separate filesystem,
processes, network) at higher overhead. Best for untrusted agent code or
agents needing distinct runtime environments.

**Deterministic workflow scoping** separates LLM reasoning from flow control.
YAML or code-defined workflows control execution order; the LLM handles
decisions within each step. Google ADK and OpenClaw both embody this principle.

## Key Tradeoffs

Exclusive resource ownership works cleanly for greenfield partitioning but
struggles with inherently shared resources (config files, package manifests).
Real codebases likely need hybrid approaches combining design-time ownership
with lightweight runtime detection.

Git worktrees share the `.git` directory -- agents could interfere via
concurrent git operations (rebases, force pushes). Pre-flight dependency
analysis before task assignment reduces this risk.

Context sharing remains the hardest problem. Combining structured state,
conversation history, and persistent facts across agents is still a manual
integration task across all frameworks.
