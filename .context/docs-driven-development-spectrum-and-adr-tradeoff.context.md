---
name: Docs-Driven Development — Spectrum and ADR Tradeoff
description: DDD is a spectrum from Spec-First to Spec-as-Source; ADRs are the high-confidence lightweight alternative delivering organizational memory without the full synchronization burden.
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/html/2602.00180v1
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://tom.preston-werner.com/2010/08/23/readme-driven-development
  - https://abseil.io/resources/swe-book/html/ch10.html
related:
  - docs/context/docs-as-constitutional-constraints-on-llm-generation.context.md
  - docs/context/design-spec-as-tradeoff-document.context.md
  - docs/context/specification-format-taxonomy-adr-rfc-sdd.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
---
# Docs-Driven Development — Spectrum and ADR Tradeoff

Documentation-Driven Development (DDD) is writing documentation before the corresponding implementation. The spectrum ranges from a single README to executable specifications where tests fail if code diverges. The form factor determines the overhead and synchronization burden.

## Three Adoption Levels

**Spec-First** — write documentation for initial clarity only. No ongoing synchronization requirement. Documentation captures intent at design time; code may diverge during implementation. Lowest overhead; highest portability to iterative teams.

**Spec-Anchored** — documentation is maintained alongside code throughout the lifecycle. Captures design decisions as they evolve. Requires co-location in the same repository and PR-gated updates to prevent drift. Google's SWE Book is the canonical reference: documentation placed under source control, given clear ownership, reviewed alongside code changes.

**Spec-as-Source** — the specification is the only artifact humans edit; code is fully generated or verified against it. Tests fail if code diverges from the spec. The highest overhead level; currently emerging in AI-assisted development contexts where LLMs generate implementation from specifications.

## Evidence for Effectiveness

The primary evidence is qualitative, not quantitative. Canonical's year-long DDD adoption report: design documentation forced decisions to be explicit early, caught an identity-management incompatibility before implementation, and improved design clarity across the team. Google's design docs: most valuable "when design uncertainty is significant" and when cross-cutting concerns (security, privacy, observability) need explicit consideration.

The 50% error reduction figure from an arXiv preprint (2025) frames a ceiling from two industry blog posts, not a typical result — no independent replication exists. Apply as directional evidence only.

**Counter-evidence to note:** Marmelab (2025) found spec-first in AI-assisted contexts produced ~4x overhead (2,577 lines of markdown for 689 lines of code) with no quality improvement versus iterative prompting. The benefit is selection-sensitive: it applies in coordination-heavy, design-uncertain contexts and may be absent or inverted in exploratory or maintenance work.

## ADRs as High-Confidence Lightweight Alternative

Architecture Decision Records (ADRs) capture a single architectural decision with: context, problem statement, trade-offs considered, serious alternatives with pros/cons, explicit consequences, confidence level, and triggers for re-evaluation.

Key properties that make ADRs high-confidence:
- **Never modified after acceptance** — an accepted ADR is superseded by a new ADR, never edited in place. This provides immutable audit trail without ongoing maintenance.
- **Versioned alongside code** in `doc/adr/` — same lifecycle as the code they describe
- **Narrow scope** — one decision per document; no synchronization with implementation details
- **Progressive lifecycle** — Proposed → Accepted → Superseded; state is always clear

ADRs provide the primary organizational memory benefit of DDD — capturing the "why" behind decisions, preventing repeated relitigating of settled questions — without requiring full documentation synchronization. "The act of writing them helps to clarify thinking, particularly with groups of people."

**The tradeoff:** DDD captures intent before code; ADRs capture rationale after decision. For teams where spec-first overhead is prohibitive, ADRs are the minimum viable documentation discipline that still delivers organizational memory.

**The takeaway:** Match the DDD level to team size, coordination cost, and design uncertainty. Spec-First is the low-risk entry point. ADRs are the default recommendation for most teams — they deliver the cognitive benefit of writing down decisions without ongoing synchronization liability.
