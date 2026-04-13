---
name: "Claude Code Wrong-Primitive Failure Modes"
description: "Five documented failure modes from wrong primitive selection in Claude Code: CLAUDE.md-for-enforcement, skills-for-always-on-context, hooks-for-advisory, subagents-for-sequential-work, and CLAUDE.md bloat"
type: context
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://www.shareuhack.com/en/posts/claude-code-claude-md-setup-guide-2026
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/hooks-guide
related:
  - docs/context/claude-code-primitive-routing-and-reliability.context.md
  - docs/context/claude-md-to-hook-conversion-signals.context.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/primitive-selection-failure-signals.context.md
  - docs/research/2026-04-13-hook-vs-primitives.research.md
---

Wrong-primitive failures in Claude Code are almost always reliability failures, not capability failures. The primitives are largely capability-equivalent for expressing many constraints; the failure is in the reliability guarantee each primitive provides.

## Failure Mode 1: CLAUDE.md for Enforcement (HIGH risk)

**What it looks like:** A behavioral rule ("never edit .env files," "always run tests before committing") lives in CLAUDE.md. Claude follows it most of the time, then violates it in a long session or under context pressure.

**Why it fails:** CLAUDE.md is advisory. Claude evaluates rule relevance per-turn and may deprioritize rules in long sessions. The model's "skip this rule" judgment is always available — CLAUDE.md cannot remove it.

**Documented incidents:** "NEVER edit .env files" → Claude loaded .env and replicated credentials into generated code. `rm -rf` with an intended path restriction → executed broadly after user intended a limited removal.

**Recovery:** Convert to a PreToolUse hook. The hook fires before the tool call, regardless of LLM judgment.

## Failure Mode 2: Skills for Always-On Context (MODERATE risk)

**What it looks like:** A skill is used to hold "always follow these conventions" guidance. Works at session start; behavior changes after auto-compaction.

**Why it fails:** Skill content lifecycle: when invoked, the rendered SKILL.md enters conversation as a single message and stays for the rest of the session — but only within a token budget. After auto-compaction, invoked skills share a combined 25,000-token budget, filled from most-recently-invoked first. Skills invoked early in a long session are candidates for eviction.

**Recovery:** Always-on behavioral context belongs in CLAUDE.md (advisory) or in hooks (deterministic). Skills are demand-loaded procedures, not session-persistent context.

## Failure Mode 3: Hooks for Advisory Guidance (MODERATE risk)

**What it looks like:** A hook exits 2 for something that is usually correct but sometimes legitimately shouldn't be blocked. Users start bypassing the hook or running with `--no-verify`.

**Why it fails:** One false positive per session is sufficient to generate bypass culture. Once bypass is normalized, the hook provides no protection. The blocking mechanism is spent on guidance that should have been advisory.

**Recovery:** Convert to advisory output (exit 1 = warning, or stdout advisory message with exit 0). Reserve exit 2 for invariants that are never legitimate to skip. The graduated deployment pattern — start as warning, graduate to block after monitoring — exists precisely to prevent this failure mode.

## Failure Mode 4: Subagents for Sequential Dependent Work (MODERATE risk)

**What it looks like:** Sequential multi-step work is delegated to subagents, with each step's output needed as input for the next. Round-trips accumulate; latency grows; the isolation benefit doesn't apply.

**Why it fails:** Subagents prevent context poisoning by isolating work in separate context windows and returning only summaries. This is the right pattern when the intermediate work (search results, logs, file contents) would clutter the main conversation. For sequential work where step N+1 needs full step N output, the isolation is a liability — each step requires a new context fork.

**Recovery:** Sequential dependent work belongs in the main conversation or in a skill. Subagents are appropriate when the intermediate work can be summarized and discarded.

## Failure Mode 5: CLAUDE.md Bloat Past ~150–200 Lines (HIGH risk)

**What it looks like:** Compliance with important rules degrades silently over time as more rules are added. There is no error — Claude still "reads" the file — but adherence becomes inconsistent for both high-value and low-value rules equally.

**Why it fails:** Instruction density degradation is uniform — every rule added reduces the compliance probability of every other rule. After the system prompt consumes roughly the first 50 lines of effective budget, the usable CLAUDE.md instruction space is approximately 150–200 lines. Rules beyond this compete equally, regardless of importance.

**Recovery:** Rules that are shell-expressible or must fire at lifecycle events belong in hooks, not CLAUDE.md. Removing them from CLAUDE.md improves compliance for the rules that remain. Treat CLAUDE.md size as a resource that degrades under load.

## Diagnostic Pattern

To distinguish a primitive problem from a rule quality problem:

1. Paste the failing rule directly into the first session message (outside CLAUDE.md)
2. If Claude follows it: the issue is primitive delivery → change the primitive
3. If Claude still doesn't follow it: the issue is the rule itself → rewrite the rule, add examples or counterexamples

This isolates the variable. Both problems exist; they require different fixes.

**Takeaway:** Wrong-primitive failures don't announce themselves as configuration errors. They surface as intermittent behavioral inconsistency — rules that mostly work, sometimes don't. The pattern is the signal.
