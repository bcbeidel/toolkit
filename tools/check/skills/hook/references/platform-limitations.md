---
name: Hook Platform Limitations
description: Per-platform behavioral differences and enforcement gaps for Claude Code hooks — Copilot, Codex CLI, Windsurf, and Cline quirks that affect hook portability
---

# Hook Platform Limitations

All six major hook systems are pre-stable (Experimental / Preview / beta) as of Q1 2026. Re-audit after major platform updates.

## Copilot (VS Code / cloud agent)

Matchers are parsed but not enforced — every tool event fires regardless of `matcher` value. Tool arguments are serialized as a string (`toolArgs`), not a `tool_input` object — jq field extraction fails silently. Cloud agent skips remaining hooks after the first deny decision.

## Codex CLI

`PreToolUse` only intercepts `Bash` — Write, WebSearch, and MCP calls cannot be gated via hooks.

## Windsurf

`updatedInput` is not supported — pre-hooks are block/allow only. `~` is not expanded in `working_directory` fields; use absolute paths.

## Cline

Blocking uses `{"cancel": true}` in JSON stdout, not exit code 2. PostToolUse hooks that exit 1 block unexpectedly in practice despite documentation (community-confirmed anomaly).
