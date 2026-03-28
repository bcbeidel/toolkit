---
name: "Plugin and Extension Architecture Patterns"
description: "How host systems discover, load, and invoke plugins — registration mechanisms, script execution patterns, sandboxing constraints, and version management across Claude Code, VS Code, Vim/Neovim, JetBrains, browser extensions, and other extension models"
metadata:
  type: research
  sources:
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/plugins-reference
    - https://code.visualstudio.com/api/references/activation-events
    - https://code.visualstudio.com/api/advanced-topics/extension-host
    - https://code.visualstudio.com/api/get-started/extension-anatomy
    - https://code.visualstudio.com/api/references/extension-manifest
    - https://code.visualstudio.com/blogs/2022/11/28/vscode-sandbox
    - https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security
    - https://deepwiki.com/microsoft/vscode/3-product-configuration-and-policy
    - https://neovim.io/doc/user/lua-plugin.html
    - https://github.com/folke/lazy.nvim
    - https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html
    - https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html
    - https://plugins.jetbrains.com/docs/intellij/plugin-services.html
    - https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3
    - https://www.figma.com/blog/how-we-built-the-figma-plugin-system/
    - https://www.figma.com/blog/an-update-on-plugin-security/
    - https://dev.to/cyberpath/designing-secure-plugin-architectures-for-desktop-applications-1meh
  related:
    - docs/research/tool-design-for-llms.md
    - docs/research/workflow-orchestration.md
    - docs/research/context-engineering.md
    - docs/context/plugin-extension-architecture.md
---

## Summary

Plugin and extension architectures share a common structural pattern — manifest-driven discovery, lazy activation, controlled API surfaces — but diverge sharply on sandboxing and execution models depending on threat model and performance requirements.

**Key findings:**

- **Manifest files are universal.** Every system uses a declarative descriptor (plugin.json, package.json, plugin.xml, manifest.json, SKILL.md frontmatter) for discovery, dependency declaration, and capability registration. The manifest is the contract between plugin and host (HIGH).
- **Lazy loading is the dominant activation strategy.** VS Code uses activation events, Neovim uses autoload/lazy.nvim event triggers, JetBrains uses on-demand service loading, Claude Code uses progressive disclosure of skill metadata. Eager loading is universally discouraged (HIGH).
- **Sandboxing models span a wide spectrum.** From no isolation (Vim/Neovim plugins run in-process with full access) through process isolation (VS Code extension host) to WebAssembly sandboxing (Figma). The choice is driven by threat model: editor plugins trust the developer; web-facing systems trust no one (HIGH).
- **Claude Code's plugin model is uniquely prompt-based.** Unlike programmatic extension APIs, Claude Code plugins are discovered and invoked by the LLM based on textual descriptions, not by code calling APIs. This makes the manifest's descriptive fields load-bearing for functionality, not just metadata (HIGH).
- **Version management converges on semantic versioning.** All systems use semver (MAJOR.MINOR.PATCH). Host compatibility ranges vary: VS Code uses `engines.vscode`, JetBrains uses `since-build`/`until-build`, Claude Code uses marketplace version tracking with cache-based distribution (MODERATE).
- **The trend is toward stronger isolation.** Chrome moved from background pages to service workers (MV3), VS Code migrated renderer processes to sandboxed utility processes, Figma moved from Realms to WASM. Security constraints are tightening across all ecosystems (HIGH).

## Research Brief

Landscape investigation of how host applications discover, load, invoke, sandbox, and version-manage plugins. Covers six ecosystems representing different architectural traditions: AI agent plugins (Claude Code), IDE extensions (VS Code, JetBrains), editor plugins (Vim/Neovim), browser extensions (Chrome MV3), and design tool plugins (Figma).

### Sub-Questions

1. How does Claude Code discover and load plugins (directory conventions, manifest files, skill registration)?
2. How does VS Code discover, load, and manage extensions (Extension API, activation events, sandboxing)?
3. How do Vim/Neovim plugin managers discover and load plugins (runtime paths, autoload, lazy loading)?
4. What other notable extension models exist and what patterns do they share (JetBrains, Chrome, Figma)?
5. What are the common patterns for plugin sandboxing and security across these systems?
6. How do these systems handle versioning, dependency resolution, and update lifecycle?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/plugins | Create Plugins - Claude Code Docs | Anthropic | 2025 | T1 | verified |
| 2 | https://code.claude.com/docs/en/plugins-reference | Plugins Reference - Claude Code Docs | Anthropic | 2025 | T1 | verified |
| 3 | https://code.visualstudio.com/api/references/activation-events | Activation Events - VS Code Extension API | Microsoft | 2024 | T1 | verified |
| 4 | https://code.visualstudio.com/api/advanced-topics/extension-host | Extension Host - VS Code Extension API | Microsoft | 2024 | T1 | verified |
| 5 | https://code.visualstudio.com/api/get-started/extension-anatomy | Extension Anatomy - VS Code Extension API | Microsoft | 2024 | T1 | verified |
| 6 | https://code.visualstudio.com/api/references/extension-manifest | Extension Manifest - VS Code Extension API | Microsoft | 2024 | T1 | verified |
| 7 | https://code.visualstudio.com/blogs/2022/11/28/vscode-sandbox | Migrating VS Code to Process Sandboxing | Microsoft | 2022 | T1 | verified |
| 8 | https://code.visualstudio.com/docs/configure/extensions/extension-runtime-security | Extension Runtime Security - VS Code | Microsoft | 2025 | T1 | verified |
| 9 | https://deepwiki.com/microsoft/vscode/3-product-configuration-and-policy | Extension System - VS Code DeepWiki | DeepWiki / Community | 2025 | T3 | verified |
| 10 | https://neovim.io/doc/user/lua-plugin.html | Lua-plugin - Neovim Docs | Neovim Project | 2024 | T1 | verified |
| 11 | https://github.com/folke/lazy.nvim | lazy.nvim - Modern Plugin Manager for Neovim | folke | 2024 | T2 | verified |
| 12 | https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html | Extensions - IntelliJ Platform Plugin SDK | JetBrains | 2024 | T1 | verified |
| 13 | https://plugins.jetbrains.com/docs/intellij/plugin-configuration-file.html | Plugin Configuration File - IntelliJ SDK | JetBrains | 2024 | T1 | verified |
| 14 | https://plugins.jetbrains.com/docs/intellij/plugin-services.html | Services - IntelliJ Platform Plugin SDK | JetBrains | 2024 | T1 | verified |
| 15 | https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3 | Manifest V3 - Chrome for Developers | Google | 2024 | T1 | verified |
| 16 | https://www.figma.com/blog/how-we-built-the-figma-plugin-system/ | How We Built the Figma Plugin System | Figma / Evan Wallace | 2019 | T1 | verified |
| 17 | https://www.figma.com/blog/an-update-on-plugin-security/ | An Update on Plugin Security | Figma | 2020 | T1 | verified |
| 18 | https://dev.to/cyberpath/designing-secure-plugin-architectures-for-desktop-applications-1meh | Designing Secure Plugin Architectures for Desktop Applications | CyberPath / DEV Community | 2024 | T4 | verified |

## Research Protocol

| # | Query | Tool | Results | Selected |
|---|-------|------|---------|----------|
| 1 | Claude Code plugins architecture discovery loading skills 2025 2026 | WebSearch | Plugin docs, blog posts, community guides | [1][2] |
| 2 | VS Code extension API activation events host process architecture | WebSearch | Official VS Code docs on activation, extension host, anatomy, manifest | [3][4][5][6] |
| 3 | Vim Neovim plugin loading architecture runtime path autoload lazy | WebSearch | Neovim lua-plugin docs, lazy.nvim, autoload references | [10][11] |
| 4 | Plugin extension architecture patterns discovery registration sandboxing comparison | WebSearch | .NET plugin patterns, desktop security architecture, general patterns | [18] |
| 5 | Claude Code plugins reference plugin.json manifest schema | WebSearch | Full plugins reference documentation | [2] |
| 6 | VS Code extension sandboxing security model extension host isolation | WebSearch | Sandbox migration blog, runtime security docs, community analysis | [7][8] |
| 7 | JetBrains IntelliJ plugin architecture extension points service registration | WebSearch | IntelliJ SDK docs on extensions, services, configuration | [12][13][14] |
| 8 | Chrome browser extension manifest v3 architecture service worker sandboxing | WebSearch | Chrome MV3 migration docs, sandbox manifest, security model | [15] |
| 9 | Figma plugin sandboxing WebAssembly WASM isolation security model | WebSearch | Figma engineering blog posts on plugin system and security | [16][17] |
| 10 | VS Code extension system architecture (DeepWiki) | WebFetch | Detailed extension host internals, RPC protocol, activation | [9] |
| 11 | Claude Code plugins reference full schema | WebFetch | Complete manifest schema, directory structure, CLI commands, caching | [2] |
| 12 | Claude Code create plugins guide | WebFetch | Plugin structure overview, skill creation, testing workflow | [1] |

## Extracts by Sub-Question

### SQ1: Claude Code Plugin Discovery and Loading

**Directory-based discovery with optional manifest:**
Claude Code plugins are self-contained directories. The `.claude-plugin/plugin.json` manifest is optional — if omitted, Claude Code auto-discovers components in default locations (`skills/`, `commands/`, `agents/`, `hooks/`) and derives the plugin name from the directory name [1][2]. This is a convention-over-configuration approach: the directory structure itself is the registration mechanism.

**Search paths for discovery:**
Plugins are loaded from multiple sources: user settings (`~/.claude/settings.json`), project settings (`.claude/settings.json`), local settings (`.claude/settings.local.json`), managed settings, and via `--plugin-dir` for development [2]. Installed marketplace plugins are cached at `~/.claude/plugins/cache` — Claude Code copies plugins to the local cache rather than using them in-place, providing a security and verification boundary [2].

**Skill registration as progressive disclosure:**
At session start, Claude sees only the name and description of every available skill (~100 tokens per skill). When Claude determines a skill is relevant, it loads the full SKILL.md (<5k tokens). Bundled resources load only as needed. This three-tier progressive disclosure (metadata → instructions → resources) is unique among plugin systems — it is optimized for LLM context window economics rather than process startup time [1].

**Prompt-based invocation (not API-based):**
Unlike every other system surveyed, Claude Code plugins are invoked by the LLM making a decision based on textual descriptions in its system prompt. There is no programmatic `activate()` function or API call. The SKILL.md `description` frontmatter field is functionally equivalent to an activation event — it determines when the skill gets loaded. This makes description quality load-bearing for plugin functionality [1][2].

**Plugin manifest schema:**
The `plugin.json` requires only `name` (kebab-case identifier). Optional fields: `version`, `description`, `author` (name/email/url), `homepage`, `repository`, `license`, `keywords`. Component path fields (`commands`, `agents`, `skills`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`) supplement default directories — they do not replace them [2].

**Environment and script execution:**
Hooks and scripts use `${CLAUDE_PLUGIN_ROOT}` for path resolution, ensuring correct paths regardless of installation location. Scripts are executed via `uv run` with PEP 723 inline metadata. Path traversal outside the plugin root is blocked for installed plugins (symlinks are honored during cache copy as an escape hatch) [2].

### SQ2: VS Code Extension Discovery and Loading

**Manifest-driven discovery (package.json):**
Every VS Code extension requires a `package.json` manifest declaring: `name`, `publisher`, `version`, `engines.vscode` (minimum VS Code version), `activationEvents`, `main` (entry module), and `contributes` (contribution points). The manifest is both the discovery mechanism and the capability declaration [5][6].

**Activation events for lazy loading:**
VS Code defines activation events for lazy extension loading. An extension's `activate()` function is called only once, when a matching event fires. Key activation events include [3]:
- `onLanguage:languageId` — file of specific language opened
- `onCommand:commandId` — command invoked
- `workspaceContains:glob` — workspace contains matching files
- `onView:viewId` — view becomes visible
- `onFileSystem:scheme` — file system scheme accessed
- `onUri` — URI opened for the extension
- `*` — eager activation (discouraged for performance)

**Extension host process architecture:**
Extensions run in dedicated Extension Host processes, separate from the VS Code renderer [4][9]. Three host types exist:
- **LocalProcess**: Node.js child process for desktop (IPC sockets)
- **LocalWebWorker**: Web Worker for browser/sandboxed contexts (postMessage)
- **Remote**: TCP socket to VS Code Server for remote development

The `AbstractExtHostExtensionService` receives the extension list from the main process, loads modules from disk, calls `activate(context)`, and manages per-extension state [9].

**RPC protocol:**
Communication between extension host and main process uses typed interfaces defined in `extHost.protocol.ts`. Method names use `$` prefixes (e.g., `$registerHoverProvider`). Both sides hold `ProxyIdentifier` objects as typed registry keys. Each activated extension receives its own scoped `vscode` namespace object [9].

**Contribution points (declarative registration):**
Extensions declare capabilities through `contributes` in package.json: commands, keybindings, menus, languages, themes, snippets, debuggers, views. This is static, declarative registration — the host reads contributions from the manifest without executing extension code [5][6].

### SQ3: Vim/Neovim Plugin Loading

**Runtime path scanning:**
Vim/Neovim discovers plugins by scanning the `runtimepath` option. Each directory in runtimepath is checked for well-known subdirectories: `plugin/` (always loaded at startup), `autoload/` (loaded on demand), `ftplugin/` (loaded per filetype), `lua/` (Neovim Lua modules) [10].

**Autoload (Vimscript):**
When a function with an autoload-style name (e.g., `somefile#function()`) is called, Vim looks for `autoload/somefile.vim`, sources it, then calls the function. This provides implicit lazy loading without any manifest or declaration — the function naming convention itself is the registration mechanism [10].

**Lua module loading (Neovim):**
Neovim searches every `runtimepath` directory for a `lua/` subdirectory. Modules are loaded via `require()` when first referenced. Plugin authors can provide a small `plugin/<name>.lua` that defines commands and keymappings but defers `require()` of the main module until invocation — a manual lazy loading pattern [10].

**Package system (packpath):**
Neovim supports a native package system via `packpath`. Start plugins (`pack/*/start/`) are loaded automatically. Optional plugins (`pack/*/opt/`) are loaded explicitly via `:packadd`. This is the foundation for plugin manager lazy loading [10].

**lazy.nvim (modern manager):**
lazy.nvim takes over the entire startup sequence, disabling Neovim's native plugin loading for maximum control. It provides automatic lazy-loading on events, commands, filetypes, and key mappings. Specifying any trigger implies `lazy = true`. It also automatically installs missing plugins before startup [11].

**No manifest:**
Vim/Neovim plugins have no formal manifest file. Discovery is purely directory-convention-based. Plugin metadata (name, description, version) has no standardized location — it lives in README files or vim-doc help files, not in a machine-readable format.

### SQ4: Other Extension Models

**JetBrains IntelliJ Platform:**
Plugins declare themselves via `plugin.xml`, containing: `<id>`, `<name>`, `<version>`, `<vendor>`, `<description>`, `<depends>` (dependencies on other plugins), `<extensions>` (implementations of extension points), `<actions>` (UI actions), and `<extensionPoints>` (points other plugins can extend) [12][13].

Extension points come in two types: interface extension points (plugin implements an interface) and bean extension points (plugin provides data). Extensions are registered declaratively in XML, and the IDE loads them lazily. Services use `getService()` and are instantiated on demand at three scopes: application, project, module [14].

JetBrains uses `since-build` and `until-build` attributes in the `<idea-version>` element for host compatibility ranges, enabling plugins to declare the IDE build range they support [13].

**Chrome Browser Extensions (Manifest V3):**
Chrome extensions use `manifest.json` declaring permissions, content scripts, service workers, and web-accessible resources. MV3 replaced persistent background pages with service workers that terminate when idle — a fundamental shift toward ephemeral execution [15].

Key MV3 security changes:
- Remote code execution banned (no `eval()`, no remotely-hosted code)
- Service workers have no DOM access
- Granular permissions model (host permissions requested separately)
- Content Security Policy tightened (no `unsafe-eval`)
- Sandboxed pages available for code needing `eval()` but with no extension API access [15]

**Figma:**
Figma's plugin system evolved through three sandboxing approaches: (1) iframes (too slow for document access), (2) Realms shim (found to have escape vulnerabilities), and (3) compiling QuickJS (a JavaScript VM written in C) to WebAssembly. The WASM approach provides strong isolation: plugin code runs in a WASM sandbox with no access to browser APIs, communicating only through explicit whitelisted APIs [16][17].

The architecture splits plugins into two parts: UI runs in an iframe, document manipulation runs in the QuickJS/WASM sandbox. This dual-context model prevents plugins from accessing the host application's JavaScript objects directly [16].

### SQ5: Sandboxing and Security Patterns

**Spectrum of isolation models:**

| System | Isolation Model | Plugin Access | Trust Model |
|--------|----------------|---------------|-------------|
| Vim/Neovim | None (in-process) | Full system access | Trust the developer |
| Claude Code | Process boundary + cache | `${CLAUDE_PLUGIN_ROOT}` scoping, path traversal blocked | Trust but verify (marketplace scanning) |
| VS Code | Separate process (Extension Host) | Full Node.js APIs within host process | Trust but isolate from renderer |
| JetBrains | In-process with API surface | Full JVM access within IDE process | Trust the developer |
| Chrome MV3 | Service worker + CSP + permissions | Declared permissions only, no remote code | Trust no one |
| Figma | WASM sandbox (QuickJS) | Whitelisted APIs only | Trust no one |

**Key patterns:**

1. **Process isolation** (VS Code): Extensions run in a separate Node.js process. Crashes don't affect the editor. But all extensions in the same host share the same runtime — one extension can monkey-patch globals affecting others [7][8][9].

2. **WASM sandboxing** (Figma): Strongest isolation. Plugin code cannot escape the sandbox because object representations are fundamentally different between host and sandbox. Performance cost: interpreted JS is slower than native execution [16][17].

3. **Permission-based** (Chrome MV3): Static permission declarations in manifest. Host grants/denies access at install time. Runtime enforcement through CSP and API surface restriction [15].

4. **Convention-based** (Claude Code): Path scoping rather than runtime sandboxing. Installed plugins are cached and cannot traverse outside their root. Scripts execute via `uv run` with explicit dependency isolation. Security comes from marketplace scanning + caching rather than runtime enforcement [2].

5. **No isolation** (Vim/Neovim, JetBrains): Full access to host process. Security relies entirely on user trust and code review. This is viable for developer tools where the user explicitly installs plugins they trust.

**VS Code's security gap:**
VS Code extensions have the same permissions as VS Code itself — they can read/write files, make network requests, run processes. There is no per-extension permission model. The marketplace uses malware scanning and clean-room VM testing, but runtime isolation between extensions is minimal (shared Node.js global scope) [8][9].

### SQ6: Versioning and Update Lifecycle

**Semantic versioning is universal:**
All systems use MAJOR.MINOR.PATCH. The interpretation is consistent: MAJOR for breaking changes, MINOR for backward-compatible additions, PATCH for bug fixes.

**Host compatibility mechanisms:**

| System | Mechanism | Example |
|--------|-----------|---------|
| VS Code | `engines.vscode` in package.json | `"^1.74.0"` |
| JetBrains | `<idea-version since-build="..." until-build="..."/>` | `since-build="223" until-build="231.*"` |
| Chrome | `minimum_chrome_version` in manifest.json | `"88"` |
| Claude Code | Version in plugin.json or marketplace.json | `"2.1.0"` |
| Vim/Neovim | None (convention only) | README mentions required features |

**Claude Code's cache-based distribution:**
Claude Code copies marketplace plugins to `~/.claude/plugins/cache`. Version determines update eligibility — if code changes without a version bump, users won't see updates due to caching. Version can be specified in either `plugin.json` or `marketplace.json` (plugin.json takes priority) [2].

**Dependency resolution varies widely:**
- VS Code: `extensionDependencies` in package.json, resolved by marketplace
- JetBrains: `<depends>` in plugin.xml, with optional config-file for soft dependencies
- Chrome: No inter-extension dependencies
- Neovim: Plugin managers (lazy.nvim) handle dependencies via configuration
- Claude Code: No formal dependency system between plugins

## Challenge

### Counter-evidence: Process isolation is not true sandboxing

VS Code's extension host provides stability isolation (crashes don't take down the editor) but not security isolation. All extensions in a single host share the Node.js runtime, global scope, and module cache. One extension can monkey-patch `fs`, `http`, or other core modules, affecting all other extensions. The 2024 research paper "Developers Are Victims Too" (arXiv:2411.07479) found significant security concerns in the VS Code extension ecosystem. Calling VS Code "sandboxed" overstates its security properties (HIGH — multiple T1 sources).

### Counter-evidence: Claude Code's prompt-based discovery has unique failure modes

When an LLM decides whether to invoke a skill based on description text, the failure mode is fundamentally different from programmatic activation. A poorly-written description means the skill is never activated, regardless of its code quality. No other system has this property — in VS Code, a registered `onCommand` handler always fires when the command is invoked. This makes Claude Code's model more fragile for discoverability, though more flexible for novel combinations (MODERATE — architectural reasoning).

### Counter-evidence: Manifest-less systems (Vim) can be more resilient

Vim's convention-based discovery (directory structure is the manifest) has no single point of failure for plugin loading. A malformed `plugin.xml` or `package.json` prevents an entire extension from loading, while a Vim plugin with a broken `autoload/` function only breaks that specific function. The manifest-less approach degrades more gracefully. However, it provides no metadata for discovery, dependency resolution, or tooling integration (MODERATE — design trade-off analysis).

### Counter-evidence: WASM sandboxing has significant performance costs

Figma chose to run plugin JavaScript through QuickJS compiled to WASM, which means interpreted execution rather than JIT-compiled native execution. For compute-intensive plugins, this is a meaningful performance penalty. Figma accepted this trade-off because plugin security in a web-facing design tool is non-negotiable, but for developer tools (where the user trusts their own plugins), this overhead is harder to justify (MODERATE — T1 source [16]).

## Findings

### 1. Manifest Files Are the Universal Contract Between Plugin and Host

Every surveyed system uses a declarative descriptor to register plugins with their host. The manifest serves three functions: identity (who is this plugin?), capability declaration (what does it contribute?), and activation specification (when should it load?).

| System | Manifest | Identity | Capabilities | Activation |
|--------|----------|----------|-------------|------------|
| Claude Code | plugin.json + SKILL.md frontmatter | name, description, version | skills/, commands/, agents/, hooks/ | LLM reads description text |
| VS Code | package.json | name, publisher, version | contributes{} | activationEvents[] |
| JetBrains | plugin.xml | id, name, version, vendor | extensions, actions, extensionPoints | on-demand service loading |
| Chrome MV3 | manifest.json | name, version, description | permissions, content_scripts, service_worker | Service worker events |
| Figma | manifest.json | name, id, api | parameters, editorType | User invocation |
| Vim/Neovim | None | Directory name | Directory conventions | runtimepath scanning |

The manifest is the key architectural decision in any plugin system. Claude Code's innovation is splitting the manifest across two layers: structural metadata in `plugin.json` and semantic capability descriptions in SKILL.md frontmatter, where the latter is consumed by an LLM rather than by code (HIGH — T1 sources converge across all systems [1][2][5][12][15]).

### 2. Lazy Loading Is the Dominant Activation Strategy

All mature plugin systems implement some form of deferred activation. The specific mechanisms vary but the principle is consistent: load plugin code only when it is actually needed.

**Activation trigger taxonomy:**

| Trigger Type | VS Code | Neovim | JetBrains | Chrome MV3 | Claude Code |
|-------------|---------|---------|-----------|------------|-------------|
| File type/language | `onLanguage:*` | `ftplugin/`, lazy.nvim `ft` | File type registration | content_scripts matches | N/A |
| Command invocation | `onCommand:*` | lazy.nvim `cmd` | Action registration | `onCommand` in service worker | `/skill-name` |
| Event/hook | `onView:*`, `onUri` | lazy.nvim `event` | Listener registration | Service worker events | Hook events |
| Workspace content | `workspaceContains:*` | N/A | N/A | N/A | N/A |
| Task context | N/A | N/A | N/A | N/A | LLM description matching |

Claude Code introduces a novel activation paradigm: task-context matching. Rather than predefined event types, the LLM evaluates skill descriptions against the current task and decides whether to activate. This is more flexible than event-based systems (can handle unanticipated combinations) but less predictable (activation depends on model judgment) (HIGH — T1 sources [1][3][11][12][15]).

### 3. Sandboxing Models Reflect Threat Models

The choice of sandboxing architecture directly reflects the system's threat model:

**Developer tools (Vim, JetBrains):** No sandboxing. The user is a developer who chooses and reviews their plugins. Security is the user's responsibility. This enables maximum flexibility and performance.

**IDE platforms (VS Code):** Process isolation for stability, not security. Extensions can't crash the editor, but they have full system access within the extension host process. The marketplace provides pre-installation scanning, but runtime enforcement is minimal [7][8][9].

**Web-facing applications (Figma, Chrome):** Strong sandboxing is mandatory. Figma uses WASM-compiled JavaScript VM, Chrome uses service workers with CSP and permission declarations. Neither system trusts plugin code with direct access to host internals [15][16][17].

**AI agent tools (Claude Code):** Structural isolation through caching and path scoping. Installed plugins are copied to a local cache, and path traversal outside the plugin root is blocked. Scripts execute via `uv run` with isolated dependencies. This is a lightweight model that relies on marketplace scanning plus structural constraints rather than runtime enforcement [2].

The trend across all systems is toward stronger isolation: Chrome MV2 → MV3 (background pages → service workers), VS Code renderer → sandboxed utility processes [7], Figma Realms → WASM [17]. No system has relaxed its security model (HIGH — T1 sources across all ecosystems).

### 4. Claude Code's Plugin Model Is Architecturally Distinct

Claude Code's plugin system differs from traditional extension architectures in several fundamental ways:

**No programmatic API.** Traditional systems expose a host API (VS Code's `vscode.*`, JetBrains' `com.intellij.*`, Chrome's `chrome.*`). Claude Code plugins are markdown documents and scripts — there is no SDK, no type system, no API surface to version.

**LLM-mediated invocation.** In every other system, the host calls the plugin's entry point (`activate()`, extension point implementation, service worker handler). In Claude Code, the LLM reads the skill description and decides to invoke it. The "API" is natural language.

**Progressive disclosure for token economics.** Claude Code's three-tier loading (metadata → full SKILL.md → resources) is optimized for context window constraints unique to LLM-based systems. Traditional lazy loading optimizes for process startup time and memory; Claude Code optimizes for prompt token budget [1][2].

**Convention-based components.** The plugin directory structure (`skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.lsp.json`, `settings.json`) uses convention-over-configuration — components are discovered by location, not declared in code. This mirrors Vim's directory-convention model more than VS Code's manifest-declared contribution points (HIGH — T1 sources [1][2]).

### 5. Version Management Is Converging but Incomplete

All systems use semantic versioning, but the sophistication of version management varies dramatically:

**Strong version management (VS Code, JetBrains):** Host compatibility ranges (`engines.vscode`, `since-build`/`until-build`), dependency version resolution, marketplace version diffing, automatic update detection.

**Moderate version management (Chrome, Claude Code):** Version tracking for updates, but limited dependency resolution. Claude Code's cache-based distribution means version bumps are mandatory for update propagation — changing code without bumping version is a silent failure [2].

**Minimal version management (Vim/Neovim):** Plugin managers track git commits, not semantic versions. There is no host compatibility declaration. Updates are "pull latest" with no compatibility guarantees.

No system surveyed has solved the fundamental version management problem for plugin ecosystems: how to evolve a host API without breaking existing plugins while avoiding API calcification. VS Code and JetBrains have the most mature approaches, using deprecation cycles and compatibility shims. Claude Code sidesteps the problem by having no programmatic API to version (MODERATE — comparative analysis across T1 sources).

### 6. Cross-Cutting Patterns: What All Systems Share

Despite architectural differences, several patterns appear in every system:

**Directory-as-namespace:** All systems use directory structure as organizational scaffolding. Claude Code: `skills/<name>/SKILL.md`. VS Code: `src/extension.ts`. JetBrains: `src/main/resources/META-INF/plugin.xml`. Chrome: root `manifest.json`. Vim: `plugin/`, `autoload/`, `lua/`.

**Declarative capability registration:** Capabilities are declared in metadata, not discovered through code introspection. Even Vim's convention-based approach is declarative — the directory name is the declaration.

**Marketplace as distribution + trust layer:** All systems with user-installed plugins have a marketplace (VS Code Marketplace, JetBrains Marketplace, Chrome Web Store, Figma Community, Claude Code Plugin Marketplace). Marketplaces serve dual functions: discovery/distribution and trust/verification.

**Hot-reload during development:** Claude Code (`/reload-plugins`), VS Code (Extension Development Host with auto-reload), Chrome (`chrome://extensions` reload button), JetBrains (Run Plugin configuration). All systems optimize the developer inner loop.

**Plugin isolation from other plugins:** Even in systems without host/plugin sandboxing, there is an expectation that plugins do not interfere with each other. VS Code's shared extension host is the notable exception — it provides no inter-extension isolation (HIGH — cross-system analysis).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claude Code auto-discovers components in default locations if plugin.json is omitted | factual | [1][2] | verified |
| 2 | VS Code extension host runs as a separate Node.js process | factual | [4][9] | verified |
| 3 | All extensions in a VS Code extension host share the same Node.js runtime and global scope | factual | [8][9] | verified |
| 4 | Figma moved from Realms-based sandboxing to QuickJS compiled to WebAssembly | factual | [16][17] | verified |
| 5 | Chrome Manifest V3 replaced background pages with service workers | factual | [15] | verified |
| 6 | Chrome MV3 bans remote code execution (no eval, no remotely-hosted code) | factual | [15] | verified |
| 7 | Claude Code caches installed marketplace plugins at ~/.claude/plugins/cache | factual | [2] | verified |
| 8 | Claude Code skills use three-tier progressive disclosure: ~100 tokens metadata, <5k tokens SKILL.md, then resources | factual | [1] | verified |
| 9 | VS Code extension host has same permissions as VS Code itself | factual | [8] | verified |
| 10 | JetBrains services are loaded on demand via getService() | factual | [14] | verified |
| 11 | lazy.nvim disables Neovim's native plugin loading completely | factual | [11] | verified |
| 12 | IntelliJ extension points come in two types: interface and bean | factual | [12] | verified |

## Takeaways

Plugin architecture is a solved problem at the pattern level — manifest-driven discovery, lazy activation, controlled API surfaces — but an unsolved problem at the security level. The six systems surveyed represent a spectrum from "trust everything" (Vim) to "trust nothing" (Figma WASM), with most production systems trending toward stronger isolation over time.

For WOS and Claude Code plugin development specifically:

1. **Description quality is the new API quality.** In LLM-mediated plugin systems, the textual description determines whether a plugin gets activated. Invest in description engineering the way traditional plugins invest in API design.

2. **Convention-over-configuration scales well.** Claude Code's directory-structure-as-manifest approach (shared with Vim) avoids the complexity of XML/JSON schema evolution while remaining discoverable. The trade-off is weaker tooling support for validation and dependency resolution.

3. **Cache-based distribution is a lightweight security boundary.** Copying plugins to a local cache with path traversal blocking provides meaningful isolation without runtime sandboxing overhead. This is appropriate for developer tools where the threat model is "supply chain compromise" rather than "untrusted code execution."

4. **Progressive disclosure is Claude Code's architectural innovation.** No other plugin system optimizes for context window token economics. This pattern — metadata → instructions → resources — is uniquely suited to LLM-hosted plugins and should be considered a first-class architectural concern.

5. **Version management needs explicit strategy.** The cache-based model means version bumps are mandatory for update propagation. A forgotten version bump is a silent deployment failure.
