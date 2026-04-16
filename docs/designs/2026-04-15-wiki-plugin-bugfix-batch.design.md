---
name: Wiki Plugin Bugfix Batch
description: Fix 6 bugs in the wiki plugin — 4 root-caused in Python code, 2 in skill text only
type: design
status: approved
related:
  - plugins/wiki/skills/setup/SKILL.md
  - plugins/wiki/skills/ingest/SKILL.md
  - plugins/wiki/scripts/update_preferences.py
  - plugins/wiki/scripts/_bootstrap.py
  - plugins/wiki/src/wiki/agents_md.py
---

# Wiki Plugin Bugfix Batch

**Purpose:** Fix 6 bugs in the wiki plugin across issues #265–#270. No new features; scope is strictly the 6 open issues.

## Issues

| # | Title | Root cause location | Severity |
|---|-------|-------------------|----------|
| #265 | wiki:ingest error references `/wos:setup` | SKILL.md text | Low |
| #266 | wiki:setup step 3 references `reindex.py` (doesn't exist) | SKILL.md + missing script | Medium |
| #267 | Plugin scripts fail without `PYTHONPATH=src` and `python3` | `_bootstrap.py` sys.path bug | High |
| #268 | wiki:setup never creates `wiki/SCHEMA.md` or `wiki/_index.md` | SKILL.md missing step | High |
| #269 | `update_preferences.py` silently rewrites Areas table | `update_preferences.py` calls `discover_areas` as side-effect | Medium |
| #270 | Uncommitted-changes guard offers no actionable resolution | SKILL.md guard text vague | Low |

## Behavior by Issue

### #265 — ingest typo (text only)
Change `/wos:setup` → `/wiki:setup` in `skills/ingest/SKILL.md` Pre-Ingest error message.

### #266 — reindex.py doesn't exist (new script + skill text)
Create `scripts/reindex.py` that:
1. Walks the project finding directories that contain `.md` files (excluding `_index.md` itself)
2. For each such directory, reads each `.md` file and extracts `name` and `description` from frontmatter
3. Writes `<dir>/_index.md` — a markdown table of `| File | Description |` rows, sorted alphabetically
4. Updates the AGENTS.md areas table: preserves existing descriptions for known paths, uses path as fallback for new ones

Update `setup/SKILL.md` step 3 and `ingest/SKILL.md` post-ingest to call `python3 <plugin-scripts-dir>/reindex.py --root <project-root>`.

### #267 — _bootstrap.py sys.path bug (code)
`_bootstrap.py` inserts `plugin_root` (= `plugins/wiki/`) into sys.path, but the package lives at `plugins/wiki/src/wiki/`. Fix: also insert `plugin_root / "src"` so scripts work without a prior editable install.

Also update all `python` → `python3` references in skill files.

### #268 — setup never creates wiki infrastructure (skill text)
Add a step (numbered 2.8, between current steps 2 and 3) to `setup/SKILL.md`:
- Create `wiki/` directory if missing
- Create `wiki/SCHEMA.md` from `references/wiki-schema-template.md` if missing
- Create `wiki/_index.md` with empty page inventory header if missing
- Idempotent: skip any file that already exists

### #269 — update_preferences.py destroys Areas table (code)
Root cause: `update_preferences.py` calls `discover_areas(root)` and passes it to `update_agents_md`, which re-renders the entire areas table with bare paths in both name and description columns.

Fix:
1. Add `extract_areas(content: str) -> List[Dict[str, str]]` to `agents_md.py` — parses the existing `### Areas` table, returning `{"name": <col1>, "path": <col2>}` dicts
2. Make `areas` parameter in `update_agents_md` optional (default `None`). When `None`, call `extract_areas` to preserve existing table content. Existing callers that supply `areas` explicitly are unaffected.
3. Remove `discover_areas` call from `update_preferences.py`

### #270 — uncommitted-changes guard vague (skill text)
Update anti-pattern guard #1 in `setup/SKILL.md`:
- Scope check to tracked modified files only (check `git diff --name-only HEAD`, not untracked files)
- Untracked files alone: advisory note, not a blocking gate
- When tracked modifications are found: suggest `git stash`, explain why (post-setup git diff becomes ambiguous; if setup fails partway, recovery state is unclear)

## Components

**New files:**
- `plugins/wiki/scripts/reindex.py`
- `plugins/wiki/tests/test_reindex.py`

**Modified files:**
- `plugins/wiki/scripts/_bootstrap.py` — add `src/` to sys.path
- `plugins/wiki/scripts/update_preferences.py` — remove `discover_areas` call
- `plugins/wiki/src/wiki/agents_md.py` — add `extract_areas`; make `areas` optional in `update_agents_md`
- `plugins/wiki/skills/setup/SKILL.md` — add step 2.8; fix step 3 ref; improve guard #1; `python3`
- `plugins/wiki/skills/ingest/SKILL.md` — fix `/wos:setup`; fix post-ingest reindex ref; `python3`
- `plugins/wiki/tests/test_agents_md.py` — add `extract_areas` tests; `update_agents_md(areas=None)` tests
- `plugins/wiki/tests/test_update_preferences.py` — update `test_preserves_areas` to match new behavior

## Acceptance Criteria

1. `python3 plugins/wiki/scripts/update_preferences.py --root . directness=blunt` — Preferences section updated, Areas table unchanged
2. `python3 plugins/wiki/scripts/reindex.py --root .` — `_index.md` created in each directory with `.md` files; AGENTS.md areas table updated with existing descriptions preserved
3. Any `scripts/*.py` invocation — no `ModuleNotFoundError` without prior `pip install -e .`
4. `/wiki:setup` on a fresh project → `wiki/SCHEMA.md` and `wiki/_index.md` created
5. `/wiki:ingest` missing-wiki error says `/wiki:setup`, not `/wos:setup`
6. All existing tests pass; new tests cover `extract_areas`, `update_agents_md(areas=None)`, and `reindex.py`

## Out of Scope

- `wiki/_index.md` regeneration during reindex (wiki page inventory is managed by ingest)
- Changes to `lint`, `research`, or other skills
- Changing AGENTS.md format or WOS section structure
- Preserving human edits to `_index.md` across reindex runs
