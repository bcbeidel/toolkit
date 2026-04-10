---
name: "Knowledge Confidence Lifecycle and State Tracking"
description: "Knowledge confidence is a lifecycle property (WIP → Not Validated → Validated → Archived), not binary; confidence degrades without explicit maintenance"
type: context
sources:
  - https://library.serviceinnovation.org/KCS/KCS_v6/KCS_v6_Practices_Guide/030/040/010/030
  - https://gdt.gradepro.org/app/handbook/handbook.html
related:
  - docs/context/context-rot-and-window-degradation.context.md
  - docs/context/confidence-calibration-and-self-correction.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
---

Knowledge confidence is not binary. A document is not simply "correct" or "incorrect" — it occupies a state in a lifecycle, and that state can upgrade or downgrade over time as evidence accumulates, usage confirms, or conditions change. Treating confidence as a static property leads to stale documents being trusted without review.

## The KCS Four-State Model

KCS (Knowledge-Centered Service) v6 defines four article states with explicit criteria for transitions:

- **Work in Progress (WIP):** Problem captured, resolution unknown. Prevents duplicate effort. Publishable immediately — waiting for validation wastes the "just-in-time" window.
- **Not Validated:** Complete but lacking confidence. Created by candidates awaiting review, or early drafts where the author has not yet confirmed the resolution.
- **Validated:** Complete, reusable, and reliable. Requires two co-equal criteria: (1) responder confidence — confirmed by user, recreated and validated, or experience-based certainty; and (2) compliance with content standard.
- **Archived:** Logically removed from search but preserved for historical linking. Not deleted — archiving maintains the citation chain while removing the document from active retrieval.

The model originated in IT service management but its state-transition logic applies broadly to any knowledge artifact: research documents, context files, ADRs, and technical guides all benefit from explicit state tracking.

## Confidence Is Visible Infrastructure

KCS is explicit that "technology should make article confidence visible to users" because "confidence affects the trust users place in its accuracy and is extremely important and frequently referenced." For agent-facing knowledge bases, this means the confidence state should appear in frontmatter — not buried in document body prose where it may be missed.

A `status:` or equivalent frontmatter field serves this function. An agent encountering a document in `WIP` or `Not Validated` state can treat it differently from `Validated` content: lower weight for factual claims, higher emphasis on verification, or flagging for human review before acting.

## Confidence Degrades Without Maintenance

Validated status is not permanent. Conditions change: APIs deprecate, best practices evolve, dependencies update. A document validated 18 months ago against outdated tooling is functionally unreliable even though its state field still reads `Validated`. This is the same phenomenon as context rot — content that was accurate at creation becomes misleading through environmental change, not internal error.

Maintenance requires an owner and a review cycle. Assign authorship at creation. Archive rather than delete obsolete content — preservation maintains citation chains and provides historical context for decisions made against now-outdated information.

## GRADE as a Complementary Model

The GRADE framework (designed for clinical evidence) provides a four-tier certainty model: High, Moderate, Low, Very Low. It models confidence as a spectrum with explicit downgrade factors (risk of bias, inconsistency across sources, imprecision) and upgrade factors (large effect size, convergence across independent sources).

GRADE was designed for clinical medicine and its specific criteria do not transfer directly to software documentation without adaptation. The transferable insight is the framework's logic: confidence can be upgraded or downgraded based on new evidence, and the reasons for a confidence level should be stated explicitly rather than left implicit.

## Practical Application for Context Files

For a WOS knowledge base:
- New research documents start at `WIP` until the investigation is complete
- Research becomes `Not Validated` when findings are written but not yet challenged or cross-checked
- Research advances to `Validated` when the challenge section has been completed and key claims verified
- Context files distilled from research inherit the confidence ceiling of their source material
- Archived documents remain on disk but are excluded from active index entries and retrieval

The state does not need to be mechanically enforced — a frontmatter field and a review discipline are sufficient for knowledge bases in the 100-500 document range.
