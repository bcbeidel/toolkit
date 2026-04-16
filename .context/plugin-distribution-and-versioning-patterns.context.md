---
name: "Plugin Distribution and Versioning Patterns"
description: "Plugin systems converged on JSON manifests, git-based distribution with SHA pinning, version-keyed caching, and scoped installation across user/project/local/managed levels"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/plugins-reference
  - https://code.claude.com/docs/en/plugin-marketplaces
  - https://code.claude.com/docs/en/discover-plugins
  - https://code.visualstudio.com/api/references/extension-manifest
  - https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
related:
  - docs/context/instruction-file-fragmentation-and-convergence.context.md
---
All major AI coding tool plugin systems have converged on the same structural patterns: a JSON manifest declaring identity and component paths, git-based distribution as the primary flexible channel, scoped installation with user/project/local separation, and semantic versioning as the version language.

**JSON manifests are universal.** VS Code's `package.json`, Claude Code's `plugin.json`, and GitHub Copilot's `plugin.json` all serve the same function: declaring what a plugin provides and where its components live. Claude Code's manifest is optional — components are auto-discovered from conventional directory locations if no manifest is present. This lowers the friction for simple plugins while enabling full control for complex ones.

**Git-based distribution with SHA pinning.** Claude Code's `marketplace.json` supports five plugin source types: relative path, GitHub repo, git URL, monorepo subdirectory (sparse clone), and npm package. The critical pattern is dual-field versioning: a human-readable `ref` (e.g., `"v2.0.0"`) alongside an exact `sha` (40-character git SHA) for reproducible deployments. Same version = cached copy reused. Version bump forces re-fetch. This solves version drift without requiring a dedicated package registry.

**Version-keyed caching.** Claude Code caches plugins to `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. Orphaned versions (after updates) are deleted after 7 days. The `${CLAUDE_PLUGIN_ROOT}` environment variable resolves to the current cached path and changes on update — scripts must use it rather than hard-coded paths. `${CLAUDE_PLUGIN_DATA}` provides a persistent directory that survives updates, used for state and installed dependencies.

**Four installation scopes (Claude Code):**
- `user` — available across all projects (`~/.claude/settings.json`)
- `project` — shared via version control (`.claude/settings.json`)
- `local` — gitignored personal preferences (`.claude/settings.local.json`)
- `managed` — read-only, administrator-set via `managed-settings.json`

The `managed` scope enables enterprise governance: admins can allowlist specific marketplaces and plugins, preventing installation outside approved sources. This maps directly to enterprise security requirements without blocking individual developer autonomy for local scope.

**MCP has displaced GitHub App-based extensions.** GitHub deprecated its GitHub App-based Copilot Extensions in September 2025, directing developers to MCP servers for external service integration. This reflects a broader pattern: bespoke plugin-as-GitHub-App architectures are giving way to MCP as the standard for external tool connectivity. Plugins now focus on Claude-specific functionality (skills, hooks, commands) rather than API adapters.

**Container and CI seeding.** `CLAUDE_CODE_PLUGIN_SEED_DIR` pre-populates the plugin cache in Docker images without network access at runtime — the canonical pattern for air-gapped or reproducible CI environments. Seed directories are read-only and never modified by Claude Code.
