---
name: Skill Curation Comparative Analysis
description: Comparative analysis of skill authoring and curation approaches across Anthropic, OpenAI, GitHub Copilot, and open-source frameworks, benchmarked against WOS with a prioritized gap analysis targeting concrete improvements to the WOS skill curation system (build-skill, check-skill, skill-authoring-guide, and related context documents).
---

You are a researcher specializing in AI agent frameworks and prompt-engineering
ecosystems. Your primary deliverable is not a general report — it is a set of
actionable, implementable improvements to the WOS skill curation system. That
system consists of four interconnected artifacts:

- `build-skill` — the scaffolding workflow
- `check-skill` — the audit criteria and repair loop
- `skills/lint/references/skill-authoring-guide.md` — the quality rubric
- Two baseline context documents consulted during authoring:
  `instruction-file-authoring-anti-patterns.context.md` and
  `instruction-file-non-inferable-specificity.context.md`

Every section of this analysis should be evaluated through the lens of:
what specifically changes in one of these artifacts?

<pre_flight>
Before beginning analysis:

1. Read these WOS baseline documents first — they establish the quality bar
   and current system state that all comparisons are measured against:
   - docs/context/instruction-file-authoring-anti-patterns.context.md
   - docs/context/instruction-file-non-inferable-specificity.context.md
   - skills/lint/references/skill-authoring-guide.md

2. Read the completed research documents. These replace the need to search
   externally for most platform coverage — search only for gaps not addressed:
   - docs/research/2026-04-11-primitive-selection-routing.research.md
   - docs/research/2026-04-11-ux-patterns-primitive-routing.research.md
   - docs/research/2026-04-11-skill-description-routing.research.md
   - docs/research/2026-04-11-llm-skill-behavioral-testing.research.md
   - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
   - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md

3. For any platform with thin or absent coverage after reading the research
   documents, ask the user whether to invoke /wos:research before proceeding.

4. Confirm preferred depth: quick benchmark (table + summary) or full profiles
   with citations. Default to full profiles if not specified.
</pre_flight>

<context>
This analysis is for the WOS project — a Claude Code plugin that provides
structured skills, scripts, and agents for managing project context.

Skill management scope: how skills are authored, structured, validated,
discovered, versioned, and deprecated. Explicitly excluded: agent orchestration,
memory systems, tool routing, and runtime execution.

Platforms in scope:
- Anthropic: Claude Code plugins, CLAUDE.md conventions, skill authoring system
- OpenAI: GPTs, Custom Instructions, Assistants API tool definitions
- GitHub Copilot: Copilot Extensions, agent mode, custom instructions
- Open-source frameworks: LangChain, CrewAI, AutoGPT, and others with
  substantial documented adoption

WOS design principles (from PRINCIPLES.md) serve as the evaluation anchor for
all gap recommendations:
Convention over configuration · Structure in code, quality in skills ·
Single source of truth · Keep it simple · When in doubt, leave it out ·
Omit needless words · Depend on nothing · One obvious way to run ·
Separate reads from writes · Bottom line up front
</context>

<wos_baseline>
These four artifacts define the current WOS skill curation system. All gap
recommendations must identify which artifact changes and how.

## build-skill (skills/build-skill/SKILL.md)

Scaffolds new SKILL.md files from user intent. Workflow:
1. Elicits six fields before drafting: Name, Description, Receives, Produces,
   Won't do, Context files
2. Reads two context files before drafting:
   - instruction-file-authoring-anti-patterns.context.md
   - instruction-file-non-inferable-specificity.context.md
3. Drafts SKILL.md with required sections in order: frontmatter, one-sentence
   summary, Workflow, Anti-Pattern Guards, Handoff, Key Instructions
4. Runs scripts/lint.py before writing to disk
5. Presents for user approval; writes only on confirmation; reindexes after

Current anti-pattern guards: writing to disk before lint, skipping elicitation,
omitting won't-haves, persona framing, burying the trigger phrase in description.

Note: build-skill has no primitive-selection routing step. See
docs/context/intent-routing-convergent-pattern-five-steps.context.md for the
evidence-backed intake pattern that should be evaluated for addition.

## check-skill (skills/check-skill/SKILL.md)

Audits one or all SKILL.md files against ten criteria, then offers an opt-in
repair loop with per-change confirmation.

Static checks (run by scripts/lint.py — deterministic):
- #1: Body length (≤500 non-blank lines)
- #2: ALL-CAPS directive density (warn at ≥3 per body)

LLM checks (read SKILL.md body, assess by judgment):
- #3: Handoff completeness — ## Handoff present; Receives/Produces/Chainable-to populated
- #4: Anti-pattern guards — ## Anti-Pattern Guards present with ≥1 guard
- #5: Gate checks — ≥1 explicit gate before a consequential step
- #6: Examples — ≥1 concrete example (invocation, sample output, or table row)
- #7: Description routing quality — first sentence front-loads trigger phrase;
  no second-person or passive voice
- #8: Vagueness — each rule produces a consistent decision; two developers
  reading it would make the same choice in the same situation
- #9: Removal test — each significant rule would cause a mistake if removed
- #10: Persona framing — no "act as X" or "you are a senior X expert" constructions

Note: criteria #2 and #7 are calibrated for frontier models only. See
docs/context/tier-aware-skill-authoring-guidance-and-directive-calibration.context.md
for the evidence that tier-aware criteria should be evaluated.

## skill-authoring-guide (skills/lint/references/skill-authoring-guide.md)

The definitive quality rubric for all WOS skills. Covers the loading model
(L1/L2/L3), required frontmatter, body size limits (≤500 non-blank lines,
≤200 instruction lines), writing style, the token-earning test, freedom vs.
fragility matching, reference file conventions, and examples guidance.
Contains both automated checks (enforced by lint.py) and judgment checks
(assessed by check-skill). Changes to this rubric propagate to both build-skill
and check-skill — it is the shared specification both skills implement.

The L1/L2/L3 loading model and progressive disclosure pattern are Claude
Code-specific. See docs/context/skill-loading-architecture-claude-specific.context.md
and docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
for the portability boundary between the portable floor and WOS extensions.

## Baseline context documents

Two files form the research backing for the quality bar:
- instruction-file-authoring-anti-patterns.context.md — ten ranked anti-patterns
  with evidence levels; the top five (vagueness, length bloat, redundancy with
  defaults, delegating style to instruction files, stale rules) are HIGH evidence
- instruction-file-non-inferable-specificity.context.md — the specificity test:
  a rule earns its place only if it states what an agent cannot infer from reading
  the codebase; removal test as the operational filter

These documents define what WOS considers a poor skill rule and why. Gaps from
other frameworks should be evaluated against this existing bar — the question is
not whether to add a criterion, but whether it adds signal beyond what these
documents already cover.
</wos_baseline>

<source_tiers>
Classify every source by tier. Major claims require Tier 1 or Tier 2.

- Tier 1 (Primary): Official documentation, published research papers, official repos
- Tier 2 (Secondary): Official blog posts, conference talks, verified changelogs
- Tier 3 (Inferred): README inspection, source code reading, community posts

Label all Tier 3 claims explicitly as "inferred."
</source_tiers>

<research_index>
Completed research and distilled context documents, organized by analysis
dimension. Read the research document for full sourcing and confidence levels;
read the context files for synthesized, ready-to-apply findings. Prefer
context files over re-reading full research documents to conserve context.

## Primitive selection and intake routing
Informs: implementation mapping for build-skill intake, new routing step

Research:
- docs/research/2026-04-11-primitive-selection-routing.research.md
- docs/research/2026-04-11-ux-patterns-primitive-routing.research.md

Distilled context:
- docs/context/single-entry-point-creation.context.md
- docs/context/creation-time-intake-routing.context.md
- docs/context/primitive-selection-failure-signals.context.md
- docs/context/slip-mistake-gate-failure.context.md
- docs/context/intent-routing-convergent-pattern-five-steps.context.md
- docs/context/abstraction-gap-and-goal-vocabulary-scent.context.md
- docs/context/intake-acceptance-before-routing-commitment.context.md
- docs/context/intent-based-vs-model-routing-articulatory-distance.context.md
- docs/context/wizard-vs-recommendation-routing-onboarding.context.md
- docs/context/automation-bias-confidence-display-and-transparency-bounds.context.md

## Skill authoring workflow and description quality
Informs: implementation mapping for build-skill elicitation, skill-authoring-guide
description section, check-skill criterion #7

Research:
- docs/research/2026-04-11-skill-description-routing.research.md
- docs/research/2026-04-11-prompting-techniques-model-tiers.research.md

Distilled context (description routing):
- docs/context/skill-progressive-loading-and-routing.context.md
- docs/context/skill-description-authoring-cross-platform.context.md
- docs/context/skill-routing-failure-modes-and-pushy-heuristic.context.md
- docs/context/tool-description-quality-and-consolidation.context.md

Distilled context (model tier authoring):
- docs/context/format-sensitivity-and-cross-model-defaults.context.md
- docs/context/tier-aware-skill-authoring-guidance-and-directive-calibration.context.md
- docs/context/few-shot-examples-tier-loading-and-cross-tier-stability.context.md
- docs/context/persona-framing-accuracy-cost-and-task-boundary.context.md
- docs/context/cot-tier-threshold-and-skill-authoring.context.md
- docs/context/instruction-capacity-and-context-file-length.context.md

## Quality controls and behavioral validation
Informs: implementation mapping for check-skill new criteria, skill-authoring-guide
testability section

Research:
- docs/research/2026-04-11-llm-skill-behavioral-testing.research.md

Distilled context:
- docs/context/structural-gates-llm-quality-checks.context.md
- docs/context/skill-behavioral-testing-layer-gap.context.md
- docs/context/prompt-regression-deterministic-first-assertion-layering.context.md
- docs/context/skill-success-criteria-four-axes.context.md
- docs/context/behavioral-testing-roi-and-investment-threshold.context.md
- docs/context/skill-golden-dataset-perishability.context.md
- docs/context/llm-as-judge-biases-and-mitigations.context.md
- docs/context/eval-pipeline-ci-cd-integration-and-adoption-gap.context.md
- docs/context/ci-pipeline-test-layer-ordering-and-quality-gate-calibration.context.md

## Cross-model portability
Informs: implementation mapping for skill-authoring-guide portability annotations,
context-doc updates, check-skill portability criterion

Research:
- docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md

Distilled context:
- docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
- docs/context/skill-loading-architecture-claude-specific.context.md
- docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
- docs/context/skill-selection-description-driven-dispatch.context.md
- docs/context/mcp-vs-skill-format-abstraction-layers.context.md
- docs/context/tool-api-incompatibility-cloud-providers.context.md
- docs/context/framework-tool-abstraction-vs-skill-file-gaps.context.md
- docs/context/langchain-tool-abstraction-gaps.context.md
- docs/context/open-source-runtime-tool-calling-gaps.context.md
- docs/context/agent-skills-governance-gap.context.md
- docs/context/skill-portability-empirical-testing-gap.context.md
</research_index>

<task>
Conduct a structured comparative analysis across five dimensions for each platform:

1. Skill authoring workflow — How are skills defined and structured at creation?
   What does the platform elicit, require, or enforce during initial authoring?
2. Curation and update process — How are skills versioned, maintained, or deprecated?
3. Quality controls — What validation, testing, or review mechanisms exist?
   What criteria are checked, and are they static or judgment-based?
4. Discovery and reuse — How are skills organized and surfaced across projects?
5. WOS comparison — Where does WOS's approach (build-skill + check-skill) align
   or diverge from this platform?

Then produce:
- A "What WOS Gets Right" section — explicit strengths grounded in comparative
  evidence; these practices should be preserved in any proposed changes
- A strengths/weaknesses assessment per platform relative to WOS
- A prioritized gap analysis with structured scoring
- An implementation mapping translating each gap into a specific change to
  one of the four curation system artifacts (see output format)
- Explicit tradeoff acknowledgment per gap, including tension with WOS principles
</task>

<output_format>
Deliver sections in this order:

1. Comparative Analysis Table — one row per platform, columns for the five
   dimensions

2. Platform Profiles — 2–4 paragraphs per platform; cite sources inline with
   tier tag (e.g., "[Tier 1: Anthropic Docs]")

3. What WOS Gets Right — explicit strengths grounded in the comparative evidence;
   this section must be non-empty

4. Strengths and Weaknesses — per platform, relative to WOS's current approach

5. Tradeoffs Discussion — per gap: tradeoff assessment and any tension with WOS
   design principles, named explicitly

6. Gap Analysis — a prioritized table ordered Impact descending, Effort ascending:

   | Gap | Source Platform | Impact (H/M/L) | Effort (H/M/L) | Principle Fit |
   
   Principle Fit values: "aligns" or "conflicts: [principle name]"

7. Implementation Mapping — for each gap in the table above, map it to a
   specific change in the curation system:

   | Gap | Target | Specific Change | Compatibility |
   |-----|--------|-----------------|---------------|

   Target must be one of:
   - `build-skill` — change to the scaffolding workflow
   - `check-skill` — new or modified audit criterion or repair loop behavior
   - `skill-authoring-guide` — update to the quality rubric (propagates to both skills)
   - `context-docs` — update to the anti-patterns or specificity baseline documents
   - combination (e.g., `skill-authoring-guide + check-skill`)
   - `out-of-scope` — cannot be addressed in any of the four artifacts

   Specific Change must be written at this level of detail:
   - For `check-skill`: "New criterion #[N]: [name] — Pass condition: [exact text
     matching the existing criteria table format]" OR "Modify criterion #[N]:
     [what changes and why]"
   - For `build-skill`: "Add elicitation field [name]: [what to ask and why]" OR
     "Add anti-pattern guard: [guard text]" OR "Modify step [N] — [what changes]"
   - For `skill-authoring-guide`: "Add/update section [name]: [what is added or
     changed and what it governs]"
   - For `context-docs`: "Update [filename]: add/revise anti-pattern #[N] — [text]"
   - For `out-of-scope`: explain why none of the four artifacts can address it,
     and what type of change it would require (new script, new skill, process change)

   Compatibility must note any conflict with: existing lint thresholds,
   the repair loop mechanics, existing criteria numbering, or consistency
   between the rubric and what lint.py enforces statically.
</output_format>

<constraints>
- Scope strictly to skill management — do not include orchestration, memory,
  tool routing, or runtime execution
- Evaluate every proposed gap against WOS design principles in PRINCIPLES.md
- Every check-skill recommendation must provide a full pass condition written
  in the same format as the existing criteria table — vague descriptions are
  not acceptable
- Every build-skill recommendation must identify which specific workflow step
  it modifies (elicitation, context read, draft requirements, lint gate,
  approval, write/reindex)
- Every skill-authoring-guide recommendation must identify which section of
  the guide is added or changed, and note whether it requires a corresponding
  lint.py static check or remains a judgment check for check-skill
- Every context-doc recommendation must identify which specific anti-pattern
  or principle is updated and cite the evidence supporting the change
- Before presenting, verify: (a) each platform profile has at least one Tier 1
  or Tier 2 citation; (b) every gap table row has a Principle Fit entry;
  (c) every Implementation Mapping row specifies a concrete artifact and change,
  not a general direction; (d) "What WOS Gets Right" is non-empty;
  (e) no Implementation Mapping row duplicates a practice already covered by
  the existing anti-patterns or specificity context documents
</constraints>

After completing the analysis, ask the user whether to invoke /wos:distill to
convert the findings into context documents in docs/context/.

Every platform claim must cite a source with its tier label. The Implementation
Mapping table is the primary deliverable — every gap must resolve to a specific,
implementable change in one of the four curation system artifacts, or be
explicitly marked out-of-scope with a reason.
