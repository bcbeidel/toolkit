---
name: Multi-Agent Orchestration Patterns and Selection Criteria
description: "Five orchestration patterns (orchestrator-worker, hierarchical, pipeline, mesh, swarm) have distinct tradeoffs; most production systems combine them, and qualitative fit criteria are high-confidence but quantitative thresholds are not."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://blog.langchain.com/langgraph-multi-agent-workflows/
  - https://arxiv.org/abs/2601.13671
  - https://dev.to/jose_gurusup_dev/agent-orchestration-patterns-swarm-vs-mesh-vs-hierarchical-vs-pipeline-b40
  - https://arxiv.org/html/2604.02460v1
related:
  - docs/context/agent-tool-portability-and-mcp-as-transport-layer.context.md
  - docs/context/multi-agent-shared-state-failure-mechanisms.context.md
  - docs/context/agentic-planning-hybrid-global-plan-local-react.context.md
  - docs/context/skill-chain-sequential-and-recursive-design-rules.context.md
---
# Multi-Agent Orchestration Patterns and Selection Criteria

**Five patterns are documented in the literature. The qualitative tradeoffs are high-confidence (T1/T3 sources converge); specific numeric thresholds are low-confidence (T5 single source).** Use pattern descriptions for architecture decisions; treat the numbers as rough intuition.

## The Five Patterns

**Orchestrator-Worker (Supervisor)**
A central orchestrator decomposes tasks and assigns them to specialized workers. All coordination flows through the orchestrator; workers do not communicate directly. Anthropic describes this as: "A central LLM breaks down tasks dynamically and delegates to specialized workers, then synthesizes results." LangGraph implements it via a supervisor agent whose "tools are other agents."

Best for: fan-out workloads with independent subtasks (document processing, customer support triage, code generation). Easiest to debug — single control flow. Bottleneck risk emerges when many subtasks run concurrently.

**Hierarchical**
Agents organized in a tree: strategy at top, tactics in middle, execution at leaves. Each level holds only its relevant context. IBM enterprise research confirms this as the standard for large-scale systems with "domain-specific agent clusters each managed by supervisors, with supervisors reporting to a top-level strategic coordinator."

Best for: complex enterprise tasks with many agents, or when context window constraints require level-specific summarization. Latency compounds at each level; information can be lost through inter-level summarization.

**Pipeline**
Fixed sequential stages with defined input/output contracts at each boundary. Each stage receives input from the prior stage, transforms it, and passes output forward.

Best for: content generation workflows (research → outline → draft → edit → publish), ETL, batch processing. Highly debuggable. Cannot handle conditional branching; cold-start latency accumulates across stages.

**Mesh (Peer-to-Peer)**
Agents maintain explicit, persistent connections to specific peers defined at deploy time. Direct agent-to-agent communication without a central coordinator.

Best for: small groups (3–8) of tightly coupled agents with iterative feedback loops (planning → coding → testing). Combinatorial connection growth makes it impractical at scale.

**Swarm**
Autonomous peer agents coordinate through shared state without direct connections. Coordination emerges from simple local rules applied simultaneously. Both AutoGen and CrewAI adopted swarm-style agent-initiated handoffs in late 2025.

Best for: exploration tasks and parallel discovery where the optimal path is unknown. High fault tolerance, but observability is difficult and convergence conditions require careful design.

## Pattern Selection

| Pattern | Scalability | Debugging | Best For |
|---------|-------------|-----------|----------|
| Orchestrator-Worker | Medium | Easy | Fan-out, independent tasks |
| Hierarchical | High | Medium | Enterprise, many agents |
| Pipeline | Medium | Easy | Batch, sequential workflows |
| Mesh | Low | Medium | Small collaborative groups |
| Swarm | High | Hard | Exploration, parallel discovery |

Most production systems combine patterns: a hierarchical system where leaf-level teams use mesh coordination internally, or a pipeline where one stage launches a swarm for parallel data collection. The selection principle: match control flow structure to how information actually flows in the task, not to how many agents you have.

## Important Caveat: Single Agents Often Match Multi-Agent

A 2026 empirical study (arXiv 2604.02460, April 2026) found that under matched thinking-token budgets, single-agent systems consistently match or outperform multi-agent systems on multi-hop reasoning tasks. The key finding: MAS advantages reported in prior literature frequently stem from unaccounted computation differences rather than architectural benefits. Single agents are the strongest default architecture for multi-hop reasoning when compute is controlled.

MAS becomes competitive only when a single agent's effective context genuinely degrades — through context deletion, masking, or distraction injection — or when tasks are truly parallelizable and independent. Economic analysis (Iterathon 2026) suggests that for the majority of use cases, a well-prompted single agent delivers equivalent results at approximately one-third the cost.

The selection criteria above remain valid as qualitative tradeoffs between patterns. The higher-order selection criterion is: **verify that a single agent with tools does not suffice before adopting multi-agent architecture**. Pattern selection is a secondary decision.

## Takeaway

Start with orchestrator-worker unless you have a clear reason not to — it offers the best debuggability and is directly confirmed by Anthropic and LangGraph. But first: verify that a single agent with tools does not suffice. Multi-agent systems are justified when context genuinely degrades or tasks are truly parallelizable — not as a general upgrade from single agents. Add hierarchical tiers when context window constraints or organizational scale require it. Treat numeric thresholds (N(N-1)/2 mesh connections, 50-agent orchestrator bottleneck) as rough intuition from a single practitioner source, not empirical design criteria.
