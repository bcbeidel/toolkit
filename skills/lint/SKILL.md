---
name: lint
description: >
  Runs lint checks on project content quality and reports frontmatter, URL,
  index, and skill issues. Use when the user asks to "lint", "run lint",
  "check lint", "check health", "validate documents", "run validation",
  "audit content quality", "review documents", "check coverage",
  "check freshness", "run health check", or "what needs attention".
argument-hint: "[lint|check|review|coverage|freshness]"
user-invocable: true
references:
  - references/skill-authoring-guide.md
---

# Audit Skill

Observe and report on project content quality. Read-only -- reports but
does not modify any files (unless `--fix` is used for index regeneration).

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

# Auto-fix out-of-sync or missing _index.md files
python <plugin-scripts-dir>/lint.py --root . --fix

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
Artifacts and `_index.md` files are excluded.

### 3. Source URL Reachability (fail + warn)

Checks that every URL in `sources` is reachable via HTTP.
Skipped with `--no-urls`. URLs returning 403/429 are downgraded to
`warn` — these sites likely block automated checks, not dead links.

### 4. Related Path Validation (fail)

Checks that local file paths in `related` exist on disk.

### 5. Index Sync (fail + warn)

- **fail:** `_index.md` missing or out of sync
- **warn:** `_index.md` has no area description (preamble)

## Interpreting Results

Summary line first, then table:

```
2 fail, 1 warn across 15 files

file                              | sev  | issue
docs/context/api/auth.md           | fail | Frontmatter 'name' is empty
docs/context/api/_index.md        | warn | Index has no area description (preamble)
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

- **Missing AGENTS.md or CLAUDE.md:** Offer to run `/wos:setup` to
  initialize. Confirm with the user before writing any files.
- **AGENTS.md missing WOS markers:** Offer to run `/wos:setup` to add
  the WOS-managed section. Confirm before modifying existing content.
- **CLAUDE.md missing @AGENTS.md reference:** Offer to add the reference.
  Do not rewrite CLAUDE.md contents — only add the `@AGENTS.md` line.
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

## Key Rules

- Audit is read-only (except `--fix` which only regenerates `_index.md` files)
- Use `/wos:setup` to initialize missing project structure
- Empty project (no `docs/` directory) exits 0 with no issues

## Skill Evaluation

When audit encounters a skill directory (a directory containing `SKILL.md`),
it runs two layers of checks:

1. **Automated checks** (Python) — name format, description length/voice,
   body size, instruction density. These appear in the standard issue table.

2. **Judgment checks** (guided by this section) — evaluate the skill against
   the criteria in [skill-authoring-guide.md](references/skill-authoring-guide.md).

For judgment checks, read the target skill's SKILL.md and references, then
evaluate against the "Judgment" criteria table in the guide. Report findings
with explanations that reference the relevant guide section.

Present judgment findings as a narrative after the automated results:

```
Skill Evaluation: [skill-name]

- **Description triggers:** [finding + explanation]
- **Description breadth:** [finding + explanation]
- **Freedom ↔ fragility:** [finding + explanation]
- **Rationale over rigidity:** [finding + explanation]
- **Unnecessary context:** [finding + explanation]
- **Token-earning:** [finding + explanation]
- **Generality:** [finding + explanation]
- **Examples:** [finding + explanation]
- **Terminology:** [finding + explanation]
- **Reference depth:** [finding + explanation]
```

Only report issues — if a criterion passes, omit it.

## Anti-Pattern Guards

1. **Attributing pre-existing issues to recent changes** — a project may have accumulated failures before your work began. Establish a baseline before blaming new issues on recent changes. Run lint on the main branch first, then compare.
2. **Dismissing warn-tier findings** — warns that are never enforced become noise that teams learn to ignore. Each warn represents degradation; a project with 50 active warns is not "clean." Address warns or explicitly accept them with a rationale.
3. **Using --strict as a substitute for fixing root causes** — `--strict` promotes all warnings to failures, which is appropriate for CI gating. Using it to artificially block progress without fixing the underlying issues is not.
4. **Skipping individual error messages** — lint output is not a pass/fail score; it is a diagnostic. Every issue entry specifies a file, line, and reason. Reading the summary number without reading the individual issues skips the diagnostic value entirely.

## Handoff

**Receives:** Project root path (defaults to CWD); optional flags (--no-urls, --strict, --fix)
**Produces:** Validation report listing warnings and failures by file; read-only — no modifications made
**Chainable to:** —
