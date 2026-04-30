---
name: check-bash-script
description: >
  Audits a Bash 4.0+ script against ~26 deterministic checks (shebang,
  `set -euo pipefail`, header comment, main + sourceable guard,
  shellcheck rule set SC2086 / SC2046 / SC2068 / SC2154 / SC2155 /
  SC2006 / SC2010 / SC2013 / SC2038 / SC2164 / SC2002 / SC2294, shfmt
  format compliance, eval / GNU-flag / `/tmp/` literal flagging,
  secret patterns, line count) plus seven judgment dimensions.
  Use when the user wants to "audit a bash script", "check this bash
  script", "review my bash script", "lint a bash script", "is this
  bash script safe", "what's wrong with my shell script", or "run
  shellcheck on this". Not for POSIX `sh` portability — refused at
  scope. Not for Python scripts — route to `/build:check-python-script`.
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/bash-script-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check Bash Script

Audit a Bash 4.0+ script for structural soundness, safety, idiom
discipline, and adherence to the project's Bash conventions. The
rubric — what makes a script load-bearing, the anatomy template, the
patterns that work — lives in
[bash-script-best-practices.md](../../_shared/references/bash-script-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — seven
shell scripts run per target and emit fixed-format findings, leaning
hard on `shellcheck` and `shfmt` for the heavy lifting. **Tier-2** is
a single locked-rubric LLM call per target evaluating all seven
[audit dimensions](references/audit-dimensions.md) at once;
dimensions that don't apply return PASS silently. **Tier-3** is
cross-entity collision detection — when the scope holds multiple
scripts in the same directory, check for duplicated logic the
maintainer could consolidate.

Read-only by default. The opt-in repair loop applies fixes only after
per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Entity Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `.sh` file (or extensionless executable)** —
  audit that file.
- **Directory path** — walk the directory, audit every `.sh` at the
  top level and every extensionless file with a bash shebang. Do not
  recurse into subdirectories — Bash scripts are top-level by
  convention, and recursion pulls in helpers / libraries / vendored
  shell that the audit does not model.
- **Empty** — refuse and explain: this skill operates on a target,
  not a configuration.

Confirm the scope aloud before proceeding (one line: "Auditing
<path> (N scripts found)").

### 2. Tier-1 Deterministic Checks

Run seven scripts in sequence against each target. Each exits `0` on
clean / WARN / INFO and `1` on one or more FAIL; do not stop on any
script's FAIL exit — all seven contribute findings to the merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"   # resolved by Claude at invocation
TARGETS="$ARGUMENTS"

"$SCRIPTS/check_secrets.py"          $TARGETS   # FAIL: secret patterns — excludes from Tier-2
"$SCRIPTS/check_structure.py"        $TARGETS   # FAIL: shebang/strict-mode; WARN: header/main/main-guard/readonly/mktemp-trap
"$SCRIPTS/check_idioms.py"           $TARGETS   # WARN: [[ ]] over [ ], printf over echo, ${var} braces
"$SCRIPTS/check_safety.py"           $TARGETS   # FAIL: eval/tmp-literal; WARN: GNU flags
"$SCRIPTS/check_shellcheck.py"       $TARGETS   # FAIL: SC2086/2046/2068/2294/parse-ls; WARN: others; INFO if absent
bash "$SCRIPTS/check_shfmt.sh"       $TARGETS   # WARN: format drift; INFO if absent
bash "$SCRIPTS/check_size.sh"        $TARGETS   # WARN: line count > 300 or line length > 100
```

The scripts live next to `SKILL.md` under `scripts/` and are
executable. Claude resolves `${SKILL_DIR}` from the skill's own
directory at invocation time — hooks use `$CLAUDE_PLUGIN_ROOT`, but
skills do not.

**Script-to-check map** (full check list per script):

| Script | Checks |
|---|---|
| `check_secrets.py` | API keys, tokens, private URLs (toolkit convention) |
| `check_structure.py` | shebang form (bash, not `/bin/sh`); `set -euo pipefail` in prologue; header comment in first 10 lines; `main` function exists; sourceable guard `[[ "${BASH_SOURCE[0]}" == "$0" ]]`; `readonly` for top-level constants; `mktemp` paired with `trap ... EXIT` |
| `check_idioms.py` | `[[ ]]` over `[ ]` in bash files; `printf` over `echo` for non-trivial output; `${var}` braces when adjacent to text |
| `check_safety.py` | `eval` (require `# shellcheck disable=SC2294` or `# eval-justified:` comment); GNU-only flags (`sed -i`, `grep -P`, `readlink -f`, `date -d`, `stat -c`); hardcoded `/tmp/` / `/var/tmp/` path literals |
| `check_shellcheck.py` | wraps `shellcheck` for SC2086/2046/2068 (unquoted), SC2154 (referenced-but-not-assigned), SC2155 (no `local`), SC2006 (backticks), SC2010/2012/2045 (parse `ls`), SC2013/2162 (`for in $(cat)`), SC2038 (`find | xargs` no `-print0`), SC2164 (`cd` no exit), SC2002 (useless cat, WARN), SC2294 (eval array); emits INFO + exits 0 if shellcheck absent |
| `check_shfmt.sh` | wraps `shfmt -d -i 2 -ci -bn`; emits INFO + exits 0 if shfmt absent |
| `check_size.sh` | script length ≤ 300 non-blank lines; per-line length ≤ 100 chars |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing required dependency (not shellcheck / shfmt — those
are optional with graceful degradation).

**FAIL findings that exclude the file from Tier-2** (evaluation is
not useful until these are resolved):

- Any finding from `check_secrets.py` (secrets present)
- `check_structure.py` shebang FAIL (`#!/bin/sh` or other non-bash —
  the file is not in scope)
- `check_safety.py` `eval` FAIL (without justification comment)
- `check_safety.py` `/tmp/` literal FAIL
- `check_shellcheck.py` FAILs on SC2086, SC2046, SC2068, SC2294, or
  the parse-`ls` family — these are correctness bugs that bias every
  judgment dimension toward false negatives

**FAIL findings that do NOT exclude from Tier-2:** `check_structure.py`
strict-mode-missing FAIL leaves a parseable bash script that judgment
can still evaluate productively.

**WARN / INFO / HINT findings never exclude.** They surface in the
report alongside Tier-2 findings.

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together — no trigger gating. A dimension that does
not apply (e.g., D2 Input Validation on a script with no destructive
operations) returns PASS silently.

The seven dimensions:

| Dimension | What it judges |
|---|---|
| D1 Output Discipline | Data to stdout / chatter to stderr; `die` helper present and used; meaningful non-zero exit codes on every failure path |
| D2 Input Validation & Destructive-Op Safety | Inputs validated before destructive work; `${var:?}` for required, `${var:-}` for optional; `--dry-run` for deletes/overwrites; no secrets in argv; `--` before untrusted args; cron-context absolute paths when invoked from automation |
| D3 Subprocess & Tool Hygiene | `command -v` preflight for required externals; signal handling via trap when destructive ops are present; GNU-flag declarations when used |
| D4 Performance Intent | Bash builtins over forking in hot loops; parameter expansion (`${var##*/}`, `${var%.*}`) over `basename`/`dirname`/`sed` for simple string ops |
| D5 Function Design | `main()` reads as orchestrator (sequence of named operations); function bodies short and single-purpose; sourceable guard at the bottom |
| D6 Naming | snake_case for locals; UPPERCASE for env vars and exported constants; descriptive names; no builtin shadowing (`local`, `echo`, etc.) |
| D7 Commenting Intent | Header comment names purpose / usage / dependencies; inline comments explain *why* (constraints, workarounds), not *what*; TODOs carry an owner or ticket |

Feed the file contents plus any Tier-1 HINT lines (none currently
emitted; reserved for future pre-filters) into the prompt. Parse the
model's response into the fixed lint format (one finding per
dimension at most; PASS produces no finding).

### 4. Tier-3 Cross-Entity Collision

When the scope holds multiple scripts (directory walk, step 1), check
for structural duplication the maintainer could consolidate:

- Two or more scripts sharing identical or near-identical `die` /
  `usage` / `preflight` helper functions (candidate for a shared
  `_helpers.sh` sourced by each script)
- Identical or near-identical `main` argument-parsing blocks across
  scripts (the same `case "$1" in -h|--help) usage; exit 0 ;; esac`
  pattern repeated)
- Repeated `command -v` preflight blocks for the same dependency set

Report collisions as INFO findings — they are maintainer guidance,
not failures. Single-script scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN > INFO
> HINT), then by file path. Deduplicate exact-match findings at merge
time — `shellcheck` may emit the same SC code from multiple lines,
which is informative the first time and noise after.

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Summary line at top and bottom: `N fail, N warn, N info across N
scripts`. If any file was excluded from Tier-2, name it and the
exclusion-trigger finding.

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated
> finding numbers."

For each selected finding, follow the recipe in
[repair-playbook.md](references/repair-playbook.md):

1. Read the relevant section of the target file.
2. Propose a minimal specific edit — fix the finding without
   restructuring surrounding code.
3. Show the diff.
4. Write the change only on explicit user confirmation.
5. Re-run the Tier-1 script that produced the finding; confirm it
   passes.

Per-change confirmation is non-negotiable. Bulk application removes
the user's ability to review individual edits.

## Anti-Pattern Guards

1. **Running Tier-2 before Tier-1** — deterministic checks are cheap
   and authoritative; running them first avoids spending LLM calls on
   files that should have been excluded.
2. **Trigger-gating Tier-2 dimensions** — all seven dimensions run on
   every file. A dimension that doesn't apply returns PASS silently.
   Conditional dimensions produce inconsistent rubrics across runs
   and make findings non-comparable.
3. **Applying all repair fixes in one batch** — per-finding
   confirmation is required.
4. **Auditing recursively into subdirectories** — Bash scripts are
   top-level by convention; recursion pulls in libraries the rubric
   does not model. Top-level only.
5. **Skipping the re-run after a fix** — Step 5 of the repair loop
   re-runs the script that produced the finding. A fix that produces
   a new finding elsewhere is more common than it sounds.
6. **Suppressing the Missing Tools INFO** — when `shellcheck` or
   `shfmt` is absent, the INFO line is the user's signal that
   coverage is reduced. Surfacing it is the contract; hiding it
   silently under-audits.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files
  that passed the Tier-2-exclusion filter.
- All seven Tier-2 dimensions are evaluated on every non-excluded
  file. A dimension that does not apply returns PASS silently.
- Repairs require per-finding confirmation — each change writes
  individually and waits for explicit approval before the next.
- When a Tier-1 script reports missing dependencies (exit 69),
  surface the dependency name and install hint to the user.
- When `shellcheck` or `shfmt` is absent, the wrapper emits an INFO
  line naming the reduced coverage and exits 0. Other scripts
  continue.
- Won't modify files without per-change confirmation — the audit is
  read-only by default; repair fixes opt in one at a time.
- Won't audit paths outside `$ARGUMENTS` — the scope the user named
  is the only scope.
- Won't audit POSIX `sh` scripts — out of scope; the principles doc
  this skill enforces is bash-only. The `check_structure.py` shebang
  FAIL is the structural refusal.
- Recovery if a repair edit produces a worse state: the edit is a
  single file change; revert with `git checkout -- <path>` or the
  editor's undo.

## Handoff

**Receives:** Path to a single `.sh` file (or extensionless
executable with a bash shebang) or a directory holding such files at
the top level.
**Produces:** Structured findings table in the lint format
(`SEVERITY  <path> — <check>: <detail>` with a `Recommendation:`
follow-up line); optionally, targeted edits applied to the audited
script(s) after per-finding confirmation.
**Chainable to:** `/build:build-bash-script` (rebuild from scratch
after flagged repairs if the repair loop surfaces structural issues
bigger than point fixes).
