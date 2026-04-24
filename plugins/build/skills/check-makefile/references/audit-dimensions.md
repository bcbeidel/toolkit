---
name: Audit Dimensions — Makefiles
description: The complete check inventory for check-makefile — Tier-1 deterministic check table (~29 checks across 11 scripts) and Tier-2 judgment dimension specifications (7 dimensions, each citing its source principle). Referenced by the check-makefile workflow.
---

# Audit Dimensions

The check-makefile audit runs in three tiers. This document is the
inventory: every deterministic check Tier-1 emits, every judgment
dimension Tier-2 evaluates. Every dimension cites the source
principle it audits from
[makefile-best-practices.md](../../../_shared/references/makefile-best-practices.md).

## Tier-1 — Deterministic Checks

Eleven scripts, ~29 atomic checks. Each emits findings in the fixed
lint format. Exit codes: `0` clean / WARN / INFO; `1` on FAIL; `64`
arg error; `69` missing required dependency (`checkmake` is optional
and degrades gracefully).

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.py` | `secret` | API keys, tokens, private URLs via regex pattern list | FAIL | Don't embed secrets |
| `check_structure.py` | `shell-pin` | `SHELL := bash` (or `/bin/bash`) assignment | FAIL | Pin the shell explicitly |
| `check_structure.py` | `shellflags` | `.SHELLFLAGS` assignment contains `-e`, `-o pipefail`, `-c` (at minimum) | FAIL | Pin the shell explicitly |
| `check_structure.py` | `warn-undefined` | `MAKEFLAGS += --warn-undefined-variables` present | WARN | Enable the safety MAKEFLAGS |
| `check_structure.py` | `no-builtin-rules` | `MAKEFLAGS += --no-builtin-rules` OR a bare `.SUFFIXES:` line present | WARN | Enable the safety MAKEFLAGS |
| `check_structure.py` | `delete-on-error` | `.DELETE_ON_ERROR:` present | WARN | Enable the safety MAKEFLAGS |
| `check_structure.py` | `default-goal` | `.DEFAULT_GOAL := help` OR `help` is the first non-pattern target defined | WARN | Make help the default goal |
| `check_structure.py` | `header-comment` | Comment block in first ~5 lines names project and requirements (GNU Make ≥ 4, bash) | WARN | Document intent at the top |
| `check_phony.py` | `phony-coverage` | Every target with no real output file is declared in a `.PHONY:` prerequisite list (heuristic: exclude targets whose names contain `/`, `.`, or are variable expansions) | WARN | Declare every non-file target as `.PHONY` |
| `check_help.py` | `help-target` | A `help` target is defined | WARN | Make help the default goal |
| `check_help.py` | `help-auto` | The `help` recipe parses `##` from `$(MAKEFILE_LIST)` (not a hand-maintained echo list) | WARN | Document every public target |
| `check_help.py` | `help-desc` | Every public target (non-`_`-prefixed, `.PHONY` listed) has a `## description` suffix on its definition line | WARN | Document every public target |
| `check_indent.py` | `tab-indent` | Every recipe line starts with a real tab, not spaces | FAIL | Indent recipes with real tabs |
| `check_naming.py` | `target-name` | Public target names match `^[a-z][a-z0-9-]*$` | WARN | Name public targets as lowercase-hyphenated verbs |
| `check_naming.py` | `helper-prefix` | Internal helper targets (no `##` description) are prefixed with `_` | INFO | Prefix internal helpers with `_` |
| `check_variables.py` | `assignment-op` | Top-level assignments use `:=` / `?=` / `+=` (not bare `=` unless a `# deferred:` / `# recursive:` comment is adjacent) | WARN | Use `:=` and `?=` deliberately |
| `check_variables.py` | `top-level-shell` | No top-level `$(shell …)` expansions outside an allowlist (`git rev-parse`, `uname`, `pwd`) | WARN | Don't call expensive `$(shell …)` at parse time |
| `check_safety.py` | `unguarded-rm` | `rm -rf $(VAR)` flagged unless preceded by a non-empty guard, scoped to `$(BUILD_DIR)` / allowlisted path, or uses `--` before args | FAIL | No unguarded `rm -rf $(VAR)` |
| `check_safety.py` | `sudo` | `sudo` in a recipe | FAIL | No `sudo` in recipes |
| `check_safety.py` | `global-install` | `npm install -g`, unscoped `pip install`, `gem install` without `--user-install` | FAIL | Never mutate the user's machine |
| `check_safety.py` | `curl-pipe` | `curl \| sh` or `curl \| bash` in a recipe | FAIL | No `curl \| sh` |
| `check_safety.py` | `destructive-guard` | Targets named `deploy`, `publish`, `release`, or `prod-*` begin their recipe with a confirmation-variable guard | WARN | Guard destructive targets |
| `check_recipes.py` | `literal-make` | Bare `make` (not `$(MAKE)`) as a command token in recipe lines | WARN | Use `$(MAKE)` when recursion is needed |
| `check_recipes.py` | `at-discipline` | `@`-prefixed recipe lines begin only with `echo`, `printf`, or `:` | WARN | Don't hide commands |
| `check_recipes.py` | `or-true-guard` | `\|\| true` in a recipe line requires an adjacent explanatory comment | WARN | Don't swallow failures |
| `check_recipes.py` | `recipe-length` | Recipe line count per target ≤ 10 (soft cap; WARN above) | WARN | Keep recipes short |
| `check_checkmake.sh` | `checkmake` | Wraps `checkmake` when available; emits INFO + exits 0 when absent | WARN (tool finding) / INFO (tool missing) | (covers MIXDEPS, TIMESTAMP_EXPANDED, MAX_BODY_LENGTH, MIN_PHONY, etc.) |
| `check_size.sh` | `size` | File length exceeds 300 non-blank lines | WARN | Review and Decay (split into `*.mk`) |
| `check_size.sh` | `line-length` | Any line exceeds 120 characters | WARN | Review and Decay (readability) |

**FAIL exclusions from Tier-2.** Any `secret`, `shell-pin`,
`shellflags`, `tab-indent`, `unguarded-rm`, `sudo`,
`global-install`, or `curl-pipe` finding excludes the file from
Tier-2. Other FAILs are not currently defined; the exclusion list
stays conservative so that a partially-broken Makefile is still
worth judging.

**Missing-tool degradation.** `check_checkmake.sh` emits an INFO
(`tool-missing`) and exits 0 when `checkmake` is absent. Other
scripts continue. The Missing Tool INFO is the user's signal that
Tier-1 coverage is reduced — surfacing it is the contract.

## Tier-2 — Judgment Dimensions

One LLM call per file. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless a dimension explicitly marks otherwise.

### D1 Target Contract Integrity

**Source principles:** *Make `help` the default goal*; *Provide a
`ci` target*; *Name public targets as lowercase-hyphenated verbs.*

**Judges:** Does the public target surface fulfill the
workflow-orchestration contract for this repo? Are the canonical
verbs present where the project actually has the workflow (`test`
when tests exist, `deploy` when deploys exist, `ci` always)? Does
`ci` call the same targets CI actually runs? Are target names
consistent across related verbs (`lint` and `lint-py` vs `lint` and
`pylint`)?

**PASS conditions:** Public target list covers the repo's actual
workflows; `ci` references `lint` and `test` (or the repo's
equivalent coverage); no aspirational verbs (`deploy` declared but
empty) and no missing verbs (a test suite with no `test` target).

**Common fail signal:** `ci` target that re-invokes `pytest` and
`ruff` directly instead of calling `$(MAKE) test lint`; `deploy`
declared with a `TODO` recipe; `test` missing in a repo with a
`tests/` directory and a `pytest.ini`.

### D2 Destructive-Op Safety

**Source principles:** *Scope `clean` and guard destructive
targets*; *No unguarded `rm -rf $(VAR)`*; *Never mutate the user's
machine.*

**Judges:** Beyond the Tier-1 guard check: does the `CONFIRM=1`
pattern actually gate the destructive command, or is it a
decoration that fails open? Is `clean`'s scope tight (only
`$(BUILD_DIR)` and explicit artifacts), or does it `rm -rf`
directory trees broader than the build output? Are there
destructive side effects hidden in non-destructive-named targets
(e.g., a `fmt` target that rewrites config files in place)?

**PASS conditions:** Every destructive recipe has a confirmation
guard as the first command in the recipe (not just a declared
variable). `clean`'s scope is a fixed list or `$(BUILD_DIR)`. No
destructive side effects hidden in innocuously-named targets.

**Common fail signal:** `deploy:` that declares a `CONFIRM` variable
but never tests it; `clean: rm -rf *.pyc node_modules .venv build`
(too broad); `fmt` target that writes to `~/.gitconfig`.

### D3 Recipe Hygiene

**Source principles:** *Keep recipes short*; *Indent recipes with
real tabs*; *Don't hide commands*; *Don't swallow failures*;
*Quote variable expansions in recipes.*

**Judges:** Are recipes doing legitimate glue vs inline scripting?
Each recipe line runs in a fresh shell — are multi-step shell
operations joined with `\` continuations or moved to a `scripts/`
file? Are `$$` escapes used correctly when shell variables are
needed (vs Make variables)? Are variable expansions quoted as
`"$(VAR)"`?

**PASS conditions:** Recipes read as lists of glue commands, not
inline programs. Multi-step shell operations use `\` continuations
or live in `scripts/`. `$$` is used for shell-variable escapes.
Variable expansions are quoted where paths or user input flow in.

**Common fail signal:** A 20-line recipe that chains `cd`, `if`,
`for`, and `case` across separate physical lines (each runs in a
fresh shell — the `cd` was lost); `$foo` in a recipe that meant
`$$foo` (shell); `$(VAR)` unquoted in a path expansion.

### D4 Variable & Override Discipline

**Source principles:** *Put variables at the top; use `:=` and `?=`
deliberately*; *Pin tool invocations to project-local versions.*

**Judges:** Are user-configurable variables factored into `?=`
overrides that respect environment and CI? Are computed values
using `:=` vs `=` deliberately, with `=` annotated when used? Are
tool invocations pinned to project-local versions
(`./node_modules/.bin/eslint`, `.venv/bin/pytest`) vs relying on
`$PATH`?

**PASS conditions:** Tool variables use `?=` at the top.
Configuration comes before behavior. `:=` is the default; `=` is
rare and annotated. Tool invocations use `.venv/bin/…` or
equivalent, not bare command names that rely on `$PATH`.

**Common fail signal:** `PYTHON = python3` (bare `=` with no
explanation); `pytest` in a recipe (uses `$PATH`, not
`.venv/bin/pytest`); hardcoded `docker` image tag as `:latest`.

### D5 Incremental Correctness

**Source principles:** *Use sentinel files for expensive idempotent
setup*; *Use order-only prerequisites for directories*; *Declare
file-producing targets against their output files.*

**Judges:** Are file-producing targets declared against their
output files, not `.PHONY` names? Is `.DELETE_ON_ERROR:` present
(Tier-1 already checks; dimension weighs whether expensive failed
recipes would leave partial outputs)? Are sentinels used for
expensive idempotent setup (`.venv/.installed`, `.stamp-deps`)?
Order-only prerequisites for directories?

**PASS conditions:** File-producing targets declared by output
path, not phony name. Expensive idempotent setup uses a sentinel.
Directory creation uses order-only prerequisites (`target: |
$(BUILD_DIR)`).

**Common fail signal:** `build: $(PYTHON) -m build` declared as
`.PHONY` when it produces `dist/*.whl` (rebuild every time);
`setup: pip install -r requirements.txt` with no sentinel (reinstalls
on every invocation); `build_dir: mkdir -p build` as a regular
prerequisite (retriggers every time mtime changes).

### D6 Naming & Structure

**Source principles:** *Name public targets as lowercase-hyphenated
verbs*; *Prefix internal helpers with `_`*; *Keep recipes short.*

**Judges:** Target names verb-ish and consistent? Grouped logically
(setup → build → test → lint → run → deploy → clean)? Helpers
prefixed `_`? `.PHONY` list readable as a public-API surface?

**PASS conditions:** All public targets match `^[a-z][a-z0-9-]*$`
and are verbs (`build`, `test`, `lint-py`, not `format-the-code`).
Helpers prefixed with `_`. Targets grouped by lifecycle with section
comments. `.PHONY` list mirrors the public surface.

**Common fail signal:** `runTheTests:`, `do_stuff:`,
`format-the-python-code:`; public and helper targets interleaved
with no grouping; `.PHONY` includes 30 targets but the file has 40
public verbs.

### D7 Documentation Intent

**Source principles:** *Document intent at the top*; *Document
every public target with a `## description`.*

**Judges:** Does the header comment name the project, purpose, and
non-obvious requirements (GNU Make ≥ 4, bash)? Does every public
target have a `## description`? Do inline comments explain *why*
non-obvious choices were made (a `CONFIRM=1` gate, a `# deferred:`
annotation on a bare `=`, a sentinel-file rationale), not *what*
the recipe does?

**PASS conditions:** Header block in the first ~5 lines. `##`
description on every public target. Inline comments explain
rationale; none restate code.

**Common fail signal:** No header; `deploy:` with no `##` (visible
to humans but not `make help`); `# run tests` above `pytest` (what
restated); no explanation for a bare `VAR =` deferred assignment.

## Tier-3 — Cross-Entity Collision

### collision

**What it checks:** When the audit scope holds multiple Makefile /
`*.mk` files, look for structural drift: divergent `SHELL` /
`.SHELLFLAGS` assignments, duplicated `.PHONY` lists, or `help`
defined in more than one file.
**Severity:** INFO.
**Source principle:** *Review and Decay* — drift across included
files is the early warning that the Makefile split has outgrown
its coordination.

## Cross-Dimension Notes

**All dimensions run always.** A dimension that doesn't apply (D5
Incremental Correctness on a Makefile with only phony workflow
verbs) returns PASS silently.

**One finding per dimension maximum.** If D6 identifies four
naming issues, surface the highest-signal one with concrete detail.
Bulk findings train the user to disregard the audit.

**Severity defaults to WARN.** Tier-2 findings are judgment-level
coaching, not blocking. A dimension that surfaces a safety concern
Tier-1 missed (e.g., a destructive `$(MAKE) -C subdir clean` with a
malformed guard) can be escalated to FAIL by the judge, but the
default is WARN — Tier-1 is where blocking lives.
