---
name: Bash Scripts Best Practices
description: Authoring guide for Bash 4.0+ scripts — what makes a script load-bearing in production ops tooling, how to shape the file, the positive patterns that work, and the safety and maintenance posture. Referenced by build-bash-script and check-bash-script.
---

# Bash Scripts Best Practices

## What a Good Bash Script Does

A Bash script is a single-file program that automates a workflow built from existing CLI tools — `git`, `curl`, `jq`, `find`, `xargs`, `rsync`, and the shell itself. It runs from a terminal or a Makefile, returns a useful exit code, and stays composable in pipelines. The value proposition is narrow: a script earns its place when the work is genuine glue across CLI tools, the failure modes are mostly subprocess failures, and the alternative (a Python script or a service) would add ceremony the task does not need.

The scope here is **Bash 4.0 or newer**. POSIX `sh` portability is a different concern — when the work needs `dash` / BusyBox / Alpine, that is a separate decision the language-selection step in `primitive-routing.md` covers. Authoring this skill assumes Bash on macOS (Homebrew) or Linux (system).

## Anatomy

```bash
#!/usr/bin/env bash
#
# greet.sh — Print a greeting.
#
# Usage:
#   greet.sh <name>
#
# Dependencies: none

set -euo pipefail

readonly DEFAULT_GREETING="hello"

die() {
  printf 'error: %s\n' "$*" >&2
  exit 1
}

main() {
  local name="${1:?name required}"
  printf '%s, %s\n' "$DEFAULT_GREETING" "$name"
}

[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"
```

Load-bearing pieces: the explicit `bash` shebang, `set -euo pipefail` in the prologue, a header comment naming purpose and usage, configuration as `readonly` constants near the top, a `die`/`error` helper, function-scoped variables declared with `local`, a `main` function as the orchestrator, and the sourceable guard at the bottom that lets the file be tested without executing.

## Authoring Principles

**Declare the dialect explicitly.** Start with `#!/usr/bin/env bash` (or `#!/bin/bash` in tightly controlled environments where PATH is trusted). The shebang is the dialect contract — readers, ShellCheck, and `shfmt` all key off it. Bash-only features under a `#!/bin/sh` shebang fail silently on `dash`, BusyBox, and Alpine; pick one dialect per script and stay there.

**Enable strict mode at the top.** `set -euo pipefail` near the top of every script turns silent failures, unset-variable typos, and mid-pipeline errors into loud, early exits. Strict mode has known edge cases — `-e` is skipped in `&&` chains, function calls in conditions, and similar contexts — so check exit statuses explicitly where strict mode does not help. The defaults make scripts safer; the supplements make them correct.

**Quote everything that expands.** `"$var"`, `"$(cmd)"`, `"${arr[@]}"`, `"$@"` — double-quote variable expansions and command substitutions unless splitting or globbing is *explicitly* intended. Unquoted expansion is the single largest source of real-world Bash bugs. Forward arguments with `"$@"`, never `$*` or unquoted `$@`.

**Use modern Bash idioms.** `[[ ... ]]` over `[ ... ]` for conditionals (no word-splitting inside tests, supports pattern matching). `$(...)` over backticks for command substitution (nestable, readable). `printf` over `echo` for anything beyond a literal string (`echo`'s flag handling varies). Iterate files with `while IFS= read -r line; do ...; done < file` — never `for line in $(cat file)`, which word-splits and globs.

**Make scripts sourceable.** Wrap execution in a `main` function and call it from a sourceable guard at the bottom: `[[ "${BASH_SOURCE[0]}" == "$0" ]] && main "$@"`. Sourcing the file then loads the functions for testing with `bats` or `shunit2` without running `main`. A flat top-level script cannot be tested.

**Scope variables locally.** Function-scoped variables get `local`. Global variables leak across function calls and produce cross-call state bugs that are nearly impossible to track down later. Top-level configuration goes at the top as `readonly` constants — readers should not hunt for magic values, and `readonly` makes accidental reassignment a hard error.

**Treat I/O as a contract.** Primary data goes to stdout; logs, errors, and prompts go to stderr. Define a `die` (or `error`) helper that prints to stderr and exits non-zero, and use it instead of bare `exit 1`. Errors without messages are useless in CI logs. Exit codes communicate intent to callers — `0` for success, non-zero for failure, with a documented meaning per code if more than two are used.

**Validate inputs early; fail before damage.** Use `${var:?message}` to assert a required input is set; `${var:-default}` for optional inputs. Validate arguments before performing any destructive work. For deletes, overwrites, and irreversible network calls, gate the destructive branch on a `--dry-run` or confirmation flag and *actually consult it* before executing.

**Set up cleanup before you create temp state.** Use `mktemp` (never `/tmp/foo_$$` or other predictable names — they invite races and symlink attacks). Register cleanup with `trap 'rm -rf "$tmpdir"' EXIT INT TERM` immediately after `mktemp`, so the cleanup runs on any exit path including signals.

**Verify required commands exist up front.** `command -v <cmd> >/dev/null || die "missing: <cmd>"` for every external dependency at the top of `main`. Failing fast with an actionable message beats failing mid-run with a cryptic shell error. Avoid GNU-specific flags (`sed -i`, `grep -P`, `readlink -f`, `date -d`, `stat -c`) unless the script declares the dependency — they silently differ between Linux and macOS/BSD.

**Hold the safety posture.** Never `eval` input you do not fully control. Pass `--` before untrusted arguments to commands that take options (`rm`, `grep`, `mv`, `cp`). Ensure variables passed to `rm -rf` are quoted *and* validated non-empty — `rm -rf $var` with an empty `$var` is one typo away from catastrophe. Do not pass secrets as command-line arguments — argv is visible to other users via `ps`; use environment variables or files instead.

**Name intent into the code.** `snake_case` lowercase for local and script variables; `UPPERCASE` for exported env vars and constants. Function and variable names state what they represent specifically enough that a reader can predict behavior without diving into the body. Single-letter names belong to short loop counters, not module scope.

**Keep functions small and single-purpose.** A function does one coherent thing at one level of abstraction. `main()` reads as a sequence of named operations — fetch, transform, validate, write — not a wall of inline pipelines. When a function name needs conjunctions (`parse_and_validate`), it is two functions pretending to be one.

**Document intent at the top.** A header comment at the top names the script's purpose, its usage signature, and any non-obvious dependencies. Comments inside the body explain *why* a non-obvious choice was made, not what the code does — code shows what; comments earn their place when they capture a constraint, a workaround, or a hidden invariant.

## Patterns That Work

These are the positive shapes durable Bash scripts tend to take. Each corresponds to a failure mode the audit rubric catches.

**Strict mode over silent failure.** `set -euo pipefail` plus explicit checks where strict mode misses.

**Quoted expansions over implicit splitting.** Every `$var` is a `"$var"` unless splitting is the point.

**`[[ ]]` over `[ ]`** in conditionals; `$()` over backticks; `printf` over `echo`; `${var}` braces when adjacent to text.

**`while IFS= read -r` over `for in $(cat)`.** Filename-safe iteration.

**`mktemp` over hand-built temp paths.** Race-free, attack-resistant.

**`trap` over hope.** Cleanup that actually runs on every exit path.

**`local` over global leakage.** Function-scoped state stays scoped.

**`readonly` constants over magic values.** Readers see configuration at the top.

**`main "$@"` + sourceable guard over flat top-level flow.** Testable, structured, single entry point.

**`die`-to-stderr over bare `exit 1`.** Errors with messages, on the right stream.

**`command -v` preflight over mid-run failure.** Fail fast on missing dependencies.

**Bash builtins over forking in hot loops.** `${var##*/}` over `basename`; parameter expansion over `sed` for simple string ops.

## Safety

Bash scripts run with the invoker's privileges and reach the filesystem, the network, and arbitrary subprocesses. The safety rules are non-negotiable.

- **No `eval` on untrusted input.** Shell injection, full stop.
- **`mktemp` for temporary paths; pair with `trap ... EXIT`.** No `$$` or other predictable names.
- **Validate inputs before destructive work.** A `--dry-run` flag for anything that deletes or overwrites is cheap insurance. Never `rm -rf $var` unquoted or unvalidated.
- **No secrets in argv.** Environment variables or files; `ps` shows command lines to other users.
- **Pass `--` before untrusted arguments** to option-parsing commands.
- **Verify `cd` succeeded** before doing anything destructive. A failed `cd` followed by `rm -rf *` has destroyed real systems.
- **No GNU-only flags** (`sed -i`, `grep -P`, `readlink -f`) without declaring the dependency — they silently differ on macOS/BSD.

`eval`, `mktemp`/`trap` pairing, hardcoded `/tmp/` literals, `cd` without exit, GNU-flag detection, and unquoted-variable expansion are audited deterministically (mostly via ShellCheck). The remaining rules rely on author judgment — they live in the audit rubric and code review.

## Review and Decay

Bash scripts rot. The platform `bash` moves (especially across macOS-Homebrew and Linux versions), the external CLI tools change flags, the `find`/`xargs`/`grep` flavors diverge between distributions. Retire a script when its automation is no longer invoked, when its logic has migrated into a real tool, or when its exit contract can no longer be trusted. **Convert to a real language when the script grows past a few hundred lines, acquires data structures Bash cannot express, or accumulates control flow Bash cannot debug** — `primitive-routing.md` covers the shell-vs-Python decision. A neglected script is worse than a missing one — callers trust the exit code they have stopped reading.

---

**Diagnostic when a script misbehaves.** First check the prologue: shebang, `set -euo pipefail`, header comment. Then check the contract: data to stdout, errors to stderr, non-zero exit on every failure path, `die`-helper-with-message instead of bare `exit`. Then check the quoting: ShellCheck against the file should produce zero findings. If prologue, contract, and quoting are all clean, check the structure: is logic split into small functions with `main()` as the orchestrator, or is one big top-level pipeline carrying the script? Most pathologies live in one of those four places.
