---
name: "Claude Code Subagent Context Isolation Model"
description: "What spawned subagents receive in their context window, what is excluded, and why the prompt string is the only communication channel from parent to subagent"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://www.morphllm.com/claude-subagents
related:
  - docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/subagent-cross-platform-format-comparison.context.md
---

# Claude Code Subagent Context Isolation Model

The prompt string from the Agent tool call is the only channel between parent and subagent. The parent must embed all needed context explicitly — file paths, prior outputs, architectural decisions. Nothing else carries over.

## What Subagents Receive

A subagent's context window contains exactly four components:

1. **System prompt** — the Markdown body of the agent definition file
2. **Task context** — the prompt string from the Agent tool call
3. **Environment** — working directory, platform, shell
4. **Listed skills only** — skills declared in the `skills` frontmatter field

## What Subagents Do Not Receive

Explicitly excluded:
- Parent's conversation history and prior tool calls
- Parent's full Claude Code system prompt
- Skills active in the parent session (must be listed explicitly in `skills`)
- Other subagents' outputs
- MCP server tool descriptions (unless configured via `mcpServers`)

"Each subagent starts fresh, unburdened by the history of the conversation or invoked skills." (Anthropic blog)

## CLAUDE.md Inheritance — QUALIFIED

For Agent-tool-spawned subagents, CLAUDE.md is NOT inherited. Current docs state isolation explicitly: "Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt."

In session-wide `--agent` mode, CLAUDE.md does load via normal message flow — a distinct code path from Agent-tool spawning. The mechanism of CLAUDE.md injection (message-flow vs. system prompt) leaves room for ambiguity in edge cases, but the spawned-subagent isolation path is the better-supported behavior in current docs.

## Output Flow

Subagent output returns as a single `tool_result` in the parent's message history when `stop_reason` is `end_turn`. Intermediate reasoning, tool calls, and results remain isolated within the subagent — the parent has no visibility into intermediate steps.

"One string in, one string out."

**Context consumption warning**: Many subagents each returning detailed results can rapidly fill the parent's context window. Request specific formats — summaries, specific findings, named recommendations — rather than raw data dumps. For large structured outputs (database query results, search corpora, file trees), instruct the subagent to write results to a file and return the file path, not the content.

## Transcript Persistence

Each subagent's full transcript is stored at:
```
~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl
```

Subagents can be resumed, retaining full conversation history exactly where they stopped. Foreground subagents block the parent until complete (permission prompts pass through). Background subagents run concurrently; all needed tool permissions are cleared before launch.

## Design Implication

Because the prompt string is the only channel, parent agents must be explicit about what they pass down. Poorly designed parent prompts — those that assume the subagent knows the project structure or prior decisions — are the primary cause of subagent failures. The subagent file body provides behavioral instructions; the invocation prompt provides task-specific context.

## Takeaway

Subagent isolation is complete and intentional. Design for it: write subagent system prompts as self-contained behavioral specs, and write invocation prompts as complete task briefs. Never assume the subagent knows anything the parent hasn't told it.
