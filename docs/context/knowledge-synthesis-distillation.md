---
name: "Knowledge Synthesis and Distillation"
description: "How to compress raw research into focused, actionable context: purpose-driven compression, structured preservation, provenance separation, and practical keep/discard heuristics"
type: reference
sources:
  - https://arxiv.org/abs/physics/0004057
  - https://arxiv.org/abs/2307.03172
  - https://arxiv.org/abs/2310.05736
  - https://factory.ai/news/evaluating-compression
  - https://factory.ai/news/compressing-context
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
  - https://fortelabs.com/blog/progressive-summarization-a-practical-technique-for-designing-discoverable-notes/
related:
  - docs/research/knowledge-synthesis-distillation.md
  - docs/context/context-window-management.md
  - docs/context/prompt-engineering.md
---

Knowledge distillation is lossy compression. You cannot compress without defining what counts as acceptable loss, and that definition depends on the downstream task. The information bottleneck method (Tishby et al., 1999) formalizes this: relevant information is what the compressed output needs to predict. For agent-facing documents, the relevant variable is the decision or action the agent will take. Content that informs agent behavior is incompressible; everything else is compressible.

This is the single most important principle: **compress relative to purpose, not uniformly.**

## Structure Forces Preservation

Structured summarization with dedicated sections outperforms opaque compression. Factory.ai's benchmark across 36,000+ messages showed structured approaches scoring 3.70 vs 3.35 for opaque compression at similar compression ratios. Each section acts as a checklist the compressor must populate — decisions, constraints, findings, sources, limitations — preventing silent information drift. When a section exists, information that belongs there is harder to silently drop.

## Provenance in a Separate Channel

Provenance is metadata about compressed content, not part of the content itself. Citation references, source tables, and file path pointers add minimal tokens while maintaining traceability. Three mechanisms scale differently:

- **Inline citations** ([1], [2]) — lightest weight, survives multiple compression rounds
- **Restorable compression** — replace content with pointers to re-fetch it (URLs replace page content, file paths replace file contents)
- **Traceable text** — phrase-level provenance links; most granular but increases document size substantially

Keep provenance in a separate channel (frontmatter `sources`, footnotes, reference tables) so it does not consume the same token budget as substance.

## Progressive Distillation

Progressive summarization (Forte, 2017) provides a multi-pass technique: capture raw notes (Layer 1), bold key phrases (Layer 2), highlight the best of the bolded (Layer 3), write a 1-2 sentence executive summary (Layer 4). Each layer leaves behind good-but-not-great content. This maps directly to agent-facing documents: Layer 1 is the raw research artifact, Layer 4 is the frontmatter `description` field.

Not everything compresses equally. Specific facts — names, dates, exact figures, file paths, identifiers — resist compression (Kolmogorov complexity sets the floor). Patterns and generalizations compress well. A good distillation preserves the specific and compresses the general.

## What to Keep, What to Discard

Factory.ai and Manus arrived at similar heuristics independently:

**Keep:**
- Decisions and their rationale (why, not just what)
- Specific constraints, requirements, and stated goals
- Key findings with confidence levels and source citations
- File paths, identifiers, and proper nouns (incompressible)
- Counter-evidence and limitations (easily lost in summarization)

**Discard:**
- Exploratory dead ends once conclusions exist
- Raw tool outputs when the conclusion is preserved
- Redundant restatements and acknowledgements
- Boilerplate, navigation, and formatting artifacts
- Intermediate reasoning steps once final reasoning is captured

## Compression Limits

Aggressive compression works: LLMLingua achieves 20x prompt compression with 1.5% performance loss. But cutting too aggressively forces re-fetching, adding latency that outweighs token savings. If an agent frequently re-reads files after compression, the threshold is too aggressive. Compress reversibly — strip information that exists in the environment, preserve only the pointer needed to recover it.

For agent-specific positioning and attention-curve strategies, see the companion context on [context window management](context-window-management.md).
