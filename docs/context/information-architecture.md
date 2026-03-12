---
name: "Information Architecture for Agent Navigation"
description: "Structural patterns for organizing knowledge that LLM agents can navigate efficiently: shallow hierarchy, metadata-first discovery, index files, and faceted classification through frontmatter"
type: reference
sources:
  - https://www.nngroup.com/articles/taxonomy-101/
  - https://www.nngroup.com/articles/ia-vs-navigation/
  - https://www.nngroup.com/articles/information-scent/
  - https://en.wikipedia.org/wiki/Faceted_classification
  - https://fortelabs.com/blog/para/
  - https://thenewstack.io/agentic-knowledge-base-patterns/
  - https://www.microsoft.com/en-us/research/blog/from-raw-interaction-to-reusable-knowledge-rethinking-memory-for-ai-agents/
  - https://claude.com/blog/using-claude-md-files
related:
  - docs/research/information-architecture.md
  - docs/context/context-window-management.md
  - docs/context/agent-state-persistence.md
  - docs/context/tool-design-for-llms.md
---

Information architecture (IA) determines how agents find and navigate knowledge. Traditional IA focuses on humans who browse, scan, and build spatial memory. Agent-oriented IA must account for different constraints: no spatial memory, token cost for every file read, no visual scanning, and session boundaries that reset navigational context. Six principles emerge from foundational IA research adapted for agent consumption.

## Shallow Hierarchy with Flat Internals

The flat-vs-hierarchical debate resolves pragmatically: use 1-2 levels of meaningful directory grouping, but keep each directory flat internally. Deep hierarchies (3+ levels) force agents into expensive traversal. Purely flat structures degrade past 30 items because the agent must scan the entire index to find relevant content. Shallow categories (5-10 directories) dramatically reduce scan cost while avoiding nesting that obscures content.

The PARA method illustrates this well — four top-level categories organized by actionability (Projects, Areas, Resources, Archives), flat within each. The principle is to organize by *when you will use it*, not *what it is about*.

## Metadata as Primary Navigation

Frontmatter fields (name, description, type, related) are the agent's equivalent of information scent — the cues that predict what lies behind a link before following it. The description field answers "is this document worth reading?" in milliseconds rather than consuming the full context window. Investing in accurate, descriptive metadata yields more navigational value than elaborate folder structures.

This maps to the IA distinction between structure and navigation: IA is the underlying organization; metadata, indexes, and cross-references are surface expressions of that structure. The same IA can support multiple navigation patterns without changing the underlying organization.

## Auto-Generated Indexes over Hand-Curated Navigation

A dedicated index file per directory lists all contents with descriptions extracted from frontmatter. This is the single most important pattern for agent navigation — it converts expensive file-by-file exploration into a single cheap lookup. The agent reads one file to understand an entire directory.

Index files derived from disk state are always accurate. Hand-maintained tables of contents drift from reality. Convention over configuration.

## Faceted Classification through Frontmatter

Faceted classification allows the same item to be found via different search strategies by combining independent dimensions. For agent knowledge bases, the most effective approach is a small set of flat facets encoded in frontmatter metadata rather than folder nesting. A `type` field acts as one facet (research, reference, plan). A `related` field encodes graph relationships. Additional fields (domain, status) add facets without hierarchy. The agent reads metadata to filter and select, never needing to traverse a deep taxonomy tree.

## Cross-References Create a Navigable Graph

Bidirectional links between documents (via the `related` field) create a navigable graph on top of any hierarchical structure. When document A references B and B references A, agents can traverse laterally across categories without returning to the index. This lateral movement is especially valuable for cross-cutting concerns that span multiple directories.

## Entrypoint Files for Orientation

A single root-level file (CLAUDE.md, AGENTS.md) that explains the structure, points to key locations, and states conventions gives agents the bootstrap context they need without reading every index. The entrypoint serves as a map — agents read it first to understand where things live, then navigate by convention or index to specific content.

## Institutional vs. Situational Separation

Stable knowledge (architecture decisions, conventions, principles) belongs in persistent context files. Transient knowledge (current goals, in-progress work) belongs in plans or session state. This separation prevents context pollution and keeps stable knowledge retrievable across sessions. Microsoft Research's PlugMem system confirms the principle: structuring knowledge *before* storage, rather than at retrieval time, reduces redundancy and improves retrieval precision.
