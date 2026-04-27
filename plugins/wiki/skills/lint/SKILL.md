---
name: lint
description: >
  Runs lint checks on project content quality and reports frontmatter, URL,
  index, and skill issues. Use when the user asks to "lint", "run lint",
  "check lint", "check health", "validate documents", "run validation",
  "audit content quality", "review documents", "check coverage",
  "check freshness", "run health check", or "what needs attention".
argument-hint: "[path/to/file.md]"
user-invocable: true
references: []
---

# Audit Skill

Observe and report on project content quality. Read-only -- reports but
does not modify any files.

## Workflow

1. **Run** `lint.py` against the project root (see [How to Run](#how-to-run))
2. **Checks** — the script applies five check categories; results are collected (see [The Checks](#the-checks))
3. **Interpret** — present the findings table to the user (see [Interpreting Results](#interpreting-results))
4. **Cleanup** — for actionable findings (missing setup, blocked URLs), offer guided resolution (see [Cleanup Actions](#cleanup-actions))

Each phase depends on the previous. Do not offer cleanup actions before presenting results.

## How to Run

```bash
# Default: run all checks including URL reachability
python <plugin-scripts-dir>/lint.py --root .

# Skip URL reachability checks (fast, offline-friendly)
python <plugin-scripts-dir>/lint.py --root . --no-urls

# Validate a single file
python <plugin-scripts-dir>/lint.py path/to/file.md --root . --no-urls

# JSON output for programmatic use
python <plugin-scripts-dir>/lint.py --root . --json

# Exit 1 on any issue (including warnings)
python <plugin-scripts-dir>/lint.py --root . --strict

# Custom word count threshold for context files (default: 800)
python <plugin-scripts-dir>/lint.py --root . --context-max-words 500
```

Exit code: 1 if any `fail`, 0 if only `warn`. Use `--strict` to exit 1 on any issue.

## The Checks

### 1. Frontmatter Validation (fail + warn)

Verifies:
- **fail:** `name` and `description` are non-empty
- **fail:** `type: research` documents have a non-empty `sources` list
- **warn:** Source items should be URL strings, not dicts
- **warn:** Context files should have `related` fields

### 2. Content Length (warn)

Warns when context files exceed 800 words (configurable via `--context-max-words`).
Artifacts are excluded.

### 3. Source URL Reachability (fail + warn)

Checks that every URL in `sources` is reachable via HTTP.
Skipped with `--no-urls`. URLs returning 403/429 are downgraded to
`warn` — these sites likely block automated checks, not dead links.

### 4. Related Path Validation (fail)

Checks that local file paths in `related` exist on disk.

### 5. Resolver Threshold (warn)

Warns when no `RESOLVER.md` exists at the project root but ≥3 top-level
directories follow a filing convention (≥2 files matching `*.context.md`,
`*.plan.md`, `*.design.md`, or `*.research.md`). The recommendation is to
run `/build:build-resolver`. Routing-artifact quality (when a resolver
*does* exist) is not checked here — see [Resolver Evaluation](#resolver-evaluation).

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
- **403/429 URL warnings:** Present each blocked URL to the user and ask
  them to verify it manually. For each URL:
  1. Show the URL and the file it appears in
  2. Ask the user to verify the URL. Offer these options:
     - **Visit in browser** and confirm it's still valid
     - **Provide a screenshot** of the page (drag/paste image)
     - **Provide a printed PDF** of the page (drag/paste file)
     - **Paste the page content** or a relevant excerpt
     - **Mark as dead** if the URL no longer works
  3. Based on response:
     - User confirms valid or provides content → no source change needed.
       If the user provided a screenshot, PDF, or pasted content, use it
       to verify the source is still relevant to the document. Note any
       discrepancies.
     - User says dead → offer to remove it from the document's `sources:`
       list. Show the proposed edit and get approval before writing.
     - User provides a replacement URL → offer to update the `sources:`
       entry. Verify the new URL with `python <plugin-scripts-dir>/check_url.py URL`
       before writing.

  Process URLs one at a time. Do not batch-ask about all URLs at once.

## Key Instructions

- Audit is strictly read-only — no log files, no side effects
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

**Receives:** Project root path (defaults to CWD); optional flags (--no-urls, --strict)
**Produces:** Validation report listing warnings and failures by file; read-only — no modifications made
**Chainable to:** `/build:check-skill` (per-skill quality); `/build:check-resolver` (routing-artifact audit when RESOLVER.md exists); `/build:build-resolver` (when threshold is crossed without one)
