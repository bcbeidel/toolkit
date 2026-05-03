---
name: check-pre-commit-config
description: >
  Audits a `.pre-commit-config.yaml` (and referenced local hook
  scripts) against ~15 deterministic checks (YAML shape, `rev:`
  pinning, scope declarations, network-call / destructive-command /
  error-suppression patterns, shell-script strict mode, hook
  explicit-name and require-serial hygiene) plus seven judgment
  dimensions. Use when the user wants to "audit pre-commit", "check
  .pre-commit-config.yaml", "review my pre-commit hooks", "is my
  pre-commit config safe", "lint pre-commit", or "what's wrong with
  my pre-commit". Not for hand-rolled `.git/hooks/` — out of scope.
  Not for CI pipelines — route elsewhere.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path-to-repo-root-or-config-file]"
user-invocable: true
references:
  - ../../_shared/references/pre-commit-config-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check Pre-Commit Config

Audit a `.pre-commit-config.yaml` — plus the local shell/Python
scripts it invokes — for reproducibility, scope, safety, error
handling, and adherence to the `pre-commit` framework's conventions.
The rubric lives in
[pre-commit-config-best-practices.md](../../_shared/references/pre-commit-config-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — six
scripts emit fixed-format findings, leaning on YAML parsing and
targeted regex over hook entries and referenced scripts. **Tier-2**
is a single locked-rubric LLM call evaluating all seven
[audit dimensions](references/audit-dimensions.md) at once;
dimensions that don't apply return PASS silently. **Tier-3** is
cross-entity — when the scope holds multiple local hook scripts,
check for duplicated helper logic the maintainer could consolidate.

Read-only by default. The opt-in repair loop applies fixes only after
per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Entity Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Path to a `.pre-commit-config.yaml` file** — audit that file and
  any local scripts it references under `entry:`.
- **Path to a directory (repo root)** — locate `.pre-commit-config.yaml`
  at the root; if present, audit it; if absent, refuse with a
  discovery hint.
- **Empty** — refuse and explain: this skill operates on a target.

Resolve local-hook script paths relative to the repo root. Do not
walk into `node_modules` / `.venv` / `dist` / vendored directories
even when looking for referenced scripts — a script referenced by a
hook lives in the repo, not vendored code.

Confirm scope aloud: "Auditing `<path>` (config + N referenced local
scripts)."

### 2. Tier-1 Deterministic Checks

Run six scripts in sequence against the config + its referenced
local scripts. Each exits `0` on clean / WARN / INFO and `1` on FAIL;
all findings contribute to the merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"
TARGETS="$ARGUMENTS"

"$SCRIPTS/check_yaml_shape.py"      $TARGETS   # FAIL: file missing / parse error / no top-level `repos:`
"$SCRIPTS/check_rev_pinning.py"     $TARGETS   # FAIL: floating rev; WARN: non-semver / non-SHA shape
"$SCRIPTS/check_hook_scope.py"      $TARGETS   # WARN: hook without files/types; WARN: pass_filenames:false unjustified
"$SCRIPTS/check_safety.py"          $TARGETS   # FAIL: network I/O, destructive cmds, sudo, error suppression
"$SCRIPTS/check_script_strictness.sh" $TARGETS # FAIL: shell hook without shebang+strict-mode
"$SCRIPTS/check_hygiene.py"         $TARGETS   # WARN: missing `name`, missing `require_serial` on mutators, duplicate built-ins
```

Scripts live next to `SKILL.md` under `scripts/` — scaffolding them
is out of scope for this SKILL.md; see Handoff. The check half ships
with the rubric and the repair playbook; Tier-1 scripts are a
follow-on via `/build:build-python-script` and `/build:build-bash-script`.

**Script-to-check map:**

| Script | Checks |
|---|---|
| `check_yaml_shape.py` | `.pre-commit-config.yaml` exists at expected path; parses as valid YAML; top-level `repos:` key present; hook entries are well-formed mappings with `id:` |
| `check_rev_pinning.py` | Every non-`local` repo's `rev:` is either a semver-like tag (`^v?\d+\.\d+(\.\d+)?([-.].+)?$`) or a 40-char hex SHA; reject `main` / `master` / `HEAD` / `develop` / `latest` / `stable`; WARN if shape is neither semver nor 40-char SHA |
| `check_hook_scope.py` | Every `repo: local` hook declares `files:` or `types:` or `types_or:`; `pass_filenames: false` appears only with a `# justified:` comment on the same or prior line |
| `check_safety.py` | Scan `entry:` values *and* referenced local script contents for: network-fetch patterns (`curl`, `wget`, `pip install`, `npm install`, `apt-get`, `brew`, `gem install`, `go get`), destructive git (`git push`, `git commit`, `git reset --hard`, `git clean -fdx`, `git rebase`, `git tag`, `git update-ref`, `git add`), destructive shell (`rm -rf`, `docker system prune`, `terraform destroy`), `sudo` / `su -c`, error suppression (`|| true`, `--exit-zero`, `set +e`) |
| `check_script_strictness.sh` | Every referenced local shell script has a bash shebang and `set -euo pipefail` within the first ~20 non-comment lines |
| `check_hygiene.py` | `minimum_pre_commit_version` present; `default_language_version` pins interpreters for language-specific hooks; every hook has an explicit `id`; every `repo: local` hook has a human-readable `name`; file-mutating hooks (by id-and-args heuristic: Black, Prettier, gofmt, rustfmt, Ruff+`--fix`, ESLint+`--fix`, shfmt, clang-format, `terraform fmt`) declare `require_serial: true`; no local hook reimplements a built-in `pre-commit-hooks` check |

**Exit-code contract:** `0` clean / WARN / INFO; `1` FAIL; `64`
argument error; `69` missing required dependency (e.g., a Python
YAML parser) — `shellcheck` is optional inside
`check_script_strictness.sh` and degrades gracefully.

**FAIL findings that exclude from Tier-2:**

- `check_yaml_shape.py` file-missing / parse-error / no-`repos:`
  (the audit target is unreadable)
- `check_safety.py` network I/O, destructive git / shell, `sudo`,
  or error suppression — correctness bugs that bias judgment
  toward false negatives

**FAIL findings that do NOT exclude from Tier-2:**
`check_rev_pinning.py` floating-ref FAIL leaves a parseable config
that judgment can still evaluate productively.

### 3. Tier-2 Judgment Checks

For each config file that passed the Tier-2-exclusion filter, make
one LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together. A dimension that doesn't apply returns PASS
silently.

| Dimension | What it judges |
|---|---|
| D1 Reproducibility | `minimum_pre_commit_version` matches tested version; `default_language_version` pins present; `rev:` shapes match the stricter interpretation (40-char SHA preferred when available) |
| D2 Scope Discipline | Every hook scoped to changed files via `files:` / `types:`; `pass_filenames: false` used only where genuine repo-wide invariants require it; repo-wide `exclude` covers generated + vendored paths |
| D3 Safety Posture | No network I/O / destructive commands / `sudo` / ref-mutating git / error suppression in hook entries or local scripts; `--no-verify` not defeated |
| D4 Error Handling & Messaging | Local scripts fail loudly with actionable messages (file / line / fix); no silent error swallowing; shell scripts use strict mode + safe `IFS`; linter-rule disables documented with rationale comments |
| D5 Performance Intent | No full test suites / whole-repo type checkers in the commit stage; file-mutating hooks declare `require_serial: true`; hook selection prioritizes fast incremental tools; formatters ordered before linters |
| D6 Developer Experience | Bootstrap documented (README or setup script); CI mirror present (`pre-commit run --all-files`); `--no-verify` preserved as escape hatch; `pre-commit autoupdate` cadence evidence present (recent dated update commit or scheduled workflow) |
| D7 Hook Structure | Every hook has explicit `id` + human-readable `name`; custom logic lives in `scripts/hooks/*.sh|py`, not inline YAML shell; no duplication of built-in `pre-commit-hooks` |

### 4. Tier-3 Cross-Entity Collision

When the scope holds multiple local hook scripts, check for
structural duplication:

- Two or more scripts sharing near-identical `die` / `usage` /
  argument-validation blocks (candidate for `scripts/hooks/_helpers.sh`)
- Identical per-file-iteration loops across scripts
  (`for file in "$@"; do ...; done` with the same guard pattern)

Report collisions as INFO — maintainer guidance, not failures.
Single-script scopes skip this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN >
INFO) and then by path. Deduplicate exact-match findings.

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Summary line at top and bottom: `N fail, N warn, N info across
1 config + N local scripts`. Name any files excluded from Tier-2
and the exclusion-trigger finding.

### 6. Opt-In Repair Loop

Ask:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated
> finding numbers."

For each selected finding, follow the recipe in
[repair-playbook.md](references/repair-playbook.md):

1. Read the relevant config section or script region.
2. Propose a minimal specific edit.
3. Show the diff.
4. Write only on explicit user confirmation.
5. Re-run the producing Tier-1 script; confirm it passes.

Per-change confirmation is non-negotiable.

## Anti-Pattern Guards

1. **Running Tier-2 before Tier-1** — deterministic checks are cheap
   and authoritative; Tier-2 runs second.
2. **Trigger-gating Tier-2 dimensions** — all seven run on every
   non-excluded file. Dimensions that don't apply return PASS
   silently.
3. **Batch-applying repairs** — per-finding confirmation required.
4. **Walking into vendored paths** — `node_modules`, `.venv`, `dist`,
   `vendor` contain hook scripts that aren't the audit target.
5. **Treating `--no-verify` as a bug** — bypass is a feature; flag
   attempts to *defeat* bypass, not its existence.

## Key Instructions

- Tier-1 runs first and always. Tier-2 runs only on files that
  passed the Tier-2-exclusion filter.
- All seven Tier-2 dimensions evaluate on every non-excluded target.
  Dimensions that don't apply return PASS silently.
- Repairs require per-finding confirmation.
- Won't audit hand-rolled `.git/hooks/pre-commit` files — out of
  scope; the principles doc this skill enforces is framework-only.
- Won't audit paths outside `$ARGUMENTS`.
- Won't walk into vendored directories for referenced scripts —
  scripts referenced by hooks live in the repo, not vendored code.
- Recovery if a repair edit produces a worse state: edit is a single
  file change; revert with `git checkout -- <path>` or editor undo.

## Handoff

**Receives:** path to a `.pre-commit-config.yaml` (or the repo root
holding one) plus any local scripts it references via `entry:`.
**Produces:** a structured findings table (`SEVERITY <path> —
<check>: <detail>` + `Recommendation:`); optionally, targeted edits
applied after per-finding confirmation.
**Chainable to:** `/build:build-pre-commit-config` (rescaffold from
scratch if findings are structural rather than pointwise);
`/build:build-python-script` / `/build:build-bash-script` (when a
local hook's logic outgrows its current script and deserves a
proper script convention).
