---
name: Pre-Commit Config Best Practices
description: Authoring guide for `.pre-commit-config.yaml` and the local scripts it invokes — what makes a pre-commit configuration load-bearing, how to shape the file, positive patterns, and the safety and maintenance posture. Referenced by build-pre-commit-config and check-pre-commit-config.
---

# Pre-Commit Config Best Practices

## What a Good Pre-Commit Config Does

A pre-commit config is a reproducible quality gate for staged changes
— a `.pre-commit-config.yaml` at the repo root (plus any local shell
scripts it invokes under `scripts/hooks/`) that runs formatters,
linters, and validators via the `pre-commit` framework. It fires on
`git commit`, operates only on the staged set, and either passes
silently or fails with a message the developer can act on in under a
minute.

The value proposition is narrow. A pre-commit config earns its place
when the checks are *fast*, *local*, *deterministic*, and *actionable*
— properties a full CI run cannot provide because CI arrives too late
to prevent the broken commit from entering history. When checks are
slow, repo-wide, or flaky, developers bypass them with
`git commit --no-verify` and the gate provides zero protection.

The scope here is **the `pre-commit` framework** (`pre-commit-config.yaml`
plus referenced local scripts). Hand-rolled `.git/hooks/pre-commit`
files, `commit-msg` / `pre-push` / server-side hooks, and CI pipeline
configuration are out of scope — each has a different contract and a
different audience.

## Anatomy

```yaml
# .pre-commit-config.yaml
minimum_pre_commit_version: "3.7.0"           # match what CI tests

default_language_version:
  python: python3.11                          # pin interpreter, don't rely on default

exclude: |                                    # repo-wide ignores: generated + vendored
  (?x)^(
    node_modules/|
    dist/|
    build/|
    \.venv/|
    vendor/
  )

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0                               # immutable tag (or 40-char SHA); never `main`
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        name: ruff (fix + lint)               # human-readable name for failure output
        args: [--fix]
        require_serial: true                  # file-mutating: no parallel races
        types_or: [python, pyi]

  - repo: local                               # in-repo hook → versioned script
    hooks:
      - id: validate-schema
        name: validate jsonschema contract
        entry: scripts/hooks/validate_schema.py
        language: python
        language_version: python3.11
        files: ^schemas/.*\.json$
        pass_filenames: true
```

Local hook script (`scripts/hooks/validate_schema.py` or `.sh`):

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# validate_schema.sh — reject schema files that fail jsonschema validation.
# Invoked per-file by pre-commit (filenames passed as args).

for file in "$@"; do
  python -c "import json; json.load(open('$file'))" \
    || { printf 'error: %s: invalid JSON\n' "$file" >&2; exit 1; }
done
```

Load-bearing pieces: `minimum_pre_commit_version` set (so incompatible
runners fail loudly), `default_language_version` pinned (no reliance
on `$PATH` Python), repo-wide `exclude` for generated / vendored
paths, every `rev:` an immutable tag or 40-char SHA, every hook with
an explicit `id` and human-readable `name`, file-mutating hooks
declaring `require_serial: true`, custom logic in
`scripts/hooks/*.sh|py` (not inline YAML), and `files:` / `types:`
scoping on every local hook.

## Patterns That Work

**Framework over hand-rolled `.git/hooks/` scripts.** `pre-commit`
handles staging isolation, per-language environments, and caching
correctly; hand-rolled scripts almost never do.

**Single `.pre-commit-config.yaml` at the repo root.** The discoverable
source of truth for what runs on commit. Monorepos with genuinely
independent sub-trees are the only defensible exception.

**Immutable `rev:` pins (tag or 40-char SHA) over floating refs.**
Floating `main` / `master` / `HEAD` / `latest` / `stable` break
reproducibility across machines and over time — the same config on
two developers' machines can run two different hook versions.

**Custom hook logic in `scripts/hooks/` over inline YAML.** Inline
shell in `entry:` is unreviewable, untestable, and hides
complexity. A hook that needs `&&`, `||`, `|`, or `$(...)` wants a
script file.

**Hooks scoped to changed files.** `pre-commit` passes the staged
file list as argv by default; declaring `files:` / `types:` /
`types_or:` per hook keeps runtime proportional to diff size and
avoids reporting pre-existing issues.

**Formatters before linters.** Linters should not report issues a
formatter would fix. Within a tier, prefer fastest-first for
fail-fast feedback.

**Explicit `id` + human-readable `name` on every hook.** Failure
output is only as clear as the hook names. `id: validate-schema`
with `name: validate jsonschema contract` reads cleanly in CI logs.

**File-mutating hooks declare `require_serial: true`.** Black,
Prettier, gofmt, rustfmt, Ruff+`--fix`, ESLint+`--fix`, shfmt,
clang-format, `terraform fmt` — all race when parallelized.

**Staged content only, via framework argv or `git diff --cached`.**
Never `find` / `git ls-files` / raw working-tree reads — those
escape the staging isolation the framework provides.

**Default to `pass_filenames: true`.** Only use `false` for genuinely
repo-wide invariants, and justify the exception with a comment.

**Mirror enforcement in CI.** Run `pre-commit run --all-files` in
CI (or use `pre-commit.ci`). Divergence between local and CI produces
unreproducible failures.

**Bootstrap documented in README** (minimally the command
`pre-commit install`) or automated via `make setup` / `husky install`
/ setup script. Discoverability is the difference between enforced
and ignored.

**`pre-commit autoupdate` on a regular cadence.** Monthly, committed
as a dedicated reviewable PR. Stale pins rot.

**Actionable failure messages.** Name file, line, and fix:
`app/x.py:42: unused import 'os' (run 'ruff check --fix')` is
actionable; `lint failed` is useless.

**Shell hook scripts start with `#!/usr/bin/env bash` + `set -euo pipefail` + safe `IFS`.** Default shell semantics hide failures;
strict mode surfaces them. (Relax `pipefail` only if a POSIX
`/bin/sh` target is forced.)

## Anti-Patterns

- **Floating `rev:` refs** (`main`, `master`, `HEAD`, `latest`,
  `stable`) — fails silently, differently, on every machine.
- **Network I/O inside a hook** (`curl`, `wget`, `pip install`,
  `npm install`, `apt-get`, `brew`, `gem install`, `go get`) —
  breaks offline work, slows every commit, introduces flakiness.
- **`sudo` / password prompts / elevated privileges** — hooks must
  run as the normal developer user.
- **Mutating files outside the staged set, auto-`git add`, or
  rewriting history from a hook** — surprising side effects destroy
  developer trust. The framework already re-runs after fixers modify
  files; manual `git add` hides that signal.
- **Destructive shell commands** (`rm -rf`, `docker system prune`,
  `terraform destroy`, `git reset --hard`, `git clean -fdx`,
  `git push`, `git tag`, `git rebase`) — commit-time is the wrong
  layer for those operations.
- **Full test suites or whole-repo type checking in pre-commit**
  (`pytest`, `go test`, `cargo test`, `npm test`, `mypy .`,
  `pyright`, `tsc`) — too slow, too noisy; move to `pre-push` or
  CI. Slow hooks get bypassed, which is worse than no hook.
- **Silent error swallowing** (`|| true`, `--exit-zero`, toggled
  `set +e`, `exit 0` in error branches) — defeats the hook's
  purpose.
- **Duplicating built-in `pre-commit-hooks`** — reinventing
  `trailing-whitespace`, `end-of-file-fixer`, `check-merge-conflict`,
  `check-added-large-files` is pure tech debt.
- **Complex inline shell in `entry:`** (`&&`, `||`, `|`, `;`,
  `$(...)`, backticks, >80 chars) — unreviewable, untestable.
- **Inventing bypass** (trying to defeat `--no-verify`, using git
  hooks the framework doesn't know about) — the escape hatch is a
  feature; enforce via CI and server-side checks instead.
- **Un-serialized file-mutating hooks** — races on shared files.
- **Unpinned `language_version`** for language-specific hooks —
  Python 3.9 vs 3.12 on two machines produces two different
  lint outputs.

## Safety & Maintenance

Pre-commit configs decay in three recognizable ways. Spot them
early.

**Version drift.** Pinned `rev:` values age. Monthly
`pre-commit autoupdate` committed as a standalone reviewable PR keeps
them current without letting unbounded change land alongside feature
work.

**Bypass culture.** Once developers habitually append `--no-verify`,
the hooks provide zero value. Chronic bypass is a design signal —
fix the hook (scope better, speed it up, reduce false positives) or
remove it. Preserving `--no-verify` as a working escape hatch is
intentional; trying to defeat it is the wrong response.

**Local / CI divergence.** If CI runs hooks that local doesn't (or
vice versa), failures become unreproducible. Mirror local enforcement
in CI with `pre-commit run --all-files` so both layers evaluate the
same rubric.

**Retire hooks that no longer earn their place.** A hook whose rule
now lives in CI, a formatter superseded by a more-opinionated
successor, a validator whose schema moved elsewhere — remove it.
Stale hooks are advisory pressure without signal.

---

**Diagnostic when pre-commit misbehaves.** First check
reproducibility: floating `rev:`, unpinned `language_version`, missing
`minimum_pre_commit_version`. Then check scope: every hook has
`files:` / `types:` / `types_or:`; no hook uses `pass_filenames: false`
without a justification comment. Then check safety: no network I/O,
no `sudo`, no destructive / history-mutating git commands, no
`|| true`. Then check the custom scripts: shebang + `set -euo pipefail`
+ safe `IFS`, `shellcheck` clean. Most pathologies live in one of
those four places.
