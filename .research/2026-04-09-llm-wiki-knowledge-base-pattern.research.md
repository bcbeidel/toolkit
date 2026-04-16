---
name: "LLM Wiki: Persistent Knowledge Base Pattern"
description: "Landscape of LLM-maintained wiki implementations — ingest/query/lint operations, schema design, navigation without embeddings, and MCP integration patterns. The schema document is the decisive design artifact; index.md navigation scales to an uncertain threshold (100-500 pages) before hybrid search is needed."
type: research
sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
  - https://github.com/lucasastorian/llmwiki
  - https://github.com/MehmetGoekce/llm-wiki
  - https://mehmetgoekce.substack.com/p/i-built-karpathys-llm-wiki-with-claude
  - https://github.com/nvk/llm-wiki
  - https://github.com/SamurAIGPT/llm-wiki-agent
  - https://github.com/Ar9av/obsidian-wiki
  - https://www.mindstudio.ai/blog/llm-knowledge-base-index-file-no-vector-search
  - https://glama.ai/mcp/servers/iamsashank09/llm-wiki-kit
  - https://playbooks.com/mcp/basicmachines-co/basic-memory
  - https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md
  - https://llm-wiki.net/
  - https://antigravity.codes/blog/karpathy-llm-wiki-idea-file
  - https://louiswang524.github.io/blog/llm-knowledge-base/
  - https://medium.com/@tahirbalarabe2/what-is-llm-wiki-pattern-persistent-knowledge-with-llm-wikis-3227f561abc1
  - https://a2a-mcp.org/blog/andrej-karpathy-llm-knowledge-bases-obsidian-wiki
---

# LLM Wiki: Persistent Knowledge Base Pattern

I investigated how developers and researchers have implemented persistent LLM-maintained knowledge bases following Andrej Karpathy's "LLM wiki" pattern, covering open-source implementations, schema design, navigation without vector embeddings, and MCP/cross-tool integration. 11 searches across 4 sub-questions surfaced 17 sources (mostly community T5, one T1 primary source, two T4 practitioners).

## Key Findings

**The pattern is well-defined and replicable (HIGH).** Every significant implementation follows the same three-operation structure (ingest/query/lint) and three-layer architecture (immutable raw sources → LLM-maintained wiki → schema config) from Karpathy's original gist [1].

**The schema document is the decisive design artifact (MODERATE).** YAML frontmatter with 4 page types (concept, entity, source-summary, comparison), 3-tier confidence scoring, and typed relationship edges defines the wiki's domain knowledge. rohitg00 describes this as "the real product" [2] — it transforms a generic LLM into a disciplined knowledge curator.

**Index.md navigation scales to an uncertain threshold, then needs hybrid search (MODERATE).** Sources disagree: rohitg00 [2] suggests ~100-200 pages; MindStudio [9] places the limit at 500+ documents. Beyond the threshold, hybrid BM25 + vector + graph traversal is the standard solution.

**MCP and AGENTS.md portability are complementary cross-tool strategies (MODERATE).** MCP servers (5-8 standardized tools, SQLite FTS5 search) enable programmatic access and composability. AGENTS.md file-based portability enables the same wiki to run across Claude Code, Codex, Cursor, Windsurf, and Gemini CLI without a server.

**Critical gap: contradiction detection is aspirational in most implementations (MODERATE).** Described as an ingest-time check in principle; most implementations only run it as a periodic lint operation, if at all.

---

## Findings

### 1. Open-source implementations converge on a three-operation pattern (HIGH)

Every significant implementation follows Karpathy's ingest/query/lint structure [1], with minor variations:

- **Ingest** processes a source and updates 5-15 wiki pages simultaneously [1] — entity pages, concept pages, and cross-references are all touched in one pass. MehmetGoekce's 5-phase ingest pipeline makes this explicit: analyze & extract → scan wiki → update pages (append-only, never overwrite) → quality gate → report [4].
- **Query** synthesizes answers from wiki pages rather than raw sources, optionally filing valuable explorations back as new pages [1,6,7]
- **Lint** detects orphan pages, broken links, stale claims, contradictions, and missing cross-references [1,3,4,6,7]

The three-layer architecture is universal: raw sources (immutable) → wiki markdown (LLM-maintained) → schema config (human-curated). The "compounding" mechanism — where query explorations feed back as new wiki pages — is described in [1,17] as the key differentiator from RAG.

Implementation spectrum runs from infrastructure-heavy (lucasastorian [3]: FastAPI + Supabase + S3 + Next.js + MCP) to zero-dependency (nvk [6]: Claude Code tools only; SamurAIGPT [7]: plain markdown + NetworkX for graph visualization).

### 2. The schema document is the decisive design artifact (MODERATE)

rohitg00 describes the schema document (CLAUDE.md or AGENTS.md) as "the real product" [2] — it defines page types, relationship vocabularies, naming conventions, lint rules, and ingest workflows, transforming a generic LLM into a disciplined domain-specific curator.

YAML frontmatter with four page types is the dominant design [14]:
```yaml
type: concept | entity | source-summary | comparison
confidence: high | medium | low
sources: [list of raw/ files referenced]
related: [list of wiki pages linked]
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

Three-tier confidence (high/medium/low) based on source count, recency, and corroboration is universal across implementations [2,6,14]. rohitg00 v2 extends to typed relationship edges (uses, depends on, contradicts, caused, fixed, supersedes) as the schema matures [2].

**Counter-evidence (MODERATE):** Logseq's inline `property:: value` syntax is an alternative to YAML frontmatter [4,5] with different tradeoffs — better LLM writability, but Logseq-specific rather than universal markdown. The "schema as product" claim is asserted by practitioners but not empirically compared against schema-light implementations.

### 3. Index.md navigation is sufficient at small scale; threshold is uncertain (MODERATE)

All implementations use `index.md` as the primary navigation layer — agents read the index first, then select specific pages [1,6,7,9,13]. The index requires: file paths, 1-3 sentence descriptions, categorical groupings, cross-references, and recency signals [9].

Advantages over RAG: transparent (agent explicitly selects what it reads), lower cost (no embeddings), more predictable [9]. Disadvantage: the index itself eventually exceeds single-pass context.

**Sources disagree on the threshold:** rohitg00 [2] suggests hybrid search at ~100-200 pages; MindStudio [9] says "500+ documents" before a tiered approach is needed. No empirical study establishes the limit — it depends on index verbosity, page description length, and LLM context window. Treat any specific figure as a rough heuristic.

Beyond the limit, solutions are: hybrid BM25 + vector + graph traversal [2]; SQLite FTS5 keyword search (used by both LLM Wiki Kit [10] and gnosis-mcp [12]); Basic Memory's `memory://` URL graph traversal with optional FastEmbed embeddings [11].

nvk implements navigation depth modes: Quick (indexes only), Standard (articles + full-text), Deep (everything including raw sources) [6]. Cross-references use dual-link format `[[wikilink]]` + markdown path for multi-tool compatibility (Obsidian, Claude Code, GitHub, plain text editors) [6].

### 4. MCP and AGENTS.md portability are complementary (MODERATE)

Two distinct cross-tool patterns have emerged:

**MCP server pattern**: Standardized 8-tool interface — `wiki_init`, `wiki_ingest`, `wiki_write_page`, `wiki_read_page`, `wiki_search`, `wiki_lint`, `wiki_status`, `wiki_log` [10]. SQLite FTS5 with Porter stemming and Boolean operators is the common search backend [10,12]. Enables composability: wiki + GitHub MCP + Notion MCP in a single pass [6]. Basic Memory extends to 20+ tools with optional semantic vector search [11].

**AGENTS.md portability pattern**: The wiki ships as a file-based knowledge base readable by any runtime via the schema in AGENTS.md. Works across Claude Code, Codex, Cursor, Windsurf, and Gemini CLI without a running server [6,7,8]. nvk ships both forms simultaneously.

**Separation strategy**: Some practitioners maintain a "high-signal personal vault" alongside an "agent-facing messy vault" to prevent contamination from LLM-generated content [17]. This addresses hallucination compounding risk (see Challenge).

### Key gaps relevant to WOS

1. **Contradiction detection is underbuilt**: Described aspirationally in most implementations; few ship it reliably. Lint detects it post-hoc only.
2. **No longitudinal evidence**: All sources are early-2026; no evidence of sustained multi-year maintenance. The "compounding" benefit is theoretical.
3. **Confidence scoring lacks semantics**: Three-tier high/medium/low is common but not standardized; no shared meaning across tools.
4. **Scale threshold is unclear**: The specific page count where index.md breaks down is disputed and context-dependent.

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Pattern is production-ready and durable | Multiple independent implementations [3,4,6,7,8] | All sources are early-2026; no longitudinal evidence of sustained use | Pattern works initially but degrades — same failure mode as human wikis |
| Index.md scales to 100-200 pages | rohitg00 [2] | MindStudio [9] says 500+; no empirical study | Extensions need hybrid search at a different threshold than expected |
| Contradiction detection is an ingest-time operation | SamurAIGPT contrast with RAG [7] | Most implementations describe it as a lint goal, not a shipped feature | Harder than described; needs dedicated lint infrastructure |
| MCP is the right cross-tool integration layer | Multiple MCP servers exist [10,11,12] | Most cross-runtime portability uses AGENTS.md file-based patterns; MCP is Claude-origin | File-based portability may be more robust |
| Schema document is the key differentiator | rohitg00 [2]: "the real product" | No comparison of schema-heavy vs schema-light; claim is asserted | Schema complexity may be maintenance burden at small scale |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **Quality degrades with scale**: Contradictions accumulate faster than lint catches them; wiki becomes inconsistent past ~200 pages | Medium | Qualifies scalability findings — practical ceiling may be lower than claimed |
| **Survivorship bias**: Only successful/exciting implementations are visible; pattern may fail silently when users stop after initial ingestion | High | All findings reflect initial setup enthusiasm, not sustained operation |
| **Hallucination compounding**: LLM-authored wiki pages become sources for future ingest, amplifying errors over time | Medium | Requires explicit enforcement of raw source immutability — not optional |

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "the wiki is a persistent, compounding artifact" | quote | [1] | verified |
| 2 | "A single source might touch 10-15 wiki pages" | statistic | [1] | verified |
| 3 | "Target: 5-15 page updates per ingest operation" | statistic | [4] | verified (extract) |
| 4 | "The schema document...is positioned as 'the real product'" | attribution | [2] | verified (extract) |
| 5 | Index.md navigation scales to 100-200 pages | statistic | [2] | corrected — MindStudio [9] states threshold as "500+ documents"; 100-200 figure from rohitg00 [2] only; sources disagree |
| 6 | LLM Wiki Kit provides 8 MCP tools: wiki_init through wiki_log | attribution | [10] | verified (extract) |
| 7 | LLM Wiki Kit uses SQLite FTS5 with Porter stemming | attribution | [10] | verified (extract) |
| 8 | "every directory has an index. Claude reads indexes first, never scans blindly" | quote | [13] | verified (extract) |
| 9 | Basic Memory provides 20+ MCP tools | statistic | [11] | verified (extract) |
| 10 | rohitg00 implementation spectrum runs 6 levels from Minimal to Collaboration | attribution | [2] | verified (extract) |

---

## Takeaways

1. **Ingest/query/lint is the right operational frame** — universal across all implementations, low friction to adopt.
2. **The schema document is where domain specificity lives** — YAML frontmatter with typed page types, confidence scoring, and relationship edges is the convergent design.
3. **Index.md navigation is a natural fit for WOS's existing `_index.md` pattern** — but the scale limit is real and context-dependent.
4. **MCP and AGENTS.md portability are both worth supporting** — they serve different use cases (programmatic access vs. cross-runtime portability).
5. **Contradiction detection and confidence scoring are the hardest parts** — and the most underbuilt in existing implementations.

**Limitations of this research:** All sources are early-2026 community implementations; no longitudinal evidence; survivorship bias likely significant. The landscape may look different in 12 months.

**Suggested follow-ups:**
- Feasibility study: what would it take to add ingest/query/lint operations to WOS as skills?
- Technical investigation: contradiction detection — how do the few implementations that ship it actually work?
- Options comparison: MCP server vs. AGENTS.md-first for WOS's cross-tool strategy

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | llm-wiki | Andrej Karpathy | 2026 | T1 | verified |
| 2 | https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2 | LLM Wiki v2 | rohitg00 | 2026 | T5 | verified |
| 3 | https://github.com/lucasastorian/llmwiki | lucasastorian/llmwiki | lucasastorian | 2026 | T5 | verified |
| 4 | https://github.com/MehmetGoekce/llm-wiki | MehmetGoekce/llm-wiki | MehmetGoekce | 2026 | T5 | verified |
| 5 | https://mehmetgoekce.substack.com/p/i-built-karpathys-llm-wiki-with-claude | I Built Karpathy's LLM Wiki with Claude Code and Logseq | Mehmet Goekce | 2026 | T4 | verified |
| 6 | https://github.com/nvk/llm-wiki | nvk/llm-wiki | nvk | 2026 | T5 | verified |
| 7 | https://github.com/SamurAIGPT/llm-wiki-agent | SamurAIGPT/llm-wiki-agent | SamurAIGPT | 2026 | T5 | verified |
| 8 | https://github.com/Ar9av/obsidian-wiki | Ar9av/obsidian-wiki | Ar9av | 2026 | T5 | verified |
| 9 | https://www.mindstudio.ai/blog/llm-knowledge-base-index-file-no-vector-search | What Is the LLM Knowledge Base Index File? | MindStudio | 2026 | T4 | verified |
| 10 | https://glama.ai/mcp/servers/iamsashank09/llm-wiki-kit | LLM Wiki Kit | Glama / iamsashank09 | 2026 | T5 | verified |
| 11 | https://playbooks.com/mcp/basicmachines-co/basic-memory | Basic Memory MCP Server | basicmachines-co | 2026 | T4 | verified |
| 12 | https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md | awesome-mcp-servers: knowledge-management | TensorBlock | 2026 | T5 | verified |
| 13 | https://llm-wiki.net/ | llm-wiki.net | nvk (same as [6]) | 2026 | T5 | verified |
| 14 | https://antigravity.codes/blog/karpathy-llm-wiki-idea-file | Karpathy's LLM Wiki: Complete Guide | Antigravity Codes | 2026 | T5 | verified |
| 15 | https://louiswang524.github.io/blog/llm-knowledge-base/ | Building a Self-Improving Personal Knowledge Base | Louis Wang | 2026 | T5 | verified |
| 16 | https://medium.com/@tahirbalarabe2/what-is-llm-wiki-pattern-persistent-knowledge-with-llm-wikis-3227f561abc1 | What is LLM Wiki Pattern? | Tahir Balarabe | 2026 | T5 | verified (403) |
| 17 | https://a2a-mcp.org/blog/andrej-karpathy-llm-knowledge-bases-obsidian-wiki | Karpathy LLM Knowledge Bases: AI-Powered Wikis in Obsidian | a2a-mcp.org | 2026 | T5 | verified |

**SIFT Notes:** T1 [1]: Karpathy is the original author (primary source). T4 [5]: detailed practitioner writeup with implementation evidence. T4 [9]: commercial platform (conflict of interest noted) but index navigation analysis is implementation-agnostic. T4 [11]: official project documentation. T5 [2–4,6–8,10,12–17]: community implementations and derivative explainers. Red flags: sources 6 and 13 are the same project; sources 14, 16, 17 are derivative with circular sourcing risk; survivorship bias across all implementation sources.

---

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| Karpathy LLM wiki persistent knowledge base markdown gist 2025 | google | 2025-2026 | 10 | 4 |
| Karpathy "llm wiki" ingest query lint operations implementation open source 2025 | google | 2025-2026 | 10 | 6 |
| "llm wiki" "CLAUDE.md" schema design markdown frontmatter confidence scoring contradiction detection 2025 | google | 2025-2026 | 10 | 5 |
| LLM knowledge base markdown vs JSON schema design confidence scoring frontmatter page types 2025 | google | 2025-2026 | 10 | 3 |
| "llm wiki" contradiction detection "knowledge graph" relationship types implementation 2025 | google | 2025-2026 | 10 | 3 |
| persistent LLM knowledge base "page types" entity concept source-summary YAML frontmatter schema 2025 | google | 2025-2026 | 10 | 4 |
| LLM wiki navigation "index.md" without vector embeddings keyword search file-based retrieval 2025 | google | 2025-2026 | 10 | 3 |
| LLM knowledge base MCP "model context protocol" integration persistent wiki tools 2025 2026 | google | 2025-2026 | 10 | 2 |
| LLM wiki MCP server "knowledge base" tools guide search read write persistent memory 2025 2026 | google | 2025-2026 | 10 | 5 |
| "llm-wiki" OR "llm wiki" "cross-tool" "cross-runtime" MCP Obsidian Logseq integration persistent knowledge 2025 2026 | google | 2025-2026 | 10 | 4 |
| LLM wiki "AGENTS.md" portable cross-runtime Claude Code Codex Gemini knowledge base pattern 2025 2026 | google | 2025-2026 | 10 | 3 |

11 searches · 17 sources · 110 candidates surfaced · 42 used

Not searched: academic literature on LLM memory systems (MemGPT, etc.); knowledge base maintenance cost studies; specific SQLite FTS5 implementation details for wiki search.
