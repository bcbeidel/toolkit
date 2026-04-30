---
name: build-pre-commit-config
description: >
  Scaffolds a reproducible pre-commit configuration — a
  `.pre-commit-config.yaml` at the repo root (optionally with local
  shell scripts under `scripts/hooks/`) that runs formatters, linters,
  and validators against staged changes via the `pre-commit`
  framework. Pins every `rev:`, declares scope per hook, serializes
  file-mutators, and documents the bootstrap. Use when the user wants
  to "set up pre-commit", "add a pre-commit config", "scaffold
  pre-commit hooks", "add commit-time linting", "gate commits with
  checks", or "configure .pre-commit-config.yaml". Not for
  hand-rolled `.git/hooks/` scripts, not for `pre-push` /
  `commit-msg` / server-side hooks, not for CI pipelines — route to
  the appropriate primitive.
argument-hint: "[project-context]"
user-invocable: true
references:
  - ../../_shared/references/pre-commit-config-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build Pre-Commit Config

Scaffold a `.pre-commit-config.yaml` plus any accompanying local hook
scripts. The authoring rubric — anatomy template, patterns that work,
anti-patterns, safety posture — lives in
[pre-commit-config-best-practices.md](../../_shared/references/pre-commit-config-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

This skill is **`pre-commit` framework only by scope**. Hand-rolled
`.git/hooks/pre-commit` scripts, `commit-msg` / `pre-push` /
server-side hooks, and CI pipeline configuration are out of scope and
refused at the Scope Gate.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a pre-commit config is the right primitive:

- **Event-triggered Claude Code quality gate** (PreToolUse,
  SessionStart, Stop, etc.) → `/build:build-hook`. Claude Code hooks
  and git pre-commit hooks share a name but nothing else.
- **`pre-push`, `commit-msg`, or server-side git hook** → out of
  scope. The `pre-commit` framework supports `pre-push` via `stages:`,
  but this skill scaffolds `pre-commit` stage only.
- **CI pipeline configuration** (GitHub Actions, GitLab CI) → wrong
  layer. A CI step that runs `pre-commit run --all-files` is the
  right *mirror* of this config, not a replacement.
- **A single ad-hoc validation script** → `/build:build-bash-script` or
  `/build:build-python-script`. This skill produces a config that
  orchestrates hooks; a standalone script is a different unit.

Right primitive → proceed to Scope Gate.

## 2. Scope Gate

Refuse — and name the alternative — when any of these fire:

1. **`.pre-commit-config.yaml` already exists at the project root.**
   Offer to `/build:check-pre-commit-config` on the existing file
   and iterate from findings instead of scaffolding over it.
2. **Target environment cannot run Python ≥ 3.9.** The
   `pre-commit` framework is Python-based; without it, scaffold a
   different quality gate (CI-only, language-native runner, etc.).
3. **User wants hand-rolled `.git/hooks/pre-commit`.** Refuse; the
   principles doc this skill enforces is framework-only.
4. **User wants a server-side or CI-only gate.** Different primitive
   class; route to the CI config or a repo-hosting feature (branch
   protection, required status checks).

If any signal fires, state the signal, name the alternative, and stop.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse it as free-form project context
and pre-fill inferable fields. Otherwise ask, one question at a time:

**1. Repo root** — where will `.pre-commit-config.yaml` land? Usually
the project root (default); monorepo sub-trees may land elsewhere.

**2. Languages present** — which languages/file types exist in the
repo? (Python, JavaScript/TypeScript, Go, Rust, Shell, YAML, JSON,
Markdown, Terraform, Dockerfile, etc.) Drives the hook selection.

**3. Existing tooling preferences** — is the team already using
specific formatters/linters? (Black vs Ruff-format, ESLint vs
Biome, gofmt vs goimports, rustfmt, shfmt, etc.) Prefer opinionated
formatters with minimal config.

**4. Baseline hygiene hooks** — include the `pre-commit-hooks`
baseline (`trailing-whitespace`, `end-of-file-fixer`,
`check-merge-conflict`, `check-added-large-files`, `check-yaml`,
`check-json`)? Default yes; skip only if the user explicitly opts out.

**5. Custom local hooks** — does the repo need any in-repo validation
(schema validation, config consistency, license headers, secret
scanning beyond `detect-secrets`)? If yes, scaffold one or more
`scripts/hooks/*.sh|py` stubs and wire them as `repo: local` hooks.

**6. CI mirror** — is CI configured to run
`pre-commit run --all-files`? If not, offer to emit a CI-snippet
alongside the config (GitHub Actions `.github/workflows/pre-commit.yml`
template) — the mirror is explicitly out-of-scope to write, but
called out in the Test handoff.

**7. Minimum pre-commit version** — default to the version the user
tests in CI; if unknown, default to the current stable minor.

## 4. Draft

Produce three artifacts.

**Artifact 1: `.pre-commit-config.yaml`.**

One conditionalized template. Omit sections the intake rules out.

```yaml
minimum_pre_commit_version: "<from intake #7>"

default_language_version:
  python: python3.11                          # (if Python in intake #2)
  node: "20.17.0"                             # (if JS/TS in intake #2)

exclude: |                                    # vendored + generated
  (?x)^(
    node_modules/|
    dist/|
    build/|
    target/|
    \.venv/|
    vendor/|
    third_party/
  )

repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0                               # verify current tag before save
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-merge-conflict
      - id: check-added-large-files
      - id: check-yaml                        # (if YAML in intake #2)
      - id: check-json                        # (if JSON in intake #2)

  # One block per language, driven by intake #2 + #3. Example (Python):
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        name: ruff (fix + lint)
        args: [--fix]
        require_serial: true
        types_or: [python, pyi]
      - id: ruff-format
        name: ruff format
        require_serial: true
        types_or: [python, pyi]

  # Local hooks (if intake #5 named any):
  - repo: local
    hooks:
      - id: <custom-id>
        name: <human-readable name>
        entry: scripts/hooks/<custom>.sh
        language: script
        files: <regex>
        pass_filenames: true
```

Every `rev:` is a placeholder — the draft states explicitly that
the user (or the Review Gate) verifies the current stable tag before
save. Never commit `rev: main` or `HEAD`.

**Artifact 2: local hook scripts** (one per intake #5 entry).

Each script uses the toolkit's bash-script convention: shebang,
`set -euo pipefail`, safe `IFS`, header comment, operates on argv
(pre-commit passes staged filenames). Actual hook logic is a stub
the user fills in — scaffolding the *shape* is this skill's job.

```bash
#!/usr/bin/env bash
#
# <id>.sh — <one-line purpose>.
# Invoked by pre-commit; staged filenames passed as positional args.

set -euo pipefail
IFS=$'\n\t'

for file in "$@"; do
  : # TODO(<owner>): implement <id> check for "$file"
done
```

**Artifact 3: bootstrap snippet** — README lines documenting
`pre-commit install` and the one-time `pre-commit install --install-hooks`
warm-up, ready to paste.

Present all artifacts to the user before the Safety Check.

## 5. Safety Check

Review the draft against the rubric before presenting. Group:

**Reproducibility.** `minimum_pre_commit_version` set. Every `rev:`
is an immutable tag (`vX.Y.Z`) or 40-char SHA — no `main` / `master` /
`HEAD` / `latest` / `stable`. `default_language_version` pins
interpreters for language-specific hooks.

**Scope.** Every hook has `files:`, `types:`, or `types_or:` (or
inherits one from the upstream repo). Repo-wide `exclude` covers
generated / vendored directories. `pass_filenames: false` appears
only with a justifying comment.

**Safety.** No network I/O in `entry:` or referenced scripts (no
`curl`, `wget`, `pip install`, `npm install`, `apt-get`, `brew`,
`gem install`, `go get`). No `sudo` / elevated privileges. No
destructive commands (`rm -rf`, `docker system prune`,
`terraform destroy`, `git reset --hard`, `git clean -fdx`,
`git push`, `git tag`, `git rebase`, `git update-ref`).

**Error handling.** No `|| true` / `--exit-zero` / toggled `set +e`
in scripts. Shell scripts start with `#!/usr/bin/env bash` +
`set -euo pipefail` + safe `IFS`.

**File-mutator discipline.** Any hook that modifies files
(Black/Ruff-format/Prettier/gofmt/rustfmt/shfmt/clang-format/
`terraform fmt`, or any `--fix` / `--write` variant) declares
`require_serial: true`.

**Hygiene.** Every hook has an explicit `id` and a human-readable
`name`. No duplication of built-in `pre-commit-hooks`
(`trailing-whitespace`, `end-of-file-fixer`,
`check-merge-conflict`, `check-added-large-files`) across multiple
repos.

**Performance.** No full test suites (`pytest`, `go test`,
`cargo test`, `npm test`) or whole-repo type checkers
(`mypy .`, `pyright`, `tsc`) in the commit-time stage.

If any check fails, revise before presenting. The Review Gate is for
user approval, not correctness recovery.

## 6. Review Gate

Present all artifacts and wait for explicit user approval before
writing any file. If the user requests changes, revise and
re-present. Continue until explicit approval or cancellation.

## 7. Save

Write the approved files to their paths:

- `<repo-root>/.pre-commit-config.yaml`
- `<repo-root>/scripts/hooks/<id>.sh` (or `.py`) for each local hook

For shell scripts, `chmod +x` them — `pre-commit` respects the
executable bit.

Show the bootstrap snippet for the user to paste into the README.

## 8. Test

Offer the audit:

> "Run `/build:check-pre-commit-config <repo-root>` to audit the
> scaffolded config against YAML shape, `rev:` pinning, scope
> declarations, safety rules, and the judgment dimensions?"

Also offer the CI mirror (explicitly not scaffolded above):

> "Add a GitHub Actions workflow that runs
> `pre-commit run --all-files` on every PR? I can produce a
> `.github/workflows/pre-commit.yml` stub."

## Anti-Pattern Guards

1. **Scaffolding over an existing config.** Scope Gate signal #1 —
   offer the audit + repair loop instead.
2. **Using `rev: main` / `HEAD` / any floating ref.** Every `rev:`
   in the draft is a verified immutable tag or a clear placeholder
   the user must resolve before save.
3. **Inline shell complexity in `entry:`** — any hook needing `&&`,
   `||`, `|`, `;`, `$(...)` gets a `scripts/hooks/*.sh` file instead.
4. **Scaffolding test runners or whole-repo type checkers.**
   `pytest`, `go test`, `tsc`, `mypy .` belong in CI / `pre-push`,
   not here. Refuse if the user asks for them in the commit stage.
5. **Skipping the Review Gate.** Write to disk only after explicit
   approval.

## Key Instructions

- Won't scaffold over an existing `.pre-commit-config.yaml` — Scope
  Gate signal #1 applies. Offer the audit instead.
- Won't scaffold hand-rolled `.git/hooks/pre-commit` files — out of
  scope; the principles doc is framework-only.
- Every `rev:` in the draft is either a verified current tag or a
  placeholder flagged for the user to resolve at Review Gate.
- `require_serial: true` is mandatory on any hook that modifies
  files. Do not omit it to "keep the config short."
- Every hook carries an explicit `id` and a human-readable `name`.
- Local hook scripts follow the toolkit bash-script convention
  (shebang + strict mode + safe `IFS` + header comment) —
  dogfooded via `/build:build-bash-script` when the hook logic is
  non-trivial.
- Recovery if the config is scaffolded in error: `rm
  <repo-root>/.pre-commit-config.yaml` plus `rm -rf
  <repo-root>/scripts/hooks/` if scaffolded. The artifacts are
  self-contained — no `settings.json` entry, no installer state
  until the user runs `pre-commit install`.

## Handoff

**Receives:** repo root path, languages present, tooling preferences,
baseline-hooks opt-in, custom-local-hook list, CI-mirror status,
minimum pre-commit version.
**Produces:** a `.pre-commit-config.yaml`, optional
`scripts/hooks/*.sh|py` stubs, and a README bootstrap snippet.
**Chainable to:** `/build:check-pre-commit-config` (audit the
scaffolded config), `/build:build-bash-script` or
`/build:build-python-script` (when a local hook's logic is
non-trivial and deserves the bash / Python script conventions).
