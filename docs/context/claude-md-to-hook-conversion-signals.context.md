---
name: "CLAUDE.md to Hook Conversion Signals"
description: "Three signals that indicate a CLAUDE.md rule belongs in a hook instead: keep-violating, shell-expressible, lifecycle-timing — plus the diagnostic test to distinguish primitive problems from rule quality problems"
type: context
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026
  - https://code.claude.com/docs/en/hooks-guide
related:
  - docs/context/claude-code-primitive-routing-and-reliability.context.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-quality-criteria.context.md
  - docs/context/claude-code-wrong-primitive-failure-modes.context.md
  - docs/research/2026-04-13-hook-vs-primitives.research.md
---

CLAUDE.md is advisory. Rules that need to be enforced — not suggested — belong in hooks. Three signals indicate the wrong primitive is in use.

## Three Conversion Signals

**Signal 1: Claude keeps violating the rule.** Under normal conditions, with fresh context, the rule isn't consistently followed. This is a reliability problem, not a rule quality problem. If CLAUDE.md is the primitive and the behavior is inconsistent, the correct fix is converting to a PreToolUse hook, not rewriting the rule.

**Signal 2: The rule is shell-expressible.** Any rule that can be expressed as a shell one-liner is always more reliable as a hook. CLAUDE.md compliance for "always run prettier before committing" is probabilistic; a PostToolUse hook running prettier is guaranteed. Format checks, test coverage thresholds, file naming patterns — anything objectively determinable belongs in a hook.

**Signal 3: The rule needs to fire at a specific lifecycle moment.** If the rule requires enforcement before a tool call (PreToolUse) or at session end (Stop), CLAUDE.md cannot provide timing guarantees. CLAUDE.md content is available throughout the session but is not bound to lifecycle events.

## The Diagnostic Test

Before converting a rule, distinguish between a primitive problem and a rule quality problem:

> Paste the ignored rule directly into the first session message (outside CLAUDE.md). If Claude follows it then, the issue is delivery — use a hook. If ignored again, the rule needs rewriting.

If behavior changes when the rule is delivered differently, the problem is the delivery primitive. If behavior doesn't change, the problem is the rule itself — more specificity, examples, or counterexamples are needed regardless of which primitive carries it.

## CLAUDE.md Failure Modes

Three documented failure modes indicate CLAUDE.md is wrong for enforcement:

1. **Context dilution** — instructions buried in a long CLAUDE.md are deprioritized as sessions grow. Rules that matter late in a session may not arrive. No hard cutoff exists, but community research points to compliance degradation past ~150–200 lines (after system prompt consumes roughly the first 50).

2. **Relevance judgment** — Claude evaluates whether a rule applies to the current task and may skip it if not. This is by design — it's what makes CLAUDE.md useful for guidelines that need interpretation. It's also why CLAUDE.md fails for enforcement: the "skip this rule" judgment is always available to the model.

3. **Instruction density degradation** — every rule added to CLAUDE.md dilutes the compliance probability of every other rule equally. High-value and low-value rules are affected uniformly. Rules that belong in hooks should be removed from CLAUDE.md, not kept as duplicates — this improves compliance for the rules that remain.

## The settings.json Boundary

A fourth primitive is often conflated with hooks: `permissions.deny` in `settings.json`. The distinction:

- **`permissions.deny`**: no logic, unconditional block, always active — correct for "never allow tool X under any circumstances"
- **Hook**: conditional logic, fires at lifecycle events — correct for "block tool X when condition Y"

When the block has no conditions, permissions.deny is simpler and more reliable than a hook that always exits 2.

## Practical Pattern

Every rule being added to CLAUDE.md should pass this pre-add test:
1. Is this advisory guidance that benefits from Claude's interpretation? → CLAUDE.md is correct
2. Is this mechanical, shell-expressible, or lifecycle-bound? → Hook is correct
3. Is this an unconditional block? → permissions.deny is correct

Rules that fail the hook test and are added to CLAUDE.md anyway degrade compliance for the rules that should be there.

**Takeaway:** CLAUDE.md rules that keep getting violated are signals, not failures. The rule content may be correct; the delivery primitive is wrong.
