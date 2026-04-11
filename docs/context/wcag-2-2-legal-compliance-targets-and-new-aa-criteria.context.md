---
name: WCAG 2.2 Legal Compliance Targets and New AA Criteria
description: "WCAG 2.2 AA is the current legal target globally (EU EAA enforced June 2025, US ADA de facto standard); WCAG 3.0 won't supersede WCAG 2 before 2028+ and WCAG 2 will not be deprecated."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.w3.org/WAI/standards-guidelines/wcag/
  - https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
  - https://www.w3.org/press-releases/2025/wcag22-iso-pas/
  - https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/
related:
  - docs/context/accessibility-automation-coverage-ceiling-and-manual-testing-floor.context.md
  - docs/context/semantic-html-first-and-overlay-anti-pattern.context.md
---
# WCAG 2.2 Legal Compliance Targets and New AA Criteria

## Key Insight

WCAG 2.2 AA is the current legal compliance target for the EU, UK, and US. The European Accessibility Act (EAA) went into force June 28, 2025. WCAG 3.0 remains a Working Draft as of September 2025 — Draft Candidate Recommendation planned Q4 2027; full standard not before 2028. Implement WCAG 2.2, not WCAG 3.

## Legal Status

**European Accessibility Act (EAA)**: Enforced June 28, 2025, requiring WCAG 2.2 Level AA compliance across EU product and service categories.

**UK public sector**: Full WCAG 2.2 Level AA compliance required as of June 2025.

**US ADA**: References WCAG 2.2 AA as the de facto litigation standard.

**ISO/IEC 40500:2025**: WCAG 2.2 was approved as an international ISO standard in 2025, giving it additional regulatory weight globally.

WCAG 2.2 is backwards compatible: content conforming to WCAG 2.2 also conforms to WCAG 2.1 and WCAG 2.0. Targeting 2.2 automatically satisfies all earlier versions.

## WCAG 2.2 New Level AA Criteria (the legal floor additions)

Four new AA criteria were added. All must be satisfied for WCAG 2.2 AA compliance:

**2.4.11 Focus Not Obscured (Minimum):** When an element receives keyboard focus, it must be at least partially visible — not entirely hidden by sticky headers, modals, or overlays. CSS fix: `html { scroll-padding-top: 100px; } *:focus { scroll-margin-top: 120px; }`

**2.5.7 Dragging Movements:** All drag-and-drop functionality requires a simple pointer alternative (arrow buttons for sortable lists, browse buttons for file uploads, +/- buttons for sliders).

**2.5.8 Target Size (Minimum):** Interactive targets must be 24×24 CSS pixels or positioned with adequate spacing. Critical for mobile usability.

**3.3.8 Accessible Authentication (Minimum):** Must enable password managers (`autocomplete="current-password"`), offer email/SMS codes, or use reCAPTCHA v3 rather than text CAPTCHAs. Cannot require users to solve, recall, or transcribe anything to log in.

## WCAG 2.2 New Level A Criteria

**3.2.6 Consistent Help:** Help mechanisms (chat widget, support link) must appear in a consistent relative order across pages where repeated.

**3.3.7 Redundant Entry:** Previously entered information must be auto-populated or selectable within the same session. Use `autocomplete` attributes and "same as shipping address" checkboxes.

## What Was Removed

**4.1.1 Parsing** was removed from WCAG 2.2 — it is always satisfied for any content using HTML or XML and no longer requires explicit testing.

## WCAG 3.0: Not a Near-Term Target

W3C's official position: "WCAG 3 will not supersede WCAG 2 and WCAG 2 will not be deprecated for at least several years after WCAG 3 is finalized." WCAG 3 will introduce a substantially different scoring model (outcome-based rather than pass/fail), which means current compliance infrastructure investment remains valid.

Do not build WCAG 3 compliance programs now. Build WCAG 2.2 AA compliance programs; they will remain legally required through at least 2028.

## Takeaway

Target WCAG 2.2 AA. The four new AA criteria — Focus Not Obscured, Dragging Movements, Target Size, and Accessible Authentication — are the new legal requirements added since WCAG 2.1. WCAG 3.0 is not a near-term concern; WCAG 2.2 will remain the legal standard through at least the end of this decade.
