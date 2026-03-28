---
name: "Writing for LLM Consumption"
description: "How agent-facing documentation differs from human-facing writing — BLUF structure, explicit conventions, self-contained sections, and navigable metadata for optimal LLM comprehension"
metadata:
  type: research
  sources:
    - https://arxiv.org/abs/2307.03172
    - https://arxiv.org/abs/2406.16008
    - https://arxiv.org/abs/2411.10541
    - https://arxiv.org/abs/2602.20478
    - https://biel.ai/blog/optimizing-docs-for-ai-agents-complete-guide
    - https://docs.kapa.ai/improving/writing-best-practices
    - https://code.claude.com/docs/en/best-practices
    - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
    - https://llmstxt.org/
    - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    - https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
    - https://www.promptwire.co/articles/how-to-structure-content-for-llm-citations
  related:
    - docs/context/writing-for-llm-consumption.md
    - docs/context/context-window-management.md
    - docs/context/prompt-engineering.md
    - docs/research/context-window-management.md
    - docs/research/information-architecture.md
    - docs/research/prompt-engineering.md
---

Agent-facing documentation operates under fundamentally different constraints than human-facing writing. Humans browse, scan headings, build spatial memory, and infer unstated context from experience. LLMs process documents as linear token sequences within a fixed-size context window, exhibit measurable positional attention biases, and cannot infer information that is not explicitly stated. These differences demand specific structural patterns: BLUF (Bottom Line Up Front) positioning, explicit over implicit conventions, self-contained sections, and machine-navigable metadata. The research converges on a clear finding: how documentation is structured affects LLM output quality as much as what the documentation contains.

## Sub-Questions

1. How does document position affect LLM attention and comprehension?
2. Why does BLUF structure matter more for LLMs than for humans?
3. What happens when LLMs encounter implicit rather than explicit information?
4. How should sections be structured for independent comprehension?
5. What metadata and navigation patterns enable efficient agent discovery?
6. How does document formatting quantitatively affect LLM output quality?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. / Stanford, UC Berkeley | 2023 | T1 | verified |
| 2 | https://arxiv.org/abs/2406.16008 | Found in the Middle: Calibrating Positional Attention Bias | Hsieh et al. | 2024 | T2 | verified |
| 3 | https://arxiv.org/abs/2411.10541 | Does Prompt Formatting Have Any Impact on LLM Performance? | Siddiqui et al. | 2024 | T2 | verified |
| 4 | https://arxiv.org/abs/2602.20478 | Codified Context: Infrastructure for AI Agents in a Complex Codebase | Factory.ai | 2025 | T2 | verified |
| 5 | https://biel.ai/blog/optimizing-docs-for-ai-agents-complete-guide | Optimizing Docs for AI Agents: Complete Guide | Biel.ai | 2025 | T3 | verified |
| 6 | https://docs.kapa.ai/improving/writing-best-practices | Writing Documentation for AI: Best Practices | Kapa.ai | 2025 | T3 | verified |
| 7 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic | 2025 | T1 | verified |
| 8 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill Authoring Best Practices | Anthropic | 2025 | T1 | verified |
| 9 | https://llmstxt.org/ | The /llms.txt File Specification | Jeremy Howard / Answer.AI | 2024 | T2 | verified |
| 10 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |
| 11 | https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ | How to Write a Great agents.md: Lessons from 2,500+ Repos | GitHub | 2025 | T1 | verified |
| 12 | https://www.promptwire.co/articles/how-to-structure-content-for-llm-citations | How to Structure Content for LLM Citations | PromptWire | 2025 | T3 | verified |

## Findings

### 1. Positional Attention Bias: The U-Shaped Curve

LLMs exhibit a well-documented U-shaped attention pattern: information at the beginning and end of the context window receives stronger attention than information in the middle. The seminal "Lost in the Middle" paper demonstrated that "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle" [1]. This effect was observed across model architectures, including models explicitly designed for long contexts.

The root cause is positional attention bias — LLMs distribute attention disproportionately to boundary positions regardless of content relevance [2]. Follow-up research ("Found in the Middle") confirmed this as an intrinsic bias and proposed calibration mechanisms that improved long-context retrieval by up to 15 percentage points [2]. While newer models show improvement (Claude achieves state-of-the-art on long-context retrieval benchmarks), the effect persists to varying degrees across all current architectures.

**Implication for documentation:** Content placed in the middle of a document or context window is at highest risk of being underweighted during processing. This is not a minor effect — it produces measurable performance degradation on retrieval and question-answering tasks (HIGH — T1 peer-reviewed research, reproduced across benchmarks) [1][2].

### 2. BLUF Structure: Why Position Matters More for LLMs

Bottom Line Up Front (BLUF) is the practice of beginning a message with its key information. For human readers, BLUF is a communication preference — useful but not essential, since humans can scan backward and re-read. For LLMs, BLUF is a structural necessity dictated by the attention curve.

**Why BLUF is critical for LLM consumption:**

- **Early tokens receive disproportionate attention.** The first 100-200 tokens of a document or section establish the parsing framework that shapes how subsequent content is interpreted. Placing the core claim or instruction here ensures it lands in the model's "attentional sweet spot" [1][12].
- **Retrieval systems pre-filter by position.** In RAG pipelines, content that is difficult to parse or that buries the answer is often discarded during the retrieval phase before it ever reaches the LLM. Documents that front-load key information survive retrieval filtering at higher rates [12].
- **Context window pressure.** When agents process many documents, they may read only the opening of each to assess relevance. A document that requires 500 tokens of preamble before stating its point may never be fully read [7][8].
- **Queries at the end exploit the curve's other peak.** Anthropic's documentation confirms that placing queries and specific instructions at the end of context improves response quality "by up to 30% in tests, especially with complex, multi-document inputs" [7].

The optimal pattern for agent-facing documents mirrors the U-shaped curve: key findings first (beginning), supporting detail in the middle (acceptable degradation zone), and actionable takeaways last (end). This is the structural basis for the "key insights first and last, detail in the middle" convention (HIGH — T1 vendor documentation + T1 research converge) [1][7].

### 3. Explicit Over Implicit: LLMs Cannot Infer Unstated Context

The most fundamental difference between human and agent readers is inference. Humans fill gaps using experience, domain knowledge, organizational context, and common sense. LLMs can only work with what is explicitly stated in the context window.

**What agents cannot do:**

- **Infer cross-document relationships** unless explicitly stated in metadata (related fields, cross-references). A human reader might notice that two documents in the same directory are related; an agent processes each document as an independent token sequence [5][6].
- **Understand organizational conventions** unless documented. "We always deploy on Tuesdays" is knowledge an agent cannot derive from code. If it matters, state it [7][11].
- **Recognize implicit dependencies.** If Document A assumes the reader has read Document B, an agent processing Document A alone will miss that context. Each document must either be self-contained or explicitly declare its dependencies [6].
- **Interpret visual layout.** Agents cannot scan headings spatially. Navigation that relies on visual hierarchy (indentation patterns, color coding, spatial grouping) is invisible to LLMs. Structural signals must be encoded in text: headings, lists, metadata fields [5][8].

Anthropic's skill authoring best practices emphasize this directly: "Only add context Claude doesn't already have" — but the corollary is that all necessary context must be explicitly present [8]. The AGENTS.md specification embodies this principle: it exists to encode "the same tribal knowledge senior engineers already carry in their heads" — knowledge that is implicit for humans but must be made explicit for agents [11].

**Practical patterns for explicitness:**

- State the purpose of every section in its first sentence
- Declare all dependencies and prerequisites explicitly
- Use controlled vocabulary (consistent terminology throughout)
- Encode relationships in machine-readable metadata, not prose
- Replace "as mentioned above" with explicit back-references

(HIGH — T1 vendor docs + T3 practitioner consensus converge) [6][7][8][11].

### 4. Self-Contained Sections: Independent Comprehension Units

Agents often process individual pages or sections without broader navigation context. If a section depends on context established elsewhere in the document, an agent reading only that section will produce degraded output [5][6].

**Design principles for self-contained sections:**

- **Each section answers one question.** If a section mixes multiple topics, the agent may address the wrong one or conflate them. Keep procedures and references separate [5].
- **No forward references for critical information.** A section that says "as explained in Section 5" breaks when Section 5 is not in context. Either repeat the essential information or make the section independently useful without it.
- **Include context re-establishment.** Brief restatements at the start of each major section ("This section covers X, which is relevant when Y") cost few tokens but ensure the section is comprehensible in isolation.
- **One level of reference depth.** When a document references additional files, those references should link directly from the main document — not from referenced files to other referenced files. Deeply nested references cause agents to partially read files or miss information entirely [8].

Anthropic's skill authoring documentation explicitly warns against deeply nested references: "Claude may partially read files when they're referenced from other referenced files... resulting in incomplete information" [8]. The recommended pattern is one level of progressive disclosure — a main document that links directly to supplementary materials.

The Codified Context paper [4] found that treating documentation as "load-bearing infrastructure" — artifacts that agents depend on to produce correct output — fundamentally changes how documents should be structured. Their three-tier architecture (always-loaded conventions, per-task specialists, on-demand specifications) ensures agents always have the minimum context needed for any given task without requiring access to the full document collection (MODERATE — single study, strong architectural rationale) [4].

### 5. Navigable Metadata: Machine-Readable Discovery

Agents need structured, machine-readable signals to navigate document collections efficiently. Without metadata, an agent must read full documents to assess relevance — consuming context window tokens on exploration rather than task execution.

**Metadata patterns that enable agent navigation:**

**YAML frontmatter.** Structured fields at the top of each document (name, description, type, related, sources) let agents assess relevance from metadata alone. The description field is the agent's equivalent of information scent — a parseable signal that answers "is this document worth reading?" without consuming the full document's tokens [8].

**Index files.** Auto-generated index files that list directory contents with descriptions extracted from frontmatter. The agent reads one file to understand an entire directory, converting expensive exploration into cheap lookup. This is the single most important pattern for agent navigation in filesystem-based knowledge systems [11].

**Entrypoint files (CLAUDE.md, AGENTS.md).** A root-level file that provides orientation: what the project is, where things live, how to navigate. The agent reads this file first to bootstrap its understanding of the knowledge structure [7][11].

**The llms.txt standard** [9] extends this principle to web documentation. It provides a plain-text, Markdown-formatted map of a site's key resources, designed specifically for LLM consumption. The specification uses Markdown rather than XML because LLMs are the primary consumer. Two variants exist: llms.txt (compact overview with links) and llms-full.txt (complete content embedded directly). By stripping HTML navigation, ads, and JavaScript, llms.txt reduces token consumption by 90%+ compared to raw web pages [9].

**Progressive disclosure through metadata.** At startup, agents load only skill names and descriptions. Full content is read only when relevant. This pattern — metadata first, content on demand — keeps context lean while maintaining comprehensive coverage [8]. The Anthropic skill authoring guidelines specify that SKILL.md bodies should stay under 500 lines, with additional content split into separate reference files that load only when needed [8].

(HIGH — T1 vendor documentation + T2 standard specification converge) [7][8][9][11].

### 6. Formatting Effects on Output Quality

Document formatting has a quantitative impact on LLM output quality. Research on prompt formatting [3] tested four formats (plain text, Markdown, YAML, JSON) across GPT-3.5 and GPT-4 models and found:

- GPT-3.5-turbo's performance varied **by up to 40%** on a code translation task depending on the prompt template [3].
- On the FIND dataset, GPT-3.5 showed a **200% improvement** when switching from Markdown to plain text for that specific task [3].
- GPT-4 demonstrated substantially greater robustness to formatting variations, with consistency scores above 0.5 compared to GPT-3.5's scores below 0.5 [3].
- **No universal optimal format exists.** The best format depends on the model, the task, and the content type [3].

However, cross-source consensus identifies several formatting principles that consistently improve agent comprehension:

- **Markdown headings create parseable landmarks** that help models navigate large documents. Consistent heading levels (## for main sections, ### for subsections) establish information hierarchy [7][8].
- **Bulleted lists improve instruction following.** List items are easier for models to enumerate, track, and execute compared to the same instructions in prose [7].
- **Consistent formatting reduces ambiguity.** Using the same structural pattern throughout a document (same heading level for parallel sections, same list style) helps models maintain context about document organization [8].
- **XML tags create strong structural boundaries.** Anthropic recommends XML tags for multi-document inputs because they create unambiguous section delimiters [7].
- **Token efficiency matters.** Markdown is preferred over more verbose formats because it provides structural hierarchy with minimal token overhead [9].

(MODERATE — T2 research with quantitative results, but findings are model-dependent; T1 vendor recommendations provide practical grounding) [3][7][8].

## Challenge

**Are these patterns already obsolete?** The "Lost in the Middle" paper [1] used 2023-era models. The "Found in the Middle" paper [2] demonstrated that calibration techniques can reduce positional bias by 15 percentage points. Newer models like Claude show substantially improved long-context performance. If positional bias is a training artifact being steadily eliminated, BLUF formatting may become unnecessary.

**Counter-argument:** Even if positional bias diminishes in newer models, the other constraints remain. Context windows are finite. Token costs are real. Agents still cannot infer unstated context. Self-contained sections are valuable regardless of attention curves. BLUF is beneficial even without positional bias because it enables faster relevance assessment and supports progressive disclosure. The attention curve provides the strongest empirical justification, but it is not the only justification.

**Does explicit always beat implicit?** Over-specification can degrade LLM performance. Anthropic's best practices warn that "bloated CLAUDE.md files cause Claude to ignore your actual instructions" [7]. The skill authoring guide emphasizes that Claude "is already very smart" and authors should only add context the model does not already have [8]. The principle is not "state everything" but rather "state everything the model needs that it cannot infer from the content itself."

**Is formatting sensitivity a model-specific artifact?** GPT-4 showed much greater robustness to formatting variations than GPT-3.5 [3]. As models improve, formatting sensitivity may decrease. However, even GPT-4 showed measurable (though smaller) performance differences across formats. Consistent formatting remains a low-cost, high-value practice.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Performance is often highest when relevant information occurs at the beginning or end" | quote | [1] | verified |
| 2 | Positional attention calibration improves retrieval by up to 15 percentage points | statistic | [2] | verified |
| 3 | GPT-3.5-turbo performance varies by up to 40% based on prompt template | statistic | [3] | verified |
| 4 | GPT-3.5 showed 200% improvement switching from Markdown to plain text on FIND dataset | statistic | [3] | verified |
| 5 | Queries at the end improve response quality by up to 30% | statistic | [7] | verified |
| 6 | Documentation as "load-bearing artifacts that AI agents depend on to produce correct output" | quote | [4] | verified |
| 7 | Codified Context infrastructure reached 26,200 lines across 54 files | statistic | [4] | verified |
| 8 | llms.txt reduces token consumption by 90%+ compared to raw HTML | statistic | [9] | verified |
| 9 | SKILL.md bodies should stay under 500 lines for optimal performance | recommendation | [8] | verified |
| 10 | Claude may partially read files referenced from other referenced files | behavior | [8] | verified |
| 11 | Bloated CLAUDE.md files cause Claude to ignore instructions | behavior | [7] | verified |

## Search Protocol

| # | Query | Tool | Results | Selected |
|---|-------|------|---------|----------|
| 1 | writing documentation for LLM consumption agent-facing best practices 2025 2026 | WebSearch | 10 | 3 |
| 2 | BLUF bottom line up front LLM attention patterns document structure | WebSearch | 10 | 3 |
| 3 | "lost in the middle" LLM research paper attention long context position bias | WebSearch | 10 | 4 |
| 4 | llms.txt standard specification documentation AI agents machine readable | WebSearch | 10 | 3 |
| 5 | how document formatting structure affects LLM output quality prompt engineering markdown | WebSearch | 10 | 4 |
| 6 | Anthropic Claude documentation conventions AGENTS.md CLAUDE.md context files best practices | WebSearch | 10 | 4 |
| 7 | explicit vs implicit information LLM comprehension self-contained documentation sections AI agents | WebSearch | 10 | 3 |
| 8 | structured context for AI coding assistants YAML frontmatter metadata navigation 2025 | WebSearch | 10 | 4 |
| 9 | LLM reading comprehension document structure effects research paper 2024 2025 | WebSearch | 10 | 2 |
| 10 | AGENTS.md specification standard agent-facing documentation conventions 2025 2026 | WebSearch | 10 | 4 |
| 11 | context engineering AI agents documentation self-contained sections token efficiency 2025 | WebSearch | 10 | 4 |
| 12 | arxiv 2307.03172 Lost in the Middle abstract | WebFetch | 1 | 1 |
| 13 | arxiv 2411.10541 prompt formatting LLM performance | WebFetch | 1 | 1 |
| 14 | arxiv 2602.20478 codified context infrastructure | WebFetch | 1 | 1 |
| 15 | Anthropic Claude Code best practices | WebFetch | 1 | 1 |
| 16 | Anthropic skill authoring best practices | WebFetch | 1 | 1 |

## Takeaways

Six principles define effective agent-facing documentation, grounded in the research above:

1. **Position strategically (BLUF).** Place key findings, instructions, and constraints at the beginning and end of documents. Place supporting detail in the middle. This directly exploits the U-shaped attention curve and mirrors how retrieval systems assess relevance. The first sentence of every section should state the section's conclusion.

2. **Make everything explicit.** Agents cannot infer unstated context, organizational conventions, or cross-document relationships. If information matters for task execution, it must be stated in the document or encoded in machine-readable metadata. Replace implicit assumptions with explicit declarations.

3. **Design self-contained sections.** Each section should be independently useful without requiring context from other sections or documents. One topic per section. No forward references for critical information. Brief context re-establishment at section boundaries.

4. **Provide navigable metadata.** YAML frontmatter, index files, and entrypoint files convert expensive exploration into cheap lookup. The description field is the agent's primary relevance signal. Auto-generated indexes ensure navigation stays current with content.

5. **Use consistent, minimal formatting.** Markdown headings for hierarchy, bulleted lists for instructions, consistent patterns throughout. Over-formatting is as harmful as under-formatting. Every structural element should serve navigation or comprehension.

6. **Earn every token.** Context window space is finite and shared. Agent-facing documentation must justify its token cost through information density. Concise documentation that states only what the model needs — and cannot infer — outperforms comprehensive documentation that dilutes attention across unnecessary content.
