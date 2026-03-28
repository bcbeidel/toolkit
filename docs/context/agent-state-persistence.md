---
name: "Agent State Persistence"
description: "Architectural patterns for carrying agent knowledge across session boundaries: file-based, checkpoint-based, and database-backed persistence with tradeoffs"
metadata:
  type: reference
  sources:
    - https://arxiv.org/abs/2512.13564
    - https://arxiv.org/abs/2404.13501
    - https://arxiv.org/abs/2310.08560
    - https://arxiv.org/abs/2502.12110
    - https://docs.langchain.com/oss/python/langgraph/persistence
    - https://code.claude.com/docs/en/memory
    - https://arxiv.org/html/2602.20478v1
  related:
    - docs/research/agent-state-persistence.md
    - docs/context/context-window-management.md
---

Each new agent session starts with a blank context window. State persistence solves the problem of carrying knowledge, decisions, and progress across that boundary. Three architectural families dominate, each optimized for different constraints.

## Three Persistence Architectures

**File-based (disk-as-truth).** Agents read state from files at session start and write updates during execution. The filesystem is the single source of truth. Claude Code uses this pattern: CLAUDE.md files provide persistent instructions, and auto memory (`~/.claude/projects/<project>/memory/`) captures learned knowledge with a 200-line index loaded at startup and topic files read on demand. The "three-file pattern" formalizes this with a current-task file (immediate state), session log (what happened), and standing rules (persistent memory). A large-scale case study demonstrated this across 283 sessions producing 108,000 lines of code using tiered loading: a constitution document always loaded, specialized specs loaded when relevant, and detailed docs retrieved on demand.

**Advantages:** Human-readable, git-versionable, debuggable with standard tools, zero infrastructure, natural fit for LLM tool use. **Limits:** No concurrent-write safety, no semantic search, manual organization burden. Scales well for single-agent developer tools but hits ceilings with multi-agent concurrency.

**Checkpoint-based (graph state snapshots).** Workflow frameworks like LangGraph save full execution state at each step. Checkpoints enable fault-tolerant resumption (completed nodes are not re-run), human-in-the-loop pauses with arbitrary delays, and time-travel debugging by replaying from any historical state. Multiple storage backends are supported through a common serialization interface.

**Advantages:** Structural crash recovery, inspectable execution history. **Limits:** Serialization overhead at every step, not all state is serializable (function references, external handles), overkill for simple workflows.

**Database-backed (structured extraction).** Purpose-built memory services extract and index information from conversations into structured stores supporting semantic retrieval. MemGPT introduced an OS-inspired memory hierarchy where agents manage their own context through function calls across memory tiers. Zep uses temporal knowledge graphs with bi-temporal tracking. Mem0 extracts memories into flat stores and directed labeled graphs, achieving 26% accuracy gains with 91% lower latency versus full-context approaches.

**Advantages:** Concurrent access, ACID transactions, semantic retrieval, scalable to multi-agent scenarios. **Limits:** Infrastructure overhead, opaque to human inspection, extraction process is lossy and non-deterministic.

## Memory Taxonomy

Academic surveys identify consistent memory categories mapped from cognitive science: **short-term/working memory** (conversation history within a session, provided by the context window itself), **episodic memory** (records of past interactions, retrievable by recency and relevance), **semantic memory** (consolidated knowledge extracted from experience), and **procedural memory** (learned rules and behavioral patterns -- CLAUDE.md files are a form of human-authored procedural memory).

## Session Resumption Patterns

Four patterns enable cross-session continuity: checkpoint-as-snapshot (full state capture at every step), file-as-checkpoint (structured file writes create implicit checkpoints), tiered context loading (hot/warm/cold memory with selective loading), and memory consolidation (compressing raw logs into structured knowledge, identified as the primary mechanism for agent lifelong learning).

## Practical Guidance

Production systems increasingly combine substrates: files for human-readable configuration and audit trails, databases for semantic retrieval and concurrency, checkpoints for workflow resumption. For developer-facing agent tools, file-based persistence with structured conventions (frontmatter, indexes, tiered loading) provides the best balance of simplicity, transparency, and agent compatibility. The academic consensus treats memory as a first-class architectural primitive -- the most effective systems implement active memory management where agents curate their own memory rather than passively logging interactions.
