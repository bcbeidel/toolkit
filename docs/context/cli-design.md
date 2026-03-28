---
name: "CLI Design for Humans and Agents"
description: "Patterns for CLI argument conventions, output formatting, exit codes, and agent-readiness that make scripts usable by both humans and AI agents from the same codebase"
metadata:
  type: reference
  sources:
    - https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html
    - https://clig.dev/
    - https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46
    - https://www.anthropic.com/engineering/writing-tools-for-agents
  related:
    - docs/research/cli-design.md
    - docs/context/tool-design-for-llms.md
    - docs/context/convention-driven-design.md
    - docs/context/idempotency-convergent-operations.md
---

A well-designed CLI serves both humans and agents from the same codebase. The principles are complementary: POSIX argument conventions for predictability, stream separation for composability, `--json` for machine readability, simple exit codes for programmatic handling, and TTY detection for automatic adaptation. The agent-specific layer (schema introspection, idempotent operations, context-window-conscious output) extends these fundamentals rather than replacing them.

## Argument Conventions

POSIX defines the foundation: single-character options with `-` prefix, groupable when they take no arguments (`-abc`), and the `--` terminator that ends option processing. GNU extends this with long options (`--verbose`), `=` syntax for arguments (`--output=file`), and the expectation that every program supports `--help` and `--version`.

Configuration follows a strict precedence hierarchy: CLI flags override environment variables, which override config files, which override defaults. This is the 12-factor CLI consensus and matches how users expect layered configuration to behave.

## Output Formatting

Stream separation is the most important output design decision. Data goes to stdout. Diagnostics, progress, and errors go to stderr. This enables piping -- downstream programs receive only data, never noise.

The `--json` flag is the dominant pattern for machine-readable output. When active, stdout emits structured JSON while stderr remains human-readable. JSON output should be treated as a stable API contract: adding fields is safe, removing or renaming fields is a breaking change.

TTY detection enables automatic adaptation. Interactive terminals get colors and tables. Piped output drops ANSI codes and becomes plain text. The `NO_COLOR` environment variable provides an explicit override when set to any non-empty value.

## Exit Codes

Three codes cover nearly all cases:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General failure |
| 2 | Usage/argument error |

BSD's `sysexits.h` (codes 64-78) attempted finer granularity but has been deprecated by FreeBSD and was never part of POSIX. The modern recommendation: put specifics in the error message, not the exit code. Avoid codes 126-255, which are reserved by the shell for signaling execution failures and signal termination.

Error messages go to stderr, include the program name (`myctl: error: file not found`), and should be actionable -- state what went wrong and suggest what to do about it. The `--strict` pattern (promoting warnings to errors) is well-established for validation tools.

## Agent-Readiness

Agent-specific CLI design is an emerging field (2025-2026) with rapidly converging recommendations. The core requirements:

**Non-interactive operation.** Agents cannot answer prompts or navigate pagers. Provide `--yes`/`--force` for confirmation bypass and `--no-interactive` to disable stdin reads. TTY detection should suppress interactive behavior automatically.

**Deterministic output.** Same inputs produce same output format. No random element ordering, no locale-dependent formatting. JSON with sorted keys is the baseline.

**Context window protection.** A single verbose response can consume significant agent context. Support `--fields` for output selection, pagination with sensible defaults, and explicit truncation signals (`"truncated": true, "total": 1523`).

**Idempotent operations.** `ensure` instead of `create`, `apply` instead of `update`. When idempotency is not possible, return distinct exit codes for conflict states so agents can handle them programmatically.

**Schema introspection.** `mytool schema <command>` returning JSON parameter descriptions eliminates the need for agents to parse unstructured `--help` text.

**Structured errors.** Error codes (`"error_code": "image_not_found"`) are actionable. Generic messages (`"Error occurred"`) are not. Including `"suggestion"` fields with concrete next commands enables agent self-recovery.

## Key Insight

The agent-ready checklist (`--json`, `--yes`, `--quiet`, `--fields`, `--dry-run`, schema introspection, idempotent operations) benefits scripts and CI pipelines equally. Designing for agents is designing for automation.
