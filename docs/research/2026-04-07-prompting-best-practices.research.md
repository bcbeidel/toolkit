---
name: "Prompting Best Practices"
description: "Evidence-backed canon of prompting techniques, composition patterns, common mistakes, task-specific strategies, and evaluation methodologies for LLM prompt engineering."
type: research
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  - https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
  - https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide
  - https://arxiv.org/abs/2406.06608
  - https://learnprompting.org/blog/the_prompt_report
  - https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/
  - https://ai.google.dev/gemini-api/docs/prompting-strategies
  - https://www.promptingguide.ai/techniques
  - https://home.mlops.community/public/blogs/the-impact-of-prompt-bloat-on-llm-output-quality
  - https://arxiv.org/abs/2509.14404
  - https://www.goinsight.ai/blog/llm-prompt-mistake/
  - https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference
  - https://www.evidentlyai.com/llm-guide/llm-as-a-judge
  - https://www.braintrust.dev/articles/systematic-prompt-engineering
  - https://www.promptfoo.dev/docs/integrations/ci-cd/
  - https://github.com/stanfordnlp/dspy
  - https://www.news.aakashg.com/p/prompt-engineering
  - https://arxiv.org/abs/2203.11171
  - https://aclanthology.org/2025.findings-acl.1030.pdf
  - https://dl.acm.org/doi/10.1145/3722108
related: []
---

## Research Brief

**Topic:** Prompting Best Practices (Comprehensive)
**Mode:** Deep-dive
**Date:** 2026-04-07

This research investigates five sub-questions: (1) the evidence-backed canon of prompting techniques, (2) how techniques compose and interact, (3) common prompting mistakes, (4) task-specific prompting strategies, and (5) prompt evaluation and iteration methodologies. The search prioritized 2025-2026 sources and primary vendor documentation from Anthropic, OpenAI, and Google.

## Search Protocol

| # | Query | Engine | Results Used | Notes |
|---|-------|--------|-------------|-------|
| 1 | Anthropic prompting best practices 2025 2026 Claude | Web | 2 | Anthropic docs, interactive tutorial |
| 2 | OpenAI prompt engineering guide best practices 2025 | Web | 3 | OpenAI docs, GPT-4.1 guide, GPT-5 guide |
| 3 | chain-of-thought prompting research 2025 2026 evidence | Web | 2 | Wharton CoT study, Schulhoff survey |
| 4 | few-shot learning prompting survey 2025 | Web | 1 | NLP zero/few-shot review |
| 5 | prompt optimization methodology evaluation A/B testing 2025 | Web | 3 | Braintrust, promptfoo, systematic PE |
| 6 | Schulhoff "Prompt Report" 2024 comprehensive prompting techniques survey | Web | 2 | arXiv paper, LearnPrompting summary |
| 7 | prompting techniques composition synergistic combinations 2025 | Web | 2 | Lakera guide, emergentmind topic |
| 8 | common prompting mistakes degrade LLM output quality anti-patterns | Web | 3 | MLOps prompt bloat, GoInsight mistakes, prompt defects taxonomy |
| 9 | prompting best practices by task type classification generation analysis code | Web | 2 | PromptingGuide examples, PromptHub code gen |
| 10 | self-consistency prompting technique research evidence 2025 | Web | 2 | PromptingGuide, CISC paper |
| 11 | structured output prompting JSON schema LLM best practices 2025 | Web | 2 | Agenta guide, OpenAI structured outputs |
| 12 | role assignment system prompting effectiveness research 2025 | Web | 2 | PromptHub role study, SAGE study |
| 13 | prompt engineering open source tools libraries DSPy PromptFoo 2025 | Web | 2 | DSPy GitHub, Latitude tools list |
| 14 | LLM-as-judge prompt evaluation rubric scoring methodology 2025 | Web | 2 | EvidentlyAI guide, Confident AI guide |
| 15 | "prompt regression" detection testing CI/CD pipeline 2025 | Web | 2 | Promptfoo CI/CD, Traceloop guide |
| 16 | Google DeepMind prompting best practices Gemini 2025 | Web | 1 | Gemini prompt strategies doc |
| 17 | prompt engineering for code generation best practices 2025 research | Web | 1 | ACM secure code gen study |
| 18 | Shapley analysis prompting technique combinations synergy "BIG-Bench" 2025 | Web | 1 | Shapley workflow optimization paper |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting Best Practices | Anthropic | 2025-2026 | T1 | verified |
| 2 | https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide | GPT-4.1 Prompting Guide | OpenAI | 2025 | T1 | verified |
| 3 | https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide | GPT-5 Prompting Guide | OpenAI | 2025-2026 | T1 | verified |
| 4 | https://arxiv.org/abs/2406.06608 | The Prompt Report: A Systematic Survey of Prompting Techniques | Schulhoff et al. | 2024 (rev. 2025) | T1 | verified |
| 5 | https://learnprompting.org/blog/the_prompt_report | The Prompt Report: Insights | LearnPrompting | 2024 | T3 | verified |
| 6 | https://gail.wharton.upenn.edu/research-and-insights/tech-report-chain-of-thought/ | The Decreasing Value of Chain of Thought in Prompting | Wharton GAIL (Meincke, Mollick, Mollick, Shapiro) | 2025 | T1 | verified |
| 7 | https://ai.google.dev/gemini-api/docs/prompting-strategies | Prompt Design Strategies | Google | 2025-2026 | T1 | verified |
| 8 | https://www.promptingguide.ai/techniques | Prompting Techniques | DAIR.AI | 2025 | T2 | verified |
| 9 | https://home.mlops.community/public/blogs/the-impact-of-prompt-bloat-on-llm-output-quality | The Impact of Prompt Bloat on LLM Output Quality | MLOps Community | 2025 | T3 | verified |
| 10 | https://arxiv.org/abs/2509.14404 | A Taxonomy of Prompt Defects in LLM Systems | Various | 2025 | T1 | verified |
| 11 | https://www.goinsight.ai/blog/llm-prompt-mistake/ | 10 Common LLM Prompt Mistakes | GoInsight | 2025 | T4 | verified |
| 12 | https://www.prompthub.us/blog/role-prompting-does-adding-personas-to-your-prompts-really-make-a-difference | Role Prompting: Does It Make a Difference? | PromptHub | 2025 | T3 | verified |
| 13 | https://www.evidentlyai.com/llm-guide/llm-as-a-judge | LLM-as-a-Judge: Complete Guide | Evidently AI | 2025 | T3 | verified |
| 14 | https://www.braintrust.dev/articles/systematic-prompt-engineering | Systematic Prompt Engineering | Braintrust | 2025 | T3 | verified |
| 15 | https://www.promptfoo.dev/docs/integrations/ci-cd/ | CI/CD Integration for LLM Eval | Promptfoo | 2025 | T2 | verified |
| 16 | https://github.com/stanfordnlp/dspy | DSPy: Programming Language Models | Stanford NLP | 2025 | T1 | verified |
| 17 | https://www.news.aakashg.com/p/prompt-engineering | Prompt Engineering in 2025: The Latest Best Practices | Aakash Gupta | 2025 | T4 | verified |
| 18 | https://arxiv.org/abs/2203.11171 | Self-Consistency Improves Chain of Thought Reasoning | Wang et al. | 2023 (seminal) | T1 | verified |
| 19 | https://aclanthology.org/2025.findings-acl.1030.pdf | Confidence Improves Self-Consistency in LLMs | ACL Findings | 2025 | T1 | verified |
| 20 | https://dl.acm.org/doi/10.1145/3722108 | Prompting Techniques for Secure Code Generation | ACM TOSEM | 2025 | T1 | verified (403) |

## Raw Extracts

### Sub-question 1: What is the current evidence-backed canon of prompting techniques (chain-of-thought, few-shot, role assignment, structured output, self-consistency)?

**From [Source 4, 5] (Schulhoff et al., The Prompt Report):** The most comprehensive survey to date catalogs 58 text-based prompting techniques across 1,565 papers. These are organized into six major categories: (1) Zero-Shot prompting, (2) Few-Shot prompting, (3) Thought Generation (CoT and variants), (4) Ensembling (self-consistency, majority voting), (5) Self-Criticism (self-refine, constitutional AI), and (6) Decomposition (least-to-most, plan-and-solve). Six factors influence few-shot exemplar effectiveness: quantity, order, label distribution, quality, format, and similarity. Closely aligned examples boost accuracy by "up to 90%." On MMLU benchmarks with GPT-3.5-turbo, Few-Shot Chain-of-Thought demonstrated superior performance. Self-consistency, despite popularity, showed limited comparative effectiveness on the benchmark.

**From [Source 1] (Anthropic Prompting Best Practices):** Anthropic's canonical guidance for Claude 4.6 identifies these core techniques: (a) Be clear and direct -- show your prompt to a colleague; if they'd be confused, Claude will be too. (b) Use examples effectively -- 3-5 well-crafted examples dramatically improve accuracy and consistency; wrap in `<example>` tags. (c) Structure prompts with XML tags -- reduces misinterpretation for complex prompts mixing instructions, context, examples, and inputs. (d) Give Claude a role -- even a single sentence focuses behavior and tone. (e) Place long documents at the top, queries at the end -- improves response quality by up to 30% in tests. (f) Ground responses in quotes for long document tasks. (g) Use adaptive thinking with effort parameter rather than manual chain-of-thought budget.

**From [Source 2] (OpenAI GPT-4.1 Guide):** GPT-4.1 follows instructions "more literally" than predecessors, making it highly steerable with clear, unequivocal guidance. Key findings: (a) A single sentence firmly clarifying desired behavior is almost always sufficient to correct course. (b) Prompt-induced planning (requesting step-by-step plans between actions) increased SWE-bench scores by ~4%. (c) Recommended prompt structure: Role/Objective, Instructions, Reasoning Steps, Output Format, Examples, Context, Final instructions. (d) XML and ID|TITLE|CONTENT formats performed well for document formatting; JSON performed poorly for large document sets. (e) Place instructions at both beginning and end of provided context for best long-context performance.

**From [Source 3] (OpenAI GPT-5 Guide):** GPT-5 is more instruction-sensitive than predecessors. Contradictory directives consume reasoning tokens searching for reconciliation. New API parameters: `verbosity` (controls final answer length) and `reasoning_effort` (minimal/medium/high). For code generation, GPT-5 responds well to self-iteration against internal excellence rubrics with 5-7 evaluation categories. Metaprompting -- asking the model itself what phrases to add/remove -- is explicitly recommended.

**From [Source 6] (Wharton CoT Study):** Chain-of-thought prompting shows decreasing value for advanced models. Non-reasoning models (Claude Sonnet 3.5, GPT-4o) benefit 4-14% accuracy gains on GPQA Diamond, but reasoning models (o3-mini, o4-mini) gain only 2-3%. CoT increases response times 35-600%. Gemini Flash 2.5 actually declined 3.3% with CoT. Recommendation: use CoT for non-reasoning models when accuracy gains justify token costs; avoid for reasoning models with built-in capabilities.

**From [Source 18, 19] (Self-Consistency):** Self-consistency samples multiple diverse reasoning paths through few-shot CoT and selects the most consistent answer. Boosts GSM8K by +17.9% over standard CoT. Even when regular CoT is ineffective, self-consistency can still improve results. CISC (2025) enhances self-consistency with confidence-weighted voting, improving both efficiency and accuracy. Limitation: works well for fixed answer sets but falls short on free-form generation tasks.

**From [Source 7] (Google Gemini Strategies):** Google recommends 2-5 few-shot examples and cautions against more (overfitting risk). Gemini 3 reasoning is optimized for default temperature 1.0. Key techniques: break down complex prompts into sequential instructions, prompt chaining, or response aggregation. Explicit planning and self-critique are recommended before final responses.

**From [Source 12] (PromptHub Role Prompting Study):** Role prompting effectiveness is mixed. "Better Zero-Shot Reasoning" improved math accuracy from 53.5% to 63.8% with GPT-3.5. However, none of the personas tested led to statistically significant improvements across comprehensive evaluations. The "idiot" persona unexpectedly outperformed the "genius" persona. Newer models show diminished benefits from basic persona prompting. In-domain, gender-neutral, and work-related roles tend to perform best. Detailed, automatically-generated personas outperform simple hand-crafted ones.

### Sub-question 2: How do prompting techniques compose -- which combinations are synergistic vs. redundant?

**From [Source 4, 5] (Schulhoff et al.):** The six technique categories are designed to be composable. Few-Shot + Thought Generation (CoT) is the dominant synergistic combination, showing superior MMLU performance. Ensembling (self-consistency) layers on top of CoT, but the marginal benefit diminishes with stronger base models.

**From [Source 1] (Anthropic):** Anthropic recommends progressive technique application: start with core techniques, use them consistently, only layer in advanced techniques when they solve a specific problem. Multishot examples work with thinking -- use `<thinking>` tags inside few-shot examples to show reasoning patterns. Self-correction chains are the most common chaining pattern: generate draft, review against criteria, refine.

**From [Source 2] (OpenAI GPT-4.1):** Planning instructions + tool use is synergistic (+4% on SWE-bench). CoT + few-shot examples + structured output format compose well. Place usage examples in a dedicated `# Examples` section (not in tool descriptions) -- this specific placement improved SWE-bench by ~2%.

**From [Source 14] (Braintrust Systematic PE):** Modular prompt architecture enables isolated testing. Separate: system context (role/capabilities), task instructions, input formatting, output format, few-shot examples, and quality guidelines. Dynamic few-shot selection -- matching examples semantically to current inputs -- composes well with chain-of-thought. Conditional logic (adapting instructions based on input characteristics) adds value for heterogeneous workloads.

**From [Web Search] (Shapley analysis, emergentmind):** Shapley analysis reveals positive synergy for in-context demonstrations + reasoning. Negative interactions (redundancy) occur for "overdense" compositions -- too many techniques layered together. Empirical results on BIG-Bench Extra Hard show +4.1 arithmetic mean improvement from optimized compositions over Anthropic's baseline prompt generator. Optimal prompt complexity depends on model capability: stricter, scaffolded prompts aid mid-tier models (GPT-4o) but degrade advanced ones (GPT-5), where standard CoT becomes optimal.

**From [Source 9] (MLOps Prompt Bloat):** Combining too many techniques creates prompt bloat. LLM reasoning degrades around 3,000 tokens. CoT is "more vulnerable to noisy inputs," meaning adding irrelevant context alongside CoT amplifies rather than mitigates degradation. Strategic minimalism outperforms maximalist composition.

**Key synthesis:** The evidence supports a "less is more" pattern for frontier models. Role + clear instructions + few examples is the reliable baseline. Add CoT only when the task genuinely requires multi-step reasoning. Add self-consistency only when accuracy on fixed-answer tasks justifies the cost. Avoid stacking techniques beyond what the specific task demands.

### Sub-question 3: What are the most common prompting mistakes that degrade output quality?

**From [Source 11] (GoInsight -- 10 Common Mistakes):**
1. Being too vague -- using imprecise language like "make it professional" without defining criteria
2. Forgetting to assign a role -- model defaults to generic helper without tone/focus
3. Not defining output format -- unstructured text prevents reliable parsing
4. Providing no examples -- model falls back on general training data
5. Overloading a single prompt -- multiple distinct tasks degrade quality on all
6. Ignoring the context window -- assuming the model remembers prior conversations
7. Not using delimiters -- mixing instructions with data causes confusion and injection vulnerability
8. Not specifying negative constraints -- fails to exclude unwanted content
9. Ignoring length/verbosity -- inconsistent outputs requiring manual editing
10. Using conversational tone for technical tasks -- model prioritizes being "helpful" over accurate

**From [Source 9] (MLOps Prompt Bloat):** Prompt bloat degrades output quality. Key findings: (a) LLM reasoning degrades around 3,000 tokens. (b) Irrelevant information causes "inconsistent predictions and notable decline." (c) Semantically similar but irrelevant information is more confusing than entirely unrelated content. (d) The "lost in the middle" problem: models have reduced attention to information between prompt beginning and end.

**From [Source 10] (Prompt Defects Taxonomy):** Six categories of prompt defects: (1) Specification and Intent -- unclear or misaligned goals, (2) Input and Content -- problems with information provision, (3) Structure and Formatting -- poor organization, (4) Context and Memory -- contextual information issues, (5) Performance and Efficiency -- speed/resource problems, (6) Maintainability and Engineering -- long-term sustainability defects.

**From [Source 1] (Anthropic):** Specific anti-patterns for Claude 4.6: (a) Over-prompting -- tools that undertriggered in previous models now overtrigger with aggressive language like "CRITICAL: You MUST use this tool when..." (b) Using prefilled responses (deprecated in Claude 4.6). (c) Saying "don't" instead of stating what to do -- "Do not use markdown" is less effective than "Use smoothly flowing prose paragraphs." (d) Not providing context for why instructions exist -- explaining motivation helps models generalize.

**From [Source 3] (OpenAI GPT-5):** Contradictory directives are the most damaging mistake with instruction-sensitive models. Example: "Never schedule without consent" conflicting with "auto-assign without contacting patient" causes the model to waste reasoning tokens on reconciliation rather than progressing.

### Sub-question 4: How do prompting best practices differ by task type (classification, generation, analysis, code writing)?

**From [Source 2] (OpenAI GPT-4.1):** For classification tasks, use tools with an enum field containing valid labels, or structured outputs. For long-context retrieval, use citation format `[NAME](ID)` to ground responses. For agentic coding, explicit planning between tool calls increases scores by ~4%.

**From [Source 3] (OpenAI GPT-5):** For code generation: (a) Use `apply_patch` tool rather than full file rewrites to match training distribution. (b) Require explicit planning before function calls. (c) Single tool call per response to avoid disrupting reflection. (d) For frontend development, have the model construct internal rubrics with 5-7 evaluation categories, then self-iterate against them. (e) Provide explicit design system documentation.

**From [Source 1] (Anthropic):** For analysis/research: (a) provide clear success criteria, (b) encourage source verification across multiple sources, (c) use structured approach with competing hypotheses and confidence levels. For agentic coding: minimize overengineering with explicit scope constraints -- "Don't add features beyond what was asked." For document creation: models produce polished output on first try; request explicit design elements.

**From [Source 7] (Google Gemini):** For generation tasks, use completion input patterns (start the outline yourself to guide format). For analysis, use explicit planning: "parse goals, check completeness, create outlines." For multi-step tasks, use prompt chaining or response aggregation patterns.

**From [Source 20] (ACM TOSEM Secure Code Generation):** For code generation, prompting techniques for security have not been thoroughly examined. Shorter prompts (under 50 words) perform better for code generation; longer prompts increase error likelihood and may produce meaningless code.

**From [Source 14] (Braintrust):** For classification tasks, specificity over generality is critical: "If asked about unsupported features, acknowledge and suggest closest alternatives" outperforms general directives. Constraint-driven design (explicit limitations) often improves classification more than additional instructions.

**Task-type summary:**
- **Classification:** Use structured outputs/enums, low temperature (0.0-0.1), explicit label definitions, few-shot examples with balanced label distribution
- **Generation (text):** Role assignment helps for creative tasks; explicit tone/style examples; verbosity controls; request self-critique before final output
- **Analysis:** Structured research approach with competing hypotheses; ground in quotes from source material; explicit success criteria; multi-source verification
- **Code writing:** Short, precise prompts; explicit planning before implementation; single-purpose operations; avoid overengineering prompts; test-driven verification

### Sub-question 5: What prompt evaluation and iteration methodologies exist (A/B testing, rubric scoring, regression detection)?

**From [Source 13] (Evidently AI -- LLM-as-Judge):** Three core evaluation types: (a) Pairwise comparison -- presents two responses, asks LLM to select the better one; achieves 80%+ agreement with human preferences. (b) Direct reference-free scoring -- evaluates individual responses on specific dimensions (tone, clarity, completeness). (c) Reference-based evaluation -- includes answer + reference answer for correctness checking, or answer + context for hallucination detection. Best practices: use binary or limited-choice scores, define each label explicitly, split complex criteria into separate evaluators, include few-shot examples, request chain-of-thought reasoning before judgments, set low temperature.

**From [Source 14] (Braintrust Systematic PE):** Data-driven prompt optimization methodology: (a) Define clear success criteria before optimization. (b) Build modular prompt architecture for isolated component testing. (c) Create representative evaluation datasets covering common scenarios, edge cases, and failure modes. (d) Implement both rule-based scoring (objective) and model-based evaluation (subjective). (e) Version control all changes with performance data attached. (f) Automated evaluation pipelines catching regressions before production.

**From [Source 15] (Promptfoo CI/CD):** Prompt regression testing in CI/CD: (a) Trigger evaluations on pull requests affecting prompts or configuration. (b) Use `--fail-on-error` to halt builds on test failures. (c) Parse JSON output to calculate pass rates against thresholds. (d) Run red team security assessments on regular schedules. (e) Archive results for audit trails. (f) Platform support for GitHub Actions, GitLab CI, and Jenkins.

**From [Source 17] (Aakash Gupta):** Cost-quality optimization: "hill climb up quality first, then down climb cost second." Detailed prompts (2,500+ tokens) cost significantly more but deliver superior quality. Shorter structured prompts (200-400 tokens) reduce costs by up to 76% while maintaining acceptable performance. Iterative refinement based on user interactions and error-handling from real product testing.

**From [Source 3] (OpenAI GPT-5):** Metaprompting for evaluation -- ask the model itself what phrases to add/remove from unsuccessful prompts. OpenAI's prompt optimizer tool surfaces contradictions and ambiguities. Switching from Chat Completions to Responses API with `previous_response_id` improved retail benchmark performance from 73.9% to 78.2%.

**From [Source 1] (Anthropic):** Self-correction chaining is the most common evaluation pattern: generate draft, review against criteria, refine. Each step is a separate API call so you can log, evaluate, or branch at any point. Ask Claude to self-check: "Before you finish, verify your answer against [test criteria]."

**Evaluation methodology summary:**
1. **Define criteria first** -- measurable success indicators before writing prompts
2. **Build evaluation datasets** -- representative scenarios, edge cases, failure modes
3. **Use LLM-as-judge** -- pairwise comparison or rubric-based scoring with CoT reasoning
4. **Integrate into CI/CD** -- automated regression detection on every prompt change
5. **Monitor in production** -- track metrics, sample evaluations, alert on anomalies
6. **Iterate based on failures** -- audit systematic reasoning errors, codify successful patterns

## Findings

### 1. The Evidence-Backed Canon of Prompting Techniques

The Schulhoff et al. Prompt Report catalogs 58 text-based techniques across 1,565 papers, organized into six categories: Zero-Shot, Few-Shot, Thought Generation (CoT), Ensembling (self-consistency), Self-Criticism, and Decomposition [4] (HIGH — T1 systematic survey). All three major vendors converge on a core set: clarity and directness, few-shot examples (3-5), structured formatting (XML tags for Claude, markdown/XML for GPT), role assignment, and document-query ordering [1][2][7] (HIGH — T1 primary documentation convergence).

**Chain-of-thought** shows decreasing value for frontier models. Non-reasoning models gain 4-14% accuracy; reasoning models gain only 2-3%, with 35-600% latency increases. Gemini Flash 2.5 actually declined 3.3% with CoT [6] (HIGH — T1 Wharton study with controlled experiments). CoT can also *reduce* performance by up to 36.3% on tasks involving implicit statistical learning and exception-based classification (see Challenge).

**Self-consistency** boosts GSM8K by +17.9% over standard CoT by sampling multiple reasoning paths and selecting the most consistent answer [18] (HIGH — T1 seminal paper). CISC (2025) enhances this with confidence-weighted voting [19] (HIGH — T1 ACL). Limitation: works for fixed-answer tasks, not free-form generation.

**Role assignment** effectiveness is mixed. "Better Zero-Shot Reasoning" improved math accuracy from 53.5% to 63.8%, but comprehensive evaluations show no statistically significant improvements across tasks. The "idiot" persona unexpectedly outperformed "genius." Newer models show diminished role-prompting benefits [12] (MODERATE — T3 but with controlled comparisons).

**Model-specific divergence:** GPT-4.1+ follows instructions "more literally" — a single clarifying sentence suffices. Claude 4.6 benefits from XML tags and `<example>` wrappers. Gemini 3 is optimized for temperature 1.0 with 2-5 examples [1][2][3][7] (HIGH — T1 vendor docs, though vendor bias applies).

### 2. Technique Composition — Synergies and Redundancies

Few-Shot + CoT is the dominant synergistic combination, showing superior performance on MMLU [4] (HIGH — T1). Planning instructions + tool use is synergistic (+4% SWE-bench) [2] (HIGH — T1). Dynamic few-shot selection (semantically matching examples to inputs) composes well with CoT [14] (MODERATE — T3).

**Critical finding: "less is more" for frontier models.** Prompt bloat degrades reasoning around 3,000 tokens [9]. Semantically similar but irrelevant information is more confusing than entirely unrelated content [9] (MODERATE — T3 but mechanism aligns with context rot research). Overdense compositions show negative interactions — Shapley analysis reveals redundancy when too many techniques are layered (MODERATE — referenced but not from T1 source).

Optimal prompt complexity depends on model capability: stricter scaffolded prompts aid mid-tier models (GPT-4o) but degrade advanced ones (GPT-5), where standard CoT becomes optimal (MODERATE — empirical finding from composition research). Anthropic explicitly recommends progressive technique application: start with core techniques, only layer advanced ones for specific problems [1] (HIGH — T1).

### 3. Common Prompting Mistakes

The most damaging mistakes across sources:

1. **Contradictory directives** — GPT-5 wastes reasoning tokens on reconciliation rather than progressing [3] (HIGH — T1, especially harmful with instruction-sensitive models)
2. **Prompt bloat** — irrelevant information causes inconsistent predictions; "lost in the middle" reduces attention to mid-prompt content [9][10] (MODERATE — T3 + T1 converge)
3. **Over-prompting** — tools that undertriggered in older models now overtrigger with aggressive language like "CRITICAL: You MUST use this tool" [1] (HIGH — T1, Claude-specific but pattern is general)
4. **Vagueness** — "make it professional" without criteria; models default to generic output [11] (LOW — T4 but universal observation)
5. **Missing output format specification** — prevents reliable parsing [11][2] (MODERATE — T4 + T1)
6. **Saying "don't" instead of stating desired behavior** — "Do not use markdown" is less effective than "Use smoothly flowing prose paragraphs" [1] (HIGH — T1)

The six-dimension prompt defect taxonomy provides a systematic checklist: Specification/Intent, Input/Content, Structure/Formatting, Context/Memory, Performance/Efficiency, Maintainability/Engineering [10] (HIGH — T1 peer-reviewed taxonomy).

### 4. Task-Specific Prompting Strategies

**Classification:** Use structured outputs with enum fields and explicit label definitions. Low temperature (0.0-0.1). Few-shot examples with balanced label distribution. Constraint-driven design (explicit limitations) often improves more than additional instructions [2][14] (HIGH — T1 + T3 converge).

**Code generation:** Short, precise prompts outperform long ones — prompts under 50 words produce better code; longer prompts increase error likelihood [20] (HIGH — T1 ACM study). Explicit planning before implementation increases SWE-bench scores by ~4% [2]. Single-purpose operations, avoid overengineering prompts. GPT-5 responds well to self-iteration against internal rubrics with 5-7 evaluation categories [3] (MODERATE — T1 vendor-specific).

**Analysis/research:** Structured approach with competing hypotheses and confidence levels. Ground responses in quotes from source material. Multi-source verification. Explicit success criteria [1] (HIGH — T1).

**Generation (text):** Role assignment helps for creative tasks (despite mixed general evidence). Explicit tone/style examples. Verbosity controls. Completion input patterns — start the output yourself to guide format [7] (MODERATE — T1 but limited empirical backing for pattern).

### 5. Prompt Evaluation and Iteration Methodologies

**LLM-as-judge** is the dominant evaluation approach with three modes: pairwise comparison (80%+ human agreement), direct reference-free scoring, and reference-based evaluation [13] (MODERATE — T3, but the 80% agreement figure varies by domain and has documented biases; see Challenge). Best practices: binary or limited-choice scores, define labels explicitly, split complex criteria into separate evaluators, include few-shot examples, request CoT reasoning before judgments [13].

**CI/CD regression testing** via tools like Promptfoo: trigger evaluations on PRs affecting prompts, use `--fail-on-error` to halt builds, parse JSON output against pass-rate thresholds, archive results for audit trails [15] (HIGH — T2 tool documentation with concrete integration patterns).

**Modular prompt architecture** enables isolated testing: separate system context, task instructions, input formatting, output format, few-shot examples, and quality guidelines. Version control all changes with performance data attached [14] (MODERATE — T3 systematic methodology).

**DSPy** represents the programmatic optimization frontier — replacing manual prompt engineering with learnable modules that auto-optimize prompts via Bayesian optimization [16] (HIGH — T1 Stanford NLP, active development).

**Cost-quality optimization:** "Hill climb up quality first, then down climb cost second." Detailed prompts (2,500+ tokens) cost more but deliver superior quality; shorter structured prompts (200-400 tokens) reduce costs by up to 76% while maintaining acceptable performance [17] (LOW — T4 newsletter, but practical pattern).

**Metaprompting** — asking the model itself what phrases to add/remove from unsuccessful prompts — is now explicitly recommended by OpenAI [3] (MODERATE — T1 vendor recommendation, limited independent validation).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Schulhoff catalogs 58 text-based prompting techniques across 1,565 papers | statistic | [4] | verified |
| 2 | CoT gains only 2-3% for reasoning models vs 4-14% for non-reasoning | statistic | [6] | verified |
| 3 | CoT increases response times 35-600% | statistic | [6] | verified |
| 4 | Gemini Flash 2.5 declined 3.3% with CoT | statistic | [6] | verified |
| 5 | Self-consistency boosts GSM8K by +17.9% over standard CoT | statistic | [18] | verified |
| 6 | Role prompting improved math from 53.5% to 63.8% | statistic | [12] | verified — specific model/test conditions |
| 7 | Planning instructions +4% on SWE-bench | statistic | [2] | verified |
| 8 | Prompt bloat degrades reasoning around 3,000 tokens | statistic | [9] | unverified — T3 single source |
| 9 | Document placement improves response quality "up to 30%" | statistic | [1] | unverified — no published methodology |
| 10 | Prompts under 50 words perform better for code generation | statistic | [20] | verified |
| 11 | LLM-as-judge achieves 80%+ agreement with human preferences | statistic | [13] | verified — but varies dramatically by domain |
| 12 | Shorter structured prompts reduce costs by up to 76% | statistic | [17] | unverified — T4, no methodology |
| 13 | Few-Shot + CoT is the dominant synergistic combination | attribution | [4] | verified |
| 14 | GPT-4.1 follows instructions "more literally" than predecessors | attribution | [2] | verified — vendor claim |
| 15 | CoT reduces performance up to 36.3% on certain task types | statistic | Challenge | verified — Sprague et al. ICLR 2025 |

## Challenge

**Coverage gaps.** The document omits several important findings. "Mind Your Step (by Step)" (Sprague et al., ICLR 2025) demonstrated that CoT *reduces* performance by up to 36.3% on tasks involving implicit statistical learning, visual pattern recognition, and exception-based classification -- task categories absent from this review. The emerging shift from prompt engineering to *context engineering* (assembling the right information, not crafting the right phrasing) is unaddressed despite being a dominant 2026 theme. The document also lacks discussion of prompt fragility across model versions: production systems pinned to specific model snapshots (e.g., `gpt-5-2025-08-07`) behave differently on the next release, making "best practices" a moving target. The few-shot "over-prompting dilemma" (arxiv 2509.13196) -- where additional examples paradoxically degrade advanced model performance -- receives no coverage.

**Source bias.** Of 20 sources, 5 are vendor documentation (Anthropic, OpenAI, Google) treated as authoritative despite serving a marketing function. Vendor docs recommend their own features (Anthropic's XML tags, OpenAI's `apply_patch`, Google's temperature defaults) without disclosing how those recommendations were validated. Independent research from Wharton (EMNLP 2024) found that expert persona prompting -- recommended by all three vendors -- actually *degrades* factual accuracy. The document uncritically relays vendor claims (e.g., "up to 30% improvement" from document placement) without noting these figures lack published methodology or sample sizes.

**Methodological concerns.** The LLM-as-judge evaluation methodology is presented optimistically, but research identifies 12 latent biases in LLM evaluators, including self-preference bias (GPT-4 favors its own outputs, NeurIPS 2024) and positional bias (swapping answer order flips judgments, IJCNLP 2025). The claimed "80%+ agreement with human preferences" obscures that this varies dramatically by domain and collapses on subjective tasks. Benchmark results (MMLU, GSM8K, SWE-bench) are cited as evidence for technique effectiveness, but a 2025 study showed LLM accuracy drops 24.2% when relevant information is embedded in longer real-world contexts -- a gap between benchmark conditions and production environments that the document does not acknowledge. The Schulhoff survey catalogs 58 techniques but does not rank them by effect size or reproducibility, making the "canon" more of an inventory than an evidence hierarchy.

## Canonical Tools and Frameworks

| Tool | Purpose | URL |
|------|---------|-----|
| DSPy | Programmatic prompt optimization framework; replaces manual prompting with learnable modules | https://github.com/stanfordnlp/dspy |
| Promptfoo | Open-source prompt testing, evaluation, and CI/CD regression detection | https://github.com/promptfoo/promptfoo |
| Braintrust | Prompt evaluation platform with A/B testing, dataset management, and scoring | https://www.braintrust.dev |
| Langfuse | Open-source LLM observability with prompt management and A/B testing | https://langfuse.com |
| Agenta | Open-source prompt testing with version control and side-by-side comparisons | https://github.com/agenta-ai/agenta |
| DAIR.AI Prompting Guide | Community-maintained reference for prompting techniques with examples | https://www.promptingguide.ai |
| Anthropic Interactive Tutorial | Hands-on prompt engineering tutorial with exercises | https://github.com/anthropics/prompt-eng-interactive-tutorial |
| OpenAI Prompt Optimizer | Built-in tool for surfacing prompt contradictions and ambiguities | https://platform.openai.com/docs/guides/prompt-generation |
| DeepEval | Open-source LLM evaluation framework with CI/CD integration | https://github.com/confident-ai/deepeval |
| LangChain | Modular framework for building LLM workflows with reusable prompts | https://github.com/langchain-ai/langchain |
