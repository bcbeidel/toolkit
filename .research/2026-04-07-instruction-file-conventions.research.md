---
name: "Instruction File Conventions & Cross-Platform Standards"
description: "Survey of how AI coding tools structure instruction files and the status of cross-platform standardization in 2026"
type: research
sources:
  - https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  - https://openai.com/index/agentic-ai-foundation/
  - https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/
  - https://aaif.io/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation-aaif-anchored-by-new-project-contributions-including-model-context-protocol-mcp-goose-and-agents-md/
  - https://developers.openai.com/codex/guides/agents-md
  - https://agents.md/
  - https://code.claude.com/docs/en/memory
  - https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
  - https://docs.cline.bot/features/cline-rules
  - https://aider.chat/docs/usage/conventions.html
  - https://geminicli.com/docs/cli/gemini-md/
  - https://www.agentrulegen.com/guides/cursor-rules-guide
  - https://thepromptshelf.dev/blog/agents-md-vs-claude-md/
  - https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/
  - https://vibecoding.app/blog/agents-md-review
  - https://arxiv.org/html/2601.18341v1
  - https://www.deployhq.com/blog/ai-coding-config-files-guide
related: []
---

## Research Question

How do AI coding tools structure their instruction files, and what is the current state of cross-platform standardization as of 2026?

## Sub-Questions

1. How do AI coding tools (Claude Code, Cursor, Copilot, Windsurf, Codex, Cline, Aider, Gemini CLI) structure their instruction files in 2026?
2. What is the current adoption and governance status of AGENTS.md as a cross-platform standard?
3. How do hierarchical instruction files (root + subdirectory overrides) work across tools?
4. What metadata fields are supported and how do they vary across platforms?

## Search Protocol

| # | Query | Key Findings |
|---|-------|-------------|
| 1 | AGENTS.md Linux Foundation governance cross-platform AI coding standard 2025 2026 | AAIF formed Dec 9, 2025; 60k+ projects; founding members |
| 2 | Claude Code CLAUDE.md instruction file format documentation 2025 | Memory doc: 4-tier hierarchy, @ imports, .claude/rules/, path-scoped YAML frontmatter |
| 3 | Cursor .cursorrules cursor rules instruction file format 2025 2026 | Deprecated .cursorrules → .cursor/rules/*.mdc with YAML frontmatter |
| 4 | GitHub Copilot .github/copilot-instructions.md instruction files 2025 | .github/copilot-instructions.md + .github/instructions/*.instructions.md with applyTo frontmatter |
| 5 | Windsurf AI rules instruction files .windsurfrules format 2025 | .windsurf/rules/ directory; 6,000 char per file, 12,000 char combined limit |
| 6 | OpenAI Codex AGENTS.md support format specification 2025 | Full hierarchy spec; walks git root → CWD; configurable fallback filenames |
| 7 | Cline AI instruction files .clinerules format system prompt 2025 | .clinerules/ directory; paths frontmatter for conditional activation |
| 8 | Aider AI instruction files .aider.conf convention project settings 2025 | CONVENTIONS.md loaded via --read; .aider.conf.yml config |
| 9 | AGENTS.md specification adoption 60000 projects Codex Cursor Copilot 2025 | Broad adoption confirmed; agents.md official spec site |
| 10 | AI coding tools instruction file hierarchy subdirectory overrides global local project scoping 2025 | Comparative overview across tools; monorepo patterns |
| 11 | Gemini CLI GEMINI.md instruction file format 2025 2026 | GEMINI.md; global + workspace + just-in-time loading; @import syntax; configurable filename |
| 12 | AI coding instruction file metadata frontmatter YAML fields applyTo globs paths comparison 2025 | GitHub Copilot uses `applyTo`; Claude Code uses `paths`; Cursor uses `globs` |
| 13 | AGENTS.md vs CLAUDE.md cross-tool compatibility 2025 which to use monorepo | Practical coexistence patterns; CLAUDE.md can @import AGENTS.md |
| 14 | OpenAI AGENTS.md Agentic AI Foundation AAIF December 2025 governance membership | Platinum members confirmed; Linux Foundation directed fund |
| 15 | Fetch: linuxfoundation.org/press/aaif | Official announcement details; founding date Dec 9, 2025 |
| 16 | Fetch: developers.openai.com/codex/guides/agents-md | Full Codex spec: 32KiB default limit, AGENTS.override.md, config.toml customization |
| 17 | Fetch: docs.github.com/copilot/customizing-copilot | applyTo + excludeAgent frontmatter; 6-IDE support matrix |
| 18 | Fetch: agents.md | Open spec: no required fields; 25+ tools; closest file wins for monorepos |
| 19 | Fetch: docs.cline.bot/features/cline-rules | paths frontmatter; .clinerules/ directory; global vs workspace |
| 20 | Fetch: code.claude.com/docs/en/memory | Full Claude Code spec: 5-tier hierarchy, CLAUDE.local.md, managed policy, auto-memory |
| 21 | Fetch: agentrulegen.com/guides/cursor-rules-guide | MDC frontmatter fields: alwaysApply, description, globs |
| 22 | Fetch: geminicli.com/docs/cli/gemini-md | 3-tier hierarchy; context.fileName configurable; @import syntax |
| 23 | Fetch: aider.chat/docs/usage/conventions.html | CONVENTIONS.md; --read flag; no frontmatter |
| 24 | Fetch: thepromptshelf.dev/blog/agents-md-vs-claude-md | Side-by-side feature comparison table |
| 25 | Fetch: deployhq.com/blog/ai-coding-config-files-guide | Cross-tool comparison; limits; AGENTS.md as universal baseline |
| 26 | Fetch: vibecoding.app/blog/agents-md-review | 2026 review: 4 weaknesses; human authorship critical |
| 27 | Fetch: arxiv.org/html/2601.18341v1 | Academic study: 15-22% adoption rate; 55.8% single-file projects |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | Linux Foundation Announces the Formation of the Agentic AI Foundation (AAIF) | Linux Foundation | Dec 9, 2025 | T1 | verified |
| 2 | https://openai.com/index/agentic-ai-foundation/ | OpenAI co-founds the Agentic AI Foundation under the Linux Foundation | OpenAI | Dec 9, 2025 | T1 | verified |
| 3 | https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/ | OpenAI, Anthropic, and Block join new Linux Foundation effort | TechCrunch | Dec 9, 2025 | T3 | verified |
| 4 | https://developers.openai.com/codex/guides/agents-md | Custom instructions with AGENTS.md – Codex | OpenAI | 2025 | T1 | verified |
| 5 | https://agents.md/ | AGENTS.md — Open Standard | AAIF/OpenAI | 2025-2026 | T1 | verified |
| 6 | https://code.claude.com/docs/en/memory | How Claude remembers your project (CLAUDE.md) | Anthropic | 2025-2026 | T1 | verified |
| 7 | https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | Adding custom instructions for GitHub Copilot | GitHub/Microsoft | 2025-2026 | T1 | verified |
| 8 | https://docs.cline.bot/features/cline-rules | Cline Rules | Cline | 2025 | T1 | verified |
| 9 | https://aider.chat/docs/usage/conventions.html | Specifying coding conventions | Aider | 2025-2026 | T1 | verified |
| 10 | https://geminicli.com/docs/cli/gemini-md/ | Provide context with GEMINI.md files | Google | 2025-2026 | T1 | verified |
| 11 | https://www.agentrulegen.com/guides/cursor-rules-guide | The Complete Cursor Rules Guide (2026) | AgentRuleGen | 2026 | T3 | verified |
| 12 | https://thepromptshelf.dev/blog/agents-md-vs-claude-md/ | AGENTS.md vs CLAUDE.md: What's the Difference | The Prompt Shelf | 2026 | T3 | verified |
| 13 | https://tessl.io/blog/the-rise-of-agents-md-an-open-standard-and-single-source-of-truth-for-ai-coding-agents/ | The Rise of AGENTS.md: An Open Standard | Tessl.io | 2025 | T3 | verified |
| 14 | https://vibecoding.app/blog/agents-md-review | AGENTS.md Review 2026 — Open Standard for AI Agent | Vibe Coding App | 2026 | T4 | verified |
| 15 | https://arxiv.org/html/2601.18341v1 | Agentic Much? Adoption of Coding Agents on GitHub | Academic | Jan 2026 | T2 | verified |
| 16 | https://www.deployhq.com/blog/ai-coding-config-files-guide | CLAUDE.md, AGENTS.md, and Every AI Config File Explained | DeployHQ | 2025-2026 | T3 | verified |
| 17 | https://github.blog/changelog/2025-07-23-github-copilot-coding-agent-now-supports-instructions-md-custom-instructions/ | GitHub Copilot coding agent now supports .instructions.md | GitHub | Jul 23, 2025 | T1 | verified |
| 18 | https://www.infoq.com/news/2025/12/agentic-ai-foundation/ | OpenAI and Anthropic Donate AGENTS.md and MCP to New AAIF | InfoQ | Dec 2025 | T3 | verified |

## Raw Extracts

### Sub-question 1: How do AI coding tools structure their instruction files in 2026?

**Claude Code (Anthropic)**
The instruction file is `CLAUDE.md`. Claude Code implements a 5-tier hierarchy (managed policy → user global → project → local → subdirectory), loaded at the start of every session. Key features: [6]
- `CLAUDE.md` (project root) or `.claude/CLAUDE.md`
- `CLAUDE.local.md` for personal, gitignored overrides
- `~/.claude/CLAUDE.md` for user-global preferences
- Organization-managed policy at `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `/etc/claude-code/CLAUDE.md` (Linux)
- `.claude/rules/*.md` for scoped rules (unconditional or path-gated via YAML `paths` frontmatter)
- `@path/to/file` import syntax in any CLAUDE.md; recursive with 5-hop limit
- Files in ancestor directories load at launch; subdirectory files load on-demand when Claude accesses files there
- Recommended size: under 200 lines per file
- HTML comments (`<!-- ... -->`) stripped from context (maintainer notes pattern)
- Claude Code reads `CLAUDE.md`, not `AGENTS.md` natively; it recommends a CLAUDE.md that `@AGENTS.md` imports if both are needed

**OpenAI Codex**
Primary file is `AGENTS.md`. Discovery builds an instruction chain once per run: [4]
- Global: `~/.codex/AGENTS.override.md` → `AGENTS.md` (first non-empty wins)
- Project: walks from git root → CWD, checking each level for `AGENTS.override.md`, then `AGENTS.md`, then `project_doc_fallback_filenames`
- Files concatenate (root first, closest last); no merging logic — pure concatenation
- Default size cap: 32 KiB (`project_doc_max_bytes`); configurable up to 65,536 bytes
- `config.toml` lets teams add fallback filenames: `project_doc_fallback_filenames = ["TEAM_GUIDE.md", ".agents.md"]`
- Empty files skipped; chain rebuilds each run

**GitHub Copilot (Microsoft)**
Three distinct file types: [7][17]
- `.github/copilot-instructions.md` — repository-wide, always applied
- `.github/instructions/*.instructions.md` — path-scoped, YAML `applyTo` + optional `excludeAgent` frontmatter
- `AGENTS.md` or root `CLAUDE.md`/`GEMINI.md` — agent instructions (nearest file takes precedence)
Priority hierarchy: personal > repository > organization
Supported in: GitHub.com, VS Code, Visual Studio, JetBrains, Xcode, Eclipse (IDE support varies by feature)

**Cursor**
Evolved from `.cursorrules` (legacy, deprecated) to `.cursor/rules/*.mdc` (current): [11]
- `.cursorrules` — plain markdown at root, applied uniformly to all requests (backward compatible, still functional)
- `.cursor/rules/*.mdc` — MDC format (Markdown+YAML frontmatter) with 4 activation modes:
  - Always Apply (`alwaysApply: true`) — injected into every request
  - Auto Attach (via `globs`) — triggers on matching file patterns
  - Agent Requested (`description` only) — agent decides relevance from description
  - Manual (no frontmatter) — user @-mentions rule explicitly
- Priority: Team Rules > Project Rules > User Rules

**Windsurf (Codeium)**
Evolved from `.windsurfrules` (legacy) to `.windsurf/rules/*.md` (current): [5][16]
- `.windsurfrules` — single file, plain-text numbered rules, no activation modes (legacy)
- `.windsurf/rules/` — directory-based; GUI wrapper around markdown files
- Global rules: `global_rules.md`; workspace rules: `.windsurf/rules/`
- Hard limits: 6,000 characters per file, 12,000 characters combined total
- No YAML frontmatter documented for path-scoping in rules (unlike Cursor)

**Cline**
Uses `.clinerules/` directory system: [8]
- `.clinerules/` at project root (workspace scope, version-controlled)
- Global scope: `~/Documents/Cline/Rules` (cross-project personal preferences)
- Files: `.md` and `.txt`; optional numeric prefixes for ordering
- YAML frontmatter with `paths` field for conditional activation (glob patterns)
- Rules without frontmatter are always active; `paths: []` disables a rule
- Rules injected into system prompt between base instructions and tool definitions
- Workspace rules override global when conflicting; both combine otherwise

**Aider**
Convention-file approach; no auto-discovery: [9]
- Standard filename: `CONVENTIONS.md` (community convention, not enforced)
- Must be explicitly loaded via: `aider --read CONVENTIONS.md`, `/read` in-chat, or `read: CONVENTIONS.md` in `.aider.conf.yml`
- Loaded as read-only (prevents accidental modification by agent)
- Benefits from prompt caching when loaded via `--read`
- No YAML frontmatter; no path scoping; no hierarchy
- Multiple files supported: `read: [CONVENTIONS.md, style-guide.md]`

**Gemini CLI (Google)**
Uses `GEMINI.md` with a 3-tier hierarchy: [10]
- Global: `~/.gemini/GEMINI.md`
- Workspace: GEMINI.md files in configured workspace directories and parents
- Just-in-time: GEMINI.md in any directory accessed by a tool, scanning ancestors to trusted root
- All found files concatenated; footer shows count of active context files
- `@file.md` import syntax for modularization (relative and absolute paths)
- Configurable filename via `settings.json`: `context.fileName: ["AGENTS.md", "CONTEXT.md", "GEMINI.md"]` — Gemini CLI can be configured to read AGENTS.md natively
- `/memory show`, `/memory reload`, `/memory add` commands for inspection and editing

### Sub-question 2: What is the current adoption and governance status of AGENTS.md?

**Origin and Release**
AGENTS.md was released by OpenAI in August 2025. It emerged to solve fragmentation: each tool had its own format (CLAUDE.md, GEMINI.md, .cursorrules), forcing teams to maintain duplicate instructions. [13]

**Adoption Statistics**
- 60,000+ open-source repositories on GitHub use AGENTS.md as of late 2025 [1][5]
- Academic study (arxiv 2601.18341, January 2026) measured 15.85%–22.60% coding agent adoption rate across 129,134 GitHub projects; 7.89% have visible agent configuration files [15]
- Major adopters include projects from OpenAI, Apache Airflow, and Temporal
- OpenAI reportedly uses 88 separate AGENTS.md files internally across their monorepo [14]
- Supported tools: Codex, GitHub Copilot, Cursor, Windsurf, Amp, Factory, Devin, Gemini CLI, Jules, VS Code, Aider, RooCode, Zed, Warp, Continue.dev, OpenHands [5][14]

**Governance: Agentic AI Foundation (AAIF)**
On December 9, 2025, the Linux Foundation announced the AAIF with three founding projects: [1][2][3]
- Anthropic's Model Context Protocol (MCP)
- Block's goose
- OpenAI's AGENTS.md

AAIF operates as a directed fund under the Linux Foundation. Platinum members: Amazon Web Services, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI. Dozens of Gold and Silver members also joined.

Mission: "a neutral, open foundation to ensure this critical capability evolves transparently, collaboratively, and in ways that advance the adoption of leading open source AI projects" (Jim Zemlin, LF Executive Director).

**Current Limitations**
The 2026 review identified four weaknesses: [14]
1. No validation schema — any .md file named AGENTS.md counts; no linting or required sections
2. Quality dependency — human-authored files outperform auto-generated ones; auto-generation can degrade performance
3. Token cost — large instruction files accumulate processing overhead
4. Immaturity — best practices unsettled; GitHub Copilot's analysis of 2,500+ files revealed wide structural variation

### Sub-question 3: How do hierarchical instruction files work across tools?

**Pattern: Concatenation from broad → specific**
All major tools follow the same broad pattern: global/user-level instructions load first, then project root, then subdirectory-level instructions closest to the work. More specific files provide higher-priority context because they appear later in the concatenated context window.

**Claude Code** — most sophisticated hierarchy: [6]
- 5 scopes: managed policy (cannot be excluded) → user global → project root → local (gitignored) → subdirectory
- Ancestor CLAUDE.md files load at launch; descendant CLAUDE.md files load on-demand when Claude accesses files in those directories
- `claudeMdExcludes` setting lets teams skip irrelevant files in large monorepos
- `.claude/rules/` adds path-scoped rules loaded conditionally based on file patterns

**OpenAI Codex** — configurable walk: [4]
- Walks git root → CWD; each level checked for `AGENTS.override.md` then `AGENTS.md` then fallbacks
- Pure concatenation; no override/merge semantics — all files contribute
- `AGENTS.override.md` at any level replaces `AGENTS.md` at that level (allows personal per-directory overrides)

**Gemini CLI** — just-in-time loading: [10]
- Unique "just-in-time" behavior: when any tool accesses a directory, Gemini CLI scans that directory and ancestors for GEMINI.md files
- Enables lazy loading of deep project-specific instructions without loading everything at session start

**AGENTS.md (specification level)**: [5]
- "The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything"
- Subdirectory placement for monorepos is the documented pattern

**Cursor** — activation modes replace hierarchy: [11]
- Instead of a loading hierarchy, Cursor uses 4 activation modes (always/auto-attached/agent-requested/manual)
- Per-file glob matching in MDC frontmatter (`globs`) controls when rules become active
- No global → local precedence per se; rules coexist and may all be active simultaneously

**GitHub Copilot** — priority-based: [7]
- Explicit priority order: personal > repository > organization
- Path-specific instructions (`.github/instructions/*.instructions.md`) supplement (not replace) repository-wide instructions when file patterns match

**Cline** — workspace overrides global: [8]
- When workspace and global rules conflict, workspace rules win
- No subdirectory hierarchy documented for workspace rules

**Monorepo patterns**: [12][13][16]
- Common pattern: single AGENTS.md at root for shared conventions + per-package AGENTS.md for stack-specific guidance
- CLAUDE.md imports AGENTS.md to avoid duplication: `@AGENTS.md` at top of CLAUDE.md, with Claude-specific extensions below
- Gemini CLI can list multiple filenames in `context.fileName`, allowing a single AGENTS.md to serve multiple tools

### Sub-question 4: What metadata fields are supported and how do they vary?

**Summary: AGENTS.md and most tools use plain Markdown with no frontmatter.**
Path-scoping and activation control are tool-specific extensions layered on top of the open standard.

**Claude Code `.claude/rules/*.md`** — `paths` frontmatter: [6]
```yaml
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---
```
Rules without `paths` load unconditionally. `paths` triggers when Claude reads matching files. Glob syntax: `**/*.ts`, `src/**/*`, brace expansion `{ts,tsx}`.

**GitHub Copilot `.github/instructions/*.instructions.md`** — `applyTo` + `excludeAgent`: [7]
```yaml
---
applyTo: "app/models/**/*.rb"
excludeAgent: "code-review"
---
```
`applyTo` is required for scoped files. `excludeAgent` restricts which Copilot agent type uses the rule. `applyTo: "*"` matches all files.

**Cursor `.cursor/rules/*.mdc`** — `alwaysApply`, `description`, `globs`: [11]
```yaml
---
alwaysApply: true
description: "TypeScript coding standards"
globs:
  - "src/components/**"
---
```
`alwaysApply: true` bypasses all other conditions. `description` enables agent-requested mode (agent decides relevance). `globs` enables auto-attach based on active file.

**Cline `.clinerules/*.md`** — `paths` frontmatter: [8]
```yaml
---
paths:
  - "src/components/**"
  - "src/hooks/**"
---
```
Glob syntax: `*` (no slash), `**` (recursive), `?`, `[abc]`, `{a,b}`. Multiple `paths` patterns: any match activates the rule. `paths: []` explicitly disables a rule.

**AGENTS.md (all tools)** — no metadata: [5]
Free-form Markdown; no required sections, no frontmatter schema. "AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide."

**Aider** — no frontmatter: [9]
CONVENTIONS.md is plain Markdown with no metadata support. Control is via loading mechanism (`--read` flag), not file content.

**Gemini CLI** — filename configurability (not per-file metadata): [10]
Configuration is in `settings.json`, not in the files themselves:
```json
{ "context": { "fileName": ["AGENTS.md", "CONTEXT.md", "GEMINI.md"] } }
```

**Field naming divergence:**
The three tools that support path-scoping use different YAML field names:
- Claude Code / Cline: `paths`
- GitHub Copilot: `applyTo`
- Cursor: `globs` (with `alwaysApply` and `description` for additional control)

No cross-tool standardization of metadata fields exists as of 2026. Path-scoping is a per-tool extension, not part of the AGENTS.md standard.

## Findings

### Every major AI coding tool uses a different primary instruction filename

As of 2026, there is no single dominant filename. The landscape: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex, cross-platform standard), `.github/copilot-instructions.md` (GitHub Copilot), `.cursor/rules/*.mdc` (Cursor), `.windsurf/rules/*.md` (Windsurf), `.clinerules/` (Cline), `CONVENTIONS.md` (Aider), `GEMINI.md` (Gemini CLI) [1-18]. All tools evolved from single-file to directory-based structures between 2024-2026. HIGH confidence (T1 official docs for each tool).

### AGENTS.md is the cross-platform convergence point, but adoption is early

OpenAI released AGENTS.md in August 2025; the Agentic AI Foundation (AAIF) formed under the Linux Foundation on December 9, 2025 with Anthropic, Google, Microsoft, AWS, and OpenAI as Platinum members [1][2][5]. 60,000+ open-source repos have adopted it; 25+ tools support it [5]. However, an academic study (arxiv Jan 2026) found only 7.89% of studied GitHub projects have any agent configuration file [15]. AGENTS.md is a convention (free-form Markdown, no required fields, no schema) rather than a technical standard. MODERATE confidence that it becomes dominant; HIGH confidence it is already the best cross-platform baseline.

### The hierarchy pattern is universal: concatenate from global → project → local → subdirectory

All tools follow this broad-to-specific pattern [4][6][7][8][10]. Specifics vary: Claude Code has 5 tiers with on-demand subdirectory loading; Codex uses a configurable git-root walk; Gemini CLI adds just-in-time loading when tools access directories; Cursor replaces hierarchy with activation modes (always/auto-attach/agent-requested/manual). HIGH confidence for the pattern; MODERATE confidence that practitioners understand the Cursor divergence.

### Path-scoping metadata exists but uses incompatible field names across tools

Three tools support conditional rule activation via YAML frontmatter: Claude Code and Cline use `paths`, GitHub Copilot uses `applyTo`, Cursor uses `globs` (plus `alwaysApply`, `description`) [6][7][8][11]. AGENTS.md itself has no metadata schema. There is no standardization. A rule file cannot be shared across tools without modification. HIGH confidence (T1 sources converge).

### Practical coexistence: CLAUDE.md imports AGENTS.md

The recommended pattern for teams using multiple tools is: maintain one AGENTS.md for the cross-tool baseline and have CLAUDE.md `@AGENTS.md` at the top, with Claude-specific extensions below [12][13]. Gemini CLI can also be configured to read AGENTS.md natively via `context.fileName` in settings.json. This avoids duplicating shared conventions across files. MODERATE confidence (T3 practitioner sources; not documented in official T1 docs).

### Key canonical tools and references

- **AGENTS.md spec:** https://agents.md/ — official open spec, 25+ tool compatibility list
- **Claude Code docs:** https://code.claude.com/docs/en/memory — 5-tier hierarchy, path-scoped rules, import syntax
- **OpenAI Codex docs:** https://developers.openai.com/codex/guides/agents-md — full discovery spec, config.toml customization
- **Academic baseline:** arxiv 2601.18341 (Jan 2026) — adoption rate measurement methodology

## Challenge

### Claim: AGENTS.md is a cross-platform standard with broad adoption
**Strength of evidence:** MODERATE. The 60,000+ GitHub repos figure and Linux Foundation governance are well-sourced (T1). However, the academic study [15] (T2, arxiv) found only 7.89% of 129,134 projects have any visible agent configuration file, with AGENTS.md being one of several formats. "Cross-platform standard" risks overstating the state: the AAIF was only formed in December 2025, governance structures are early, and tools like Cursor and Windsurf have their own proprietary formats they continue to develop independently.

**Counter-evidence:** Cursor's `.mdc` format, Windsurf's directory-based system, and Claude Code's `CLAUDE.md` are all actively maintained separately. Many tools support AGENTS.md as one option among many rather than as the primary format. The "standard" is currently more a common convention than a technical specification.

### Claim: All tools follow a broad→specific concatenation hierarchy
**Strength of evidence:** HIGH for the pattern; MODERATE for the details. Every tool surveyed concatenates from broader to more specific scope, but the mechanisms differ significantly: Cursor uses activation modes rather than a true hierarchy, Aider requires explicit opt-in via `--read`, and Windsurf has hard character limits that break naive hierarchy assumptions.

**Counter-evidence:** Cursor's rule system is categorically different — it's selection by activation mode, not hierarchical inheritance. Calling it a "hierarchy" may mislead practitioners.

### Claim: Claude Code has the most sophisticated hierarchy (5 tiers)
**Strength of evidence:** MODERATE. The 5-tier description is accurate per Anthropic's documentation, but "most sophisticated" is a qualitative judgment. Gemini CLI's just-in-time loading is arguably more sophisticated in certain monorepo scenarios. The assessment reflects current documentation; features may change rapidly.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | AGENTS.md was released by OpenAI in August 2025 | attribution | [13] | verified |
| 2 | AAIF formed December 9, 2025 under the Linux Foundation | attribution | [1][2] | verified |
| 3 | Platinum AAIF members: AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI | attribution | [1] | verified |
| 4 | 60,000+ GitHub repos have adopted AGENTS.md | statistic | [1][5] | verified |
| 5 | Academic study measured 7.89% visible agent config files across 129,134 GitHub projects | statistic | [15] | verified |
| 6 | Claude Code has a 5-tier instruction hierarchy | attribution | [6] | verified |
| 7 | Codex default project_doc_max_bytes: 32 KiB (32,768 bytes), configurable to 65,536 | statistic | [4] | verified |
| 8 | Gemini CLI supports `context.fileName` list for multi-filename support | attribution | [10] | verified |
| 9 | Cursor deprecated `.cursorrules` in favor of `.cursor/rules/*.mdc` | attribution | [11] | verified |
| 10 | GitHub Copilot supports `applyTo` and `excludeAgent` frontmatter fields | attribution | [7] | verified |
| 11 | OpenAI reportedly uses 88 separate AGENTS.md files internally | statistic | [14] | human-review (T4 source only, not corroborated by OpenAI) |

### What this research does NOT cover
- Empirical performance comparisons: no evidence about whether more complex hierarchies improve agent output quality
- Adoption within enterprises vs. open-source (the 60k figure is GitHub public repos only)
- Windsurf-specific recent changes (some sources noted it is evolving rapidly)
