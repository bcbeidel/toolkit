---
name: SLO/SLI Error Budget Policy and Multi-Window Alerting Mechanics
description: Four-week rolling error budgets with deploy-freeze policy and multi-burn-rate alerting reduce alert fatigue and enforce reliability accountability.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://sre.google/workbook/implementing-slos/
  - https://sre.google/workbook/error-budget-policy/
  - https://sre.google/workbook/alerting-on-slos/
  - https://www.nobl9.com/resources/a-complete-guide-to-error-budgets-setting-up-slos-slis-and-slas-to-maintain-reliability
  - https://grafana.com/blog/how-to-implement-multi-window-multi-burn-rate-alerts-with-grafana-cloud/
related:
  - docs/context/toil-definition-measurement-and-automation-gate.context.md
  - docs/context/blameless-postmortem-prerequisites-and-effectiveness-limits.context.md
  - docs/context/runbook-as-code-quality-criteria-and-automation-path.context.md
---
# SLO/SLI Error Budget Policy and Multi-Window Alerting Mechanics

The four-week rolling error budget with explicit policy consequences is the canonical SRE approach to reliability accountability. Multi-window multi-burn-rate alerting solves the false-positive problem inherent in single-threshold approaches.

## Error Budget Fundamentals

An SLI measures service health as the ratio of good events to total events. An SLO sets the target percentage; the error budget is `100% - SLO`. For a 99.9% SLO, the error budget is 0.1% of requests — roughly 43.8 minutes of allowed downtime per month.

Burn rate measures how quickly the budget is depleting: burn rate = observed errors / acceptable errors over a period. When burn rate exceeds 1, the budget exhausts faster than the allowance permits.

## Four-Week Rolling Window Policy

Google SRE recommends a four-week rolling window as the default measurement period. Rolling windows prevent artificial budget resets that would obscure recent incidents. Weekly summaries support tactical decisions; quarterly reviews support strategic planning.

The canonical error budget policy has two enforcement actions:

- **Deploy freeze**: If the service has exhausted its four-week error budget, all changes and releases halt except P0 issues and security fixes, until the service returns within SLO.
- **Postmortem trigger**: If a single incident consumes more than 20% of the four-week error budget, the team must conduct a blameless postmortem.

These consequences require agreement from three parties before adoption: product managers must confirm the SLO threshold reflects acceptable user experience; engineering must commit to following the policy at exhaustion; operations must confirm the SLO is maintainable without excessive toil.

## Multi-Window Multi-Burn-Rate Alerting

Single-window alerting produces noise: a one-hour outage triggers alerts that fire for 36+ hours, long after the incident resolves. Multi-window alerting fires only while the budget is actively burning.

The recommended starting thresholds for a 99.9% SLO:

| Severity | Long Window | Short Window | Burn Rate | Budget Consumed |
|----------|------------|--------------|-----------|-----------------|
| Page | 1 hour | 5 minutes | 14.4× | 2% |
| Page | 6 hours | 30 minutes | 6× | 5% |
| Ticket | 3 days | 6 hours | 1× | 10% |

The dual-window approach: an alert fires only when both the long and short windows exceed the burn rate threshold simultaneously. This eliminates the 36-hour false-positive tail — the alert resets five minutes after the event, not one hour later.

The short window should be 1/12 the duration of the long window. The PromQL pattern for the 14.4× burn rate condition:

```
rate(errors[1h]) / rate(total[1h]) > (14.4 * 0.001)
AND
rate(errors[5m]) / rate(total[5m]) > (14.4 * 0.001)
```

## Practical Guidance

Start with a single SLO per critical user journey, not a comprehensive set. A poorly chosen SLO that no one trusts is worse than no SLO. The goal is a shared decision-making tool, not a compliance checkbox.

Error budget exhaustion is not a punishment — it is a signal to pause velocity and invest in reliability. Teams that frame it as punishment game the SLO instead of using it.

**Takeaway**: Implement the four-week rolling window with a written deploy-freeze policy before building alerting. Multi-window multi-burn-rate alerting is the correct alerting mechanism — tune burn rates to your SLO target, not the other way around.
