---
name: build-shell
description: >
  Scaffolds a general-purpose shell script with a strict-mode preamble,
  structured file header, dependency preflight, and conditional features
  scoped to a declared target shell (bash 3.2 / 4+ / 5+ / POSIX sh). Use
  when the user wants to "create a shell script", "scaffold a bash
  script", "write a CLI script", "new utility script", or "build a shell
  script". Not for Claude Code hooks — route to `/build:build-hook`.
argument-hint: "[target-shell] [purpose]"
user-invocable: true
references:
  - references/scope-gate.md
---

# Build Shell

Scaffold a general-purpose shell script: a deterministic automation unit
with a consistent structural shape (strict mode, structured header,
dependency preflight, `main` + self-sourcing guard) scoped to a declared
target shell.

This skill is not for Claude Code hooks — `/build:build-hook` owns that
lifecycle. Route there when the script has an event trigger and
`settings.json` wiring.

**Workflow sequence:** 1. Route → 2. FX.1 Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Determine whether a general-purpose shell script is the right primitive
before asking scaffold-specific questions.

- **Goal is event-triggered quality enforcement** (PreToolUse, SessionStart,
  Stop, etc.) → suggest `/build:build-hook` instead. Hooks have a
  `settings.json` registration, a `tool_input` payload contract, and
  lifecycle semantics this skill does not handle.
- **Goal is a Claude Code skill definition** (markdown with frontmatter,
  invoked by slash command) → suggest `/build:build-skill` instead.
- **Goal is a semantic judgment captured as an LLM-evaluated rule** →
  suggest `/build:build-rule` instead.
- **Goal is a general-purpose automation or CLI script** (glue, setup,
  CI step, utility called by humans or Makefiles) → proceed to Scope
  Gate.

## 2. FX.1 Scope Gate

Refuse to scaffold — and recommend an alternative — when the request
signals shell is the wrong tool. The full signal catalog with per-signal
recommendation copy lives in [scope-gate.md](references/scope-gate.md).
Probe for any of:

1. **Structured records** — arrays of typed objects, joins across
   multiple data sources, schema validation. Recommend Python with
   `pydantic`/`dataclasses`, or Go.
2. **JSON/YAML beyond a jq one-liner** — multi-step transformation,
   schema-aware reads. Recommend Python.
3. **Projected >100 LOC of business logic** — not counting headers,
   help, or boilerplate. Recommend Python for maintainability.
4. **Windows compatibility need** — PowerShell scripts are a different
   primitive; shell pipelines don't translate cleanly. Recommend the
   user pick a target platform (Unix-only bash or PowerShell) or use a
   cross-platform language.
5. **Concurrency / threading** — parallel task orchestration is
   fragile in bash (`wait -n` is bash 4+, race conditions are easy).
   Recommend Python `concurrent.futures` or Go.

If any signal fires, state the signal, quote the recommendation, and
stop. Do not proceed to Elicit. The skill's value is in refusing cleanly
as much as in scaffolding cleanly.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse as `[target-shell] [purpose]` and
pre-fill the first two fields. Otherwise ask, one question at a time:

**1. Target shell** — which shell + version should the script target?

| Target | When to pick |
|--------|--------------|
| `bash-3.2-portable` | Default for macOS compatibility (Apple ships bash 3.2). Safest. Strips `mapfile`, `wait -n`, `lastpipe`, `${var^^}`, associative arrays. |
| `bash-4+` | Linux default on most distros. Adds associative arrays, `mapfile`, `wait -n`. Breaks on macOS's `/bin/bash` without a Homebrew upgrade. |
| `bash-5+` | Adds `EPOCHSECONDS`, `BASH_ARGV0`, nameref loops. Only pick if a bash-5 feature is required. |
| `posix-sh` | Strict POSIX, runs under `dash`/`busybox sh`. Strips `[[ ]]`, `local`, arrays beyond `$@`, `${var//a/b}` globals. |

**2. Script purpose** — one sentence: what does this script do?

**3. Invocation style** — pick one:
- `cli` — accepts flags and positional args, has a usage/help output.
- `glue` — one-shot, no flags, called from a Makefile or another script.
- `library` — sourceable (`. ./script.sh`) to export functions; the
  self-sourcing guard lets the same file also run as a CLI.

**4. Setuid intent** — is this script installed with the setuid bit?
(Rare. Yes/No.) If yes, the shebang becomes `#!/bin/bash` instead of
`#!/usr/bin/env bash` — setuid + `env` is a PATH-hijack vector.

**5. Runtime dependencies** — which external commands does the script
call beyond shell builtins? (e.g., `jq`, `curl`, `git`, `rsync`.) These
populate the preflight array.

**6. Save path** — where should the script land? No default; common
homes: `scripts/`, `.claude/scripts/`, `plugins/<name>/scripts/`,
`.github/scripts/`. Ask explicitly.

## 4. Draft

Produce two artifacts.

**Artifact 1: The script.**

One conditionalized template. Sections below marked *(bash-only)* or
*(non-setuid)* are omitted when the target rules them out.

```bash
#!/usr/bin/env bash                             # non-setuid; else #!/bin/bash
#
# <progname> — <one-line purpose>
#
# Usage:
#   <progname> [options] <args>
#
# Exit codes:
#   0  success
#   64 usage error
#   69 missing dependency
#   70 internal error
#
# Dependencies:
#   <cmd1>, <cmd2>, ...

set -Eeuo pipefail                              # abort on error, unset var, pipeline failure
IFS=$'\n\t'                                     # safe field splitting for whitespace-heavy input

PROGNAME="$(basename "${0}")"
PROGDIR="$(cd "$(dirname "${0}")" && pwd)"

REQUIRED_CMDS=(jq curl)                         # populated from intake

usage() {
  cat <<'EOF'
<progname> — <purpose>

Usage:
  <progname> [options] <args>

Options:
  -h, --help   Show this help and exit.
EOF
}

preflight() {
  local missing=()
  for cmd in "${REQUIRED_CMDS[@]}"; do
    if ! command -v "${cmd}" >/dev/null 2>&1; then
      missing+=("${cmd}")
    fi
  done
  if (( ${#missing[@]} > 0 )); then
    for cmd in "${missing[@]}"; do
      printf '%s: missing required command %q. Install with: %s\n' \
        "${PROGNAME}" "${cmd}" "$(install_hint "${cmd}")" >&2
    done
    exit 69
  fi
}

install_hint() {
  # Platform-specific install hint for common tools.
  case "${1}" in
    jq)   printf 'brew install jq  |  apt install jq  |  dnf install jq' ;;
    curl) printf 'brew install curl  |  apt install curl  |  dnf install curl' ;;
    git)  printf 'brew install git  |  apt install git  |  dnf install git' ;;
    *)    printf 'see your package manager' ;;
  esac
}

main() {
  preflight
  # <script body>
}

# Self-sourcing guard: run main only when executed, not when sourced.
if [[ "${0}" == "${BASH_SOURCE[0]}" ]]; then
  main "$@"
fi
```

*(posix-sh target only)* Strip `[[ ]]` for `[ ]`, `local` for
subshell-scoped function variables, `(( ))` arithmetic for `$(( ))`,
the `BASH_SOURCE`-based guard for `"$0" = "$(basename "$0")"`-style
handling, and replace array syntax with whitespace-tokenized strings.
`set -Eeuo pipefail` becomes `set -eu` (pipefail is not POSIX).

*(setuid target only)* Use `#!/bin/bash` instead of `#!/usr/bin/env bash`.
`env` resolves `bash` from `PATH`, which a setuid caller can poison.

**Artifact 2: A suggested invocation line** — how the user or a Makefile
would call the script, ready to paste into a Makefile rule or README.

Present both artifacts to the user before any safety checks.

## 5. Safety Check

Review the draft against the 14 lints `/build:check-shell` enforces,
grouped:

**Portability.** Target-shell features match declaration. `mktemp`
usage has a portable fallback. POSIX-sh target uses no bash-only syntax.

**Safety.** All variable expansions quoted. No `for f in $(ls ...)`,
`cat file | cmd > file`, `while | read` without process-substitution,
unscoped `IFS=`, `find | xargs` without `-print0`, `cd X; Y` without
`||`, `[[ ]]` with `>`/`<` on numerics, `mktemp` before its cleanup
`trap`, function-local variables without `local`.

**Documentation.** Top-of-file header present and populated. All
non-zero exit codes documented. No bare `TODO` — use `TODO(name)`.
Filename matches `PROGNAME` derivation. Heredocs in help are quoted
(`<<'EOF'`). Error output goes to stderr (`>&2`).

Also re-check the FX.1 signals now that the draft exists — signals
hiding behind a feature request sometimes only surface once the
scaffold is concrete. If a signal fires now, halt and recommend an
alternative.

## 6. Review Gate

Present both artifacts and wait for explicit user approval before
writing any file to disk. Write only after this gate passes.

If the user requests changes, revise and re-present. Continue until
the user explicitly approves the artifacts or cancels. Proceed to Save
only on explicit approval.

## 7. Save

Write the approved script to the user-supplied path from Elicit. Make
it executable:

```bash
chmod +x <path>
```

Show the suggested invocation line for the user to wire into their
Makefile, CI config, or README.

## 8. Test

Offer the audit:

> "Run `/build:check-shell <path>` to audit the scaffolded script
> against the 14 lints plus `shellcheck` / `shfmt` (when installed)?"

## Anti-Pattern Guards

1. **Skipping the FX.1 Scope Gate** — always probe the five signals
   before Elicit. A scaffolded script for a case that should have been
   Python or a hook actively increases shell in the codebase where it
   does not belong.
2. **Single-template rigidity** — the template is conditionalized on
   target-shell and setuid. Producing a bash-4 template when the user
   picked `bash-3.2-portable`, or an `env bash` shebang for a setuid
   script, is a correctness failure, not a style preference.
3. **Skipping the Review Gate** — write to disk only after explicit
   approval. Present both artifacts first.
4. **Scaffolding without populating `REQUIRED_CMDS`** — an empty
   preflight array silently skips the whole fail-fast mechanism. Always
   elicit runtime deps and populate the array, even if the list is `()`.

## Key Instructions

- Refuse cleanly on FX.1 signals. Do not scaffold a script when shell
  is the wrong tool and then apologize in comments.
- Do not write any file before the Review Gate passes.
- Do not invent a save path. Elicit it.
- Strip bash-only features when the target is `posix-sh`; do not leave
  them in with a disclaimer.
- The dependency preflight must name the missing tool and emit a
  platform-specific install hint to stderr. Silent `exit 1` is a
  failure of this skill's core contract.

## Handoff

**Receives:** user intent for a shell script (target shell, purpose,
invocation style, setuid intent, runtime dependencies, save path).
**Produces:** an executable shell script at the user-supplied path
plus a suggested invocation line.
**Chainable to:** `/build:check-shell` (audit the scaffold against
the 14 lints and available external tools).
