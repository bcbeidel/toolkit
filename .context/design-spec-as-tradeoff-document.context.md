---
name: Design Spec as Trade-off Document
description: "A design spec's core function is recording WHAT and WHY a decision was made — alternatives considered, constraints accepted — not HOW to implement. Write only when triggered by irreversibility or genuine ambiguity."
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.industrialempathy.com/posts/design-docs-at-google/
  - https://ntietz.com/blog/reasons-to-write-design-docs/
  - https://news.ycombinator.com/item?id=44779428
  - https://codydjango.com/software-technical-design-documents/
related:
  - docs/context/specification-format-taxonomy-adr-rfc-sdd.context.md
  - docs/context/diverge-converge-design-mode-switching.context.md
  - docs/context/mental-models-software-decisions-practitioner-vs-empirical.context.md
---
# Design Spec as Trade-off Document

## Key Insight

A design spec is a trade-off document, not an implementation blueprint. Its value is recording *why* a decision was made — alternatives considered, constraints accepted, risks surfaced. A document that only describes what was built should have been replaced by the working code. Write when the solution is ambiguous; don't write when the path is clear (HIGH — T4 sources converge, corroborated by HN community).

## What Belongs in a Spec

**The core function:** "The design doc is the place to write down the trade-offs you made in designing your software." Not the implementation details — those belong in code. The document captures: which options were evaluated, which constraints shaped the decision, which risks were accepted and why.

**Non-goals are as important as goals.** Multiple independent sources identify non-goals as a critical scope management tool. Explicit non-goals prevent scope creep, set reviewer expectations, and document what the team decided *not* to do and why. No disconfirming evidence was found for this claim.

**Canonical structure (adapt to fit):**
1. Context and Scope — "a very rough overview of the landscape"
2. Goals and Non-goals
3. The Actual Design — APIs, data storage, key interfaces
4. Alternatives Considered
5. Cross-Cutting Concerns — security, privacy, observability

Sections are not mandatory. "Write them in whatever form makes the most sense." Not every section applies to every problem.

## What Doesn't Belong in a Spec

Avoid copying in formal interface definitions or data definitions — these "are often verbose, contain unnecessary detail and quickly get out of date." If a document "basically says 'This is how we are going to implement it' without going into trade-offs, alternatives, and explaining decision making... it would probably have been better to write the actual program right away."

A spec that records implementation without exploring trade-offs or alternatives should be replaced with the code. The implementation itself is a better artifact.

## Design Docs Are Time-Stamped Artifacts

Design docs are not living documentation. They capture intent at a moment in time. "Reading a design doc will not tell you how the system works now." Subsequent changes warrant new documents, not updates to the original. The doc's value is historical — understanding why a decision was made under the constraints that existed at that moment.

## When to Write

**The trigger is ambiguity or irreversibility, not task size.** "At the center of that decision lies whether the solution to the design problem is ambiguous — because of problem complexity or solution complexity, or both."

**Practical default: no spec** until a specific condition triggers it:
- Cross-team impact (needs buy-in or awareness)
- Irreversibility (hard to undo after implementation starts)
- Genuine solution ambiguity (multiple valid approaches with different trade-offs)

For clear, reversible, team-scoped changes: write code. The overhead of a spec exceeds its value when the path is unambiguous.

## Takeaway

If a document doesn't record why alternatives were rejected, it is not a design spec — it's an implementation summary. The spec's long-term value depends entirely on the alternatives-and-rationale content. Treat every spec as time-stamped at decision point; never update it to reflect what was eventually built.
