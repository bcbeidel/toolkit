---
name: Hook Audit Dimensions
description: Scoreable rubric for /build:check-hook. Each dimension has pass/fail criteria, severity, and the hook-best-practices.md section it enforces.
---

# Hook Audit Dimensions

Sixteen dimensions grouped as Structure (6), Safety (7), and Maintenance (3).
Each dimension enforces a specific section of
[hook-best-practices.md](../../../_shared/references/hook-best-practices.md).

## Tier-2 — Structure

### event-matcher-fit

**What:** The hook fires on the right lifecycle event for its enforcement goal, and the matcher selects the intended tool invocations with correct syntax.
**Pass:** Blocking goals use a blockable event (PreToolUse, UserPromptSubmit, etc.). Matcher uses canonical tool casing (`Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, `NotebookRead`). Matcher syntax matches the event's evaluation tier (exact/pipe/regex/wildcard, or literal list for FileChanged).
**Fail:** Blocking intent on a non-blockable event (most commonly PostToolUse). Matcher uses lowercase or typo'd tool name (silently matches nothing). Regex syntax in FileChanged (interpreted as literal list; matches nothing).
**Severity:** `fail`
**Principles section:** §Anatomy §Event selection, §Anatomy §Matcher syntax

### exit-code-contract

**What:** Command hooks signal pass/warn/block through the correct exit code, and Python hooks handle exceptions explicitly.
**Pass:** Blocking paths call `exit 2` (bash) or `sys.exit(2)` (Python, including in exception handlers). Warn paths use `exit 1`. Pass paths use `exit 0`. Python hooks do not rely on uncaught exception fall-through.
**Fail:** Blocking intent expressed as `exit 1` or uncaught Python exception (both silently non-blocking). Python hook with no explicit `sys.exit(2)` in exception handlers.
**Severity:** `fail`
**Principles section:** §Anatomy §Exit codes and the JSON output contract

### stdin-consumption

**What:** Command hooks consume stdin before the pipe buffer saturates, and the script file is executable.
**Pass:** Script contains `INPUT=$(cat)` (or equivalent stdin consumption) at or near the top. File has execute bit set.
**Fail:** No stdin consumption (hook hangs or fails silently on large payloads). File missing execute bit (silently fails indistinguishably from an unloaded hook).
**Severity:** `warn`
**Principles section:** §Anatomy §Payload schema and extraction

### json-output-contract

**What:** Structured JSON responses comply with the exit-0-only contract, include required fields, and fit within the 10,000-character cap.
**Pass:** JSON stdout appears only on exit 0 paths. Output begins directly with the JSON object (no leading text). `hookSpecificOutput.hookEventName` present. Output size under 10 KB in realistic cases. For PreToolUse, at most one hook per tool returns `updatedInput`.
**Fail:** JSON emitted on non-zero exit (silently discarded). Leading non-JSON text before the object. Missing `hookEventName` (triggers "JSON validation failed"). Output that can exceed 10 KB (silently truncated, corrupts JSON). Multiple PreToolUse hooks returning `updatedInput` for the same tool (race: last to finish wins).
**Severity:** `warn`
**Principles section:** §Anatomy §Exit codes and the JSON output contract

### async-blocking-coherence

**What:** Blocking intent and `async: true` do not coexist.
**Pass:** Synchronous hook (`async` omitted or `false`) with blocking paths (`exit 2`); or async hook with no blocking intent.
**Fail:** `"async": true` alongside `exit 2` paths or prose describing the hook as a gate/blocker. Async hooks run after execution regardless of exit code.
**Severity:** `fail`
**Principles section:** §Anti-Patterns (async: true with exit 2)

### command-path-expansion

**What:** The `"command"` field in `settings.json` uses a path form that resolves reliably.
**Pass:** `"$CLAUDE_PROJECT_DIR"/.claude/hooks/<name>.sh` or an absolute path. Plugin hooks may use `$CLAUDE_PLUGIN_ROOT` / `$CLAUDE_PLUGIN_DATA`.
**Fail:** `$HOME` or `~` in the path (expansion inconsistent across versions; hook silently fails to load).
**Severity:** `warn`
**Principles section:** §Anatomy §Path expansion variables

## Tier-2 — Safety

### stop-loop-guard

**What:** Blocking `Stop` and `SubagentStop` hooks have a re-entry guard that breaks infinite loops.
**Pass:** SubagentStop hooks exit 0 when `stop_hook_active == True`; optionally also inspect `last_assistant_message` for progress. Stop hooks use a session-scoped mechanism (e.g., temp file keyed to `session_id`) since `stop_hook_active` is absent from Stop payloads.
**Fail:** Blocking (`exit 2`) Stop or SubagentStop hook with no re-entry guard. Loop requires a session kill to recover.
**Severity:** `fail`
**Principles section:** §Patterns That Work (belt-and-suspenders Stop loops)

### destructive-operations

**What:** Hook scripts do not execute irreversible commands without explicit user action.
**Pass:** Script contains none of: `rm -rf`, `git reset --hard`, `git checkout .`, `git push --force`, `git push -f`.
**Fail:** Any of the above present in a command hook body.
**Severity:** `fail`
**Principles section:** §Safety & Maintenance

### injection-safety

**What:** Payload-derived values cannot trigger shell injection or PATH hijacking.
**Pass:** No `eval` on any value derived from `tool_input` / stdin payload. All shell expansions on payload values quoted as `"${var}"`. Bare command names absolute-pathed or guarded with `command -v` in adversarial environments (project `settings.json` with team commit access, CI contexts with `.github/`).
**Fail:** `eval "$command"` where `$command` comes from payload (shell injection, no safe sanitization). Unquoted payload expansions (word-splitting / glob exploitation).
**Severity:** `fail` for `eval` on payload; `warn` for unquoted expansions and bare commands in adversarial environments.
**Principles section:** §Anti-Patterns (eval on payload values; unquoted payload expansions)

### jq-handling

**What:** `jq` calls check availability, use tool-appropriate field paths, and account for cross-platform payload shape.
**Pass:** Availability check present (`command -v jq &>/dev/null` or equivalent). jq field paths match the matcher's tool (`.tool_input.command` for Bash, `.tool_input.file_path` for Write, etc.). Cross-platform hooks branch on payload shape or use separate configurations per platform.
**Fail:** Copilot-capable hook reading `.tool_input.*` — Copilot uses `toolArgs` (JSON string) and silently returns null.
**Severity:** `fail` for Copilot field-path mismatch; `warn` for missing availability check or field-path mismatch vs matcher's tool.
**Principles section:** §Anatomy §Payload schema and extraction

### shell-hygiene

**What:** Shell scripts use the safety preamble, route output correctly, and follow portable conventions.
**Pass:** Starts with `set -Eeuo pipefail`. Detection commands (`grep`, `diff`, `test`, `[`) that legitimately exit non-zero are guarded with `|| true` or inside `if`. Errors route to stderr (`>&2`). `[[` used over `[`. No committed `set -x`. Shebang is `#!/usr/bin/env bash`, not `#!/bin/bash`.
**Fail:** Missing `set -Eeuo pipefail`. Detection commands outside `if` without `|| true` (legitimate non-zero exits trip `-e` and abort prematurely — false-positive blocks). Errors to stdout instead of stderr. Bare `[` in bash. Committed `set -x` (floods stderr; leaks payload values).
**Severity:** `warn`
**Principles section:** §Safety & Maintenance (shell hygiene preamble; output routing)

### attack-surface

**What:** Hook placement and content reflect the attack surface of `settings.json` (CVE-2025-59536).
**Pass:** Hooks in project `settings.json` treated as executable code in review. Security-sensitive or personal-only hooks in `settings.local.json`. User-level hooks (`~/.claude/settings.json`) absent when CI may run the project.
**Fail:** Security-sensitive hooks in project `settings.json` without evidence of code review. User-level hooks present alongside CI usage (enforcement designed for local ergonomics applies in GitHub Actions).
**Severity:** `warn`
**Principles section:** §Safety & Maintenance (attack surface)

### latency

**What:** Synchronous hooks do not create session sluggishness that pressures bypass.
**Pass:** Synchronous hook body stays under ~1 second in the hot path. LLM calls, network requests, and slow subprocesses (`curl`, `claude`, large Python imports) move to `async: true`.
**Fail:** Synchronous hook shells out to `claude` or `claude-code` (recursive-loop safety; spec-warned).
**Severity:** `fail` for recursive `claude` invocation; `warn` for suggested network/LLM in the hot path.
**Principles section:** §Safety & Maintenance (latency budget; recursive-loop safety)

## Tier-2 — Maintenance

### idempotency

**What:** Running the hook twice produces the same outcome.
**Pass:** No unbounded log appending, no unreset counters, no files that are never cleaned up.
**Fail:** State-accumulating pattern present (script degrades over time).
**Severity:** `warn`
**Principles section:** §Safety & Maintenance (idempotency)

### static-analysis

**What:** Hook scripts are covered by ShellCheck and `shfmt`.
**Pass:** Evidence of ShellCheck integration (CI step, pre-commit, script comment). `shfmt -i 2` integration alongside. False positives (SC2034 on jq-assigned vars, SC2016 on single-quoted JSON) suppressed inline or via `.shellcheckrc`.
**Fail:** ShellCheck disabled wholesale (`# shellcheck disable` without rule number, or absent from CI). `shfmt` absent.
**Severity:** `warn`
**Principles section:** §Safety & Maintenance (static analysis)

### claude-md-overlap

**What:** Hooks that duplicate CLAUDE.md instructions are surfaced for user judgment, not auto-removed.
**Pass:** Either no overlap with CLAUDE.md, or overlap is documented as intentional belt-and-suspenders.
**Fail:** Never — this dimension is always advisory.
**Severity:** `warn`
**Principles section:** §Safety & Maintenance (CLAUDE.md overlap)

### brief-presence-and-content

**What:** A `.briefs/<hook-name>.brief.md` exists at the repo root capturing the build's intent, carries the five required H2 sections (*User ask*, *So-what*, *Scope boundaries*, *Planned artifacts*, *Planned handoffs*), and the *So-what* paragraph names a specific enforcement gap rather than a category description.
**Pass:** Brief file exists; all five required sections are present; *So-what* names a specific scenario the hook prevents (a real near-miss, a class of mistakes the team kept making) rather than reading as "deterministically enforces X"; *Scope boundaries* lists concrete in/out items.
**Fail:** Brief is missing entirely; or one or more required sections are absent; or the *So-what* reads as a category description; or *Scope boundaries* is empty / vague.
**Severity:** `warn` (presence and content). Briefs are throw-away — a missing brief does not break the hook, but it leaves the build untraceable to its original intent. Hooks built before the brief pattern existed will trip this; a retroactive brief is acceptable.
**Principles section:** [brief-best-practices.md](../../../_shared/references/brief-best-practices.md) §What a Brief Is and §Anti-Patterns
