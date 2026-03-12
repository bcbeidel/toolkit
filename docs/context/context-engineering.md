---
name: "Context Engineering"
description: "The discipline of structuring, storing, and surfacing project knowledge so LLMs consume it effectively — document models, indexing strategies, and the curation hierarchy"
type: reference
sources:
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2404.16811
  - https://arxiv.org/abs/2312.06648
  - https://platform.claude.com/docs/en/docs/build-with-claude/context-windows
  - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
related:
  - docs/research/context-engineering.md
  - docs/context/context-window-management.md
  - docs/context/prompt-engineering.md
---

## Key Insight

Context engineering is not prompt engineering. Prompt engineering optimizes instruction phrasing. Context engineering addresses the broader problem: what information enters an LLM's working memory, how it is organized, and where critical content sits relative to attention patterns. The distinction matters because most performance gains come from what you include, not how you phrase the request.

## The Document Model: Flat and Atomic

The most effective storage format for LLM-consumable knowledge is a flat collection of atomic, self-contained documents with lightweight metadata. This conclusion draws from converging evidence:

- **Proposition-level retrieval outperforms passage-level.** Dense X Retrieval demonstrates that atomic indexing units significantly outperform coarser retrieval across downstream tasks. This maps directly to one-concept-per-file.
- **Industry convergence on flat markdown.** Claude Code (CLAUDE.md), Cursor (.cursorrules), and GitHub Copilot (.github/copilot-instructions.md) all use flat, human-readable files with metadata headers. No major tool uses hierarchical databases.
- **Self-describing metadata enables navigation.** Two required fields — `name` (identity) and `description` (purpose) — let an agent decide whether to read a document without consuming its full token budget. Optional fields (`type`, `sources`, `related`) extend without cluttering the baseline.

The optimal document targets 200-800 words. At this size, the "middle" where attention degrades is only 100-400 words, limiting the U-shaped degradation zone.

## Progressive Disclosure Through Auto-Generated Indexes

Effective context engineering uses layered navigation so agents consume only the tokens relevant to their current task:

| Layer | Content | Token Cost | Purpose |
|-------|---------|------------|---------|
| AGENTS.md | Navigation instructions + area overview | ~500 tokens | Teaches agents how to explore |
| `_index.md` | File list with descriptions per directory | ~50-200 tokens | Enables read/skip decisions |
| Frontmatter | Per-file metadata | ~30-50 tokens | Fine-grained routing |
| Body | Full document content | ~200-800 words | Actual knowledge |

Auto-generation from disk state is critical. Hand-curated indexes drift from reality, creating navigation failures worse than no index at all. Deriving indexes from frontmatter ensures correctness by construction.

## The Curation Hierarchy

The most important insight: quality of context dominates quantity. "More context isn't automatically better. As token count grows, accuracy and recall degrade" — a phenomenon called context rot.

Ranked by impact on LLM performance:

1. **Selection** — choosing which documents enter context at all (highest impact)
2. **Ordering** — positioning critical information at attention-optimal positions
3. **Compression** — reducing token cost of included content
4. **Formatting** — using structural markup for navigability
5. **Capacity** — having enough tokens available (lowest impact)

Prompt caching reinforces this hierarchy. Static context placed as stable prefixes gets cached at 90% cost reduction. This creates an economic incentive for consistent document ordering and separation of static knowledge from dynamic conversation state.

## The Lifecycle Gap

Most existing tools address only one layer of the context problem. RAG systems handle retrieval. CLAUDE.md handles instruction. Cursor handles project rules. None provide the full pipeline: research, author, validate, maintain. Context without maintenance decays — sources go stale, documents drift from implementation, indexes fall out of sync. Systematic lifecycle management is what separates context engineering from ad-hoc documentation.

## Takeaways

Context engineering rests on six operational principles: atomic documents with self-describing metadata, progressive disclosure through auto-generated indexes, BLUF formatting to exploit attention patterns, curation over capacity, consistent ordering for cache efficiency, and lifecycle management from research through maintenance. These are not theoretical — they are validated against peer-reviewed research, vendor documentation, and industry practice.
