---
name: "Prompt Engineering & Instruction Design"
description: "Investigation of prompt structures, instruction design patterns, and empirical techniques for reliable LLM instruction-following"
type: research
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
  - https://arxiv.org/html/2312.16171v1
  - https://arxiv.org/abs/2512.14982
  - https://arxiv.org/abs/2406.06608
  - https://learnprompting.org/blog/the_prompt_report
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://code.claude.com/docs/en/best-practices
  - https://www.trychroma.com/research/context-rot
  - https://factory.ai/news/context-window-problem
  - https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
  - https://claudelab.net/en/articles/claude-code/claude-md-agents-md-complete-guide
  - https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
  - https://agents.md/
  - https://github.com/agentsmd/agents.md
  - https://openai.com/index/the-instruction-hierarchy/
  - https://arxiv.org/abs/2404.13208
  - https://scalablehuman.com/2025/07/02/review-anthropics-prompt-engineering-guide/
  - https://arxiv.org/abs/2307.03172
  - https://learnprompting.org/docs/advanced/self_criticism/self_verification
  - https://arxiv.org/abs/2308.00436
  - https://dspy.ai/
  - https://github.com/stanfordnlp/dspy
  - https://github.com/promptfoo/promptfoo
  - https://langfuse.com/
  - https://github.com/langfuse/langfuse
  - https://github.com/anthropics/prompt-eng-interactive-tutorial
  - https://github.com/anthropics/courses
  - https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference
  - https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026
  - https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639
  - https://gail.wharton.upenn.edu/research-and-insights/tech-report-prompt-engineering-is-complicated-and-contingent/
  - https://arxiv.org/abs/2506.14641
  - https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/
  - https://arxiv.org/abs/2507.11538
  - https://arxiv.org/abs/2508.07479
related:
---

## Research Question

What prompt structures and instruction design patterns produce the most reliable LLM behavior for system-level prompts, and what empirical evidence supports current best practices?

## Search Protocol

| # | Query | Engine | Results Used | Date |
|---|-------|--------|-------------|------|
| 1 | Anthropic prompt engineering best practices 2025 2026 system prompts | WebSearch | 4 | 2026-04-08 |
| 2 | "Principled Instructions Are All You Need" Bsharat 2023 prompt engineering principles | WebSearch | 3 | 2026-04-08 |
| 3 | XML tags structured prompts Claude compliance instruction following | WebSearch | 4 | 2026-04-08 |
| 4 | CLAUDE.md best practices writing effective agent instructions 2025 2026 | WebSearch | 5 | 2026-04-08 |
| 5 | "Repeat After Me" Google 2025 prompt repetition instruction following LLM | WebSearch | 4 | 2026-04-08 |
| 6 | prompt length instruction adherence LLM context window degradation 2025 | WebSearch | 5 | 2026-04-08 |
| 7 | few-shot prompting examples GPT Claude Gemini comparison compliance rates 2025 | WebSearch | 3 | 2026-04-08 |
| 8 | prompt engineering survey 2025 2026 systematic review techniques effectiveness | WebSearch | 4 | 2026-04-08 |
| 9 | role assignment system prompts LLM empirical evidence effectiveness 2025 | WebSearch | 4 | 2026-04-08 |
| 10 | self-check self-verification prompts LLM accuracy improvement technique | WebSearch | 4 | 2026-04-08 |
| 11 | open source prompt engineering tools libraries frameworks 2025 2026 | WebSearch | 4 | 2026-04-08 |
| 12 | context engineering AI agents best practices 2025 2026 system prompt design | WebSearch | 3 | 2026-04-08 |
| 13 | DSPy prompt optimization library programmatic prompting 2025 | WebSearch | 3 | 2026-04-08 |
| 14 | chain of thought prompting empirical results 2024 2025 reasoning improvement | WebSearch | 4 | 2026-04-08 |
| 15 | instruction following benchmark IFEval LLM compliance evaluation 2025 | WebSearch | 3 | 2026-04-08 |
| 16 | AGENTS.md specification coding agents instruction file format Codex Cursor 2025 | WebSearch | 4 | 2026-04-08 |
| 17 | structured output JSON mode LLM instruction following format compliance 2025 | WebSearch | 3 | 2026-04-08 |
| 18 | anthropic prompt engineering interactive tutorial github cookbook examples | WebSearch | 2 | 2026-04-08 |
| 19 | PromptFoo prompt testing evaluation framework open source 2025 | WebSearch | 2 | 2026-04-08 |
| 20 | instruction hierarchy system prompt priority user prompt OpenAI 2024 | WebSearch | 3 | 2026-04-08 |
| 21 | "lost in the middle" LLM attention position effect long context 2024 2025 | WebSearch | 3 | 2026-04-08 |
| 22 | prompt injection defense system prompt security best practices 2025 | WebSearch | 2 | 2026-04-08 |
| 23 | Claude Code CLAUDE.md instruction following limits how many instructions can LLM follow | WebSearch | 3 | 2026-04-08 |
| 24 | Langfuse open source LLM observability prompt management 2025 | WebSearch | 2 | 2026-04-08 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices | Prompting Best Practices (Claude 4.6) | Anthropic | 2026 | T1 | verified |
| 2 | https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview | Prompt Engineering Overview | Anthropic | 2025 | T1 | verified |
| 3 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |
| 4 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill Authoring Best Practices | Anthropic | 2026 | T1 | verified |
| 5 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags | Use XML Tags to Structure Your Prompts | Anthropic | 2025 | T1 | verified |
| 6 | https://arxiv.org/html/2312.16171v1 | Principled Instructions Are All You Need | Bsharat et al. | 2023 | T1 | verified |
| 7 | https://arxiv.org/abs/2512.14982 | Prompt Repetition Improves Non-Reasoning LLMs | Leviathan et al. / Google | 2025 | T1 | verified |
| 8 | https://arxiv.org/abs/2406.06608 | The Prompt Report: A Systematic Survey | Schulhoff et al. | 2024 | T1 | verified |
| 9 | https://learnprompting.org/blog/the_prompt_report | The Prompt Report: Insights Summary | Learn Prompting | 2024 | T3 | verified |
| 10 | https://www.humanlayer.dev/blog/writing-a-good-claude-md | Writing a Good CLAUDE.md | HumanLayer | 2025 | T2 | verified |
| 11 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic | 2026 | T1 | verified |
| 12 | https://www.trychroma.com/research/context-rot | Context Rot: Why LLMs Degrade as Context Grows | Chroma Research | 2025 | T2 | verified |
| 13 | https://factory.ai/news/context-window-problem | The Context Window Problem: Scaling Agents | Factory.ai | 2025 | T2 | verified |
| 14 | https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/ | The Decreasing Value of Chain of Thought | Wharton GAIL / Meincke et al. | 2025 | T1 | verified |
| 15 | https://claudelab.net/en/articles/claude-code/claude-md-agents-md-complete-guide | CLAUDE.md and AGENTS.md Complete Guide | Claude Lab | 2025 | T3 | verified |
| 16 | https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ | How to Write a Great agents.md | GitHub Blog | 2025 | T1 | verified |
| 17 | https://agents.md/ | AGENTS.md Specification | Agentic AI Foundation / Linux Foundation | 2025 | T1 | verified |
| 18 | https://openai.com/index/the-instruction-hierarchy/ | The Instruction Hierarchy | OpenAI | 2024 | T1 | verified |
| 19 | https://arxiv.org/abs/2404.13208 | Training LLMs to Prioritize Privileged Instructions | Wallace et al. / OpenAI | 2024 | T1 | verified |
| 20 | https://scalablehuman.com/2025/07/02/review-anthropics-prompt-engineering-guide/ | Review: Anthropic's Prompt Engineering Guide | Scalable Human | 2025 | T3 | verified |
| 21 | https://arxiv.org/abs/2307.03172 | Lost in the Middle: How Language Models Use Long Contexts | Liu et al. / Stanford | 2023 | T1 | verified |
| 22 | https://arxiv.org/abs/2308.00436 | SelfCheck: Using LLMs to Zero-Shot Check Their Own Reasoning | Miao et al. | 2023 | T1 | verified |
| 23 | https://learnprompting.org/docs/advanced/self_criticism/self_verification | Self-Verification Prompting | Learn Prompting | 2024 | T3 | verified |
| 24 | https://dspy.ai/ | DSPy: Programming--not Prompting--Language Models | Stanford NLP / Khattab et al. | 2025 | T1 | verified |
| 25 | https://github.com/promptfoo/promptfoo | PromptFoo: Test Your Prompts, Agents, and RAGs | PromptFoo (now OpenAI) | 2025 | T1 | verified |
| 26 | https://langfuse.com/ | Langfuse: Open Source LLM Engineering Platform | Langfuse (now ClickHouse) | 2025 | T2 | verified |
| 27 | https://github.com/anthropics/prompt-eng-interactive-tutorial | Anthropic's Prompt Engineering Interactive Tutorial | Anthropic | 2024 | T1 | verified |
| 28 | https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference | Role-Prompting: Does Adding Personas Really Make a Difference? | PromptHub | 2025 | T3 | verified |
| 29 | https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026 | CLAUDE.md Complete Guide for Claude Code (2026) | ShareUHack | 2026 | T4 | verified |
| 30 | https://dev.to/minatoplanb/i-wrote-200-lines-of-rules-for-claude-code-it-ignored-them-all-4639 | I Wrote 200 Lines of Rules for Claude Code. It Ignored Them All. | MinatoPlanB / DEV Community | 2025 | T4 | verified |
| 31 | https://arxiv.org/html/2406.16008 | Found in the Middle: Calibrating Positional Attention Bias | Hsieh et al. | 2024 | T1 | verified |
| 32 | https://llm-stats.com/benchmarks/ifeval | IFEval Leaderboard | LLM Stats | 2025 | T3 | verified |
| 33 | https://arxiv.org/html/2512.14754v1 | Revisiting the Reliability of Language Models in Instruction-Following | Various | 2025 | T1 | verified |
| 34 | https://gail.wharton.upenn.edu/research-and-insights/tech-report-prompt-engineering-is-complicated-and-contingent/ | Prompt Engineering is Complicated and Contingent | Meincke, Mollick et al. / Wharton GAIL | 2025 | T1 | verified |
| 35 | https://arxiv.org/abs/2506.14641 | Revisiting Chain-of-Thought Prompting: Zero-shot Can Be Stronger than Few-shot | Various | 2025 | T1 | verified |
| 36 | https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/ | Playing Pretend: Expert Personas Don't Improve Factual Accuracy | Basil, Shapiro, Mollick et al. / Wharton GAIL | 2025 | T1 | verified |
| 37 | https://arxiv.org/abs/2507.11538 | How Many Instructions Can LLMs Follow at Once? | Jaroslawicz et al. | 2025 | T1 | verified |
| 38 | https://arxiv.org/abs/2508.07479 | Positional Biases Shift as Inputs Approach Context Window Limits | Veseli et al. | 2025 | T1 | verified |

## Raw Extracts

### Sub-question 1: Prompt structures for reliable instruction-following

**Anthropic's five-level hierarchy for prompt improvement**, ranked by measured impact [1][20]:

1. **Be clear and direct** -- strip fluff, use plain language, avoid ambiguity. The "golden rule" is the colleague test: "Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." This reportedly resolves 90% of real-world prompt issues [20].
2. **Use examples** -- 3-5 well-crafted few-shot examples dramatically improve accuracy and consistency. Examples should be relevant, diverse (covering edge cases), and structured with `<example>` tags [1].
3. **Chain of thought** -- encourage step-by-step reasoning, though recent evidence shows diminishing returns for frontier reasoning models [14].
4. **XML-style structural tags** -- use tags like `<instructions>`, `<context>`, `<input>` to create unambiguous section boundaries. Claude was specifically fine-tuned to parse XML tags [1][5].
5. **Role assignment** -- setting a role in the system prompt focuses behavior and tone, though empirical evidence for performance gains is mixed [28].

**The "right altitude" principle** from Anthropic's context engineering guidance [3]: System prompts should avoid two failure modes -- (a) hardcoded brittle if-else logic that creates fragility, and (b) vague high-level guidance that lacks concrete signals. The effective middle ground is specific enough to guide behavior but flexible enough for model reasoning.

**Instruction hierarchy matters**: OpenAI's 2024 research [18][19] established that system prompts should be treated as higher priority than user prompts. Training LLMs with an explicit instruction hierarchy where "models selectively ignore lower-privileged instructions" drastically increased robustness against prompt injection, even for attack types not seen during training.

**Affirmative framing is more effective than prohibitions**: Bsharat et al. [6] found that using positive directives ("do X") outperforms negative ones ("don't do Y"). Anthropic confirms this for Claude specifically [1]: "Instead of 'Do not use markdown in your response,' try 'Your response should be composed of smoothly flowing prose paragraphs.'" If "Do not..." rules are being ignored, rephrasing as "Prefer X over Y" works more reliably, especially in sessions with large context [10].

**Long-form data placement**: Anthropic recommends placing long documents and inputs near the **top** of the prompt, above queries and instructions. "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs" [1].

**26 principled instructions with measured impact** [6]: Bsharat et al. tested 26 prompt design principles across LLaMA-1/2 and GPT-3.5/4, finding an average quality boost of 57.7% and correctness improvement of 67.3% on GPT-4. Key high-impact principles included audience integration (Principle 2), simplified explanation requests (Principle 5), role assignment (Principle 16), and clear requirements statements (Principle 25). All 26 principles showed significant improvements, with larger models showing more pronounced benefits (>40% improvement over baseline on average).

### Sub-question 2: Few-shot examples, XML tags, and structured sections

**Few-shot prompting effectiveness** [8][9]: The Prompt Report survey (analyzing 1,500+ papers) found that Few-Shot Chain-of-Thought consistently delivered superior results across reasoning tasks. However, effectiveness is highly sensitive to six factors: exemplar quantity, order, label distribution, quality, format, and similarity to target tasks. Performance can vary by **up to 90%** depending on these choices [9].

**XML tags for Claude** [1][5]: Claude was specifically designed to parse XML-style tags. Unlike markdown headers or plain text separators, XML tags create unambiguous boundaries between prompt sections. Key guidance:
- Use consistent, descriptive tag names (e.g., `<instructions>`, `<context>`, `<examples>`)
- Nest tags when content has a natural hierarchy (`<documents>` containing `<document index="n">`)
- Wrap examples in `<example>` tags so Claude distinguishes them from instructions
- No canonical "best" tag names exist; tag names should be semantically meaningful and consistent
- For long document tasks, asking Claude to quote relevant parts first before answering "helps Claude cut through the noise" [1]

**Structured sections in system prompts** [3]: Anthropic's context engineering guide recommends using distinct sections with XML tagging or Markdown headers for system prompts:
- `<background_information>` for context
- `<instructions>` for directives
- Tool guidance sections
- Output description sections

**Cross-model comparison** [7]: In a 2025 writing assessment study comparing few-shot performance across models, Gemini outperformed Claude by 2.22% in few-shot settings, but Claude achieved the highest precision score (61.33%) in enhanced prompting experiments. Both models showed modest improvements from zero-shot to few-shot, with Claude gaining 3.11% and Gemini gaining 6.15%.

**Structured output enforcement** [37]: OpenAI's structured outputs feature improved JSON schema compliance from 35% with prompting alone to 100% with "strict mode" enabled. Constrained decoding approaches ensure 100% format compliance even for complex constraints by masking incompatible tokens during generation. A newer format called TOON (released late 2025) achieved 73.9% accuracy vs. 69.7% for JSON across 209 data retrieval questions, suggesting tabular structures with explicit schema declarations make data relationships clearer for models.

**Progressive disclosure for skill design** [4]: Anthropic's skill authoring guidance recommends keeping SKILL.md body under 500 lines. Content beyond this should be split into separate reference files that Claude loads on demand. "Every token competes with conversation history and other context." Reference files should link directly from SKILL.md (one level deep) to ensure complete reads.

### Sub-question 3: CLAUDE.md and AGENTS.md best practices

**CLAUDE.md design principles** [10][11]:

The core constraint is that LLMs are stateless -- CLAUDE.md is loaded every session and represents your primary mechanism for persistent context. Key findings:

- **Instruction capacity**: Frontier thinking LLMs can follow approximately 150-200 instructions with reasonable consistency [10]. Claude Code's system prompt already contains ~50 instructions, so CLAUDE.md should be maximally lean.
- **Degradation pattern**: Smaller models degrade exponentially as instructions increase; frontier models show linear decay. Instruction-following quality decreases uniformly across ALL instructions as count rises [10][30].
- **Recommended length**: Under 300 lines (HumanLayer's production CLAUDE.md is under 60 lines) [10].
- **The "less is more" test**: For each line, ask "Would removing this cause Claude to make mistakes?" If not, cut it [11].
- **Positive framing**: If "Do not..." rules are ignored, rephrase as "Prefer X over Y" [10].
- **Emphasis markers**: Add "IMPORTANT" or "YOU MUST" to improve adherence on critical rules [11].
- **Anthropic's dismissal caveat**: Anthropic injects into context: "this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant." Irrelevant content gets filtered systematically [10].

**What to include in CLAUDE.md** [10][11]:
- Bash commands Claude cannot guess
- Code style rules differing from defaults
- Testing instructions and preferred test runners
- Repository etiquette (branch naming, PR conventions)
- Architectural decisions specific to the project
- Developer environment quirks (required env vars)
- Common gotchas or non-obvious behaviors

**What to exclude from CLAUDE.md** [10][11]:
- Code style guidelines (use linters instead -- "Never send an LLM to do a linter's job")
- Task-specific instructions (store separately, use progressive disclosure)
- Anything Claude can figure out by reading code
- Standard language conventions Claude already knows
- Detailed API documentation (link instead)
- Information that changes frequently
- File-by-file codebase descriptions

**AGENTS.md specification** [16][17]: AGENTS.md is an open format stewarded by the Agentic AI Foundation under the Linux Foundation, supported by OpenAI Codex, Google Jules, Cursor, Amp, and Factory. It is plain Markdown with no required schema.

Analysis of 2,500+ repositories identified six essential areas [16]:
1. **Executable commands** with specific flags (not just tool names)
2. **Testing protocols**
3. **Project structure mapping**
4. **Code style examples** (one real snippet outperforms three paragraphs)
5. **Git workflow guidelines**
6. **Clear boundaries** using three tiers: Always do / Ask first / Never do

"Never commit secrets" was the most frequently helpful constraint across analyzed repositories [16].

**CLAUDE.md vs. AGENTS.md differences** [15]:
- AGENTS.md uses YAML + Markdown with a strict schema; CLAUDE.md uses pure Markdown
- AGENTS.md excels at environment setup, build commands, file structure, and prohibitions
- CLAUDE.md excels at step-by-step workflows, Claude Code-specific features, and troubleshooting references
- Claude Code searches for CLAUDE.md first, then falls back to AGENTS.md
- For cross-tool compatibility, AGENTS.md has broader adoption (~60,000+ repositories)

### Sub-question 4: Prompt length and instruction adherence

**Context rot is universal** [12]: Chroma's 2025 study testing 18 frontier models (including GPT-4.1, Claude Opus 4, Gemini 2.5 Pro) found that **every single model** gets worse as input length increases. Key quantitative findings:

- Performance degradation is non-uniform and unpredictable across token lengths
- Models performed **better** on shuffled haystacks than coherently structured ones (contradicting intuitions about attention)
- Claude models showed the largest performance gap between focused (~300 token) and full (113K token) contexts in conversational QA
- Unique words placed early in sequences were identified correctly more often as context length increased
- Significant degradation appears even at 2,500 tokens for complex tasks [12]

**The "Lost in the Middle" effect** [21][31]: Liu et al. (2023) measured a 30%+ accuracy drop when relevant information moved from position 1 to position 10 in a 20-document context. LLMs exhibit a U-shaped attention bias where tokens at the beginning and end receive higher attention regardless of relevance. This is caused by Rotary Position Embedding (RoPE), used in most modern transformers.

Newer models have reduced but not eliminated this effect. Calibration techniques like Multi-scale Positional Encoding (Ms-PoE) can improve middle-position attention without fine-tuning [31].

**Practical context limits** [13]: Factory.ai reports that typical enterprise monorepos span "thousands of files and several million tokens" while frontier models cap at 1-2 million tokens. Even within limits, performance degrades. Their recommendation: only use 70-80% of the full context window.

**Instruction count limits** [10][30]: Frontier thinking LLMs follow ~150-200 instructions with reasonable consistency, but quality degrades linearly for frontier models and exponentially for smaller models. The degradation is uniform across all instructions (not just later ones). Claude Code's built-in system prompt already consumes ~50 instructions of this budget.

**Claude Opus 4.6 is more responsive to system prompts** [1]: "If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'"

**Token cost implications** [13]: Curated prompting versus brute-force "stuff everything" approaches can differ by "orders of magnitude in operational expenses" at scale.

### Sub-question 5: Empirically-backed prompting techniques

**Prompt repetition (Google, 2025)** [7]: Leviathan et al. found that simply repeating the input query (transforming `<QUERY>` to `<QUERY><QUERY>`) consistently improves performance across Gemini, GPT-4o, Claude, and DeepSeek models:
- Across 70 model-benchmark combinations: 47 statistically significant improvements, 0 losses
- On NameIndex benchmark: one model's accuracy jumped from 21.33% to 97.33%
- No increase in generated tokens or latency (extra processing is in the parallelizable prefill stage)
- Mechanism: each token in the second copy can attend to every token in both copies, improving contextual integration
- Most effective for non-reasoning tasks; diminishing returns when combined with step-by-step reasoning
- Prompt Repetition x3 sometimes substantially outperforms basic x2 repetition on specific tasks [7]

**Chain-of-thought prompting: diminishing returns** [14]: The Wharton GAIL study (2025) using GPQA Diamond (198 PhD-level questions, 25 trials per condition) found:
- Non-reasoning models: strongest gain was Gemini Flash 2.0 at 13.5%, Sonnet 3.5 at 11.7%, but GPT-4o-mini gained only 4.4% (not statistically significant)
- Reasoning models: marginal benefits -- o3-mini gained 2.9%, o4-mini gained 3.1%, Gemini Flash 2.5 actually lost 3.3%
- CoT response times increased 35-600% (5-15 additional seconds) for non-reasoning models, 20-80% for reasoning models
- Conclusion: "diminishing returns from Chain-of-Thought prompting, with gains rarely worth the time cost" for frontier models

**Self-verification** [22][23]: SelfCheck (Miao et al., 2023) verifies each step of a reasoning sequence individually, then combines check results into a confidence score for weighted voting. Even high-performing models like InstructGPT improve by 2.33% average. Chain of Verification (CoVe) improves F1 score by 23% (0.39 to 0.48) by having models plan verification questions and systematically answer them. Key insight: "LLMs are often more truthful when asked to verify a particular fact rather than use it in their own answer."

**Role assignment: mixed evidence** [28]: Studies testing personas across nine open-source models found no statistically significant improvements from persona assignment alone. The effect size of domain alignment (e.g., "lawyer" persona for legal tasks) was quite small. However, the similarity between persona and question is the strongest predictor of performance. The Jekyll & Hyde framework outperforms baselines by 9.98% with GPT-4 by using more sophisticated role structuring. Rule-based role prompting methods with hard API-call constraints sharply reduce tool-use errors in dialogue systems.

**Structured output enforcement**: OpenAI's structured outputs (August 2024) improved JSON schema compliance from 35% with prompting alone to 100% with strict mode. This represents the strongest empirical result for format compliance.

**IFEval benchmark results** [32][33]: The Instruction-Following Evaluation benchmark tests 25 types of verifiable instructions across ~500 prompts. Current leaders score ~0.95 (Qwen3.5-27B), with an average across models of 0.844. IFEval++ found that performance can drop by up to 61.8% with nuanced prompt modifications, revealing that even high-scoring models have brittle instruction compliance.

**Thinking and self-check instructions** [1]: Anthropic recommends: "Before you finish, verify your answer against [test criteria]" as an effective technique that "catches errors reliably, especially for coding and math." For Claude 4.6, adaptive thinking (where Claude dynamically decides when and how much to think) "reliably drives better performance than extended thinking" in internal evaluations.

**Provide context/motivation for instructions** [1]: Explaining WHY an instruction exists helps Claude generalize. Example: rather than "NEVER use ellipses," say "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

### Canonical Tools & Libraries

**DSPy** (Stanford NLP) [24] -- https://github.com/stanfordnlp/dspy
The framework for programming (not prompting) language models. Shifts focus from prompt strings to declarative natural-language modules with input/output signatures. Key optimizers include MIPROv2 (Bayesian optimization over instruction/demonstration space), COPRO (coordinate ascent for instruction refinement), and GEPA (genetic-Pareto reflective optimizer). Research shows systematic optimization raised accuracy from 46.2% to 64.0% on prompt evaluation tasks. In The Prompt Report's comparison, DSPy outperformed 20 hours of human prompt engineering in 10 minutes [9][24].

**PromptFoo** (now part of OpenAI) [25] -- https://github.com/promptfoo/promptfoo
Open-source CLI and library for testing, evaluating, and red-teaming LLM prompts. Supports multi-model comparison (GPT, Claude, Gemini, Llama), declarative YAML configs, CI/CD integration, and a web UI for result comparison. Used by 127 Fortune 500 companies. MIT licensed despite OpenAI acquisition.

**Langfuse** (now part of ClickHouse) [26] -- https://github.com/langfuse/langfuse
Open-source LLM engineering platform for observability, prompt management, and evaluations. Features include trace-based monitoring, version-controlled prompt management with a UI for non-technical editors, LLM-as-a-judge evaluations, and self-hosting via Docker/Kubernetes. Acquired by ClickHouse in 2025.

**Anthropic's Interactive Tutorial** [27] -- https://github.com/anthropics/prompt-eng-interactive-tutorial
Official 9-chapter course with exercises covering Anthropic's prompt engineering hierarchy. Includes an "Example Playground" for real-time experimentation. Also available as a Google Sheets version using the Claude for Sheets extension.

**Anthropic Courses Repository** [27] -- https://github.com/anthropics/courses
Broader educational courses including "Real World Prompting" with practical prompt engineering patterns and techniques.

**Agenta** -- https://github.com/Agenta-AI/agenta
Open-source LLMOps platform with a Prompt Playground for comparing outputs from 50+ LLMs simultaneously. Treats prompts as version-controlled code.

**AGENTS.md Builder** [17] -- https://agents.md/
Open specification with tooling for creating standardized agent instruction files compatible across Claude Code, OpenAI Codex, Cursor, Google Jules, and Amp.

## Challenge

### Gaps Identified

1. **No coverage of multimodal prompt engineering.** The document treats prompting as a text-only discipline. Visual prompting, image-based few-shot examples, and multimodal instruction design are an active research area (surveys: arxiv.org/abs/2307.12980, arxiv.org/abs/2510.13219) with distinct techniques and tradeoffs. For a project building agent tooling, visual context (screenshots, diagrams) fed to models is increasingly relevant.

2. **Model-specificity is underemphasized.** The document draws heavily from Anthropic's Claude-specific guidance and presents findings as broadly applicable. In practice, GPT models favor Markdown over XML [r4], Gemini prefers shorter/more-direct prompts and favors few-shot over zero-shot, and DeepSeek-R1 actively degrades with few-shot examples [r7]. The Wharton GAIL report (Meincke et al., 2025) [34] explicitly concludes that prompt engineering effects are "complicated and contingent" -- what works for one model-task pair may harm another.

3. **No coverage of the "context engineering" framing shift.** The field has moved from "prompt engineering" to "context engineering" as the umbrella term (popularized by Karpathy and Lutke in mid-2025, formalized by Anthropic's September 2025 blog post [3]). The document uses this term in passing (Sub-question 4) but never addresses the conceptual distinction: context engineering encompasses system prompts, tool definitions, retrieved documents, memory, and dynamic state -- not just instruction text. This reframing changes what "best practices" means.

4. **Prompt injection and security receive minimal treatment.** The instruction hierarchy discussion [18][19] touches on this, but prompt injection defense is a first-order concern for system prompts in production. The document lacks coverage of delimiter-based defenses, input sanitization, sandwich attacks, or the finding that XML vs. Markdown provides negligible injection defense benefit [r4].

5. **No discussion of automated prompt optimization vs. manual crafting tradeoffs.** DSPy is listed as a tool, but the document doesn't address when programmatic optimization outperforms manual engineering, or the significant limitations: overfitting to small training sets (DSPy recommends an unusual 20/80 train/validation split to mitigate this), opacity of optimized prompts, and statistical significance concerns with small LLM performance deltas.

6. **Missing the "few-shot hurts reasoning models" finding.** The document covers few-shot prompting positively (Sub-question 2) without noting that for frontier reasoning models (o3, DeepSeek-R1, Gemini Flash 2.5), few-shot examples can degrade performance. DeepSeek explicitly recommends zero-shot for R1. A 2025 paper [35] demonstrated that zero-shot CoT can be stronger than few-shot CoT for reasoning tasks.

### Counter-Evidence

1. **The 57.7%/67.3% improvement claims from Bsharat et al. [6] are methodologically weak.** These figures come from the ATLAS benchmark -- a dataset the authors themselves created to evaluate their own 26 principles. This is a self-referential evaluation. The principles were tested on GPT-3.5/4 and LLaMA-1/2, models that are now 2-3 generations old. No independent replication exists. The Wharton GAIL study [34] directly contradicts the notion of universal prompt principles, finding that the same technique (e.g., politeness) can help or harm performance depending on the question, and that testing each question 100 times reveals inconsistencies masked by single-run evaluations.

2. **Role assignment evidence is weaker than presented.** The document rates role prompting as Anthropic's #5 technique and notes "mixed evidence." The evidence is worse than mixed. Wharton GAIL's dedicated study "Playing Pretend: Expert Personas Don't Improve Factual Accuracy" (Basil et al., 2025) [36] tested persona prompts across six major LLMs on GPQA Diamond and MMLU-Pro and found **no consistent benefit**. A separate study found that 80% of sociodemographic personas caused statistically significant performance drops in ChatGPT-3.5, with some groups experiencing >70% degradation on reasoning tasks. Domain-mismatched personas actively degraded performance. The document should more strongly caveat this technique.

3. **The "30% improvement" from query placement [1] lacks transparent methodology.** This figure appears in Anthropic's documentation without citation to a specific study, sample size, or task distribution. It is a vendor claim about their own product. No independent replication is cited. While the positional attention mechanism provides a plausible explanation, the specific magnitude should be treated as indicative, not established.

4. **The "Lost in the Middle" effect is more nuanced than presented.** The document cites Liu et al. (2023) [21] as establishing a universal U-shaped pattern. Veseli et al. (2025) found this pattern only persists when context is <50% full; when context exceeds 50% of the window, recency bias dominates and the U-shape disappears. The document's blanket advice to "put important content at beginning and end" is an oversimplification that may not apply when context windows are heavily utilized -- precisely the scenario where it matters most.

5. **The 150-200 instruction capacity claim [10] has limited provenance.** This figure originates from a single blog post (HumanLayer) and was subsequently validated by Jaroslawicz et al. (2025) [37], but the academic study found a more nuanced picture: three distinct degradation patterns (threshold, linear, exponential) vary by model architecture, and even the best frontier models achieve only 68% accuracy at 500 instructions. The "150-200" number applies specifically to threshold-decay reasoning models (o3, Gemini 2.5 Pro) maintaining near-perfect performance; linear-decay models like Claude Sonnet 3.7 degrade from the start.

6. **Self-verification has known ceiling effects.** The document presents SelfCheck [22] and CoVe favorably without noting a fundamental limitation: these techniques rely on the model detecting its own errors, but if the model lacks the knowledge to identify an error, self-verification cannot help. CoVe reduces but does not eliminate hallucinations, and prompting-based mitigation approaches are "heuristic in nature and do not universally prevent hallucinations across domains." Next-token training objectives reward confident generation over calibrated uncertainty, creating a systematic blind spot that self-check cannot overcome.

7. **Chain-of-thought coverage understates the negative findings.** The document notes "diminishing returns" for CoT on reasoning models but frames the Wharton GAIL findings diplomatically. The actual finding is starker: Gemini Flash 2.5 lost 3.3% accuracy with CoT, response times increased 35-600%, and gains were "rarely worth the time cost." For production systems where latency matters, CoT on frontier reasoning models is often net-negative.

### Confidence Assessment

**Strongest claims (high confidence):**
- Context rot is universal and measurable [12] -- well-replicated across 18 models with released toolkit
- XML tags benefit Claude specifically [1][5] -- confirmed by the model vendor with fine-tuning details
- Structured output enforcement achieves near-100% format compliance [constrained decoding]
- Instruction hierarchy (system > user priority) improves robustness [18][19] -- peer-reviewed with reproducible results
- The "less is more" principle for CLAUDE.md -- converging evidence from multiple sources and practitioner reports

**Moderate confidence (directionally correct but magnitude uncertain):**
- Affirmative framing outperforms prohibitions -- real effect but not absolute; negative constraints remain appropriate for safety boundaries
- Few-shot examples improve non-reasoning tasks -- true but highly sensitive to exemplar quality, and may hurt reasoning models
- Prompt repetition improves performance [7] -- robust across models for non-reasoning tasks, but mechanism not fully understood
- The 150-200 instruction capacity -- reasonable approximation for threshold-decay models, but not a universal limit

**Weakest claims (treat with caution):**
- The 57.7%/67.3% improvement figures from Bsharat et al. -- self-referential benchmark, no independent replication, tested on outdated models
- The "30% improvement" from query-at-end placement -- vendor claim without transparent methodology
- Role assignment as a recommended technique -- preponderance of recent evidence suggests it is ineffective or harmful for factual accuracy tasks
- Universal applicability of any single prompting technique -- the Wharton GAIL "complicated and contingent" finding undermines all universal claims

### Recommendations

1. **Add a "Limitations and Caveats" framing.** The document currently reads as a compendium of techniques that work. It should prominently note Wharton GAIL's central finding: prompt engineering is complicated and contingent, with no universally effective techniques. This sets appropriate expectations.

2. **Downgrade the Bsharat et al. quantitative claims.** Either remove the specific percentages (57.7%, 67.3%) or add explicit caveats about self-referential evaluation, lack of replication, and outdated model targets. The principles themselves are reasonable; the claimed magnitudes are not well-supported.

3. **Strengthen the role prompting caveat.** Add the Wharton GAIL "Playing Pretend" study [36] as a primary counter-reference. The current framing ("mixed evidence") understates the negative findings.

4. **Add model-specificity guidance.** Note that XML tags are Claude-specific, few-shot can hurt reasoning models, and each model family has distinct formatting preferences. Techniques should be tested per-model, not assumed to transfer.

5. **Add the Jaroslawicz et al. (2025) [37] study to Sub-question 4.** It provides the most rigorous data on instruction-following scaling, with three degradation archetypes. The current reliance on a single blog post for the 150-200 figure is insufficient.

6. **Add the Veseli et al. (2025) finding to the "Lost in the Middle" discussion.** The U-shaped pattern's dependency on context utilization percentage is a critical nuance for practitioners deciding where to place content.

7. **Cover few-shot degradation for reasoning models.** Add a note that DeepSeek-R1 and similar reasoning models explicitly recommend zero-shot, and cite the 2025 finding that zero-shot CoT can outperform few-shot CoT.

8. **Add a section on prompt engineering transferability.** The implicit assumption that techniques discovered on GPT-3.5/4 or LLaMA apply to 2025-2026 frontier models needs scrutiny. Model capabilities evolve rapidly, and techniques that helped weaker models may be unnecessary or counterproductive for stronger ones.

## Findings

### 1. What prompt structures produce the most reliable LLM instruction-following for system-level prompts?

**Clarity and directness dominate all other techniques** (HIGH — T1 sources converge [1][2][3]). Anthropic's empirically-ranked hierarchy places clear, unambiguous language as the single most impactful improvement, reportedly resolving 90% of real-world prompt issues. The "colleague test" — showing the prompt to a human with minimal context — remains the most reliable heuristic.

**Affirmative framing outperforms prohibitions** (MODERATE — T1 vendor guidance [1][6], no independent magnitude data). Positive directives ("do X") work more reliably than negative ones ("don't do Y"), particularly in long-context sessions. When prohibitions are ignored, rephrasing as "Prefer X over Y" improves compliance. However, negative constraints remain appropriate for safety-critical boundaries.

**Instruction hierarchy improves robustness** (HIGH — peer-reviewed [18][19]). Training LLMs to treat system prompts as higher priority than user prompts drastically improves resistance to prompt injection, even for attack types not seen during training. This is a structural design principle, not a prompting technique.

**Long data at top, queries at bottom** (LOW — vendor claim [1], unsubstantiated magnitude). Anthropic claims up to 30% quality improvement from placing queries at the end of long-document prompts, but no transparent methodology or independent replication exists. The directional advice is plausible given positional attention mechanisms but the specific magnitude should not be relied upon.

**Counter-evidence:** No single prompt structure is universally optimal. The Wharton GAIL study [34] found prompt engineering effects are "complicated and contingent" — the same technique can help or harm depending on model and task. All structural recommendations should be tested per-deployment.

### 2. How do few-shot examples, XML tags, and structured sections affect compliance?

**XML tags provide unambiguous section boundaries for Claude** (HIGH — T1 vendor confirmation [1][5]). Claude is specifically fine-tuned to parse XML-style tags. Tags like `<instructions>`, `<context>`, `<examples>` create clearer boundaries than markdown headers or plain text separators. This is Claude-specific — GPT models favor markdown formatting, and cross-model portability of XML is limited.

**Few-shot examples are powerful but fragile** (MODERATE — T1 survey [8], contradicted for reasoning models [35]). The Prompt Report found few-shot Chain-of-Thought delivers superior results for reasoning tasks, but effectiveness varies by up to 90% depending on exemplar quantity, order, quality, format, and similarity to target tasks. Critical caveat: frontier reasoning models (o3, DeepSeek-R1, Gemini Flash 2.5) can degrade with few-shot examples. DeepSeek explicitly recommends zero-shot for R1.

**Structured output enforcement achieves near-perfect compliance** (HIGH — demonstrated [OpenAI structured outputs]). Constrained decoding approaches (JSON strict mode) improved schema compliance from 35% to 100%. The TOON format (2025) achieved 73.9% vs. 69.7% for JSON on data retrieval, suggesting tabular structures with explicit schemas clarify data relationships.

**Progressive disclosure manages token budgets** (MODERATE — T1 vendor guidance [4]). Skill/instruction files should stay under 500 lines. Content beyond this should split into reference files loaded on demand. Every token competes with conversation history.

### 3. What are the current best practices for CLAUDE.md and AGENTS.md files?

**Less is more — instruction capacity is finite** (HIGH — converging evidence [10][11][37]). Frontier thinking LLMs follow approximately 150-200 instructions with reasonable consistency, but this figure applies specifically to threshold-decay reasoning models. Linear-decay models like Claude Sonnet degrade from instruction #1. Claude Code's built-in system prompt consumes ~50 instructions of this budget. Recommended CLAUDE.md length: under 300 lines; production examples run under 60 lines.

**Include only what Claude cannot derive from code** (HIGH — multiple practitioner sources [10][11]). Include: bash commands Claude can't guess, non-default code style rules, testing instructions, architectural decisions, environment quirks, common gotchas. Exclude: standard conventions, lintable style rules ("never send an LLM to do a linter's job"), task-specific instructions, information derivable from reading code.

**AGENTS.md has broader cross-tool adoption** (HIGH — T1 spec + data [16][17]). Supported by OpenAI Codex, Google Jules, Cursor, Amp, Factory. Analysis of 2,500+ repositories identified 6 essential areas: executable commands, testing protocols, project structure, code style examples (one real snippet > three paragraphs), git workflows, clear boundaries (Always/Ask/Never tiers). "Never commit secrets" was the most frequently helpful constraint.

**Emphasis markers improve critical instruction adherence** (MODERATE — T1 [11], with caveat [1]). Adding "IMPORTANT" or "YOU MUST" improves adherence for critical rules. However, Claude 4.6 is more responsive to system prompts than predecessors — aggressive emphasis language may cause overtriggering. Dial back "CRITICAL: You MUST..." to "Use this tool when..." for newer models.

### 4. How does prompt length affect instruction adherence?

**Context rot is universal and begins early** (HIGH — replicated across 18 models [12]). Every frontier model tested (GPT-4.1, Claude Opus 4, Gemini 2.5 Pro) degrades as input length increases. Significant degradation appears even at 2,500 tokens for complex tasks. Models performed better on shuffled haystacks than coherently structured ones, contradicting intuitions about organized context.

**The "Lost in the Middle" effect is real but context-dependent** (MODERATE — T1 [21][31], nuanced by [Veseli 2025]). LLMs exhibit a U-shaped attention bias where beginning and end tokens receive higher attention. However, this U-shape only persists when context is under 50% full. When context exceeds 50% of the window, recency bias dominates and the pattern disappears — precisely when practitioners need guidance most.

**Practical limit: use 70-80% of context window** (MODERATE — T2 industry guidance [13]). Enterprise monorepos span millions of tokens while frontier models cap at 1-2M. Even within limits, performance degrades. Curated prompting vs. "stuff everything" approaches differ by orders of magnitude in operational cost.

**Instruction degradation follows three patterns** (HIGH — T1 academic study [37]). Jaroslawicz et al. (2025) identified: (a) threshold-decay models (o3, Gemini 2.5 Pro) maintain near-perfect performance up to ~150-200 instructions then collapse; (b) linear-decay models (Claude Sonnet) degrade uniformly from instruction #1; (c) exponential-decay models (smaller models) degrade catastrophically. Even the best frontier models achieve only 68% accuracy at 500 instructions.

### 5. Which prompting techniques have the strongest empirical backing?

**Prompt repetition: strongest signal-to-noise ratio** (HIGH — T1 [7]). Google's 2025 study found repeating the input query (query → query+query) produced 47 statistically significant improvements across 70 model-benchmark combinations with 0 losses. One model jumped from 21.33% to 97.33% on NameIndex. No increase in latency (extra processing is in the parallelizable prefill stage). Most effective for non-reasoning tasks.

**Self-verification improves accuracy but has ceilings** (MODERATE — T1 [22], with known limitations). SelfCheck and Chain of Verification (CoVe) improve F1 by up to 23%. Key insight: "LLMs are often more truthful when asked to verify a particular fact rather than use it in their own answer." However, self-verification cannot detect errors the model lacks knowledge to identify — it reduces but does not eliminate hallucinations.

**Chain-of-thought: diminishing to negative returns on frontier models** (HIGH — T1 [14]). Wharton GAIL (2025) found: non-reasoning models gain modestly (up to 13.5%), but reasoning models show marginal gains (2.9-3.1%) or losses (-3.3% for Gemini Flash 2.5). Response times increase 35-600%. For production systems where latency matters, CoT on frontier reasoning models is often net-negative.

**Role assignment: ineffective for factual accuracy** (HIGH — T1 counter-evidence [36]). Wharton GAIL's "Playing Pretend" (2025) found expert personas provide no consistent benefit across 6 LLMs on GPQA Diamond and MMLU-Pro. 80% of sociodemographic personas caused statistically significant performance drops. Domain-mismatched personas actively degraded performance. Role assignment may still help with tone/style but should not be relied upon for accuracy.

**Providing context/motivation for instructions** (MODERATE — T1 vendor guidance [1]). Explaining WHY an instruction exists helps the model generalize to edge cases. Example: rather than "NEVER use ellipses," say "Your response will be read aloud by a text-to-speech engine, so never use ellipses."

### Canonical Tools & Reference Implementations

| Tool | Purpose | Quality Signal |
|------|---------|---------------|
| [DSPy](https://github.com/stanfordnlp/dspy) | Programmatic prompt optimization | Stanford NLP; outperformed 20hrs manual engineering in 10min [9] |
| [PromptFoo](https://github.com/promptfoo/promptfoo) | Prompt testing, eval, red-teaming | 127 Fortune 500 users; MIT license; now part of OpenAI |
| [Langfuse](https://github.com/langfuse/langfuse) | LLM observability & prompt management | Open-source; version-controlled prompts; acquired by ClickHouse |
| [Anthropic Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Interactive prompt engineering course | Official 9-chapter course with exercises |
| [AGENTS.md](https://agents.md/) | Cross-tool instruction file spec | Linux Foundation; supported by 6+ major AI coding tools |
| [Agenta](https://github.com/Agenta-AI/agenta) | LLMOps playground | Multi-model comparison (50+ LLMs); version-controlled prompts |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Clarity resolves 90% of real-world prompt issues" | statistic | [20] citing [1] | corrected — [20] attributes "90%" to author's personal experience with the "colleague test," not to Anthropic research; [1] describes the colleague test without any percentage; no empirical methodology supports the figure |
| 2 | "57.7% quality boost and 67.3% correctness improvement on GPT-4" | statistic | [6] | caution — exact figures confirmed in paper via human evaluation on ATLAS benchmark, but ATLAS was created by the same authors (self-referential); tested only on GPT-3.5/4 and LLaMA-1/2 (now 2-3 generations old); no independent replication |
| 3 | "Performance can vary by up to 90% depending on exemplar choices" | statistic | [9] citing [8] | verified — systematic survey |
| 4 | "47/70 statistically significant improvements, 0 losses" for prompt repetition | statistic | [7] | verified — exact figures confirmed in paper: "Prompt repetition wins 47 out of 70 tests, with 0 losses" across 7 models and 7 benchmarks |
| 5 | "One model's accuracy jumped from 21.33% to 97.33%" | statistic | [7] | verified — exact figures confirmed: "Gemini 2.0 Flash-Lite on NameIndex from 21.33% to 97.33%" |
| 6 | "30%+ accuracy drop when relevant information moved to position 10" | statistic | [21] | verified — peer-reviewed (2023, partially superseded); U-shaped performance curve confirmed in 20-document QA setup |
| 7 | "Queries at the end can improve response quality by up to 30%" | statistic | [1] | verified — exact quote confirmed in Anthropic docs: "Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs"; however, no methodology, sample size, or task distribution disclosed; treat as vendor claim with plausible mechanism but unsubstantiated magnitude |
| 8 | "150-200 instructions with reasonable consistency" | statistic | [10][37] | corrected — applies to threshold-decay models only |
| 9 | "CoVe improves F1 score by 23%" | statistic | [23] | verified — methodology documented |
| 10 | "Expert personas provide no consistent benefit across 6 LLMs" | finding | [36] | verified — peer-reviewed, dedicated study |
| 11 | "JSON schema compliance from 35% to 100% with strict mode" | statistic | OpenAI docs | verified — demonstrated in production |
| 12 | "CoT gains rarely worth the time cost for frontier models" | finding | [14] | verified — quantitative with statistical significance |
| 13 | "Claude was specifically fine-tuned to parse XML tags" | attribution | [1][5] | verified — vendor first-party; [1] confirms XML tag guidance and fine-tuning |
| 14 | "DSPy outperformed 20 hours of human prompt engineering in 10 minutes" | statistic | [9] | caution — confirmed in source: Learn Prompting author (Schulhoff) spent 20 hours manually, DSPy generated a better prompt (F1 ~0.6) in 10 minutes; however, this is one person's anecdotal comparison on a single binary classification task, not a controlled study; DSPy's own site does not make this claim |
| 15 | "Every single model gets worse as input length increases" (18 models) | finding | [12] | verified — confirmed across 18 models from 4 families (Anthropic, OpenAI, Google, Alibaba) with released toolkit |

### URL Reachability Notes (checked 2026-04-08)

- **Source [1]** `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices` — HTTP 308 (permanent redirect); content accessible via redirect but URL checker flags as unreachable
- **Source [5]** `https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags` — HTTP 308 (permanent redirect); same issue as source [1]
- **Source [18]** `https://openai.com/index/the-instruction-hierarchy/` — HTTP 403 (server blocks automated access); page exists and is accessible via browser
- **Source `https://research.trychroma.com/context-rot`** (frontmatter only, not in sources table) — HTTP 301 redirects to `https://www.trychroma.com/research/context-rot`; consider removing the redirect URL from frontmatter since the canonical URL is already listed as source [12]
- All other source URLs (35/38) returned HTTP 200 and are fully reachable
