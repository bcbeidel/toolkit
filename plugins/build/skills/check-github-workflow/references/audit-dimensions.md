---
name: Audit Dimensions — GitHub Workflows
description: The complete check inventory for check-github-workflow — Tier-1 deterministic check table (~28 checks across 9 scripts) and Tier-2 judgment dimension specifications (7 dimensions, each citing its source principle). Referenced by the check-github-workflow workflow.
---

# Audit Dimensions

The check-github-workflow audit runs in three tiers. This document
is the inventory: every deterministic check Tier-1 emits, every
judgment dimension Tier-2 evaluates. Every dimension cites the
source principle it audits from
[github-workflow-best-practices.md](../../../_shared/references/github-workflow-best-practices.md).

## Tier-1 — Deterministic Checks

Nine scripts, ~28 atomic checks. Each script emits findings in the
fixed lint format (`SEVERITY  <path> — <check>: <detail>` +
`Recommendation:`). Exit codes: `0` clean / WARN / INFO / HINT-only;
`1` on FAIL; `64` arg error; `69` missing required dependency
(`actionlint`, `zizmor`, `yamllint`, `shellcheck` are optional and
degrade gracefully).

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.py` | `secret` | API keys, tokens, private URLs via regex pattern list | FAIL | Safety & Maintenance (toolkit convention) |
| `check_structure.py` | `workflow-name` | Top-level `name:` field present and non-empty | WARN | Name every workflow, job, and multi-line step |
| `check_structure.py` | `job-name` | Every job has a non-empty `name:` field | WARN | Name every workflow, job, and multi-line step |
| `check_structure.py` | `step-name` | Every multi-line `run:` step has a `name:` field | WARN | Name every workflow, job, and multi-line step |
| `check_structure.py` | `permissions-top` | Top-level `permissions:` block exists and is not `write-all` | FAIL | Declare top-level `permissions:` with least privilege |
| `check_structure.py` | `timeout-minutes` | Every job has `timeout-minutes:` as a positive integer | FAIL | Set `timeout-minutes` on every job |
| `check_structure.py` | `defaults-shell` | `defaults.run.shell: bash` at workflow level | WARN | Strict bash everywhere |
| `check_structure.py` | `concurrency-group` | `concurrency.group` includes `${{ github.workflow }}` and `${{ github.ref }}` | WARN | Concurrency deliberately |
| `check_structure.py` | `concurrency-deploy` | Workflows classified as deploy/release (filename `deploy*.yml` / `release*.yml`) do NOT set `cancel-in-progress: true` | FAIL | Never cancel-in-progress on deploy |
| `check_structure.py` | `id-kebab` | Job IDs and step IDs match `^[a-z][a-z0-9-]*$` | WARN | kebab-case job and step IDs |
| `check_pinning.py` | `sha-pin-third-party` | Every third-party `uses:` ref resolves to a 40-char commit SHA | FAIL | SHA-pin every `uses:` reference |
| `check_pinning.py` | `sha-pin-first-party` | First-party (`actions/*`, `github/*`) refs are either SHA or a major tag paired with a `# dependabot-managed` (or equivalent) comment | WARN | SHA-pin universal with documented first-party exemption |
| `check_pinning.py` | `no-floating-ref` | No `@main`, `@master`, or floating semver wildcards on any `uses:` | FAIL | Never use `@main`, `@master`, or floating wildcards |
| `check_pinning.py` | `docker-tag` | Docker image references (`uses: docker://...`, `jobs.*.container.image`, `services.*.image`) include an explicit non-`latest` tag or `@sha256:` digest | FAIL | Unpinned Docker images are the same class as unpinned actions |
| `check_pinning.py` | `runner-pin-deploy` | Release/deploy workflows (filename heuristic) pin `ubuntu-<version>` or other explicit version instead of `*-latest` | WARN | Pin runner images for release/deploy |
| `check_safety.py` | `pr-target-checkout` | `pull_request_target` trigger combined with `actions/checkout` of a PR ref (`github.event.pull_request.head.*`, `github.head_ref`) | FAIL | `pull_request_target` is dangerous — never check out PR code |
| `check_safety.py` | `template-injection` | `${{ github.event.* }}`, `${{ github.head_ref }}`, `${{ inputs.* }}`, or similar user-controlled expression interpolated directly into `run:` block text | FAIL | Treat user-controlled context as untrusted |
| `check_safety.py` | `deprecated-cmds` | `::set-output`, `::set-env`, or `::add-path` appears in any `run:` block | FAIL | No deprecated workflow commands |
| `check_safety.py` | `workflow-env-secrets` | `${{ secrets.* }}` referenced from top-level `env:` | FAIL | Scope `env:` narrowly |
| `check_safety.py` | `fork-pr-secrets` | `pull_request` workflows reference `${{ secrets.* }}` without a source-gating `if:` (e.g., `github.event.pull_request.head.repo.full_name == github.repository`) | FAIL | Don't expose secrets to fork PRs |
| `check_safety.py` | `self-hosted-public-pr` | Public-repo (detected via `gh api` or the presence of a repo-visibility marker) `pull_request` workflow uses `self-hosted` runners | FAIL | Public-repo `pull_request` must not use self-hosted runners |
| `check_safety.py` | `strict-bash` | Every multi-line bash `run:` block begins with `set -euo pipefail` (or equivalent) | WARN | Strict bash everywhere |
| `check_safety.py` | `persist-credentials` | `actions/checkout` steps set `persist-credentials: false` unless a subsequent `git push` or push-shaped action is present in the same job | WARN | `persist-credentials: false` on `actions/checkout` |
| `check_safety.py` | `harden-runner-first` | `step-security/harden-runner` is the first step of every job, with `egress-policy: audit` or `block` | INFO | Add `step-security/harden-runner` as the first step of every job |
| `check_actionlint.sh` | `actionlint` | Workflow passes `actionlint` (workflow schema, expression types, shellcheck-integrated `run:` validation) | WARN | Tooling readiness |
| `check_zizmor.sh` | `zizmor` | Workflow passes `zizmor` audit (unpinned-uses, excessive-permissions, template-injection, dangerous-triggers, self-hosted-runner rules) | WARN | Tooling readiness |
| `check_yamllint.sh` | `yaml-valid` | YAML is syntactically valid and passes `yamllint` default config | WARN | Style & Review |
| `check_shellcheck.py` | `shellcheck-run` | `run:` block content, where effective shell is bash, passes `shellcheck` (SC2086, SC2046, SC2068, SC2154) | WARN | Strict bash everywhere |
| `check_size.py` | `run-block-size` | No `run:` block exceeds ~20 non-blank lines (beyond which extract to `.github/scripts/`) | INFO | Extract long `run:` blocks into checked-in scripts |
| `check_size.py` | `workflow-size` | Workflow file ≤ ~200 lines (beyond which extract to reusable workflows / composite actions) | INFO | Rotate workflow structure when a file exceeds ~200 lines |

**FAIL exclusions from Tier-2.** Any `secret`, `pr-target-checkout`,
`template-injection`, `no-floating-ref`, or `deprecated-cmds`
finding excludes the file from Tier-2. These are either
correctness/safety bugs that bias judgment toward false negatives
(the file is exploitable as written — judgment-level coaching is
the wrong coverage) or render the file non-functional on current
runners. Other FAILs (`permissions-top`, `timeout-minutes`,
`concurrency-deploy`, `docker-tag`, `workflow-env-secrets`,
`fork-pr-secrets`, `self-hosted-public-pr`) leave a parseable
workflow that judgment can still usefully evaluate.

**Missing-tool degradation.** `check_actionlint.sh`,
`check_zizmor.sh`, `check_yamllint.sh`, and `check_shellcheck.py`
emit an INFO finding (`tool-missing`) and exit 0 when the wrapped
tool is absent. The remaining scripts continue running. The
Missing Tools INFO is the user's signal that Tier-1 coverage is
reduced — surfacing it is the contract.

**Release/deploy classification.** The `runner-pin-deploy` and
`concurrency-deploy` checks use a filename heuristic — files
matching `deploy*.yml`, `release*.yml`, or containing `publish` in
the filename are classified as deploy/release. An explicit override
is supported via a `# classification: deploy` or `#
classification: ci` header comment on the first line of the file;
the header comment wins over the filename heuristic when both are
present.

## Tier-2 — Judgment Dimensions

One LLM call per file. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless a dimension explicitly marks otherwise —
judgment-level drift is coaching, not blocking.

### D1 Trigger Discipline

**Source principles:** *Scope triggers narrowly.* *`pull_request_target`
is dangerous and rarely necessary.* *Randomize scheduled cron
minutes.*

**Judges:** Are triggers scoped with `paths:`, `branches:`, `types:`
filters where they make sense, or is the workflow firing on every
push to every branch? Is `pull_request` vs `pull_request_target`
chosen deliberately — is there a reason this workflow needs the
elevated trigger? Are `schedule` cron expressions using a non-zero
minute to avoid thundering-herd on GitHub's runner pool? Are
`workflow_dispatch` inputs typed (`type: choice`) and documented?
Does the trigger set match the workflow's stated purpose — a CI
workflow should fire on `pull_request`, a release workflow on tag
push, a scheduled audit on `schedule`, and mismatches are worth
flagging?

### D2 Permissions & Secrets Discipline

**Source principles:** *Declare top-level `permissions:` with least
privilege.* *Scope `env:` narrowly.* *Prefer OIDC over static cloud
credentials.*

**Judges:** Is the top-level `permissions:` block at the narrowest
useful scope (`contents: read` at minimum), and are per-job
elevations justified by the work that job does? Are secrets
referenced only in the specific step that needs them, or are they
exposed to more steps than necessary via job-level or workflow-level
`env:`? If the workflow authenticates to a cloud provider, is it
using OIDC (`id-token: write` + federated credentials) or long-lived
static cloud keys — and if static, is there a documented reason
OIDC wasn't chosen? Does `permissions: id-token: write` appear if
and only if the workflow actually uses OIDC?

### D3 Pinning & Supply-Chain Posture

**Source principles:** *SHA-pin every `uses:` reference.* *Never
use `@main`, `@master`, or floating semver wildcards.* *Dependabot
for `github-actions` is non-optional if you SHA-pin.*

**Judges:** Is every third-party `uses:` a 40-char SHA (not a tag)?
For first-party (`actions/*`, `github/*`) tag-pinning, is there an
inline comment documenting the exemption and a Dependabot config in
the repo for the `github-actions` ecosystem? Are docker image
references (`uses: docker://...`, `container.image:`, `services.*.image:`)
pinned to a non-`latest` tag or `@sha256:` digest? If the repo has
no `.github/dependabot.yml` with `package-ecosystem: github-actions`,
is the SHA-pinning strategy viable — or will SHAs silently rot?

### D4 Runtime Safety

**Source principles:** *Add `step-security/harden-runner` as the
first step of every job.* *`persist-credentials: false` on
`actions/checkout`.* *Treat user-controlled context as untrusted.*
*`pull_request_target` is dangerous and rarely necessary.*

**Judges:** Is `step-security/harden-runner` the first step of every
job (audit or block mode)? Does `actions/checkout` have
`persist-credentials: false` unless the job genuinely needs to push
back (a subsequent `git push` or push-shaped action)? Are all uses
of `${{ github.event.* }}`, `${{ github.head_ref }}`, `${{ inputs.*
}}`, `${{ github.ref_name }}` routed through `env:` before reaching
any `run:` block — or are any interpolated directly into `run:`
text? If `pull_request_target` is used, does the workflow avoid any
PR-code checkout, and does it avoid granting elevated permissions
to steps that run before the trust boundary is established?

### D5 Correctness & Error Handling

**Source principles:** *Set `timeout-minutes` on every job.* *Strict
bash everywhere.* *Reserve `continue-on-error` for explicitly
non-blocking steps.*

**Judges:** Does every job have a deliberate `timeout-minutes:`
value (not just the default, and not set to an unreasonably high
number to paper over a hang)? Does every multi-line bash `run:`
block start with `set -euo pipefail` (or equivalent)? Is
`defaults.run.shell: bash` set at workflow level to avoid
OS-dependent shell differences? Is `continue-on-error: true` used
only on steps that are explicitly non-blocking (coverage uploads,
advisory linters) with an inline comment justifying use — and
never on test, build, deploy, or security-scan steps? Are `needs:`
relationships declared explicitly, and do post-failure /
post-success jobs use `if: always() && needs.<job>.result == '<val>'`
rather than bare `if: failure()` (which is brittle across `needs:`
chains)?

### D6 Performance & Concurrency

**Source principles:** *Concurrency deliberately.* *Cache keyed by
lockfile hash.* *Scope triggers narrowly.*

**Judges:** Is `concurrency` defined at workflow level with
`cancel-in-progress: true` for PR/push workflows, and explicitly
`false` (or omitted) for deploy/release workflows? Is caching used
where dependencies are installed, and is the cache key derived from
a lockfile hash (`hashFiles('**/package-lock.json')`,
`hashFiles('**/poetry.lock')`) rather than a static string? Is the
`cache:` option on `setup-node`/`setup-python`/`setup-java`
preferred over a hand-rolled `actions/cache` entry? Are costly jobs
gated with `paths:` filters or conditional `if:` so they don't run
on unrelated changes? Does `actions/checkout` set an explicit
`fetch-depth` (usually `1`) rather than defaulting to full history?

### D7 Maintainability

**Source principles:** *Single-purpose per file.* *Extract long
`run:` blocks into checked-in scripts.* *Extract shared logic.*
*kebab-case job and step IDs.* *Scope `env:` narrowly.* *Artifacts
with `name` and `retention-days`.*

**Judges:** Is the workflow single-purpose — does its name and
trigger set tell a coherent story, or is it an omnibus file? Are
any `run:` blocks longer than ~20 non-blank lines (candidate for
extraction to `.github/scripts/<name>.sh`)? Is logic duplicated
across jobs that could be consolidated into a reusable workflow
(`workflow_call`) or composite action? Are job IDs and step IDs
kebab-case and descriptive? Are `env:` blocks at the narrowest
useful scope (step > job > workflow)? Do `actions/upload-artifact`
steps always set explicit `name:` and `retention-days:`?

## Tier-3 — Cross-Workflow Collision

One analysis per directory-scope run. INFO severity — maintainer
guidance, not failures.

**Triggered checks:**

- **Duplicated job definitions** — two or more workflows contain a
  job with near-identical `runs-on:` + `steps:` sequences. Recommend
  extracting to a reusable workflow `_<name>.yml` with
  `on: workflow_call:` and referencing via `uses:
  ./.github/workflows/_<name>.yml`.
- **Duplicated step sequences** — identical (or near-identical)
  `harden-runner` + `checkout` + `setup-*` preambles across jobs in
  different workflows. Recommend a composite action under
  `.github/actions/<name>/action.yml`.
- **Duplicated matrix strategies** — the same `strategy.matrix`
  block repeated across workflows. Recommend consolidating via a
  reusable workflow that accepts the matrix as input.

Single-workflow scope skips this tier entirely.

## Finding Format

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Example findings:

```
FAIL     .github/workflows/deploy-prod.yml — sha-pin-third-party:
         uses: tj-actions/changed-files@v44 (tag, not SHA)
  Recommendation: Pin to the full 40-char SHA. Fetch via `gh api repos/tj-actions/changed-files/git/refs/tags/v44 --jq '.object.sha'`. Add inline comment `# v44`.

FAIL     .github/workflows/ci.yml — timeout-minutes:
         job `test` has no timeout-minutes; default is 360
  Recommendation: Add `timeout-minutes: 20` to the job.

WARN     .github/workflows/ci.yml — harden-runner-first:
         job `lint` does not start with step-security/harden-runner
  Recommendation: Prepend a `Harden runner` step pinned to a SHA with `egress-policy: audit`.

INFO     .github/workflows/ — duplicated-job (cross-workflow):
         jobs `build` in ci.yml and release.yml share 17 of 18 steps
  Recommendation: Extract to `.github/workflows/_build.yml` with `on: workflow_call:`; reference via `uses: ./.github/workflows/_build.yml` from both callers.
```

Summary line at the top and bottom:
`N fail, N warn, N info across N workflows`.
