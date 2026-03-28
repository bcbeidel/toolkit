---
name: "Structured Thinking and Decision Frameworks"
description: "Mental models and structured thinking frameworks — how to operationalize them as agent-usable tools rather than passive reference material"
metadata:
  type: research
  sources:
    - https://fs.blog/mental-models/
    - https://arxiv.org/abs/2201.11903
    - https://arxiv.org/abs/2305.10601
    - https://arxiv.org/html/2602.16512
    - https://arxiv.org/abs/2210.03629
    - https://lilianweng.github.io/posts/2023-06-23-agent/
    - https://towardsdatascience.com/something-of-thought-in-llm-prompting-an-overview-of-structured-llm-reasoning-70302752b390/
    - https://arxiv.org/html/2510.08104
    - https://learnprompting.org/docs/advanced/self_criticism/cumulative_reasoning
    - https://www.promptingguide.ai/techniques/tot
  related:
    - docs/context/structured-thinking-decision-frameworks.md
    - docs/context/agentic-planning-execution.md
    - docs/context/prompt-engineering.md
---

# Structured Thinking and Decision Frameworks

## Key Findings

1. **Mental models become agent-usable only when converted from descriptive frameworks into executable procedures** — a named model with input/output contracts, decision criteria, and output format that an agent can invoke as a reasoning step within a workflow.

2. **The gap between knowing a framework and operationalizing it is the same gap between chain-of-thought prompting and agentic reasoning** — both require making implicit reasoning explicit, structuring it into discrete steps, and enabling self-evaluation at each step.

3. **Five classical models map directly to agent operations**: first principles → recursive decomposition; inversion → pre-mortem failure analysis; Eisenhower → urgency/importance classification; Pareto → impact-weighted ranking; second-order effects → consequence chain tracing.

4. **Structured reasoning research (CoT, ToT, GoT, FoT) provides the execution substrate** — these are not just prompting tricks but architectural patterns for how agents traverse decision spaces, with measurable performance gains (ToT improved GPT-4 from 4% to 74% on Game of 24).

5. **The operational pattern is: decompose → evaluate → select → verify** — every mental model, when made executable, follows this same meta-structure regardless of the specific framework.

---

## Classical Mental Models and Their Agent Translations

### First Principles Thinking

**What it is.** Decompose a problem to its fundamental truths and reason upward, discarding assumptions and analogies. Attributed to Aristotle, popularized in engineering and entrepreneurship contexts.

**Agent translation.** Recursive decomposition with assumption auditing. The agent receives a problem statement, identifies all implicit assumptions, strips each one, and rebuilds understanding from verified base facts. This maps directly to task decomposition in agentic planning — breaking complex goals into atomic subtasks that can be independently verified.

**Executable pattern:**
- Input: problem statement + current assumptions
- Process: list assumptions → challenge each → identify irreducible facts → rebuild solution from facts only
- Output: decomposed problem with assumption audit trail
- Verification: each base fact must be independently confirmable

### Inversion (Pre-Mortem)

**What it is.** Instead of asking "How do I succeed?", ask "What would guarantee failure?" Identify failure modes first, then design to prevent them. The pre-mortem variant assumes the project has already failed and asks why.

**Agent translation.** Failure-mode enumeration before plan execution. Before committing to a plan, the agent runs an inversion pass: assume the plan failed, enumerate the most likely causes, then check whether the current plan addresses each failure mode.

**Executable pattern:**
- Input: proposed plan or decision
- Process: assume failure → enumerate causes → rank by likelihood × impact → check mitigations
- Output: risk-annotated plan with unaddressed failure modes flagged
- Verification: each high-risk failure mode has an explicit mitigation or acceptance rationale

### Eisenhower Matrix

**What it is.** Classify tasks on two dimensions: urgency (time-sensitive) and importance (contributes to goals). Four quadrants: Do (urgent+important), Schedule (important, not urgent), Delegate (urgent, not important), Eliminate (neither).

**Agent translation.** Task triage with explicit criteria. The agent classifies incoming work against defined urgency and importance criteria, routing tasks to appropriate handling modes. Quadrant 2 (important, not urgent) is where strategic value lives — agents should protect time for it.

**Executable pattern:**
- Input: task list + goal definitions + deadline information
- Process: score each task on urgency [0-1] and importance [0-1] → classify into quadrants → apply routing rules
- Output: prioritized task list with quadrant assignments and recommended actions
- Verification: no Quadrant 2 tasks displaced by Quadrant 3 tasks without explicit override

### Pareto Principle (80/20)

**What it is.** Roughly 80% of effects come from 20% of causes. Applied to prioritization: identify the vital few inputs that produce most of the desired output.

**Agent translation.** Impact-weighted ranking with diminishing returns detection. The agent estimates the expected impact of each candidate action, ranks them, identifies the concentration point where effort-to-impact ratio degrades, and recommends a cutoff.

**Executable pattern:**
- Input: candidate actions + estimated impact per action + estimated effort per action
- Process: compute impact/effort ratio → sort descending → find the knee (where cumulative impact crosses ~80%) → mark items above and below the knee
- Output: ranked list with Pareto frontier marked, recommendation to focus on above-knee items
- Verification: cumulative impact of recommended items should cover majority of total available impact

### Second-Order Effects

**What it is.** Ask "and then what?" for each decision. First-order effects are direct; second-order effects are consequences of consequences. Most planning failures come from ignoring second-order effects.

**Agent translation.** Consequence chain tracing with depth limits. The agent takes a proposed action, traces its immediate consequences, then traces consequences of those consequences, to a configurable depth (typically 2-3 levels). Each level is evaluated for desirability.

**Executable pattern:**
- Input: proposed action + system context
- Process: identify 1st-order effects → for each, identify 2nd-order effects → for each, identify 3rd-order effects → evaluate desirability of each effect chain
- Output: consequence tree with desirability annotations at each node
- Verification: any undesirable 2nd+ order effect with high probability should trigger plan revision

---

## The Operationalization Gap

The central problem is not that agents lack access to mental model descriptions — it is that descriptions are not executable. Reading about inversion thinking does not produce inversion thinking any more than reading about swimming produces swimming.

Three properties distinguish an operationalized framework from reference material:

1. **Defined trigger conditions.** The agent knows *when* to apply the framework. First principles thinking triggers when assumptions are unexamined. Inversion triggers before committing to a plan. Eisenhower triggers when task volume exceeds capacity. Without triggers, models sit inert in context.

2. **Structured procedure.** The framework specifies discrete steps with inputs and outputs at each step. This is the difference between "consider second-order effects" (vague instruction) and "for each proposed action, list 3 immediate consequences, then for each consequence list 2 further consequences, then rate each leaf consequence as beneficial/neutral/harmful" (executable procedure).

3. **Verification criteria.** The agent can check whether it applied the framework correctly. Did the inversion pass actually enumerate failure modes? Did the Pareto analysis produce a ranked list? Without verification, the agent cannot self-correct.

This mirrors the evolution in LLM reasoning research. Early chain-of-thought prompting (Wei et al., 2022) simply asked models to "think step by step" — a vague instruction that sometimes helped. Tree-of-Thought (Yao et al., 2023) added structured exploration with self-evaluation at each node, producing dramatic improvements. The Framework of Thoughts (FoT, 2026) further unified these into dynamic execution graphs where reasoning operations have explicit inputs, outputs, and dependency relationships.

The pattern is consistent: **making reasoning structure explicit and evaluable produces better outcomes than asking for reasoning in general.**

---

## Structured LLM Reasoning Research

### Chain-of-Thought (CoT)

Wei et al. (2022) demonstrated that providing a few examples of step-by-step reasoning in prompts enables LLMs to generate intermediate reasoning steps. CoT is now understood as a foundational technique, but its limitation is linearity — it follows a single reasoning path without exploring alternatives or backtracking.

**Key finding for operationalization:** CoT works because it makes reasoning explicit, not because the specific chain matters. This supports the principle that any mental model must be rendered as explicit steps to be agent-usable.

### Tree-of-Thought (ToT)

Yao et al. (2023) generalized CoT by allowing models to explore multiple reasoning paths, evaluate them, and backtrack. On Game of 24, GPT-4 with CoT solved 4% of problems; with ToT it solved 74%. The key mechanism is self-evaluation: at each node, the model assesses whether the current path is promising before continuing.

**Key finding for operationalization:** Exploration + self-evaluation dramatically outperforms linear reasoning. Mental models like inversion and second-order effects are inherently tree-structured — they branch into multiple scenarios. ToT provides the execution pattern.

### ReAct (Reasoning + Acting)

Yao et al. (2023) interleaved reasoning traces with actions (tool calls, observations). The thought-action-observation cycle allows agents to reason about what they know, act to learn more, and adjust plans based on results. ReAct reduces hallucination by grounding reasoning in external observations.

**Key finding for operationalization:** Mental models need grounding in external data to be useful. First principles thinking requires verifying base facts; Pareto analysis requires actual impact data. The ReAct pattern provides the mechanism for agents to gather evidence during structured reasoning.

### Framework of Thoughts (FoT)

FoT (2026) is a unifying framework that models reasoning as a dynamic execution graph where operations (LLM calls, tool calls, code execution) chain together with explicit input/output contracts. It achieved 10.7x average speedup through parallelization and caching, with cost reductions to 9-36% of unoptimized variants.

**Key finding for operationalization:** Mental models can be composed into graphs where the output of one model feeds the input of another. First principles decomposition can feed into Pareto ranking, which feeds into Eisenhower classification — each as a discrete graph node with defined interfaces.

### Cumulative Reasoning

Cumulative reasoning extends CoT by maintaining a growing context of verified propositions. Each reasoning step adds to a knowledge base that subsequent steps can reference. A verification step checks each new proposition against existing ones for consistency.

**Key finding for operationalization:** Mental models produce intermediate conclusions that should accumulate and be cross-checked. Second-order effect chains, for instance, may contradict conclusions from an inversion analysis — cumulative reasoning catches these conflicts.

---

## Practical Patterns for Agent Workflows

### Pattern 1: Framework as Tool

Define each mental model as a callable tool with a schema. The agent selects which framework to apply based on the problem type.

```
Tool: first_principles_decomposition
Input: { problem: string, known_assumptions: string[] }
Output: { base_facts: string[], rebuilt_solution: string, assumptions_challenged: string[] }
```

This makes frameworks composable and auditable. The agent's reasoning trace shows which tool was called, with what inputs, producing what outputs.

### Pattern 2: Framework as Gate

Use frameworks as decision gates in workflows. Before a plan executes, it must pass through an inversion gate (failure modes identified and mitigated) and a second-order effects gate (consequence chains traced and evaluated). If the gate fails, the plan returns for revision.

### Pattern 3: Framework as Evaluation Rubric

Use frameworks to evaluate outputs, not just produce them. An Eisenhower classification of a generated task list can identify whether the agent is spending effort on Quadrant 3 (urgent but unimportant) work. A Pareto analysis of completed work can identify whether the vital few items were addressed.

### Pattern 4: Metacognitive Trigger

Train the agent to recognize when a specific framework applies. Problem feels stuck? Apply first principles. About to commit to a plan? Apply inversion. Task list growing? Apply Eisenhower + Pareto. This is the "defined trigger conditions" property from the operationalization gap analysis.

### Pattern 5: Composed Pipeline

Chain frameworks in sequence for complex decisions:
1. First principles → decompose the problem
2. Pareto → identify highest-impact subproblems
3. Inversion → identify failure modes for top subproblems
4. Eisenhower → prioritize remaining work
5. Second-order effects → validate the plan doesn't create worse problems

Each stage has explicit inputs from the previous stage and verification criteria.

---

## Source Quality Assessment

| Tier | Source | Type | Relevance |
|------|--------|------|-----------|
| T1 | Wei et al. 2022 — Chain-of-Thought (arXiv:2201.11903) | Peer-reviewed (NeurIPS) | Foundational CoT research |
| T1 | Yao et al. 2023 — Tree of Thoughts (arXiv:2305.10601) | Peer-reviewed (NeurIPS) | ToT framework and results |
| T1 | Yao et al. 2023 — ReAct (arXiv:2210.03629) | Peer-reviewed (ICLR) | Reasoning + Acting framework |
| T2 | FoT 2026 — Framework of Thoughts (arXiv:2602.16512) | Preprint | Unified reasoning framework |
| T2 | Mental Models in Human-AI Collaboration (arXiv:2510.08104) | Preprint | Mental model conceptual framework |
| T3 | Farnam Street — Mental Models | Established reference | Comprehensive model catalog |
| T3 | Lilian Weng — LLM Powered Autonomous Agents | Established blog (OpenAI) | Agent architecture survey |
| T3 | Towards Data Science — Something-of-Thought Overview | Established blog | Structured reasoning survey |
| T3 | Learn Prompting — Cumulative Reasoning | Educational resource | Reasoning technique reference |
| T3 | Prompting Guide — Tree of Thoughts | Educational resource | ToT technique reference |

---

## Claims Verification

| Claim | Source | Status |
|-------|--------|--------|
| CoT improves multi-step reasoning in LLMs | Wei et al. 2022 (NeurIPS) | Verified — replicated widely |
| ToT improved GPT-4 from 4% to 74% on Game of 24 | Yao et al. 2023 (NeurIPS) | Verified — published results |
| ReAct reduces hallucination through grounding | Yao et al. 2023 (ICLR) | Verified — published results |
| FoT achieves 10.7x speedup via parallelization | FoT 2026 preprint | Plausible — preprint, not yet peer-reviewed |
| Mental models need trigger conditions to be operational | Synthesized from multiple sources | Analytical claim — well-supported pattern |
| Five classical models map to specific agent operations | Author synthesis | Analytical claim — novel contribution |
| Decompose → evaluate → select → verify is universal meta-pattern | Author synthesis from CoT/ToT/ReAct literature | Analytical claim — supported by convergent evidence |

---

## Search Protocol

| # | Query | Engine | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | mental models decision making first principles inversion Pareto operationalize AI agents 2025 2026 | Web | 10 | 4 |
| 2 | LLM reasoning structured frameworks chain-of-thought tree-of-thought structured thinking 2025 | Web | 10 | 6 |
| 3 | operationalizing mental models AI agents executable frameworks not just reference material | Web | 10 | 4 |
| 4 | Eisenhower matrix AI task prioritization agent systems second-order effects thinking | Web | 10 | 3 |
| 5 | first principles thinking AI prompt engineering decomposition reasoning 2025 | Web | 10 | 5 |
| 6 | "second-order effects" "second order thinking" AI agents decision making consequences | Web | 10 | 4 |
| 7 | structured reasoning prompts LLM decision frameworks inversion thinking pre-mortem agent | Web | 10 | 5 |
| 8 | knowledge-action gap mental models operationalize structured prompts AI executable decision procedures 2024 2025 | Web | 10 | 3 |
| 9 | ReAct reasoning acting LLM agents Yao 2023 structured decision making | Web | 10 | 4 |
| 10 | chain of thought prompting Wei 2022 arxiv reasoning large language models | Web | 10 | 3 |
| 11 | tree of thoughts deliberate problem solving Yao 2023 LLM reasoning | Web | 10 | 3 |
| 12 | Lilian Weng LLM powered autonomous agents planning reasoning tool use 2023 | Web | 10 | 3 |

**Total searches:** 12 | **Total results reviewed:** 120 | **Sources selected:** 10

---

## Key Takeaways

1. **Mental models are not useful as reference material for agents.** They must be converted to executable procedures with defined inputs, outputs, trigger conditions, and verification criteria.

2. **The structured reasoning literature (CoT → ToT → ReAct → FoT) provides the execution substrate.** These are not alternative approaches but a progressive stack: CoT makes reasoning explicit, ToT adds exploration, ReAct adds grounding, FoT adds composition.

3. **Five classical models are directly implementable as agent tools:** first principles (decomposition), inversion (failure-mode analysis), Eisenhower (priority classification), Pareto (impact ranking), second-order effects (consequence tracing). Each follows the decompose → evaluate → select → verify meta-pattern.

4. **The operationalization gap has three dimensions:** trigger conditions (when to apply), structured procedure (how to apply), and verification criteria (whether it was applied correctly). Missing any one makes the framework inert.

5. **Composition is the high-value pattern.** Individual frameworks are useful; chaining them (decompose → rank → risk-check → prioritize → validate) produces decision quality that exceeds any single model. FoT demonstrates this can be done efficiently with parallelization and caching.
