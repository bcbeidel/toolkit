---
name: Core Web Vitals Thresholds and SEO Floor Not Target
description: CWV thresholds apply at the 75th percentile of real user sessions; reaching "Good" removes a ranking penalty but exceeding it yields no additional SEO benefit — engineering effort past the floor has diminishing returns.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://web.dev/articles/defining-core-web-vitals-thresholds
  - https://www.debugbear.com/docs/core-web-vitals-metrics
  - https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/Performance_budgets
related:
  - docs/context/performance-test-type-taxonomy-and-environment-parity-prerequisite.context.md
  - docs/context/percentile-approximation-hazard-and-histogram-based-slo-metrics.context.md
  - docs/context/opentelemetry-overhead-and-sampling-strategy-timing.context.md
---
# Core Web Vitals Thresholds and SEO Floor Not Target

## Key Insight

Core Web Vitals act as a ranking tiebreaker, not a primary ranking driver. Reaching "Good" thresholds removes a ranking penalty; engineering effort beyond that threshold yields no additional SEO benefit. Optimize to the floor, then stop. Track with CrUX field data, not just Lighthouse lab scores.

## Official Thresholds (HIGH confidence — T1 Google/web.dev)

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2,500 ms | 2,500–4,000 ms | >4,000 ms |
| INP (Interaction to Next Paint) | ≤200 ms | 200–500 ms | >500 ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

All three thresholds apply at the **75th percentile** of real user sessions (CrUX field data). A page passes "Good" only when 75% of its visitors experience the metric at or below the Good threshold.

INP measures the 95th percentile of user interactions on a given page — the 95th slowest interaction out of 100 determines the INP score.

## The SEO Floor Finding (MODERATE confidence — T4 with confirmed counter-evidence)

Only 47% of sites pass Google's "Good" thresholds in 2026, yet poorly-performing sites still rank on content quality and backlinks. CWV function as a tiebreaker in competitive search contexts — reaching "Good" removes a penalty and unlocks the floor. Exceeding "Good" thresholds produces no measurable additional ranking benefit.

The engineering implication: if you're at "Good," stop optimizing CWV and invest engineering effort elsewhere.

## Lab Data vs. Field Data Gap

Lighthouse scores (lab data) diverge significantly from CrUX scores (field data). Lighthouse captures performance under controlled conditions, typically reflecting the 5–10th percentile of observed user latency rather than the 75th percentile used for ranking. A page with a "Good" Lighthouse score may fail CrUX thresholds at scale.

**Use Lighthouse** for catching regressions in CI/CD (relative comparisons).  
**Use CrUX/PageSpeed Insights** for measuring actual Google ranking eligibility.

## Performance Budgets (HIGH confidence — T1 MDN)

Set two-level budgets:
- **Warning level**: proactive signal; allows planning without blocking development or deploys
- **Error level**: hard upper bound; changes at this level will have noticeable negative impact

Budget types: timing (LCP, TTI), quantity (total JS size, image weight), or rule-based (Lighthouse score minimum). Budgets should be dynamic — multiple budgets for different pages/flows, updated as goals change.

Default baseline from MDN: Time to Interactive <5s on 3G/4G, <2s for repeat loads.

## Takeaway

LCP ≤2,500ms, INP ≤200ms, CLS ≤0.1 at the 75th percentile of real sessions — these are the targets. Reaching them removes the SEO penalty. Further optimization is a user experience investment, not an SEO one. Validate with CrUX field data; use Lighthouse only for relative regression detection in CI.
