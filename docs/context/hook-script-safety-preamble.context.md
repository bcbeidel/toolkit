---
name: "Hook Script Safety Preamble"
description: "The set -Eeuo pipefail preamble is the canonical safety standard for bash hook scripts, with mandatory guard patterns for commands that legitimately exit non-zero."
type: context
sources:
  - https://sipb.mit.edu/doc/safe-shell/
  - https://citizen428.net/blog/bash-error-handling-with-trap/
  - https://bertvv.github.io/cheat-sheets/Bash.html
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script Safety Preamble

Every hook script must open with `set -Eeuo pipefail`. This is the canonical safety preamble confirmed by convergent evidence from MIT SIPB, citizen428, and the Bash best practices cheat sheet.

## What Each Flag Does

Each flag has a distinct, non-overlapping role:

- **`-e`** — exits immediately when any command returns a non-zero status, preventing silent continuation after failures
- **`-E`** — propagates `ERR` traps into subshells and functions; without this, a failed command inside a function bypasses the top-level trap
- **`-u`** — treats any reference to an unset variable as a fatal error, catching typos in variable names before they cause silent misbehavior
- **`-o pipefail`** — surfaces failures from intermediate pipeline stages; without it, `false | true` exits 0 and the failure is invisible

Together these flags convert silent failures — the dominant failure mode of shell scripts — into explicit exits with non-zero status codes.

## The Mandatory Companion: `|| true`

`set -e` does not distinguish between failure and a legitimate non-zero exit. Several common patterns used in detection hooks exit non-zero by design:

- `grep` exits 1 when a pattern is not found (normal POSIX behavior)
- `test`/`[` exits 1 when a condition is false
- `diff` exits 1 when files differ

Without guards, these trip `-e` and abort the hook prematurely. The fix is explicit: append `|| true` or `|| :` to any command whose non-zero exit is expected and should not terminate the script.

```bash
set -Eeuo pipefail

# grep exits 1 when no match — guard it
grep -q "pattern" file.txt || true

# Or use assignment to suppress exit
if grep -q "pattern" file.txt; then
  echo "found"
fi
```

The `if`-statement form is the cleanest: `-e` does not fire for commands evaluated inside `if`, `while`, or `until` conditions.

## Takeaway

Place `set -Eeuo pipefail` as the first non-comment, non-shebang line in every hook script. Audit every `grep`, `diff`, and conditional command for whether a non-zero exit is legitimate behavior — if it is, guard it with `|| true` or wrap it in an `if` condition. Omitting either the preamble or the guards produces brittle hooks.
