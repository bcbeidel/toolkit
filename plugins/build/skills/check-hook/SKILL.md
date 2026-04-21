---
name: check-hook
description: >
  Audits Claude Code hooks configuration for event coverage, script safety,
  async and blocking contradictions, Stop hook loop risks, rule overlap,
  and idempotency. Use when the user wants to "audit hooks", "check hooks",
  "review hooks", "check my hooks", "what quality gates are missing", or
  "are my hooks safe".
argument-hint: "[settings.json path]"
user-invocable: true
references:
  - references/platform-limitations.md
---

# Check Hook

Inspect a project's Claude Code hooks configuration for coverage gaps,
misconfigurations, unsafe patterns, and redundancy. Read-only — reports
findings but does not modify any files.

## 1. Input

If `$ARGUMENTS` is non-empty, read the settings file at that path. Otherwise,
read hooks from both of these default locations (use whichever exist):
- `.claude/settings.json`
- `.claude/settings.local.json`

If neither location exists, or neither contains a `hooks:` key, report
this as the first finding before running any checks:

> **No hooks configured** (warn) — No hooks found in `.claude/settings.json`
> or `.claude/settings.local.json`. PreToolUse hooks provide deterministic
> enforcement that CLAUDE.md instructions cannot guarantee.

Then continue to the Event coverage check, which will also fire.

## 2. Primitive Routing

Before running numbered checks, scan `CLAUDE.md` (if it exists) for rules that match any of the three conversion signals — rules that belong in hooks but are currently advisory only:

1. The rule is one Claude keeps violating under normal conditions
2. The rule can be expressed as a shell one-liner (format check, test gate, naming pattern)
3. The rule requires enforcement at a specific lifecycle moment (before a tool call, at session end)

For each matching rule found: flag as `warn`, quote the rule text, and note which signal it matches. Suggest converting to a PreToolUse hook.

## 3. Platform Scope

Run alongside the numbered checks in step 4. Cross-platform findings are appended as a separate section of the report in step 5.

These checks target Claude Code (`settings.json` / `settings.local.json`). If the project's hooks may run on additional platforms, read [platform-limitations.md](references/platform-limitations.md) and flag the relevant limitations in the report.

## 4. Checks

Run sixteen checks. For each configured hook, apply all relevant checks.

### 1. No hooks / PreToolUse gap

Is a `PreToolUse` hook present?

`PreToolUse` is the only event that can block tool execution (via exit
code 2). Flag as `warn` if no `PreToolUse` hook is present, with a note that
quality-gate enforcement requires PreToolUse.

### 2. Script safety

For each hook using `"type": "command"`, read the command string. Flag
as `fail` if it contains:
- `rm -rf`
- `git reset --hard`
- `git checkout .`
- `git push --force` or `git push -f`

These operations are irreversible and should never run automatically
without explicit user intent.

### 3. Async + blocking contradiction

For each hook, check whether `"async": true` is set alongside a script
that contains `exit 2` logic, or is described as a gate or blocker.

Async hooks run in the background after execution proceeds — they can
never block regardless of exit code. A hook that needs to block must be
synchronous (the default; `async` omitted or `false`).

Flag as `fail` if `async: true` is paired with blocking intent.

Also flag as `warn` for Python hook scripts that use `sys.exit(1)` to signal validation failure, or that have no explicit `sys.exit(2)` in exception handlers. Python uncaught exceptions default to exit code 1 — non-blocking. A Python validator that throws exits 1, showing a hook error in the transcript while execution proceeds silently.

Also flag as `warn` if a hook writes structured JSON output (`hookSpecificOutput`, `systemMessage`, or raw stdout) that could exceed 10,000 characters in practice — hook stdout is capped at 10,000 characters and truncated silently, which corrupts structured JSON responses.

Also flag as `warn` if a hook emits JSON on stdout but any non-zero exit path precedes or follows the emission — Claude Code parses stdout only on exit 0; stdout on any non-zero exit is discarded, so a JSON block emitted on exit 2 is silently lost. For the same reason, flag as `warn` if a JSON-emitting hook omits `hookSpecificOutput.hookEventName` (spec-required field) or emits leading non-JSON text (e.g., `echo "info" ; jq -n '...'`) — "JSON validation failed" errors surface in the transcript with no block effect.

### 4. Stop hook loop risk

For any `Stop` or `SubagentStop` hook that may exit 2, check whether a re-entry guard is present.

**`SubagentStop`:** The payload includes a `stop_hook_active` boolean field. Check that the script reads this field and exits 0 when it is `True`. Without this guard, a blocking SubagentStop hook forces Claude to keep responding indefinitely.

**`Stop`:** The payload does not include `stop_hook_active` (it includes `stop_reason` instead). An equivalent re-entry guard is still required — check that the script uses a session-scoped mechanism (e.g., a temp file keyed to `session_id`) to detect and short-circuit repeated firing.

Flag as `fail` for any Stop or SubagentStop hook that may exit 2 but contains no re-entry guard of either form.

Also flag as `warn` for SubagentStop hooks that exit 2 and use `stop_hook_active` alone without inspecting `last_assistant_message` (the subagent's most recent output) for progress indicators. Spec recommends layering both: `stop_hook_active` shortcircuits the infinite re-fire, while the `last_assistant_message` check lets the block resolve naturally once the subagent satisfies the requirement — without it the hook remains a hard gate that the subagent cannot learn to pass.

### 5. Stdin correctness

For each `"type": "command"` hook, check whether the script body contains `INPUT=$(cat)` or equivalent stdin consumption. Scripts that skip this will hang or fail silently when the hook payload exceeds the OS pipe buffer — a common failure on large files. Flag as `warn`.

Also check that each command hook's script file is executable (`chmod +x`). A non-executable script silently fails with no distinguishing error from a hook that isn't loaded. Flag as `warn`. Also flag as `warn` if a hook command spawns a subshell and the project's shell profiles (`.bashrc`, `.zshrc`) contain unconditional output statements; output emitted during non-interactive hook execution is prepended to hook stdout and corrupts the JSON payload parse. Guard pattern: `if [[ $- == *i* ]]; then`.

### 6. Tool name case mismatch and path expansion

For each hook with a `matcher` field, verify the tool name uses exact canonical casing: `Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Agent`, `NotebookEdit`, `NotebookRead`. A matcher on `bash` or `write` silently matches nothing, disabling the hook without any error. Flag as `fail`.

Also check each hook's `"command"` field in `settings.json` for `$HOME` or `~`. Both have been observed to expand inconsistently across versions and silently fail to load the script; the spec's reference pattern is `"$CLAUDE_PROJECT_DIR"/.claude/hooks/<name>.sh` (or an absolute path), which resolves regardless of cwd. Flag as `warn`.

### 7. Enforcement intent on PostToolUse

`PostToolUse` fires after execution and cannot prevent it — a
`PostToolUse` hook intended to block is a misconfiguration that silently
fails to enforce. Flag as `warn` for any `PostToolUse` hook whose script
or description suggests a blocking or gating intent.

Also flag as `warn` if the project may run under `claude -p` and uses `AskUserQuestion` or `ExitPlanMode` without a `PreToolUse` hook that returns `permissionDecision: "allow"` plus an `updatedInput` supplying the answer. Per spec, those tools block in non-interactive mode; the documented workaround is a PreToolUse hook that pre-answers them. Enforcement logic that must fire under `-p` must be anchored on `PreToolUse`, not on interactive-only events.

Also flag as `warn` if more than one `PreToolUse` hook targeting the same tool name returns `updatedInput`. Hooks run in parallel; the last to finish wins. Multiple hooks rewriting the same tool's input produce non-deterministic results with no runtime warning — consolidate input modifications for a given tool into one hook.

Also flag as `warn` for any blocking `PreToolUse` hook (exit 2 paths present) that has no companion warning-only hook on the same matcher and no comment in the script indicating a prior warning phase has been completed. Best practice: deploy with `exit 1` (warn only) for at least a week before graduating to `exit 2` (block). One false positive per session is sufficient to establish a bypass habit that defeats the gate permanently.

Also flag as `warn` if user-level hooks (`~/.claude/settings.json`) exist alongside project hooks — user-level hooks fire in all projects, including CI automation. Enforcement designed for local use silently applies in GitHub Actions and other automated pipelines.

### 8. Rule overlap

Read `CLAUDE.md` (if it exists) and check whether any hook duplicates an
instruction already expressed there.

Overlap is not always wrong — a hook that enforces a CLAUDE.md rule
deterministically is intentional belt-and-suspenders. But one of the two
may be stale, or the hook may have been added without knowing the rule
already exists.

Flag as `warn` for each overlap found, noting which CLAUDE.md instruction
the hook may duplicate.

### 9. Idempotency

For each hook script, check for patterns that accumulate state across
invocations:
- Unbounded appending to a log file without rotation
- Incrementing a counter without a reset mechanism
- Creating files that are never cleaned up

Running a hook twice should produce the same result. State accumulation
is a sign the hook will degrade over time.

Flag as `warn` per pattern found.

### 10. Latency risk

For each synchronous hook (no `async: true`), check whether the command calls an LLM, makes a network request, or runs a slow external process (e.g., `curl`, `claude`, a Python script that imports large models). Synchronous hooks block Claude while they run; slow hooks create session sluggishness that accumulates across a session and generates pressure to bypass hooks entirely. Flag as `warn` for any hook whose command string suggests a network call or LLM invocation in the hot path.

### 11. Script safety preamble

For each readable hook script (command type), check whether it begins with `set -Eeuo pipefail`. This preamble converts silent failures — commands exiting non-zero without aborting the script — into explicit exits. Flag as `warn` if absent. Also flag as `warn` any detection command (`grep`, `diff`, `test`, `[`) that appears outside an `if` condition without a `|| true` guard; these commands' legitimate non-zero exits trip `-e` and abort the hook prematurely, producing false-positive blocks on normal operations.

### 12. Injection safety

For each hook script, flag as `fail` if the script passes a payload-derived variable to `eval` (e.g., `eval "$command"` where `command` is extracted from `tool_input`). Hook payloads are user-influenced — `tool_input.command` in Bash hooks reflects what the user asked Claude to run — and `eval` on user-controlled data is a shell injection vector with no safe sanitization path. Also flag as `warn` for unquoted variable expansions on payload-derived values (`$var` instead of `"${var}"`); unquoted variables undergo word-splitting and globbing that payload content can exploit. Evidence suggests bare command names (`jq`, `grep`) are susceptible to PATH override in adversarial environments — flag as `warn` for hooks defined in project-level `settings.json` (where any collaborator with commit access can influence the environment) or hooks with evidence of CI usage (e.g., a `.github/` directory exists), where PATH may be injected by the build environment (MODERATE confidence from a single T5 source).

### 13. jq availability and field path correctness

For each hook script that calls `jq`, check whether `jq` availability is verified before use (e.g., `command -v jq &>/dev/null`). Claude Code runs hooks with a restricted PATH; `jq` is not guaranteed on all systems. A missing `jq` causes the hook to fail in an uncontrolled way — silently passing (exit 0) or blocking everything (exit 2) — depending on script structure. Flag as `warn` if no availability check is present. Also check that jq field paths match the target tool's `tool_input` schema: `jq -r '.tool_input.command'` is correct for Bash hooks but returns `null` silently for Write hooks (`.tool_input.file_path`). Flag as `warn` for scripts whose matcher targets a tool whose `tool_input` structure differs from what the jq path assumes.

If the hook may run on Copilot, flag as `fail`: Copilot serializes tool arguments as `toolArgs` (a JSON string), not as `tool_input` (an object). Hooks using `jq '.tool_input.*'` fail silently on Copilot — cross-platform hooks require a platform detection branch or separate configurations.

### 14. ShellCheck static analysis

For each hook script (command type), check whether there is evidence it has been run through ShellCheck (e.g., a CI step, a pre-commit hook, or a comment). ShellCheck is the de facto static analysis standard for bash — it catches quoting issues, deprecated backtick syntax, incorrect conditionals, and command misuse. Flag as `warn` if no ShellCheck integration is apparent. Note: ShellCheck passing is a floor, not a ceiling — wrong exit code intent and incorrect jq field paths are logic errors invisible to static analysis.

Also flag as `warn` if ShellCheck appears to be disabled wholesale (e.g., `# shellcheck disable` with no rule number, or ShellCheck absent from CI). Hook scripts commonly trigger false positives on jq-assigned variables (SC2034) and intentionally single-quoted JSON strings (SC2016) — these should be suppressed inline or via `.shellcheckrc`, not by disabling ShellCheck entirely.

Also flag as `warn` if `shfmt` is absent from the project's formatting or CI pipeline alongside ShellCheck. ShellCheck catches bugs; `shfmt` enforces consistent formatting — both together constitute complete static analysis coverage for bash hook scripts.

### 15. Script style conventions

Evidence suggests several MODERATE-confidence style conventions reduce silent failures in hook scripts. Flag as `warn` if: (a) error or blocking messages go to stdout rather than stderr (`>&2`) — stdout is for structured JSON output on exit 0; stderr is what Claude reads on blocking exits and what appears in the transcript; (b) conditionals use `[` instead of `[[` in bash scripts — `[[` does not word-split unquoted variables and supports `=~` for regex matching; (c) `set -x` appears in a committed hook script — in production it floods stderr with trace output and can leak sensitive payload values; (d) the shebang is `#!/bin/bash` rather than `#!/usr/bin/env bash` — the `env` form locates whichever `bash` is active in `$PATH` and is more portable across NixOS, Homebrew-managed bash, and other non-standard installations where bash is not at `/bin/bash`.

### 16. settings.json as attack surface

Check whether hooks are defined in project-level `.claude/settings.json` (checked into the repo) versus `.claude/settings.local.json` (gitignored, personal only). Project-level hook entries execute automatically on any developer who opens the repo — a collaborator with commit access can inject arbitrary commands (CVE-2025-59536). Flag as `warn` for any hook in project `settings.json` that has not been treated with the same code-review scrutiny as executable source files. Flag as `warn` if security-sensitive hooks (credentials protection, command blocking) live in `settings.json` where they are also visible and modifiable by the full team — suggest moving personal-only enforcement to `settings.local.json`.

## 5. Report

Present findings as a table with a summary count at the top:

```
N issues across M hooks (X fail, Y warn)

event          | hook command          | check             | finding
---------------+-----------------------+-------------------+---------------------------
PostToolUse    | .claude/hooks/gate.sh | Event coverage    | PostToolUse cannot block; use PreToolUse for enforcement
Stop           | .claude/hooks/stop.sh | Stop hook loop    | No stop_hook_active guard — infinite loop risk
PostToolUse    | lint-after-write.sh   | Async + blocking  | async:true with exit 2 — hook will never block
```

If cross-platform gaps were identified in Platform Scope, append a separate section to the report:
```
**Cross-platform limitations:** [list each platform and its specific gap]
```

If no issues are found, confirm:
> "Hooks look well-configured."

## Anti-Pattern Guards

1. **Treating rule overlap as always wrong** — hook + CLAUDE.md duplication can be intentional belt-and-suspenders; flag for user decision, don't recommend removal
2. **Skipping Primitive Routing when no hooks exist** — always scan CLAUDE.md for conversion signals even when there are no hooks; absence of hooks is itself a coverage gap worth surfacing
3. **Reading settings files from outside the current project** — only read `.claude/settings.json` and `.claude/settings.local.json` under the current project root unless the user provides an explicit path argument

## Key Instructions

- Read-only — do not modify any files; report findings only
- Always run Primitive Routing before numbered checks, even when no hooks are configured
- Stop hook loop risk (check 4) is a fail, not a warn — an unguarded blocking Stop hook creates an infinite loop that requires a session kill to recover

## Handoff

**Receives:** Settings file path (optional); reads `.claude/settings.json` and `.claude/settings.local.json` by default
**Produces:** Findings table per hook; read-only — no files modified
**Chainable to:** build-hook (to create or fix a hook based on findings)
