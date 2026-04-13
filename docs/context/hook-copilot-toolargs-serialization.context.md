---
name: "Copilot toolArgs String Serialization"
description: "GitHub Copilot delivers toolArgs as a string-encoded JSON blob rather than a parsed object; all other platforms deliver tool_input as a parsed JSON object"
type: context
sources:
  - https://docs.github.com/en/copilot/reference/hooks-configuration
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cross-platform-payload-nonportability.context.md
  - docs/context/hook-github-copilot-surface-divergence.context.md
---

GitHub Copilot is the only platform that delivers tool arguments as a string-encoded JSON blob rather than a parsed JSON object. This requires an extra deserialization step in every Copilot hook script that needs to inspect what the agent is about to do.

**The difference**

All other platforms (Claude Code, Cursor, Windsurf, Codex, Cline) deliver tool arguments as a parsed JSON object directly in the payload:

```bash
# Claude Code / Cursor / Codex — tool_input is already an object
tool_name=$(echo "$payload" | jq -r '.tool_name')
command=$(echo "$payload" | jq -r '.tool_input.command')
```

GitHub Copilot delivers `toolArgs` as a string that contains JSON:

```bash
# Copilot — toolArgs is a string; must parse it as a nested JSON value
tool_name=$(echo "$payload" | jq -r '.toolName')
command=$(echo "$payload" | jq -r '.toolArgs | fromjson | .command')
```

The `fromjson` step is required on every field access. Missing it silently returns null for all nested fields.

**Why it matters for portability**

A script that handles `tool_input.command` (the Claude Code pattern) will not work on Copilot. A script that uses `.toolArgs | fromjson | .command` (the Copilot pattern) will fail with a parse error on Claude Code, which has no `toolArgs` field and would return null at `.toolArgs`. There is no shared abstraction — field access patterns are necessarily platform-specific.

**Scope**

This applies to the cloud agent surface. The Copilot VS Code surface uses `PreToolUse` with a slightly different payload format, but `toolArgs` serialization behavior is consistent with the cloud agent. Any Copilot hook that inspects tool inputs requires platform-specific field parsing.
