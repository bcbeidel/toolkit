---
name: build-github-workflow
description: >
  Scaffolds a GitHub Actions workflow — a YAML file under
  `.github/workflows/` — with top-level least-priv `permissions:`,
  SHA-pinned `uses:`, per-job `timeout-minutes`, workflow-level
  `defaults.run.shell: bash`, scoped triggers, `harden-runner` as
  first step, `set -euo pipefail` in every multi-line `run:`, and
  deliberate concurrency posture (cancel-in-progress for PR/push,
  no-cancel for deploy). Use when the user wants to "create a github
  workflow", "scaffold a ci workflow", "new deploy workflow", "build
  a github actions workflow for X", or "write a release workflow".
  Not for composite actions (`action.yml` — separate primitive), org
  rulesets, Dependabot configs, or GitHub Apps.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[purpose]"
user-invocable: true
references:
  - ../../_shared/references/github-workflow-best-practices.md
  - ../../_shared/references/primitive-routing.md
license: MIT
---

# Build GitHub Workflow

Scaffold a GitHub Actions workflow: a single YAML file under
`.github/workflows/` that runs on repository events, holds an explicit
permissions / timeout / concurrency / pinning posture, and stays
under the Checks-UI-and-required-checks contract. The authoring
rubric — anatomy template, authoring principles, patterns that work,
anti-patterns — lives in
[github-workflow-best-practices.md](../../_shared/references/github-workflow-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

The scope is **a single workflow file**. Composite actions,
organization rulesets, Dependabot configs, and GitHub Apps are
separate primitives.

**Workflow sequence:** 1. Route → 2. Scope Gate → 3. Elicit →
4. Draft → 5. Safety Check → 6. Review Gate → 7. Save → 8. Test

## 1. Route

Confirm a GitHub Actions workflow is the right primitive before
asking scaffold questions.

**Wrong primitive:**

- **Composite action** (a reusable unit under `.github/actions/<name>/`
  with an `action.yml` exposing `inputs`/`outputs`/`runs`) — a
  different rubric (input schemas, `runs.using`, release tagging).
  No `/build:build-github-action` skill exists yet; hand-author.
- **Organization ruleset / branch protection config** — lives in
  GitHub settings, not in `.github/workflows/`.
- **Dependabot config** (`.github/dependabot.yml`) — different schema.
- **CODEOWNERS** — `.github/CODEOWNERS`, different schema.
- **A Claude Code hook** — route to `/build:build-hook`.
- **A shell script that runs in CI** — the workflow is the trigger;
  the script goes to `/build:build-bash-script` and is called from
  the workflow.

**Right primitive** (YAML file fired by a repository event, runs jobs
on a runner, uses the `GITHUB_TOKEN`) → proceed to Scope Gate.

## 2. Scope Gate

Refuse to scaffold — and recommend an alternative — when the request
signals one of these:

1. **Composite action authoring.** Out of scope; hand-author or wait
   for `/build:build-github-action`. Do not approximate a composite
   action shape inside `.github/workflows/`.
2. **`pull_request_target` + checkout of PR code.** Textbook Actions
   CVE vector. Refuse and explain: this combination has no safe
   form — fork code executes with base-repo write permissions and
   secrets. Offer `pull_request` (no secrets for forks; safe) or
   `pull_request_target` *without* PR checkout as alternatives.
3. **`@main`, `@master`, or floating semver wildcards** for any
   `uses:`. Refuse and explain: mutable refs are unreproducible and
   unsafe. Ask the user for a pinnable SHA or major tag; offer to
   resolve a SHA via `gh api` if they approve.
4. **Secrets in public-repo fork `pull_request` workflows.** Secrets
   can't safely reach fork PR code. Refuse and explain; recommend
   splitting into a `pull_request` (no secrets) and a merge- or
   label-triggered workflow (with secrets).
5. **Self-hosted runners on public-repo `pull_request` workflows.**
   PR code would execute on your infrastructure. Refuse and explain.
6. **Multi-workflow refactor.** This skill scaffolds one file. For
   splitting an omnibus workflow or introducing reusable workflows
   across several files, iterate — scaffold one at a time.

If any signal fires, state the signal, name the alternative, and
stop. Do not proceed to Elicit.

## 3. Elicit

If `$ARGUMENTS` is non-empty, parse it as `[purpose]` and pre-fill
question 1. Otherwise ask, one question at a time:

**1. Purpose** — one sentence: what does this workflow do?
("Run pytest on pull requests against `main`", "Deploy the prod
service on a `v*` tag push", "Nightly lockfile audit at 03:00 UTC".)
Drives the filename (`ci.yml`, `deploy-prod.yml`, `audit-locks.yml`).

**2. Triggers** — pick the set deliberately:

- `push` — branch list (e.g., `[main]`), `paths:` filter if the
  workflow only cares about a subset.
- `pull_request` — branch list, `types:` (default
  `[opened, synchronize, reopened]` — name explicitly if different).
- `schedule` — cron expression (randomize the minute; never `0`).
- `workflow_dispatch` — inputs with `type: choice` where possible;
  document each input.
- `workflow_call` — this becomes a reusable workflow; declare
  `inputs:` and `secrets:`.

Any use of `pull_request_target` triggers a Scope Gate re-check —
return to Step 2.

**3. Jobs and dependencies** — which work splits across which jobs?
Which jobs `needs:` which? Prefer small jobs with explicit `needs:`
over one large job; parallelism is free, serial jobs block the DAG.

**4. Runner** — `ubuntu-latest` (CI) vs pinned `ubuntu-24.04`
(release / deploy). Ask: "Is this a release or deploy workflow?
Pin the runner if yes." Self-hosted requires justification; public-repo
`pull_request` workflows cannot use self-hosted.

**5. External actions** — full list. For each: full 40-char commit
SHA (user provides, or Claude offers to fetch via `gh api` with user
approval). First-party `actions/*`/`github/*` may tag-pin (`@v4`)
with an inline comment and Dependabot coverage — otherwise SHA.

**6. Deploys?** — if yes: target `environment:` name; required
reviewers configured? Promise the user the `environment:` key will
be scaffolded; actual protection rules are a GitHub UI configuration.

**7. Cloud authentication** — OIDC (provider + role ARN/federated
identity) or static secrets (discouraged). If OIDC, scaffold
`permissions: id-token: write` and the federated-credentials step;
if static, warn and scaffold with a comment pointing to OIDC migration.

**8. Concurrency behavior** — cancel-in-progress (default for PR/push
workflows) or no-cancel (mandatory for deploy/release — scaffold
rejects `cancel-in-progress: true` on deploys).

**9. Artifacts?** — names, `retention-days`. Skip artifact block if
none.

**10. Save path** — must be under `.github/workflows/`. Default:
`.github/workflows/<derived-from-purpose>.yml`. Confirm the filename.

## 4. Draft

Produce two artifacts.

**Artifact 1: The workflow YAML.**

One conditionalized template. Sections marked *(if deploy)*,
*(if OIDC)*, *(if schedule)*, *(if destructive)*, *(if has-artifacts)*
are omitted when intake rules them out.

```yaml
name: <Purpose>                                                 # from Step 3.1

on:
  # <triggers from Step 3.2, scoped with paths/branches/types>
  push:
    branches: [main]
    paths: ['<path-filter>']

permissions:                                                    # top-level least-priv
  contents: read
  # id-token: write                                             # (if OIDC)

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true                                      # (false or omitted for deploy)

defaults:
  run:
    shell: bash

jobs:
  <job-id>:                                                     # kebab-case IDs
    name: <Job Name>
    runs-on: ubuntu-latest                                      # pinned for deploy/release
    timeout-minutes: 20                                         # every job
    # environment: <env-name>                                   # (if deploy)
    # needs: <upstream-job-id>                                  # (if dependent)
    permissions:                                                # (elevate only if job needs it)
      contents: read
    steps:
      - name: Harden runner
        uses: step-security/harden-runner@<SHA>                 # v<N>.<M>.<P>
        with:
          egress-policy: audit

      - name: Checkout
        uses: actions/checkout@<SHA>                            # v<N>
        with:
          persist-credentials: false
          fetch-depth: 1

      # <language setup with built-in caching>
      - name: Setup
        uses: actions/setup-<lang>@<SHA>                        # v<N>
        with:
          <lang>-version: '<version>'
          cache: <ecosystem>

      # <OIDC cloud auth — if Step 3.7 = OIDC>
      # - name: Configure AWS credentials
      #   uses: aws-actions/configure-aws-credentials@<SHA>
      #   with:
      #     role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
      #     aws-region: us-east-1

      - name: <Action>
        env:
          # Route user-controlled context through env, NEVER ${{ }} in run
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          set -euo pipefail
          # <body — extract to a script under .github/scripts/ past ~20 lines>

      # (if has-artifacts)
      - name: Upload artifact
        uses: actions/upload-artifact@<SHA>                     # v<N>
        with:
          name: <artifact-name>
          path: <path>
          retention-days: 7                                     # minimum the workflow needs
```

**Artifact 2: A commit summary** — one paragraph naming what the
workflow does, what triggers it, what it produces (checks,
artifacts, deploys), and the first-run expectation. Used for the
commit message or PR description.

Present both artifacts before safety checks.

## 5. Safety Check

Review the draft against
[github-workflow-best-practices.md](../../_shared/references/github-workflow-best-practices.md)
before presenting. Fail any check → revise; the Review Gate is for
user approval, not correctness recovery.

**Structure:**
- Top-level `name:` present
- Triggers scoped (`paths` / `branches` / `types` named deliberately)
- Top-level `permissions:` present and is not `write-all`
- Workflow-level `defaults.run.shell: bash`
- Concurrency group defined; `cancel-in-progress: true` iff not a
  deploy/release workflow
- Every job has `name:` and `timeout-minutes:`
- Job/step IDs are kebab-case

**Pinning:**
- Every `uses:` is a 40-char commit SHA, or a first-party tag with
  an inline comment documenting the exemption
- No `@main`, `@master`, `@v*.*`, or other mutable ref
- Any `docker://` image has an explicit non-`latest` tag or
  `@sha256:` digest

**Safety:**
- `step-security/harden-runner` is the first step of every job
  (audit or block mode)
- `actions/checkout` has `persist-credentials: false` unless a push
  step is present
- No `${{ github.event.* }}` / `github.head_ref` / `inputs.*` in any
  `run:` block body — user-controlled context routed through `env:`
- `pull_request_target` unused, or if used, no PR-ref checkout
- No `${{ secrets.* }}` in top-level `env:`
- No `${{ secrets.* }}` in `pull_request` workflows without source
  gating
- If public-repo `pull_request`: no self-hosted runners

**Correctness:**
- Every multi-line bash `run:` block starts with `set -euo pipefail`
- No deprecated commands (`::set-output`, `::set-env`, `::add-path`)
- `continue-on-error: true` present only on steps with an inline
  comment justifying non-blocking behavior
- `needs:` explicit between jobs that depend on each other

**Deploy-specific (if deploy):**
- `environment:` key present with a name
- Runner pinned (`ubuntu-24.04`, not `ubuntu-latest`)
- `cancel-in-progress` is `false` or omitted

**Artifacts (if has-artifacts):**
- Every `actions/upload-artifact` has explicit `name` and
  `retention-days`

## 6. Review Gate

Present the workflow YAML and the commit summary. Wait for explicit
user approval before writing any file to disk. Write only after this
gate passes.

If the user requests changes, revise and re-present. Continue until
the user explicitly approves or cancels. Proceed to Save only on
explicit approval.

## 7. Save

Write the approved workflow to the path elicited in Step 3.10 — must
be under `.github/workflows/`. No other save location is valid for
this primitive.

Show the commit summary for the user to wire into the commit message
or PR description.

## 8. Test

Offer the audit:

> "Run `/build:check-github-workflow <path>` to audit the scaffolded
> workflow against actionlint, zizmor, yamllint, shellcheck on
> extracted `run:` content, plus the seven judgment dimensions?"

The audit is the canonical follow-on; running it once after scaffold
catches anything the Safety Check missed and gives a clean baseline.

## Anti-Pattern Guards

1. **Skipping the Scope Gate.** The six refusal signals are the
   most-exploited patterns in the Actions domain — scaffolding past
   any of them ships a known CVE shape.
2. **Scaffolding `pull_request_target` with PR checkout.** Unconditional
   refuse. There is no safe form of this combination.
3. **Scaffolding with `@main` / `@master` / `@v*.*`.** Unconditional
   refuse. Ask for a SHA.
4. **Missing top-level `permissions:`.** Default `GITHUB_TOKEN` is too
   broad. Every scaffolded workflow has `contents: read` at minimum
   at the top level.
5. **Missing `timeout-minutes:` on any job.** Default is 360 minutes;
   every job gets an explicit timeout.
6. **User-controlled expressions in `run:` bodies.** Route through
   `env:` without exception.
7. **`cancel-in-progress: true` on deploy.** Scaffold rejects this
   combination; the deploy concurrency group omits the cancel flag.
8. **Empty `REQUIRED_CMDS`-equivalent.** Whatever the Intake
   collected, the scaffold uses it — don't scaffold placeholder
   steps the user didn't ask for (`setup-python` when the Intake
   said Node, etc.).
9. **Skipping the Review Gate.** Write to disk only after explicit
   approval.

## Key Instructions

- Refuse cleanly on any of the six Scope Gate signals. These are
  hard refuses, not "scaffold-and-warn" cases.
- Save location is always under `.github/workflows/`. No other path
  is valid.
- SHA-pin universally, including first-party. First-party tag-pinning
  is an exception requiring an inline comment and Dependabot coverage.
- Offer to fetch release SHAs via `gh api repos/<owner>/<repo>/git/refs/tags/<tag>`
  when the user provides a tag instead of a SHA — with user approval
  before running `gh`.
- `step-security/harden-runner` is the first step of every job —
  no exceptions; this is the post-tj-actions runtime defense.
- Every multi-line bash `run:` block starts with `set -euo pipefail`.
- Write files to disk only after the Review Gate passes.
- Won't scaffold composite actions — different rubric, different
  schema. Out of scope.
- Won't scaffold `pull_request_target` + PR checkout — unconditional
  refuse.
- Won't scaffold mutable refs (`@main`, `@master`, `@v*.*`) —
  unconditional refuse.
- Recovery if a workflow is written in error: `rm <path>` removes it
  cleanly. The scaffold is self-contained — no settings.json, no
  shared-module registration — so removal leaves no dangling state.

## Handoff

**Receives:** user intent for a GitHub Actions workflow (purpose,
triggers, jobs + dependencies, runner, external actions + SHAs,
deploy target, cloud auth mode, concurrency behavior, artifacts,
save filename).

**Produces:** a workflow YAML at `.github/workflows/<name>.yml` plus
a commit summary describing what it does, what triggers it, and
what it produces.

**Chainable to:** `/build:check-github-workflow` (audit the scaffolded
workflow against actionlint, zizmor, yamllint, shellcheck, and the
seven judgment dimensions); `/build:build-bash-script` if a `run:`
block grew past ~20 lines and wants to become a checked-in script
under `.github/scripts/`.
