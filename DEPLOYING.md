# Deploying WOS

WOS skills can be deployed to other AI coding platforms beyond Claude Code.
The deploy script creates symlinks from a target directory back to the WOS
plugin, keeping skills automatically in sync with updates.

## Quick Start

**Deploy to a specific project:**

```bash
python scripts/deploy.py --target /path/to/project
```

**Deploy to a platform (all projects):**

```bash
python scripts/deploy.py --platform copilot
```

**Preview without writing:**

```bash
python scripts/deploy.py --target /path/to/project --dry-run
```

## Project-Level Deployment

Use `--target` to make WOS skills available in a specific project.
Skills are symlinked into the project's `.agents/` directory:

```
your-project/
  .agents/
    wos/              → <wos-plugin>/wos/
    scripts/          → <wos-plugin>/scripts/
    skills/
      audit-wos/      → <wos-plugin>/skills/audit-wos/
      brainstorm/     → <wos-plugin>/skills/brainstorm/
      research/       → <wos-plugin>/skills/research/
      ...
```

Platforms that support `.agents/skills/` discovery (Copilot, Cursor,
Windsurf, Codex, and others) will automatically find the skills.

## Platform-Level Deployment

Use `--platform` to make WOS skills available across all projects for
a specific platform. Skills are symlinked into the platform's home
directory:

```bash
python scripts/deploy.py --platform cursor
# Creates symlinks in ~/.cursor/
```

This is useful when you want WOS skills available everywhere without
adding `.agents/` to each project.

## Supported Platforms

| Platform | Key | Command | Deploy Path |
|----------|-----|---------|-------------|
| GitHub Copilot | `copilot` | `python scripts/deploy.py --platform copilot` | `~/.copilot/` |
| Cursor | `cursor` | `python scripts/deploy.py --platform cursor` | `~/.cursor/` |
| Claude Code | `claude` | `python scripts/deploy.py --platform claude` | `~/.claude/` |
| Codex CLI | `codex` | `python scripts/deploy.py --platform codex` | `~/.codex/` |
| Gemini CLI | `gemini` | `python scripts/deploy.py --platform gemini` | `~/.gemini/` |
| Windsurf | `windsurf` | `python scripts/deploy.py --platform windsurf` | `~/.codeium/windsurf/` |
| OpenCode | `opencode` | `python scripts/deploy.py --platform opencode` | `~/.config/opencode/` |

## How It Works

### Symlinks, not copies

The deploy script creates symbolic links from the target directory back
to the WOS plugin source. This means:

- **No re-deployment needed** — when the plugin updates, deployed skills
  update automatically.
- **No disk duplication** — symlinks are lightweight pointers.
- **Source is untouched** — deployment never modifies the plugin repo.

### Backup behavior

If a target path already exists (a previous deployment, a directory, or
a stale symlink), it is renamed with a timestamped backup suffix before
the new symlink is created:

```
skills/audit-wos → skills/audit-wos.backup_20260313T141500
```

### Idempotency

Re-running the deploy command is safe. Symlinks that already point to the
correct source are skipped:

```
$ python scripts/deploy.py --platform copilot
Deployed to GitHub Copilot (~/.copilot/)
  skip wos (already linked)
  skip scripts (already linked)
  skip audit-wos (already linked)
  ...
```

### What gets deployed

| Directory | Contents |
|-----------|----------|
| `skills/` | Individual skill directories (one symlink each) |
| `scripts/` | CLI scripts (audit, reindex, deploy, etc.) |
| `wos/` | Python package (importable by scripts) |

### Script compatibility

Deployed scripts resolve their imports through the symlink. Python's
`Path(__file__).resolve()` follows symlinks back to the real file,
so the existing plugin root detection works without modification.

## Prerequisites

- Python 3.9+
- WOS plugin installed or cloned locally
