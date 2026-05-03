---
name: check-python-script
description: >
  Audits a standalone Python 3 script against 22 deterministic checks
  (shebang, `__main__` guard, argparse shape, declared dependencies,
  ruff-backed AST lints, line count, secret patterns) plus nine
  judgment dimensions (output discipline, input validation, dependency
  posture, performance intent, naming, function design, module-scope
  discipline, literal intent, commenting intent). Use when the user
  wants to "audit a python script", "check my python script",
  "review this script", "lint a python script", "is this script
  safe", "what's wrong with my script", or "why is my script
  failing". Not for general-purpose shell scripts — route to
  `/build:check-bash-script`.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/python-script-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check Python Script

Audit a standalone Python 3 script for structural soundness, safety,
and adherence to the project's Python-script conventions. The rubric
— what makes a script load-bearing, the anatomy template, patterns
that work — lives in
[python-script-best-practices.md](../../_shared/references/python-script-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — six shell
scripts run per target and emit fixed-format findings. **Tier-2** is a
single locked-rubric LLM call per target evaluating all nine
[audit dimensions](references/audit-dimensions.md) at once; dimensions
that don't apply return PASS silently, so every target gets the full
pass. **Tier-3** is cross-entity collision detection — when the scope
holds multiple scripts in the same directory, check for duplicated
logic the maintainer could consolidate.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Entity Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `.py` file** — audit that file.
- **Directory path** — walk the directory, audit every `.py` at the
  top level; do not recurse into sub-packages (scripts are flat by
  definition).
- **Empty** — refuse and explain: this skill operates on a target,
  not a configuration.

Confirm the scope aloud before proceeding (one line: "Auditing
<path> (N scripts found)"). Miscounted scope is one of the most
common report-confusion signals.

### 2. Tier-1 Deterministic Checks

Run six scripts in sequence against each target. Each exits `0`
on clean / WARN / INFO and `1` on one or more FAIL; do not stop on
any script's FAIL exit — all six contribute findings to the merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"   # resolved by Claude at invocation
TARGETS="$ARGUMENTS"

bash "$SCRIPTS/check_secrets.sh"   $TARGETS   # FAIL: any secret pattern — excludes file from Tier-2
bash "$SCRIPTS/check_structure.sh" $TARGETS   # FAIL: shebang / guard-missing / guard-shape; WARN: main-returns, KeyboardInterrupt; INFO: exec bit
bash "$SCRIPTS/check_argparse.sh"  $TARGETS   # WARN: argparse-when-argv, add-argument help=, subprocess check=True
bash "$SCRIPTS/check_deps.sh"      $TARGETS   # WARN: non-stdlib import without declared-deps mechanism
bash "$SCRIPTS/check_ruff.sh"      $TARGETS   # FAIL: E722/F403/S108/S307/S602; WARN: others; INFO if ruff absent
bash "$SCRIPTS/check_size.sh"      $TARGETS   # WARN: line count over 500
```

The scripts and their helper `_ast_checks.py` live next to `SKILL.md`
under `scripts/` and are executable. Claude resolves `${SKILL_DIR}`
from the skill's own directory at invocation time — hooks use
`$CLAUDE_PLUGIN_ROOT`, but skills do not.

**Script-to-check map** (what each script covers, from
Section 5 of the ensemble synthesis):

| Script | Checks |
|---|---|
| `check_secrets.sh` | API keys, tokens, private URLs (toolkit convention) |
| `check_structure.sh` | shebang, `__main__` guard invokes `sys.exit(main())`, `main()` returns int, `except KeyboardInterrupt`, exec bit |
| `check_argparse.sh` | `argparse` imported when `sys.argv` used past `[0]`, every `add_argument` has non-empty `help=`, `subprocess.run(..., check=True)` or result inspected |
| `check_deps.sh` | declared dependencies (requirements.txt, PEP 723 block, or top-of-file comment) when non-stdlib import present |
| `check_ruff.sh` | wraps `ruff check` for D100, E722, SIM115, PLW1514, PTH, S602/S604, S307, F401, ANN, UP031/UP032, F403, S108, plus `ruff format --check`; emits INFO + exits 0 if ruff absent |
| `check_size.sh` | script length ≤ 500 non-blank lines |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing required dependency (not ruff — ruff is optional).

**FAIL findings that exclude the file from Tier-2** (evaluation is
not useful until these are resolved):

- Any finding from `check_secrets.sh` (secrets present)
- Python `SyntaxError` surfaced by any AST-parsing script
- `check_ruff.sh` FAILs on `S307` (eval/exec), `S602` (shell=True),
  `S108` (`/tmp/` literal), `E722` (bare except), `F403` (wildcard
  import)

**FAIL findings that do NOT exclude from Tier-2:** shebang malformed,
`__main__` guard missing or mis-shaped. These leave a parseable
script that Tier-2 can still evaluate productively.

**WARN / INFO / HINT findings never exclude.** They surface in the
report alongside Tier-2 findings. HINT lines (if a pre-filter is ever
added — Phase 9 of the synthesis-to-skill-pair workflow) feed into
the Tier-2 prompt as pre-evaluation context so the judge does not
rediscover the same signal; they are not themselves repair targets.

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All nine
dimensions run together — no trigger gating. A dimension that doesn't
apply (e.g., Performance intent on a script that never reads a file)
returns PASS silently.

The nine dimensions:

| Dimension | What it judges |
|---|---|
| D1 Output Discipline | Does data go to stdout and chatter to stderr; do error paths actually exit non-zero; is `logging` used for operational messages? |
| D2 Input Validation | Are inputs validated before destructive work; do deletes/overwrites gate on `--dry-run` or confirmation; are credentials externalized? |
| D3 Dependency Posture | When a third-party dep is imported, is it justified, or would stdlib suffice? |
| D4 Performance Intent | Does the script `.read()` a whole file it only iterates, or materialize lists it only iterates? |
| D5 Naming | Do names state intent; are single-letter names confined to loop counters and math? |
| D6 Function Design | Does each function do one thing at one level of abstraction; are near-identical blocks extracted to helpers? |
| D7 Module-Scope Discipline | Does module scope hold only imports, constants, defs, and the guard — no side-effecting calls or mutable state? |
| D8 Literal Intent | Do numeric/string literals carrying meaning have named-constant homes? |
| D9 Commenting Intent | Do comments explain why rather than restate what; are TODOs owned? |

Feed the file contents plus any Tier-1 HINT lines (if added later as
pre-filters) into the prompt. Parse the model's response into the
fixed lint format (one finding per dimension at most; dimensions that
PASS produce no finding).

### 4. Tier-3 Cross-Entity Collision

When the scope holds multiple scripts (directory walk, step 1), check
for structural duplication the maintainer could consolidate:

- Two or more scripts sharing the same module docstring or example
  invocation line (likely copy-paste drift)
- Identical or near-identical `get_parser()` functions across scripts
  (candidate for a shared helper module)
- Identical or near-identical error-handling patterns that should live
  in a shared `utils.py`

Report collisions as INFO findings — they are maintainer guidance,
not failures. Single-script scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN > INFO
> HINT), then by file path. Deduplicate exact-match findings at merge
time — a Python `SyntaxError` surfaces from every AST-parsing script
(structure, argparse, deps), which is expected but noisy unless
reduced to one row.

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
2. **Trigger-gating Tier-2 dimensions** — all nine dimensions run on
   every file. A dimension that doesn't apply returns PASS silently.
   Conditional dimensions produce inconsistent rubrics across runs
   and make findings non-comparable.
3. **Applying all repair fixes in one batch** — per-finding
   confirmation is required. The user loses the ability to review
   individual edits in a bulk apply.
4. **Auditing a directory recursively** — scripts are single-file by
   definition; recursing into sub-packages pulls in library code that
   the script rubric doesn't model. Top-level `.py` only.
5. **Skipping the re-run after a fix** — Step 5 of the repair loop
   re-runs the script that produced the finding. A fix that produces
   a new finding elsewhere is more common than it sounds.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files that
  passed the Tier-2-exclusion filter.
- All nine Tier-2 dimensions are evaluated on every non-excluded file.
  A dimension that does not apply returns PASS silently.
- Repairs require per-finding confirmation — each change writes
  individually and waits for explicit approval before the next.
- When a Tier-1 script reports missing dependencies (exit 69), surface
  the dependency name and install hint to the user; do not silently
  skip.
- When `ruff` is absent, `check_ruff.sh` emits an INFO line naming the
  reduced coverage and exits 0. Continue with the other scripts.
- Won't modify files without per-change confirmation — the audit is
  read-only by default; repair fixes opt in one at a time.
- Won't audit paths outside `$ARGUMENTS` — the scope the user named is
  the only scope.
- Recovery if a repair edit produces a worse state: the edit is a
  single file change; revert with `git checkout -- <path>` or the
  editor's undo.

## Handoff

**Receives:** Path to a single `.py` file or a directory holding `.py`
scripts at the top level.
**Produces:** Structured findings table in the lint format
(`SEVERITY  <path> — <check>: <detail>` with a `Recommendation:`
follow-up line); optionally, targeted edits applied to the audited
script(s) after per-finding confirmation.
**Chainable to:** `/build:build-python-script` (rebuild from scratch
after flagged repairs if the repair loop surfaces structural issues
bigger than point fixes).
