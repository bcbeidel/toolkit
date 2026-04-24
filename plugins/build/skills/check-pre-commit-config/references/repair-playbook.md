---
name: Repair Playbook — Pre-Commit Config
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-pre-commit-config opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-pre-commit-config. Every Tier-1
finding type and every Tier-2 dimension has a recipe. Apply one at a
time, with explicit user confirmation, re-running the producing
check after each fix.

## Format

Each recipe carries five fields:
- **Signal** — the finding string or dimension name that triggers it
- **CHANGE** — what to modify, in one sentence
- **FROM** — the non-compliant pattern
- **TO** — the compliant replacement
- **REASON** — tied to the source principle

---

## Tier-1 — `check_yaml_shape.py`

### Signal: `config-missing — .pre-commit-config.yaml not found at repo root` *(FAIL)*

**CHANGE** Run `/build:build-pre-commit-config` to scaffold a fresh
config. This recipe intentionally does not stub an empty file —
scaffolding needs intake.

**REASON** An empty or hand-stubbed config obscures the real decision
about which hooks belong in this repo.

### Signal: `yaml-parse — .pre-commit-config.yaml fails YAML parse` *(FAIL)*

**CHANGE** Fix the YAML syntax error named by the parser. Common
culprits: mixed tabs and spaces, unquoted values starting with `*`
/ `&` / `!`, unbalanced brackets.

**REASON** An unparseable config means `pre-commit` runs nothing;
every commit silently passes the hook stage.

### Signal: `repos-key — top-level \`repos:\` key missing or empty` *(FAIL)*

**CHANGE** Add a `repos:` list at the top level; populate with at
least the `pre-commit-hooks` baseline.

**FROM**
```yaml
minimum_pre_commit_version: "3.7.0"
```

**TO**
```yaml
minimum_pre_commit_version: "3.7.0"
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

**REASON** A config without `repos:` is structurally inert.

### Signal: `hook-shape — hook entry is not a mapping with a string \`id:\`` *(FAIL)*

**CHANGE** Reformat the hook entry as a YAML mapping; ensure `id:`
is a quoted or bare string, not a list/number.

**REASON** `pre-commit` rejects malformed hook entries; the whole
repos block may be skipped depending on version.

---

## Tier-1 — `check_rev_pinning.py`

### Signal: `floating-rev — \`rev:\` uses a floating ref (main / master / HEAD / develop / latest / stable)` *(FAIL)*

**CHANGE** Replace the floating ref with an immutable tag or a
40-char SHA. Easiest path: run `pre-commit autoupdate` to pin to
the current stable tag.

**FROM**
```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: main
```

**TO**
```yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
```

**REASON** Floating refs produce different hook versions on different
machines and at different times — the config stops being
reproducible. `pre-commit autoupdate` produces an auditable change.

### Signal: `rev-shape — \`rev:\` is neither a semver tag nor a 40-char SHA`

**CHANGE** Resolve to a stricter reference: a versioned tag (`vX.Y.Z`)
or a 40-char commit SHA from the upstream repo.

**FROM** `rev: "2024-01-15"` *(date tag — immutable but opaque)*
**TO** `rev: v4.6.0` *or* `rev: 0a0d7cb8e2d1d99f73d0d9a9ca2a3b...`

**REASON** Semver tags and 40-char SHAs communicate intent (release
boundary or exact commit) that date tags and short SHAs do not.

---

## Tier-1 — `check_hook_scope.py`

### Signal: `hook-scope — \`repo: local\` hook without \`files:\` / \`types:\` / \`types_or:\``

**CHANGE** Add a scoping directive matching the file types the hook
is meant to process.

**FROM**
```yaml
  - repo: local
    hooks:
      - id: validate-schema
        entry: scripts/hooks/validate_schema.py
```

**TO**
```yaml
  - repo: local
    hooks:
      - id: validate-schema
        entry: scripts/hooks/validate_schema.py
        files: ^schemas/.*\.json$
```

**REASON** Without a scope, the hook runs on every staged file and
its logic has to filter — hidden cost, harder to audit.

### Signal: `pass-filenames-false — \`pass_filenames: false\` without a justifying comment`

**CHANGE** Either remove `pass_filenames: false` (let the framework
pass the staged list) or add a comment naming the repo-wide
invariant that requires it.

**FROM**
```yaml
      - id: check-something
        entry: scripts/hooks/check.py
        pass_filenames: false
```

**TO**
```yaml
      - id: check-something
        entry: scripts/hooks/check.py
        pass_filenames: false   # justified: inspects cross-file consistency
```

**REASON** The default (`true`) parallelizes cleanly and scales with
diff size; `false` is exceptional and the comment forces the author
to name the exception.

---

## Tier-1 — `check_safety.py`

### Signal: `network-io — network-fetch pattern in hook entry or script` *(FAIL)*

**CHANGE** Move the dependency installation out of the hook. The
framework-managed language env (`language: python` with pinned
`language_version`) is the right place to install Python deps via
`additional_dependencies:`.

**FROM**
```yaml
      - id: custom-check
        entry: bash -c 'pip install requests && python scripts/hooks/check.py'
```

**TO**
```yaml
      - id: custom-check
        entry: scripts/hooks/check.py
        language: python
        language_version: python3.11
        additional_dependencies: [requests==2.32.3]
```

**REASON** Network I/O in a hook breaks offline commits and slows
every commit by a network round-trip. The framework caches
per-language envs — use that cache.

### Signal: `destructive-git — destructive git command in hook entry or script` *(FAIL)*

**CHANGE** Remove the destructive git call. Pre-commit is the wrong
layer for push / tag / reset / `git add` / history rewrites.

**FROM** `entry: bash -c 'ruff check --fix && git add .'`
**TO** `entry: ruff` (plus `args: [--fix]`; the framework handles
re-staging on its own when the hook modifies files)

**REASON** `git add` from inside a hook hides the fixer's changes
from the developer — the commit-visible diff no longer reflects
what they reviewed. The framework's fail-if-modified behavior is
the right signal.

### Signal: `destructive-shell — destructive shell command in hook or script` *(FAIL)*

**CHANGE** Remove the destructive call. If the script genuinely needs
a working directory, use `mktemp -d` + `trap ... EXIT` for cleanup
instead of `rm -rf`.

**REASON** Commit-time is the wrong moment to delete, destroy, or
prune. Move cleanup to CI, `pre-push`, or a dedicated maintenance
script.

### Signal: `sudo — \`sudo\` or \`su -c\` in hook or script` *(FAIL)*

**CHANGE** Remove the privilege escalation. If the check genuinely
needs elevated privileges, it does not belong at commit time — move
to a CI job that runs in a controlled environment.

**REASON** Hooks run as the developer's user. Prompting for a
password breaks workflow; silent `sudo` (passwordless) is a
privilege-escalation vector.

### Signal: `error-suppression — \`|| true\` / \`--exit-zero\` / \`set +e\` in hook or script` *(FAIL)*

**CHANGE** Remove the suppression. If the tool legitimately needs a
warning-only mode, use the tool's native warning level (most linters
support `--warn-only` or a severity config) rather than hiding the
exit code.

**FROM** `entry: bash -c 'ruff check || true'`
**TO** `entry: ruff` (with appropriate severity config in
`ruff.toml` / `pyproject.toml`)

**REASON** Silent pass-through defeats the hook's purpose; the
developer sees "hook passed" while the check found issues.

---

## Tier-1 — `check_script_strictness.sh`

### Signal: `shell-strictness — local shell script missing shebang + \`set -euo pipefail\`` *(FAIL)*

**CHANGE** Add the standard bash prologue.

**FROM**
```bash
for file in "$@"; do
  python -c "import json; json.load(open('$file'))"
done
```

**TO**
```bash
#!/usr/bin/env bash
#
# validate_schema.sh — reject files that fail JSON parse.
#
# Invoked by pre-commit; staged filenames passed as positional args.

set -euo pipefail
IFS=$'\n\t'

for file in "$@"; do
  python -c "import json; json.load(open('$file'))" \
    || { printf 'error: %s: invalid JSON\n' "$file" >&2; exit 1; }
done
```

**REASON** Strict mode turns silent failures into loud, early exits;
`IFS=$'\n\t'` prevents word-splitting surprises on filenames with
spaces.

---

## Tier-1 — `check_hygiene.py`

### Signal: `min-version — \`minimum_pre_commit_version\` missing`

**CHANGE** Add `minimum_pre_commit_version` matching the version CI
tests.

**FROM** *(config starts with `repos:`)*
**TO**
```yaml
minimum_pre_commit_version: "3.7.0"

repos:
  ...
```

**REASON** Incompatible runner versions produce cryptic errors;
declaring the minimum surfaces the mismatch immediately.

### Signal: `lang-version-pin — language-specific hook without \`language_version\` pin`

**CHANGE** Add `default_language_version` at the top, or pin per hook.

**FROM**
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
```

**TO**
```yaml
default_language_version:
  python: python3.11

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
```

**REASON** Without the pin, the hook runs against whatever Python is
first in `$PATH` — Python 3.9 vs 3.12 can produce different lint
outputs.

### Signal: `hook-id — hook entry missing \`id:\`` *(FAIL)*

**CHANGE** Add a kebab-case `id:` naming what the hook does.

**REASON** `pre-commit` requires an `id` for every hook; missing-id
entries are silently skipped in some framework versions.

### Signal: `local-hook-name — \`repo: local\` hook missing human-readable \`name:\``

**CHANGE** Add a `name:` that reads well in failure output.

**FROM**
```yaml
      - id: validate-schema
        entry: scripts/hooks/validate_schema.py
```

**TO**
```yaml
      - id: validate-schema
        name: validate jsonschema contract
        entry: scripts/hooks/validate_schema.py
```

**REASON** When this hook fails, the developer sees the `name:` in
the output. A missing name falls back to the `id:`, which is usually
terser than useful.

### Signal: `require-serial — file-mutating hook missing \`require_serial: true\``

**CHANGE** Add `require_serial: true` to any hook known to mutate
files.

**FROM**
```yaml
      - id: black
        args: [--safe]
```

**TO**
```yaml
      - id: black
        args: [--safe]
        require_serial: true
```

**REASON** Parallel file-mutating hooks race on shared files —
intermittent corruption that only surfaces under load.

### Signal: `builtin-duplication — local hook reimplements a built-in \`pre-commit-hooks\` check`

**CHANGE** Remove the local hook; use the upstream
`pre-commit/pre-commit-hooks` equivalent.

**FROM** A local hook implementing trailing-whitespace-stripping.
**TO** The upstream `id: trailing-whitespace` in the
`pre-commit/pre-commit-hooks` repo block.

**REASON** Local reimplementations are tech debt — they drift, miss
edge cases the upstream handles, and waste maintenance effort.

---

## Tier-2 — Judgment Dimension Recipes

Tier-2 findings are WARN severity; they're coaching. Each recipe is
a repair pattern the user applies after the judge names a specific
violation.

### D1 Reproducibility

**CHANGE** Pin `minimum_pre_commit_version`, `default_language_version`
entries, and tighten any `rev:` that is a partial tag or short SHA.

**REASON** Reproducibility is the hook system's whole premise.

### D2 Scope Discipline

**CHANGE** Add `files:` / `types:` to any unscoped local hook.
Expand `exclude:` to cover the repo's actual generated / vendored
paths. Add a justifying comment to any `pass_filenames: false`.

**REASON** Unscoped hooks pay full cost on every commit and report
pre-existing issues — both drive bypass culture.

### D3 Safety Posture

**CHANGE** Inspect local hook scripts for indirect safety issues
Tier-1 regex missed — HTTP libraries, `exec` of downloaded content,
reading non-version-controlled config.

**REASON** Commit-time is a sensitive moment; quiet safety
exceptions accumulate into real incidents.

### D4 Error Handling & Messaging

**CHANGE** Rewrite bare `exit 1` / `echo "failed"` paths to emit
actionable messages (file / line / fix). Document linter-rule
disables with in-line comments.

**FROM** `echo "failed" >&2; exit 1`
**TO** `printf 'error: %s:%d: %s (fix: %s)\n' "$file" "$lineno" "$msg" "$fix" >&2; exit 1`

**REASON** Actionable messages distinguish a working gate from a
noisy one; noisy gates get bypassed.

### D5 Performance Intent

**CHANGE** Move test runners and whole-repo type checkers out of
the commit stage into `pre-push` or CI. Add `require_serial: true`
to formatter hooks. Reorder repos so formatters run before linters.

**REASON** Slow pre-commit hooks get bypassed; formatters before
linters avoid reporting lint issues a formatter would have fixed.

### D6 Developer Experience

**CHANGE** Add a CI workflow that runs `pre-commit run --all-files`
on every PR. Add a README section documenting `pre-commit install`.
Set up a monthly `pre-commit autoupdate` — either manually on a
cadence or via a scheduled workflow.

**REASON** Local / CI divergence produces unreproducible failures;
un-bootstrapped configs are unenforced; stale pins rot.

### D7 Hook Structure

**CHANGE** Extract any `entry:` containing `&&` / `||` / `|` / `;`
/ `$(...)` into `scripts/hooks/<id>.sh`. Add `name:` to every hook.
Replace local reimplementations of built-in `pre-commit-hooks` with
the upstream originals.

**REASON** Inline shell in YAML is unreviewable and untestable;
unnamed hooks produce opaque failure output; duplicated built-ins
are pure tech debt.

---

## Tier-3 — Cross-Entity Collision

### Signal: `collision — duplicated helpers across local hook scripts`

**CHANGE** Extract the shared block into `scripts/hooks/_helpers.sh`
and `source` it from each hook script.

**FROM** `die() { ... }` and per-file iteration loop copied across
three scripts in `scripts/hooks/`.

**TO**
```bash
# scripts/hooks/_helpers.sh
die() { printf 'error: %s\n' "$*" >&2; exit 1; }

iterate_files() {
  local file
  for file in "$@"; do
    "$1_handler" "$file" || die "$1 failed on $file"
  done
}
```
sourced from each script:
```bash
source "$(dirname "${BASH_SOURCE[0]}")/_helpers.sh"
```

**REASON** Shared utilities drift when maintained in triplicate; a
single source of truth keeps hook scripts coherent.

---

## Notes

- **Per-finding confirmation** is non-negotiable. Bulk application
  removes review opportunity.
- **Re-run after each fix.** Repairs can introduce new findings
  (adding `set -euo pipefail` may surface SC2155 in local scripts
  that were latent).
- **Missing-tool INFO is not a repair target.** Install the tool:
  `brew install pre-commit shellcheck` / `pip install pre-commit`
  / `apt install shellcheck`.
