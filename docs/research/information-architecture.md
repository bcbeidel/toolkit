---
name: "Information Architecture for Knowledge Retrieval"
description: "Taxonomy design, flat vs. hierarchical structures, navigation patterns, and discoverability — including agent-specific patterns like index files and metadata-first navigation"
metadata:
  type: research
  sources:
    - https://www.nngroup.com/articles/taxonomy-101/
    - https://www.nngroup.com/articles/ia-vs-navigation/
    - https://www.nngroup.com/articles/information-scent/
    - https://en.wikipedia.org/wiki/Faceted_classification
    - https://fortelabs.com/blog/para/
    - https://thenewstack.io/agentic-knowledge-base-patterns/
    - https://www.infoworld.com/article/4091400/anatomy-of-an-ai-agent-knowledge-base.html
    - https://en.wikipedia.org/wiki/Richard_Saul_Wurman
    - https://www.hedden-information.com/faceted-classification-and-faceted-taxonomies/
    - https://fortelabs.com/blog/a-complete-guide-to-tagging-for-personal-knowledge-management/
    - https://bloomfire.com/blog/folders-complex-knowledge/
    - https://www.matrixflows.com/blog/knowledge-base-taxonomy-best-practices
    - https://understandinggroup.com/ia-theory/understanding-information-architecture
    - https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/
    - https://claude.com/blog/using-claude-md-files
  related:
    - docs/research/context-window-management.md
    - docs/research/agent-state-persistence.md
    - docs/research/tool-design-for-llms.md
    - docs/context/information-architecture.md
---

Organizing knowledge for retrieval is the central problem of information architecture (IA). For agent-based systems, the challenge intensifies: agents cannot browse, scan headings, or build spatial memory the way humans do. They need explicit structural cues — metadata, index files, and conventions — to navigate efficiently. This research covers foundational IA principles, structural trade-offs, and the emerging patterns specific to LLM agent navigation.

## Sub-Questions

1. What are the foundational principles of information architecture for knowledge organization?
2. What are the trade-offs between flat vs. hierarchical organizational structures?
3. What navigation patterns enable discoverability in document collections?
4. How do taxonomy and classification schemes support retrieval?
5. What agent-specific patterns exist for knowledge navigation (index files, metadata-first)?
6. How do existing knowledge management systems approach structure at scale?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.nngroup.com/articles/taxonomy-101/ | Taxonomy 101: Definition, Best Practices, and How It Complements Other IA Work | Nielsen Norman Group | 2024 | T1 | verified |
| 2 | https://www.nngroup.com/articles/ia-vs-navigation/ | The Difference Between Information Architecture and Navigation | Nielsen Norman Group | 2024 | T1 | verified |
| 3 | https://www.nngroup.com/articles/information-scent/ | Information Scent: How Users Decide Where to Go Next | Nielsen Norman Group | 2024 | T1 | verified |
| 4 | https://en.wikipedia.org/wiki/Faceted_classification | Faceted Classification | Wikipedia | 2024 | T3 | verified |
| 5 | https://fortelabs.com/blog/para/ | The PARA Method | Forte Labs / Tiago Forte | 2023 | T3 | verified |
| 6 | https://thenewstack.io/agentic-knowledge-base-patterns/ | 6 Agentic Knowledge Base Patterns Emerging in the Wild | The New Stack | 2025 | T3 | verified |
| 7 | https://www.infoworld.com/article/4091400/anatomy-of-an-ai-agent-knowledge-base.html | Anatomy of an AI Agent Knowledge Base | InfoWorld | 2025 | T3 | verified |
| 8 | https://en.wikipedia.org/wiki/Richard_Saul_Wurman | Richard Saul Wurman | Wikipedia | 2024 | T3 | verified |
| 9 | https://www.hedden-information.com/faceted-classification-and-faceted-taxonomies/ | Faceted Classification and Faceted Taxonomies | Hedden Information Management | 2023 | T2 | verified |
| 10 | https://fortelabs.com/blog/a-complete-guide-to-tagging-for-personal-knowledge-management/ | A Complete Guide to Tagging for Personal Knowledge Management | Forte Labs / Tiago Forte | 2023 | T3 | verified |
| 11 | https://bloomfire.com/blog/folders-complex-knowledge/ | Why a Folder Structure Doesn't Cut It for Organizing Complex Knowledge | Bloomfire | 2024 | T4 | verified |
| 12 | https://www.matrixflows.com/blog/knowledge-base-taxonomy-best-practices | Knowledge Base Taxonomy: 10 Principles That Work | MatrixFlows | 2024 | T4 | verified |
| 13 | https://understandinggroup.com/ia-theory/understanding-information-architecture | Understanding Information Architecture | The Understanding Group | 2024 | T2 | verified |
| 14 | https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/ | PlugMem: Transforming Raw Agent Interactions into Reusable Knowledge | Microsoft Research | 2025 | T1 | verified |
| 15 | https://claude.com/blog/using-claude-md-files | Using CLAUDE.MD Files | Anthropic | 2025 | T1 | verified |

## Findings

### 1. Foundational Principles of Information Architecture

Information architecture is the structural design of shared information environments — the practice of organizing, labeling, and relating content so it can be found and understood [2][13]. The field rests on three interlocking components identified by The Understanding Group: **ontology** (what things mean), **taxonomy** (how meaning is structured), and **choreography** (how users flow through structure) [13].

Richard Saul Wurman, who coined the term "information architect" in 1976, identified five — and only five — ways to organize information, known as LATCH: **Location**, **Alphabet**, **Time**, **Category**, and **Hierarchy** [8]. This constraint is powerful: every organizational system, no matter how complex, reduces to one or a combination of these five axes. A knowledge base sorted by topic uses Category. A changelog uses Time. A directory listing uses Alphabet. An org chart uses Hierarchy. Understanding LATCH prevents inventing ad-hoc schemes when a proven pattern already fits.

The Rosenfeld-Morville framework (from the foundational "polar bear book" *Information Architecture for the Web and Beyond*) identifies four interconnected systems: organization systems, labeling systems, navigation systems, and search systems. Each handles a different aspect of findability (HIGH — T1 + T2 sources converge on this framework) [2][13].

**Key principle:** IA is not navigation. IA is the underlying structure; navigation is one surface expression of that structure. The same IA can support multiple navigation patterns — tables of contents, indexes, breadcrumbs, search — without changing the underlying organization [2].

### 2. Flat vs. Hierarchical Structures

The flat-vs-hierarchical debate is the central structural question for any knowledge system. Neither wins universally; the right choice depends on collection size, retrieval patterns, and the consumer (human or agent).

**Hierarchical structures** provide predictable paths. Users can narrow from broad categories to specific items through progressive disclosure. Research suggests 5-9 top-level categories as optimal for human navigation — more creates decision paralysis, fewer means categories are too broad [1][12]. Hierarchies impose a single ordering that mirrors how the organizer thinks, which may not match how the retriever thinks.

**Flat structures** eliminate categorization friction. The Zettelkasten method exemplifies this: all notes exist at one level, connected by explicit links rather than folder placement. The argument is that hierarchies create silos — notes within a folder tend to link only to siblings, suppressing cross-domain connections. Flat structures force every relationship to be explicit through links or tags [10].

**Practical trade-offs:**

| Dimension | Hierarchical | Flat |
|-----------|-------------|------|
| Browsability | Strong — progressive disclosure | Weak — requires search or index |
| Cross-cutting concerns | Weak — items can only live in one place | Strong — tags/links allow multi-membership |
| Scalability | Degrades past ~3 levels deep | Degrades past ~30 top-level items without grouping |
| Cognitive load (organizing) | High — must choose the "right" place | Low — just add and tag |
| Cognitive load (finding) | Low if structure matches mental model | High without good search/filtering |
| Agent navigability | Moderate — requires traversal | Moderate — requires index or metadata scan |

**Hybrid approaches dominate in practice.** Shallow hierarchies (1-2 levels) with cross-cutting metadata provide the browsability benefits of hierarchy without deep nesting. The PARA method uses exactly four top-level categories (Projects, Areas, Resources, Archives) organized by actionability rather than topic, with tags for cross-cutting concerns [5]. This "just enough hierarchy" pattern — broad categories at the top, flat within each — appears repeatedly in successful knowledge systems (HIGH — multiple sources converge) [5][10][11].

### 3. Navigation Patterns and Discoverability

Discoverability depends on **information scent** — the strength of cues that help a user (or agent) predict what lies behind a link or label before following it [3]. The term comes from Pirolli and Card's information foraging theory, which models information-seeking behavior as analogous to animal foraging: users follow scent trails of increasingly relevant cues toward their goal [3].

**Key navigation patterns for document collections:**

**Index-based navigation.** A dedicated index file per directory lists all contents with descriptions. This is the primary pattern for agent navigation — agents read the index to understand what exists and select relevant documents by description rather than traversing blindly. The index serves as a "menu" with information scent baked into each entry.

**Metadata-first navigation.** Frontmatter metadata (name, description, type, related) at the top of each document lets agents assess relevance without reading full content. This is the agent equivalent of information scent — a structured, parseable signal that answers "is this document worth reading?" in milliseconds rather than consuming the full context window [15].

**Breadcrumb/path-based orientation.** Knowing where you are in a structure (which directory, which category) provides context for interpreting content and finding related items. For agents, this translates to directory conventions — predictable paths like `docs/research/` or `docs/context/` that encode document purpose in the path itself.

**Cross-references (related field).** Bidirectional links between documents create a navigable graph on top of any hierarchical structure. When document A references B in its `related` field, and B references A, agents can traverse laterally across categories without returning to the index.

**Progressive disclosure.** Show summaries first, details on demand. For agents, this means the description field provides a one-sentence summary, the first paragraph provides key insights, and the full body provides detail — matching the principle of "bottom line up front" (HIGH — T1 sources on information scent + practical pattern convergence) [3][15].

### 4. Taxonomy and Classification for Retrieval

A taxonomy is a controlled vocabulary structured into broader-narrower concept relationships, used to tag content for findability [1][9]. Taxonomies differ from free-text tags in that they are curated, unambiguous, and relational.

**Three taxonomy types:**

**Hierarchical taxonomy** arranges terms in parent-child trees. "Programming Languages > Python > AsyncIO" is hierarchical. Works well when items have clear is-a or part-of relationships. Breaks down when items belong to multiple categories [1][9].

**Flat taxonomy** is a single-level list of controlled terms without hierarchy. Best for tagging content types or stages ("how-to," "reference," "research," "decision"). Does not scale past 20-30 terms without becoming overwhelming [12].

**Faceted taxonomy** combines multiple independent hierarchies that describe different aspects of the same item. A document might be classified along facets of *topic* (security), *type* (research), and *audience* (engineering). Faceted classification allows navigation along multiple paths — users are not forced into a single predetermined order [4][9]. This is the most powerful approach for complex collections because it enables the same item to be found via different search strategies (HIGH — T1 + T2 sources on taxonomy types) [1][4][9].

**For agent consumption**, the most effective approach is a small set of flat facets encoded in frontmatter metadata. A `type` field acts as one facet. A `related` field encodes graph relationships. Additional fields (audience, status, domain) add facets without hierarchy. The agent reads metadata to filter and select, never needing to understand or traverse a deep taxonomy tree.

### 5. Agent-Specific Navigation Patterns

LLM agents face unique constraints that make traditional IA patterns insufficient on their own:

- **No spatial memory.** Agents cannot "remember" where things were from previous sessions without explicit persistence.
- **Token cost for exploration.** Every file read consumes context window. Browsing is expensive.
- **No visual scanning.** Agents cannot glance at a page and pick out relevant sections the way humans do.
- **Session boundaries.** Agent context resets between invocations; navigation knowledge must be re-acquired.

**Emerging patterns for agent knowledge bases [6][7][14]:**

**Pattern 1: Metadata-first index files.** Auto-generated index files that list directory contents with descriptions extracted from frontmatter. The agent reads one file to understand an entire directory. This is the single most important pattern for agent navigation — it converts expensive exploration into cheap lookup.

**Pattern 2: Convention-driven paths.** Predictable directory structures (`docs/research/`, `docs/context/`, `docs/plans/`) where the path itself encodes document purpose. Agents can navigate by convention without reading indexes when they know what type of content they need.

**Pattern 3: Entrypoint files (CLAUDE.md, AGENTS.md).** A single root-level file that provides orientation: what the project is, where things live, how to navigate. The agent reads this file first to bootstrap its understanding of the knowledge structure [15].

**Pattern 4: Structured frontmatter as faceted metadata.** YAML frontmatter with controlled fields (name, description, type, sources, related) serves as machine-readable facets. Agents can filter by type, follow related links, and assess relevance from description — all without reading document bodies.

**Pattern 5: Institutional vs. situational context separation.** Stable knowledge (architecture decisions, conventions, principles) lives in persistent context files. Transient knowledge (current sprint goals, in-progress work) lives in plans or session state. This separation prevents context pollution and keeps stable knowledge retrievable across sessions [7][14].

**Pattern 6: Structured memory over raw retrieval.** Microsoft Research's PlugMem system demonstrates that organizing agent memory into structured facts and reusable skills — rather than storing raw interaction history — reduces redundancy, increases information density, and improves retrieval precision [14]. The principle: structure the knowledge *before* storage, not at retrieval time.

**Counter-evidence:** Some practitioners argue that sophisticated IA is unnecessary for agents because vector search and semantic retrieval can find relevant content regardless of organization. However, this assumes reliable embedding quality and ignores the token cost of retrieving false positives. Structured navigation consistently outperforms pure search for known-item retrieval and context-constrained agents (MODERATE — emerging consensus in practitioner literature, limited formal research) [6][7].

### 6. Knowledge Management Systems at Scale

Real-world knowledge systems reveal patterns that formal IA theory sometimes misses:

**PARA method** [5]: Four categories organized by actionability (Projects, Areas, Resources, Archives). Key insight: organize by *when you will use it*, not *what it is about*. This principle — actionability over topic — directly applies to agent knowledge bases where the retrieval question is usually "what do I need to do this task?" not "what do we know about this subject?"

**Zettelkasten** [10]: Flat linked notes. Key insight: connections between ideas are more valuable than categories. Structure emerges from links, not from pre-imposed hierarchy. For agents, this translates to the `related` field — explicit links between documents that create a navigable graph.

**Wiki-style systems** (Confluence, Notion): Shallow hierarchy with search. Key insight: beyond 2-3 levels of nesting, hierarchy actively hinders findability because users cannot predict which branch contains their target. Wikis that succeed keep hierarchies shallow and invest in search and cross-linking instead.

**Documentation-as-code** (docs-in-repo patterns): Convention-driven organization where directory structure mirrors project structure. Key insight: co-locating documentation with the code it describes creates natural navigation paths — developers already know where to look because the docs live next to the code.

## Challenge

**What if flat is always better?** The Zettelkasten community argues that all hierarchy is harmful. But agent navigation without *any* grouping degrades rapidly as collection size grows. An agent facing 200 ungrouped documents in a single directory must read the entire index to find relevant items. Shallow categories (even 5-10 directories) dramatically reduce this scan cost.

**What if agents don't need IA at all?** If embedding-based retrieval is good enough, perhaps organizational structure is unnecessary overhead. Current evidence suggests this is wrong for two reasons: (1) retrieval quality depends on chunk boundaries that reflect document structure, and (2) agents need to *understand* relationships between documents, not just find individual documents. Structure encodes relationships that flat retrieval misses.

**What about evolving structure?** Any classification scheme becomes outdated as knowledge grows. The PARA method addresses this with "just-in-time organization" — organize as a consequence of work, not as a separate maintenance task. For agent knowledge bases, auto-generated indexes (derived from disk state) embody this principle: the structure updates itself when documents change.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Wurman coined the term "information architect" in 1976 | attribution | [8] | verified |
| 2 | LATCH identifies five and only five ways to organize information | framework | [8] | verified |
| 3 | 5-9 top-level categories is optimal for human navigation | statistic | [1][12] | verified — NN/g cites Miller's Law and usability research |
| 4 | Flat taxonomy does not scale past 20-30 categories | threshold | [12] | verified — practitioner consensus, not formal research |
| 5 | Information scent coined by Pirolli and Card at PARC | attribution | [3] | verified |
| 6 | PARA stands for Projects, Areas, Resources, Archives | definition | [5] | verified |
| 7 | PlugMem reduces redundancy and improves retrieval precision | performance | [14] | verified — Microsoft Research publication |
| 8 | Faceted classification allows navigation along multiple paths | capability | [4][9] | verified |

## Search Protocol

| # | Query | Tool | Results | Useful |
|---|-------|------|---------|--------|
| 1 | "information architecture principles knowledge organization taxonomy design" | WebSearch | 10 | 5 |
| 2 | "flat vs hierarchical information structure trade-offs knowledge management" | WebSearch | 10 | 4 |
| 3 | "LLM agent knowledge navigation patterns metadata-first index files" | WebSearch | 10 | 5 |
| 4 | "faceted classification vs hierarchical taxonomy information retrieval" | WebSearch | 10 | 4 |
| 5 | "Nielsen Norman Group information architecture navigation patterns discoverability" | WebSearch | 10 | 3 |
| 6 | "knowledge base organization flat structure tags vs folders documents" | WebSearch | 10 | 5 |
| 7 | "PARA method Tiago Forte knowledge organization system" | WebSearch | 10 | 3 |
| 8 | "AI agent context retrieval structured knowledge base design patterns 2025" | WebSearch | 10 | 4 |
| 9 | "Richard Saul Wurman LATCH information organization" | WebSearch | 10 | 3 |
| 10 | "Peter Morville information architecture polar bear book findability" | WebSearch | 10 | 2 |
| 11 | "Zettelkasten knowledge organization method flat linked notes vs hierarchical folders" | WebSearch | 10 | 4 |
| 12 | "Claude Code AGENTS.md CLAUDE.md context navigation project structure" | WebSearch | 10 | 3 |
| 13 | "information scent navigation usability research findability cues" | WebSearch | 10 | 4 |

## Takeaways

For agent-oriented knowledge systems, six principles emerge from this research:

1. **Shallow hierarchy with flat internals.** Use 1-2 levels of meaningful directory grouping (by domain or document type), but keep each directory flat. This balances browsability against the cost of deep traversal.

2. **Metadata as the primary navigation mechanism.** Frontmatter fields (name, description, type, related) are the agent's information scent. Invest in descriptive, accurate metadata over elaborate folder structures.

3. **Auto-generated indexes over hand-curated navigation.** Index files derived from disk state are always accurate. Hand-maintained tables of contents drift from reality. Convention over configuration.

4. **Faceted classification through frontmatter fields, not folder nesting.** Use flat controlled vocabularies (type: research | context | plan) as facets. Multiple facets encoded in metadata are more powerful than a single deep hierarchy.

5. **Explicit cross-references.** The `related` field creates a navigable graph that supplements hierarchical browsing. Bidirectional links are especially valuable — they let agents traverse laterally.

6. **Entrypoint files for orientation.** A single root file (CLAUDE.md, AGENTS.md) that explains the structure, points to key locations, and states conventions gives agents the bootstrap context they need without reading every index.
