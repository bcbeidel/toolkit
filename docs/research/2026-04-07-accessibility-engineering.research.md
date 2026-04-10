---
name: "Accessibility Engineering"
description: "WCAG 2.2 (now ISO/IEC 40500:2025) is the current legal standard; open-source axe-core covers ~30–40% of WCAG criteria in CI; the remaining gap requires manual screen reader testing, shift-left design review, and organizational champions programs — all of which have documented failure modes the tooling literature underweights."
type: research
sources:
  - https://www.w3.org/WAI/standards-guidelines/wcag/
  - https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/
  - https://www.w3.org/press-releases/2025/wcag22-iso-pas/
  - https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/
  - https://www.w3.org/WAI/ARIA/apg/
  - https://www.deque.com/axe/axe-core/
  - https://github.com/dequelabs/axe-core
  - https://dequeuniversity.com/resources/wcag-2.2/
  - https://playwright.dev/docs/accessibility-testing
  - https://www.allaccessible.org/blog/wcag-22-complete-guide-2025
  - https://testparty.ai/blog/cicd-accessibility-integration-complete-developer-guide
  - https://testparty.ai/blog/screen-reader-testing-guide
  - https://www.accesify.io/blog/accessibility-testing-automation-axe-pa11y-lighthouse-ci/
  - https://www.accesify.io/blog/accessibility-design-systems-component-libraries/
  - https://rishikc.com/articles/accessibility-testing-ci-integration/
  - https://accessibility.civicactions.com/guide/champions-program
  - https://humanmade.com/accessibility/accessible-design-systems-scaling-inclusive-design/
  - https://www.numberanalytics.com/blog/accessibility-champions-leading-the-way
  - https://accessibility-test.org/blog/development/screen-readers/nvda-vs-jaws-vs-voiceover-2025-screen-reader-comparison/
  - https://khacreationusa.com/shift-left-the-strategic-economic-and-regulatory-imperative/
related:
---

# Accessibility Engineering

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.w3.org/WAI/standards-guidelines/wcag/ | WCAG 2 Overview | W3C / WAI | Updated May 2025 | T1 | verified |
| 2 | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | What's New in WCAG 2.2 | W3C / WAI | Oct 2023, Updated 2025 | T1 | verified |
| 3 | https://www.w3.org/press-releases/2025/wcag22-iso-pas/ | WCAG 2.2 Approved as ISO/IEC International Standard | W3C | 2025 | T1 | verified |
| 4 | https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/ | WCAG 3 Introduction | W3C / WAI | Sep 2025 | T1 | verified |
| 5 | https://www.w3.org/WAI/ARIA/apg/ | ARIA Authoring Practices Guide (APG) | W3C / WAI | Ongoing | T1 | verified |
| 6 | https://github.com/dequelabs/axe-core | axe-core GitHub Repository | Deque Systems | Ongoing (latest 2025) | T1 | verified |
| 7 | https://dequeuniversity.com/resources/wcag-2.2/ | WCAG 2.2 Updates - Accessibility Resources and Code Examples | Deque University | 2024-2025 | T1 | verified |
| 8 | https://playwright.dev/docs/accessibility-testing | Accessibility Testing — Playwright Docs | Playwright / Microsoft | 2025 | T1 | verified |
| 9 | https://www.allaccessible.org/blog/wcag-22-complete-guide-2025 | WCAG 2.2: Complete Compliance Guide 2025 | AllAccessible | 2025 | T2 | verified |
| 10 | https://testparty.ai/blog/cicd-accessibility-integration-complete-developer-guide | CI/CD Accessibility Integration: Complete Developer Guide | TestParty | 2025 | T3 | verified |
| 11 | https://testparty.ai/blog/screen-reader-testing-guide | Screen Reader Testing Guide: NVDA, JAWS, and VoiceOver | TestParty | 2025 | T3 | verified |
| 12 | https://www.accesify.io/blog/accessibility-testing-automation-axe-pa11y-lighthouse-ci/ | Accessibility Testing Automation — Integrating axe, Pa11y, and Lighthouse CI | Accesify | 2025 | T3 | verified |
| 13 | https://www.accesify.io/blog/accessibility-design-systems-component-libraries/ | Accessibility in Design Systems — Build Accessible Components | Accesify | 2025 | T3 | verified |
| 14 | https://rishikc.com/articles/accessibility-testing-ci-integration/ | Automated Accessibility Testing with axe-core, Playwright & GitHub Actions | Rishik Chaudhary | 2025 | T4 | verified |
| 15 | https://accessibility.civicactions.com/guide/champions-program | CivicActions' Accessibility Champions Program | CivicActions | 2025 | T2 | verified |
| 16 | https://humanmade.com/accessibility/accessible-design-systems-scaling-inclusive-design/ | Accessible Design Systems: Scaling Inclusive Design | Human Made | 2025 | T2 | verified |
| 17 | https://www.numberanalytics.com/blog/accessibility-champions-leading-the-way | Accessibility Champions: Leading the Way | Number Analytics | Jun 2025 | T4 | verified |
| 18 | https://accessibility-test.org/blog/development/screen-readers/nvda-vs-jaws-vs-voiceover-2025-screen-reader-comparison/ | NVDA vs JAWS vs VoiceOver: 2025 Screen Reader Comparison | accessibility-test.org | 2025 | T3 | verified |
| 19 | https://khacreationusa.com/shift-left-the-strategic-economic-and-regulatory-imperative/ | Shift Left: 2025 Accessibility Strategy | Kha Creation | 2025 | T4 | verified |
| 20 | https://dequeuniversity.com/rules/axe/4.6 | List of Axe 4.6 Rules | Deque University | 2024-2025 | T1 | verified |

## Evaluation

SIFT assessment per source group:

**T1 — Primary / Official (Sources 1-8, 20):**
- W3C/WAI (1-5): The definitive standard-setting body for WCAG and ARIA. No credibility concerns. All publications are authoritative. Note dates: sources 2-4 reflect 2025 updates (WCAG 2.2 ISO approval, WCAG 3 Working Draft). These are the ground truth.
- axe-core GitHub repo (6): Canonical source for the tool. README and CHANGELOG are authoritative for coverage claims and rule counts. Deque has commercial incentive to promote its tools but the repo data (rules, WCAG mapping) is factual.
- Deque University (7, 20): Deque created axe-core. Their documentation on axe rules and WCAG 2.2 coverage is authoritative for that tool's behavior. Deque has commercial products (axe DevTools Pro) — some claims distinguish free vs. paid features; this is disclosed in extracts.
- Playwright docs (8): Microsoft official documentation. Authoritative for the `@axe-core/playwright` API.

**T2 — Institutional / Established Practitioners (Sources 9, 15, 16):**
- AllAccessible.org (9): Specialty accessibility consultancy with detailed WCAG 2.2 breakdown. Implementation guidance is consistent with W3C sources — no conflicting claims found.
- CivicActions (15): US public sector digital services firm with a published, documented accessibility program. Champions program is real and actively maintained. T2 appropriate.
- Human Made (16): Established open-source WordPress agency. Design systems accessibility guidance aligns with W3C APG. T2 appropriate.

**T3 — Quality Secondary (Sources 10, 11, 12, 13, 18):**
- TestParty.ai (10, 11): Commercial testing platform. Content is practical and tool-specific but no author credentials visible; claim coverage ceiling ("30-40% of WCAG issues") diverges slightly from axe-core's own claim (57%). Treat statistics with caution; defer to T1 sources for coverage claims.
- Accesify.io (12, 13): Small accessibility consultancy blog. Content consistent with T1 sources; used for confirmatory triangulation only. No unique statistical claims relied upon.
- accessibility-test.org (18): Screen reader comparison is factual (NVDA/JAWS/VoiceOver features are verifiable). AI image description feature claims (NVDA AI, JAWS FSCompanion) require confirmation from primary tool documentation.

**T4 — Weak Secondary (Sources 14, 17, 19):**
- rishikc.com (14): Personal developer blog. Code examples and GitHub Actions YAML are technically consistent with T1 docs. Used only for configuration pattern triangulation; no unique claims adopted.
- Number Analytics (17): Analytics company blog — not a specialist source. ROI figure ("$1.40-$1.70 per dollar invested") is cited without original attribution. Trace needed (likely from Accenture or Forrester research). Treat as indicative; flagged for verifier.
- Kha Creation (19): Unknown US web firm. "80% reduction in issues within 8 months" and "50% cut in remediation time" statistics lack attribution. Do not use as primary evidence; used only for corroborating shift-left framing.

**SIFT Flags for Verifier / Challenger:**
1. Coverage ceiling claim: "57% of WCAG issues" (axe-core, T1) vs. "30-40%" (TestParty T3) — reconcile which is correct or context-dependent.
2. ROI figure "$1.40-$1.70 per dollar" — T4 source (Number Analytics), no original study cited. Needs chain-of-custody.
3. NVDA AI image descriptions and JAWS FSCompanion AI — 2025 feature claims from T3 source; verify against NVDA/JAWS release notes.
4. "80% reduction in 8 months" — T4 (Kha Creation), no case study cited. Treat as illustrative, not evidential.

## Challenge

### Counter-evidence and Complications

**1. The 57% coverage claim is tool-suite-specific, not a free axe-core figure.**
Deque's 2021 study (BusinessWire, March 10 2021) used "Deque's axe suite of tools, powered by the open-source axe-core rules library" — a formulation that encompasses both the free browser extension and commercial audit tooling. Deque later disclosed that axe DevTools Pro (paid) identifies 76–84% of issues through its Intelligent Guided Testing, while the free axe-core alone aligns more closely with the 30–40% floor reported by independent sources. The 57% figure is therefore a reasonable average across Deque's full commercial audit pipeline, not a claim that can be reproduced by dropping `axe.min.js` into a test suite. The document uses this figure in a context (CI integration with open-source axe-core) where the lower independent estimate is more applicable.

**2. Coverage ceiling framing differs by measurement method — neither figure is wrong.**
Search results confirm a genuine methodological split: the 30–40% figure counts WCAG Success Criteria that automation can address (roughly 16 of 50 under WCAG 2.1 AA per criteria-counting approaches); the 57% figure counts volume of detected issues across real audit data (common, automatable failures like missing alt text and low-contrast text are vastly over-represented in real-world page populations). Both are technically defensible. The 30–40% figure is not simply "weaker" — it accurately describes criteria coverage and is the right frame for compliance gap analysis. Presenting 57% without this context overstates what CI automation delivers.

**3. WebAIM Million 2025/2026 data shows automated tools are not closing the gap.**
The 2026 WebAIM Million report found that 94.8% of the top 1,000,000 home pages still had detected WCAG failures (down only marginally from 95.9% in 2024), averaging 51 errors per page. The most common error types — low contrast text (79.1% of pages), missing alt text, empty links — are precisely the ones automated tools detect well. Despite broad axe-core CI adoption, the overall compliance failure rate is essentially static. This complicates document claims that CI integration reliably "catches violations before they reach production."

**4. Accessibility champions programs carry well-documented failure modes the document underweights.**
Structured searches found that champions programs routinely fail due to: lack of executive sponsorship (the single biggest predictor of program collapse), champion burnout when accessibility work is unfunded on top of primary duties, skill atrophy without ongoing practice, and program collapse when trained champions leave the organization. The document (Sub-question 5) presents the program pattern with strong optimism and minimal discussion of these failure conditions. Sources: Level Access, AbilityNet, Fable.

**5. WCAG 2.2 focus appearance (AAA) is substantially harder to implement than presented.**
2.4.13 Focus Appearance is listed as a straightforward "AAA enhanced" criterion. In practice, implementation requires complex area calculations for non-rectangular focus indicators, and once any default browser outline styles are overridden, developers take on full WCAG responsibility for contrast compliance. The most common accessibility failure overall (WebAIM) is still inadequate focus styling, suggesting the design pattern guidance in Sub-question 3 is aspirational rather than descriptive of typical practice.

**6. Accessibility overlays are a significant counter-pattern not addressed.**
The FTC fined accessiBe $1 million in January 2025 (with final order April 2025) for claiming its overlay achieved automatic WCAG compliance. Over 1,000 overlay-equipped websites faced lawsuits in 2024. The document's CI/CD and organizational sections do not address the overlay anti-pattern, which is one of the most commercially prevalent "accessibility solutions" in the market today. Omitting this creates an incomplete picture of the organizational landscape.

---

### Limits of the Evidence

- **Implementation outcomes are not measured.** All sources describe process and tooling patterns; none provide longitudinal data on whether organizations following these patterns achieve and sustain WCAG 2.2 AA compliance over time. The champions program, CI integration, and design system guidance are all reasonable hypotheses, not demonstrated outcomes.
- **Enterprise bias.** The cited programs (CivicActions, GitHub Primer, GOV.UK, Adobe Spectrum) are large, well-resourced organizations. Findings about what "works" in these contexts do not translate directly to small or medium businesses, where the compliance costs ($10–35K for a first audit) are frequently prohibitive.
- **Screen reader testing guidance lacks user research grounding.** Sub-question 2 prescribes screen reader testing methodology (keyboard-only, heading hierarchy, landmark traversal) but all cited sources are practitioner guides, not studies of how disabled users actually interact with failing content. "Testing with actual disabled users" (mentioned once, in the GOV.UK reference) is presented as a best practice but not operationalized.
- **WCAG 3.0 timeline assumptions.** The document correctly states WCAG 3 is not near finalization, but does not address the risks of the WCAG 2.2 → WCAG 3 transition gap: WCAG 3 will introduce a substantially different scoring model (outcome-based rather than pass/fail), which could invalidate current compliance infrastructure investment.
- **No coverage of multi-language or non-English accessibility.** NVDA's on-device image description (when shipped) will initially support English only. The document's WCAG and screen reader guidance implicitly assumes English-language content.

---

### SIFT Flag Resolution

**Flag 1 — Coverage ceiling (57% vs. 30–40%):**
Resolved — both figures are correct in different contexts. The 30–40% figure counts WCAG Success Criteria addressable by automation; the 57% figure measures volume of real-world issues found in Deque audit data. Critically, the 57% figure derives from Deque's full axe suite (including commercial tooling and professional audit methodology), not the standalone axe-core library. Documents using the 57% figure in the context of free/open-source CI integration are overstating what axe-core alone delivers. Recommend the document qualify: "57% using Deque's full axe suite; ~30–40% of WCAG criteria coverage for standalone axe-core in CI."

**Flag 2 — ROI figure "$1.40–$1.70 per dollar":**
Unresolved — original source not found. The specific range does not appear in Accenture's "Getting to Equal: The Disability Inclusion Advantage" (2018), which reported 28% higher revenue and 2.6x shareholder returns for disability inclusion leaders — a different metric. The most commonly cited accessibility ROI figure in current circulation is a Forrester Research estimate of "$100 for every $1 invested," which is a different order of magnitude. The $1.40–$1.70 figure appears to originate from a source that is no longer traceable through current web searches. The Number Analytics T4 source that carries this figure should be removed from evidential use; it cannot be verified.

**Flag 3 — NVDA AI image descriptions and JAWS FSCompanion AI:**
Partially resolved, with important corrections needed.
- *NVDA*: On-device AI image description is in alpha as of October 2025 and planned for stable release in NVDA 2026.1. It is **not** a shipped 2025 feature. The claim in Sub-question 2 ("NVDA added AI-powered image descriptions" in 2025) is premature — the feature is in alpha-only builds that require NVDA 2026.1 pre-release and are incompatible with existing add-ons. Third-party add-ons (e.g., AI Content Describer by Carter Temm) have provided this functionality via cloud APIs for longer, but that is not native NVDA functionality.
- *JAWS FSCompanion*: Confirmed as a real, shipped feature in JAWS 2025 (released October 30, 2024). However, FSCompanion is an AI assistant that answers questions about *how to use JAWS and Microsoft applications* — it is a help/training AI, not an AI image description engine within JAWS itself. The document's framing implies FSCompanion is an accessibility enhancement for end users consuming content; its actual function is a JAWS-user productivity tool for learning the software. This is a material mischaracterization.

**Flag 4 — Shift-left ROI statistics ("80% reduction in 8 months", "50% cut in remediation time"):**
Partially resolved. The statistic traces to a Siteimprove blog post (June 16, 2025) citing a webinar case study featuring Valentina Tarantini, technology consultant and lead of the accessibility initiative at Merkle, a digital marketing agency. This moves it from T4 (unknown web firm) to T3 (secondary source citing a named practitioner case study), but it remains a single company's self-reported outcome from one practitioner's webinar presentation, with no independently audited methodology. The Kha Creation source (T4) appears to have cited the same statistic without attribution. The 80%/50% figures are real but remain a single unaudited case study rather than a generalizable finding. Recommend retaining as "illustrative case study (Merkle/Siteimprove, 2025)" rather than citing as an industry benchmark.

---

### Commercial Bias Notes

- **Deque Systems** (Sources 6, 7, 20): The 57% coverage figure originated in a Deque press release (March 2021) timed to coincide with the launch of axe DevTools Pro (March 2021, separate BusinessWire announcement). Deque measured their own tools against their own audit data, then published the result as a study. No external peer review is documented. The figure has since been widely reprinted as an independent benchmark, which it is not. Deque's commercial incentive is to maximize the perceived coverage ceiling of automation to sell their paid tooling.
- **TestParty.ai** (Sources 10, 11): Commercial testing platform with a SaaS product. All content on their blog functions as lead generation. Their "$67% lower compliance costs" for shift-left adopters is not sourced to any study.
- **Number Analytics** (Source 17): Analytics services company with no stated expertise in accessibility. The ROI figure "$1.40–$1.70 per dollar" appears on their blog without original attribution; it is plausible they synthesized or misrepresented a figure from a paywalled Forrester or Accenture report.
- **Kha Creation** (Source 19): Unknown US web firm; blog content is likely SEO-oriented. Statistics are repeated without sourcing.
- **Level Access, Siteimprove, Deque** (webinar and blog content throughout): All have commercial products for accessibility programs, CI tooling, and champion training. Their organizational guidance is sound but directionally self-serving — each recommends tooling investment in areas where they have products.

## Search Protocol

| # | Query | Tool | Results | Used |
|---|-------|------|---------|------|
| 1 | WCAG 2.2 guidelines implementation 2025 web accessibility | WebSearch | 10 | Y |
| 2 | automated accessibility testing axe-core Lighthouse 2025 | WebSearch | 10 | Y |
| 3 | accessible design patterns inclusive UI components 2025 | WebSearch | 10 | Y |
| 4 | accessibility CI/CD pipeline integration GitHub Actions 2025 | WebSearch | 10 | Y |
| 5 | organizational accessibility program champions audits training 2025 | WebSearch | 10 | Y |
| 6 | WCAG 2.2 new success criteria focus appearance authentication cognitive 2024 2025 | WebSearch | 10 | Y |
| 7 | axe-core WCAG 2.2 rules coverage 2025 Deque | WebSearch | 10 | Y |
| 8 | screen reader testing NVDA JAWS VoiceOver accessibility 2025 methodology | WebSearch | 10 | Y |
| 9 | accessibility design review process shift-left developer workflow 2025 | WebSearch | 10 | Y |
| 10 | ARIA authoring practices guide APG W3C keyboard patterns 2024 2025 | WebSearch | 10 | Y |
| 11 | WCAG 3.0 status timeline 2025 W3C accessibility guidelines | WebSearch | 10 | Y |
| 12 | https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ | WebFetch | N/A | Y |
| 13 | https://github.com/dequelabs/axe-core | WebFetch | N/A | Y |
| 14 | https://playwright.dev/docs/accessibility-testing | WebFetch | N/A | Y |
| 15 | https://testparty.ai/blog/cicd-accessibility-integration-complete-developer-guide | WebFetch | N/A | Y |
| 16 | https://www.accesify.io/blog/accessibility-testing-automation-axe-pa11y-lighthouse-ci/ | WebFetch | N/A | Y |
| 17 | https://accessibility.civicactions.com/guide/champions-program | WebFetch | N/A | Y |
| 18 | https://humanmade.com/accessibility/accessible-design-systems-scaling-inclusive-design/ | WebFetch | N/A | Y |
| 19 | https://testparty.ai/blog/screen-reader-testing-guide | WebFetch | N/A | Y |
| 20 | https://www.accesify.io/blog/accessibility-design-systems-component-libraries/ | WebFetch | N/A | Y |
| 21 | https://www.numberanalytics.com/blog/accessibility-champions-leading-the-way | WebFetch | N/A | Y |
| 22 | https://rishikc.com/articles/accessibility-testing-ci-integration/ | WebFetch | N/A | Y |
| 23 | https://dequeuniversity.com/resources/wcag-2.2/ | WebFetch | N/A | Y |
| 24 | https://www.allaccessible.org/blog/wcag-22-complete-guide-2025 | WebFetch | N/A | Y |
| 25 | https://www.w3.org/WAI/standards-guidelines/wcag/ | WebFetch | N/A | Y |

## Extracts

### Sub-question 1: WCAG Guidelines 2.2+

**Standard Status and Versions [1][2][3]:**
- WCAG 2.2 was published as a W3C Recommendation on October 5, 2023, with updates on December 12, 2024, and May 6, 2025.
- In 2025, WCAG 2.2 was approved as ISO/IEC 40500:2025, making it an international standard [3].
- WCAG 2.2 is "backwards compatible": content conforming to WCAG 2.2 also conforms to WCAG 2.1 and WCAG 2.0. Targeting 2.2 automatically satisfies all earlier versions [1].
- W3C official guidance: "W3C encourages using the latest WCAG version." [1]

**WCAG 2.2: 9 New Success Criteria [2][7][9]:**

The 9 new criteria are organized across three conformance levels:

Level A (mandatory baseline):
- **3.2.6 Consistent Help (A):** "Put help in the same place when it is on multiple pages." Help mechanisms (chat widget, support link) must appear in consistent relative order across pages where repeated.
- **3.3.7 Redundant Entry (A):** "Don't ask for the same information twice in the same session." Previously entered information must be auto-populated or selectable. Implementation: use `autocomplete` attributes, "same as shipping address" checkboxes.

Level AA (legal compliance standard for most regulations):
- **2.4.11 Focus Not Obscured (Minimum) (AA):** "Ensure when an item gets keyboard focus, it is at least partially visible." Components must not be entirely hidden by sticky headers, modals, or overlays. CSS fix: `html { scroll-padding-top: 100px; } *:focus { scroll-margin-top: 120px; }` [9]
- **2.5.7 Dragging Movements (AA):** "For any action that involves dragging, provide a simple pointer alternative." All drag-and-drop needs alternatives: arrow buttons for sortable lists, browse buttons for file uploads, +/- buttons for sliders.
- **2.5.8 Target Size (Minimum) (AA):** "Ensure targets meet a minimum size or have sufficient spacing around them." Interactive targets must be 24×24 CSS pixels or positioned with adequate spacing. Covers buttons, links, form inputs — essential for mobile.
- **3.3.8 Accessible Authentication (Minimum) (AA):** "Don't make people solve, recall, or transcribe something to log in." Must enable password managers (`autocomplete="current-password"`), offer email/SMS codes, or use reCAPTCHA v3 rather than text CAPTCHAs.

Level AAA (enhanced, not universally required):
- **2.4.12 Focus Not Obscured (Enhanced) (AAA):** No part of the focused element may be hidden by any author-created content.
- **2.4.13 Focus Appearance (AAA):** Focus indicators must be at least 2 CSS pixels thick with 3:1 contrast ratio between focused and unfocused states. Practical implementation: `outline: 3px solid #0066CC` with offset.
- **3.3.9 Accessible Authentication (Enhanced) (AAA):** No cognitive function tests at all — stricter version with fewer exceptions than Minimum.

**Removed Criterion [7]:**
- Success Criterion 4.1.1 (Parsing) was removed from WCAG 2.2 — it is "always satisfied for any content using HTML or XML."

**WCAG 2.2 Level AA is the current legal standard [1][9]:**
- European Accessibility Act (EAA) went into force June 28, 2025, requiring WCAG 2.2 Level AA compliance across EU product/service categories.
- US ADA litigation references WCAG 2.2 AA as the de facto standard.
- UK public sector: full WCAG 2.2 Level AA compliance required as of June 2025.

**WCAG 3.0 Status [4]:**
- WCAG 3 remains a Working Draft as of September 2025 — not finalized.
- "WCAG 3 will not supersede WCAG 2 and WCAG 2 will not be deprecated for at least several years after WCAG 3 is finalized."
- Draft Candidate Recommendation planned for Q4 2027; full standard not before 2028.
- Current guidance: implement WCAG 2.2, not WCAG 3.

**Implementation Priority Order [9]:**
- Week 1-2 (Critical): Target size (2.5.8), Redundant entry (3.3.7), Consistent help (3.2.6)
- Week 3-4 (Important): Accessible authentication (3.3.8), Dragging alternatives (2.5.7)
- Week 5-6 (Enhanced): Focus not obscured (2.4.11)
- Total implementation timeline: simple sites 2-3 weeks, moderate 4-8 weeks, complex web apps 2-3 months.

**POUR Principles (foundational, from WCAG 2.x) [1]:**
WCAG is organized around 4 principles: Perceivable, Operable, Understandable, Robust. Each has guidelines, each guideline has testable success criteria at A/AA/AAA levels.

---

### Sub-question 2: Automated Accessibility Testing

**The Coverage Ceiling [6][2][10]:**
- "Automated tools detect approximately 40% of WCAG 2.2 issues" — manual testing required for focus visibility, consistent help, redundant entry, and authentication [1].
- axe-core specifically "detects on average 57% of WCAG issues automatically" [6].
- The remaining 40-60%+ "require manual testing" including reading order, keyboard traps, contextual clarity.
- "Automated scanning catches approximately 30-40% of WCAG issues" per broader industry consensus [11][12].

**axe-core [6][7]:**
- Open-source accessibility testing engine by Deque. Powers Google Lighthouse (since 2017) and Accessibility Insights.
- Covers WCAG 2.0, 2.1, and 2.2 at levels A, AA, and AAA, plus best practice checks.
- Rule count: approximately 100+ rules; axe DevTools Pro runs ~96+ rules; Lighthouse runs only a subset (~57 audits).
- Key limitation for WCAG 2.2: "Because of how few new success criteria in WCAG 2.2 can be automated without false positives, the `target-size` rule is likely the only rule for WCAG 2.2 that will be added to axe-core." Tests for Focus Appearance and Focus Not Obscure are only available in axe DevTools Pro (commercial tier).
- WCAG 2.2 rules are "disabled by default, until WCAG 2.2 is more widely adopted."
- Primary API: include `axe.min.js`, call `axe.run()` at relevant UI states, process `violations`, `passes`, and `incomplete` results via Promise-based API.
- Integration: axe-linter VSCode extension for early-stage detection; browser extension for guided testing; `@axe-core/playwright` for Playwright test suites.

**Google Lighthouse [12]:**
- Built on axe-core but runs subset of rules (~57 vs 100+ for full axe-core).
- Examines performance, best practices, SEO, and accessibility in one audit.
- Configuration: `.lighthouserc.js` with `'categories:accessibility': ['error', {minScore: 0.9}]` for score gating.
- CLI: `npm install -g @lhci/cli`; integrates into CI via `lhci autorun`.

**Pa11y [12]:**
- "Lightweight CLI-based accessibility checker" with built-in CI support.
- Supports multiple testing standards, generates readable reports in JSON or HTML.
- Configuration: `.pa11yci` config file specifying URLs and WCAG standard (e.g., `WCAG2AA`).
- CLI: `npm install -g pa11y-ci`

**Playwright + axe-core Integration [8][14]:**
- Package: `@axe-core/playwright` — runs axe as part of Playwright test suites.
- `AxeBuilder` class methods:
  - `include(selector)` — limit scan scope to specific page sections
  - `exclude(selector)` — remove elements from scan
  - `withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])` — filter by WCAG criteria
  - `disableRules(['rule-id'])` — suppress specific rules
  - `analyze()` — execute scan in current page state
- CI integration: use `testInfo.attach()` to export scan results as JSON for reporter integration; snapshot testing to fingerprint known violations.
- "Automated accessibility tests can detect some common problems, but manual assessment remains essential for comprehensive WCAG 2.1 AA compliance." [8]

**Screen Reader Testing [11][18]:**
- Screen readers reveal what automated tools miss — "real assistive technology testing reveals how users actually experience your site." [11]
- Recommended combinations [11]:
  - NVDA + Firefox or Chrome (Windows) — best free option; catches majority of issues
  - JAWS + Chrome or Edge (Windows) — professional/enterprise standard
  - VoiceOver + Safari (macOS/iOS) — required for Apple platform coverage
- 2025 advancements: NVDA added AI-powered image descriptions; JAWS introduced FSCompanion AI assistant [18].
- Testing rule: "NEVER use a mouse, rely ONLY on what you can hear." [11]
- Key test patterns:
  - Heading hierarchy: verify logical progression (h1 → h2 → h3) with no skipped levels
  - Landmark regions: confirm main, nav, aside, footer landmarks exist and are labeled
  - Reading order: test element sequencing matches visual layout
  - Form labels: fields must have associated labels (explicit or implicit)
  - Dynamic content: `aria-live` regions announce changes; modal dialogs trap focus
- Screen readers cannot be effectively automated in CI for full coverage — manual testing sessions are required.

**Tool Comparison Summary [10][12]:**
- axe-core vs Lighthouse: "Since Lighthouse actually uses axe-core as its accessibility engine, the question isn't really 'which is better' — it's 'which fits your workflow.'"
- For CI gating: use all three tools in combination — axe-core for deep WCAG violation detection, Lighthouse for broad accessibility scoring, Pa11y for CLI-based reporting.

---

### Sub-question 3: Inherently Accessible Design Patterns

**Semantic HTML First Principle [13]:**
- "Select HTML elements that convey functionality natively — `<button>`, `<nav>`, `<ul>` — before applying ARIA." Native-first approach reduces complexity and ensures built-in AT compatibility.
- ARIA is for extending semantics of HTML, not replacing them. The W3C APG states: roles, states, and properties supplement, they don't substitute.

**ARIA Authoring Practices Guide (APG) [5]:**
- W3C resource that teaches how to "apply accessibility semantics to common design patterns and widgets."
- Covers: keyboard interface development, ARIA roles/states/properties, accessible names and descriptions, landmark regions.
- Each pattern provides working examples demonstrating one or more implementation methods.
- Key interactive patterns documented: accordion, alert, breadcrumb, button, carousel, checkbox, combobox, dialog, disclosure, feed, grid, link, listbox, menu/menubar, meter, radio group, slider, spinbutton, switch, table, tabs, toolbar, tooltip, tree/treegrid.

**ARIA Component Patterns [13]:**
- Buttons: use `aria-pressed` (toggle) or `aria-expanded` (disclosure) to convey state.
- Modals/Dialogs: apply `role="dialog"`, trap focus within the dialog, return focus on close.
- Navigation menus: follow APG menu pattern; support arrow key navigation, Escape to close.
- Forms: use semantic `<label>` associations; group related fields with `<fieldset>`/`<legend>`.
- Tabs: implement APG tab pattern with `role="tablist"`, `role="tab"`, `role="tabpanel"`, and arrow key navigation.
- Custom widgets: "dynamic states (expanded, pressed, checked) must sync visually and programmatically."

**Keyboard and Focus Management [13][16]:**
- Every interactive component requires full keyboard operability with "visible focus indicators and logical tab order."
- Composite widgets (menus, trees, grids) use arrow keys for internal navigation — tab moves between composites, not within them (APG "roving tabindex" pattern).
- Focus capture: modal dialogs trap focus inside; on close, focus returns to the trigger element.
- Avoid `outline: none` or `outline: 0` — focus indicators must always be visible.

**Design Systems as Accessibility Infrastructure [16]:**
- "Design systems eliminate inconsistency by establishing a single source of truth. When accessibility is built into reusable, tested components, compliance naturally scales."
- Leading systems (GOV.UK, GitHub Primer, Adobe Spectrum) embed accessibility in reusable components: "once solved, distributed everywhere."
- GitHub Primer emphasizes "progressive enhancement, assistive technology documentation, and automated accessibility testing."
- GOV.UK "tests with actual disabled users" — real user testing over purely automated validation.
- Enforce guardrails in design tokens: color contrast ratios, minimum touch targets (44×44px recommended by WCAG, 24×24px minimum), semantic typography scale.

**Documentation as Part of the Pattern [16]:**
- "Embed accessibility guidance directly in design system documentation, covering WCAG mappings, keyboard interactions, screen reader expectations, and contrast compliance for each component."
- Distinguish design guidance, development guidance, and content guidance separately for each component.

**Color and Contrast [9][16]:**
- WCAG 2.2 requires 3:1 contrast ratio for focus indicator state changes.
- Regular text: 4.5:1 (AA) / 7:1 (AAA); large text: 3:1 (AA).
- Design tokens enforce color decisions: codify accessible palettes, prevent ad hoc color choices.

**Touch Targets [2][9]:**
- WCAG 2.5.8 (AA): minimum 24×24 CSS pixels for interactive targets.
- Best practice (and Apple HIG / Google Material): 44×44px minimum for comfortable touch interaction.
- Add padding rather than increasing visual size where visual design constraints exist.

**Cognitive Accessibility Patterns [9]:**
- 3.3.7 Redundant Entry: auto-populate previously entered data, use address copy checkboxes.
- 3.3.8 Accessible Authentication: eliminate CAPTCHAs requiring transcription/recognition; use magic links, passkeys, or reCAPTCHA v3.
- Error messages: identify the specific field, describe what went wrong, suggest a correction.
- Plain language: short sentences, active voice, common words, defined jargon.

---

### Sub-question 4: Accessibility in CI/CD and Design Review

**Business Case for CI Integration [10]:**
- "Integrating accessibility testing into your CI/CD pipeline catches violations before they reach production, reducing remediation costs by up to 100x compared to post-deployment fixes."
- Organizations implementing shift-left approaches have achieved "an 80 percent reduction in accessibility issues within 8 months, a 50 percent cut in remediation time." [19]

**Three Gating Strategies [10]:**

1. **Gatekeeper Pattern (Blocking):** Prevents merge when accessibility violations exist. Fails the workflow on any violation. Best for compliant codebases with zero-tolerance policies.

2. **Advisory Pattern (Warning):** Reports violations without blocking merges. Use `continue-on-error: true`. Useful during adoption phases or when clearing existing violation backlogs.

3. **Hybrid Pattern:** Combines both — critical violations block merges, secondary issues generate warnings. Enables gradual adoption while protecting against severe accessibility regressions.

**GitHub Actions Configuration [10][14]:**

Basic GitHub Actions workflow structure for accessibility testing:
```yaml
name: Accessibility Checks
on:
  pull_request:
    branches: [main, develop]
  push:
    branches: [main]

jobs:
  accessibility:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - name: Install dependencies
        run: npm ci
      - name: Run accessibility tests
        run: npm run test:a11y
```

For applications requiring a running server:
```yaml
- name: Start server
  run: npm run start &
- name: Wait for server
  run: npx wait-on http://localhost:3000
```

axe-core + Playwright specific integration [14]:
- Install: `npm install @axe-core/playwright`
- Configure severity thresholds to fail on critical/serious violations
- Use `if: failure()` condition to post violation reports as PR comments
- Posts violation reports as PR comments for developer visibility during code review

**Tool Configurations for CI [12]:**

Lighthouse CI threshold:
```js
// .lighthouserc.js
'categories:accessibility': ['error', {minScore: 0.9}]
```

Pa11y CI configuration:
```
// .pa11yci
{
  "standard": "WCAG2AA",
  "urls": ["http://localhost:3000"],
  "reporters": ["json"]
}
```

**Testing Scope Strategy [10]:**
- Component-level: fast feedback on individual UI elements (seconds) — run on every commit
- Critical paths: full-page integration tests on business-critical workflows (minutes) — run on every PR
- Complete coverage: scheduled nightly or weekly full-site scans (extended runs)
- Run accessibility checks in parallel with unit/integration tests to keep CI times low.

**Design Review Integration [19]:**
- "Shift Left" paradigm: move accessibility validation from QA phase to earliest design and requirements stages.
- Design phase tooling: Figma A11y Annotation Kit to mark heading levels, reading order, and interactive elements before handoff to developers.
- Contrast validation plugins run inside design tools (Figma, Sketch) during design — not after development.
- Annotation requirements: heading hierarchy, ARIA labels, focus order, alt text intent, interactive states.

**PR and Reporting [10]:**
- **PR Comments**: report violations directly in pull requests with element selectors and remediation suggestions.
- **Slack Integration**: alert teams on workflow failures using GitHub Actions webhooks.
- **Dashboard Tracking**: monitor violation trends over time for organizational visibility.

**Section 508 / Government Context [source not directly fetched but referenced in search]:**
- Section508.gov provides guidance on incorporating accessibility conformance within development processes — relevant for US federal contractors.

---

### Sub-question 5: Organizational Patterns for Sustained Accessibility

**Accessibility Champions Programs [15][17]:**

CivicActions program structure [15]:
- "It takes company-wide effort" to embed accessibility — distributes responsibility beyond specialists.
- Recruitment: all staff encouraged to volunteer; teams determine their own champion count (1 or multiple).
- Ideal profile: self-directed, team-attuned, action-oriented; interest in learning, coaching, problem-solving, systems thinking.

Three-level progression system [15]:
- **Level 1:** Basic knowledge with enthusiasm; articulate importance, identify common issues.
- **Level 2:** Analyze multi-component accessibility and recommend solutions; pursue certifications (CPACC, WAS, Trusted Tester).
- **Level 3:** Evaluate products systemically; mentor teammates; innovate practice area approaches; engage external communities.

Champion responsibilities [15][17]:
- "Acts as a conduit of information between the Accessibility Practice Area and functional/client teams."
- Raises accessibility issues in meetings; audits projects for improvement opportunities.
- Ensures automated testing integration (axe-core, Pa11y) in team CI pipelines.
- Coordinates accessibility code reviews; builds acceptance criteria and checklists.
- Leads accessibility workshops for new hires.

**Strategic Organizational Model [17]:**
1. Business case development → leadership alignment → team formation → execution
2. Develop "comprehensive plans including clear goals and objectives for accessibility, current assessments, gap-closure strategies, success metrics, and implementation timelines."
3. "Identify and involve employees, customers, and partners in accessibility efforts."

**Measurable Outcomes [17]:**
- Website accessibility compliance scores (quantitative)
- Employee knowledge assessments before/after training
- Customer satisfaction surveys for accessibility usability
- Accessibility complaint reduction metrics
- ROI: cited range of "$1.40 to $1.70 per dollar invested" in accessibility

**Audit Practices [17][15]:**
- Regular accessibility audits using "a combination of automated and manual testing methods."
- Automated: axe-core, Pa11y, Lighthouse for coverage baseline.
- Manual: screen reader testing (NVDA/JAWS/VoiceOver), keyboard-only navigation, cognitive walkthroughs.
- Champion role: "auditing projects for improvement opportunities" is a named duty, not a specialist-only function.

**Training and Onboarding [15][17]:**
- "Structured onboarding training for new employees" by champions.
- Training scope: accessibility laws and regulations (ADA, EAA), WCAG standards, common failure patterns, tool usage.
- Certifications referenced: CPACC (Certified Professional in Accessibility Core Competencies), WAS (Web Accessibility Specialist), Trusted Tester.
- Level Access Academy offers an "Accessibility Champion certification program" [referenced in search results].

**Sustaining Accessibility Culture [15][16]:**
- Regular practice area calls and Slack/team engagement to maintain momentum.
- Cross-functional relationship-building reduces silos.
- "Accessibility becomes an organizational culture, not merely a compliance checklist." [16]
- Celebrate documented progress and successes to reinforce behavior.
- Continuously review and update accessibility plans; incorporate feedback-driven improvements.
- Emerging governance models: design system owners maintain accessible components, reducing per-team burden.

**Common Failure Patterns [15][17]:**
- Treating accessibility as a final-phase QA check rather than a continuous practice.
- Relying solely on automated tools (which cover only 30-57% of issues).
- No ownership — accessibility "belongs to everyone" without explicit champions fails in practice.
- One-time training with no follow-up: accessibility skills decay without ongoing practice.

## Findings

### 1. WCAG 2.2 Guidelines and Systematic Implementation

WCAG 2.2 is the current mandatory standard, now ISO/IEC 40500:2025, with Level AA being the legal compliance target for the EU (EAA, June 2025), US (ADA enforcement), and UK public sector (HIGH — T1 sources [1][2][3] converge). WCAG 3.0 remains a Working Draft with no projected finalization before 2028 and will not supersede WCAG 2.2 for at least several years after that; organizations should implement 2.2 now rather than waiting (HIGH — W3C explicitly states this [1][4]).

The 9 new success criteria in WCAG 2.2 are backwards-compatible with 2.0 and 2.1. At Level AA, four new criteria require systematic implementation: Focus Not Obscured (2.4.11), Dragging Movements (2.5.7), Target Size Minimum (2.5.8), and Accessible Authentication Minimum (3.3.8) (HIGH — [2][7][9]). Of these, target size (2.5.8) and accessible authentication (3.3.8) represent the most common implementation gaps in existing products. The practical CSS fix for focus obscurance — `scroll-padding-top` / `scroll-margin-top` — is straightforward, but implementation varies across sticky header designs (MODERATE — practitioner guidance [9]; not independently validated at scale).

**Counter-evidence:** WCAG 2.4.13 Focus Appearance (AAA) is more complex than its non-required status implies. Any override of default browser focus styles transfers full contrast compliance responsibility to the developer, and inadequate focus styling remains one of the most prevalent failures in the WebAIM Million 2026 report (94.8% of top million pages still fail WCAG). This suggests that even WCAG 2.2 AA compliance is aspirational for most of the web despite the standard being well-established (HIGH — WebAIM Million 2026).

**Recommended implementation order:** Target Size → Redundant Entry → Consistent Help (Weeks 1-2), then Accessible Authentication → Dragging Movements (Weeks 3-4), then Focus Not Obscured (Weeks 5-6) — sourced from practitioner guidance [9], not W3C, so treat as indicative (MODERATE).

---

### 2. Automated Accessibility Testing

Automation coverage has a ceiling that must be correctly framed. The 30–40% figure represents the percentage of WCAG Success Criteria that any automated tool can address (roughly 16 of 50 under WCAG 2.2 AA). The widely-cited 57% figure (Deque) measures volume of real-world detected issues in Deque's full commercial audit suite — not standalone open-source axe-core in a CI pipeline. For a team using free axe-core in CI, 30–40% criteria coverage is the honest expectation (HIGH — reconciled from T1 sources [6][7] and challenger analysis).

axe-core is the canonical open-source accessibility testing engine, embedded in Playwright, Lighthouse, and Accessibility Insights [6][8]. Its WCAG 2.2-specific rules are limited: the `target-size` rule is likely the only freely available WCAG 2.2 rule; Focus Appearance and Focus Not Obscured checks require the commercial axe DevTools Pro tier [6][7]. This means CI automation alone cannot verify the most novel WCAG 2.2 AA criteria (MODERATE — Deque documentation, commercial interest acknowledged).

The three-tool CI stack — axe-core (deep WCAG violation detection), Lighthouse (overall accessibility score), Pa11y (CLI reporting) — is the established best practice for layered coverage [10][12]. Playwright's `@axe-core/playwright` integration enables in-test accessibility assertions with scope filtering (`include`, `exclude`, `withTags`) [8]. Testing scope should tier by cadence: component-level on every commit, critical-path integration on every PR, full-site scans on a nightly schedule [10] (MODERATE — practitioner guidance; independent validation limited).

Screen reader testing with NVDA+Firefox, JAWS+Chrome, VoiceOver+Safari covers the primary AT matrix [11]. These tests are irreducibly manual — no CI runner can replicate the human experience of navigating by headings, forms, and landmark regions. The most important test pattern is keyboard-only navigation: tab through the entire UI without a mouse, verifying focus visibility and logical order (HIGH — consistent across T1/T2/T3 sources [5][8][11]).

**Correction:** The NVDA "AI-powered image descriptions" claim in the Extracts refers to an alpha feature (planned NVDA 2026.1), not a shipped 2025 capability. JAWS FSCompanion is a real JAWS 2025 feature but is a help AI for JAWS users learning the software, not an in-stream content accessibility enhancement (HIGH — challenger research, per NVDA/Freedom Scientific primary sources).

**Counter-evidence:** The WebAIM Million 2026 data shows 94.8% of homepages still fail WCAG despite broad axe-core CI adoption. Automated CI integration is not sufficient on its own to close the compliance gap at scale — it catches regressions but does not address the underlying deficit in how interfaces are designed (HIGH — WebAIM Million 2026, T1-equivalent).

---

### 3. Inherently Accessible Design Patterns

The foundational principle is semantic HTML first: use `<button>`, `<nav>`, `<ul>`, `<label>` before reaching for ARIA (HIGH — W3C WAI, APG [5]). Native HTML elements carry built-in keyboard behavior, accessibility tree roles, and AT compatibility that custom ARIA implementations must laboriously replicate. When ARIA is needed, the W3C Authoring Practices Guide (APG) provides authoritative patterns for every major widget type (accordion through tree/treegrid), each with working code examples and keyboard interaction specifications [5] (HIGH).

Keyboard and focus management patterns: every interactive element needs a visible focus indicator; composite widgets (menus, trees, grids) use the roving tabindex pattern for internal arrow key navigation; modal dialogs must trap focus on open and return it to the trigger on close [5][13][16] (HIGH — APG is T1; implementation quality varies in practice). The design rule "never set `outline: none` or `outline: 0`" is absolute — doing so breaks keyboard navigation for all users who cannot use a mouse (HIGH).

Design systems multiply the value of accessible patterns: an accessible component built once and distributed through a shared library reaches every team without per-team accessibility expertise [16]. Well-resourced systems like GOV.UK, GitHub Primer, and Adobe Spectrum demonstrate this model working at scale, but all three are large organizations with dedicated accessibility engineers — the pattern is harder to sustain for smaller teams without equivalent investment (MODERATE — Human Made T2 [16]; challenger notes enterprise bias in the evidence).

For WCAG 2.2 specifically: enforce 24×24px minimum touch targets via design tokens; auto-populate form fields using `autocomplete` attributes to satisfy Redundant Entry (3.3.7); eliminate text CAPTCHAs and use passkeys, magic links, or reCAPTCHA v3 for Accessible Authentication (3.3.8) [2][9] (HIGH — W3C spec requirements, not practitioner opinion).

Color contrast: 4.5:1 for normal text, 3:1 for large text and focus indicator state changes [9]. Design tokens enforcing these ratios in a shared palette prevent ad hoc violations before code is written (MODERATE — practitioner guidance; no independent outcome data on token-based enforcement).

---

### 4. Accessibility in CI/CD and Design Review

Three gating strategies are available: blocking (fail the build on any violation), advisory (report without blocking), and hybrid (block on critical/serious violations only) [10]. The hybrid pattern is the practical entry point for teams adopting accessibility CI: it prevents severe regressions while allowing teams to address existing backlogs without constant build failures. Once the violation backlog is cleared, shifting to blocking is the goal (MODERATE — practitioner guidance [10][14]; not independently validated at scale).

The standard CI integration pattern pairs axe-core or axe-core/playwright with a GitHub Actions workflow, using `continue-on-error` to toggle between advisory and blocking modes [10][14]. Lighthouse CI provides accessibility score gating (`minScore: 0.9`) as a complementary threshold-based check [12]. PR comment reporting — posting violation selectors and remediation hints directly in the pull request — has emerged as the most developer-facing delivery pattern for actionable feedback [10].

The "shift-left" design review integration — annotating Figma files with heading levels, reading order, ARIA labels, and focus order before handoff — is the most impactful intervention point in the development lifecycle. Contrast validation in design tools (Figma plugins) before any code is written is dramatically cheaper than post-development remediation [19] (MODERATE — principle well-supported; the specific statistics from T4 sources [19] citing "80% reduction in 8 months" trace to a single unaudited Merkle/Siteimprove case study and should not be treated as industry benchmarks).

**Counter-evidence:** WebAIM Million 2026 shows that broad CI tool adoption has not produced measurable population-level compliance improvement. CI accessibility checks are effective at preventing regressions on pages already in the pipeline but do not reach legacy content, third-party embeds, dynamically generated pages, or content created through CMS interfaces. This creates a gap that CI alone cannot bridge.

---

### 5. Organizational Patterns for Sustained Accessibility

The Accessibility Champions model — embedding accessibility advocates within delivery teams with structured skill progression — is the predominant organizational pattern documented in this research [15][17]. The CivicActions three-level progression (Level 1: awareness; Level 2: analysis + certification; Level 3: mentoring + innovation) provides a replicable framework with defined promotion criteria [15] (MODERATE — T2 source, real program; no longitudinal effectiveness data published).

Champion responsibilities that distinguish the pattern from informal advocacy: the champion is a *named role* with explicit duties (auditing projects, coordinating accessibility code reviews, maintaining CI integration, training new hires), not a volunteer who occasionally raises issues [15][17]. This structural specificity is what distinguishes programs that persist from those that dissolve.

**Counter-evidence (substantial):** Champions programs have well-documented failure modes that the primary sources underweight. The single biggest predictor of program collapse is lack of executive sponsorship — when champions do accessibility work on top of their primary duties without protected time, burnout is common. Champion turnover (people leaving the organization or role) causes skill loss without succession planning. These failure modes are documented by Level Access, AbilityNet, and Fable (accessibility research org), all of which have studied program sustainability. The document's primary sources (CivicActions, Number Analytics) represent programs promoting their own success; failure cases are systematically underrepresented (MODERATE — challenger research).

Design system governance is an emerging alternative or complement to champions: by embedding accessible components in a shared library with enforced accessibility testing, teams can achieve a baseline without requiring every team to have an accessibility champion. This reduces per-team burden but concentrates knowledge risk in the design system team [16] (MODERATE — practitioner evidence, not independently validated).

Certification paths (CPACC, WAS, Trusted Tester) and structured onboarding training by champions are widely recommended for sustaining knowledge [15][17]. Training alone, without ongoing practice and measurement, decays — the literature consistently notes that one-time training is insufficient (HIGH — consistent finding across all organizational sources).

The accessibility overlay anti-pattern — deploying a JavaScript overlay product (accessiBe, UserWay, etc.) in lieu of structural remediation — is a prevalent market failure mode absent from most "best practices" literature. The FTC's April 2025 final order fining accessiBe $1M and the 1,000+ overlay-related lawsuits in 2024 demonstrate that overlays do not achieve WCAG compliance and expose organizations to legal liability. Any organizational guide to accessibility must explicitly warn against overlays (HIGH — FTC enforcement action, public record).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "WCAG 2.2 published as a W3C Recommendation on October 5, 2023" | attribution | [1][2] | verified |
| 2 | "WCAG 2.2 approved as ISO/IEC 40500:2025 in 2025" | attribution | [3] | verified |
| 3 | "WCAG 2.2 is backwards compatible — content conforming to 2.2 also conforms to 2.1 and 2.0" | attribution | [1] | verified |
| 4 | "WCAG 3 remains a Working Draft as of September 2025 — not finalized" | attribution | [4] | verified |
| 5 | "WCAG 3 Draft Candidate Recommendation planned for Q4 2027; full standard not before 2028" | statistic | [4] | verified |
| 6 | "European Accessibility Act (EAA) went into force June 28, 2025" | attribution | [1][9] | verified |
| 7 | "UK public sector: full WCAG 2.2 Level AA compliance required as of June 2025" | attribution | [1][9] | verified |
| 8 | "94.8% of top 1,000,000 home pages still had detected WCAG failures (2026)" | statistic | WebAIM Million 2026 (cited in Challenge/Findings) | verified |
| 9 | "Averaging 51 errors per page" (WebAIM Million 2026) | statistic | WebAIM Million 2026 (cited in Challenge/Findings) | verified |
| 10 | "Low contrast text on 79.1% of pages" (WebAIM Million 2026) | statistic | WebAIM Million 2026 (cited in Challenge/Findings) | verified |
| 11 | "axe-core detects on average 57% of WCAG issues automatically" | statistic | [6] (Deque press release, March 2021) | corrected — Findings clarifies this applies to Deque's full commercial axe suite, not standalone open-source axe-core in CI |
| 12 | "Automated tools detect approximately 30–40% of WCAG Success Criteria" | statistic | [10][11][12] | verified — Findings adopts this as the honest CI expectation for standalone axe-core |
| 13 | "axe-core `target-size` rule is likely the only WCAG 2.2 rule that will be added to axe-core [free tier]" | attribution | [6][7] (Deque documentation) | verified |
| 14 | "Focus Appearance and Focus Not Obscured checks require axe DevTools Pro (commercial tier)" | attribution | [6][7] | verified |
| 15 | "NVDA added AI-powered image descriptions" (2025, in Extracts) | attribution | [18] (T3) | corrected — Findings: NVDA on-device AI image description is in alpha as of Oct 2025, planned NVDA 2026.1; not a shipped 2025 capability |
| 16 | "JAWS introduced FSCompanion AI assistant" | attribution | [18] (T3) | corrected — Findings: FSCompanion is a help/training AI for JAWS users, not an in-stream content accessibility enhancement; description in Extracts was materially misleading |
| 17 | "Organizations implementing shift-left approaches achieved 80% reduction in accessibility issues within 8 months, 50% cut in remediation time" | statistic | [19] (T4, citing Siteimprove/Merkle webinar) | corrected — Findings: single unaudited case study (Merkle/Siteimprove 2025); not an industry benchmark; retained as illustrative only |
| 18 | "ROI of $1.40–$1.70 per dollar invested in accessibility" | statistic | [17] (T4, Number Analytics) | corrected — Findings/Challenge: source not traceable; original study not found; figure retired from evidential use |
| 19 | "FTC fined accessiBe $1 million (final order April 2025)" | attribution | FTC enforcement record (public) | verified |
| 20 | "Over 1,000 overlay-equipped websites faced lawsuits in 2024" | statistic | challenger research (public record) | human-review — figure widely cited but primary source (e.g., Seyfarth accessibility report) not fetched in this research session |
| 21 | "WCAG 2.2 has 9 new success criteria relative to WCAG 2.1" | statistic | [2][7][9] | verified |
| 22 | "4.5:1 contrast ratio required for regular text (AA); 3:1 for large text (AA)" | statistic | [1][9] | verified |
| 23 | "WCAG 2.5.8 minimum touch target: 24×24 CSS pixels" | statistic | [2][9] | verified |
| 24 | "Success Criterion 4.1.1 (Parsing) was removed from WCAG 2.2" | attribution | [7] | verified |
| 25 | "Google Lighthouse runs only a subset of axe-core rules (~57 audits vs 100+)" | statistic | [12] | verified |
