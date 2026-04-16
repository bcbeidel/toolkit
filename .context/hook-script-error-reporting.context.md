---
name: "Hook Script Error Reporting"
description: "Structured error reporting patterns for bash hook scripts using ERR and EXIT traps, and guidance on when set -x is and is not appropriate."
type: context
sources:
  - https://citizen428.net/blog/bash-error-handling-with-trap/
  - https://www.howtogeek.com/782514/how-to-use-set-and-pipefail-in-bash-scripts-on-linux/
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-shellcheck-static-analysis.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script Error Reporting

Evidence suggests `trap` with ERR and EXIT signals provides structured error context without requiring an external logging framework — and `set -x` belongs only in development, never in production hook scripts.

## ERR and EXIT Traps

The ERR signal fires whenever a command exits with a non-zero status (and `set -E` is active, so it propagates into subshells). A minimal trap pattern:

```bash
trap 'echo "Error on line ${LINENO}: ${BASH_COMMAND}" >&2' ERR
```

`${LINENO}` is the line number where the failure occurred; `${BASH_COMMAND}` is the command that failed. The `caller` builtin provides the script name as well, for hooks that source other files.

The EXIT signal fires on any termination path — including normal exit. Use it for cleanup:

```bash
trap 'rm -f "${TMPFILE:-}"' EXIT
```

Combining both traps with `set -Eeuo pipefail` gives full coverage: failures are caught, the failing location is reported to stderr, and any temporary resources are cleaned up.

## Why `set -x` Does Not Belong in Production Hooks

Evidence suggests `set -x` (print each command before execution) is a debugging aid only. In production hooks it creates two problems:

1. **Noise** — every command execution writes to stderr, flooding Claude Code's output with trace lines that obscure the meaningful error messages
2. **Leakage** — `set -x` prints variable values as they are expanded; if the hook processes sensitive fields from the JSON payload, those values appear in the trace

Use `set -x` locally during development by adding it temporarily and removing it before committing. Never ship a hook with `set -x` active.

## Takeaway

Use `trap '...' ERR` for structured error lines with line number and command, and `trap '...' EXIT` for cleanup. Direct `set -x` use to development-only debugging sessions — it must not appear in committed hook scripts.
