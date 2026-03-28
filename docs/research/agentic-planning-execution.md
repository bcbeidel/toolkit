---
name: "Agentic Planning and Execution Patterns"
description: "How LLM agents decompose goals, sequence tasks, track progress via artifacts, handle failures, and resume across sessions — comparing ReAct, plan-and-execute, and tree-of-thought approaches"
metadata:
  type: research
  sources:
    - https://arxiv.org/abs/2210.03629
    - https://arxiv.org/abs/2305.04091
    - https://arxiv.org/abs/2305.10601
    - https://arxiv.org/abs/2402.02716
    - https://arxiv.org/abs/2305.16291
    - https://arxiv.org/abs/2308.00352
    - https://arxiv.org/abs/2303.11366
    - https://arxiv.org/abs/2312.04511
    - https://arxiv.org/abs/2304.09842
    - https://arxiv.org/abs/2308.08155
    - https://arxiv.org/abs/2310.04406
    - https://arxiv.org/abs/2402.01030
    - https://arxiv.org/abs/2303.17580
  related:
    - docs/research/llm-capabilities-limitations.md
    - docs/research/prompt-engineering.md
    - docs/context/agentic-planning-execution.md
---

Agentic planning and execution is the set of patterns by which LLM-based agents break goals into tasks, order and execute them, track progress through persistent artifacts, recover from failures, and resume interrupted work. This document surveys the landscape across academic research and practical frameworks.

Key insight: The field has converged on three dominant paradigms — reactive (ReAct), deliberative (plan-and-execute), and exploratory (tree-of-thought) — each with distinct trade-offs for goal decomposition, failure recovery, and session persistence.

## Findings

### How do agents decompose goals into tasks?

Goal decomposition is the most-studied aspect of agentic planning. Three primary strategies have emerged:

**Sequential decomposition (Chain of Thought lineage).** The simplest approach generates a linear sequence of subtasks. Plan-and-Solve prompting [2] explicitly instructs the LLM to "first, devise a plan to divide the entire task into smaller subtasks, and then carry out the subtasks according to the plan." This produces flat, ordered task lists. The PS+ variant adds detailed instructions for each step to reduce calculation and missing-step errors. This approach consistently outperforms zero-shot CoT and matches 8-shot CoT on math reasoning (HIGH — T1 source, peer-reviewed ACL 2023).

**Hierarchical decomposition.** HuggingGPT [13] decomposes complex requests into a planning stage that identifies subtasks, a model selection stage that assigns each subtask to a specialist, and an execution stage. The decomposition is inherently hierarchical: top-level goals map to domain-specific subtasks, each handled by different models (HIGH — T1 source, NeurIPS-adjacent). MetaGPT [6] takes this further by encoding Standard Operating Procedures (SOPs) into the decomposition, creating multi-level task breakdowns that mirror organizational workflows.

**Adaptive decomposition.** Voyager [5] uses an automatic curriculum that generates progressively harder goals based on the agent's current capabilities. Rather than decomposing a single goal upfront, it generates a sequence of achievable subgoals that build toward complex objectives. The curriculum adapts based on what the agent has already accomplished (HIGH — T1 source).

**Formal planning representations.** The planning survey by Huang et al. [4] identifies five categories of LLM planning: task decomposition, plan selection, external module-aided planning, reflection-based planning, and memory-augmented planning. Most practical systems use natural language plans rather than formal representations like PDDL, though LLM+P approaches translate natural language to formal planning domains (MODERATE — survey paper, not primary research).

### How are tasks sequenced and dependencies tracked?

**Linear sequencing** is the default. ReAct [1] interleaves reasoning and action in a strict sequence: think, act, observe, think, act, observe. Each step depends on the previous observation. There is no parallel execution or dependency graph — the sequence is emergent from the reasoning loop (HIGH — T1 source, ICLR 2023).

**DAG-based parallelism.** LLMCompiler [8] introduces a compiler-inspired architecture with a Function Calling Planner that creates execution plans with explicit dependencies, a Task Fetching Unit that dispatches independent tasks concurrently, and an Executor that runs tasks in parallel where possible. This achieves up to 3.7x latency speedup over sequential approaches (HIGH — T1 source, ICML 2024).

**Pipeline sequencing.** HuggingGPT [13] and MetaGPT [6] use pipeline architectures where tasks flow through defined stages. MetaGPT's assembly-line paradigm assigns roles to agents and passes artifacts between stages, creating implicit dependencies through the artifact chain (MODERATE — abstracts only, limited detail on internals).

**Conversation-based coordination.** AutoGen [10] uses multi-agent conversations as the coordination mechanism. Agents "converse with each other to accomplish tasks," with flexible conversation patterns serving as the sequencing mechanism. Dependencies are implicit in the conversation flow rather than explicitly modeled (MODERATE — T2 source).

### How do agents track progress through artifacts?

This is where the literature is thinnest relative to practical importance. Most academic work focuses on in-context tracking rather than persistent artifact-based tracking.

**Skill libraries as progress artifacts.** Voyager [5] is the strongest example of artifact-based tracking. It maintains "an ever-growing skill library of executable code for storing and retrieving complex behaviors." Each completed task produces a reusable code artifact. Progress is measured by the library's contents — what the agent can do is determined by what artifacts exist (HIGH — T1 source, demonstrated 3.3x improvement in unique items obtained).

**Reflection logs as artifacts.** Reflexion [7] stores verbal reflections in an "episodic memory buffer." These reflections are text artifacts that persist across attempts. On subsequent tries, the agent retrieves relevant past reflections to inform its approach. This achieved 91% pass@1 on HumanEval, surpassing GPT-4's 80% (HIGH — T1 source).

**Structured document artifacts.** MetaGPT [6] uses documents, diagrams, and code as shared artifacts between agents. An agent's output becomes the next agent's input, and the artifacts on disk represent the project's state. This mirrors how human teams track progress through deliverables rather than status updates (MODERATE — limited detail from abstract).

**Code as execution record.** CodeAct [12] uses Python code as a unified action space. The agent writes and executes code, then "dynamically revise[s] prior actions or emit[s] new actions upon new observations." The code history serves as both execution log and progress record (MODERATE — T2 source).

**Plan documents with checkboxes.** This pattern is common in practical systems (Claude Code, GitHub Copilot Workspace) but underrepresented in academic literature. A markdown plan with checkboxes provides both the task sequence and progress state. The agent reads the plan to determine what's done and what's next. The document is the single source of truth for execution state.

### How do agents handle failures?

**Reactive retry (ReAct pattern).** ReAct [1] handles failures through its reasoning-action loop. When an action fails or returns unexpected results, the reasoning trace identifies the issue and generates a corrective action. The agent "induce[s], track[s], and update[s] action plans as well as handle[s] exceptions" through ongoing reasoning (HIGH — T1 source).

**Verbal reflection.** Reflexion [7] generates textual analysis of what went wrong after a failed attempt. These reflections are stored and retrieved on subsequent attempts, enabling the agent to avoid repeating mistakes. The feedback loop accepts "various types (scalar values or free-form language) and sources (external or internally simulated) of feedback signals" (HIGH — T1 source).

**Iterative refinement.** Voyager [5] uses "a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification for program improvement." When code fails, the agent receives the error, revises the code, and retries (HIGH — T1 source).

**SOP-based validation.** MetaGPT [6] reduces cascading failures by validating intermediate outputs against standardized procedures. This addresses "logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs" (MODERATE — abstract-level detail).

**Backtracking.** Tree of Thoughts [3] enables explicit backtracking: agents can "look ahead or backtrack when necessary to make global choices." When a reasoning path fails, the agent returns to a previous state and tries an alternative (HIGH — T1 source, NeurIPS 2023).

**Replanning.** The When2Ask framework enables agents to "halt an ongoing plan and transition to a more suitable one based on new environmental observations." This represents full plan abandonment and regeneration rather than incremental repair (MODERATE — T2 source).

### How do agents resume across sessions?

Session resumption is the least-studied area in academic literature. Most research assumes single-session execution.

**Persistent skill libraries.** Voyager [5] is the clearest example: its skill library persists across sessions. "Voyager is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other techniques struggle to generalize" (HIGH — T1 source). The library is the checkpoint — no explicit save/restore is needed because the artifacts accumulate on disk.

**Episodic memory buffers.** Reflexion [7] maintains reflection logs that persist across attempts, though within a session. The pattern generalizes: if reflections are written to disk, they enable cross-session learning.

**Plan-document persistence.** In practical systems, the plan document itself serves as the resumption artifact. An agent reads a markdown plan with checkboxes, identifies incomplete items, and continues execution. This requires no special checkpoint mechanism — the plan is both the specification and the state.

**Conversation serialization.** AutoGen [10] and similar frameworks can serialize conversation history, but this is memory-based rather than artifact-based. The distinction matters: memory-based resumption requires loading the full prior context, while artifact-based resumption requires only reading the current state of deliverables.

### How are approval gates integrated?

**Human-in-the-loop modes.** AutoGen [10] explicitly supports "human inputs" as an agent mode, allowing human participation in multi-agent conversations. However, the paper doesn't specify structured approval gate patterns.

**SOP checkpoints.** MetaGPT's [6] SOP approach implicitly creates approval points: when an artifact passes from one agent role to another, the transition can include validation. This mirrors how human organizations use sign-offs between stages.

**Practical patterns.** In production systems, approval gates typically manifest as:
- Permission prompts before destructive actions (file deletion, deployments)
- Plan review before execution begins
- Checkpoint reviews at phase boundaries
- Escalation when confidence is low

These patterns are well-established in software engineering but have limited formal treatment in the LLM agent literature.

### How do ReAct, Plan-and-Execute, and Tree-of-Thought compare?

| Dimension | ReAct [1] | Plan-and-Execute [2] | Tree of Thoughts [3] |
|-----------|-----------|----------------------|----------------------|
| **Planning horizon** | None (reactive) | Full plan upfront | Explores multiple paths |
| **Decomposition** | Emergent from reasoning | Explicit subtask list | Branching thought units |
| **Sequencing** | Strict linear (think-act-observe) | Ordered plan steps | Tree search (BFS/DFS) |
| **Failure handling** | In-loop correction | Replan from scratch | Backtrack to branch point |
| **Progress tracking** | Reasoning trace | Plan completion status | Tree exploration state |
| **Best for** | Dynamic tasks, information gathering | Well-defined multi-step tasks | Constrained search problems |
| **Weakness** | No lookahead, local decisions | Plan may be wrong, costly replan | Expensive (many LLM calls) |
| **Session resumption** | Requires full context replay | Plan document persists | Tree state is transient |

ReAct excels at tasks requiring real-time adaptation to new information, such as web browsing or research. Plan-and-Execute suits tasks with clear structure where upfront planning reduces wasted work. Tree of Thoughts is most effective for problems with discrete solution spaces where exploration and backtracking provide value — it achieved 74% on Game of 24 vs. 4% for standard prompting [3] (HIGH — T1 source).

Hybrid approaches are increasingly common. LLMCompiler [8] combines plan-and-execute structure with parallel execution. LATS [11] integrates Monte Carlo Tree Search with LLM reasoning. Practical systems like Claude Code use plan-and-execute for the overall workflow with ReAct-style reasoning within each step.

## Challenge

**Artifact-based tracking is undertheorized.** Most academic work focuses on in-context state management. The practical pattern of using plan documents, code artifacts, and file system state as progress indicators has limited formal treatment. This gap means practitioners rely on engineering intuition rather than established patterns.

**Session resumption assumes memory, not artifacts.** The dominant approach to multi-session agents involves serializing conversation history or memory stores. Artifact-based resumption — where the agent reads the current state of deliverables to determine what's done — is more robust but less studied.

**Approval gates lack formal models.** Human-in-the-loop interaction is acknowledged but rarely formalized. Most frameworks treat human input as just another message in a conversation, without structured gate semantics (approve/reject/modify).

**Counter-evidence on plan quality.** Plan-and-execute approaches assume the initial plan is useful. However, plans generated by LLMs can be incorrect, incomplete, or based on hallucinated capabilities. ReAct's reactive approach avoids this by never committing to a plan, which can be more robust for novel tasks where the solution path is unknown.

**Scalability of tree search.** Tree of Thoughts requires multiple LLM calls per decision point. For complex real-world tasks with many steps, the combinatorial explosion makes full tree search impractical. LATS partially addresses this with MCTS, but the fundamental cost scaling remains.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/abs/2210.03629 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. / Princeton, Google | 2022 | T1 | verified |
| 2 | https://arxiv.org/abs/2305.04091 | Plan-and-Solve Prompting | Wang et al. / SMU Singapore | 2023 | T1 | verified |
| 3 | https://arxiv.org/abs/2305.10601 | Tree of Thoughts: Deliberate Problem Solving with LLMs | Yao et al. / Princeton, Google | 2023 | T1 | verified |
| 4 | https://arxiv.org/abs/2402.02716 | Understanding the Planning of LLM Agents: A Survey | Huang et al. / USTC | 2024 | T2 | verified |
| 5 | https://arxiv.org/abs/2305.16291 | Voyager: An Open-Ended Embodied Agent with LLMs | Wang et al. / NVIDIA, Caltech | 2023 | T1 | verified |
| 6 | https://arxiv.org/abs/2308.00352 | MetaGPT: Meta Programming for Multi-Agent Collaboration | Hong et al. | 2023 | T1 | verified |
| 7 | https://arxiv.org/abs/2303.11366 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. / Northeastern, MIT, Princeton | 2023 | T1 | verified |
| 8 | https://arxiv.org/abs/2312.04511 | LLMCompiler: An LLM Compiler for Parallel Function Calling | Kim et al. / UC Berkeley | 2023 | T1 | verified |
| 9 | https://arxiv.org/abs/2304.09842 | Chameleon: Plug-and-Play Compositional Reasoning with LLMs | Lu et al. / UCLA, Microsoft | 2023 | T1 | verified |
| 10 | https://arxiv.org/abs/2308.08155 | AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation | Wu et al. / Microsoft | 2023 | T2 | verified |
| 11 | https://arxiv.org/abs/2310.04406 | Language Agent Tree Search (LATS) | Zhou et al. / UIUC | 2023 | T1 | verified |
| 12 | https://arxiv.org/abs/2402.01030 | Executable Code Actions Elicit Better LLM Agents (CodeAct) | Wang et al. / UIUC | 2024 | T2 | verified |
| 13 | https://arxiv.org/abs/2303.17580 | HuggingGPT: Solving AI Tasks with ChatGPT and Friends | Shen et al. / Zhejiang, Microsoft | 2023 | T1 | verified |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | ReAct achieved 34% absolute success rate gain on ALFWorld | statistic | [1] | verified |
| 2 | Plan-and-Solve consistently outperforms Zero-shot-CoT across all datasets | superlative | [2] | verified |
| 3 | Tree of Thoughts achieved 74% on Game of 24 vs 4% for standard prompting | statistic | [3] | verified |
| 4 | Voyager achieves 3.3x more unique items than prior approaches | statistic | [5] | verified |
| 5 | MetaGPT generates more coherent solutions than previous chat-based multi-agent systems | superlative | [6] | verified |
| 6 | Reflexion achieved 91% pass@1 on HumanEval, surpassing GPT-4's 80% | statistic | [7] | verified |
| 7 | LLMCompiler achieves up to 3.7x latency speedup and 6.7x cost reduction | statistic | [8] | verified |
| 8 | LATS achieved 92.7% pass@1 on HumanEval with GPT-4 | statistic | [11] | verified |
| 9 | Huang et al. survey identifies five categories of LLM planning | attribution | [4] | verified |

## Search Protocol

| # | Query | Source | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | ReAct paper arxiv 2210.03629 | arxiv.org | 1 | ReAct paper details on reasoning-action interleaving |
| 2 | Plan-and-Solve prompting arxiv 2305.04091 | arxiv.org | 1 | Plan-and-Solve two-stage decomposition approach |
| 3 | Tree of Thoughts arxiv 2305.10601 | arxiv.org | 1 | ToT branching exploration with backtracking |
| 4 | LLM agent planning survey arxiv 2402.02716 | arxiv.org | 1 | Five-category planning taxonomy |
| 5 | Voyager LLM Minecraft arxiv 2305.16291 | arxiv.org | 1 | Skill library as persistent artifacts |
| 6 | MetaGPT arxiv 2308.00352 | arxiv.org | 1 | SOP-based multi-agent artifact passing |
| 7 | Reflexion arxiv 2303.11366 | arxiv.org | 1 | Verbal reflection as persistent learning artifacts |
| 8 | LLMCompiler arxiv 2312.04511 | arxiv.org | 1 | DAG-based parallel function calling |
| 9 | Chameleon arxiv 2304.09842 | arxiv.org | 1 | Tool composition planning |
| 10 | AutoGen arxiv 2308.08155 | arxiv.org | 1 | Multi-agent conversation coordination |
| 11 | LATS arxiv 2310.04406 | arxiv.org | 1 | Monte Carlo Tree Search with LLM agents |
| 12 | CodeAct arxiv 2402.01030 | arxiv.org | 1 | Code as unified action space |
| 13 | HuggingGPT arxiv 2303.17580 | arxiv.org | 1 | Pipeline task decomposition with model selection |
