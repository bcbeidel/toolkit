---
name: "Claude Code Subagent Invocation and Routing"
description: "Three invocation patterns for Claude Code subagents, why auto-delegation is unreliable in practice, how @-mention is the only reliable routing path, and the nesting restriction with available workarounds"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://www.ibuildwith.ai/blog/task-tool-vs-subagents-how-agents-work-in-claude-code/
related:
  - docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/subagent-cross-platform-format-comparison.context.md
---

# Claude Code Subagent Invocation and Routing

Auto-delegation by description is documented but frequently fails in practice. @-mention is the only reliable invocation path for a specific task.

## Three Invocation Patterns

| Pattern | Mechanism | Reliability |
|---|---|---|
| Natural language (auto) | Claude matches task to agent `description` | LOW — frequently fails |
| @-mention | Guarantees the agent runs for one task | HIGH |
| Session-wide (`--agent`) | Full session uses agent system prompt, tools, model | HIGH |

**Auto-delegation reliability gap (CONFIRMED)**: Claude frequently handles tasks in the main session rather than delegating even when the agent's description clearly matches. Official docs acknowledge this implicitly by recommending "use proactively" in descriptions as a workaround — which is guidance, not a guarantee. Multiple practitioner reports confirm the failure. Explicit @-mention is the only reliable routing mechanism for a specific task.

## `description` Field Is the Routing Signal

For auto-delegation, Claude uses the `description` field to match tasks to agents. Write it like a routing rule:
- Name specific trigger phrases and problem patterns
- Include "use proactively" to encourage delegation without being asked
- Prefer concrete action verbs and named domains over abstract descriptions

Example of a routing-optimized description:
```
Reviews Python code for security vulnerabilities. Use proactively after any
code changes to auth, database, or API surface areas.
```

## @-mention Behavior

An @-mention guarantees the named agent runs for that task. The full message still goes to Claude, which writes the actual Agent tool prompt based on what you asked. The @-mention controls which subagent Claude invokes, not the prompt it receives.

## Session-Wide Mode

Launching with `--agent <name>` or setting `agent` in configuration makes the entire session run under that agent's system prompt, tool restrictions, and model. `initialPrompt` only fires in this mode — it does not fire for Agent-tool-spawned subagents.

## Nesting Restriction

Subagents cannot spawn other subagents. The Agent tool is filtered out of subagent tool sets at the platform level. `Agent(agent_type)` syntax in a subagent's `tools` field has no effect.

**Workaround**: A subagent can call `claude -p` via the Bash tool to launch a headless Claude subprocess. This bypasses the restriction but runs outside Claude Code's orchestration — no visibility into results, no error propagation, no coordination with the parent session.

## Background vs Foreground

**Foreground** (default): blocks the parent conversation until the subagent completes. Permission prompts and clarifying questions pass through to the user.

**Background** (`background: true`): runs concurrently while the parent continues. Claude Code prompts for all needed tool permissions before launching. Use for parallelizable work where you do not need to wait for results before proceeding.

## Historical Note

The Task tool was renamed to Agent tool in Claude Code v2.1.63. `Task(...)` references still work as aliases.

## Takeaway

Do not build workflows that depend on auto-delegation for correctness. Use @-mention when you need a specific agent for a specific task. Use session-wide mode when the entire workflow should run under a single agent context. Design the `description` field to be a routing rule, not a capability summary.
