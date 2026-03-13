---
name: Cross-Platform Skill Deployment
description: Export script that deploys WOS skills into .agents/ for Copilot and other Agent Skills-compatible copilots without uv or Claude Code
type: design
status: draft
related:
  - docs/research/2026-03-13-copilot-skill-format.md
  - docs/research/2026-03-13-cross-platform-skill-formats.md
---

## Purpose

A deploy script that exports WOS skills into a target project's `.agents/`
directory, making them discoverable by GitHub Copilot (and other Agent
Skills-compatible copilots) without requiring `uv` or Claude Code.

## Context

The Agent Skills open standard (agentskills.io) uses the same `SKILL.md`
format WOS already uses. `.agents/skills/` is the cross-platform neutral
discovery path supported by Copilot, Cursor, Windsurf, and Codex. WOS is
90% compatible — the gaps are script invocation (`uv run` → `python`),
preflight removal, and deployment packaging.

## Deployed Structure

```
<target-project>/
  .agents/
    wos/                              # Python package (for script imports)
      __init__.py
      document.py
      frontmatter.py
      index.py
      validators.py
      ...
    scripts/                          # Shared scripts (stdlib-only)
      audit.py
      reindex.py
      check_url.py
      update_preferences.py
      get_version.py
    skills/
      _shared/references/             # Shared refs (preflight.md excluded)
      audit/
        SKILL.md                      # Rewritten: uv run → python
        references/
      research/
        SKILL.md
        scripts/research_assess.py
        references/
      ...                             # All other skills
```

This structure preserves the same relative depth as the source repo.
`scripts/audit.py` is 2 levels below root. `skills/research/scripts/
research_assess.py` is 4 levels below root. The root is `.agents/`
instead of the plugin directory. Existing `__file__` parent-chain root
detection works without modification.

## Deploy Script Behavior

`scripts/deploy.py --target /path/to/project [--dry-run]`

### Four operations

1. **Copy** — Copies `skills/`, `scripts/`, and `wos/` into
   `<target>/.agents/`, preserving directory structure.

2. **Rewrite invocations** — Replaces `uv run <path>` → `python <path>`
   in all `.md` files under the deployed tree.

3. **Remove preflight** — Strips `preflight.md` from SKILL.md `references:`
   frontmatter. Removes preflight instruction blocks from SKILL.md bodies.
   The 3-step uv canary check is meaningless without uv.

4. **Skip non-deployable content** — Excludes `check_runtime.py` (uv canary,
   only script with external dependency) and `preflight.md`.

### What it does NOT do

- Does not modify the source repo — export only.
- Does not touch existing files in the target `.agents/` directory outside
  WOS-managed paths.
- Does not modify Python scripts — only markdown rewriting. Scripts already
  have `__file__` fallback that works without `CLAUDE_PLUGIN_ROOT`.

### Flags

- `--target PATH` (required) — target project directory
- `--dry-run` — show what would be copied/rewritten without writing

### Idempotent

Safe to re-run. Overwrites previously deployed WOS files.

## Constraints

- `deploy.py` is stdlib-only, runnable with `python scripts/deploy.py`
- Python 3.9+ (matching repo convention)
- No changes to existing Claude Code plugin functionality

## Root Detection

Scripts use a hybrid pattern to find the plugin root:

```python
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent  # fallback
)
```

In deployed mode, `CLAUDE_PLUGIN_ROOT` is not set. The `__file__` fallback
resolves to `.agents/` because the relative depth is preserved. No changes
to existing scripts required.

## Acceptance Criteria

1. Skills discoverable by Copilot from `.agents/skills/`
2. All deployed scripts run with `python` — no uv required
3. Scripts can `import wos` via existing `__file__` parent-chain detection
4. No `uv run` references remain in any deployed `.md` file
5. No `preflight.md` reference remains in any deployed SKILL.md frontmatter
6. Source repo unchanged after deploy
7. Re-running deploy on same target produces identical output
8. `--dry-run` shows planned operations without side effects
