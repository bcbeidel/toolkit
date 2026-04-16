---
name: Rule System Failure Modes — Fatigue and Instability
description: "Alert fatigue, enforcement without rationale, and rubric instability are three self-reinforcing failure modes that compound each other and destroy trust in rule-based systems."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://corgea.com/Learn/how-to-reduce-false-positives-in-sast
  - https://www.coderabbit.ai/blog/why-developers-hate-linters
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://arxiv.org/abs/2601.08654
related:
  - docs/context/llm-rule-structural-characteristics.context.md
  - docs/context/linter-patterns-transferable-to-llm-rules.context.md
  - docs/context/rule-library-operational-practices.context.md
---
# Rule System Failure Modes — Fatigue and Instability

## Key Insight

Three failure modes — alert fatigue, enforcement without rationale, and rubric instability — form a self-reinforcing cascade. Each one amplifies the others. Rule systems that trigger any one failure mode without intervention typically degrade all three simultaneously.

## Failure Mode 1: Alert Fatigue

False positives create a behavioral cascade: more FPs → reduced trust → fewer fixes applied → more violations → rules perceived as noise. Even 20–30% false positive rates are sufficient to produce this cascade. At 1,500–5,000 false-positive instances per scan, annual triage costs reach $432K–$1.44M.

"When developers see scan after scan flagging code they know is safe, they stop paying attention." This destroys the enforcement mechanism entirely — meaningful alerts are lost in noise. Teams conclude "the tool isn't configured well or useful" rather than investigating their own setup.

Alert fatigue has a secondary effect: a false sense of security. Teams begin equating "clean linting report" with "correct code," neglecting peer review and architectural review.

## Failure Mode 2: Enforcement Without Rationale

When rules enforce without explaining why, developers route around them rather than comply. `// eslint-disable-next-line` spam is "a rule authorship failure, not a developer behavior problem." Enforcement shifts focus from code quality to silencing alerts.

"Engineers aren't factory line operators; they're knowledge workers who benefit from context." Rules imposed without team consensus create adversarial dynamics — rules are perceived as gatekeeper constraints rather than team tools. The net effect: compliance theater, not quality improvement.

This failure mode is recoverable: rules that link to documentation within IDE error messages restore the educational function. But rules deployed without rationale create a credibility deficit that makes subsequent fixes harder.

## Failure Mode 3: Rubric Instability

Natural language rubrics behave differently depending on minor phrasing changes. "Rubric instability caused by prompt sensitivity" produces inconsistent evaluations — the same content scores differently because of a word choice change in the rule. "Unverifiable reasoning that lacks auditable evidence" compounds this: evaluations that cannot be traced back to specific text excerpts cannot be calibrated.

Temperature settings exacerbate instability. Evaluations run at high temperature introduce random variance on top of phrasing sensitivity. Low temperature is required for evaluation tasks — "you don't need creativity."

Rubric instability is particularly destructive in LLM-as-judge pipelines because it creates a moving threshold. Teams calibrate against a rubric, the rubric drifts through informal editing, and calibration breaks without anyone noticing.

## The Compound Effect

These three failure modes compound: fatigue reduces attention, enforcement without rationale motivates bypassing, and rubric instability undermines the calibration that would reduce fatigue. A rule system can enter all three failure modes simultaneously through the combination of over-broad rules (fatigue), no educational context (rationale gap), and informal rubric maintenance (instability).

## Takeaway

Monitor for early-stage failure signals: rising bypass rates (`// disable` or `--no-verify` usage), increasing FP complaints, and drift in rubric phrasing. Treat each as a signal for the entire cascade, not an isolated problem. The intervention order is: reduce FPs first (trust recovery), then add rationale (compliance improvement), then version-lock rubric text (stability).
