---
name: "Merge preferences into init, consolidate on AGENTS.md"
description: "Roll /wos:preferences into /wos:init and make AGENTS.md the single delivery mechanism"
type: plan
related:
  - docs/plans/2026-03-05-init-wos-design.md
  - docs/plans/2026-03-05-init-wos-implementation.md
---

# Merge Preferences into Init

## Summary

Roll `/wos:preferences` into `/wos:init` and eliminate the standalone skill.
All WOS-managed content lives in AGENTS.md. CLAUDE.md becomes a thin pointer
(`@AGENTS.md`).

## Motivation

- **Too many skills for simple operations** — preferences is a 4-step workflow
  that init can absorb naturally as part of bootstrap
- **CLAUDE.md vs AGENTS.md split is confusing** — preferences currently writes
  to CLAUDE.md with its own markers while everything else goes to AGENTS.md
- **One delivery mechanism** — AGENTS.md is the content, CLAUDE.md is the pointer

## Design Decisions

- **Always ask about preferences during init** — not just first run. If
  preferences already exist, show current settings and offer to update.
- **Delete `/wos:preferences` entirely** — no redirect, no thin wrapper. Init
  is the only entry point.
- **Preferences render inside the WOS section** — `render_wos_section()`
  already accepts a `preferences` parameter. Captured preferences feed through
  this existing pipeline.
- **`update_preferences.py` takes `--root`** — re-discovers areas from disk,
  re-renders the full WOS section with updated preferences. Consistent with
  how `reindex.py` works.
- **Init manages CLAUDE.md pointer** — if CLAUDE.md doesn't reference
  `@AGENTS.md`, init creates/adds it. Part of complete bootstrap.

## Changes

### 1. Expand `/wos:init` SKILL.md

Add two workflow steps:

- **Preferences capture** (after AGENTS.md update): If no `### Preferences`
  subsection exists → run full capture workflow (ask freeform → map dimensions
  → confirm → write). If preferences exist → show current, offer to update.
- **CLAUDE.md pointer** (final step): If CLAUDE.md doesn't exist or doesn't
  reference `@AGENTS.md`, create/add the pointer.

Move `capture-workflow.md` reference into `skills/init/references/`.

### 2. Rework `wos/preferences.py`

- **Keep:** `DIMENSIONS`, `DIMENSION_INSTRUCTIONS`, `_DISPLAY_NAMES`,
  `render_preferences()`
- **Delete:** `COMM_MARKER_BEGIN`, `COMM_MARKER_END`, `update_preferences()`
- The rendered preference strings become input to
  `render_wos_section(preferences=...)`

### 3. Rework `scripts/update_preferences.py`

Change from writing to CLAUDE.md with its own markers to:

1. Accept `--root` (project root, like `reindex.py`)
2. Accept `key=value` preference pairs
3. Call `discover_areas(root)` to get current areas
4. Call `render_preferences()` to get instruction strings
5. Call `update_agents_md()` with areas + preferences
6. Write updated AGENTS.md

### 4. Delete `skills/preferences/`

Remove entire directory (SKILL.md + references/).

### 5. Update CLAUDE.md

Remove `/wos:preferences` row from skills table. Decrement count to 8.

### 6. Update tests

- `tests/test_preferences.py`: Remove marker-related tests
  (`TestUpdatePreferences`), keep dimension/render tests
  (`TestDimensionInstruction`, `TestRenderPreferences`)
- Add integration test: `update_preferences.py --root` writes preferences
  into AGENTS.md WOS section

## Not Changed

- `DIMENSIONS`, `DIMENSION_INSTRUCTIONS`, `render_preferences()` — mapping
  logic stays
- `render_wos_section()` — already accepts `preferences` param
- `wos/markers.py` — shared marker replacement unchanged
- Preference capture UX (freeform question → map → confirm → write)

## Branch / PR

- Branch: `feat/merge-preferences`
- PR: TBD
