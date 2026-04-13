---
name: "Hook Quality and Evaluation"
description: "Structural, behavioral, and security properties that distinguish well-formed Claude Code hooks from misconfigured ones; testing strategies and audit rubrics for hook validation"
type: research
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/hooks-guide
  - https://thinkingthroughcode.medium.com/the-silent-failure-mode-in-claude-code-hook-every-dev-should-know-about-0466f139c19f
  - https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3
  - https://blakecrosley.com/blog/claude-code-hooks-tutorial
  - https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
  - https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns
  - https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hook-matcher-syntax.context.md
  - docs/context/hook-output-and-decision-control.context.md
  - docs/context/hook-quality-criteria.context.md
  - docs/research/2026-04-07-hooks-ecosystem.research.md
---

I investigated what structural, behavioral, and security properties distinguish a well-formed Claude Code hook from a misconfigured or unsafe one, and what methods exist to test, evaluate, and audit hook configurations. This is a technical investigation targeting practitioners who author or audit hooks. Domain: Claude Code hooks (Anthropic, 2024–2026). Stack: shell/bash scripts, JSON payloads, `settings.json`. Preferred source types: official Anthropic docs (T1), security research (T2), production practitioners (T3).

## Research Question

What structural, behavioral, and security properties distinguish a well-formed Claude Code hook from a misconfigured or unsafe one — and what methods exist to test, evaluate, and audit hook configurations?

## Sub-Questions

1. What structural properties are required for a hook to function correctly?
2. What behavioral anti-patterns cause hooks to silently fail, produce unsafe outcomes, or degrade over time?
3. What testing and debugging strategies exist for validating hook scripts?
4. What does a comprehensive hook audit rubric look like, and how have practitioners implemented graduated enforcement?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/hooks | Hooks reference | Anthropic | 2026 | T1 | verified |
| 2 | https://code.claude.com/docs/en/hooks-guide | Automate workflows with hooks | Anthropic | 2026 | T1 | verified |
| 3 | https://thinkingthroughcode.medium.com/the-silent-failure-mode-in-claude-code-hook-every-dev-should-know-about-0466f139c19f | The Silent Failure Mode in Claude Code Hook Every Dev Should Know About | Thinking Through Code / Medium | Mar 2026 | T3 | verified (403) |
| 4 | https://dev.to/yurukusa/5-claude-code-hook-mistakes-that-silently-break-your-safety-net-58l3 | 5 Claude Code Hook Mistakes That Silently Break Your Safety Net | yurukusa / DEV | 2026 | T3 | verified |
| 5 | https://blakecrosley.com/blog/claude-code-hooks-tutorial | Claude Code Hooks Tutorial: 5 Production Hooks From Scratch | Blake Crosley | 2026 | T3 | verified |
| 6 | https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow | Claude Code Hook Control Flow | Steve Kinney | 2026 | T3 | verified |
| 7 | https://paddo.dev/blog/claude-code-hooks-guardrails/ | Claude Code Hooks: Guardrails That Actually Work | paddo.dev | 2026 | T3 | verified |
| 8 | https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/ | Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files | Check Point Research | 2026 | T2 | verified |
| 9 | https://www.pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns | Claude Code Hooks: All 12 Events with Examples | Pixelmojo | 2026 | T3 | verified |
| 10 | https://blog.codacy.com/equipping-claude-code-with-deterministic-security-guardrails | Equipping Claude Code with Deterministic Security Guardrails | Codacy | 2026 | T3 | verified |

## Raw Extracts

### Sub-question 1: Structural properties for correct hook operation

**stdin must be consumed (T1, hooks-guide):**
The official guide's protected-files example shows `INPUT=$(cat)` at the top of every hook script. This is not optional: if a hook does not read stdin, the OS pipe buffer can fill and block Claude Code when the JSON payload is large. Every hook — even one that doesn't use the payload — must consume stdin.

**Script executability is silently required (T1, hooks-guide):**
> "Hook scripts must be executable for Claude Code to run them"

A non-executable script silently fails to run. The required command: `chmod +x .claude/hooks/<name>.sh`. There is no error message distinguishing "script not found" from "script not executable" — both produce a hook error with no output.

**`$HOME` is not expanded in JSON config (T3, DEV):**
> "`$HOME` isn't expanded in the JSON config. The hook silently doesn't load."

Using `$HOME` in a `"command"` field causes silent non-load. Use `~` expansion or `$CLAUDE_PROJECT_DIR` instead. Absolute paths are the safest option.

**Shell profile pollution corrupts stdin JSON (T1, hooks-guide):**
When Claude Code runs a hook, it spawns a shell that sources `~/.zshrc` or `~/.bashrc`. Unconditional `echo` statements in shell profiles get prepended to hook JSON output, causing JSON parse failures. The fix:

```bash
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

The `$-` variable contains `i` in interactive shells only. Hooks run non-interactively, so the echo is skipped.

**Dependency availability must be declared explicitly (T3, DEV; T1, hooks-guide):**
`jq` is not guaranteed to be available. Claude Code runs hooks with a restricted PATH that may not include Homebrew-installed binaries (`/opt/homebrew/bin`). From the official guide:
> "If you see 'jq: command not found', install jq or use Python/Node.js for JSON parsing"

Failure mode when `jq` is missing depends on the script: it may exit 0 (fail open, allow everything) or exit 1 (non-blocking error, also allows everything). Neither blocks. The T3 source recommends explicit dependency checking:

```bash
if ! command -v jq &>/dev/null; then
  echo "WARN: jq not installed, hook disabled" >&2
  exit 0  # decide: fail open or fail closed (exit 2)
fi
```

**The `if` field provides argument-level filtering (T1, hooks-guide, v2.1.85+):**
The `matcher` field filters hook groups by tool name. The `if` field (added in v2.1.85) filters individual handlers by tool name AND arguments using permission rule syntax:

```json
{ "if": "Bash(git *)", "command": "check-git-policy.sh" }
```

This prevents the hook process from spawning at all for non-matching calls, reducing latency. `if` only works on tool events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest, PermissionDenied). Adding it to non-tool events prevents the hook from running.

**Non-deterministic updatedInput when multiple hooks modify the same tool (T1, hooks-guide):**
> "When multiple PreToolUse hooks return `updatedInput` to rewrite a tool's arguments, the last one to finish wins. Since hooks run in parallel, the order is non-deterministic."

More than one hook modifying the same tool's input produces unpredictable behavior. This is a structural anti-pattern with no workaround other than consolidating modifications into one hook.

**Performance threshold (T3, blakecrosley):**
> "Individual hooks should complete under 200ms"
> "PostToolUse hooks adding 500ms+ create noticeable session sluggishness"
> "Ten fast hooks outperform two slow ones"

The author reports running 95 hooks with acceptable performance because each is scoped narrowly and completes under 200ms. Synchronous hooks block Claude while they run — there is no timeout that prevents perceived latency.

---

### Sub-question 2: Behavioral anti-patterns causing silent failure or unsafe outcomes

**Exit code 1 misuse — the most common enforcement failure (T3, Medium; T3, DEV; T1, hooks-guide):**

The Medium source documents this as the central silent failure mode. The author wrote a path traversal validator using `sys.exit(1)` and it "completely failed to block anything." The mechanism:

> "Exit code 1 is an error. In Claude Code hooks, it's non-blocking."

> "When a PreToolUse hook returns exit code 1, Claude Code shows ⎿ PreToolUse:Bash hook error and then the command runs."

This creates false confidence: the error log shows the hook fired, but execution continued. The DEV source captures the same pattern:

> "Your 'security gate' is a suggestion, not a gate."

The inverted convention is the root cause: Unix convention treats non-zero as failure; Claude Code treats exit 1 as "warning, continue" and only exit 2 as "block."

**Python uncaught exceptions default to exit 1 (T3, Medium):**
Any unhandled exception in a Python hook script defaults to exit code 1 — not exit 2. This means an exception in a security validator causes a silent pass-through: the validator appears to have "failed" (exit 1 shown in transcript) but does not block. The fix: wrap all validator logic in try/except with explicit `sys.exit(2)` in the exception handler.

Detection method:
```bash
grep -n "sys.exit" ~/.claude/validators/*.py
# Every result should be sys.exit(0) or sys.exit(2) only
```

**jq returns null silently on wrong paths (T3, blakecrosley):**
> "Watch for jq failures — if your JSON path is wrong, jq returns null silently and your conditionals won't match."

A hook that reads `jq -r '.tool_input.command'` on a Write event (where the field is `.tool_input.file_path`) gets `null`. If the hook logic depends on this value to decide whether to block, `null` causes the condition to not match — the hook passes everything through silently.

**Async hooks cannot block, but the combination looks plausible (T1, hooks-reference from existing research):**
Setting `"async": true` runs the hook in the background after the event proceeds. An async hook with exit 2 logic or `decision: "block"` in its JSON output has no effect — the action has already executed. This is a structural misconfiguration that does not produce any warning; the hook simply runs late and its output is discarded.

**Stop/SubagentStop hooks without loop guards create infinite loops (T1, hooks-guide):**
A Stop hook that exits 2 to block without checking `stop_hook_active` forces Claude to keep responding indefinitely. The official troubleshooting section documents this:

```bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
```

Without this guard, each Stop hook execution triggers another Stop event, trapping the session.

**Tool name case sensitivity causes silent matcher failure (T3, DEV; T3, blakecrosley):**
Matchers are case-sensitive. `bash` ≠ `Bash`. A miscased matcher matches nothing and the hook never fires. There is no warning — the hook is configured, appears valid in `/hooks`, and silently does nothing.

**Hooks too slow accumulate unnoticed latency (T3, DEV):**
Running expensive checks on every tool use creates 2–3 second delays per execution. The article documents: "Synchronous execution overhead accumulates unnoticed during refactoring (50 edits = 2.5+ minutes lost)." The symptom is gradual session slowness, not a hook error.

**PermissionRequest hooks do not fire in non-interactive mode (T1, hooks-guide):**
> "PermissionRequest hooks do not fire in non-interactive mode (-p). Use PreToolUse hooks for automated permission decisions."

A PermissionRequest hook designed to enforce policy in CI/automated pipelines silently does nothing when run with `claude -p`.

**Hooks can tighten but not loosen permission restrictions (T1, hooks-guide):**
> "A hook returning 'allow' does not bypass deny rules from settings."

A PreToolUse hook returning `permissionDecision: "allow"` does not override deny rules in any settings scope, including managed policy settings. This is a documented limitation that affects hooks intended to auto-approve operations that enterprise policy denies.

---

### Sub-question 3: Testing and debugging strategies

**Manual stdin pipe test is the foundational pattern (T1, hooks-guide; T3, blakecrosley; T3, steve kinney):**
The official guide documents:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
echo $?  # Check the exit code
```

All three sources converge on this as the first validation step. The blakecrosley source adds: "Hooks fail silently more often than expected; test scripts independently first." Steve Kinney: "Test by piping sample JSON to stdin and check exit code."

**`/hooks` menu for configuration verification (T1, hooks-guide; T3, DEV; T3, steve kinney):**
The `/hooks` menu shows all configured hooks grouped by event, with counts. Selecting a hook shows: event, matcher, type, source file, and command. This is the canonical way to confirm a hook is loaded before testing behavior.

The DEV source recommends verifying with `/hooks` after any configuration change: "Paths are absolute (no $HOME). Verify with /hooks command in Claude Code."

**`claude --debug-file` for execution trace (T1, hooks-guide):**
```bash
claude --debug-file /tmp/claude.log
tail -f /tmp/claude.log  # in another terminal
```

The debug log contains: which hooks matched, exit codes, stdout, and stderr for every hook that fired. The transcript view (`Ctrl+O`) shows a one-line summary per hook: success is silent, blocking errors show stderr, non-blocking errors show `<hook name> hook error` followed by the first line of stderr.

`/debug` mid-session enables logging when the session was started without `--debug-file`.

**Verify jq paths against real payload (T3, blakecrosley):**
> "Verify your jq expressions against real tool input."

The real payload can be captured by running a hook that writes stdin to a file:
```bash
cat > /tmp/last-hook-input.json
```
Then inspect the actual field names before writing extraction logic.

**`time` command for performance validation (T3, blakecrosley):**
```bash
time echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
```
Measure execution time before deploying. The target is under 200ms for synchronous hooks.

**Use stderr for diagnostics during development (T3, steve kinney; T1, hooks-guide):**
> "Anything your hook writes to stderr appears in Claude's context."

During development, stderr is the correct channel for diagnostic output. The hooks-guide documents that stderr from blocking hooks is "fed back to Claude as feedback." Stdout is reserved for JSON structured output (exit 0 only).

**Scan for exit code misuse in Python validators (T3, Medium):**
```bash
grep -n "sys.exit" ~/.claude/validators/*.py
```
Every result should be `sys.exit(0)` or `sys.exit(2)` only. Any `sys.exit(1)` is a non-blocking "error" that silently allows execution.

---

### Sub-question 4: Audit rubric and graduated enforcement

**The official troubleshooting checklist (T1, hooks-guide):**

The hooks-guide documents four troubleshooting scenarios as an implicit audit structure:

1. **Hook not firing:** check `/hooks` list, case-sensitive matcher, correct event type, PermissionRequest in `-p` mode
2. **Hook error in output:** test with `echo '...' | ./script.sh; echo $?`, check absolute paths, check `jq` availability, check `chmod +x`
3. **`/hooks` shows no hooks:** verify valid JSON (no trailing commas), correct file location, restart session if file watcher missed
4. **Stop hook runs forever:** check `stop_hook_active` guard

**The practitioner quick-audit checklist (T3, DEV):**

```
[ ] Security hooks use exit 2, not exit 1
[ ] Paths are absolute (no $HOME)
[ ] Dependencies checked (command -v jq)
[ ] Heavy hooks limited via matchers
[ ] Context window monitored
```

**Graduated enforcement approach (T3, paddo.dev):**
The paddo.dev source recommends a staged deployment pattern:
1. Deploy single low-friction warning rule first (exit 1, observe without blocking)
2. Monitor triggers for one week, tune for false positives
3. Escalate to blocking (exit 2) only after pattern is validated
4. Add one rule per week maximum

The rationale: one false positive per session is enough to cause `--no-verify` culture. Starting permissive and tightening progressively maintains trust.

**The `if` field enables scope-narrowing without matcher changes (T1, hooks-guide, v2.1.85+):**
A key audit dimension is whether hooks are over-broad. The `if` field provides a second scoping layer:

```json
{
  "matcher": "Bash",
  "hooks": [
    { "if": "Bash(git *)", "command": "check-git-policy.sh" }
  ]
}
```

Without `if`, the hook spawns for every Bash call. With `if`, it only spawns for `git` commands. Audit finding: hooks that use broad matchers (`"*"` or `"Bash"`) without `if` for scoped enforcement are candidates for refinement.

**Non-deterministic conflict for updatedInput (T1, hooks-guide):**
An audit-specific finding: more than one PreToolUse hook returning `updatedInput` for the same tool produces non-deterministic behavior. This is a structural anti-pattern with no runtime warning — it surfaces only as unpredictable tool input modifications.

**Security audit dimension: settings.json as attack surface (T2, Check Point Research):**
CVE-2025-59536 demonstrated that `.claude/settings.json` can be used to inject arbitrary hook commands. Audit implication: hook changes in project-level `settings.json` must be treated with the same code-review scrutiny as executable source files. The correct scope question: should this hook be in project `settings.json` (shareable, higher risk) or `settings.local.json` (gitignored, personal only)?

## Challenge

### Assumptions Check

**Assumption:** exit code 1 is universally non-blocking.

**Challenge:** The hooks-guide documents that exit codes other than 0 and 2 are "non-blocking errors" — this covers exit 1. However, the hook-output reference also documents `"decision": "block"` as a separate JSON mechanism that works independently of exit code (only requires exit 0 for JSON parsing). It is possible to signal a block via JSON on exit 0 for events that support it (PostToolUse, Stop, UserPromptSubmit) without using exit 2. Practitioners conflating "exit 2 is the only way to block" may miss the JSON decision mechanism.

**Resolution:** Exit 2 is the correct blocking mechanism for PreToolUse and the events that can block via exit code. JSON `decision: block` is the correct mechanism for PostToolUse and Stop (which cannot block via exit code alone per the event table). These are complementary, not competing.

### Premortem

**Scenario:** A hook passes the structural checklist but silently degrades over time.

Most checklist items are point-in-time checks. The following failure modes are not caught by standard structural audit:
- A jq path that was valid when written becomes invalid after an upstream schema change (a tool payload field is renamed)
- A hook that was under 200ms with a small codebase slows above threshold as the project grows
- A dependency installed at hook-authoring time is removed from PATH (Homebrew uninstall, CI environment change)
- Shell profile changes by another process or user reintroduce profile pollution after the hook was validated

**Implication:** Effective hook quality requires periodic re-validation, not just authoring-time checks. A periodic audit cadence (monthly, or on tool version upgrades) is warranted.

## Findings

### SQ1: Structural requirements for correct hook operation

**Every hook script must consume stdin, be executable, and avoid `$HOME` in config paths (HIGH — T1 + T3 converge on all three).**

The three requirements that account for the majority of "hook not firing" issues are: (1) `INPUT=$(cat)` at the top of every command hook, (2) `chmod +x` on the script file, (3) absolute paths in the `"command"` field (not `$HOME`). All three are silent failures — no error distinguishes them from each other or from a correctly firing hook.

Shell profile pollution is a fourth structural requirement: any unconditional `echo` in `~/.zshrc` or `~/.bashrc` corrupts JSON output. The fix is guarding with `if [[ $- == *i* ]]; then`.

**Dependency availability must be declared, not assumed (HIGH — T1 + T3).**

`jq` is not in Claude Code's restricted PATH on all systems. A hook depending on `jq` without checking availability will fail silently in some environments. The declared failure mode matters: fail open (exit 0) passes everything through; fail closed (exit 2) blocks everything. Neither is correct by default — the hook author must decide and make the choice explicit.

**The `if` field provides argument-level scoping unavailable via matchers (MODERATE — T1 only, v2.1.85+).**

The `if` field prevents the hook process from spawning at all when the argument pattern doesn't match, reducing per-call latency. This is strictly superior to spawning the process and checking arguments inside the script. Adoption is gated on v2.1.85+.

---

### SQ2: Behavioral anti-patterns causing silent failure or unsafe outcomes

**Exit code 1 as enforcement is the most prevalent silent failure (HIGH — T3 converge, corroborated by T1 semantics).**

The Medium source documents a complete security gate bypass via exit 1 misuse. The DEV source documents it as mistake #1. The Steve Kinney source independently identifies it. The root cause is inverted convention: Unix treats any non-zero as failure; Claude Code reserves exit 2 for blocking and treats exit 1 as "log and continue." The false-confidence mechanism — the transcript shows a hook error while execution proceeds — is particularly dangerous for security hooks.

Python hooks face the additional risk that uncaught exceptions produce exit 1 by default, causing pass-through for any validator that throws.

**Async hooks with blocking intent are a misconfiguration that produces no warning (HIGH — T1).**

`async: true` runs the hook after the event proceeds; exit 2 and `decision: block` are both ignored. No warning is produced. This is likely to occur when hooks are copied from synchronous configurations and `async: true` is added for performance reasons without understanding the blocking model.

**jq null returns from wrong field paths bypass conditional logic silently (HIGH — T3; mechanism corroborated by T1 payload schemas).**

jq returns null rather than erroring when a field path is absent. A blocking condition that depends on a null check will pass null through the conditional rather than blocking. This is particularly common when hook scripts are adapted across tool types without updating the field path (e.g., reusing a Bash hook for Write hooks where `tool_input.command` becomes `tool_input.file_path`).

**PermissionRequest hooks silently do nothing in non-interactive mode (MODERATE — T1 only).**

Documented in the official hooks-guide limitations section. Affects CI/automation use cases where hooks are intended to enforce policy.

---

### SQ3: Testing and debugging strategies

**Manual stdin pipe testing is universal and sufficient for structural validation (HIGH — T1 + T3 all recommend).**

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh; echo $?
```

Every practitioner source converges on this. It validates: script executability, stdin consumption, jq path correctness, exit code behavior, stderr output. It does not validate matcher configuration or event-type selection — those require `/hooks` verification.

**A three-layer debugging stack covers the full failure space (HIGH — T1; MODERATE — T3).**

Layer 1: `/hooks` menu — confirms the hook is loaded and associated with the correct event and matcher.
Layer 2: `echo '...' | ./script.sh; echo $?` — confirms script logic and exit code behavior.
Layer 3: `claude --debug-file /tmp/claude.log` + `tail -f` — confirms end-to-end execution including which hooks matched, exit codes, stdout, and full stderr.

The `Ctrl+O` transcript view shows one-line summaries (success silent, blocking shows stderr, non-blocking shows `<name> hook error` + first stderr line). The debug log shows the complete execution record.

**Performance testing with `time` prevents slow-hook accumulation (MODERATE — T3 only).**

The 200ms-per-hook threshold from blakecrosley is not in official docs, but the convergence with the T1 performance note ("keep synchronous hooks under 1 second") supports it as a practical baseline. Using `time echo '...' | ./script.sh` during authoring is the only proactive way to catch latency issues before they accumulate in sessions.

---

### SQ4: Hook audit rubric

**A complete hook audit has three tiers: structural, behavioral, and deployment-scope (HIGH — T1 + T3 synthesis).**

Tier 1 (structural, detectable by inspection):
1. Every command hook has `INPUT=$(cat)` — stdin consumption
2. Script file has `chmod +x` — executability
3. No `$HOME` in `"command"` field — path expansion
4. Tool names in matchers are correctly cased — case sensitivity
5. No `async: true` paired with blocking intent — async contradiction
6. Stop/SubagentStop hooks have `stop_hook_active` guard — loop prevention
7. No destructive operations (`rm -rf`, `git reset --hard`, force-push) — safety
8. Idempotent: no unbounded log appending, counters, file accumulation

Tier 2 (behavioral, requires logic inspection):
9. All exit-2 paths are intentional blocking; exit-1 paths are intentional warnings
10. Python validators wrap logic in try/except with explicit `sys.exit(2)` in exception handler
11. jq field paths match the target tool's `tool_input` schema (not cross-adapted from another tool type)
12. Enforcement intent matches event capability (PreToolUse for blocking; PostToolUse only for feedback)
13. Dependency availability checked with `command -v` before use
14. Shell profile guarded with `if [[ $- == *i* ]]; then` if hooks spawn subshells

Tier 3 (deployment scope):
15. Security hooks in `settings.json` are reviewed as executable code, not config
16. Project-level hooks use `.claude/settings.local.json` for personal-only rules
17. Broad matchers (`"*"`, `"Bash"`) are justified or refined with `if` field
18. Enforcement is graduated: warnings before blocks, patterns validated before enforcement

**Graduated enforcement reduces bypass culture (HIGH — T3; consistent with T1 latency guidance).**

The paddo.dev one-rule-per-week approach is practitioner-derived. The T1 hooks-guide validates the principle via its latency note: "Keep synchronous hooks under 1 second" implies that slow hooks drive `--no-verify` bypass. Starting permissive and tightening progressively applies the same principle to enforcement strictness.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Exit code 1 is non-blocking in all Claude Code hook events | behavior | [1] hooks reference | verified — reference documents exit code semantics explicitly |
| 2 | jq returns null (not error) on missing paths | behavior | [5] blakecrosley | verified — consistent with jq documentation |
| 3 | Python uncaught exceptions produce exit 1 by default | behavior | [3] medium | verified — Python sys.exit() documentation |
| 4 | `$HOME` is not expanded in JSON command fields | behavior | [4] DEV | verified — corroborated by hooks-guide absolute path guidance |
| 5 | Shell profile sourcing corrupts hook JSON output | behavior | [2] hooks-guide | verified — documented in official troubleshooting |
| 6 | `async: true` hooks cannot block regardless of exit code | behavior | [1] hooks reference | verified — explicitly stated in reference |
| 7 | PermissionRequest hooks do not fire in `-p` mode | behavior | [2] hooks-guide | verified — documented in official limitations |
| 8 | Multiple updatedInput returns are non-deterministic | behavior | [2] hooks-guide | verified — explicitly documented |
| 9 | The `if` field requires v2.1.85+ | behavior | [2] hooks-guide | verified — stated in official guide |
| 10 | The 200ms-per-hook threshold is sufficient for acceptable latency | threshold | [5] blakecrosley | human-review — T3 practitioner only; official docs say "under 1 second" |

## Search Protocol

<!-- search-protocol
{"entries": [
  {"query": "Claude Code hooks testing debugging strategies validate hook script 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 4},
  {"query": "Claude Code hooks audit checklist quality criteria evaluation 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Claude Code hooks anti-patterns silent failure misconfiguration exit code 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 5},
  {"query": "Claude Code hooks stdin JSON payload shell script best practices 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Claude Code hooks \"if field\" argument filtering \"Bash(git*)\" matcher advanced 2026", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1}
], "not_searched": [
  "github.com/anthropics/claude-code/issues (bug tracker) — skipped; search surface covered by hooks-guide troubleshooting",
  "deepwiki hook-failures page — fetched but content not available in rendered excerpt"
]}
-->
