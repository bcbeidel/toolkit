---
name: "LLM Capabilities & Limitations"
description: "Landscape survey of frontier LLM capabilities, cross-model differences, reliable failure modes, and the 2025-2026 capability frontier shift for coding agent use cases"
type: research
sources:
  - https://www.apolloresearch.ai/blog/forecasting-frontier-language-model-agent-capabilities/
  - https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
  - https://arxiv.org/abs/2503.13657
  - https://www.trychroma.com/research/context-rot
  - https://smartscope.blog/en/generative-ai/chatgpt/llm-coding-benchmark-comparison-2026/
  - https://byteiota.com/ai-coding-benchmarks-2026-claude-vs-gpt-vs-gemini/
  - https://www.openaitoolshub.org/en/blog/gpt-5-4-review
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
  - https://arxiv.org/abs/2601.16280
  - https://arxiv.org/html/2601.06112v1
  - https://www.aisi.gov.uk/blog/5-key-findings-from-our-first-frontier-ai-trends-report
  - https://galileo.ai/blog/multi-agent-llm-systems-fail
  - https://arxiv.org/pdf/2512.07497
  - https://metr.org/blog/2026-1-29-time-horizon-1-1/
  - https://ai.google.dev/gemini-api/docs/models
  - https://lmcouncil.ai/benchmarks
related: []
---

## Research Brief

- **Mode:** landscape
- **Sub-questions:**
  1. What are the current practical limits of frontier LLMs for agent tasks (instruction following, tool use, long context, code generation)?
  2. How do capabilities differ across Claude, GPT, Gemini for coding agent use cases?
  3. What tasks do LLMs reliably fail at, and what workarounds exist (decomposition, verification, human escalation)?
  4. How has the capability frontier shifted in 2025-2026, and what previously-impossible tasks are now viable?
- **Search strategy:** LLM benchmark comparisons 2025-2026, Claude capabilities documentation, GPT-4o/o3 capabilities, frontier model limitations, LLM failure modes for agents
- **Freshness requirement:** prioritize 2025-2026 sources
- **Canonical tooling requirement:** identify high-quality open-source tools, libraries, or reference implementations

## Search Protocol

| # | Query | Engine | Results Used | Notes |
|---|-------|--------|-------------|-------|
| 1 | "frontier LLM capabilities limits agent tasks 2025 2026" | WebSearch | 1, 2, 8 | Apollo Research forecasting, METR time horizons, AISI report |
| 2 | "LLM benchmark comparisons Claude GPT Gemini coding agents 2025 2026" | WebSearch | 5, 6 | SmartScope and ByteIota benchmark comparisons |
| 3 | "LLM failure modes agents tasks workarounds decomposition verification 2025" | WebSearch | 3, 12, 13 | MAST taxonomy, Galileo summary, multi-agent failure research |
| 4 | "frontier model capabilities 2025 2026 previously impossible tasks now viable" | WebSearch | 11 | AISI frontier AI trends report |
| 5 | "Claude capabilities documentation instruction following tool use 2026" | WebSearch | 8 | Anthropic tool use docs |
| 6 | "GPT-4o o3 GPT-5 capabilities limitations coding tool use 2025 2026" | WebSearch | 7 | GPT-5.4 review with benchmarks |
| 7 | "LLM long context limitations accuracy degradation 2025 research" | WebSearch | 4 | Chroma context rot study |
| 8 | "METR task completion time horizons frontier AI agents 2025 2026" | WebSearch | 2, 14 | METR time horizons blog and update |
| 9 | "SWE-bench verified results 2026 Claude GPT Gemini leaderboard" | WebSearch | 5, 6 | Cross-validated benchmark data |
| 10 | "Apollo Research forecasting frontier language model agent capabilities 2025" | WebSearch | 1 | Detailed forecasting methodology |
| 11 | "Gemini 2.5 3.0 capabilities coding agents context window 2025 2026" | WebSearch | 15 | Gemini model evolution and benchmarks |
| 12 | "LLM agent tool use reliability structured output failures 2025 2026" | WebSearch | 9, 10 | Tool invocation reliability, ReliabilityBench |
| 13 | "open source tools LLM evaluation agents evals framework 2025 2026" | WebSearch | 16 | Evaluation frameworks landscape |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.apolloresearch.ai/blog/forecasting-frontier-language-model-agent-capabilities/ | Forecasting Frontier Language Model Agent Capabilities | Apollo Research | 2025-02 | T2 | verified |
| 2 | https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/ | Measuring AI Ability to Complete Long Tasks | METR | 2025-03 | T1 | verified |
| 3 | https://arxiv.org/abs/2503.13657 | Why Do Multi-Agent LLM Systems Fail? | Mehta et al. | 2025-03 | T1 | verified |
| 4 | https://www.trychroma.com/research/context-rot | Context Rot: How Increasing Input Tokens Impacts LLM Performance | Chroma Research | 2025 | T2 | verified |
| 5 | https://smartscope.blog/en/generative-ai/chatgpt/llm-coding-benchmark-comparison-2026/ | Best LLM for Coding 2026: Opus 4.6 vs GPT-5.3-Codex vs Gemini 3 | SmartScope | 2026-03 | T3 | verified |
| 6 | https://byteiota.com/ai-coding-benchmarks-2026-claude-vs-gpt-vs-gemini/ | AI Coding Benchmarks 2026: Claude vs GPT vs Gemini | ByteIota | 2026 | T3 | verified |
| 7 | https://www.openaitoolshub.org/en/blog/gpt-5-4-review | GPT-5.4 Review: 1M Context, 83% Superhuman Tasks | OpenAI Tools Hub | 2026-03 | T4 | verified |
| 8 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tool use with Claude | Anthropic | 2026 | T1 | verified |
| 9 | https://arxiv.org/abs/2601.16280 | When Agents Fail to Act: A Diagnostic Framework for Tool Invocation Reliability | arxiv | 2026-01 | T1 | verified |
| 10 | https://arxiv.org/html/2601.06112v1 | ReliabilityBench: Evaluating LLM Agent Reliability Under Production-Like Stress | arxiv | 2026-01 | T1 | verified |
| 11 | https://www.aisi.gov.uk/blog/5-key-findings-from-our-first-frontier-ai-trends-report | 5 Key Findings from Our First Frontier AI Trends Report | UK AI Safety Institute | 2025 | T1 | verified |
| 12 | https://galileo.ai/blog/multi-agent-llm-systems-fail | Why Do Multi-Agent LLM Systems Fail | Galileo AI | 2025 | T3 | verified (308) |
| 13 | https://arxiv.org/pdf/2512.07497 | How Do LLMs Fail In Agentic Scenarios? | Roig | 2025-12 | T2 | verified |
| 14 | https://metr.org/blog/2026-1-29-time-horizon-1-1/ | Time Horizon 1.1 | METR | 2026-01 | T1 | verified |
| 15 | https://ai.google.dev/gemini-api/docs/models | Gemini API Models | Google | 2026 | T1 | verified |
| 16 | https://lmcouncil.ai/benchmarks | AI Model Benchmarks Apr 2026 | LM Council | 2026-04 | T3 | verified |

## Raw Extracts

### Sub-question 1: What are the current practical limits of frontier LLMs for agent tasks (instruction following, tool use, long context, code generation)?

**From [Source 2] (METR — Task Completion Time Horizons):**
The "time horizon" metric measures how long a task (in human expert time) an AI can reliably complete. This metric has been consistently exponentially increasing over the past 6 years, with a doubling time of around 7 months. Recently the trend accelerated to doubling every 4 months (2024-2025). Current frontier model performance:
- Claude Opus 4.6: 50% success on ~719-minute tasks
- GPT-5.1 Codex Max: ~162-minute horizon
- Gemini 3 Pro: ~224-minute horizon
- Models have almost 100% success rate on tasks taking humans less than 4 minutes, but succeed less than 10% of the time on tasks taking more than around 4 hours.

Extrapolating present trends: within 2-4 years, frontier AI agents could autonomously complete week-long projects with reasonable reliability.

**From [Source 1] (Apollo Research — Forecasting Agent Capabilities):**
By the beginning of 2026, non-specialized LM agents with low capability elicitation reach 54% on SWE-Bench Verified, while state-of-the-art LM agents reach 87%. With high elicitation, SWE-Bench is expected to reach the 90% threshold around March 2026 (95% CI: October 2025 to September 2027). For Cybench, high-elicitation scaffolds predicted to reach 90% by December 2026. RE-Bench expert-level performance (1.0) predicted around December 2026 but with substantially higher uncertainty (95% CI spans 8+ years). The approach does not account for inference-compute scaling, so estimates may be conservative.

**From [Source 4] (Chroma — Context Rot):**
Context rot is the degradation of LLM performance as input length increases, even on simple tasks. Testing 18 LLMs (Claude, GPT, Gemini, Qwen families):
- Models can maintain near-perfect accuracy up to a certain context length, then performance drops off a cliff unpredictably.
- Even when a model can perfectly retrieve all evidence (100% exact match), performance still degrades substantially as input length increases.
- The "lost in the middle" problem: accuracy can drop by over 30% when relevant information is placed in the middle of the input versus beginning or end.
- Counterintuitively, models perform better on shuffled haystacks than logically structured ones.
- Claude models showed lowest hallucination rates under context pressure; GPT models showed highest.

**From [Source 9] (Tool Invocation Reliability Framework):**
A 12-category error taxonomy captures failure modes across tool initialization, parameter handling, execution, and result interpretation. Mid-sized models (Qwen2.5:14b) demonstrated 96.6% success rate on tool use tasks. Qwen2.5:32b matched GPT-4.1 performance. Smaller models showed tool initialization as their primary bottleneck. Testing across 1,980 deterministic instances on both open-source and proprietary models.

**From [Source 8] (Anthropic — Tool Use Documentation):**
Claude's tool use supports both client tools (executed in user application) and server tools (executed on Anthropic infrastructure). Strict tool use mode (`strict: true`) guarantees schema conformance. Opus models are more likely to ask clarifying questions when parameters are missing rather than guessing; Sonnet models may infer values. Adding even basic tools produces outsized capability gains on benchmarks like SWE-bench and LAB-Bench FigQA, often surpassing human expert baselines.

**From [Source 10] (ReliabilityBench):**
Under production-like stress conditions:
- Agents achieving 96.9% success at baseline declined to 88.1% under medium perturbations (8.8% drop).
- Rate limiting was the most damaging fault type (2.5% degradation).
- ReAct agents recovered from 80.9% of faults; Reflexion agents recovered from only 67.3%.
- Simpler ReAct agents outperformed more complex Reflexion architectures by 2.5% under stress, suggesting complexity introduces failure modes.
- Pass@1 results systematically overestimate production reliability by 20-40%.

### Sub-question 2: How do capabilities differ across Claude, GPT, Gemini for coding agent use cases?

**From [Source 5] (SmartScope — March 2026 Benchmark Comparison):**
SWE-bench Verified (real GitHub issue resolution):
- Claude Opus 4.6: 80.8%
- Claude Sonnet 4.6: 79.6%
- Gemini 3.1 Pro: 80.6%
- GPT-5.2: 80.0%

Terminal-Bench 2.0 (CLI task agents):
- Codex CLI + GPT-5.3-Codex: 77.3%
- Droid + Claude Opus 4.6: 69.9%
- Claude Opus 4.6 (standalone): 65.4%
- Gemini 3 Pro: 54.2%

Terminal-Bench Hard subset:
- Gemini 3.1 Pro Preview: 53.8%
- GPT-5.3-Codex: 53.0%
- Claude Sonnet 4.6 (Adaptive): 53.0%

WebDev Arena (UI quality, Elo-based):
- Claude Opus 4.5 (thinking): ~1510
- Gemini 3 Pro: 1487
- GPT-5.2 High: 1477

Cost per 1M tokens (March 2026): GPT-5.2 ($1.75/$14), Claude Opus 4.6 ($5/$25), Claude Sonnet 4.6 ($1/$5), Gemini 3 Pro ($2/$12).

Key insight: "Results vary not just by model but also by agentic implementation" -- performance heavily depends on which CLI/IDE framework is used alongside the model.

**From [Source 6] (ByteIota — Coding Benchmarks 2026):**
SWE-bench Pro (harder variant): GPT-5.4 (57.7%), Gemini 3.1 Pro (54.2%), Claude Opus 4.6 (~45%).
ARC-AGI-2 (abstract reasoning): Gemini 3.1 Pro (77.1%), Claude Opus 4.6 (68.8%), GPT-5.2 (52.9%).

Model-specific strengths:
- Claude Opus 4.6 excels at "long-form, large codebases" — 1M context window + 128K output capacity enables whole-repository understanding across multiple files.
- GPT-5.3-Codex leads "terminal execution and agentic tasks" — dominates automation and DevOps scripting.
- Gemini 3.1 Pro dominates "abstract reasoning and problem-solving" with superior cost-performance value.
- No single best model: Grok 4/Claude Opus 4.6 lead coding benchmarks, Gemini 3.1 Pro leads reasoning, Claude writes the most natural prose, GPT-5.4 is the best all-rounder with the largest ecosystem.
- 37% of enterprises deploy 5+ models through intelligent routing, cutting costs 60-85% while maintaining performance.

**From [Source 7] (GPT-5.4 Review):**
GPT-5.4 key metrics: 1M native context window (practical quality through ~800K tokens, 15-20% retrieval degradation beyond). 78.2% on GPQA Diamond. 83.0% on Humanity's Last Exam with tools (61% without). SWE-Bench 79.1%. 38% hallucination reduction vs GPT-5, but still ~1 in 12 factual claims contain errors. 99.7% JSON schema compliance in structured output mode across 300 test calls. Max output: 64K tokens (versus Opus's 128K).

**From [Source 16] (LM Council Benchmarks Apr 2026):**
No single best model — ranking depends heavily on the specific task. Claude Opus 4.6 and Grok 4 lead coding, Gemini 3.1 Pro leads reasoning, Claude writes the most natural prose, GPT-5.4 is the best all-rounder. Benchmark results fragment by task type, causing rank reversals.

### Sub-question 3: What tasks do LLMs reliably fail at, and what workarounds exist (decomposition, verification, human escalation)?

**From [Source 3] (MAST — Multi-Agent System Failure Taxonomy):**
14 unique failure modes across 3 categories, identified from 1,600+ annotated traces across 7 MAS frameworks:

**Category 1 — Specification and System Design (5 modes):**
- FM-1.1: Disobey task specification (agents fail to meet stated constraints)
- FM-1.2: Disobey role specification (agents overstep assigned responsibilities)
- FM-1.3: Step repetition (unnecessary reiteration of completed steps)
- FM-1.4: Loss of conversation history (context truncation, reversion to prior states)
- FM-1.5: Unaware of termination conditions (failure to recognize when to stop)

**Category 2 — Inter-Agent Misalignment (6 modes):**
- FM-2.1: Conversation reset (unwarranted dialogue restart losing progress)
- FM-2.2: Fail to ask for clarification (agents don't request needed information)
- FM-2.3: Task derailment (deviation from intended objectives)
- FM-2.4: Information withholding (failure to share critical data)
- FM-2.5: Ignored other agent's input (disregarding peer recommendations)
- FM-2.6: Reasoning-action mismatch (discrepancy between stated logic and behavior)

**Category 3 — Task Verification and Termination (3 modes):**
- FM-3.1: Premature termination (ending before objectives are met)
- FM-3.2: No or incomplete verification (omitting proper outcome checks)
- FM-3.3: Incorrect verification (inadequate validation of decisions)

Framework failure rates ranged from 41% to 86.7%. Coordination breakdowns accounted for 36.9% of all failures. Tactical interventions (better prompts, verification sections) yielded only 14% improvement, emphasizing the need for structural redesigns.

**From [Source 12] (Galileo — Multi-Agent Failures):**
Exponential coordination costs: 2 agents = 1 interaction, 4 = 6, 10 = 45.
Seven primary failure modes: agent coordination breakdowns (most common), lost context during handoffs, endless loops, runtime coordination failures, cascading single-agent failures, role confusion, inadequate observability.
Cost impact: tasks costing $0.10 for single agents can escalate to $1.50 for multi-agent systems.

Success conditions for multi-agent systems:
- Tasks must be embarrassingly parallel with zero inter-agent communication during processing
- Read-heavy (90% analysis, 10% writing)
- Orchestrated deterministically, not emergently

Before using multi-agent: verify better prompt engineering couldn't solve the problem, subtasks are genuinely independent, cost multiplication is justified, latency tolerance allows for handoffs, debugging infrastructure exists. "Your sophisticated multi-agent system might be obsolete before it reaches production scale."

**From [Source 13] (Roig — LLM Failures in Agentic Scenarios):**
Failure categories: planning failures (agents struggle to decompose complex tasks), tool misuse (incorrect application or sequencing), context loss (inability to maintain focus across extended interactions), reasoning errors (logical inconsistencies).
Failure frequency varies by task complexity, number of reasoning steps required, and availability of explicit environmental feedback.
Workarounds: enhanced prompting for planning, structured reasoning frameworks (chain-of-thought), improved tool specification and usage guidelines, better feedback loops.

**From [Source 10] (ReliabilityBench):**
Production recommendations:
1. Discount benchmark metrics significantly — Pass@1 overestimates production reliability by 20-40%.
2. Prioritize fault tolerance mechanisms — implement robust retry logic, especially for rate-limited APIs.
3. Test under stress before deployment — single-run metrics on clean data are dangerously optimistic.
4. Favor architectural simplicity — complex reasoning mechanisms degrade more under realistic conditions than simpler alternatives.

**From [Source 4] (Context Rot):**
Reliable failure: long-context tasks. Models degrade non-linearly as context grows. Workarounds:
- Place critical information at the beginning and end of context (avoid middle).
- Remove irrelevant content for measurable accuracy improvements.
- Context engineering: careful construction and placement of information within prompts.

### Sub-question 4: How has the capability frontier shifted in 2025-2026, and what previously-impossible tasks are now viable?

**From [Source 11] (UK AISI — Frontier AI Trends Report):**
- Chemistry and biology: AI models have far surpassed PhD-level experts. Human baselines were 48% (chemistry) and 38% (biology); frontier models now exceed these by up to 60%.
- Cybersecurity: In 2025, the first model completed expert-level cyber tasks typically requiring 10+ years of experience. Performance on apprentice-level tasks jumped from 9% (late 2023) to 50%.
- Self-replication capabilities emerging: models excel at "obtaining compute and money" but struggle with persistent access maintenance.
- Safeguards improving: 40x increase in time required to find biological misuse jailbreaks between two models released six months apart.

**From [Source 2] (METR — Task Time Horizons):**
The most advanced models now handle tasks taking humans up to ~12 hours (Claude Opus 4.6 at 50% reliability on 719-minute tasks). In mid-2020 models could handle 9-second tasks; early 2023 brought 4-minute tasks; late 2024 reached 40-minute tasks. The doubling rate has accelerated from every 7 months to every 4 months. Within 2-4 years, week-long autonomous projects projected as feasible.

**From [Source 7] (GPT-5.4 Review):**
Contract review that took junior lawyers 8 hours now takes 15 minutes with comparable accuracy. Financial forecasting models outperform human analysts on 3-month revenue predictions for 73% of publicly traded companies. OpenAI's GDPval benchmark: frontier models complete professional work 100x faster and 100x cheaper than human experts, with best models producing outputs rated as good as or better than human experts in nearly half of all comparisons.

**From [Source 5] (SmartScope):**
SWE-bench Verified top score jumped from ~65% (early 2025) to 80.9% (March 2026). Claude Sonnet 4.6 at 79.6% nearly matches flagships at 1/5th the cost. Context windows expanded from 128K to 1M tokens across all major providers at standard pricing. Agent deployments in production increased 340% in Q4 2025.

**From [Source 1] (Apollo Research):**
SWE-bench with high elicitation expected to reach 90% around March 2026. Cybench 90% by December 2026. The forecasts may be conservative because they don't account for inference-compute scaling advances.

## Challenge

**Coverage gaps:**
- Sources skew toward coding/engineering benchmarks. Limited coverage of LLM capabilities for non-code tasks (writing, analysis, creative work) relevant to broader agent use.
- No direct primary data from Anthropic, OpenAI, or Google on failure modes — relying on third-party benchmarks and academic research.
- The T3/T4 benchmark aggregator sources (SmartScope, ByteIota, OpenAI Tools Hub) may lag behind or misreport primary benchmark results. Numbers should be cross-verified against leaderboard primaries where possible.

**Potential biases:**
- METR's time-horizon metric is compelling but extrapolation (week-long tasks in 2-4 years) is speculative. Past exponential trends in AI capability have hit plateaus.
- Apollo Research forecasts explicitly exclude inference-compute scaling — this may make predictions conservative or irrelevant if paradigms shift.
- Context rot study (Chroma) tested specific retrieval tasks; generalization to all long-context use cases is uncertain.
- Multi-agent failure studies (MAST, Galileo) may over-represent failures since they specifically study failure modes — survivorship bias in reverse.

**Counter-evidence:**
- The "simpler is better" finding from ReliabilityBench (ReAct > Reflexion under stress) partially contradicts the trend toward increasingly complex agent architectures. This tension is real and unresolved.
- GPT-5.4's "83% superhuman tasks" claim (Source 7, T4) lacks methodological detail and should be treated with skepticism.

## Findings

### 1. Practical Limits of Frontier LLMs for Agent Tasks

Frontier LLMs in 2026 handle tasks that would take human experts up to ~12 hours, but reliability drops sharply beyond that threshold [2][14]. Claude Opus 4.6 achieves 50% success on 719-minute tasks; models have near-100% success on sub-4-minute tasks but <10% on tasks exceeding 4 hours [2] (HIGH — T1 primary research with quantified methodology).

**Tool use** is now robust for well-specified schemas — Claude's strict mode guarantees schema conformance, and mid-sized open-source models achieve 96.6% tool-use success rates [8][9] (HIGH — T1 sources converge). However, production reliability systematically underperforms benchmarks: Pass@1 overestimates real-world reliability by 20-40% [10] (HIGH — T1 empirical study).

**Long context** remains a reliability boundary. All models exhibit "context rot" — performance degrades non-linearly as input grows, with 30%+ accuracy drops when critical information sits mid-context [4] (MODERATE — T2 single study, specific task types). Claude models showed lowest hallucination rates under context pressure [4].

**Code generation** at the frontier reaches 80.8% on SWE-bench Verified (Claude Opus 4.6), with the top-5 models clustered within 1.2 points [5][6] (HIGH — T3 sources cross-validated, consistent with leaderboard data).

### 2. Cross-Model Capability Differences

No single model dominates all coding agent use cases — capability leadership fragments by task type [16] (HIGH — multiple sources converge):

- **Long-form codebase work:** Claude Opus 4.6 leads with 1M context + 128K output, best for multi-file repository understanding [6].
- **Terminal/agentic execution:** GPT-5.3-Codex leads Terminal-Bench 2.0 (77.3%) via Codex CLI integration [5].
- **Abstract reasoning:** Gemini 3.1 Pro leads ARC-AGI-2 (77.1%) with best cost-performance ratio [6].
- **Harder benchmarks (SWE-bench Pro):** GPT-5.4 leads (57.7%), suggesting harder problems re-separate the field [6].

Performance depends heavily on the agentic framework wrapping the model, not just the model itself [5] (HIGH — explicitly noted across multiple benchmark suites). Enterprise adoption reflects this: 37% deploy 5+ models through routing, cutting costs 60-85% [6] (MODERATE — T3 single source).

Cost structures vary 3-5x across providers at comparable capability levels, making model selection a cost-optimization problem as much as a capability one [5][7].

### 3. Reliable Failure Modes and Workarounds

Multi-agent systems fail at rates of 41-86.7% across frameworks, with coordination breakdowns causing 36.9% of failures [3] (HIGH — T1 study, 1,600+ annotated traces). The MAST taxonomy identifies 14 failure modes across specification/design, inter-agent alignment, and verification categories [3].

Key failure patterns with the highest practical impact:
- **Context loss during handoffs** — agents lose state between interactions [3][12]
- **Premature termination** — ending before objectives are met [3][13]
- **Planning decomposition failures** — inability to break complex tasks into viable sub-steps [13]
- **Tool misuse** — incorrect application or sequencing of tools [13]
- **Reasoning-action mismatch** — stated logic diverges from actual behavior [3]

**Critical finding:** Tactical prompt-level fixes yield only ~14% improvement in multi-agent failure rates. Structural redesigns (architectural changes, deterministic orchestration) are required for meaningful reliability gains [3] (HIGH — T1 with quantified evidence).

**Workarounds that work:**
- Favor architectural simplicity — ReAct agents recover from 80.9% of faults vs. 67.3% for more complex Reflexion agents [10]
- Ensure tasks are "embarrassingly parallel" before using multi-agent patterns [12]
- Place critical context at document start/end, never middle [4]
- Discount benchmark metrics 20-40% when planning for production [10]
- Test under stress conditions before deployment [10]

### 4. Capability Frontier Shift (2025-2026)

The capability frontier has accelerated dramatically. Task time horizons doubled every 7 months historically but shifted to every 4 months in 2024-2025 [2][14] (HIGH — T1 longitudinal measurement).

**Previously impossible, now viable:**
- Resolving real GitHub issues at 80%+ success (SWE-bench jumped from ~65% to 80.9% in one year) [5]
- Expert-level cybersecurity tasks requiring 10+ years experience [11] (HIGH — T1 government research)
- PhD-level science knowledge exceeded in chemistry and biology [11]
- Contract review at comparable accuracy in 15 minutes vs. 8 hours for junior lawyers [7] (LOW — T4 source, unverified claim)
- Professional work at 100x speed and cost reduction for many tasks [7] (LOW — same T4 source)

Context windows expanded from 128K to 1M tokens at standard pricing across all major providers [5][7]. Agent deployments in production increased 340% in Q4 2025 [5] (MODERATE — T3 source).

Apollo Research forecasts SWE-bench reaching 90% with high elicitation around March 2026, and Cybench 90% by December 2026 [1] (MODERATE — T2 forecasting methodology, explicitly excludes inference-compute scaling).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claude Opus 4.6 achieves 50% success on 719-minute tasks | statistic | [2] | verified |
| 2 | Task time horizon doubling every 4 months (2024-2025) | statistic | [2][14] | verified |
| 3 | Pass@1 overestimates production reliability by 20-40% | statistic | [10] | verified |
| 4 | Claude Opus 4.6 at 80.8% on SWE-bench Verified | statistic | [5] | verified |
| 5 | Framework failure rates 41-86.7% | statistic | [3] | verified |
| 6 | Coordination breakdowns = 36.9% of all failures | statistic | [3] | verified |
| 7 | Tactical fixes yield only ~14% improvement | statistic | [3] | verified |
| 8 | ReAct recovers 80.9% of faults vs Reflexion 67.3% | statistic | [10] | verified |
| 9 | SWE-bench top score jumped from ~65% to 80.9% in one year | statistic | [5] | verified |
| 10 | 37% of enterprises deploy 5+ models | statistic | [6] | unverified — single T3 source |
| 11 | GPT-5.4 83% superhuman tasks | statistic | [7] | unverified — T4 source, no methodology |
| 12 | Contract review 15 min vs 8 hours at comparable accuracy | statistic | [7] | unverified — T4, anecdotal |
| 13 | Professional work 100x speed/cost reduction | superlative | [7] | unverified — T4, promotional framing |
| 14 | Agent deployments increased 340% in Q4 2025 | statistic | [5] | unverified — single T3 source |
| 15 | Context rot 30%+ accuracy drop mid-context | statistic | [4] | verified |
| 16 | Mid-sized models 96.6% tool use success | statistic | [9] | verified |

## Canonical Tools and Frameworks

| Tool | Purpose | URL |
|------|---------|-----|
| DeepEval | Open-source LLM evaluation framework, 14+ metrics, plugs into any LLM framework | https://github.com/confident-ai/deepeval |
| OpenAI Evals | Open-source evaluation framework for systematic LLM assessment | https://github.com/openai/evals |
| LangChain OpenEvals | Readymade evaluators for LLM apps | https://github.com/langchain-ai/openevals |
| Arize Phoenix | Open-source LLM observability and evaluation platform | https://github.com/Arize-AI/phoenix |
| Langfuse | Open-source LLM engineering platform for observability and evaluation | https://github.com/langfuse/langfuse |
| RAGAS | Evaluation framework for RAG and agentic LLM applications | https://github.com/explodinggradients/ragas |
| Google LMEval | Open-source cross-model evaluation framework (LiteLLM-based) | https://opensource.googleblog.com/2025/05/announcing-lmeval-an-open-ource-framework-cross-model-evaluation.html |
| SWE-bench | Industry standard benchmark for evaluating code generation agents | https://www.swebench.com/ |
| MAST-Data | Annotated dataset of 1600+ multi-agent system failure traces | https://arxiv.org/abs/2503.13657 |
| ReliabilityBench | Production-stress testing framework for LLM agents | https://arxiv.org/html/2601.06112v1 |
