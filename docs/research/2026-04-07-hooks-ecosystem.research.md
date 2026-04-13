---
name: "Claude Code Hooks Ecosystem & Best Practices"
description: "How Claude Code hooks work, patterns for deterministic guardrails vs. advisory guidance, and real-world configurations for code quality and security"
type: research
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/best-practices
  - https://claude.com/blog/how-to-configure-hooks
  - https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md
  - https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks
  - https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://medium.com/becoming-for-better/taming-claude-code-a-guide-to-claude-md-and-hooks-ed059879991c
  - https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
  - https://aiorg.dev/blog/claude-code-hooks
  - https://github.com/disler/claude-code-hooks-mastery
  - https://github.com/rulebricks/claude-code-guardrails
  - https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json
  - https://dev.to/gunnargrosch/automating-your-workflow-with-claude-code-hooks-389h
  - https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement
  - https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
  - https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails
  - https://github.com/hesreallyhim/awesome-claude-code
related:
  - docs/research/2026-04-07-instruction-file-conventions.research.md
  - docs/research/2026-04-07-cli-tool-design.research.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hook-matcher-syntax.context.md
  - docs/context/hook-output-and-decision-control.context.md
  - docs/context/hook-quality-criteria.context.md
---

## Research Question

How does the Claude Code hooks system work, what patterns exist for deterministic guardrails vs. advisory guidance, and what real-world configurations are effective for code quality, security, and convention enforcement?

## Sub-Questions

1. What hook types does Claude Code support and what are their execution models?
2. How can hooks improve agent output quality (pre-commit validation, file-save checks, rule enforcement, auto-formatting)?
3. What patterns exist for deterministic guardrails via hooks vs. advisory guidance via CLAUDE.md?
4. How should hooks balance enforcement strictness with developer experience (latency, noise, override mechanisms)?
5. What are real-world examples of effective hook configurations for code quality, security scanning, and convention enforcement?

## Search Protocol

| # | Query | Key Finding |
|---|-------|-------------|
| 1 | Claude Code hooks documentation PreToolUse PostToolUse 2025 | Found official docs at code.claude.com/docs/en/hooks; confirmed 4 hook handler types and exit code semantics |
| 2 | Claude Code settings.json hooks configuration examples | Found configuration hierarchy, three file locations, and Prettier/TypeScript examples |
| 3 | Claude Code hooks exit codes blocking behavior SubagentStop Notification Stop hook types | Confirmed exit 0/2/other semantics; stop_hook_active flag for loop prevention |
| 4 | Claude Code hooks pre-commit validation security scanning code quality real-world examples 2025 2026 | Found pre-commit skill, security scanning integrations, GitLab/GitHub CI patterns |
| 5 | Claude Code hooks deterministic guardrails vs CLAUDE.md advisory guidance enforcement patterns 2025 | Found clear articulation: CLAUDE.md = advisory, hooks = deterministic; specific incident reports |
| 6 | Claude Code hooks latency performance overhead developer experience override mechanisms 2025 2026 | Found ~20s latency issue report; async:true recommendation; per-hook timeout configuration |
| 7 | Claude Code UserPromptSubmit SessionStart PreCompact hook examples practical patterns 2026 | Found SessionStart for context injection, UserPromptSubmit for prompt augmentation, PreCompact for transcript backup |
| 8 | Claude Code hooks "settings.json" real examples GitHub security scanning linting convention enforcement 2026 | Found CVE-2025-59536 (hook RCE vulnerability); awesome-claude-code curated list; everything-claude-code hooks.json |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://code.claude.com/docs/en/hooks | Hooks reference | Anthropic | 2026 | T1 | verified |
| 2 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic | 2026 | T1 | verified |
| 3 | https://claude.com/blog/how-to-configure-hooks | Claude Code power user customization: How to configure hooks | Anthropic | 2026 | T1 | verified |
| 4 | https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/hook-development/SKILL.md | Hook Development Best Practices (official plugin skill) | Anthropic | 2026 | T1 | verified |
| 5 | https://blog.gitbutler.com/automate-your-ai-workflows-with-claude-code-hooks | Automate Your AI Workflows with Claude Code Hooks | GitButler | 2025-2026 | T3 | verified |
| 6 | https://smartscope.blog/en/generative-ai/claude/claude-code-hooks-guide/ | Claude Code Hooks Complete Guide — Automate and Enforce Rules Reliably | SmartScope | 2026 | T3 | verified |
| 7 | https://paddo.dev/blog/claude-code-hooks-guardrails/ | Claude Code Hooks: Guardrails That Actually Work | paddo.dev | 2026 | T3 | verified |
| 8 | https://medium.com/becoming-for-better/taming-claude-code-a-guide-to-claude-md-and-hooks-ed059879991c | Taming Claude Code: A Guide to CLAUDE.md and Hooks | Mustafa Morbel / Medium | Mar 2026 | T3 | verified |
| 9 | https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns | Claude Code Hooks Reference: All 12 Events [2026] | Pixelmojo | 2026 | T3 | verified |
| 10 | https://aiorg.dev/blog/claude-code-hooks | Claude Code Hooks: Complete Guide with 20+ Ready-to-Use Examples | aiorg.dev | 2026 | T3 | verified |
| 11 | https://github.com/disler/claude-code-hooks-mastery | claude-code-hooks-mastery (GitHub repository) | disler | 2026 | T4 | verified |
| 12 | https://github.com/rulebricks/claude-code-guardrails | claude-code-guardrails (GitHub repository) | Rulebricks | 2026 | T4 | verified |
| 13 | https://github.com/affaan-m/everything-claude-code/blob/main/hooks/hooks.json | everything-claude-code hooks.json | affaan-m | 2026 | T4 | verified |
| 14 | https://dev.to/gunnargrosch/automating-your-workflow-with-claude-code-hooks-389h | Automating Your Workflow with Claude Code Hooks | Gunnar Grosch / DEV | 2026 | T3 | verified |
| 15 | https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement | Claude Code Stop Hook: Force Task Completion | claudefa.st | 2026 | T3 | verified |
| 16 | https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/ | Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files (CVE-2025-59536) | Check Point Research | 2026 | T2 | verified |
| 17 | https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails | Equipping Claude Code with Deterministic Security Guardrails | Codacy | 2026 | T3 | verified |
| 18 | https://github.com/hesreallyhim/awesome-claude-code | awesome-claude-code (curated list) | hesreallyhim | 2026 | T4 | verified |

## Raw Extracts

### Sub-question 1: Hook types and execution models

**Core Hook Events (from official docs, T1):**

Claude Code supports four hook handler types and multiple lifecycle events. As of 2026, the documented event set includes:

**Tool execution events:**
- `PreToolUse` — fires before a tool call executes; can block, modify, or approve it
- `PostToolUse` — fires after a tool completes successfully; cannot prevent execution
- `PostToolUseFailure` — fires when a tool execution fails

**Session lifecycle events:**
- `SessionStart` — fires when a new session begins or resumes
- `SessionEnd` — fires when a session ends
- `UserPromptSubmit` — fires before Claude processes a user prompt
- `PreCompact` — fires before context compaction
- `PostCompact` — fires after context compaction

**Agent coordination events:**
- `Stop` — fires when Claude finishes responding
- `SubagentStop` — fires when a subagent finishes
- `SubagentStart` — fires when a subagent begins

**Permission events:**
- `Notification` — fires when Claude sends notifications (permission_prompt, idle_prompt, auth_success, elicitation_dialog); observability only, cannot block
- `PermissionRequest` — fires before permission dialogs
- `PermissionDenied` — fires after a permission is denied

**Hook handler types (four kinds):**

| Type | Use Case | Blocking Support |
|------|----------|------------------|
| `command` | Shell execution, deterministic rules | Full (via exit codes) |
| `http` | External service integration (POST to endpoints) | Full |
| `prompt` | Single-turn LLM evaluation | Conditional |
| `agent` | Multi-turn subagent with file/command access | Conditional |

**Input schema (all events):**
All hooks receive JSON on stdin:
```json
{
  "session_id": "string",
  "transcript_path": "string",
  "cwd": "string",
  "permission_mode": "default|plan|acceptEdits|auto|dontAsk|bypassPermissions",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": { /* tool-specific */ },
  "tool_use_id": "string"
}
```

**Exit code behavior (official docs, T1):**

| Exit Code | Behavior |
|-----------|----------|
| 0 | Success — parse JSON from stdout |
| 2 | Blocking error — stderr becomes feedback; effect depends on event |
| Other | Non-blocking error — stderr shown in transcript, execution continues |

Exit code 2 is the *only* code that blocks. Exit code 1 is treated as non-blocking error.

**PreToolUse decision control (hookSpecificOutput):**

PreToolUse is uniquely powerful: it can return four outcomes (allow, deny, ask, defer) and modify tool input before execution. The decision lives inside `hookSpecificOutput`, unlike other events that use a top-level `decision` field:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer",
    "permissionDecisionReason": "string",
    "updatedInput": { /* modified tool input */ },
    "additionalContext": "string"
  }
}
```

When multiple PreToolUse hooks return conflicting decisions: deny > defer > ask > allow.

**PostToolUse behavior:**
PostToolUse fires after execution — it cannot prevent the tool from running. `decision: "block"` provides feedback to Claude but does not reverse the executed action. Useful for: running formatters, injecting quality feedback, logging.

**Stop/SubagentStop behavior:**
Exit code 2 prevents Claude from stopping and continues the conversation (or subagent). The `stop_hook_active` boolean in the input must be checked to prevent infinite loops:

```python
if input_data.get('stop_hook_active', False):
    sys.exit(0)  # Break the loop — already forced once
```

**Matcher syntax:**
Matchers filter which tools trigger a hook (tool name events only):
- Simple string: `"Bash"`, `"Write"`, `"Edit"`
- Pipe-separated: `"Write|Edit|MultiEdit"`
- Wildcard: `"*"` or omitted
- Regex: any pattern with characters outside alphanumeric/underscore/pipe — e.g., `"mcp__memory__.*"`, `"^Notebook"`
- Argument matching: `"Bash(npm test*)"` — matches Bash with command starting with `npm test`

**Configuration format:**
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validator.sh",
            "timeout": 60,
            "async": false,
            "statusMessage": "Validating command..."
          }
        ]
      }
    ]
  }
}
```

**Configuration locations (priority order):**
1. `~/.claude/settings.json` — user level, all projects
2. `.claude/settings.json` — project level, shareable via git
3. `.claude/settings.local.json` — project level, gitignored (personal preferences)
4. Plugin `hooks/hooks.json` — bundled with installed plugins
5. Skill/agent frontmatter — component-scoped

**JSON output universal fields (exit 0):**
```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": false,
  "systemMessage": "Message shown to Claude"
}
```

**Environment variables available to hooks:**
```bash
$CLAUDE_PROJECT_DIR         # Project root
$CLAUDE_PLUGIN_ROOT         # Plugin installation directory
$CLAUDE_PLUGIN_DATA         # Plugin persistent data directory
$CLAUDE_ENV_FILE            # SessionStart only: persist env vars across session
$CLAUDE_CODE_REMOTE         # "true" in web, unset in CLI
```

**Async hooks:**
Setting `"async": true` runs the hook in the background without blocking Claude. Async hooks cannot block via exit code 2 — that action has already proceeded. Async is for logging, notifications, and non-critical follow-up, not gating.

**JSON output cap:** 10,000 characters maximum; larger output is saved to a file.

**Hook deduplication:** Identical command strings or URLs run only once even if matched by multiple hook rules.

---

### Sub-question 2: Improving agent output quality via hooks

**Auto-formatting (PostToolUse, T1 + T3):**

The most commonly deployed pattern. Trigger formatters (Prettier, Black, Ruff) immediately after file edits:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit|MultiEdit",
      "hooks": [{"type": "command", "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""}]
    }]
  }
}
```

Key advantage: every file Claude generates is formatted before it enters your review queue, eliminating formatting noise from code review.

**Type checking after edits (PostToolUse):**
```json
{
  "matcher": "Edit",
  "hooks": [{"type": "command", "command": "if [[ \"$CLAUDE_FILE_PATHS\" =~ \\.(ts|tsx)$ ]]; then npx tsc --noEmit --skipLibCheck \"$CLAUDE_FILE_PATHS\"; fi"}]
}
```

**Test enforcement (Stop hook with stop_hook_active guard, T1 + T3):**
Block session completion until tests pass:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "INPUT=$(cat); [ \"$(echo $INPUT | jq -r '.stop_hook_active')\" = 'true' ] && exit 0; npm test || exit 2"
      }]
    }]
  }
}
```

The `stop_hook_active` check is mandatory — without it, Claude would enter an infinite loop if tests always fail.

**Linting with automatic fixes (PostToolUse, T3):**
Apply ESLint/Ruff conditionally by extension:
```bash
#!/bin/bash
FILE=$(jq -r '.tool_input.file_path' <<< "$1")
case "$FILE" in
  *.ts|*.tsx|*.js) npx eslint --fix "$FILE" ;;
  *.py) ruff check --fix "$FILE" ;;
esac
```

**Commit validation (PreToolUse, T4 from everything-claude-code):**
The everything-claude-code `hooks.json` shows `PreToolUse` Bash hooks that validate commit messages and detect secrets before `git commit` executes. These gate the commit itself.

**Stop-hook batch quality gate (T3):**
The SmartScope guide documents running full quality suites (format + typecheck + lint) as a batch on Stop, covering all JS/TS files modified during the session. Avoids running checks redundantly on every file edit by deferring to session end.

**Agent hooks for deep verification (T1 + T3):**
For comprehensive output quality, agent hooks spawn subagents that can:
- Run the test suite across modified files
- Check for debug code (`console.log`, breakpoints, `TODO(fix)`)
- Verify type system consistency
- Scan for architectural pattern violations

Agent hooks are slower and consume API credits, so they are reserved for high-value completion gates, not per-file operations.

**Prompt hooks for semantic validation (T3):**
A prompt hook can ask an LLM reviewer "does this output match the original request scope?" without file access. Returns `{"ok": true}` or `{"ok": false, "reason": "..."}`. Useful for: checking if Claude drifted from task scope, flagging unrelated changes.

**PostToolUse feedback injection (T1):**
PostToolUse hooks can provide structured feedback via `additionalContext` in `hookSpecificOutput`. This lets the hook inject quality findings (lint errors, type violations) directly into Claude's context for self-correction in the same session.

---

### Sub-question 3: Deterministic guardrails vs. advisory guidance

**The core distinction (T1 official docs + multiple T3):**

> "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." — Anthropic Best Practices documentation

The Mustafa Morbel Medium article articulates this most cleanly:
> "CLAUDE.md answers 'what should be done'; Hooks answer 'how do we enforce it.'"

**Why CLAUDE.md instructions fail as enforcement:**

1. **Context dilution** — In long sessions, important rules buried in CLAUDE.md get lost as context fills. The model stops attending to them.
2. **Probabilistic compliance** — Instructions are weighed against other signals. A sufficiently urgent user request can override a soft instruction.
3. **LLM interpretation** — Claude processes CLAUDE.md as context, not as a rule engine. It exercises judgment about when to apply rules.

The paddo.dev guardrails article documents concrete incidents where CLAUDE.md instructions failed:
- "NEVER edit .env files" → Claude loaded .env and replicated credentials to committed files
- "rm -rf" with home path → executed after user intended only a limited directory removal
- Test files modified to pass incorrectly, then defended as correct implementation

**The enforcement model for hooks:**
PreToolUse with exit code 2 is non-negotiable. As the paddo.dev article states: "Exit code 2 = blocked. No negotiation." No LLM interpretation, no context pressure can override a hook that returns exit code 2.

**What belongs in CLAUDE.md vs. hooks:**

| CLAUDE.md (Advisory) | Hooks (Deterministic) |
|---|---|
| Architectural decisions and engineering philosophy | Running linters and formatters |
| Coding preferences and naming conventions | Blocking dangerous commands |
| Technology stack documentation | Protecting sensitive files (.env, credentials) |
| Project-specific anti-patterns to avoid | Auto-staging changes for git workflow |
| Context about how the project works | Security pattern enforcement |
| Flexible guidance with edge cases | Pre-commit validation gates |

From the eesel.ai article: "For operations like running lint, applying formatting, or blocking dangerous commands, trust Hooks — not CLAUDE.md."

**Layered enforcement model (Pixelmojo T3):**

A production governance framework uses both:
1. **CLAUDE.md** defines coding standards (advisory context)
2. **Hooks** enforce standards at tool-use events (deterministic)
3. **CI/CD Pipeline** runs identical checks (reproducible)

Without hooks, standards remain advisory. With enforcement, "every rule becomes a gate that cannot be bypassed."

**The "systems engineering" framing (cobusgreyling.medium.com, T3):**

> "You would not secure a database with a comment that says 'please don't drop tables.' You write a permission system."

Hooks represent systems engineering applied to AI agents. The model operates freely within boundaries; crossing them triggers immediate, deterministic blocks — not probabilistic suggestions.

**Implementation recommendation:**
- Use CLAUDE.md for context and guidance that genuinely has edge cases
- Convert any CLAUDE.md rule that "Claude keeps violating" into a hook
- If a rule can be expressed as a shell one-liner, it belongs in a hook, not CLAUDE.md

---

### Sub-question 4: Balancing enforcement with developer experience

**Latency is the primary DX concern:**

Synchronous hooks add latency directly — Claude waits for each hook to complete before proceeding. An ~20s latency issue was reported in a GitHub issue for a misconfigured hook setup. Community guidance:
- Keep synchronous hooks under 1 second
- Use `"async": true` for anything that takes longer and doesn't need to block
- HTTP hooks have a 30-second default timeout (lower than the 600-second command default)
- Agent hooks spawn full Claude sessions — significant API cost and time

**Graduated enforcement (paddo.dev, T3):**

The paddo.dev guardrails article recommends a graduated approach:
1. Start with warnings to observe triggers without blocking
2. Monitor for false positives before escalating to blocking
3. Tune patterns incrementally — one rule per week
4. Reserve exit-code-2 blocking for truly dangerous operations

**Async hooks for non-critical automation:**
```json
{
  "type": "command",
  "command": "echo \"$(date): session completed\" >> ~/claude-work.log",
  "async": true
}
```

Async hooks are appropriate for: logging, notifications, transcript backup, metrics collection — anything where the result doesn't need to gate Claude's next action.

**Reducing permission noise (PermissionRequest hooks):**

Auto-approve known-safe operations to eliminate repetitive prompts:
```json
{
  "hooks": {
    "PermissionRequest": [{
      "matcher": "Bash(npm test*)",
      "hooks": [{"type": "command", "command": "/path/to/validate-test-command.sh"}]
    }]
  }
}
```

Similarly, auto-approve read-only operations (Read, Glob, Grep) that cannot modify state.

**Infinite loop prevention (Stop hooks):**

Stop hooks that block without checking `stop_hook_active` will trap Claude in an infinite loop. The mandatory pattern:

```python
import json, sys
data = json.load(sys.stdin)
if data.get('stop_hook_active', False):
    sys.exit(0)  # Already forced once — allow stopping
# ... run quality checks ...
```

**CLAUDE.md token economy (Medium article, T3):**

Keep CLAUDE.md under ~2,500 tokens. Longer files cause Claude to ignore sections. The corollary: when CLAUDE.md becomes long because Claude "keeps forgetting" a rule, convert that rule to a hook. This simultaneously shortens CLAUDE.md (improving signal-to-noise) and makes the rule actually enforced.

**Override mechanisms:**

The official docs note `"disableAllHooks": true` in any settings file to temporarily disable all hooks without deleting configuration. Per-hook, `"async": true` for background execution, and configurable `"timeout"` per hook.

**Security tradeoffs:**

Hooks execute arbitrary commands on the developer's machine with the developer's permissions. CVE-2025-59536 (Check Point Research, T2) demonstrated that `.claude/settings.json` is just a repository file — any collaborator with commit access can inject malicious hooks. Anthropic's fix: enhanced warning dialog before trusting a project's hooks.

Practical implication: treat `.claude/settings.json` hook changes with the same code review scrutiny as executable source files, not as configuration metadata.

**Command injection defense (official plugin skill, T1):**

Always validate and sanitize stdin in hook scripts:
```bash
set -euo pipefail
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')
# Validate format before processing
if [[ ! "$tool_name" =~ ^[a-zA-Z0-9_]+$ ]]; then
  echo '{"decision": "deny", "reason": "Invalid tool name"}' >&2
  exit 2
fi
```

Quote all shell variables. Never trust hook input as safe without validation.

---

### Sub-question 5: Real-world hook configurations

**Destructive command blocking (widely documented across T1, T3, T4):**

```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command' <<< "$(cat)")
if echo "$COMMAND" | grep -qE '(rm\s+-rf\s+.*(/|~)|DROP TABLE|git push --force)'; then
  echo "BLOCKED: Destructive command detected" >&2
  exit 2
fi
exit 0
```

The paddo.dev article lists patterns blocking: `rm -rf` with home paths, force push, production deployment commands, database drops, and AWS deletion commands.

**Sensitive file protection (T1 + T3 + T4):**

```bash
#!/bin/bash
FILE=$(jq -r '.tool_input.file_path' <<< "$(cat)")
PROTECTED=(".env" ".env.local" ".pem" "secrets/" ".git/config" "*.lock")
for pattern in "${PROTECTED[@]}"; do
  if [[ "$FILE" == *"$pattern"* ]]; then
    echo "BLOCKED: Sensitive file protected: $FILE" >&2
    exit 2
  fi
done
```

**Auto-format on every write (T1):**

Anthropic's own how-to-configure-hooks article shows this as the first example:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""}]
    }]
  }
}
```

**TypeScript type checking (T1 + T3):**
```json
{
  "matcher": "Edit",
  "hooks": [{
    "type": "command",
    "command": "if [[ \"$CLAUDE_FILE_PATHS\" =~ \\.(ts|tsx)$ ]]; then npx tsc --noEmit --skipLibCheck \"$CLAUDE_FILE_PATHS\" || echo '⚠️ TypeScript errors detected'; fi"
  }]
}
```

**Session context loading (T1 + T3):**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "git status --short && echo '---' && git log --oneline -5"
      }]
    }]
  }
}
```

**GitButler session branch isolation (T3):**

GitButler's production hook configuration isolates parallel Claude sessions into independent git branches using shadow index files:
```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "Edit|MultiEdit|Write", "hooks": [{"type": "command", "command": "but claude pre-tool"}]}],
    "PostToolUse": [{"matcher": "Edit|MultiEdit|Write", "hooks": [{"type": "command", "command": "but claude post-tool"}]}],
    "Stop": [{"hooks": [{"type": "command", "command": "but claude stop"}]}]
  }
}
```

This creates automatic rollback points per session without touching the working branch.

**Rulebricks dynamic guardrails (T4):**

The rulebricks/claude-code-guardrails repository uses a PreToolUse hook wired to an external decision engine for dynamic, updateable policy:
- Three matchers: `Bash`, `Read|Write|Edit`, `mcp__*`
- Policies managed at rulebricks.com, not in the repo
- Instant policy updates without restarting Claude Code
- Audit trails for compliance

**everything-claude-code production hooks.json (T4):**

The affaan-m/everything-claude-code repository's `hooks.json` shows a production pattern covering:
- PreToolUse: git hook bypass protection, dev env setup (tmux sessions), commit validation, secrets detection, MCP health verification
- PostToolUse: command auditing, cost tracking, PR creation logging
- Stop: batch formatting + type checking, console.log detection, session state persistence, desktop notifications
- SessionStart/SessionEnd: context loading, package manager detection

**Codacy MCP security integration (T3):**

The Codacy article describes using MCP (not hooks directly) for real-time security scanning, but includes hook-compatible patterns in CLAUDE.md: mandatory `codacy_cli_analyze` after each file edit, Trivy for dependency scanning after `npm install`. This represents a hybrid: MCP tools for scanning, CLAUDE.md rules enforcing their invocation — a case where MCP tools and advisory rules substitute for hooks.

**Linter config protection (T4 from everything-claude-code):**

Block modifications to `.eslintrc`, `prettier.config.js`, `pyproject.toml` (linter sections) with a governance hook. If Claude tries to weaken a lint rule to make errors go away, the hook blocks it and redirects Claude to fix the code instead.

**Rate limiting MCP calls (T3 from aiorg.dev):**

Track MCP tool invocations and block repeated calls exceeding thresholds within time windows — useful for preventing runaway external API consumption.

**Desktop notification on session completion (T1 example):**

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": "osascript -e 'display notification \"Claude finished!\" with title \"Claude Code\"'"
      }]
    }]
  }
}
```

**Cross-platform notes:**
- macOS: `osascript` for notifications
- Linux: `notify-send`
- Windows: hooks use PowerShell via `"shell": "powershell"`

## Findings

1. **Hooks are infrastructure, not prompts.** Exit code 2 is non-negotiable enforcement; no LLM reasoning can override it. CLAUDE.md is advisory; hooks are deterministic.

2. **PreToolUse is the highest-leverage event.** It is the only event that can prevent tool execution, modify tool inputs, and implement true security gates.

3. **Stop hooks need loop prevention.** Always check `stop_hook_active` before blocking. Without this guard, quality-gate hooks create infinite loops.

4. **Latency scales with synchrony.** Keep blocking hooks fast. Defer logging, metrics, and notifications to async hooks. Agent hooks (full Claude subagents) carry significant API cost — reserve for high-value completion gates.

5. **Configuration files are executable.** CVE-2025-59536 proved `.claude/settings.json` is an attack surface. Review hook changes with the same scrutiny as source code.

6. **The canonical division of labor:** CLAUDE.md for context and philosophy; hooks for operations that must happen every time without exception. If Claude keeps forgetting a CLAUDE.md rule, convert it to a hook.

7. **Graduated enforcement reduces friction.** Start with warnings, monitor false positives, then escalate to blocking only for genuinely dangerous operations.

## Challenge

### Methodology

Counter-evidence searches run April 9, 2026. Queries targeted: (1) official hooks reference at code.claude.com, (2) GitHub issues against anthropics/claude-code, (3) NVD/Check Point CVE records. Findings compared against specific claims in this document.

---

### Claim 1 — Hook types list (PreToolUse, PostToolUse, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, PermissionRequest, PostToolUseFailure, Stop, SubagentStop, SubagentStart, Notification, PermissionDenied, PostCompact)

**Strength: MODERATE — mostly confirmed, but the list as presented is incomplete and slightly misframed.**

Core findings:
- All 14 events named in this document are confirmed in the official hooks reference (code.claude.com/docs/en/hooks). No speculative or community-only events were found among them.
- The document presents these 14 events as a near-complete picture. The actual official event set is substantially larger — approximately 21–25 events as of early 2026. Events confirmed in official docs but absent from this document include: `WorktreeCreate`, `WorktreeRemove`, `TeammateIdle`, `TaskCompleted`, `StopFailure`, `ConfigChange`, `CwdChanged`, `Elicitation`, `ElicitationResult`, `FileChanged`, `InstructionsLoaded`.
- `TeammateIdle` and `TaskCompleted` have a documented history: they were added in v2.1.33 but omitted from the docs table for weeks (GitHub issue #23545), and their JSON decision-control semantics were again outdated in the docs as of issue #30574 (March 2026). This confirms even the official docs have lagged the implementation — a gap this document does not note.
- The Pixelmojo T3 source in this document's sources table claims "All 12 Events" in its title; the actual count has grown beyond 12, indicating third-party sources are themselves stale.

**Flag:** The framing "as of 2026, the documented event set includes" should be read as a subset, not an exhaustive list. The document's event taxonomy covers the highest-traffic events well but omits the multi-agent and worktree event families entirely.

---

### Claim 2 — "Exit code 2 blocks; exit code 0 allows; other non-zero triggers error"

**Strength: HIGH — confirmed from official docs, with one real-world caveat.**

The three-tier exit code model (0 = success, 2 = blocking, other = non-blocking) is directly documented in the official hooks reference. The claim that "exit code 1 is treated as non-blocking error" is stated correctly.

One caveat the document does not flag: GitHub issue #4809 documents a confirmed bug where PostToolUse hooks with exit code 1 blocked execution despite the documentation saying non-blocking. This has been present in the bug tracker long enough to indicate the implementation has diverged from the spec at times. The document presents exit code semantics as rock-solid; in practice, non-blocking behavior for exit 1 has been unreliable in at least one hook event type.

---

### Claim 3 — CVE-2025-59536 (malicious hooks in cloned repos enabling RCE)

**Strength: HIGH — CVE exists, is accurately characterized, with one nuance.**

The CVE is real: confirmed in NVD (nvd.nist.gov/vuln/detail/CVE-2025-59536), Check Point Research, The Hacker News, The Register, and DevOps.com. CVSS score 8.7. Published October 2025, disclosed by Check Point Research in February 2026.

The document's characterization — that `.claude/settings.json` in a repo can inject malicious hooks executing on SessionStart — is accurate. The vulnerability class is configuration injection, not a memory corruption bug; it exploits the trust dialog bypass in versions before 1.0.111.

Nuance: the document says "any collaborator with commit access can inject malicious hooks." The CVE's actual attack surface is broader: it requires only that a victim clone a repo and open it in Claude Code — the attacker does not need commit access to a legitimate repo. Crafting a purpose-built malicious repo is sufficient. This makes the threat slightly more severe than the document implies. A companion CVE (CVE-2026-21852) covering MCP server injection from the same report is not mentioned.

---

### Claim 4 — "`stop_hook_active` prevents infinite Stop-hook loops"

**Strength: HIGH — confirmed as officially documented.**

The `stop_hook_active` boolean in the Stop hook JSON input payload is documented in the official hooks reference (code.claude.com/docs/en/hooks). Multiple T1 and T3 sources confirm the field and its purpose. The document's code pattern for checking it is consistent with official examples. No counter-evidence found.

---

### Claim 5 — "PreToolUse uniquely supports four decisions: allow/deny/ask/defer"

**Strength: HIGH — confirmed, with one version-scoping note the document omits.**

All four `permissionDecision` values (allow, deny, ask, defer) are documented in the official hooks reference. The precedence order (deny > defer > ask > allow) is confirmed.

Omission: the `defer` value requires Claude Code v2.1.89 or later per official docs. The document presents all four decisions as uniformly available without noting this version constraint. Teams on older installs would not have `defer` available.

A GitHub issue (#15486 "[DOCS] Document support for 'ask' in deprecated PreToolUse decision field") notes the top-level `decision` field was deprecated in favor of `hookSpecificOutput.permissionDecision`. The document correctly uses `hookSpecificOutput`, but the deprecated path still works in some versions — a migration nuance the document does not mention.

---

### Claim 6 — "Keep hooks under 1 second" (latency recommendation)

**Strength: LOW — practitioner inference, not an official Anthropic recommendation.**

No official Anthropic documentation specifies a "1 second" threshold. The recommendation in this document ("Community guidance: Keep synchronous hooks under 1 second") appears to originate from practitioner inference and community blog posts, not the official docs. Third-party sources cite targets ranging from "under 200ms" (blakecrosley.com) to "under 500ms" (getaiperks.com, hexdocs) to "under 2 seconds" (other community posts) — there is no community consensus either.

The official docs acknowledge latency impact but specify only the per-hook configurable timeout, not a latency target. The ~20s latency report cited in this document is real (GitHub issue ruvnet/ruflo #1530), but it describes a misconfiguration (11+ hooks spawning Node.js processes per event), not a baseline characteristic.

The claim is reasonable engineering advice, but its authority is overstated by attributing it to "community guidance" without noting the absence of an official threshold.

---

### What This Research Does Not Cover

1. **Multi-agent hook events.** The `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, and `WorktreeRemove` events — which control multi-agent coordination and isolation workflows — are absent. These are officially documented and increasingly used in production agent-team configurations.

2. **Hook versioning and migration.** Several hook behaviors changed across minor versions (e.g., `defer` added in v2.1.89, `PostCompact` added in v2.1.76, JSON decision control for `TeammateIdle`/`TaskCompleted` added in v2.1.64). The document presents a static picture with no versioning caveats, which can mislead users on older installs.

3. **CVE-2026-21852.** The companion CVE in the same Check Point report — covering MCP server injection via repository config — is not mentioned. The attack surface is broader than hooks alone.

4. **Hook debugging and observability.** No coverage of how to diagnose hook failures, inspect hook output in the transcript, or profile hook latency (cf. claudekit hook-profiling docs).

5. **Prompt and agent hook evaluation mechanics.** The document lists these handler types but does not cover how prompt hooks receive/return JSON, how agent hooks communicate decisions back, or the cost implications of spawning full Claude sessions as hooks.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claude Code supports 14 hook event types (PreToolUse, PostToolUse, PostToolUseFailure, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, PostCompact, Stop, SubagentStop, SubagentStart, Notification, PermissionRequest, PermissionDenied) | Factual | T1 (S1, S2) | corrected — all 14 are confirmed in official docs, but the full event set is 21–25 events; the list is a subset, not exhaustive (multi-agent and worktree events omitted) |
| 2 | Exit code 2 is the only exit code that blocks execution; exit code 0 means success; any other non-zero is a non-blocking error | Factual | T1 (S1) | verified — confirmed directly in official hooks reference; one caveated bug (PostToolUse exit 1 occasionally blocked, GitHub #4809) not noted in document |
| 3 | CVE-2025-59536 enables RCE via malicious hooks in `.claude/settings.json` in cloned repos | Factual | T2 (S16) | corrected — CVE is real with CVSS 8.7; disclosed by Check Point February 2026, not just "October 2025"; attack surface is broader than stated (cloning any malicious repo is sufficient; attacker does not need commit access to a legitimate repo) |
| 4 | `stop_hook_active` boolean in Stop hook input prevents infinite loops | Factual | T1 (S1) | verified — field and purpose confirmed in official hooks reference |
| 5 | PreToolUse supports four `permissionDecision` values: allow, deny, ask, defer | Factual | T1 (S1) | verified — all four confirmed in official docs; `defer` requires v2.1.89+ (version constraint not noted in document) |
| 6 | The correct field for PreToolUse decisions is `hookSpecificOutput.permissionDecision`, not a top-level `decision` field | Factual | T1 (S1) | verified — top-level `decision` field is deprecated; `hookSpecificOutput.permissionDecision` is the current form |
| 7 | PreToolUse conflict resolution order: deny > defer > ask > allow | Factual | T1 (S1) | verified — precedence order confirmed in official hooks reference |
| 8 | Synchronous hooks should be kept under 1 second | Prescriptive | T3 (S5–S10, S14) | human-review — no official Anthropic doc specifies a 1-second threshold; community sources cite conflicting targets (200ms to 2s); this is practitioner inference only |
| 9 | CLAUDE.md instructions are advisory; hooks are deterministic and cannot be overridden by LLM reasoning | Conceptual | T1 (S2), T3 (S7, S8) | verified — explicitly stated in Anthropic Best Practices documentation and corroborated by multiple T3 sources |
| 10 | Setting `"async": true` prevents a hook from blocking via exit code 2 | Factual | T1 (S1) | verified — confirmed in official docs; async hooks run in background and cannot gate execution |
| 11 | Hooks receive JSON on stdin including `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`, `tool_name`, `tool_input`, and `tool_use_id` | Factual | T1 (S1) | verified — input schema confirmed in official hooks reference |
| 12 | JSON output from hooks is capped at 10,000 characters | Factual | T1 (S1) | verified — official docs document the 10,000 character cap |
| 13 | `.claude/settings.json` can be committed to git and applies hooks to all users who clone the repo | Factual | T1 (S1, S2), T2 (S16) | verified — confirmed in configuration docs and demonstrated by CVE-2025-59536 |
| 14 | The ~20-second latency issue cited in community reports was caused by misconfiguration (11+ hooks spawning Node.js processes per event), not a baseline characteristic | Contextual | T3–T4 (community) | human-review — GitHub issue referenced (ruvnet/ruflo #1530) is real, but root-cause attribution to a specific misconfiguration is from community analysis, not official Anthropic docs |
| 15 | `disableAllHooks: true` in any settings file temporarily disables all hooks without deleting configuration | Factual | T1 (S1) | verified — confirmed in official hooks reference |
