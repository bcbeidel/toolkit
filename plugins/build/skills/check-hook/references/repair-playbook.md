---
name: Hook Repair Playbook
description: Fix recipes for /build:check-hook findings. One entry per audit dimension with diagnosis and concrete remediation.
---

# Hook Repair Playbook

One entry per dimension in [audit-dimensions.md](audit-dimensions.md).
Each entry: **Finding** → **Diagnosis** → **Fix** (concrete, with snippet).

## Structure

### event-matcher-fit

**Finding:** Blocking intent on non-blockable event, or matcher that silently matches nothing.
**Diagnosis:** Blocking hook on PostToolUse — the tool has already run, exit 2 is ignored. Or: matcher uses non-canonical tool casing (`bash`, `write`).
**Fix:**
- Move blocking hooks to PreToolUse.
- Correct casing to canonical names (`Bash`, `Write`, `Edit`, `MultiEdit`, `Read`, `Glob`, `Grep`, `WebFetch`, `WebSearch`).
- For FileChanged, use `"matcher": ".envrc|.env"` as a literal list — never regex syntax.
- For regex matchers, include a non-alphanumeric character (`"mcp__memory__.*"`) to escape the exact-match tier.

### exit-code-contract

**Finding:** Blocking path uses `exit 1` or relies on uncaught exception; Python hook has no explicit `sys.exit(2)`.
**Diagnosis:** `exit 1` is non-blocking — transcript shows error, execution proceeds. Python uncaught exceptions exit 1 by default.
**Fix:**
```bash
# Bash blocking path
echo "blocked: ${reason}" >&2
exit 2
```
```python
# Python blocking path, including in handlers
except Exception as e:
    print(f"blocked: {e}", file=sys.stderr)
    sys.exit(2)
```

### stdin-consumption

**Finding:** Script lacks `INPUT=$(cat)` or is not executable.
**Diagnosis:** Scripts that do not drain stdin hang when the payload exceeds the OS pipe buffer. Non-executable scripts silently fail indistinguishably from an unloaded hook.
**Fix:**
- Add `INPUT=$(cat)` at or near the top of the script.
- `chmod +x .claude/hooks/<name>.sh`.

### json-output-contract

**Finding:** JSON on non-zero exit, missing `hookEventName`, leading non-JSON, >10 KB output, or multiple PreToolUse hooks returning `updatedInput` for the same tool.
**Diagnosis:** Claude Code parses stdout only on exit 0. The JSON object must be the entire stdout — any preceding text triggers "JSON validation failed." Output is truncated silently at 10,000 characters. Multiple `updatedInput` returns for the same tool race; last finisher wins.
**Fix:**
- Emit JSON only on `exit 0`; for blocks, use `exit 2` with a plain-text message to stderr.
- Ensure `hookSpecificOutput.hookEventName` is present.
- Keep `additionalContext` / `systemMessage` under ~8 KB as a safety margin.
- Consolidate all `updatedInput` logic for a given tool into one hook.

### async-blocking-coherence

**Finding:** `"async": true` on a hook with `exit 2` paths or blocking prose.
**Diagnosis:** Async hooks cannot block — they run after execution regardless of exit code.
**Fix:** Remove `"async": true` (synchronous is the default) if blocking is required. If the hook is genuinely non-blocking (observability, logging), remove `exit 2` paths.

### command-path-expansion

**Finding:** `settings.json` `"command"` field uses `$HOME` or `~`.
**Diagnosis:** Expansion is inconsistent across Claude Code versions; the hook silently fails to load.
**Fix:**
```json
"command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/<name>.sh"
```
Or use an absolute path. For plugin hooks, `"$CLAUDE_PLUGIN_ROOT"/...` is appropriate.

## Safety

### stop-loop-guard

**Finding:** Blocking Stop or SubagentStop hook without re-entry guard.
**Diagnosis:** The hook exits 2, Claude retries stopping, hook blocks again, loop requires session kill.
**Fix (SubagentStop):**
```bash
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false')
[[ "$STOP_ACTIVE" == "true" ]] && exit 0
```
**Fix (Stop — `stop_hook_active` absent):**
```bash
SESSION=$(echo "$INPUT" | jq -r '.session_id')
GUARD="/tmp/claude-stop-guard-${SESSION}"
[[ -f "$GUARD" ]] && exit 0
touch "$GUARD"
```
For production gates, layer: `stop_hook_active` + `last_assistant_message` progress check + session-scoped guard.

### destructive-operations

**Finding:** Script contains `rm -rf`, `git reset --hard`, `git checkout .`, or `git push --force`.
**Diagnosis:** Irreversible operations should never run automatically without explicit user intent.
**Fix:** Remove the destructive command. If cleanup is genuinely needed, move it to a user-invoked skill or make the path explicit (`rm -rf "${SPECIFIC_TMPFILE}"` not `rm -rf "$DIR"/*`).

### injection-safety

**Finding:** `eval` on payload value, unquoted payload expansions, or bare command names in adversarial environment.
**Diagnosis:** Payload fields reflect user input; interpreting them as shell is injection. Unquoted expansions word-split and glob.
**Fix:**
- Remove `eval`. If you must execute a derived command, use an array: `cmd=(executable --arg "$value"); "${cmd[@]}"`.
- Quote all expansions: `"${VAR}"`, never `$VAR`.
- Use absolute paths or guard with `command -v`:
  ```bash
  JQ=$(command -v jq) || { echo "jq required" >&2; exit 2; }
  "$JQ" -r '.tool_input.command'
  ```

### jq-handling

**Finding:** No jq availability check; jq field path mismatch for matcher's tool; Copilot compatibility issue.
**Diagnosis:** jq is not guaranteed in Claude Code's restricted PATH. Field paths are tool-specific (`.tool_input.command` for Bash but `.tool_input.file_path` for Write). Copilot uses `toolArgs` (JSON string), not `tool_input`.
**Fix:**
```bash
command -v jq &>/dev/null || { echo "jq required" >&2; exit 2; }
# Match field path to matcher tool:
# Bash: .tool_input.command
# Write: .tool_input.file_path
# Edit/MultiEdit: .tool_input.path
```
Copilot-capable hooks:
```bash
PLATFORM=$(echo "$INPUT" | jq -r 'if .toolArgs then "copilot" else "claude" end')
case "$PLATFORM" in
  claude) CMD=$(echo "$INPUT" | jq -r '.tool_input.command') ;;
  copilot) CMD=$(echo "$INPUT" | jq -r '.toolArgs | fromjson | .command') ;;
esac
```

### shell-hygiene

**Finding:** Missing `set -Eeuo pipefail`, unguarded detection commands, stdout errors, bare `[`, committed `set -x`, `#!/bin/bash` shebang.
**Diagnosis:** Missing preamble hides failures. Unguarded `grep`/`diff`/`test` trips `-e` on legitimate non-zero exits. stdout on blocking exits is discarded; stderr appears in transcripts. `[` lacks `[[`'s safety. `set -x` leaks payload.
**Fix:**
```bash
#!/usr/bin/env bash
set -Eeuo pipefail

# Detection with expected non-zero:
if grep -q "pattern" "$FILE"; then ...; fi
# Or:
grep -q "pattern" "$FILE" || true

# Errors to stderr:
echo "blocked: ${reason}" >&2
exit 2

# [[ over [:
if [[ "$VAR" == "value" ]]; then ...; fi
```
Remove committed `set -x` — uncomment locally only.

### attack-surface

**Finding:** Security-sensitive hook in project `settings.json` without review gate; user-level hooks alongside CI usage.
**Diagnosis:** Project `settings.json` executes for every collaborator who opens the repo (CVE-2025-59536). User-level hooks fire in CI automation too.
**Fix:**
- Personal-only enforcement → move to `.claude/settings.local.json` (gitignored).
- Team-wide enforcement in `settings.json` → add code-review requirement; document in CONTRIBUTING or README.
- Remove user-level hooks (`~/.claude/settings.json`) if the project runs in CI where they would apply out-of-scope.

### latency

**Finding:** Synchronous hook calls LLM, makes network request, or runs slow subprocess; or a hook invokes `claude` / `claude-code` (recursive).
**Diagnosis:** Synchronous hooks block Claude while running; slow hooks create bypass pressure. Recursive `claude` spawns compound exponentially.
**Fix:**
- Move non-critical slow work to `"async": true` (accepts it cannot block).
- For LLM-mediated decisions inside the hook path, use `"type": "prompt"` or `"type": "agent"` — not a shell-out to `claude`.
- Raise `timeout` only to accommodate realistic execution; a slow synchronous gate generates bypass culture.

## Maintenance

### idempotency

**Finding:** Hook accumulates state — log append without rotation, counter increment, orphan files.
**Diagnosis:** Running the hook twice produces different outputs; state degrades over time.
**Fix:**
- Log to `>>` with external rotation (`logrotate`) rather than unbounded append.
- Replace counters with event-sourced logs that derive count at read time.
- Clean up temp files on EXIT:
  ```bash
  trap 'rm -f "${TMPFILE:-}"' EXIT
  ```

### static-analysis

**Finding:** No ShellCheck / `shfmt` integration, or ShellCheck disabled wholesale.
**Diagnosis:** Static analysis catches quoting, deprecated syntax, and command misuse — bugs dynamic testing misses.
**Fix:**
- Add ShellCheck + `shfmt` to CI or pre-commit.
- Suppress false positives *inline* (`# shellcheck disable=SC2034` with the rule number) or in `.shellcheckrc` — never disable wholesale.
- Common hook-script false positives: SC2034 (jq-assigned vars), SC2016 (intentional single-quoted JSON).

### claude-md-overlap

**Finding:** Hook duplicates a CLAUDE.md instruction.
**Diagnosis:** Not always wrong. Belt-and-suspenders is intentional. One of the two may also be stale.
**Fix (user decision):**
- **Keep both:** no change; document the intent in a comment or CONTRIBUTING.
- **Drop CLAUDE.md entry:** remove the advisory line — the hook enforces deterministically.
- **Drop the hook:** if the advisory is sufficient and the hook generates false positives.

Never auto-resolve. The user chooses.
