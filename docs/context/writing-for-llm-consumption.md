---
name: "Writing for LLM Consumption"
description: "Six structural principles for agent-facing documentation: BLUF positioning, explicit conventions, self-contained sections, navigable metadata, consistent formatting, and token efficiency"
metadata:
  type: reference
  sources:
    - https://arxiv.org/abs/2307.03172
    - https://arxiv.org/abs/2406.16008
    - https://arxiv.org/abs/2411.10541
    - https://arxiv.org/abs/2602.20478
    - https://llmstxt.org/
    - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    - https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
  related:
    - docs/research/writing-for-llm-consumption.md
    - docs/context/context-window-management.md
    - docs/context/prompt-engineering.md
---

Agent-facing documentation operates under different constraints than human-facing writing. Humans scan headings, build spatial memory, and infer unstated context from experience. LLMs process documents as linear token sequences within a fixed context window, exhibit positional attention biases, and cannot infer information that is not explicitly stated. How documentation is structured affects LLM output quality as much as what it contains.

## Position Strategically (BLUF)

LLMs exhibit a U-shaped attention pattern: content at the beginning and end of context receives stronger attention than content in the middle (Liu et al., 2023). This is not a minor effect — it produces measurable performance degradation on retrieval and QA tasks across model architectures.

Place key findings, instructions, and constraints at the beginning and end. Place supporting detail in the middle. The first sentence of every section should state its conclusion. Queries and specific instructions placed at the end of context improve response quality by up to 30% on complex multi-document inputs.

While newer models show improvement on long-context benchmarks, the bias persists to varying degrees. Even without positional bias, BLUF enables faster relevance assessment and supports progressive disclosure.

## Make Everything Explicit

The most fundamental difference between human and agent readers is inference. Agents cannot infer cross-document relationships unless declared in metadata. They cannot understand organizational conventions unless documented. They cannot recognize implicit dependencies between files.

Practical patterns: state the purpose of every section in its first sentence. Declare all dependencies explicitly. Use controlled vocabulary throughout. Encode relationships in machine-readable metadata, not prose. Replace "as mentioned above" with explicit back-references.

The principle is not "state everything" but "state everything the model needs that it cannot infer from the content itself." Over-specification degrades performance — bloated instruction files cause models to ignore actual instructions.

## Design Self-Contained Sections

Agents often process individual sections without broader document context. If a section depends on context established elsewhere, an agent reading only that section produces degraded output.

Each section should answer one question. Avoid forward references for critical information — "as explained in Section 5" breaks when Section 5 is not in context. Include brief context re-establishment at the start of major sections. Limit reference depth to one level: a main document links to supplementary materials directly, never through intermediate files. Deeply nested references cause agents to partially read files or miss information entirely.

## Provide Navigable Metadata

Without structured metadata, agents must read full documents to assess relevance, consuming context window tokens on exploration rather than task execution.

YAML frontmatter (name, description, type, related) lets agents assess relevance from metadata alone. The description field is the agent's primary relevance signal. Auto-generated index files convert expensive directory exploration into cheap lookup — the single most important pattern for agent navigation in filesystem-based knowledge systems. Entrypoint files (CLAUDE.md, AGENTS.md) provide orientation that bootstraps understanding of the knowledge structure.

Progressive disclosure through metadata keeps context lean: load only skill names and descriptions at startup, read full content only when relevant.

## Use Consistent Formatting

Document formatting has quantitative impact on LLM output quality. Research found performance variations of up to 40% based on prompt template alone, though newer models show greater robustness to formatting differences.

Markdown headings create parseable landmarks for navigating large documents. Bulleted lists improve instruction following compared to equivalent prose. XML tags create strong structural boundaries for multi-document inputs. Consistent patterns throughout a document (same heading levels for parallel sections, same list styles) reduce ambiguity. Markdown is preferred over verbose formats because it provides hierarchy with minimal token overhead.

## Earn Every Token

Context window space is finite and shared across all loaded content. Agent-facing documentation must justify its token cost through information density. Concise documentation that states only what the model needs — and cannot infer — outperforms comprehensive documentation that dilutes attention across unnecessary content. The llms.txt standard demonstrates this principle: stripping HTML navigation, ads, and scripts reduces token consumption by 90%+ compared to raw web pages.
