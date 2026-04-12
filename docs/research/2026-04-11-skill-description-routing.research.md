---
name: "Skill and Tool Description Characteristics for LLM Routing Accuracy"
description: "What description factors improve trigger recall and routing precision in LLM tool/skill selection: evidence from vendor docs, adversarial research, and agentic benchmarks — with explicit confidence levels and empirical gaps."
type: research
sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
  - https://developers.openai.com/api/docs/guides/function-calling
  - https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html
  - https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html
  - https://gorilla.cs.berkeley.edu/leaderboard.html
  - https://arxiv.org/abs/2305.15334
  - https://arxiv.org/abs/2307.16789
  - https://arxiv.org/abs/2501.05255
  - https://arxiv.org/abs/2512.07497
  - https://arxiv.org/html/2503.13657v1
  - https://arxiv.org/html/2510.02554v1
  - https://achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-21e0a82b7847
  - https://www.analyticsvidhya.com/blog/2026/03/claude-skills-custom-skills-on-claude-code/
  - https://arxiv.org/abs/2602.20426
  - https://aclanthology.org/2025.naacl-long.44
related: []
---

# Skill and Tool Description Characteristics for LLM Routing Accuracy

## Key Findings

**What works (MODERATE–HIGH confidence):**
- Descriptions that convey *both* what the skill does *and* when to use it outperform those that answer only one. The "Use when..." clause is the documented trigger pattern across Anthropic and OpenAI; it is prescriptive consensus, not experimentally ablated.
- For Claude Code specifically: the 250-character truncation limit is the binding constraint. Only the first 250 characters participate in routing. Descriptions should front-load the most discriminating routing signal.
- Assertive, specific wording increases selection rates — causal evidence from adversarial research (ToolTweak: ~20% → 81% in a 5-tool slate). Direction is supported; transferability to non-adversarial settings is untested.
- Description quality becomes *more* important at scale, not less: as skill count grows, the per-skill character budget shrinks dynamically (1% of context window), making each character carry more weight.

**What is undocumented (the empirical gaps):**
- The undertriggering/overtriggering tradeoff from "pushy" language is not quantified anywhere. The heuristic is documented by Anthropic as a workaround, but no study measures whether assertive descriptions increase false positives in mixed-query settings.
- No controlled ablation on description length, trigger phrase placement (front vs. end), or synonym density was retrieved. All length guidance is prescriptive vendor convention.
- LangChain has no structured description authoring guidance — docstring-based, "informative and concise" only. This is a near-absence of guidance, not a gap in this research.

**The most important caveat for WOS:**
All T2 research studies API-style function calling (JSON schema in API payload), not system-prompt-injected skill descriptions (Claude Code's actual mechanism). Whether findings transfer is an untested assumption. The architectural surfaces are different; the routing behavior may or may not be analogous.

---

## Search Protocol

| # | Query / URL | Results / Notes |
|---|-------------|-----------------|
| 1 | https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview | 301 redirect → platform.claude.com |
| 2 | https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview | Retrieved: tool use overview — how Claude decides when to call, based on user request + description; no description authoring guidance here |
| 3 | https://docs.anthropic.com/en/docs/build-with-claude/tool-use/best-practices-for-tool-definitions | 301 redirect → platform URL; platform URL returned 404 Not Found |
| 4 | https://platform.openai.com/docs/guides/function-calling | 403 Forbidden — unreachable |
| 5 | https://developers.openai.com/api/docs/guides/function-calling | Retrieved: guidance on description clarity, "intern test," examples vs. reasoning model caveat, <100 tool reliability bound |
| 6 | https://python.langchain.com/docs/how_to/tool_calling/ | 308 redirect → docs.langchain.com/oss — overview page, no tool description guidance |
| 7 | https://python.langchain.com/docs/concepts/tools/ | 308 redirect → same overview page — no tool description guidance |
| 8 | https://docs.anthropic.com/en/docs/claude-code/skills | 301 redirect → code.claude.com/docs/en/skills |
| 9 | https://code.claude.com/docs/en/skills | Retrieved: full skill description format, 250-char truncation, undertriggering/overtriggering guidance, disable-model-invocation, pushy heuristic |
| 10 | https://arxiv.org/abs/2305.15334 | Retrieved: Gorilla abstract — hallucination, argument accuracy, retrieval augmentation mitigates routing errors |
| 11 | https://arxiv.org/abs/2307.16789 | Retrieved: ToolLLM abstract — dataset + neural API retriever; no routing precision detail in abstract |
| 12 | `LLM tool description routing accuracy precision recall ablation study 2024 2025 arxiv` | Returned routing papers (model-to-model routing, not tool-within-agent routing); arxiv:2510.15955 on tool output processing gap |
| 13 | `function calling description format routing LLM benchmark undertriggering overtriggering 2024` | CallNavi (arXiv:2501.05255), BFCL V4, Databricks blog, ToolACE |
| 14 | https://arxiv.org/abs/2501.05255 | Retrieved: abstract — hybrid routing (LLM for selection, fine-tuned for parameters), 100+ API candidate scenarios |
| 15 | https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html | Retrieved: description format impacts, parameter extraction failures, parallel function failures, REST URL omission |
| 16 | https://www.databricks.com/blog/unpacking-function-calling-eval | Returned CSS/styling content only — unusable |
| 17 | `LLM agent tool selection failure modes description quality undertriggering overtriggering 2024 2025` | arXiv:2512.07497 (KAMI benchmark), arXiv:2503.13657 (MASFT failure taxonomy) |
| 18 | https://arxiv.org/abs/2512.07497 | Retrieved: KAMI benchmark, 900 traces, premature action, over-helpfulness, CSV tool avoidance |
| 19 | https://arxiv.org/html/2512.07497v2 | Retrieved: full detail — Granite tool avoidance, DeepSeek substitution, Chekhov's gun overtriggering, accuracy 58.5%/74.6%/92.2% |
| 20 | `tool description "synonym coverage" OR "trigger phrase" OR "example invocation" LLM routing selection 2024` | LLM-based prompt routing papers; emergentmind topics; no direct synonym-coverage ablation found |
| 21 | `OpenAI function calling best practices description guidelines tool selection accuracy 2024 2025` | Retrieved: strict mode, role prompting, <100 tool bound, May 2025 in-distribution bounds, "intern test" guideline |
| 22 | https://community.openai.com/t/prompting-best-practices-for-tool-use-function-calling/1123036 | Retrieved: community thread — debate about parameter visibility, no description optimization guidance |
| 23 | https://arxiv.org/html/2503.13657v1 | Retrieved: MASFT 14-failure-mode taxonomy; communication challenges; +14% from targeted fixes |
| 24 | `LLM tool selection "description length" accuracy routing precision "many tools" scaling degradation 2024` | Tool RAG (Red Hat), ToolScale, BFCL averages 3 tools, OpenAI 128-tool hard limit |
| 25 | https://next.redhat.com/2025/11/26/tool-rag-the-next-breakthrough-in-scalable-ai-agents/ | Retrieved: CSS/metadata only — article body not accessible |
| 26 | https://achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-21e0a82b7847 | Retrieved: 1–3 tools optimal, 10+ risks degradation, OpenAI 128 hard limit, BFCL max tested 37 tools |
| 27 | https://arxiv.org/html/2510.02554v1 (ToolTweak) | Retrieved: adversarial description manipulation raises selection from ~20% to 81%; ordinal name bias; JSD divergence metric |
| 28 | `Anthropic Claude Code skill description trigger automatic invocation "when to use" best practices 2024 2025` | code.claude.com/skills, analyticsvidhya, resources.anthropic.com PDF, agentskills.io |
| 29 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Retrieved: comprehensive authoring guide — description field, third person requirement, specificity, 1024-char max, 500-line SKILL.md limit |
| 30 | https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf | PDF not text-readable via fetch — binary content |
| 31 | https://www.analyticsvidhya.com/blog/2026/03/claude-skills-custom-skills-on-claude-code/ | Retrieved: undertriggering/overtriggering definitions, "pushy" description advice, action-verb prefix, trigger scenario listing |
| 32 | `LangChain tool description best practices "when to use" "tool_description" routing agent 2024 2025` | Overview and multi-agent docs; no LangChain-specific description guidance on description quality found |
| 33 | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Retrieved: progressive disclosure, name+description triggering, undertriggering/overtriggering named, iterative refinement recommended |
| 34 | https://gorilla.cs.berkeley.edu/leaderboard.html | Retrieved: BFCL V4 metrics overview; Irrelevance Accuracy (IrrelAcc) measure for abstention |
| 35 | https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html | Retrieved: undertriggering (fuel-check omission) and overtriggering (redundant authentication) named explicitly; long-context category |
| 36 | `Berkeley function calling leaderboard "irrelevance detection" "tool selection" description characteristics accuracy 2024` | BFCL irrelevance detection: 875 test entries, IrrelAcc metric; Relevance Detection for open-ended cases |
| 37 | `"tool description" "when to use" OR "when NOT to use" LLM agent routing "false positive" OR "false negative" 2024 2025` | Patronus.ai routing tutorial; misrouting downstream cost; non-stationary distribution challenge |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| S1 | https://code.claude.com/docs/en/skills | Extend Claude with Skills | Anthropic | 2025–2026 | T1 | verified |
| S2 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Agent Skills Overview | Anthropic | 2025–2026 | T1 | verified |
| S3 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill Authoring Best Practices | Anthropic | 2025–2026 | T1 | verified |
| S4 | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Equipping Agents with Agent Skills | Anthropic Engineering | 2025 | T1 | verified |
| S5 | https://developers.openai.com/api/docs/guides/function-calling | Function Calling | OpenAI | 2024–2025 | T1 | verified |
| S6 | https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html | Berkeley Function-Calling Leaderboard (BFCL) | UC Berkeley / Gorilla LLM | 2024 | T2 | verified |
| S7 | https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html | BFCL V3: Multi-Turn & Multi-Step | UC Berkeley / Gorilla LLM | 2024 | T2 | verified |
| S8 | https://gorilla.cs.berkeley.edu/leaderboard.html | BFCL V4 Leaderboard | UC Berkeley / Gorilla LLM | 2024–2026 | T2 | verified |
| S9 | https://arxiv.org/abs/2305.15334 | Gorilla: LLM Connected with Massive APIs (Patil et al.) | UC Berkeley | 2023 | T2 | verified |
| S10 | https://arxiv.org/abs/2307.16789 | ToolLLM / ToolBench (Qin et al.) | Multiple | 2023 | T2 | verified |
| S11 | https://arxiv.org/abs/2501.05255 | CallNavi: LLM Function Calling and Routing | Multiple | 2025 | T2 | verified |
| S12 | https://arxiv.org/abs/2512.07497 | How Do LLMs Fail in Agentic Scenarios? (KAMI) | Multiple | 2025 | T2 | verified |
| S13 | https://arxiv.org/html/2503.13657v1 | Why Do Multi-Agent LLM Systems Fail? (MASFT) | Multiple | 2025 | T2 | verified |
| S14 | https://arxiv.org/html/2510.02554v1 | ToolTweak: An Attack on Tool Selection | Multiple | 2024 | T2 | verified |
| S15 | https://achan2013.medium.com/how-many-tools-functions-can-an-ai-agent-has-21e0a82b7847 | How Many Tools Can an AI Agent Have? | Allen Chan / Medium | 2025 | T3 | verified |
| S16 | https://www.analyticsvidhya.com/blog/2026/03/claude-skills-custom-skills-on-claude-code/ | Claude Skills Explained | AnalyticsVidhya | 2026 | T3 | verified |
| S17 | https://platform.openai.com/docs/guides/function-calling | Function Calling (OpenAI docs) | OpenAI | 2024–2025 | T1 | unreachable (403) |
| S18 | https://python.langchain.com/docs/concepts/tools/ | Tools Concept (LangChain) | LangChain | 2024–2025 | T1 | unreachable (308 redirect to unhelpful overview) |
| S19 | https://www.databricks.com/blog/unpacking-function-calling-eval | Unpacking Function Calling Eval | Databricks | 2024 | T3 | unreachable (CSS only) |
| S20 | https://arxiv.org/abs/2602.20426 | Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use | Multiple | 2026 | T2 | verified (abstract) |
| S21 | https://aclanthology.org/2025.naacl-long.44 | EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction | Multiple | 2025 | T2 | verified (ACL Anthology URL confirmed; PDF not retrieved) |

## Source Evaluation (SIFT)

| # | Source | Tier | SIFT Assessment | Flags |
|---|--------|------|-----------------|-------|
| S1 | Anthropic Claude Code Skills docs | T1 | Primary source, stated rationale (250-char truncation, context budget architecture). Official Anthropic documentation. | — |
| S2 | Anthropic Agent Skills Overview | T1 | Primary source. States rationale (~100 tokens per skill drives conciseness). 1,024-char max documented. | — |
| S3 | Anthropic Agent Skills Best Practices | T1 | Primary source. Prescriptive guidance with stated reasoning (context window as shared resource). Third-person requirement has stated rationale (system prompt injection). | — |
| S4 | Anthropic Engineering Blog: Agent Skills | T1 | Official Anthropic engineering post. States design rationale for progressive disclosure. Blog format but author-attributed Anthropic publication. | Borderline T1 — no ablation data; guidance is design intent, not measurement |
| S5 | OpenAI Function Calling docs | T1 | Primary source. Intern test has stated rationale. Reliability bound (<100 tools) stated as "in-distribution" without citing empirical study. | Reliability bound is stated as a guideline, not a measured threshold |
| S6 | BFCL Blog (V1) | T2 | UC Berkeley empirical benchmark. Formatting impact observed on real models. | Observation-level, not controlled ablation |
| S7 | BFCL V3 Multi-Turn Blog | T2 | Named undertriggering/overtriggering examples. Empirical multi-turn evaluation. | Examples are qualitative illustrations, not quantified failure rates |
| S8 | BFCL V4 Leaderboard | T2 | IrrelAcc metric formally measures overtriggering abstention (875 test entries). Direct evidence for SQ2. | Measures model abstention, not description-driven failure specifically |
| S9 | Gorilla (arXiv:2305.15334) | T2 | Peer-reviewed. Shows retrieval augmentation reduces hallucination in large API sets. Abstract only — full ablation details not extracted. | Only abstract retrieved; specific description-quality ablation not confirmed |
| S10 | ToolLLM (arXiv:2307.16789) | T2 | Peer-reviewed. 16,464 APIs; neural retriever for large-scale selection. | Abstract only; description characteristics not specifically studied |
| S11 | CallNavi (arXiv:2501.05255) | T2 | Peer-reviewed. 100+ API candidate routing. Hybrid routing architecture. | Focus on parameter generation, not description-driven selection |
| S12 | KAMI (arXiv:2512.07497) | T2 | Peer-reviewed. 900 traces, named failure modes, quantified accuracy per model. Direct evidence for SQ2. | Agentic task failures; description wording not the specific independent variable |
| S13 | MASFT (arXiv:2503.13657v1) | T2 | Peer-reviewed. 14-failure-mode taxonomy. +14% from interventions. | Multi-agent system focus; not tool-selection description quality specifically |
| S14 | ToolTweak (arXiv:2510.02554v1) | T2 | Peer-reviewed. Adversarial description optimization raises selection 20%→81%. JSD metric. | Adversarial research, not optimal-design research — causal claims are valid but direction is manipulation, not improvement |
| S15 | Allen Chan / Medium | T3 | Practitioner post. Token cost calculations plausible. Tool count thresholds (1–3 optimal, 10+ risky) presented without experimental citations. | Thresholds are practitioner observation; no methodology |
| S16 | AnalyticsVidhya | T3 | Practitioner post. Mirrors Anthropic official guidance on undertriggering/overtriggering. "40% support ticket reduction" claim has no methodology or sample size. | ⚠ Unverifiable practitioner claim: "40% cut in support tickets" — do not cite as evidence |
| S17 | platform.openai.com/docs/guides/function-calling | T1 | Unreachable (403) | Excluded from sources frontmatter |
| S18 | python.langchain.com/docs/concepts/tools/ | T1 | Unreachable (redirect to unhelpful overview) | Excluded from sources frontmatter — LangChain gap confirmed |
| S19 | Databricks blog | T3 | Unreachable (CSS only) | Excluded |

**Evaluator summary:**
- 14 verified sources (4 T1, 7 T2, 3 T3)
- 3 unreachable/excluded (S17, S18, S19)
- Critical gap: No LangChain tool description guidance captured — SQ3 cross-platform comparison is Anthropic vs. OpenAI only
- Critical gap: No empirical ablation on description length, synonym coverage, or trigger phrase placement
- Caution: S16's "40% support ticket" claim must not be cited as evidence
- Caution: S5 reliability bound (<100 tools) is a stated guideline, not an empirically measured threshold

## Raw Extracts

### Sub-Question 1: Description Characteristics Affecting Routing Accuracy

**[S1 — Anthropic Claude Code Skills docs]**

"Claude uses this [description field] to decide when to apply the skill." The description should "include both what the skill does and when to use it." Descriptions longer than 250 characters are truncated in the skill listing to reduce context usage. The full description field maximum is 250 characters in the listing context (even though the underlying field allows more). The first paragraph of markdown content is used as a fallback if `description` is omitted.

Troubleshooting guidance explicitly states: "Check the description includes keywords users would naturally say." For overtriggering: "Make the description more specific." The description is "the primary triggering mechanism — include both what the skill does AND specific contexts for when to use it."

**[S2 — Anthropic Agent Skills Overview]**

"Claude uses this metadata at startup and includes it in the system prompt." The description field is described as "discovery information." The example given includes both action and context trigger: `"Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."` The field maximum is 1,024 characters; descriptions cannot contain XML tags.

"The description is critical for skill selection: Claude uses it to choose the right Skill from potentially 100+ available Skills."

**[S3 — Anthropic Agent Skills Best Practices]**

"Be specific and include key terms. Include both what the Skill does and specific triggers/contexts for when to use it."

Third-person requirement: "Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems." (Good: "Processes Excel files and generates reports." Avoid: "I can help you process Excel files.")

Effective description structure demonstrated:
- PDF Processing: action phrase + "Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."
- Excel Analysis: action phrase + "Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files."
- Git Commit: action phrase + "Use when the user asks for help writing commit messages or reviewing staged changes."

Vague descriptions called out as anti-patterns: "Helps with documents," "Processes data," "Does stuff with files."

Naming conventions: gerund form recommended (`processing-pdfs`, `analyzing-spreadsheets`). Avoid vague names: `helper`, `utils`, `tools`.

**[S4 — Anthropic Engineering Blog: Agent Skills]**

"Pay special attention to the `name` and `description` of your skill. Claude will use these when deciding whether to trigger the skill in response to its current task." The description provides "just enough information for Claude to know when each skill should be used without loading all of it into context." No quantitative thresholds reported.

**[S5 — OpenAI Function Calling docs]**

"Explicitly describe the purpose of the function and each parameter (and its format), and what the output represents." Use system prompts to "clarify when and when *not* to use each tool." The "intern test": "Could someone use your function with only the provided description? If not, add those clarifications to your prompt."

Role prompting guidance: "You are an AI retail agent. As a retail agent, you can help users cancel or modify pending orders..." to set base behavior context framing tool scope.

For deferred tools: "keep namespace descriptions concise while placing detailed guidance in function descriptions — the namespace helps with tool selection, the function description ensures proper usage."

Caveat on examples: "Adding examples may hurt performance for reasoning models." (No further quantification given.)

**[S6 — BFCL Blog]**

"Function documentation formatting impacts results." GPT's "function documents are difficult to format and their typings are restrictive in real-world scenarios." Inflexible type systems (e.g., float vs. number) force manual conversion and reduce accuracy.

**[S14 — ToolTweak adversarial study]**

Tool names and descriptions both influence selection. Ordinal naming (`Tool 1` vs `Tool 2`) creates systematic bias — models show preference for numerically-ranked names. Adversarial description optimization raised selection rates from ~20% baseline to 81% by iteratively refining tool names and descriptions using LLM feedback. Effective adversarial descriptions used: subjective wording, assertive cues, implicit comparisons, and structural patterns that survive paraphrasing. This demonstrates that surface-level text metadata has strong causal influence on routing decisions.

**[S16 — AnalyticsVidhya on Claude Skills]**

"The description field in frontmatter is what Claude uses for relevance evaluation. Keep it under 20 words. Focus on when to use it, not what it does." Contrast offered: `'Activates for prospect qualification conversations'` beats `'A comprehensive tool for evaluating prospect fit'`.

"The practice that had the biggest impact was explicit edge case documentation... Adding a 'When NOT to use this skill' section cut support tickets by 40%." (Practitioner claim, no methodology described.)

---

### Sub-Question 2: Failure Modes — Undertriggering vs. Overtriggering

**[S1 — Claude Code Skills docs]**

Undertriggering: "Claude doesn't use your skill when expected." Causes: description doesn't include keywords users would naturally say; skill not discoverable. Fix: "Check the description includes keywords users would naturally say."

Overtriggering: "Claude uses your skill when you don't want it." Fix: "Make the description more specific." Hard fix: `disable-model-invocation: true`.

Description budget constraint: "if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request." Environment variable `SLASH_COMMAND_TOOL_CHAR_BUDGET` can raise the limit. Budget scales dynamically at 1% of the context window, fallback 8,000 characters.

**[S3 — Best Practices]**

"Strengthen the skill's description and instructions so the model keeps preferring it, or use hooks to enforce behavior deterministically." If a skill "seems to stop influencing behavior after the first response, the content is usually still present and the model is choosing other tools or approaches."

**[S4 — Engineering Blog]**

Two named problems: undertriggering (skill not activated when relevant) and overtriggering (skill activated inappropriately). Recommended fix: iterative — "Monitor how Claude uses your skill in real scenarios and iterate based on observations."

**[S7 — BFCL V3 Multi-Turn]**

Explicit undertriggering example: models "fail to infer the need to check the existing fuel level before making the decision." Explicit overtriggering example: models "needlessly planned to authenticate the user even though authentication had already been completed." These are named as the two opposing failure modes in multi-step function calling.

**[S12 — KAMI / arXiv:2512.07497]**

Undertriggering (tool avoidance): Granite 4 Small "consistently avoids the optimal Python-execution strategy in all CSV tasks, instead attempting to 'eye-ball' aggregated values — a strategy that always fails." DeepSeek V3.1 reliably invokes Python for computational tasks.

Overtriggering (over-helpfulness): "When requested entities don't exist, [DeepSeek V3.1] autonomously decides to substitute a similar company name without explicit instruction, producing misleading data." Called "wrong adaptation to missing values."

Context-pollution overtriggering (Chekhov's gun): "Models attempt using all provided information, even when irrelevant." In SQL task with distractor tables, models "fixate on irrelevant tables, causing incorrect JOIN logic."

Quantitative accuracy: Granite 4 Small 58.5%, Llama 4 Maverick 74.6%, DeepSeek V3.1 92.2% pooled accuracy across agentic tasks. Architecture-matched V3 (identical to V3.1) scores only 59.4% — pointing to post-training RL, not scale, as the driver.

**[S13 — MASFT / arXiv:2503.13657]**

14 distinct failure modes in 3 categories: specification/system design failures, inter-agent misalignment, task verification/termination. "Agents mainly communicate via unstructured text, leading to ambiguities." Targeted interventions (improved prompting, topology redesign) yielded only +14% for ChatDev — suggesting systemic issues rather than surface-level description fixes alone.

**[S16 — AnalyticsVidhya]**

"Undertriggering occurs when Claude fails to load a skill despite a matching request. This typically results from vague descriptions that don't align with how users naturally phrase requests. Overtriggering happens when overlapping descriptions cause the wrong skill to fire."

"Make descriptions a little bit 'pushy': include prompts like 'Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics...'"

**[S8 — BFCL V4 Leaderboard]**

IrrelAcc (Irrelevance Accuracy): measures fraction of no-call cases where model correctly abstains. 875 test entries in irrelevance detection category. Distinguishes from Relevance Detection (at least one function relevant). This is a formal benchmark of the overtriggering failure mode: model calling a tool when none should be called.

---

### Sub-Question 3: Cross-Platform Guideline Comparison (Anthropic / OpenAI / LangChain)

**[S1, S2, S3 — Anthropic]**

- Primary trigger mechanism: `description` field in YAML frontmatter
- Field max: 250 chars in skill listing context (truncated); 1,024 chars max total
- Required content: what the skill does + when to use it (both)
- Recommended format: third-person, action-verb prefix, "Use when..." clause
- Negative trigger: `disable-model-invocation: true` (hard off) or `user-invocable: false` (Claude-only)
- No guidance on synonym coverage or explicit trigger phrases
- No quantitative evidence cited; guidance is prescriptive
- Rationale given: descriptions load into context at startup (~100 tokens each); efficiency drives conciseness
- Examples in body: recommended; examples in description: not discussed separately

**[S5 — OpenAI]**

- Primary trigger mechanism: function `description` field in JSON schema
- No stated character limit in retrieved content
- Required content: purpose, parameters, formats, outputs; when and when *not* to use
- Recommended format: "intern test" — could an intern use this with only the description?
- Role prompting: system prompt context frames tool scope before descriptions
- Examples caveat: "Adding examples may hurt performance for reasoning models" — diverges from Anthropic (no such warning given)
- Reliability bound: fewer than ~100 tools and ~20 arguments per tool is "in-distribution" for reliability
- Namespace descriptions vs. function descriptions: namespace for selection, function for usage — two-level description hierarchy
- Rationale given: offloads interpretation burden from model to explicit specification; reduces token usage and improves accuracy

**[LangChain — not retrieved]**

LangChain tool description guidance was not accessible via the fetched URLs (both redirected to a general overview with no description authoring content). Web search results describe LangChain routing at the agent/workflow level, not individual tool description authoring. Gap: no direct LangChain tool description guidance captured in this research.

**Key divergence identified:**

OpenAI explicitly warns that examples may hurt reasoning model performance; Anthropic's best practices recommend examples as a pattern for output quality improvement (no analogous caveat). This represents a documented cross-platform divergence with practical implications.

---

### Sub-Question 4: Optimal Description Length

**[S1 — Claude Code Skills]**

Descriptions longer than 250 characters are truncated in the skill listing. Character budget scales at 1% of context window, fallback 8,000 characters total across all skills. Per-entry cap of 250 characters regardless of budget. Description field itself can be longer (up to 1,024 chars per S2), but listing context truncates at 250.

**[S2 — Agent Skills Overview]**

Description field maximum: 1,024 characters. Rationale: metadata (name + description) loads at startup (~100 tokens per skill). Progressive disclosure means description length is not the main token cost driver — it's the SKILL.md body that loads on trigger.

**[S3 — Best Practices]**

"Keep SKILL.md body under 500 lines for optimal performance." Conciseness principle: "The context window is a public good." Challenge each piece of information: "Does Claude really need this explanation?" Concise PDF example (~50 tokens) vs. verbose version (~150 tokens) shown as explicit good/bad contrast.

**[S5 — OpenAI]**

No stated character limit retrieved. Guidance: "detailed enough to prevent misuse." For deferred tools: concise namespace descriptions + detailed function descriptions (two-level system).

**[S16 — AnalyticsVidhya]**

Practitioner guidance: "Keep it under 20 words. Focus on when to use it, not what it does." No empirical basis stated.

**[S15 — Allen Chan / Medium]**

Minimizing token usage requires "short parameter names and description." Each tool definition consumes tokens: simple single-parameter tool = 96 tokens, 28-parameter tool = 1,633 tokens. "Sending that many tools in every interaction will reduce reasoning quality" at scale.

**Gap:** No empirical study was found that directly measures routing accuracy as a function of description length, tests a range of lengths, or identifies a precision/recall inflection point. The evidence is entirely prescriptive from vendor guidance, not experimental.

---

### Sub-Question 5: Example Invocations and Trigger Phrase Placement

**[S3 — Best Practices]**

Examples pattern for descriptions: "For Skills where output quality depends on seeing examples, provide input/output pairs just like in regular prompting." Examples are placed in the SKILL.md body, not the description field. This is about output format guidance, not routing trigger.

Example description that includes trigger contexts: `"Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes."` — trigger phrases embedded naturally in the description.

**[S5 — OpenAI]**

"Include examples and detailed guidance, particularly to address recurring failures." Caveat: "Adding examples may hurt performance for reasoning models." No placement guidance (description vs. system prompt vs. function body) specified beyond this.

**[S1 — Claude Code Skills, Troubleshooting]**

"Check the description includes keywords users would naturally say." This implies trigger phrases should match user vocabulary, embedded directly in the description.

**[S16 — AnalyticsVidhya]**

"Starting with the action verb ('Generates…', 'Reviews…', 'Formats…'). Specifying trigger scenarios explicitly. Including likely keywords from natural user requests." Placement: description field, front-loaded.

**[S14 — ToolTweak]**

Adversarial research: iterative refinement of tool names and descriptions using LLM feedback — with subjective wording, assertive cues, and structural patterns — raised selection rates from ~20% to 81%. This is evidence that specific phrasing choices have large causal impact on routing, but it is adversarial rather than optimal-design research.

**Gap:** No controlled ablation study was found comparing trigger phrase placement (beginning vs. end vs. middle of description) or density (how many trigger phrases). No study on synonym coverage impact was found.

---

### Sub-Question 6: The "Slightly Pushy" Heuristic — Evidence and Tradeoffs

**[S1 — Claude Code Skills]**

The pushy heuristic is documented as a practitioner pattern: "Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, make the skill descriptions a little bit 'pushy'. For instance, include prompts like 'Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics...'" This is presented as a workaround for a known failure mode.

Countermeasure to overtriggering from pushy descriptions: "Make the description more specific" or use `disable-model-invocation: true`.

**[S16 — AnalyticsVidhya]**

Mirrors S1: "Claude has a tendency to undertrigger skills." Pushy descriptions are presented as the fix.

**[S3 — Best Practices]**

Does not use the term "pushy" but recommends strengthening description and instructions if a skill "stops influencing behavior." Iterative process: test, observe, refine. No stated risk of overtriggering from stronger descriptions.

**[S14 — ToolTweak]**

Adversarial evidence that assertive, subjective wording and implicit comparisons strongly biases selection. Jensen-Shannon Divergence used to measure distributional shift. Paraphrasing defenses reduce but don't eliminate the effect. This suggests pushy language does carry overtriggering risk in multi-skill ecosystems if descriptions are not carefully scoped.

**[S7 — BFCL V3]**

Overtriggering example: model "needlessly planned to authenticate the user even though authentication had already been completed." The failure mode is invocation of correct-but-already-done tools — not directly caused by description wording, but illustrates that over-eagerness is a real class of error.

**Gap:** No controlled study directly tests the pushy heuristic vs. neutral language and measures the undertriggering/overtriggering tradeoff quantitatively. The evidence for the heuristic is practitioner consensus; the risk evidence is indirect (adversarial research and qualitative failure analysis).

---

### Sub-Question 7: Routing at Scale (Tool Count Effects)

**[S2 — Agent Skills Overview]**

"Claude uses it [the description] to choose the right Skill from potentially 100+ available Skills." Progressive disclosure design: metadata only at startup (~100 tokens per skill), full skill body only on trigger. This architectural design explicitly addresses scale.

**[S5 — OpenAI]**

"Any setup with fewer than ~100 tools and fewer than ~20 arguments per tool is considered in-distribution and should perform within expected reliability bounds." Implicit: beyond ~100 tools, behavior is not guaranteed. "Filter tools to avoid ballooning payloads by taking advantage of the allowed_tools parameter to use only the tools that are necessary."

**[S15 — Allen Chan]**

Hard limit: OpenAI 128 tools maximum. BFCL average test: 3 functions per test, maximum tested 37. "Performance degradation likely starts much sooner" than the hard limit. Token cost examples: 37-tool set = 6,218 tokens. 1–3 tools "optimal." "4–10 tools: may slow down execution and consume more tokens." "10+: risks token limit breaches, reduced inference accuracy, and increased costs."

**[S9 — Gorilla / arXiv:2305.15334]**

Retrieval augmentation at scale: integrating a document retriever allows the model to "adapt to documentation changes at test time" — reducing hallucination and improving accuracy across large API sets (HuggingFace, TorchHub, TensorHub). Evidence that retrieval-based selection is a viable architecture for large tool counts.

**[S11 — CallNavi / arXiv:2501.05255]**

"Prior benchmarks limit API candidates to fewer than five per task." CallNavi introduces 100+ API candidate selection as a more realistic large-scale scenario. Hybrid routing approach: LLM for selection (generalization), fine-tuned model for parameter generation (precision). Large API sets require different strategies than small sets.

**[S10 — ToolLLM / arXiv:2307.16789]**

Dataset: 16,464+ real-world APIs across 49 categories. Neural API retriever recommends APIs per instruction — at this scale, retrieval rather than in-context enumeration is the proposed solution. Zero-shot generalization tested on APIBench (out-of-distribution).

**[S6 — BFCL Blog]**

Proprietary models (GPT series) demonstrate "superior performance handling multiple and parallel function calls compared to open-source counterparts." Implicit: tool count and parallelism interact with model capability.

**[S7 — BFCL V3]**

"Long-Context Multi-Turn" category introduces "large volumes of extraneous data (hundreds of files, thousands of records)" to test performance under information overload — a proxy for many-tool scenarios.

**[S14 — ToolTweak]**

At baseline (~20% selection rate in an ecosystem of tools), adversarial description optimization can move a tool's selection rate to 81%. This implies that in crowded tool ecosystems, description quality strongly determines selection share — both a vulnerability and a signal that descriptions remain high-leverage even at scale.

**Web search summary (no direct source):**

Tool RAG (retrieval-augmented generation for tool selection) is described as tripling tool invocation accuracy while reducing prompt length by half in some reported cases. Dense and hybrid retrieval (semantic + keyword) cited as improving both recall and precision. ToolScale framework cited for auto-synchronizing tool knowledge bases with dynamic retrieval for thousands of tools. These are practitioner/blog claims; primary sources not directly verified in this research.

---

## Challenge

### Causal vs. Correlational Claims

**"Descriptions longer than 250 characters are truncated in the skill listing" (S1)**
Causal claim — verifiable as a stated architectural constraint, not an empirical finding. Re-fetching the current live documentation confirms this claim is accurate as of April 2026. Exact quote: "Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage." The documentation also clarifies that this is a per-entry cap regardless of the overall character budget. Claim stands.

**"Adding examples may hurt performance for reasoning models" (S5)**
Practitioner assertion from vendor documentation with zero quantification. The OpenAI docs say exactly this — "Adding examples may hurt performance for reasoning models" — but provide no numbers, no model list, no conditions under which this fires. The claim is directionally plausible (reasoning models chain steps rather than pattern-match, so example-heavy prompts may bias step generation), but there is no study cited by OpenAI and none found in this research. The draft correctly notes the lack of quantification but does not flag this as unsubstantiated. It should be treated as a stated caveat, not evidence.

**ToolTweak: "phrasing has strong causal impact on routing"**
The causal claim is valid but severely context-constrained. ToolTweak ran adversarial optimization across 5-tool slates (10 tasks × 5 tools each). The draft generalizes this to "crowded tool ecosystems," but the paper's baseline ecosystem is deliberately small. Furthermore, the attack exploits iterative LLM feedback to find successful phrasing — which is an optimization process, not a design principle. Most critically: the paper shows differential selection rates within a fixed task-matched tool set. It does not demonstrate that the same phrasing strategies improve routing in benign, mixed-query settings. Transferability across models is also mixed: selection rate doubled for Qwen but quadrupled for DeepSeek; Llama and Gemini are more resilient. The draft presents ToolTweak as general evidence for description-driven routing without acknowledging these constraints.

**The "slightly pushy" heuristic and overtriggering risk**
The draft correctly identifies this as practitioner consensus with indirect risk evidence (ToolTweak). The specific risk ToolTweak implies is not examined closely enough. ToolTweak's adversarial descriptions use "subjective wording and assertive cues" embedded in "factual-sounding claims" — the paper explicitly names this mechanism. However, the paper does **not** measure whether these same descriptions cause false positives on off-topic queries (overtriggering). The adversarial success is measured as selection rate within task-relevant slates; the overtriggering question — does a pushy description cause activation when the query has no relevance to the skill — is not studied. The draft implies ToolTweak supports an overtriggering risk from pushy language, but this is an extrapolation, not a direct finding.

**"1–3 tools optimal, 10+ risks degradation" (Allen Chan / Medium, S15)**
Pure practitioner assertion with no experimental citation or controlled methodology. The search confirmed the Medium article states "nobody has systematically tested sending a large number of tools in an agent definition." The thresholds (1–3, 4–10, 10+) are narrative categories constructed from token-cost arithmetic and the BFCL's incidental average of 3 tools per test — not from experiments that varied tool count and measured routing accuracy. These are not empirical thresholds.

**"OpenAI <100 tools in-distribution" (S5)**
The draft conflates two separate OpenAI guidances. The main function calling docs (developers.openai.com) say "fewer than 20 functions available at the start of a turn" as a soft suggestion — not 100. The "<100 tools" bound with "<20 arguments per tool" appears in the o3/o4-mini reasoning model prompting guide specifically. These are guidance for different model families and contexts. The draft treats them as a single unified claim about OpenAI's guidance without flagging that the number and scope differ by model family. Additionally, even within the o3/o4-mini guide, the text frames this as "in-distribution based on training data and observed behavior" — not a measured empirical bound.

**"No empirical ablation on description length was found" (draft's own gap claim)**
This self-assessment is substantially correct but incomplete. A February 2026 paper — "Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use" (arXiv:2602.20426) — directly studies description quality effects on routing via teacher-forcing evaluation that isolates description-induced failures from cascading errors. It finds causal impact of description quality on agent success (70.1% vs. 67.3% subtask-level success on StableToolBench). However, this paper studies overall description quality (clarity, completeness, schema alignment), not description length specifically. A second paper found — "Enhancing LLM-based Agents with Concise Tool Instruction" (NAACL 2025, ACL Anthology 2025.naacl-long.44) — directly targets conciseness vs. verbosity in tool descriptions. The PDF was unreadable via fetch but the title and venue confirm this paper exists and addresses conciseness effects. The draft's claim that no empirical ablation on description length exists should be revised to "no ablation was retrieved in this research session, but at least one paper (NAACL 2025) directly targets this question."

---

### Counter-Evidence Found

**Description quality has measured causal effect (arXiv:2602.20426)**
The "Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use" (Feb 2026) demonstrates via teacher-forcing evaluation — which holds intermediate tool call context fixed and isolates description-induced failures — that description quality causally affects agent task success. This is the strongest causal evidence found for description quality mattering, and it was not in the draft. The paper proposes rewriting tool descriptions automatically using a curriculum approach and shows 70.1% vs. 67.3% subtask-level success on StableToolBench, plus robustness improvements as tool count exceeds 100. This paper directly contradicts the draft's framing that the causal link between description wording and routing is supported only by adversarial research.

**Concise descriptions paper (NAACL 2025)**
"Enhancing LLM-based Agents with Concise Tool Instruction" is a peer-reviewed NAACL 2025 paper that appears to directly address the description length question (the draft claims no empirical ablation on length exists). PDF was unreadable via fetch. The draft's claim about the gap in empirical length research should be flagged as possibly incorrect.

**ToolTweak ecosystem size matters**
ToolTweak's experimental ecosystem was 5 tools per task — a small slate. The draft uses this to argue that description quality "remains high-leverage even at scale," but the paper's setup does not support that generalization. In a larger, semantically diverse tool ecosystem, adversarial phrasing effects may dilute. No study runs ToolTweak-style experiments at 50+ tool counts.

**No counter-evidence found that description wording is irrelevant**
No study was found showing that routing is invariant to description wording. The weight of evidence — adversarial research (ToolTweak), description rewriting research (arXiv:2602.20426), vendor documentation, and BFCL formatting observations — consistently supports that description text matters. This part of the draft's thesis appears robust.

**OpenAI's 20-function soft suggestion vs. 100-tool in-distribution bound**
The main OpenAI function calling docs recommend "fewer than 20 functions" as a soft suggestion. The 100-tool bound is o3/o4-mini-specific, framed as in-distribution guidance based on training data, not a measured accuracy inflection. Both numbers appear in the draft but their distinct scope is not separated.

**LangChain description guidance exists — but is minimal**
LangChain's guidance is: the function's docstring becomes the tool description; the docstring should be "informative and concise." The official LangChain docs confirm that "the description string is critical, as it's the LLM's only understanding of what the tool does and what arguments it expects. A poorly described tool gets misused or ignored." There is no "when to use" clause pattern, no third-person requirement, no character limit, no format template. LangChain's guidance is entirely practitioner-level and substantially thinner than Anthropic's or OpenAI's published best practices. The draft states "no LangChain tool description guidance captured" — this is accurate for structured authoring guidance, but misses the docstring-as-description mechanism and the "informative and concise" baseline. This is a partial gap, not a total gap.

---

### LangChain Gap — Additional Search Results

Additional search attempts confirmed LangChain has no structured description authoring documentation equivalent to Anthropic's best practices or OpenAI's function calling guide. What exists:

- The tool description is the Python function docstring. LangChain agents receive it verbatim as the tool's description.
- Official LangChain documentation says: "the docstring should be informative and concise to help the model understand the tool's purpose."
- When agents misroute tools, the community recommendation is to switch to Pydantic schemas for cleaner schema generation — not to improve the docstring. This is a signal that LangChain's ecosystem treats description quality as an engineering problem (schema structure) rather than a prompt-authoring problem (description text).
- No "when to use" clause pattern, third-person requirement, character limit guidance, or negative trigger mechanism is documented in LangChain.

Conclusion: LangChain's tool description guidance is real but minimal. It is not a gap in the research — it is accurately a near-absence of guidance, which itself is a meaningful finding for the cross-platform comparison in SQ3.

---

### Logical Gaps and Alternative Interpretations

**Gap 1: Claude Code skills vs. API tool use — different routing mechanisms**
The draft treats these as equivalent surfaces for the same routing mechanism. They are not. Claude Code skill routing works by injecting description metadata into the system prompt at session startup (as the docs confirm: "Claude uses this metadata at startup and includes it in the system prompt"). API tool use (function calling) delivers tool definitions in the API payload, where models may have been fine-tuned specifically on structured function schemas. The research base — ToolTweak, BFCL, KAMI, CallNavi, Gorilla — entirely studies API-style function calling. Whether findings about function call routing transfer to system-prompt-injected skill description routing is an untested assumption. This is the draft's largest single logical gap. The mechanisms may behave similarly but the evidence base does not demonstrate this.

**Gap 2: Routing vs. argument generation conflated throughout**
Most of the cited research — BFCL, KAMI, CallNavi, Gorilla — measures end-to-end task success or argument generation accuracy, not routing/selection as an isolated step. The draft correctly notes this in the Source Evaluation table but does not trace the specific claims where this conflation affects the findings. For example: KAMI's accuracy figures (58.5%, 74.6%, 92.2%) measure agentic task success, not routing precision. The BFCL adversarial formatting finding (S6) is about parameter extraction failures, not selection failures. The draft uses these numbers in discussions of "routing accuracy" without the qualifier.

**Gap 3: Third-person requirement and "discovery problems"**
The draft reports Anthropic's claim that first-person descriptions "can cause discovery problems" when injected into the system prompt. No evidence is cited for why point-of-view would affect routing accuracy. The stated rationale (inconsistent POV in a system prompt causes problems) is plausible for instruction-following but is not a documented routing mechanism. No study compares first- vs. third-person tool descriptions on routing outcome. This is a formatting convention with a stated but unverified rationale.

**Gap 4: ToolTweak adversarial mechanism not probed for benign implications**
ToolTweak's assertive wording works through "factual-sounding subjective claims" and "implicit comparisons." The paper's attack prompt trains descriptions to position a tool as the optimal choice without overt deception. This is the same structural pattern as the "pushy" heuristic. However, ToolTweak doesn't measure whether these descriptions also cause selection in off-target query contexts. The overtriggering risk from pushy descriptions is inferred but not demonstrated.

**Gap 5: Vocabulary matching assumed to be literal**
The Anthropic troubleshooting guidance says "Check the description includes keywords users would naturally say." This implies surface-level keyword match. But LLM routing operates via semantic embedding, not keyword lookup. A description that doesn't contain the user's exact words may still route correctly via semantic proximity, and a description with exact keyword matches may still fail on paraphrase. The draft presents keyword matching as the mechanism without examining whether the actual routing is semantic rather than lexical.

---

### Missing Coverage

**1. Technical vs. natural-language vocabulary alignment**
The research question asks what description characteristics "most reliably improve trigger recall." The draft addresses keyword matching from the user's natural vocabulary (Anthropic guidance) but does not ask: should descriptions use technical vocabulary (exact tool capabilities) or natural language vocabulary (how users phrase requests)? These may diverge significantly. A skill that "generates TypeScript interfaces from JSON schemas" might be triggered by users saying "convert my JSON to types" — only natural-language vocabulary coverage would match. No study in the draft addresses this vocabulary alignment question.

**2. Small-set vs. large-set routing dynamics**
ToolTweak uses 5 tools, BFCL averages 3, CallNavi introduces 100+. The draft provides scale data but never asks: are the description characteristics that improve routing in a 3-tool set the same as those that work in a 50-tool set? The scale section (SQ7) covers quantity effects on overall accuracy but not whether description strategy should change with scale. For the Claude Code context (typically 5–15 skills in a plugin), the BFCL 3-tool averages are more applicable than the 100+ scenarios — but the draft doesn't make this differentiation.

**3. Overlapping descriptions between skills**
The draft has no discussion of what happens when two skills have semantically overlapping descriptions. This is a practical problem in any multi-skill ecosystem (e.g., a "git-commit" skill and a "code-review" skill that both trigger on "review staged changes"). The Partnership on AI failure analysis (2025) identified overlapping tool descriptions as a significant failure mode. No guidance on disambiguation is present in the draft.

**4. Effect of description on selection vs. effect on output quality**
The draft distinguishes routing (selection) from argument generation in the source evaluation table but does not discuss whether description text affects output quality post-trigger. Anthropic's best practices place examples in SKILL.md body (not description) precisely because they affect output quality, not routing. The research question is about routing, but a complete answer should acknowledge that optimizing the description for routing may conflict with optimizing SKILL.md for output quality — and the split between them is a design choice, not an invariant.

---

### Challenger Assessment

**Well-supported findings:**
- Descriptions are the primary routing mechanism in Claude Code (T1 primary source, confirmed architectural)
- 250-character truncation limit is accurate and current (re-verified against live docs)
- Pushy/assertive wording increases selection rate (ToolTweak, causal within its experimental bounds)
- Description quality causally affects agent task success, not just correlates (arXiv:2602.20426, teacher-forcing isolation)
- Scale beyond ~20-100 tools degrades reliability (multiple converging sources, though thresholds are guidance not measurements)
- LangChain has no structured description authoring guidance (confirmed by multiple fetch attempts and search)

**Weakly supported findings:**
- "Examples may hurt reasoning model performance" — vendor assertion, no quantification, no study
- "1–3 tools optimal" thresholds — practitioner narrative from token arithmetic, no controlled study
- Third-person POV requirement prevents "discovery problems" — stated rationale, no mechanism or evidence
- Keyword front-loading is better than end-loading — prescriptive guidance, no ablation

**Unsupported practitioner assumptions presented without adequate caveat:**
- The "pushy" heuristic controlling undertriggering without increasing overtriggering — the overtriggering risk from pushy language in mixed-query settings is not studied
- ToolTweak as evidence for "description quality remains high-leverage even at scale" — ToolTweak used 5-tool slates; the generalization to scale is an extrapolation
- The <100-tool reliability bound applying to all OpenAI models — it is specifically documented for o3/o4-mini and appears with different numbers elsewhere
- Research on API function calling transferring directly to system-prompt-injected skill descriptions — this mechanism equivalence is assumed throughout but never validated

## Findings

**Bottom line:** Description content reliably affects routing — the mechanism is real and causal, not just observed. The two highest-leverage factors are (1) including what the skill does AND specific "Use when..." trigger contexts, and (2) matching vocabulary to how users naturally phrase requests. Everything else — trigger phrase placement, synonym density, pushy language — is practitioner convention with no controlled evidence. The most important gap: all research studies API function-call routing, not system-prompt-injected skill descriptions, so transferability to Claude Code is assumed but unvalidated.

---

### SQ1: What description characteristics measurably affect routing accuracy?

**Content over format** (HIGH — T1 Anthropic S1/S2/S3, T1 OpenAI S5, indirectly T2 S20)

The single consistent requirement across platforms: descriptions must convey both (a) what the skill does and (b) when to use it. Descriptions that answer only "what" but not "when" underperform on routing. This is documented prescriptively by Anthropic (S1–S3) and OpenAI (S5), and the causal direction is supported by arXiv:2602.20426 (S20), which isolates description-induced failures via a curriculum learning framework and shows description quality directly predicts agent task success on StableToolBench. *(Specific accuracy figures reported by the challenger as 70.1% vs. 67.3% are not confirmed in the abstract and require human verification against the full paper.)*

**Keyword vocabulary matching user phrasings** (MODERATE — T1 S1, T3 S16)

Anthropic troubleshooting guidance: "Check the description includes keywords users would naturally say." This is prescriptive, not measured. The mechanism is stated as keyword matching, but LLM routing operates semantically — a description without the user's exact words may still route correctly via semantic proximity. The specific vocabulary alignment claim is plausible but unvalidated against the actual routing mechanism.

**Specific trigger contexts (the "Use when..." pattern)** (MODERATE — T1 S2/S3)

Anthropic's documented example structure: `"[Action verb phrase]. Use when [user context or file type or phrasing]."` This pattern appears in all Anthropic examples but is not compared against descriptions without the "Use when" clause. The rationale is sound (the clause provides explicit discrimination signal), but no ablation compares it to alternatives.

**Assertive, specific wording raises selection rate** (MODERATE — T2 S14; constrained to 5-tool slates)

ToolTweak (S14) demonstrates adversarially that assertive descriptions with implicit comparisons and subjective cues can raise a tool's selection rate from ~20% to 81%. This is causal within the paper's 5-tool experimental bounds. The implications for benign description design are suggestive but not direct — the paper studies manipulation, not optimization.

**No controlled ablations on** trigger phrase position (start vs. end), synonym density, specificity vs. breadth, or example inclusion within descriptions. These remain conventions without evidence.

---

### SQ2: Failure modes — undertriggering vs. overtriggering

**Undertriggering causes** (HIGH — T1 S1/S4, T2 S7/S12)

Documented causes:
1. **Vocabulary mismatch** — description doesn't include keywords users naturally use (S1)
2. **Vague descriptions** — "Helps with documents" provides insufficient discrimination signal (S1, S16)
3. **Context budget exhaustion** — with many skills, descriptions are shortened to fit the character budget, stripping the keywords needed for matching (S1: 1% of context window / 8,000-char budget)
4. **Tool avoidance** — model "eye-balls" answers rather than invoking the skill (KAMI S12: Granite 4 Small CSV task failure, 58.5% accuracy vs. 92.2% for DeepSeek V3.1)

**Overtriggering causes** (MODERATE — T1 S1, T2 S7/S8/S12/S14)

Documented causes:
1. **Overlapping descriptions** between two skills with similar "Use when" clauses (S1, S16 — stated cause, not ablated)
2. **Overgeneralized "pushy" language** — assertive trigger conditions that don't distinguish irrelevant from relevant queries (implied by S14, not directly measured)
3. **Chekhov's gun** — models attempt to use all available tools when context contains irrelevant ones (KAMI S12: models fixate on irrelevant distractor tables in SQL tasks)
4. **Already-completed action retriggering** — model replays authentication after it's already done (BFCL V3 S7: explicit named example)

**Formal measurement of overtriggering** (HIGH — T2 S8)

BFCL V4's irrelevance detection metric (formally "IrrelAcc" — metric name requires human verification against BFCL V4 documentation) measures model abstention when no tool should be invoked. Test entry count is unverified: the BFCL V3 blog reports 240 (Irrelevance) + 882 (Live Irrelevance) = 1,122 total; a figure of 875 cited by the gatherer does not match any retrieved source and should be treated as unverified. This is nonetheless the most direct benchmark measure of overtriggering behavior found. No equivalent metric exists for undertriggering in the same benchmark.

**The asymmetry in intervention guidance:** Undertriggering has a recommended fix (strengthen description, add keywords, add "pushy" language). Overtriggering has weaker guidance (make description more specific, or use `disable-model-invocation: true` as a hard stop). No study measures whether the fixes for undertriggering cause overtriggering or vice versa — the tradeoff is documented as a concern but not quantified.

---

### SQ3: Cross-platform guideline comparison

| Factor | Anthropic (Claude Code) | OpenAI (Function Calling) | LangChain |
|--------|------------------------|---------------------------|-----------|
| Description mechanism | YAML frontmatter `description` field, injected into system prompt at startup | JSON schema `description` field, in API payload | Python function docstring |
| Character limit | 250-char truncation in listing; 1,024-char total field max | None stated | None stated |
| Required content | What skill does + when to use it | Purpose, parameters, output, when/when-not-to-use | Informative and concise (no structure) |
| Format requirement | Third-person, action-verb prefix | "Intern test" (could an intern use this alone?) | None |
| Negative triggers | `disable-model-invocation: true` or description specificity | Explicit "when NOT to use" guidance recommended | None |
| Example guidance | Examples in SKILL.md body, not description | Examples in description; caveat for reasoning models | None |
| Rationale given | Context efficiency, progressive disclosure, system-prompt injection | Offloads interpretation to spec, reduces token use | None |
| Tool count guidance | N/A (progressive disclosure architecture scales) | <20 functions (general soft suggestion); <100 tools/<20 args per tool (o3/o4-mini specific) | None |

**Key documented divergence** (HIGH — T1 S3 vs. S5)

OpenAI explicitly warns: "Adding examples may hurt performance for reasoning models." Anthropic's best practices place examples in the SKILL.md body for output quality, not routing — so they don't conflict directly, but Anthropic has no analogous caveat. This divergence is documented but not explained by either platform; the rationale behind OpenAI's reasoning-model caveat is unstated.

**LangChain guidance: near-absence** (HIGH — challenger confirmed via search)

LangChain treats the Python docstring as the tool description and provides no authoring guidance beyond "informative and concise." No character limit, no "when to use" pattern, no format requirement, no negative triggers. This near-absence of guidance is itself the finding for SQ3: LangChain delegates description quality to the developer without a framework.

---

### SQ4: Optimal description length

**Hard constraint drives effective length** (HIGH — T1 S1/S2)

For Claude Code: the 250-character truncation in the skill listing is the binding constraint. Regardless of the 1,024-character field maximum, only the first ~250 characters participate in routing decisions. This means the optimal description is one that packs the most routing signal into 250 characters — not longer.

**Prescriptive shorter-is-better consensus** (MODERATE — T1 S5, T3 S16)

OpenAI guidance: "detailed enough to prevent misuse" — no specific length recommendation. AnalyticsVidhya (T3, S16): "under 20 words" — with the supporting logic that when-to-use signal beats what-it-does verbosity. Anthropic's best practices illustrate concise descriptions (PDF skill example: ~50 tokens preferred over ~150 tokens). Consistent direction, no experimental basis.

**Empirical gap** (HIGH — confirmed by two independent searches)

No study was retrieved that directly measures routing accuracy as a function of description character count. NAACL 2025 (S21, "EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction") appears to study this question directly; its PDF was not retrieved, so its findings cannot be incorporated. The claim that shorter descriptions improve routing is well-supported by prescriptive consensus but not by controlled experiment in this research.

---

### SQ5: Example invocations and trigger phrase placement

**Trigger phrases belong in the description, not examples** (HIGH — T1 S1/S3)

Anthropic's design makes a functional distinction: the description field routes (trigger phrases, "Use when..." clauses, keyword coverage); the SKILL.md body provides output-quality guidance (examples, detailed instructions). Mixing examples into the description would consume the 250-character budget available for routing signal.

**"Use when..." clause is the documented trigger phrase format** (MODERATE — T1 S2/S3)

The documented example pattern: `"[What skill does]. Use when [specific user context / file type / phrasing]."` Action verb first, then capabilities, then trigger contexts. No ablation compares this pattern against alternatives. Anthropic's examples are consistent but not experimentally validated against other formats.

**Front-loading is documented but not ablated** (LOW — T3 S16)

AnalyticsVidhya (S16): "Starting with the action verb ('Generates…', 'Reviews…', 'Formats…'). Specifying trigger scenarios explicitly." The WOS check-skill criterion #7's "first sentence front-loads the primary trigger phrase" is consistent with this practitioner convention. No study compares front-loaded vs. end-loaded trigger phrases on routing outcome.

**OpenAI: examples in descriptions are acceptable with caveats** (MODERATE — T1 S5)

OpenAI function calling: "Include examples and detailed guidance, particularly to address recurring failures." The caveat — "may hurt performance for reasoning models" — is unquantified. For Claude Code, the architectural choice to keep examples out of descriptions and in SKILL.md body is a design decision, not an empirically validated optimization.

---

### SQ6: The "slightly pushy" heuristic

**Documented as a workaround, not a design principle** (HIGH — T1 S1, T3 S16)

The "pushy" heuristic is documented by Anthropic as a response to a known failure mode ("Claude has a tendency to undertrigger skills"). The documentation presents it as a workaround: `"Make sure to use this skill whenever the user mentions dashboards, data visualization..."`. This is design intent from the primary source, not a claim that the heuristic is optimal.

**Causal direction for recall: plausible but indirect** (MODERATE — T2 S14)

ToolTweak (S14) demonstrates that assertive, specific, implicit-comparison wording increases selection rates (adversarial context, 5-tool slates). The direction of effect (assertive wording → higher recall) is supported. Transferability to non-adversarial settings is untested.

**Overtriggering risk from pushy descriptions: real concern, unquantified** (LOW)

ToolTweak's assertive descriptions use the same structural patterns as the pushy heuristic (implicit claims, assertive cues). However, ToolTweak measures differential selection *within* task-relevant slates — it does not measure whether pushy descriptions cause selection on off-topic queries. The overtriggering risk in mixed-query settings is inferred from adversarial mechanism, not demonstrated. No study directly tests pushy vs. neutral descriptions on overtriggering rates.

**The tradeoff is undocumented** (HIGH — confirmed gap)

No controlled study measures the undertriggering-reduction vs. overtriggering-increase tradeoff from pushy language. This is the central empirical gap for the WOS authoring guide's guidance. The evidence supports "pushy helps recall" but cannot quantify the precision cost.

---

### SQ7: Routing at scale (tool count effects)

**Progressive disclosure is the architectural response** (HIGH — T1 S1/S2)

Claude Code's design: description metadata (~100 tokens per skill) loads at startup; the full SKILL.md body loads only on trigger. This is explicitly documented as the architectural solution to scale, allowing "100+ available Skills" without proportional context growth.

**Context budget scales with context window; per-skill budget is dynamic** (HIGH — T1 S1)

Character budget = 1% of context window (fallback 8,000 chars). At 100 skills, each gets ~80 chars of budget — well below the 250-char field length, meaning descriptions are further truncated as skill count grows. This creates a diminishing-returns dynamic: more skills → less routing signal per skill.

**API-level reliability degrades with tool count** (MODERATE — T1 S5)

OpenAI guidance: "fewer than 20 functions" (general recommendation); "<100 tools and <20 arguments per tool in-distribution" (specific to o3/o4-mini reasoning models). These are guidelines, not measured inflection points. The specific numbers differ by model family.

**Academic benchmarks severely underrepresent real-world scale** (HIGH — T2 S6/S7/S8/S11)

BFCL averages 3 tools per test, max 37. CallNavi calls 100+ a "more realistic" scenario. ToolLLM uses 16,464 APIs but with a neural retriever (not in-context enumeration). Research findings from 3-tool test environments may not transfer to 20-skill Claude Code deployments.

**At scale: description quality has higher leverage, not lower** (MODERATE — T2 S14/S20)

ToolTweak: in a 5-tool ecosystem, description quality moves selection from ~20% to 81%. arXiv:2602.20426 (S20): description rewriting improves robustness as tool count grows, with gains observed on StableToolBench across tool-count conditions per the abstract. Both suggest that description quality becomes *more* important at scale, not less — a counterintuitive finding that merits explicit mention in WOS authoring guidance.

---

### Cross-cutting: The mechanism transfer gap

**The most important unresolved question for WOS specifically** (HIGH — confirmed by challenger)

All T2 research (ToolTweak, BFCL, KAMI, CallNavi, Gorilla, ToolLLM) studies API-style function calling: tool definitions delivered in the API payload, where models may have been specifically fine-tuned on structured JSON schemas. Claude Code skill routing works differently: description metadata is injected into the system prompt at session startup as prose text. Whether the research findings on API function-call routing transfer to system-prompt-injected description routing is unvalidated. The mechanisms may behave similarly — Claude's underlying routing is likely semantic in both cases — but no study directly compares the two surfaces. WOS guidance that relies on this research should note this transfer assumption.

---

### Summary: Evidence quality per authoring recommendation

| Recommendation | Evidence quality | Basis |
|---------------|-----------------|-------|
| Include "what + when" in every description | MODERATE | T1 prescriptive consensus (Anthropic, OpenAI); indirectly T2 causal (S20) |
| Stay within 250 chars (Claude Code) | HIGH | T1 architectural fact (S1/S2) |
| Third-person format (Claude Code) | MODERATE | T1 stated rationale (system prompt injection); mechanism unverified |
| Match vocabulary to user natural language | MODERATE | T1 prescriptive (S1); mechanism semantic not lexical |
| "Use when..." trigger clause | MODERATE | T1 documented pattern (S2/S3); no ablation |
| Front-load action verb | LOW | T3 practitioner (S16); no ablation |
| Pushy language to fix undertriggering | MODERATE | T1 documented workaround (S1); causal direction indirect (S14) |
| Pushy language safe for precision | LOW | No study measures overtriggering from pushy descriptions |
| Examples in descriptions (OpenAI) | LOW | T1 stated; reasoning-model caveat unquantified |
| Keep tool count below 20–100 | MODERATE | T1 guidance (S5); model-family specific, not measured threshold |
| Description quality matters more at scale | MODERATE | T2 partial evidence (S14, S20); both constrained experimental setups |

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | 250-character truncation in skill listing | statistic | S1 | verified |
| 2 | 1,024-character field maximum for description | statistic | S2 | verified |
| 3 | ~100 tokens per skill (metadata loaded at startup) | statistic | S2 | verified |
| 4 | Claude uses description to choose from "potentially 100+ available Skills" | quote/statistic | S2/S3 | verified |
| 5 | 70.1% vs. 67.3% subtask-level success on StableToolBench (arXiv:2602.20426) | statistic | S20 | corrected |
| 6 | KAMI: Granite 4 Small 58.5%, Llama 4 Maverick 74.6%, DeepSeek V3.1 92.2% pooled accuracy | statistic | S12 | verified |
| 7 | Architecture-matched V3 (identical to V3.1) scores only 59.4% | statistic | S12 | verified |
| 8 | ToolTweak: selection rate from ~20% to 81% | statistic | S14 | verified |
| 9 | ToolTweak experimental setup uses 5-tool slates | statistic | S14 | verified |
| 10 | BFCL average test: 3 functions per test, maximum tested 37 | statistic | S15 | verified |
| 11 | OpenAI 128-tool hard limit | statistic | S15 | verified (S15 only — not in S5) |
| 12 | OpenAI: fewer than 20 functions guidance | statistic | S5 | verified |
| 13 | OpenAI "<100 tools and <20 arguments per tool in-distribution" (o3/o4-mini) | statistic | S5 | corrected |
| 14 | 875 test entries in irrelevance detection | statistic | S8 | corrected |
| 15 | IrrelAcc metric in BFCL V4 | attribution | S8 | human-review |
| 16 | arXiv:2602.20426 — paper exists with title "Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use" | attribution | S20 | verified |
| 17 | NAACL 2025 ACL Anthology 2025.naacl-long.44 — paper exists | attribution | S21 | corrected |
| 18 | 1% of context window / 8,000-char budget (description character budget) | statistic | S1 | verified |
| 19 | BFCL overtriggering example: "needlessly planned to authenticate the user even though authentication had already been completed" | quote | S7 | verified (paraphrase only — exact wording differs) |
| 20 | BFCL undertriggering example: model failed to "infer the need to check the existing fuel level" | quote | S7 | verified |
| 21 | 900 traces in KAMI | statistic | S12 | verified |
| 22 | arXiv:2602.20426 uses "teacher-forcing evaluation" to isolate description-induced failures | attribution | S20 | corrected |
| 23 | Third-person requirement: "inconsistent point-of-view can cause discovery problems" | quote | S3 | verified |
| 24 | 500-line SKILL.md body limit | statistic | S3 | verified |
| 25 | Concise PDF example ~50 tokens vs. verbose ~150 tokens | statistic | S3 | verified |
| 26 | JSD (Jensen-Shannon Divergence) metric in ToolTweak | attribution | S14 | verified |

### Corrections

**Claim 5 — arXiv:2602.20426 accuracy figures (70.1% vs. 67.3%)**

The draft states "70.1% vs. 67.3% subtask-level success on StableToolBench" as specific figures from the paper. The abstract of arXiv:2602.20426 does not contain these percentages. The abstract mentions StableToolBench and RestBench as evaluation benchmarks and describes "consistent gains on unseen tools," but no specific accuracy percentages appear in the abstract text retrieved. The figures may be present in the paper body (not the abstract), so they cannot be confirmed or refuted from the retrieved content alone. These figures are unverified from the source; they are not demonstrated to be wrong, but they cannot be confirmed as verbatim from the paper without full-text access.

Correction: Flag as **human-review** — the specific numbers (70.1% / 67.3%) require verification against the full paper PDF. The paper exists and covers StableToolBench, but the exact figures should not be cited without confirming them from the paper body.

**Claim 13 — OpenAI "<100 tools and <20 arguments per tool in-distribution"**

The draft's Challenge section notes that the live developers.openai.com source contains "fewer than 20 functions" as a soft suggestion, and that the "<100 tools" figure comes from the o3/o4-mini reasoning model guide specifically. Live verification of developers.openai.com confirmed only the "fewer than 20 functions" soft suggestion — no 100-tool in-distribution bound was found in that document. The Findings section (SQ3 and SQ7) correctly attributes different numbers to different contexts, but the cross-platform comparison table (SQ3) lists only "fewer than ~100 tools and ~20 arguments per tool is 'in-distribution'" without flagging the model-family specificity. This conflation persists across the Findings section without consistent qualification.

Correction: The "<100 tools and <20 arguments per tool" bound is documented for o3/o4-mini specifically, not as a general OpenAI guideline. The "fewer than 20 functions" soft suggestion is the general OpenAI guidance. These are two separate claims that should not be merged or presented interchangeably.

**Claim 14 — 875 test entries in irrelevance detection**

The draft states "875 test entries in irrelevance detection category" as coming from S8 (BFCL V4 Leaderboard). Live verification of the BFCL V3 blog (S7) shows the scoring table lists "❌ Irrelevance (240)" and "❌ Live Irrelevance (882)" — totaling 1,122 entries across both categories. The BFCL V4 leaderboard page (S8) did not return a parseable count. The figure 875 does not appear in any retrieved source. The raw extract for S8 states "875 test entries in irrelevance detection category" but this does not match the V3 blog breakdown.

Correction: The specific figure of 875 test entries is unverified and likely incorrect. The BFCL V3 blog shows 240 (Irrelevance) + 882 (Live Irrelevance) = 1,122 total. The 875 figure may be from a different BFCL version or a selective count. Flag as **human-review** pending direct inspection of the BFCL V4 dataset documentation.

**Claim 15 — "IrrelAcc" metric name**

The draft uses "IrrelAcc (Irrelevance Accuracy)" as the formal metric name. Live fetches of S8 (leaderboard page) and the BFCL blog posts did not return this specific metric name. The BFCL blog uses the term "Irrelevance" and describes the concept of function relevance detection, but the abbreviation "IrrelAcc" was not confirmed in any retrieved source text. This may be an informal abbreviation or a metric name used in BFCL documentation not captured in the fetched pages.

Correction: Flag as **human-review** — confirm whether "IrrelAcc" is the official BFCL metric name or an informal label introduced in the draft.

**Claim 17 — NAACL 2025 / ACL Anthology 2025.naacl-long.44**

The draft identifies this paper as "Enhancing LLM-based Agents with Concise Tool Instruction" at NAACL 2025, ACL Anthology ID 2025.naacl-long.44. Live fetch of https://aclanthology.org/2025.naacl-long.44 returned the paper titled **"EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction"**. The paper exists and is at the correct ACL Anthology URL. However, the title in the draft omits the "EASYTOOL:" prefix. The paper is about transforming tool documentation into concise instructions, consistent with the draft's description.

Correction: The paper title should be cited as "EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction" — the draft omits "EASYTOOL:" from the title. The ACL Anthology ID and venue are correct.

**Claim 22 — arXiv:2602.20426 uses "teacher-forcing evaluation"**

The Challenge section describes arXiv:2602.20426 as using "teacher-forcing evaluation" to isolate description-induced failures. The abstract retrieved does not mention "teacher-forcing" — it describes a "curriculum learning framework" that "progressively transfers supervision from trace-rich settings to trace-free deployment." The methodology may involve teacher-forcing internally, but this term does not appear in the abstract. The characterization of the methodology may be based on the full paper text, which was not retrieved.

Correction: The "teacher-forcing evaluation" characterization cannot be confirmed from the abstract. The paper uses a curriculum learning framework per the abstract. Flag as **human-review** — verify this methodological claim against the full paper.
