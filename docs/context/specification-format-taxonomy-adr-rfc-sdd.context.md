---
name: "Specification Format Taxonomy — ADR, RFC, Design Doc, SDD"
description: "ADRs, RFCs, design docs, and SDDs serve distinct purposes — format choice depends on scope, audience, and whether the goal is recording a decision vs. building cross-team consensus."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
  - https://candost.blog/adrs-rfcs-differences-when-which/
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://github.com/github/spec-kit/blob/main/spec-driven.md
  - https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices
  - https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
related:
  - docs/context/design-spec-as-tradeoff-document.context.md
  - docs/context/diverge-converge-design-mode-switching.context.md
  - docs/context/mental-models-software-decisions-practitioner-vs-empirical.context.md
---
# Specification Format Taxonomy — ADR, RFC, Design Doc, SDD

## Key Insight

Four formats serve distinct purposes. Choosing the wrong format for a decision scope creates failure modes: RFCs without decision-owners stall permanently; ADRs used for cross-team decisions lack buy-in; design docs used for team-scoped decisions generate overhead without value. Format choice is the first decision.

## The Four Formats

**Architecture Decision Record (ADR)**

- Scope: team-scoped, single architectural decision
- Length: 1–2 pages; inverted pyramid — decision first, context after
- Status lifecycle: proposed → accepted → superseded (never reopened)
- Storage: source repo, near the code it concerns
- Key rule: "Once an ADR is accepted, it should never be reopened or changed — instead it should be superseded."
- Best for: decisions executable within the team, no external buy-in required
- Confidence: HIGH (Martin Fowler, who popularized ADRs, is the primary source)

**Request for Comments (RFC)**

- Scope: cross-team impact, requires broad buy-in before decision
- Structure: Abstract, Architecture changes, Dependencies, Performance, Security, Rollout, Monitoring
- Known failure mode: RFC processes without an explicit decision step default to "no" through inertia — discussions never conclude
- Scale failure: Uber at 2,000+ engineers produced "hundreds of RFCs weekly," creating reviewer overload
- Rule: only use RFC when cross-team buy-in is required AND a decision-owner is assigned
- Confidence: MODERATE — T4 sources support the format; failure modes are well-documented

**Design Document (tech spec)**

- Scope: new systems, major features, or anything requiring trade-off exploration
- Length: 5–20 pages for larger projects; 1–10 pages for most work
- Sections: Context/Scope, Goals/Non-goals, Design options, Alternatives Considered, Appendices
- Function: not a decision record — explores the problem space before deciding
- For small features, functional and technical spec can merge into one document
- Confidence: HIGH (Google, widely cited)

**Spec-First / SDD Artifact (2025)**

- Scope: behavior-oriented specification written before AI-generated code
- Six essential areas (from GitHub analysis of 2,500+ agent configuration files): Commands with full flags, Testing frameworks and locations, Project structure, Code style with examples, Git workflow, Boundaries (what agents should never touch)
- Built for AI agent consumption, not team communication
- Confidence: LOW to MODERATE — GitHub and Thoughtworks endorse it; significant counter-evidence that agents frequently ignore spec instructions; "curse of instructions" research shows performance drops under many simultaneous requirements

## Format Selection Rules

- Change affects multiple teams → RFC (assign a decision-owner or it will stall)
- Team-scoped architectural decision → ADR
- New system or major feature requiring trade-off exploration → Design doc
- AI code generation task → SDD artifact (treat as promising, not proven)
- Small, clear, reversible change → no document; make the change

## Scale and Taxonomy Erosion

The clean format taxonomy erodes under organizational pressure. Uber introduced lightweight and heavyweight template variants as team count grew. No format stays clean at scale without active process maintenance. For teams under ~20 engineers, spec and plan may reasonably merge into a single design document — the clean separation is primarily validated for large organizations.

## The Spec/Plan Boundary

A specification defines WHAT the system does and under what conditions. A plan describes HOW it will be built. "The specification should not bias the design; premature HOW thinking makes requirements harder to validate and limits design space." This distinction is most valuable for large cross-functional teams; small teams often merge both into a single document without loss.

## Takeaway

Match format to scope before writing. RFCs without decision-owners stall. ADRs supersede rather than amend. Design docs explore trade-offs — if they don't, they should have been code. SDD artifacts are an active experiment, not a proven practice. For most changes at teams under 20, the correct format is no document.
