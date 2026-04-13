---
name: Hook Quality Criteria
description: "Canonical rubric for evaluating Claude Code hook quality: structural requirements, anti-patterns, graduated deployment, testing strategies, and security criteria — used by check-hook"
type: reference
confidence: high
created: 2026-04-13
updated: 2026-04-13
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/hooks-guide
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
  - https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails
  - https://thinkingthroughcode.medium.com/the-silent-failure-mode-in-claude-code-hook-every-dev-should-know-about-0466f139c19f
  - https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-output-and-decision-control.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hook-testing-and-debugging.context.md
  - docs/research/2026-04-13-hook-quality-and-evaluation.research.md
---
A well-formed hook is deterministic, idempotent, fast, and scoped exactly to its stated goal. Quality breaks into two tiers: structural (verifiable by inspection) and behavioral (requires judgment about intent and deployment context).

## Tier 1: Structural Requirements (All Hooks)

**Exit code correctness**
- Blocking hooks must exit 2. Exit 1 is non-blocking — it shows a warning but execution continues. A hook that calls `exit 1` when it intends to block silently fails.
- `async: true` hooks can never block regardless of exit code — the action has already proceeded. Flag `async: true` paired with any `exit 2` logic as a misconfiguration.
- JSON `decision: block` output is parsed only on exit code 0. Returning `decision: block` with exit code 2 is redundant; exit code 2 ignores stdout.

**Stop/SubagentStop loop guard**
- Any Stop or SubagentStop hook that may exit 2 must check `stop_hook_active` (SubagentStop) or implement equivalent re-entry detection (Stop). Without this, a failing Stop hook traps Claude in an infinite loop.
- Required pattern for SubagentStop: `[ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ] && exit 0`

**Idempotency**
- Running the hook twice must produce identical outcomes. Flags: unbounded log appending without rotation, counter incrementing without reset, file creation that accumulates without cleanup. These degrade over time and produce unexpected behavior in long sessions.

**Script safety**
- Hooks must not contain `rm -rf`, `git reset --hard`, `git checkout .`, `git push --force`. These are irreversible and must never execute automatically without explicit user intent.

**Stdin correctness**
- All hook types receive stdin. Scripts that don't read stdin will hang or fail when the payload is larger than the OS pipe buffer. Pattern: `INPUT=$(cat)` at the top of every hook script, even if the payload isn't used.
- Shell profiles (`.bashrc`, `.zshrc`) that emit output on load corrupt the stdin JSON pipe. Scripts invoking subshells must suppress interactive-mode output: `if [[ $- == *i* ]]; then ...; fi`.

**Tool name case sensitivity**
- Matchers are case-sensitive. `bash` ≠ `Bash`. Verify against the canonical tool name list. A miscased matcher matches nothing and silently disables the hook.

**Path expansion in `"command"` fields**
- `$HOME` is not expanded in `settings.json` `"command"` values. A hook using `"$HOME/.claude/hooks/script.sh"` silently fails to load. Use `~` expansion or absolute paths. Verify the hook appears in `/hooks` after any path change.

**Known limitations**
- `PermissionRequest` hooks do not fire in non-interactive mode (`claude -p`). Any hook intended to enforce policy in CI or automation must use `PreToolUse` instead — `PermissionRequest` silently does nothing in headless runs.
- Multiple `PreToolUse` hooks returning `updatedInput` for the same tool produce non-deterministic results — hooks run in parallel and the last to finish wins. Consolidate all input modifications for a given tool into one hook.

## Tier 2: Behavioral Quality

**Event selection correctness**
- Enforcement (blocking) requires PreToolUse. PostToolUse, Stop, and other events that appear after execution cannot prevent the triggering action — only provide feedback. A PostToolUse hook described as a "gate" is an intent mismatch: it cannot gate what has already run.

**Scope precision**
- Matchers should be as specific as the enforcement goal requires. `"*"` on PreToolUse fires on every tool call — appropriate for session-wide security rules, not for formatting a single file type. Over-broad matchers create latency on every tool call.

**Latency budget**
- Synchronous hooks block Claude while they run. Keep synchronous hooks under 1 second. Use `async: true` for logging, notifications, and non-critical follow-up that doesn't need to gate. Agent hooks spawn full Claude sessions — significant API cost; reserve for high-value completion gates, not per-file operations.

**Graduated deployment**
- New hooks should start as warnings (exit 1 or stdout advisory) before graduating to blocks (exit 2). Monitor for one week to identify false positives before enforcing. One false positive per session is enough to cause `--no-verify` bypass culture. Tune patterns incrementally — one rule per week.

**No self-grading**
- Security validation must not rely on the same model that generated the content being validated. Hooks provide the deterministic enforcement layer independent of Claude's reasoning.

## Anti-Pattern Catalog

| Anti-pattern | Risk |
|---|---|
| `async: true` + `exit 2` logic | Hook never blocks — silently fails to enforce |
| Stop hook without loop guard | Infinite loop — Claude cannot stop |
| `exit 1` where `exit 2` intended | Non-blocking — warning only, enforcement fails |
| Missing `INPUT=$(cat)` | Hang or pipe buffer overflow on large payloads |
| Tool name miscased in matcher | Hook silently matches nothing |
| Blocking CLAUDE.md rule, no hook | Advisory only — subject to context dilution and probabilistic override |
| Destructive commands in hook script | Irreversible data loss triggered automatically |
| Broad matcher on slow script | Latency on every tool call; bypass pressure accumulates |
| Shell profile emitting output | Corrupts stdin JSON; hook silently fails or crashes |
| Python `sys.exit(1)` or uncaught exception | Exit 1 is non-blocking — validator fires but execution proceeds |
| jq path wrong for target tool type | jq returns null silently; blocking condition never matches |
| `PermissionRequest` hook in `-p` mode | Hook does not fire; enforcement silently absent in CI/automation |
| Multiple hooks writing `updatedInput` to same tool | Non-deterministic result — last hook to finish wins |
| `$HOME` in `"command"` field | `$HOME` not expanded in JSON; hook silently fails to load |

## Testing Strategies

**Test hooks in isolation before deployment:**
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf ~/"},"hook_event_name":"PreToolUse"}' \
  | .claude/hooks/safety-check.sh; echo "exit: $?"
```

**Verify `jq` availability** — hooks commonly depend on `jq`; fall back to `python3 -c "import json,sys; ..."` for portability.

**Confirm hook is loaded:** Use the `/hooks` menu in Claude Code or run `claude --debug` to observe hook execution.

**Verify script is executable:** `chmod +x .claude/hooks/<name>.sh` — a non-executable script silently fails.

**Monitor transcript for hook output:** `tail -f "$CLAUDE_PROJECT_DIR/.claude/transcripts/<id>.jsonl" | jq`

## Canonical Check Order for check-hook

1. No hooks configured → warn (PreToolUse gap)
2. Script safety (`rm -rf`, force-push) → fail
3. Async + blocking contradiction → fail
4. Stop/SubagentStop loop guard → fail
5. Missing `INPUT=$(cat)` in command hooks → warn
6. Tool name case mismatch in matcher → fail
7. Enforcement intent on PostToolUse → warn (cannot block)
8. Rule overlap with CLAUDE.md → warn
9. Idempotency (unbounded appends, counters) → warn
10. Latency risk (sync hook calling LLM or network) → warn
