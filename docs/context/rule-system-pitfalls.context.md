---
name: Rule System Pitfalls
description: How rule-based enforcement systems fail — false positives, alert fatigue, enforcement without education, and adoption barriers
type: context
sources:
  - https://cardinalops.com/blog/rethinking-false-positives-alert-fatigue/
  - https://www.coderabbit.ai/blog/why-developers-hate-linters
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://code.claude.com/docs/en/best-practices
related:
  - docs/research/2026-04-07-effective-rules-for-llm-enforcement.research.md
  - docs/context/effective-rule-anatomy.context.md
  - docs/context/llm-rule-evaluation-reliability.context.md
---

Rule systems die from trust erosion, not from technical failure. Every
design decision in a rule enforcement system should be evaluated against
these failure modes.

## False Positives Erode Trust Faster Than False Negatives

Some organizations experience false positive rates exceeding 95%. A
mining company's monitoring generated thousands of false positives until
alerts changed meaning from "this is important" to "this can be ignored."
The pattern is consistent across domains: one flaky test at a time leads
to entire test suites being abandoned. Trust is the currency of
enforcement systems, and false positives spend it rapidly.

**Implication:** Default severity should be `warn`, not `fail`. Scope
rules as narrowly as possible so they fire only on relevant files.

## Alert Fatigue Is the Primary Killer

Warning fatigue from excessive non-critical alerts is the top developer
complaint about linting systems. One team received 140 code review
comments on a 500-line PR, 80% style-related. When every file triggers
warnings, developers disable the system rather than fix violations.

**Implication:** Keep the number of active rules per file small. A
project with 20 rules and broad scopes will produce noise; a project
with 5 well-scoped rules will produce signal.

## Enforcement Without Education Backfires

Enforcement-first strategies cause developers to bypass rules with
disable comments rather than understanding the intent. "If the team
doesn't believe in the linting rules, they won't follow them, at least
not in the spirit they were intended." Teams that build consensus before
enforcement, deploy warnings before failures, and provide reasoning
with every rule see sustained adoption.

**Implication:** Every rule needs an Intent section explaining why it
exists. Understanding purpose is prerequisite to accepting enforcement.

## Legacy Code Creates Adoption Barriers

Teams avoid new rules because applying them to existing code would
create a backlog of issues. The "Hold the Line" principle — checking
only changed files, not the full codebase — is the standard mitigation.

**Implication:** Default to checking git-changed files, not the entire
project. New rules should enforce going forward, not retroactively.

## Rule Conflicts Compound With Scale

Multiple rules applying simultaneously can produce inconsistent outcomes.
Maintenance burden compounds: verification across hundreds of rules
becomes untenable, and updates to one rule create unforeseen conflicts.
Each rule should be evaluated independently against matching files, with
no cross-rule interaction.
