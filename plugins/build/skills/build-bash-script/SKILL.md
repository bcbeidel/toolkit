---
name: build-bash-script
description: >
  Scaffolds a standalone Bash 4.0+ script — a single-file CLI tool,
  glue automation, or ops utility — with explicit shebang,
  `set -euo pipefail`, header comment, `readonly` constants, `die`
  helper, `local` variables, `main` function, and a sourceable guard.
  Use when the user wants to "create a bash script", "scaffold a
  bash script", "write a CLI script in bash", "new bash automation",
  "build a bash glue script", or "scaffold a shell script". Not for
  POSIX `sh` portability targets, Claude Code hooks, or scripts that
  would be cleaner in Python — route to the appropriate primitive.
argument-hint: "[purpose]"
user-invocable: true
references:
  - ../../_shared/references/bash-script-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build Bash Script

Scaffold a standalone Bash 4.0+ script: a single-file program built
from existing CLI tools that runs from a terminal or Makefile, returns
a useful exit code, and stays composable in pipelines. The authoring
rubric — anatomy template, patterns that work — lives in
[bash-script-best-practices.md](../../_shared/references/bash-script-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

This skill is **bash-only by scope**. POSIX `sh` portability targets
(`dash`, BusyBox, Alpine) are out of scope and refused at the Scope
Gate. It is also not for Claude Code hooks (`/build:build-hook`), not
for tasks better expressed in Python (`/build:build-python-script`),
and not for multi-file Bash applications (those want a real language).

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a standalone Bash script is the right primitive *and* that
Bash is the right language before asking scaffold-specific questions.

**Wrong primitive:**

- **Event-triggered quality enforcement** (PreToolUse, SessionStart,
  Stop, etc.) → `/build:build-hook`. Hooks have a `settings.json`
  registration, a `tool_input` payload contract, and lifecycle
  semantics a standalone script doesn't express.
- **A Claude Code skill definition** → `/build:build-skill`.
- **A semantic judgment captured as an LLM-evaluated rule** →
  `/build:build-rule`.

**Wrong language — should be Python instead:**

- Task manipulates structured data — arrays of typed records, nested
  JSON beyond a `jq` one-liner, schema-validated payloads
- Projected logic exceeds ~300 LOC of business code
- Task needs testable seams beyond `bats`/`shunit2` glue
- Task needs concurrency, HTTP with retry / JSON, or cross-platform
  correctness (Windows)

The full language-selection decision lives in the *Language Selection*
section of
[primitive-routing.md](../../_shared/references/primitive-routing.md) —
consult it when the choice is not obvious. **Tiebreaker rule from that
doc:** when the decision is genuinely balanced, Python wins on
interpretability.

**Right primitive and right language** (CLI glue stitching `git` /
`curl` / `jq` / `find` / `xargs`; Makefile-invoked automation; one-shot
ops utility; <300 LOC of bash logic) → proceed to Scope Gate.

## 2. Scope Gate

Refuse to scaffold — and recommend an alternative — when the request
signals bash-script is the wrong tool. Probe for any of:

1. **POSIX `sh` portability needed** — `dash`, BusyBox, Alpine, or
   any environment where Bash is unavailable. Bash 4.0+ is this
   skill's scope; portable `sh` is out of scope. Recommend the user
   either install Bash in the target environment or rewrite the
   logic in a portable language. **Do not scaffold a "portable-ish
   bash" script** — silent bashisms under `#!/bin/sh` fail on those
   targets.
2. **Setuid script intent** — setuid + shell is a security minefield
   (`PATH` poisoning, `IFS` injection, signal handling). This skill
   does not scaffold setuid scripts; recommend a compiled wrapper
   (`sudo`, a tiny C/Go binary) that delegates to the unprivileged
   bash script.
3. **Multiple entry points or long-running service** — a daemon, a
   web hook listener, anything with more than one callable surface
   is not a script. Recommend a real language and a proper service
   pattern.
4. **Projected >300 lines of business logic** — Bash's lack of data
   structures and error handling does not scale. Recommend Python
   via `/build:build-python-script`.
5. **Cross-platform Windows requirement** — Bash on Windows needs
   WSL or Git Bash, both of which introduce path-translation
   surprises. Recommend a cross-platform language.

If any signal fires, state the signal, name the recommended
alternative, and stop. Do not proceed to Elicit.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse it as `[purpose]` and pre-fill the
purpose field. Otherwise ask, one question at a time:

**1. Purpose** — one sentence: what does this script do? Preferably
verb-phrased ("rotate the logs in /var/log/app and gzip the
oldest 30 days").

**2. Invocation style** — pick one:
- `cli` — accepts flags and positional args; has `--help` output.
  Default for anything a human invokes directly.
- `glue` — fixed positional args, called from a Makefile or another
  script. Minimal argument-parsing surface.
- `library` — sourceable for testing (`. ./script.sh`) but also
  runnable directly via the sourceable guard. The default scaffold
  already supports this; pick when the user will write `bats` /
  `shunit2` against internal functions.

**3. Input shape** — where does the script read from?
- `args` — positional arguments and/or flags via `getopts` or hand
  parsing.
- `stdin` — reads from stdin, supports `-` as stdin sentinel.
- `none` — no input beyond flags or env vars.

**4. Output destination** — where does primary output go?
- `stdout` — default; data to stdout, logs to stderr. Composable in
  pipelines.
- `file` — writes to a path provided as a flag.
- `none` — the script is called for its side effects (filesystem
  changes, network calls).

**5. Destructive operations?** — does the script delete, overwrite,
move files, or make irreversible network calls? If yes, the scaffold
adds a `--dry-run` flag (default off but visible) and a `--yes`
confirmation flag, plus the `if [[ "${dry_run}" ]]; then ...` branch
in `main`. If no, those are omitted.

**6. External CLI dependencies** — which tools does the script call
beyond Bash builtins? (e.g., `jq`, `curl`, `git`, `rsync`, `find`,
`xargs`.) These populate the `command -v` preflight.

**7. Save path** — where should the script land? No default; common
homes: `scripts/`, `bin/`, `.claude/scripts/`,
`plugins/<name>/scripts/`, `.github/scripts/`. Ask explicitly.

## 4. Draft

Produce two artifacts.

**Artifact 1: The script.**

One conditionalized template. Sections marked *(if destructive)* or
*(if has-deps)* are omitted when the intake rules them out.

```bash
#!/usr/bin/env bash
#
# <progname> — <one-line purpose>
#
# Usage:
#   <progname> [options] <args>
#
# Dependencies: <comma-separated list of external CLI tools>
#
# Exit codes:
#   0   success
#   1   general failure
#   64  usage error
#   69  missing required dependency

set -euo pipefail

readonly PROGNAME="$(basename "${0}")"
readonly DEFAULT_TIMEOUT=30                                   # named constant

REQUIRED_CMDS=(jq curl)                                       # (if has-deps) populated from intake

usage() {
  cat <<'EOF'
<progname> — <purpose>

Usage:
  <progname> [options] <args>

Options:
  --dry-run    Print planned actions; take none.              # (if destructive)
  --yes        Skip confirmation for destructive ops.         # (if destructive)
  -h, --help   Show this help and exit.
EOF
}

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

preflight() {                                                 # (if has-deps)
  local missing=()
  local cmd
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      missing+=("${cmd}")
    fi
  done
  if [[ "${#missing[@]}" -gt 0 ]]; then
    die "missing required commands: ${missing[*]}"
  fi
}

main() {
  case "${1:-}" in
    -h|--help) usage; exit 0 ;;
  esac

  preflight                                                   # (if has-deps)

  local input="${1:?input required}"
  # validate inputs before destructive work
  [[ -e "${input}" ]] || die "not found: ${input}"

  # <body — split into small functions as the script grows>
}

# Sourceable guard: run main only when executed, not when sourced.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

*(if not destructive)* Omit the `--dry-run` and `--yes` lines from
`usage()` and skip the `if [[ "${dry_run}" ]]; then ...` branch. The
rest stays.

*(if no external deps)* Omit `REQUIRED_CMDS`, `preflight()`, and the
`preflight` call. Drop the `Dependencies:` header line.

*(library invocation style)* No scaffold changes — the default
structure (`main` orchestrator, sourceable guard) already supports
`. ./script.sh` for testing.

**Artifact 2: A suggested invocation line** — how the user or a
Makefile would call the script, ready to paste. Include `chmod +x` so
the shebang + executable-bit contract holds.

Present both artifacts to the user before any safety checks.

## 5. Safety Check

Review the draft against the rubric in
[bash-script-best-practices.md](../../_shared/references/bash-script-best-practices.md)
before presenting. Group the checks:

**Structure.** Shebang is `#!/usr/bin/env bash` (or `#!/bin/bash`
when explicitly justified). `set -euo pipefail` is in the prologue. A
header comment names purpose, usage, dependencies, and exit codes.
Top-level configuration is `readonly`. A `main` function exists. The
sourceable guard `[[ "${BASH_SOURCE[0]}" == "${0}" ]]` invokes `main`.

**Quoting & idioms.** Every variable expansion is quoted (`"$var"`,
`"$(cmd)"`, `"${arr[@]}"`). `"$@"` forwards arguments. Conditionals
use `[[ ... ]]`, not `[ ... ]`. Command substitution uses `$()`, not
backticks. `printf` is used for non-trivial output, not `echo`.

**Safety.** No `eval`. No hardcoded `/tmp/` paths (use `mktemp` and
pair with `trap`). No `rm -rf $var` unquoted or unvalidated. No
GNU-specific flags without a declared dependency. `cd` invocations
check the exit status. `--` precedes untrusted arguments to
option-parsing commands.

**Function discipline.** Function-scoped variables use `local`. The
`die`/`error` helper writes to stderr and exits non-zero — no bare
`exit 1` with no message.

**Tooling readiness.** The output is structured to pass `shellcheck`
(quoted variables, `$()` over backticks, `[[ ]]` over `[ ]`) and
`shfmt -i 2 -ci -bn` (2-space indent, switch-case indent, binop on
next line).

If any check fails, revise the draft before presenting. The Review
Gate is for user approval, not correctness recovery.

## 6. Review Gate

Present both artifacts (script + invocation line) and wait for
explicit user approval before writing any file to disk. Write only
after this gate passes.

If the user requests changes, revise and re-present. Continue until
the user explicitly approves or cancels. Proceed to Save only on
explicit approval.

## 7. Save

Write the approved script to the path elicited in Step 3.7. Mark it
executable:

```bash
chmod +x <path>
```

A shebang without `+x` is a lie — the executable bit is part of the
contract the principles doc names. Show the suggested invocation line
for the user to wire into a Makefile, CI config, or README.

## 8. Test

Offer the audit:

> "Run `/build:check-bash-script <path>` to audit the scaffolded
> script against ShellCheck, shfmt, and the deterministic + judgment
> dimensions?"

The audit is the canonical follow-on; running it once after scaffold
catches anything the Safety Check missed and gives the user a
baseline-clean starting point.

## Anti-Pattern Guards

1. **Skipping the Scope Gate** — always probe the five signals before
   Elicit. Scaffolding bash for a workflow that wants Python or POSIX
   `sh` pushes the wrong primitive into the codebase.
2. **Scaffolding under `#!/bin/sh`** — this skill is bash-only. Bash
   features under a `sh` shebang fail silently on `dash`/BusyBox.
   Refuse via Scope Gate signal #1; do not produce a "mostly portable"
   hybrid.
3. **Setuid scaffolding** — security minefield. Refuse via Scope Gate
   signal #2; recommend a compiled wrapper instead.
4. **Hand-waving `--dry-run`** — if Intake step 3.5 flagged
   destructive operations, the draft must wire the dry-run flag into
   the destructive code path, not just declare the flag and ignore
   it. Show the `if [[ "${dry_run}" ]]; then ...` branch in `main`.
5. **Empty `REQUIRED_CMDS`** — when external deps are intaken, the
   array is populated. Empty array silently skips preflight, killing
   the fail-fast contract.
6. **Skipping the Review Gate** — write to disk only after explicit
   user approval. Present both artifacts first.

## Key Instructions

- Refuse cleanly on Scope Gate signals. POSIX-sh and setuid intents
  are hard refuses, not "scaffold and warn" cases.
- Write files to disk only after the Review Gate passes.
- Elicit the save path from the user explicitly — paths are project-specific and inventing one wastes a Review Gate cycle.
- The `--dry-run` flag is only scaffolded when Intake step 3.5
  flagged destructive operations. Do not add it unconditionally — it
  clutters read-only scripts.
- The `command -v` preflight is only scaffolded when Intake step 3.6
  named external dependencies. Do not add an empty preflight as
  "best-effort" structure — it is dead code.
- Won't scaffold scripts for Claude Code hook events — route to
  `/build:build-hook`.
- Won't scaffold POSIX `sh` scripts — out of scope; the synthesis
  this skill operationalizes is bash-only.
- Won't scaffold setuid scripts — recommend a compiled wrapper.
- Won't scaffold when any Scope Gate signal fires — recommend the
  appropriate alternative.
- Recovery if a script is written in error: `rm <path>` removes it
  cleanly. The scaffold is self-contained (no settings.json entry,
  no shared-module registration), so removal leaves no dangling state.

## Handoff

**Receives:** user intent for a Bash 4.0+ script (purpose, invocation
style, input shape, output destination, destructive-op flag, external
CLI dependencies, save path).
**Produces:** an executable Bash script at the user-supplied path
plus a suggested invocation line.
**Chainable to:** `/build:check-bash-script` (audit the scaffolded
script against ShellCheck, shfmt, and the judgment dimensions).
