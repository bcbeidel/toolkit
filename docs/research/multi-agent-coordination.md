---
name: "Multi-Agent Coordination Patterns"
description: "Landscape survey of parallel dispatch, context sharing, conflict detection, and work scoping patterns across six major LLM agent frameworks and low-level execution models"
metadata:
  type: research
  sources:
    - https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
    - https://deepwiki.com/langchain-ai/langchain-academy/7.3-parallelization-techniques
    - https://arxiv.org/html/2503.03505v1
    - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/concurrent
    - https://docs.crewai.com/en/learn/sequential-process
    - https://github.com/rinadelph/Agent-MCP
    - https://code.claude.com/docs/en/sub-agents
    - https://openai.github.io/openai-agents-python/
    - https://google.github.io/adk-docs/agents/multi-agents/
    - https://langchain-ai.github.io/langgraphjs/how-tos/map-reduce/
    - https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool
    - https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them
  related:
    - docs/context/multi-agent-coordination.md
---

## Summary

Multi-agent coordination has converged on a small set of dispatch patterns,
context sharing mechanisms, and isolation strategies across all major
frameworks (2024-2026). The core patterns are:

- **Dispatch**: Sequential, parallel (fan-out/fan-in), hierarchical delegation,
  and DAG-based execution. Every major framework implements at least three of
  these. Dynamic map-reduce (LangGraph Send API) and dual-thread
  planning-acting (research) represent the frontier.
- **Context sharing**: Three dominant mechanisms -- state/reducer merging
  (LangGraph), task-output chaining (CrewAI), and conversation handoff
  (OpenAI). Shared knowledge graphs and centralized memory systems appear in
  research and community projects.
- **Conflict detection**: Prevention-first via exclusive resource ownership is
  the consensus approach. Runtime detection mechanisms (reducers, atomic
  supersteps, pre-execution file overlap analysis) supplement but do not
  replace design-time partitioning.
- **Work scoping**: Git worktrees have emerged as the dominant isolation
  pattern for coding agents, with container-based isolation as an
  alternative. Framework-level scoping uses agent hierarchies, deterministic
  workflow engines, and permission boundaries.

16 searches across Google, 160 results found, 46 used. 12 sources verified,
all reachable.

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/ | Developer's Guide to Multi-Agent Patterns in ADK | Google | 2025-12 | verified | T1 |
| 2 | https://deepwiki.com/langchain-ai/langchain-academy/7.3-parallelization-techniques | Parallelization Techniques - LangGraph | LangChain/DeepWiki | 2025 | verified | T4 |
| 3 | https://arxiv.org/html/2503.03505v1 | Parallelized Planning-Acting for Efficient LLM-based MAS | Xu et al. | 2025-03 | verified | T3 |
| 4 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/concurrent | Concurrent Agent Orchestration | Microsoft | 2025-07 | verified | T1 |
| 5 | https://docs.crewai.com/en/learn/sequential-process | Sequential Processes - CrewAI | CrewAI | 2025 | verified | T1 |
| 6 | https://github.com/rinadelph/Agent-MCP | Agent-MCP: Multi-Agent System | rinadelph | 2025 | verified | T5 |
| 7 | https://code.claude.com/docs/en/sub-agents | Create Custom Subagents - Claude Code | Anthropic | 2025 | verified | T1 |
| 8 | https://openai.github.io/openai-agents-python/ | OpenAI Agents SDK | OpenAI | 2025 | verified | T1 |
| 9 | https://google.github.io/adk-docs/agents/multi-agents/ | Multi-Agent Systems - ADK | Google | 2025 | verified | T1 |
| 10 | https://langchain-ai.github.io/langgraphjs/how-tos/map-reduce/ | Map-Reduce Branches for Parallel Execution | LangChain | 2025 | verified | T1 |
| 11 | https://dev.to/ggondim/how-i-built-a-deterministic-multi-agent-dev-pipeline-inside-openclaw-and-contributed-a-missing-4ool | Deterministic Multi-Agent Dev Pipeline (OpenClaw) | ggondim | 2025 | verified | T4 |
| 12 | https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them | Why Multi-Agent LLM Systems Fail | Augment Code | 2025 | verified | T4 |

## Findings

### 1. Parallel Dispatch Patterns

Five dispatch patterns recur across all surveyed frameworks (HIGH -- T1
sources from Google, Microsoft, LangChain, CrewAI, OpenAI converge):

**Sequential pipeline.** The simplest pattern. Tasks execute in order, each
receiving the prior task's output as context. Google ADK's SequentialAgent
"works like a classic assembly line where Agent A finishes a task and hands
the baton directly to Agent B" [1]. CrewAI's sequential process follows the
same model with "output of one task serving as the context for the next"
[5]. Microsoft Agent Framework includes a sequential orchestration pattern
[4]. Best for workflows with strict ordering dependencies.

**Fan-out / fan-in (parallel).** Independent tasks execute concurrently,
results merge at a synchronization point. LangGraph implements this through
graph topology with explicit fan-out and fan-in nodes [2]. Google ADK's
ParallelAgent "fans out work, running all its sub-agents at the same time"
[1]. Microsoft's concurrent orchestration "enables multiple agents to work
on the same task in parallel" with results "collected and aggregated" [4].
LangGraph enforces this through state reducers -- without a reducer,
parallel writes to the same state key raise an error [2]. LangGraph also
"ensures that all parallel branches complete before continuing to the next
step" [2].

**Hierarchical delegation.** A coordinator agent routes work to specialist
agents. CrewAI's hierarchical process "emulates a corporate hierarchy" where
an auto-generated manager "oversees task execution and allocates tasks to
agents based on their capabilities" [5]. Google ADK uses "a central
LlmAgent (Coordinator)" managing specialized sub-agents [9]. Microsoft's
Magentic pattern (from AutoGen's MagenticOne) uses "a dedicated Magentic
manager" coordinating "a team of specialized agents" for complex tasks [4].
OpenAI Agents SDK supports an "Agent as a Tool" approach where "one agent
(often a central planner or manager) calls other agents as if they were
tools" [8].

**DAG-based execution.** Tasks form a directed acyclic graph with
prerequisite edges controlling execution order. Xu et al. describe recursive
task decomposition via weighted DAG where "vertex set V={vi} represents
atomic tasks" with edges encoding dependencies [3]. LangGraph's Send API
enables dynamic map-reduce that "dynamically creates parallel tasks based on
runtime conditions" [10]. This is the most flexible pattern, subsumes both
sequential (linear DAG) and fan-out/fan-in (single-level DAG).

**Dual-thread planning-acting.** A research-stage pattern separating
planning from execution into concurrent threads. Xu et al.'s framework uses
"a dual-thread architecture" with "interruptible execution" -- the planning
thread generates actions while the acting thread executes them, with
priority-based interruption when "the LLM determines that the new action has
a higher priority than the current action" [3]. The latency advantage
follows from overlapping planning and acting: Tp=Tplan(1)+sum(max(Tplan(k),
Tact(k-1)))+Tact(n), versus serialized Ts=sum(Tplan(k)+Tact(k)) [3]
(MODERATE -- single T3 source, not yet replicated in production frameworks).

**Loop / iterative refinement.** Google ADK's LoopAgent implements
generate-critique-refine cycles [1]. Not strictly a dispatch pattern for
parallelism, but frequently composed with parallel dispatch -- e.g., parallel
fan-out for gathering, then iterative refinement of aggregated results.

#### Framework Comparison Matrix

| Framework | Sequential | Parallel | Hierarchical | DAG | Loop |
|-----------|-----------|----------|-------------|-----|------|
| Google ADK | SequentialAgent | ParallelAgent | Coordinator + sub_agents | Via composition | LoopAgent |
| LangGraph | Linear graph | Fan-out/fan-in nodes | Subgraphs | Send API map-reduce | Cycles in graph |
| CrewAI | Sequential process | Parallel tasks | Hierarchical process | Not native | Not native |
| MS Agent Framework | Sequential orch. | Concurrent orch. | Magentic (MagenticOne) | Via composition | Not native |
| OpenAI Agents SDK | Python orchestration | Python orchestration | Agent-as-tool | Python orchestration | Python orchestration |
| Claude Code | Subagent chaining | Agent Teams / worktrees | Parent-subagent | Not native | Not native |

### 2. Context Sharing Mechanisms

Four context sharing mechanisms emerge across the landscape (HIGH -- multiple
T1 sources converge on the taxonomy):

**State object with reducers.** LangGraph's primary mechanism. All nodes read
from and write to a shared typed state dictionary. Parallel updates merge
via reducer functions (e.g., `operator.add` concatenates lists) [2]. Custom
reducers can enforce deterministic ordering of parallel results. This is the
most explicit and type-safe approach but requires upfront state schema
design.

**Task-output chaining.** CrewAI's approach where each task's output becomes
the next task's input context. The `context` parameter customizes which
outputs feed into which tasks [5]. Simpler than state reducers but limited
to sequential workflows unless explicitly configured for parallel task
outputs. CrewAI also supports persistent memory across tasks via
`memory=True` [5].

**Conversation handoff.** OpenAI Agents SDK's pattern where agents transfer
an active conversation including full history. Agents have "complete
knowledge of your prior conversation" after a handoff [8]. Sessions provide
"a persistent memory layer for maintaining working context within an agent
loop" [8]. Preserves conversational context but does not support structured
data sharing.

**Centralized shared memory.** Xu et al.'s centralized memory system updates
at each timestep with observation records, chat logs, and action history
[3]. Agent-MCP uses a persistent knowledge graph where agents query via
`ask_project_rag` and update via `update_project_context` [6]. This
blackboard-style approach scales to many agents but requires careful
access control. Communication modes include passive (automatic after each
cycle) and active (agent-initiated) messaging [3].

**Hybrid patterns in practice.** Claude Code combines parent-child context
isolation (subagents get focused tasks, return results to parent) with
optional team-level communication (Agent Teams "stay in communication" so
"when the backend developer changes a data model, the frontend developer
hears about it immediately") [7]. Each subagent "maintains its own context
window, model configuration, and permission scope" [7].

### 3. Conflict Detection and Resolution

Conflict handling follows a prevention-first hierarchy (HIGH -- T1 and T4
sources converge):

**Exclusive resource ownership (design-time).** The consensus approach.
Augment Code states: "Each database table, API endpoint, file, or process
should belong to exactly one agent" [12]. This eliminates runtime conflict
detection entirely by making overlap impossible. Google ADK enforces this
through coordinator routing to non-overlapping specialist agents [9].
CrewAI's role-based task assignment achieves similar partitioning [5].

**State reducers (runtime merge).** LangGraph's reducer mechanism handles
concurrent writes to shared state by defining merge semantics upfront [2].
Without a reducer, concurrent writes raise an explicit error, forcing
developers to handle the conflict at design time. This is conflict
prevention through type-system enforcement rather than runtime detection.

**Atomic superstep failure (runtime).** LangGraph implements transactional
semantics for parallel execution where if one parallel node fails, the
entire superstep fails atomically, preventing partial state updates
(MODERATE -- described in LangGraph practitioner content [2] but exact
quote `unverifiable` against primary DeepWiki source; consistent with
LangGraph's documented reducer-based state management).

**Pre-execution overlap analysis (emerging).** Tools analyze whether tasks
risk touching the same files before parallel execution begins and "warn
when agents approach the same code regions during execution." CodeCompass
uses AST-based graph navigation to expose structural dependencies, enabling
agents to discover "semantically distant but architecturally critical files"
(MODERATE -- practitioner reports, not yet in major frameworks).

**Optimistic concurrency control.** The traditional database pattern where
transactions proceed without locks and verify at commit time. Applied in
some multi-agent file systems. If conflicts detected, the committing
transaction rolls back (MODERATE -- general pattern applied to agent
systems, limited framework-native support).

**File-level locking (emerging).** OpenClaw is adding file locking for
multi-agent file access [11]. This is the most direct conflict prevention
for coding agents but may create bottlenecks and deadlocks if not carefully
managed (LOW -- single community source, feature under development).

### 4. Work Scoping and Interference Prevention

Three isolation strategies dominate for coding agents (HIGH -- T1 sources
from Anthropic and practitioner reports converge):

**Git worktree isolation.** The dominant pattern for parallel coding agents.
Each agent gets its own worktree -- a separate working directory with its
own branch sharing the same repository history. Claude Code v2.1.50
provides built-in worktree support where subagents can use
`isolation: worktree` [7]. "Worktrees with no changes are automatically
cleaned up while worktrees with changes persist for your review" [7].
Incident.io runs four or five parallel Claude agents routinely using this
pattern. The pattern is especially effective for "batched code
migrations -- spawn 5 agents, each handling 10 files in their own worktree,
all running in parallel without stepping on each other."

**Container-based isolation.** Anthropic's Container Use provides "isolated
development environments" where "developers can safely run multiple agents
on the same codebase without interference." Stronger isolation than
worktrees (separate filesystem, processes, network) but higher overhead.
Best for untrusted agent code or when agents need distinct runtime
environments.

**Deterministic workflow scoping.** OpenClaw/Lobster separates LLM reasoning
from orchestration: "the LLM does not decide the flow" -- YAML workflows
control execution [11]. Each agent "functions as a fully scoped brain with
its own workspace, authentication profiles, and session store" [11].
maxConcurrentRuns configuration and lane/queue systems provide session
isolation. Google ADK's workflow agents similarly "control the execution flow
of other agents in predefined, deterministic patterns without using an LLM
for the flow control itself" [1].

**Hierarchical permission scoping.** Claude Code subagents operate in a
parent-child hierarchy where each subagent "maintains its own context
window, model configuration, and permission scope" [7]. The parent agent
retains control: subagents "get a focused task, execute it, and return the
result. The parent agent never loses control, and the subagent never needs
to talk to anyone else" [7]. This prevents scope creep and lateral
interference between siblings.

**Task decomposition via dependency graphs.** DAG-based decomposition ensures
agents work on genuinely independent subtasks. Prerequisite edges prevent
parallel execution of dependent work [3]. This structural guarantee is
stronger than runtime conflict detection because overlapping work is
impossible by construction.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Git worktrees are sufficient isolation for coding agents | T1 Anthropic docs [7], widespread practitioner adoption | Worktrees share .git directory; agents could interfere via git operations (rebases, force pushes) | Container isolation would be necessary default, increasing overhead |
| Exclusive resource ownership scales to large agent teams | T4 Augment Code [12], T1 Google ADK [1] routing design | As agent count grows, partitioning becomes harder; some resources are inherently shared (config files, package manifests) | Need runtime conflict detection, not just design-time prevention |
| Reducer-based state merging handles all parallel update scenarios | T1 LangGraph [2,10] with type-safe reducers | Complex merge conflicts (semantic conflicts, not just structural) cannot be resolved by simple reducers | Agents would need semantic conflict resolution, possibly LLM-mediated |
| Deterministic workflow engines are preferable to LLM-driven orchestration | T1 Google ADK [1], T4 OpenClaw [11] | LLM-driven routing offers more flexibility for novel task types; deterministic workflows require upfront design | Hybrid approaches (deterministic skeleton with LLM-driven routing at decision points) may win |
| Dual-thread planning-acting represents a performance frontier | T3 Xu et al. [3] with latency formulas | Only demonstrated in game environments (Minecraft); may not translate to coding tasks | Sequential planning-then-acting may be adequate for most production use cases |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| This landscape overfits to current frameworks; a dominant new framework could change all patterns | Medium | Pattern taxonomy would hold (sequential, parallel, hierarchical are fundamental) but framework recommendations would change |
| Conflict detection is treated as solved by design-time ownership, but real codebases have shared resources that make this impractical | High | Finding #3 would need qualification: ownership works for greenfield but real-world requires hybrid with runtime detection |
| Worktree isolation works for independent tasks but fails for tasks with implicit dependencies (shared types, APIs) | Medium | Finding #4 would need qualification: worktrees need pre-flight dependency analysis before task assignment |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Google ADK SequentialAgent "works like a classic assembly line" | quote | [1] | verified |
| 2 | Google ADK ParallelAgent "fans out work, running all its sub-agents at the same time" | quote | [1] | verified |
| 3 | Google ADK workflow agents "control the execution flow of other agents in predefined, deterministic patterns without using an LLM for the flow control itself" | quote | [1] | verified |
| 4 | LangGraph "ensures that all parallel branches complete before continuing to the next step" | quote | [2] | corrected (original: "automatically synchronizes branches with varying depths") |
| 5 | LangGraph atomic failure: "If one parallel node fails, the entire superstep fails atomically" | quote | [2] | unverifiable (not found in DeepWiki source; may originate from LangGraph forum or substack) |
| 6 | Microsoft concurrent orchestration "enables multiple agents to work on the same task in parallel" | quote | [4] | verified |
| 7 | CrewAI hierarchical process "emulates a corporate hierarchy" | quote | [5] | verified |
| 8 | CrewAI "output of one task serving as the context for the next" | quote | [5] | verified |
| 9 | OpenAI handoff gives agents "complete knowledge of your prior conversation" | quote | [8] | verified |
| 10 | Xu et al. dual-thread latency formula Tp vs Ts | statistic | [3] | verified |
| 11 | Xu et al. "vertex set V={vi} represents atomic tasks" | quote | [3] | verified |
| 12 | Augment Code: "Each database table, API endpoint, file, or process should belong to exactly one agent" | quote | [12] | verified |
| 13 | Claude Code subagents "get a focused task, execute it, and return the result" | quote | [7] | verified |
| 14 | Claude Code worktrees: "worktrees with no changes are automatically cleaned up" | quote | [7] | verified |
| 15 | Incident.io runs four or five parallel Claude agents routinely | attribution | -- | human-review |
| 16 | Claude Code v2.1.50 adds first-class worktree support | attribution | [7] | human-review |
| 17 | OpenClaw: "the LLM does not decide the flow" | quote | [11] | verified |
| 18 | Microsoft Magentic based on MagenticOne pattern from AutoGen | attribution | [4] | verified |
| 19 | OpenAI Agents SDK launched March 2025 replacing Swarm | attribution | [8] | human-review |
| 20 | Microsoft Agent Framework merges AutoGen with Semantic Kernel (October 2025) | attribution | [4] | human-review |

## Detailed Evidence

### Sub-Question 1: Parallel Dispatch Patterns

#### Source [1]: Developer's Guide to Multi-Agent Patterns in ADK (T1: official docs)
- **URL:** https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
- **Author/Org:** Google | **Date:** 2025-12

Google ADK defines three workflow agent primitives for deterministic execution:
- **SequentialAgent**: "works like a classic assembly line where Agent A finishes a task and hands the baton directly to Agent B. It is linear, deterministic, and easy to debug."
- **ParallelAgent**: "fans out work, running all its sub-agents at the same time, rather than in a sequence. This is highly efficient for tasks that don't depend on each other."
- **LoopAgent**: Generator creates a draft, Critique Agent provides optimization notes, Refinement Agent polishes output.

These workflow agents "control the execution flow of other agents in predefined, deterministic patterns without using an LLM for the flow control itself."

#### Source [2]: Parallelization Techniques - LangGraph (T4: expert practitioner)
- **URL:** https://deepwiki.com/langchain-ai/langchain-academy/7.3-parallelization-techniques
- **Author/Org:** LangChain/DeepWiki | **Date:** 2025

LangGraph implements fan-out/fan-in through graph topology:
- **Fan-out**: "Starting from a single node and branching out to multiple parallel nodes"
- **Fan-in**: "Combining the results from parallel nodes back into a single path"
- State updates merge via reducers. Without a reducer: "Can receive only one value per step. Use an Annotated key to handle multiple values."
- "Automatically synchronizes branches with varying depths."
- **Map-reduce via Send API**: "dynamically creates parallel tasks based on runtime conditions."
- Atomic failure: "If one parallel node fails, the entire superstep fails atomically."

#### Source [3]: Parallelized Planning-Acting for Efficient LLM-based MAS (T3: peer-reviewed)
- **URL:** https://arxiv.org/html/2503.03505v1
- **Author/Org:** Xu et al. | **Date:** 2025-03

Dual-thread architecture: planning thread "generates actions using Ait+1=LLM(S,Oit,Ct,Ait)." Acting thread executes with priority-based interruption: "If an interruption is triggered -- i.e., when the LLM determines that the new action has a higher priority than the current action -- the planning thread sends an interrupt signal to the acting thread."

Single-slot action buffer: "If the buffer is already occupied, the previous action is discarded to make space for the new one."

Recursive task decomposition via weighted DAG: "vertex set V={vi} represents atomic tasks" with prerequisite edges.

#### Source [4]: Concurrent Agent Orchestration (T1: official docs)
- **URL:** https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/concurrent
- **Author/Org:** Microsoft | **Date:** 2025-07

Microsoft Agent Framework provides sequential, concurrent, handoff, group chat, and Magentic orchestration. Concurrent: "enables multiple agents to work on the same task in parallel. Each agent processes the input independently, and their results are collected and aggregated." Magentic: "a flexible, general-purpose multi-agent pattern designed for complex, open-ended tasks."

#### Source [5]: CrewAI Process Types (T1: official docs)
- **URL:** https://docs.crewai.com/en/learn/sequential-process
- **Author/Org:** CrewAI | **Date:** 2025

Sequential: "tasks are executed one after the other, following a linear progression." Hierarchical: "emulates a corporate hierarchy" with auto-generated manager. Parallel: "Independent tasks execute simultaneously, then results merge."

### Sub-Question 2: Context Sharing

#### Source [2]: LangGraph State (T4)
Typed state dictionaries with reducer annotations. All nodes share the state object. Custom reducers enforce ordering for parallel results.

#### Source [5]: CrewAI Context (T1)
Task-output chaining: "output of one task serving as the context for the next." Memory: "Enable by setting memory=True when creating the Crew."

#### Source [3]: Centralized Memory (T3)
Memory updated at each timestep maintaining observations, chat logs, and action history. Passive (automatic) and active (agent-initiated) communication modes.

#### Source [6]: Agent-MCP Knowledge Graph (T5)
Persistent knowledge graph. Agents query via `ask_project_rag` and update via `update_project_context`. Direct and broadcast messaging.

#### Source [8]: OpenAI Handoff (T1)
Conversation handoff: agents have "complete knowledge of your prior conversation." Sessions provide persistent memory.

### Sub-Question 3: Conflict Detection

#### Source [12]: Resource Ownership (T4)
"When multiple agents think they control the same resource, conflicts become impossible to debug. Each database table, API endpoint, file, or process should belong to exactly one agent."

#### Source [2]: Reducers and Atomic Failure (T4)
Reducers prevent state conflicts. Atomic superstep: "If one parallel node fails, the entire superstep fails atomically."

### Sub-Question 4: Work Scoping

#### Source [7]: Claude Code Isolation (T1)
Subagents: "get a focused task, execute it, and return the result." Agent Teams: "stay in communication." Worktree isolation: "creates a temporary worktree for the entire session, isolating all file operations." Each subagent "maintains its own context window, model configuration, and permission scope."

#### Source [11]: OpenClaw Scoping (T4)
Deterministic orchestration: "the LLM does not decide the flow." Each agent "functions as a fully scoped brain with its own workspace, authentication profiles, and session store."

#### Source [1]: ADK Scoping (T1)
Coordinator routing: "A central LlmAgent (Coordinator) manages several specialized sub_agents." Workflow agents control flow without LLM involvement.

## Key Takeaways

1. **Pattern convergence.** Every major framework implements sequential,
   parallel, and hierarchical dispatch. The differences are in abstraction
   level: LangGraph exposes graph primitives, Google ADK provides
   pre-built workflow agents, CrewAI uses role-based metaphors. Choose
   based on how much control you need, not which patterns are available.

2. **Prevention beats detection.** Conflict detection at runtime is hard
   and expensive. The strongest systems prevent conflicts by construction:
   exclusive resource ownership, typed state reducers, and workspace
   isolation. Design-time partitioning is the consensus best practice.

3. **Worktrees won for coding agents.** Git worktree isolation is the
   de facto standard for parallel coding agents. Container isolation
   provides stronger guarantees but at higher cost. The key insight is
   that filesystem isolation is necessary -- shared working directories
   reliably produce conflicts.

4. **Context sharing is the hardest problem.** While dispatch and isolation
   have mature solutions, context sharing between agents remains
   fragmented. No framework has a universal answer. State reducers work
   for structured data, conversation handoff works for chat, knowledge
   graphs work for persistent facts, but combining these remains manual.

5. **Deterministic orchestration with LLM reasoning.** The emerging best
   practice separates flow control (deterministic, predictable,
   debuggable) from decision-making (LLM-driven, flexible). Google ADK
   and OpenClaw both embody this principle.

## Limitations

- This survey covers the landscape as of early 2026; the field is evolving
  rapidly.
- WebFetch access was intermittently restricted, limiting depth of extraction
  from some sources.
- The dual-thread planning-acting pattern [3] is demonstrated only in game
  environments (Minecraft), not production coding tasks.
- Conflict detection for coding agents specifically (as opposed to general
  multi-agent systems) has limited formal research; most evidence comes from
  practitioner reports.

## Follow-ups

- Deep-dive into LangGraph Send API map-reduce patterns for dynamic task
  decomposition.
- Technical investigation of git worktree limitations for agents (shared
  .git directory risks, rebase conflicts).
- Feasibility study of AST-based pre-execution overlap analysis for
  scoping agent work.
- Comparison of container vs. worktree isolation overhead for coding agent
  workloads.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| multi-agent parallel dispatch patterns fork-join wave-based DAG execution LLM agents 2024 2025 | google | 2024-2025 | 10 | 4 |
| LangGraph parallel agent execution patterns branching fan-out fan-in 2024 2025 | google | 2024-2025 | 10 | 3 |
| CrewAI AutoGen parallel task execution multi-agent orchestration patterns 2024 2025 | google | 2024-2025 | 10 | 3 |
| multi-agent context sharing patterns shared memory blackboard message passing LLM agents 2024 2025 | google | 2024-2025 | 10 | 3 |
| multi-agent file conflict detection resource locking optimistic concurrency code agents 2024 2025 | google | 2024-2025 | 10 | 3 |
| agent workspace isolation scoping work prevent interference parallel coding agents 2024 2025 | google | 2024-2025 | 10 | 5 |
| Google ADK multi-agent patterns parallel sequential loop delegation agent orchestration 2025 | google | 2025 | 10 | 2 |
| Claude Code container use git worktrees parallel agents isolation workspace 2025 | google | 2025 | 10 | 4 |
| Microsoft Semantic Kernel AutoGen concurrent agent orchestration patterns 2025 | google | 2025 | 10 | 3 |
| OpenAI agents SDK handoff pattern swarm multi-agent coordination 2025 | google | 2025 | 10 | 2 |
| deterministic multi-agent pipeline wave-based execution file ownership conflict detection coding agents 2025 | google | 2025 | 10 | 2 |
| CrewAI process types sequential hierarchical parallel crew execution context sharing 2025 | google | 2025 | 10 | 2 |
| OpenClaw deterministic multi-agent pipeline wave execution Lobster file ownership agent scoping | google | 2025 | 10 | 2 |
| multi-agent coding conflict resolution merge strategies file-level ownership static analysis dependency graph 2025 | google | 2025 | 10 | 3 |
| Anthropic Claude sub-agent task tool parallel execution worktree isolation architecture pattern 2025 2026 | google | 2025-2026 | 10 | 3 |
| LangGraph map-reduce Send API dynamic parallel branching state reducer agent coordination 2025 | google | 2025 | 10 | 2 |

16 searches across 1 source (Google), 160 found, 46 used. Not searched: academic databases (ACM, IEEE) -- search engine covers arxiv; vendor-specific Slack/Discord communities.
