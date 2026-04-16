---
name: Wiki Plugin Bugfix Batch
description: Fix 6 bugs in the wiki plugin covering broken scripts, missing wiki init, stale skill text, and silent data loss
type: plan
status: executing
branch: fix/wiki-plugin-bugfix-batch
related:
  - docs/designs/2026-04-15-wiki-plugin-bugfix-batch.design.md
---

# Wiki Plugin Bugfix Batch

## Goal

Fix 6 bugs filed as issues #265–#270, all in the wiki plugin. The fixes restore correct behavior for `wiki:setup`, `wiki:ingest`, and the scripts backing them. Users following skill instructions verbatim should reach working state on a fresh project after these changes.

## Scope

Must have:
- Fix `/wos:setup` typo in ingest SKILL.md (#265)
- Create `scripts/reindex.py`; update SKILL.md refs from nonexistent `reindex.py` (#266)
- Fix `_bootstrap.py` to add `src/` to sys.path; update skill text to say `python3` (#267)
- Add wiki infrastructure creation step to setup SKILL.md (#268)
- Add `extract_areas` to `agents_md.py`; make `areas` optional in `update_agents_md`; remove `discover_areas` from `update_preferences.py` (#269)
- Improve uncommitted-changes guard in setup SKILL.md (#270)
- All existing tests pass; new tests for `extract_areas`, `update_agents_md(areas=None)`, `reindex.py`

Won't have:
- `wiki/_index.md` regeneration during reindex (wiki page inventory is managed by ingest, not reindex)
- Changes to `lint`, `research`, or any other skills
- Changing AGENTS.md format or WOS section structure
- Preserving human edits to `_index.md` files across reindex runs (first write wins)

## Approach

Six issues split across two tracks. Track 1 (task 1): skill text fixes to SKILL.md files only — typo, wiki init step, guard language, python3 refs. Track 2 (tasks 2–5): Python code fixes with tests. Task 6 closes the loop by updating SKILL.md references to the newly-created `reindex.py`. Tasks are ordered so code changes land before the skill text that references them: `extract_areas` added before `update_preferences.py` is changed to rely on it; `reindex.py` created before SKILL.md references it.

## File Changes

- Create: `plugins/wiki/scripts/reindex.py`
- Create: `plugins/wiki/tests/test_reindex.py`
- Create: `docs/designs/2026-04-15-wiki-plugin-bugfix-batch.design.md` (done)
- Modify: `plugins/wiki/scripts/_bootstrap.py` (add `src/` to sys.path)
- Modify: `plugins/wiki/scripts/update_preferences.py` (remove `discover_areas` call)
- Modify: `plugins/wiki/src/wiki/agents_md.py` (add `extract_areas`; make `areas` optional)
- Modify: `plugins/wiki/skills/setup/SKILL.md` (step 2.8, step 3 ref, guard #1, python3)
- Modify: `plugins/wiki/skills/ingest/SKILL.md` (typo fix, post-ingest reindex ref, python3)
- Modify: `plugins/wiki/tests/test_agents_md.py` (add extract_areas tests, areas=None tests)
- Modify: `plugins/wiki/tests/test_update_preferences.py` (update test_preserves_areas)

**Branch:** `fix/wiki-plugin-bugfix-batch`
**PR:** TBD

## Tasks

---

### Chunk 1: Skill Text Fixes

### Task 1: Fix SKILL.md text issues (#265, #268, #270, #267 python3)

Fix all issues that require only SKILL.md changes. No code changes in this task.

**Files:**
- Modify: `plugins/wiki/skills/ingest/SKILL.md`
- Modify: `plugins/wiki/skills/setup/SKILL.md`

- [x] In `skills/ingest/SKILL.md` Pre-Ingest section, change `/wos:setup` → `/wiki:setup` (line 35). <!-- sha:819d8eb -->
- [x] In `skills/ingest/SKILL.md` Post-Ingest section, change `python` → `python3` for both script calls. <!-- sha:819d8eb -->
- [x] In `skills/setup/SKILL.md` step 5, change `python` → `python3` for the `update_preferences.py` call. <!-- sha:819d8eb -->
- [x] In `skills/setup/SKILL.md`, add step **2.8 — Initialize wiki infrastructure** between step 2 and step 3. <!-- sha:819d8eb -->
- [x] In `skills/setup/SKILL.md`, update anti-pattern guard #1. <!-- sha:819d8eb -->
- [x] Verify: `grep -n "wos:setup" plugins/wiki/skills/ingest/SKILL.md` → no matches <!-- sha:819d8eb -->
- [x] Verify: `grep -n "python " plugins/wiki/skills/setup/SKILL.md plugins/wiki/skills/ingest/SKILL.md` → no bare `python ` (only `python3`) <!-- sha:819d8eb -->
- [x] Verify: `grep -n "2.8" plugins/wiki/skills/setup/SKILL.md` → wiki init step present <!-- sha:819d8eb -->
- [x] Verify: `grep -n "git stash" plugins/wiki/skills/setup/SKILL.md` → remediation hint present <!-- sha:819d8eb -->
- [x] Commit: `fix: skill text fixes — typo, wiki init step, guard improvement, python3 refs (#265 #268 #270 #267)` <!-- sha:819d8eb -->

---

### Chunk 2: Code Fixes

### Task 2: Fix _bootstrap.py sys.path (#267)

`_bootstrap.py` inserts `plugin_root` (`plugins/wiki/`) into sys.path, but the `wiki` package lives at `plugins/wiki/src/wiki/`. Scripts fail with `ModuleNotFoundError` unless an editable install is active.

**Files:**
- Modify: `plugins/wiki/scripts/_bootstrap.py`

- [x] After inserting `plugin_root` into sys.path, also insert `plugin_root / "src"` if it is a directory and not already in sys.path. Insert at position 0 (highest priority). <!-- sha:bd28cc1 -->
- [x] Verify: `cd plugins/wiki && python3 scripts/check_url.py --help` succeeds without `ModuleNotFoundError`. <!-- sha:bd28cc1 -->
- [x] Verify: `python -m pytest plugins/wiki/tests/test_script_syspath.py -v` passes (2 pre-existing failures about `check` module, unrelated to this fix; 1 passes). <!-- sha:bd28cc1 -->
- [x] Commit: `fix: _bootstrap.py — add src/ to sys.path so scripts work without editable install (#267)` <!-- sha:bd28cc1 -->

---

### Task 3: Add extract_areas and make areas optional in agents_md.py (#269)

Add `extract_areas` function and make `areas` optional in `update_agents_md`. When `areas=None`, the function preserves existing table content by calling `extract_areas` internally.

**Files:**
- Modify: `plugins/wiki/src/wiki/agents_md.py`
- Modify: `plugins/wiki/tests/test_agents_md.py`

**Depends on:** Task 2 (clean sys.path for test runner)

- [x] Add `extract_areas(content: str) -> List[Dict[str, str]]` to `agents_md.py`. <!-- sha:bef3a16 -->
- [x] Change `areas` parameter in `update_agents_md` to `Optional[List[Dict[str, str]]]` with default `None`. <!-- sha:bef3a16 -->
- [x] Add tests in `test_agents_md.py` (round-trip, human descriptions, no markers, no table, areas=None). <!-- sha:bef3a16 -->
- [x] Verify: `python -m pytest plugins/wiki/tests/test_agents_md.py -v` — 34 passed. <!-- sha:bef3a16 -->
- [x] Commit: `feat: agents_md — add extract_areas, make areas optional in update_agents_md (#269)` <!-- sha:bef3a16 -->

---

### Task 4: Fix update_preferences.py (#269)

Remove `discover_areas` call. After Task 3, passing `areas=None` preserves existing table content — no `discover_areas` side-effect.

**Files:**
- Modify: `plugins/wiki/scripts/update_preferences.py`
- Modify: `plugins/wiki/tests/test_update_preferences.py`

**Depends on:** Task 3

- [x] In `update_preferences.py`: remove `discover_areas` call; pass `areas=None` to `update_agents_md`. <!-- sha:1ee957d -->
- [x] Update `test_preserves_areas` → `test_preserves_existing_area_descriptions` to assert correct behavior. <!-- sha:1ee957d -->
- [x] Verify: `python -m pytest plugins/wiki/tests/test_update_preferences.py -v` — 4 passed. <!-- sha:1ee957d -->
- [x] Verify: `python -m pytest plugins/wiki/tests/` — 233 pass (pre-existing lint/syspath failures unchanged). <!-- sha:1ee957d -->
- [x] Commit: `fix: update_preferences.py — remove discover_areas side-effect, preserve existing areas (#269)` <!-- sha:1ee957d -->

---

### Task 5: Create reindex.py (#266)

Create a standalone script that creates `_index.md` files in all directories containing `.md` files, and updates the AGENTS.md areas table using `extract_areas` to preserve existing descriptions.

**Files:**
- Create: `plugins/wiki/scripts/reindex.py`
- Create: `plugins/wiki/tests/test_reindex.py`

**Depends on:** Task 3 (needs `extract_areas` and `update_agents_md(areas=...)`)

- [x] Create `plugins/wiki/scripts/reindex.py` (scope limited to AGENTS.md areas table; docs/ fallback on first run). <!-- sha:e86f9f2 -->
- [x] `reindex.py` does NOT index dirs outside the areas table; wiki/_index.md untouched. <!-- sha:e86f9f2 -->
- [x] Create `test_reindex.py` (11 tests). <!-- sha:e86f9f2 -->
- [x] Verify: `python -m pytest plugins/wiki/tests/test_reindex.py -v` — 11 passed. <!-- sha:e86f9f2 -->
- [x] Verify: `python3 plugins/wiki/scripts/reindex.py --root .` indexes only 4 registered areas. <!-- sha:e86f9f2 -->
- [x] Commit: `feat: add reindex.py — create _index.md for WOS-registered areas only (#266)` <!-- sha:e86f9f2 -->

---

### Task 6: Update SKILL.md references to reindex.py (#266)

Update setup and ingest skills to call the now-existing `reindex.py`.

**Files:**
- Modify: `plugins/wiki/skills/setup/SKILL.md`
- Modify: `plugins/wiki/skills/ingest/SKILL.md`

**Depends on:** Task 5 (reindex.py must exist before SKILL.md references it)

- [ ] In `skills/setup/SKILL.md` step 3, replace the `reindex.py` description with the correct invocation: `python3 <plugin-scripts-dir>/reindex.py --root <project-root>`. Update the description to reflect what the script actually does (creates `_index.md` files in directories with managed documents; updates AGENTS.md areas table).
- [ ] In `skills/ingest/SKILL.md` Post-Ingest section, replace the `reindex.py` call with: `python3 <plugin-scripts-dir>/reindex.py --root <project-root>`.
- [ ] Verify: `grep -n "reindex.py" plugins/wiki/skills/setup/SKILL.md plugins/wiki/skills/ingest/SKILL.md` → both reference it correctly
- [ ] Verify: `python -m pytest plugins/wiki/tests/ -v` — full suite still passes (no regressions)
- [ ] Commit: `fix: update SKILL.md refs to use reindex.py now that script exists (#266)`

---

## Validation

- [ ] `python -m pytest plugins/wiki/tests/ -v` — all tests pass, including new ones for `extract_areas`, `update_agents_md(areas=None)`, and `reindex.py`
- [ ] `python3 plugins/wiki/scripts/update_preferences.py --root . directness=blunt` (run in this repo) — `AGENTS.md` Preferences section updated; Areas table unchanged (verify with `git diff`)
- [ ] `python3 plugins/wiki/scripts/reindex.py --root .` (run in this repo) — `_index.md` files created in `docs/context/`, `docs/plans/`, etc.; AGENTS.md updated; `wiki/_index.md` not created or touched
- [ ] `grep "wos:setup" plugins/wiki/skills/ingest/SKILL.md` → no output
- [ ] `grep "git stash" plugins/wiki/skills/setup/SKILL.md` → line present
- [ ] `grep "2.8" plugins/wiki/skills/setup/SKILL.md` → wiki init step present

## Notes
<!-- Decisions made during execution, scope adjustments, lessons learned -->
