---
name: "Claude Code Subagent Description Field Authoring"
description: "How to write the description field for routing effectiveness — and why 'use proactively' is aspirational, not reliable"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://github.com/anthropics/claude-code/issues/5688
  - https://github.com/anthropics/claude-code/issues/10504
  - https://johnsonlee.io/2026/03/02/claude-code-background-subagent.en/
related:
  - docs/research/2026-04-14-subagent-authoring-best-practices.research.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/claude-code-subagent-definition-format.context.md
---

# Claude Code Subagent Description Field Authoring

The `description` field is the routing signal Claude uses to decide when to delegate. Write it to target the router, not the agent — behavioral instructions belong in the body.

## Format Pattern

Official examples follow a consistent structure:

`[Role] + [domain/specialty] + [trigger phrase] + [trigger condition]`

From Anthropic's built-in examples:
- `"Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."`
- `"Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues."`
- `"Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries."`

## The "Use Proactively" Caveat

Official docs say: "To encourage proactive delegation, include phrases like 'use proactively' in your subagent's description field."

This is aspirational framing, not reliable behavior. GitHub Issue #5688 documented a user with "You MUST use this agent PROACTIVELY whenever you want to run tests" (all-caps) in the description — the primary agent ignored it entirely. The issue was closed NOT_PLANNED, meaning Anthropic acknowledged the gap and chose not to fix it. The routing mechanism is a soft preference signal, not a hard rule.

Practitioners confirm: "Auto-selection of custom agents remains unreliable. Claude frequently handles tasks in the main session rather than delegating to a defined agent, which defeats the purpose of automatic routing." (ksred.com)

## Description Targets the Router, Not the Agent

The `description` field is read when Claude decides which agent to invoke. It is not read during the agent's execution. Mixing behavioral instructions into it creates two problems:

1. Routing signal dilution — instructions obscure the delegation trigger
2. Instructions go unread — the agent never sees the `description` field while executing

Over-length descriptions are a documented antipattern. GitHub Issue #10504 found Claude-generated agents producing 1,297–1,308 character descriptions with embedded examples — well over the 1,024-character limit — without warnings. A concise routing hint around 140 characters is the practitioner-derived heuristic, though the real constraint is: keep routing cues and behavioral instructions separate.

Bad pattern:
```yaml
description: "Use this agent when...\\n\\nContext: User has...\\n<example>...</example>"
```

Better pattern:
```yaml
description: "Expert Python code reviewer for FastAPI, async patterns, and backend features. Use after implementing or refactoring Python services."
```

## The Only Reliable Trigger

Explicit invocation by name — either via @-mention or by passing `subagent_type` in the Agent tool call — is the only trigger you can depend on. "Use proactively" signals intent; it does not guarantee delegation.

Design workflows around explicit invocation. Treat auto-delegation as a convenience when it fires, not as a guarantee you can architect around.

**Takeaway:** Write description as a routing cue — role, domain, trigger condition, ~140 chars. Include "use proactively" as a signal but do not build workflows that depend on it firing. The only reliable trigger is explicit invocation by name.
