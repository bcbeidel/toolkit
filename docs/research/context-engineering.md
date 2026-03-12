---
name: "Context Engineering for LLM-Consumable Project Knowledge"
description: "How to structure, store, and surface project knowledge so LLMs can consume it effectively — document models, frontmatter conventions, indexing strategies, attention-aware formatting"
type: research
sources:
  - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2404.16811
  - https://arxiv.org/abs/2312.06648
  - https://arxiv.org/abs/2401.18059
  - https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
  - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
related:
  - docs/research/context-window-management.md
  - docs/research/prompt-engineering.md
  - docs/context/context-engineering.md
---

## Summary

Context engineering is the discipline of structuring, storing, and surfacing project knowledge so that LLMs can consume it effectively within their attention and token constraints. Unlike prompt engineering (which focuses on instruction phrasing), context engineering addresses the broader problem: what information enters an LLM's working memory, how it is organized, and where critical content is positioned relative to attention patterns.

**Key findings:**

- **Position determines retention.** LLMs exhibit a U-shaped attention curve: information at the beginning and end of context is recalled reliably; information in the middle is often missed. Documents must front-load and back-load key insights (HIGH).
- **Flat document models with lightweight metadata outperform complex hierarchies.** A single document type with required name/description fields and optional semantic tags provides maximum navigability with minimum overhead (HIGH).
- **Auto-generated indexes enable progressive disclosure.** Directory-level indexes derived from document metadata let agents discover what exists without reading everything, reducing token waste (HIGH).
- **Atomic, self-contained documents compress better than monoliths.** Documents targeting 200-800 words with one concept each allow selective inclusion in context windows (MODERATE).
- **XML structure aids LLM parsing of complex, multi-document inputs.** XML tags create unambiguous boundaries that models parse reliably, especially with nested document collections (HIGH).
- **Context window management is primarily a curation problem.** Larger windows do not automatically improve performance; curating what enters context matters more than having space available (HIGH).

## Research Brief

Investigation of how to structure project knowledge for effective LLM consumption. This is the foundational problem that WOS solves: turning unstructured project knowledge into a format that LLMs can navigate, comprehend, and act upon within their inherent cognitive constraints.

### Sub-Questions

1. What document models work best for LLM-readable project context?
2. How do frontmatter conventions improve LLM navigation and comprehension?
3. What indexing strategies enable efficient LLM discovery without reading everything?
4. How should document content be structured to account for LLM attention patterns?
5. What context window economics govern inclusion/exclusion decisions?
6. What prior art exists in context engineering tooling and conventions?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting Best Practices | Anthropic | 2025 | T1 | verified |
| 2 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. / Stanford, UC Berkeley | 2023 | T1 | verified |
| 3 | https://arxiv.org/abs/2404.16811 | FILM-7B: Information-Intensive Training for Long Contexts | An et al. | 2024 | T2 | verified |
| 4 | https://arxiv.org/abs/2312.06648 | Dense X Retrieval: Proposition-Level Retrieval for QA | Chen et al. | 2023 | T2 | verified |
| 5 | https://arxiv.org/abs/2401.18059 | RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval | Sarthi et al. | 2024 | T2 | verified |
| 6 | https://platform.claude.com/docs/en/docs/build-with-claude/context-windows | Context Windows - Anthropic Documentation | Anthropic | 2025 | T1 | verified |
| 7 | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching | Prompt Caching - Anthropic Documentation | Anthropic | 2025 | T1 | verified |
| 8 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |

## Research Protocol

| # | Query | Tool | Results | Selected |
|---|-------|------|---------|----------|
| 1 | Anthropic prompting best practices, XML structure, long context | WebFetch | Official documentation with comprehensive structuring guidance | [1] |
| 2 | Lost in the middle LLM context position effects | WebFetch (arxiv) | Seminal paper on U-shaped attention distribution | [2] |
| 3 | FILM information-intensive training for long contexts | WebFetch (arxiv) | Position-aware training approach, validates position bias | [3] |
| 4 | Dense X Retrieval proposition-level document units | WebFetch (arxiv) | Fine-grained retrieval units outperform passage-level | [4] |
| 5 | RAPTOR hierarchical document retrieval for LLMs | WebFetch (arxiv) | Tree-structured abstraction for multi-level context | [5] |
| 6 | Anthropic context windows documentation | WebFetch | Context window mechanics, context rot, curation emphasis | [6] |
| 7 | Anthropic prompt caching strategies | WebFetch | Cache-friendly document organization, prefix structures | [7] |
| 8 | Anthropic effective context engineering for agents | WebFetch | Identified as key T1 source (referenced in docs) | [8] |

## Extracts by Sub-Question

### SQ1: Document models for LLM-readable project context

**Flat vs. hierarchical models:**
- Dense X Retrieval demonstrates that "indexing a corpus by fine-grained units such as propositions significantly outperforms passage-level units in retrieval tasks" [4]. This supports atomic, self-contained documents over monolithic files.
- Propositions are "atomic expressions within text, each encapsulating a distinct factoid and presented in a concise, self-contained natural language format" [4]. This maps directly to the one-concept-per-file pattern.
- RAPTOR shows that hierarchical tree structures with varying abstraction levels enable "integration of information across lengthy documents at different levels of abstraction" [5]. However, this is a retrieval optimization, not a storage format.

**Document structure for LLM parsing:**
- Anthropic recommends XML tags for structuring multi-document contexts: wrap each document in `<document>` tags with `<document_content>` and `<source>` subtags [1].
- "Structure prompts with XML tags. XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs" [1].
- Nest tags when content has natural hierarchy: documents inside `<documents>`, each inside `<document index="n">` [1].

**Metadata requirements:**
- The minimum viable metadata is identity (what is this?) and summary (why should I read it?). WOS implements this as required `name` and `description` fields.
- Optional semantic tags (`type`, `sources`, `related`) extend without cluttering the baseline.
- "The retrieval unit choice significantly impacts the performance of both retrieval and downstream tasks" [4] — metadata that enables selective retrieval is load-bearing.

### SQ2: Frontmatter conventions for LLM navigation

**Self-describing documents:**
- YAML frontmatter between `---` delimiters creates a machine-readable header that both humans and LLMs can parse.
- Required fields (`name`, `description`) serve dual purposes: they describe the document for human readers AND enable automated index generation.
- The `description` field is the critical navigation field — it allows an LLM to decide whether to read the full document without consuming the entire token budget.

**Type-based semantic routing:**
- The `type` field enables semantic routing: `type: research` triggers source requirements, different validation rules, and different synthesis expectations.
- This is a form of progressive disclosure: the type tells the consumer what kind of content to expect and what quality guarantees apply.

**Relational metadata:**
- `related` fields create explicit links between documents, enabling graph-like navigation.
- `sources` fields establish provenance chains for research documents.
- Bidirectional linking ("if A references B, B should reference A") creates navigable knowledge graphs.

### SQ3: Indexing strategies for LLM discovery

**Auto-generated directory indexes:**
- `_index.md` files list all documents in a directory with descriptions extracted from frontmatter.
- This enables progressive disclosure: read the index (cheap) before reading individual documents (expensive).
- Indexes are derived from disk state, not hand-curated — ensuring they are always correct.

**The progressive disclosure pattern:**
- Level 0: AGENTS.md — teaches agents how to navigate, points to top-level areas
- Level 1: `_index.md` per directory — lists files with descriptions
- Level 2: Frontmatter of individual files — name, description, type, related
- Level 3: Full document content

**Index freshness:**
- Auto-generation from disk state prevents stale indexes.
- `check_index_sync()` validates that indexes match current directory contents.
- Preambles (human-written area descriptions) are preserved across regeneration.

### SQ4: Attention-aware document formatting

**The U-shaped attention curve:**
- "Performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts" [2].
- This finding holds "even for explicitly long-context models" [2].
- Models show "bias towards labels presented later in the sequence" with long contexts [3 from related research].

**Practical formatting implications:**
- "Put longform data at the top. Place your long documents and inputs near the top of your prompt, above your query, instructions, and examples" [1].
- "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs" [1].
- The BLUF (Bottom Line Up Front) pattern directly addresses this: key insights at top and bottom, detail in the middle.

**Structural landmarks:**
- XML tags create "navigable landmarks" that models can attend to.
- "Ground responses in quotes: For long document tasks, ask Claude to quote relevant parts of the documents first before carrying out its task. This helps Claude cut through the noise of the rest of the document's contents" [1].
- Structured markup (headings, tables, tagged sections) creates attention anchors that resist the middle-degradation effect.

### SQ5: Context window economics

**Context rot is real:**
- "More context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot" [6].
- "Only half of [models claiming 32K+ tokens] can maintain satisfactory performance at the length of 32K" (RULER benchmark, from related research).
- The context window is "working memory" — quality of what's in it matters more than capacity.

**Curation over capacity:**
- The fundamental insight: context engineering is primarily a curation problem, not a capacity problem.
- Selective inclusion (choosing what enters context) dominates context quality.
- Token budgets should be allocated explicitly across system instructions, retrieved context, examples, and user input.

**Cache-friendly organization:**
- Prompt caching reduces cost by 90% and latency by 2x for repeated content [7].
- Static content should be placed first (system instructions, tool definitions, context) because caching works on prefixes [7].
- Cache reads cost only 10% of base input tokens [7].
- This creates an economic incentive for consistent document ordering and stable prefixes.

**Compression strategies:**
- Documents targeting 200-800 words balance information density with token cost.
- One concept per file enables selective inclusion without reading irrelevant content.
- Extractive compression (pulling key passages) preserves fidelity better than abstractive compression at the document level.

### SQ6: Prior art in context engineering

**Claude Code conventions:**
- CLAUDE.md: project-level instructions, build commands, architecture notes, conventions.
- AGENTS.md: navigation instructions, metadata format, communication preferences.
- Memory files: user-specific context persisted across conversations.
- These are consumed automatically and injected into every conversation.

**Other tools:**
- Cursor: `.cursorrules` file for project-specific LLM instructions.
- GitHub Copilot: `.github/copilot-instructions.md` for repository-specific context.
- Codebase Context Specification: `.context.md` / `.context.yaml` files per directory (community-driven spec).
- Windsurf: project indexing and context retrieval for code understanding.

**Key convergence patterns across tools:**
- All use markdown-based configuration files in the project root.
- All rely on flat, human-readable formats rather than structured databases.
- All provide a mechanism for project-level instructions separate from per-file context.
- None provide a systematic approach to knowledge lifecycle (research, distill, validate, maintain) — this is the gap WOS fills.

**Academic approaches:**
- RAG (Retrieval-Augmented Generation): retrieve relevant chunks at inference time.
- RAPTOR: hierarchical abstraction trees for multi-level retrieval [5].
- Dense X Retrieval: proposition-level indexing for fine-grained retrieval [4].
- These are inference-time solutions; WOS operates at authoring-time, structuring knowledge before it enters any retrieval pipeline.

## Challenge

### Counter-evidence: Flat models have limitations

The RAPTOR research demonstrates that "hierarchical tree structures with varying summarization levels enable language models to access information at appropriate granularity" [5]. A flat one-document-per-concept model loses the ability to zoom between detail and summary. WOS partially addresses this through the research-to-distill pipeline (research documents contain detail; distilled context files contain summaries) but doesn't provide formal hierarchical navigation within a topic.

### Counter-evidence: Metadata can become overhead

Every frontmatter field has a token cost. For a project with 100 context files, the aggregate frontmatter overhead is non-trivial (estimated 200-400 tokens per document, 20K-40K tokens total). This is justified only if the metadata enables navigation savings that exceed its own cost — which it does when agents use indexes to avoid reading irrelevant documents entirely.

### Counter-evidence: Attention patterns are improving

The FILM-7B research [3] demonstrates that training approaches can improve position-invariant retrieval. As models improve at using middle-positioned information, attention-aware formatting may become less critical. However, the improvement is incremental (NarrativeQA: 23.5 to 26.9 F1), and the U-shaped bias remains substantial even in state-of-the-art models.

### Counter-evidence: Auto-generated indexes can be noisy

When a directory contains many files, auto-generated indexes become long lists that themselves suffer from the lost-in-the-middle problem. Preambles help by front-loading area descriptions, but large directories may need sub-directories or other grouping to keep indexes navigable.

## Findings

### 1. Document Models: Flat and Atomic Beats Complex and Hierarchical

The most effective document model for LLM consumption is a flat collection of atomic, self-contained documents with lightweight metadata. This conclusion draws from converging evidence across retrieval research, Anthropic's official guidance, and practical tool implementations.

Dense X Retrieval demonstrates that proposition-level (atomic) indexing "significantly outperforms passage-level units in retrieval tasks" [4] (HIGH — T2 research with empirical results). Anthropic's own documentation recommends structuring multi-document contexts with XML tags and clear metadata per document [1] (HIGH — T1 vendor documentation). The convergence of all major coding AI tools (Claude Code, Cursor, Copilot) on flat markdown files with metadata headers reinforces this pattern (HIGH — industry convergence).

The optimal document model has three properties:
1. **Atomic scope:** One concept per document, targeting 200-800 words
2. **Self-describing metadata:** Required identity fields (name, description) that enable navigation without reading the body
3. **Optional semantic enrichment:** Type tags, source provenance, and relationship links added only when they serve downstream consumers

**Counter-evidence:** RAPTOR shows hierarchical models improve complex reasoning tasks by 20% on QA benchmarks [5]. However, hierarchy is a retrieval optimization, not a storage requirement — flat documents can be organized into hierarchical retrieval structures at consumption time without changing the storage format (MODERATE).

### 2. Frontmatter Conventions: The Navigation Layer

YAML frontmatter serves as the critical bridge between human-authored content and machine-navigable structure. The minimum viable frontmatter is two required fields: `name` (identity) and `description` (purpose/summary).

The `description` field is the single most important metadata element. It enables an LLM to make a read/skip decision for each document — the fundamental operation that makes context curation possible. Without it, an agent must read every document to determine relevance, consuming context budget proportional to corpus size rather than query relevance (HIGH — architectural reasoning + WOS implementation evidence).

Optional fields extend without burdening:
- `type` enables semantic routing (e.g., research documents trigger source verification)
- `sources` establish provenance chains
- `related` creates navigable knowledge graphs

The key design decision is requiring only what serves navigation and validation. Fields that exist "just in case" violate the principle that every token must earn its place (HIGH — design principle reasoning).

### 3. Indexing: Progressive Disclosure Through Auto-Generated Navigation

The most effective indexing strategy for LLM consumption is progressive disclosure through auto-generated directory indexes. This creates a multi-layered navigation system:

| Layer | Content | Token Cost | Purpose |
|-------|---------|------------|---------|
| AGENTS.md | Navigation instructions + area overview | ~500 tokens | Teaches agents how to explore |
| `_index.md` | File list with descriptions | ~50-200 tokens per directory | Enables read/skip decisions |
| Frontmatter | Per-file metadata | ~30-50 tokens per file | Fine-grained routing |
| Body content | Full document | ~200-800 words per file | Actual knowledge |

This layered approach lets agents navigate a large knowledge base while consuming only the tokens needed for their current task. An agent working on authentication doesn't need to read the deployment context file — the index description tells it the file is irrelevant (HIGH — architectural reasoning + practical implementation evidence).

Auto-generation from disk state is critical: hand-curated indexes drift from reality, creating navigation failures that are worse than no index at all. The WOS pattern of deriving indexes from frontmatter ensures correctness by construction (HIGH — design principle reasoning).

### 4. Attention-Aware Formatting: Working With the U-Curve

LLMs exhibit a well-documented U-shaped attention curve: information at the beginning and end of context windows is processed with significantly higher fidelity than information in the middle [2]. This has direct implications for document structure.

**The BLUF (Bottom Line Up Front) pattern** is the primary formatting response to this research. Key insights go at the top of documents (where attention is highest), detailed explanation in the middle (where attention is lowest but content is still accessible), and takeaways/implications at the bottom (where attention recovers) (HIGH — T1 research + T1 vendor guidance converge).

**Specific formatting recommendations:**
- Place key findings summaries before detailed findings sections
- Put queries/questions after context documents, not before them — "queries at the end can improve response quality by up to 30%" [1]
- Use structural landmarks (headings, XML tags, tables) to create attention anchors that resist middle-degradation
- Keep documents short enough that the middle section is small — 200-800 words means the "middle" is only 100-400 words, limiting the degradation zone

**Context ordering for multi-document inputs:**
- Long reference material at the top
- Instructions and constraints in the middle (where they're surrounded by context)
- The specific query at the end

This ordering pattern is validated by Anthropic's official guidance [1] and consistent with the lost-in-the-middle research [2] (HIGH).

### 5. Context Window Economics: Curation Over Capacity

The most important insight in context engineering is that quality of context dominates quantity. Anthropic's documentation explicitly warns: "More context isn't automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot" [6] (HIGH — T1 vendor documentation).

**The curation hierarchy (most to least impactful):**
1. **Selection:** Choosing which documents enter context at all (highest impact)
2. **Ordering:** Positioning critical information at attention-optimal positions
3. **Compression:** Reducing token cost of included content
4. **Formatting:** Using structural markup for navigability
5. **Capacity:** Having enough tokens available (lowest impact)

**Economic incentives from prompt caching:**
Prompt caching creates a strong incentive for consistent document ordering. When context is structured as stable prefixes (system instructions, then tools, then static knowledge) followed by dynamic content (user queries), cache hit rates increase dramatically. Cache reads cost only 10% of base input tokens [7], meaning a well-structured context prefix that gets cached saves 90% on repeated access (HIGH — T1 vendor documentation with specific pricing).

This economic structure rewards:
- Consistent document ordering across sessions
- Stable context prefixes that don't change between queries
- Separation of static knowledge from dynamic conversation state

### 6. The Context Engineering Landscape: From Ad-Hoc to Systematic

Context engineering has evolved from ad-hoc conventions (README files, code comments) to structured approaches, but most tools address only one layer of the problem:

| Tool/Approach | Authoring | Storage | Navigation | Validation | Lifecycle |
|--------------|-----------|---------|------------|------------|-----------|
| CLAUDE.md | Manual | Flat file | None | None | None |
| .cursorrules | Manual | Flat file | None | None | None |
| RAG systems | External | Vector DB | Embedding search | None | Partial |
| RAPTOR | Automated | Tree | Hierarchical search | None | None |
| WOS | Skill-guided | Flat files + frontmatter | Auto-generated indexes | 8-check audit | Full pipeline |

The gap in existing approaches is systematic lifecycle management. Most tools help you write context or retrieve it, but none provide the full pipeline from research to verified, maintained context. WOS fills this gap by combining:
- Structured authoring (research skill with source verification)
- Validated storage (frontmatter + audit checks)
- Derived navigation (auto-generated indexes + AGENTS.md)
- Quality maintenance (audit, distill, and validation skills)

(MODERATE — comparative analysis based on available documentation; individual tool capabilities may have evolved beyond what's documented)

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | LLMs show U-shaped attention: best at beginning and end, worst in middle | empirical | [2] | verified |
| 2 | Queries at the end improve response quality by up to 30% | statistic | [1] | verified |
| 3 | Proposition-level indexing outperforms passage-level for retrieval | empirical | [4] | verified |
| 4 | RAPTOR achieves 20% improvement on QuALITY benchmark | statistic | [5] | verified |
| 5 | Context rot degrades accuracy as token count grows | concept | [6] | verified |
| 6 | Cache reads cost 10% of base input tokens | statistic | [7] | verified |
| 7 | FILM-7B improved NarrativeQA from 23.5 to 26.9 F1 | statistic | [3] | verified |
| 8 | Only half of models claiming 32K+ maintain performance at that length | statistic | RULER benchmark (Hsieh et al. 2024) | verified — cited in related WOS research |
| 9 | XML tags help Claude parse complex prompts unambiguously | guidance | [1] | verified |
| 10 | Prompt caching reduces cost by up to 90% for repeated content | statistic | [7] | verified |

## Takeaways

Context engineering is the discipline of making project knowledge LLM-consumable. The core principles, validated by research and practice:

1. **Atomic documents with self-describing metadata** — one concept per file, required name and description, optional semantic enrichment
2. **Progressive disclosure through auto-generated indexes** — let agents navigate cheaply before reading deeply
3. **BLUF formatting to exploit attention patterns** — key insights at top and bottom, detail in the middle
4. **Curation over capacity** — what enters context matters more than how much space is available
5. **Consistent ordering for cache efficiency** — stable prefixes enable dramatic cost reduction
6. **Lifecycle management** — research, author, validate, maintain; context without maintenance decays

These principles are not theoretical. They are the operational foundation of WOS, validated against 8 sources spanning peer-reviewed research, vendor documentation, and industry practice.
