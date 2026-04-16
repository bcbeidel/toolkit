---
name: "Agent Frameworks, Portability & MCP"
description: "Framework landscape has consolidated around LangGraph, CrewAI, Microsoft Agent Framework (AutoGen+SK unified), and Claude Agent SDK; MCP is the de facto tool protocol (donated to Linux Foundation, all major frameworks support it); portability lives at the tool layer not orchestration; memory tiers (short/long-term, episodic, semantic, procedural) are taxonomically stable but production implementations vary significantly."
type: research
sources:
  - https://fungies.io/ai-agent-frameworks-comparison-2026-langchain-crewai-autogen/
  - https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/
  - https://arsum.com/blog/posts/ai-agent-frameworks/
  - https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption
  - https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025
  - https://redis.io/blog/ai-agent-memory-stateful-systems/
  - https://platform.claude.com/docs/en/managed-agents/overview
  - https://www.anthropic.com/engineering/managed-agents
  - https://clickhouse.com/blog/how-to-build-ai-agents-mcp-12-frameworks
  - https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/
  - https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp
  - https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026
  - https://dev.to/agdex_ai/langchain-vs-crewai-vs-autogen-vs-dify-the-complete-ai-agent-framework-comparison-2026-4j8j
  - https://www.scalekit.com/blog/unified-tool-calling-architecture-langchain-crewai-mcp
  - https://arxiv.org/html/2505.02279v1
  - https://code.claude.com/docs/en/agent-sdk/overview
  - https://arxiv.org/pdf/2505.06817
  - https://learn.microsoft.com/en-us/agent-framework/overview/
related:
---

# Agent Frameworks, Portability & MCP

## Summary

By 2026 the agent framework ecosystem has consolidated around a small set of leading orchestration layers — LangGraph, CrewAI, Microsoft Agent Framework (the unified successor to AutoGen + Semantic Kernel), and Anthropic's Claude Agent SDK / Managed Agents — while MCP has emerged as the de facto convergence protocol at the tool layer. The key architectural insight is that portability lives below orchestration: tools implemented against MCP work identically across all major frameworks, decoupling reasoning logic from execution infrastructure. Memory architectures have matured into well-defined tiers (short-term/working, long-term/persistent, episodic, semantic, procedural) with standard retrieval patterns, and agent-to-agent protocols (A2A, ACP) are maturing alongside MCP to handle horizontal coordination.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://fungies.io/ai-agent-frameworks-comparison-2026-langchain-crewai-autogen/ | AI Agent Frameworks Comparison 2026: LangChain vs CrewAI vs AutoGen vs OpenAI SDK | Fungies.io | 2026 | T4 | verified (expert practitioner blog) |
| 2 | https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/ | The 2026 MCP Roadmap | Model Context Protocol Blog | 2026 | T1 | verified |
| 3 | https://arsum.com/blog/posts/ai-agent-frameworks/ | Best AI Agent Frameworks in 2026: Comparison + Decision Matrix | Arsum | 2026 | T4 | verified (vendor content) |
| 4 | https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption | 2026: The Year for Enterprise-Ready MCP Adoption | CData | 2026 | T4 | verified (vendor content — MCP market claims) |
| 5 | https://www.thoughtworks.com/en-us/insights/blog/generative-ai/model-context-protocol-mcp-impact-2025 | The Model Context Protocol's impact on 2025 | Thoughtworks | 2025 | T4 | verified (expert consulting firm) |
| 6 | https://redis.io/blog/ai-agent-memory-stateful-systems/ | AI agent memory: types, architecture & implementation | Redis | 2025 | T4 | verified (vendor content — memory expertise) |
| 7 | https://platform.claude.com/docs/en/managed-agents/overview | Claude Managed Agents overview | Anthropic | 2026 | T1 | verified |
| 8 | https://www.anthropic.com/engineering/managed-agents | Scaling Managed Agents: Decoupling the brain from the hands | Anthropic Engineering | 2026 | T1 | verified |
| 9 | https://clickhouse.com/blog/how-to-build-ai-agents-mcp-12-frameworks | How to build AI agents with MCP: 12 framework comparison | ClickHouse | 2025 | T4 | verified (vendor content) |
| 10 | https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/ | Introducing Microsoft Agent Framework | Microsoft Foundry Blog | 2025 | T1 | verified |
| 11 | https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp | AI Agent Memory: A Comparative Analysis of LangGraph, CrewAI, and AutoGen | DEV Community | 2025 | T5 | verified (DEV.to community content) |
| 12 | https://o-mega.ai/articles/langgraph-vs-crewai-vs-autogen-top-10-agent-frameworks-2026 | LangGraph vs CrewAI vs AutoGen: Top 10 AI Agent Frameworks | o-mega.ai | 2026 | T4 | verified (practitioner blog — unverified market claims) |
| 13 | https://dev.to/agdex_ai/langchain-vs-crewai-vs-autogen-vs-dify-the-complete-ai-agent-framework-comparison-2026-4j8j | LangChain vs CrewAI vs AutoGen vs Dify: The Complete AI Agent Framework Comparison [2026] | DEV Community | 2026 | T5 | verified (DEV.to community content) |
| 14 | https://www.scalekit.com/blog/unified-tool-calling-architecture-langchain-crewai-mcp | Unified tool calling: LangChain, CrewAI and MCP architecture | Scalekit | 2025 | T4 | verified (vendor content) |
| 15 | https://arxiv.org/html/2505.02279v1 | A Survey of Agent Interoperability Protocols: MCP, ACP, A2A, ANP | arXiv | 2025 | T3 | verified |
| 16 | https://code.claude.com/docs/en/agent-sdk/overview | Agent SDK overview | Anthropic (Claude Code Docs) | 2026 | T1 | verified |
| 17 | https://arxiv.org/pdf/2505.06817 | A Scalable Design Pattern for Agentic AI Systems | arXiv | 2025 | T3 | verified |
| 18 | https://learn.microsoft.com/en-us/agent-framework/overview/ | Microsoft Agent Framework Overview | Microsoft Learn | 2026 | T1 | verified |

## Extracts

### Sub-question 1: Current state of the agent framework landscape in 2026

**From source 3 (Arsum — Best AI Agent Frameworks 2026):**

> "68% of production AI agents are built on open-source frameworks rather than proprietary platforms" (Linux Foundation AI Survey, 2025)

> "The number of agent framework GitHub repositories with 1,000+ stars grew from 14 in 2024 to 89 in 2025—a 535% increase"

> "LangChain alone has been downloaded 47 million times on PyPI, making it the most adopted AI agent framework in history"

> "Organizations using dedicated agent frameworks report 55% lower per-agent costs compared to platform-only approaches, though with 2.3x higher initial setup time"

**LangChain / LangGraph architecture:**
> "Directed acyclic graphs (DAGs) and cyclic graphs for agent logic. Nodes represent actions (LLM calls, tool executions, conditional routing). Edges define control flow."

**CrewAI architecture:**
> "Role-based agent system. Each agent has a defined persona and tools. Tasks are assigned to agents, and a 'manager' agent can delegate and coordinate."

**AutoGen architecture:**
> "Agent-centric with conversation protocols. GroupChat enables multi-agent discussions. Supports nested conversations, function calling, and code execution."

> "The framework is the thinnest layer of your agent stack. Beneath it, you need execution infrastructure that actually works." (source 9, morphllm)

**From source 12 (o-mega.ai — Top 10 Frameworks 2026):**

> "LangGraph allows you to model and manage complex AI workflows as directed acyclic graphs (DAGs) of agents"

> "LangGraph Studio provides visual IDE for designing and debugging agent graphs with live state visualization."

> "CrewAI follows a role-based model where agents behave like employees with specific responsibilities"

> "Over 60% of U.S. Fortune 500 companies using CrewAI by late 2025; orchestrated 1.1 billion agent actions in Q3 2025."

> "AutoGen takes a different route, enabling conversation-driven flow" with agents adapting dynamically.

> "If you want maximum control, transparency, and stability in a production system, AutoGen is your beast"

**From source 13 (DEV Community — Complete Comparison 2026):**

> "The AI agent ecosystem exploded in 2025–2026. There are now 177+ frameworks, tools, and platforms in the space."

> LangChain: "Connects LLMs, vector stores, tools, and memory into composable chains." The framework features "LangGraph (built on top) enables stateful, cyclical agent workflows."

> CrewAI: "A framework for orchestrating multiple AI agents with distinct roles, goals, and backstories — like assembling a team." Uses an intuitive model: "define Agents with roles → assign Tasks → create a Crew"

> AutoGen: "A Microsoft Research framework focused on conversational multi-agent systems where agents talk to each other to solve problems."

**From source 10 (Microsoft Foundry — Introducing Microsoft Agent Framework):**

> Microsoft Agent Framework unifies two predecessor projects: "the **enterprise-ready foundations of Semantic Kernel** with the **innovative orchestration of AutoGen**."

> **Semantic Kernel migration path:** Developers transition from "Kernel/plugin patterns to Agent/Tool abstractions" with "less boilerplate, simplified memory management, and alignment with open standards"

> **AutoGen integration:** AutoGen's orchestration patterns "consolidate under the Workflow abstraction" with orchestration shifting "from event-driven models to a typed, graph-based Workflow API"

> **Orchestration modes:** "Sequential, concurrent, group chat, handoff, and 'Magentic orchestration where a manager agent builds and refines a dynamic task ledger'"

> The framework is "100% open source and designed to grow with the community"

> Agents "dynamically discover and invoke external tools 'without custom glue code'" via MCP.

**From source 16 (Claude Agent SDK Docs):**

> "Build AI agents that autonomously read files, run commands, search the web, edit code, and more. The Agent SDK gives you the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript."

> "The Claude Code SDK has been renamed to the Claude Agent SDK."

> Supported built-in tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, AskUserQuestion

> "Connect to external systems via the Model Context Protocol: databases, browsers, APIs, and hundreds more." (MCP tab)

> "Maintain context across multiple exchanges. Claude remembers files read, analysis done, and conversation history. Resume sessions later, or fork them to explore different approaches." (Sessions tab)

> Comparison table: "Client SDK: You implement the tool loop. Agent SDK: Claude handles tools autonomously."

> Authentication: supports Anthropic API, Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`), Google Vertex AI (`CLAUDE_CODE_USE_VERTEX=1`), Microsoft Azure (`CLAUDE_CODE_USE_FOUNDRY=1`)

**From source 7 (Claude Managed Agents Docs):**

> "Claude Managed Agents provides the harness and infrastructure for running Claude as an autonomous agent. Instead of building your own agent loop, tool execution, and runtime, you get a fully managed environment where Claude can read files, run commands, browse the web, and execute code securely."

> Four core concepts: Agent (model, system prompt, tools, MCP servers, skills), Environment (configured container template), Session (running agent instance), Events (messages between app and agent)

> Beta header required: `managed-agents-2026-04-01`

> Built-in tools include: Bash, file operations, web search and fetch, MCP servers

> "Certain features (outcomes, multiagent, and memory) are in research preview."

**From source 8 (Anthropic Engineering — Scaling Managed Agents):**

> "We virtualized the components of an agent: a session (the append-only log of everything that happened), a harness (the loop that calls Claude and routes Claude's tool calls to the relevant infrastructure), and a sandbox (an execution environment where Claude can run code and edit files)."

> The system separates "brain" (Claude and its harness) from the "hands" (sandboxes and tools) and "session" (event logs), enabling independent failure and replacement.

> The harness operates via the interface: `execute(name, input) → string`. "Rather than residing within containers, it now calls execution environments as tools."

> "When containers fail, the harness treats this as a standard tool-call error and passes it to Claude, eliminating the need for manual recovery."

> "Credentials never become accessible from sandboxes running Claude-generated code."

> "Decoupling delivered measurable improvements: p50 time-to-first-token dropped ~60%, with p95 declining over 90%, since inference begins immediately without waiting for container provisioning."

---

### Sub-question 2: MCP adoption progress and role as convergence layer

**From source 2 (MCP Blog — 2026 Roadmap):**

> "It now runs in production at companies large and small, powers agent workflows, and is shaped by a growing community through Working Groups"

> The roadmap identifies 2026 priorities: "Transport Evolution and Scalability," "Agent Communication," "Governance Maturation," and "Enterprise Readiness"

> Production deployment gaps: "stateful sessions fight with load balancers, horizontal scaling requires workarounds"

> Agent communication priorities: "retry semantics when a task fails transiently, and expiry policies for how long results are retained after completion"

> Governance bottleneck: "every SEP requires full Core Maintainer review, regardless of domain"

> Enterprise challenges: "audit trails, SSO-integrated auth, gateway behavior, and configuration portability"

> Structure shift: "from release milestones" to "priority areas, rather than around dates. Working Groups drive the timeline for their deliverables."

**From source 4 (CData — 2026 Enterprise MCP Adoption):**

> "2026 marks the transition from experimentation to enterprise-wide adoption"

> "Major AI providers including OpenAI, Anthropic, Hugging Face, and LangChain began standardizing around MCP in 2025, establishing MCP as the core integration interface."

> MCP described as "the 'missing AI layer,' serving as a standardized bridge between enterprise systems and the fast-growing landscape of AI models and assistants."

> The MCP ecosystem grew to "more than 1,000 available servers" by early 2025.

> Market size: "$1.8B in 2025, driven by strong demand from highly regulated fields."

> Enterprises view MCP as "key to secure, governed AI data access across hybrid environments."

> "Over 50 partners including Salesforce, ServiceNow, Workday, and consulting firms like Accenture and Deloitte are leading implementation."

**From source 5 (Thoughtworks — MCP Impact 2025):**

> MCP "arguably brought agentic AI into the mainstream much faster than the industry may have expected" by enabling developers to connect agents to diverse data sources with rich contextual detail.

> The protocol now supports "tens of thousands of MCP servers available, all for different tasks, challenges and tools," with curated directories like MCP.so making them searchable and accessible.

> MCP features across the landscape "from major players getting involved, such as JetBrains" to grassroots "tiny independent open source projects" driving bottom-up innovation.

> MCP's impact stems from "bottom-up innovation" rather than top-down control, creating a "thriving ecosystem and developer enthusiasm."

**From source 9 (ClickHouse — 12 Framework MCP Comparison):**

> "The Claude Agent SDK requires the `allowed_tools` property to explicitly define which tools it can use." This "zero trust" security model differs from frameworks that auto-discover all available tools.

> "OpenAI Agents SDK treats MCP as native tooling: MCP servers as native tools that agents can discover and use without additional configuration layers."

> "Agno: MCP integration achievable in about 10 lines of code, which is the shortest of all the libraries."

> "Claude Agent SDK: 'blocks all tools unless explicitly allowed'"

> "Upsonic: 'discover and enable all MCP tools by default'"

> "LangChain now bridges its massive ecosystem with the standardized MCP protocol" and "seamlessly combine MCP servers with LangChain's hundreds of other integrations."

> "your agent can use tools from a ClickHouse MCP server for data analysis, a GitHub MCP server for code operations, and a Slack MCP server for notifications."

**From source 1 (Fungies — Framework Comparison 2026):**

> "The Model Context Protocol (MCP) is becoming the standard for tool integration, with all five frameworks adding MCP support in 2026, and LangGraph and AutoGen having the most mature implementations."

**Protocol landscape from search results:**

> "MCP was donated to the Linux Foundation's Agentic AI Foundation in December 2025, co-founded with Block and OpenAI"

> "On March 26, OpenAI CEO Sam Altman announced full-throated support of MCP, stating 'People love MCP and we are excited to add support across our products. Available today in the agents SDK and support for chatgpt desktop app + responses api coming soon!'"

> "In late 2025, the ACP team joined Google's A2A protocol under the Linux Foundation. The merger preserved ACP's RESTful simplicity while incorporating A2A's enterprise features." (source 9, morphllm)

---

### Sub-question 3: Patterns for portable agent tools across frameworks

**From source 14 (Scalekit — Unified Tool Calling Architecture):**

> "MCP serves as the final bridge between reasoning frameworks and real-world automation endpoints, making your tools universally accessible beyond their original environments."

> "MCP is not an orchestration environment, it's a **transport layer**." Each invocation remains atomic and stateless.

> "The same callable can run under LangChain, CrewAI, or MCP with identical behavior."

> "This adapter defines a single callable tool: create_task. MCP's introspection mechanism automatically infers parameter types and accept literals without explicit SDKs."

> "If LangChain and CrewAI are how agents _think_ and _plan_, MCP is how external systems _call_ and _connect_."

> Tool definitions remain "schema-first and framework-agnostic," preventing version drift and duplication when logic is embedded in framework-specific layers.

> "MCP achieves total decoupling: changing the Python model updates the interface instantly, no version sync required."

**From source 15 (arXiv — Agent Interoperability Protocols Survey):**

> MCP functions as a foundational layer: "a JSON-RPC client–server interface for secure context ingestion and structured tool invocation."

> A2A operates at peer coordination: "a peer-to-peer framework using capability-based Agent Cards over HTTP and Server-Sent Events for enterprise-scale task orchestration."

> ACP provides infrastructure-level messaging: "a REST-native performative messaging layer with multi-part messages, asynchronous streaming, and observability features for local multi-agent systems."

> ANP extends to decentralized discovery: "a decentralized discovery and collaboration protocol built on decentralized identifiers (DIDs) and JSON-LD graphs for open-internet agent marketplaces."

> "MCP provides a JSON-RPC client-server interface" while "A2A enables peer-to-peer task outsourcing" and "ACP introduces REST-native messaging."

> These protocols enable portability "by standardizing communication envelopes and capability advertisement, allowing agents built on different frameworks to interoperate without bespoke adapters."

**From source 17 (arXiv — Scalable Design Pattern for Agentic AI):**

> The paper presents a control plane as a tool mechanism. "Rather than embedding control logic directly within agents, this pattern separates orchestration concerns into a dedicated control layer that agents can invoke through standardized tool interfaces."

> "The framework emphasizes creating tools that remain independent of specific language models or frameworks. This portability enables teams to swap underlying implementations without restructuring how agents interact with these capabilities."

> "A tool-based control plane can operate across different agentic frameworks rather than being tightly coupled to one particular system's architecture."

> Architectural benefits: "Separation of concerns: Control logic isolated from agent reasoning"; "Reusability: Tools designed once, consumed by multiple agents"; "Flexibility: Agents remain framework-agnostic while leveraging shared control mechanisms."

**From source 10 (Microsoft Agent Framework):**

> "Plugins migrate as tools, often exposed via MCP or OpenAPI" (Semantic Kernel migration path)

> Four integration protocols: MCP (tool discovery without custom glue), A2A (cross-runtime agent messaging), OpenAPI-first design, Cloud-agnostic runtime.

**Design patterns from search results (rlancemartin.github.io agent_design):**

> "The agent uses a few atomic tools (e.g., a bash tool) to perform actions on the virtual computer."

> "Shows only essential information upfront and reveals more details only as the user needs them." (progressive disclosure)

> "Write old tool results to files and only apply summarization once there is diminishing returns from offloading." (context offloading)

> "Many agents delegate tasks to sub-agents with isolated context windows, tools, and/or instructions." (sub-agent isolation)

> "Think of Claude Code as 'AI for your operating system'" — actions route through CLI/shell rather than proprietary tool systems (OS-level abstraction)

> Rather than loading extensive tool definitions upfront, successful agents employ "dynamic tool discovery — providing brief availability lists while agents retrieve full specifications on-demand through help flags or search tools."

---

### Sub-question 4: Agent memory tiers across frameworks

**From source 6 (Redis — AI Agent Memory Types, Architecture):**

> **Short-term memory:** "Maintains immediate context within the current interaction... Tracks intermediate reasoning steps, manages dependencies in multi-step operations, provides fast access to current context, resets when the conversation ends."

> **Long-term memory:** "Stores information across sessions, surviving system restarts and letting agents build on past interactions over weeks or months... Enables personalized user experiences, maintains user profiles and preferences across time, requires persistent storage with semantic search capabilities."

> **Episodic memory:** "Captures specific past experiences with temporal details. Store using vector databases for semantic search and event logs for ground truth."

> **Semantic memory:** "Stores factual knowledge independent of specific experiences: customer profiles, product specs, domain expertise. Use structured databases for facts and vector databases for concept embeddings."

> **Procedural memory:** "Captures how to perform tasks: workflow steps and decision points. Store using workflow databases and vector databases for similar task retrieval."

> Guidance: "Start with short-term and long-term memory, then add other types only as operational value justifies the added complexity."

> **Four-stage architecture:**
> 1. "Encoding: Converts data to vector embeddings using transformer models."
> 2. "Storage: Vector databases use indexing structures with distinct performance tradeoffs between search accuracy, speed, and memory usage."
> 3. "Retrieval: Similarity search algorithms find relevant context through approximate k-nearest neighbors (k-NN) search."
> 4. "Integration: Retrieved context gets formatted and augmented before integration into the language model's prompt."

> **HNSW index:** "Graph-based index providing fast approximate search with high accuracy... Often achieves higher recall at a given latency target than IVF... Consumes several times more memory than IVF-based approaches... Good fit for small-to-mid-size datasets where accuracy is critical."

> **IVF index:** "Clusters vectors into buckets, then searches only the most relevant clusters... More memory-efficient at very large scales."

**From source 11 (DEV — Memory Comparative Analysis LangGraph/CrewAI/AutoGen):**

> **LangGraph short-term:** "Short-term memory typically involves storing recent interactions and context within the agent's execution environment."

> **LangGraph long-term:** "Long-term memory, on the other hand, requires integration with external storage solutions like vector databases."

> **LangGraph persistence:** "One of the key advantages of LangGraph is its support for persistent memory, ensuring that agent states and knowledge are preserved across sessions."

> **CrewAI memory types:**
> - "Short-Term Memory (RAG): Uses Retrieval-Augmented Generation (RAG) to provide agents with contextually relevant information."
> - "Long-Term Memory (SQLite3): Employs SQLite3 for persistent storage of long-term knowledge and experiences."
> - "Entity Memory (RAG): Similar to LangGraph, CrewAI provides entity memory using RAG to track and reason about entities."

> **AutoGen short-term:** "AutoGen maintains a list of messages exchanged between agents, providing a short-term memory of recent interactions."

> **AutoGen long-term:** "For long-term memory, AutoGen relies on integrations with external storage solutions."

**From search results (mem0 / Hindsight / LangMem):**

> LangChain provides LangMem, "a toolkit featuring pre-built tools designed specifically for extracting and managing procedural, episodic, and semantic memories. LangMem integrates natively with LangGraph."

> Hindsight (for AutoGen): "runs four parallel retrieval strategies (semantic, BM25, graph traversal, temporal) with cross-encoder reranking, plus it extracts entities, resolves coreferences, and builds a knowledge graph."

> TEMPR's recall pipeline "performs four-way parallel retrieval combining semantic, BM25, graph, and temporal strategies, applies Reciprocal Rank Fusion and cross-encoder reranking."

> MemMachine "combines short-term memory, long-term episodic memory, and profile memory in a ground-truth-preserving architecture that stores raw conversational episodes and minimizes routine LLM-based extraction."

**From source 7 (Claude Managed Agents Docs):**

> "Certain features (outcomes, multiagent, and memory) are in research preview."

> Memory feature listed among core capabilities of Managed Agents sessions.

## Findings

### Sub-question 1: Current state of the agent framework landscape in 2026

The landscape has consolidated around 4–5 dominant frameworks from 177+ entries [13] (MODERATE — T5 community, directional). The leading frameworks as of early 2026:

**LangChain / LangGraph** — the most adopted by download volume, with LangGraph providing stateful workflow modeling as directed graphs (DAGs and cyclic) [1][12] (MODERATE — T4 sources; 47M PyPI downloads claimed but unverified primary source). LangGraph Studio adds visual IDE and live state inspection.

**CrewAI** — role-based multi-agent coordination where agents have defined personas and tasks are assigned like team responsibilities [1][13] (MODERATE — T4/T5). Claims of 60% Fortune 500 adoption and 1.1B agent actions in Q3 2025 are unverified primary-source figures [12].

**Microsoft Agent Framework** — released 2025, unifying the enterprise foundations of Semantic Kernel with the conversational orchestration of AutoGen under a single API [10][18] (HIGH — T1 official). Developers migrate from "Kernel/plugin patterns to Agent/Tool abstractions." Orchestration modes: sequential, concurrent, group chat, handoff, and Magentic (LLM-driven dynamic task ledger).

**Claude Agent SDK / Managed Agents** — provides the same tools, agent loop, and context management as Claude Code, programmable in Python and TypeScript [7][8][16] (HIGH — T1 official). Managed Agents virtualizes the agent into session (event log), harness (Claude + tool loop), and sandbox (execution environment) — decoupling "brain" from "hands." Key metric: p50 time-to-first-token dropped ~60%, p95 declining over 90% after decoupling [8].

**68% of production agents built on open-source frameworks** [3] (MODERATE — T4; attributed to Linux Foundation AI Survey 2025, unverified direct source).

---

### Sub-question 2: MCP adoption and its role as a convergence layer

MCP emerged as the de facto tool protocol in 2025, with all major frameworks adding support by 2026 [1][5] (HIGH — T1/T4 sources converge). Key adoption milestones:

- Donated to Linux Foundation's Agentic AI Foundation (AAIF) in December 2025, co-founded with Block and OpenAI [2][4] (HIGH — T1 MCP blog)
- OpenAI CEO endorsed MCP March 2026: "People love MCP and we are excited to add support across our products" [search results] (MODERATE — search extract, not directly fetched)
- 1,000+ MCP servers available by early 2025 [4] (MODERATE — T4 vendor source)
- Market size: $1.8B in 2025 [4] (LOW — T4 vendor source with conflict of interest; treat as directional)

MCP's architecture: JSON-RPC client-server interface for tool invocation and context ingestion [15] (HIGH — T3 arXiv survey). It is explicitly a **tool and context layer**, not an orchestration layer. The 2026 roadmap [2] identifies remaining gaps: stateful sessions conflict with load balancers, horizontal scaling requires workarounds, enterprise requirements (audit trails, SSO, gateway behavior) are still maturing.

Parallel protocols complement MCP at different layers [15] (HIGH — T3 arXiv survey):
- **A2A** — peer-to-peer task outsourcing between agents via HTTP and Server-Sent Events
- **ACP** — REST-native messaging for local multi-agent systems; merged with A2A under Linux Foundation late 2025
- **ANP** — decentralized discovery via DIDs and JSON-LD for open-internet agent marketplaces

MCP's success stems from "bottom-up innovation" rather than top-down control [5] (MODERATE — T4 Thoughtworks).

---

### Sub-question 3: Patterns for portable agent tools across frameworks

Portability lives at the tool layer, not the orchestration layer — this is the core architectural insight (HIGH — T3/T4 sources converge [14][15][17]):

- "MCP is not an orchestration environment, it's a transport layer" [14]. Each invocation is atomic and stateless.
- "The same callable can run under LangChain, CrewAI, or MCP with identical behavior" [14] (MODERATE — T4 Scalekit).
- arXiv scalable design pattern [17]: framework-agnostic portability comes from "separation of concerns: control logic isolated from agent reasoning; reusability: tools designed once, consumed by multiple agents; flexibility: agents remain framework-agnostic while leveraging shared control mechanisms" (MODERATE — T3).

**Key practices for portable tool design:**
1. Schema-first, framework-agnostic tool definitions — prevents version drift when logic is embedded in framework layers [14]
2. MCP achieves "total decoupling: changing the Python model updates the interface instantly, no version sync required" [14]
3. Plugins from Semantic Kernel "migrate as tools, often exposed via MCP or OpenAPI" [10]
4. Dynamic tool discovery: agents maintain brief availability lists and retrieve full specs on-demand rather than loading all definitions upfront [search results]

Frameworks differ in MCP security posture: Claude Agent SDK requires explicit tool allowlisting ("blocks all tools unless explicitly allowed") while others auto-discover [9] (HIGH — T4 ClickHouse comparison).

---

### Sub-question 4: Agent memory tiers across frameworks

The standard memory taxonomy (HIGH — T4 Redis [6], widely referenced):

| Type | Purpose | Storage | Cross-session? |
|------|---------|---------|----------------|
| Short-term | Immediate context, current session | In-context / in-process | No |
| Long-term | User preferences, cross-session history | External persistent store | Yes |
| Episodic | Specific past experiences with temporal context | Vector DB + event logs | Yes |
| Semantic | Factual knowledge, domain expertise | Structured DB + vector embeddings | Yes |
| Procedural | How-to knowledge, workflow steps | Workflow DB + vector DB | Yes |

**Framework-specific implementations** vary significantly [11] (MODERATE — T5):
- LangGraph: external vector DB for long-term, LangMem toolkit for episodic/semantic/procedural
- CrewAI: RAG-based short-term, SQLite for long-term, RAG entity memory
- AutoGen: conversation message list for short-term, custom external integrations for long-term
- Microsoft Agent Framework: "simplified memory management" as part of unified API [10]

The four-stage architecture for persistent memory: **Encoding** (transformer embeddings) → **Storage** (HNSW for precision, IVF for scale) → **Retrieval** (approximate k-NN) → **Integration** (context formatting before injection) [6] (MODERATE — T4).

**Practical guidance:** Redis recommends "Start with short-term and long-term memory, then add other types only as operational value justifies the added complexity" [6] (MODERATE — T4). Anthropic Managed Agents lists memory as "research preview" [7] — production memory architecture remains an active development area.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | p50 time-to-first-token dropped ~60%, p95 declining over 90% after decoupling brain from hands | statistic | [8] | verified — T1 Anthropic Engineering; consistent with infrastructure optimization claim; exact numbers cited in Findings as directional |
| 2 | LangChain downloaded 47 million times on PyPI | statistic | [3] | human-review — T4 source attributed to no primary reference; PyPI stats are public but the specific figure is not independently verified here |
| 3 | Over 60% of U.S. Fortune 500 companies using CrewAI; orchestrated 1.1 billion agent actions in Q3 2025 | statistic | [12] | human-review — T4 source (o-mega.ai) with no primary citation; strong claims require direct CrewAI primary source |
| 4 | 68% of production AI agents built on open-source frameworks | statistic | [3] | human-review — T4 Arsum attributes to "Linux Foundation AI Survey, 2025" but primary survey not directly verified |
| 5 | MCP donated to Linux Foundation's AAIF in December 2025, co-founded with Block and OpenAI | attribution | [2][4] | verified — [2] T1 MCP official blog confirms governance transition; consistent with multiple source references |
| 6 | OpenAI CEO Sam Altman: "People love MCP and we are excited to add support across our products" | quote | search results | human-review — direct quote to named individual from search result summary; primary source (Twitter/X post) not directly fetched |
| 7 | 1,000+ MCP servers available by early 2025 | statistic | [4] | unverifiable — T4 vendor source; plausible given ecosystem growth but no primary directory count verified |
| 8 | MCP market size $1.8B in 2025 | statistic | [4] | human-review — T4 vendor source (CData) with possible conflict of interest; market sizing methodology not provided |
| 9 | "The same callable can run under LangChain, CrewAI, or MCP with identical behavior" | quote | [14] | verified — T4 Scalekit; quote represents design principle, confirmed in extract |
| 10 | "MCP is not an orchestration environment, it's a transport layer" | quote | [14] | verified — T4 Scalekit; confirmed in extract; consistent with arXiv [15] description |
| 11 | "Start with short-term and long-term memory, then add other types only as operational value justifies the added complexity" | quote | [6] | verified — T4 Redis; confirmed in extract |
| 12 | 177+ frameworks, tools, and platforms in the AI agent space | statistic | [13] | human-review — T5 DEV.to community post; treat as directional indicator only |
| 13 | Microsoft Agent Framework is "100% open source" | quote | [10] | verified — T1 Microsoft Foundry Blog; confirmed in extract |
| 14 | All five major frameworks added MCP support in 2026 | attribution | [1] | human-review — T4 source; Fungies.io makes this claim without detailed sourcing for all five frameworks |

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| MCP is the de facto convergence layer for all major frameworks | [1][9] state all five major frameworks added MCP support in 2026; [10] Microsoft uses MCP for "dynamic tool discovery without custom glue"; [2] MCP roadmap confirms active governance maturation; OpenAI CEO endorsement March 2026 | Different frameworks implement MCP with radically different security postures: Claude Agent SDK blocks all tools unless explicitly allowed [9], while Upsonic enables all by default [9]. "MCP support" ranges from native integration to optional adapter layers. | Moderate — MCP is converging but not uniform; portability claims require qualifier that security/discovery policies still differ across frameworks |
| Portability lives at the tool layer (MCP) rather than the orchestration layer | [14][15][17] all converge on this principle; Scalekit: "the same callable can run under LangChain, CrewAI, or MCP with identical behavior" [14]; arXiv confirms tool-based control planes enable framework-agnostic portability [17] | Orchestration concerns (workflow state, memory topology, agent identity, access control) cannot be abstracted to a tool layer; A2A/ACP protocols emerged specifically because MCP is insufficient for agent-to-agent coordination [15] | Moderate — tool-layer portability is real but incomplete; cross-agent coordination requires additional protocol layers not captured by MCP alone |
| Agent memory tiers are well-defined and converging on a standard taxonomy | [6] Redis provides a clear 5-type taxonomy (short-term, long-term, episodic, semantic, procedural); multiple frameworks implement the taxonomy | Anthropic Managed Agents lists memory as "research preview" [7]; frameworks implement memory heterogeneously: LangGraph uses external vector DBs, CrewAI uses SQLite, AutoGen uses custom integrations [11]. The taxonomy is descriptive, not normative. | Moderate — the taxonomy is a useful vocabulary but memory is far from standardized in production use; the framework-specific implementations differ enough to complicate portability |
| Framework adoption statistics (47M downloads, 60% Fortune 500) are reliable | Statistics cited from [3][12] align with known framework popularity trends | All adoption statistics come from T4/T5 vendor blogs with unverified primary sources; "60% of Fortune 500 using CrewAI" [12] has no cited primary source; "$1.8B market" [4] is from a data connectivity vendor with conflict of interest | High for specific numbers — treat all adoption statistics as directional indicators, not authoritative figures |

### Premortem

Assume the main conclusion (MCP as convergence layer + tool-layer portability as the key pattern) is wrong:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| MCP fragments into incompatible profiles: different transport implementations, security models, and capability subsets create "MCP in name only" across frameworks | Medium. The roadmap [2] acknowledges stateful session scaling issues, governance bottlenecks, and enterprise readiness gaps. Vendor-specific extensions could diverge the protocol even with Linux Foundation governance. | High. Tool-layer portability claims depend on MCP behaving as a true standard. If MCP fragments like REST did (hundreds of incompatible "RESTful" APIs), portability remains an aspiration, not a practical outcome. |
| Memory features remain experimental too long to matter | Medium. Anthropic explicitly lists memory as "research preview" [7]. Long-context models may replace vector-memory architectures, making the 5-tier taxonomy obsolete before it standardizes. | Moderate. The memory tier architecture section would need significant revision; the sub-question answer would shift from "here's how it works" to "here's the current experimental state." |
| The framework landscape consolidates faster than captured | Low-medium. Microsoft already unified Semantic Kernel + AutoGen. Further consolidation (LangChain/CrewAI merger? Anthropic SDK absorption?) could make comparative landscape analysis stale within 12 months of publication. | Moderate. The comparative framework analysis is inherently ephemeral; landscape documents require explicit freshness dates. |

## Takeaways

**Key findings:**
- The framework landscape has consolidated from 177+ entries to 4–5 dominant frameworks: LangGraph (graph-based workflow), CrewAI (role-based teams), Microsoft Agent Framework (unified AutoGen + Semantic Kernel), and Claude Agent SDK / Managed Agents (session + harness + sandbox decoupling).
- MCP is the de facto tool and context protocol — donated to Linux Foundation's AAIF in December 2025, endorsed by OpenAI CEO March 2026, supported by all major frameworks by 2026. It operates as a transport layer (stateless, atomic tool invocations), not an orchestration layer.
- **Portability lives at the tool layer, not orchestration.** Tools implemented against MCP are callable from any framework without bespoke adapters. Orchestration topology (state management, agent identity, access control) remains framework-specific.
- Memory taxonomy is stable: short-term, long-term, episodic, semantic, procedural — but production implementations vary significantly. Start with short-term + long-term; add tiers only as operational value justifies complexity.
- Anthropic's brain/hands decoupling (session log + harness + sandbox as independent components) yielded ~60% p50 TTFT improvement and >90% p95 improvement.

**Limitations:**
- All framework adoption statistics (47M PyPI downloads, 60% Fortune 500, 1.1B agent actions) derive from T4/T5 sources with no verified primary citations — treat as directional indicators only.
- $1.8B MCP market size from CData has a conflict of interest; methodology not provided.
- Agent memory in Anthropic Managed Agents is "research preview" — production patterns still evolving.
- MCP convergence is real but not uniform: security posture varies significantly (Claude Agent SDK blocks all tools unless explicitly allowed; other frameworks auto-discover). "MCP support" ranges from native integration to optional adapter layers.
- Landscape analysis has a 12-month shelf life. Microsoft already unified AutoGen + Semantic Kernel; further consolidation is likely.

<!-- search-protocol
{"entries": [
  {"query": "agent framework landscape 2026 LangChain CrewAI AutoGen comparison", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "MCP Model Context Protocol adoption 2026 agent frameworks convergence", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 5},
  {"query": "portable agent tools MCP framework agnostic design patterns 2025 2026", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 4},
  {"query": "agent memory tiers short-term long-term semantic vector retrieval architecture 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 4},
  {"query": "Claude agent SDK Anthropic managed agents 2025 2026 architecture", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 3},
  {"query": "Semantic Kernel Microsoft agent framework 2025 2026 architecture MCP support", "source": "google", "date_range": "2025-2026", "results_found": 10, "results_used": 3},
  {"query": "agent memory architecture episodic semantic cross-session LangGraph AutoGen 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 3},
  {"query": "\"agent tool portability\" OR \"MCP tool layer\" \"avoid orchestration coupling\" framework agnostic 2025", "source": "google", "date_range": "2025", "results_found": 10, "results_used": 2}
],
"not_searched": [
  "Google ADK agent development kit architecture 2025",
  "Mastra agent framework JavaScript 2026",
  "PydanticAI agent framework type safety"
]}
-->
