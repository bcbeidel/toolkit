---
name: check-makefile
description: >
  Audits a top-level Makefile against ~29 deterministic checks
  (strict-shell header, `.PHONY` coverage, tab-indented recipes,
  variable discipline, scoped `clean`, destructive-target
  confirmation, `@`-prefix and `|| true` discipline, secrets/size,
  `checkmake` wrap) plus seven judgment dimensions. Use when the
  user wants to "audit a makefile", "check my makefile", or "lint
  a makefile". Not for POSIX-`make`, compilation trees, or
  recursive multi-module builds.
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/makefile-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check Makefile

Audit a top-level `Makefile` for structural soundness, safety,
help/`.PHONY` coverage, variable and recipe hygiene, and adherence
to the workflow-orchestration rubric. The rubric — what makes a
Makefile load-bearing, the anatomy, the patterns that work — lives
in
[makefile-best-practices.md](../../_shared/references/makefile-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — nine
scripts run per target and emit fixed-format findings, wrapping
`checkmake` where available for additional coverage. **Tier-2** is
a single locked-rubric LLM call per target evaluating all seven
[audit dimensions](references/audit-dimensions.md) at once;
dimensions that don't apply return PASS silently. **Tier-3** is
cross-entity collision detection — when the scope holds multiple
`*.mk` files in addition to the top-level `Makefile`, check for
structural drift (duplicated `.PHONY` lists, divergent `SHELL`
pins).

Read-only by default. The opt-in repair loop applies fixes only
after per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Entity Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `Makefile` (or `*.mk` file)** — audit that file.
- **Directory path** — walk the directory, audit every `Makefile`,
  `GNUmakefile`, and `*.mk` at the top level. Do not recurse —
  recursive multi-module builds are out of scope; included `*.mk`
  files belong next to the main Makefile by convention.
- **Empty** — refuse and explain: this skill operates on a target,
  not a configuration.

Confirm the scope aloud before proceeding ("Auditing <path> (N
Makefiles found)").

### 2. Tier-1 Deterministic Checks

Run nine scripts in sequence against each target. Each exits `0` on
clean / WARN / INFO and `1` on one or more FAIL; do not stop on any
script's FAIL exit — all nine contribute findings to the merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"
TARGETS="$ARGUMENTS"

"$SCRIPTS/check_secrets.py"        "$TARGETS"   # FAIL: secret patterns — excludes from Tier-2
"$SCRIPTS/check_structure.py"      "$TARGETS"   # FAIL: SHELL/.SHELLFLAGS; WARN: MAKEFLAGS, .DEFAULT_GOAL, .DELETE_ON_ERROR, header
"$SCRIPTS/check_phony.py"          "$TARGETS"   # WARN: non-file targets missing from .PHONY
"$SCRIPTS/check_help.py"           "$TARGETS"   # WARN: missing help target, missing ## descriptions
"$SCRIPTS/check_indent.py"         "$TARGETS"   # FAIL: space-indented recipe lines
"$SCRIPTS/check_naming.py"         "$TARGETS"   # WARN: non-conforming public target names
"$SCRIPTS/check_variables.py"      "$TARGETS"   # WARN: bare = without comment, top-level $(shell …)
"$SCRIPTS/check_safety.py"         "$TARGETS"   # FAIL: sudo/global-install/pipe-to-shell/unguarded rm; WARN: unconfirmed destructive targets
"$SCRIPTS/check_recipes.py"        "$TARGETS"   # WARN: literal `make`, @ discipline, || true without comment, recipe length
bash "$SCRIPTS/check_checkmake.sh" "$TARGETS"   # INFO if checkmake absent; WARN on checkmake findings
bash "$SCRIPTS/check_size.sh"      "$TARGETS"   # WARN: file > 300 non-blank lines or lines > 120 chars
```

The scripts live next to `SKILL.md` under `scripts/` and are
executable. Claude resolves `${SKILL_DIR}` from the skill's own
directory at invocation time.

**Script-to-check map** (full check list per script):

| Script | Checks |
|---|---|
| `check_secrets.py` | API keys, tokens, private URLs (toolkit convention) |
| `check_structure.py` | `SHELL := bash`; `.SHELLFLAGS` contains `-e`, `-o pipefail`, `-c`; `MAKEFLAGS += --warn-undefined-variables`; `MAKEFLAGS += --no-builtin-rules` (or `.SUFFIXES:` present); `.DELETE_ON_ERROR:`; `.DEFAULT_GOAL := help` (or `help` is the first target); header comment in first ~5 lines naming project/requirements |
| `check_phony.py` | Every target with no real output file is declared `.PHONY` — target list parsed, `.PHONY` prerequisites collected, suspected file-producing targets excluded (heuristic: target name contains `/`, `.`, or is a variable expansion) |
| `check_help.py` | `help` target defined; recipe parses `##` from `$(MAKEFILE_LIST)`; every public target (non-`_`-prefixed) has a `## description` on its definition line |
| `check_indent.py` | Every recipe line starts with a real tab (`\t`), not spaces |
| `check_naming.py` | Public target names match `^[a-z][a-z0-9-]*$`; internal helpers prefixed with `_` (if they omit `##`) |
| `check_variables.py` | Top-level assignments use `:=` / `?=` / `+=` (not bare `=` unless accompanied by `# deferred:` / `# recursive:` comment); no top-level `$(shell …)` outside an allowlist of cheap commands (`git rev-parse`, `uname`, `pwd`) |
| `check_safety.py` | `rm -rf $(VAR)` requires a non-empty guard, a `$(BUILD_DIR)`-scoped path, or `--` before args; no `sudo`; no `npm install -g`, unscoped `pip install`, `gem install` without `--user-install`; no pipe-to-shell installers (curl/wget into sh/bash); destructive target names (`deploy`, `publish`, `release`, `prod-*`) begin their recipe with a confirmation guard |
| `check_recipes.py` | Literal `make` (not `$(MAKE)`) as a command token; `@` prefix only on `echo`, `printf`, `:`; `\|\| true` requires an adjacent explanatory comment; recipe line count per target ≤ 10 |
| `check_checkmake.sh` | Wraps `checkmake` if available; emits INFO + exits 0 when absent |
| `check_size.sh` | File length ≤ 300 non-blank lines; per-line length ≤ 120 chars |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing required dependency (not `checkmake` — it degrades
gracefully).

**FAIL findings that exclude the file from Tier-2:**

- Any finding from `check_secrets.py` (secrets present)
- `check_structure.py` `SHELL` / `.SHELLFLAGS` FAIL (file is not in
  this skill's scope until the strict-shell contract holds)
- `check_indent.py` space-indent FAIL (file does not parse as a
  valid Makefile)
- `check_safety.py` `sudo` / global-install / pipe-to-shell / unguarded
  `rm -rf` FAIL (correctness bugs that bias every judgment
  dimension toward false negatives)

**FAIL findings that do NOT exclude from Tier-2:** none currently;
the exclusion list is conservative because a partially-broken
Makefile is still worth judging.

**WARN / INFO / HINT findings never exclude.** They surface in the
report alongside Tier-2 findings.

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together — no trigger gating. A dimension that does
not apply returns PASS silently.

The seven dimensions:

| Dimension | What it judges |
|---|---|
| D1 Target Contract Integrity | Does the public target surface fulfill the workflow-orchestration contract? `build`, `test`, `lint`, `fmt`, `run`, `deploy`, `clean`, `ci`, `help` — the right subset for the repo, and named consistently? Does `ci` call the same targets CI actually runs? |
| D2 Destructive-Op Safety | Beyond the Tier-1 guard check: does the `CONFIRM=1` pattern actually gate the destructive command (not just decorate the target)? Is `clean`'s scope tight? Are there destructive side effects hiding in non-destructive-named targets? |
| D3 Recipe Hygiene | Are recipes doing legitimate glue vs inline scripting? Shell state (each line runs in a fresh shell) handled via `\` continuations or a moved-to-script? `$$` escapes used when shell variables are needed? |
| D4 Variable & Override Discipline | Are configurable variables factored into `?=` overrides? Are environment overrides anticipated? Is `:=` vs `=` used deliberately? Are tool invocations pinned to project-local versions (`./node_modules/.bin/eslint`, `.venv/bin/pytest`)? |
| D5 Incremental Correctness | Are file-producing targets declared against their output files, not `.PHONY` names? Is `.DELETE_ON_ERROR:` present? Are sentinels used for expensive idempotent setup? Order-only prerequisites for directories? |
| D6 Naming & Structure | Target names verb-ish and consistent; grouped logically (setup → build → test → lint → run → deploy → clean); helpers prefixed `_`; `.PHONY` list readable as a public-API surface? |
| D7 Documentation Intent | Header comment names purpose and requirements (GNU Make ≥ 4, bash). Every public target has a `## description`. Inline comments explain *why* non-obvious choices were made (the `CONFIRM=1` gate, a `# deferred:` annotation), not *what* the recipe does. |

Feed the file contents plus any Tier-1 HINT lines into the prompt.
Parse the model's response into the fixed lint format (one finding
per dimension at most; PASS produces no finding).

### 4. Tier-3 Cross-Entity Collision

When the scope holds multiple `Makefile` / `*.mk` files, check for
structural drift:

- Divergent `SHELL` / `.SHELLFLAGS` assignments across included
  files (the main Makefile pins bash; an included `*.mk` overrides
  to `sh`)
- Duplicated `.PHONY` lists between files (one file declares `build
  test lint` and another re-declares the same — `.PHONY` is
  additive, but duplicated declarations are a readability smell)
- `help` targets defined in more than one file (the top-level
  Makefile should own `help`)

Report collisions as INFO findings — maintainer guidance, not
failures. Single-file scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN > INFO
> HINT), then by file path. Deduplicate exact-match findings at merge
time.

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Summary line at top and bottom: `N fail, N warn, N info across N
Makefiles`. If any file was excluded from Tier-2, name it and the
exclusion-trigger finding.

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated
> finding numbers."

For each selected finding, follow the recipe in
[repair-playbook.md](references/repair-playbook.md):

1. Read the relevant section of the target file.
2. Propose a minimal specific edit.
3. Show the diff.
4. Write the change only on explicit user confirmation.
5. Re-run the Tier-1 script that produced the finding; confirm it
   passes.

Per-change confirmation is non-negotiable. Bulk application removes
the user's ability to review individual edits.

## Anti-Pattern Guards

1. **Running Tier-2 before Tier-1** — deterministic checks are cheap
   and authoritative; running them first avoids spending LLM calls
   on files that should have been excluded.
2. **Trigger-gating Tier-2 dimensions** — all seven dimensions run
   on every file. A dimension that doesn't apply returns PASS
   silently.
3. **Applying all repair fixes in one batch** — per-finding
   confirmation is required.
4. **Auditing recursively into subdirectories** — recursive
   multi-module builds are out of scope for this skill's rubric.
   Top-level and sibling `*.mk` files only.
5. **Skipping the re-run after a fix** — Step 5 of the repair loop
   re-runs the script that produced the finding; a fix that
   produces a new finding elsewhere is more common than it sounds.
6. **Suppressing the `checkmake`-missing INFO** — when `checkmake`
   is absent, the INFO line is the user's signal that coverage is
   reduced. Surfacing it is the contract.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files
  that passed the exclusion filter.
- All seven Tier-2 dimensions are evaluated on every non-excluded
  file. A dimension that does not apply returns PASS silently.
- Repairs require per-finding confirmation — each change writes
  individually and waits for explicit approval.
- When a Tier-1 script reports missing dependencies (exit 69),
  surface the dependency name and install hint.
- When `checkmake` is absent, the wrapper emits an INFO line and
  exits 0; other scripts continue.
- Won't modify files without per-change confirmation — the audit is
  read-only by default.
- Won't audit paths outside `$ARGUMENTS`.
- Won't audit POSIX-`make` Makefiles, compilation trees, or
  recursive multi-module builds — out of scope. The
  `check_structure.py` `SHELL` FAIL is the structural refusal when
  `SHELL` is not bash.
- Recovery if a repair edit produces a worse state: revert with
  `git checkout -- <path>` or the editor's undo.

## Handoff

**Receives:** Path to a single `Makefile` / `GNUmakefile` / `*.mk`
file, or a directory holding such files at the top level.

**Produces:** Structured findings table in the lint format; optionally,
targeted edits applied to the audited file(s) after per-finding
confirmation.

**Chainable to:** `/build:build-makefile` (rebuild from scratch after
flagged repairs if the repair loop surfaces structural issues bigger
than point fixes).
