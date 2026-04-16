---
name: "Hook Handler Type Comparison"
description: "Claude Code is the only platform with non-shell handler types (http, prompt, agent); all other platforms are command/shell-only"
type: context
sources:
  - https://code.claude.com/docs/en/hooks
  - https://cursor.com/docs/hooks
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://docs.github.com/en/copilot/reference/hooks-configuration
  - https://developers.openai.com/codex/hooks
  - https://docs.cline.bot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-cross-platform-payload-nonportability.context.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
---

Every platform surveyed supports command (shell script) hooks. Claude Code is the only platform that goes beyond this, offering three additional handler types that fundamentally expand what hooks can do.

**Handler type comparison**

| Platform | command | http | prompt | agent |
|----------|---------|------|--------|-------|
| Claude Code | Yes (600s timeout) | Yes (30s timeout) | Yes | Yes |
| Cursor | Yes | No | No | No |
| Windsurf | Yes | No | No | No |
| Copilot (cloud + VS Code) | Yes (bash/powershell, 30s) | No | No | No |
| Codex CLI | Yes (600s timeout) | No | No | No |
| Cline | Yes | No | No | No |

**What each Claude Code handler type enables**

**http** — POSTs the hook payload to an external HTTP endpoint and expects a JSON response. Enables hooks that call external services, trigger webhooks, or consult remote policy systems without requiring a local process. 30-second default timeout.

**prompt** — Evaluates the hook payload via a single-turn LLM call (no tool access, no file reads). Enables hooks that apply judgment-based decisions — e.g., "does this command look dangerous?" — without writing a rule-based script. Claude Code determines the outcome from the LLM response.

**agent** — Spawns a full multi-turn subagent with complete tool access. Enables hooks that perform complex verification workflows before allowing an action to proceed.

**Timeout differences**

Claude Code `command` handler default timeout is 600 seconds (same as Codex). GitHub Copilot default timeout is 30 seconds (same as Claude Code's `http` handler). Cursor and Windsurf do not document a specific default timeout. Cline's timeout documentation was removed in a corrected claim (previously cited as 30 seconds, but the official docs do not specify).

**Practical implication**

For teams using Claude Code: the `prompt` and `agent` handler types enable policy checks that require language model judgment rather than pattern matching. For teams on other platforms: hooks are shell-only, meaning any LLM-based policy evaluation must be wrapped in a shell script that makes an external API call.
