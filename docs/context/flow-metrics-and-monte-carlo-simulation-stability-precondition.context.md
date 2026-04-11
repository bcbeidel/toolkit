---
name: Flow Metrics and Monte Carlo Simulation Stability Precondition
description: "Flow metrics (WIP, cycle time, lead time, throughput) enable data-driven delivery forecasting; Monte Carlo simulation achieves 81% accuracy at the 85th percentile, but only when the system is stable — check control limits before trusting confidence intervals."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://teachingagile.com/kanban/introduction/kanban-metrics
  - https://resources.scrumalliance.org/Article/blending-scrum-and-kanban-for-better-flow-and-predictability
  - https://www.scrum.org/resources/blog/story-points-estimate-or-not-estimate
  - https://www.prokanban.org/blog/trustingmcs
related:
  - docs/context/agile-methodology-selection-by-context-and-hybrid-principle-commitment.context.md
  - docs/context/team-topologies-coordination-and-dependency-visibility-mechanisms.context.md
  - docs/context/okr-co-creation-cascade-failure-and-structural-discipline.context.md
---
# Flow Metrics and Monte Carlo Simulation Stability Precondition

## Key Insight

Flow metrics — WIP, cycle time, lead time, throughput — are the convergent direction of travel for delivery predictability (Scrum.org T1, Scrum Alliance T1, Kanban practitioners). Monte Carlo simulation achieves 81% accuracy at the 85th percentile versus 59% for simple averages. The precondition that is routinely skipped: verify system stability before trusting MCS confidence intervals. Teams in flux produce MCS outputs that mislead.

## The Four Core Flow Metrics

**WIP (Work in Progress)**: Items actively being worked on. Lower WIP correlates with faster delivery and better predictability. WIP management directly impacts cycle time — the first lever for improving flow.

**Cycle Time**: Duration from when work begins until completion. Measures execution efficiency. Separate from Lead Time: cycle time is within team control; it excludes waiting time before work starts.

**Lead Time**: Total duration from request initiation through delivery, including queue time. The metric customers experience. Distinguishing lead time gaps (intake/approval bottlenecks) from cycle time (execution delays) enables targeted improvements.

**Throughput**: Items completed per unit time. The most reliable basis for forecasting delivery dates. When combined with historical distributions (not averages), enables probabilistic forecasting.

## Monte Carlo Simulation (MODERATE confidence — works when conditions are met)

Monte Carlo simulation uses historical throughput distributions to generate confidence intervals rather than point predictions:
- 50% probability range: median forecast
- 85% probability range: practical planning target
- 95% probability range: conservative commitment basis

Empirical data shows MCS achieves 81% accuracy at the 85th percentile versus 59% for simple averages, even with as few as 5–11 historical data samples. This is a meaningful improvement over naive estimation.

## The Stability Precondition

MCS accuracy depends on throughput data within control limits. Three conditions invalidate MCS outputs:

1. **Staffing changes**: team composition changes alter throughput distributions; pre-change data no longer represents current capacity
2. **Major process transitions**: switching methodologies or workflows resets the baseline
3. **External pressure patterns**: sprint velocity shaped by leadership pressure rather than organic throughput produces systematically optimistic data

**Step zero before trusting MCS outputs**: run a stability check. If data points are outside control limits (significant outliers in your throughput data), acknowledge that MCS outputs reflect a distribution that no longer describes your team's current operation.

A second precondition: **probabilistic literacy**. Leaders unfamiliar with confidence intervals treat the 85th percentile estimate as a near-guarantee, recreating the same false confidence as point estimates. MCS requires communication discipline alongside statistical computation.

## Story Points vs. Flow Metrics: The Real Divide

Both camps converge on what not to do:
- Do not equate story points to hours
- Do not use velocity as a commitment or individual productivity measure
- Historical throughput data is more reliable for forecasting than abstract estimates

Story points have a credible defense: relative effort comparison via planning poker accelerates team consensus and surfaces hidden complexity assumptions that individuals don't voice when estimating independently. The NoEstimates alternative (standardize item size, track throughput) works but requires mature decomposition discipline that is itself a form of estimation judgment.

Practical recommendation: track cycle time and throughput alongside whatever estimation method you use. Start flow metrics before abandoning story points; add MCS when you have stable data.

## Takeaway

WIP limits, cycle time tracking, and throughput measurement provide delivery insight without estimation overhead. Monte Carlo simulation on that data gives probabilistic forecasts that are measurably more accurate than simple averages — when the system is stable. Check control limits first. Don't replace story points with MCS until you have stable throughput data and stakeholders who can interpret confidence intervals as probabilities, not deadlines.
