---
name: check-readme
description: >
  Audits a project's top-level README.md against ~28 deterministic
  checks across seven scripts (secret scanning, H1 uniqueness &
  position, heading-hierarchy skips, section presence & order, TOC
  threshold, line count & length, code-block language tags,
  shell-prompt prefixes, smart quotes in code, relative-link
  resolution, fragment-anchor resolution, image alt text,
  badge/image byte size, destructive-command flagging, pipe-to-shell
  patterns, TLS-disable instructions, non-reserved
  hostnames/IPs, emoji in headings, LICENSE file presence & link,
  CONTRIBUTING link, TODO/FIXME/XXX markers, README gitignore
  status) plus seven judgment dimensions. Use when the user wants
  to "audit a README", "check this README", "review my README",
  "lint a README", "is this README any good", "what's wrong with
  the README", or "run linters on README.md". Not for sub-package
  READMEs (different rubric) or docs-site pages (different
  toolchain).
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/readme-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
license: MIT
---

# Check README

Audit a project's top-level `README.md` for structural soundness,
safety, completeness, and adherence to the rubric. The rubric — what a
good README does, the anatomy, the patterns that work — lives in
[readme-best-practices.md](../../_shared/references/readme-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — seven
scripts run per target and emit fixed-format findings, wrapping
`markdownlint` / `lychee` / `gitleaks` where available and degrading
gracefully when absent. **Tier-2** is a single locked-rubric LLM call
per target evaluating all seven [audit
dimensions](references/audit-dimensions.md) at once; dimensions that
don't apply return PASS silently. **Tier-3** is cross-entity collision
detection — when the scope holds multiple READMEs (unusual but
possible in a monorepo scan), flag content-overlap the maintainer
could consolidate upstream.

Read-only by default. The opt-in repair loop applies fixes only after
per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Cross-Entity Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `README.md` file** — audit that file.
- **Directory path** — resolve to `<dir>/README.md` and audit that.
  Do not recurse — sub-package READMEs are out of scope and carry a
  different rubric.
- **Empty** — default to `./README.md` at the current working
  directory; refuse if it is absent.

Confirm the scope aloud before proceeding ("Auditing
`<path>` (1 README)").

### 2. Tier-1 Deterministic Checks

Run seven scripts in sequence against the target. Each exits `0` on
clean / WARN / INFO and `1` on one or more FAIL; do not stop on any
script's FAIL exit — all seven contribute findings to the merge.

```bash
SCRIPTS="${SKILL_DIR}/scripts"
TARGET="$ARGUMENTS"

"$SCRIPTS/check_secrets.py"      "$TARGET"   # FAIL: secret patterns — excludes from Tier-2
"$SCRIPTS/check_structure.py"    "$TARGET"   # FAIL: missing/multiple H1; WARN: hierarchy, section coverage, section order, TOC threshold, size
"$SCRIPTS/check_codeblocks.py"   "$TARGET"   # WARN: missing language tag, shell prompts, smart quotes, line length
"$SCRIPTS/check_links.py"        "$TARGET"   # FAIL: broken relative links; WARN: broken anchors, external URL 4xx/5xx
"$SCRIPTS/check_images.py"       "$TARGET"   # WARN: missing/placeholder alt text, oversized images, badge overload
"$SCRIPTS/check_safety.py"       "$TARGET"   # FAIL: destructive-without-warning, pipe-to-shell unguarded, TLS-disable, non-reserved hosts/IPs; WARN: emoji in headings
"$SCRIPTS/check_completeness.py" "$TARGET"   # FAIL: no LICENSE file + link; WARN: no CONTRIBUTING link, TODO/FIXME/XXX markers, README gitignored
```

The scripts live next to `SKILL.md` under `scripts/` and are
authored separately via `/build:build-python-script` per the
Language Selection section of `primitive-routing.md` (all seven
parse Markdown AST and return structured findings — Python wins on
interpretability over bash for this workload).

**Script-to-check map** (full check list per script):

| Script | Checks |
|---|---|
| `check_secrets.py` | API keys, tokens, private URLs via regex pattern list; optional `gitleaks`/`detect-secrets` wrapper |
| `check_structure.py` | Single H1 on first content line (after frontmatter); no skipped heading levels (MD001); standard H2 sections present (Installation, Usage, License minimum); H2 sequence matches reader-intent order; TOC present when rendered document > 400 lines; total line count; prose line length ≤ 120 |
| `check_codeblocks.py` | Every fenced block carries a non-empty language info-string (MD040); no shell-prompt prefixes (`$`, `>`, `#`) in `bash`/`sh`/`console` blocks; no smart quotes or em/en-dash inside code blocks; code-block line length ≤ 80 |
| `check_links.py` | Every relative link resolves to an existing file; every fragment link matches a heading slug; optional wrapper for `lychee` / `markdown-link-check` to verify external URLs |
| `check_images.py` | Every image has non-empty, non-placeholder alt text (MD045); embedded images < 500 KB each, total < 2 MB; ≤ 5 badges in the prelude |
| `check_safety.py` | Destructive commands (`rm -rf`, `dd if=`, `mkfs`, `DROP DATABASE`, `--force`) in fenced blocks without an adjacent warning; `curl ... \| sh` / `wget ... \| bash` / `iex (iwr ...)` patterns without a manual alternative; instructions to disable TLS / SELinux / firewall; hostnames/IPs outside reserved ranges (`example.com`, `*.test`, `*.local`, `127.0.0.1`, RFC 5737); emoji code points in heading text |
| `check_completeness.py` | A `LICENSE` file exists in the repo root; README contains a link to `LICENSE` and a heading matching `/license/i`; README contains a Contributing section or link to `CONTRIBUTING.md`; no `TODO`/`FIXME`/`XXX` markers in the published document; README.md not listed in `.gitignore` |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing required dependency (optional tools like `gitleaks`,
`lychee`, `markdownlint` degrade gracefully — they emit a
`tool-missing` INFO and exit 0).

**FAIL findings that exclude the file from Tier-2** (evaluation is
not useful until these are resolved):

- Any finding from `check_secrets.py` (secrets present).
- `check_structure.py` FAILs on missing or multiple H1 — the
  document has no anchor; judgment dimensions lose their fix point.
- `check_safety.py` FAILs on destructive-without-warning,
  unguarded pipe-to-shell, TLS-disable instructions, or
  non-reserved hosts/IPs — these are safety bugs that bias every
  judgment dimension toward false negatives.
- `check_completeness.py` FAIL on missing LICENSE file — the
  project is structurally incomplete; re-run after license is
  added.

**FAIL findings that do NOT exclude from Tier-2:** broken relative
links leave a parseable document that judgment can still evaluate
productively; they surface in the report alongside Tier-2 findings.

**WARN / INFO / HINT findings never exclude.**

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the audit rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together — no trigger gating. A dimension that does
not apply returns PASS silently.

The seven dimensions:

| Dimension | What it judges |
|---|---|
| D1 Opening Clarity | Does the H1 + one-sentence description + problem statement answer "what is this and should I care" in the top 30 seconds for a stranger? |
| D2 Installation Correctness | Prerequisites list is complete and versioned; install commands would actually succeed on a clean machine; platform coverage matches stated support |
| D3 Quickstart Effectiveness | Is the minimal example genuinely minimal and genuinely runnable? Does it produce visible output? Is expected output shown? |
| D4 Placeholder Discipline | Are `<PLACEHOLDER>` tokens clearly marked, defined once, consistently used, and distinct from real values? No undefined placeholders; no real values masquerading as placeholders |
| D5 Warning Prominence | Are destructive-op, pipe-to-shell, and security-weakening warnings prominent (callouts / blockquotes / bold) rather than buried prose? |
| D6 Maintenance Posture | Staleness indicators: commands that probably no longer work, hand-maintained `--help` duplicates, version numbers that look out-of-date, duplicated content from `CONTRIBUTING.md` / `ARCHITECTURE.md`, "coming soon" links |
| D7 Style & Voice | Imperative mood and second person for instructions; clear direct language; jargon defined on first use; no emoji in headings; prose lines ≤ 120 chars |

Feed the file contents plus any Tier-1 HINT lines (e.g., repo-name
context, distribution channel if detectable) into the prompt. Parse
the model's response into the fixed lint format (one finding per
dimension at most; PASS produces no finding).

### 4. Tier-3 Cross-Entity Collision

When the scope holds multiple READMEs (monorepo scan, multi-project
audit), check for content overlap that should be consolidated:

- Identical or near-identical install / usage sections across top-level
  READMEs in related projects (candidate for a shared docs page).
- Identical license / contributing boilerplate (candidate for an org-level
  default).

Report collisions as INFO findings — maintainer guidance, not
failures. Single-README scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN > INFO
> HINT), then by file path. Deduplicate exact-match findings at merge
time — `markdownlint` may emit the same rule code from multiple lines,
informative the first time and noise after.

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

Summary line at top and bottom: `N fail, N warn, N info across N
READMEs`. If any file was excluded from Tier-2, name it and the
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

1. **Running Tier-2 before Tier-1** — deterministic checks are cheap
   and authoritative.
2. **Trigger-gating Tier-2 dimensions** — all seven run always. A
   dimension that doesn't apply returns PASS silently.
3. **Applying all repair fixes in one batch** — per-finding
   confirmation is required.
4. **Recursing into sub-package READMEs** — out of scope; different
   rubric. Top-level only.
5. **Skipping the re-run after a fix** — a fix that introduces a new
   finding elsewhere is more common than it sounds.
6. **Suppressing missing-tool INFOs** — when `markdownlint` / `lychee`
   / `gitleaks` are absent, the INFO line is the user's signal that
   coverage is reduced.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files that
  passed the Tier-2-exclusion filter.
- All seven Tier-2 dimensions evaluate on every non-excluded file.
- Repairs require per-finding confirmation.
- When `markdownlint` / `lychee` / `gitleaks` are absent, the wrapper
  emits an INFO line naming reduced coverage and exits 0.
- Won't modify files without per-change confirmation — read-only by
  default.
- Won't audit paths outside `$ARGUMENTS`.
- Won't audit sub-package READMEs — out of scope.
- Recovery if a repair edit produces a worse state: single-file
  change; revert with `git checkout -- <path>`.

## Handoff

**Receives:** Path to a single `README.md` at a repository root (or
a directory resolving to one).

**Produces:** Structured findings table in the lint format
(`SEVERITY  <path> — <check>: <detail>` with a `Recommendation:`
follow-up line); optionally, targeted edits applied after per-finding
confirmation.

**Chainable to:** `/build:build-readme` (rebuild from scratch after
flagged repairs if the repair loop surfaces structural issues bigger
than point fixes).
