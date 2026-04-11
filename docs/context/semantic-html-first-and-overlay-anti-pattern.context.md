---
name: Semantic HTML First and Overlay Anti-Pattern
description: "Use semantic HTML elements before ARIA; overlays (accessiBe, UserWay) do not achieve WCAG compliance and introduce legal risk — the FTC fined accessiBe $1M in 2025."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.w3.org/WAI/ARIA/apg/
  - https://www.accesify.io/blog/accessibility-design-systems-component-libraries/
  - https://dequeuniversity.com/resources/wcag-2.2/
related:
  - docs/context/wcag-2-2-legal-compliance-targets-and-new-aa-criteria.context.md
  - docs/context/accessibility-automation-coverage-ceiling-and-manual-testing-floor.context.md
---
# Semantic HTML First and Overlay Anti-Pattern

## Key Insight

Select HTML elements that convey functionality natively before applying ARIA. ARIA is for extending semantics of HTML, not replacing them. Accessibility overlays (accessiBe, UserWay, and similar products) do not achieve WCAG compliance — the FTC fined accessiBe $1 million in January 2025 for claiming otherwise, with over 1,000 overlay-equipped websites facing lawsuits in 2024.

## Semantic HTML First Principle (HIGH confidence — T1 W3C/WAI)

The ARIA Authoring Practices Guide (APG) from W3C is the authoritative reference for applying accessibility semantics. The foundational rule: **use native HTML elements that convey functionality natively before ARIA**.

- `<button>` instead of `<div role="button">`
- `<nav>` instead of `<div role="navigation">`
- `<ul>/<li>` instead of `<div role="list"><div role="listitem">`

Native HTML elements have built-in accessibility tree entries, keyboard behavior, and screen reader announcements. ARIA roles, states, and properties supplement native semantics — they do not substitute for them. Adding ARIA to an element that already has semantic meaning creates conflicts, not accessibility.

The practical rule: **if a native HTML element exists for the interaction, use it**. Reserve ARIA for custom widgets and patterns with no native HTML equivalent.

## When ARIA is Appropriate

ARIA becomes necessary for custom interactive patterns that have no native HTML equivalent. The APG provides keyboard interaction patterns and ARIA attribute requirements for common widget types: dialogs, comboboxes, tabs, trees, and menus. For each pattern, the APG specifies required ARIA roles, managed keyboard focus behavior, and `aria-` property requirements.

Key ARIA patterns most frequently implemented incorrectly:
- Modal dialogs: require focus trap within the dialog while open; restore focus to trigger on close
- Dynamic content: `aria-live` regions with appropriate `aria-atomic` and `aria-relevant` for announcements
- Form validation: use `aria-describedby` linking error messages to form fields; `aria-invalid="true"` on failing inputs

## The Overlay Anti-Pattern

Accessibility overlays are JavaScript products that claim to automatically fix accessibility issues on any website by injecting a widget layer. They include accessiBe, UserWay, AudioEye, and others.

**Why they don't work**: Overlays attempt to fix accessibility post-render by modifying the DOM after page load. They cannot reliably fix: semantic structure errors, keyboard traps, reading order problems, or dynamic content announcements. Screen reader users consistently report that overlays introduce new barriers rather than removing existing ones.

**Legal status**:
- FTC fined accessiBe $1 million in January 2025 (final order April 2025) for false claims that its overlay achieved automatic WCAG compliance
- Over 1,000 overlay-equipped websites faced lawsuits in 2024
- DOJ guidance is that overlays do not satisfy ADA requirements

**Organizations that have publicly opposed overlays**: National Federation of the Blind, Disability Rights Advocates, and over 600 accessibility practitioners who signed the Overlay Fact Sheet (overlayfactsheet.com).

## Design System Approach

Building accessibility into a shared component library prevents defects from propagating across products. Components that correctly implement semantic HTML, keyboard behavior, and ARIA patterns once become the source of truth for the entire organization. This scales accessibility investment — fixing a component library component fixes every place it is used.

Critical design system components to audit first: form inputs and validation, modal dialogs, navigation menus, buttons and links, notifications and alerts.

## Takeaway

Use semantic HTML as the default. Add ARIA only when no native element fits. Never purchase or deploy overlay products — they create legal liability and fail screen reader users. Build accessibility into components at the design system level; fixing it post-render via overlays has a proven failure record.
