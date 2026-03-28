---
name: "AI Coding Assistant Conventions: Instruction Files, Context, and Extensibility"
description: "Landscape survey of how AI coding tools (Claude Code, GitHub Copilot, Cursor, Windsurf, Codex CLI, Cline, Aider) handle project context, instruction files, tool invocation, and skill/command systems — mapping common patterns and divergences across the ecosystem"
metadata:
  type: research
  sources:
    - https://claude.com/blog/using-claude-md-files
    - https://code.claude.com/docs/en/skills
    - https://code.claude.com/docs/en/overview
    - https://docs.cursor.com/context/rules
    - https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
    - https://code.visualstudio.com/docs/copilot/customization/custom-instructions
    - https://github.blog/changelog/2025-07-23-github-copilot-coding-agent-now-supports-instructions-md-custom-instructions
    - https://docs.windsurf.com/windsurf/cascade/memories
    - https://developers.openai.com/codex/guides/agents-md/
    - https://developers.openai.com/codex/skills/
    - https://docs.cline.bot/prompting/cline-memory-bank
    - https://cline.ghost.io/clinerules-version-controlled-shareable-and-ai-editable-instructions/
    - https://aider.chat/docs/usage/conventions.html
    - https://agents.md/
    - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
    - https://www.agentrulegen.com/guides/cursorrules-vs-claude-md
    - https://modelcontextprotocol.io/specification/2025-11-25
  related:
    - docs/research/plugin-extension-architecture.md
    - docs/research/context-engineering.md
    - docs/research/tool-design-for-llms.md
    - docs/research/workflow-orchestration.md
    - docs/context/instruction-file-conventions.md
    - docs/context/agents-md-standard.md
    - docs/context/context-injection-strategies.md
    - docs/context/mcp-extensibility-standard.md
    - docs/context/skill-command-system-landscape.md
---

## Summary

AI coding assistants have converged on a shared architectural pattern: a markdown file in the repository root that provides project-specific instructions to the AI before it begins work. Every major tool — Claude Code, GitHub Copilot, Cursor, Windsurf, Codex CLI, Cline, and Aider — implements some variant of this pattern, though file names, loading semantics, and advanced features diverge significantly. The ecosystem is consolidating around AGENTS.md as a cross-tool standard (now under the Linux Foundation's Agentic AI Foundation), while tool-specific files persist for proprietary features. MCP has become the universal protocol for tool extensibility, adopted by all major players. Skill/command systems remain the most divergent area, with each tool taking a distinct approach.

**Key findings:**

- **Instruction files have converged on markdown-in-repo.** All seven tools use markdown files committed to the repository for project context. The content is 90%+ identical across formats; differences are in file location, naming, and metadata schema (HIGH).
- **AGENTS.md is emerging as the cross-tool standard.** Adopted by 60,000+ projects and supported by Codex, Cursor, Copilot, Claude Code, Gemini CLI, and others, AGENTS.md is the closest thing to a universal instruction file, now stewarded by the Linux Foundation (HIGH).
- **Hierarchical precedence is universal.** Every tool supports directory-level instruction overrides where more specific (closer-to-file) instructions take precedence over root-level ones (HIGH).
- **MCP is the universal extensibility protocol.** Every major tool supports MCP for connecting to external tools and data sources. The November 2025 spec update and Linux Foundation stewardship have solidified it as an industry standard (HIGH).
- **Skill/command systems remain fragmented.** Claude Code has skills + commands, Codex has skills, Cursor has slash commands via CLI, Copilot has agents, Cline relies on MCP tools, Aider has in-chat commands. No convergence here yet (MODERATE).
- **Context injection strategies differ substantially.** Aider builds repo maps from AST analysis; Windsurf tracks editor actions in real-time; Cursor uses indexed retrieval; Claude Code reads files on demand. The "how" of context assembly is where tools differentiate most (MODERATE).

## Findings

### 1. Instruction File Conventions

Each tool has its own primary instruction file, but the underlying concept is identical: a markdown document in the repository that tells the AI how the codebase works.

| Tool | Primary File | Location | Format | Metadata |
|------|-------------|----------|--------|----------|
| Claude Code | `CLAUDE.md` | Project root | Markdown | `@path` imports |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/` dir | Markdown | None (plain) |
| Copilot (path-specific) | `*.instructions.md` | `.github/instructions/` | Markdown | YAML frontmatter (`applyTo` globs) |
| Cursor | `.cursor/rules/*.md` | `.cursor/rules/` dir | MDC (Markdown + YAML frontmatter) | `description`, `globs`, `alwaysApply` |
| Cursor (legacy) | `.cursorrules` | Project root | Plain text | None |
| Windsurf | `.windsurf/rules/*.md` | `.windsurf/rules/` dir | Markdown | Rule type metadata |
| Windsurf (legacy) | `.windsurfrules` | Project root | Plain text | None |
| Codex CLI | `AGENTS.md` | Project root + subdirs | Markdown | None (plain) |
| Cline | `.clinerules` | Project root | Markdown | None |
| Aider | `CONVENTIONS.md` | Project root | Markdown | None |
| Cross-tool | `AGENTS.md` | Project root + subdirs | Markdown | None (plain) |

**Key observations:**

- Cursor and Windsurf have both migrated from single root files (`.cursorrules`, `.windsurfrules`) to directory-based rule systems (`.cursor/rules/`, `.windsurf/rules/`), mirroring a broader trend toward modular, per-concern instruction files.
- Copilot added path-specific `.instructions.md` files with YAML frontmatter in July 2025, converging with Cursor's glob-based auto-attachment pattern.
- Claude Code's `CLAUDE.md` supports `@path` imports for composing instructions from multiple files — a unique feature for cross-referencing.
- Aider is model-agnostic by design: `CONVENTIONS.md` works across any LLM backend, unlike tool-specific files.

### 2. Instruction Hierarchy and Precedence

Every tool implements a layered instruction system where specificity increases with proximity to the working file.

**Claude Code:**
1. Enterprise policies (loaded first)
2. `~/.claude/CLAUDE.md` (personal/global)
3. Project root `CLAUDE.md`
4. Subdirectory `CLAUDE.md` files (closest wins)
5. User prompt (overrides everything)

Also reads `AGENTS.md` files in the directory tree. The nearest file to the current working context takes precedence.

**Codex CLI:**
1. Global `~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md` (first non-empty wins)
2. Repository root `AGENTS.md`
3. Subdirectory `AGENTS.md` files (concatenated root-down, later content overrides)
4. 32 KiB combined size limit (`project_doc_max_bytes`)

**Cursor:**
- Four rule types with different loading semantics:
  - **Always**: `alwaysApply: true` — included in every session
  - **Auto-Attached**: triggered when files matching `globs` pattern are referenced
  - **Agent-Requested**: description shown to agent, which decides whether to load
  - **Manual**: only loaded when explicitly invoked
- Legacy `.cursorrules` still functional but deprecated since v2.2

**GitHub Copilot:**
- `.github/copilot-instructions.md` loaded for all Copilot interactions
- `.github/instructions/*.instructions.md` with `applyTo` glob patterns for path-specific rules
- Path-specific instructions currently limited to coding agent and code review

**Windsurf:**
- Global rules in `~/.codeium/windsurf/memories/global_rules.md`
- Workspace rules in `.windsurf/rules/`
- Cascade assembles context: Rules → Memories → open files → indexed retrieval → recent actions
- Individual rule files capped at 6,000 characters; combined limit 12,000 characters

**Cline:**
- `.clinerules` for project-specific rules
- Memory Bank files loaded in dependency order: `projectBrief.md` → context files → `activeContext.md` → `progress.md`
- Custom instructions set globally in VS Code extension settings

**Aider:**
- `CONVENTIONS.md` loaded via `--read` flag or `.aider.conf.yml`
- Config files checked in order: home directory → git repo root → current directory (later files take priority)
- Also reads `AGENTS.md` files

### 3. Context Injection Strategies

Tools differ most in how they assemble context beyond instruction files.

**Repo-map approach (Aider):** Uses tree-sitter AST analysis to build a graph of the entire codebase, ranking files by relevance using a PageRank-like algorithm. Produces a compact "repo map" showing the most important classes, functions, and their signatures. This is the most sophisticated automated context strategy — no manual file selection needed.

**Flow-based tracking (Windsurf):** Cascade tracks edits, terminal commands, and navigation patterns in real-time, maintaining "deep awareness" of development patterns over time. Automatically generates Memories (persistent facts) from observed patterns.

**Indexed retrieval (Cursor):** Indexes the full codebase and uses semantic search to pull relevant code into context. Combined with explicit `@file` and `@folder` references.

**On-demand file reading (Claude Code):** Reads files as needed during task execution. Uses tool calls to search, read, and navigate. Skills and CLAUDE.md provide static context; dynamic context is assembled through tool use. Supports up to 10 concurrent subagents, each with 200K token context.

**Explicit file management (Cline):** Memory Bank pattern requires manual creation of structured documentation files. Cline starts each session with zero retained context and must reload from Memory Bank files.

**Copilot context:** Relies on open editor tabs, referenced files, and repository-level instructions. Agent mode adds file system access and terminal execution.

### 4. Tool Invocation and MCP Adoption

MCP (Model Context Protocol) has become the universal standard for extending AI coding tools with external capabilities.

| Tool | MCP Support | Configuration | Notes |
|------|------------|---------------|-------|
| Claude Code | Yes | `.mcp.json` | First-class; Anthropic created MCP |
| GitHub Copilot | Yes | `.vscode/mcp.json`, `.github/copilot/` | Agent mode + coding agent |
| Cursor | Yes | `.cursor/mcp.json` | One-click setup, OAuth support |
| Windsurf | Yes | Settings UI or config file | Integrated with Cascade |
| Codex CLI | Yes | `agents/openai.yaml` dependencies | Skills can declare MCP dependencies |
| Cline | Yes | `cline_mcp_settings.json` | Can create MCP servers on the fly |
| Aider | Limited | N/A | No native MCP; model-agnostic approach |

MCP crossed 97 million monthly SDK downloads by February 2026. The November 2025 spec update added server identity verification, async operations, and statelessness by default. In December 2025, Anthropic donated MCP to the Agentic AI Foundation under the Linux Foundation.

### 5. Skill and Command Systems

This is the most divergent area across tools. No two implementations are alike.

**Claude Code — Skills + Commands:**
- **Skills**: `SKILL.md` files with YAML frontmatter (`name`, `description`). Auto-discovered and loaded by context match. Support `!command` syntax for dynamic shell output injection. Persistent instructions, not one-shot.
- **Commands**: Markdown files in `.claude/commands/` that become `/slash-commands`. Explicitly invoked by users.
- **Subagents**: Specialized Claude instances for parallel subtask processing (up to 10 concurrent, each with 200K token context).
- **Hooks**: Event-driven scripts triggered by lifecycle events (pre-tool-use, post-tool-use, etc.).

**Codex CLI — Skills:**
- Skills are directories with `SKILL.md` plus optional scripts and references, stored in `~/.codex/skills/`.
- Two invocation modes: explicit (user invokes via `/skills` or `$` mention) and implicit (agent auto-selects based on task-description match).
- Skills can declare MCP server dependencies in `agents/openai.yaml`.
- Currently gated behind `--enable skills` feature flag.

**Cursor — Rules + CLI Commands:**
- Rules (`.cursor/rules/`) are the primary customization mechanism — no separate skill concept.
- CLI supports `/rules` for creating and managing rules, `/models` for model switching, `/mcp` for server management.
- Agent-requested rules function somewhat like implicit skills: the agent reads the description and decides whether to load them.

**GitHub Copilot — Agents + Extensions:**
- Custom agents configurable via `.github/copilot/` configuration.
- Agent mode handles multi-file editing, test execution, and self-healing.
- Copilot CLI (GA February 2026) ships with GitHub's MCP server built in and supports custom MCP servers.
- Extensions can bundle MCP servers, agents, skills, and hooks.

**Windsurf — Workflows:**
- Rules files define workflow patterns.
- Cascade automatically generates Memories from observed development patterns.
- No explicit skill/command system; extensibility primarily through MCP and rules.

**Cline — MCP-First Extensibility:**
- No built-in skill system. Extensibility is through MCP: users can ask Cline to "add a tool" and it creates an MCP server automatically.
- `.clinerules` provides static instructions but no dynamic invocation.
- Permission-based approval for all tool actions.

**Aider — In-Chat Commands:**
- `/add`, `/drop`, `/read`, `/load`, `/model`, and other in-chat commands.
- No skill or plugin system. Extensibility is through model selection and configuration.
- `/load` can execute arbitrary command sequences from files.

### 6. Cross-Tool Standardization: AGENTS.md

AGENTS.md represents the most significant convergence in the ecosystem. Key facts:

- **Origin:** Released by OpenAI in August 2025 as part of Codex CLI.
- **Adoption:** 60,000+ open source projects by December 2025.
- **Supporting tools:** Codex, Cursor, Copilot, Claude Code, Gemini CLI, Devin, Jules (Google), Factory, Amp, VS Code.
- **Governance:** Donated to the Agentic AI Foundation (AAIF) under the Linux Foundation in December 2025, alongside MCP and Goose. Platinum members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI.
- **Format:** Plain markdown. No required metadata schema. Hierarchical (subdirectory files override root).
- **Relationship to tool-specific files:** AGENTS.md provides shared cross-tool instructions; tool-specific files (CLAUDE.md, .cursorrules, etc.) add proprietary features on top.

The practical recommendation emerging from practitioners: put shared conventions in AGENTS.md, use tool-specific files only for features that AGENTS.md cannot express (e.g., Claude Code's `@path` imports, Cursor's glob-based auto-attachment).

## Challenges

**Counter-evidence and limitations:**

- **AGENTS.md adoption may be overstated.** The 60,000 project figure comes from AAIF announcements. Many of these may be trivial or auto-generated files, not carefully maintained instructions.
- **Convergence is superficial.** While all tools read markdown instruction files, the loading semantics, precedence rules, and metadata schemas differ enough that a single file cannot fully serve all tools without compromises.
- **MCP universality has gaps.** Aider does not natively support MCP. Tools implement different subsets of the MCP specification. Security concerns remain despite the November 2025 spec improvements.
- **Skill systems may not converge.** The fragmentation in skill/command systems reflects genuinely different architectural philosophies (Claude Code's persistent skills vs. Codex's explicit invocation vs. Cursor's rule-based approach). These may not converge because they serve different interaction models.
- **Context injection is the real differentiator.** Instruction files are table stakes. The competitive differentiation is in context assembly — Aider's repo maps, Windsurf's flow tracking, Cursor's indexed retrieval. These approaches are architecturally incompatible and unlikely to converge.

**Assumptions to check:**
- Assumption: AGENTS.md will become the README.md of AI coding. Risk: Tool vendors may resist ceding control to an open standard if it limits their ability to differentiate.
- Assumption: MCP is sufficient for tool extensibility. Risk: Complex workflows may need orchestration primitives that MCP's tool-call model does not provide.

**Premortem (what could make this research wrong):**
- A new dominant tool could emerge with a fundamentally different instruction paradigm.
- AAIF governance could stall, causing AGENTS.md and MCP evolution to fragment.
- Tool vendors could start reading each other's instruction files directly, making cross-tool files unnecessary.

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|------------|------|--------|------|
| 1 | https://claude.com/blog/using-claude-md-files | Using CLAUDE.MD files | Anthropic | 2025 | Active | T1 |
| 2 | https://code.claude.com/docs/en/skills | Extend Claude with Skills | Anthropic | 2025 | Active | T1 |
| 3 | https://docs.cursor.com/context/rules | Cursor Rules | Cursor/Anysphere | 2025 | Active | T1 |
| 4 | https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | Adding Custom Instructions for Copilot | GitHub/Microsoft | 2025 | Active | T1 |
| 5 | https://code.visualstudio.com/docs/copilot/customization/custom-instructions | Custom Instructions in VS Code | Microsoft | 2025 | Active | T1 |
| 6 | https://github.blog/changelog/2025-07-23-github-copilot-coding-agent-now-supports-instructions-md-custom-instructions | Copilot .instructions.md Support | GitHub | 2025-07 | Active | T1 |
| 7 | https://developers.openai.com/codex/guides/agents-md/ | Custom Instructions with AGENTS.md | OpenAI | 2025 | Active | T1 |
| 8 | https://developers.openai.com/codex/skills/ | Agent Skills | OpenAI | 2025 | Active | T1 |
| 9 | https://docs.windsurf.com/windsurf/cascade/memories | Cascade Memories | Windsurf/Codeium | 2025 | Active | T1 |
| 10 | https://docs.cline.bot/prompting/cline-memory-bank | Cline Memory Bank | Cline | 2025 | Active | T1 |
| 11 | https://cline.ghost.io/clinerules-version-controlled-shareable-and-ai-editable-instructions/ | .clinerules Instructions | Cline | 2025 | Active | T2 |
| 12 | https://aider.chat/docs/usage/conventions.html | Specifying Coding Conventions | Aider | 2025 | Active | T1 |
| 13 | https://agents.md/ | AGENTS.md Specification | AAIF/Linux Foundation | 2025 | Active | T1 |
| 14 | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | AAIF Formation | Linux Foundation | 2025-12 | Active | T1 |
| 15 | https://modelcontextprotocol.io/specification/2025-11-25 | MCP Specification | Anthropic/AAIF | 2025-11 | Active | T1 |
| 16 | https://www.agentrulegen.com/guides/cursorrules-vs-claude-md | Cursorrules vs CLAUDE.md vs Copilot | AgentRuleGen | 2025 | Active | T3 |
| 17 | https://simonwillison.net/2025/Dec/12/openai-skills/ | OpenAI Skills in Codex CLI | Simon Willison | 2025-12 | Active | T2 |
| 18 | https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/ | Copilot CLI GA | GitHub | 2026-02 | Active | T1 |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | All 7 major AI coding tools use markdown files in the repository for project instructions | Pattern | Sources 1-12 | Verified |
| 2 | AGENTS.md adopted by 60,000+ open source projects | Metric | Source 14 | Reported by AAIF; not independently verified |
| 3 | MCP crossed 97M monthly SDK downloads by Feb 2026 | Metric | Source 15, web search | Reported; not independently verified |
| 4 | Cursor deprecated .cursorrules in favor of .cursor/rules/ directory in v2.2 | Feature change | Source 3 | Verified via official docs |
| 5 | Copilot added path-specific .instructions.md with YAML frontmatter in July 2025 | Feature release | Source 6 | Verified via GitHub changelog |
| 6 | AGENTS.md donated to Linux Foundation AAIF in December 2025 | Governance | Source 14 | Verified via press release |
| 7 | Claude Code supports up to 10 concurrent subagents with 200K token context each | Architecture | Source 2 | Verified via official docs |
| 8 | Windsurf rules capped at 6,000 chars per file, 12,000 combined | Constraint | Source 9 | Reported; needs official docs verification |
| 9 | Codex CLI skills gated behind --enable skills flag | Feature status | Source 8, 17 | Verified |
| 10 | Aider does not natively support MCP | Gap | Source 12 | Verified; no MCP docs in Aider |
| 11 | Cline can auto-create MCP servers when asked to "add a tool" | Feature | Source 10 | Verified via docs |
| 12 | All tools except Aider support MCP for extensibility | Pattern | Sources 1-12 | Verified |

## Key Takeaways

1. **The instruction file pattern is settled.** Every tool uses markdown files in the repository. The remaining question is not "if" but "which file" — and AGENTS.md is winning the standardization race with Linux Foundation backing and broad tool adoption. Put shared conventions in AGENTS.md; use CLAUDE.md, .cursor/rules/, etc. only for tool-specific features.

2. **MCP is the extensibility standard.** With 97M monthly downloads and adoption by every major vendor except Aider, MCP is the way tools connect to external systems. The protocol is mature enough for production use, though security practices are still evolving.

3. **Context assembly is the frontier of differentiation.** Instruction files are table stakes. The competitive battleground is in how tools automatically discover and inject relevant context: Aider's AST-based repo maps, Windsurf's real-time flow tracking, Cursor's semantic indexing, and Claude Code's on-demand tool-based exploration represent fundamentally different philosophies.

4. **Skill/command systems have not converged and may not.** Claude Code's skills (persistent, auto-discovered), Codex's skills (directory-based, feature-flagged), Cursor's rules (glob-triggered), and Cline's MCP-first approach reflect genuinely different interaction models. Teams building cross-tool workflows should invest in AGENTS.md and MCP rather than tool-specific skill systems.

5. **The modular rules trend is accelerating.** Cursor, Windsurf, and Copilot have all moved from single-file instructions to directory-based, glob-scoped rule systems. This mirrors the broader software pattern of convention-over-configuration with escape hatches for specificity.

## Limitations

- This survey covers the state of the ecosystem as of early 2026. The space is evolving rapidly; tool capabilities may change within months.
- Aider and Cline have smaller teams and less official documentation than the others, making some claims harder to verify.
- Usage metrics (60K AGENTS.md adoptions, 97M MCP downloads) come from vendor/foundation announcements and were not independently verified.
- The survey focuses on instruction files, context, and extensibility. Other important dimensions (model selection, pricing, IDE integration quality, code generation accuracy) are out of scope.
- Windsurf was acquired by OpenAI in early 2026; its roadmap and integration status are in flux.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| Claude Code CLAUDE.md instruction file project context 2025 2026 | WebSearch | 2025-2026 | 10 | 3 |
| Cursor .cursorrules rules for AI project instructions convention 2025 | WebSearch | 2025 | 10 | 3 |
| GitHub Copilot .github/copilot-instructions.md project context custom instructions 2025 | WebSearch | 2025 | 10 | 3 |
| Windsurf AI coding assistant project context rules instructions configuration 2025 | WebSearch | 2025 | 10 | 2 |
| OpenAI Codex CLI AGENTS.md convention project context instructions 2025 | WebSearch | 2025 | 10 | 4 |
| Cline AI coding assistant .clinerules project context memory instructions 2025 | WebSearch | 2025 | 10 | 3 |
| Aider AI coding assistant conventions.md project context instructions configuration | WebSearch | 2025-2026 | 10 | 2 |
| AI coding tools MCP model context protocol tool invocation comparison 2025 2026 | WebSearch | 2025-2026 | 10 | 3 |
| Claude Code skills commands slash commands custom tools extensibility | WebSearch | 2025-2026 | 10 | 3 |
| GitHub Copilot agent mode extensions custom tools MCP integration 2025 2026 | WebSearch | 2025-2026 | 10 | 3 |
| Codex CLI skills system tool invocation custom commands extensibility OpenAI 2025 | WebSearch | 2025 | 10 | 4 |
| AGENTS.md standard specification Linux Foundation agentic AI 2025 2026 | WebSearch | 2025-2026 | 10 | 4 |
| "AI coding assistant" instruction files comparison convergence patterns | WebSearch | 2025-2026 | 10 | 3 |
| Cursor rules .mdc files frontmatter auto-attached always-on rule types 2025 | WebSearch | 2025 | 10 | 2 |
| Windsurf .windsurfrules cascade rules AI context management 2025 | WebSearch | 2025 | 10 | 2 |
| GitHub Copilot custom instructions .instructions.md path-specific YAML frontmatter 2025 | WebSearch | 2025 | 10 | 3 |
| Cline VS Code tool use commands MCP support extensibility 2025 | WebSearch | 2025 | 10 | 2 |
