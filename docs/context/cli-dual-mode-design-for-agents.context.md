---
name: "CLI Dual-Mode Design for Agents"
description: "CLIs for LLM agents: stdout is the API contract (clean JSON), stderr is diagnostics, exit codes are a versioned API, TTY detection enables dual-mode output for humans and agents"
type: context
sources:
  - https://www.infoq.com/articles/ai-agent-cli/
  - https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
  - https://dev.to/meimakes/rewrite-your-cli-for-agents-or-get-replaced-2a2h
  - https://www.firecrawl.dev/blog/why-clis-are-better-for-agents
related:
  - docs/context/tool-description-quality-and-consolidation.context.md
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
  - docs/context/llm-failure-modes-and-mitigations.context.md
---

CLIs built for humans use color, pagination, interactive prompts, and pretty-printed output. Each of these breaks agent workflows. The solution is dual-mode design: full UX for TTY sessions, machine output for non-TTY sessions, detected via `isatty()`.

**The stdout/stderr contract is non-negotiable.** Stdout is the machine-parseable data — the API contract. When `--json` is used, stdout must be clean JSON and nothing else. Stderr is for diagnostics: progress messages, warnings, spinners, human-readable errors. Agents pipe stdout to subsequent commands. Any human text in stdout breaks parsing. The asymmetry matters in the failure case: "Stderr is the information agents need most, precisely when commands fail — never drop it."

**Three escape hatches every CLI must provide:**
1. Explicit flags: `--no-prompt`, `--no-interactive`, `--no-color`, `--json`, `--quiet/-q`
2. Environment variables: `NO_COLOR=true`, `MYCLI_NO_INTERACTIVE=1`, `OUTPUT_FORMAT=json` (flags take precedence over env vars)
3. Stable semantic exit codes — treated as a versioned API

**Exit code taxonomy (practitioner consensus):**

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General failure |
| 2 | Usage error (bad arguments) |
| 3 | Resource not found |
| 4 | Permission denied |
| 5 | Conflict (resource already exists) |

A tool that returns 0 on failure breaks every agent workflow that depends on it. Exit codes must remain stable across minor versions. Changing them is a breaking change.

**Error responses must be actionable.** Structured errors with machine-readable codes and agent-facing suggestions outperform technical stack traces. Pattern:
```json
{"error": "image_not_found", "image": "registry/name:tag", "suggestion": "run 'mycli images list' to see available images"}
```

Three error categories enable agents to reason about next action: transient (retry), permanent (do not retry), correctable (retry with different input).

**Command structure for discoverability.** Use noun-verb hierarchy: `mytool resource action`. This converts discovery into tree search — agents enumerate resources then actions, rather than guessing valid flag combinations. Flat, flag-heavy commands force agents to memorize or inject the full man page into context.

**The AWS CLI pager incident** (widely cited): defaulting `--output json` to pipe through `less` in headless environments broke agent workflows. Agents cannot type "q" to dismiss pagers. Every UX convenience needs a machine-override path.

**CLIs over IDEs for agents.** CLIs are stateless, pipe-composable, and feedback-via-exit-code. IDEs introduce full editor state into the agent's context. For autonomous operation at scale, the clean input/output contract of a CLI is more reliable than IDE agent "suggestions."
