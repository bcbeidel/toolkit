---
name: check-shell
description: >
  Audits a general-purpose shell script against 14 curated lints grouped
  into Portability / Safety / Documentation, detects and merges findings
  from shellcheck / shfmt / checkbashisms when present, and surfaces a
  Missing Tools preamble with install hints when any are absent. Use
  when the user wants to "audit a shell script", "check this bash
  script", "review my shell script", "lint a script", or "is this
  script safe". Not for hook scripts — route to `/build:check-hook`.
argument-hint: "[script path]"
user-invocable: true
references:
  - references/external-tools.md
---

# Check Shell

Inspect a general-purpose shell script for portability, safety, and
documentation problems. Run 14 curated lints plus output from
`shellcheck` / `shfmt` / `checkbashisms` when they are installed.
Read-only — reports findings but does not modify the script.

This skill is not for Claude Code hooks — `/build:check-hook` owns that
lifecycle. Route there when the script is wired to a hook event.

**Workflow sequence:** 1. Input → 2. Tool Detection → 3. Missing Tools
Preamble → 4. Checks → 5. Report → 6. Handoff

## 1. Input

If `$ARGUMENTS` is non-empty, read the script at that path. Otherwise
ask the user for a path. Read the script's shebang line and scan its
body to detect the target shell:

| Detected marker | Inferred target |
|-----------------|-----------------|
| `#!/usr/bin/env bash` or `#!/bin/bash` + `[[ ]]` / `local` / arrays | `bash-*` |
| `declare -A`, `mapfile`, `wait -n`, `${var^^}` | `bash-4+` |
| `EPOCHSECONDS`, nameref loops, `BASH_ARGV0` | `bash-5+` |
| `#!/bin/sh` or `#!/usr/bin/env sh` and no bash-only syntax | `posix-sh` |
| setuid bit present (`stat -c %a` or `ls -l` shows `s`) | record; suppresses the `env bash` recommendation |

If the target is ambiguous, state the ambiguity in the report header
and scope conservatively (treat as `bash-3.2-portable` unless a
bash-4+ feature is already in use).

## 2. Tool Detection

Probe `PATH` for three tools. Record which are present and which are
absent.

```
command -v shellcheck     >/dev/null 2>&1
command -v shfmt          >/dev/null 2>&1
command -v checkbashisms  >/dev/null 2>&1   # only relevant when target = posix-sh
```

Invocation and output parsing details live in
[external-tools.md](references/external-tools.md).

## 3. Missing Tools Preamble

When any relevant tool is absent from `PATH`, the report's first
section is a **Missing Tools** block. Format:

```
## Missing tools

- **shellcheck** not found on PATH.
  Install: brew install shellcheck  |  apt install shellcheck  |  dnf install ShellCheck
  Coverage gap: quoting errors, deprecated syntax, SC2xxx/SC1xxx bug classes,
  command misuse. These will not be checked on this run.

- **shfmt** not found on PATH.
  ...
```

List one block per missing tool. Each block names the tool, gives
macOS + Debian + RHEL install commands, and enumerates the lint
categories that tool would have covered so the user can decide whether
to install it or accept the gap.

`check-shell` does not hard-exit when a tool is missing. It proceeds
to Checks with whichever tools are present. The fail-loud mechanism is
the visibility of the preamble at the top of the report.

## 4. Checks

Run 14 lints scoped to the detected target shell, plus output from
whichever external tools are available. Each lint entry below names
the pattern, why it is wrong, severity, and fix guidance.

### Portability

#### P1. Target-shell feature mismatch

Script uses a feature unavailable in its declared or inferred target.
Examples: `declare -A` or `mapfile` in a `bash-3.2-portable` script;
`[[ ]]` or `local` in a `posix-sh` script; `EPOCHSECONDS` in
`bash-4+`. Severity: **fail**. Fix: remove the feature or change the
target.

#### P2. `mktemp -t` or `--tmpdir` without portable fallback

GNU `mktemp` rejects `-c`, HP-UX requires it, BSD `-t` differs, and
Solaris lacks `mktemp` entirely. The only cross-platform invocation is
argumentless `mktemp` (writes to `$TMPDIR`). Severity: **warn**. Fix:
call `mktemp` with no flags, or fall back with a `command -v` probe.

#### P3. POSIX-sh target uses bash-only features

`posix-sh` target contains `[[ ]]`, `local`, `<<<` here-strings,
`$'...'`, `(( ))` arithmetic, arrays, or process substitution.
Severity: **fail**. Fix: rewrite using POSIX equivalents (`[ ]`,
function-scoped vars, pipes instead of here-strings).

### Safety

#### S1. Unquoted variable expansion

`$var` without surrounding quotes. Word-splits on `IFS`, glob-expands
on filesystem contents, and exposes the script to payload-driven
exploits. Severity: **fail**. Fix: `"${var}"` unless word-splitting is
deliberate (rare; comment when it is).

#### S2. `for f in $(ls ...)` instead of glob

Iterates a command-substituted `ls` output; breaks on filenames with
spaces, newlines, or leading dashes (BashPitfalls #1). Severity:
**fail**. Fix: `for f in *.ext` or `find ... -print0 | while IFS= read -r -d ''`.

#### S3. Clobbering redirect (`cat file | cmd > file`)

Truncates the destination before the producer finishes reading it; in
most shells the file ends up empty (BashPitfalls #13). Severity:
**fail**. Fix: use a temp file or `sponge` from moreutils.

#### S4. `while | read` pipeline variable loss

Variables set inside a `while ... read` loop fed by a pipe are lost
when the loop exits because the right-hand side runs in a subshell
(BashPitfalls #8). Severity: **warn**. Fix: use process substitution
(`while read ...; do ...; done < <(producer)`) in bash, or a named
pipe / temp file in POSIX sh.

#### S5. Unscoped `IFS=` without restore

`IFS=` changed at file scope and never restored leaks into downstream
commands. Severity: **warn**. Fix: assign `IFS` only on the line that
needs it (`IFS=, read -r a b c <<<"..."`), or save + restore in the
function.

#### S6. `find | xargs` without `-print0` / `-0`

Whitespace in filenames breaks the pipeline. Severity: **fail**. Fix:
`find ... -print0 | xargs -0 cmd`, or `find ... -exec cmd {} +`.

#### S7. `cd X; Y` without `||` guard

If `cd` fails, `Y` runs in the wrong directory (BashPitfalls #19).
Severity: **fail**. Fix: `cd X || exit 70` or `(cd X && Y)` in a
subshell.

#### S8. `[[ ]]` with `>` or `<` on numerics

`[[ $a > $b ]]` compares as strings, not numbers (BashPitfalls #7).
Severity: **fail**. Fix: `(( a > b ))` or `[ "$a" -gt "$b" ]`.

#### S9. `mktemp` before cleanup `trap`

`mktemp` creates the temp file before the `trap` is installed, so a
signal between the two leaks the file. Severity: **warn**. Fix:
install the `trap` first, then call `mktemp`.

#### S10. Function-local variable without `local`

Variables assigned inside a function leak to global scope when
`local` is omitted. Severity: **warn**. Fix: declare with `local`
(bash) or use a subshell `( ... )` (POSIX sh).

### Documentation

#### D1. Missing top-of-file header

No structured block after the shebang describing purpose, usage, exit
codes, and dependencies. Severity: **warn**. Fix: add the header per
the `build-shell` scaffold template.

#### D2. Undocumented non-zero exit code

The script calls `exit N` (N ≠ 0) for a code not listed in the
header's `Exit codes:` block. Severity: **warn**. Fix: document every
non-zero exit in the header, or use sysexits codes (64–78) consistently.

#### D3. Bare `TODO` without attribution

`TODO`, `FIXME`, or `XXX` without a parenthesized name (per the Google
Shell Style Guide: `TODO(mrmonkey): ...`). Severity: **warn**. Fix:
attribute every TODO so readers know who to ask.

#### D4. Filename / `PROGNAME` drift

`PROGNAME` hardcoded to a string that does not match `basename "$0"`
or the file's basename. Severity: **warn**. Fix: `PROGNAME="$(basename "${0}")"`.

#### D5. Unquoted heredoc in help / usage functions

`<<EOF` (unquoted) performs variable expansion inside the heredoc,
which is usually unintended for static help text and can leak shell
state. Severity: **warn**. Fix: `<<'EOF'` for literal help text.

#### D6. Error message not going to stderr

`echo "Error: ..."` without `>&2`. Errors on stdout poison pipelines
that consume the script's output. Severity: **warn**. Fix: `echo "..." >&2`
or `printf '...\n' >&2`.

## 5. Report

Present findings as a table, preceded by the Missing Tools preamble
when applicable. Summary count at the top:

```
N findings across <script path> (X fail, Y warn)

[Missing Tools preamble if any tool absent]

group         | lint | finding                                     | line
--------------+------+---------------------------------------------+-----
Portability   | P1   | `declare -A` requires bash 4+               | 42
Safety        | S1   | Unquoted $INPUT expansion                   | 57
Safety        | S7   | `cd "$WORKDIR"; do_work` missing `||`       | 61
Documentation | D1   | Missing top-of-file header                  | -
```

When `shellcheck`, `shfmt`, or `checkbashisms` were run, append their
output as a separate section below the 14-lint table (one section per
tool), preserving the tool's native output format so the user can
correlate with upstream documentation.

If zero findings: "Script looks clean (against the 14 lints and the
available external tools)."

## 6. Handoff

Offer the follow-up:

> "Findings suggest a rewrite may be cheaper than remediation — want
> to run `/build:build-shell` to scaffold a fresh version?"

Only suggest this when the severity mix is heavy on `fail`-level
structural issues; for a handful of `warn` findings, the user should
fix in place.

## Anti-Pattern Guards

1. **Hard-failing on a missing external tool** — a missing
   `shellcheck` should produce a Missing Tools block, not an error
   exit. The 14 FX lints run independently of tool availability.
2. **Silent coverage-gap reporting** — the Missing Tools block must be
   prominent (top of report, named tools, install commands, coverage
   gap description). A one-liner note at the end fails the fail-fast
   contract.
3. **Modifying the script** — this skill is read-only. Report only;
   do not apply fixes.
4. **Ignoring the target-shell declaration** — running bash-only lints
   against a `posix-sh` script produces false negatives. Scope every
   lint to the detected or declared target.

## Key Instructions

- Read-only: report findings only; do not write, edit, or reformat
  the script under audit.
- Always run all 14 FX lints, even when every external tool is
  available — the FX lints catch things shellcheck does not (filename
  drift, undocumented exits, `mktemp`-before-`trap`, bare TODO).
- The Missing Tools preamble is part of the contract. If a relevant
  tool is absent, naming it loudly with a platform-specific install
  command is the fail-fast mechanism.
- Severity classification is fixed per the lint catalog above —
  preserve `fail` at `fail` even when the script is small.
- Won't audit Claude Code hook scripts — route to `/build:check-hook`,
  which handles hook-specific checks (matcher casing, Stop hook loop
  risk, jq field paths on `tool_input`).
- Won't modify the script — chain to `/build:build-shell` when a
  rewrite is cheaper than remediation, or leave the user to apply
  fixes in place.

## Handoff

**Receives:** path to a shell script (from `$ARGUMENTS` or elicited).
**Produces:** a findings table with the Missing Tools preamble when
applicable; read-only — no files modified.
**Chainable to:** `/build:build-shell` (when findings suggest rewrite
is cheaper than remediation).
