---
name: Rule Intent Section Quality
description: Five structural components required for an educationally effective Intent section, plus the signals that indicate a weak Intent. A rule with all five components prevents enforcement-without-education workaround behavior; a rule missing (2) or (4) should not be published.
type: concept
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://medium.com/agoda-engineering/how-to-make-linting-rules-work-from-enforcement-to-education-be7071d2fcf0
  - https://www.joshuakgoldberg.com/blog/if-i-wrote-a-linter-part-2-developer-experience/
  - https://rustc-dev-guide.rust-lang.org/diagnostics.html
  - https://gitnation.com/contents/road-to-zero-lint-failures-tackling-code-quality-challenges-at-scale
related:
  - docs/research/2026-04-13-rule-taxonomy-intent-quality.research.md
  - docs/context/rule-type-taxonomy-and-structural-properties.context.md
  - docs/context/rule-system-failure-modes-fatigue-and-instability.context.md
---

# Rule Intent Section Quality

## Key Insight

The enforcement-without-education failure mode — developers responding to rule violations by disabling the rule rather than fixing the code — is driven by Intent sections that state *what* the rule catches but not *why the cost is real*, *who bears it*, or *when disabling is legitimate*. An Intent section that contains all five required components prevents this; an Intent section missing components (2) or (4) should not be published.

## Five Required Components

1. **Violation** — what pattern does this rule detect?
2. **Failure cost** — what specifically goes wrong when the pattern occurs, and who bears the cost?
3. **Principle** — what underlying value does this rule enforce (type safety, security, maintainability)?
4. **Exception policy** — when is disabling this rule legitimate? Name at least one case.
5. **Fix-safety signal** — is the auto-fix always safe, or does it require human review?

Components (2) and (4) are load-bearing. Without the failure cost, developers cannot perform the rational cost-benefit analysis that determines whether compliance is worth the effort. Without the exception policy, developers reach for blanket disable when they encounter a legitimate exception — because the rule gave them no other option.

## Strong vs. Weak Intent

**Weak:** *"Avoid using `console.log` in production code. It creates noise."*

Problems: names the violation (✓) but not the cost (✗), no principle (✗), no exception policy (✗), no fix-safety signal (✗). Developers responding to this rule have no information to act on.

**Strong:** *"`console.log` in production builds exposes internal state to end users via browser developer tools, and adds measurable latency in high-frequency call paths. Exception: `console.error` for critical runtime errors where structured logging is unavailable. Fix-safety: auto-remediable — removes statement without semantic change."*

All five components present. A developer reading this can evaluate whether the rule applies to their specific case, understand the legitimate exception, and know the fix is safe to apply.

## Weak Intent Signals

Five signals indicate a weak Intent section that needs revision:

1. **Violation-only** — describes what the rule checks but not why it matters
2. **Hedging language** — "generally," "often," "might," "could" signals uncertain criteria that developers bypass under time pressure
3. **No exception policy** — forces developers to choose between compliance and blanket disable when they encounter a legitimate exception
4. **Prohibition without consequence** — "do not use X" without naming what breaks if X is used
5. **Author-preference framing** — cites the rule author's preference without grounding in a principle the reader already accepts

## Four Preventions for Workaround Behavior

When rules produce workaround behavior (`eslint-disable` comments, blanket rule disabling), the causes and fixes are:

1. **Automated fix available** — compliance requires less effort than bypass when the fix is machine-safe
2. **IDE-level surfacing before CI failure** — a CI failure requires branch surgery; an IDE underline is corrected in place
3. **Trial period before enforcement** — warn mode before fail mode prevents the shock response that triggers mass disabling
4. **Failure cost named** — developers disable rules through rational cost-benefit analysis; naming the consequence raises the perceived value side of that equation

Rationale quality is necessary but not sufficient. Existing technical debt is a confounding factor: when a codebase contains thousands of pre-existing failures, even well-explained rules feel punitive regardless of Intent quality.

## Takeaway

Require all five components before publishing a rule. Rules that cannot answer "what goes wrong?" (component 2) and "when can I disable this?" (component 4) will generate workaround behavior regardless of how precisely the criterion is stated.
