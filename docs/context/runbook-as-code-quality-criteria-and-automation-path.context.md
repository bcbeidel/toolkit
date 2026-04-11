---
name: Runbook as Code — Quality Criteria and Automation Path
description: "Runbooks and playbooks serve distinct scopes; both are treated as code — Git-versioned, post-incident updated, and quarterly reviewed."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://rootly.com/blog/incident-response-runbook-template-2025-step-by-step-guide-real-world-examples
  - https://rootly.com/incident-response/runbooks
  - https://uptimelabs.io/learn/what-is-an-incident-response-runbook/
  - https://www.squadcast.com/sre-best-practices/runbook-automation
related:
  - docs/context/blameless-postmortem-prerequisites-and-effectiveness-limits.context.md
  - docs/context/slo-error-budget-policy-and-alerting-mechanics.context.md
  - docs/context/toil-definition-measurement-and-automation-gate.context.md
---
# Runbook as Code — Quality Criteria and Automation Path

Runbooks and playbooks are distinct tools. Conflating them produces documents that do neither job well. Both must be treated as code: versioned, reviewed, and updated after every incident.

## Runbook vs. Playbook: Distinct Scopes

A **runbook** is a tactical, scenario-specific guide that directs responders through the lifecycle of a specific technical issue — from detection and triage through containment, resolution, and verification. Every step should be a command, not a paragraph. Commands must be copy-pasteable.

A **playbook** provides high-level strategic coordination for a class of incidents. It covers coordination across teams, escalation chains, stakeholder communication, and decisions that require judgment rather than execution.

Example distinction for a security incident:
- **Runbook**: "Isolate infected VLANs," "Capture memory dumps for forensics," "Restore data from immutable backups"
- **Playbook**: "Coordinate with legal counsel," "Notify law enforcement," "Manage public relations"

## The 5 A's Quality Framework

A quality runbook satisfies five criteria:

1. **Actionable** — every step is a command. Not "check the logs" but "run `grep ERROR /var/log/syslog | tail -100`."
2. **Accessible** — available where responders work during incidents: Slack, PagerDuty, incident management platforms. Not buried in a wiki.
3. **Accurate** — a single outdated command destroys trust. Quarterly reviews and version control are required. Archive deprecated runbooks; don't delete them.
4. **Authoritative** — one clear, definitive source per procedure. Multiple conflicting runbooks for the same scenario force responders to make judgment calls under pressure.
5. **Adaptable** — updated through post-incident reviews. Systems evolve; runbooks must track that evolution.

## Treat as Code: The Lifecycle Model

Version control is not optional. Store runbooks in Git:
- Track changes with commit messages explaining why steps changed
- Review runbooks in pull requests, especially after major incidents
- Tag runbook versions to align with corresponding infrastructure versions

Mandatory update triggers:
- After every post-incident review in which the runbook was used
- After any significant system architecture change
- On a quarterly review cadence even without triggering incidents

Set automated reminders for owners to verify runbooks quarterly. When a system is deprecated, archive its runbook with a clear deprecation note rather than deleting it — future responders encountering similar symptoms may still benefit.

## The Automation Path

Automation amplifies procedure quality — do not automate before achieving manual consistency.

The correct sequence:
1. Build a reliable manual runbook first
2. Document each step, map dependencies, and validate accuracy through real incident use
3. Add rollback plans for each automated step
4. Implement success checks to prevent automated steps from proceeding on failure
5. Monitor the automated runbook as a first-class system component

A runbook that humans can't execute reliably will be executed unreliably by automation, at higher speed and without human judgment to catch early failures.

**Takeaway**: Write runbooks as executable commands, store them in Git, update them immediately after every incident where they were used, and don't automate until the manual version works consistently.
