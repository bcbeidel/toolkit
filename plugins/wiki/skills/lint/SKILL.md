---
name: lint
description: >
  Runs lint checks on project content quality and reports frontmatter, URL,
  index, and skill issues. Use when the user asks to "lint", "run lint",
  "check lint", "check health", "validate documents", "run validation",
  "audit content quality", "review documents", "check coverage",
  "check freshness", "run health check", or "what needs attention".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path/to/file.md]"
user-invocable: true
references: []
license: MIT
---

# Audit Skill

Observe and report on project content quality. Read-only by default —
reports findings without modifying files. The one exception is a
single opt-in additive edit (adding an `@AGENTS.md` line to `CLAUDE.md`)
performed only on explicit user confirmation; all other cleanup actions
delegate to other skills.

This skill ships **no scripts of its own**. `lint.py` is a plugin-shared
script under `plugins/wiki/scripts/lint.py`; `<plugin-scripts-dir>` in
the invocation lines below resolves there. Inputs are validated by
argparse; the script does not call `subprocess` with `shell=True` or
take untrusted command strings.

## Workflow

1. **Run** `lint.py` against the project root (see [How to Run](#how-to-run))
2. **Checks** — the script applies four check categories; results are collected (see [The Checks](#the-checks))
3. **Interpret** — present the findings table to the user (see [Interpreting Results](#interpreting-results))
4. **Cleanup** — for actionable findings (missing setup, blocked URLs), offer guided resolution (see [Cleanup Actions](#cleanup-actions))

Each phase depends on the previous. Do not offer cleanup actions before presenting results.

## How to Run

```bash
# Default: fast, offline checks only
python <plugin-scripts-dir>/lint.py --root .

# Include URL reachability (network-dependent, off by default)
python <plugin-scripts-dir>/lint.py --root . --urls

# Validate a single file
python <plugin-scripts-dir>/lint.py path/to/file.md --root .

# JSON output for programmatic use
python <plugin-scripts-dir>/lint.py --root . --json

# Exit 1 on any issue (including warnings)
python <plugin-scripts-dir>/lint.py --root . --strict

# Override the resolver-recommendation threshold (default: 3)
python <plugin-scripts-dir>/lint.py --root . --resolver-threshold 5
```

Exit code: 1 if any `fail`, 0 if only `warn`. Use `--strict` to exit 1 on any issue.

## The Checks

### 1. Frontmatter Validation (fail)

Verifies:
- **fail:** `name` and `description` are non-empty

Other frontmatter fields (`type`, `sources`, `confidence`, schema-defined
values, etc.) are not enforced here. Project-specific schema validation
belongs in the project's own conventions — `wiki/SCHEMA.md` lint hooks
in when present.

### 2. Source URL Reachability (fail + warn) — opt-in

Checks that every URL in `sources` is reachable via HTTP. **Off by
default** (network-dependent, slow). Enable with `--urls`. URLs
returning 403/429 are downgraded to `warn` — these sites likely block
automated checks, not dead links.

### 3. Related Path Validation (fail)

Checks that local file paths in `related` exist on disk.

### 4. Resolver Threshold (warn)

Warns when no `RESOLVER.md` exists at the project root but enough
top-level directories contain ≥2 markdown files with valid YAML
frontmatter (ambient dirs like `.git`, `node_modules`, `.venv`
excluded). The recommendation is to run `/build:build-resolver`.

The default threshold is 3 conventionful directories — override with
`--resolver-threshold N`. Routing-artifact quality (when a resolver
*does* exist) is not checked here — see
[Resolver Evaluation](#resolver-evaluation).

## Interpreting Results

Summary line first, then table:

```
2 fail across 15 files

file                              | sev  | issue
docs/context/api/auth.md           | fail | Frontmatter 'name' is empty
docs/context/api/another.md        | fail | Source URL unreachable
```

With `--json`, output is a JSON array of objects:

```json
[
  {
    "file": "docs/context/area/topic.md",
    "issue": "Frontmatter 'name' is empty",
    "severity": "fail"
  }
]
```

A clean project produces:

```
All checks passed.
```

## Cleanup Actions

After presenting audit results, offer to help resolve actionable warnings:

- **Missing AGENTS.md or CLAUDE.md:** Offer to run `/wiki:setup` to
  initialize. Confirm with the user before writing any files.
- **AGENTS.md missing managed-section markers:** Offer to run `/wiki:setup`
  to add the managed section. Confirm before modifying existing content.
- **CLAUDE.md missing @AGENTS.md reference:** Offer to add the reference.
  Do not rewrite CLAUDE.md contents — only add the `@AGENTS.md` line.
- **Missing RESOLVER.md (threshold crossed):** Offer to run
  `/build:build-resolver` to scaffold a routing table. Show the
  conventionful directories the lint check detected so the user can
  judge whether the recommendation fits.
- **403/429 URL warnings:** List the blocked URLs and the files they
  appear in. Ask the user to verify them manually — these sites likely
  block automated checks rather than indicate dead links. The user
  decides whether each URL is still valid; lint does not prescribe a
  verification protocol.

## Key Instructions

- Audit is read-only by default — no log files, no side effects. The
  only write is the opt-in `@AGENTS.md` line added to `CLAUDE.md`,
  performed only after user confirmation.
- Use `/wiki:setup` to initialize missing project structure
- Empty project (no convention-following directories) exits 0 with no issues

## Skill Evaluation

Skill quality evaluation is handled entirely by `/build:check-skill` — lint does
not run automated Python-level skill checks. Invoke `/build:check-skill` on each
skill directory found and incorporate its findings into the report. Do not perform
independent skill quality judgment here — `check-skill` is the single source of
truth for what good looks like. Delegating keeps criteria consistent and prevents
drift between the two skills.

If the user ran lint on a specific skill path, pass that path to `check-skill`.
If lint ran across the full project, offer: "Found N skill(s) — run
`/build:check-skill` to evaluate quality?"

## Resolver Evaluation

Routing-artifact evaluation is handled entirely by `/build:check-resolver` —
lint does not audit `RESOLVER.md`, the AGENTS.md pointer, or
`.resolver/evals.yml`. When `RESOLVER.md` exists at the project root, offer:
"Found a resolver — run `/build:check-resolver` to audit filing coverage,
context actionability, and eval pass rate?"

Do not duplicate the resolver audit dimensions here — `check-resolver` is the
single source of truth for routing quality, the same way `check-skill` is for
skills. The lint script's own resolver check is intentionally narrow: it only
warns when no `RESOLVER.md` exists but the repo crosses the threshold.

## Anti-Pattern Guards

1. **Attributing pre-existing issues to recent changes** — a project may have accumulated failures before your work began. Establish a baseline before blaming new issues on recent changes. Run lint on the main branch first, then compare.
2. **Dismissing warn-tier findings** — warns that are never enforced become noise that teams learn to ignore. Each warn represents degradation; a project with 50 active warns is not "clean." Address warns or explicitly accept them with a rationale.
3. **Using --strict as a substitute for fixing root causes** — `--strict` promotes all warnings to failures, which is appropriate for CI gating. Using it to artificially block progress without fixing the underlying issues is not.
4. **Skipping individual error messages** — lint output is not a pass/fail score; it is a diagnostic. Every issue entry specifies a file, line, and reason. Reading the summary number without reading the individual issues skips the diagnostic value entirely.

## Handoff

**Receives:** Project root path (defaults to CWD); optional flags (--urls, --strict)
**Produces:** Validation report listing warnings and failures by file; read-only — no modifications made
**Chainable to:** `/build:check-skill` (per-skill quality); `/build:check-resolver` (routing-artifact audit when RESOLVER.md exists); `/build:build-resolver` (when threshold is crossed without one)
