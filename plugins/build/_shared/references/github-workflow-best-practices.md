---
name: GitHub Workflow Best Practices
description: Authoring guide for GitHub Actions workflows — what a good workflow does, the canonical anatomy, the patterns that work, and the safety posture under 2025–2026 GitHub + OpenSSF guidance post-tj-actions. Referenced by build-github-workflow and check-github-workflow.
---

# GitHub Workflow Best Practices

## What a Good Workflow Does

A GitHub Actions workflow is a YAML file under `.github/workflows/` that automates a single concern — CI, release, deploy-staging, scheduled maintenance — triggered by repository events, run on a GitHub-hosted or self-hosted runner, and holding an explicit permissions, timeout, concurrency, and pinning posture. It is *executed code* that carries the trust boundary of the repository it lives in; the authoring rubric is shaped by that fact.

The scope here is **a single workflow file**. Composite actions (`action.yml`), organization rulesets, Dependabot configs, and GitHub Apps are separate primitives with different rubrics. A workflow earns its place when the work is genuinely repository-scoped automation, the triggers are real repository events, and the alternative (a cron on an internal CI server, a shell script in a Makefile) would lose integration with the GitHub Checks UI, protected-branch enforcement, or environment-gated deploys.

## Anatomy

```yaml
# .github/workflows/ci.yml
name: CI                                                        # Workflow-level name — shows in Checks UI
on:                                                             # Triggers scoped with paths/branches/types
  push:
    branches: [main]
    paths: ['src/**', '.github/workflows/ci.yml']
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

permissions:                                                    # Top-level least-priv; elevate per-job
  contents: read

concurrency:                                                    # Cancel in-progress for PR/push (NOT deploy)
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

defaults:                                                       # Avoid OS-dependent shell surprises
  run:
    shell: bash

jobs:
  test:
    name: Unit tests
    runs-on: ubuntu-latest                                      # `-latest` ok for CI; pin for deploy/release
    timeout-minutes: 20                                         # Default is 360 — silently burns compute
    steps:
      - name: Harden runner                                     # First step every job — post-tj-actions
        uses: step-security/harden-runner@0634a2670c59f64b4a01f0f96f84700a4088b9f0  # v2.12.0
        with:
          egress-policy: audit

      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683      # v4.2.2
        with:
          persist-credentials: false                            # Default leaves a usable token on disk
          fetch-depth: 1

      - name: Set up Python
        uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065  # v5.6.0
        with:
          python-version: '3.12'
          cache: pip                                            # Built-in caching over hand-rolled actions/cache

      - name: Install
        run: |
          set -euo pipefail                                     # Strict bash in every multi-line run
          pip install -e ".[test]"

      - name: Test
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}      # User-controlled context in env, NOT run
        run: |
          set -euo pipefail
          echo "Running against: $PR_TITLE"                     # Safe — no ${{ }} in run body
          pytest -v
```

Load-bearing pieces: top-level `name`, trigger filters (`paths`, `branches`, `types`), `permissions: contents: read` at workflow level, `concurrency` group with `cancel-in-progress: true` for PR/push (omit or flip for deploy), `defaults.run.shell: bash`, per-job `name` and `timeout-minutes`, `harden-runner` as the first step, SHA-pinned `uses:` (including first-party), `persist-credentials: false` on checkout, `set -euo pipefail` in every multi-line `run:`, user-controlled context routed through `env:` not interpolated into `run:`.

## Authoring Principles

**Name every workflow, job, and multi-line step.** The Checks UI, required-check configuration, and log readability all depend on names. A job called `test` with a step called `Run` is invisible in a list of 40 checks.

**Single-purpose per file.** `ci.yml`, `release.yml`, `deploy-prod.yml`. Omnibus workflows are harder to reason about, harder to cancel, and harder to gate — a single `everything.yml` defeats every tool built on workflow identity (concurrency, required checks, environment protection).

**Extract shared logic.** Reusable workflows (`on: workflow_call`) for whole-job reuse; composite actions (`.github/actions/<name>/action.yml`) for step sequences. Don't copy-paste job bodies across files — they drift, and silent drift between CI and release is a class of bug in its own right.

**Extract long `run:` blocks into checked-in scripts.** Past ~20 non-blank lines, YAML is the wrong place for code. Scripts under `.github/scripts/` (or `scripts/`) can be shellchecked, tested with `bats`/`shunit2`, and reviewed in diffs that don't wrap at 80 columns inside a string literal.

**Scope triggers narrowly.** `paths`, `branches`, `types`. Running the backend test suite on a docs-only change is wasted minutes; triggering on every tag push when you meant `v*` is an accidental release. `pull_request` defaults to `opened`/`synchronize`/`reopened` — narrow the `types` when you want something different, don't rely on memory.

**Declare top-level `permissions:` with least privilege.** Start from `contents: read` and elevate per-job. The default `GITHUB_TOKEN` scope is broader than almost any workflow needs — and that scope is inherited by every action called from the job, including compromised third-party actions. This is the #1 defense if an upstream dependency is ever poisoned.

**SHA-pin every `uses:` reference.** Full 40-char commit SHA, including first-party `actions/*` and `github/*`. GitHub's 2025 official guidance and OpenSSF's post-tj-actions / post-reviewdog recommendations both treat SHA-pinning as universal, not a third-party-only practice. Tags are mutable — a compromised tag is a supply-chain incident, which is exactly what CVE-2025-30066 (tj-actions/changed-files, March 2025) demonstrated. Tag-pinning a first-party action is a documented exception, paired with an inline comment and Dependabot for the `github-actions` ecosystem so SHAs don't rot.

**Never use `@main`, `@master`, or floating semver wildcards** (`@v3.1.x`). Unreproducible and unsafe regardless of the action's source. If you see one, treat it as a security finding, not a style issue.

**Set `timeout-minutes` on every job.** The runner default is 360 minutes. A hung job at that default burns $40+ of compute per incident and masks a hang you want to see fail loudly. 60 is a reasonable default ceiling; tune down from there.

**Strict bash everywhere.** `set -euo pipefail` at the top of every multi-line bash `run:` block. `defaults.run.shell: bash` at the workflow level so every `run:` uses the same shell regardless of the runner OS. Bash's defaults silently swallow pipeline failures and unset variables — the exact class of bug CI is supposed to catch.

**Concurrency deliberately.** Workflow-level `concurrency.group: ${{ github.workflow }}-${{ github.ref }}` with `cancel-in-progress: true` for PR and branch-push workflows — stops queue pile-up from force-pushes and superseded runs. **Never** set `cancel-in-progress: true` on deploy or release workflows: cancelling a deploy mid-run leaves systems in inconsistent states, and recovery is manual. Deploys get a concurrency group (to serialize) but not cancellation.

**Treat user-controlled context as untrusted.** Never interpolate `${{ github.event.* }}`, `github.head_ref`, `inputs.*`, or similar attacker-controlled context directly into `run:` script bodies. This is script injection — a PR title of `"; rm -rf / #` executes as shell when `${{ github.event.pull_request.title }}` is substituted into a `run:` string. Route through `env:` and reference as `"$VAR"` in the shell; the `env:` assignment goes through a safe channel and the expansion happens at runtime in quoted context.

**`pull_request_target` is dangerous and rarely necessary.** This trigger runs with write permissions and secrets against the base repo, and is the vector behind most Actions CVEs. Never check out PR code when using it. The November 2025 GitHub change (workflow file + checkout commit always from the default branch) fixed one class of vulnerability — outdated workflows on side branches — but the core risk (fork code executing with base-repo write access and secrets) remains. If you're reaching for `pull_request_target`, stop and ask whether `pull_request` would work; it almost always does.

**Gate production deploys behind environments.** GitHub `environment:` with required reviewers and deployment branch rules is the only reliable human gate on deploys. Protection rules enforce at the API level — nobody can bypass via a clever workflow edit.

**Prefer OIDC over static cloud credentials.** Federated credentials (`id-token: write` + cloud-provider trust policy) replace the largest-blast-radius secret most teams hold. Static AWS/GCP/Azure keys in `secrets.*` leak through every vector — logs, artifacts, compromised actions, misconfigured permissions. OIDC tokens are scoped, short-lived, and bound to the specific workflow run. This is now mainstream guidance, not a strong-minority position.

**Add `step-security/harden-runner` as the first step of every job.** Audit mode at minimum; block mode where you can characterize legitimate egress. Provides egress monitoring and supply-chain tamper detection — the runtime defense that would have caught tj-actions/changed-files in March 2025. OpenSSF explicitly recommends it post-incident.

**`persist-credentials: false` on `actions/checkout`** unless the workflow needs to push back to the repo. The default leaves a usable `GITHUB_TOKEN` on disk for the rest of the job; every subsequent action sees it. Scope the credential to the push step that actually needs it.

**Cache keyed by lockfile hash.** `hashFiles('**/package-lock.json')`, `hashFiles('**/poetry.lock')`. Prefer the caching built into `setup-node`/`setup-python`/`setup-java` — their keys are correct by default. Hand-rolled `actions/cache` entries frequently cache-miss (key too specific) or cache-poison (key too loose).

**Artifacts with `name` and `retention-days`.** Default 90-day retention is often too long and always too expensive. Set `name:` explicitly so downloads are findable; set `retention-days:` to the minimum the workflow needs.

**No deprecated workflow commands.** `::set-output`, `::set-env`, `::add-path` are deprecated and being removed. Use `$GITHUB_OUTPUT`, `$GITHUB_ENV`, `$GITHUB_PATH`.

**Pin runner images for release/deploy.** `ubuntu-24.04`, not `ubuntu-latest`, on workflows where image drift would break production. `ubuntu-latest` migrated from 22.04 to 24.04 in Jan 2025; the next rollover will happen again. CI can tolerate the drift; releases should not.

**Public-repo `pull_request` workflows must not use self-hosted runners.** PR code would execute on your infrastructure with whatever access the runner has. This is severe and commonly missed. Private repos are a judgment call; public repos are a hard refusal.

**kebab-case job and step IDs** — `build-and-test`, not `BuildAndTest`. IDs appear in URLs, required-check names, and `needs:` references. Consistency matters because every downstream consumer (branch protection, badges, API calls) has to match the exact string.

**Scope `env:` narrowly.** Step-level > job-level > workflow-level. Secrets should never appear in workflow-level `env:` — that exposes them to every job and every action in every job. Step-level `env:` limits the blast radius to the one step that needs the value.

## Patterns That Work

**SHA-pin + Dependabot.** Pinning stops silent updates; Dependabot raises a PR when a new SHA is available. The two are one pattern — pin without Dependabot and SHAs rot into known-vulnerable versions.

**`harden-runner` first, every job.** Runtime defense. Catches the class of compromise that static pinning misses.

**Top-level `contents: read` + per-job elevation.** The workflow defaults to the narrowest scope; jobs that need `packages: write` or `id-token: write` ask for it explicitly. A reader can see the elevated permissions at the exact job where they apply.

**User input through `env:`, never `${{ }}` in `run:`.** Every piece of `github.event.*`, `inputs.*`, `github.head_ref` that touches a shell goes through `env:` first.

**OIDC over static secrets** for cloud auth. Scoped, short-lived, bound to the run.

**Environment + required reviewers** for production deploys. Humans approve in the UI; workflows can't bypass.

**Concurrency cancel-in-progress for PR/push; no-cancel for deploy.** The deploy workflow gets a `concurrency.group` (to serialize) without `cancel-in-progress` (to let the running deploy finish).

**Lockfile-hashed cache keys, setup-* built-in caching preferred.** Correct by default.

**`run:` blocks short; scripts checked in.** If it's over ~20 lines, move it to `.github/scripts/foo.sh` and call `bash .github/scripts/foo.sh`.

**Reusable workflows for whole-job reuse; composite actions for step sequences.** Don't copy-paste job bodies across workflow files.

**`if: always() && needs.<job>.result == '<result>'`** for post-run cleanup / notification jobs. `if: failure()` alone is brittle across `needs:` chains.

## Anti-Patterns

**`@v4` for third-party actions.** A tag is a movable pointer. The tj-actions/changed-files compromise (March 2025, CVE-2025-30066) was a malicious commit pushed under existing tags — every repo pinned to `@v44` got the poisoned code on their next run. SHA-pinning stops this class of attack at the cost of Dependabot PRs.

**`${{ github.event.issue.title }}` in a `run:` block.** Template injection. An attacker-supplied issue title becomes attacker-supplied shell. Route through `env:`.

**`pull_request_target` + `actions/checkout` of the PR ref.** The textbook Actions CVE. Fork code runs with base-repo write permissions and base-repo secrets. There is no safe configuration of this combination.

**`permissions: write-all`** or no top-level permissions block. A compromised action inherits the full `GITHUB_TOKEN` scope. Least-priv at workflow level is the single largest defense.

**`continue-on-error: true` on a test or build step.** Silent CI decay. A red test that reports green erodes trust in every signal CI produces. Reserve for explicitly optional steps (coverage uploads, advisory linters) with an inline comment justifying use.

**`cancel-in-progress: true` on deploy or release.** Cancelling mid-deploy leaves half-deployed state. Recovery is manual and error-prone.

**`::set-output` / `::set-env` / `::add-path`.** Deprecated; silently non-functional on new runners. Use `$GITHUB_OUTPUT` etc.

**`ubuntu-latest` on release workflows.** Image rollovers break release pipelines — a rare but catastrophic failure mode on the exact workflow you can least afford to break.

**Secrets in workflow-level `env:`.** Every job sees them. Every action called from every job sees them. Scope to the step.

**Self-hosted runners on public-repo `pull_request` workflows.** PR code executes on your infrastructure. Severe.

**`fetch-depth: 0` by default.** Full history clones are slow and usually unnecessary. Use `1` unless the job genuinely needs history (release notes generation, blame-based checks).

**Unpinned Docker images** (`docker://node:latest`). Same class as unpinned actions.

**Hardcoded secrets** in the workflow file. Every secret scanner in existence catches these; treat any hit as an incident, not a style issue.

## Safety & Maintenance

**Dependabot for `github-actions` is non-optional if you SHA-pin.** Without it, pinned SHAs silently rot into known-vulnerable versions. `.github/dependabot.yml` with `package-ecosystem: github-actions` is two lines of config for the biggest supply-chain defense you can add.

**Review action permissions at every Dependabot bump.** New versions can request new scopes. The bump PR is where you catch scope creep — once merged, scope escalation is invisible.

**Audit `step-security/harden-runner` egress logs** if you're running with `egress-policy: audit`. The logs surface unexpected outbound traffic; ignoring them defeats the point.

**Rotate workflow structure when a file exceeds ~200 lines.** Extract jobs to reusable workflows; extract step sequences to composite actions. Past 200 lines, every change risks touching something unrelated.

**Retire workflows when their triggers stop firing.** A workflow that hasn't run in six months is either dead weight or a broken trigger — either way it needs a decision, not silent accumulation.

---

**Diagnostic when a workflow misbehaves.** Check in order:

1. **Trigger and filters** — is the workflow even firing? GitHub's Actions UI shows dropped runs on `paths`/`branches` filter misses.
2. **Permissions** — does the job have the scopes the action needs? `actions/github-script` failing with "Resource not accessible by integration" is almost always permissions.
3. **Pinning** — has a SHA been moved under you (Dependabot bump, force-push to a third-party action, compromised tag)? Cross-reference the action's release history.
4. **Concurrency** — is a prior run queued or cancelled? The Actions UI shows both.
5. **Quoting and strict mode in `run:`** — unquoted variable expansion, missing `set -euo pipefail`, broken pipeline without `pipefail`.

Most pathologies live in one of those five. Skip ahead to the one the symptom points at.
