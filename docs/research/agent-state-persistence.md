---
name: "Agent State Persistence"
description: "Architectural patterns for maintaining agent context across sessions — disk-as-truth, checkpoint-based resumption, memory taxonomies, and persistence substrate tradeoffs"
metadata:
  type: research
  sources:
    - https://arxiv.org/abs/2512.13564
    - https://arxiv.org/abs/2404.13501
    - https://arxiv.org/abs/2310.08560
    - https://arxiv.org/abs/2502.12110
    - https://arxiv.org/abs/2501.13956
    - https://arxiv.org/abs/2504.19413
    - https://arxiv.org/abs/2512.05470
    - https://arxiv.org/html/2602.20478v1
    - https://docs.langchain.com/oss/python/langgraph/persistence
    - https://code.claude.com/docs/en/memory
    - https://openai.github.io/openai-agents-python/sessions/
    - https://earezki.com/ai-news/2026-03-09-the-state-management-pattern-that-runs-our-5-agent-system-24-7/
    - https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2
    - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
    - https://blogs.oracle.com/developers/comparing-file-systems-and-databases-for-effective-ai-agent-memory-management
    - https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp
    - https://dl.acm.org/doi/10.1145/3748302
    - https://docs.letta.com/concepts/memgpt/
  related:
    - docs/research/context-window-management.md
    - docs/context/agent-state-persistence.md
---

## Key Findings

Agent state persistence is the problem of carrying knowledge, decisions, and progress across session boundaries where each new conversation starts with a blank context window. Three architectural families have emerged: file-based persistence (disk-as-truth), checkpoint-based resumption (graph state snapshots), and memory-layer services (structured extraction into databases or knowledge graphs). The choice between them depends on whether agents need human-readable audit trails, fault-tolerant workflow resumption, or semantic retrieval over accumulated experience.

**Bottom line:** File-based persistence is the simplest and most debuggable approach, sufficient for single-agent developer tools. Checkpoint-based persistence suits stateful multi-step workflows that must survive crashes. Database-backed memory layers become necessary when agents need semantic retrieval, temporal reasoning, or multi-user concurrency. Production systems increasingly combine all three.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2512.13564 | Memory in the Age of AI Agents: A Survey | Yuyang Hu et al. | 2025-12 | T1 | verified |
| 2 | https://arxiv.org/abs/2404.13501 | A Survey on the Memory Mechanism of LLM-based Agents | Zeyu Zhang et al. / ACM TOIS | 2024-04 | T1 | verified |
| 3 | https://arxiv.org/abs/2310.08560 | MemGPT: Towards LLMs as Operating Systems | Charles Packer et al. / UC Berkeley | 2023-10 | T1 | verified |
| 4 | https://arxiv.org/abs/2502.12110 | A-MEM: Agentic Memory for LLM Agents | Wujiang Xu et al. / NeurIPS 2025 | 2025-02 | T1 | verified |
| 5 | https://arxiv.org/abs/2501.13956 | Zep: Temporal Knowledge Graph Architecture for Agent Memory | Preston Rasmussen et al. / Zep AI | 2025-01 | T2 | verified |
| 6 | https://arxiv.org/abs/2504.19413 | Mem0: Production-Ready AI Agents with Scalable Long-Term Memory | Prateek Chhikara et al. | 2025-04 | T2 | verified |
| 7 | https://arxiv.org/abs/2512.05470 | Everything is Context: Agentic File System Abstraction | Xiwei Xu et al. | 2025-12 | T2 | verified |
| 8 | https://arxiv.org/html/2602.20478v1 | Codified Context: Infrastructure for AI Agents in a Complex Codebase | Aristidis Vasilopoulos | 2026-02 | T2 | verified |
| 9 | https://docs.langchain.com/oss/python/langgraph/persistence | Persistence — LangGraph Documentation | LangChain | 2025 | T2 | verified |
| 10 | https://code.claude.com/docs/en/memory | How Claude Remembers Your Project | Anthropic | 2026 | T2 | verified |
| 11 | https://openai.github.io/openai-agents-python/sessions/ | Sessions — OpenAI Agents SDK | OpenAI | 2025 | T2 | verified |
| 12 | https://earezki.com/ai-news/2026-03-09-the-state-management-pattern-that-runs-our-5-agent-system-24-7/ | Three-File State Management Pattern | Dev Journal | 2026-03 | T4 | verified |
| 13 | https://engineering.atspotify.com/2025/11/context-engineering-background-coding-agents-part-2 | Context Engineering for Background Coding Agents | Spotify Engineering | 2025-11 | T2 | verified |
| 14 | https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Effective Harnesses for Long-Running Agents | Anthropic Engineering | 2025 | T2 | verified |
| 15 | https://blogs.oracle.com/developers/comparing-file-systems-and-databases-for-effective-ai-agent-memory-management | Comparing File Systems and Databases for Agent Memory | Oracle / Richmond Alake | 2026-02 | T3 | verified (403) |
| 16 | https://dev.to/foxgem/ai-agent-memory-a-comparative-analysis-of-langgraph-crewai-and-autogen-31dp | AI Agent Memory: Comparative Analysis | foxgem / DEV Community | 2025 | T4 | verified |
| 17 | https://dl.acm.org/doi/10.1145/3748302 | Survey on Memory Mechanism of LLM-based Agents (ACM version) | Zeyu Zhang et al. / ACM | 2024 | T1 | verified (403) |
| 18 | https://docs.letta.com/concepts/memgpt/ | Intro to Letta / MemGPT Concepts | Letta | 2025 | T2 | verified |

## Search Protocol

| # | Query | Engine | Results Used |
|---|-------|--------|-------------|
| 1 | LLM agent state persistence patterns disk-as-truth checkpoint resumption 2025 2026 | WebSearch | [1], [9], [12] |
| 2 | LLM agent memory systems short-term long-term episodic semantic architecture survey 2024 2025 | WebSearch | [1], [2], [4], [6] |
| 3 | LangGraph agent state persistence checkpointing documentation 2025 | WebSearch | [9] |
| 4 | Claude Code agent session persistence memory file-based context 2025 2026 | WebSearch | [8], [10] |
| 5 | AutoGen CrewAI agent state persistence memory architecture comparison 2025 | WebSearch | [16] |
| 6 | arxiv "agent memory" survey LLM persistence architecture 2024 2025 | WebSearch | [1], [2], [4], [6] |
| 7 | conversation-based vs file-based vs database persistence LLM agents tradeoffs 2025 | WebSearch | [7], [15] |
| 8 | MemGPT Letta agent memory operating system virtual context management 2024 2025 | WebSearch | [3], [18] |
| 9 | OpenAI Agents SDK state persistence memory tool conversation history 2025 2026 | WebSearch | [11] |
| 10 | "disk as truth" pattern agent context file-based state management 2025 | WebSearch | [7], [8], [12], [13], [14] |
| 11 | Zep temporal knowledge graph agent memory architecture 2025 | WebSearch | [5] |
| 12 | Mem0 production agent long-term memory architecture scalable 2025 | WebSearch | [6] |

## Findings

### What are the core architectural patterns for agent state persistence?

Three dominant patterns have emerged for persisting agent state across sessions, each with distinct guarantees and failure modes.

**Disk-as-truth (file-based persistence).** The simplest pattern: agents read state from files at session start and write state back to files during or after execution. The filesystem serves as the single source of truth. Claude Code exemplifies this — each session starts with a fresh context window, and two mechanisms carry knowledge forward: CLAUDE.md files (human-authored persistent instructions) and auto memory (notes Claude writes to `~/.claude/projects/<project>/memory/`) [10]. The "three-file pattern" described by Rezki (2026) formalizes this: `current-task.json` (immediate state), `memory/today.md` (session log), and `MEMORY.md` (standing rules), with agents reading all three at loop start and writing updates during execution [12]. Vasilopoulos (2026) demonstrated this at scale across 283 development sessions producing a 108,000-line system, using a three-tier architecture: a ~660-line "constitution" document loaded every session (hot memory), 19 specialized agent specifications (~9,300 lines), and 34 on-demand specification documents (~16,250 lines) as cold memory [8].

The file-system abstraction pattern proposed by Xu et al. (2025) generalizes this further, treating all context artifacts — knowledge, memory, tools, human inputs — as files in a Unix-inspired mount/metadata/access-control framework [7]. This aligns with a practical observation: LLMs already know how to read and write files, making file-based persistence a zero-friction interface (HIGH — T1 + T2 + T4 sources converge on this point).

**Checkpoint-based resumption (graph state snapshots).** Stateful workflow frameworks like LangGraph save the full execution graph state at each step, enabling resumption from any checkpoint after crashes or interruptions. LangGraph's persistence layer compiles graphs with a checkpointer that saves a snapshot at every step, organized into threads identified by unique IDs [9]. Key capabilities include fault tolerance (if a node fails mid-execution, completed nodes are not re-run on resumption), durable execution (workflows can pause for human-in-the-loop approval and resume after arbitrary delays), and time travel debugging (replaying execution from any historical checkpoint). Multiple storage backends are supported: in-memory, SQLite, Redis, Couchbase, and custom implementations using a common serialization protocol (JsonPlusSerializer with ormsgpack) [9] (HIGH — T2 official documentation).

**Memory-layer services (structured extraction into databases/graphs).** Purpose-built memory services extract, consolidate, and index information from conversations into structured stores that support semantic retrieval. MemGPT/Letta pioneered this with an OS-inspired memory hierarchy: main context (fast, limited, within the context window), recall storage (intermediate), and archival storage (slow, unlimited) [3]. The agent manages its own memory through function calls, moving data between tiers autonomously. More recent systems like Zep use temporal knowledge graphs with bi-temporal tracking (when events occurred and when they were ingested) [5], while Mem0 extracts memories into both flat stores and directed labeled graphs [6] (HIGH — T1 + T2 sources converge).

### How do memory systems categorize and manage agent state?

The academic literature identifies a consistent taxonomy of memory types, drawing from cognitive science analogies.

**Functional taxonomy (Hu et al., 2025).** The most comprehensive recent survey proposes three memory functions: factual memory (storage of knowledge and information), experiential memory (recording of interactions and outcomes), and working memory (temporary processing of current task information). Orthogonally, it identifies three memory forms: token-level (direct manipulation of tokens in context), parametric (knowledge stored in model weights), and latent (hidden representations in vector spaces) [1]. Memory dynamics are analyzed across three temporal aspects: formation (capture and encoding), evolution (transformation over time), and retrieval (access and utilization) (HIGH — T1 survey with 47 authors).

**Cognitive-inspired taxonomy (Zhang et al., 2024).** The earlier ACM TOIS survey organizes memory by cognitive analogy: short-term memory (in-task working memory within the context window), and long-term memory subdivided into episodic (specific interaction records), semantic (general knowledge and facts), and procedural (learned behavioral patterns) [2]. This maps closely to how production frameworks implement memory:

- **Short-term / Working memory:** Conversation history within a single session. All frameworks provide this by default through the context window itself. OpenAI's Agents SDK sessions and LangGraph thread state are implementations of this [9][11].
- **Long-term / Episodic memory:** Records of past interactions, retrievable by recency, importance, and relevance. CrewAI stores these in SQLite and ChromaDB vector stores [16]. A-MEM enriches each memory unit with LLM-generated keywords, tags, and contextual descriptions in a Zettelkasten-inspired structure [4].
- **Long-term / Semantic memory:** Consolidated knowledge extracted from experience. Zep's temporal knowledge graph with three-tier subgraphs (episode, semantic entity, community) represents this most explicitly [5]. Mem0's graph-enhanced variant stores memories as directed labeled graphs with entities as nodes and relationships as edges [6].
- **Long-term / Procedural memory:** Learned rules and patterns. Claude Code's CLAUDE.md files function as human-authored procedural memory, while auto memory captures discovered patterns [10].

A 2026 evolutionary framework (Preprints.org) formalizes development into three stages: Storage (trajectory preservation), Reflection (trajectory refinement), and Experience (trajectory abstraction), tracking how the field has progressed from simple logging to sophisticated consolidation (MODERATE — T3 preprint, not yet peer-reviewed).

### What are the tradeoffs between conversation-based, file-based, and database-backed persistence?

The persistence substrate choice involves fundamental tradeoffs across transparency, scalability, retrieval capability, and operational complexity.

**Conversation-based persistence** treats the conversation history itself as memory. Each turn appends to a growing context that the model can reference. This is the default in most LLM interactions. AutoGen exemplifies this approach, maintaining a centralized transcript as short-term memory and pruning aggressively as token limits approach [16]. **Advantages:** Zero implementation cost, natural temporal ordering, complete fidelity to what was said. **Disadvantages:** Bounded by context window limits, no semantic retrieval, no cross-session persistence, linear scaling costs. When conversations end, state is lost unless explicitly externalized (MODERATE — T4 source, corroborated by T1 survey findings).

**File-based persistence** writes state to human-readable files on disk. Claude Code's dual system (CLAUDE.md + auto memory in `~/.claude/projects/`) demonstrates the pattern at its most refined: instructions are loaded at session start, auto memory is capped at 200 lines for the index file, and topic files are read on demand [10]. The Oracle developer blog comparison found that file systems win as an interface (LLMs already know how to use them) while databases win as a substrate for concurrent, semantically-rich workloads [15]. **Advantages:** Human-readable, debuggable with standard tools, version-controllable with git, zero infrastructure, natural fit for LLM tool use. **Disadvantages:** No concurrent-write safety, no semantic search, no structured queries, manual organization burden. The practical ceiling: "a folder of markdown gets you surprisingly far when iteration speed matters most" [15] (HIGH — T2 + T3 sources converge).

**Database-backed persistence** stores state in structured databases — relational (SQLite, PostgreSQL), vector stores (ChromaDB, Pinecone), knowledge graphs (Neo4j), or purpose-built memory services (Mem0, Zep). LangGraph supports multiple checkpoint backends through a common interface [9]. CrewAI uses SQLite for long-term task memory and ChromaDB for semantic entity memory [16]. Mem0 achieves 26% accuracy improvements over OpenAI baselines with 91% lower latency and 90% token savings through structured extraction [6]. Zep's temporal knowledge graph achieves 18.5% accuracy improvements on long-memory benchmarks with 90% latency reduction versus baseline [5]. **Advantages:** Concurrent access, ACID transactions, semantic retrieval, structured queries, scalable to multi-agent and multi-user scenarios. **Disadvantages:** Infrastructure overhead, serialization complexity, opaque to human inspection, harder to debug (HIGH — T1 + T2 sources converge).

**Emerging consensus:** Production systems combine substrates. File-based for human-readable configuration and audit trails, database-backed for semantic retrieval and concurrent state, checkpoint-based for workflow resumption. The "three-file pattern" [12] uses files as the agent's interface while production backends can swap in databases underneath (MODERATE — emerging pattern, limited peer-reviewed evidence).

### How do production agent frameworks implement state persistence?

Framework implementations reveal distinct architectural philosophies toward persistence.

**LangGraph (LangChain):** Persistence is a first-class architectural concept. Every graph compilation accepts a checkpointer. State is saved at every super-step as a checkpoint identified by a monotonically increasing ID, organized into threads. When a node fails, completed nodes' writes are preserved. Supports in-memory, SQLite, Redis, Couchbase, and custom backends. Durable execution enables human-in-the-loop workflows with arbitrary pause durations. Serialization uses JsonPlusSerializer with ormsgpack fallback [9] (HIGH — T2 official documentation).

**Claude Code (Anthropic):** Purely file-based. CLAUDE.md files at project/user/org scopes provide persistent instructions loaded at every session start. Auto memory in `~/.claude/projects/<project>/memory/` captures learnings automatically — Claude decides what to save based on future utility. The MEMORY.md index (first 200 lines loaded at startup) links to topic files read on demand. All worktrees within the same git repository share one memory directory. Files survive conversation compaction because they are re-read from disk [10] (HIGH — T2 official documentation).

**OpenAI Agents SDK:** Session-based persistence with pluggable backends. The session object handles context length, history, and continuity. Storage options include SQLiteSession (in-memory or persistent file), RedisSession (distributed), SQLAlchemySession (any SQL database), and DaprSession (portable state stores). The Conversations API creates durable conversation objects usable across sessions, devices, and jobs [11] (HIGH — T2 official documentation).

**CrewAI:** Multi-store memory architecture. Short-term memory in ChromaDB vector store, recent task results in SQLite, long-term memory in separate SQLite tables indexed by task description, entity memory using vector embeddings for tracking and reasoning about entities. Task-level error boundaries enable reassignment without full crew restart [16] (MODERATE — T4 community source).

**AutoGen:** Minimal built-in persistence. Conversation transcript serves as short-term memory with aggressive token-limit pruning. A centralized `context_variables` object stores interaction history. No built-in persistent memory — external stores must be added manually. Error handling relies on conversational retries rather than checkpoint-based recovery [16] (MODERATE — T4 community source).

**MemGPT/Letta:** OS-inspired memory hierarchy with agent-managed tiering. Main context (within context window), recall storage (intermediate), archival storage (unlimited). The agent moves data between tiers through function calls, inspired by virtual memory management in operating systems. As of 2026, Letta introduced Context Repositories with git-based versioning for programmatic context management [3][18] (HIGH — T1 + T2 sources converge).

### What patterns exist for checkpoint annotations and session resumption?

Several concrete patterns enable agents to resume work across session boundaries.

**Checkpoint-as-snapshot (LangGraph).** Each checkpoint captures the full graph state: node outputs, pending writes, and execution position. Checkpoints are identified by monotonically increasing IDs within threads. Resumption restores exact state and skips completed nodes. Time travel debugging allows replaying from any historical checkpoint, transforming non-deterministic agent execution into inspectable state machines [9] (HIGH — T2).

**File-as-checkpoint (disk-as-truth tools).** The three-file pattern creates implicit checkpoints through structured file writes. `current-task.json` records what the agent is doing right now (enabling mid-task resumption), `memory/today.md` logs what happened in the current session (enabling handoff), and `MEMORY.md` captures standing rules that persist indefinitely [12]. Claude Code's auto memory similarly creates implicit checkpoints — notes saved mid-session are immediately available to future sessions [10] (MODERATE — T2 + T4 sources).

**Tiered context loading (hot/warm/cold).** Vasilopoulos (2026) demonstrated a three-tier approach across 283 production sessions: a constitution document always loaded (hot), specialized agent specs loaded when relevant (warm), and detailed documentation retrieved on demand (cold) [8]. Claude Code implements a similar pattern: CLAUDE.md files in the working directory tree always load, subdirectory files load on demand, and auto memory topic files are read only when needed [10] (HIGH — T2 sources converge).

**Memory consolidation (episodic to semantic).** Rather than preserving raw interaction logs, several systems consolidate experience into compressed representations. A-MEM creates Zettelkasten-inspired notes with generated keywords, tags, and contextual descriptions, dynamically linking to related memories [4]. Mem0 extracts salient information and consolidates it, with graph-enhanced variants capturing relational structure [6]. The consolidation pattern is identified by Hu et al. (2025) as "the primary mechanism of lifelong learning" for agents [1] (HIGH — T1 + T2 sources converge).

### What does the academic literature say about memory architectures for LLM-based agents?

The field has rapidly matured from ad-hoc conversation logging to formalized memory architectures.

**Survey landscape.** Two comprehensive surveys anchor the field. Hu et al. (2025) with 47 authors provides the most recent taxonomy, distinguishing agent memory from LLM memory, RAG, and context engineering, and arguing that memory should be treated as "a first-class primitive in the design of future agentic intelligence" [1]. Zhang et al. (2024), published in ACM TOIS, provides a systematic review of memory module design and evaluation [2]. Both identify the transition from simple storage to active memory management as the central trend.

**Key architectural innovations.** MemGPT (Packer et al., 2023) introduced the operating system analogy for agent memory, demonstrating that agents can manage their own context through function-call-based data movement between memory tiers [3]. A-MEM (Xu et al., 2025, NeurIPS) showed that Zettelkasten-inspired dynamic linking outperforms fixed-operation baselines across six foundation models [4]. Zep (Rasmussen et al., 2025) demonstrated that temporal knowledge graphs with bi-temporal tracking achieve 94.8% accuracy on deep memory retrieval (vs. 93.4% for MemGPT) with 90% latency reduction [5]. Mem0 (Chhikara et al., 2025) proved that structured extraction achieves 26% accuracy gains with 91% lower latency and 90% token savings versus full-context approaches [6].

**Emerging research directions.** The field is moving toward: memory automation (agents that manage their own memory lifecycle without human intervention), reinforcement learning integration (using memory effectiveness as reward signal), multimodal memory (capturing and retrieving non-text artifacts), multi-agent shared memory (blackboard-style architectures and iterative summarization), and trustworthy memory (verification, privacy, and consistency guarantees) [1] (HIGH — T1 survey).

**An ICLR 2026 workshop proposal (MemAgents)** further signals the field's maturation, focusing specifically on memory systems for agentic applications as a distinct research area from general LLM memory (MODERATE — workshop proposal, not yet held).

## Challenge

**Counter-evidence: File-based persistence has scaling limits.** While file-based persistence is praised for simplicity and debuggability, concurrent filesystem writes can silently corrupt data [15], and as memory accumulates, the lack of semantic retrieval means agents must either load everything (exceeding context limits) or have humans curate what loads. Claude Code addresses this partially with the 200-line MEMORY.md cap and on-demand topic files [10], but this is a manual workaround, not a structural solution.

**Counter-evidence: Checkpoint-based persistence has overhead costs.** LangGraph checkpointing adds serialization/deserialization overhead at every step. For simple workflows, this overhead exceeds the cost of re-execution. The JsonPlusSerializer must handle diverse types (LangChain objects, datetimes, enums), adding complexity. Not all state is serializable — function references, database connections, and external handles require special handling [9].

**Counter-evidence: Database-backed memory introduces opacity.** When memories are extracted and consolidated by an LLM, the extraction process itself is lossy and non-deterministic. Mem0's 26% accuracy improvement [6] is measured on specific benchmarks that may not generalize. Knowledge graphs can accumulate stale or contradictory edges. The Zep bi-temporal model mitigates staleness but adds implementation complexity [5].

**Counter-evidence: Memory taxonomies may be artificial.** The cognitive-science-inspired categories (episodic, semantic, procedural) may not map cleanly to engineering requirements. An agent that needs "what happened in my last session" (episodic) versus "what are the project coding standards" (procedural) may be better served by simple file-based patterns than by a system with formal memory-type distinctions. The practical value of formal taxonomies versus informal conventions remains an open question.

**Tension: Observation vs. action.** Disk-as-truth patterns treat files as ground truth, but file-based memory is only as good as the agent's write discipline. If agents fail to externalize state before a crash (or between tool calls), context is lost regardless of the persistence substrate. Checkpoint-based systems handle this structurally by saving at every step, but at a performance cost.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | MemGPT introduced the OS-inspired memory hierarchy for LLM agents | attribution | [3] | verified — Packer et al. 2023 is the originating paper |
| 2 | Zep achieves 94.8% accuracy on Deep Memory Retrieval benchmark vs. 93.4% for MemGPT | statistic | [5] | verified — matches arXiv abstract |
| 3 | Zep achieves accuracy improvements of up to 18.5% on LongMemEval with 90% latency reduction | statistic | [5] | verified — matches arXiv abstract |
| 4 | Mem0 achieves 26% relative improvement in LLM-as-a-Judge metric over OpenAI | statistic | [6] | verified — matches arXiv abstract |
| 5 | Mem0 achieves 91% lower p95 latency and 90% token savings | statistic | [6] | verified — matches arXiv abstract |
| 6 | Vasilopoulos (2026) demonstrated the three-tier pattern across 283 sessions producing 108,000 lines | statistic | [8] | verified — matches arXiv paper |
| 7 | A-MEM was accepted to NeurIPS 2025 | attribution | [4] | verified — stated in arXiv metadata |
| 8 | Claude Code auto memory loads first 200 lines of MEMORY.md at session start | statistic | [10] | verified — matches official docs |
| 9 | The Hu et al. survey had 47 authors | statistic | [1] | verified — "Yuyang Hu et al." with 47 total authors listed |
| 10 | CrewAI uses SQLite for long-term memory and ChromaDB for short-term vector memory | attribution | [16] | verified — matches DEV Community comparative analysis |
| 11 | LangGraph checkpoint IDs are monotonically increasing | attribution | [9] | verified — matches official documentation |

## Takeaways

Three persistence substrates serve different needs: files for transparency and debuggability, checkpoints for fault-tolerant workflow resumption, databases for semantic retrieval and scale. The field is converging on hybrid architectures that combine all three. For developer-facing agent tools like Claude Code and WOS, file-based persistence with structured conventions (frontmatter, indexes, tiered loading) provides the best balance of simplicity, transparency, and agent compatibility. The academic literature strongly supports treating memory as a first-class architectural primitive rather than an afterthought, with the most effective systems implementing active memory management (agents that curate their own memory) rather than passive logging.
