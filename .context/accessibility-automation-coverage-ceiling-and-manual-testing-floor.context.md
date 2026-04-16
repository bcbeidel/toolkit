---
name: Accessibility Automation Coverage Ceiling and Manual Testing Floor
description: "Automated tools cover only 30–40% of WCAG criteria in open-source CI configurations; a three-tool CI stack (axe-core, Lighthouse, Pa11y) plus manual screen reader testing is required for meaningful coverage."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://github.com/dequelabs/axe-core
  - https://playwright.dev/docs/accessibility-testing
  - https://www.accesify.io/blog/accessibility-testing-automation-axe-pa11y-lighthouse-ci/
  - https://testparty.ai/blog/cicd-accessibility-integration-complete-developer-guide
related:
  - docs/context/wcag-2-2-legal-compliance-targets-and-new-aa-criteria.context.md
  - docs/context/semantic-html-first-and-overlay-anti-pattern.context.md
  - docs/context/ci-pipeline-test-layer-ordering-and-quality-gate-calibration.context.md
---
# Accessibility Automation Coverage Ceiling and Manual Testing Floor

## Key Insight

Automated accessibility tools do not close the compliance gap alone. Open-source axe-core covers approximately 30–40% of WCAG Success Criteria in CI configurations. The commonly-cited 57% figure is Deque's full commercial audit pipeline, not standalone axe-core. A three-tool CI stack plus manual screen reader testing is the minimum for credible WCAG 2.2 AA coverage.

## The Coverage Ceiling: Clarifying the 57% Figure

Two figures circulate: "30–40%" and "57%." Both are correct in different contexts:

- **30–40%**: counts the WCAG Success Criteria that automation can address (roughly 16 of 50 under WCAG 2.1 AA). This is the right frame for compliance gap analysis and reflects standalone axe-core in CI.
- **57%**: Deque's 2021 study measuring volume of real-world issues found across their full commercial audit suite (free browser extension + paid axe DevTools Pro + professional methodology). This is not reproducible by adding `axe.min.js` to a test suite.

Despite broad axe-core CI adoption, WebAIM 2026 data shows 94.8% of the top 1,000,000 home pages still have detected WCAG failures, averaging 51 errors per page — down only marginally from 95.9% in 2024. Automated CI adoption is not closing the compliance gap in practice.

## The Three-Tool CI Stack

Use all three tools in combination — they are complementary, not redundant:

**axe-core** (Deque, open-source): 100+ rules covering WCAG 2.0, 2.1, 2.2 at A/AA/AAA levels. The deepest WCAG violation detection. Powers Google Lighthouse and Accessibility Insights. Note: WCAG 2.2 rules are disabled by default; enable explicitly. Target-size rule may be the only WCAG 2.2 rule added to free axe-core; Focus Appearance and Focus Not Obscured detection require axe DevTools Pro (commercial).

**Lighthouse** (Google, open-source): Runs a subset of axe-core rules (~57 audits). Combines accessibility, performance, SEO, and best-practices scoring in one audit. Use for broad accessibility scoring and regression detection. Configure in CI with minimum score threshold (`'categories:accessibility': ['error', {minScore: 0.9}]`).

**Pa11y** (open-source): Lightweight CLI-based accessibility checker with built-in CI support. Supports multiple testing standards, generates readable JSON or HTML reports. Fastest to integrate for automated URL testing pipelines.

## Playwright + axe-core Integration

For component-level and page-level accessibility testing in Playwright test suites:
- Package: `@axe-core/playwright`
- `AxeBuilder.withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])` to scope to relevant criteria
- `AxeBuilder.include(selector)` to limit scope; `exclude(selector)` to suppress known issues
- Export violations as JSON for reporter integration; use snapshot testing to track known violations

## The Manual Testing Floor

Screen readers reveal what automated tools cannot. Criteria requiring manual testing include: reading order, keyboard traps, contextual link clarity, focus management in dynamic content, and the four new WCAG 2.2 AA criteria (Focus Not Obscured, Dragging Movements, Target Size, Accessible Authentication).

Recommended combinations:
- NVDA + Firefox or Chrome (Windows) — best free option
- JAWS + Chrome or Edge (Windows) — professional/enterprise standard
- VoiceOver + Safari (macOS/iOS) — required for Apple platform coverage

Testing rule: never use a mouse; rely only on what you can hear.

Key manual test patterns: heading hierarchy (h1→h2→h3, no skipped levels), landmark regions, form label associations, dynamic content announcements via `aria-live`.

## Takeaway

Automated tools are necessary but not sufficient. Deploy the three-tool CI stack for broad automated coverage, then schedule regular manual screen reader sessions for the 60–70% of criteria that automation cannot reach. Without manual testing, CI-green does not mean compliant.
