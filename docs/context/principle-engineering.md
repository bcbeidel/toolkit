---
name: "Principle Engineering"
description: "Methods for classifying, verifying, and maintaining design principles as living documents — taxonomy dimensions, fitness functions, drift detection, instruction density limits, and governance lifecycles"
metadata:
  type: reference
  sources:
    - https://arxiv.org/html/2507.11538v1
    - https://www.anthropic.com/news/claudes-constitution
    - https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
    - https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
    - https://continuous-architecture.org/practices/fitness-functions/
    - https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
  related:
    - docs/research/principle-engineering.md
    - docs/context/prompt-engineering.md
    - docs/context/context-window-management.md
    - docs/context/information-architecture.md
---

Design principles drift, conflict, and accumulate. Maintaining them as living
documents requires classification, layered verification, active drift detection,
and respect for instruction density limits.

## Classification Taxonomy

Principles have three independent dimensions that determine where and how they
are enforced:

**Enforcement level.** Mandatory principles produce failing checks on violation
(structural requirements, dependency constraints). Advisory principles produce
warnings and allow exceptions (word count targets, style guidance). This maps to
the `fail` vs `warn` severity distinction in validators.

**Verification method.** Deterministic principles are verifiable by code — unit
tests, linters, CI checks. Judgmental principles require interpretation by
humans or LLMs. This drives the "structure in code, quality in skills" split:
deterministic principles belong in automated checks; judgmental principles
belong in skills and reviews.

**Scope.** Structural principles constrain what exists (files, formats,
dependencies). Behavioral principles constrain how things operate (communication
style, workflow patterns). Structural principles tend to be deterministic and
mandatory; behavioral principles tend to be judgmental and advisory.

These dimensions are orthogonal. A single principle like "single source of
truth" can be structural + mandatory + deterministic for its index-sync check,
yet behavioral + advisory + judgmental for its curation pattern.

## Layered Verification

No single verification method covers all principle types. Three layers form a
defense in depth:

**Fitness functions** handle deterministic principles. Architecture fitness
functions — automated, objective integrity assessments of architectural
characteristics — translate principles into executable checks that run in CI/CD.
WOS validators are a fitness function suite for document architecture. The most
effective fitness functions are atomic (one principle per check), triggered (on
every commit), static (code analysis), and automated (no human intervention).

**LLM-based assessment** handles judgmental principles. Assessment modules
report structural facts (word count, section presence) that models interpret
against judgment criteria encoded in skill instructions. This mirrors
constitutional AI: principles provide the criteria, the model applies
deliberation rather than mechanical rule-following.

**Human review** resolves conflicts between principles and governs principle
evolution. When principles contradict each other or need revision, neither code
nor models are sufficient arbiters.

## Instruction Density Limits

Agent performance degrades with instruction count, following three patterns:
reasoning models (o3, gemini-2.5-pro) maintain near-perfect accuracy through
~150 instructions then decline steeply; linear-decay models (gpt-4.1,
claude-3.7-sonnet) degrade steadily across the spectrum; exponential-decay
models collapse early to 7-15% accuracy floors. At 500 instructions, even the
best models achieve only ~65% accuracy.

Practical implications: target 50-100 active principles for non-reasoning
models, up to 150 for reasoning models. Position critical principles first and
last — primacy effects peak at 150-200 instructions, and mid-document content
falls into the attention dead zone. Beyond ~200 instructions, structural
enforcement (tool-based checks, phase gates) must supplement instruction-based
approaches.

Treat principle sets like dependency lists. Each addition requires
justification. Periodic pruning removes principles that are redundant, implicit
in model behavior, or no longer relevant. An unused principle still consumes
attention budget.

## Drift Detection

Drift — gradual divergence between stated principles and actual implementation —
takes three forms:

**Structural drift** (code diverges from architectural intent): detected by
static conformance checking tools, view-based drift analysis, and runtime
verification. **Semantic drift** (principles no longer reflect practice):
detected by periodic audits, automated coverage analysis (which principles lack
automated checks?), and LLM-based consistency checking. **Instruction drift**
(principles accumulate without pruning): detected by monitoring instruction
count and token volume against known performance thresholds.

## Governance Lifecycle

ADRs and principles serve complementary roles. ADRs capture specific decisions
with context (immutable once accepted, superseded by new ADRs). Principles
capture the recurring reasoning that informs those decisions (persistent,
evolving). A principle like "depend on nothing" generates many ADRs; the
decisions change but the principle persists.

The full lifecycle: proposal (articulate with rationale and verification
criteria), adoption (document immutably with status and consequences),
operationalization (encode as fitness functions or skill instructions),
monitoring (drift detection), evolution (new proposal supersedes original,
preserving the audit trail).

An explicit priority hierarchy — even a simple ordering like safety >
correctness > simplicity > convention — dramatically reduces ambiguity when
principles conflict. Supplement with worked conflict resolution examples for
cases where ordering alone is insufficient.
