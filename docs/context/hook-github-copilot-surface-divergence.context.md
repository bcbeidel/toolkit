---
name: "GitHub Copilot Hook Surface Divergence"
description: "Copilot cloud agent and VS Code hook surfaces each have 8 events but diverge by one event each; neither supports matcher filtering or file-type-specific hooks"
type: context
sources:
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks
  - https://docs.github.com/en/copilot/reference/hooks-configuration
  - https://code.visualstudio.com/docs/copilot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-github-copilot-blocking-gaps.context.md
  - docs/context/hook-github-copilot-no-global-config.context.md
  - docs/context/hook-cross-platform-payload-nonportability.context.md
---

GitHub Copilot offers two distinct hook surfaces: the cloud agent (GitHub Actions and cloud-hosted runs) and the VS Code extension. Both support 8 events, but they are not the same 8. The surfaces diverge at exactly one event each — and the divergence is architecturally meaningful.

**Event comparison**

| Event | Cloud agent | VS Code |
|-------|-------------|---------|
| `sessionStart` / `SessionStart` | Yes | Yes |
| `userPromptSubmitted` / `UserPromptSubmit` | Yes | Yes |
| `preToolUse` / `PreToolUse` | Yes | Yes |
| `postToolUse` / `PostToolUse` | Yes | Yes |
| `agentStop` / `Stop` | Yes | Yes |
| `subagentStop` / `SubagentStop` | Yes | Yes |
| `sessionEnd` | Yes | No — replaced by `Stop` |
| `errorOccurred` | Yes | No |
| `PreCompact` | No | Yes |
| `SubagentStart` | No | Yes |

`errorOccurred` is unique to the Copilot cloud agent and has no equivalent in any other platform surveyed (Claude Code, Cursor, Windsurf, Codex, Cline). It fires when an error occurs during agent execution. `PreCompact` (context compaction) and `SubagentStart` (subagent spawn) are VS Code only.

**No matchers, no file-type hooks**

Neither surface supports the per-tool-type hooks available in Cursor (`beforeShellExecution`, `beforeReadFile`, `afterFileEdit`) or Claude Code's matcher syntax for filtering events by tool name or file pattern. The VS Code documentation notes that matcher values in Claude Code format are "parsed but not applied" — meaning if you copy a Claude Code hook definition to VS Code, the matcher field will be silently ignored and all events will trigger the hook regardless of tool type.

**Payload format divergence between surfaces**

The cloud agent uses `camelCase` event names (`sessionStart`, `preToolUse`, `toolName`, `toolArgs`). The VS Code implementation uses `PascalCase` event names with `snake_case` field names (`SessionStart`, `PreToolUse`, `hook_event_name`). Hook scripts written for one surface are not portable to the other without modification.

**Practical implication**

Teams using Copilot across both cloud and VS Code contexts must maintain separate hook scripts for each surface, accounting for different event sets and different payload schemas. The cloud agent's `errorOccurred` event enables error-state handling that VS Code cannot replicate; VS Code's `PreCompact` enables compaction control that the cloud agent cannot replicate.
