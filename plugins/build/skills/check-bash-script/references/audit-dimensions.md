---
name: Audit Dimensions — Bash Scripts
description: The complete check inventory for check-bash-script — Tier-1 deterministic check table (~26 checks across 7 scripts) and Tier-2 judgment dimension specifications (7 dimensions, each citing its source principle). Referenced by the check-bash-script workflow.
---

# Audit Dimensions

The check-bash-script audit runs in three tiers. This document is the
inventory: every deterministic check Tier-1 emits, every judgment
dimension Tier-2 evaluates. Every dimension cites the source principle
it audits from
[bash-script-best-practices.md](../../../_shared/references/bash-script-best-practices.md).

## Tier-1 — Deterministic Checks

Seven scripts, ~26 atomic checks. Each script emits findings in the
fixed lint format (`SEVERITY  <path> — <check>: <detail>` +
`Recommendation:`). Exit codes: `0` clean / WARN / INFO / HINT-only;
`1` on FAIL; `64` arg error; `69` missing required dependency
(shellcheck and shfmt are optional and degrade gracefully).

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.sh` | `secret` | API keys, tokens, private URLs via regex pattern list | FAIL | Hold the safety posture (toolkit convention) |
| `check_structure.sh` | `shebang` | First line is `#!/usr/bin/env bash` or `#!/bin/bash`; reject `#!/bin/sh` and other non-bash shebangs | FAIL | Declare the dialect explicitly |
| `check_structure.sh` | `strict-mode` | `set -euo pipefail` (or equivalent three separate `set` lines) appears in the first ~20 non-comment lines | FAIL | Enable strict mode at the top |
| `check_structure.sh` | `header-comment` | A comment block in the first 10 lines names purpose / usage / dependencies | WARN | Document intent at the top |
| `check_structure.sh` | `main-fn` | A `main` function is defined | WARN | Make scripts sourceable |
| `check_structure.sh` | `main-guard` | `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"` (or equivalent) at module bottom | WARN | Make scripts sourceable |
| `check_structure.sh` | `readonly-config` | Top-level non-trivial constants declared with `readonly` | WARN | Scope variables locally |
| `check_structure.sh` | `mktemp-trap-pairing` | Every `mktemp` invocation is preceded by a `trap ... EXIT` registration | WARN | Set up cleanup before you create temp state |
| `check_idioms.sh` | `bracket-test` | `[[ ... ]]` used in place of `[ ... ]` for tests | WARN | Use modern Bash idioms |
| `check_idioms.sh` | `printf-over-echo` | `printf` used for non-trivial output (multi-arg, escapes, format specifiers) | WARN | Use modern Bash idioms |
| `check_idioms.sh` | `var-braces` | `${var}` braces present when the expansion is adjacent to text that could be part of an identifier | WARN | Use modern Bash idioms |
| `check_safety.sh` | `eval` | `eval` flagged unless the same line or preceding line carries `# shellcheck disable=SC2294` or `# eval-justified:` | FAIL | Hold the safety posture |
| `check_safety.sh` | `gnu-flags` | `sed -i` (without backup), `grep -P`, `readlink -f`, `date -d`, `stat -c`, `xargs -r` flagged unless a `# requires: gnu-coreutils` prologue comment is present | WARN | Verify required commands exist up front |
| `check_safety.sh` | `tmp-literal` | String literals starting with `/tmp/` or `/var/tmp/` flagged | FAIL | Set up cleanup before you create temp state |
| `check_shellcheck.sh` | `SC2086` | Unquoted variable expansion permitting word-splitting / globbing | FAIL | Quote everything that expands |
| `check_shellcheck.sh` | `SC2046` | Unquoted command substitution | FAIL | Quote everything that expands |
| `check_shellcheck.sh` | `SC2068` | Unquoted `$@` (use `"$@"`) | FAIL | Quote everything that expands |
| `check_shellcheck.sh` | `SC2154` | Variable referenced but not assigned | WARN | Quote everything that expands |
| `check_shellcheck.sh` | `SC2155` | Function variable assigned without `local` | WARN | Scope variables locally |
| `check_shellcheck.sh` | `SC2006` | Backtick command substitution; use `$(...)` | WARN | Use modern Bash idioms |
| `check_shellcheck.sh` | `SC2010` / `SC2012` / `SC2045` | Parsing `ls` output | FAIL | Use modern Bash idioms (filename safety) |
| `check_shellcheck.sh` | `SC2013` / `SC2162` | `for line in $(cat ...)`; use `while IFS= read -r` | WARN | Use modern Bash idioms |
| `check_shellcheck.sh` | `SC2038` | `find ... | xargs ...` without `-print0` / `-0` | WARN | Use modern Bash idioms (filename safety) |
| `check_shellcheck.sh` | `SC2164` | `cd` not followed by `|| exit` / `|| return` (without `set -e` covering it) | WARN | Hold the safety posture |
| `check_shellcheck.sh` | `SC2002` | Useless use of `cat` | WARN | Performance (Patterns That Work) |
| `check_shellcheck.sh` | `SC2294` | `eval` of array contents | FAIL | Hold the safety posture |
| `check_shfmt.sh` | `format` | `shfmt -d -i 2 -ci -bn` produces a non-empty diff | WARN | Use modern Bash idioms (style consistency) |
| `check_size.sh` | `size` | Script length exceeds 300 non-blank lines | WARN | Review and Decay (graduate to a real language) |
| `check_size.sh` | `line-length` | Any line exceeds 100 characters | WARN | Review and Decay (readability) |

**FAIL exclusions from Tier-2.** Any `secret`, `shebang` (non-bash),
`eval`, `tmp-literal`, `SC2086`, `SC2046`, `SC2068`, `SC2294`, or
`SC2010` / `SC2012` / `SC2045` (parse-`ls`) finding excludes the file
from Tier-2. Other FAILs (`strict-mode` missing) leave a parseable
bash script that judgment can still evaluate productively.

**Missing-tool degradation.** `check_shellcheck.sh` and
`check_shfmt.sh` emit an INFO finding (`tool-missing`) and exit 0 when
the wrapped tool is absent. The remaining scripts continue running.
The Missing Tools INFO is the user's signal that Tier-1 coverage is
reduced — surfacing it is the contract.

## Tier-2 — Judgment Dimensions

One LLM call per file. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless a dimension explicitly marks otherwise —
judgment-level drift is coaching, not blocking.

### D1 Output Discipline

**Source principles:** *Treat I/O as a contract.*

**Judges:** Does data output go to stdout while logs / errors /
prompts go to stderr? Is a `die` (or `error`) helper defined and used
for failure paths, instead of bare `exit 1` with no message? Does
every documented or implied failure mode produce a non-zero exit
code?

**PASS conditions:** Error and log output uses `>&2` or routes through
`die`. The `die` helper exists if the script has any error paths.
Every error branch ends with `die` or `exit N` where `N > 0`.

**Common fail signal:** `echo "error: $err"` (no `>&2`); error
branches that log and then `exit 0`; `exit 1` with no preceding
message.

### D2 Input Validation & Destructive-Op Safety

**Source principles:** *Validate inputs early; fail before damage*;
*Hold the safety posture*; *Set up cleanup before you create temp
state.*

**Judges:** Are inputs validated before any destructive or expensive
work? Are required inputs gated with `${var:?message}` (or equivalent
explicit check)? For deletes / overwrites / irreversible network
calls, is there a `--dry-run` (or confirmation) flag, and does the
destructive branch actually consult it? Are credentials and hostnames
externalized (env vars or files), never argv? Is `--` used before
untrusted arguments to option-parsing commands?

**PASS conditions:** `${var:?}` or explicit `[[ -n "$var" ]] || die`
for required inputs. Destructive branches check a dry-run / yes flag.
No secrets in argv. `rm -rf "$var"` is preceded by `[[ -n "$var" ]]`
validation. `--` precedes any user-supplied argument to `rm`, `grep`,
`mv`, `cp`.

**Common fail signal:** `rm -rf "$dir"` with no existence check;
`--dry-run` flag declared but never consulted; `password=$1` (secret
in argv); `rm -rf $var` unquoted.

### D3 Subprocess & Tool Hygiene

**Source principles:** *Verify required commands exist up front*;
*Hold the safety posture* (signal handling subset); *Declare the
dialect explicitly* (GNU-flag declaration subset).

**Judges:** Does `main` (or the prologue) preflight required external
commands with `command -v`? When the script uses GNU-specific flags
(`sed -i`, `grep -P`, etc.), does the header declare the dependency
or pin to GNU coreutils? Is `trap` registered for `EXIT` (and often
`INT` / `TERM`) when the script creates temp state, opens
connections, or holds locks?

**PASS conditions:** `command -v <cmd> >/dev/null || die "missing:
<cmd>"` for every external dep. GNU-only flags either avoided or
documented. `trap 'cleanup' EXIT INT TERM` registered before the
first `mktemp` / `mkdir -p $tmp` / connection-open.

**Common fail signal:** A script that calls `jq` with no preflight;
`sed -i` used silently (Linux/macOS divergence on `-i` argument
semantics); `mktemp -d` with no trap.

### D4 Performance Intent

**Source principles:** Performance subsection of the principles doc.

**Judges:** Does the script call external commands inside a tight
loop where a single `awk` / `sed` pass would do? Does it use
`basename` / `dirname` / `sed` for simple string operations where
parameter expansion (`${var##*/}`, `${var%.*}`) suffices? Are
unnecessary subshells (`$(...)` for non-substitution work) eliminated?

**PASS conditions:** Loops use builtins for per-iteration work;
parameter expansion replaces obvious external-tool calls. Subshells
present only where command substitution requires them.

**Common fail signal:** `for f in *.log; do basename "$f" .log; done`
(use `${f%.log}` instead); `cat file | grep pattern` (use `grep
pattern file`); a tight loop calling `date` or `wc` per iteration.

### D5 Function Design

**Source principles:** *Make scripts sourceable*; *Keep functions
small and single-purpose.*

**Judges:** Does `main` read as an orchestrator — a sequence of named
operations — rather than a wall of inline pipelines? Are function
bodies short and named for what they do? Does the sourceable guard
exist at the bottom so `bats` / `shunit2` can load the file without
running `main`?

**PASS conditions:** `main` reads top-to-bottom as a list of helper
calls; helpers each have a verb-phrased name and short body; the
guard `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"` is at the
file's bottom.

**Common fail signal:** A 200-line `main` that inlines everything;
helper names like `do_stuff`; the file is not sourceable (no guard).

### D6 Naming

**Source principles:** *Name intent into the code.*

**Judges:** Are local variables `snake_case` lowercase? Are exported
env vars and module-level constants `UPPERCASE`? Do names state
intent (no `tmp`, `data`, `i` outside short loops, `process_it`)? Are
shell builtins shadowed (`local`, `echo`, `set`)?

**PASS conditions:** Local variables consistently `snake_case`; env
vars / readonly constants `UPPERCASE`; descriptive names; no builtin
shadowing.

**Common fail signal:** `local Tmp=...`, `local x=$(cmd)` at module
scope, a function named `do_thing`, a local variable named `echo`.

### D7 Commenting Intent

**Source principles:** *Document intent at the top.*

**Judges:** Does the header comment name purpose, usage signature,
and external dependencies? Do inline comments explain *why* a
non-obvious choice was made — constraints, workarounds, hidden
invariants — or do they restate what the code already says? Do TODOs
carry an owner or ticket?

**PASS conditions:** Header block in the first 10 lines covers
purpose / usage / dependencies. Inline comments explain rationale;
none restate code. TODOs are tagged.

**Common fail signal:** No header comment; `# increment counter`
above `((counter++))`; bare `# TODO: fix this` with no owner.

## Tier-3 — Cross-Entity Collision

### collision

**What it checks:** When the audit scope holds multiple scripts in the
same directory, look for duplicated helpers / argument-parsing /
error-handling logic that the maintainer could consolidate.
**Severity:** WARN.
**Source principle:** *Keep functions small and single-purpose* +
*Review and Decay* — duplicated logic is the early warning that the
script collection wants a real library.

## Cross-Dimension Notes

**All dimensions run always.** A dimension that doesn't apply (D2
Input Validation on a script with no destructive operations; D3
Subprocess Hygiene on a script with no external calls) returns PASS
silently.

**One finding per dimension maximum.** If D5 Function Design
identifies four problematic functions, surface the highest-signal
one with concrete detail (line numbers, what to extract). Bulk
findings train the user to disregard the audit.

**Severity defaults to WARN.** Tier-2 findings are judgment-level
coaching, not blocking. A dimension that surfaces a safety concern
the Tier-1 scripts missed (e.g., a hand-rolled SQL-shaped string in
shell that shellcheck did not flag) can be escalated to FAIL by the
judge, but the default is WARN — Tier-1 is where blocking lives.
