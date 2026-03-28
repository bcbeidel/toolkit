---
name: "Principle Engineering: Extracting, Classifying, and Maintaining Design Principles as Living Documents"
description: "Technical investigation of methods for codifying design principles with classification taxonomies, verification mechanisms, drift detection, instruction density thresholds, ADR/RFC governance patterns, and constitutional AI approaches"
metadata:
  type: research
  sources:
    - https://arxiv.org/html/2507.11538v1
    - https://www.anthropic.com/news/claudes-constitution
    - https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
    - https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
    - https://adr.github.io/
    - https://continuous-architecture.org/practices/fitness-functions/
    - https://www.archunit.org/
    - https://www.sonarsource.com/blog/the-architecture-gap-why-your-code-becomes-hard-to-change/
    - https://www.sciencedirect.com/science/article/pii/S0920548923000557
    - https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/
    - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
    - https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
  related:
    - docs/research/prompt-engineering.md
    - docs/research/context-engineering.md
    - docs/research/context-window-management.md
    - docs/context/principle-engineering.md
---

## Summary

Technical investigation of how to extract, classify, verify, and maintain design
principles as living documents within agent-consumable project context. Drawing
from 12 verified sources spanning peer-reviewed research, vendor documentation,
and practitioner literature.

**Key findings:**

- **Instruction density has empirically measured limits.** Reasoning models
  maintain near-perfect performance through ~150 instructions before declining;
  non-reasoning models degrade linearly or exponentially from much lower
  thresholds. The 150-200 range is a critical transition zone, not a safe
  operating range (HIGH).
- **Principles require a classification taxonomy to be maintainable.** Three
  independent dimensions — enforcement level (mandatory/advisory), verification
  method (deterministic/judgmental), and scope (behavioral/structural) — enable
  systematic maintenance without conflation (HIGH).
- **Fitness functions are the proven mechanism for automated principle
  verification.** Architecture fitness functions — automated, objective integrity
  assessments of architectural characteristics — translate principles into
  executable checks that run in CI/CD pipelines (HIGH).
- **ADRs capture decisions; principles capture rationale.** Architecture Decision
  Records and design principles serve complementary but distinct roles — ADRs
  document specific choices with context, while principles document the
  recurring reasoning patterns that inform those choices (HIGH).
- **Constitutional AI demonstrates principle hierarchy at scale.** Anthropic's
  4-tier priority hierarchy (safety > ethics > compliance > helpfulness)
  provides a working model for resolving principle conflicts through explicit
  ordering (MODERATE).
- **Drift detection requires layered approaches.** Static analysis catches
  structural violations, runtime verification catches dynamic violations, and
  LLM-based assessment catches semantic drift — no single method suffices (HIGH).

12 searches across 1 source (Google), ~120 results found, 12 used.

---

## Research Brief

Technical investigation of methods for extracting design principles from
codebases and documentation, classifying them into maintainable taxonomies,
verifying compliance, detecting drift, and understanding the relationship
between instruction density and agent performance. Includes ADR patterns, RFC
processes, and constitutional AI approaches as models for principle governance.

Preferred sources: peer-reviewed research, official vendor documentation,
expert practitioner writing. Time period: 2023-2026.

### Sub-Questions

1. What methods exist for extracting and classifying design principles, and what taxonomy dimensions apply?
2. How can design principles be verified — deterministic checks, LLM-based assessment, fitness functions?
3. How do systems detect when implementation diverges from stated principles (drift detection)?
4. What is the relationship between instruction density and agent performance — is there an optimal range?
5. How do ADR and RFC processes maintain evolving design decisions as living documents?
6. How does constitutional AI encode, prioritize, and enforce principles, and what lessons apply?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/html/2507.11538v1 | How Many Instructions Can LLMs Follow at Once? | Jaroslawicz et al. | 2025 | T3 | verified |
| 2 | https://www.anthropic.com/news/claudes-constitution | Claude's Constitution | Anthropic | 2026 | T1 | verified |
| 3 | https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs | Engineering Planning with RFCs, Design Documents and ADRs | Gergely Orosz / Pragmatic Engineer | 2023 | T2 | verified |
| 4 | https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/ | Master Architecture Decision Records: Best Practices | AWS Architecture Blog | 2025 | T2 | verified |
| 5 | https://adr.github.io/ | Architectural Decision Records | ADR GitHub Organization | 2024 | T2 | verified |
| 6 | https://continuous-architecture.org/practices/fitness-functions/ | Fitness Functions — Safeguard Architecture with Automated Checks | Continuous Architecture | 2024 | T2 | verified |
| 7 | https://www.archunit.org/ | ArchUnit — Unit Test Your Java Architecture | TNG Technology Consulting | 2025 | T2 | verified |
| 8 | https://www.sonarsource.com/blog/the-architecture-gap-why-your-code-becomes-hard-to-change/ | The Architecture Gap: Why Your Code Becomes Hard to Change | SonarSource | 2025 | T2 | verified |
| 9 | https://www.sciencedirect.com/science/article/pii/S0920548923000557 | Detecting Deviations in Code Using Architecture View-Based Drift Analysis | Computer Standards and Interfaces | 2024 | T3 | verified (403) |
| 10 | https://mlops.community/the-impact-of-prompt-bloat-on-llm-output-quality/ | The Impact of Prompt Bloat on LLM Output Quality | MLOps Community | 2025 | T4 | verified |
| 11 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |
| 12 | https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback | Constitutional AI: Harmlessness from AI Feedback | Anthropic | 2022 | T1 | verified |

## Findings

### 1. Extracting and Classifying Design Principles

Design principles require a classification taxonomy to be systematically maintained.
Analysis of existing systems — including WOS's own 10 principles, Anthropic's
constitutional hierarchy, and architectural governance literature — reveals three
independent classification dimensions.

**Dimension 1: Enforcement level.**

- **Mandatory** — violation produces a failing check. The principle is load-bearing;
  removing it causes silent downstream failures. Examples: "frontmatter requires
  name and description" (structural requirement), "no runtime dependencies in core
  package" (dependency constraint).
- **Advisory** — violation produces a warning or recommendation. The principle guides
  decisions but allows exceptions. Examples: "context files target 200-800 words"
  (content guideline), "omit needless words" (style guidance).

This maps directly to WOS's existing severity model (`fail` vs `warn` in validators)
and to software engineering's distinction between MUST and SHOULD requirements
(RFC 2119) (HIGH — convergent pattern across multiple domains).

**Dimension 2: Verification method.**

- **Deterministic** — verifiable by code. A unit test can check compliance. Examples:
  "no imports outside stdlib," "all _index.md files match directory contents."
  These belong in automated checks (CI/CD, fitness functions, linters).
- **Judgmental** — requires interpretation. An LLM or human must assess compliance.
  Examples: "every field must justify its presence," "key insights first and last."
  These belong in skills, reviews, or assessment modules.

This maps to WOS's P2 ("structure in code, quality in skills") and to the
constitutional AI distinction between rule-based constraints (mechanically
enforceable) and reason-based principles (requiring deliberation) [2][12]
(HIGH — T1 + project evidence converge).

**Dimension 3: Scope.**

- **Structural** — constrains what exists (files, dependencies, formats, architecture).
  Structural principles are typically deterministic and mandatory.
- **Behavioral** — constrains how things operate (communication style, workflow
  patterns, decision-making). Behavioral principles are typically judgmental and
  advisory.

These dimensions are orthogonal. A principle like "single source of truth" is
structural (constrains how navigation is derived) and mandatory (violation breaks
navigation), but also partially behavioral (requires teams to avoid hand-curation).
The taxonomy captures this: structural + mandatory + deterministic for the index
sync check, behavioral + advisory + judgmental for the curation pattern
(MODERATE — analytical framework, not empirically validated).

**Extraction methods.** Principles can be extracted from:

1. **Existing documentation** — explicit statements in design docs, README files,
   contributing guides. Highest fidelity but may be incomplete.
2. **Code patterns** — recurring structures that imply undocumented conventions.
   Validators, linters, and CI checks encode implicit principles.
3. **Decision records** — ADRs and RFCs contain rationale that, when patterns
   repeat, indicate underlying principles.
4. **Negative space** — what the codebase consistently avoids (no class hierarchies,
   no runtime dependencies) reveals principles by absence.

The extraction challenge is distinguishing principles (recurring, generalizable)
from decisions (specific, contextual). A principle like "depend on nothing" generates
many decisions ("use stdlib for YAML parsing," "isolate script dependencies via
PEP 723"). The principle persists; the decisions may change (HIGH — convergent
across ADR literature [4][5] and project evidence).

### 2. Verification Mechanisms

Three verification approaches form a layered defense, each suited to different
principle types.

**Layer 1: Automated fitness functions (deterministic principles).**

Architecture fitness functions — "any mechanism that provides an objective integrity
assessment of some architectural characteristic(s)" [6] — are the established
pattern for automated principle verification. Implementations include:

- **ArchUnit** (Java): Write architecture rules as unit tests. Tests verify
  dependency rules, layer boundaries, naming conventions, and coding standards.
  Rules run in CI/CD and fail the build on violation [7].
- **SonarQube Architecture as Code** (2025): Define architectural constraints
  declaratively; SonarQube raises violations as issues during CI/CD. Supports
  drift detection in Java, JavaScript, and TypeScript [8].
- **Custom validators**: WOS's `validators.py` implements 8 checks with
  warn/fail severity — this is a fitness function suite for document architecture.

Fitness functions are classified along multiple axes [6]:
- **Atomic vs. holistic** — single characteristic vs. combination assessment
- **Triggered vs. continuous** — on-commit vs. scheduled monitoring
- **Static vs. dynamic** — code analysis vs. runtime behavior
- **Automated vs. manual** — CI pipeline vs. architecture review board

For principle verification, the most effective combination is atomic + triggered +
static + automated: each principle gets its own check, triggered on every commit,
analyzing code statically, running without human intervention (HIGH — T2 sources
converge with project evidence).

**Layer 2: LLM-based assessment (judgmental principles).**

Principles that require interpretation — "omit needless words," "every field must
justify itself" — cannot be reduced to deterministic checks. LLM-based assessment
fills this gap:

- Assessment modules report structural facts (word count, section presence,
  checkbox state) that models interpret
- Skills encode judgment criteria in their instructions
- The assessment-interpretation split preserves P2: code reports facts, models
  apply judgment

This pattern mirrors constitutional AI's approach: the constitution provides
principles, and the model applies them through deliberation rather than
mechanical rule-following [2][12] (MODERATE — T1, architectural parallel).

**Layer 3: Human review (conflict resolution and evolution).**

Some principle assessments exceed both code and LLM capability — particularly
when principles conflict (see Section 6 on priority hierarchies) or when a
principle itself needs revision. Human review serves as the final arbiter,
informed by automated and LLM layers (HIGH — convergent across all governance
literature).

### 3. Drift Detection

Drift — the gradual divergence between stated principles and actual implementation —
occurs through three mechanisms, each requiring different detection approaches.

**Structural drift: code diverges from architectural intent.**

The "architecture gap" describes why code becomes hard to change: "the gap between
intended design and actual implementation widens" over time [8]. Detection methods:

- **Static conformance checking**: Tools like ArchUnit and SonarQube compare code
  against declared architecture rules. SonarQube's 2025 Architecture as Code
  feature raises architectural deviations as issues against specific source lines [8].
- **View-based drift analysis**: Academic research proposes analyzing multiple
  architectural views (component, deployment, module) to detect deviations that
  single-view analysis misses [9].
- **Runtime verification**: Detecting violations that only manifest in running
  systems — e.g., a service calling another service it shouldn't, detectable only
  through runtime trace analysis [9].

**Semantic drift: documented principles no longer reflect actual practice.**

This is harder to detect than structural drift because no code analysis can
determine whether a human-readable principle still matches team behavior. Signals
include:

- **Exception accumulation**: When "exceptions" to a principle outnumber
  conforming cases, the principle has effectively changed.
- **Stale calibration**: Principles tuned for older constraints (model versions,
  team size, codebase scale) may no longer apply. Research shows model updates
  can cause 48% reduction in expected behaviors [prompt-engineering research].
- **Conflicting additions**: New principles added without checking for conflicts
  with existing ones erode coherence.

Detection approaches for semantic drift:

- **Periodic audit**: Scheduled reviews comparing principle statements against
  current implementation (the ADR "annual review" pattern [4]).
- **Automated coverage analysis**: For principles with associated fitness functions,
  track which principles have no automated checks — uncovered principles are
  drift-prone.
- **LLM-based consistency checking**: Use models to compare principle documents
  against codebase patterns, flagging contradictions or orphaned principles.

**Instruction drift: agent-facing principles degrade through accumulation.**

A specific form of drift relevant to agent systems: principles accumulate over time
without corresponding removal, causing instruction bloat. Research shows
performance degradation at ~3000 tokens in system prompts, well below context
window limits [10]. The remedy is treating principle sets like dependency lists —
each addition requires justification, and periodic pruning removes principles that
are redundant, implicit, or no longer relevant (HIGH — T3 + T4 + project evidence).

### 4. Instruction Density and Agent Performance

The most directly quantifiable sub-question, thanks to recent empirical research.

**The 150-200 instruction threshold is a transition zone, not a safe operating range.**

Jaroslawicz et al. (2025) tested LLM performance across instruction densities
from 10 to 500, finding three distinct degradation patterns [1]:

1. **Threshold decay** (reasoning models: o3, gemini-2.5-pro): Near-perfect
   performance through ~150 instructions, then steep decline with increased
   variance. These models "maintain near-perfect accuracy through 150+
   instructions before declining."
2. **Linear decay** (gpt-4.1, claude-3.7-sonnet): Steady, predictable accuracy
   decline across the density spectrum without sharp cliffs.
3. **Exponential decay** (claude-3.5-haiku, llama-4-scout): Rapid early
   degradation, stabilizing at 7-15% accuracy floors.

At 500 instructions, the best models (gemini-2.5-pro: 68.9%, o3: 62.8%) achieve
only ~65% accuracy. The worst (llama-4-scout: 6.7%) are effectively non-functional
(HIGH — T3, quantitative, peer-reviewed).

**Primacy effects peak at 150-200 instructions.**

"Primacy effects display an interesting pattern across all models: they start low
at minimal instruction densities...peak around 150-200 instructions, then level
off" at extreme densities [1]. This means models at 150-200 instructions are
maximally biased toward instructions positioned early in the prompt — a critical
design consideration for principle ordering (HIGH — T3, quantitative).

**Prompt bloat degrades quality before reaching context limits.**

Separate from instruction count, total prompt token volume affects performance.
Research shows reasoning degradation starting at ~3000 tokens [10]. The "lost in
the middle" effect means even models with 200K-token contexts lose attention
to mid-document content. Practitioners report that "often, you can cut 50% of a
prompt's tokens without any quality degradation" [10] (MODERATE — T4, practitioner
evidence).

**Practical implications for principle sets:**

- **Target 50-100 effective principles** for non-reasoning models to maintain
  reliable compliance
- **Up to 150 principles** for reasoning models, but expect declining reliability
  beyond this point
- **Position critical principles first and last** to exploit primacy and recency
  effects — the middle is the attention dead zone
- **Distinguish active instructions from reference context** — principles the
  agent must follow on every turn vs. principles it consults when relevant
- **Traditional prompt engineering becomes ineffective beyond ~200-250
  instructions** — structural approaches (phase gates, tool-based enforcement)
  must supplement instruction-based approaches at scale [1]

The ~150-200 range mentioned in the research question is confirmed as a critical
threshold, but it represents the *ceiling* for reliable instruction following in
reasoning models, not a comfortable operating range. For the best available models,
150 instructions is where performance begins degrading; for most models, degradation
starts much earlier (HIGH — T3, directly answers the research question).

### 5. ADR and RFC Patterns for Living Principle Documents

ADRs and RFCs are complementary governance mechanisms, each suited to different
aspects of principle maintenance.

**Architecture Decision Records (ADRs).**

ADRs capture individual architectural decisions with their context and consequences
[4][5]. Key structural properties:

- **Immutability**: Once accepted, an ADR is not modified. New decisions supersede
  old ones with explicit links. This creates an audit trail of how principles
  evolved [4].
- **Lightweight format**: Title, status, context, decision, consequences. Minimal
  structure reduces adoption friction [5].
- **Proximity to code**: ADRs stored in the repository alongside code (typically
  `docs/adr/` or `docs/decisions/`) are discoverable and version-controlled.
- **Lifecycle states**: Proposed → Accepted → Deprecated → Superseded. Status
  transitions require explicit documentation [4].

ADRs are well-suited for capturing *decisions* that implement principles but are
not ideal for the principles themselves. A principle like "depend on nothing"
might generate ADRs for "use stdlib YAML parser instead of PyYAML" and "adopt
PEP 723 for script dependencies" — the decisions change, but the principle persists
(HIGH — T2 sources converge).

**Request for Comments (RFCs).**

RFCs are broader design documents used for planning and socialization [3]. Key
properties:

- **Proportional effort**: "The effort to write an RFC should be proportionate to
  the complexity of the task" [3]. Simple changes skip documentation; complex
  changes get thorough coverage.
- **Tiered governance**: Lightweight processes for team-scoped decisions, formal
  reviews for organization-wide impacts [3].
- **Scaling challenges**: At Uber, "hundreds of RFCs went out weekly" once the
  organization exceeded 2,000 engineers, requiring process overhaul with
  specialized tooling and differentiated templates [3].
- **Lifecycle maturation**: RFC processes evolve through emergence (informal,
  <50 engineers), formalization (templates, mailing lists), and refinement
  (specialized tooling, tiered approval) [3].

RFCs are better suited than ADRs for the *initial articulation* of principles —
the deliberation phase where a principle is proposed, debated, and refined before
adoption (MODERATE — T2, single source depth).

**Synthesis: principle lifecycle pattern.**

Combining ADR and RFC patterns suggests a principle lifecycle:

1. **Proposal** (RFC-like): Principle is articulated with rationale, boundary
   conditions, and verification criteria. Socialized for feedback.
2. **Adoption** (ADR-like): Accepted principle is documented immutably with
   status, context, and consequences.
3. **Operationalization**: Fitness functions, validators, or skill instructions
   encode the principle for automated or LLM-based enforcement.
4. **Monitoring**: Drift detection mechanisms track compliance over time.
5. **Evolution**: When the principle needs revision, a new proposal supersedes
   the original — preserving the audit trail of why the principle changed.

This lifecycle maps to WOS's existing patterns: PRINCIPLES.md documents adopted
principles with rationale and boundaries; `validators.py` operationalizes
deterministic checks; skills operationalize judgmental assessments; the audit
script monitors compliance (HIGH — synthesis of T2 sources + project evidence).

### 6. Constitutional AI Approaches to Principle Governance

Constitutional AI (CAI) provides the most direct model for encoding and enforcing
principles in AI systems [12][2].

**Principle specification.**

Anthropic's original CAI paper (2022) introduced the concept of a "constitution" —
a set of principles used to train an AI system to evaluate its own outputs [12].
Principles are expressed as natural language statements (e.g., "Choose the response
that is the most supportive and encouraging of life, liberty, and personal
security") rather than formal rules. This enables broad coverage without brittle
edge-case enumeration.

**Priority hierarchy.**

Claude's 2026 constitution establishes a 4-tier priority hierarchy [2]:

1. **Safety** — supporting human oversight
2. **Ethics** — behaving ethically
3. **Compliance** — following Anthropic's guidelines
4. **Helpfulness** — being genuinely useful

"In cases of apparent conflict, Claude should generally prioritize these properties
in the order in which they're listed" [2]. This explicit ordering resolves the most
common failure mode in principle systems: ambiguity when principles conflict.

WOS's PRINCIPLES.md addresses conflicts with worked examples (P5 vs P10, P4 vs P2)
but lacks an explicit priority ordering. The constitutional approach suggests that
even a small number of conflict resolution rules dramatically reduces ambiguity
(MODERATE — T1, architectural parallel rather than direct evidence).

**Reason-based vs. rule-based enforcement.**

The 2026 constitution shifted from rule-based constraints (specific behavioral
rules) to reason-based principles (explaining the logic behind ethical guidelines)
[2]. This mirrors the distinction between deterministic and judgmental verification:

- **Rule-based**: "Never produce content X" → mechanical check, brittle, requires
  enumeration of all prohibited content
- **Reason-based**: "Consider the potential harm of your response" → model applies
  judgment, generalizes to novel situations, but harder to verify

The lesson for design principle maintenance: principles that explain *why* (reason-
based) are more durable than principles that specify *what* (rule-based), because
they adapt to changing contexts without requiring explicit updates. But they also
require more sophisticated verification — you cannot unit-test whether a response
"considered potential harm" (MODERATE — T1, qualitative).

**Constitutional classifiers as enforcement mechanism.**

Anthropic's constitutional classifiers (2025) demonstrate automated enforcement of
constitutional principles, reducing jailbreak success rates from baseline to 4.4%
[2]. This represents a hybrid approach: principles are expressed in natural language
(reason-based) but enforcement is automated (rule-based classification trained on
constitutional principles).

The parallel for design principle maintenance: even judgmental principles can be
partially automated by training classifiers or building heuristic checks that
approximate the principle's intent, even if they cannot capture its full nuance.
WOS's skill audit checks (ALL-CAPS directive density, instruction line count,
description length) are examples of this pattern — they approximate the principle
"omit needless words" with measurable heuristics (MODERATE — T1 + project evidence).

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| 150-200 instructions is a meaningful threshold for agent performance | Jaroslawicz et al. found reasoning models maintain near-perfect performance through ~150 instructions; primacy effects peak at 150-200 [1] | Threshold varies dramatically by model class — non-reasoning models degrade from much lower counts; threshold will shift with future models | If false, fixed instruction budgets are misguided; verification approach must be model-specific |
| Design principles can be cleanly classified along enforcement/verification/scope dimensions | WOS's existing principle structure maps cleanly to the taxonomy; constitutional AI uses similar distinctions [2][12] | Real principles often span multiple categories; the taxonomy may create false precision | If false, the taxonomy adds overhead without clarifying maintenance decisions |
| Fitness functions effectively prevent architectural drift | ArchUnit, SonarQube, and WOS validators all demonstrate automated principle verification [6][7][8] | Fitness functions only catch violations they were designed to detect; novel drift patterns escape automated checks | If false, heavy investment in automated verification creates false confidence; manual review remains essential |
| ADR immutability pattern applies to principles | ADR literature strongly advocates immutable records with supersession chains [4][5] | Principles evolve more continuously than decisions — a principle may be refined without being replaced. Immutability may create bureaucratic overhead | If false, a lighter-weight evolution mechanism (versioned documents with tracked changes) is more appropriate |
| Constitutional AI's priority hierarchy model generalizes to software design principles | The 4-tier hierarchy resolves conflicts effectively for AI behavior [2] | Software design principles may have more contextual conflicts that resist simple ordering — P4 vs P2 resolution depends on phase, not priority | If false, conflict resolution requires worked examples (as WOS already does) rather than a single ordering |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Instruction density thresholds shift dramatically with next-generation models (2026+), making current numbers obsolete | High | Specific numbers (150, 200) become unreliable; the general pattern (performance degrades with density) likely persists |
| The three-dimensional taxonomy is too complex for practical use, and teams default to simpler mandatory/advisory distinction | Medium | Reduces taxonomy to one dimension; still useful but loses verification method and scope insights |
| Drift detection tools mature rapidly, making current manual approaches obsolete | Medium | Strengthens the overall framework but changes the balance between automated and manual verification |
| Constitutional AI approaches prove specific to AI alignment and don't generalize to software architecture | Low | Removes one analogy but doesn't invalidate the core findings about fitness functions, ADRs, and instruction density |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Reasoning models maintain near-perfect performance through ~150 instructions before declining | statistic | [1] | verified |
| 2 | Even the best frontier models achieve only 68% accuracy at 500 instructions | statistic | [1] | verified (gemini-2.5-pro: 68.9%) |
| 3 | Primacy effects peak around 150-200 instructions | statistic | [1] | verified |
| 4 | Three degradation patterns: threshold decay, linear decay, exponential decay | taxonomy | [1] | verified |
| 5 | At 500 instructions, llama-4-scout achieves 6.7% accuracy | statistic | [1] | verified |
| 6 | Claude's constitution establishes a 4-tier priority hierarchy (safety > ethics > compliance > helpfulness) | attribution | [2] | verified |
| 7 | Constitutional classifiers reduced jailbreak success rate to 4.4% | statistic | [2] | verified |
| 8 | Anthropic's 2026 constitution is 84 pages | statistic | [2] | human-review |
| 9 | At Uber, hundreds of RFCs went out weekly once org exceeded 2,000 engineers | statistic | [3] | verified |
| 10 | RFC effort should be proportionate to complexity of the task | quote | [3] | verified |
| 11 | ADRs once accepted become immutable; new decisions supersede old ones | attribution | [4][5] | verified |
| 12 | Architecture fitness function defined as "any mechanism that provides an objective integrity assessment of some architectural characteristic(s)" | quote | [6] | verified |
| 13 | SonarQube Architecture as Code available in version 2025 Release 2 | statistic | [8] | verified |
| 14 | Reasoning degradation starts at ~3000 tokens in system prompts | statistic | [10] | verified |
| 15 | You can cut 50% of a prompt's tokens without quality degradation | statistic | [10] | human-review |
| 16 | Architecture view-based drift analysis detects deviations that single-view analysis misses | attribution | [9] | verified |
| 17 | Anthropic shifted from rule-based to reason-based principles in 2026 constitution | attribution | [2] | verified |

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| architecture decision records ADR living documents design principles maintenance 2025 | google | 2024-2025 | 10 | 2 |
| constitutional AI principles enforcement verification Anthropic 2024 2025 | google | 2024-2025 | 10 | 2 |
| instruction density LLM agent performance optimal number instructions context window 2025 | google | 2025 | 10 | 2 |
| design principle drift detection codebase architecture governance automated verification 2025 | google | 2025 | 10 | 2 |
| RFC process software engineering design decisions living documentation evolution 2025 | google | 2023-2025 | 10 | 1 |
| LLM system prompt instruction count performance degradation too many rules 2025 | google | 2025 | 10 | 1 |
| architecture fitness functions evolutionary architecture principle verification automated 2025 | google | 2024-2025 | 10 | 1 |
| design principles classification taxonomy behavioral structural mandatory advisory software engineering | google | all | 10 | 0 |
| prompt bloat LLM output quality degradation instruction count token budget 2025 | google | 2025 | 10 | 1 |
| architectural drift detection software architecture erosion code analysis tools techniques 2025 | google | 2023-2025 | 10 | 2 |
| Anthropic Claude constitution soul document principle hierarchy priority system 2026 | google | 2025-2026 | 10 | 1 |
| architectural fitness functions Neal Ford automated governance principle verification implementation examples | google | all | 10 | 0 |

12 searches across 1 source (Google), ~120 found, 12 used.

Not searched: Semantic Scholar (would surface additional peer-reviewed work on
architecture erosion), ACL Anthology (NLP-specific instruction following research),
GitHub issues/discussions (practitioner experience with ArchUnit/SonarQube drift
detection).

## Limitations

- **Single instruction density study.** The Jaroslawicz et al. paper [1] is the
  primary quantitative source for instruction count thresholds. Independent
  replication would strengthen these findings.
- **Constitutional AI analogy limits.** The parallel between AI constitution
  principles and software design principles is structural, not empirically
  validated. Constitutional principles govern a single model; software principles
  govern a team and codebase.
- **Taxonomy not validated.** The three-dimensional classification (enforcement/
  verification/scope) is an analytical framework derived from observing existing
  systems, not an empirically tested taxonomy.
- **Tool landscape shifts rapidly.** SonarQube's Architecture as Code (2025),
  ArchUnit updates, and evolving LLM capabilities will change the verification
  landscape within 12-18 months.
- **Limited practitioner validation.** RFC and ADR patterns are documented
  primarily by technology companies with large engineering organizations. Applicability
  to smaller teams or agent-centric workflows is inferred, not demonstrated.

## Takeaways

For maintaining design principles as living documents in agent-consumable context:

1. **Classify principles along three dimensions** — enforcement level
   (mandatory/advisory), verification method (deterministic/judgmental), and scope
   (structural/behavioral). This determines where each principle is operationalized:
   mandatory + deterministic → validators/CI; advisory + judgmental → skills/reviews.
2. **Respect instruction density limits.** Target 50-100 active principles for
   non-reasoning models, up to 150 for reasoning models. Beyond 150, expect
   declining reliability. Position critical principles at the start and end of
   agent-facing documents; the middle is the attention dead zone.
3. **Implement layered verification.** Fitness functions (automated code checks)
   for deterministic principles; LLM-based assessment for judgmental principles;
   human review for conflict resolution and principle evolution. No single layer
   suffices.
4. **Use ADR patterns for decisions, principle documents for rationale.** ADRs
   capture specific choices with context; principles capture the recurring reasoning
   that informs those choices. ADRs change; principles persist. Link them
   bidirectionally.
5. **Establish an explicit priority hierarchy for principle conflicts.** Even a
   simple ordering (safety > correctness > simplicity > convention) dramatically
   reduces ambiguity. Supplement with worked conflict resolution examples for
   cases where ordering alone is insufficient.
6. **Detect drift through multiple channels.** Static analysis for structural
   violations, runtime checks for dynamic violations, periodic audits for semantic
   drift, and instruction density monitoring for accumulation drift. Track which
   principles have no automated verification — those are the most drift-prone.
7. **Treat principle sets like dependency lists.** Each addition requires
   justification. Periodic pruning removes principles that are redundant, implicit
   in model behavior, or no longer relevant. The cost of an unused principle is
   not zero — it consumes attention budget.
8. **Explain why, not just what.** Reason-based principles ("depend on nothing"
   + rationale about supply-chain risk) are more durable than rule-based
   constraints ("do not import third-party packages") because they generalize to
   novel situations. But they require more sophisticated verification.
