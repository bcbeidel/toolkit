---
name: Repair Playbook — GitHub Workflows
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-github-workflow opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-github-workflow. Every Tier-1
finding type and every Tier-2 dimension has a recipe here. Apply
one at a time, with explicit user confirmation, re-running the
producing check after each fix.

**INFO-severity findings are guidance, not repair targets.** They
inform the Tier-2 prompt; they surface in the report; they do not
enter the default repair queue unless the user explicitly selects
them.

## Table of Contents

- [Format](#format)
- Tier-1 recipes
  - [`check_secrets.py`](#tier-1--check_secretspy)
  - [`check_structure.py`](#tier-1--check_structurepy)
  - [`check_pinning.py`](#tier-1--check_pinningpy)
  - [`check_safety.py`](#tier-1--check_safetypy)
  - [`check_actionlint.sh`](#tier-1--check_actionlintsh)
  - [`check_zizmor.sh`](#tier-1--check_zizmorsh)
  - [`check_yamllint.sh`](#tier-1--check_yamllintsh)
  - [`check_shellcheck.py`](#tier-1--check_shellcheckpy)
  - [`check_size.py`](#tier-1--check_sizepy)
- [Tier-2 — Judgment Dimension Recipes](#tier-2--judgment-dimension-recipes)
  - D1 Trigger Discipline · D2 Permissions & Secrets · D3 Pinning &
    Supply Chain · D4 Runtime Safety · D5 Correctness · D6
    Performance & Concurrency · D7 Maintainability
- [Tier-3 — Cross-Workflow Collision](#tier-3--cross-workflow-collision)
- [Notes](#notes)

## Format

Each recipe carries five fields:

- **Signal** — the finding string or dimension name that triggers the recipe
- **CHANGE** — what to modify, in one sentence
- **FROM** — a concrete example of the non-compliant pattern
- **TO** — the compliant replacement
- **REASON** — why the change matters, tied to the source principle

---

## Tier-1 — `check_secrets.py`

### Signal: `secret — API key / token / private URL detected`

**CHANGE** Remove the secret from workflow source. Replace with a
`${{ secrets.<NAME> }}` reference to a GitHub Secret configured in
the repository or environment. Rotate the exposed credential.

**FROM**
```yaml
env:
  API_KEY: sk-proj-abc123def456...
```

**TO**
```yaml
env:
  API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

**REASON** Hardcoded secrets leak through git history, logs,
artifacts, and forks. Externalizing to GitHub Secrets is the
minimum bar; environment-scoped secrets with required reviewers are
better for production credentials. Rotate the exposed key — its
prior presence in git history means it cannot be trusted going
forward.

---

## Tier-1 — `check_structure.py`

### Signal: `workflow-name — top-level name missing`

**CHANGE** Add a top-level `name:` field on the first non-comment
line.

**FROM** `on: push:`
**TO** `name: CI` + `on: push:`

**REASON** Without a `name:`, the Checks UI derives a label from
the filename. Required-check configuration and PR comments read
worse, and the workflow is harder to identify in run lists.

### Signal: `job-name — job missing name`

**CHANGE** Add a `name:` to the job (human-readable, distinct from
the job ID).

**FROM**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

**TO**
```yaml
jobs:
  test:
    name: Unit tests
    runs-on: ubuntu-latest
```

**REASON** Job names appear in the Checks UI and required-check
names. Terse job IDs like `test` repeat across workflows; the
`name:` is what makes a row in the UI identifiable.

### Signal: `step-name — multi-line run step missing name`

**CHANGE** Add a `name:` above the `run:` block.

**FROM**
```yaml
- run: |
    set -euo pipefail
    pytest -v
```

**TO**
```yaml
- name: Run tests
  run: |
    set -euo pipefail
    pytest -v
```

**REASON** Unnamed multi-line steps show as `Run set -euo pipefail`
(or longer) in logs — unreadable in a list of 20 steps.

### Signal: `permissions-top — top-level permissions missing or write-all`

**CHANGE** Add top-level `permissions: contents: read`. Elevate
per-job where the specific job needs write scopes.

**FROM** (no top-level permissions block, or `permissions: write-all`)

**TO**
```yaml
permissions:
  contents: read

jobs:
  release:
    permissions:
      contents: write   # only the release job elevates
```

**REASON** The default `GITHUB_TOKEN` scope is too broad. A
compromised action inherits the full scope — including write.
Least-priv at workflow level plus per-job elevation is the OpenSSF
2025 recommendation and the largest defense against supply-chain
compromise.

### Signal: `timeout-minutes — job missing timeout`

**CHANGE** Add `timeout-minutes:` to the job. Default ceiling: 60;
tune to the expected duration + 25% buffer.

**FROM**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]
```

**TO**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps: [...]
```

**REASON** Runner default is 360 minutes. A hung job at that
default burns $40+ of compute per incident and masks a hang you want
to see fail fast.

### Signal: `defaults-shell — workflow missing defaults.run.shell: bash`

**CHANGE** Add `defaults.run.shell: bash` at workflow top level.

**FROM** (no `defaults:` block)

**TO**
```yaml
defaults:
  run:
    shell: bash
```

**REASON** The default `run:` shell differs across runner OSes
(`bash` on Linux/macOS, PowerShell on Windows). Setting
`defaults.run.shell: bash` pins one shell and avoids the class of
bugs where the same `run:` body behaves differently on different
runners.

### Signal: `concurrency-group — concurrency group missing or under-scoped`

**CHANGE** Add workflow-level `concurrency` with a group keyed on
`github.workflow` and `github.ref`. Set `cancel-in-progress: true`
for PR/push workflows; omit (or set `false`) for deploy/release.

**FROM** (no `concurrency:` block)

**TO**
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**REASON** Without concurrency, force-pushes pile up queued runs
and waste minutes. The `workflow + ref` key is the standard; `ref`
isolates PRs from branch pushes.

### Signal: `concurrency-deploy — deploy workflow sets cancel-in-progress: true`

**CHANGE** Remove `cancel-in-progress: true` (or set `false`) on
the deploy/release workflow. Keep the `group:` key to serialize
deploys.

**FROM**
```yaml
concurrency:
  group: deploy-prod
  cancel-in-progress: true
```

**TO**
```yaml
concurrency:
  group: deploy-prod
  cancel-in-progress: false
```

**REASON** Cancelling a deploy mid-run leaves systems in inconsistent
states. Recovery is manual and error-prone. Deploys get serialization
(the group) but not cancellation.

### Signal: `id-kebab — job or step ID not kebab-case`

**CHANGE** Rename the ID to lowercase kebab-case (`build-and-test`,
not `buildAndTest` or `BuildAndTest`). Update all `needs:` / `if:`
/ output references.

**FROM** `jobs: { BuildAndTest: ... }`
**TO** `jobs: { build-and-test: ... }`

**REASON** Job IDs appear in URLs and required-check names. Mixed
case hurts readability and breaks downstream consumers that
normalize case differently. Kebab-case is the GitHub Actions
convention.

---

## Tier-1 — `check_pinning.py`

### Signal: `sha-pin-third-party — @vN ref on third-party action`

**CHANGE** Replace the tag ref with the full 40-char commit SHA.
Add a trailing comment with the tag for readability. Ensure
`.github/dependabot.yml` configures `github-actions` so the SHA
doesn't rot.

**FROM**
```yaml
uses: tj-actions/changed-files@v44
```

**TO**
```yaml
uses: tj-actions/changed-files@2f7c5bfce28377bc069a65ba478de0a74aa0ca32  # v44
```

Fetch the SHA with:
```bash
gh api repos/tj-actions/changed-files/git/refs/tags/v44 --jq '.object.sha'
```

**REASON** Post-tj-actions (CVE-2025-30066, March 2025), tags are
mutable supply-chain liabilities. GitHub and OpenSSF both recommend
SHA-pin universally. Dependabot for `github-actions` raises a PR
when a new SHA is available, so pinning doesn't rot into
known-vulnerable versions.

### Signal: `sha-pin-first-party — first-party action tag-pinned without documented exemption`

**CHANGE** Either (a) SHA-pin like a third-party action (preferred),
or (b) keep the major tag and add an inline `# dependabot-managed`
comment, then verify `.github/dependabot.yml` covers
`package-ecosystem: github-actions`.

**FROM**
```yaml
uses: actions/checkout@v4
```

**TO** (option a — SHA-pin)
```yaml
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
```

**TO** (option b — documented tag exemption)
```yaml
uses: actions/checkout@v4  # dependabot-managed (first-party)
```

**REASON** GitHub's current guidance recommends SHA-pinning
universally. The first-party tag exemption is pragmatic given
Dependabot noise, but it requires documentation and Dependabot
coverage — otherwise the exemption is invisible to the auditor.

### Signal: `no-floating-ref — @main, @master, or @v*.*`

**CHANGE** Replace the floating ref with a pinned SHA (preferred) or
a specific tag (`@v4.2.2`, not `@v4`).

**FROM** `uses: some-action/foo@main`
**TO** `uses: some-action/foo@<SHA>  # v1.2.3`

**REASON** Mutable refs are unreproducible and unsafe. A push to
`main` or a tag move on `@v4` silently changes what runs. Every
published advisory in this class pivots on mutable-ref trust.

### Signal: `docker-tag — docker image missing tag or using :latest`

**CHANGE** Pin the image to an explicit non-`latest` tag or
`@sha256:` digest.

**FROM**
```yaml
container:
  image: node:latest
```

**TO**
```yaml
container:
  image: node:20.11.1
# or
  image: node@sha256:abc123...
```

**REASON** Docker `:latest` has the same mutable-ref failure mode
as `@main` on an action. Pinning is required for reproducibility
and supply-chain safety.

### Signal: `runner-pin-deploy — deploy/release workflow uses *-latest runner`

**CHANGE** Replace `ubuntu-latest` with the current Ubuntu LTS
version (`ubuntu-24.04`, as of 2026).

**FROM** `runs-on: ubuntu-latest`
**TO** `runs-on: ubuntu-24.04`

**REASON** `ubuntu-latest` migrated from 22.04 to 24.04 in Jan
2025; the next rollover will happen again. Image drift breaks
production release pipelines — rare but catastrophic on the exact
workflow you can least afford to break. CI can tolerate the drift;
releases should not.

---

## Tier-1 — `check_safety.py`

### Signal: `pr-target-checkout — pull_request_target + PR ref checkout`

**CHANGE** Either (a) switch the trigger to `pull_request` and
remove any secret usage that depended on `pull_request_target`, or
(b) keep `pull_request_target` but remove the PR-ref checkout and
run only on the base ref. The combined pattern has no safe form.

**FROM**
```yaml
on: pull_request_target
jobs:
  test:
    steps:
      - uses: actions/checkout@...
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: npm test  # running fork code with secrets!
```

**TO** (option a — safer default)
```yaml
on: pull_request
jobs:
  test:
    # no secrets available for fork PRs — plan accordingly
    steps:
      - uses: actions/checkout@...  # default ref = PR code
      - run: npm test
```

**TO** (option b — pull_request_target without PR checkout)
```yaml
on: pull_request_target
jobs:
  label:
    permissions:
      pull-requests: write
    steps:
      - uses: actions/checkout@...  # default ref = base branch, NOT PR code
      - run: gh pr edit ${{ github.event.number }} --add-label needs-review
```

**REASON** Textbook GitHub Actions CVE vector. Fork code executing
with write permissions and secrets is one of the most-exploited
patterns. The Nov 2025 change (workflow file always from the default
branch) did not fix this — the core risk is fork code + secrets,
not outdated workflow files.

### Signal: `template-injection — user-controlled expression in run: block`

**CHANGE** Move the expression to a per-step `env:` block; reference
as `"$VAR"` in the `run:` body.

**FROM**
```yaml
- run: |
    echo "Title: ${{ github.event.issue.title }}"
```

**TO**
```yaml
- env:
    TITLE: ${{ github.event.issue.title }}
  run: |
    set -euo pipefail
    echo "Title: $TITLE"
```

**REASON** Direct `${{ }}` interpolation into `run:` text is shell
injection — a PR title of `"; rm -rf / #` executes as shell. `env:`
assignment goes through a safe channel; the expansion happens at
runtime in quoted shell context.

### Signal: `deprecated-cmds — ::set-output / ::set-env / ::add-path`

**CHANGE** Replace with the environment-file equivalents.

**FROM**
```yaml
- run: |
    echo "::set-output name=version::1.2.3"
    echo "::set-env name=FOO::bar"
    echo "::add-path::$HOME/bin"
```

**TO**
```yaml
- run: |
    set -euo pipefail
    echo "version=1.2.3" >> "$GITHUB_OUTPUT"
    echo "FOO=bar" >> "$GITHUB_ENV"
    echo "$HOME/bin" >> "$GITHUB_PATH"
```

**REASON** The `::set-*` commands are deprecated and silently
non-functional on new runners. Workflows using them fail to pass
outputs without any error signal — the step looks green but
downstream jobs see empty values.

### Signal: `workflow-env-secrets — secret referenced in top-level env:`

**CHANGE** Remove from top-level `env:`; add as step-level `env:`
on the specific step that uses the secret.

**FROM**
```yaml
env:
  GH_TOKEN: ${{ secrets.GH_TOKEN }}

jobs:
  release: ...
  build: ...
  docs: ...
```

**TO**
```yaml
jobs:
  release:
    steps:
      - name: Publish
        env:
          GH_TOKEN: ${{ secrets.GH_TOKEN }}
        run: gh release create ...
```

**REASON** Workflow-level `env:` exposes the secret to every job,
every step, and every action called from every step — including
third-party actions that don't need it. Step-scoping is the
smallest blast radius.

### Signal: `fork-pr-secrets — pull_request workflow references secrets.* without source gating`

**CHANGE** Split the workflow into two — a `pull_request` workflow
with no secrets (runs tests on fork PRs safely), and a second
workflow triggered on merge or a `pull-request-target` label with
secret access. Alternatively, gate the secret-using step on
`github.event.pull_request.head.repo.full_name == github.repository`.

**FROM**
```yaml
on: pull_request
jobs:
  deploy-preview:
    steps:
      - env:
          NETLIFY_TOKEN: ${{ secrets.NETLIFY_TOKEN }}
        run: netlify deploy ...
```

**TO** (two-workflow split)
```yaml
# ci.yml — no secrets
on: pull_request
jobs:
  test:
    # safe for fork PRs

# preview.yml — label-gated, secrets available
on:
  pull_request_target:
    types: [labeled]
jobs:
  deploy-preview:
    if: github.event.label.name == 'preview'
    # runs only on trusted maintainer labeling
```

**REASON** Fork PRs cannot safely receive secrets — fork code could
exfiltrate them. The two-workflow pattern separates the trust
boundaries explicitly; the label gate requires a trusted maintainer
to opt in per-PR.

### Signal: `self-hosted-public-pr — self-hosted runner on public pull_request`

**CHANGE** Switch the runner to a GitHub-hosted runner
(`ubuntu-latest` for CI, pinned for deploy). If self-hosted is
genuinely required, move the job to a merge- or label-gated
workflow.

**FROM**
```yaml
on: pull_request
jobs:
  test:
    runs-on: [self-hosted, linux]
```

**TO**
```yaml
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
```

**REASON** PR code running on your self-hosted infrastructure is
severe — a malicious PR has access to whatever the runner has
(persistent disk, network, credentials, neighbors on the host).
Public-repo `pull_request` workflows must use GitHub-hosted runners.

### Signal: `strict-bash — multi-line bash run: missing set -euo pipefail`

**CHANGE** Prepend `set -euo pipefail` to the `run:` block.

**FROM**
```yaml
- run: |
    echo "step 1"
    make build
    make test
```

**TO**
```yaml
- run: |
    set -euo pipefail
    echo "step 1"
    make build
    make test
```

**REASON** Bash defaults silently swallow pipeline failures and
unset-variable typos. `set -euo pipefail` turns those into loud,
early exits — the exact class of bug CI is supposed to catch.

### Signal: `persist-credentials — actions/checkout without persist-credentials: false`

**CHANGE** Add `persist-credentials: false` to the checkout `with:`
block. Remove only if the job has a subsequent `git push` or
push-shaped step (e.g., `peaceiris/actions-gh-pages`).

**FROM**
```yaml
- uses: actions/checkout@<SHA>
```

**TO**
```yaml
- uses: actions/checkout@<SHA>
  with:
    persist-credentials: false
    fetch-depth: 1
```

**REASON** The checkout default leaves a usable `GITHUB_TOKEN` on
disk (`.git/config`) for the rest of the job. Every subsequent
action in that job can read it. Scoping the credential to the push
step reduces the blast radius of a compromised action.

### Signal: `harden-runner-first — harden-runner missing or not first step`

**CHANGE** Prepend a `Harden runner` step to every job, pinned to a
SHA, with `egress-policy: audit` (or `block` if you've characterized
the egress).

**FROM**
```yaml
jobs:
  build:
    steps:
      - uses: actions/checkout@<SHA>
      - ...
```

**TO**
```yaml
jobs:
  build:
    steps:
      - name: Harden runner
        uses: step-security/harden-runner@<SHA>  # v2.x
        with:
          egress-policy: audit
      - uses: actions/checkout@<SHA>
      - ...
```

**REASON** Runtime egress monitoring is the defense that catches
what static pinning misses. OpenSSF explicitly recommends post-
tj-actions; the tj-actions compromise would have surfaced in
`harden-runner` egress logs before secret exfiltration completed.

---

## Tier-1 — `check_actionlint.sh`

### Signal: `actionlint — <rule-id>: <actionlint description>`

**CHANGE** Apply the actionlint suggestion. Actionlint findings are
schema / expression / shell issues with specific, prescriptive
fixes — follow the tool's recommendation.

**REASON** Actionlint is the most comprehensive workflow schema
validator; its rule-level output is the source of truth. If a
finding doesn't match a rule recipe here, apply the tool's
suggestion verbatim.

## Tier-1 — `check_zizmor.sh`

### Signal: `zizmor — <rule-id>: <zizmor description>`

**CHANGE** Apply the zizmor suggestion. Zizmor findings are
security-focused and frequently overlap with the `check_pinning.py`
and `check_safety.py` recipes — use the relevant recipe in this
playbook; for zizmor-only rules (e.g., `template-injection` that
`check_safety.py` missed), follow zizmor's output.

**REASON** Zizmor is purpose-built for Actions security; it covers
patterns `check_pinning.py` and `check_safety.py` may miss (rare
expression shapes, composite-action boundary issues).

## Tier-1 — `check_yamllint.sh`

### Signal: `yaml-valid — <yamllint rule>`

**CHANGE** Fix the YAML style issue per yamllint's output. Common
fixes: consistent indentation, trailing newline, no trailing
whitespace, key ordering (within a given mapping).

**REASON** Style hygiene compounds with diff readability. Parse
errors stop the workflow from running at all.

## Tier-1 — `check_shellcheck.py`

### Signal: `shellcheck-run — SC<code>: <message>`

**CHANGE** Apply the shellcheck recommendation to the `run:` block.
Most common: quote variable expansions (SC2086), use `$()` over
backticks (SC2006), forward `"$@"` not `$@` (SC2068).

**REASON** Unquoted variables in `run:` blocks are the largest
class of shell bugs in CI. Shellcheck catches them mechanically;
every finding is a real issue.

## Tier-1 — `check_size.py`

### Signal: `run-block-size — run: block exceeds ~20 lines`

**CHANGE** Extract the `run:` body to `.github/scripts/<name>.sh`;
replace with `bash .github/scripts/<name>.sh <args>`.

**FROM**
```yaml
- run: |
    set -euo pipefail
    # 40 lines of build logic
    ...
```

**TO**
```yaml
- run: bash .github/scripts/build.sh
```

Then hand off to `/build:build-bash-script` to scaffold
`.github/scripts/build.sh` with proper structure (shebang, strict
mode, header comment, `main` function, sourceable guard).

**REASON** Past ~20 lines, YAML is the wrong place for code —
`shellcheck` can't see inside the heredoc, tests can't exercise the
logic, and diff review is painful. A checked-in script is
reviewable and testable.

### Signal: `workflow-size — workflow file exceeds ~200 lines`

**CHANGE** Extract one or more jobs to reusable workflows
(`_<name>.yml` with `on: workflow_call:`) or step sequences to a
composite action (`.github/actions/<name>/action.yml`). Call them
from the original workflow.

**REASON** Past 200 lines, every change risks touching unrelated
work; the file becomes a maintenance tarpit. Reusable workflows
and composite actions are the consolidation primitives.

---

## Tier-2 — Judgment Dimension Recipes

### D1 Trigger Discipline

**Signal** Trigger filters absent, `pull_request_target` used
without clear justification, `schedule` cron at minute 0, or
`workflow_dispatch` inputs untyped.

**CHANGE** Narrow triggers with `paths:`, `branches:`, `types:`.
Switch `pull_request_target` to `pull_request` if the workflow
doesn't need elevated permissions or secrets. Randomize cron
minutes. Type `workflow_dispatch` inputs.

**REASON** Unfiltered triggers burn minutes and create surprise
runs. `pull_request_target` is the most-exploited trigger in the
Actions ecosystem; `pull_request` is safer and sufficient for most
CI.

### D2 Permissions & Secrets Discipline

**Signal** Permissions broader than needed, secrets referenced
from job- or workflow-level `env:`, static cloud credentials used
when OIDC is available.

**CHANGE** Narrow `permissions:` to the smallest scope each job
needs. Move secrets to step-level `env:`. Migrate to OIDC where
the cloud provider supports it.

**REASON** Least privilege is the largest single defense against
compromised actions. OIDC short-lived tokens replace the
largest-blast-radius credentials most teams hold.

### D3 Pinning & Supply-Chain Posture

**Signal** Non-SHA third-party `uses:`, first-party tag-pinning
without Dependabot coverage, unpinned Docker images, missing
`.github/dependabot.yml` for `github-actions`.

**CHANGE** SHA-pin every `uses:` (fetch via `gh api`). Add
`.github/dependabot.yml` with `package-ecosystem: github-actions`.
Pin Docker images to tags or digests.

**REASON** The tj-actions and reviewdog compromises in 2025
demonstrated that tag-pinning is not sufficient. Dependabot keeps
SHAs from rotting into known-vulnerable versions.

### D4 Runtime Safety

**Signal** Missing `harden-runner`, `persist-credentials: true`
(default), user-controlled context in `run:` bodies, or
`pull_request_target` with PR-code checkout.

**CHANGE** Prepend `harden-runner` to every job. Set
`persist-credentials: false` on every `actions/checkout`. Route
`${{ github.event.* }}` / `inputs.*` through `env:`. Remove PR
checkout from `pull_request_target`.

**REASON** These are the runtime-layer defenses. Static pinning
catches known-bad SHAs; runtime defenses catch novel compromise at
the egress or injection point.

### D5 Correctness & Error Handling

**Signal** Missing `timeout-minutes`, missing `set -euo pipefail`,
missing `defaults.run.shell: bash`, unjustified
`continue-on-error: true`, or brittle `if: failure()` patterns.

**CHANGE** Add `timeout-minutes:` to every job. Prepend `set -euo
pipefail` to every multi-line bash `run:`. Set
`defaults.run.shell: bash`. Remove or justify
`continue-on-error`. Use `if: always() && needs.*.result` patterns.

**REASON** Silent failures erode trust in every CI signal. Strict
defaults and explicit timeouts make failures loud and fast.

### D6 Performance & Concurrency

**Signal** Missing or misconfigured `concurrency`, cache keys not
keyed on lockfile hash, hand-rolled `actions/cache` where `setup-*`
caching would do, missing `paths:` filters on costly jobs,
`fetch-depth: 0` without a reason.

**CHANGE** Add `concurrency` with `cancel-in-progress: true` for
PR/push (false for deploy). Key caches on `hashFiles(...)`. Use
`setup-*` `cache:` options. Add `paths:` filters. Set `fetch-depth:
1`.

**REASON** Correct concurrency + caching reduces CI cost and
latency measurably. Fetch-depth drives checkout time for large
repos.

### D7 Maintainability

**Signal** Workflow is multi-purpose, `run:` blocks exceed ~20
lines, logic duplicated across jobs, non-kebab-case IDs, broad
`env:` scoping, artifacts missing `name`/`retention-days`.

**CHANGE** Split multi-purpose workflows into focused files.
Extract long `run:` blocks to scripts. Extract duplicated logic to
reusable workflows or composite actions. Rename IDs to kebab-case.
Narrow `env:` to step level. Add `name:` and `retention-days:` to
every `upload-artifact`.

**REASON** Each of these individually is small; together they
compound into workflows that can be modified safely.

---

## Tier-3 — Cross-Workflow Collision

### Signal: `duplicated-job (cross-workflow) — identical job in multiple workflows`

**CHANGE** Extract the duplicated job into a reusable workflow
`_<name>.yml` with `on: workflow_call:`; reference with `uses:
./.github/workflows/_<name>.yml` from each caller. Pass per-caller
config via `inputs:` and `secrets:`.

**FROM** Same `build` job body inlined in `ci.yml` and `release.yml`.

**TO**
```yaml
# .github/workflows/_build.yml
on:
  workflow_call:
    inputs:
      ref:
        type: string
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps: [...]

# .github/workflows/ci.yml
jobs:
  build:
    uses: ./.github/workflows/_build.yml
    with:
      ref: ${{ github.sha }}

# .github/workflows/release.yml
jobs:
  build:
    uses: ./.github/workflows/_build.yml
    with:
      ref: ${{ github.ref_name }}
```

**REASON** Copy-paste workflows drift. The reusable-workflow
pattern keeps a single source of truth — bug fixes and pinning
bumps apply to every caller atomically.

### Signal: `duplicated-steps (cross-workflow) — identical step sequence across workflows`

**CHANGE** Extract the step sequence into a composite action under
`.github/actions/<name>/action.yml`; reference via `uses:
./.github/actions/<name>` from each caller.

**FROM** Same `harden-runner` + `checkout` + `setup-python` preamble
in 8 separate jobs across 4 workflows.

**TO**
```yaml
# .github/actions/setup-python-env/action.yml
name: Set up Python environment
runs:
  using: composite
  steps:
    - uses: step-security/harden-runner@<SHA>
      with:
        egress-policy: audit
    - uses: actions/checkout@<SHA>
      with:
        persist-credentials: false
        fetch-depth: 1
    - uses: actions/setup-python@<SHA>
      with:
        python-version: '3.12'
        cache: pip

# every caller
steps:
  - uses: ./.github/actions/setup-python-env
```

**REASON** Composite actions are the right primitive for repeated
step sequences — lower ceremony than a reusable workflow, and
usable mid-job instead of as a whole-job replacement.

### Signal: `duplicated-matrix (cross-workflow) — same matrix strategy across workflows`

**CHANGE** Consolidate the matrix into a reusable workflow that
accepts the matrix configuration as an input, or into a composite
action if the matrix drives step behavior.

**REASON** Matrix changes should happen in one place, not five.

---

## Notes

**Apply one finding at a time.** Bulk application removes the
user's ability to review individual edits and to catch the case
where one fix introduces a new finding elsewhere.

**Re-run the producing script after each fix.** Step 5 of the
repair loop — a fix that resolves finding A while producing
finding B is common, especially around concurrency / permissions /
`env:` scoping changes that touch multiple places.

**Prefer mechanical fixes before judgment-level refactors.** Tier-1
recipes are mostly single-line or single-block edits. Tier-2
dimension recipes (especially D7 Maintainability) can escalate to
extracting jobs or rewriting trigger structures — flag those as
larger changes and confirm scope with the user before applying.

**Dependabot config is out of scope for this skill.** When a recipe
recommends adding `.github/dependabot.yml`, note it in the repair
output but don't scaffold it inline — Dependabot config is a
separate primitive with its own schema.
