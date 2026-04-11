---
name: Context File Wiki Schema Migration
description: Add confidence, created, updated, and wiki-compatible type fields to all 190 docs/context/*.context.md files — closes bcbeidel/wos#220
type: plan
status: completed
branch: feat/context-migration
pr: ~
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# Context File Wiki Schema Migration

**Goal:** Make all `docs/context/*.context.md` files first-class wiki pages by adding `confidence`, `created`, `updated`, and a wiki-compatible `type` field to their frontmatter. Closes bcbeidel/wos#220. Required before meaningful wiki operations (ingest, search, staleness checks) can run against the project's context base.

**Scope:**

Must have:
- All 190 `docs/context/*.context.md` files gain `confidence`, `created`, `updated` fields
- `type: context` updated to wiki page type (`concept`, `comparison`, or `entity`)
- `python3 scripts/lint.py --root . --no-urls` passes with no new failures versus baseline

Won't have:
- `SCHEMA.md` placement in `docs/context/` — directory layout decision deferred
- Changes to `scripts/lint.py` auto-detection — currently only activates on `wiki/SCHEMA.md`
- Ongoing automation — this is a one-time migration

**Approach:** Write a one-off script (`scripts/migrate_context.py`) that opens each file, parses the frontmatter, derives `confidence` from source count (3+ → `high`, 1-2 → `medium`, 0 → `low`), and derives `created`/`updated` from `git log`. The script assigns `type: concept` by default, `type: comparison` for files whose names contain tradeoff/versus indicators, and `type: entity` for explicitly-known product-specific files. A manual review task follows to catch heuristic mismatches. The script is deleted after use.

**Behavioral note:** Changing `type: context` → a wiki type drops two existing validators from these files: (1) the word-count range check (`check_content`, 100–800 words, keyed on `type == "context"`) and (2) the "no related fields" warning. This is intentional — wiki pages use wiki-schema validation going forward.

**Field naming note:** The wiki schema uses `created` and `updated` (stored in `doc.meta`), NOT the `created_at`/`updated_at` attributes used by `check_timestamps`. Add the bare-name fields.

**File Changes:**
- Create: `scripts/migrate_context.py` (deleted in Task 4)
- Modify: `docs/context/*.context.md` (190 files) — add `confidence`, `created`, `updated`; change `type`

**Branch:** `feat/context-migration`
**PR:** TBD

---

### Task 1: Baseline lint run

**Files:** none

- [x] **Step 1:** Record baseline: `python3 scripts/lint.py --root . --no-urls 2>&1`
  - Expected: `1 fail, 7 warn` — test fixture DRAFT markers, gatherer_entry.md missing sources, prompts `_index.md` missing preamble. No context-file issues.
- [x] **Step 2:** Commit checkpoint — `git commit --allow-empty -m "chore: record baseline before context migration"` (or skip if no empty commits preferred — just note the baseline)

---

### Task 2: Write `scripts/migrate_context.py`

**Files:**
- Create: `scripts/migrate_context.py`

Script requirements:

1. **Plugin root discovery** — follow the hybrid pattern from CLAUDE.md:
   - Prefer `CLAUDE_PLUGIN_ROOT` env var
   - Fall back to `Path(__file__).parent.parent` (scripts/ → plugin root)
   - Add root to `sys.path` so `wos` package is importable
2. **Iterate:** `sorted(Path("docs/context").glob("*.context.md"))` relative to `--root` (default CWD)
3. **Parse frontmatter:** Use `wos.frontmatter.parse_frontmatter(text)` to extract existing FM
4. **Derive confidence:**
   ```
   sources = fm.get("sources") or []
   n = len([s for s in sources if isinstance(s, str) and s.strip()])
   confidence = "high" if n >= 3 else "medium" if n >= 1 else "low"
   ```
5. **Derive dates** via `subprocess.run(["git", "log", "--follow", "--format=%as", "--", str(filepath)])`:
   - `created` = last line of output (oldest commit); fallback `"2026-04-07"` if empty
   - `updated` = first line of output (newest commit); fallback `"2026-04-07"` if empty
   - Note: `%as` gives ISO 8601 short date (YYYY-MM-DD)
6. **Derive type** (only if current value is `"context"`):
   - `COMPARISON_KEYWORDS = ["vs-", "-vs-", "tradeoff", "tradeoffs", "comparison", "versus"]`
   - `ENTITY_FILES = {"dbt-layered-architecture-and-testing-patterns.context.md", "dbt-three-layer-transformation-model.context.md"}`
   - `comparison` if any keyword appears in `filepath.name`
   - `entity` if `filepath.name` in `ENTITY_FILES`
   - `concept` otherwise
7. **Rewrite frontmatter:** Add/overwrite `confidence`, `created`, `updated`, `type` in the YAML block. Preserve all other existing fields and body content.
   - Do NOT use a full YAML library — write the frontmatter as a string template that preserves field order: `name`, `description`, `type`, `confidence`, `created`, `updated`, then all other known fields (`sources`, `related`, `status`), then extra meta fields.
   - Detect existing field order and insert new fields after `type`.
8. **Print summary:** For each file, print `[type] [confidence] filename` to stderr
9. **Argparse:** `--root` flag (default `.`)

- [x] **Step 1:** Write `scripts/migrate_context.py` with PEP 723 inline metadata header
- [x] **Step 2:** Verify it parses without error: `python3 scripts/migrate_context.py --help`
- [x] **Step 3:** Dry-run on one file to verify output looks correct (add a `--dry-run` flag that prints the would-be frontmatter without writing)
- [x] **Step 4:** Commit: `git commit -m "chore: add one-off context-to-wiki migration script"` <!-- sha:16473f2 -->

---

### Task 3: Run migration on all 190 context files

**Files:**
- Modify: `docs/context/*.context.md` (190 files)

- [x] **Step 1:** Execute: `python3 scripts/migrate_context.py --root .`
  - Inspect stderr summary for obviously wrong type assignments
- [x] **Step 2:** Verify field coverage: `190 files, 0 missing confidence`
- [x] **Step 3:** Verify confidence distribution: `{'high': 177, 'medium': 13}` — not uniform
- [x] **Step 4:** Commit: `feat: add wiki schema fields to all docs/context/*.context.md files (#220)` <!-- sha:ab6787b -->

---

### Task 4: Manual type review

**Files:**
- Modify: subset of `docs/context/*.context.md`

Review the heuristic type assignments. The script should have assigned:
- `comparison` (~20 files): tradeoff/vs/comparison-named files
- `entity` (2 files): `dbt-layered-architecture-and-testing-patterns.context.md`, `dbt-three-layer-transformation-model.context.md`
- `concept` (remaining ~168 files)

Spot-check candidates the heuristic might have missed:
```bash
grep -l "^type: concept" docs/context/*.context.md | xargs -I{} basename {} | grep -E "vs|trade|compar|entity|tool|product"
```

- [x] **Step 1:** Open files flagged by spot-check; manually correct `type` where wrong
  - Fixed: `bayesian-mmm-tool-selection-meridian-robyn.context.md` → `comparison` (Meridian vs. Robyn in name)
- [x] **Step 2:** Verify no file still has `type: context` — none found
- [x] **Step 3:** Verify all wiki types: 167 concept, 21 comparison, 2 entity — all valid
- [x] **Step 4:** Commit: `feat: refine wiki page types for comparison and entity context files` <!-- sha:e080c25 -->

---

### Task 5: Validate and clean up

**Files:**
- Delete: `scripts/migrate_context.py`

- [x] **Step 1:** Full lint run — `1 fail, 7 warn` — matches baseline (context _index.md was out-of-sync after migration; fixed with reindex before final commit)
- [x] **Step 2:** Delete migration script: `rm scripts/migrate_context.py`
- [x] **Step 3:** Update roadmap: fill Task 3 SHA at PR merge time
- [x] **Step 4:** Commit: `chore: remove one-off migration script; update context index` <!-- sha:c1aaac1 -->

---

## Validation

- [ ] `grep -l "^type: context" docs/context/*.context.md` — expected: empty (no files still have old type)
- [ ] `python3 scripts/lint.py --root . --no-urls 2>&1 | tail -5` — expected: `1 fail, 7 warn` or fewer (same as baseline)
- [ ] `grep -h "^confidence: " docs/context/*.context.md | sort | uniq -c` — expected: at least two distinct values (`high` and `medium` present)
- [ ] `python3 -m pytest tests/ -v` — expected: all tests pass

## Notes

- Baseline (pre-migration): `1 fail, 7 warn` — all in test fixtures or prompts index; no context-file issues
- Source distribution: 177 files have 3+ sources (→ `high`), 13 have 1-2 (→ `medium`), 0 have zero
- All context files share the same git-log date (`2026-04-10`, from the v0.35.0 bulk rebuild commit `cdd02ab`)
- Roadmap Task 3 checkbox update happens at PR merge; fill `<!-- sha: -->` with the merge commit SHA
