---
name: Repair Playbook — Bash Scripts
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-bash-script opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-bash-script. Every Tier-1
finding type and every Tier-2 dimension has a recipe here. Apply one
at a time, with explicit user confirmation, re-running the producing
check after each fix.

**HINT-severity findings are feed-forward context, not repair
targets.** They inform the Tier-2 prompt; they do not enter the
repair queue.

## Table of Contents

- [Format](#format)
- Tier-1 recipes
  - [`check_secrets.py`](#tier-1--check_secretspy)
  - [`check_structure.py`](#tier-1--check_structurepy)
  - [`check_idioms.py`](#tier-1--check_idiomspy)
  - [`check_safety.py`](#tier-1--check_safetypy)
  - [`check_shellcheck.py`](#tier-1--check_shellcheckpy)
  - [`check_shfmt.sh`](#tier-1--check_shfmtsh)
  - [`check_size.sh`](#tier-1--check_sizesh)
- [Tier-2 — Judgment Dimension Recipes](#tier-2--judgment-dimension-recipes)
  - D1 Output Discipline · D2 Input Validation · D3 Subprocess & Tool Hygiene · D4 Performance Intent · D5 Function Design · D6 Naming · D7 Commenting Intent
- [Tier-3 — Cross-Entity Collision](#tier-3--cross-entity-collision)
- [Notes](#notes)

## Format

Each recipe carries five fields:

- **Signal** — the finding string or dimension name that triggers the recipe
- **CHANGE** — what to modify, in one sentence
- **FROM** — a concrete example of the non-compliant pattern
- **TO** — the compliant replacement
- **REASON** — why the change matters, tied to the source principle

---

## Tier-1 — `check_secrets.py`

### Signal: `secret — API key / token / private URL detected`

**CHANGE** Remove the secret from source. Replace with an env-var
read at the top of the script and a `${VAR:?...}` guard so the
script fails fast if the variable is unset.

**FROM**
```bash
readonly API_KEY="sk-proj-abc123def456..."
```

**TO**
```bash
readonly API_KEY="${OPENAI_API_KEY:?OPENAI_API_KEY env var required}"
```

**REASON** Secrets in committed source leak through git history,
logs, and backups. Externalizing to the environment is the minimum
bar; a secret manager is better where available.

---

## Tier-1 — `check_structure.py`

### Signal: `shebang — first line is not a bash shebang`

**CHANGE** Replace the first line with `#!/usr/bin/env bash` (or
`#!/bin/bash` in tightly controlled environments where `PATH` is
trusted).

**FROM** `#!/bin/sh` *or* `#!/usr/bin/python` *or* missing shebang
**TO** `#!/usr/bin/env bash`

**REASON** This skill is bash-only. A `#!/bin/sh` shebang invites
silent bashisms-fail-on-dash bugs; missing shebang means the script
runs under whatever shell the invoker happens to have.

### Signal: `strict-mode — \`set -euo pipefail\` missing from prologue`

**CHANGE** Add `set -euo pipefail` immediately after the shebang and
header comment.

**FROM**
```bash
#!/usr/bin/env bash
# Process some files.

main() { ... }
```

**TO**
```bash
#!/usr/bin/env bash
# Process some files.

set -euo pipefail

main() { ... }
```

**REASON** Strict mode turns silent failures, unset-variable typos,
and mid-pipeline errors into loud, early exits. Without it, a typo
in `$user_imput` silently expands to empty.

### Signal: `header-comment — no purpose/usage comment in first 10 lines`

**CHANGE** Add a header comment block naming purpose, usage,
dependencies, and exit codes.

**FROM**
```bash
#!/usr/bin/env bash
set -euo pipefail
main() { ... }
```

**TO**
```bash
#!/usr/bin/env bash
#
# rotate-logs — Compress logs older than 30 days.
#
# Usage:
#   rotate-logs.sh [--dry-run] <log-dir>
#
# Dependencies: gzip, find
#
# Exit codes: 0 success, 1 failure, 64 usage error

set -euo pipefail

main() { ... }
```

**REASON** The header is the first thing a reader sees. A script
without one is opaque to anyone who isn't the author.

### Signal: `main-fn — no main function defined`

**CHANGE** Wrap the top-level execution logic in a `main` function.

**FROM**
```bash
#!/usr/bin/env bash
set -euo pipefail

input="$1"
process "$input"
```

**TO**
```bash
#!/usr/bin/env bash
set -euo pipefail

main() {
  local input="${1:?input required}"
  process "$input"
}

main "$@"
```

**REASON** A `main` function makes the script sourceable for testing
and gives a single entry point a reader can find immediately.

### Signal: `main-guard — no \`[[ "${BASH_SOURCE[0]}" == "$0" ]]\` guard`

**CHANGE** Add the sourceable guard at the bottom; let it invoke
`main`.

**FROM**
```bash
main "$@"
```

**TO**
```bash
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

**REASON** The guard lets the file be sourced for testing (`. ./script.sh`
loads functions without running `main`). Without it, sourcing the
file runs the entire script as a side effect.

### Signal: `readonly-config — top-level constants not declared readonly`

**CHANGE** Promote top-level configuration to `readonly` constants.

**FROM**
```bash
TIMEOUT=30
MAX_RETRIES=3
```

**TO**
```bash
readonly TIMEOUT=30
readonly MAX_RETRIES=3
```

**REASON** `readonly` makes accidental reassignment a hard error and
signals to the reader that the value is configuration, not state.

### Signal: `mktemp-trap-pairing — \`mktemp\` invoked without prior \`trap ... EXIT\``

**CHANGE** Register a cleanup `trap` immediately after `mktemp` (or
before, when feasible). Capture the temp path in a variable so the
trap can reference it.

**FROM**
```bash
tmpdir="$(mktemp -d)"
do_work "$tmpdir"
```

**TO**
```bash
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT INT TERM
do_work "$tmpdir"
```

**REASON** Without the trap, the temp directory leaks on any non-zero
exit (including signals). Disk fills up; subsequent runs collide.

---

## Tier-1 — `check_idioms.py`

### Signal: `bracket-test — \`[ ... ]\` used in a bash script`

**CHANGE** Replace `[ ... ]` with `[[ ... ]]`.

**FROM** `if [ "$x" = "y" ]; then`
**TO** `if [[ "$x" == "y" ]]; then`

**REASON** `[[ ]]` does not word-split inside the brackets, supports
pattern matching, and has saner numeric / string comparison. There's
no portability cost in a bash-only file.

### Signal: `printf-over-echo — \`echo\` used for non-trivial output`

**CHANGE** Replace `echo` with `printf` when escapes, format
specifiers, or multi-arg output is involved.

**FROM** `echo -e "name:\t$name\nvalue:\t$value"`
**TO** `printf 'name:\t%s\nvalue:\t%s\n' "$name" "$value"`

**REASON** `echo`'s handling of `-e`, `-n`, and escape sequences
varies across shells. `printf` is portable and does what you wrote.

### Signal: `var-braces — \`$var\` adjacent to text without braces`

**CHANGE** Add braces when the variable is followed by characters
that could be part of an identifier.

**FROM** `printf '%s_log\n' "$prefix$timestamp"`
**TO** `printf '%s_log\n' "${prefix}${timestamp}"`

**REASON** `"$prefixfoo"` is a different (probably empty) variable;
`"${prefix}foo"` is unambiguous.

---

## Tier-1 — `check_safety.py`

### Signal: `eval — \`eval\` invocation without justification comment` *(FAIL)*

**CHANGE** Replace `eval` with a targeted construct (parameter
expansion, `case`, dispatch table). If `eval` is genuinely required
(rare), justify it with `# shellcheck disable=SC2294 # <reason>` or
`# eval-justified: <reason>`.

**FROM** `eval "$user_input"`
**TO** Replace with explicit dispatch:
```bash
case "$action" in
  start) start_server ;;
  stop)  stop_server  ;;
  *)     die "unknown action: $action" ;;
esac
```

**REASON** `eval` on input is shell injection — full stop. Most
`eval` uses are pattern matches that `case` or arrays cover safely.

### Signal: `gnu-flags — GNU-specific flag used without dependency declaration`

**CHANGE** Either declare the GNU-coreutils dependency in the header
comment, or replace the flag with a portable alternative.

**FROM** `sed -i 's/foo/bar/' file.txt`
**TO** Either:
```bash
# Dependencies: gnu-coreutils (sed -i without backup is GNU-only)
```
Or use a portable form:
```bash
sed 's/foo/bar/' file.txt > file.txt.new && mv file.txt.new file.txt
```

**REASON** `sed -i` accepts no argument on GNU and requires a
backup-suffix argument on macOS/BSD. Silent cross-platform divergence
is a recurring real-world failure.

### Signal: `tmp-literal — hardcoded \`/tmp/\` or \`/var/tmp/\` path` *(FAIL)*

**CHANGE** Replace with `mktemp` + `trap` cleanup.

**FROM** `out="/tmp/work_$$"`
**TO**
```bash
out="$(mktemp)"
trap 'rm -f "$out"' EXIT INT TERM
```

**REASON** Predictable temp paths invite races (other processes can
guess the name) and symlink attacks (a malicious symlink at the
expected location redirects writes elsewhere).

---

## Tier-1 — `check_shellcheck.py`

`check_shellcheck.py` wraps `shellcheck`; the recipes below cover the
emitted rule codes.

### Signal: `SC2086 — unquoted variable expansion` *(FAIL)*

**CHANGE** Add double quotes around the expansion.

**FROM** `for f in $files; do`
**TO** `for f in "$files"; do` *or* iterate properly: `for f in "${files[@]}"; do`

**REASON** Without quotes, `$files` word-splits on `IFS` and globs
filenames containing `*` / `?`. The single largest source of
real-world bash bugs.

### Signal: `SC2046 — unquoted command substitution` *(FAIL)*

**CHANGE** Quote the `$(...)` expansion.

**FROM** `cmd $(other_cmd)`
**TO** `cmd "$(other_cmd)"`

**REASON** Same issue as SC2086 — splitting and globbing of
substitution output.

### Signal: `SC2068 — unquoted \`$@\`` *(FAIL)*

**CHANGE** Quote `$@` as `"$@"`.

**FROM** `cmd $@`
**TO** `cmd "$@"`

**REASON** `"$@"` preserves argument boundaries (whitespace, special
characters). `$@` unquoted re-splits arguments and merges them.

### Signal: `SC2154 — referenced but not assigned`

**CHANGE** Either assign the variable, or add a default with
`${var:-default}`, or guard it with `${var:?message}` to fail fast.

**FROM** `printf '%s\n' "$config_path"`  *(when never assigned)*
**TO** `printf '%s\n' "${config_path:?config_path required}"`

**REASON** Shellcheck's static analysis caught a likely typo or
forgotten assignment. Either name an intent or fail fast.

### Signal: `SC2155 — function variable assigned without \`local\``

**CHANGE** Split into `local` declaration + assignment so the exit
status is preserved.

**FROM** `local result=$(some_cmd)`
**TO**
```bash
local result
result="$(some_cmd)"
```

**REASON** `local result=$(cmd)` masks the return code of `cmd`
because `local` itself returns 0. Splitting the declaration preserves
the substitution's exit status, which strict mode (`set -e`) needs.

### Signal: `SC2006 — backtick command substitution`

**CHANGE** Replace backticks with `$(...)`.

**FROM** `count=`wc -l < file``
**TO** `count="$(wc -l < file)"`

**REASON** `$(...)` is nestable, more readable, and universally
supported by linters and modern shells. Backticks are a 1980s relic.

### Signal: `SC2010` / `SC2012` / `SC2045` — parsing `ls` output *(FAIL)*

**CHANGE** Use globs or `find -print0` instead.

**FROM** `for f in $(ls *.log); do`
**TO** `for f in *.log; do` *or* `find . -name '*.log' -print0 | xargs -0 ...`

**REASON** Filenames with spaces, newlines, or leading dashes break
`ls` parsing. Globs and `find -print0` handle them safely.

### Signal: `SC2013 / SC2162 — \`for line in $(cat file)\``

**CHANGE** Replace with `while IFS= read -r`.

**FROM** `for line in $(cat file); do`
**TO**
```bash
while IFS= read -r line; do
  ...
done < file
```

**REASON** The `for in $(cat)` idiom word-splits on `IFS` and globs
each line — it's wrong, not just slow. `while IFS= read -r` reads
lines verbatim.

### Signal: `SC2038 — \`find ... | xargs ...\` without \`-print0\``

**CHANGE** Add `-print0` to `find` and `-0` to `xargs`, or use
`-exec ... {} +`.

**FROM** `find . -name '*.log' | xargs rm`
**TO** `find . -name '*.log' -print0 | xargs -0 rm` *or* `find . -name '*.log' -exec rm {} +`

**REASON** Default whitespace separation in `xargs` breaks on
filenames with spaces or newlines. Null-separated piping is
filename-safe.

### Signal: `SC2164 — \`cd\` without \`|| exit\``

**CHANGE** Add `|| exit` (or `|| return` inside a function), or rely
on `set -e` and document that.

**FROM** `cd /some/dir; rm -rf *`
**TO** `cd /some/dir || exit; rm -rf *`

**REASON** A failed `cd` followed by `rm -rf *` operates on the
current directory — a destroyed-systems pattern. The guard is one
character of insurance.

### Signal: `SC2002 — useless use of \`cat\``

**CHANGE** Pipe directly from the file.

**FROM** `cat file | grep pattern`
**TO** `grep pattern file` *or* `< file grep pattern`

**REASON** Style; ShellCheck flags it as wasteful (one extra fork).
Some authors prefer the left-to-right `cat | cmd` reading order — if
that's the case, leave a `# shellcheck disable=SC2002` justification.

### Signal: `SC2294 — \`eval\` of array contents` *(FAIL)*

**CHANGE** Pass arguments directly without `eval`.

**FROM** `eval "${cmd[@]}"`
**TO** `"${cmd[@]}"`

**REASON** `eval` on array contents performs a second shell-parsing
pass over the expanded values, which re-introduces injection
vulnerability for any value containing shell metacharacters.

---

## Tier-1 — `check_shfmt.sh`

### Signal: `format — \`shfmt -d\` produces non-empty diff`

**CHANGE** Run `shfmt -w -i 2 -ci -bn <file>` to apply the canonical
format.

**FROM** *(formatting drift — tab indent, missing case-indent, etc.)*
**TO** *(formatted: 2-space indent, case-indent, binop on next line)*

**REASON** Formatter drift produces noisy diffs and triggers the
"someone fix the spacing" PR trickle. `shfmt` is mechanical; let the
tool do the work.

---

## Tier-1 — `check_size.sh`

### Signal: `size — script length over 300 non-blank lines`

**CHANGE** Extract cohesive sections into helper scripts (`source`d
from a top-level orchestrator), or convert to a real language
(Python via `/build:build-python-script`).

**FROM** *(a 500-line single-file bash script with four logical
sections inlined)*

**TO** Either a smaller orchestrator that sources `_lib_fetch.sh`,
`_lib_transform.sh`, `_lib_validate.sh`, or a Python rewrite if the
logic genuinely outgrew bash.

**REASON** Bash's lack of data structures and error handling does not
scale. Past ~300 lines, a refactor is cheaper than maintenance.

### Signal: `line-length — line exceeds 100 characters`

**CHANGE** Break long lines using bash continuation (`\`) or refactor
into a helper.

**FROM**
```bash
result="$(some_command --with --many --flags --and "$arg" --more "$another" 2>/dev/null || die "failed")"
```

**TO**
```bash
result="$(
  some_command --with --many --flags --and "$arg" --more "$another" 2>/dev/null \
    || die "some_command failed"
)"
```

**REASON** Long lines are unreadable in code review and break
side-by-side diff views. The 100-char threshold is the Google Shell
Style Guide convention.

---

## Tier-2 — Judgment Dimension Recipes

Tier-2 findings carry WARN severity; they're coaching, not blocking.
Each recipe is a repair pattern the user can apply after the judge
names a specific violation.

### D1 Output Discipline

**CHANGE** Define a `die` helper (if absent), route error and log
output through it (or with explicit `>&2`), and ensure every error
branch returns non-zero.

**FROM**
```bash
echo "error: $err"
exit 0
```

**TO**
```bash
die() { printf 'error: %s\n' "$*" >&2; exit 1; }
die "$err"
```

**REASON** Unix pipelines depend on the stdout-for-data /
stderr-for-chatter convention. Callers in cron, CI, and Makefiles
depend on the exit-code contract.

### D2 Input Validation & Destructive-Op Safety

**CHANGE** Add input validation early in `main`. Wire the `--dry-run`
flag into the destructive code path.

**FROM**
```bash
for path in "$@"; do
  rm -rf "$path"
done
```

**TO**
```bash
for path in "$@"; do
  [[ -e "$path" ]] || { printf 'skip: %s does not exist\n' "$path" >&2; continue; }
  if [[ "${dry_run:-0}" -eq 1 ]]; then
    printf 'would remove: %s\n' "$path"
    continue
  fi
  rm -rf -- "$path"
done
```

**REASON** "Fail before damage" is cheap to implement and expensive
to skip. `--dry-run` that isn't consulted is worse than no flag — it
implies a safety that isn't there. `--` before `"$path"` prevents
option-injection from filenames starting with `-`.

### D3 Subprocess & Tool Hygiene

**CHANGE** Add a `preflight` function that verifies every required
external command up front; register a `trap` for cleanup if the
script creates state; declare GNU-coreutils dependency in the header
when GNU flags are used.

**FROM** *(no preflight; direct call to `jq` deep in the script)*
**TO**
```bash
REQUIRED_CMDS=(jq curl)

preflight() {
  local cmd missing=()
  for cmd in "${REQUIRED_CMDS[@]}"; do
    command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
  done
  [[ "${#missing[@]}" -eq 0 ]] || die "missing required commands: ${missing[*]}"
}

main() {
  preflight
  ...
}
```

**REASON** Failing fast with an actionable message beats failing
mid-run with a cryptic "command not found".

### D4 Performance Intent

**CHANGE** Replace external-command calls inside loops with bash
builtins or parameter expansion.

**FROM** `for f in *.log; do basename "$f" .log; done`
**TO** `for f in *.log; do echo "${f%.log}"; done`

**REASON** Each `basename` invocation is a fork — at scale, the loop
becomes fork-dominated. Parameter expansion is in-process and
typically 100×+ faster.

### D5 Function Design

**CHANGE** Extract cohesive sections of a long `main` into named
helpers. Add the sourceable guard if missing.

**FROM** *(a 150-line `main` that inlines fetch, transform, validate, write)*
**TO**
```bash
main() {
  local args="$*"
  local raw=$(fetch "$args")
  local records=$(transform "$raw")
  validate "$records"
  write "$records"
}

[[ "${BASH_SOURCE[0]}" == "${0}" ]] && main "$@"
```

**REASON** Short named helpers read as their own commentary. The
sourceable guard enables `bats` / `shunit2` testing.

### D6 Naming

**CHANGE** Rename the variable / function to state intent. Replace
single-letter / shadowing names.

**FROM** `local Tmp=$(some_cmd); local x=...`
**TO** `local raw_records=$(some_cmd); local row_count=...`

**REASON** Bash's lack of types makes naming the load-bearing
documentation. `Tmp` and `x` force the reader to derive intent from
the body.

### D7 Commenting Intent

**CHANGE** Add or fix the header comment; remove what-comments;
tag owner-less TODOs.

**FROM**
```bash
# TODO: fix this
# increment counter
((counter++))
```

**TO**
```bash
# TODO(bbeidel): handle Unicode normalization before count
((counter++))
```

**REASON** Comments that restate code rot alongside it. Comments that
explain *why* stay useful. Untagged TODOs accumulate as orphan
maintenance debt.

---

## Tier-3 — Cross-Entity Collision

### Signal: `collision — duplicated helpers / argument-parsing across scripts`

**CHANGE** Extract the shared block into a helper file
(`<dir>/_helpers.sh`) and `source` it from each script. If the
scripts are truly independent, accept the duplication — DRY applies
to scripts that will co-evolve, not scripts that happen to look alike.

**FROM** `die() { ... }` / `usage() { ... }` / `preflight() { ... }`
copied across three scripts with identical or near-identical bodies.

**TO**
```bash
# _helpers.sh
die() { printf 'error: %s\n' "$*" >&2; exit 1; }
usage() { ... }
preflight() { ... }

# script1.sh
source "$(dirname "${BASH_SOURCE[0]}")/_helpers.sh"
```

**REASON** Shared utilities drift when maintained in triplicate. A
single source of truth keeps the helpers coherent.

---

## Notes

- **HINT-severity findings** are pre-filter pre-evaluations, not
  repair targets. They inform the Tier-2 prompt and do not enter the
  repair queue.
- **Per-finding confirmation** is non-negotiable. Bulk application
  removes the user's ability to review individual changes and is a
  documented anti-pattern in the check-bash-script SKILL.md.
- **Re-run after each fix.** A repair can introduce a new finding
  elsewhere (e.g., adding `set -euo pipefail` may surface SC2155
  findings that were latent). The Tier-1 script that produced the
  original finding re-runs before moving to the next repair.
- **Missing-tool INFO is not a repair target.** When `shellcheck` or
  `shfmt` is absent, install the tool — `brew install shellcheck`
  / `brew install shfmt` on macOS, `apt install shellcheck` /
  `apt install shfmt` on Debian/Ubuntu — and re-run the audit.
