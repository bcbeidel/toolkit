---
name: "Writing for LLM Consumption"
description: "Investigation of document structure, formatting, and abstraction patterns for optimal LLM comprehension in agent-facing artifacts"
type: research
sources:
  - https://arxiv.org/abs/2307.03172
  - https://www.trychroma.com/research/context-rot
  - https://arxiv.org/abs/2411.10541
  - https://arxiv.org/abs/2406.15981
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
  - https://daplab.cs.columbia.edu/general/2026/03/31/your-ai-agent-doesnt-care-about-your-readme.html
  - https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
  - https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
  - https://01.me/en/2025/12/context-engineering-from-claude/
  - https://claude.com/blog/using-claude-md-files
  - https://arxiv.org/html/2504.09798v2
  - https://llmstxt.org/
  - https://agents.md/
  - https://arxiv.org/html/2502.04295v3
  - https://arxiv.org/abs/2602.11988
  - https://arxiv.org/abs/2601.20404
  - https://arxiv.org/abs/2509.21361
  - https://www.improvingagents.com/blog/best-nested-data-format/
  - https://epoch.ai/data-insights/context-windows/
related:
  - docs/research/2026-04-07-context-engineering.research.md
  - docs/research/2026-04-07-prompt-engineering.research.md
---

## Research Question

How should documents be structured, formatted, and calibrated for optimal LLM comprehension, and what thresholds trigger comprehension degradation?

## Search Protocol

| # | Query | Source | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | writing documents for LLM consumption best practices 2025 2026 | WebSearch | 10 | 3 |
| 2 | Anthropic documentation best practices structuring context for Claude agents | WebSearch | 10 | 5 |
| 3 | LLM reading comprehension document structure research primacy recency effect | WebSearch | 10 | 4 |
| 4 | markdown vs XML vs plain text LLM prompt parsing accuracy structured input | WebSearch | 10 | 5 |
| 5 | LLM context window length degradation comprehension threshold tokens 2025 | WebSearch | 10 | 5 |
| 6 | agent-facing documentation patterns abstraction level AI agents vs human readable docs | WebSearch | 10 | 5 |
| 7 | llms.txt specification standard machine readable documentation site | WebSearch | 10 | 3 |
| 8 | "lost in the middle" LLM information retrieval position effect Liu 2023 | WebSearch | 10 | 3 |
| 9 | prompt formatting impact LLM performance research paper arxiv 2024 2025 | WebSearch | 10 | 4 |
| 10 | AGENTS.md specification standard AI coding agents documentation convention 2025 | WebSearch | 10 | 4 |
| 11 | CLAUDE.md file specification project instructions Claude Code context file best practices | WebSearch | 10 | 3 |
| 12 | XML tags structured prompting LLM accuracy improvement Claude Anthropic research evidence | WebSearch | 10 | 3 |
| 13 | tools libraries LLM-optimized documentation generation markdownlint linter AI readability | WebSearch | 10 | 4 |
| 14 | context engineering AI agents 2025 2026 techniques token optimization | WebSearch | 10 | 4 |
| 15 | agentic content design guidelines writing for AI agents UX patterns 2025 2026 | WebSearch | 10 | 2 |
| 16 | "writing for AI" structured content headings sections ordering key information first last middle | WebSearch | 10 | 3 |

## Sources

| # | Source | Tier | Status |
|---|--------|------|--------|
| 1 | Liu et al. "Lost in the Middle: How Language Models Use Long Contexts" (TACL 2024, arXiv 2307.03172) | T1 | verified |
| 2 | Chroma Research. "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (2025) | T2 | verified |
| 3 | Agrawal et al. "Does Prompt Formatting Have Any Impact on LLM Performance?" (arXiv 2411.10541, Nov 2024) | T1 | verified |
| 4 | Wu et al. "Serial Position Effects of Large Language Models" (ACL Findings 2025, arXiv 2406.15981) | T1 | verified |
| 5 | Anthropic. "Effective Context Engineering for AI Agents" (2025) | T1 | verified |
| 6 | Anthropic. "Prompting Best Practices" (Claude API Docs, 2025-2026) | T1 | verified |
| 7 | Anthropic. "Use XML Tags to Structure Your Prompts" (Claude API Docs) | T1 | verified |
| 8 | Columbia DAPLab. "Your AI Agent Doesn't Care About Your README" (Mar 2026) | T2 | verified |
| 9 | GitHub Blog. "How to Write a Great agents.md: Lessons from Over 2,500 Repositories" (2025) | T1 | verified |
| 10 | Manus. "Context Engineering for AI Agents: Lessons from Building Manus" (2025) | T2 | verified |
| 11 | Li. "Claude's Context Engineering Secrets: Best Practices Learned from Anthropic" (Dec 2025) | T3 | verified |
| 12 | Anthropic. "Using CLAUDE.md Files: Customizing Claude Code for Your Codebase" (2025) | T1 | verified |
| 13 | Giordano et al. "ReadMe.LLM: A Framework to Help LLMs Understand Your Library" (arXiv 2504.09798, 2025) | T1 | verified |
| 14 | Howard. "The /llms.txt File" (llmstxt.org, 2024) | T2 | verified |
| 15 | agents.md specification (agentsmd/agents.md, 2025) | T1 | verified |
| 16 | Chen et al. "Beyond Prompt Content: Content-Format Integrated Prompt Optimization" (arXiv 2502.04295, 2025) | T1 | verified |
| 17 | Gloaguen et al. "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" (ETH Zurich, arXiv 2602.11988, Feb 2026) | T1 | verified |
| 18 | Gallotta et al. "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents" (arXiv 2601.20404, Jan 2026) | T1 | verified |
| 19 | Paulsen. "Context Is What You Need: The Maximum Effective Context Window for Real World Limits of LLMs" (arXiv 2509.21361, Sep 2025) | T1 | verified |
| 20 | ImprovingAgents. "Which Nested Data Format Do LLMs Understand Best? JSON vs. YAML vs. XML vs. Markdown" (Oct 2025) | T2 | verified |
| 21 | Epoch AI. "LLMs now accept longer inputs, and the best models can use them more effectively" (2025-2026) | T2 | verified |

## Raw Extracts

### Sub-question 1: Document structure for LLM comprehension

**Lost-in-the-Middle Effect (Liu et al., 2024)**

Performance is highest when relevant information is at the beginning or end of context, and significantly degrades when models must access information in the middle. This holds across multi-document QA and key-value retrieval tasks. The finding has been replicated across model families and context lengths.

- Placing queries at the end of long documents improves response quality by up to 30% (Anthropic docs).
- Serial position effects are consistent across various LLMs, suggesting SPE is a general characteristic of generative models (Wu et al., 2025).
- In summarization tasks, a recency effect appears with few documents, but as length increases, the model's focus shifts to the beginning, with middle sections becoming "dead zones" for retrieval.

**Structural Coherence Hurts (Chroma, 2025)**

Counter-intuitively, models perform better on shuffled haystacks than on logically structured ones. Structural coherence consistently hurts performance, suggesting attention mechanisms respond differently to organized input in ways that can mask needle signals.

**Key-Insights-First Pattern**

State the answer in the first 1-2 sentences of each section without lengthy exposition. AI tools often pull the first sentence as the core summary; if it's vague or buried, content won't be selected (multiple SEO/GEO sources). Each section should be self-contained and understandable without relying on surrounding text.

**Heading Structure**

Descriptive headings act as semantic markers. Use headings that mirror real queries rather than vague labels (e.g., "How Adaptive Reuse Impacts Asset Value" over "Looking Ahead"). Hierarchy: H1 page title, H2 major sections, H3 subtopics, H4 deeper explanations.

**Anthropic's Ordering Recommendation**

Put longform data at the top of prompts, above queries, instructions, and examples. Documents first, questions last. Structure multi-document input with XML tags using `<document>` wrappers with `<source>` and `<document_content>` subtags.

**Manus Attention Manipulation**

Push objectives to context end to combat lost-in-the-middle. Manus agents maintain a `todo.md` file updated step-by-step, keeping current objectives at the tail of context. Average agent task length: ~50 tool calls.

### Sub-question 2: Formatting choices and parsing accuracy

**Format Performance Variance (Agrawal et al., 2024)**

Testing plain text, Markdown, JSON, and YAML across GPT models:
- GPT-3.5-turbo performance varies up to 40% depending on prompt template (code translation task).
- Specific ranges: MMLU 50.0% (Markdown) to 59.7% (JSON); HumanEval 40.2% (plain text) to 59.8% (JSON).
- GPT-4 is more robust but still shows variation: HumanEval anomaly with JSON (21.95%) vs plain text (76.2%).
- No universal optimal format; best format depends on model AND task.
- Only 16% identical responses between Markdown and JSON on MMLU (GPT-3.5).
- Models from the same sub-series show IoU > 0.7 for format preferences; cross-series IoU often below 0.2.
- All statistical tests showed p-values below 0.05, confirming format sensitivity is significant.

**Format-Content Interaction (Chen et al., 2025)**

Different LLMs have distinct format preferences. Formats performing well on one model sometimes fail on another. Even within a single LLM, the optimal format varies by prompt content. One-size-fits-all formatting is unlikely to succeed.

**XML vs Markdown Trade-offs**

XML advantages:
- Multi-line certainty with explicit open/close delimiters.
- Better control for highly structured, interdependent, or nested content.
- Claude was specifically trained with XML tags, improving parsing reliability.
- Anthropic heavily uses XML tags internally (documented in leaked prompts and official docs).
- Queries at the end of XML-structured multi-document input improve quality by up to 30%.

Markdown advantages:
- ~15% fewer tokens than equivalent XML representations.
- Reduced processing overhead; straightforward syntax.
- Better for simple, flat content where nesting is unnecessary.
- Readability for both humans and machines.

**Anthropic's Specific Recommendations**

- Use XML tags when prompts mix instructions, context, examples, and variable inputs.
- Use consistent, descriptive tag names.
- Nest tags for natural hierarchies (e.g., `<documents>` containing `<document index="n">`).
- Wrap examples in `<example>` tags to distinguish them from instructions.
- 3-5 examples is the sweet spot for few-shot prompting.

**Prompt Brittleness**

LLMs are sensitive to meaning-preserving changes like extra spaces, colon variations, or few-shot example ordering. This "prompt brittleness" is underappreciated (NAACL 2025).

### Sub-question 3: Abstraction calibration for agent vs. human docs

**Agent Documentation Is Fundamentally Different**

Agents need "insight into where things live, what rules to follow, and how to implement changes" rather than high-level overviews humans can infer. Traditional README files fail agents because they contain "fluff" irrelevant to programmatic task execution (Columbia DAPLab, 2026).

**AGENTS.md Standard**

Adopted by 20,000+ GitHub repositories. Donated to Linux Foundation's Agentic AI Foundation (AAIF) in December 2025. Core sections that put repositories in the top tier: commands, testing, project structure, code style, git workflow, and boundaries (GitHub Blog analysis of 2,500+ repos).

Effective patterns:
- Specificity over generality: "React 18 with TypeScript, Vite, and Tailwind CSS" beats "React project."
- Executable commands early (agents frequently reference them).
- One real code snippet beats three paragraphs describing conventions.
- Three-tier boundaries: Always do, Ask first, Never do.
- Concrete persona: "test engineer who writes tests for React components" beats "helpful coding assistant."

**CLAUDE.md Calibration**

- Keep under 200 lines / 200-800 words.
- Every line costs context tokens; expand deliberately based on actual friction, not theoretical concerns.
- Later-loaded files have higher effective priority (recency effect in context).
- Define standard workflows (explore, plan, implement, test) rather than abstract goals.

**ReadMe.LLM Framework (Giordano et al., 2025)**

Providing traditional ReadMe.md files alone actually DECREASED performance for some models. DeepSeek R1 showed performance degradation with human-facing documentation. LLMs process human-optimized formats poorly.

ReadMe.LLM structure (XML-tagged):
- Rules: guidelines instructing the LLM on processing.
- Library Description: concise overview of purpose and core functionalities.
- Code Snippets: function signatures paired with usage examples.

Results: ~5x correctness improvement over baseline. Zero-shot baseline averaged 30% success; with ReadMe.LLM, near-perfect accuracy across most models. Key finding: include function signatures and examples, but EXCLUDE full implementation code (causes hallucinations due to excessive length).

**Abstraction Level Guidance**

Anthropic's "altitude calibration" principle: be "specific enough to guide behavior effectively, yet flexible enough to provide strong heuristics." Start with the smallest viable prompt, then iteratively add based on observed failures, not anticipated edge cases.

Agent-facing artifacts should favor:
- Explicit file paths and concrete commands over descriptions.
- Flat structure over deep nesting.
- Single-concept sections over multi-topic narratives.
- Constraints and boundaries over aspirational guidance.

**Size Constraints (Columbia DAPLab)**

- Maximum 8,000 characters per agent-facing file.
- Maximum 40,000 characters total per directory.
- OpenAI recommends ~100 lines for agent.md files.
- Hierarchical organization: multiple files per subfolder rather than single global files.

### Sub-question 4: Length and complexity degradation thresholds

**Context Rot (Chroma, 2025)**

Tested 18 frontier models (Claude Opus 4, Sonnet 4, GPT-4.1, Gemini 2.5, Qwen3). Every model exhibits performance degradation at every input length increment tested. Key findings:

- A model with a 200K token window can exhibit significant degradation at 50K tokens.
- Maximum Effective Context Window (MECW) falls far below advertised maximum, by up to 99% on some tasks.
- Attention degradation is non-linear past the effective ceiling.
- Gemini 1.5 maintains recall up to 1M tokens but average recall hovers around 60% (40% of facts effectively lost).

Specific degradation mechanisms:
1. **Lost-in-the-middle effect**: 30%+ accuracy drops for mid-context information.
2. **Attention dilution**: 100K tokens = 10 billion pairwise attention relationships.
3. **Distractor interference**: Semantically similar but irrelevant content actively misleads.

**Repeated Words Task (Chroma)**

Performance consistently degrades across all models as context length increases. Tested at: 25, 50, 75, 100, 250, 500, 750, 1,000, 2,500, 5,000, 7,500, 10,000 words. Unique word placement accuracy highest when placed near the beginning.

**Distractor Effects**

- Single distractors reduce performance relative to needle-only baselines.
- Multiple distractors compound degradation further.
- Claude models exhibited lowest hallucination rates; GPT models highest.
- Structural coherence hurts: models perform better on shuffled haystacks than logically structured ones.

**LongMemEval Results**

Significant performance gap between focused prompts (~300 tokens) and full prompts (~113K tokens). Pattern holds across GPT, Gemini, Claude, and Qwen families. Thinking mode improved performance but the gap persisted.

**Practical Token Thresholds**

- Llama 3.1 405B: optimal performance after 32K tokens.
- General pattern: degradation begins well before advertised context limits.
- Real-world applications involving synthesis or multi-step reasoning see even more severe degradation than controlled experiments.
- Token complexity: most questions have a minimum number of tokens required to solve; this predicts performance with 95% accuracy.

**Document Length Guidance**

- Context files: target 200-800 words (WOS convention, consistent with CLAUDE.md guidance).
- Agent-facing files: maximum 8,000 characters per file, 40,000 per directory (Columbia DAPLab).
- CLAUDE.md: under 200 lines (Anthropic recommendation).
- SKILL.md: under 500 lines before splitting (Anthropic/Claude Code conventions).
- Reference files: ~100 lines threshold for directory organization.
- 100 tokens ~ 75 words; document-level budgets matter more than absolute context limits.

**Compression Techniques (Manus, Anthropic)**

- Compression can reduce token usage by 80% while preserving important information.
- ACON (Agent Context Optimization) reduces peak token usage 26-54% while preserving 95%+ task accuracy.
- Anthropic's five context operations: select, compress, order, isolate, format.
- KV-cache hit: 10x cost reduction (cached tokens $0.30/MTok vs uncached $3/MTok for Claude Sonnet).
- All compression should be reversible (Manus principle): drop content but preserve URLs for restoration.

### Canonical Tools & Libraries

| Tool | Purpose | Notes |
|------|---------|-------|
| **llms.txt / llmstxt.org** | Standard for exposing site content to LLMs | Proposed by Jeremy Howard (Answer.AI, 2024). Markdown file at site root with H1 project name, blockquote summary, H2 sections with prioritized links. Generates /llms.txt and /llms-full.txt. |
| **AGENTS.md** | Open standard for AI coding agent documentation | 20K+ repos adopted. Donated to Linux Foundation AAIF Dec 2025. Markdown file at repo root with commands, testing, structure, style, workflow, boundaries. |
| **CLAUDE.md** | Claude Code project context specification | Loaded every session. Hierarchical (global, project, folder). Later files have higher priority. Under 200 lines recommended. |
| **Mintlify** | Documentation platform with llms.txt generation | Auto-generates llms.txt, llms-full.txt. Supports `<llms-only>` and `<llms-ignore>` tags for selective AI exposure. |
| **Fern** | API documentation with LLM optimization | Auto-generates llms.txt/llms-full.txt. Detects LLM bot traffic, serves markdown instead of HTML. Claims 90%+ token reduction. |
| **GitBook** | Documentation with llms.txt support | Added llms.txt support Jan 2025, llms-full.txt and .md page support June 2025. |
| **ReadMe.LLM** | Framework for LLM-oriented library documentation | XML-tagged structure (rules, description, code snippets). ~5x correctness improvement. Human README alone can decrease performance. |
| **markdownlint** | Markdown style enforcement | Supports style files for rule configuration. Ensures clean, consistent markdown for both human and LLM consumption. |
| **Redocly** | API docs platform with linting | Automatic detection of terminology inconsistencies. LLM-readability optimization features. |
| **gptlint** | LLM-powered code linter | Uses LLMs to enforce best practices beyond traditional static analysis. |

## Challenge

### Gaps Identified

**1. AGENTS.md effectiveness is empirically contested, not established.**

The document presents AGENTS.md adoption (20K+ repos, Linux Foundation donation) as evidence of value, citing GitHub's analysis of 2,500+ repositories. But two peer-reviewed papers from early 2026 challenge this narrative directly:

- Gloaguen et al. (ETH Zurich, arXiv 2602.11988) found that context files **reduce task success rates** compared to providing no repository context, while increasing inference cost by over 20%. LLM-generated context files had a marginal negative effect; developer-written ones provided only a marginal positive effect.
- Gallotta et al. (arXiv 2601.20404) found the opposite on efficiency: AGENTS.md reduced median runtime by 28.6% and output tokens by 16.6%.

These two studies directly contradict each other on key metrics. The document treats AGENTS.md as an unambiguously positive pattern. It should instead present the contested evidence and note that adoption volume is not evidence of effectiveness.

**2. "Structural coherence hurts" is presented without sufficient qualification.**

The Chroma finding that shuffled haystacks outperform coherent ones is reported twice (Sub-questions 1 and 4) as a general principle. But this was measured on needle-in-a-haystack retrieval tasks, not on comprehension, reasoning, or instruction-following tasks. The mechanism (disrupted logical flow makes needles more salient) may not generalize to agent-facing documentation where the model needs to understand and apply instructions holistically, not retrieve a single fact from noise.

**3. Lost-in-the-middle is presented as a settled, immutable finding.**

The document frames the lost-in-the-middle effect as a universal characteristic of LLMs. More recent evidence complicates this:

- Epoch AI reports that the input length where top models reach 80% accuracy has risen by over 250x in 9 months.
- Anthropic Claude 4 Sonnet shows less than 5% accuracy degradation across its full context window.
- Databricks reports that recent models (gpt-4o, claude-3.5-sonnet) show "little to no performance deterioration" as context length increases.

The effect is real but its severity is model-dependent and rapidly improving. The document should distinguish between the general principle (position matters) and the degree (which is shrinking in frontier models).

**4. XML advantage for Claude is overstated relative to the broader landscape.**

The document heavily favors XML for structured content, citing Claude's specific training on XML tags. But recent benchmarking (ImprovingAgents, Oct 2025) found that YAML outperformed XML by 17.7 percentage points on GPT-5 Nano, and XML was the worst-performing format on Gemini 2.5 Flash Lite. XML required 80% more tokens than Markdown for equivalent data. The document acknowledges format-model dependence (Chen et al.) but then proceeds to present XML as the recommended choice without adequately emphasizing that this recommendation is Claude-specific and may actively harm performance on other models.

**5. Document length thresholds lack primary evidence.**

The "200-800 words" target for context files, "8,000 characters per file," and "40,000 characters per directory" are presented as research-backed thresholds. But:

- The 200-800 word range appears to be a WOS convention bootstrapped from Anthropic's CLAUDE.md guidance, not derived from controlled experiments.
- The 8,000/40,000 character limits come from a single Columbia DAPLab blog post (T2 source), not peer-reviewed research.
- Paulsen (arXiv 2509.21361) found some models fail at as few as 100 tokens, while others handle 200K+. Fixed word-count thresholds obscure this massive model-dependent variance.

**6. The "reasoning models reduce prompting burden" trajectory is absent.**

The document does not address the emerging evidence that reasoning models (o1, o3, Claude with extended thinking) are substantially more robust to prompt formatting variations. Multiple sources note that elaborate prompting and structural optimization matter less when models can decompose problems and self-correct. This is a significant omission because it affects how durable the document's recommendations are.

**7. ReadMe.LLM's "5x improvement" needs context.**

The ~5x correctness improvement is striking but was measured on library API usage tasks with niche libraries where baseline performance was 0-40%. The improvement is real but context-specific: it measures going from "model has never seen this library" to "model has a cheat sheet." This does not generalize to documentation patterns for well-known frameworks or project-specific context files.

### Counter-Evidence

| Claim in Document | Counter-Evidence | Source |
|---|---|---|
| AGENTS.md is an effective standard (20K+ repos, top-tier patterns) | Context files reduce task success rates vs. no context; increase inference cost 20%+ | Gloaguen et al. (arXiv 2602.11988) |
| AGENTS.md improves agent performance | Efficiency improved (28.6% faster runtime), but effectiveness (task completion) not clearly improved | Gallotta et al. (arXiv 2601.20404) |
| Lost-in-the-middle is a general LLM characteristic | Claude 4 Sonnet shows <5% degradation across full window; top models improved 250x in 9 months | Epoch AI; Anthropic benchmarks |
| Structural coherence hurts performance | Finding specific to needle-in-haystack retrieval; no evidence for instruction-following or comprehension tasks | Chroma methodology limitation |
| XML is recommended for structured content | XML worst-performing format on GPT-5 Nano and Gemini 2.5 Flash Lite; YAML outperformed by 17.7pp; XML uses 80% more tokens than Markdown | ImprovingAgents benchmark (Oct 2025) |
| Fixed length thresholds (200-800 words, 8K chars) | MECW varies by orders of magnitude across models; some fail at 100 tokens, others handle 200K+ | Paulsen (arXiv 2509.21361) |
| ReadMe.LLM achieves ~5x improvement | Measured on niche libraries with 0-40% baselines; may not generalize to well-known codebases | ReadMe.LLM paper scope |
| LLM-generated context files are useful | LLM-generated files mostly repeat discoverable information; add cost without adding value for well-documented repos | Gloaguen et al. (arXiv 2602.11988) |

### Confidence Assessment

| Section | Confidence | Notes |
|---|---|---|
| Lost-in-the-middle (general principle) | **High** | Well-replicated across studies, but severity is model-dependent and improving rapidly |
| Context rot / degradation thresholds | **High** | Consistent findings across multiple studies; specific thresholds are model-dependent |
| Format sensitivity exists | **High** | Multiple studies confirm format matters; Agrawal et al. is well-designed |
| XML superiority for Claude | **Medium** | Anthropic confirms Claude was trained on XML, but advantage magnitude is unquantified in public research |
| XML as general recommendation | **Low** | Counter-evidence shows XML is worst format for some 2025-2026 models; recommendation is Claude-specific |
| AGENTS.md effectiveness | **Low** | Two peer-reviewed studies with contradictory findings; adoption is not evidence of value |
| Document length thresholds | **Low-Medium** | Reasonable heuristics but not empirically derived; high variance across models |
| Key-insights-first pattern | **Medium** | Follows from primacy effect research, but mostly supported by SEO/GEO sources (T3), not LLM-specific studies |
| Structural coherence hurts | **Low** | Single study, narrow task type (retrieval), counter-intuitive enough to warrant replication |
| ReadMe.LLM 5x improvement | **Medium** | Replicable within its scope, but scope is narrow (niche library API tasks) |

### Recommendations

1. **Add the ETH Zurich AGENTS.md studies.** The document's treatment of AGENTS.md as an unambiguously positive pattern is not supported by the empirical literature. Present both the efficiency gains (Gallotta) and the effectiveness concerns (Gloaguen). Note the key finding: signal-to-noise ratio matters more than comprehensiveness, and a 5-line context file addressing project-specific quirks outperforms a 2,000-word generated overview.

2. **Qualify the lost-in-the-middle effect with temporal context.** Add a paragraph noting that frontier models (Claude 4 Sonnet, GPT-4o) show dramatically reduced position bias compared to the 2023 models originally studied. The principle remains valid for prompt design, but the degree of concern should be calibrated to the target model generation.

3. **Reframe format recommendations as model-specific.** Replace the implicit "use XML for structured content" recommendation with an explicit model-conditional recommendation. For Claude: XML. For GPT-5 family and Gemini 2.5: test YAML and Markdown first. For cross-model content: prefer Markdown (fewest tokens, broadest acceptable performance).

4. **Distinguish heuristic thresholds from empirical thresholds.** Label the 200-800 word and 8K character limits as "practitioner heuristics" rather than research-derived findings. Reference Paulsen's MECW research to explain why fixed thresholds are inherently approximate.

5. **Add a section on reasoning model robustness.** The document's recommendations may be partially obsolete for reasoning-capable models (o1/o3, extended thinking modes) that show reduced sensitivity to prompt formatting and structural choices. This trajectory should be acknowledged.

6. **Scope the "structural coherence hurts" finding.** Explicitly limit this to needle-retrieval tasks. Add a note that for instruction-following contexts (which is what agent documentation is), coherence likely helps comprehension, and no counter-evidence exists for that task type.

7. **Add the Paulsen MECW paper to the degradation thresholds section.** It is the most rigorous treatment of the gap between advertised and effective context windows and directly supports the document's core argument while adding precision.

## Findings

### 1. How should documents be structured for optimal LLM comprehension?

**Place key insights at the beginning and end; middle sections are retrieval dead zones** (HIGH — T1 [1][4], improving in frontier models). The lost-in-the-middle effect causes 30%+ accuracy drops at middle positions. Serial position effects are consistent across model families [4]. Placing queries at the end of long documents improves quality by up to 30% (vendor-reported [6]). However, frontier 2025-2026 models (Claude 4 Sonnet, GPT-4o) show substantially reduced position bias — <5% degradation across full windows [21].

**Each section should be self-contained with answer-first structure** (MODERATE — T2/T3 practitioner consensus [10]). State the answer in the first 1-2 sentences. Descriptive headings act as semantic markers — use headings that mirror real queries. Manus agents push objectives to context end via a continuously updated `todo.md` file [10].

**Structural coherence may hurt retrieval but likely helps comprehension** (LOW — single T2 study [2], narrow task type). Chroma found shuffled haystacks outperform coherent ones, but this was measured on needle-in-haystack retrieval, not instruction-following. For agent documentation where holistic understanding matters, coherence likely helps — no counter-evidence exists for that task type.

### 2. What formatting choices affect LLM parsing accuracy?

**Format sensitivity is real and significant** (HIGH — T1 [3][16]). Prompt format can swing GPT-3.5 performance by up to 40% [3]. Only 16% identical responses between Markdown and JSON on MMLU. No universal best format exists — optimal format depends on both model AND task [16].

**XML is recommended for Claude; other models may prefer different formats** (MODERATE — T1 vendor [7], counter-evidence [20]). Claude was specifically trained on XML tags, providing better control for structured, nested content. However, YAML outperformed XML by 17.7pp on GPT-5 Nano, and XML was the worst format on Gemini 2.5 Flash Lite [20]. XML uses ~80% more tokens than Markdown. For cross-model content, Markdown is the safest default (fewest tokens, broadest acceptable performance).

**Prompt brittleness is underappreciated** (HIGH — T1 [3]). LLMs are sensitive to meaning-preserving changes — extra spaces, colon variations, few-shot example ordering all affect output. This fragility is a fundamental challenge for standardized documentation.

### 3. How should abstraction be calibrated for agent-facing vs. human-facing docs?

**Agent documentation is fundamentally different from human documentation** (HIGH — converging T1/T2 evidence [8][9][13]). Agents need file paths, commands, and constraints — not narratives. Human-optimized README files can actually *decrease* LLM performance [13]. Traditional READMEs contain "fluff" irrelevant to programmatic task execution [8].

**AGENTS.md effectiveness is empirically contested** (LOW confidence — conflicting T1 studies [17][18]). Gallotta et al. found AGENTS.md reduced runtime by 28.6% and tokens by 16.6% [18]. But Gloaguen et al. (ETH Zurich) found context files *reduce* task success rates and increase inference costs by 20%+ [17]. Reconciliation: minimal, human-curated files addressing project-specific quirks help; verbose or auto-generated files hurt. Signal-to-noise ratio matters more than comprehensiveness.

**ReadMe.LLM achieves ~5x correctness improvement in scope** (MODERATE — T1 [13], narrow scope). XML-tagged structure with rules, library description, and code snippets dramatically improves LLM performance on niche library API tasks. Key finding: include function signatures and examples but EXCLUDE full implementation code (causes hallucinations). Note: baseline was 0-40% on unfamiliar libraries; improvement may not generalize to well-known frameworks.

**Practical calibration guidance** (MODERATE — converging sources [5][9][12]):
- Explicit file paths and concrete commands over descriptions
- Flat structure over deep nesting; single-concept sections
- Constraints and boundaries over aspirational guidance
- Three-tier boundaries: Always do / Ask first / Never do [9]
- One real code snippet beats three paragraphs describing conventions [9]

### 4. What length and complexity thresholds trigger degradation?

**Every model degrades at every length increment** (HIGH — T1 [2][19]). Chroma tested 18 frontier models; all degraded. Maximum Effective Context Window (MECW) can fall 99% below advertised limits on some tasks [19]. A 200K-window model can exhibit significant degradation at 50K tokens. However, the trajectory is improving: top models' 80% accuracy threshold rose 250x in 9 months [21].

**Practitioner heuristics for document sizing** (LOW-MEDIUM — these are conventions, not empirically derived thresholds):
- Context files: 200-800 words (WOS/CLAUDE.md convention)
- Agent-facing files: max 8,000 characters per file, 40,000 per directory [8]
- CLAUDE.md: under 200 lines [12]
- SKILL.md: under 500 lines before splitting [6]
- These are reasonable heuristics but Paulsen's MECW research shows massive model-dependent variance — some models fail at 100 tokens, others handle 200K+ [19]

**Compression mitigates degradation** (MODERATE — T1/T2 [5][10]). ACON reduces peak token usage 26-54% while preserving 95%+ task accuracy. KV-cache hits provide 10x cost reduction. All compression should be reversible — drop content but preserve URLs for restoration [10].

### Canonical Tools

| Tool | Purpose | Quality Signal |
|------|---------|---------------|
| [llms.txt](https://llmstxt.org/) | LLM-optimized site documentation | Emerging standard; adopted by Mintlify, Fern, GitBook |
| [AGENTS.md](https://agents.md/) | Cross-tool agent instruction files | Linux Foundation; 20K+ repos; contested effectiveness |
| [ReadMe.LLM](https://arxiv.org/html/2504.09798v2) | LLM-oriented library docs | ~5x improvement in scope; peer-reviewed |
| [markdownlint](https://github.com/DavidAnson/markdownlint) | Markdown style enforcement | Clean, consistent markdown for human and LLM consumption |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Format can swing GPT-3.5 performance by 40% | statistic | [3] | verified — peer-reviewed |
| 2 | Queries at end improve quality by up to 30% | statistic | [6] | caution — vendor claim, no transparent methodology |
| 3 | AGENTS.md reduces runtime by 28.6% | statistic | [18] | verified — but contradicted by [17] on effectiveness |
| 4 | Context files reduce task success rates | finding | [17] | verified — ETH Zurich, 138 repos |
| 5 | ReadMe.LLM achieves ~5x correctness improvement | statistic | [13] | verified — peer-reviewed, narrow scope |
| 6 | Human README alone decreases LLM performance | finding | [13] | verified — DeepSeek R1 specifically |
| 7 | MECW can fall 99% below advertised limits | statistic | [19] | verified — peer-reviewed |
| 8 | Every model degrades at every length increment | finding | [2] | verified — 18 models tested |
| 9 | Shuffled haystacks outperform coherent ones | finding | [2] | verified for retrieval — not tested on instruction-following |
| 10 | YAML outperformed XML by 17.7pp on GPT-5 Nano | statistic | [20] | verified — T2 benchmark |
| 11 | XML uses 80% more tokens than Markdown | statistic | [20] | verified — T2 benchmark |
| 12 | 200-800 word target for context files | heuristic | [12] | practitioner convention — not empirically derived |
