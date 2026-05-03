---
name: check-github-workflow
description: >
  Audits a GitHub Actions workflow YAML file (or a directory under
  `.github/workflows/`) against ~28 deterministic checks (top-level
  `name:`, permissions, timeouts, concurrency, SHA-pinning for every
  `uses:`, no `@main`/`@master`/floating refs, `pull_request_target`
  + PR checkout combo, template injection in `run:`, deprecated
  commands, secrets-in-top-env, fork-PR secret exposure, harden-runner
  first, persist-credentials, strict bash, actionlint, zizmor,
  yamllint, shellcheck on extracted `run:` content) plus seven
  judgment dimensions. Use when the user wants to "audit a github
  workflow", "check this workflow", "review my github actions", "is
  this workflow safe", "lint my workflow", or "run zizmor on this".
  Not for composite actions — different rubric.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/github-workflow-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check GitHub Workflow

Audit a GitHub Actions workflow file for structural soundness,
safety posture, pinning discipline, and adherence to the authoring
rubric. The rubric — authoring principles, patterns that work,
anti-patterns — lives in
[github-workflow-best-practices.md](../../_shared/references/github-workflow-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — a set
of wrapper scripts runs per target and emits fixed-format findings,
leaning on `actionlint`, `zizmor`, `yamllint`, and `shellcheck` for
external-tool coverage. **Tier-2** is a single locked-rubric LLM
call per file evaluating all seven
[audit dimensions](references/audit-dimensions.md) at once;
dimensions that don't apply return PASS silently. **Tier-3** is
cross-workflow collision detection — when the scope holds multiple
workflows in `.github/workflows/`, check for duplication the
maintainer could consolidate via reusable workflows or composite
actions.

Read-only by default. The opt-in repair loop applies fixes only
after per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Workflow Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `.yml` / `.yaml` file under `.github/workflows/`**
  — audit that file.
- **Directory path** — walk the directory top-level, audit every
  `.yml` / `.yaml` file. Do not recurse into `.github/actions/` —
  composite actions have a different rubric and are out of scope.
- **Empty** — refuse and explain: this skill operates on a target,
  not a configuration.

Refuse if the target is a composite action (`action.yml` with a
top-level `runs:` block instead of `jobs:`). Report the mismatch and
stop.

Confirm the scope aloud before proceeding (one line: "Auditing
<path> (N workflows found)").

### 2. Tier-1 Deterministic Checks

Run the wrapper scripts in sequence against each target. Each exits
`0` on clean / WARN / INFO and `1` on one or more FAIL; do not stop
on any script's FAIL exit — all scripts contribute findings to the
merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"   # resolved by Claude at invocation
TARGETS="$ARGUMENTS"

"$SCRIPTS/check_secrets.py"          $TARGETS   # FAIL: hardcoded secret patterns — Tier-2 exclude
"$SCRIPTS/check_structure.py"        $TARGETS   # FAIL: permissions/timeouts; WARN: names/concurrency/shell
"$SCRIPTS/check_pinning.py"          $TARGETS   # FAIL: non-SHA third-party, floating refs, docker:latest
"$SCRIPTS/check_safety.py"           $TARGETS   # FAIL: pr-target+checkout, template injection, deprecated cmds
bash "$SCRIPTS/check_actionlint.sh"  $TARGETS   # WARN: actionlint findings; INFO if absent
bash "$SCRIPTS/check_zizmor.sh"      $TARGETS   # WARN: zizmor findings; INFO if absent
bash "$SCRIPTS/check_yamllint.sh"    $TARGETS   # WARN: yamllint findings; INFO if absent
"$SCRIPTS/check_shellcheck.py"       $TARGETS   # WARN: shellcheck on extracted run: blocks; INFO if absent
"$SCRIPTS/check_size.py"             $TARGETS   # INFO: file size / run-block size flags for extraction
```

The scripts live next to `SKILL.md` under `scripts/` and are
executable. Claude resolves `${SKILL_DIR}` from the skill's own
directory at invocation time. These scripts are **out of scope for
this SKILL.md** — scaffolding them is routed to
`/build:build-python-script` / `/build:build-bash-script` via the
*Language Selection* section of `primitive-routing.md` (structured
YAML parsing and `gh api` calls favor Python; `actionlint`-/
`zizmor`-/`yamllint`-/`shfmt`-wrapper scripts favor Bash).

**Script-to-check map** (full check list in
[audit-dimensions.md](references/audit-dimensions.md)):

| Script | Checks |
|---|---|
| `check_secrets.py` | hardcoded API keys, tokens, private URLs |
| `check_structure.py` | top-level `name:`; job/step `name:`; top-level `permissions:` present and not `write-all`; every job has `timeout-minutes:`; `defaults.run.shell: bash`; concurrency group includes `github.workflow`+`github.ref`; deploy/release workflows do not set `cancel-in-progress: true`; job/step IDs kebab-case |
| `check_pinning.py` | every third-party `uses:` is 40-char SHA; first-party allowed to tag-pin with `# dependabot-managed` comment; no `@main`/`@master`/`@v*.*`; docker image references non-`latest` tag or `@sha256:` digest; release/deploy workflows pin runner |
| `check_safety.py` | `pull_request_target` + PR-ref checkout (hard FAIL); `${{ github.event.* }}`/`github.head_ref`/`inputs.*` in `run:` text; `::set-output`/`::set-env`/`::add-path`; `${{ secrets.* }}` in top-level `env:`; `pull_request` workflows referencing `secrets.*` without source gating; public-repo `pull_request` on self-hosted runner; multi-line bash `run:` starts with `set -euo pipefail`; `actions/checkout` `persist-credentials: false` unless push detected; `step-security/harden-runner` first step |
| `check_actionlint.sh` | wraps `actionlint` (native workflow schema + expressions + shellcheck integration); emits INFO + exits 0 if absent |
| `check_zizmor.sh` | wraps `zizmor` (unpinned-uses, excessive-permissions, template-injection, dangerous-triggers, self-hosted-runner); emits INFO + exits 0 if absent |
| `check_yamllint.sh` | wraps `yamllint` with default config; emits INFO + exits 0 if absent |
| `check_shellcheck.py` | extracts `run:` content, pipes to `shellcheck` (SC2086/2046/2068/2154); emits INFO + exits 0 if absent |
| `check_size.py` | file length; `run:` block length (>20 non-blank lines → flag for extraction to `.github/scripts/`) |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing required dependency (not actionlint / zizmor /
yamllint / shellcheck — those are optional with graceful degradation
via INFO emission).

**FAIL findings that exclude the file from Tier-2** (evaluation is
not useful until these are resolved):

- Any finding from `check_secrets.py` (secrets present)
- `check_safety.py` `pr-target-checkout` (workflow has a severe CVE
  shape; judgment would coach on layout while the file is exploitable)
- `check_safety.py` `template-injection` (same rationale)
- `check_pinning.py` `no-floating-ref` (`@main`/`@master` on any
  action — same rationale)
- `check_safety.py` `deprecated-cmds` (file is non-functional on
  new runners)

**FAIL findings that do NOT exclude from Tier-2:** missing top-level
`permissions:`, missing `timeout-minutes`, missing `set -euo
pipefail` — these leave a parseable workflow that judgment can
still usefully evaluate.

**WARN / INFO / HINT findings never exclude.** They surface in the
report alongside Tier-2 findings.

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together — no trigger gating. A dimension that does
not apply (e.g., D4 Runtime Safety on a workflow that has no fork-
triggerable events) returns PASS silently.

The seven dimensions:

| Dimension | What it judges |
|---|---|
| D1 Trigger Discipline | Triggers scoped with `paths`/`branches`/`types`; right trigger chosen deliberately (`pull_request` vs `pull_request_target`); `schedule` cron not at minute 0; `workflow_dispatch` inputs typed |
| D2 Permissions & Secrets Discipline | Permissions at narrowest useful scope; secrets referenced only in the step that needs them; OIDC preferred over static cloud creds; no `write-all`; `permissions: id-token: write` present iff OIDC used |
| D3 Pinning & Supply-Chain Posture | Every `uses:` SHA-pinned (or first-party tag with documented exemption + Dependabot); no mutable refs; docker images tagged or digested; Dependabot config present in repo for `github-actions` ecosystem |
| D4 Runtime Safety | `step-security/harden-runner` first step of every job; `persist-credentials: false` on checkout; user-controlled context routed through `env:`; `pull_request_target` unused or demonstrably safe |
| D5 Correctness & Error Handling | `timeout-minutes` on every job; `set -euo pipefail` in multi-line bash `run:`; `defaults.run.shell: bash`; `continue-on-error` only for commented non-blocking steps; explicit `needs:`; `always() && needs.*.result` for post-failure jobs |
| D6 Performance & Concurrency | Concurrency group for PR/push with `cancel-in-progress: true`; deploy/release no-cancel; cache keyed by lockfile hash; `setup-*` built-in caching over hand-rolled; `paths:` filters on costly jobs; `fetch-depth: 1` unless history needed |
| D7 Maintainability | Single-purpose workflow; `run:` blocks > ~20 lines extracted to scripts; shared logic in reusable workflows / composite actions; kebab-case IDs; narrow `env:` scoping; artifact `name` + `retention-days` explicit |

Feed the file contents plus any Tier-1 HINT lines into the prompt.
Parse the model's response into the fixed lint format (one finding
per dimension at most; PASS produces no finding).

### 4. Tier-3 Cross-Workflow Collision

When the scope holds multiple workflows (directory walk, step 1),
check for structural duplication the maintainer could consolidate:

- Two or more workflows inlining the same job definition (candidate
  for a reusable workflow `_<name>.yml` called via `uses:
  ./.github/workflows/_<name>.yml`)
- Identical or near-identical step sequences across workflows
  (candidate for a composite action under `.github/actions/<name>/`)
- Duplicated `permissions:` + `runs-on:` + `setup-*` preambles
  across jobs in separate workflows (same composite-action candidate)
- Matrix definitions that duplicate each other across workflows

Report collisions as INFO findings — they are maintainer guidance,
not failures. Single-workflow scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN >
INFO > HINT), then by file path. Deduplicate exact-match findings
at merge time.

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Summary line at top and bottom: `N fail, N warn, N info across N
workflows`. If any file was excluded from Tier-2, name it and the
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

1. **Running Tier-2 before Tier-1.** Deterministic checks are cheap
   and authoritative; running them first avoids spending LLM calls
   on files that should have been excluded.
2. **Trigger-gating Tier-2 dimensions.** All seven dimensions run on
   every file. A dimension that doesn't apply returns PASS silently.
   Conditional dimensions produce inconsistent rubrics across runs.
3. **Applying all repair fixes in one batch.** Per-finding
   confirmation is required.
4. **Auditing recursively into `.github/actions/`.** Composite
   actions have a different rubric. Walk `.github/workflows/`
   top-level only.
5. **Skipping the re-run after a fix.** Step 5 of the repair loop
   re-runs the script that produced the finding. A fix that
   produces a new finding elsewhere is common.
6. **Suppressing the Missing Tools INFO.** When `actionlint`,
   `zizmor`, `yamllint`, or `shellcheck` is absent, the INFO line
   is the user's signal that coverage is reduced. Surfacing it is
   the contract; hiding it silently under-audits.
7. **Treating `pr-target-checkout` as a non-blocker.** This finding
   excludes the file from Tier-2 because the file is exploitable as
   written — judgment-level coaching is the wrong coverage for a
   CVE shape.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files
  that passed the Tier-2-exclusion filter.
- All seven Tier-2 dimensions are evaluated on every non-excluded
  file. A dimension that does not apply returns PASS silently.
- Repairs require per-finding confirmation — each change writes
  individually and waits for explicit approval before the next.
- When a Tier-1 script reports missing required dependencies (exit
  69), surface the dependency name and install hint to the user.
- When `actionlint`, `zizmor`, `yamllint`, or `shellcheck` is
  absent, the wrapper emits an INFO line naming the reduced
  coverage and exits 0. Other scripts continue.
- Won't modify files without per-change confirmation — the audit is
  read-only by default; repair fixes opt in one at a time.
- Won't audit paths outside `$ARGUMENTS` — the scope the user named
  is the only scope.
- Won't audit composite actions (`action.yml`) — different rubric,
  different primitive.
- Won't recurse into `.github/actions/` — composite actions are
  out of scope; top-level `.github/workflows/` only.
- Recovery if a repair edit produces a worse state: the edit is a
  single file change; revert with `git checkout -- <path>` or the
  editor's undo.

## Handoff

**Receives:** Path to a single `.yml` / `.yaml` file under
`.github/workflows/`, or the `.github/workflows/` directory itself.

**Produces:** Structured findings table in the lint format
(`SEVERITY  <path> — <check>: <detail>` with a `Recommendation:`
follow-up line); optionally, targeted edits applied to the audited
workflow(s) after per-finding confirmation.

**Chainable to:** `/build:build-github-workflow` (rebuild from
scratch after flagged repairs if the repair loop surfaces structural
issues bigger than point fixes); `/build:build-bash-script` for
extracting a long `run:` block to `.github/scripts/`.
