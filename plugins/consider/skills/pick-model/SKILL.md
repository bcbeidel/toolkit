---
name: pick-model
description: "Select the right AI model for a task based on external benchmarks, pricing, and effort tradeoffs. Use when the user asks \"which model should I use?\", \"what's the best model for X?\", \"help me pick a model\", \"model comparison\", \"should I use Opus or Sonnet?\", or needs to decide between AI models for a specific workload. Also use when someone mentions cost optimization for LLM usage or wants to know if a cheaper model would work."
argument-hint: "[task or workload to select a model for]"
user-invocable: true
license: MIT
---

<objective>
Recommend the right AI model for a task by routing through three decisions:
what type of work, how much a mistake costs, and what the budget allows.
Recommendations are grounded in external benchmarks — not vendor marketing.
</objective>

<process>
1. **Classify the task type.** Ask what the user is trying to accomplish.
   Decompose broad categories into specific sub-types — "coding" could mean
   function completion (saturated — any model works), bug fixing (Claude/Gemini
   lead), or agentic multi-file refactoring (scaffold matters more than model).
   Read `references/model-landscape.md` for the task-type mapping table.

2. **Assess stakes.** Ask: "What happens if the model gets this wrong?"
   Map to one of three levels:
   - **Exploratory** — brainstorming, throwaway drafts, learning. Mistakes
     are free. Route to budget tier, low effort.
   - **Professional** — real work that matters but is recoverable. Wrong
     answers cost time, not catastrophe. Route to value tier, medium effort.
   - **Critical** — production-facing, high-stakes, expensive to fix.
     Wrong answers have business impact. Route to frontier tier, high effort.

3. **Check cost sensitivity.** Ask if there's a budget constraint:
   - **Unconstrained** — recommend the leader for the task type.
   - **Cost-aware** — recommend the value pick (best quality-per-dollar).
   - **Budget-limited** — recommend the budget pick (cheapest viable).

4. **Apply the crossover check.** Before recommending a cheaper model,
   check: does it score >70% of the frontier on the relevant benchmark?
   If yes, recommend it with high effort. If <50%, skip to frontier.
   Between 50-70%, note the tradeoff explicitly.

5. **Set the effort parameter.** Based on stakes and provider, recommend
   the specific effort setting. Read the effort controls table in
   `references/model-landscape.md`.

6. **Present the recommendation.** Use the output format below. Include
   the primary pick, an alternative at a different price point, the
   effort setting, and a one-line rationale citing the benchmark evidence.
</process>

<output_format>
## Model Recommendation: [Task Description]

### Primary Pick
**[Model Name]** ([Provider]) — [one-line rationale with benchmark cite]
- Cost: $X.XX / $X.XX per M tokens (input/output)
- Effort: `[parameter_name]` = `[value]`

### Alternative
**[Model Name]** — [why this is the tradeoff option]
- Cost: $X.XX / $X.XX per M tokens

### Why This Over That
[2-3 sentences explaining the key differentiator — benchmark evidence,
cost math, or capability gap that drives the recommendation]

### Caveats
- Data as of [month year]. Benchmark rankings shift quarterly.
- [Any task-specific caveats — scaffold matters, score variance, etc.]
</output_format>

<example>
User: "I need to pick a model for our code review pipeline. It reviews
PRs automatically, leaves comments, and sometimes suggests fixes. We
process about 200 PRs a day. Cost matters but quality matters more —
bad reviews erode developer trust."

## Model Recommendation: Automated PR Code Review

### Primary Pick
**Claude Sonnet 4.6** (Anthropic) — SWE-bench Verified 79.6%, Chatbot
Arena Coding ELO 1523. Within 1.2 points of Opus on coding benchmarks
at 60% of the cost.
- Cost: $3.00 / $15.00 per M tokens (input/output)
- Effort: `effort` = `high`

### Alternative
**DeepSeek V3.2** — 73% SWE-bench at $0.26/M input (17x cheaper). For
200 PRs/day, the cost difference is significant. Quality gap is real but
may be acceptable for initial triage before human review.
- Cost: $0.26 / $0.38 per M tokens

### Why This Over That
At 200 PRs/day, the Sonnet-to-Opus upgrade buys 1.2 SWE-bench points
for a 67% price increase — not justified when developer trust depends
on consistency, not peak capability. Sonnet's coding ELO (1523) is third
overall, behind only Opus variants. The DeepSeek alternative is viable
for a two-tier setup: DeepSeek for initial scan, Sonnet for flagged PRs.

### Caveats
- Data as of April 2026. SWE-bench Verified is saturated at the top —
  the 1.2-point Sonnet-to-Opus gap is within noise.
- For agentic PR review (multi-file reasoning, not just line comments),
  agent scaffold quality matters more than model choice — the ~22%
  scaffold effect dwarfs the ~1% model effect at the frontier.
</example>

## Key Instructions

- **Ground every recommendation in external benchmarks.** Cite the
  benchmark name and score. Do not recommend based on vendor marketing,
  model descriptions, or general reputation. Read the benchmark tables
  in `references/model-landscape.md`.
- **Decompose broad task types before recommending.** "Coding" spans
  function completion (saturated), bug fixing (differentiated), and
  agentic workflows (scaffold-dependent). Different sub-types get
  different models. Ask the user to be specific.
- **State the freshness date on every recommendation.** Benchmark data
  is from April 2026. Rankings shift. Say so explicitly.
- **Does not recommend infrastructure, scaffolds, or architectures** —
  produces model selection guidance only. For agentic tasks, note that
  scaffold investment may yield more than model upgrades, but don't
  design the scaffold.
- **Does not make provider-loyalty assumptions.** Recommend across
  providers based on benchmark evidence. A user on Claude may get a
  Gemini recommendation if the benchmarks support it.

## Anti-Pattern Guards

1. **Recommending frontier for everything** — the most expensive model
   is not always the best choice. On saturated benchmarks (function
   completion, simple math), budget models perform equivalently. Cost
   sensitivity matters — a 19x price difference for 1.2 benchmark points
   is rarely justified.
2. **Treating benchmark scores as cardinal** — the same model scores
   2-17 points apart depending on evaluation protocol. Close-margin
   comparisons (e.g., "Opus beats Sonnet by 1.2 points") should be
   presented as ties, not winners. Use ordinal rankings.
3. **Ignoring the scaffold effect** — for agentic coding tasks,
   recommending a model upgrade when the real bottleneck is scaffold
   quality wastes the user's money. Flag this when the task is agentic.
4. **Stale data presented as current** — benchmark landscapes shift
   quarterly. If the user asks about a model or benchmark not in the
   reference data, say so rather than guessing.

## Handoff

**Receives:** A task or workload description the user wants to select a model for; optionally, constraints (budget, provider preference, latency requirements)
**Produces:** A model recommendation with benchmark rationale, effort parameter guidance, cost comparison, and freshness caveat
**Chainable to:** `opportunity-cost` (to analyze what switching models gives up), `pareto` (to find the 20% of workloads driving 80% of model costs)
