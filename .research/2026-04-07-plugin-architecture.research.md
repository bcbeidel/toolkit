---
name: "Plugin Architecture & Distribution"
description: "How AI coding tool plugins are discovered, installed, versioned, and distributed — covering Claude Code, VS Code, GitHub Copilot, and Cursor"
type: research
sources:
  - https://code.claude.com/docs/en/plugins-reference
  - https://code.claude.com/docs/en/discover-plugins
  - https://code.claude.com/docs/en/plugin-marketplaces
  - https://code.visualstudio.com/api/references/extension-manifest
  - https://code.visualstudio.com/api/working-with-extensions/publishing-extension
  - https://code.visualstudio.com/api/references/contribution-points
  - https://cursor.com/blog/marketplace
  - https://deepwiki.com/github/awesome-copilot/8.1-plugin-architecture-and-marketplace
  - https://github.blog/changelog/2025-02-19-announcing-the-general-availability-of-github-copilot-extensions/
  - https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/
related:
  - docs/research/2026-04-07-instruction-file-conventions.research.md
  - docs/research/2026-04-07-skill-ecosystem-design.research.md
---

## Research Question

How do AI coding tool plugin ecosystems structure discovery, installation, versioning, and distribution — and what patterns are converging across Claude Code, VS Code, GitHub Copilot, and Cursor?

## Sub-Questions

1. How do AI coding tool plugins get discovered, installed, and updated (Claude Code, VS Code extensions, Cursor extensions)?
2. What manifest formats and metadata schemas do plugin systems use?
3. How do plugins handle versioning, compatibility, and dependency management?
4. What deployment patterns exist (symlinks, package managers, git-based, marketplace)?

## Search Protocol

| # | Query | Result |
|---|-------|--------|
| 1 | Claude Code plugin system architecture 2025 plugin.json format discovery | Found official docs, plugins-reference, marketplace.json, demo repo |
| 2 | VS Code extension manifest package.json format contributes activationEvents 2025 | Found official VS Code API docs for extension-manifest, contribution-points, activation-events |
| 3 | Claude Code plugin distribution installation git-based 2025 2026 | Found discover-plugins, plugin-marketplaces official docs |
| 4 | Cursor IDE extensions plugins architecture 2025 | Found cursor.com/blog/marketplace, cursor.com/docs/reference/plugins |
| 5 | VS Code extension marketplace vsce publish versioning engine compatibility 2025 | Found publishing-extension official docs, vsce tool details |
| 6 | Claude Code plugin marketplaces format marketplace.json schema 2025 2026 | Found plugin-marketplaces official docs, unofficial JSON schema repo |
| 7 | AI coding tool plugin versioning compatibility dependency management patterns 2025 | Found supply chain risk research, SemVer practices |
| 8 | git-based plugin distribution symlinks caching "plugin cache" AI tools 2025 | Confirmed Claude Code caching behavior from plugin-marketplaces docs |
| 9 | GitHub Copilot extensions plugin architecture 2025 manifest discovery distribution | Found awesome-copilot DeepWiki, GA announcement, deprecation of GitHub App extensions in favor of MCP |
| 10 | npm package distribution vs git-based developer tool plugins versioning semver pinning SHA 2025 | Found npm SemVer docs, dependency pinning best practices |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/plugins-reference | Plugins reference | Anthropic | 2025-2026 | T1 | verified |
| 2 | https://code.claude.com/docs/en/discover-plugins | Discover and install prebuilt plugins | Anthropic | 2025-2026 | T1 | verified |
| 3 | https://code.claude.com/docs/en/plugin-marketplaces | Create and distribute a plugin marketplace | Anthropic | 2025-2026 | T1 | verified |
| 4 | https://code.visualstudio.com/api/references/extension-manifest | Extension Manifest | Microsoft | 2025 | T1 | verified |
| 5 | https://code.visualstudio.com/api/working-with-extensions/publishing-extension | Publishing Extensions | Microsoft | 2025 | T1 | verified |
| 6 | https://code.visualstudio.com/api/references/contribution-points | Contribution Points | Microsoft | 2025 | T1 | verified |
| 7 | https://cursor.com/blog/marketplace | Extend Cursor with plugins | Cursor | 2025 | T1 | verified |
| 8 | https://deepwiki.com/github/awesome-copilot/8.1-plugin-architecture-and-marketplace | Plugin Architecture and Marketplace (awesome-copilot) | DeepWiki/GitHub | 2025 | T3 | verified |
| 9 | https://github.blog/changelog/2025-02-19-announcing-the-general-availability-of-github-copilot-extensions/ | GA of GitHub Copilot Extensions | GitHub | Feb 2025 | T1 | verified |
| 10 | https://github.blog/changelog/2025-09-24-deprecate-github-copilot-extensions-github-apps/ | Sunset: GitHub App-based Copilot Extensions | GitHub | Sep 2025 | T1 | verified |

## Raw Extracts

### Sub-question 1: Discovery, installation, and updates

**Claude Code**

Claude Code (released Oct 2025) uses a two-step model: add a marketplace catalog first, then install individual plugins from it. The official Anthropic marketplace (`claude-plugins-official`) is pre-registered and browsable via `/plugin` → Discover tab or `claude.com/plugins`.

Discovery mechanisms:
- `/plugin` interactive UI with Discover, Installed, Marketplaces, and Errors tabs
- `claude plugin install <name>@<marketplace>` CLI command
- Auto-discovery on session start: Claude Code scans enabled plugins and loads components from default directory locations without explicit registration in `plugin.json` (manifest is optional)
- `extraKnownMarketplaces` in `.claude/settings.json` prompts team members to install on project trust

Installation scopes:
- `user` (~/.claude/settings.json) — default, available across all projects
- `project` (.claude/settings.json) — shared via version control, for teams
- `local` (.claude/settings.local.json) — gitignored, project-specific personal use
- `managed` — read-only, set by administrators via managed-settings.json

Update mechanism: Version-based cache invalidation. Claude Code caches plugins to `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`. If the version in `plugin.json` or `marketplace.json` does not change, the cached copy is used. Auto-update runs at startup for marketplaces with `autoUpdate: true` (default for official Anthropic marketplace; opt-in for third-party). `/reload-plugins` applies changes mid-session without restart. Previous version directories are marked orphaned and deleted after 7 days.

**VS Code**

Extensions install from the Visual Studio Marketplace via the Extensions view, CLI (`code --install-extension publisher.name`), or VSIX file. Discovery is keyword/category search in Marketplace. Auto-updates enabled by default; VS Code updates extensions to the highest compatible version at launch.

**Cursor**

Cursor is a VS Code fork, so it inherits VS Code extension compatibility broadly. Its own plugin system (introduced in late 2025 via the Cursor Marketplace) adds a marketplace at cursor.com/marketplace with categories: planning, payments, infrastructure, analytics, and more. Partners include Amplitude, AWS, Figma, Linear, Stripe. Unlike VS Code extensions, Cursor's native AI layer is not an extension — it is part of the editor core, sharing context across Tab completion, Composer, agent mode, and terminal. Private team marketplaces are in development.

**GitHub Copilot (awesome-copilot)**

The CLI scans `.github/extensions/` (project-scoped) and `~/.copilot/extensions/` (user-scoped) for extension directories containing `extension.mjs`. The marketplace endpoint at `https://raw.githubusercontent.com/github/awesome-copilot/main/.github/plugin/marketplace.json` serves discovery. Installation channels: `copilot plugin install <name>@awesome-copilot`, VS Code `@agentPlugins` search, website install buttons, or manual file copy. GitHub App-based Copilot Extensions deprecated Sep 2025 in favor of MCP servers.

---

### Sub-question 2: Manifest formats and metadata schemas

**Claude Code — `plugin.json`**

Location: `.claude-plugin/plugin.json` (manifest is optional; components auto-discovered if absent)

Required field (if manifest present): `name` (kebab-case, unique identifier)

Key optional fields:
```json
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": { "name": "...", "email": "...", "url": "..." },
  "homepage": "https://...",
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["tag1", "tag2"],
  "commands": "./custom/commands/",
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "userConfig": { "api_token": { "description": "...", "sensitive": true } },
  "channels": [{ "server": "telegram", "userConfig": {...} }]
}
```

Component path fields (commands, agents, skills, outputStyles) replace defaults when specified. Hooks, MCP servers, and LSP servers support multiple sources merged together. Paths must be relative and start with `./`.

Environment variables available in manifests and scripts:
- `${CLAUDE_PLUGIN_ROOT}` — absolute path to plugin's install directory (changes on update)
- `${CLAUDE_PLUGIN_DATA}` — persistent directory at `~/.claude/plugins/data/{id}/` (survives updates)

**Claude Code — `marketplace.json`**

Location: `.claude-plugin/marketplace.json`

Required: `name`, `owner.name`, `plugins[]` with each entry requiring `name` and `source`

Plugin source types:
- Relative path string (`"./plugins/my-plugin"`) — only works with git-based marketplace add
- `{ "source": "github", "repo": "owner/repo", "ref": "v2.0.0", "sha": "..." }`
- `{ "source": "url", "url": "https://...", "ref": "...", "sha": "..." }`
- `{ "source": "git-subdir", "url": "...", "path": "tools/claude-plugin" }` — sparse clone for monorepos
- `{ "source": "npm", "package": "@org/plugin", "version": "^2.0.0", "registry": "..." }`

Optional metadata on marketplace entries: `description`, `version`, `author`, `homepage`, `repository`, `license`, `keywords`, `category`, `tags`, `strict` (bool — controls whether `plugin.json` or the marketplace entry is authoritative).

**VS Code — `package.json`**

Required fields: `name` (lowercase, no spaces), `version` (SemVer), `publisher`, `engines.vscode` (minimum compatibility, cannot be `*`)

Key optional fields: `displayName`, `description`, `categories`, `keywords` (max 30), `main` (entry point), `browser` (web extension), `contributes`, `activationEvents`, `extensionDependencies`, `extensionPack`, `extensionKind` (`ui` or `workspace`), `pricing` (`Free` or `Trial`), `icon` (min 128×128px), `license`

The `contributes` key is a large declarative schema covering: `commands`, `menus`, `views`, `viewsContainers`, `languages`, `grammars`, `snippets`, `themes`, `colors`, `iconThemes`, `debuggers`, `authentication`, `customEditors`, `keybindings`, `configuration`, `taskDefinitions`, `walkthroughs`, `problemMatchers`, `jsonValidation`, `typescriptServerPlugins`, `terminal`.

`activationEvents` determines when extension code loads: `onLanguage`, `onCommand`, `onView`, `onFileSystem`, `workspaceContains`, `onStartupFinished`, `*` (always). Since VS Code 1.74, contributed commands no longer need a matching `onCommand` activation event.

**GitHub Copilot (awesome-copilot) — `plugin.json`**

Required: `name` (must match directory name, lowercase-hyphenated), `description`, `version` (SemVer)

Optional: `author`, `keywords`, `license`, `repository`, `homepage`

Content declarations via path references: `agents` (→ `agents/*.agent.md`), `commands` (→ `prompts/*.prompt.md`), `skills` (→ `skills/*/` directories)

The marketplace aggregator at `eng/generate-marketplace.mjs` merges local plugins and external plugins into a single `.github/plugin/marketplace.json`.

---

### Sub-question 3: Versioning, compatibility, and dependency management

**Claude Code versioning**

- SemVer in `plugin.json` or `marketplace.json` (plugin.json takes priority if both set)
- Version drives cache key: same version = cached copy reused; bump version to force update
- Pin to exact commit via `sha` field (40-char git SHA) for reproducibility alongside `ref` for human-readable label
- Release channels implemented by maintaining two marketplaces pointing to different `ref` or `sha` values of same repo (stable vs. latest)
- No declared dependency system between plugins; MCP and LSP server binaries must be separately installed
- Persistent data in `${CLAUDE_PLUGIN_DATA}` uses a diff-and-reinstall pattern (compare bundled manifest against stored copy, reinstall on change) for managing plugin-level dependencies like `node_modules`

**VS Code versioning and compatibility**

- SemVer for extension versions
- `engines.vscode` constrains compatible VS Code range; caret (`^1.8.0`) means ≥1.8.0
- `extensionDependencies` array lists other extensions that must be installed first
- `extensionPack` bundles multiple extensions together as a single installable unit
- Pre-release: recommended `major.EVEN_NUMBER.patch` for stable, `major.ODD_NUMBER.patch` for pre-release to prevent unintended downgrades
- vsce CLI handles version increments (`vsce publish minor` bumps 1.0.0 → 1.1.0, commits to git, creates tag)
- `vscode:uninstall` lifecycle script in `package.json` `scripts` runs cleanup on full uninstall

**GitHub Copilot**

- SemVer required; validated by automated CI pipeline
- Build integration (`npm run build`) validates schemas and regenerates marketplace artifacts on manifest change
- GitHub App-based extensions deprecated Sep 2025; MCP servers now the preferred integration path

**Supply chain risks (2025 research)**

- AI agents introduce new dependency risks: 45% of AI-generated dependency edits are new additions, 25.5% are version updates
- Agents select known-vulnerable versions at higher rate than humans (2.46% vs. 1.64%)
- 75% of MCP servers are built by individuals without enterprise-grade safeguards; 41% lack license info
- Emerging best practice: define approved dependency policies at selection time, enforce via allowlists

---

### Sub-question 4: Deployment patterns

**Pattern 1: Git-based marketplace (Claude Code primary pattern)**
- Marketplace = a git repo containing `.claude-plugin/marketplace.json`
- Plugins fetched from GitHub repos, git URLs, monorepo subdirs (sparse clone), or relative paths within marketplace repo
- Claude Code clones marketplace repo and copies plugin content to versioned cache at `~/.claude/plugins/cache/`
- Symlinks within plugin directories are followed during copy (enables sharing files across plugins)
- After copy, `${CLAUDE_PLUGIN_ROOT}` resolves to cache path; files outside plugin dir are inaccessible post-install
- Relative path sources only work when marketplace is added via git (not raw URL); monorepo sparse checkout minimizes bandwidth

**Pattern 2: npm distribution (Claude Code, GitHub Copilot)**
- Plugins published as npm packages, installed via `npm install`
- Supports public registry, private/internal registries, version ranges (SemVer), pinned versions
- Familiar tooling for JS/Node ecosystem; handles dependency trees
- Claude Code also uses npm internally for plugin-level JS dependencies via `${CLAUDE_PLUGIN_DATA}` pattern

**Pattern 3: VSIX + Marketplace (VS Code)**
- Extensions packaged as VSIX (zip format) via `vsce package`
- Published to Visual Studio Marketplace via Azure DevOps PAT
- Marketplace handles discovery, download, versioning, and auto-update
- Also supports: direct VSIX install from file, `code --install-extension publisher.name`, private OVSX registries
- Extensions stored per-user; VS Code updates to highest compatible version automatically

**Pattern 4: In-place / symlink / local path (development + team use)**
- Claude Code: `--plugin-dir` flag loads a plugin directory for a single session without caching; local marketplace paths for testing
- VS Code: workspace extensions; extensions loaded from a local `.vscode/extensions/` directory
- Claude Code team settings: `extraKnownMarketplaces` in `.claude/settings.json` seeds marketplace for whole team via version control
- Claude Code container seeding: `CLAUDE_CODE_PLUGIN_SEED_DIR` pre-populates plugin cache in Docker images for CI/CD; seed dirs are read-only and never modified

**Pattern 5: Managed / centralized governance**
- Claude Code `managed` scope: `managed-settings.json` (read-only for users) specifies `strictKnownMarketplaces` allowlist and `enabledPlugins`
- Restriction types: empty array (lockdown), allowlist by exact source, regex `hostPattern` (all plugins from a git host), regex `pathPattern` (filesystem paths)
- VS Code for Enterprise: organization can host private OVSX registry; extension packs for standardized toolsets
- Cursor: private team marketplaces in development

**Convergence observations**

All major AI coding tools have converged on:
1. A JSON or YAML manifest file declaring plugin identity and component paths
2. Git-based distribution as the primary flexible channel (vs. centralized registry)
3. Scoped installation: user-global, project-shared, local-only
4. Semantic versioning as the version language, with optional SHA pinning for exact reproducibility
5. MCP servers as the emerging standard for external tool integration (GitHub deprecated its GitHub App-based extensions in favor of MCP, Sep 2025)
6. Separation of plugin content (files in plugin dir, immutable after install) from persistent plugin state (separate data directory)

## Findings

### Claude Code plugin architecture is the most fully specified for AI-native workflows

Claude Code's plugin system (released Oct 2025) is the most complete design for AI-native extensibility: optional `plugin.json` (auto-discovery without manifest), 5 source types in `marketplace.json`, version-keyed caching at `~/.claude/plugins/cache/`, and 4 installation scopes (user/project/local/managed) [1][2][3]. The `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_DATA}` environment variables solve the update-while-preserving-state problem cleanly. HIGH confidence (all T1 Anthropic docs, thoroughly fetched).

### All major tools converged on JSON manifests, git-based distribution, and MCP for external tools

VS Code's `package.json`, Claude Code's `plugin.json`, and GitHub Copilot's `plugin.json` all use JSON with SemVer. Git-based distribution (GitHub repos, monorepo sparse clones) is the primary flexible channel for Claude Code and GitHub Copilot. GitHub deprecated its GitHub App-based Copilot Extensions in September 2025, directing developers to MCP servers [9][10]. MCP is now the converging standard for external service integration across all tools. HIGH confidence.

### SHA pinning is the key pattern for reproducible plugin deployments

Claude Code's `marketplace.json` supports an explicit `sha` field (40-char git SHA) alongside a human-readable `ref`. Dual-channel release management (stable/latest) is implemented by maintaining two marketplace configs pointing to different refs of the same repo [3]. This pattern solves the version drift problem without a dedicated package registry. HIGH confidence (T1 docs).

### Supply chain security for AI-generated dependencies is an emerging risk

AI agents select known-vulnerable dependency versions at a higher rate than humans (2.46% vs. 1.64%); 75% of MCP servers are built by individuals without enterprise safeguards [source: unnamed security research in search results — see challenge]. These figures appear only in the Search Protocol and lack numbered sources. MODERATE confidence directionally; LOW confidence for specific statistics.

### Key canonical tools and references

- **Claude Code plugin reference:** https://code.claude.com/docs/en/plugins-reference — full `plugin.json` and `marketplace.json` schema
- **Claude Code marketplace docs:** https://code.claude.com/docs/en/plugin-marketplaces — distribution patterns, scopes, governance
- **VS Code extension manifest:** https://code.visualstudio.com/api/references/extension-manifest — `package.json` reference

## Challenge

### Claim: "Claude Code manifest is optional"
**Strength:** HIGH. Per T1 Anthropic docs, Claude Code auto-discovers components (skills/, commands/, agents/ under `.claude-plugin/`) without `plugin.json` present. The manifest is needed only to specify non-default paths, add metadata, or configure hooks/MCP/LSP. This design reduces friction for simple plugins.

### Claim: "75% of MCP servers built by individuals without enterprise safeguards" and related security statistics
**Strength:** LOW. These figures appear in the Search Protocol summary but have no numbered source entry in the document. The specific percentages cannot be traced to a verifiable T1-T3 source. The directional point (supply chain risk from individual-authored MCP servers) is plausible given MCP's rapid growth but should not be cited as fact.

### Claim: "GitHub App-based Copilot Extensions deprecated in favor of MCP, Sep 2025"
**Strength:** HIGH. This is directly sourced from a T1 GitHub changelog entry dated Sep 24, 2025 [10]. It represents a significant ecosystem shift: GitHub is explicitly directing developers away from GitHub App-based plugins toward MCP servers.

### What this research does NOT cover
- Non-Claude-Code tools' plugin architectures are shallower (Cursor's is particularly underspecified here beyond what the blog post covers)
- Plugin security review processes for marketplace gatekeeping
- Enterprise deployment automation (CI/CD plugin pre-caching beyond the seed dir pattern)
- Windsurf plugin/extension system (no data collected)

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claude Code plugin system released October 2025 | date | [1][2][3] | verified |
| 2 | Claude Code `plugin.json` has one required field: `name` | attribution | [1] | verified |
| 3 | Claude Code caches plugins to `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` | attribution | [3] | verified |
| 4 | Orphaned plugin versions deleted after 7 days | attribution | [3] | verified |
| 5 | Claude Code supports 5 plugin source types in `marketplace.json` | statistic | [3] | verified |
| 6 | VS Code `engines.vscode` field cannot be `*` (must specify minimum version) | attribution | [4] | verified |
| 7 | VS Code pre-release convention: stable uses even minor (1.0.x), pre-release uses odd minor (1.1.x) | attribution | [5] | verified |
| 8 | GitHub Copilot App-based Extensions deprecated September 24, 2025, in favor of MCP | date/attribution | [10] | verified |
| 9 | GitHub Copilot Extensions reached GA on February 19, 2025 | date | [9] | verified |
| 10 | 45% of AI-generated dependency edits are new additions; agents select vulnerable versions at 2.46% vs. 1.64% for humans | statistic | none (search protocol only) | human-review — no numbered source; cannot verify |
| 11 | 75% of MCP servers built by individuals without enterprise-grade safeguards | statistic | none (search protocol only) | human-review — no numbered source; cannot verify |
| 12 | `CLAUDE_CODE_PLUGIN_SEED_DIR` env var pre-populates plugin cache for Docker/CI | attribution | [3] | verified |
