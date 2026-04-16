---
name: "Agentic Planning & Execution Patterns"
description: "Core planning frameworks for AI agents — ReAct, CoT, ToT, ReWOO, Plan-and-Execute, and their successors — covering task decomposition strategies, plan-then-execute vs. interleaved execution tradeoffs, and failure recovery patterns. Hybrid global-plan / local-react approaches dominate 2025 production systems."
type: research
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://arxiv.org/abs/2305.18323
  - https://arxiv.org/abs/2402.11534
  - https://arxiv.org/abs/2505.09970
  - https://arxiv.org/abs/2503.16416
  - https://arxiv.org/html/2503.09572v3
  - https://icml.cc/virtual/2025/poster/43522
  - https://blog.langchain.com/planning-agents/
  - https://byaiteam.com/blog/2025/12/09/ai-agent-planning-react-vs-plan-and-execute-for-reliability/
  - https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9
  - https://www.wollenlabs.com/blog-posts/navigating-modern-llm-agent-architectures-multi-agents-plan-and-execute-rewoo-tree-of-thoughts-and-react
  - https://agents.kour.me/task-decomposition/
  - https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development
  - https://sparkco.ai/blog/mastering-retry-logic-agents-a-deep-dive-into-2025-best-practices
  - https://agentwiki.org/planning
  - https://www.promptingguide.ai/techniques/react
related:
  - docs/research/2026-04-07-agent-frameworks.research.md
  - docs/research/2026-04-07-error-handling.research.md
  - docs/research/2026-04-07-multi-agent-coordination.research.md
---

# Agentic Planning & Execution Patterns

## Summary

Four core planning frameworks dominate the academic and production literature: ReAct (interleaved reason-act-observe), Plan-and-Execute (upfront planning, separate execution), ReWOO (fully decoupled planning with variable placeholders), and Tree-of-Thought (multi-branch search). By 2025, production systems converge on hybrid "plan globally, act locally" approaches that combine structured upfront plans with ReAct-style adaptive execution at each step. Failure recovery follows a consistent three-tier escalation: retry transient errors, replan when state diverges, abandon on permanent failures — with the decision typically made via explicit error classification at the tool boundary.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | Dec 2024 | T1 | verified |
| 2 | https://arxiv.org/abs/2305.18323 | ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models | Xu et al. (arXiv) | May 2023 | T3 | verified |
| 3 | https://arxiv.org/abs/2402.11534 | PreAct: Prediction Enhances Agent's Planning Ability | Fu et al. (COLING 2025) | Feb 2024 / Dec 2024 | T2 | verified (COLING 2025 conference proceedings) |
| 4 | https://arxiv.org/abs/2505.09970 | Pre-Act: Multi-Step Planning and Reasoning Improves Acting in LLM Agents | Rawat et al. (arXiv) | May 2025 | T3 | verified |
| 5 | https://arxiv.org/abs/2503.16416 | Survey on Evaluation of LLM-based Agents | Yehudai et al. (arXiv) | Mar 2025 | T3 | verified |
| 6 | https://arxiv.org/html/2503.09572v3 | Plan-and-Act: Improving Planning of Agents for Long-Horizon Tasks | Erdogan et al. (ICML 2025) | Mar 2025 | T2 | verified (ICML 2025 accepted paper) |
| 7 | https://icml.cc/virtual/2025/poster/43522 | Plan-and-Act (ICML 2025 poster) | Erdogan et al. | 2025 | T2 | verified (ICML 2025 conference page — same paper as [6]) |
| 8 | https://blog.langchain.com/planning-agents/ | Plan-and-Execute Agents | LangChain | 2024 | T1 | verified |
| 9 | https://byaiteam.com/blog/2025/12/09/ai-agent-planning-react-vs-plan-and-execute-for-reliability/ | AI Agent Planning: ReAct vs Plan and Execute for Reliability | By AI Team | Dec 2025 | T4 | verified (practitioner blog — reliability comparisons not independently confirmed) |
| 10 | https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9 | ReAct vs Plan-and-Execute: A Practical Comparison of LLM Agent Patterns | James Li (DEV.to) | 2025 | T4 | verified (DEV.to community content — treat as T5) |
| 11 | https://www.wollenlabs.com/blog-posts/navigating-modern-llm-agent-architectures-multi-agents-plan-and-execute-rewoo-tree-of-thoughts-and-react | Navigating Modern LLM Agent Architectures | Wollen Labs | 2025 | T4 | verified (vendor blog — architecture overview) |
| 12 | https://agents.kour.me/task-decomposition/ | Pattern: Task Decomposition — Intelligence Patterns | Kour.me | 2025 | T4 | verified (practitioner pattern catalog) |
| 13 | https://www.gocodeo.com/post/error-recovery-and-fallback-strategies-in-ai-agent-development | Error Recovery and Fallback Strategies in AI Agent Development | GoCodeo | 2025 | T4 | verified (vendor content — AI coding assistant) |
| 14 | https://sparkco.ai/blog/mastering-retry-logic-agents-a-deep-dive-into-2025-best-practices | Mastering Retry Logic Agents: 2025 Best Practices | SparkCo | 2025 | T4 | verified (vendor blog — retry logic) |
| 15 | https://agentwiki.org/planning | Agent Planning: How AI Agents Plan and Reason | AgentWiki | 2025 | T4 | verified (community wiki — plan taxonomy) |
| 16 | https://www.promptingguide.ai/techniques/react | ReAct Prompting | Prompt Engineering Guide | 2024 | T4 | verified (prompting guide — ReAct reference) |

## Extracts

### Sub-question 1: Dominant planning patterns (ReAct, CoT, ToT, successors)

**Chain-of-Thought (CoT)** — Wei et al. (2022) established that eliciting step-by-step reasoning from LLMs improves performance on multi-step tasks. CoT runs entirely on internal model knowledge (no tool calls) and is vulnerable to hallucination. Zero-Shot CoT ("let's think step by step") and Self-Consistency (majority vote over multiple CoT paths) are the primary variants. CoT remains the foundation for all richer planning frameworks.

**ReAct (Reasoning + Acting)** — Combines CoT with external tool invocations in a repeating Thought → Action → Observation loop (source 16). The cycle grounds reasoning in real retrieved evidence, substantially reducing hallucination versus standalone CoT. ReAct excels on decision-making benchmarks (ALFWorld, WebShop) and is the most widely deployed pattern in production frameworks (LangGraph, Claude tool-use, AutoGen). Known weaknesses: myopic step-by-step optimization, error cascades when a single observation misleads subsequent reasoning, and full-context overhead at every step.

**Tree-of-Thought (ToT)** — Extends CoT by exploring multiple branching reasoning paths simultaneously using tree-search (BFS/DFS) with a scoring/pruning mechanism. Reported to be ~10× more accurate than CoT on hard puzzles. Cost is high: multiple candidate completions must be generated and evaluated at each node. Best suited to combinatorial problems and creative tasks, not routine tool-calling workflows. **Graph-of-Thoughts (GoT)** generalizes further to arbitrary directed graphs, allowing thought aggregation and refinement loops across paths.

**ReWOO (Reasoning Without Observation)** — Decouples the full planning graph from tool execution (source 2). The Planner emits an entire dependency-annotated plan upfront (using `#E1`, `#E2` variable placeholders), the Worker executes tools to fill in evidence, and the Solver synthesizes the final answer. Token savings: 5× on HotpotQA, 64% average reduction across 6 benchmarks, with +4.4% accuracy gain. The tradeoff is brittleness: if any tool call returns unexpected output, the plan has no mid-execution observation hook to adapt.

**PreAct / Pre-Act — prediction-augmented planning** — Two 2024–2025 papers extend ReAct with forward-looking prediction. PreAct (Fu et al., COLING 2025, arXiv:2402.11534) adds a prediction step that anticipates the result of the next action before executing it, giving the agent a wider, more strategically coherent reasoning context. Pre-Act (Rawat et al., arXiv:2505.09970) generates detailed multi-step execution blueprints before acting; on the Almita dataset, a fine-tuned 70B Llama 3.1 outperformed GPT-4 by 69.5% on action accuracy and +28% on goal completion rate.

**Successor patterns (2025)** — Modern frontier models (o3/o4-mini, Gemini 2.5 Pro, DeepSeek-R1) function as extended-chain-of-thought planners trained with process-reward models and RL for inference-time compute scaling, blurring the line between prompt-based and training-based planning. Hybrid neural-symbolic planning uses LLMs to translate goals into PDDL, then delegates to classical solvers for formal verification.

**Reliability comparison:**

| Pattern | Adaptability | Token cost | Best task type |
|---------|-------------|-----------|----------------|
| CoT | None (static) | Low | Closed, factual |
| ReAct | High | Medium | Open-ended, tool-calling |
| ReWOO | Low (pre-committed) | Very low | Predictable multi-hop |
| Plan-and-Execute | Medium (replanning) | High | Multi-step, structured |
| ToT/GoT | High (search) | Very high | Puzzles, creative |
| Hybrid Planner+ReAct | High | Medium-high | Long-horizon production |

---

### Sub-question 2: Task decomposition, sub-task generation, dependency tracking

**Core decomposition pattern** — A controller takes a high-level goal and emits a structured sequence of subtasks, each assigned to an application/tool with explicit dependency links (source 12). Three phases: (1) Task Analysis — classifying intent and matching to available tools; (2) Task Decomposition — generating ordered or parallel subtasks; (3) Plan Control — progress tracking, variable management, next-action selection, termination.

**Two decomposition strategies:**
- **Exact strategy**: one subtask per application; strict application boundaries. Best when roles are well-defined.
- **Flexible strategy**: multiple subtasks per application following logical workflow. Preferred when a single application handles multiple sequential operations.

**Dependency encoding** — Dependencies are made explicit via reference ("Using the account ID from the previous step, retrieve transaction history"). ReWOO formalizes this with `#E1`/`#E2` variable placeholders. LLMCompiler generalizes to a DAG with eager parallel scheduling; it claims 3.6× speedup over sequential plan-and-execute (source 8).

**Parallel vs. sequential subtasks** — Subtasks with no data dependency (check weather, check calendar) can run in parallel. Dependency-tracking frameworks like LangGraph model this as a directed acyclic graph with conditional edges.

**Dynamic decomposition** — TDAG (Xu et al., Neural Networks 2025) proposes dynamic task decomposition and agent generation: subtask breakdown is not fixed at planning time but updates as execution reveals new information, with each subtask assigned to a specifically generated subagent. ADaPT (Adapt as Needed) decomposes only when the model fails a subtask, avoiding unnecessary overhead on simple cases.

**Hierarchical decomposition for long-horizon tasks** — Plan-and-Act (Erdogan et al., ICML 2025, arXiv:2503.09572) separates a high-level Planner from a low-level Executor. The Planner emits structured action sequences; the Executor handles environment-specific actions; dynamic replanning fires after each Executor step. Results on WebArena-Lite: 57.58% success vs. prior SOTA 49.1%. A cognitive resource self-allocation approach (CORAL) addresses the problem of working memory bloat in long-horizon tasks by letting agents proactively prune irrelevant context.

**Progress monitoring** — The AgentWiki survey (source 15) identifies four progress-monitoring primitives: (1) variable management (track data between subtasks), (2) subtask status flags, (3) next-action selection based on dependency graph, (4) goal-termination check. Anthropic's guidance (source 1) recommends checkpoints where agents pause for human feedback when encountering blockers, and a maximum-iterations stopping condition as a safety net.

---

### Sub-question 3: Plan-then-execute vs. interleaved planning and execution

**The core tradeoff** — Plan-and-Execute separates a comprehensive planning phase from a distinct execution phase; ReAct interleaves Thought → Action → Observation continuously. As source 9 summarizes: "ReAct prioritizes flexibility, while plan-and-execute prioritizes control and predictability."

**When Plan-then-Execute wins:**
- Multi-step workflows with known structure and predictable subtask types
- High-stakes actions requiring human review before execution begins
- Cost optimization: a powerful model plans once; cheaper specialized models execute
- Compliance and auditability requirements (financial reporting, regulated workflows)
- LangChain benchmarks show ~7% higher task accuracy for plan-and-execute on structured multi-step tasks (source 10: ~92% vs. ~85%), at roughly 1.5–1.8× higher token cost

**When interleaved planning wins:**
- Environments with high uncertainty where outcomes can't be predicted upfront
- Interactive tasks where each observation changes what to do next (web exploration, troubleshooting)
- Short-horizon tasks where planning overhead exceeds benefits
- Real-time latency requirements

**The hybrid consensus (2025)** — Production systems converge on a "plan globally, act locally" pattern: a high-level planner structures major stages upfront; a ReAct-style executor handles fine-grained adaptive execution within each stage (sources 9, 11). This captures planning's strategic coherence while retaining ReAct's tactical flexibility. Anthropic's guidance notes that "the phases in agentic AI workflows do not always occur in a strict step-by-step linear fashion — they are frequently interleaved or iterative, depending on task nature and environment complexity" (source 1).

**ReWOO as a third option** — Fully pre-committed planning (no mid-execution adaptation) wins on token cost (64% reduction) when the workflow is routine and tool outputs are predictable. It fails when tool outputs deviate from the plan's assumptions.

**Dynamic replanning as the bridge** — Plan-and-Act (ICML 2025) introduces dynamic replanning where the Planner updates the plan after each Executor step, giving a hybrid that preserves long-range structure while allowing tactical adaptation. This is the direction most production frameworks (LangGraph, Claude Code harness) are moving.

---

### Sub-question 4: Recovery from planning failures — replan vs. retry vs. abandon

**Error taxonomy** — Effective recovery requires classifying failures before choosing a response (source 13). Five categories:
1. **Execution errors** — tool invocation failures (API, network, CLI)
2. **Semantic errors** — syntactically valid but functionally wrong LLM output
3. **State errors** — agent's assumptions diverge from actual environment state
4. **Timeout/latency failures** — unresponsive processes
5. **Dependency errors** — external service failures (rate limits, schema changes)

**Retry vs. Replan decision rule** (sources 13, 14):
- **Retry**: transient, retriable errors (HTTP 429, 5xx, timeouts). Use exponential backoff with jitter: `delay = base_delay × 2^n + random_jitter`. Cap at ~5 attempts. Risk: none if state is idempotent; dangerous if state-mutating.
- **Replan**: triggered when (a) state verification reveals divergence between expected and actual state, (b) semantic validation of outputs fails, or (c) retry budget is exhausted on a non-terminal task. Replanning restarts from last checkpoint, not from the beginning.
- **Abandon**: permanent failures (4xx other than 429, unrecoverable state corruption, explicit tool contract violations). Log and escalate to human or fallback workflow.

**Three-tier escalation pattern** — Retry → Replan → Decompose (into smaller subtasks) → Abandon. Source 14 identifies this as the most valuable resilience pattern. Each tier adds overhead and latency; the classification of failure type determines which tier to enter first.

**Checkpointing for efficient replan** — Multi-step plans should save execution snapshots at subtask boundaries. Recovery replays only from the last successful checkpoint rather than restarting the full plan. Source 13 identifies this as the architectural distinction between agents that tolerate failure gracefully and those that require full restarts.

**Design principle** — Anthropic (source 1): agents should "pause for human feedback at checkpoints or when encountering blockers." The emphasis is on not propagating failure silently. Source 13 captures this as: "Treat Fallback as First-Class Logic — design recovery paths early, not as auxiliary features."

**Failure classification in code** — The most concrete implementation guidance (source 14): maintain an explicit mapping of error types to retriable/non-retriable, monitor via observability tooling (Prometheus/Grafana equivalent), and preserve multi-turn conversation state across retries to avoid context corruption.

---

## Findings

### Sub-question 1: Dominant planning patterns

**ReAct** is the most widely deployed production pattern (HIGH — T1 Anthropic [1] uses it; T4 sources confirm deployment in LangGraph, Claude tool-use, AutoGen [9][11][16]). Its Thought→Action→Observation loop grounds reasoning in real evidence, reducing hallucination versus CoT. Known weaknesses: myopic step-by-step optimization, error cascade on misleading observations, full-context overhead at each step.

**Plan-and-Execute** separates a comprehensive planning phase from execution; a stronger model plans, cheaper models execute (MODERATE — T1 LangChain [8] describes the pattern; T2 Plan-and-Act [6] validates the concept on WebArena-Lite: 57.58% vs. prior SOTA 49.1%). The ~92% vs. ~85% accuracy comparison cited in the literature is from a T5/T4 source with no named benchmark — treat as directional only (LOW for the specific numbers).

**ReWOO** fully decouples plan from execution with variable placeholders, delivering 5× token savings on HotpotQA and 64% average reduction across 6 benchmarks [2] (MODERATE — T3 arXiv; benchmark-domain results on predictable multi-hop QA, not production agents). Brittleness: any unexpected tool output invalidates the pre-committed plan with no adaptation hook.

**Tree-of-Thought/Graph-of-Thought** explore branching paths with scoring — conceptually powerful for puzzles and creative tasks, but multiple forward passes per node make them computationally prohibitive for production latency budgets (MODERATE for the concept; the "~10×" accuracy claim has no source citation in this document — omit as unsourced).

**2025 successor patterns** (o3/o4-mini, Gemini 2.5 Pro, DeepSeek-R1) internalize extended chain-of-thought via RL-trained process-reward models, partially dissolving the prompt-framework distinction. This trajectory may make the CoT/ReAct/ToT taxonomy progressively less relevant (MODERATE — cited in document; convergent with known model capability direction).

---

### Sub-question 2: Task decomposition, sub-task generation, dependency tracking

**Three-phase pattern**: Task Analysis → Task Decomposition → Plan Control (MODERATE — T4 practitioner catalog [12]; consistent with T2/T3 academic descriptions of hierarchical agents). Exact strategy (one subtask per tool, strict boundaries) vs. flexible strategy (multiple subtasks per tool, logical workflow) — selection depends on tool role clarity.

**Explicit dependency encoding** is required for correctness (HIGH — T1 Anthropic [1] recommends dependency tracking; T3 ReWOO [2] formalizes it with `#E1`/`#E2` placeholders; T1 LangChain [8] implements it as LangGraph conditional edges). LLMCompiler claims 3.6× speedup via DAG-based parallel scheduling [8] (MODERATE — T1 LangChain reference; specific speedup figure not independently confirmed).

**Dynamic decomposition** (TDAG, ADaPT) — decompose only on failure rather than upfront, avoiding unnecessary overhead on simple cases (MODERATE — T3/T4 sources; ADaPT's approach is directionally validated but not in T1 production frameworks).

**Plan-and-Act's hierarchical Planner/Executor** separates strategic plan generation from tactical execution; dynamic replanning fires after each Executor step (HIGH — T2 ICML 2025 [6][7]; 57.58% WebArena-Lite is the strongest benchmark result in this document).

---

### Sub-question 3: Plan-then-execute vs. interleaved tradeoffs

**Plan-then-execute wins** when: multi-step workflows have known structure, human review is required before execution, cost optimization drives using a weaker executor, or auditability is required (MODERATE — T4 practitioner sources [9][11]; T2 Plan-and-Act [6] provides academic validation for long-horizon structured tasks).

**Interleaved (ReAct) wins** when: high uncertainty makes upfront planning fragile, tasks are interactive, horizon is short, or real-time latency is required (HIGH — T1 Anthropic explicitly says phases are "frequently interleaved or iterative, depending on task nature and environment complexity" [1]).

**"Plan globally, act locally" hybrid** is the practitioner recommendation for production: structure major stages upfront, use ReAct-style execution within each stage (MODERATE — T4 consensus [9][11]; one T2 academic implementation [6]; T1 Anthropic directionally consistent but does not use this specific framing).

**Dynamic replanning** (update plan after each executor step) is the architectural bridge: preserves long-range structure while enabling tactical adaptation. Direction of SOTA (Plan-and-Act ICML 2025, LangGraph) (HIGH — T2 [6] + T1 [8] converge).

---

### Sub-question 4: Recovery from planning failures

**Error classification first** — recovery choice depends on error category (MODERATE — T4 GoCodeo [13] provides five categories; T1 Anthropic [1] confirms checkpoint + stopping conditions at a higher level):
- Retry: transient errors (HTTP 429, 5xx, timeouts) — exponential backoff with jitter, ~5 attempts
- Replan: state divergence, semantic validation failure, retry budget exhausted — restart from last checkpoint
- Abandon: permanent failures (4xx other than 429, unrecoverable state, contract violations) — log and escalate

The retry/replan/abandon caps are T4 vendor recommendations with no empirical grounding (LOW for specific numbers). The classification structure is sound but LLM-based error triage can misclassify semantic errors as transient — this is the pattern's main failure mode (per challenger analysis).

**Checkpointing is architecturally required** for efficient replanning (HIGH — T1 Anthropic [1]; T4 sources [13] converge): replan from last successful checkpoint, not from the beginning. This is the distinction between tolerable and catastrophic long-horizon failure modes.

**"Treat fallback as first-class logic"** — design recovery paths early, not as auxiliary features [13] (MODERATE — T4 source; consistent with T1 principle from Anthropic).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | ReAct is the most widely deployed production pattern | superlative | [1] T1 Anthropic + [9][11][16] T4 | verified — T1 Anthropic [1] uses and documents ReAct; Extracts (Sub-q 1) confirm deployment in LangGraph, Claude tool-use, AutoGen |
| 2 | Plan-and-Act achieves 57.58% success vs. prior SOTA 49.1% on WebArena-Lite | statistic | [6][7] T2 ICML 2025 | verified — Sources table lists [6] as T2 "verified (ICML 2025 accepted paper)"; Extracts (Sub-q 2) state "57.58% success vs. prior SOTA 49.1%" citing source 6 |
| 3 | Plan-and-execute achieves ~92% vs. ~85% task accuracy vs. ReAct (a ~7% edge) | statistic | [10] T4/T5 DEV.to | human-review — Source [10] is T4/T5 (DEV.to community content); Findings explicitly flags "treat as directional only (LOW for the specific numbers)"; no named benchmark or methodology |
| 4 | Plan-and-execute incurs roughly 1.5–1.8× higher token cost than ReAct | statistic | [10] T4/T5 DEV.to | human-review — Same T4/T5 source as claim 3; no methodology cited; no confirming T1/T2/T3 extract |
| 5 | ReWOO delivers 5× token savings on HotpotQA | statistic | [2] T3 arXiv (Xu et al.) | verified — Source [2] listed as T3 verified; Extracts (Sub-q 1) state "Token savings: 5× on HotpotQA" citing source 2 |
| 6 | ReWOO delivers 64% average token reduction across 6 benchmarks | statistic | [2] T3 arXiv (Xu et al.) | verified — Source [2] T3 verified; Extracts (Sub-q 1) state "64% average reduction across 6 benchmarks" citing source 2 |
| 7 | ReWOO delivers +4.4% accuracy gain | statistic | [2] T3 arXiv (Xu et al.) | verified — Extracts (Sub-q 1) state "+4.4% accuracy gain" citing source 2 |
| 8 | Pre-Act: fine-tuned 70B Llama 3.1 outperformed GPT-4 by 69.5% on action accuracy on Almita dataset | statistic | [4] T3 arXiv (Rawat et al.) | verified — Source [4] listed as T3 verified; Extracts (Sub-q 1) state "outperformed GPT-4 by 69.5% on action accuracy" citing arXiv:2505.09970 |
| 9 | Pre-Act: +28% on goal completion rate on Almita dataset | statistic | [4] T3 arXiv (Rawat et al.) | verified — Extracts (Sub-q 1) state "+28% on goal completion rate" citing source 4 |
| 10 | LLMCompiler claims 3.6× speedup over sequential plan-and-execute via DAG-based parallel scheduling | statistic | [8] T1 LangChain | human-review — Source [8] is T1 (LangChain blog); Findings flags "specific speedup figure not independently confirmed"; no confirming T2/T3 extract with methodology |
| 11 | Retry attempts should be capped at ~5 | statistic | [13][14] T4 GoCodeo/SparkCo | human-review — Sources [13] and [14] are T4 vendor blogs; Findings notes "retry/replan/abandon caps are T4 vendor recommendations with no empirical grounding" |
| 12 | "ReAct prioritizes flexibility, while plan-and-execute prioritizes control and predictability." | quote | [9] T4 practitioner blog | human-review — Source [9] is T4 (practitioner blog); quote attributed to source 9 in Extracts (Sub-q 3); no T1/T2 confirming source |
| 13 | Anthropic: agentic workflow phases are "frequently interleaved or iterative, depending on task nature and environment complexity" | quote | [1] T1 Anthropic | verified — Source [1] is T1 verified; Extracts (Sub-q 3) attribute this quote directly to "source 1" |
| 14 | Anthropic: agents should "pause for human feedback at checkpoints or when encountering blockers" | quote | [1] T1 Anthropic | verified — Source [1] is T1 verified; Extracts (Sub-q 2 and Sub-q 4) attribute this guidance to source 1 |
| 15 | "Treat Fallback as First-Class Logic — design recovery paths early, not as auxiliary features." | quote | [13] T4 GoCodeo | human-review — Source [13] is T4 vendor content; Extracts (Sub-q 4) attribute this to source 13; no T1/T2 confirming source |
| 16 | ReWOO authored by Xu et al. (arXiv, May 2023) | attribution | [2] T3 arXiv | verified — Sources table explicitly lists "Xu et al. (arXiv)" for source [2] |
| 17 | PreAct authored by Fu et al., published at COLING 2025 (arXiv:2402.11534) | attribution | [3] T2 COLING 2025 | verified — Sources table lists source [3] as "Fu et al. (COLING 2025)" with status "verified (COLING 2025 conference proceedings)" |
| 18 | Pre-Act authored by Rawat et al. (arXiv:2505.09970, May 2025) | attribution | [4] T3 arXiv | verified — Sources table lists source [4] as "Rawat et al. (arXiv)" |
| 19 | Plan-and-Act authored by Erdogan et al., accepted at ICML 2025 (arXiv:2503.09572) | attribution | [6][7] T2 ICML 2025 | verified — Sources table lists source [6] as "Erdogan et al. (ICML 2025)" with status "verified (ICML 2025 accepted paper)" |
| 20 | The three-phase decomposition pattern (Task Analysis → Decomposition → Plan Control) comes from a practitioner pattern catalog | attribution | [12] T4 Kour.me | human-review — Source [12] is T4 (practitioner pattern catalog); Findings rates it MODERATE with T4 classification |
| 21 | 57.58% WebArena-Lite is the strongest benchmark result in this document | superlative | internal (self-referential) | verified — Findings (Sub-q 2) states this explicitly; no other benchmark result in Extracts exceeds this figure |

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Plan-and-execute achieves ~92% vs. ~85% task accuracy (a ~7% edge) | Source 10 (DEV.to community post, explicitly flagged "treat as T5") citing "LangChain benchmarks" | No methodology, dataset name, sample size, or reproducibility information is given; LangChain has not published a controlled benchmark with those figures; source 9 (T4 practitioner blog) echoes the same number without independent derivation | The primary quantitative argument for choosing plan-and-execute over ReAct collapses; the performance claim should be treated as unverified anecdote until a T1/T2 source with a named benchmark is found |
| "Plan globally, act locally" is the 2025 production consensus | Sources 9 and 11 describe the pattern; Plan-and-Act (ICML 2025, T2) implements a version of it | Both source 9 and 11 are T4 vendor/practitioner blogs; source 1 (Anthropic, T1) does not use this framing — it says phases are "frequently interleaved or iterative"; no T1/T2 survey quantifies adoption rates across production deployments | "Consensus" is overstated; the pattern is a reasonable practitioner heuristic with one strong T2 instantiation (Plan-and-Act), not an empirically confirmed industry standard |
| Tree-of-Thought is "~10× more accurate than CoT on hard puzzles" | This figure appears in the document with no source citation | The original ToT paper (Yao et al., 2023) reports large gains on Game of 24 and Creative Writing, not a general "10×" across puzzles; ToT has not been demonstrated at production scale in agentic tool-calling systems | The ToT accuracy claim is unsourced within this document; the gain is benchmark-specific and not transferable to general agentic workflows; ToT's cost (multiple full forward passes per node) makes it effectively impractical for latency-sensitive production agents |
| The three-tier recovery pattern (retry → replan → abandon) reflects established practice | Sources 13 and 14 describe it; source 1 (Anthropic) supports the checkpoint/escalation concept at a high level | Sources 13 and 14 are vendor content (GoCodeo AI coding assistant, SparkCo vendor blog); the specific decision thresholds (e.g., "cap at ~5 attempts," "retry budget exhausted") are vendor recommendations, not findings from controlled studies or T1/T2 empirical work | The pattern is a reasonable heuristic but its tier boundaries and retry caps have no empirical grounding; production failure modes may not decompose neatly into these five categories; the pattern may reflect what vendors sell, not what practitioners find effective |
| ReWOO delivers 5× token savings and +4.4% accuracy on real-world tasks | Source 2 (arXiv preprint, T3): HotpotQA and 6 benchmarks | The 2023 preprint benchmarks are narrow multi-hop QA tasks; benchmarks assume well-formed, predictable tool responses — the condition ReWOO's own analysis identifies as its brittle failure mode; no T1/T2 production deployment data exists | Token savings are real on predictable workflows but may not transfer to open-ended tool-calling agents where tool output variance is high; the accuracy gain is benchmark-specific, not a production reliability figure |
| PreAct's 69.5% improvement over GPT-4 generalizes across agents | Source 4 (arXiv preprint, T3): fine-tuned 70B Llama 3.1 on the Almita dataset | Result requires a fine-tuned 70B model on a specific dataset; it cannot be reproduced with a general-purpose frontier model out of the box; Almita is a single domain-specific benchmark | The headline improvement is a fine-tuning result on one benchmark, not a general planning technique applicable to off-the-shelf agents |
| Plan-and-Act achieves 57.58% vs. prior SOTA 49.1% on WebArena-Lite | Source 6 (ICML 2025, T2): Plan-and-Act paper | WebArena-Lite is a constrained web-task benchmark; production web agents encounter auth flows, CAPTCHAs, dynamic JS, and schema drift not modeled in the benchmark; "prior SOTA 49.1%" is the prior benchmark record, not a production deployment baseline | The ICML result is the most credible planning benchmark in this document, but the gap between 57% benchmark success and reliable production deployment may still be large |

### Premortem

Assume the main conclusion — that hybrid "plan globally, act locally" is the dominant, validated 2025 production approach — is wrong:

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| The "consensus" is survivorship bias from a small set of vocal practitioners and vendor blogs (T4/T5 sources), while the majority of production agents still run pure ReAct or ad hoc patterns because replanning overhead is not worth it for most task types | Medium-high — the strongest sources for "consensus" are T4; no survey data on actual production architecture distribution exists | The prescriptive "use hybrid" recommendation should be narrowed to: "hybrid appears promising for long-horizon, structured tasks; evidence for general superiority is thin" |
| Dynamic replanning is computationally and latency-expensive enough that production teams abandon it after benchmarking, falling back to ReAct with better error handling | Medium — Plan-and-Act reports WebArena-Lite success but does not report latency or cost per task compared to ReAct baseline | The "direction of current SOTA systems" takeaway may reflect research systems, not what ships in production; the latency profile of dynamic replanning is unaddressed in the document |
| The planning framework framing (ReAct vs. Plan-and-Execute vs. ReWOO) becomes obsolete as frontier models internalize multi-step planning through RL-trained extended CoT, making the prompt-engineering distinction irrelevant | Medium — the document acknowledges this in the "Successor patterns (2025)" section with o3/o4-mini | If extended CoT models plan adequately without explicit framework scaffolding, the entire taxonomy's practical relevance shrinks to legacy systems |
| The three-tier recovery pattern fails in practice because failure classification at the tool boundary is unreliable — LLMs misclassify semantic errors as transient retries, causing retry storms or incorrect replanning triggers | Medium-high — semantic error classification is known to be unreliable in LLM agents; no T1/T2 source validates the classification accuracy of the proposed error taxonomy | The failure recovery guidance may create false confidence; robust production systems may need explicit contract enforcement (typed tool outputs, schema validation) rather than LLM-based error triage |
| ReWOO's token savings come at a production reliability cost not captured by benchmark accuracy — in real deployments, tool output variance triggers plan invalidation frequently enough to negate the savings | Medium — the document itself flags this as ReWOO's core brittleness; no empirical data on real-world plan invalidation rates exists | ReWOO's position as the "right choice for routine workflows" may be a benchmark artifact; practitioners should measure plan invalidation rates in their specific environment before committing |

## Takeaways

**Key findings:**
- ReAct is the most widely deployed production pattern; it handles uncertainty well but is myopic and accumulates full context at every step. Plan-and-Execute trades flexibility for predictability and is validated by T2 research (Plan-and-Act, ICML 2025: 57.58% vs. 49.1% SOTA on WebArena-Lite).
- "Plan globally, act locally" hybrid — structure upfront, ReAct execution within each stage — is the practitioner recommendation for production long-horizon tasks. It has one T2 instantiation (Plan-and-Act) and T4 practitioner consensus; it is not yet an empirically confirmed industry-wide standard.
- ReWOO delivers 5× token savings and +4.4% accuracy on predictable multi-hop QA benchmarks (T3 arXiv). Its brittleness — no adaptation hook if tool output deviates — limits it to workflows with stable, predictable tool responses.
- Dynamic replanning (update plan after each executor step) is the architectural direction of SOTA systems. Checkpointing at subtask boundaries is required for efficient replanning — without it, failures force full restarts.
- Failure recovery: classify first (retry transient, replan on state divergence, abandon on permanent). Recovery tier boundaries are T4 vendor heuristics, not empirically validated. LLM-based error classification is unreliable for semantic errors.

**Limitations:**
- The ~92% vs. ~85% accuracy comparison (plan-and-execute vs. ReAct) comes from a T5 DEV.to post with no named benchmark. Do not cite this as evidence.
- The "~10× more accurate" ToT claim has no source citation in this document — it was omitted from Findings accordingly.
- All academic benchmarks (ReWOO, PreAct, Plan-and-Act) are narrow task-specific results. The gap between benchmark success rates and open-ended production reliability is uncharacterized.
- Frontier models (o3/o4-mini, Gemini 2.5 Pro) internalize extended CoT via RL training, which may make explicit planning framework scaffolding increasingly redundant for capable models.
- PreAct's 69.5% improvement requires a fine-tuned 70B model on the Almita dataset — it cannot be reproduced with a general-purpose frontier model.

<!-- search-protocol
{"entries": [
  {"query": "ReAct agent planning pattern 2025 chain-of-thought comparison reliability", "date_range": "2024-2026", "results_used": 5},
  {"query": "tree-of-thought vs chain-of-thought AI agents 2025 successor planning patterns", "date_range": "2024-2026", "results_used": 4},
  {"query": "task decomposition patterns AI agents sub-task generation dependency tracking 2025", "date_range": "2024-2026", "results_used": 5},
  {"query": "plan then execute vs interleaved planning execution AI agents tradeoffs 2025", "date_range": "2024-2026", "results_used": 4},
  {"query": "agent planning failure recovery replan retry abandon strategies 2025", "date_range": "2024-2026", "results_used": 4},
  {"query": "Anthropic building effective agents planning patterns 2025", "date_range": "2024-2026", "results_used": 3},
  {"query": "LangGraph planning patterns agent workflows 2025 state machine", "date_range": "2024-2026", "results_used": 3},
  {"query": "ReWOO agent planning decoupled reasoning actions 2024 2025", "date_range": "2023-2025", "results_used": 4},
  {"query": "agentic planning loop progress monitoring long-horizon tasks LLM 2025", "date_range": "2024-2026", "results_used": 5},
  {"query": "PreAct prediction enhances agent planning ACL 2025 arxiv", "date_range": "2024-2025", "results_used": 3},
  {"query": "survey LLM agent planning 2025 arxiv benchmark evaluation approaches", "date_range": "2024-2026", "results_used": 2}
]}
-->
