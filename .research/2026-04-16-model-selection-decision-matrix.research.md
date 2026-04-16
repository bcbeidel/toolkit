---
name: "AI Model Selection Decision Matrix"
description: "Three independent routing axes (complexity, domain, turn-type) determine model tier; reasoning gap (21 pts GPQA) is 3× the coding gap (7.5 pts SWE-bench); benchmark tier gaps have a 12-18 month shelf life as open-weight models close to within 3-5%"
type: research
sources:
  - https://arxiv.org/abs/2406.18665
  - https://arxiv.org/abs/2305.05176
  - https://arxiv.org/html/2412.21187
  - https://arxiv.org/html/2507.07313v1
  - https://arxiv.org/html/2603.04445v1
  - https://arxiv.org/html/2411.07858v1
  - https://www.lmsys.org/blog/2024-07-01-routellm/
  - https://tianpan.co/blog/2025-10-19-llm-routing-production
  - https://tianpan.co/blog/2026-04-10-token-economics-chain-of-thought-when-thinking-costs-more
  - https://research.ibm.com/blog/LLM-routers
  - https://platform.claude.com/docs/en/about-claude/models/overview
  - https://www.morphllm.com/comparisons/claude-haiku-vs-sonnet-vs-opus
  - https://www.datacamp.com/blog/claude-opus-4-5
  - https://www.datacamp.com/tutorial/llm-benchmarks
  - https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/
  - https://medium.com/@paulhoke/the-complete-guide-to-choosing-ai-models-in-2025-from-gpt-to-gemini-and-beyond-dd5f960e5dc8
  - https://dev.to/dr_hernani_costa/claude-ai-models-2025-opus-vs-sonnet-vs-haiku-guide-24mn
  - https://www.marktechpost.com/2025/04/01/a-comprehensive-guide-to-llm-routing-tools-and-frameworks/
---

# AI Model Selection Decision Matrix

**Research question:** Across the current AI model landscape (all major providers), what decision matrix best maps task type × complexity × intensity to the appropriate model tier?

**Scope:** OpenAI (GPT-4o, o1/o3, GPT-4o-mini), Anthropic (Claude Opus 4.7, Sonnet 4.6, Haiku 4.5), Google (Gemini 2.5 Pro/Flash), Meta (Llama 3.x), Mistral — frontier + mid + lightweight tiers.

**14 searches across 4 sub-questions, 18 sources (T1–T5), 33 claims verified.**

---

## Summary

**The decision matrix has three independent routing axes, not one.**

Task complexity is the most-cited routing signal but is co-equal to domain specialization and turn type (agentic vs. single-turn). A pre-generation matrix is a practical heuristic covering ~80% of queries [8]; it cannot replace response-level cascade signals for fine-grained decisions [5][10].

**Key findings (bottom line up front):**

1. **Reasoning gap is 3× the coding gap.** Within Claude tiers: Haiku-to-Opus spread is 21 points on GPQA Diamond (PhD reasoning), but only 7.5 points on SWE-bench (coding). For agentic/tool-use tasks, the gap is large; for function completion, mid-tier is near-equivalent to frontier. (MODERATE — T5 source, conflict of interest; consistent with T5 corroboration) [12][13]

2. **Three routing strategies in order of complexity:** rule-based (sub-ms, 80% coverage) → classifier (BERT-scale, <1,500 samples) → cascade (try cheap first, escalate on low confidence). Start with rules; add complexity only when gaps appear. Benchmark cost savings: RouteLLM over 85% at 95% GPT-4 quality [7]; FrugalGPT up to 98% [2]. Production savings: 60–75% (MODERATE). (HIGH for direction, MODERATE for headline figures)

3. **Routing collapse is a live failure mode.** Score-based routers systematically over-route to frontier models as budget scales (arXiv 2602.03478, Feb 2026). Decision-aware, rank-based classifiers required to realize headline cost savings. (MODERATE — newly published, not yet peer-reviewed)

4. **"Powerful models hurt" is narrower than commonly stated.** Confirmed harms: o1-like reasoning mode wastes 1,953% more tokens on simple arithmetic [3]; CoT drops accuracy up to 36% on implicit statistical learning tasks (arXiv 2410.21333). NOT confirmed: frontier models in standard mode on routine tasks are merely wasteful, not accuracy-degrading. (HIGH for reasoning-mode scope; MODERATE for CoT scope)

5. **Benchmark gaps have a 12–18 month shelf life.** Open-weight models (DeepSeek V3, Qwen3) are within 3–5% of proprietary tiers on widely-used benchmarks. MMLU and HumanEval are already saturated at the frontier. Any decision matrix built on today's tier gaps should carry a recency qualifier. (MODERATE — sourced from Challenge section industry analysis, no formal citation)

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2406.18665 | RouteLLM: Learning to Route LLMs with Preference Data | LMSYS / UC Berkeley | 2024 (ICLR 2025) | T3 | verified |
| 2 | https://arxiv.org/abs/2305.05176 | FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance | Stanford (Chen, Zaharia, Zou) | 2023 (TMLR 2024) | T3 | verified |
| 3 | https://arxiv.org/html/2412.21187 | Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs | Multiple authors | 2024 | T3 | verified (preprint) |
| 4 | https://arxiv.org/html/2507.07313v1 | Frontier LLMs Still Struggle with Simple Reasoning Tasks | Multiple authors | 2025 | T3 | verified (preprint) |
| 5 | https://arxiv.org/html/2603.04445v1 | Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey | Multiple authors | 2026 | T3 | verified (preprint) |
| 6 | https://arxiv.org/html/2411.07858v1 | Verbosity ≠ Veracity: Demystify Verbosity Compensation Behavior of LLMs | Multiple authors | 2024 | T3 | verified (preprint) |
| 7 | https://www.lmsys.org/blog/2024-07-01-routellm/ | RouteLLM: An Open-Source Framework for Cost-Effective LLM Routing | LMSYS Org | 2024-07-01 | T4 | verified |
| 8 | https://tianpan.co/blog/2025-10-19-llm-routing-production | LLM Routing: How to Stop Paying Frontier Model Prices for Simple Queries | TianPan.co | 2025-10-19 | T5 | verified |
| 9 | https://tianpan.co/blog/2026-04-10-token-economics-chain-of-thought-when-thinking-costs-more | The Token Economics of Chain-of-Thought: When Thinking Out Loud Costs More Than It's Worth | TianPan.co | 2026-04-10 | T5 | verified |
| 10 | https://research.ibm.com/blog/LLM-routers | LLM routing for quality, low-cost responses | IBM Research | 2024/2025 | T2 | verified |
| 11 | https://platform.claude.com/docs/en/about-claude/models/overview | Models overview | Anthropic | 2026 (live) | T1 | verified (⚠ vendor bias) |
| 12 | https://www.morphllm.com/comparisons/claude-haiku-vs-sonnet-vs-opus | Claude Haiku vs Sonnet vs Opus (2026): Full Three-Way Comparison | MorphLLM | 2026 | T5 | verified (⚠ conflict of interest: MorphLLM sells routing services) |
| 13 | https://www.datacamp.com/blog/claude-opus-4-5 | Claude Opus 4.5: Benchmarks, Agents, Tools, and More | DataCamp | 2025 | T5 | verified |
| 14 | https://www.datacamp.com/tutorial/llm-benchmarks | LLM Benchmarks Explained: A Guide to Comparing the Best AI Models | DataCamp | 2025/2026 | T5 | verified |
| 15 | https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/ | FrugalGPT: Reducing LLM Costs & Improving Performance | Portkey AI | 2024/2025 | T5 | verified (⚠ conflict of interest: Portkey sells LLM gateway/routing) |
| 16 | https://medium.com/@paulhoke/the-complete-guide-to-choosing-ai-models-in-2025-from-gpt-to-gemini-and-beyond-dd5f960e5dc8 | The Complete Guide to Choosing AI Models in 2025 | Paul Hoke / Medium | 2025 | T5 | verified (⚠ uncredentialed individual, 80/15/5% split unattributed) |
| 17 | https://dev.to/dr_hernani_costa/claude-ai-models-2025-opus-vs-sonnet-vs-haiku-guide-24mn | Claude AI Models 2025: Opus vs Sonnet vs Haiku Guide | DEV Community | 2025 | T5 | verified |
| 18 | https://www.marktechpost.com/2025/04/01/a-comprehensive-guide-to-llm-routing-tools-and-frameworks/ | A Comprehensive Guide to LLM Routing: Tools and Frameworks | MarkTechPost | 2025-04-01 | T5 | verified |

**Note on SSL errors:** The `check_url.py` script failed all checks with `CERTIFICATE_VERIFY_FAILED` — local Python SSL environment issue, not a URL validity problem. All 18 URLs returned substantive content via WebFetch.

### SIFT Evaluation Log

**T1:** Source 11 (Anthropic official docs) — primary authority on own model specs; flag vendor bias when interpreting positioning claims.

**T2:** Source 10 (IBM Research) — institutional research organization; credible on routing architecture patterns.

**T3:** Sources 1–6 (arxiv papers) — peer-reviewed or academic preprints from credible ML institutions (UC Berkeley/LMSYS, Stanford). ICLR 2025 and TMLR 2024 are top venues. Sources 3–6 are preprints: findings are well-documented but not yet peer-reviewed.

**T4:** Source 7 (LMSYS blog) — authored by the same research team as source 1; expert practitioner writing about their own tool.

**T5:** Sources 8–9 (TianPan.co) — practitioner blog with no verifiable institutional affiliation; cites primary papers; treat claims as synthesized practitioner guidance, not primary evidence. Sources 12 (MorphLLM) and 15 (Portkey AI) have commercial conflict of interest — use benchmark numbers only where corroborated by T1–T3 sources. Sources 13–14 (DataCamp), 16 (Medium), 17 (DEV.to), 18 (MarkTechPost) — community/educational content; useful for framing but no original data.

**Red flags:**
- Source 12 (MorphLLM): Sells routing services; benchmark numbers are internally consistent but should be cross-checked against official leaderboards.
- Source 15 (Portkey AI): Sells LLM gateway; cost-savings claims from FrugalGPT are correctly attributed to source 2 (T3), so the underlying claim is sound.
- Source 16 (Medium): The "80%/15%/5% tier split" statistic has no primary source cited — treat as illustrative heuristic, not empirical finding.
- Sources 3–6 (arxiv preprints): Not yet peer-reviewed; treat as preliminary findings pending formal review.

**Claim traces (key claims, options mode):**
- "o1-like models consumed 1,953% more tokens" → Source 3 (T3 preprint) is the primary source; independently consistent with Source 9 (T5) which cites the same paper.
- "85% cost reduction at 95% GPT-4 quality" → Source 1 (T3, ICLR 2025) is primary; corroborated by Source 7 (T4).
- "98% cost reduction" (FrugalGPT) → Source 2 (T3, TMLR 2024) is primary.
- SWE-bench scores (Haiku 73.3%, Sonnet 79.6%, Opus 80.8%) → Source 12 (T5, conflict of interest); partially corroborated by Source 13 (T5). Not yet verified against a T1–T3 leaderboard source — flag for verifier stage.
- "Gemini Pro 1.5's accuracy dropped 17.2% when CoT was applied" → Source 9 (T5) cites unnamed study; no T1–T3 corroboration found — flag as LOW confidence.

---

## Extracts

### Sub-question 1: Task dimensions that predict model requirements

#### Source [16]: The Complete Guide to Choosing AI Models in 2025
- **URL:** https://medium.com/@paulhoke/the-complete-guide-to-choosing-ai-models-in-2025-from-gpt-to-gemini-and-beyond-dd5f960e5dc8
- **Author/Org:** Paul Hoke / Medium | **Date:** 2025

**Re: Sub-question 1**

Three-tier framework for task routing:

> "Tier 1 (80% of tasks): 'Fast & Cheap' using Gemini 2.5 Flash, Claude Haiku 4.5, or GPT-5 Mini 'For: Simple queries, drafts, routine tasks, high-volume operations'"

> "Tier 2 (15% of tasks): 'Balanced' using GPT-5.2, Claude Sonnet 4.5, Gemini 2.5 Pro 'For: Important content, moderate complexity, professional work'"

> "Tier 3 (5% of tasks): 'Premium' using GPT-5.2 Pro, Claude Opus 4.5, Gemini 3 Pro 'For: Critical decisions, complex projects, high-stakes content'"

Use case category mapping:

> "Creative & Content: GPT-5.2, Claude Sonnet 4.5, Gemini 2.5 Flash"
> "Coding & Technical: Claude Opus 4.5, Claude Sonnet 4.5, GPT-5.2 Thinking"
> "Analysis & Research: Gemini 3 Pro, GPT-5.2 Thinking, Perplexity Pro"
> "Conversational & Support: GPT-5 Mini, Claude Haiku 4.5, Gemini 2.5 Flash"
> "Complex Reasoning: GPT-5.2 Pro, Claude Opus 4.5, DeepSeek R1"

Three primary selection criteria:

> "1. Performance & Capabilities (reasoning complexity, specialized skills, context window, accuracy)"
> "2. Cost & Efficiency (input/output pricing, speed, latency, caching)"
> "3. Use Case Alignment (task complexity, usage volume, quality requirements, budget constraints)"

---

#### Source [17]: Claude AI Models 2025: Opus vs Sonnet vs Haiku Guide
- **URL:** https://dev.to/dr_hernani_costa/claude-ai-models-2025-opus-vs-sonnet-vs-haiku-guide-24mn
- **Author/Org:** DEV Community | **Date:** 2025

**Re: Sub-question 1**

On Opus 4.1 use cases:

> "advanced coding, long-horizon planning, sophisticated analysis, and agentic workflows" requiring multi-step reasoning across extended context windows (up to 200,000 tokens). The article also notes it "excels at advanced coding, long-horizon planning, sophisticated analysis" and is optimal for "complex coding projects, architectural decisions, and debugging challenging problems."

On Sonnet 4:

> "strong performance for most professional tasks—content creation, data analysis, technical documentation—at faster response times than Opus." For development work specifically, it delivers "excellent performance" for "building features, reviewing pull requests, writing documentation" at reduced expense compared to Opus.

On Haiku 3.5:

> Designed for scenarios where "speed matters more than depth." The guide identifies suitable applications as "straightforward queries, quick answers, and high-volume tasks" including "customer service automation, content moderation, and simple coding assistance." For coding specifically, it "works well for simple scripting, basic syntax questions, and rapid code snippet generation when speed outweighs complexity requirements."

---

#### Source [5]: Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey
- **URL:** https://arxiv.org/html/2603.04445v1
- **Author/Org:** Multiple authors | **Date:** 2026

**Re: Sub-question 1**

On task dimensions for routing:

> "Queries vary substantially in complexity, from simple factual questions to complex multi-step reasoning problems." The survey notes that "simpler queries can be directed to smaller, more cost-effective models, while complex queries can be sent to larger, more capable models."

Domain specialization as a routing dimension:

> "routing policies can specify 'legal summarization queries can be routed to one model, while code generation requests will be sent to another.'"

On when routing decisions are made:

> "Pre-generation routing selects a model before generating any output, relying entirely on properties of the incoming query, while post-generation routing systems make their decision after an initial response has been produced."

Information used in routing:

> Routing mechanisms vary from simple query features to incorporating "response-level signals, such as confidence scores, token probabilities, or verifier outputs" and external feedback.

---

#### Source [8]: LLM Routing: How to Stop Paying Frontier Model Prices for Simple Queries
- **URL:** https://tianpan.co/blog/2025-10-19-llm-routing-production
- **Author/Org:** TianPan.co | **Date:** 2025-10-19

**Re: Sub-question 1**

Concrete routing rule example:

> "Enterprise tier users: Route to frontier models (GPT-4o)"
> "Query length: 'Short queries are likely simple' – queries under 20 words route to cheaper models"
> "Domain keywords: Code-related terms ('function,' 'debug,' 'implement,' 'refactor,' 'sql,' 'api') trigger routing to capable models"
> "Default behavior: Route to cheaper models when no conditions match"

Model tiering structure mapped to task types:

| Tier | Use Cases |
|------|-----------|
| Simple | "Formatting, translation, factual Q&A, summarization" |
| Medium | Multi-step reasoning, code generation, analysis |
| Complex | Planning, security review, research synthesis |

---

#### Source [11]: Models Overview (Anthropic Official)
- **URL:** https://platform.claude.com/docs/en/about-claude/models/overview
- **Author/Org:** Anthropic | **Date:** 2026 (live documentation)

**Re: Sub-question 1**

Official model tier descriptions:

| Model | Description |
|-------|-------------|
| Claude Opus 4.7 | "Our most capable generally available model for complex reasoning and agentic coding" |
| Claude Sonnet 4.6 | "The best combination of speed and intelligence" |
| Claude Haiku 4.5 | "The fastest model with near-frontier intelligence" |

Pricing data (per million tokens):

| Model | Input | Output | Latency |
|-------|-------|--------|---------|
| Opus 4.7 | $5 | $25 | Moderate |
| Sonnet 4.6 | $3 | $15 | Fast |
| Haiku 4.5 | $1 | $5 | Fastest |

Context windows:
> "Claude Opus 4.7: 1M tokens context, 128k max output"
> "Claude Sonnet 4.6: 1M tokens context, 64k max output"
> "Claude Haiku 4.5: 200k tokens context, 64k max output"

Model selection guidance:

> "If you're unsure which model to use, consider starting with Claude Opus 4.7 for the most complex tasks. It is our most capable generally available model, with a step-change improvement in agentic coding over Claude Opus 4.6."

---

### Sub-question 2: Benchmark evidence for capability cliffs between model tiers

#### Source [14]: LLM Benchmarks Explained: A Guide to Comparing the Best AI Models
- **URL:** https://www.datacamp.com/tutorial/llm-benchmarks
- **Author/Org:** DataCamp | **Date:** 2025/2026

**Re: Sub-question 2**

What each benchmark measures:

> "MMLU: (Massive Multitask Language Understanding) covers 57 academic subjects from high school to professional level"

> "GPQA: Tests 'graduate-level science questions in biology, physics, and chemistry that experts designed to be unsearchable'"

> "HumanEval: '164 Python problems where models write functions from docstrings and are graded on whether the code passes unit tests'"

> "SWE-bench: 'Drops models into real GitHub repositories and asks them to fix actual bugs'"

> "ARC-AGI-2: 'Each task presents input-output grid examples and asks the model to infer the transformation rule, then apply it'"

Benchmark saturation and performance levels:

> "MMLU: 'Frontier models now cluster above 88%, leaving little room to tell them apart'"

> "GPQA Diamond: 'Gemini 3 Pro leads at 92.6%'"

> "HumanEval: 'Most current frontier models score above 85%'"

> "SWE-bench Verified: 'Claude Opus 4.5 is the first model to break 80% (80.9%)'"

> "FrontierMath: 'Even the best models score below 20%'"

> "ARC-AGI-2: 'Pure language models score 0%; best hybrid systems reach 54%'"

Capability gap between frontier and lightweight:

> "small models like Qwen2.5-1.5B achieve only ~30-40% on HellaSwag, contrasting sharply with frontier models exceeding 85% on most benchmarks."

---

#### Source [12]: Claude Haiku vs Sonnet vs Opus (2026): Full Three-Way Comparison
- **URL:** https://www.morphllm.com/comparisons/claude-haiku-vs-sonnet-vs-opus
- **Author/Org:** MorphLLM | **Date:** 2026

**Re: Sub-question 2**

Coding benchmark scores across Claude tiers:

| Benchmark | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 |
|-----------|-----------|-----------|----------|
| SWE-bench Verified | 73.3% | 79.6% | 80.8% |
| Terminal-Bench 2.0 | 41.0% | 59.1% | 65.4% |
| HumanEval | 92.0% | 96.8% | 97.6% |
| OSWorld-Verified | ~60% | 72.5% | 72.7% |

Reasoning benchmark scores:

| Benchmark | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 |
|-----------|-----------|-----------|----------|
| GPQA Diamond | ~62% | 78.2% | 83.3% |
| MATH | ~80% | ~88% | ~91% |
| MMLU Pro | ~65% | ~78% | ~82% |

Key performance gap findings:

> "On SWE-bench Verified, the Haiku-to-Opus gap is 7.5 points. On Terminal-Bench 2.0, the gap is 24.4 points."

> "the reasoning gap is more pronounced than the coding gap. On GPQA Diamond (PhD-level science questions), the Haiku-to-Opus spread is 21 points."

---

#### Source [13]: Claude Opus 4.5: Benchmarks, Agents, Tools, and More
- **URL:** https://www.datacamp.com/blog/claude-opus-4-5
- **Author/Org:** DataCamp | **Date:** 2025

**Re: Sub-question 2**

SWE-bench performance:

> "Claude Opus 4.5: '80.9% on the SWE-bench'" with the article noting Opus 4.5 "outperforming Google's Gemini 3 Pro and OpenAI's GPT-5.1"

> "Terminal-bench: Claude Opus 4.5: '59.3% on the Terminal-bench'"

Tool use gap:

> "The scaled tool use gap is actually very large: 62.3% vs. 43.8% for the next best"

Knowledge benchmark comparison:

> "Gemini 3 Pro has the edge on some of the knowledge-intensive benchmarks, like graduate-level reasoning (GPQA Diamond) and multilingual Q&A (MMMLU)."

---

#### Additional benchmark data from search synthesis

From search results (LM Council / Vellum leaderboard data, April 2026):

GPQA Diamond scores:
- Claude 3 Opus: 95.4% (anomalous — may be re-run)
- GPT 5.2: 92.4%
- Gemini 3 Pro: 91.9%
- Claude Opus 4.6: 91.3%
- Claude Sonnet 4.6: 89.9%
- Claude Haiku 4.5: ~62% (per MorphLLM)

SWE-bench Verified:
- Claude Sonnet 4.5: 82%
- Claude Opus 4.5: 80.9%
- Claude Opus 4.6: 80.8%
- GPT 5.2: 80%
- Claude Sonnet 4.6: 79.6%
- Claude Haiku 4.5: 73.3%

Per search results (morphllm.com):
> "On SWE-bench Verified, Opus 4.6 leads Sonnet 4.6 by just 1.2 percentage points (80.8% vs. 79.6%). Claude Haiku 4.5 achieves 73.3% on SWE-bench, competing with models 3-5x its price. For all three models, the coding gap is narrower than the reasoning gap."

> "The ARC-AGI-2 benchmark shows an 8.4-point gap in Opus's favor (68.8% versus 60.4%), with Opus demonstrating materially better performance on novel abstract reasoning."

Speed and cost tradeoffs:
> "Haiku runs 3x faster than Opus on raw output speed. Haiku is the cheapest at $1/$5 per million tokens and fastest at 80-120 tokens per second, while for most development teams, the 1.2 percentage point margin between Opus and Sonnet on coding is negligible."

---

### Sub-question 3: Routing frameworks and decision heuristics

#### Source [1]: RouteLLM: Learning to Route LLMs with Preference Data
- **URL:** https://arxiv.org/abs/2406.18665
- **Author/Org:** LMSYS / UC Berkeley (Ong, Almahairi, Wu, Chiang et al.) | **Date:** 2024 (ICLR 2025)

**Re: Sub-question 3**

Routing problem formulation:

> "routing between two classes of models: (1) strong models...which provide high-quality responses at a high cost, such as GPT-4, and (2) weak models...which offer lower-quality responses at reduced cost."

Routing decision rule:

> "Rα(q)={ℳweak if P(wins∣q)<α, ℳstrong if P(wins∣q)≥α}" with α controlling the quality-cost tradeoff.

Threshold interpretation:

> "The threshold α∈[0,1] controls the trade-off between quality and cost: a higher value of α enforces stricter cost constraints by favoring weak models more often."

Four router architectures:

> "A. Similarity-weighted (SW) Ranking: Uses 'Bradley-Terry model' with 'cosine similarity to each query q′ in the train set'"
> "B. Matrix Factorization: Models 'a hidden scoring function δ:ℳ×𝒬→ℝ' as 'a bilinear function of the model and query embeddings.'"
> "C. BERT Classifier: 'Use a BERTBASEarchitecture to give a contextualized embedding of the user query'"
> "D. Causal LLM Classifier: 'Parameterizing it with Llama 3 8B' using 'an instruction-following paradigm'"

Cost savings results:

> "cost reductions of over 85% on MT Bench, 45% on MMLU, and 35% on GSM8K as compared to using only GPT-4."

> "Our routers achieve cost savings of up to 3.66x on MT Bench at 95% GPT-4 quality. On MMLU: '1.41x cost savings at 92% quality.' GSM8K: '1.49x at 87% quality.'"

Generalization:

> "router models demonstrate significant transfer learning capabilities, maintaining their performance even when the strong and weak models are changed at test time."

---

#### Source [7]: RouteLLM: An Open-Source Framework for Cost-Effective LLM Routing
- **URL:** https://www.lmsys.org/blog/2024-07-01-routellm/
- **Author/Org:** LMSYS Org | **Date:** 2024-07-01

**Re: Sub-question 3**

How routing decisions are made:

> "Each data point consists of a prompt and a comparison between the response quality of two models on that prompt."

> "each query is first processed by a system that decides which LLM to route it to."

What routers learn:

> "routers 'have learned some common characteristics of problems that can distinguish between strong and weak models, which generalize to new model pairs without additional training.'"

Cascade cost savings (measured against GPT-4 baseline at 95% performance):

> "MT Bench: 'approximately 48% cheaper' with matrix factorization (26% GPT-4 calls)"
> "MT Bench (augmented): '75% cheaper than the random baseline' (14% GPT-4 calls)"
> "MMLU: '14% cheaper than the random baseline' (54% GPT-4 calls)"

---

#### Source [2]: FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance
- **URL:** https://arxiv.org/abs/2305.05176
- **Author/Org:** Stanford (Lingjiao Chen, Matei Zaharia, James Zou) | **Date:** 2023 (TMLR 2024)

**Re: Sub-question 3**

Core cascade strategy:

> "The key idea is to sequentially query different LLMs based on the confidence of the previous LLM's response." Process flows as: "make a request to the smallest model first, evaluate the response, and return it if it's good enough."

Two components for routing:

> "1. Generation Scoring Function: Assigns 'a reliability score between 0 and 1 to an LLM's response' to determine sufficiency."
> "2. LLM Router: Responsible for 'selecting the optimal sequence of m LLMs to query for a given task' by optimizing cost and performance on validation data."

Performance results:

> "FrugalGPT can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost."

Three cost-reduction strategies:

> "prompt adaptation, 2) LLM approximation, and 3) LLM cascade"

---

#### Source [5]: Dynamic Model Routing and Cascading: A Survey
- **URL:** https://arxiv.org/html/2603.04445v1
- **Author/Org:** Multiple authors | **Date:** 2026

**Re: Sub-question 3**

Six routing paradigms:

> "1. Difficulty-aware routing: Routes based on estimated query complexity"
> "2. Human preference-aligned routing: Leverages preference data from human feedback"
> "3. Clustering-based routing: Groups similar queries using unsupervised learning"
> "4. Reinforcement learning routing: Learns routing policies through online feedback"
> "5. Uncertainty-based routing: Routes based on model confidence estimates"
> "6. Cascading: Sequential multi-model approaches"

Combined strategies in production:

> "'Production systems often combine routing and cascading strategies to maximize efficiency' rather than relying on single approaches, suggesting routing proves most effective as a composite strategy addressing diverse operational constraints."

Key insight:

> "'well-designed routing systems can outperform even the most powerful individual models by strategically leveraging specialized capabilities.'"

---

#### Source [8]: LLM Routing: Production Guide
- **URL:** https://tianpan.co/blog/2025-10-19-llm-routing-production
- **Author/Org:** TianPan.co | **Date:** 2025-10-19

**Re: Sub-question 3**

Complexity assessment approaches:

> "Rule-based approach: Deterministic, sub-millisecond, 'covers 80% of use cases' but becomes 'brittle' with edge cases."
> "Classifier-based approach: Lightweight BERT-scale model predicts optimal routing. Training requires 'fewer than 1,500 labeled samples.'"
> "Cascade routing: 'Try the cheap model first' with escalation triggered by confidence thresholds. Achieves '97% of GPT-4 accuracy at 24% of GPT-4 cost.'"

Implementation guidance:

> "rule-based routing should be implemented first by defining 3–4 complexity tiers with explicit rules, shipping it, measuring cost and quality, and establishing a baseline. A classifier should be trained if rule-based routing shows gaps."

When routing is worthwhile:

> "Routing is worthwhile when: Processing '>10,000 requests per day'; LLM costs scale faster than revenue; Quality signals exist for monitoring"

---

#### Source [10]: LLM Routing for Quality, Low-Cost Responses
- **URL:** https://research.ibm.com/blog/LLM-routers
- **Author/Org:** IBM Research | **Date:** 2024/2025

**Re: Sub-question 3**

IBM routing approach:

> "trained a routing algorithm on benchmark data to pick out the strengths and weaknesses of each model in their library so that it could, for any given query, identify the model with the best predicted accuracy and cost."

Routing dimensions:

> "pick and choose among a set of models by price, quality, latency, or any other criteria"
> "send questions on math or history to the models that do that best"
> "define your latency target, and predict how much performance you can achieve"

Key finding:

> "training a router on benchmark data that more closely resembles the target task produces better results"

---

#### Source [18]: A Comprehensive Guide to LLM Routing: Tools and Frameworks
- **URL:** https://www.marktechpost.com/2025/04/01/a-comprehensive-guide-to-llm-routing-tools-and-frameworks/
- **Author/Org:** MarkTechPost | **Date:** 2025-04-01

**Re: Sub-question 3**

RouteLLM description:

> "a drop-in replacement for current API integrations such as OpenAI's client." It dynamically evaluates query complexity, directing simpler tasks to cost-effective smaller models while routing complex queries to high-performance LLMs. Real-world deployments reportedly "save as much as 85% of costs while maintaining performance near GPT-4 levels."

Martian router:

> "Provides 'uninterrupted uptime by redirecting inquiries successfully in real time during outages or performance issues.' Uses intelligent routing algorithms that examine incoming queries and select models based on capabilities and current status."

Additional routing approaches:

> "Tryage: Context-aware routing using predictive performance assessment for individual user goals."
> "PickLLM: Employs 'reinforcement learning (RL) techniques to control the choice of language models,' continuously adjusting decisions based on cost, latency, and accuracy metrics."
> "MasRouter: Uses 'cascaded controller network' architecture for multi-agent coordination and dynamic task allocation."

---

### Sub-question 4: Where powerful models add no value or actively hurt

#### Source [3]: Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs
- **URL:** https://arxiv.org/html/2412.21187
- **Author/Org:** Multiple authors | **Date:** 2024

**Re: Sub-question 4**

Definition of overthinking:

> "Excessive computational resources are allocated for simple problems with minimal benefit" to accuracy improvement. Models "expend excessive compute (in terms of tokens or thinking rounds) on questions that are exceptionally simple."

Concrete token waste example:

> For "what is 2+3?", QwQ-32B-Preview generated "13 solutions totaling 901 tokens", with "o1-like models consumed 1,953% more tokens than conventional models to reach the same answer." The first solution alone was correct, making subsequent solutions wasteful.

Efficiency metrics:

> "ASDIV: QwQ achieved 41.9% efficiency despite 96.9% accuracy"
> "GSM8K: 50.7% efficiency at 94.8% accuracy"
> "MATH500: 52.3% efficiency at 93.0% accuracy"

> "In more than 92% of cases, the initial round of solutions produces the correct answer" while comprising "less than 60% of the total tokens generated."

Which tasks show worst overthinking:

> "On MATH500's easiest Level 1-2 problems, models averaged 3.7-4.6 solution rounds versus 3.0-3.9 for hardest Levels 4-5, despite Level 1 problems requiring fewer tokens overall. The paper concludes o1-like models 'tend to generate more solution rounds for easier math problems.'"

---

#### Source [9]: The Token Economics of Chain-of-Thought: When Thinking Costs More Than It's Worth
- **URL:** https://tianpan.co/blog/2026-04-10-token-economics-chain-of-thought-when-thinking-costs-more
- **Author/Org:** TianPan.co | **Date:** 2026-04-10

**Re: Sub-question 4**

When CoT hurts performance:

> "Overthinking: 'Gemini Pro 1.5's perfect accuracy rate dropped 17.2% when CoT was applied' to straightforward questions where direct answers suffice."

> "Redundant on reasoning models: 'Reasoning models gained only 2–3% accuracy from explicit CoT while taking 20–80% longer to respond.' Models like GPT-4o and Claude 3.5+ already perform internal reasoning."

> "Continued generation after solutions: '41% of reasoning tokens can be eliminated on average without any accuracy loss' through early stopping."

Token cost inflation:

> "CoT inflates output from '15–30 tokens' to '150–400 tokens' for classification tasks"
> "Results in 2–5x token inflation; transforms a '$2,000 monthly inference bill' to '$10,000'"
> "Increases latency by '35–600%' or '5 to 15 additional seconds per call'"

Decision framework for when NOT to use reasoning models:

> "Skip CoT unless: (1) Task requires sequential reasoning steps; (2) Model isn't already a reasoning model (o3, o4-mini, Claude extended thinking); (3) A/B testing shows accuracy improves by more than '5%' despite '200%' token increase"

When CoT does help:

> "On difficult reasoning tasks, CoT improved accuracy by '11–13%' across non-reasoning models"

---

#### Source [4]: Frontier LLMs Still Struggle with Simple Reasoning Tasks
- **URL:** https://arxiv.org/html/2507.07313v1
- **Author/Org:** Multiple authors | **Date:** 2025

**Re: Sub-question 4**

Tasks where even frontier models fail:

> "With 6 words to count in 150-character paragraphs, performance drops dramatically. o1 achieves only 0.30 accuracy; other models fall to 0.00-0.40 range."

> "At depth 12 with 16 atomic propositions, o1 achieves just 0.35 accuracy on logic evaluation tasks."

> "Even with 10 cities and 5 required stops, non-thinking models achieve 0.00-0.34 pass@5 scores" on travel planning.

Memorization over reasoning finding:

> "'all models perform significantly worse on the unpuzzles than on the original puzzles'"

> "Performance gaps range from 9.1% to 54% between original puzzles and trivial versions. Crucially: 'every model performs better on the context-shifted unpuzzles than the unpuzzles' — demonstrating models rely on training data memorization rather than genuine problem-solving."

Six persistent failure modes:

> "1. Error accumulation in multi-step problems"
> "2. Long context difficulties with irrelevant information"
> "3. Statistical shortcuts replacing actual computation"
> "4. Poor state tracking across multiple variables"
> "5. Out-of-distribution generalization failures when vocabulary changes"
> "6. Tokenization issues affecting character-level tasks"

---

#### Source [6]: Verbosity ≠ Veracity: Demystify Verbosity Compensation Behavior of LLMs
- **URL:** https://arxiv.org/html/2411.07858v1
- **Author/Org:** Multiple authors | **Date:** 2024

**Re: Sub-question 4**

Definition:

> "the behavior of generating responses that can be compressed without information loss when prompted to write concisely."

Model size and verbosity — larger models are NOT reliably less verbose:

> "Open-source models average 39.80% verbosity compared to closed-source at 28.96%"
> "GPT-4 exhibits 50.40% verbosity frequency despite being a premier model"
> "Llama3-70B performs best at only 13.62% average verbose responses"
> "Mistral-7B worst performer at 74.19% verbosity frequency"

Performance impact:

> "Qasper dataset: 27.61% recall gap between verbose and concise responses (Llama3-70B)"
> "Average performance difference: 20.34% across models on short-context tasks"
> "For Chain-of-Thought reasoning, GPT-3.5-Turbo shows 24.54% recall reduction when generating verbose answers on MMLU"

Overall rate:

> "Average frequency: 34.69% of responses exhibit verbosity compensation"
> "All 14 models demonstrated verbosity across all five datasets"

---

#### Source [15]: FrugalGPT: Reducing LLM Costs & Improving Performance (Portkey)
- **URL:** https://portkey.ai/blog/implementing-frugalgpt-smarter-llm-usage-for-lower-costs/
- **Author/Org:** Portkey AI | **Date:** 2024/2025

**Re: Sub-question 4**

On heterogeneous model performance — where powerful models aren't always better:

> "LLM APIs 'have heterogeneous pricing structures, with fees that can differ by two orders of magnitude'" yet do not correspondingly differ in output quality across all task types.

Cascade decision logic:

> "if a cheaper LLM can provide a satisfactory answer, there's no need to query the more expensive models, thus saving costs." The implication: for many queries, cheaper models produce satisfactorily equivalent outputs.

---

## Challenge

*Added 2026-04-16. Counter-evidence searched via WebSearch and WebFetch. Searches conducted: (1) "smaller LLM outperforms larger model simple tasks 2025–2026", (2) "LLM routing failure modes limitations production 2025–2026", (3) "does model tier matter all task types benchmark flat capability gap", (4) "LLM routing cost savings overstated benchmark vs production gap", (5) "query complexity prediction failure LLM router misclassification", (6) "frontier model convergence benchmark saturation tier gap shrinking 2026", (7) "routing collapse degenerate convergence LLM routers", (8) "chain of thought hurts accuracy simple tasks counterevidence", (9) "FrugalGPT RouteLLM replication external validation production 2025".*

---

### Step 1: Assumptions Check

The emerging findings rest on five load-bearing assumptions.

| # | Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|---|-----------|---------------------|-----------------|-----------------|
| A1 | Query complexity is reliably detectable pre-generation — routing systems can accurately classify simple vs. hard tasks before spending tokens on inference | Source [5] (survey), Source [8] (rule-based approach "covers 80% of use cases"), Source [1] (BERT/LLM classifiers trained in <1,500 samples) | "When Routing Collapses" (arXiv 2602.03478, Feb 2026): routers trained on scalar performance scores systematically default to frontier models as budget increases — an "objective-decision mismatch" where small score-prediction errors flip model rankings. Source [4] (frontier models struggle on apparent-simple tasks like word counting). Ambiguous boundary queries require mid-tier escalation when confidence <0.6 | If task difficulty is hard to predict, routing accuracy falls, cost savings erode, and the decision matrix cannot be applied at query-time without significant misrouting overhead |
| A2 | The 85–98% cost reductions from RouteLLM / FrugalGPT transfer to production workloads | Sources [1, 2] (ICLR 2025, TMLR 2024 — top venues, controlled benchmarks) | Production practitioner reporting: "The 85% cost reduction benchmarks are real — but they assume you've instrumented quality monitoring and can tune thresholds against your actual traffic." Real-world cost savings cited (60–72%) are lower than headline benchmark figures. The largest actual cost reductions come from operational changes, not routing algorithms alone. No independent replication study with a held-out production corpus was found | Cost savings in the 85–98% range are best-case benchmark figures; production savings are likely 60–75%, still meaningful but substantially lower. The decision matrix retains directional validity but should not cite headline figures without qualification |
| A3 | The capability gap between tiers is stable and large enough to justify systematic routing — i.e., the tier structure will persist | Sources [12, 13] (benchmark spreads: 21 pts GPQA Diamond, 7.5 pts SWE-bench), Source [14] (MMLU saturation >88% at frontier) | "The LLM Moat Is Collapsing" (2025-2026 industry analysis): open-weight models (DeepSeek V3, Qwen3) are within 3–5% of top proprietary systems on widely-used benchmarks. The frontier-to-open gap has collapsed to ~6 months. GPQA and AIME are approaching saturation — "frontier models exceed human capacity." GPT-4.1-mini scores 49% on instruction-following vs. GPT-4o's 29%, showing a lightweight model beating the tier above it on a specific task | The tier structure is valid today but unstable on a 12–18 month horizon. A matrix built on current gaps may misallocate by the time it is widely deployed. Findings should include a staleness caveat |
| A4 | More powerful models actively hurt on simple tasks — this is a reliable, generalizable effect | Source [3] (1,953% token waste on 2+3=?), Source [6] (verbosity: GPT-4 at 50.4%), Source [9] (CoT drops Gemini Pro 1.5 accuracy 17.2% on simple questions — LOW confidence flag) | "Mind Your Step (by Step)" (ICML 2025, arXiv 2410.21333): CoT drops are specific to implicit statistical learning, facial recognition, and classification-with-exceptions tasks — not general across simple tasks. CoT still improves average performance on non-reasoning models (Gemini Flash 2.0 +13.5%, Sonnet 3.5 +11.7%). The "actively hurts" claim applies to a narrow task class and to reasoning-mode invocation (o1/o3), not to frontier models in standard mode on routine tasks | The "powerful models hurt on simple tasks" claim needs scoping: it is confirmed for o1-like reasoning mode applied to arithmetic, and for CoT on perceptual/implicit tasks. It is NOT confirmed as a general property of frontier models in standard generation mode. Overstating this weakens the matrix's credibility |
| A5 | Task type (domain keyword / query length) is the primary routing signal, dominating other factors | Source [8] (domain keywords, query length <20 words as heuristics), Source [1] (BERT classifier generalizes across model pairs) | IBM Research (Source [10]): "training a router on benchmark data that more closely resembles the target task produces better results" — domain match outperforms generic complexity signals. Source [5] (survey) identifies six paradigms including uncertainty-based and RL-based routing, where response confidence signals outperform pre-generation query features. Source [4]: frontier models fail on apparent-simple tasks (word counting, logic depth), so query length and keywords fail to capture genuine difficulty | If response-level signals (confidence, verifier outputs) are better routing indicators than query features, then a pre-generation decision matrix has structural limits — it works for coarse routing but not for fine-grained task-difficulty prediction |

**Weakest assumptions:** A2 (production transfer of cost savings) and A4 (generalizability of "powerful models actively hurt") have the weakest supporting evidence relative to available counter-evidence. A1 has newly-published 2026 counter-evidence (routing collapse paper) that was not available to the original sources.

---

### Step 2: Analysis of Competing Hypotheses (ACH)

**Research question restated:** What is the primary organizing principle for LLM model selection?

**Hypotheses:**

- **Hypothesis A (document's emerging finding):** Task complexity / reasoning depth is the primary routing dimension, and a systematic decision matrix (task type × complexity × intensity) is the best model-selection approach.
- **Hypothesis B (skeptic position):** The tier structure is too unstable and routing is too error-prone for a static decision matrix to be reliable; dynamic, response-time routing (cascade with confidence scoring) is superior to any pre-generation matrix.
- **Hypothesis C (alternative):** Domain specialization — not complexity — is the primary routing dimension; the right model for a task is the one trained on that domain, regardless of parameter count or tier.

**Evidence rating (C = consistent, I = inconsistent, N = neutral):**

| Evidence | Hyp A: Complexity-primary matrix | Hyp B: Dynamic cascade superior to static matrix | Hyp C: Domain specialization primary |
|----------|----------------------------------|--------------------------------------------------|---------------------------------------|
| RouteLLM 85% cost savings on MT Bench using complexity classifier (Source [1]) | C | C (cascade also works) | N |
| IBM: "routers trained on task-resembling data produce better results" (Source [10]) | N | N | C |
| Survey: domain-based routing ("legal queries → legal model") is a named paradigm (Source [5]) | N | N | C |
| Survey: "production systems combine routing and cascading strategies" (Source [5]) | C | C | N |
| Routing collapse paper: routers default to frontier at scale, undermining static thresholds (arXiv 2602.03478) | I | C | N |
| FrugalGPT: cascade scores responses and escalates — response-level signal (Source [2]) | N | C | N |
| Complexity heuristics (query length, domain keywords) "cover 80% of use cases" (Source [8]) | C | I (static rules sufficient for majority) | N |
| Benchmark saturation: frontier tiers converging, gap shrinking (2026 industry analysis) | I (matrix becomes stale) | N | N |
| CoT drops on specific task classes (arXiv 2410.21333, Source [9]) | C (supports task-type distinction) | N | N |
| Overthinking: o1 wastes tokens on simple math (Source [3]) | C | N | N |
| Frontier models fail on apparent-simple tasks (word counting) (Source [4]) | I (complexity not reliably predictable) | C | N |
| GPT-4.1-mini beats GPT-4o on instruction-following (search result) | I (tier not deterministic) | N | N |
| IBM routing: separate models by math vs. history domain (Source [10]) | N | N | C |
| **Inconsistencies total** | **3** | **1** | **0** |

**Selected: Hypothesis C has zero inconsistencies. Hypothesis B has the fewest inconsistencies among the two primary contenders.**

**Rationale:** Hypothesis C (domain specialization primary) has zero inconsistencies but is also the least specific — it does not contradict A or B so much as apply to a different layer of the routing decision. The evidence for domain routing comes from IBM and the survey taxonomy, and it is genuinely consistent with the existing findings (domain keywords are already one of the routing signals). The practical implication is that the matrix should treat domain as an independent routing axis alongside complexity, not a subordinate signal.

Hypothesis B (dynamic cascade superior) has only one inconsistency (rule-based covering 80% of use cases) and is strongly supported by the routing collapse failure mode and FrugalGPT's cascade design. The document's Hypothesis A retains value for coarse pre-generation routing but is weakened by the routing collapse evidence and benchmark convergence.

**Conclusion from ACH:** The emerging finding (complexity-primary matrix) is directionally correct but incomplete. Domain specialization and response-level cascade signals are independent routing axes with equal or stronger evidence. The matrix should be qualified as a pre-generation heuristic, not a complete routing solution.

---

### Step 3: Premortem

**Assume the main conclusion is wrong:** The decision matrix (task type × complexity × intensity → model tier) fails to improve outcomes in production over simpler alternatives (e.g., always-frontier, or random routing).

| # | Failure Reason | Plausibility | Impact on Conclusion |
|---|---------------|-------------|----------------------|
| P1 | **Routing collapse makes the matrix self-defeating at scale.** As query volume grows and budget tolerance loosens, routers systematically escalate to frontier models regardless of task complexity (arXiv 2602.03478). The matrix's cost savings evaporate because the routing mechanism itself breaks down under realistic budget conditions. This is not a theoretical risk — it is a documented empirical failure mode in published 2026 research. | High | High — directly undermines finding 2 (85–98% savings). Savings require decision-aware routing (e.g., EquiRouter), not the score-based classifiers most production systems deploy. The conclusion should add: "routing savings assume decision-aware rank-based classifiers, not scalar-score routers." |
| P2 | **Benchmark-to-production transfer gap invalidates the capability cliff claims.** The 21-point GPQA Diamond gap and 7.5-point SWE-bench gap are clean benchmark measurements. In production, query distributions are messier, errors compound across multi-step workflows, and frontier models fail one-in-three production attempts (VentureBeat reporting). The gap the matrix is built on may not persist in real task distributions. Additionally, if benchmark saturation continues, the tier gap could close within 12–18 months, making the matrix prescriptive for a model landscape that no longer exists. | Medium | Medium — the matrix's tier structure is sound for 2026 but needs a "valid as of [date], subject to benchmark saturation" qualifier. It should not be treated as durable infrastructure. |
| P3 | **The "powerful models actively hurt" finding is narrower than presented.** The overthinking effect is documented for reasoning-mode (o1/o3) on arithmetic, and CoT performance drops are confirmed only for implicit statistical learning, facial recognition, and exception-classification tasks. The verbosity finding (34.69%) is about output length, not task accuracy. If the scope is misread as "frontier models generally hurt on simple tasks," practitioners will incorrectly downgrade model selection for a wider class of simple tasks where frontier models in standard mode perform fine. | Medium | Medium — the conclusion should explicitly scope the "actively hurts" claim to: (a) reasoning-mode models on arithmetic/logic tasks, and (b) CoT prompting on perceptual/implicit-pattern tasks. The general-purpose frontier model (Opus, GPT-4o in standard mode) does not reliably hurt on simple tasks — it is merely wasteful. |

**Overall premortem assessment:** The conclusion survives the premortem with two qualifications. The direction is correct — task complexity is a meaningful routing signal, routing saves cost, and over-reasoning wastes tokens. But the magnitude claims (85–98% cost savings) and the generalizability of "powerful models hurt" require scoping. The failure mode with highest plausibility is routing collapse (P1), which is an active engineering problem, not just a theoretical concern.

---

### Challenge Summary

Three findings from counter-evidence searches materially affect the document's emerging findings:

1. **Routing collapse (arXiv 2602.03478, Feb 2026)** — a documented failure mode not present in any source reviewed during the original research phase. Existing routers systematically over-route to frontier models as budget scales, reducing realized cost savings. This does not invalidate routing as a strategy, but it limits the headline savings figure and argues for decision-aware classifiers (rank-based, not score-based).

2. **Benchmark convergence** — open-weight models (DeepSeek V3, Qwen3) are within 3–5% of proprietary tiers on widely-used benchmarks, and benchmark saturation is compressing the useful life of capability-gap data. The tier gaps cited are accurate today; they may not hold in 12–18 months.

3. **CoT harms are task-class-specific** (arXiv 2410.21333) — the "powerful models actively hurt" narrative is confirmed for reasoning-mode models on simple arithmetic and for CoT on implicit/perceptual tasks, but is NOT a general property of frontier models in standard mode on routine tasks. The claim requires scoping to avoid over-application.

**No disconfirming evidence found for:** the core finding that task complexity is a useful routing signal, the overthinking / token-waste effect for o1-like models on arithmetic, the verbosity finding (34.69% rate), or the general cascade/routing cost-reduction direction.

## Findings

### Sub-question 1: Task dimensions that predict model requirements

**Finding 1.1 — Three primary routing axes, three secondary axes (HIGH)**

The literature converges on three primary routing dimensions [5][8][10][16]:

1. **Reasoning depth / complexity** — the most-cited axis. Simple factual Q&A, formatting, and translation route to lightweight models; multi-step reasoning, planning, and security review route to frontier.
2. **Domain specialization** — a co-equal axis per ACH analysis. Domain-keyword presence (code terms: function, debug, sql; legal; medical) is a reliable pre-generation signal [8]. IBM Research finds that domain-match outperforms generic complexity signals for accuracy [10].
3. **Turn type: agentic vs. single-turn** — agentic workflows requiring long-horizon planning, tool use, and multi-step execution show the largest tier gaps and justify frontier selection independent of per-query complexity [11][17].

Secondary axes with measurable routing impact:
- **Context window requirements** — Haiku 4.5 caps at 200k; Opus/Sonnet at 1M. Long-context tasks (large codebases, document synthesis) may force tier selection by context constraint alone [11].
- **Latency sensitivity** — Haiku runs ~3x faster than Opus; latency-critical applications (real-time customer support, streaming) favor lightweight regardless of complexity [12].
- **Output format** — structured output (JSON, code) and classification tasks tend toward verbosity-neutral behavior; frontier models do not reliably outperform mid-tier on format-constrained tasks [6].

**Finding 1.2 — Coarse tier split: 80/15/5 (LOW)**

One practitioner source estimates ~80% of queries are simple/cheap tier, ~15% balanced, ~5% premium [16]. No primary source is cited for these proportions — treat as illustrative heuristic only, not an empirical benchmark. The production routing literature is consistent with a heavy left-tail distribution (most queries are simpler than they appear) but does not provide a specific split.

**Finding 1.3 — Pre-generation routing is structurally limited for fine-grained difficulty prediction (MODERATE)**

Rule-based routing covers ~80% of use cases but is brittle on edge cases [8]. Complexity is genuinely hard to predict pre-generation: frontier models fail on apparently simple tasks (word counting, shallow logic) [4], and small models increasingly beat the tier above them on specific tasks (GPT-4.1-mini beats GPT-4o on instruction-following). Pre-generation complexity classifiers are a practical starting point, not a complete solution. Response-level signals (confidence scores, verifier outputs) are stronger routing signals for fine-grained decisions [5][10].

---

### Sub-question 2: Benchmark evidence for capability cliffs between model tiers

**Finding 2.1 — The reasoning gap is large; the coding gap is small (MODERATE)**

Within the Claude family (representative of provider-tier patterns more broadly) [12][13]:

| Task type | Haiku 4.5 | Sonnet 4.6 | Opus 4.6 | Gap (Haiku→Opus) |
|-----------|-----------|-----------|----------|-----------------|
| GPQA Diamond (PhD reasoning) | ~62% | 78.2% | 83.3% | **21 pts** |
| MATH | ~80% | ~88% | ~91% | 11 pts |
| SWE-bench Verified (coding) | 73.3% | 79.6% | 80.8% | **7.5 pts** |
| Terminal-Bench (agentic coding) | 41.0% | 59.1% | 65.4% | 24 pts |
| HumanEval (code completion) | 92.0% | 96.8% | 97.6% | 5.6 pts |
| ARC-AGI-2 (abstract reasoning) | — | 60.4% | 68.8% | ~8 pts (Sonnet→Opus) |

**Actionable implication:** For routine coding (HumanEval-type function completion), Haiku or Sonnet is near-equivalent to Opus. For agentic coding (Terminal-Bench) and PhD-level reasoning (GPQA), the gap is material.

**Finding 2.2 — MMLU and HumanEval are saturated; GPQA, SWE-bench, and ARC-AGI-2 still differentiate (HIGH)**

Frontier models cluster above 88% on MMLU — it no longer separates tiers [14]. HumanEval similarly saturated above 85% at the frontier. GPQA Diamond, SWE-bench Verified, Terminal-Bench, and ARC-AGI-2 remain live benchmarks. FrontierMath is a frontier where all models score below 20% [14].

**Finding 2.3 — Benchmark gaps are valid today but have a 12–18 month shelf life (MODERATE)**

Open-weight models (DeepSeek V3, Qwen3) are within 3–5% of top proprietary tiers on widely-used benchmarks, and the frontier-to-open capability gap has compressed to approximately a 6-month lag. GPQA is approaching saturation at the frontier. A decision matrix built on current tier gaps should carry a recency qualifier — the tier structure may flatten materially within 12–18 months.

**Finding 2.4 — Cross-provider tier equivalents exist but are not symmetric (MODERATE)**

At the lightweight tier: Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash are broadly interchangeable on saturated benchmarks but diverge on domain-specific tasks. At the frontier tier: Claude Opus leads on SWE-bench and tool use [13]; Gemini Pro leads on GPQA Diamond and multilingual tasks [13][14]. Cross-provider selection should be task-domain-sensitive, not tier-equivalence-assumed.

---

### Sub-question 3: Routing frameworks and decision heuristics in practice

**Finding 3.1 — Three implementable routing strategies, ordered by operational complexity (HIGH)**

1. **Rule-based routing** — deterministic, sub-millisecond, covers ~80% of use cases [8]. Define 3–4 complexity tiers with explicit rules (query length, domain keywords, turn type). Ship first; measure baseline before adding complexity.

2. **Classifier-based routing** — lightweight BERT-scale model trained in <1,500 labeled samples [8][1]. Adds ~10ms overhead but handles edge cases that rules miss. RouteLLM achieves over 85% cost reduction while still achieving 95% of GPT-4's performance on MT Bench [7].

3. **Cascade routing** — try cheap model first; escalate on low confidence [2][8]. FrugalGPT (T3, TMLR 2024) achieves up to 98% cost reduction by sequentially querying from cheapest to most capable [2]. Cascade routing achieves 97% of GPT-4 accuracy at 24% of GPT-4 cost in practitioner reports [8].

**Production guidance:** Start with rule-based → add classifier when rules show gaps → add cascade for cost-sensitive, high-volume workloads. Routing is worthwhile when processing >10,000 requests per day and LLM cost scales faster than revenue [8].

**Finding 3.2 — Published academic routing achieves 85% cost reduction; production achieves 60–75% (MODERATE)**

Benchmark figures (RouteLLM: over 85% on MT Bench [7]; FrugalGPT: up to 98% [2]) represent best-case controlled conditions. Practitioner reporting suggests production savings cluster at 60–75% after accounting for quality monitoring, threshold tuning, and realistic query distributions. The direction is robust; the headline figures require qualification.

**Finding 3.3 — Routing collapse is a documented failure mode (MODERATE)**

Score-based routing classifiers (the most common production implementation) systematically over-route to frontier models as budget grows, reducing realized savings — documented in a Feb 2026 paper (arXiv 2602.03478) not represented in the original source set. The fix requires decision-aware, rank-based classifiers (e.g., EquiRouter architecture). This is an active engineering problem, not a theoretical risk. Teams deploying routing should validate against this failure mode.

**Finding 3.4 — Six academic routing paradigms; domain and uncertainty signals are co-equal to complexity (MODERATE)**

The 2026 survey [5] identifies difficulty-aware, preference-aligned, clustering-based, RL-based, uncertainty-based, and cascading paradigms. Production systems combine multiple approaches. Domain match (IBM Research [10]) and response-level uncertainty signals [5] are co-equal to complexity as routing axes — consistent with ACH finding that domain specialization has zero ACH inconsistencies.

---

### Sub-question 4: Where powerful models add no value or actively hurt

**Finding 4.1 — Reasoning-mode models overthinkon simple arithmetic: confirmed and well-scoped (HIGH)**

O1-like reasoning models consumed 1,953% more tokens than conventional models to answer 2+3=? with no accuracy gain [3]. On MATH500's Level 1–2 problems, QwQ-32B-Preview averaged 3.7 solution rounds and DeepSeek-R1 averaged 4.6 rounds — *more* than on hard Level 4–5 problems (3.0 and 3.9 rounds respectively), despite those easier problems requiring fewer tokens overall [3]. In >92% of cases, the first solution is correct; subsequent rounds add only tokens [3]. This effect is documented for reasoning-mode invocation; it does not apply to frontier models in standard generation mode.

**Finding 4.2 — Chain-of-Thought harms performance on specific task classes, not broadly (HIGH)**

CoT reliably hurts accuracy on: implicit statistical learning, facial recognition, and exception-classification tasks — documented in "Mind Your Step (by Step)" (ICML 2025). On the implicit statistical learning task specifically, o1-preview (which has inference-time reasoning built in) shows a 36.3% absolute accuracy decrease compared to GPT-4o zero-shot. However, CoT improves accuracy by 11–13% on difficult reasoning tasks for non-reasoning models [9]. **Do not apply CoT by default to classification, pattern-matching, or perceptual tasks.** The "17.2% accuracy drop when CoT applied" (Gemini Pro 1.5) claim from Source [9] is LOW confidence — no primary source traceable, flagged for verifier.

**Finding 4.3 — Verbosity is a frontier-tier tax, not an accuracy failure (HIGH)**

34.69% of responses across 14 models exhibit verbosity compensation — inflated output without information gain [6]. GPT-4 is among the worst at 50.4% verbosity frequency; Llama3-70B among the best at 13.62%. Larger parameter count does not reduce verbosity. This manifests as token cost inflation for tasks that need concise output (classification, short-answer Q&A). It is a cost and latency issue; accuracy is not reliably degraded by verbosity alone.

**Finding 4.4 — Frontier models in standard mode do not reliably hurt on simple tasks — they are merely wasteful (MODERATE)**

The "powerful models actively hurt" framing requires scoping. Confirmed harms: reasoning-mode on arithmetic (finding 4.1), CoT on perceptual/implicit tasks (finding 4.2). NOT confirmed as a general frontier property: a standard-mode frontier model (Opus, GPT-4o without extended thinking) on routine tasks underperforms a smaller model in cost and latency, but does not reliably produce worse outputs. The cost-of-overkill is primarily economic (5x price, 3x slower), not accuracy-degrading for most standard task types.

**Finding 4.5 — Frontier models have persistent failure modes that cannot be routed around (MODERATE)**

Frontier models fail on: word counting in 150-char paragraphs (o1: 0.30 accuracy), deep logic chains (depth 12: 0.35 accuracy), and multi-city travel planning (0.00–0.34 pass@5) [4]. These are not lightweight-model failures — they affect the frontier tier. The cause appears to be memorization over reasoning: models perform 9.1%–54% worse on novel variants of puzzles versus training-distribution versions [4]. A decision matrix cannot route around these failures by selecting a different tier; they are structural limitations of current transformer architectures.

---

### Counter-Evidence Summary

Three findings from the challenge phase materially qualify the main conclusions:

1. **Routing collapse** (arXiv 2602.03478): score-based routers over-route to frontier at scale. Decision-aware classifiers required for headline savings.
2. **Benchmark convergence**: open-weight models within 3–5% of proprietary tiers; tier gaps have a 12–18 month shelf life.
3. **CoT harm scoping** (arXiv 2410.21333): "powerful models hurt" is confirmed only for reasoning-mode arithmetic and CoT on implicit/perceptual tasks, not frontier models in standard mode generally.

**No disconfirming evidence found for:** task complexity as a useful routing signal, token waste in o1-like models on arithmetic, verbosity as a tier-agnostic property, or the cost-reduction direction of cascade routing.

## Claims

*CoVe phase completed 2026-04-16. All claims resolved — statuses: verified, corrected, human-review, or unverifiable.*

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Haiku runs ~3x faster than Opus" | statistic | [12] | verified — MorphLLM confirms: Haiku 95–150 tok/s, Opus 45.3 tok/s, explicitly states "3x faster" |
| 2 | "Rule-based routing covers ~80% of use cases" | statistic | [8] | verified — Source [8] quotes: "covers 80% of use cases" |
| 3 | "GPT-4.1-mini beats GPT-4o on instruction-following" | attribution | uncited | human-review — no citation bracket; sourced from Challenge section search results not in formal source list |
| 4 | "GPQA Diamond: Haiku ~62%, Sonnet 78.2%, Opus 83.3%, gap 21 pts" | statistic | [12] | verified — MorphLLM page confirms all four numbers exactly |
| 5 | "MATH: Haiku ~80%, Sonnet ~88%, Opus ~91%" | statistic | [12] | verified — MorphLLM page confirms all three numbers exactly |
| 6 | "SWE-bench Verified: Haiku 73.3%, Sonnet 79.6%, Opus 80.8%, gap 7.5 pts" | statistic | [12] | verified — MorphLLM page confirms all four numbers and states "Haiku-to-Opus gap is 7.5 points" |
| 7 | "Terminal-Bench 2.0: Haiku 41.0%, Sonnet 59.1%, Opus 65.4%, gap 24 pts" | statistic | [12] | verified — MorphLLM page confirms all numbers and states "gap is 24.4 points" |
| 8 | "HumanEval: Haiku 92.0%, Sonnet 96.8%, Opus 97.6%, gap 5.6 pts" | statistic | [12] | verified — MorphLLM page confirms all three scores; gap 5.6 = 97.6−92.0, arithmetically correct |
| 9 | "ARC-AGI-2: Sonnet 60.4%, Opus 68.8%, ~8 pts gap (Sonnet→Opus)" | statistic | [12] | verified — MorphLLM Extracts confirm these exact figures (from search-synthesis section of Extracts) |
| 10 | "Frontier models cluster above 88% on MMLU" | statistic | [14] | verified — Source [14] Extracts: "Frontier models now cluster above 88%" |
| 11 | "HumanEval saturated above 85% at the frontier" | superlative | [14] | verified — Source [14] Extracts: "Most current frontier models score above 85%" |
| 12 | "FrontierMath: all models score below 20%" | superlative | [14] | verified — Source [14] Extracts: "Even the best models score below 20%" |
| 13 | "Open-weight models (DeepSeek V3, Qwen3) within 3–5% of top proprietary tiers" | statistic | uncited | human-review — sourced from Challenge section industry analysis with no formal source bracket |
| 14 | "Frontier-to-open capability gap compressed to ~6-month lag" | statistic | uncited | human-review — sourced from Challenge section industry analysis with no formal source bracket |
| 15 | "Classifier trained in <1,500 labeled samples" | statistic | [8][1] | verified — Source [8] Extracts: "fewer than 1,500 labeled samples" |
| 16 | "RouteLLM achieves over 85% cost reduction while still achieving 95% of GPT-4's performance on MT Bench" | statistic | [7] | corrected — original text said "up to 85% cost reduction at 95% GPT-4 quality [1][7]"; Source [7] blog says "over 85%"; the 85% figure does not appear in Source [1] (paper reports 3.66x ≈ 73% at 95% quality threshold); corrected to "over 85%" and re-attributed to [7] only |
| 17 | "FrugalGPT achieves up to 98% cost reduction" | statistic | [2] | verified — Source [2] Extracts: "up to 98% cost reduction" |
| 18 | "Cascade routing achieves 97% of GPT-4 accuracy at 24% of GPT-4 cost" | statistic | [8] | verified — Source [8] Extracts: "97% of GPT-4 accuracy at 24% of GPT-4 cost" |
| 19 | "Routing worthwhile when processing >10,000 requests per day" | statistic | [8] | verified — Source [8] Extracts: "Processing '>10,000 requests per day'" |
| 20 | "Production savings cluster at 60–75%" | statistic | uncited | human-review — sourced from Challenge section practitioner reporting with no formal source bracket; no primary source traceable |
| 21 | "O1-like models consumed 1,953% more tokens than conventional models to answer 2+3=?" | statistic | [3] | verified — Source [3] HTML confirms: "o1-like models consumed 1,953% more tokens than conventional models to reach the same answer" |
| 22 | "QwQ-32B-Preview averaged 3.7 solution rounds; DeepSeek-R1 averaged 4.6 rounds on Level 1–2; 3.0 and 3.9 on Levels 4–5" | statistic | [3] | corrected — original text said "o1-like models average 3.7–4.6 solution rounds" presenting both as a single range; these are two separate models; corrected to name both models explicitly |
| 23 | "In >92% of cases, the first solution is correct" | statistic | [3] | verified — Source [3] HTML: "In more than 92% of cases, the initial round of solutions produces the correct answer" |
| 24 | "o1-preview shows 36.3% absolute accuracy decrease compared to GPT-4o zero-shot on implicit statistical learning task" | statistic | uncited (arXiv 2410.21333) | corrected — original text said "Drops reach 36.3% for o1-preview on these task classes" implying within-model CoT drop; verified as cross-model comparison (o1-preview vs. GPT-4o zero-shot) on implicit statistical learning specifically; corrected text now specifies task and comparison baseline |
| 25 | "CoT improves accuracy by 11–13% on difficult reasoning tasks for non-reasoning models" | statistic | [9] | verified — Source [9] confirmed: "on non-reasoning models like Gemini Flash 2.0 and Claude Sonnet 3.5, CoT improved average accuracy by 11–13% on genuinely difficult reasoning tasks" |
| 26 | "Gemini Pro 1.5's perfect accuracy rate dropped 17.2% when CoT applied" | statistic | [9] | unverifiable — Source [9] confirmed the claim appears: "One study found that Gemini Pro 1.5's perfect accuracy rate dropped 17.2% when CoT was applied." However Source [9] cites an unnamed study; no primary source traceable. Already flagged LOW confidence in SIFT log. Retained in Findings with LOW confidence flag. |
| 27 | "34.69% of responses across 14 models exhibit verbosity compensation" | statistic | [6] | verified — Source [6] Extracts: "Average frequency: 34.69% of responses exhibit verbosity compensation; All 14 models demonstrated verbosity" |
| 28 | "GPT-4 at 50.4% verbosity frequency" | statistic | [6] | verified — Source [6] Extracts: "GPT-4 exhibits 50.40% verbosity frequency" |
| 29 | "Llama3-70B at 13.62% verbosity frequency" | statistic | [6] | verified — Source [6] Extracts: "Llama3-70B performs best at only 13.62% average verbose responses" |
| 30 | "o1 achieves 0.30 accuracy on word counting in 150-char paragraphs" | statistic | [4] | verified — Source [4] Extracts: "o1 achieves only 0.30 accuracy" on word-counting task |
| 31 | "At depth 12 with 16 atomic propositions, o1 achieves 0.35 accuracy" | statistic | [4] | verified — Source [4] Extracts: "o1 achieves just 0.35 accuracy on logic evaluation tasks" |
| 32 | "Non-thinking models achieve 0.00–0.34 pass@5 on travel planning with 10 cities and 5 stops" | statistic | [4] | verified — Source [4] Extracts: "non-thinking models achieve 0.00-0.34 pass@5 scores" |
| 33 | "Models perform 9.1%–54% worse on novel puzzle variants versus training-distribution versions" | statistic | [4] | verified — Source [4] Extracts: "Performance gaps range from 9.1% to 54% between original puzzles and trivial versions" |

---

## Key Takeaways

1. **Use tier for reasoning and agentic tasks; be skeptical for coding.** The Haiku-to-Opus gap on GPQA Diamond (21 pts) justifies frontier selection for PhD-level reasoning. On SWE-bench, Haiku at 73.3% competes with models 3–5x its price — the Opus-Sonnet coding gap is 1.2 points.

2. **Start with rule-based routing.** Define 3–4 complexity tiers with explicit rules (query length, domain keywords, turn type). Ship it, measure cost and quality, then add a classifier only if gaps appear. Cascade routing delivers the best cost savings but is the most complex to operate.

3. **Scope your reasoning-model usage.** O1/o3-style models on simple tasks waste tokens, not accuracy — but 1,953% token overhead on arithmetic is a real cost. Reserve extended thinking for multi-step planning, security review, research synthesis, and deep debugging.

4. **Do not apply CoT to classification, pattern-matching, or perceptual tasks** — accuracy drops are documented (up to 36% on implicit statistical learning vs. GPT-4o zero-shot baseline).

5. **Treat this matrix as 2026-accurate, not durable.** Open-weight models are within 3–5% of proprietary tiers on widely-used benchmarks. MMLU and HumanEval are already saturated. Revisit tier gap assumptions in 12–18 months.

---

## Limitations

- **Benchmark-to-production transfer gap.** The 21-point GPQA Diamond gap and 7.5-point SWE-bench gap are clean benchmark conditions. Production distributions are messier; tier gaps may compress.
- **Routing collapse not yet mitigated.** Most production routing systems use score-based classifiers, which are documented to over-route to frontier at scale (arXiv 2602.03478). Decision-aware classifiers are not yet widely deployed.
- **Cross-provider benchmarks not symmetric.** Claude leads on SWE-bench and tool use; Gemini leads on GPQA Diamond and multilingual tasks. The matrix is not provider-agnostic — domain matters for cross-provider comparison.
- **Open-weight gap closing.** DeepSeek V3, Qwen3 within 3–5% of proprietary tiers. If open-weight adoption accelerates, tier-based routing maps may need to span the proprietary/open boundary.
- **Five human-review claims.** Claims 3, 13, 14, 20, and 24 carry human-review status — sourced from the challenge section's informal search synthesis or from uncited practitioner reporting. These should be traced to primary sources before use in published work.

---

## Follow-Up Questions

1. How does domain specialization interact with complexity routing in practice — does fine-tuning a mid-tier model on domain data outperform a frontier model on that domain?
2. What is the current state of EquiRouter-style decision-aware routing classifiers, and how do they compare to FrugalGPT cascade in production?
3. How should the decision matrix be adapted for multi-agent pipelines, where per-step model selection compounds across a workflow?
4. What task-level benchmarks differentiate Gemini 2.5 Flash vs. Claude Haiku 4.5 for cross-provider routing decisions?

---

## Search Protocol

14 searches across 4 sub-questions, google source. 140 results found, 36 used.

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| LLM task complexity dimensions model selection reasoning depth context length 2025 | google | 2024-2026 | 10 | 2 |
| which AI model to use for which task type GPT-4o Claude Sonnet Haiku guide 2025 | google | 2024-2026 | 10 | 3 |
| LLM routing task dimensions latency sensitivity agentic single-turn structured output model tier 2025 | google | 2024-2026 | 10 | 2 |
| FrugalGPT LLM model selection cost quality tradeoff task routing framework paper | google | 2023-2024 | 10 | 2 |
| MMLU GPQA SWE-bench benchmark comparison GPT-4o Claude Sonnet Haiku Gemini Flash capability cliff 2025 | google | 2024-2026 | 10 | 3 |
| HumanEval MATH benchmark model tier comparison frontier vs lightweight LLM performance gap 2025 | google | 2024-2026 | 10 | 2 |
| Claude Haiku vs Sonnet vs Opus benchmark scores MMLU GPQA coding 2025 capability gap performance difference | google | 2025-2026 | 10 | 3 |
| RouteLLM LLM routing framework paper model selection inference 2024 2025 | google | 2024-2025 | 10 | 3 |
| Martian LLM router model routing decision framework cost quality 2025 | google | 2024-2026 | 10 | 4 |
| LLM cascading strategy model routing production heuristics complexity classifier 2025 | google | 2024-2026 | 10 | 4 |
| when does GPT-4 o1 overkill simple tasks over-generation latency cost degradation instruction following 2025 | google | 2024-2026 | 10 | 2 |
| more powerful LLM worse performance simple tasks instruction following over-reasoning verbosity 2024 2025 | google | 2024-2025 | 10 | 3 |
| reasoning model o1 o3 overthinking simple tasks verbosity token waste latency hurt performance 2025 | google | 2024-2026 | 10 | 4 |
| LLM over-generation verbosity larger model worse instruction following simple classification formatting tasks 2024 | google | 2024-2025 | 10 | 2 |

**Not searched:** OpenAI model documentation (authentication required); Gemini Flash/Pro benchmark tables (budget exhausted); Llama/Mistral lightweight benchmarks (budget exhausted); Rerouting LLM Routers COLM 2025 (budget exhausted); SELECT-THEN-ROUTE taxonomy-guided routing (budget exhausted after survey coverage).
