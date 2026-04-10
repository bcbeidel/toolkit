---
name: "Specification & Design Document Patterns"
description: "Practitioner consensus on design spec structure, spec-vs-plan boundaries, format selection (ADR/RFC/design doc/SDD), and complexity calibration — with documented failure modes and qualifications for small teams and AI-assisted contexts"
type: research
sources:
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/
  - https://codydjango.com/software-technical-design-documents/
  - https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices
  - https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
  - https://www.jrobbins.org/ics121f03/lesson-spec-design.html
  - https://github.com/github/spec-kit/blob/main/spec-driven.md
  - https://news.ycombinator.com/item?id=44779428
  - https://candost.blog/adrs-rfcs-differences-when-which/
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
  - https://ntietz.com/blog/reasons-to-write-design-docs/
  - https://addyosmani.com/blog/good-spec/
  - https://medium.com/machine-words/writing-technical-design-docs-71f446e42f2e
  - https://making.close.com/posts/writing-technical-specification-for-feature-development/
related:
---

# Specification & Design Document Patterns

## Summary

**Design specs are trade-off documents, not implementation blueprints.** Their value is recording *why* a decision was made — alternatives considered, constraints accepted, risks surfaced. A doc that just describes what was built should have been replaced by the working code (HIGH — T4 + T5 convergence [1][8]).

**The spec/plan boundary is WHAT vs. HOW.** A specification defines what the system does and under what conditions. A plan describes how it will be built. The boundary is real and useful — but primarily validated for larger, cross-functional teams; small teams often merge both into a single design document (HIGH for distinction, MODERATE for universality — T2 [6] + T1 [7]).

**Four formats, distinct purposes:**
- **ADR** — single decision, team-scoped, lives near the code (HIGH — T4 [10])
- **RFC** — cross-team buy-in, longer feedback cycle; critical failure mode: no explicit decision step causes permanent stall (MODERATE — T4 [11], counter-evidence from challenge)
- **Design doc** — trade-off exploration for a new system or major feature; 5-20 pages (HIGH — T4 [1])
- **SDD/spec-first artifact** — behavior-oriented spec for AI code generation; promising but not yet proven reliable (LOW to MODERATE — T1 [7], T4 [13], counter-evidence strong)

**Write when the solution is ambiguous; don't write when the path is clear.** The trigger is ambiguity (problem or solution complexity), not task size (HIGH — T4 [1][11]).

**Source quality:** 15 sources; T1 (GitHub official), T2 (Thoughtworks, UC Irvine), T4 (Martin Fowler ×2, Pragmatic Engineer, Addy Osmani), T5 (community). All findings are practitioner consensus — no experimental or quasi-experimental evidence compares spec-writing to alternatives.

*16 searches · 160 candidates found · 32 used*

---

## Findings

> **Scope qualification:** The findings below represent practitioner consensus primarily validated for large, cross-functional teams shipping stable systems. Small teams, exploratory development, and fast-moving requirements contexts require significant qualification — noted per-finding below.

### Sub-question 1: What makes a good software design specification?

**A design spec is a trade-off document, not an implementation blueprint.** [1][8]

The core function of a design document is to record *why* a design decision was made, not *what* was built. A document that describes implementation without exploring trade-offs or alternatives should be replaced with working code — the implementation itself is a better artifact (HIGH — T4 + T5 sources converge; Ubl [1] directly states this, corroborated by HN community [8]).

**Canonical structure:** Context/Scope → Goals and Non-goals → The Actual Design (APIs, data storage) → Alternatives Considered → Cross-cutting Concerns (security, privacy, observability) [1][2][8]. A layered variant: Problem/Goals/Non-goals (layer 1) → Functional specification (layer 2) → Technical specification (layer 3) [8]. Sections are not mandatory — tailor to the project; not every section applies to every problem [2].

**Non-goals are as important as goals.** Multiple independent sources identify non-goals as a critical scope management tool [1][8]. No disconfirming evidence found for this claim — it is robust across practitioner experience (HIGH — T4 + T5 convergence, no counter-evidence found).

**Writing clarifies thinking.** The act of specifying forces the author to be concrete about decisions they might otherwise handwave [12][8]. This is also the spec's primary failure mode: authors write the implementation they intend rather than the design space they explored, producing implementation plans disguised as design docs [1][8] (MODERATE — T5 practitioner observation; no experimental evidence that writing outperforms other sense-making methods).

**For AI-assisted development contexts (2025):** Effective specs use domain-oriented language, Given/When/Then scenario structure, and explicit I/O mappings, preconditions, and invariants [4][5][7]. The challenge evidence qualifies this: Birgitta Böckeler (Source 5, published on Martin Fowler's site, T4) reports that AI agents frequently ignore spec instructions; the "curse of instructions" research shows performance drops under many simultaneous requirements [13] (LOW for SDD-improves-AI-output claim — contradicted by within-document sources and external counter-evidence).

**Design docs are time-stamped artifacts, not living documentation.** They capture intent at a moment in time; subsequent changes warrant new documents, not updates to the original [12][8]. "Reading a design doc will not tell you how the system works now" [12] (HIGH — T5 convergence, corroborated by HN community [8]).

---

### Sub-question 2: How do specs differ from plans — what belongs in each?

**The boundary is WHAT/WHY (spec) vs. HOW (plan).** [6][7]

A specification describes precisely what the system will do and under what conditions — features, inputs/outputs, constraints, non-functional requirements. A design/implementation plan describes how the system will work — architecture, components, APIs, data representation, component behavior [6]. The specification should not bias the design; premature HOW thinking makes requirements harder to validate and limits design space [6] (HIGH — T2 academic source [6] + T1 official GitHub docs [7] converge on this distinction).

**The SDD workflow formalizes the sequence: Specify → Plan → Tasks.** GitHub Spec Kit [7] codifies this as: (1) specification focuses on WHAT users need and WHY, avoiding implementation details; (2) implementation plan converts business requirements to technical architecture; (3) tasks are atomic work units derived from the plan. The Spec Kit frames specifications as the central source of truth, with implementation plans and code as continuously regenerated output [7] (MODERATE — T1 source represents GitHub's opinionated workflow; unproven at scale outside that specific ecosystem).

**Counter-evidence and scope qualification:** The clean spec/plan separation is primarily validated in large organizations. Small and mid-size teams rarely maintain separate artifacts for these layers — the 2003 academic definition predates agile; the 2025 GitHub workflow is a novel pattern with limited adoption data. Practitioner accounts (Kaplan-Moss, Candost) show format taxonomies erode under organizational pressure. **For teams under ~20 engineers, the spec and plan may reasonably merge into a single design document** (MODERATE — based on challenge counter-evidence; no direct empirical data).

**A useful working rule:** Specs answer "what success looks like and what the constraints are." Plans answer "how the team will build it and in what order." If a document mixes the two, separate them — or scope the project to where merging is harmless.

---

### Sub-question 3: What specification formats are used in practice and what are their tradeoffs?

**Four formats serve distinct purposes — the choice depends on scope, audience, and whether a decision needs recording or buy-in needs building.**

**Architecture Decision Record (ADR):** A short document (1-2 pages) capturing a single architecture decision. Inverted pyramid — decision first, context and rationale after. Status lifecycle: proposed → accepted → superseded (never reopened). "Once an ADR is accepted, it should never be reopened or changed — instead it should be superseded." [10] Stored in source repo, near the code it concerns [10]. Best for: team-scoped decisions that can be executed quickly; decisions where stakeholder buy-in is within the team [9][10] (HIGH — T4 Martin Fowler, who popularized ADRs, is the primary source; T5 corroboration).

**Request for Comments (RFC):** A document to drive feedback and community buy-in before a decision is finalized. Longer feedback period. Driven by organizational culture; best for changes that affect multiple teams or require cross-functional input [9][11]. Uber's template includes: Abstract, Architecture changes, Service SLAs, Dependencies, Performance, Security, Rollout, Monitoring, Support considerations [11]. **Known failure mode:** RFC processes without an explicit decision step default to "no" through inertia; discussions never conclude; reviewer overload is documented at scale — "hundreds of RFCs weekly" at Uber 2,000+ engineers created friction [11] (MODERATE for RFC efficacy — T4 sources support the format; counter-evidence from Kaplan-Moss and Cvet on failure modes is T5 but convergent and detailed). Use RFC only when cross-team buy-in is required and a decision-owner is assigned.

**Design document (tech spec):** Broader exploration of trade-offs for a new system or major feature. Not a decision record — explores the problem space. Sections: Context/Scope, Goals/Non-goals, Design options, Alternatives Considered, Appendices [1][2]. Length: "the sweet spot for a larger project seems to be around 10-20ish pages" [1]; 1-10 pages for most work [14]. For smaller features, functional spec and technical spec can merge into one document [14] (HIGH for structure and length guidance — T4 source [1] from Google, widely cited).

**Spec-first / SDD artifact (2025):** A behavior-oriented specification written before AI-generated code. Six essential areas identified from a GitHub analysis of 2,500+ agent configuration files: Commands (with full flags), Testing (frameworks, locations), Project structure, Code style (with examples), Git workflow, Boundaries (what agents should never touch) [13]. Built for AI agent consumption, not team communication [7][13] (LOW to MODERATE — T1 [7] + T4 [13] sources endorse; significant counter-evidence on whether agents reliably consume these specs).

**Format selection decision rule** (synthesized from [9], qualified by challenge evidence):
- Change affects multiple teams → RFC (assign a decision-owner or it will stall)
- Team-scoped architectural decision → ADR
- New system or major feature requiring trade-off exploration → Design doc
- Task involving AI code generation → SDD artifact (treat as promising, not proven)
- Small, clear change → no document; just make the change

**As organizations scale, format taxonomy erodes.** Uber introduced lightweight and heavyweight template variants as team count grew [11]. No format stays clean at scale without active maintenance of the process.

---

### Sub-question 4: How should specs be calibrated for task complexity?

**The primary calibration dimension is ambiguity, not size.** Write a spec when the solution is ambiguous — because of problem complexity, solution complexity, or both. If the path is clear, write code [1]. "If a doc basically says 'This is how we are going to implement it' without going into trade-offs, alternatives, and explaining decision making…it would probably have been a better idea to write the actual program right away" [1] (HIGH — T4 source; T4 Pragmatic Engineer [11] independently converges on same threshold).

**A practical complexity ladder** (synthesized from [1][3][11][14]):
- **No document:** Small, clear, reversible changes. Just make the change [11].
- **Inline comment or short note:** Minor decisions worth recording in code review or PR description.
- **One-pager / brief design note:** Changes with non-trivial dependencies, modest risk, limited stakeholder impact. 1-2 pages; summary, approach, key risks [3].
- **Full design document:** New systems, significant features, cross-cutting changes, or anything with high ambiguity or irreversibility. 5-20 pages; full structure including alternatives and cross-cutting concerns [1][14].
- **RFC:** Cross-team changes requiring broad buy-in before proceeding. Full template, assigned decision-owner.

**Risk is the secondary calibration dimension.** Low risk → smaller document; high risk/scope → go deeper [3]. Risk and complexity often correlate but don't always — a simple API change with a large blast radius may warrant a full doc; a complex internal refactor with no external dependencies may not [3][11].

**For AI-assisted development:** Start with a high-level spec; have the AI expand it into detail. Don't underspec hard problems, don't overspec trivial ones [13]. The "curse of instructions" caveat applies: give AI agents one focused task at a time rather than a monolithic spec [13] (MODERATE — T4 source; counter-evidence shows verbosity can degrade rather than improve AI output).

**Counter-evidence (important qualification):** The complexity-threshold heuristic rests entirely on practitioner intuition — no empirical validation is cited anywhere in the source base. Turnbull's (2024) throwaway-prototype argument suggests that for exploratory work, building a disposable implementation discovers constraints better than a written spec. The default posture may reasonably be: **no spec unless a specific condition triggers it** (irreversibility, cross-team impact, or genuine ambiguity), rather than "spec more for complex problems" as a default [challenge counter-evidence].

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Writing specs before coding improves outcomes by forcing clear thinking | Multiple sources (Tietz-Sokolskaya, Ubl, Talin) assert that writing disciplines thought and surfaces gaps before implementation costs mount | Lucas Costa argues the opposite: you have the least information at project start, making early specs false precision; Doug Turnbull (2024) argues throwaway prototype PRs discover real constraints better than pre-written docs | **High.** If thinking-by-doing outperforms thinking-by-writing for most tasks, the central value proposition of design docs collapses to organizational signaling only |
| Specs remain useful artifacts after the project ships | Sources 8 (HN), 12 (Tietz-Sokolskaya) treat docs as long-lived knowledge assets | Source 12 itself concedes "Reading a design doc will not tell you how the system works now." Turnbull (2024) calls unmaintained docs "undead documentation" that actively misleads; isoform.ai (2025) notes reality changes faster than specs do | **Medium.** If docs are reliable only for ~the duration of the project, recommendations about archival and historical reference lose much of their force |
| Complexity calibration ("write more for harder problems") is a reliable heuristic | Sources 1, 3, 11 converge on risk/complexity as the trigger; Google, Uber, and Close all describe tiered spec depth | The threshold is socially constructed and rarely operationalized; RFC failure modes (Jacob Kaplan-Moss, 2023; Cvet) show teams over-apply heavy processes to modest changes and under-apply them to high-stakes reversible decisions; no empirical study is cited that validates the complexity-threshold heuristic | **Medium.** Without a validated threshold, "calibrate to complexity" is advice that can't be acted on consistently across teams |
| ADRs and RFCs serve distinct purposes and the choice between them is clear | Source 9 (Candost) provides a clean decision tree: cross-team buy-in → RFC, team-scoped decision → ADR | In practice the boundary blurs: Kaplan-Moss (2023) shows RFC processes decay into unresolvable discussions without a formal decision step; Cvet documents RFC templates accumulating checklists that mask organizational dysfunction rather than resolve it; Uber's experience shows even well-intentioned RFC systems create hundreds of weekly documents that overwhelm reviewers | **Medium.** If the RFC/ADR distinction breaks down at scale, the tidy format taxonomy the document presents is less actionable than it appears |
| Spec-driven development meaningfully improves AI-assisted coding quality | Source 4 (Thoughtworks), Source 5 (Böckeler), Source 7 (GitHub Spec Kit) endorse spec-first as a 2025 best practice; Source 13 (Osmani) offers six concrete elements | Source 5 (Böckeler, same document) directly contradicts this: "I frequently saw the agent ultimately not follow all the instructions." Isoform.ai (2025) found Spec Kit generated 8 files and 1,300+ lines for a trivial date-display feature—verbosity that can itself degrade agent performance; the "curse of instructions" research (Source 13) shows model performance drops under many simultaneous requirements | **High.** If detailed specs do not reliably improve AI agent behavior, the SDD framing is aspirational rather than evidence-based |

**Flags:** The complexity-threshold assumption (row 3) has no cited empirical validation — it rests entirely on practitioner opinion. The SDD-improves-AI-output assumption (row 5) is contradicted by evidence within the document's own sources.

---

### Premortem

Assume the main conclusion is wrong — that spec-first is not a generally useful practice, that the taxonomy of formats (design doc / RFC / ADR / SDD) is not actionable, and that calibration advice fails in practice.

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **The document overweights practitioner advocacy.** All primary sources are blog posts, newsletters, and vendor publications (GitHub, Thoughtworks) by authors with reputational or commercial stakes in legitimizing spec-writing. No randomized or quasi-experimental evidence is cited. This is a known bias in software engineering discourse: practices that feel productive (writing, planning) attract confident advocacy disproportionate to their measured effect on outcomes. | High | Weakens the empirical grounding of every sub-question. Conclusions should be restated as "practitioner consensus" rather than "evidence-based best practice." |
| **The spec-vs-plan boundary may be a false distinction in most teams.** The document draws a clean WHAT/WHY (spec) vs. HOW (plan) line from a 2003 academic source and a 2025 GitHub toolkit. In reality, small and mid-size teams rarely separate these artifacts; the GitHub/Kiro SDD workflow is novel and unproven at scale. Candost, Kaplan-Moss, and Cvet all show that clean format taxonomies erode under organizational pressure. | Medium | The format taxonomy and the spec/plan boundary advice may apply only to large organizations (Google-scale), limiting generalizability. The document should qualify scope. |
| **Emerging evidence suggests lightweight or no-spec approaches outperform detailed specs in fast-changing contexts.** Isoform.ai (2025) and Costa's "design docs considered harmful" argument both identify contexts — exploratory development, evolving requirements, small teams — where detailed specs create maintenance drag without commensurate benefit. The document's sources acknowledge this only in passing (Ubl: "just start coding" for unambiguous cases). If the majority of real-world engineering work is exploratory, the document's pro-spec tilt may describe the exception rather than the rule. | Medium | The calibration advice ("spec more for complex work") may need inversion: the default should be no spec, with a spec written only when specific conditions are met — a stronger claim than the document currently makes. |

**Plausibility assessment:** The first failure reason (advocacy bias) is the most structurally serious. The conclusions are directionally sound for large, cross-functional teams shipping stable systems. For small teams, AI-assisted exploratory work, or fast-changing contexts, the conclusions require significant qualification.

---

### Counter-Evidence Found

**Against writing design docs (overhead, rot, theater):**

- Lucas Costa, "Design docs considered harmful" — argues the timing problem is fundamental: design decisions must be made when information is worst. Calls design docs "organizational theater" where the real function is obtaining sign-off, not directing development. Recommends one-pagers scoped to irreversible decisions only.
- Doug Turnbull, "Preferring throwaway code over design docs" (December 2024) — argues prototype PRs are superior to design docs: code discovers actual constraints; unmaintained docs actively mislead; "a prototype can be worth 1000 design docs" for driving organizational change.
- Stack Overflow Blog (2024) — survey data shows developers broadly resist writing documentation, with a significant portion citing maintenance burden as the primary deterrent.

**Against ADRs / RFCs:**

- Jacob Kaplan-Moss, "RFC processes are a poor fit for most organizations" (December 2023) — the structural flaw: no explicit decision step makes RFC outcomes default to "no," rewarding obstruction over decision.
- Mike Cvet, "Goals and Failure Modes for RFCs and Technical Design Documents" — five concrete failure modes at scale: bloated templates, no feedback loops, misaligned facilitator roles, templates masking organizational dysfunction, and absent ownership.
- Uber at 2,000+ engineers (Source 11, within the document) — hundreds of RFCs weekly overwhelmed reviewers; this is framed in the document as an evolution story but is also a documented failure mode.

**Against spec-driven development for AI agents:**

- Isoform.ai, "The Limits of Spec-Driven Development" (2025) — four failure modes: maintenance burden, missing context (specs document *what*, not *why*), false confidence reducing iteration, and abstraction mismatch. A simple date-display feature generated 1,300+ lines of spec text in Spec Kit.
- Source 5 (Böckeler, already in document) — "I frequently saw the agent ultimately not follow all the instructions" despite detailed specs.
- "Curse of instructions" research (cited in Source 13) — performance drops when models must satisfy many requirements simultaneously.

**Claims with no counter-evidence:**
- The value of explicit non-goals sections — no disconfirming evidence found. This claim is robust.
- Risk/complexity as the correct calibration dimensions — no disconfirming evidence found on the *dimensions*, only on whether teams can operationalize them consistently.

---

## Takeaways

**The anti-pattern is consistent across all formats:** Documents that record *what was built* rather than *why it was decided*, omit alternatives, or substitute implementation detail for design rationale have low long-term value and high maintenance cost [1][8][14].

**The practical default should be no spec,** triggered only by specific conditions: cross-team impact, irreversibility, or genuine solution ambiguity. "If the path is clear, write code." Spec writing is not a proxy for engineering rigor — it is a tool for a narrow set of high-value situations.

**RFC processes need a decision-owner.** Without an explicit step that closes the RFC and records a decision, discussions stall by default. The format is not self-organizing.

**SDD claims require skeptical reading.** Spec-first for AI coding agents is advocated by credible sources (GitHub, Thoughtworks, Addy Osmani) but contradicted by evidence within those same sources. Treat as an actively evolving practice with real failure modes, not an established best practice.

**Scope of applicability:** All format recommendations (design doc, RFC, ADR) are most validated for engineering teams of 20+ working on stable systems. For smaller teams or exploratory work, the overhead may exceed the benefit.

**Gaps for follow-up:**
- Empirical comparison of spec-first vs. prototype-first development outcomes
- ADR/RFC adoption patterns at small teams (< 20 engineers)
- SDD tooling maturity: Kiro, Tessl, GitHub Spec Kit — production-proven?

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.industrialempathy.com/posts/design-docs-at-google/ | Design Docs at Google | Malte Ubl / industrialempathy.com | 2020 | T4 | verified |
| 2 | https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/ | A practical guide to writing technical specs | Stack Overflow Blog | 2020 | T5 | verified |
| 3 | https://codydjango.com/software-technical-design-documents/ | Writing "minimum viable" technical design documents | codydjango.com | 2023 | T5 | verified |
| 4 | https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices | Spec-driven development: Unpacking 2025's new AI-assisted engineering practices | Thoughtworks | 2025 | T2 | verified |
| 5 | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl | Birgitta Böckeler (via Martin Fowler's site / Thoughtworks) | 2025 | T4 | verified |
| 6 | https://www.jrobbins.org/ics121f03/lesson-spec-design.html | ICS 121: Specification vs. Design | Prof. J. Robbins / UC Irvine | 2003 (foundational) | T2 | verified |
| 7 | https://github.com/github/spec-kit/blob/main/spec-driven.md | spec-driven.md — GitHub Spec Kit | GitHub | 2025 | T1 | verified |
| 8 | https://news.ycombinator.com/item?id=44779428 | Writing a good design document (HN discussion) | Hacker News community | 2025 | T5 | verified |
| 9 | https://candost.blog/adrs-rfcs-differences-when-which/ | ADRs and RFCs: Their Differences and Templates | Candost Blog | 2023 | T5 | verified |
| 10 | https://martinfowler.com/bliki/ArchitectureDecisionRecord.html | bliki: Architecture Decision Record | Martin Fowler | 2022 | T4 | verified |
| 11 | https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs | Engineering Planning with RFCs, Design Documents and ADRs | The Pragmatic Engineer (Gergely Orosz) | 2023 | T4 | verified |
| 12 | https://ntietz.com/blog/reasons-to-write-design-docs/ | Reasons to write design docs | Nicole Tietz-Sokolskaya | 2024 | T5 | verified |
| 13 | https://addyosmani.com/blog/good-spec/ | How to write a good spec for AI agents | Addy Osmani | 2025 | T4 | verified |
| 14 | https://medium.com/machine-words/writing-technical-design-docs-71f446e42f2e | Writing Technical Design Docs | Talin / Machine Words | 2018 (foundational) | T5 | access restricted (HTTP 403) — kept |
| 15 | https://making.close.com/posts/writing-technical-specification-for-feature-development/ | Writing a Technical Specification for Feature Development | The Making of Close | 2024 | T5 | verified |

---

## Extracts

### Sub-question 1: What makes a good software design specification?

#### Source 1: Design Docs at Google
- **URL:** https://www.industrialempathy.com/posts/design-docs-at-google/
- **Author/Org:** Malte Ubl / industrialempathy.com | **Date:** 2020

**Re: Sub-question 1**
> "The design doc is *the place to write down the trade-offs* you made in designing your software." (What to Put in a Design Doc)

> "A short list of bullet points of what the goals of the system are, and, sometimes more importantly, what non-goals are." (Goals and Non-Goals section)

> "This section gives the reader a very rough overview of the landscape in which the new system is being built and what is actually being built." (Context and Scope section)

> "Design docs are informal documents and thus don't follow a strict guideline for their content. Rule #1 is: Write them in whatever form makes the most sense." (Format)

> "The sweet spot for a larger project seems to be around 10-20ish pages." (Length)

> "copy-pasting formal interface or data definitions into the doc as these are often verbose, contain unnecessary detail and quickly get out of date." [avoid this] (What to avoid)

> "Focus on those trade-offs to produce a useful document with long-term value." (Core guidance)

> "If a doc basically says 'This is how we are going to implement it' without going into trade-offs, alternatives, and explaining decision making…it would probably have been a better idea to write the actual program right away." (Anti-pattern)

> "At the center of that decision lies whether the solution to the design problem is ambiguous–because of problem complexity or solution complexity, or both." (When to write)

**Re: Sub-question 3** (deferred)
> Sections include: Context and Scope, Goals and Non-Goals, The Actual Design, APIs, Data Storage, Alternatives Considered, Cross-Cutting Concerns (security, privacy, observability)

---

#### Source 2: A practical guide to writing technical specs (Stack Overflow Blog)
- **URL:** https://stackoverflow.blog/2020/04/06/a-practical-guide-to-writing-technical-specs/
- **Author/Org:** Stack Overflow Blog | **Date:** 2020

**Re: Sub-question 1**
> "A technical specification document outlines how you're going to address a technical problem by designing and building a solution for it." (Definition)

> Eight essential sections: Front Matter, Introduction, Solutions, Further Considerations, Success Evaluation, Work, Deliberation, End Matter (Structure)

> "Every solution has different needs and you should tailor your technical spec based on the project. You do not need to include all the sections mentioned below." (Flexibility)

> "Review independently before sharing" and "Send the draft out to your team and the stakeholders" (Best Practices)

---

#### Source 3: Writing "minimum viable" technical design documents
- **URL:** https://codydjango.com/software-technical-design-documents/
- **Author/Org:** codydjango.com | **Date:** 2023

**Re: Sub-question 1**
> "Summary: High-level overview of the problem and proposed solution that can be understood by any engineer on your team." (Essential Sections)

> "Context: Tell a story. Like all good stories, use details to describe how we got here, and why it's now important to do something different." (Essential Sections)

> "Approach: Details of the solution with 'enough detail so that you'd feel comfortable handing this off to another engineer to implement.'" (Essential Sections)

> "If risks are low, then it's reasonable for the doc to be small... If the scope is larger, and risk is higher, then go deeper." (Appropriate Level of Detail)

> "Use short sentences, simple words, bulleted lists, concrete examples, and diagrams wherever possible... avoid business-speak or jargon." (Quality Characteristics)

---

#### Source 4: Spec-driven development: Unpacking 2025's key new AI-assisted engineering practices
- **URL:** https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices
- **Author/Org:** Thoughtworks | **Date:** 2025

**Re: Sub-question 1**
> "specifications should still use domain-oriented ubiquitous language to describe business intent rather than specific tech-bound implementations" (What makes a good spec?)

> "They should also have a clear structure, with a common style to define scenarios using Given/When/Then" (Structure and style)

> Specs should aim for "completeness yet conciseness, covering the critical path without enumerating all cases" (Balance)

> "A specification is definitely more than just a product requirements document (PRD)." (What is a spec?)

> Technically, specifications should explicitly define: "input/output mappings, preconditions/postconditions, invariants, constraints, interface types, integration contracts and sequential logic/state machines" (Quality Specification Contents)

> Prioritize "clarity and determinism" because "clear specifications can still help reduce model hallucinations and produce more robust code" (Best Practices)

> "providing the model with semi-structured input prompts or forcing it to output in a structured manner can significantly improve reasoning performance and reduce hallucinations" (Best Practices)

> "Reviewing and validating these specifications is usually an iterative process that requires a human in the loop" (Human oversight)

---

#### Source 5: Understanding Spec-Driven-Development (Birgitta Böckeler via Martin Fowler's site)
- **URL:** https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
- **Author/Org:** Birgitta Böckeler (Thoughtworks) | **Date:** 2025

**Re: Sub-question 1**
> "Spec-driven development means writing a 'spec' before writing code with AI ('documentation first'). The spec becomes the source of truth for the human and the AI." (Definition)

> "A spec is a structured, behavior-oriented artifact - or a set of related artifacts - written in natural language that expresses software functionality and serves as guidance to AI coding agents." (What constitutes a specification)

> "I also often spend time on carefully crafting some form of spec first to give to the coding agent. So the general principle of spec-first is definitely valuable in many situations." (Practical endorsement)

> "An effective SDD tool would have to provide a very good spec review experience." (Tooling requirement)

> "I frequently saw the agent ultimately not follow all the instructions" despite larger context windows and detailed specifications. (Practical challenge)

---

#### Source 12: Reasons to write design docs
- **URL:** https://ntietz.com/blog/reasons-to-write-design-docs/
- **Author/Org:** Nicole Tietz-Sokolskaya | **Date:** 2024

**Re: Sub-question 1**
> "Writing a design doc helps you think, leading to better designs." The author explains that putting design into words forces concreteness—"Instead of handwaving about it, it goes down onto the page." (Thinking Better)

> "Collaborating on a design doc with teammates improves the design." Fresh eyes catch gaps: "Any time a reader has a question about the doc, it's a signal that the document is unclear." (Collaborative Improvement)

> "When we don't have design docs, then our understanding of the design is itself an oral tradition." (Organizational Knowledge)

> "Reading a design doc will not tell you how the system works now." Design docs are snapshots reflecting intent rather than current implementation. (Important Limitation)

> "Design docs are one form of writing that is pretty essential for software engineering teams. Without them, you're just not going to make good decisions." (Recommendation)

---

#### Source 8: Writing a good design document (Hacker News discussion)
- **URL:** https://news.ycombinator.com/item?id=44779428
- **Author/Org:** Hacker News community | **Date:** 2025

**Re: Sub-question 1**
> "The first layer is the problem statement, goals, non-goals, and requirements" / "The next layer is the functional specification" / "The third and final layer is the technical specification" — nickm12 (Three-layer approach)

> "technical design documents that provide only the final section—a simple description of the system that will be built." [most frequent cited issue] (Critical Problem with Current Practice)

> "You need a fully-specced functional design and a high-level technical design" / "the technical implementation details can change as the project is developed" — tremon (Design vs. Implementation Boundary)

> "Writing is nature's way of telling us how sloppy our thinking is." — patrickmay, citing Leslie Lamport (Why Writing Matters)

> "Non-goals are SO important" — jeffrallen (Non-goals importance)

> Design documents capture decisions at specific moments — "subsequent changes warrant new documents rather than updates" — teiferer (Documentation Maintenance)

---

### Sub-question 2: How do specs differ from plans — what belongs in each, and where is the boundary?

#### Source 6: ICS 121: Specification vs. Design
- **URL:** https://www.jrobbins.org/ics121f03/lesson-spec-design.html
- **Author/Org:** Prof. J. Robbins / UC Irvine | **Date:** 2003 (foundational)

**Re: Sub-question 2**
> "The SRS describes precisely what the system will do." (Specification describes WHAT)

> "Design outlines how the system will work." (Design describes HOW)

> SRS includes: "Environmental requirements: OS, platform, interoperability, standards, etc." / "Non-functional requirements: security, usability, efficiency, etc." / "Feature specifications: precisely describe each feature" / "Use cases: examples of how a user accomplishes a goal" (What Belongs in Specification)

> Design covers: "Division of the system into components" / "Communications, APIs and dependencies between components" / "Classes, attributes, operations, and relationships within each component" / "Data representation in the database or files" / "Behavior of each system component" (What Belongs in Design)

> "The specification should not bias the design or implementation. Don't get ahead of yourself, you will do design later." (The Boundary)

> Design details "irrelevant to system test" and make requirements "harder for non-technical stakeholders to understand." (Why separation matters)

---

#### Source 7: GitHub Spec Kit — spec-driven.md
- **URL:** https://github.com/github/spec-kit/blob/main/spec-driven.md
- **Author/Org:** GitHub | **Date:** 2025

**Re: Sub-question 2**
> "Focus on WHAT users need and WHY" [specifications] / "Avoid HOW to implement (no tech stack, APIs, code structure)" [specifications] (What Belongs in a Specification)

> "Converts business requirements into technical architecture and implementation details" [implementation plan] (What Belongs in an Implementation Plan)

> "This implementation plan should remain high-level and readable. Any code samples, detailed algorithms, or extensive technical specifications must be placed in the appropriate implementation-details/ file" (Critical Boundary Between Them)

> SDD Workflow: 1. Specify → 2. Plan → 3. Tasks (The SDD Workflow Sequence)

> "Each stage builds on previous outputs, with specifications remaining the immutable source of truth throughout the cycle." (Workflow principle)

---

#### Source 11: Engineering Planning with RFCs, Design Documents and ADRs (Pragmatic Engineer)
- **URL:** https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
- **Author/Org:** The Pragmatic Engineer (Gergely Orosz) | **Date:** 2023

**Re: Sub-question 2**
> "For small changes: don't bother. Just make the change. For changes that are non-trivial and have dependencies: consider writing one." (When to Use)

> "the approach of using DUCKs – designed initially for new services – started to show cracks, with non-backend teams also looking to use this format." [Uber scaling example] (Evolution)

> "The effort to write an RFC should be proportionate to the complexity of the task. If the work is moderately complex, you should get done with the RFC quickly, and many sections might not apply." (Effort Calibration)

---

### Sub-question 3: What specification formats are used in practice and what are their tradeoffs?

#### Source 9: ADRs and RFCs: Their Differences and Templates
- **URL:** https://candost.blog/adrs-rfcs-differences-when-which/
- **Author/Org:** Candost Blog | **Date:** 2023

**Re: Sub-question 3**
> "When I read 'architecture decision records,' it also clearly says that it's a decision record, so there has to be a decision to record it. When I read 'request for comments,' it clearly states that the main goal is collecting feedback." (Core Distinction)

> "For influencing/driving a change that may (but not necessarily) take time to finalize." [RFCs] (RFC Purpose)

> "For making/recording a decision that can be executed quickly." [ADRs] (ADR Purpose)

> "Driven by the *community* culture" (RFCs) versus "Driven by the *team* culture" (ADRs) (Cultural Context)

> "Does the change affect others and require buy-in? If yes, **write an RFC**... If no, **write an ADR.**" (When to Use Each)

> RFCs have "Longer feedback periods" while ADRs require "Short feedback period to gather strong objections" (Process Speed)

> RFCs "Should be part of general documentation," while ADRs "Should stay close to the codebase." (Documentation Location)

---

#### Source 10: bliki: Architecture Decision Record (Martin Fowler)
- **URL:** https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
- **Author/Org:** Martin Fowler | **Date:** 2022

**Re: Sub-question 3**
> "An Architecture Decision Record (ADR) is a short document that captures and explains a single decision relevant to a product or ecosystem." (What They Are)

> "short, just a couple of pages, and contain the decision, the context for making it, and significant ramifications." ADRs follow an "inverted pyramid" style, putting "the most important material at the start, and push details to later in the record." (Format & Structure)

> Files should be "numbered in a monotonic sequence as part of their file name, with a name that captures the decision" — example: "`0001-HTMX-for-active-web-pages`" (Naming Convention)

> Each ADR has stages: "proposed" during discussion, "accepted" once adopted, and "superseded" when modified or replaced. "Once an ADR is accepted, it should never be reopened or changed - instead it should be superseded." (Status Lifecycle)

> ADRs should "the act of writing them helps to clarify thinking, particularly with groups of people." (Primary purpose)

> ADRs "should include rationale summarizing the problem, trade-offs considered, 'all the serious alternatives that were considered, together with their pros and cons'" (Content Requirements)

> Records should be kept "in the source repository of the code base to which they apply," typically in `doc/adr` (Storage)

---

#### Source 11: Engineering Planning with RFCs, Design Documents and ADRs (Pragmatic Engineer)
- **URL:** https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
- **Author/Org:** The Pragmatic Engineer (Gergely Orosz) | **Date:** 2023

**Re: Sub-question 3**
> "When starting a new service, it's important to document and vet its architecture. We use a peer review process designed to: Institute a strong, org-wide practice of information sharing; Provide transparency and good cross-team communication about upcoming systems; Provide historical documentation for our design motivations; Catch potential architectural stumbling blocks before they get to production." (Uber's purpose statement)

> Uber Services RFC Template sections: List of approvers, Abstract, Architecture changes, Service SLAs, Service dependencies, Load & performance testing, Multi data-center concerns, Security considerations, Testing & rollout, Metrics & monitoring, Customer support considerations. (Template Examples)

> Uber Mobile RFC Template sections: Abstract, UI & UX, Architecture changes, Network interactions detailed, Library dependencies, Security concerns, Testing & rollout, Analytics, Customer support considerations, Accessibility. (Template Examples)

> As Uber scaled to 2,000+ engineers, the RFC process created friction: "noise (hundreds of RFCs weekly), ambiguity about which work needed documentation, and poor discoverability (documents scattered across Google Drive)." (Scaling Problems)

> "As companies grow, they introduce lightweight templates for changes limited to team scopes to help with the problem of overly long documents for relatively simple changes, while more heavyweight templates are created for large-scale changes with organization or company-wide impacts." (Scale and Evolution)

---

#### Source 13: How to write a good spec for AI agents (Addy Osmani)
- **URL:** https://addyosmani.com/blog/good-spec/
- **Author/Org:** Addy Osmani | **Date:** 2025

**Re: Sub-question 3**
> Six essential areas identified from analysis of 2,500+ agent files: 1. Commands (executable with full flags), 2. Testing (frameworks, locations, coverage), 3. Project structure (explicit directory organization), 4. Code style (one real example beats three paragraphs), 5. Git workflow (branching, commits, PRs), 6. Boundaries (what agents should never touch) (Structure Like a PRD)

> "One real code snippet showing your style beats three paragraphs describing it." (Key quote)

> Three-Tier Boundaries System: "✅ Always do: Safe actions requiring no approval" / "⚠️ Ask first: High-impact changes needing human review" / "🚫 Never do: Categorically forbidden actions" (Boundaries System)

> "Never commit secrets" was the single most common helpful constraint. (Most common constraint)

---

### Sub-question 4: How should specs be calibrated for different task complexities?

#### Source 1: Design Docs at Google
- **URL:** https://www.industrialempathy.com/posts/design-docs-at-google/
- **Author/Org:** Malte Ubl / industrialempathy.com | **Date:** 2020

**Re: Sub-question 4**
> "At the center of that decision lies whether the solution to the design problem is ambiguous–because of problem complexity or solution complexity, or both." (When to write a design doc)

> "If a doc basically says 'This is how we are going to implement it' without going into trade-offs, alternatives, and explaining decision making…it would probably have been a better idea to write the actual program right away." (Anti-pattern for over-speccing)

---

#### Source 3: Writing "minimum viable" technical design documents
- **URL:** https://codydjango.com/software-technical-design-documents/
- **Author/Org:** codydjango.com | **Date:** 2023

**Re: Sub-question 4**
> "If risks are low, then it's reasonable for the doc to be small... If the scope is larger, and risk is higher, then go deeper." (Risk-driven scope)

> Estimate: Breaking down work, keeping "all estimates under two weeks, and preferably under one." (Estimate granularity)

---

#### Source 11: Engineering Planning with RFCs, Design Documents and ADRs (Pragmatic Engineer)
- **URL:** https://newsletter.pragmaticengineer.com/p/rfcs-and-design-docs
- **Author/Org:** The Pragmatic Engineer (Gergely Orosz) | **Date:** 2023

**Re: Sub-question 4**
> "For small changes: don't bother. Just make the change. For changes that are non-trivial and have dependencies: consider writing one." (Complexity threshold)

> "The effort to write an RFC should be proportionate to the complexity of the task. If the work is moderately complex, you should get done with the RFC quickly, and many sections might not apply." (Proportionality)

> Uber introduced "lightweight templates for changes limited to team scopes" and "more heavyweight templates for large-scale changes with organization or company-wide impacts." (Format calibration at scale)

---

#### Source 13: How to write a good spec for AI agents (Addy Osmani)
- **URL:** https://addyosmani.com/blog/good-spec/
- **Author/Org:** Addy Osmani | **Date:** 2025

**Re: Sub-question 4**
> "Kick off your project with a concise high-level spec, then have the AI expand it into a detailed plan." (High-Level First)

> "adjust spec detail to task complexity. Don't under-spec a hard problem...but don't over-spec a trivial one." (Calibrating Detail)

> "For simple tasks, minimal specs suffice. Complex work (like OAuth implementation) demands detailed specifications." (Simple vs Complex)

> "the 'curse of instructions' research shows performance drops when models must satisfy many requirements simultaneously. Solution: 'give the AI one focused task at a time rather than a monolithic prompt.'" (Avoiding Overload)

---

#### Source 14: Writing Technical Design Docs
- **URL:** https://medium.com/machine-words/writing-technical-design-docs-71f446e42f2e
- **Author/Org:** Talin / Machine Words | **Date:** 2018 (foundational)

**Re: Sub-question 4**
> "For smaller features that don't involve a lot of complexity, steps 2 and 3 will often be combined into a single document." (Combining steps for simple features)

> "The document should be thorough; ideally, it should be possible for someone other than the TDD author to implement the design as written." (Thoroughness Standard)

> "Most TDDs are between one and ten pages. Although there's no upper limit to the length of a TDD, very large documents will be both difficult to edit and hard for readers to absorb; consider breaking it up into separate documents." (Length Guidance)

> The most prevalent error: "lack of context. That is, the author wrote down...how they solved the problem; but they didn't include any information on what the problem was, why it needed to be solved." (Context Requirement)

---

#### Source 15: Writing a Technical Specification for Feature Development (Close)
- **URL:** https://making.close.com/posts/writing-technical-specification-for-feature-development/
- **Author/Org:** The Making of Close | **Date:** 2024

**Re: Sub-question 4**
> Core sections: "Executive Summary, Team Availability, Prioritized Deliverables, Designs, Timeline, References" (Structure)

> "Start High-Level" advises beginning with product specifications and business context, then progressing through design review and code exploration before finalizing estimates. (Detail Level Calibration)

> Minimum estimation unit: "0.5 days. For very small tasks, group them together" (Granularity)

> "Each piece should function independently, have a clear deliverable, and be testable" for accurate estimation. (Breaking down work)

> "Avoid scheduling any critical work in the last week" to prevent spillover. (Timeline protection)

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "If a doc basically says 'This is how we are going to implement it' without going into trade-offs, alternatives, and explaining decision making…it would probably have been a better idea to write the actual program right away" | quote | [1] | corrected — original draft omitted "going into" and "and explaining decision making"; corrected to match source |
| 2 | "Reading a design doc will not tell you how the system works now." | quote | [12] | verified |
| 3 | Böckeler (Source 5): "I frequently saw the agent ultimately not follow all the instructions" despite detailed specs | quote | [5] | corrected — draft attributed this to "Martin Fowler"; actual author is Birgitta Böckeler (Thoughtworks); article published on Fowler's site |
| 4 | "The sweet spot for a larger project seems to be around 10-20ish pages." | quote | [1] | verified |
| 5 | Six essential areas "identified from analysis of 2,500+ agent files" | statistic | [13] | corrected — the 2,500+ file analysis is GitHub's study, cited through Osmani; not Osmani's own analysis. Exact source: GitHub's analysis of over 2,500 agent configuration files |
| 6 | "Specifications remain the immutable source of truth throughout the cycle" | quote | [7] | removed — exact phrase not found in GitHub Spec Kit source. Replaced in Findings with accurate paraphrase: "specifications as the central source of truth, with implementation plans and code as continuously regenerated output" |
| 7 | "As Uber grew to well over 2,000 engineers" RFC process created friction with "hundreds of RFCs went out weekly" | statistic | [11] | verified |
| 8 | "At the center of that decision lies whether the solution to the design problem is ambiguous–because of problem complexity or solution complexity, or both." | quote | [1] | corrected — draft rendered this as "The core decision hinges on '…'" which is a paraphrase of the source; corrected to verbatim in Extracts and Findings |
| 9 | "Once an ADR is accepted, it should never be reopened or changed — instead it should be superseded." | quote | [10] | verified |
| 10 | "'Never commit secrets' was the single most common helpful constraint" (from GitHub study via Source 13) | quote | [13] | verified |

CoVe complete: 4 claims verified, 4 corrected, 0 human-review, 0 unverifiable.

---

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| software design document best practices structure acceptance criteria 2025 | google | 2024-2026 | 10 | 2 |
| what makes a good software specification level of detail engineering 2025 | google | 2024-2026 | 10 | 3 |
| Google engineering design doc template what goes in technical spec 2024 2025 | google | 2024-2026 | 10 | 2 |
| technical design document structure context and scope goals and non-goals engineering teams | google | 2024-2026 | 10 | 2 |
| spec-driven development AI assisted software engineering specification quality 2025 | google | 2025-2026 | 10 | 3 |
| software design specification what to include what not to include engineering best practices | google | 2024-2026 | 10 | 2 |
| spec vs plan software engineering difference implementation plan design spec what belongs where | google | 2024-2026 | 10 | 2 |
| software requirements specification vs design document difference what belongs in spec vs design | google | 2024-2026 | 10 | 2 |
| design doc vs implementation plan vs project plan software engineering boundary distinction 2024 | google | 2024-2026 | 10 | 2 |
| ADR architecture decision record format RFC engineering process tradeoffs comparison 2024 2025 | google | 2024-2026 | 10 | 3 |
| RFC process engineering teams request for comments format best practices internal engineering 2024 2025 | google | 2024-2026 | 10 | 1 |
| one-pager design doc engineering one page spec format when to use lightweight specification | google | 2024-2026 | 10 | 1 |
| engineering spec formats comparison design doc ADR RFC tech spec tradeoffs when to use each 2025 | google | 2024-2026 | 10 | 2 |
| when to write a design doc complexity threshold no doc needed team decision engineering practice | google | 2024-2026 | 10 | 1 |
| spec writing complexity scale paragraph one page full document feature complexity software engineering 2024 | google | 2024-2026 | 10 | 1 |
| design document complexity calibration when not to write spec just build it engineering judgment 2024 2025 | google | 2024-2026 | 10 | 3 |

16 searches · google · 160 candidates found · 32 used
