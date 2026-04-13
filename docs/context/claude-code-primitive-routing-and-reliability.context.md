---
name: "Claude Code Primitive Routing and Reliability Tiers"
description: "Decision framework for routing work to the right Claude Code primitive: reliability tier table, hook vs. skill routing test, and scoped hook composition pattern"
type: context
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/hooks-guide
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/sub-agents
  - https://alexop.dev/posts/understanding-claude-code-full-stack/
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/claude-md-to-hook-conversion-signals.context.md
  - docs/context/claude-code-wrong-primitive-failure-modes.context.md
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
  - docs/research/2026-04-13-hook-vs-primitives.research.md
---

The six Claude Code primitives fall into two reliability tiers. Routing work to the wrong tier is the root cause of most enforcement failures — not bad instructions or misconfigured tools.

## Reliability Tiers

**Deterministic tier** — fires regardless of LLM judgment:
- Hooks (lifecycle-event triggered, no decision-making)
- User-invoked skills (user types `/skill-name` explicitly)
- `settings.json` `permissions.deny` (unconditional firewall, no logic)

**Probabilistic tier** — Claude decides whether and when to apply:
- CLAUDE.md (always-on context, but advisory; Claude judges relevance)
- Model-invoked skills (Claude matches description to task, may skip)
- Subagents (task-delegated, Claude decides when to fork)

**The core design principle:** Use the deterministic tier for enforcement. Use the probabilistic tier for guidance and procedures where Claude's judgment adds value.

## Primitive Comparison

| Primitive | Invocation | Decision-maker | Reliability | Best fit |
|-----------|-----------|----------------|-------------|----------|
| CLAUDE.md | Always-on, session-persistent | Claude (probabilistic) | Advisory | Architectural context, implicit knowledge |
| Skill | On-demand, description-matched | Claude or user | Probabilistic (model) / Deterministic (user) | Repeatable procedures, demand-loaded reference |
| Hook | Lifecycle event, automatic | None | Deterministic | Enforcement, automation at lifecycle boundaries |
| Subagent | Task-delegated | Claude | Isolated context | Side tasks that pollute main context |
| MCP server | Tool call | Claude | Deterministic (external API) | External system connectivity |
| `permissions.deny` | Always | None (firewall) | Unconditional | Permanent, unconditional blocks |

The cleanest one-line distinction (T1 docs + T3 practitioner synthesis):
> "Skills extend what Claude can do. Hooks constrain how Claude does it."
> "Hooks run without Claude's decision-making. Skills require Claude to recognize when they apply."

## Hook vs. Skill Routing Test

Two questions determine the right primitive:

1. **Must this happen at a specific lifecycle event (before/after a tool call, session start, stop)?** → Hook
2. **Should Claude decide whether this applies to the current task?** → Skill (model-invoke) or CLAUDE.md

The operational signal: if a skill-defined procedure keeps being skipped when it should run, and the correct behavior is "always run at event X," that's a hook. The official skills docs state this explicitly:

> "If the skill seems to stop influencing behavior after the first response, use hooks to enforce behavior deterministically."

The fix is not a better skill description — it's a different primitive.

## Scoped Hook Composition

Skills can define hooks in their frontmatter (`hooks:` field) that fire only while the skill is active. This is the correct composition pattern: the skill provides the instruction set; the scoped hook enforces the skill's invariants during execution. A skill can instruct *what* to do and also enforce *that* it happens — both within a single skill definition.

Use this pattern when a skill defines a procedure that has mandatory steps (e.g., "always run the linter after editing" as part of a code-review skill). The hook makes the mandatory step deterministic without requiring a separate global hook.

## permissions.deny vs. Hooks

`permissions.deny` in `settings.json` is not a hook — it's a static firewall with no runtime logic. Use it for unconditional permanent blocks (never allow tool X, ever). Use a hook when the block is conditional (block tool X when condition Y is true). The distinction: permissions.deny removes the decision entirely; hooks add conditional logic that runs at decision time.

**Takeaway:** Wrong-primitive failures are almost always reliability failures, not capability failures. The primitives are largely capability-equivalent for many tasks; the question is always which one guarantees the behavior you need.
