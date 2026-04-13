---
name: "Hook Script ShellCheck Static Analysis"
description: "ShellCheck is the de facto standard static analysis tool for bash scripts and a necessary but not sufficient quality gate for hook scripts."
type: context
sources:
  - https://github.com/koalaman/shellcheck
related:
  - docs/research/2026-04-13-shell-script-best-practices.research.md
  - docs/context/hook-script-safety-preamble.context.md
  - docs/context/hook-script-error-reporting.context.md
  - docs/context/hook-script-injection-prevention.context.md
  - docs/context/hook-script-json-payload-handling.context.md
  - docs/context/hook-script-testing-strategies.context.md
  - docs/context/hook-script-bash-style-conventions.context.md
---

# Hook Script ShellCheck Static Analysis

ShellCheck is the de facto standard static analysis tool for bash scripts. Passing ShellCheck is a necessary quality gate for hook scripts — but not a sufficient one. Runtime logic errors and incorrect exit code intent are invisible to static analysis.

## What ShellCheck Detects

ShellCheck operates as a linter for bash and sh scripts. It catches issues in four categories:

- **Quoting issues** — unquoted variables susceptible to word-splitting and globbing
- **Conditionals** — incorrect use of `[` vs `[[`, missing quotes in comparisons
- **Command misuse** — deprecated backtick syntax (recommends `$()`), incorrect use of built-ins
- **Beginner mistakes** — syntax errors that produce cryptic shell messages

It runs via `shellcheck yourscript`, online at shellcheck.net, in editor integrations (Vim, Emacs, VSCode), and in CI/CD pipelines. CI integration is standard practice.

## The Limitation: Static Analysis Does Not Catch Runtime Logic Errors

ShellCheck cannot detect:

- **Wrong jq path** — `jq -r '.tool_input.cmd'` when the field is `.tool_input.command` exits 0 and returns `null`
- **Wrong exit intent** — a hook that exits 0 when it should exit 2 to block the action
- **Pipe buffer overflow** — large payloads that exhaust pipe buffers in specific pipeline configurations
- **Field shape assumptions** — scripts assuming payload fields that Claude Code does not always populate

These failures are logic errors that require tests with realistic payloads to surface. ShellCheck passing is a floor, not a ceiling.

## Integration Pattern

Add ShellCheck to the hook development workflow at two points:

1. **Editor** — install an integration (e.g., the VSCode ShellCheck extension) for immediate feedback while writing
2. **CI** — run `shellcheck` on all hook scripts in CI so regressions are caught before merge

```bash
# Check a single hook
shellcheck hooks/pre-tool-use.sh

# Check all hooks in a directory
shellcheck hooks/*.sh
```

## Takeaway

Run ShellCheck on every hook script and treat its warnings as failures. Then complement it with bats-core tests using accurate payload shapes — static analysis catches what it can see; tests catch what executes.
