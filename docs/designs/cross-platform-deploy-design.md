---
name: Cross-Platform Skill Deployment
description: Deploy script that symlinks WOS skills to project or platform directories for cross-platform agent discovery
metadata:
  type: design
  status: approved
  created_at: 2026-03-13
  updated_at: 2026-03-13
  related:
    - docs/plans/cross-platform-deploy.plan.md
    - docs/designs/2026-03-13-deploy-documentation.design.md
---

## Purpose

A deploy script that symlinks WOS skills into a target project's `.agents/`
directory or a platform's home directory, making them discoverable by
GitHub Copilot, Cursor, Windsurf, Codex, Gemini CLI, OpenCode, and
Claude Code itself.

## Context

The Agent Skills open standard uses the same `SKILL.md` format WOS already
uses. `.agents/skills/` is the cross-platform neutral discovery path
supported by multiple platforms. Symlinks keep deployed skills in sync
with the source — no re-deployment needed after plugin updates.

## Deployment Modes

### Project-level (`--target`)

```
python scripts/deploy.py --target /path/to/project
```

Symlinks into `<target>/.agents/`:

```
<target-project>/
  .agents/
    wos/              → <plugin-root>/wos/         # Python package
    scripts/          → <plugin-root>/scripts/      # CLI scripts
    skills/
      audit-wos/      → <plugin-root>/skills/audit-wos/
      research/       → <plugin-root>/skills/research/
      ...             # One symlink per skill directory
```

Use this when skills should be available for a specific project.

### Platform-level (`--platform`)

```
python scripts/deploy.py --platform copilot
```

Symlinks into the platform's home directory (e.g., `~/.copilot/`):

```
~/.copilot/
  wos/              → <plugin-root>/wos/
  scripts/          → <plugin-root>/scripts/
  skills/
    audit/          → <plugin-root>/skills/audit/
    ...
```

Use this when skills should be available across all projects for
that platform.

### Platform Registry

| Key | Platform | Deploy Path |
|-----|----------|-------------|
| `copilot` | GitHub Copilot | `~/.copilot/` |
| `cursor` | Cursor | `~/.cursor/` |
| `claude` | Claude Code | `~/.claude/` |
| `codex` | Codex CLI | `~/.codex/` |
| `gemini` | Gemini CLI | `~/.gemini/` |
| `windsurf` | Windsurf | `~/.codeium/windsurf/` |
| `opencode` | OpenCode | `~/.config/opencode/` |

## Deploy Script Behavior

### What it does

1. **Symlinks support directories** — `scripts/` and `wos/` from the
   plugin root are symlinked directly into the target directory.

2. **Symlinks individual skill directories** — each skill directory
   under `skills/` gets its own symlink under `<target>/skills/`.

3. **Backs up existing content** — if a target path already exists
   (directory or stale symlink), it is renamed with a timestamped
   `.backup_YYYYMMDDTHHMMSS` suffix before creating the new symlink.

4. **Skips correct links** — if a symlink already points to the
   correct source, it is left untouched (idempotent).

### Flags

- `--target PATH` — target project directory (mutually exclusive with `--platform`)
- `--platform KEY` — target platform from the registry (mutually exclusive with `--target`)
- `--dry-run` — show what would be done without writing

### What it does NOT do

- Does not modify the source repo
- Does not copy files — symlinks only
- Does not touch existing files outside WOS-managed paths

## Root Detection

Scripts use a hybrid pattern to find the plugin root:

```python
_env_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
_plugin_root = (
    Path(_env_root) if _env_root and os.path.isdir(_env_root)
    else Path(__file__).resolve().parent.parent  # fallback
)
```

When accessed via symlink, `Path(__file__).resolve()` follows the symlink
back to the real file in the plugin directory. Root detection works
without modification.

## Constraints

- `deploy.py` is stdlib-only, runnable with `python scripts/deploy.py`
- Python 3.9+ (matching repo convention)
- No changes to existing Claude Code plugin functionality

## Acceptance Criteria

1. Skills discoverable from deployed `skills/` directory
2. All deployed scripts run with `python` — no external dependencies
3. Scripts can `import wos` via `__file__` resolution through symlinks
4. Re-running deploy on same target is idempotent (skips correct links)
5. `--dry-run` shows planned operations without side effects
6. Existing content is backed up before relinking
