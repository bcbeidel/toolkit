---
name: "Plugin and Extension Architecture Patterns"
description: "Universal patterns in plugin systems — manifest-driven discovery, lazy activation, sandboxing spectrums — and how Claude Code's LLM-mediated, prompt-based model diverges from traditional programmatic extension APIs"
metadata:
  type: reference
  sources:
    - https://code.claude.com/docs/en/plugins
    - https://code.claude.com/docs/en/plugins-reference
    - https://code.visualstudio.com/api/references/activation-events
    - https://code.visualstudio.com/api/advanced-topics/extension-host
    - https://www.figma.com/blog/how-we-built-the-figma-plugin-system/
    - https://developer.chrome.com/docs/extensions/develop/migrate/what-is-mv3
    - https://plugins.jetbrains.com/docs/intellij/plugin-extensions.html
  related:
    - docs/research/plugin-extension-architecture.md
    - docs/context/tool-design-for-llms.md
    - docs/context/context-window-management.md
---

Plugin systems across six ecosystems (Claude Code, VS Code, JetBrains, Vim/Neovim, Chrome, Figma) converge on three universal patterns but diverge sharply on execution models. Claude Code's architecture is fundamentally distinct from all others surveyed.

## Three Universal Patterns

**Manifest-driven discovery.** Every system uses a declarative descriptor (plugin.json, package.json, plugin.xml, manifest.json, SKILL.md frontmatter) as the contract between plugin and host. The manifest handles identity, capability declaration, and activation specification. Vim is the sole exception, using directory conventions as an implicit manifest.

**Lazy activation.** All mature systems defer plugin loading until needed. VS Code uses activation events (`onLanguage`, `onCommand`), Neovim uses autoload naming conventions and lazy.nvim triggers, JetBrains uses on-demand service loading via `getService()`. Eager loading is universally discouraged for performance reasons.

**Declarative capability registration.** Capabilities are declared in metadata rather than discovered through code introspection. Even Vim's convention-based model is declarative — the directory name is the declaration.

## Claude Code's Architectural Divergence

Claude Code's plugin system differs from traditional extension architectures in three fundamental ways.

**No programmatic API.** Traditional systems expose typed host APIs (VS Code's `vscode.*`, JetBrains' `com.intellij.*`, Chrome's `chrome.*`). Claude Code plugins are markdown documents and scripts. There is no SDK, no type system, no API surface to version. This sidesteps the unsolved problem of evolving a host API without breaking existing plugins.

**LLM-mediated invocation.** In every other system, the host calls the plugin's entry point when a matching event fires. In Claude Code, the LLM reads skill descriptions and decides whether to invoke. The SKILL.md `description` field is functionally equivalent to an activation event — description quality determines whether a skill gets activated, making it load-bearing for functionality rather than just metadata.

**Progressive disclosure for token economics.** Claude Code's three-tier loading is unique: session start shows only name and description (~100 tokens per skill), relevance triggers full SKILL.md loading (<5k tokens), and resources load on demand. Traditional lazy loading optimizes for process startup time and memory. Claude Code optimizes for context window budget. No other plugin system has this constraint.

## Sandboxing Reflects Threat Models

Isolation models span a wide spectrum, driven by who the system trusts:

- **No isolation** (Vim, JetBrains): In-process, full system access. The user is a developer who trusts their own plugins.
- **Process isolation** (VS Code): Extensions run in a separate Node.js process for stability, but all extensions share the runtime. One extension can monkey-patch globals affecting others — this is stability isolation, not security isolation.
- **Structural isolation** (Claude Code): Marketplace plugins are cached locally with path traversal blocked. Scripts execute via `uv run` with dependency isolation. Security comes from marketplace scanning plus structural constraints rather than runtime enforcement.
- **Strong sandboxing** (Chrome MV3, Figma): Chrome uses service workers with CSP and permission declarations. Figma compiles QuickJS to WebAssembly, providing the strongest isolation at the cost of interpreted (not JIT-compiled) execution performance.

The industry trend is consistently toward stronger isolation: Chrome MV2 to MV3, VS Code to sandboxed utility processes, Figma from Realms to WASM. No system has relaxed its security model.

## Implications for WOS

Description engineering matters as much as API design in LLM-mediated systems. A poorly-written skill description is functionally equivalent to a broken activation event — the skill never gets invoked regardless of code quality.

Convention-over-configuration (directory structure as manifest) scales well and avoids schema evolution complexity, but trades off tooling support for validation and dependency resolution.

Cache-based distribution requires explicit version management. Changing plugin code without bumping the version is a silent deployment failure — users will not see updates due to caching.
