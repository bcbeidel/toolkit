---
name: Rules Best Practices
description: Authoring guide for Claude Code rules — what makes a rule load-bearing, how to shape the frontmatter and body, the positive patterns that work, and how rules pair with hooks. Referenced by build-rule and check-rule.
---

# Rules Best Practices

## What a Good Rule Does

A rule is path-scoped behavioral guidance that Claude reads when editing files matching its `paths:` glob. The value proposition is narrow: a rule earns its place when a convention requires *judgment* to apply, escapes what a linter can catch, and matters enough that forgetting it produces a real cost.

Primitive selection — rule vs. hook vs. skill vs. CLAUDE.md — is covered in `primitive-routing.md`. This document assumes a rule is the right tool and focuses on making it a *good* rule.

## Anatomy

```markdown
---
paths:
  - "path/glob/**/*.ext"
---

<One-line imperative rule statement, framed as an action to take.>

**Why:** <the reason — incident, constraint, strong preference that justifies the rule>
**How to apply:** <when/where this kicks in, including edge cases and exceptions>

<Optional: one concrete example showing the compliant pattern. When the rule requires judgment and the boundary is non-obvious, show a contrasting non-compliant example alongside.>
```

Three load-bearing elements: the `paths:` scope, the rule itself, the reasoning. A rule that needs more structure is usually two rules in one file.

## Authoring Principles

**Frame in the positive.** State what to do, not what to avoid. The core reason is linguistic fragility: a single negation token (`no`, `not`, `never`, `don't`) carries the entire meaning of the sentence, and in English it is easy to misplace, misattribute across a clause boundary, or drop under attention pressure. "Thread dependencies through constructors" cannot be inverted by losing a token; "don't use global state" flips meaning if `don't` is elided or attached to the wrong verb. Positive framings are also more actionable — they name a target rather than leaving it implicit. Reserve negative framing for cases where the prohibited pattern has no clean positive counterpart, and keep those rare.

**One claim per file.** If the body needs "also" or "additionally," split it. A single-claim file is easier to cite, audit, retire, and pair with a hook. Bundled rules fail bundled — one obsolete claim degrades the authority of the whole file.

**Direct, definite voice.** "Use X." "Return Y from Z." Not "We prefer" or "It's generally better to." Hedged rules push judgment back onto Claude at every invocation, which defeats the point of writing the rule down. The scope lives in `paths:`; the body is the action.

**Specific enough to be falsifiable.** "Use `snake_case` for Postgres table names" is actionable. "Follow naming conventions" is not. A rule a reviewer can't use to say "this violates the rule" isn't doing work.

**Include the *why*.** Reasoning is what lets Claude extend a rule to edge cases instead of either applying it dogmatically or discarding it silently. It's also what lets a future maintainer decide whether the rule is still load-bearing or has outlived the situation that created it. For rules that ask Claude to judge compliance, the why should name the failure cost (what breaks, who bears it) and at least one legitimate exception — without the failure cost, the rule reads as bureaucratic overhead; without an exception, the rule gets disabled wholesale when an edge case arrives.

**Scope tightly with `paths:`.** Narrow, directory-rooted patterns (`services/api/**/*.py`) keep rules cheap — they enter context only where they apply. Widen the scope only after observing false negatives. Always-loaded rules (no `paths:`) compete with CLAUDE.md for advisory budget and lose the path-scoping advantage; justify them explicitly when used.

**Prefer short.** Rules longer than a screen are usually docs in disguise. Point to a context document from the rule body when the full explanation matters.

**Describe the codebase as it is.** Rules should capture conventions the code already follows. Aspirational rules generate false positives on every edit and teach the model to ignore the directory. When the codebase diverges from the desired state, fix the code first or retire the rule.

**Prefer structural fixes over behavioral guardrails.** A rule that says "remember to update the config in both places" is a signal that the config should live in one place. Reach for the fix before the rule.

**Reserve rules for judgment.** Deterministic checks belong in linters or hooks. Rules earn their place on conventions a grep-equivalent can't express.

## Patterns That Work

These are the positive shapes a durable rule library tends to take. Each one corresponds to a common failure mode that audits should catch.

**Definite phrasing over hedges.** "Return early from validation failures" works; "consider returning early where appropriate" doesn't. Hedges read as thoughtful but leave Claude to re-derive the judgment every time.

**Named exceptions over soft language.** When a rule has genuine exceptions, list them in `How to apply:`. Softening the rule itself to accommodate the exceptions ("usually," "tend to") erodes the whole claim.

**Judgment-based rules over linter restatements.** Rules that a formatter or type-checker already enforces add nothing and dilute the rules that genuinely need judgment. If a tool can catch it, let the tool catch it.

**Deconflicted rules over overlapping ones.** When adding a rule to a populated directory, check the other rules that will load for the same files. Two rules asserting contradictory things in the same scope leave Claude to pick — usually inconsistently.

**Stable conventions over in-flight state.** Rules describe how work is done. Who owns what this sprint, which migration is in progress, what flag is being ripped out — that's project memory or documentation, not a rule.

**Structural fixes over behavioral rules.** When a rule reads like "remember to X," ask whether the underlying system can eliminate the need to remember. A single source of truth beats a rule that patrols two.

**Contrast when the boundary is subtle.** One concrete example anchors most rules. When a rule asks Claude to judge a subtle boundary — where two files could look similar but mean different things — showing a compliant/non-compliant pair makes the boundary visible. Skip the pair when the violation is self-evident from the rule statement.

**Domain-specific examples over synthetic placeholders.** Examples using real code from the codebase — actual table names, function signatures, module paths — anchor the rule more strongly than `foo`/`bar`/`Widget` placeholders. Domain-specific identifiers let the evaluator (human or Claude) recognize the context and apply the rule the way they would to new code in the same codebase.

## Rule + Hook Pairing

The strongest enforcement pattern combines tiers. The hook catches the deterministic cases — a shell script verifies the pattern exists, the import is sorted, the migration is named correctly. The rule handles the judgment cases the hook can't express and explains *why* the fence is there.

The hook should exit non-zero only on unambiguous violations. Anything requiring interpretation stays in the rule. A hook that blocks on judgment calls generates bypass culture faster than no hook at all.

## Safety

Rule files are a trusted-instruction channel — loaded automatically, committed to git, read by Claude with implicit trust. That makes them a leak surface for secrets and a prompt-injection vector for pasted content.

- **No secrets.** Never include API keys, tokens, credentials, or private URLs in a rule file. Rule files carry the same exposure as any other committed config.
- **Destructive commands require explicit confirmation.** Rules that reference `rm -rf`, `git push --force`, `DROP`, `TRUNCATE`, migrations, production deploys, or data backfills must name the confirmation gate. Agents default to helpful, not cautious.
- **Guardrails, not shortcuts.** A rule adds a constraint. Never encode instructions that weaken security, validation, logging, or error handling.
- **Don't paste untrusted content.** Issue bodies, third-party docs, user-submitted text — paraphrase or link. Pasted content becomes a trusted instruction and opens a prompt-injection path.

## Review and Decay

A rule library should compound, not accumulate. Every rule present should still earn its place.

Retire a rule when:
- The violation is appearing in merged code without incident (the rule isn't load-bearing).
- A linter or type-checker now catches the same thing (the rule is redundant).
- The project has moved past the situation that motivated it (the rule is historical).
- Two rules contradict in overlapping paths (resolve at audit time, not at edit time).

A dead rule is worse than no rule — it trains the model to treat the library as background noise, which undermines the rules still doing work.

---

**Diagnostic when a rule isn't working:** First check whether the rule is actually loading — does a file you're editing match the `paths:` glob? If not, adjust scope. If the rule loads but gets ignored, check the body: is it positively framed, specific, and scoped to a single claim? Vague rules fail quietly. If the body is clean but the rule still fails in long sessions or under context pressure, the primitive is wrong — consider a hook.
