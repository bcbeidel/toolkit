---
name: External Tool Integration
description: >
  How check-shell invokes shellcheck / shfmt / checkbashisms, parses
  their output, merges findings with the 14 FX lints, and formats the
  Missing Tools preamble with platform-specific install commands.
---

# External Tool Integration

`check-shell` detects three tools on `PATH`, runs whichever are
present, and merges their output into the findings report. When any
tool is absent, it emits a **Missing Tools** preamble with install
commands so the user can resolve the gap deliberately.

This reference documents the invocation, parsing, and preamble format.

## Why these three tools are a hard-dep exception

The repo's core design principle is "depend on nothing" (stdlib-only
Python, no runtime dependencies added to plugins). This reference
exists because `check-shell` deliberately lifts that principle for
three specific tools:

- `shellcheck`, `shfmt`, and `checkbashisms` are T1-cited across the
  research that motivated this skill pair (issue
  bcbeidel/toolkit#322). Every serious bash style guide recommends
  `shellcheck` as the floor for static analysis.
- `/build:build-hook`'s Safety Check already recommends `shellcheck` +
  `shfmt`. The principle was already partially lifted in the build
  plugin; this skill extends that.
- The fail-fast mechanism (Missing Tools preamble) ensures a user
  without the tools installed is never *silently* under-audited.

## Tool-by-tool

### shellcheck

Covers: quoting errors, deprecated syntax (backticks, `[` vs `[[`
specifics), SC1xxx/SC2xxx bug classes, command misuse, unreachable
code, subtle word-splitting bugs.

**Invocation:**

```
shellcheck -x -f gcc <script-path>
```

- `-x` follows `source`/`.` directives to external files.
- `-f gcc` produces `file:line:col: severity: message [SC####]`
  output that is easy to grep and merges cleanly into a tabular
  report.

**Parsing.** Each non-empty output line is a finding. Severity is
`error` / `warning` / `note` / `style` in the gcc format. Map:

| shellcheck severity | check-shell severity |
|---------------------|----------------------|
| `error`             | `fail`               |
| `warning`           | `warn`               |
| `note` / `style`    | `warn` (note in report) |

**Merging.** Append a `shellcheck` section to the report below the 14
FX-lint table, preserving each line's `SC####` code so users can look
up the upstream docs.

### shfmt

Covers: formatting consistency — indentation, case/esac spacing,
redirect spacing, function style. Catches drift against a common
style, not correctness bugs.

**Invocation:**

```
shfmt -d -i 2 -ci <script-path>
```

- `-d` produces a unified diff against the formatter's preferred
  output; exit 1 if the diff is non-empty, 0 if already clean.
- `-i 2` sets indent width to 2 (match the build-shell scaffold).
- `-ci` indents switch-cases one level.

**Parsing.** Any non-empty diff output is a finding. Treat the whole
diff as one `warn`-level finding ("formatting drift detected") and
include the diff body in the report for the user to review.

### checkbashisms

Covers: bash-specific syntax used in scripts declared as `#!/bin/sh`
or `posix-sh` target. Flags `[[ ]]`, `local`, here-strings, arrays,
process substitution, `$'...'`.

**Invocation:**

```
checkbashisms <script-path>
```

Only run this when the detected target is `posix-sh` or the shebang
is `#!/bin/sh` / `#!/usr/bin/env sh`. Running it against bash scripts
produces noise.

**Parsing.** Each `possible bashism in ...` line is a finding. Treat
as `fail`-level when the target is `posix-sh` (these break POSIX
compliance); `warn` if the target is ambiguous.

## Missing Tools preamble format

When any relevant tool is absent from `PATH`, the report's first
section is a **Missing Tools** block. Emit one entry per missing
tool, in this format:

```
## Missing tools

- **<tool>** not found on PATH.
  Install:
    macOS:  brew install <tool>
    Debian: apt install <tool>
    RHEL:   dnf install <tool>
  Coverage gap: <one-sentence enumeration of what this tool would
  have caught; see per-tool gaps below>. These will not be checked on
  this run.
```

**Platform-specific install commands.** Use these exact package names
(case-sensitive):

| Tool            | macOS (brew)          | Debian/Ubuntu (apt)    | RHEL/Fedora (dnf)         |
|-----------------|-----------------------|-------------------------|---------------------------|
| `shellcheck`    | `brew install shellcheck` | `apt install shellcheck` | `dnf install ShellCheck` (capital S on RHEL) |
| `shfmt`         | `brew install shfmt`      | `apt install shfmt`       | `dnf install shfmt` (Fedora 35+; else `go install mvdan.cc/sh/v3/cmd/shfmt@latest`) |
| `checkbashisms` | `brew install checkbashisms` | `apt install devscripts` (bundle) | `dnf install devscripts` |

**Coverage-gap copy per tool:**

- **shellcheck:** "quoting errors, deprecated syntax, SC2xxx/SC1xxx
  bug classes, and command misuse".
- **shfmt:** "formatting consistency — indentation, spacing, and
  style drift".
- **checkbashisms:** "POSIX-sh compliance — bash-only syntax that
  breaks under `dash`/`busybox sh`".

For platforms outside this table (Alpine `apk`, Arch `pacman`, Nix),
append a single line pointing to each tool's upstream install docs
rather than enumerating every distro.

## Tool detection recipe

The probe is three `command -v` calls:

```
have_shellcheck=0; have_shfmt=0; have_checkbashisms=0
command -v shellcheck    >/dev/null 2>&1 && have_shellcheck=1
command -v shfmt         >/dev/null 2>&1 && have_shfmt=1
command -v checkbashisms >/dev/null 2>&1 && have_checkbashisms=1
```

`checkbashisms` is only *relevant* when the target is `posix-sh`. For
any other target, skip the `checkbashisms` probe entirely — its
absence is not a coverage gap for a bash script, and surfacing it in
the Missing Tools preamble would be noise.

## Report ordering

```
Summary: N findings (X fail, Y warn)

## Missing tools
[zero-or-more entries per tool absent from PATH]

## Findings (14 FX lints)
[tabular findings grouped by Portability / Safety / Documentation]

## shellcheck
[raw shellcheck -f gcc output, if run]

## shfmt
[unified diff, if drift detected]

## checkbashisms
[raw checkbashisms output, if run]
```

Preserve the raw output of each external tool under its own section
rather than rewriting it — users need the native format to look up
`SC####` codes and correlate with the tool's upstream documentation.
