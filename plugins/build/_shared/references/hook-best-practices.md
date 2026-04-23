---
name: Hooks Best Practices
description: Authoring guide for Claude Code hooks — what makes a hook load-bearing on the agent's critical path, how to shape registration and script together, the positive patterns that work, and the safety and maintenance posture. Referenced by build-hook and check-hook.
---

# Hooks Best Practices

## What a Good Hook Does

A Claude Code hook is a short, single-purpose script the agent invokes at a defined event — `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `Notification`, `SubagentStop`, or `PreCompact` — to apply deterministic policy on the critical path. Good hooks are fast, fail safely, stay auditable, and never surprise a reviewer: they read a JSON payload from stdin, make one decision, emit a structured log line, and return via a well-known exit code. The value proposition is narrow. A hook earns its place when the policy is mechanical (block `rm -rf /`, redact secrets, lint on save, record an audit trail) and would be error-prone to enforce via prompt instructions. If the work needs the model's judgment, it belongs in a skill or a subagent, not a hook.

## Anatomy

A hook ships as two artifacts. A **registration entry** in `.claude/settings.json` (team-shared) or `.claude/settings.local.json` (gitignored, personal), bound to a single event, scoped by a narrow `matcher`, pointing at a **script path** — not an inline pipeline, not `bash -c`. And the **script** itself under `.claude/hooks/`, named by event and purpose (`pre-tool-use--block-destructive-rm.sh`), with a shebang, the executable bit, and a header comment stating **Event**, **Matcher**, **Effect**, **Failure-mode** (`fail-closed` for safety-critical / `fail-open` for advisory), and **Bypass** (how to disable in an incident).

Beneath the header, bash hooks set strict mode immediately (`set -euo pipefail`); Python hooks declare `main()` and a locked import block. The body reads stdin as strict JSON, validates fields, makes one decision, writes a reason to stderr on block, emits one structured JSON log line to stderr on exit, and returns via `0` (allow), `2` (block with feedback), or another non-zero code for hook-internal bugs. A test fixture under `tests/` or `.claude/hooks/tests/` pipes a representative payload and asserts the contract.

## Authoring Principles

**Register on a known event with a narrow matcher.** Hooks bind to a fixed enum of events. A typo in the event key means the hook never fires and the gate silently fails open; validating `settings.json` against the known set catches this at review time. Scope each registration with a matcher that names the specific tool or pattern the hook applies to — not `*`, not `.*`, not empty. Broad matchers add latency to every tool call and output the agent must parse past.

**Put logic in versioned scripts, not inline commands.** `settings.json` is configuration; shell pipelines inside a `command` field are code hiding from review. A one-line `command: ".claude/hooks/pre-tool-use--block-rm.sh"` lets the script receive code review, linting, and testing. Inline pipelines skip all three and rot unnoticed.

**Keep each hook single-purpose and bounded in size.** One script, one decision. Composition across multiple hooks is cheaper than branching inside one — multi-purpose hooks grow state, develop subtle interactions, and become impossible to disable partially. A hook that grows past the file limit is a refactor signal, not a workaround signal.

**Give every script a shebang and the executable bit.** `#!/usr/bin/env bash`, `#!/usr/bin/env python3`. The shebang is the dialect contract; the executable bit is the "run directly" contract. Leaving either out forces the harness to guess, which goes wrong differently on different machines.

**Prefer Python past the trivial-glue boundary.** Bash is fine for small wrapper hooks that grep a field and exit. Past roughly twenty lines, or whenever structured-data parsing enters the picture (JSON, SQL, shell command tokenization), switch to Python. Bash branching and quoting get expensive fast, and shell regex on serialized data is a security bug waiting to happen.

**Keep the protocol tight: JSON in, nothing-or-JSON out, reason on stderr.** Parse stdin as strict JSON (`jq` in bash, `json.load(sys.stdin)` in Python); reject on parse error. Leave stdout empty on allow; emit exactly one JSON object (`{"decision":"block","reason":"..."}`) only when structured feedback must reach the model verbatim. Send all human logs, debug traces, and error messages to stderr — Claude Code surfaces stderr on blocking exits. A stray `echo` on stdout corrupts the agent's view of the decision. Argv and env are not part of the contract; relying on them breaks silently on version updates.

**Decide via exit codes, not prose.** `0` allows, `2` blocks with feedback (reason on stderr), other non-zero codes signal a hook-internal bug. Mixing these — returning `1` for "block," echoing "allow" on stdout, writing the reason to stdout — produces ambiguity that either lets unsafe actions through or spams "hook failed" noise.

**Make failures loud, bounded, and posture-declared.** `set -euo pipefail` at the top of every bash hook turns silent failures into loud, early exits; Python hooks wrap external I/O in narrow try-blocks with no bare `except: pass`. Enforce a per-hook timeout on any external call. The header comment declares whether the hook is `fail-closed` (safety-critical — block on ambiguity or timeout) or `fail-open` (advisory — allow past). An explicit posture turns a judgment call into a reviewable artifact; silence is an unmanaged default.

**Never trust tool input; validate paths and pass argv-only to subprocesses.** Tool inputs are LLM-generated and may carry metacharacters from web content, prompt injections, or adversarial fuzzing. Canonicalize every path field through `realpath` / `os.path.realpath` before an allowlist prefix check — naive checks miss `../../../etc/passwd` and symlink escapes. Hardcode subprocess commands, allowlist flag values, and pass untrusted data only as positional arguments. `shell=True`, `bash -c "$payload"`, `eval "$tool_input"`, `os.system(...)` are equivalent foot-guns. Parse structured data with dedicated libraries (`jq`, `json.loads`), never regex.

**Forbid network I/O in `PreToolUse`; bound it elsewhere.** `PreToolUse` runs on every intercepted tool call; a single network round trip multiplies into minutes of latency per session. Blanket-ban outgoing network calls in `PreToolUse`. `PostToolUse` telemetry that must reach a network endpoint fires-and-forgets with a short timeout and fails open.

**Emit one structured log line per invocation with named constants and a fixed decision enum.** A single JSON line on stderr per execution containing `hook`, `event`, `decision`, `reason`, `duration_ms` — and a correlation ID where available — is enough to audit, alert, and debug. Use a fixed enum (`allow`, `block`, `escalate`, `observe`) in logs and reason codes; declare timeouts, path prefixes, and decision values as named constants at the top. Magic numbers and free-text decisions defeat metrics and make refactoring risky. Redact secrets using a fixed pattern (`(?i)(token|secret|password|key|bearer)`); never log `os.environ`, `$(env)`, or raw stdin that may contain credentials.

**Write a stateless, import-safe script with one entry point.** A `main()` function called from an `if __name__ == "__main__":` guard (Python) or a sourceable `main` function under `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"` (bash) makes hooks testable by sourcing. Module-scope I/O, HTTP calls, or mutable globals run on import and contaminate the test environment. The same payload must produce the same decision regardless of clock, RNG, or prior invocations — non-deterministic hooks make incidents un-debuggable.

**Test every hook with a representative payload.** One test per hook: pipe a realistic JSON payload to stdin and assert the exit code and any stdout contract. Fixtures live beside the hook. Hooks without tests decay quietly — the first sign a gate has drifted is an incident.

**Pin interpreters and dependencies; keep scripts in source control.** Reference interpreters as `/usr/bin/env bash` / `/usr/bin/env python3`. Lock Python dependencies in a project-level lockfile or pinned requirements file. Do not download or generate hook scripts at runtime — provenance and reviewability require the script to live in the repository.

**Commit shared policy; gitignore personal workflow.** `.claude/settings.json` is the team-reviewed gate set. `.claude/settings.local.json` is personal, belongs in `.gitignore`, and carries no expectation of team review. Conflating the two either imposes one engineer's workflow on the team or buries shared gates inside un-reviewed config.

## Patterns That Work

- **Scripts over inline pipelines.** A reviewable file path in `settings.json` beats any amount of cleverness in a `command` field.
- **Exit codes over prose decisions.** Two or three integers beat a free-form string for reliability and metrics.
- **Argv arrays over shell interpolation.** Passing untrusted input as positional arguments to a fixed command is safe; interpolating into a shell string is not.
- **Narrow matchers over `.*` or empty.** Registering the hook against the tool it actually cares about keeps the hot path fast.
- **`realpath` before prefix-check.** Canonicalization first, allowlist comparison second.
- **One structured log line over scattered prints.** One JSON line on stderr per invocation supports audit and metrics; scattered prints defeat both.
- **Declared failure-mode over implicit posture.** A header that names `fail-closed` or `fail-open` is a reviewable commitment; silence is an unmanaged default.
- **One decision per hook, composed via multiple hooks.** Composition is cheap; branching inside one hook is not.

## Safety

Some hook safety properties are checkable deterministically: a shellcheck-clean bash script, a bandit-clean Python script, the absence of `eval` / `shell=True` / `os.system` on tool-derived input, a `realpath`-guarded path check, a secret-redaction pattern on logged fields, a JSON parser (not regex) consuming stdin. These are Tier-1 territory — the audit script either finds the pattern or it does not.

Other properties require judgment: whether a hook actually blocks the failure mode it claims to; whether a timeout is well-chosen for the workload; whether a `fail-open` declaration is genuinely safe for the gate in question; whether the matcher scope matches the stated intent. These are Tier-2 dimensions — a rubric-driven review reads the hook and its header together. The author-time job is to make that review easy: name the failure mode in the header, keep the body short enough to hold in working memory, and include a test that encodes the intent.

## Review and Decay

Audit hooks on the same cadence as the code they gate — every change to a protected surface is an opportunity for drift. A hook retires when its rule is enforced elsewhere (a pre-commit equivalent lands upstream, a linter covers the case, the tool it gates is deprecated), when it fires often enough to be flagged as noise rather than policy, or when its failure mode no longer matches the threat model. Retirement is a deletion plus a log-trail commit message — silent disables become undocumented trust assumptions.

A well-built hook reads like a contract: one event, one matcher, one decision, one log line, a documented failure mode, a tested fixture. Anything more is either two hooks pretending to be one, or a skill.

---

*Distilled from the `claude-code-agentic-hooks` ensemble (2026-04-22, six-model panel across OpenAI, Anthropic, Google, xAI). Inclusion bar: ≥2 model families per `coverage-llm.md`, AND either the affordable-tier Anthropic model raised the rule or the check is mechanically deterministic. Three rules were judgment-promoted: stdout-protocol discipline, fail-mode declaration (deterministic via header field), and event-name registration (clustering discrepancy between coverage sources).*
