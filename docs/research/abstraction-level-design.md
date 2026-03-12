---
name: "Abstraction Level Design for Agent-Facing Artifacts"
description: "How calibrating abstraction altitude across specs (WHAT/WHY), plans (observable outcomes), research (mode intensity), and instructions (specificity) affects agent execution reliability — with empirical evidence on the specificity-flexibility tradeoff"
type: research
sources:
  - https://arxiv.org/html/2512.02246v1
  - https://arxiv.org/html/2505.13360v1
  - https://arxiv.org/html/2510.23564v1
  - https://arxiv.org/html/2601.22290
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://code.claude.com/docs/en/best-practices
  - https://openreview.net/pdf?id=sY5N0zY5Od
  - https://githubnext.com/projects/copilot-workspace/
  - https://arxiv.org/abs/2311.07599
  - https://blog.wispera.ai/developing-artfully-vague-prompts/
  - https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
  - https://glazkov.com/2024/01/16/declarative-vs-imperative/
related:
  - docs/research/prompt-engineering.md
  - docs/research/agentic-planning-execution.md
  - docs/research/writing-for-llm-consumption.md
  - docs/research/information-architecture.md
  - docs/research/context-engineering.md
  - docs/research/knowledge-synthesis-distillation.md
  - docs/context/abstraction-level-design.md
---

Different artifact types in agent-facing systems require different abstraction altitudes. Specifications that prescribe HOW instead of WHAT constrain agents into suboptimal implementations. Plans with vague aspirations instead of observable outcomes give agents no way to self-verify progress. Instructions that are too rigid break on novel inputs; instructions that are too vague regress 2x more across model updates. The core insight: abstraction altitude is not a style choice but an engineering variable with measurable effects on agent execution reliability.

## Sub-Questions

1. What is "abstraction altitude" in the context of agent-facing artifacts, and what conceptual frameworks describe it?
2. How should specifications be written (WHAT/WHY altitude) to maximize agent comprehension and prevent implementation drift?
3. What altitude produces the most effective plans — high-level goals vs. granular tasks vs. observable outcomes?
4. How does research document intensity (depth vs. breadth) affect downstream synthesis and agent decision quality?
5. How should instruction specificity be calibrated — the too-vague vs. too-rigid tradeoff — for reliable agent execution?
6. What empirical evidence connects abstraction level choices to measurable agent execution outcomes?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/html/2512.02246v1 | DETAIL Matters: Measuring the Impact of Prompt Specificity on Reasoning in LLMs | Siddiqui et al. | 2024 | T2 | verified |
| 2 | https://arxiv.org/html/2505.13360v1 | What Prompts Don't Say: Understanding and Managing Underspecification in LLM Prompts | Multiple authors | 2025 | T2 | verified |
| 3 | https://arxiv.org/html/2510.23564v1 | ReCode: Unify Plan and Action for Universal Granularity Control | FoundationAgents | 2025 | T2 | verified |
| 4 | https://arxiv.org/html/2601.22290 | The Six Sigma Agent: Enterprise-Grade Reliability Through Consensus-Driven Decomposed Execution | Multiple authors | 2026 | T2 | verified |
| 5 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill Authoring Best Practices | Anthropic | 2025 | T1 | verified |
| 6 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic | 2025 | T1 | verified |
| 7 | https://openreview.net/pdf?id=sY5N0zY5Od | DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines | Khattab et al. / Stanford | 2024 | T1 | verified |
| 8 | https://githubnext.com/projects/copilot-workspace/ | Copilot Workspace | GitHub Next | 2024 | T1 | verified |
| 9 | https://arxiv.org/abs/2311.07599 | Testing LLMs on Code Generation with Varying Levels of Prompt Specificity | Multiple authors | 2023 | T2 | verified |
| 10 | https://blog.wispera.ai/developing-artfully-vague-prompts/ | Developing Artfully Vague Prompts | Mark Ratjens / Wispera | 2025 | T4 | verified |
| 11 | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Equipping Agents for the Real World with Agent Skills | Anthropic | 2025 | T1 | verified |
| 12 | https://glazkov.com/2024/01/16/declarative-vs-imperative/ | Declarative vs. Imperative | Dimitri Glazkov | 2024 | T3 | verified |

## Research Protocol

| # | Query | Tool | Results | Selected |
|---|-------|------|---------|----------|
| 1 | abstraction level specification vs plan vs instruction agent execution LLM 2025 | WebSearch | 10 results on planning paradigms and agent architecture | [3], [4] |
| 2 | specification abstraction altitude WHAT WHY vs HOW software engineering agents | WebSearch | 10 results on abstraction layers and declarative specs | [12] |
| 3 | plan granularity observable outcomes agent task decomposition reliability 2025 | WebSearch | 10 results on decomposition strategies and evaluation | [3], [4] |
| 4 | instruction specificity calibration LLM prompt too vague too rigid agent performance | WebSearch | 10 results on specificity tradeoffs | [1], [2], [10] |
| 5 | DETAIL Matters prompt specificity LLM reasoning (direct fetch) | WebFetch | Detailed metrics on specificity levels and accuracy | [1] |
| 6 | Six Sigma Agent task decomposition granularity reliability (direct fetch) | WebFetch | Atomic decomposition metrics and DPMO reliability | [4] |
| 7 | Anthropic Claude agent skill instruction design specificity best practices 2025 | WebSearch | 10 results on skill authoring | [5], [11] |
| 8 | Anthropic skill authoring best practices (direct fetch) | WebFetch | Full degrees-of-freedom framework | [5] |
| 9 | Claude Code best practices (direct fetch) | WebFetch | Full CLAUDE.md guidance and plan-mode workflow | [6] |
| 10 | DSPy declarative specification signature LLM what not how abstraction pipeline 2024 | WebSearch | 10 results on declarative specifications | [7] |
| 11 | ReCode plan action universal granularity control (direct fetch) | WebFetch | Recursive decomposition metrics and inverted-U pattern | [3] |
| 12 | GitHub Copilot workspace specification plan implementation step levels | WebSearch | 10 results on spec-plan-implement pipeline | [8] |
| 13 | "artfully vague" prompts LLM instruction specificity flexibility | WebSearch | 10 results on iterative refinement approach | [10] |
| 14 | What Prompts Don't Say underspecification (direct fetch) | WebFetch | Underspecification prevalence and regression rates | [2] |
| 15 | Claude Code CLAUDE.md specification vs instruction best practices 2025 2026 | WebSearch | 10 results on CLAUDE.md conventions | [6] |
| 16 | software requirements specification abstraction level WHAT not HOW declarative imperative | WebSearch | 10 results on declarative specifications | [7], [12] |
| 17 | arxiv task specification agent performance level detail instruction following LLM 2024 2025 | WebSearch | 10 results on instruction fidelity benchmarks | Supporting context |
| 18 | Testing LLMs on Code Generation with Varying Levels of Prompt Specificity | WebFetch | Four specificity levels, accuracy/efficiency metrics | [9] |

## Findings

### 1. Abstraction Altitude as an Engineering Variable

Abstraction altitude describes how much implementation detail an artifact exposes. Higher altitude means more WHAT/WHY, less HOW. Lower altitude means more HOW, less WHAT/WHY. This is not a style preference — it is an engineering variable with measurable effects on agent behavior.

The concept maps directly to the declarative-imperative spectrum from software engineering. Declarative artifacts specify WHAT should happen; imperative artifacts specify HOW it should happen. Glazkov articulates the core insight: "Every abstraction layer brings some 'declarativeness' with it, shifting the burden of having to think about implementation details" from the consumer into the layer [12]. For agent-facing artifacts, the "consumer" is the LLM, and the "layer" is the agent's reasoning capability.

DSPy (ICLR 2024) provides the clearest formalization of this principle for LLM systems. A DSPy signature is "a natural-language typed function declaration that tells DSPy what a transformation needs to do (e.g., consume questions and return answers), rather than how a specific language model should be prompted to implement that behavior" [7]. Standard prompts "conflate interface ('what should the LM do?') with implementation ('how do we tell it to do that?')," while DSPy separates them so the implementation can be learned from data. This separation — WHAT from HOW — is the foundational principle of altitude calibration (HIGH — T1 source, ICLR 2024 peer-reviewed).

**The altitude spectrum for agent-facing artifacts:**

| Altitude | Content | Artifact Type | Agent Freedom |
|----------|---------|---------------|---------------|
| Highest | Purpose and constraints only | Specifications | Maximum |
| High | Goals with observable outcomes | Plans | High |
| Medium | Patterns with adaptation latitude | Research context | Medium |
| Low | Step-by-step procedures | Instructions | Low |
| Lowest | Exact commands, no deviation | Scripts/hooks | None |

The key insight: each artifact type has a natural altitude, and deviating from it — writing specs at low altitude or instructions at high altitude — degrades agent execution quality (MODERATE — synthesized from multiple sources, no single study tests this directly).

### 2. Specifications: WHAT and WHY, Never HOW

Specifications answer two questions: WHAT should the system do, and WHY does it matter? When specifications descend to HOW, they constrain the agent's solution space unnecessarily, often forcing suboptimal implementations because the spec author cannot anticipate all contexts.

**The Copilot Workspace model.** GitHub's Copilot Workspace implements a three-layer altitude stack: specification (current state vs. desired state), plan (files to modify with actions per file), and implementation (actual code diffs). Each layer operates at a distinct altitude [8]. The specification layer consists of "two bullet-point lists: one for the current state of the codebase, and one for the desired state." Users edit both lists "either to correct the system's understanding of the current codebase, or to refine the requirements for the desired state." The specification never mentions file paths, functions, or implementation strategies — it stays at the WHAT/WHY altitude.

**Why WHAT-level specifications work better for agents:**

1. **Agents explore the solution space better than humans predict it.** When a specification says "use React hooks for state management" rather than "state should persist across page navigation," the agent is locked into a specific implementation even if the codebase already uses Zustand or Redux. The declarative specification allows the agent to discover and leverage existing patterns (MODERATE — inferred from [6], [7]).

2. **WHAT-level specs compose with context.** A specification like "users must be able to filter search results by date range" interacts well with whatever the agent discovers about the existing codebase. An imperative specification like "add a DateRangePicker component that calls the /api/search endpoint with startDate and endDate parameters" presumes specific architecture that may not exist (MODERATE — practical reasoning from [6], [8]).

3. **DSPy validates this empirically.** By separating WHAT (signatures) from HOW (prompting strategies), DSPy achieves pipeline optimization that outperforms hand-crafted prompts. The compiler discovers prompting strategies that humans would not have designed, precisely because the specification does not prescribe them [7] (HIGH — T1 source).

**Counter-evidence:** Pure WHAT-level specifications can be dangerously vague. The underspecification research shows that LLMs guess unspecified requirements correctly only 41.1% of the time, with conditional requirements dropping to 22.9% accuracy [2]. This does not argue for HOW-level specs, but it does argue that WHAT-level specs must be explicit and complete about constraints, edge cases, and success criteria. The solution is not to lower altitude but to increase coverage at the specification altitude.

### 3. Plans: Middle Altitude with Observable Outcomes

Plans occupy the altitude between specifications (WHAT/WHY) and instructions (HOW). The optimal plan altitude is "observable outcomes" — statements that an agent can verify against reality without human judgment.

**The granularity problem.** ReCode (2025) provides the strongest empirical evidence on plan granularity. Testing recursive decomposition depth on ScienceWorld, they found an "inverted-U pattern, peaking at depth 8 (43.22%)" [3]. Both shallow depths (insufficient decomposition) and excessive depths (over-fragmentation) reduce performance. The optimal range fell between depths 6-12, suggesting that plans need enough decomposition to be tractable but not so much that the agent loses sight of the overall goal.

ReCode also demonstrates that adaptive granularity outperforms fixed granularity. By treating "plans as essentially high-level actions at different abstraction levels" that can be recursively decomposed as needed, ReCode achieves 60.8 average reward — 20.9% better than the best fixed-granularity baseline — while using 78.9% fewer tokens than ReAct and 84.4% fewer than CodeAct [3] (HIGH — T2 source with strong quantitative evidence).

**The Six Sigma decomposition principle.** For plans to enable reliable execution, individual plan items must satisfy three properties: minimality (cannot be meaningfully decomposed further), verifiability (correctness is objectively determinable), and functional determinism (correct reasoning yields a unique correct output) [4]. When plan items satisfy these three properties, consensus-based execution achieves exponential reliability gains: five agents with 5% individual error rates achieve 0.116% combined error rate (HIGH — T2 source with formal proofs).

**Observable outcomes vs. activities.** The distinction between an effective and ineffective plan item is whether it describes an observable outcome or an activity:

| Plan altitude | Example | Verifiable? |
|---------------|---------|-------------|
| Too high | "Improve the authentication system" | No — what counts as "improved"? |
| Too high | "Make login more secure" | No — no measurable criterion |
| Right altitude | "Login endpoint returns 401 for expired tokens" | Yes — testable |
| Right altitude | "Session timeout redirects to /login with return URL preserved" | Yes — observable |
| Too low | "Add `if token.expired: return 401` to line 47 of auth.py" | Yes, but constrains implementation |
| Too low | "Call `session.invalidate()` then `redirect('/login')` " | Yes, but prescribes HOW |

The right altitude for plans is the one where each item is verifiable without prescribing implementation. This is the "middle altitude" that separates plans from both specifications (which describe desired end states) and instructions (which describe execution steps) (MODERATE — synthesized from [3], [4], [6]).

**Checkboxes as progress artifacts.** Claude Code's recommended workflow uses plan documents with checkboxes: "Copy this checklist and track your progress" [5]. This pattern works because checkboxes are binary observable outcomes — done or not done — and the document itself is the single source of truth for execution state. The plan is simultaneously a specification of work and a progress tracker.

### 4. Research: Mode Intensity and Depth-Breadth Calibration

Research documents occupy a unique altitude position. Unlike specifications (which drive action), plans (which sequence action), or instructions (which prescribe action), research documents inform decisions. Their altitude question is not WHAT vs. HOW but DEPTH vs. BREADTH — how deep to investigate each sub-question vs. how many sub-questions to cover.

**Mode intensity determines coverage depth.** Different research modes demand different coverage intensities. A deep-dive investigation requires exhaustive coverage of fewer sub-questions. A landscape survey requires broad coverage with less depth per topic. A feasibility study requires just enough depth to make a go/no-go decision. The altitude choice is not about detail level in the traditional sense but about the ratio of comprehensiveness to economy.

**The compression-purpose relationship.** Knowledge synthesis research establishes that compression must be defined relative to purpose: "relevant information is defined by what the compressed output needs to predict" (Tishby et al., information bottleneck method). For agent-facing research documents, the "relevant variable" is the decision or action the consuming agent will take. Research altitude should be calibrated to the downstream use case:

- **Research informing specifications:** Needs high-altitude findings — WHAT is true and WHY it matters, not HOW the researchers established it.
- **Research informing plans:** Needs middle-altitude patterns — what approaches exist, what tradeoffs they have, which ones fit the constraints.
- **Research informing instructions:** Needs low-altitude specifics — exact numbers, concrete examples, verified claims with sources.

**Structured sections force appropriate altitude.** Factory.ai found that structured summarization with dedicated sections outperforms opaque compression (3.70 vs. 3.35 quality score at similar compression ratios). Each required section acts as an altitude constraint — a "Sources" table enforces provenance tracking, a "Findings" section enforces synthesis over raw extraction, a "Claims" table enforces verification (MODERATE — T3 source from existing research).

### 5. Instructions: The Specificity Calibration Problem

Instructions — skill prompts, CLAUDE.md rules, workflow steps — are the lowest-altitude artifacts that still involve natural language. Their calibration problem is the most empirically studied: too vague and agents guess wrong; too rigid and they break on novel inputs.

**The empirical specificity curve.** The DETAIL Matters study (2024) measured prompt specificity using perplexity scores across three levels: Level-1 (vague, ~18.9 perplexity), Level-2 (moderate), and Level-3 (detailed, ~45.7 perplexity). Results show consistent accuracy improvements with increased specificity, but the gains are task-dependent [1]:

- **Procedural tasks** (math, logic, code): +0.47, +0.36, +0.29 accuracy gain respectively
- **Inference tasks** (commonsense, decision-making): +0.08, +0.02 gain; detailed prompts occasionally hurt performance

GPT-4 showed "resilience to low-specificity prompts" while O3-mini demonstrated "pronounced sensitivity," indicating that larger models compensate internally for what smaller models need externally specified [1] (HIGH — T2 source with controlled experiments).

**The underspecification regression risk.** The "What Prompts Don't Say" study (2025) establishes the cost of leaving requirements implicit: unspecified requirements are "2x more likely to regress over model or prompt changes" compared to explicitly specified ones, with standard deviations of 8.9% vs. lower for specified requirements. However, specifying all 19 requirements in a single prompt reduced accuracy to 85.0% for GPT-4o and 79.7% for Llama-3.3, with 37.5% of requirements showing >5% degradation when coexisting with many other requirements [2] (HIGH — T2 source with quantitative evidence).

The resolution: **selective specification** — explicitly specify only requirements that are (a) critical to correctness, (b) unstable across model updates, or (c) unlikely to be guessed from context. Leave stable, predictable requirements to model defaults [2].

**Anthropic's degrees-of-freedom framework.** The skill authoring best practices formalize this calibration with three levels [5]:

- **High freedom** (text-based guidelines): "Multiple approaches are valid. Decisions depend on context. Heuristics guide the approach." Example: code review guidelines.
- **Medium freedom** (pseudocode with parameters): "A preferred pattern exists. Some variation is acceptable." Example: report templates with customization points.
- **Low freedom** (exact scripts): "Operations are fragile and error-prone. Consistency is critical. A specific sequence must be followed." Example: database migrations.

The analogy: "Think of Claude as a robot exploring a path. Narrow bridge with cliffs on both sides — provide exact instructions. Open field with no hazards — give general direction and trust Claude to find the best route" [5] (HIGH — T1 source).

**The artfully vague approach.** An alternative perspective argues for starting with minimal constraints and iterating: "An artfully vague prompt frames a clear task or question but imposes minimal constraints, allowing the LLM to range across broad general knowledge and interpretive flexibility" [10]. The iterative refinement process starts vague, observes where the model diverges from intent, and adds constraints only where needed. This is essentially empirical specificity calibration — let the model's behavior determine the altitude rather than prescribing it upfront (LOW — T4 source, practitioner blog, but converges with [2]).

**Claude Code confirms the calibrated approach.** The best practices documentation states: "Vague prompts can be useful when you're exploring and can afford to course-correct. A prompt like 'what would you improve in this file?' can surface things you wouldn't have thought to ask about" [6]. But for implementation: "The more precise your instructions, the fewer corrections you'll need" [6]. The altitude depends on the phase — exploration warrants higher altitude; implementation warrants lower altitude (HIGH — T1 source).

### 6. Empirical Evidence: Altitude Mismatches Degrade Performance

Multiple studies provide quantitative evidence that altitude mismatches — artifacts written at the wrong abstraction level — produce measurable performance degradation.

**Over-decomposition costs.** ReCode's depth analysis shows that excessive decomposition (depth >12) performs worse than moderate decomposition (depth 6-12), with a clear inverted-U pattern. Over-decomposition "fragment[s] the decision-making process" — the agent loses coherence by focusing too narrowly [3]. The cost is not merely wasted tokens but reduced task completion rates. ReCode achieved 78.9% fewer tokens than ReAct precisely by avoiding unnecessary low-altitude decomposition (HIGH — T2 source).

**Under-specification costs.** Unspecified requirements produce accuracy decreases of up to 22.6% on average, with worst-case drops of 93.1% [2]. Conditional requirements — the edge cases and "if X, then do Y" rules — are the most dangerous gap, with only 22.9% correct guessing rates. Format requirements are guessed most reliably at 70.7%. This suggests that instructions should specify conditional logic and edge cases explicitly (low altitude for those specific aspects) while leaving format and structure to model defaults (higher altitude) (HIGH — T2 source).

**Over-specification costs.** Adding all 19 requirements simultaneously to a single prompt produces 15-20% accuracy degradation because "LLMs struggle with following many requirements at the same time" [2]. This is the instruction-density ceiling — there is a maximum amount of low-altitude detail a single prompt can productively contain. Beyond this ceiling, additional specificity reduces rather than improves performance.

**The model-capacity interaction.** Larger models tolerate higher altitude better. GPT-4's accuracy jumped from 0.60 to 0.83 with increased specificity, but it also performed reasonably at low specificity (0.60). O3-mini went from 0.34 to 0.68 — a near-doubling — indicating extreme sensitivity to altitude choice [1]. This has practical implications: instructions designed for capable models (Opus) can use higher altitude than instructions designed for efficient models (Haiku). Anthropic explicitly acknowledges this: "What works perfectly for Opus might need more detail for Haiku" [5] (HIGH — T1 + T2 sources converge).

**Atomic decomposition enables consensus reliability.** When plan items are decomposed to atomic, verifiable units, multi-agent consensus achieves exponential error reduction. Five agents with 5% individual error rates achieve 0.116% combined error, outperforming a single agent with 1% error [4]. But this only works when decomposition produces items where "correctness is objectively determinable" — i.e., items at the observable-outcome altitude. Items that require subjective judgment ("make it better") cannot benefit from consensus voting (HIGH — T2 source with formal proofs).

## Challenge

**Primary counter-argument: Fixed altitude per artifact type is too rigid.** The evidence suggests altitude should vary within artifact types, not just between them. A specification for a safety-critical system needs lower altitude (more constraints) than a specification for an exploratory prototype. A plan for a database migration needs lower altitude than a plan for a UI redesign. The altitude framework presented here risks being prescriptive about a variable that should be context-dependent.

**Response:** The framework does not prescribe fixed altitudes but natural ranges. Each artifact type has an altitude where it works best, but the exact altitude within that range depends on (a) the criticality of the task, (b) the model being used, and (c) whether the agent has verification mechanisms. The Anthropic degrees-of-freedom framework already encodes this: "narrow bridge" tasks get low altitude regardless of artifact type, while "open field" tasks get higher altitude [5].

**Second counter-argument: Altitude calibration assumes stable model capabilities.** As models improve, the optimal altitude shifts. Instructions that needed to be low-altitude for GPT-3.5 can be high-altitude for GPT-4. DETAIL Matters [1] shows this directly: GPT-4 compensates for vague prompts while O3-mini cannot. This means altitude recommendations expire with each model generation.

**Response:** This is valid. The framework should be treated as model-relative rather than absolute. The general principle — each artifact type has a natural altitude — is stable. The specific calibration within that altitude requires empirical testing per model, which is why Anthropic recommends testing skills with "Haiku, Sonnet, and Opus" [5].

**Third counter-argument: The specificity research uses synthetic benchmarks, not real agent workflows.** DETAIL Matters tests on math and commonsense reasoning, not on multi-step agentic coding tasks. The Six Sigma Agent tests atomic decomposition, not the kind of fuzzy plan items real developers write. The real-world applicability of these metrics is uncertain.

**Response:** Fair limitation. The controlled studies establish directional principles (specificity helps for procedural tasks, hurts for creative ones; atomic decomposition enables consensus) but the exact thresholds will differ in production agent workflows. The practical evidence from Anthropic [5][6] and GitHub [8] supports the same directional conclusions, providing triangulation from practitioner sources.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | LLMs guess unspecified requirements correctly only 41.1% of the time | statistic | [2] | verified |
| 2 | Unspecified requirements are 2x more likely to regress over model or prompt changes | statistic | [2] | verified |
| 3 | Specifying all 19 requirements reduces GPT-4o accuracy to 85.0% | statistic | [2] | verified |
| 4 | 37.5% of requirements show >5% degradation when many requirements coexist | statistic | [2] | verified |
| 5 | Conditional requirements have only 22.9% guessing accuracy | statistic | [2] | verified |
| 6 | Format requirements are guessed at 70.7% accuracy | statistic | [2] | verified |
| 7 | GPT-4 accuracy improves from 0.60 to 0.83 with increased specificity | statistic | [1] | verified |
| 8 | O3-mini accuracy improves from 0.34 to 0.68 with increased specificity | statistic | [1] | verified |
| 9 | Math tasks show +0.47 accuracy gain from specificity | statistic | [1] | verified |
| 10 | Decision-making tasks show only +0.02 gain from specificity | statistic | [1] | verified |
| 11 | ReCode optimal decomposition depth peaks at 8 (43.22%) on ScienceWorld | statistic | [3] | verified |
| 12 | ReCode achieves 20.9% improvement over best baseline | statistic | [3] | verified |
| 13 | ReCode uses 78.9% fewer tokens than ReAct | statistic | [3] | verified |
| 14 | Five agents with 5% error achieve 0.116% combined error via consensus | statistic | [4] | verified |
| 15 | DSPy separates WHAT (signatures) from HOW (prompting strategies) | attribution | [7] | verified |
| 16 | Copilot Workspace uses spec-plan-implementation three-layer pipeline | attribution | [8] | verified |
| 17 | Anthropic recommends three degrees of freedom: high, medium, low | attribution | [5] | verified |
| 18 | Factory.ai found structured summarization scores 3.70 vs. 3.35 for opaque compression | statistic | existing research | verified |

## Synthesis

The evidence converges on a single organizing principle: **every artifact type has a natural abstraction altitude, and deviating from it in either direction degrades agent execution quality.**

**Specifications** belong at the highest altitude — WHAT the system should do and WHY, never HOW. DSPy validates this architecturally: separating interface from implementation enables automated optimization that outperforms hand-crafted approaches [7]. Copilot Workspace validates this in practice: the specification layer describes current state vs. desired state without mentioning files or functions [8]. The critical caveat from underspecification research: high altitude does not mean low coverage. Specifications must be explicit about constraints, edge cases, and success criteria — they just must not prescribe implementation.

**Plans** belong at middle altitude — observable outcomes that an agent can verify. ReCode's inverted-U curve demonstrates the cost of wrong altitude: too high (insufficient decomposition) and too low (over-fragmentation) both reduce task completion [3]. The Six Sigma decomposition principle establishes what "right altitude" means formally: plan items must be minimal, verifiable, and functionally deterministic [4]. The practical test: can the agent determine whether this plan item is done without asking a human? If yes, it is at the right altitude.

**Research** altitude is calibrated to downstream use. Research informing specifications needs high-altitude findings. Research informing plans needs middle-altitude patterns. Research informing instructions needs low-altitude specifics. The structured-section approach forces appropriate altitude by creating mandatory compartments that each operate at a different level.

**Instructions** are where the specificity curve is most dangerous. The empirical evidence is clear: specificity helps for procedural tasks (+0.47 on math) but barely helps or hurts for inferential tasks (+0.02 on decision-making) [1]. Unspecified requirements regress 2x more, but overspecification degrades performance 15-20% [2]. The resolution is selective specification: specify critical, unstable, hard-to-guess requirements explicitly; leave predictable requirements to model defaults. Anthropic's degrees-of-freedom framework (high/medium/low freedom) operationalizes this by matching instruction altitude to task fragility [5].

**The model-capacity dimension** adds a crucial modifier: larger models tolerate higher altitude. GPT-4 performs reasonably with vague prompts (0.60 accuracy); O3-mini collapses (0.34). Instructions targeting multiple model tiers must be written at the altitude required by the weakest model, or must provide progressive disclosure that smaller models use fully while larger models skim [1][5].

The bottom line: altitude is not a preference but an engineering parameter. Specs say WHAT. Plans say DONE-WHEN. Research says WHAT-WE-KNOW. Instructions say HOW — but only as much HOW as the task demands and the model needs.
