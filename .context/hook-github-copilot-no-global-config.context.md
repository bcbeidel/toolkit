---
name: "GitHub Copilot No Global Hook Configuration"
description: "GitHub Copilot requires per-repository hook configuration with no user-level or system-level equivalent; personal and organization-wide policies cannot be applied across projects"
type: context
sources:
  - https://docs.github.com/en/copilot/reference/hooks-configuration
  - https://github.com/github/copilot-cli/issues/1157
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-github-copilot-surface-divergence.context.md
  - docs/context/hook-github-copilot-blocking-gaps.context.md
  - docs/context/hook-cloud-vs-local-execution-gap.context.md
---

GitHub Copilot's hook system does not support global configuration. All hooks must be configured per-repository via `.github/hooks/*.json`. There is no user-level configuration file and no system-level configuration file.

**What this means in practice**

A developer cannot set up personal hook preferences (logging, notification preferences, personal validation rules) that apply automatically when they open any project. An organization cannot define baseline hook policies that apply across all repositories without injecting the configuration into every repository separately. Hooks only exist and only fire for repositories where someone has explicitly added `.github/hooks/*.json` files.

**Contrast with other platforms**

| Platform | User-level config | System/org-level config |
|----------|------------------|------------------------|
| Claude Code | `~/.claude/settings.json` | No |
| Cursor | `~/.cursor/hooks.json` | Enterprise (MDM) + Team (cloud) |
| Windsurf | `~/.codeium/windsurf/hooks.json` | `/Library/Application Support/Windsurf/hooks.json` |
| Codex CLI | `~/.codex/hooks.json` | No |
| Cline | `~/Documents/Cline/Hooks/` | No |
| GitHub Copilot | **None** | **None** |

**Open feature request**

GitHub issue #1157 (filed January 2026) is a feature request asking for global hook configuration support for Copilot CLI. The request describes the gap: inability to set system-wide preferences for workflow automation. As of Q1 2026, this is a desired-state description, not an implemented feature.

**Impact**

For teams using GitHub Copilot as their primary AI coding platform, enforcing consistent hook policies across all projects requires a repository template or automated injection strategy. Individual developers have no way to establish personal hook defaults the way they can with Claude Code (`~/.claude/settings.json`) or Cursor (`~/.cursor/hooks.json`).
