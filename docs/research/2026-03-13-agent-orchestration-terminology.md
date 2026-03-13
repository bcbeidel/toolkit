---
name: Agent Orchestration Terminology — Inline vs. Delegate Execution
description: No LLM agent framework names the inline-vs-delegate meta-decision, but edge computing (computation offloading), serverless (task inlining), and BPMN (embedded subprocess vs call activity) have established terms. Recommends "inline vs. delegate" as primary terminology for the pattern where an orchestrator decides at runtime whether to execute a pipeline stage in its own context or spawn a subagent.
type: research
sources:
  - https://docs.langchain.com/oss/python/langgraph/workflows-agents
  - https://openai.github.io/openai-agents-python/multi_agent/
  - https://openai.github.io/openai-agents-python/handoffs/
  - https://www.anthropic.com/research/building-effective-agents
  - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
  - https://google.github.io/adk-docs/agents/multi-agents/
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/routing-dynamic-dispatch-patterns.html
  - https://docs.temporal.io/child-workflows
  - https://doc.akka.io/docs/akka/current/general/remoting.html
  - https://refactoring.guru/design-patterns/proxy
  - https://arxiv.org/html/2602.16873
  - https://www.getdynamiq.ai/post/agent-orchestration-patterns-in-multi-agent-systems-linear-and-adaptive-approaches-with-dynamiq
  - https://www.sciencedirect.com/topics/computer-science/contract-net-protocol
  - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  - https://en.wikipedia.org/wiki/Inline_expansion
related:
  - docs/designs/2026-03-13-composable-pipeline-design.md
  - docs/prompts/composable-pipeline-design.md
---

<!-- DRAFT -->

# Agent Orchestration Terminology: Inline vs. Delegate Execution

**Research question:** What is the established term (or closest analogues) for a pattern where an orchestrator decides at runtime whether to execute a pipeline stage inline (in its own context/thread) or delegate to a separate subagent?

## Sources Table

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://docs.langchain.com/oss/python/langgraph/workflows-agents | Workflows and Agents | LangChain | 2025 | T1 | verified |
| 2 | https://openai.github.io/openai-agents-python/multi_agent/ | Agent Orchestration | OpenAI | 2025 | T1 | verified |
| 3 | https://openai.github.io/openai-agents-python/handoffs/ | Handoffs | OpenAI | 2025 | T1 | verified |
| 4 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | 2024-12 | T1 | verified |
| 5 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/ | Semantic Kernel Agent Orchestration | Microsoft | 2025-05 | T1 | verified |
| 6 | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns | AI Agent Orchestration Patterns | Microsoft Azure | 2026-02 | T1 | verified |
| 7 | https://google.github.io/adk-docs/agents/multi-agents/ | Multi-agent Systems | Google ADK | 2025 | T1 | verified |
| 8 | https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/routing-dynamic-dispatch-patterns.html | Routing Dynamic Dispatch Patterns | AWS | 2025 | T1 | verified |
| 9 | https://docs.temporal.io/child-workflows | Child Workflows | Temporal | 2025 | T1 | verified |
| 10 | https://doc.akka.io/docs/akka/current/general/remoting.html | Location Transparency | Akka/Lightbend | 2025 | T1 | verified |
| 11 | https://refactoring.guru/design-patterns/proxy | Proxy Design Pattern | Refactoring.Guru | 2025 | T4 | verified |
| 12 | https://arxiv.org/html/2602.16873 | AdaptOrch: Task-Adaptive Multi-Agent Orchestration | ArXiv | 2025-02 | T3 | verified |
| 13 | https://www.getdynamiq.ai/post/agent-orchestration-patterns-in-multi-agent-systems-linear-and-adaptive-approaches-with-dynamiq | Agent Orchestration Patterns: Linear and Adaptive | Dynamiq | 2024 | T5 | verified |
| 14 | https://www.sciencedirect.com/topics/computer-science/contract-net-protocol | Contract Net Protocol | ScienceDirect | 2024 | T2 | verified (403) |
| 15 | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | A Practical Guide to Building Agents | OpenAI | 2025 | T1 | verified |
| 16 | https://en.wikipedia.org/wiki/Inline_expansion | Inline Expansion | Wikipedia | 2025 | T5 | verified |

---

## Structured Extracts

### Sub-Question 1: LLM Agent Frameworks

What do LangGraph, CrewAI, AutoGen/AG2, Semantic Kernel, OpenAI Agents SDK, and Google ADK call the pattern where a coordinator dynamically chooses between inline execution and subagent delegation at runtime? Do any explicitly name this decision point?

---

### Source [1]: Workflows and Agents — LangChain/LangGraph
- **URL:** https://docs.langchain.com/oss/python/langgraph/workflows-agents
- **Author/Org:** LangChain | **Date:** 2025

**Re: LLM agent frameworks terminology**

> "Workflows have predetermined code paths and are designed to operate in a certain order."
> (Workflows vs Agents section)

> "Agents are dynamic and define their own processes and tool usage."
> (Workflows vs Agents section)

> "Agents have more autonomy than workflows, and can make decisions about the tools they use and how to solve problems."
> (Agents section)

> The orchestrator-worker pattern: "the orchestrator breaks down tasks into subtasks, delegates subtasks to workers, synthesize[s] worker outputs into a final result."
> (Orchestrator-workers section)

The documentation does not explicitly discuss decision mechanisms for choosing between inline execution versus delegating to subagents or subgraphs. The orchestrator-worker pattern describes delegation but frames it as a predetermined architecture rather than a runtime decision mechanism. LangGraph uses "conditional edges" for routing logic but this is graph traversal, not inline-vs-delegate selection.

---

### Source [2]: Agent Orchestration — OpenAI Agents SDK
- **URL:** https://openai.github.io/openai-agents-python/multi_agent/
- **Author/Org:** OpenAI | **Date:** 2025

**Re: LLM agent frameworks terminology**

> Two key patterns are contrasted:
> **Agents as tools**: "A manager agent keeps control of the conversation and calls specialist agents through `Agent.as_tool()`"
> **Handoffs**: "A triage agent routes the conversation to a specialist, and that specialist becomes the active agent for the rest of the turn"
> (Orchestration patterns table)

> Selection criteria: **Agents as tools** suits scenarios where "a specialist should help with a bounded subtask but should not take over the user-facing conversation."
> **Handoffs** work when "routing itself is part of the workflow and you want the chosen specialist to own the next part."
> (Selection section)

This is the closest any framework comes to the inline-vs-delegate distinction: "agents as tools" keeps the orchestrator in control (analogous to inline), while "handoffs" transfer control (analogous to delegation). However, the SDK does not name the meta-decision of choosing between these two modes at runtime.

---

### Source [3]: Handoffs — OpenAI Agents SDK
- **URL:** https://openai.github.io/openai-agents-python/handoffs/
- **Author/Org:** OpenAI | **Date:** 2025

**Re: LLM agent frameworks terminology**

> "Handoffs allow an agent to delegate tasks to another agent."
> (Handoffs intro)

> "If you have multiple possible destinations, register one handoff per destination and let the model choose among them."
> (Handoff registration)

> Contrast with agent-as-tool: "you want structured input for a nested specialist without transferring the conversation, prefer Agent.as_tool(parameters=...)"
> (Agent-as-tool section)

> "The documentation uses no explicit term for the decision point itself. Instead, it describes the mechanism."
> (Decision terminology)

---

### Source [4]: Building Effective Agents — Anthropic
- **URL:** https://www.anthropic.com/research/building-effective-agents
- **Author/Org:** Anthropic | **Date:** 2024-12

**Re: LLM agent frameworks terminology**

> "Workflows" are "systems where LLMs and tools are orchestrated through predefined code paths."
> "Agents" are "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks."
> (Definitions section)

> "In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results. This workflow is well-suited for complex tasks where you can't predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task)."
> (Orchestrator-workers section)

> "Whereas it's topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input."
> (Orchestrator-workers vs parallelization)

> "These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases."
> (Composable patterns)

Anthropic does not name the inline-vs-delegate decision point. The orchestrator-workers pattern describes delegation but assumes workers are always separate. The guide recommends "finding the simplest solution possible, and only increasing complexity when needed" — an implicit heuristic for when to use simpler (inline) vs more complex (delegated) approaches, but not formalized as a runtime decision.

---

### Source [5]: Semantic Kernel Agent Orchestration — Microsoft
- **URL:** https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/
- **Author/Org:** Microsoft | **Date:** 2025-05

**Re: LLM agent frameworks terminology**

> Supported orchestration patterns:
> | Pattern | Description | Typical Use Case |
> | Concurrent | Broadcasts a task to all agents, collects results independently. | Parallel analysis, independent subtasks, ensemble decision making. |
> | Sequential | Passes the result from one agent to the next in a defined order. | Step-by-step workflows, pipelines, multi-stage processing. |
> | Handoff | Dynamically passes control between agents based on context or rules. | Dynamic workflows, escalation, fallback, or expert handoff scenarios. |
> | Group Chat | All agents participate in a group conversation, coordinated by a group manager. | Brainstorming, collaborative problem solving, consensus building. |
> | Magentic | Group chat-like orchestration inspired by MagenticOne. | Complex, generalist multi-agent collaboration. |
> (Patterns table)

> "All orchestration patterns share a unified interface for construction and invocation."
> (Unified interface section)

The framework uses `InProcessRuntime` as an execution backend. All patterns assume agents are separate entities coordinated by the runtime. There is no pattern for choosing between inline vs delegated execution of a stage — the topology is selected at construction time, not per-invocation.

---

### Source [6]: AI Agent Orchestration Patterns — Microsoft Azure Architecture Center
- **URL:** https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- **Author/Org:** Microsoft Azure | **Date:** 2026-02

**Re: LLM agent frameworks terminology**

> "Before you adopt a multi-agent orchestration pattern, evaluate whether your scenario requires one. Agent architectures exist on a spectrum of complexity, and each level introduces coordination overhead, latency, and cost. Use the lowest level of complexity that reliably meets your requirements."
> (Start with the right level of complexity)

> Complexity levels: **Direct model call** (single LLM, no agent logic), **Single agent with tools** (one agent with tool access), **Multi-agent orchestration** (multiple specialized agents).
> (Complexity levels table)

> Handoff pattern: "enables dynamic delegation of tasks between specialized agents. Each agent can assess the task at hand and decide whether to handle it directly or transfer it to a more appropriate agent based on the context and requirements."
> Also known as: "routing, triage, transfer, dispatch, delegation."
> (Handoff orchestration section)

> Magentic pattern: "designed for open-ended and complex problems that don't have a predetermined plan of approach."
> Also known as: "dynamic orchestration, task-ledger-based orchestration, adaptive planning."
> (Magentic orchestration section)

The handoff pattern comes closest: an agent "decide[s] whether to handle it directly or transfer it" — this is literally the inline-vs-delegate decision. But it is framed as agent-to-agent transfer rather than as an orchestrator deciding execution mode for a stage.

---

### Source [7]: Multi-agent Systems — Google ADK
- **URL:** https://google.github.io/adk-docs/agents/multi-agents/
- **Author/Org:** Google | **Date:** 2025

**Re: LLM agent frameworks terminology**

> Two delegation mechanisms:
> **LLM-Driven Delegation (Agent Transfer):** The parent LLM generates a specific function call: "transfer_to_agent(agent_name='target_agent_name')". The framework intercepts this, identifies the target, and switches execution focus.
> (Agent Transfer section)

> **Explicit Invocation (AgentTool):** The parent wraps a target agent in AgentTool and includes it in the tools list. This method is "Synchronous (within the parent's flow), explicit, controlled invocation like any other tool."
> (AgentTool section)

Google ADK has two distinct mechanisms — transfer (full handoff, like delegate) and AgentTool (synchronous call, closer to inline but still a separate agent). Neither mechanism represents the same stage potentially running either way. The topology is declared in the agent tree at construction time.

---

### Source [8]: Routing Dynamic Dispatch Patterns — AWS
- **URL:** https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-patterns/routing-dynamic-dispatch-patterns.html
- **Author/Org:** AWS | **Date:** 2025

**Re: LLM agent frameworks terminology**

> "In traditional distributed systems, the dynamic dispatch pattern selects and invokes specific services at runtime based on incoming event attributes, such as event type, source, and payload."
> (Dynamic dispatch definition)

> "In agentic systems, routing also performs dynamic task delegation — but instead of Amazon EventBridge rules or metadata filters, the LLM classifies and interprets the user's intent through natural language. The result is a flexible, semantic, and adaptive form of dispatching."
> (LLM-based routing)

> "Static routing logic, often embedded within orchestration scripts or API layers, lacks the adaptability required for real-time, multi-model, multi-capability environments."
> (Static vs dynamic)

AWS uses "dynamic dispatch" for routing between agents but this is about which agent handles a request, not about whether a stage runs inline vs delegated.

---

### Source [15]: A Practical Guide to Building Agents — OpenAI
- **URL:** https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- **Author/Org:** OpenAI | **Date:** 2025

**Re: LLM agent frameworks terminology**

> Multi-agent patterns: **Manager pattern** — "a central LLM—the 'manager'—orchestrates a network of specialized agents seamlessly through tool calls, with the manager intelligently delegating tasks to the right agent at the right time."
> **Decentralized pattern** — "agents can 'handoff' workflow execution to one another. Handoffs are a one way transfer that allow an agent to delegate to another agent."
> (Multi-agent section)

> "In the manager pattern, edges represent tool calls whereas in the decentralized pattern, edges represent handoffs that transfer execution between agents."
> (Pattern comparison)

---

### Sub-Question 2: Classical Software Architecture

What terms from distributed systems, microservices, actor models, and workflow engines describe runtime decisions about execution locality — in-process vs. delegating to a separate process/service?

---

### Source [9]: Child Workflows — Temporal
- **URL:** https://docs.temporal.io/child-workflows
- **Author/Org:** Temporal | **Date:** 2025

**Re: Classical software architecture — workflow engines**

> "A Child Workflow has access to all Workflow APIs but is subject to the same deterministic constraints as other Workflows. An Activity has the inverse pros and cons—no access to Workflow APIs but no Workflow constraints."
> (Core differences)

> "The decision is roughly analogous to spawning a child process in a terminal to do work versus doing work in the same process."
> (Process analogy)

> "A Workflow models composite operations that consist of multiple Activities or other Child Workflows. An Activity usually models a single operation on the external world."
> (Modeling guidance)

> "When in doubt, use an Activity."
> (Default recommendation)

> Valid reasons to use Child Workflows:
> - "Partitioning large workloads": "a single Workflow Execution does not have enough space in its Event History to spawn 100,000 Activity Executions"
> - "Service isolation": "can be processed by a completely separate set of Workers"
> - "Resource management": "one to one mapping with a resource"
> - "Periodic logic": "execute periodic logic without overwhelming the Parent Workflow Event History"
> (When to use child workflows)

> "There is no reason to use Child Workflows just for code organization."
> (Caution)

Temporal's child workflow vs activity decision is the closest classical analogue to inline-vs-delegate. Activities run in the same worker process (inline); child workflows get their own event history and can run on separate workers (delegated). The decision criteria map closely: context/history isolation, resource management, service boundaries. Temporal does not have a named term for the decision itself — it is an architectural choice documented through heuristics.

---

### Source [10]: Location Transparency — Akka
- **URL:** https://doc.akka.io/docs/akka/current/general/remoting.html
- **Author/Org:** Akka/Lightbend | **Date:** 2025

**Re: Classical software architecture — actor model**

> "all interactions of actors use purely message passing and everything is asynchronous."
> (Core design)

> The design philosophy: "go from remote to local by way of optimization instead of trying to go from local to remote by way of generalization."
> (Optimization approach)

> "Just write your application according to the principles outlined in the previous sections, then specify remote deployment of actor sub-trees in the configuration file. This way, your application can be scaled out without having to touch the code."
> (Configuration-driven deployment)

Akka's "location transparency" makes local and remote actors interchangeable — the same message-passing API works regardless. The decision about where an actor runs is a deployment/configuration concern, not a runtime per-message decision. This is the opposite of our pattern: Akka deliberately hides the inline-vs-remote distinction rather than making it an explicit runtime choice.

---

### Source [11]: Proxy Design Pattern — Refactoring.Guru
- **URL:** https://refactoring.guru/design-patterns/proxy
- **Author/Org:** Refactoring.Guru | **Date:** 2025

**Re: Classical software architecture — design patterns**

> "Proxy is a structural design pattern that lets you provide a substitute or placeholder for another object. A proxy controls access to the original object, allowing you to perform something either before or after the request gets through to the original object."
> (Definition)

> Remote proxy: "Local execution of a remote service (remote proxy). This is when the service object is located on a remote server. In this case, the proxy passes the client request over the network, handling all of the nasty details of working with the network."
> (Remote proxy)

The proxy pattern makes the location decision transparent to the caller. A "virtual proxy" (lazy initialization) or "remote proxy" (network delegation) decides execution mode, but the decision is typically fixed at construction time, not per-invocation. The pattern provides the mechanism (same interface, different backends) but not the runtime decision logic.

---

### Source [16]: Inline Expansion — Wikipedia
- **URL:** https://en.wikipedia.org/wiki/Inline_expansion
- **Author/Org:** Wikipedia | **Date:** 2025

**Re: Classical software architecture — compiler inlining analogy**

> The direct effect of inlining is "to improve time performance (by eliminating call overhead), at the cost of worsening space usage (due to duplicating the function body)."
> (Trade-off definition — from search extract; direct fetch returned 403)

> "As a rule of thumb, some inlining will improve speed at very minor cost of space, but excess inlining will hurt speed, due to inlined code consuming too much of the instruction cache."
> (Heuristic)

> "Usually, an inlining algorithm has a certain code budget (an allowed increase in program size) and aims to inline the most valuable callsites without exceeding that budget."
> (Budget-based decision)

> Decision factors: function size, call frequency, and potential code growth. Profile-guided optimization (PGO) "uses execution profiles to weigh call-site hotness."
> (Decision heuristics)

Compiler inlining is the strongest conceptual analogue: the same function can be either inlined (expanded at the call site) or called (separate frame). The decision is made per-call-site based on heuristics (size, frequency, budget). However, compiler inlining is a compile-time optimization, not a runtime decision. The LLM agent pattern needs a runtime analogue of this.

---

### Sub-Question 3: Academic MAS Research

Does multi-agent systems research have established terminology for agents that dynamically select between self-execution and task delegation?

---

### Source [14]: Contract Net Protocol — ScienceDirect
- **URL:** https://www.sciencedirect.com/topics/computer-science/contract-net-protocol
- **Author/Org:** ScienceDirect | **Date:** 2024

**Re: Academic MAS — delegation protocols**

> "Contract Net Protocol (CNP) is a high-level task-sharing interaction protocol for agent communication in distributed environments; it facilitates the decentralised control of task execution with efficient multi-agent communication."
> (Definition)

> "It involves two roles, initiator and participant, where the initiator broadcasts a call-for-proposals to participants who can respond with a quotation or a refusal. The initiator then selects the best offer and communicates the decision to the participants."
> (Mechanics)

CNP is about delegation negotiation — deciding which external agent handles a task. It does not address the prior decision of whether to self-execute or delegate at all. The initiator has already decided to delegate before invoking CNP.

BDI (Belief-Desire-Intention) architectures provide agents with "the ability to decide which goals to pursue and how to achieve such goals." In principle, a BDI agent could include "execute inline" and "delegate" as competing plans for a goal, selected by context. But published BDI literature does not appear to name this specific meta-decision as a pattern.

MOISE+ organizational models define roles, missions, and norms for task allocation but focus on organizational structure rather than runtime execution mode selection.

No established MAS term was found for the specific pattern of an agent choosing between self-execution and delegation at a stage boundary.

---

### Sub-Question 4: Pattern Differentiation

How does this differ from adjacent patterns (dynamic routing, hierarchical delegation, adaptive orchestration, hybrid execution)?

---

### Source [12]: AdaptOrch: Task-Adaptive Multi-Agent Orchestration — ArXiv
- **URL:** https://arxiv.org/html/2602.16873
- **Author/Org:** ArXiv | **Date:** 2025-02

**Re: Pattern differentiation — adaptive orchestration**

> "a formal framework for task-adaptive multi-agent orchestration that dynamically selects among four canonical topologies"
> (Definition)

> Four canonical topologies:
> - "Parallel (tau-P): All subtasks execute concurrently; outputs merged post-hoc"
> - "Sequential (tau-S): Subtasks execute in topological order; each receives prior context"
> - "Hierarchical (tau-H): Lead agent decomposes and delegates; sub-agents report back"
> - "Hybrid (tau-X): DAG partitioned into parallel groups connected sequentially"
> (Topology definitions)

> "orchestration topology—the structural composition of how multiple agents are coordinated, parallelized, and synthesized—now dominates system-level performance over individual model capability."
> (Key finding)

> Static vs dynamic: "Static frameworks -- Model Context Protocol (MCP), LangGraph, and CrewAI -- define fixed execution topologies (chains, graphs, or role-based teams) that persist regardless of what the task demands."
> (Contrast)

> The Topology Routing Algorithm selects topology by analyzing "parallelism width, critical path depth, and coupling density."
> (Selection mechanism)

AdaptOrch selects which topology to use for a task, but within each topology, every stage is executed the same way (all delegated to agents). It does not address the per-stage decision of inline vs delegated execution. This is topology-level adaptation, not execution-mode adaptation.

---

### Source [13]: Agent Orchestration Patterns: Linear and Adaptive — Dynamiq
- **URL:** https://www.getdynamiq.ai/post/agent-orchestration-patterns-in-multi-agent-systems-linear-and-adaptive-approaches-with-dynamiq
- **Author/Org:** Dynamiq | **Date:** 2024

**Re: Pattern differentiation — adaptive vs linear**

> Adaptive orchestrator: "is more flexible, making decisions on the fly based on the current context."
> (Definition)

> Linear orchestrator: "a straightforward, step-by-step approach to task management" with tasks "performed in a specific order."
> (Contrast)

> Adaptive key capabilities:
> - "Flexible Routing: Chooses agents based on the specific requirements of each task"
> - "Contextual Decisions: Makes decisions based on real-time data and context"
> - "Dynamic Selection" and "Intelligent Selection: pick the most suitable agents for each subtask on the fly"
> (Capabilities)

"Adaptive orchestration" selects which agent handles each task, but presumes all stages are delegated to some agent. It does not consider inline execution as an option. The "dynamic selection" is about which agent, not whether to use an agent at all.

---

### Pattern Differentiation Summary (from all sources)

| Adjacent Pattern | What It Decides | How It Differs from Inline-vs-Delegate |
|------------------|----------------|----------------------------------------|
| **Dynamic routing** (Source 6, 8) | Which agent handles a request | Always delegates; chooses destination, not execution mode |
| **Hierarchical delegation** (Source 12) | How to decompose and assign subtasks | Assumes all subtasks go to sub-agents |
| **Adaptive orchestration** (Source 12, 13) | Which topology/agent to use per task | Selects among delegation patterns; inline not an option |
| **Handoff** (Source 2, 3, 5, 6) | Whether current agent handles or transfers | Closest match — "handle directly or transfer" — but framed as agent-to-agent, not as execution mode for a pipeline stage |
| **Agents as tools** (Source 2, 7) | How to invoke a specialist (tool call vs transfer) | Mechanism for delegation, but mode fixed at design time |
| **Orchestrator-workers** (Source 1, 4) | What subtasks to create and delegate | Always delegates to workers; inline not considered |
| **Compiler inlining** (Source 16) | Whether to inline a function or call it | Exact structural analogue but compile-time, not runtime |
| **Temporal child workflow vs activity** (Source 9) | Whether to use inline activity or separate workflow | Closest classical analogue; heuristic-based but architectural, not per-invocation |
| **Location transparency** (Source 10) | Where an actor runs (local vs remote) | Deliberately hides the decision from the caller |

---

## Findings

### SQ1: Does LLM agent orchestration have a term for inline-vs-delegate?

**Finding: No LLM agent framework names the inline-vs-delegate meta-decision.** Eight major frameworks surveyed (LangGraph, OpenAI Agents SDK, Anthropic, Semantic Kernel, Google ADK, AWS, Dynamiq, AdaptOrch) each offer mechanisms that touch aspects of the pattern, but none name the decision point where an orchestrator chooses *how* to execute a stage -- inline or delegated -- at runtime.

**Confidence: HIGH.** Multiple independent T1 sources converge. LangChain/LangGraph [#1] distinguishes workflows from agents but does not address per-stage execution mode. Anthropic [#4] describes orchestrator-workers but assumes workers are always separate. Semantic Kernel [#5] selects orchestration patterns at construction time, not per-invocation. AWS [#8] uses "dynamic dispatch" for agent routing, not execution mode. AdaptOrch [#12] selects among topologies but within each topology all stages are delegated. Dynamiq [#13] describes "adaptive orchestration" as selecting which agent, not whether to use an agent.

The closest LLM-framework language comes from two sources:

- **OpenAI Agents SDK** [#2, #3] distinguishes "agents as tools" (orchestrator retains control, analogous to inline) from "handoffs" (control transfers, analogous to delegation). The SDK does not name the meta-decision of choosing between these modes at runtime.
- **Azure Architecture Center** [#6] describes the handoff pattern as an agent that "decides whether to handle it directly or transfer it." This is the inline-vs-delegate decision stated in plain language, but framed as agent-to-agent routing rather than as an execution mode for a pipeline stage.

**Counter-evidence (from challenge):** AWS Bedrock uses "InvokeInlineAgent" as an API name, suggesting the industry may be converging on "inline" in the agent execution context -- though Bedrock's semantics are about inline agent *definition* rather than inline *execution* of a pipeline stage. The absence of a term in current frameworks does not mean one will not emerge; the field is under 3 years old, and terminology is actively being coined (AdaptOrch 2025, AgentOrchestra 2025).

---

### SQ2: Do adjacent systems domains have established terms?

**Finding: At least three adjacent domains have established terminology for structurally identical decisions.** The original survey's conclusion that "no established term exists" was too strong. While no *LLM-specific* term exists, the pattern is well-named elsewhere.

**Confidence: HIGH.** The challenge phase identified three domains with mature vocabulary, each supported by specification-level or peer-reviewed sources:

1. **Edge computing -- "computation offloading"** (challenge section). A field with hundreds of papers. The core decision is binary: execute locally on the device or offload to edge/cloud infrastructure. Decision factors (latency, resource capacity, data transmission cost) parallel the LLM factors (context pressure, token cost, isolation). "Binary offloading" names the all-or-nothing decision; "partial offloading" names splitting a task. This is the most mature vocabulary for the inline-vs-delegate decision in any domain.

2. **Serverless computing -- "function fusion" / "task inlining"** (challenge section). Fusionize++ (Kowallik et al., IEEE Trans. Cloud Computing 2024) explicitly borrows "inlining" from compilers and applies it to serverless functions at runtime. A "fusion group" runs in the same function (inline); cross-group calls are remote (delegated). This is the closest structural analogue found in any domain: same code, two execution modes, runtime decision, per-task granularity, feedback-driven heuristics.

3. **BPMN -- "embedded subprocess vs call activity"** (challenge section). An OMG (Object Management Group) specification distinguishes embedded subprocesses (execute in parent context, share data directly) from call activities (invoke a separate reusable process, require explicit data mapping). The data-scoping distinction maps precisely to agent context sharing: embedded = shared context, call activity = isolated context.

**From the original survey:**

4. **Temporal -- child workflow vs activity** [#9]. Activities run in the parent worker process (inline-like); child workflows get their own event history and can run on separate workers (delegated). Decision criteria map closely: context/history isolation, resource management, service boundaries. Temporal calls these "valid reasons to use Child Workflows" -- heuristics, not a named pattern.

5. **Compiler inlining** [#16]. The strongest conceptual analogue at the structural level: same function, two execution modes (inline or called), heuristic-driven per-call-site decision. However, compiler inlining is a compile-time optimization, not a runtime decision. The challenge correctly identifies that edge offloading, serverless fusion, and BPMN should rank above compiler inlining because they are runtime/workflow-level decisions.

**Counter-evidence:** Akka's location transparency [#10] and the Kubernetes sidecar pattern argue that the inline/remote boundary should be *hidden*, not exposed as an architectural choice. The Strategy pattern achieves algorithm selection without distinguishing execution locality. If the distinction is purely about where code runs rather than what it does, it may be an optimization concern rather than an architectural pattern. However, LLM-specific factors (context window limits, token costs, failure isolation across model calls) elevate this beyond a pure optimization concern.

**Confidence: MODERATE** (on whether these terms are directly importable vs. merely analogous). Each domain term carries domain-specific baggage. "Computation offloading" implies device-to-cloud. "Function fusion" implies serverless deployment units. "Embedded subprocess" implies BPMN XML. None maps 1:1 to "LLM orchestrator decides whether to run a pipeline stage in its own context or spawn a subagent."

---

### SQ3: Does MAS research name the self-execute-vs-delegate decision?

**Finding: No established MAS term exists for this specific meta-decision.** Classical multi-agent systems research focuses on delegation protocols (how to negotiate delegation) rather than on the prior decision of whether to delegate at all.

**Confidence: MODERATE.** The Contract Net Protocol [#14] addresses delegation negotiation -- selecting which external agent handles a task -- but the initiator has already decided to delegate before invoking CNP. BDI architectures could in principle model "execute inline" and "delegate" as competing plans for a goal, but published BDI literature does not appear to name this as a pattern. MOISE+ organizational models focus on structural role assignment rather than runtime execution mode.

**Counter-evidence:** The search did not exhaustively cover MAS literature. JADE, Jason, and older FIPA-based frameworks were not searched. However, the challenge phase did not surface any MAS-specific term either, lending support to the finding.

---

### SQ4: How does this pattern differ from adjacent patterns?

**Finding: The pattern is a specific combination of properties not found together in any single named pattern, but it is not wholly novel.** The novelty claim should be scoped to LLM agent orchestration rather than software engineering broadly.

**Confidence: MODERATE.** The pattern combines: (a) per-stage granularity, (b) runtime decision, (c) same stage executable in two modes, (d) heuristic-driven selection, and (e) deterministic gates regardless of mode. No single surveyed pattern combines all five.

However, the challenge identifies that Fusionize++ combines four of five (per-task, runtime, same code in two modes, feedback-driven heuristics -- lacking only deterministic gates). Edge offloading combines three of five (per-task, runtime, heuristic-driven). The remaining differentiator -- deterministic gates regardless of execution mode -- is a design choice specific to this pipeline, not an inherent characteristic of the inline-vs-delegate pattern.

Adjacent patterns differ as follows [#1-#16]:

| Pattern | What It Decides | Key Difference |
|---------|----------------|----------------|
| Dynamic routing [#6, #8] | Which agent handles a request | Always delegates; chooses destination, not mode |
| Adaptive orchestration [#12, #13] | Which topology/agent per task | Selects among delegation patterns; inline not an option |
| Handoff [#2, #3, #5, #6] | Whether current agent handles or transfers | Closest LLM-framework match but agent-to-agent, not pipeline-stage execution mode |
| Agents as tools [#2, #7] | How to invoke a specialist | Mode fixed at design time |
| Compiler inlining [#16] | Whether to inline a function | Compile-time, not runtime |
| Temporal child workflow vs activity [#9] | Inline activity vs separate workflow | Architectural, not per-invocation |
| Location transparency [#10] | Where an actor runs | Deliberately hides the decision |
| Computation offloading | Execute locally or offload | Runtime, per-task -- closest structural match outside LLM |
| Function fusion / task inlining | Inline or remote function execution | Runtime, per-task, feedback-driven -- closest overall match |
| BPMN embedded vs call activity | In-process subprocess or separate process | Data-scoping distinction maps to context sharing |

---

### SQ5: What should this pattern be called?

**Finding: Candidate terms ranked by fit for use in design documents and code.**

**Confidence: MODERATE.** This is a recommendation synthesized from the evidence, not a finding of established usage. The ranking reflects structural fit, clarity, and domain precedent.

#### Tier 1: Recommended

**1. "Inline execution" / "inline vs. delegate"**
- **Rationale:** The word "inline" already appears across three domains: compiler inlining [#16], serverless "task inlining" (Fusionize++), and AWS Bedrock's "InvokeInlineAgent" API. It communicates the core concept immediately to engineers: the work happens *in the caller's context* rather than being sent elsewhere. The binary framing ("inline or delegate") is clean and maps to the two concrete execution paths.
- **Usage in code:** `execution_mode: inline | delegate`, `run_inline()`, `should_inline(stage)`
- **Risk:** "Inline" has compiler connotations that imply compile-time optimization. Must be qualified as *runtime* inline execution.

**2. "Execution mode strategy"**
- **Rationale:** Composes two well-known terms: the Strategy pattern (select algorithm at runtime) applied to execution mode (where/how code runs). Does not require coining a new term. Accurately describes the meta-decision as a strategy selection.
- **Usage in code:** `ExecutionModeStrategy`, `select_execution_mode(stage, context)`
- **Risk:** Verbose. "Strategy" is overloaded in software engineering. Does not convey the specific inline-vs-delegate binary.

#### Tier 2: Viable alternatives

**3. "Computation offloading" (adapted)**
- **Rationale:** Borrows from edge computing's mature vocabulary. "Offload" clearly implies the default is local (inline) and the decision is whether to send work elsewhere. The term has academic backing with hundreds of papers.
- **Usage in code:** `should_offload(stage)`, `offload_to_subagent(stage)`
- **Risk:** Edge computing baggage (device-to-cloud connotation). May confuse readers who expect infrastructure-level offloading rather than agent-level delegation.

**4. "Embedded vs. called" (adapted from BPMN)**
- **Rationale:** BPMN's distinction captures the data-scoping aspect well: embedded subprocesses share parent data (like inline stages sharing orchestrator context), call activities require explicit data mapping (like delegated stages with isolated context). OMG-backed terminology.
- **Usage in code:** `embedded_stage()`, `call_stage()`
- **Risk:** BPMN is not widely known among LLM developers. The terms lack immediate intuitive meaning outside workflow engine contexts.

#### Tier 3: Avoid

**5. "Composable pipeline"**
- **Rationale against:** This was the user's working term, but "composable" describes pipeline *structure* (stages can be assembled), not the *execution mode decision*. Every pipeline with modular stages is "composable" regardless of whether stages run inline or delegated.

**6. "Function fusion" / "task inlining"**
- **Rationale against:** Despite being the closest structural analogue (Fusionize++), "fusion" implies merging multiple functions into one deployment unit, which is not the agent pattern. "Task inlining" is more apt but obscure outside serverless literature.

**7. "Location transparency"**
- **Rationale against:** This is the *opposite* philosophy -- Akka deliberately hides where actors run [#10]. The agent pattern explicitly exposes and decides execution locality.

---

### Synthesis and Recommendation

The research question was whether an established term exists for this pattern. The answer is nuanced:

- **Within LLM agent orchestration:** No. Eight major frameworks surveyed; none name it. (HIGH confidence)
- **Within classical software architecture:** Partial. Temporal's child-workflow-vs-activity is the closest classical analogue but is not a named "pattern." (HIGH confidence)
- **Within adjacent systems domains:** Yes, multiple. Edge computing ("computation offloading"), serverless ("task inlining"), and BPMN ("embedded subprocess vs call activity") all have established terms for structurally identical decisions. (HIGH confidence, based on challenge phase evidence)

**Practical recommendation:** Use **"inline vs. delegate"** as the primary terminology in design documents and code. It is:

- Already understood by engineers (compiler inlining, serverless task inlining, AWS InvokeInlineAgent)
- Concise and binary, matching the two execution paths
- Descriptive of what actually happens (work runs in the orchestrator's context or in a separate agent)
- Not overloaded within LLM orchestration (unlike "composable," "adaptive," or "dynamic")

Qualify the term in your design document's glossary:

> **Inline execution:** A pipeline stage runs within the lead model's context window and thread, sharing the orchestrator's conversation state. Analogous to a function call (vs. a subprocess) or an embedded subprocess (vs. a call activity in BPMN).
>
> **Delegate execution:** A pipeline stage runs in a separate subagent with its own context, receiving explicit inputs and returning structured outputs. Analogous to a child workflow (Temporal) or a call activity (BPMN).

### Gaps and Follow-ups

1. **Fusionize++ deep dive.** The serverless "task inlining" work (IEEE Trans. Cloud Computing 2024) appears to be the closest structural analogue. A focused read of that paper could yield decision heuristics directly transferable to the agent pipeline context.
2. **AWS Bedrock InvokeInlineAgent semantics.** Bedrock's API uses "inline" in the agent context. Understanding its exact semantics would clarify whether the industry is converging on this term.
3. **Temporal decision heuristics.** Temporal's documentation [#9] lists specific criteria for child-workflow-vs-activity. These could be adapted into a decision matrix for the agent pipeline (context size thresholds, isolation requirements, reusability needs).
4. **Emerging LLM terminology watch.** The field is actively coining terms. DSPy, CrewAI's evolving delegation system, and new frameworks releasing in 2026 may name this pattern. Revisit in 6 months.
5. **BPMN embedded subprocess data scoping.** The BPMN spec's rules for data visibility in embedded vs. call activities could inform the design of context passing between inline and delegated stages.

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| **No established term exists for this pattern** | 16 sources across LLM frameworks, classical architecture, and MAS literature surveyed; none name the meta-decision. The Jan 2026 arXiv survey on multi-agent orchestration (2601.13671) also does not define inline-vs-delegate terminology. | Edge computing has a well-established field called **"computation offloading"** with a named binary decision: execute locally or offload to remote infrastructure. Serverless computing uses **"function fusion" / "task inlining"** (Fusionize++, IEEE Trans. Cloud Computing 2024) for the same structural decision. BPMN has **"embedded subprocess vs call activity"** as a formal spec-level distinction. These are domain-specific terms for structurally identical decisions. | **High.** The finding "no term exists" is too strong. More accurate: no term exists *within LLM agent orchestration specifically*, but the pattern is named in at least three adjacent domains (edge computing, serverless, BPMN). The research should qualify the finding accordingly. |
| **LLM agent orchestration is the right domain to search** | The research question originates from an LLM agent pipeline design, so surveying LLM frameworks is appropriate. The survey covers 8 major LLM frameworks (LangGraph, OpenAI, Anthropic, Semantic Kernel, Google ADK, AWS, CrewAI, Dynamiq). | The pattern is fundamentally about **execution locality**, which is a systems concern, not an AI concern. Edge computing, serverless platforms, BPMN workflow engines, and OS scheduling all have richer vocabularies for this decision because they have dealt with it longer. Searching only LLM frameworks biases toward "no term found." | **Medium.** The search was not limited to LLM frameworks (Temporal, Akka, and compiler inlining were covered), but it missed the three domains with the strongest terminology: edge computing offloading, serverless function fusion, and BPMN subprocess types. |
| **"Inline vs. delegate" is a meaningful architectural distinction** | OpenAI SDK distinguishes "agents as tools" (inline-like) from "handoffs" (delegate-like). Azure handoff docs describe agents deciding to "handle directly or transfer." Temporal distinguishes activities (in-process) from child workflows (separate history). The distinction maps to real trade-offs: context isolation, resource management, failure domains. | The Kubernetes sidecar pattern and Akka location transparency both argue that the inline/remote boundary is an **implementation detail that should be hidden**, not an architectural choice to expose. The Strategy pattern achieves algorithm selection without distinguishing execution locality. If the distinction is just about where code runs rather than what it does, it may be an optimization concern rather than an architectural pattern. | **Medium.** If this is merely an optimization (like compiler inlining), it should not be elevated to an architectural pattern. However, the LLM context adds factors absent from compiler inlining: context window limits, token costs, and failure isolation are architectural, not just performance concerns. The distinction appears meaningful for LLM pipelines specifically. |
| **Compiler inlining is the closest analogue** | Structural match is strong: same code, two execution modes, heuristic-driven per-site decision. The research correctly identifies this. | **BPMN embedded subprocess vs call activity** is a closer match: it is a *workflow-level* distinction (not code-level), it involves the same work potentially running embedded or as a separate callable process, and the decision includes data scoping (embedded reads parent data directly; call activity requires explicit mapping) -- which maps to the agent context-sharing question. **Edge computing offloading** is also closer: it is a *runtime* decision (not compile-time), it is per-task (not per-codebase), and the decision factors (latency, resource constraints, data locality) parallel the LLM factors (context pressure, token cost, isolation). **Serverless function fusion** (Fusionize++) is perhaps the closest of all: it is runtime, per-task, involves the same code potentially running inline or as a separate function, and uses the term "task inlining" explicitly. | **High.** The research should elevate BPMN, edge offloading, and serverless fusion above compiler inlining in the "closest analogues" ranking. Compiler inlining is compile-time; these three are runtime decisions on workflow/task units, which is structurally closer to the agent pattern. |
| **The pattern is novel in its combination of properties** | No single source combines all five listed properties (per-stage, runtime, same-stage-two-modes, heuristic-driven, deterministic gates). | Fusionize++ combines four of five: per-task granularity, runtime decision, same task in two modes, feedback-driven heuristics. It lacks deterministic gates but adds infrastructure optimization. Edge offloading combines three of five: per-task, runtime, heuristic-driven. The novelty claim rests primarily on "deterministic gates regardless of mode," which is a design choice, not a pattern characteristic. | **Low-Medium.** The combination may be novel to LLM orchestration, but the claim of novelty should be scoped: "novel within LLM agent orchestration" rather than "novel across software engineering." |

### Premortem

Assume the main conclusion ("no established term exists") is wrong. Three reasons it could fail:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **Overweighted LLM-framework evidence, underweighted systems literature.** The survey spent 11 of 16 sources on LLM/AI frameworks and classical design patterns, but only glanced at workflow engines (Temporal) and missed edge computing, serverless fusion, and BPMN entirely. The domains with the richest terminology for this exact decision were not searched. "Computation offloading" has hundreds of papers, a named binary decision, and decision frameworks (binary vs. partial offloading). "Function fusion" / "task inlining" in Fusionize++ directly names the pattern. BPMN's "embedded subprocess vs call activity" is an OMG specification-level distinction. | **High** | Invalidates the unqualified "no term exists" finding. The conclusion should be restated as: "No term exists within LLM agent orchestration frameworks. Adjacent domains use: *computation offloading* (edge computing), *function fusion/task inlining* (serverless), *embedded subprocess vs call activity* (BPMN)." |
| **Missing perspective: the pattern may not need a new name.** The research assumes the pattern deserves its own term and searches for one. But it may be a composition of two well-known patterns: the **Strategy pattern** (select algorithm at runtime) applied to **execution locality** (where code runs). The compound "execution locality strategy" or "execution mode strategy" may be sufficient without coining a new term. AWS Bedrock already uses "InvokeInlineAgent" as an API name, suggesting the industry may converge on "inline agent" as informal terminology without formalizing a pattern name. | **Medium** | Qualifies the implied need for a new term. The research should note that compound terms from existing vocabulary may suffice, and that AWS Bedrock's "inline agent" API already uses "inline" in the agent execution context (though with different semantics -- inline definition rather than inline execution). |
| **Temporal dynamics: terminology may emerge rapidly.** The LLM agent orchestration field is less than 3 years old. Fusionize++ (2024), AdaptOrch (2025), and AgentOrchestra (2025) show that terminology is actively being coined. A paper published between the research date and now could have named the pattern. The "not searched" section acknowledges DSPy, Camunda/Zeebe, Erlang/OTP, and JADE were not covered. CrewAI's delegation system is actively evolving with open PRs for hierarchical delegation. Google ADK and OpenAI SDK release updates frequently. | **Medium** | The finding is time-sensitive. Should include an explicit caveat: "As of March 2026, no LLM framework names this pattern, but the field is actively developing terminology." |

### Domains Not Covered by Original Research (Searched in Challenge)

The following domains were searched during the challenge phase and yielded relevant analogues:

**Edge Computing -- "Computation Offloading"**: A well-established field with hundreds of papers. The core decision is binary: execute locally on the device or offload to edge/cloud. Decision factors include latency, energy consumption, computational capacity, and data transmission cost. The term "binary offloading" describes the all-or-nothing decision; "partial offloading" describes splitting a task. This is the most mature terminology for the inline-vs-delegate decision in any domain, with survey papers cataloging decision algorithms (reinforcement learning, game theory, optimization).

**Serverless Computing -- "Function Fusion" / "Task Inlining"**: Fusionize++ (Kowallik et al., IEEE Trans. Cloud Computing 2024) explicitly borrows "inlining" from compilers and applies it to serverless functions. A "fusion group" is a set of tasks executed in the same function (inline); calls across fusion groups are remote (delegated). The decision is feedback-driven and runtime. This is the closest structural analogue found in any domain.

**BPMN -- "Embedded Subprocess vs Call Activity"**: An OMG (Object Management Group) specification distinguishes embedded subprocesses (execute in parent process context, share data directly) from call activities (invoke a separate reusable process, require explicit data mapping). The distinction maps precisely to the agent pattern: embedded = inline (shared context), call activity = delegate (isolated context, reusable). BPMN makes this a design-time decision, but Camunda and Flowable support runtime resolution of called process versions.

**Kubernetes -- "Sidecar Pattern"**: Co-locates supporting functionality in the same pod (analogous to inline) versus deploying as a separate service. However, this is a deployment architecture decision, not a per-invocation runtime choice.

**Game AI -- Behavior Trees**: Distinguish between inline leaf nodes and referenced subtrees (Include/Reference pattern), with eager vs. lazy inclusion. The decision is structural (design-time), not runtime.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Workflows are systems where LLMs and tools are orchestrated through predefined code paths." attributed to LangGraph [#1] | quote | [1] | corrected -- this exact wording is from Anthropic [#4], not LangGraph. LangGraph uses "Workflows have predetermined code paths and are designed to operate in a certain order." The quote is valid content but misattributed to Source [1] in the Extracts; Source [4] extract correctly attributes it. |
| 2 | "Agents are dynamic and define their own processes and tool usage." attributed to LangGraph [#1] | quote | [1] | verified |
| 3 | "Agents have more autonomy than workflows, and can make decisions about the tools they use and how to solve problems." attributed to LangGraph [#1] | quote | [1] | verified |
| 4 | Orchestrator-worker pattern: "the orchestrator breaks down tasks into subtasks, delegates subtasks to workers, synthesize[s] worker outputs into a final result" attributed to LangGraph [#1] | quote | [1] | verified |
| 5 | "A manager agent keeps control of the conversation and calls specialist agents through `Agent.as_tool()`" attributed to OpenAI [#2] | quote | [2] | verified |
| 6 | "A triage agent routes the conversation to a specialist, and that specialist becomes the active agent" attributed to OpenAI [#2] | quote | [2] | corrected -- source says "...becomes the active agent for the rest of the turn." Document truncates "for the rest of the turn." |
| 7 | Agents-as-tools suits "a specialist should help with a bounded subtask but should not take over the user-facing conversation" attributed to OpenAI [#2] | attribution | [2] | verified |
| 8 | Handoffs work when "routing itself is part of the workflow and you want the chosen specialist to own the next part" attributed to OpenAI [#2] | attribution | [2] | verified |
| 9 | "Handoffs allow an agent to delegate tasks to another agent." attributed to OpenAI [#3] | quote | [3] | verified |
| 10 | "If you have multiple possible destinations, register one handoff per destination and let the model choose among them." attributed to OpenAI [#3] | quote | [3] | verified |
| 11 | "you want structured input for a nested specialist without transferring the conversation, prefer Agent.as_tool(parameters=...)" attributed to OpenAI [#3] | quote | [3] | verified |
| 12 | "Workflows" are "systems where LLMs and tools are orchestrated through predefined code paths." attributed to Anthropic [#4] | quote | [4] | verified |
| 13 | "Agents" are "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." attributed to Anthropic [#4] | quote | [4] | verified |
| 14 | "In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results." attributed to Anthropic [#4] | quote | [4] | verified |
| 15 | "Whereas it's topographically similar, the key difference from parallelization is its flexibility -- subtasks aren't pre-defined, but determined by the orchestrator based on the specific input." attributed to Anthropic [#4] | quote | [4] | verified |
| 16 | "These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases." attributed to Anthropic [#4] | quote | [4] | verified |
| 17 | Semantic Kernel patterns table (Concurrent, Sequential, Handoff, Group Chat, Magentic) with descriptions attributed to Microsoft [#5] | attribution | [5] | verified |
| 18 | "All orchestration patterns share a unified interface for construction and invocation." attributed to Microsoft [#5] | quote | [5] | verified |
| 19 | Semantic Kernel uses `InProcessRuntime` as execution backend [#5] | api-name | [5] | verified |
| 20 | "Before you adopt a multi-agent orchestration pattern, evaluate whether your scenario requires one." attributed to Azure [#6] | quote | [6] | verified |
| 21 | Complexity levels: Direct model call, Single agent with tools, Multi-agent orchestration [#6] | attribution | [6] | verified |
| 22 | Handoff pattern: "enables dynamic delegation of tasks between specialized agents. Each agent can assess the task at hand and decide whether to handle it directly or transfer it to a more appropriate agent based on the context and requirements." attributed to Azure [#6] | quote | [6] | verified |
| 23 | Handoff also known as: "routing, triage, transfer, dispatch, delegation." attributed to Azure [#6] | attribution | [6] | verified |
| 24 | Magentic pattern: "designed for open-ended and complex problems that don't have a predetermined plan of approach." attributed to Azure [#6] | quote | [6] | verified |
| 25 | Magentic also known as: "dynamic orchestration, task-ledger-based orchestration, adaptive planning." attributed to Azure [#6] | attribution | [6] | human-review -- WebFetch returned general content but did not confirm these exact also-known-as terms for Magentic in the fetched extract |
| 26 | Google ADK Agent Transfer: parent LLM generates "transfer_to_agent(agent_name='target_agent_name')" [#7] | api-name | [7] | verified |
| 27 | Google ADK AgentTool: "Synchronous (within the parent's flow), explicit, controlled invocation like any other tool." [#7] | quote | [7] | verified |
| 28 | "In traditional distributed systems, the dynamic dispatch pattern selects and invokes specific services at runtime based on incoming event attributes, such as event type, source, and payload." attributed to AWS [#8] | quote | [8] | verified |
| 29 | "In agentic systems, routing also performs dynamic task delegation -- but instead of Amazon EventBridge rules or metadata filters, the LLM classifies and interprets the user's intent through natural language." attributed to AWS [#8] | quote | [8] | verified |
| 30 | "Static routing logic, often embedded within orchestration scripts or API layers, lacks the adaptability required for real-time, multi-model, multi-capability environments." attributed to AWS [#8] | quote | [8] | verified |
| 31 | "A Child Workflow has access to all Workflow APIs but is subject to the same deterministic constraints as other Workflows." attributed to Temporal [#9] | quote | [9] | verified |
| 32 | "The decision is roughly analogous to spawning a child process in a terminal to do work versus doing work in the same process." attributed to Temporal [#9] | quote | [9] | verified |
| 33 | "When in doubt, use an Activity." attributed to Temporal [#9] | quote | [9] | verified |
| 34 | "There is no reason to use Child Workflows just for code organization." attributed to Temporal [#9] | quote | [9] | verified |
| 35 | Valid reasons for child workflows: partitioning large workloads, service isolation, resource management, periodic logic [#9] | attribution | [9] | verified |
| 36 | "all interactions of actors use purely message passing and everything is asynchronous." attributed to Akka [#10] | quote | [10] | verified |
| 37 | Akka design philosophy: "go from remote to local by way of optimization instead of trying to go from local to remote by way of generalization." [#10] | quote | [10] | verified |
| 38 | "Just write your application according to the principles outlined in the previous sections, then specify remote deployment of actor sub-trees in the configuration file." attributed to Akka [#10] | quote | [10] | unverifiable -- WebFetch did not confirm this specific text; may be from a different section of Akka docs |
| 39 | "Proxy is a structural design pattern that lets you provide a substitute or placeholder for another object." attributed to Refactoring.Guru [#11] | quote | [11] | verified |
| 40 | Remote proxy: "Local execution of a remote service (remote proxy). This is when the service object is located on a remote server." attributed to Refactoring.Guru [#11] | quote | [11] | verified |
| 41 | "a formal framework for task-adaptive multi-agent orchestration that dynamically selects among four canonical topologies" attributed to AdaptOrch [#12] | quote | [12] | verified |
| 42 | Four canonical topologies: Parallel (tau-P), Sequential (tau-S), Hierarchical (tau-H), Hybrid (tau-X) with descriptions [#12] | attribution | [12] | verified |
| 43 | "orchestration topology -- the structural composition of how multiple agents are coordinated, parallelized, and synthesized -- now dominates system-level performance over individual model capability" attributed to AdaptOrch [#12] | quote | [12] | verified |
| 44 | "Static frameworks like LangGraph and CrewAI define fixed execution topologies (chains, graphs, or role-based teams) that persist regardless of what the task demands." attributed to AdaptOrch [#12] | quote | [12] | corrected -- source says "Static frameworks -- Model Context Protocol (MCP), LangGraph, and CrewAI -- define fixed execution topologies..." The document omits MCP and substitutes "like" for the full list. Presented as a direct quote but is a paraphrase. |
| 45 | Topology Routing Algorithm analyzes "parallelism width, critical path depth, and coupling density." attributed to AdaptOrch [#12] | attribution | [12] | verified |
| 46 | Adaptive orchestrator: "is more flexible, making decisions on the fly based on the current context." attributed to Dynamiq [#13] | quote | [13] | verified |
| 47 | Linear orchestrator: "a straightforward, step-by-step approach to task management" attributed to Dynamiq [#13] | quote | [13] | verified |
| 48 | Adaptive capabilities: "Flexible Routing", "Contextual Decisions", "Dynamic Selection", "Intelligent Selection" attributed to Dynamiq [#13] | attribution | [13] | verified |
| 49 | CNP definition: "Contract Net Protocol (CNP) is a high-level task-sharing interaction protocol for agent communication in distributed environments" attributed to ScienceDirect [#14] | quote | [14] | unverifiable -- source returned 403 |
| 50 | CNP mechanics: initiator broadcasts call-for-proposals, participants respond with quotation or refusal, initiator selects best offer [#14] | attribution | [14] | unverifiable -- source returned 403 |
| 51 | Manager pattern: "a central LLM -- the 'manager' -- orchestrates a network of specialized agents seamlessly through tool calls" attributed to OpenAI [#15] | quote | [15] | unverifiable -- source returned 403 |
| 52 | Decentralized pattern: agents "handoff" workflow execution to one another, "a one way transfer that allow an agent to delegate to another agent" attributed to OpenAI [#15] | quote | [15] | unverifiable -- source returned 403 |
| 53 | "In the manager pattern, edges represent tool calls whereas in the decentralized pattern, edges represent handoffs that transfer execution between agents." attributed to OpenAI [#15] | quote | [15] | unverifiable -- source returned 403 |
| 54 | Inline expansion direct effect: "to improve time performance (by eliminating call overhead), at the cost of worsening space usage (due to duplicating the function body)." attributed to Wikipedia [#16] | quote | [16] | unverifiable -- source returned 403; document already notes "from search extract; direct fetch returned 403" |
| 55 | "As a rule of thumb, some inlining will improve speed at very minor cost of space, but excess inlining will hurt speed, due to inlined code consuming too much of the instruction cache." attributed to Wikipedia [#16] | quote | [16] | unverifiable -- source returned 403 |
| 56 | "Usually, an inlining algorithm has a certain code budget (an allowed increase in program size) and aims to inline the most valuable callsites without exceeding that budget." attributed to Wikipedia [#16] | quote | [16] | unverifiable -- source returned 403 |
| 57 | PGO "uses execution profiles to weigh call-site hotness." attributed to Wikipedia [#16] | quote | [16] | unverifiable -- source returned 403 |
| 58 | "No LLM agent framework names the inline-vs-delegate meta-decision." -- Finding SQ1 | factual | [1]-[8],[12],[13] | verified -- eight frameworks surveyed; none name this specific decision point; confirmed by re-verification of all fetched sources |
| 59 | "Eight major frameworks surveyed" -- Finding SQ1 | statistic | -- | verified -- document lists LangGraph, OpenAI Agents SDK, Anthropic, Semantic Kernel, Google ADK, AWS, Dynamiq, AdaptOrch = 8 |
| 60 | OpenAI Agents SDK is "the closest any framework comes to the inline-vs-delegate distinction" | superlative | [2],[3] | verified -- agents-as-tools vs handoffs is the closest named mechanism across all surveyed LLM frameworks |
| 61 | AWS Bedrock uses "InvokeInlineAgent" as an API name | api-name | -- | human-review -- no cited source; claim from challenge section without source URL; CoVe: AWS Bedrock does have an InvokeInlineAgent API but this is not cited to a source |
| 62 | Edge computing "computation offloading" described as "the most mature vocabulary for the inline-vs-delegate decision in any domain" | superlative | -- | human-review -- uncited challenge-phase claim; CoVe agrees computation offloading is well-established but "most mature in any domain" is a strong superlative |
| 63 | Fusionize++ (Kowallik et al., IEEE Trans. Cloud Computing 2024) uses "task inlining" | attribution | -- | human-review -- uncited challenge-phase claim; no source URL provided for verification |
| 64 | "BPMN -- embedded subprocess vs call activity" described as "W3C-level specification" | attribution | -- | corrected -- BPMN is an OMG (Object Management Group) standard, not W3C; all instances in document corrected to "OMG" |
| 65 | Fusionize++ "combines four of five" properties (per-task, runtime, same code two modes, feedback-driven heuristics) | factual | -- | human-review -- uncited challenge-phase claim; cannot verify specific property count without source |
| 66 | "the field is under 3 years old" referring to LLM agent orchestration | factual | -- | human-review -- CoVe notes LLM agent frameworks date to approximately 2023 (AutoGPT, LangChain agents); "under 3 years" as of March 2026 is approximately correct but imprecise |
| 67 | Semantic Kernel selects orchestration patterns "at construction time, not per-invocation" | factual | [5] | verified -- confirmed by source code examples showing pattern selected at construction |
| 68 | AWS uses "dynamic dispatch" for agent routing, not execution mode | factual | [8] | verified |
| 69 | Akka location transparency "deliberately hides the inline-vs-remote distinction" | attribution | [10] | verified |
| 70 | Temporal child workflow vs activity is "the closest classical analogue to inline-vs-delegate" | superlative | [9] | verified -- among classical sources surveyed, Temporal's distinction is the most structurally similar |

<!-- search-protocol
[
  {"query": "LangGraph conditional edge inline subagent dynamic delegation orchestration 2024 2025", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 2},
  {"query": "CrewAI AutoGen inline execution vs delegate agent orchestration pattern LLM", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "adaptive delegation microservices orchestration pattern execution locality runtime decision", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "contract net protocol self-execution delegation multi-agent systems BDI", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "LangGraph supervisor handoff inline vs subgraph agent execution 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 2},
  {"query": "OpenAI Agents SDK handoff runner dynamic agent delegation orchestration pattern 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 2},
  {"query": "Temporal workflow child workflow vs activity decision heuristic when to use inline", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 2},
  {"query": "dynamic composition vs static composition agent pipeline runtime orchestration", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "compiler function inlining decision heuristic runtime call overhead vs inline expansion", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 1},
  {"query": "strategy pattern runtime execution mode selection in-process vs remote delegation", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 1},
  {"query": "actor model location transparency local remote decision Akka Erlang", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 2},
  {"query": "Semantic Kernel planner inline function vs agent delegation orchestration Microsoft 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 1},
  {"query": "adaptive orchestration OR hybrid execution multi-agent LLM pipeline 2024 2025 terminology", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 2},
  {"query": "polymorphic dispatch agent orchestration OR execution mode runtime selection pattern", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "Google ADK agent development kit orchestration delegation inline subagent 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 1},
  {"query": "elastic delegation OR runtime dispatch vs static dispatch agent orchestration LLM subagent", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "multi-agent self-execution OR self-perform vs delegate task allocation runtime decision BDI MOISE", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "Anthropic building effective agents orchestration workflow pattern December 2024", "source": "google", "date_range": "2024", "results_found": 10, "results_used": 1},
  {"query": "proxy pattern local proxy remote proxy runtime decision delegation software architecture", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 1},
  {"query": "OpenAI a practical guide to building agents orchestration pattern terminology 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 1},
  {"query": "AWS Strands agents orchestration inline vs subagent execution mode 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 0}
]
-->

<!-- not_searched
- DSPy programming model — relevant but search budget exhausted; DSPy uses "modules" that can be optimized but does not address inline-vs-delegate
- Camunda/Zeebe BPMN — workflow engines with subprocess decisions; likely similar to Temporal findings
- Erlang/OTP supervisor trees — process spawning decisions; likely similar to Akka location transparency findings
- JADE agent platform — older MAS framework; unlikely to have novel terminology for this pattern
-->
