---
name: Audit Dimensions — Pre-Commit Config
description: The complete check inventory for check-pre-commit-config — Tier-1 deterministic check table (~15 checks across 6 scripts) and Tier-2 judgment dimension specifications (7 dimensions, each citing its source principle). Referenced by the check-pre-commit-config workflow.
---

# Audit Dimensions

The check-pre-commit-config audit runs in three tiers. This document
is the inventory: every deterministic check Tier-1 emits, every
judgment dimension Tier-2 evaluates. Every dimension cites the source
principle it audits from
[pre-commit-config-best-practices.md](../../../_shared/references/pre-commit-config-best-practices.md).

## Tier-1 — Deterministic Checks

Six scripts, ~15 atomic checks. Each script emits findings in the
fixed lint format (`SEVERITY  <path> — <check>: <detail>` +
`Recommendation:`). Exit codes: `0` clean / WARN / INFO; `1` FAIL;
`64` arg error; `69` missing required dependency.

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_yaml_shape.py` | `config-missing` | `.pre-commit-config.yaml` exists at the expected path | FAIL | Framework & Structure |
| `check_yaml_shape.py` | `yaml-parse` | Config parses as valid YAML | FAIL | Framework & Structure |
| `check_yaml_shape.py` | `repos-key` | Top-level `repos:` key is present and is a non-empty list | FAIL | Framework & Structure |
| `check_yaml_shape.py` | `hook-shape` | Every hook entry is a mapping with a string `id:` | FAIL | Framework & Structure |
| `check_rev_pinning.py` | `floating-rev` | No `rev:` is `main`, `master`, `HEAD`, `develop`, `latest`, or `stable` | FAIL | Immutable `rev:` pins |
| `check_rev_pinning.py` | `rev-shape` | Every non-`local` `rev:` matches semver-tag or 40-char SHA shape | WARN | Immutable `rev:` pins |
| `check_hook_scope.py` | `hook-scope` | Every `repo: local` hook declares `files:` / `types:` / `types_or:` | WARN | Hooks scoped to changed files |
| `check_hook_scope.py` | `pass-filenames-false` | `pass_filenames: false` appears only with a `# justified:` comment adjacent | WARN | Default to `pass_filenames: true` |
| `check_safety.py` | `network-io` | No `curl` / `wget` / `pip install` / `npm install` / `apt-get` / `brew` / `gem install` / `go get` in `entry:` or referenced script contents | FAIL | No network I/O |
| `check_safety.py` | `destructive-git` | No `git push` / `git commit` / `git reset --hard` / `git clean -fdx` / `git rebase` / `git tag` / `git update-ref` / `git add` in hook entries or scripts | FAIL | Do not rewrite history / mutate refs / auto-`git add` |
| `check_safety.py` | `destructive-shell` | No `rm -rf` / `docker system prune` / `terraform destroy` in hook entries or scripts | FAIL | No destructive shell commands |
| `check_safety.py` | `sudo` | No `sudo` / `su -c` in hook entries or scripts | FAIL | No elevated privileges |
| `check_safety.py` | `error-suppression` | No `|| true` / `--exit-zero` / toggled `set +e` in hook entries or scripts | FAIL | Exit non-zero on failure |
| `check_script_strictness.sh` | `shell-strictness` | Every referenced local shell script has a bash shebang and `set -euo pipefail` in the first ~20 non-comment lines | FAIL | Shell hooks must start with strict mode |
| `check_hygiene.py` | `min-version` | `minimum_pre_commit_version` is set at top level | WARN | `minimum_pre_commit_version` matches tested version |
| `check_hygiene.py` | `lang-version-pin` | Language-specific hooks pin `language_version` (or `default_language_version` covers them) | WARN | Pin `language_version` |
| `check_hygiene.py` | `hook-id` | Every hook has an explicit non-empty `id:` | FAIL | Every hook has explicit `id` |
| `check_hygiene.py` | `local-hook-name` | Every `repo: local` hook has a non-empty human-readable `name:` | WARN | Every hook has human-readable `name` |
| `check_hygiene.py` | `require-serial` | File-mutating hooks (heuristic: id or args match Black, Prettier, gofmt, rustfmt, Ruff+`--fix`, ESLint+`--fix`, shfmt, clang-format, `terraform fmt`) declare `require_serial: true` | WARN | File-mutating hooks declare `require_serial: true` |
| `check_hygiene.py` | `builtin-duplication` | No local hook reimplements a built-in `pre-commit-hooks` check (trailing-whitespace, end-of-file-fixer, check-merge-conflict, check-added-large-files) | WARN | No duplication of built-in `pre-commit-hooks` |

**FAIL exclusions from Tier-2.** Any `config-missing`, `yaml-parse`,
`repos-key`, `hook-shape`, `network-io`, `destructive-git`,
`destructive-shell`, `sudo`, or `error-suppression` finding excludes
the config from Tier-2. Other FAILs (`floating-rev`,
`shell-strictness`, `hook-id`) leave a parseable config that
judgment can evaluate.

**Missing-tool degradation.** `check_script_strictness.sh` degrades
gracefully when `shellcheck` is absent (emits INFO `tool-missing`,
exits 0). `check_hygiene.py`'s require-serial heuristic is conservative
— ambiguous cases surface as INFO, not WARN.

## Tier-2 — Judgment Dimensions

One LLM call per config. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless the judge escalates for a safety concern.

### D1 Reproducibility

**Source principles:** *Framework over hand-rolled*; *Immutable `rev:`
pins*; *Pin `language_version`.*

**Judges:** Does `minimum_pre_commit_version` match the version the
team tests in CI? Are all `rev:` shapes strict (tag-like or 40-char
SHA), not date-strings or commit-SHA-shortened-to-7? Are
`default_language_version` pins present and matched to CI?

**PASS conditions:** `minimum_pre_commit_version` set; every non-`local`
`rev:` is a semver tag or a 40-char SHA; `default_language_version`
covers every language-specific hook.

**Common fail signal:** `rev: v4` (partial tag — not immutable
across minor releases), `rev: 1234abc` (7-char SHA — not immutable
across history rewrites), no `language_version` on a Python hook.

### D2 Scope Discipline

**Source principles:** *Hooks scoped to changed files*; *Default to
`pass_filenames: true`*; *Exclude generated and vendored directories.*

**Judges:** Does every hook scope its work via `files:` / `types:` /
`types_or:`? Does the repo-wide `exclude` cover the generated /
vendored paths this repo actually has? Is `pass_filenames: false`
used only for genuine repo-wide invariants with a justification?

**PASS conditions:** Every local hook has a scoping directive;
exclude regex includes the vendored directories present in the repo;
any `pass_filenames: false` carries a comment explaining why
repo-wide scanning is required.

**Common fail signal:** A local hook with no `files:` / `types:`
(runs on every staged file regardless of relevance);
`pass_filenames: false` without justification (the tool is probably
framework-correct to run per-file).

### D3 Safety Posture

**Source principles:** *No network I/O*; *No elevated privileges*;
*Do not mutate files outside the staged set / auto-`git add` /
rewrite history*; *No destructive shell commands*; *Leave
`--no-verify` working.*

**Judges:** Beyond the regex-caught patterns in Tier-1, does the
config hide safety issues in more subtle ways — a script that
`exec`s a downloaded binary, an `entry:` that references a remote
URL, a Python hook that imports `requests` and calls out? Does the
config try to defeat `--no-verify` (unlikely but worth naming)?

**PASS conditions:** Tier-1 safety checks pass; no indirect safety
bypass (remote `exec`, HTTP libraries, `--no-verify`-defeating
workarounds) detected in local scripts.

**Common fail signal:** A Python hook script that imports `requests`
and posts to a URL ("telemetry"); a shell script that sources a
file from `~/.config` (which isn't under version control).

### D4 Error Handling & Messaging

**Source principles:** *Shell hooks must start with strict mode*;
*Failure messages must be actionable*; *Exit non-zero on failure.*

**Judges:** Do local scripts emit actionable failure messages (file
+ line + fix), or do they emit bare `echo "failed"`? Do linter-rule
disables in hook args carry rationale comments? Do shell scripts
use `set -Eeuo pipefail` plus a safe `IFS`?

**PASS conditions:** Every error branch in local scripts prints
file / line / fix to stderr; linter-disable args (`--ignore E501`,
`--no-strict`) are either absent or paired with a comment; shell
scripts strict-mode-clean.

**Common fail signal:** A local script that `exit 1`s with no
message on mismatch; `ruff --ignore=E501,W291,E402` with no comment
explaining why those rules are off for this codebase.

### D5 Performance Intent

**Source principles:** *Target runtime under ~2–5s*; *Do not run
full test suites / whole-repo type checkers*; *File-mutating hooks
declare `require_serial: true`*; *Run formatters before linters.*

**Judges:** Are there hooks in this config that are well-known-slow
at commit time? Is any hook running a test runner or a whole-repo
type checker? Are file-mutators serialized? Are formatters ordered
before linters so linters see formatted code?

**PASS conditions:** No `pytest`, `go test`, `cargo test`,
`npm test`, `mypy .` (whole-repo), `pyright`, `tsc` (whole-repo) in
the commit stage; every formatter hook declares
`require_serial: true`; formatter hooks appear before linter hooks
in the repos list.

**Common fail signal:** An `id: mypy` hook with `args: [.]` (whole
repo); a `pytest` hook; Black / Ruff-format / Prettier without
`require_serial: true`; `ruff` (lint) listed before `ruff-format`.

### D6 Developer Experience

**Source principles:** *Mirror enforcement in CI*; *Document
bootstrap in README*; *Run `pre-commit autoupdate` on a regular
cadence*; *Leave `--no-verify` working.*

**Judges:** Is there evidence of a CI mirror (a
`.github/workflows/*.yml` running `pre-commit run --all-files`, or a
`pre-commit.ci` badge / config)? Is bootstrap documented somewhere
discoverable (README, `make setup`, `husky install`)? Is there
recent evidence of `pre-commit autoupdate` (dated update commit or a
scheduled workflow)?

**PASS conditions:** CI mirror exists; bootstrap documented; an
autoupdate cadence is visible in the repo.

**Common fail signal:** Config exists, no CI mirror (local / CI
divergence risk); no README mention of `pre-commit install` (new
contributor won't know to enable it); `rev:` pins untouched for 18+
months.

### D7 Hook Structure

**Source principles:** *Explicit `id` + human-readable `name`*;
*Custom hook logic in `scripts/hooks/`*; *No duplication of built-in
`pre-commit-hooks`.*

**Judges:** Does every hook have both `id` and human-readable
`name` (especially `repo: local` hooks)? Are local hooks backed by
versioned scripts under `scripts/hooks/` rather than inline shell
complexity in `entry:`? Does the config avoid reimplementing
built-in `pre-commit-hooks` (trailing-whitespace, EOF-fixer,
merge-conflict, large-file)?

**PASS conditions:** Every hook has `id` + `name`; local hook
`entry:` values are either a single command or a script file path
(no `&&` / `||` / `|` / `;` / `$(...)`); no local hook duplicates a
built-in.

**Common fail signal:** A local hook with `entry: 'bash -c "find ...
| xargs grep -q foo && echo ok"'` (inline complexity);
`id: check-trailing-whitespace` as a local hook when the upstream
`trailing-whitespace` is already available.

## Tier-3 — Cross-Entity Collision

### collision

**What it checks:** When multiple local hook scripts live under
`scripts/hooks/`, look for duplicated helpers (`die`, `usage`, input
validation, per-file iteration loops) the maintainer could
consolidate into `scripts/hooks/_helpers.sh`.
**Severity:** INFO.
**Source principle:** *Patterns That Work* (custom logic in
`scripts/hooks/`) + maintenance — duplicated logic in hook scripts
drifts over time.

## Cross-Dimension Notes

**All dimensions run always.** A dimension that doesn't apply (D6
Developer Experience in a brand-new repo with no CI yet) returns
PASS silently.

**One finding per dimension maximum.** If D2 identifies four hooks
missing scope, surface the highest-signal one with concrete detail.

**Severity defaults to WARN.** Tier-2 findings are coaching, not
blocking. A dimension that surfaces a safety concern Tier-1 missed
(e.g., a local Python hook that makes HTTP calls via a library
Tier-1's regex didn't catch) escalates to FAIL by the judge, but
the default is WARN — Tier-1 is where blocking lives.
