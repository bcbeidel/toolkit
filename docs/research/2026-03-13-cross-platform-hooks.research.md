---
name: "Cross-Platform Hook Mechanisms in AI Coding Agents"
description: "Landscape analysis of hook types, enforcement models, and portability across 15 AI coding agent platforms"
metadata:
  type: research
  sources:
    - https://code.claude.com/docs/en/hooks
    - https://code.claude.com/docs/en/hooks-guide
    - https://claude.com/blog/how-to-configure-hooks
    - https://cursor.com/docs/hooks
    - https://cursor.com/docs/rules
    - https://cursor.com/docs/cloud-agent/automations
    - https://cursor.com/docs/reference/third-party-hooks
    - https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot
    - https://docs.github.com/en/copilot/customizing-copilot/customizing-the-development-environment-for-copilot-coding-agent
    - https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review
    - https://docs.windsurf.com/windsurf/cascade/hooks
    - https://docs.windsurf.com/windsurf/cascade/skills
    - https://aider.chat/docs/usage/lint-test.html
    - https://aider.chat/docs/config/options.html
    - https://aider.chat/docs/usage/conventions.html
    - https://docs.continue.dev/customize/deep-dives/rules
    - https://docs.cline.bot/customization/hooks
    - https://docs.cline.bot/customization/cline-rules
    - https://developers.openai.com/codex/rules/
    - https://developers.openai.com/codex/guides/agents-md/
    - https://docs.devin.ai/product-guides/using-playbooks
    - https://docs.augmentcode.com/cli/hooks
    - https://docs.augmentcode.com/cli/rules
    - https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html
    - https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html
    - https://sourcegraph.com/docs/cody/enterprise/features
    - https://docs.replit.com/replitai/replit-dot-md
  related:
    - docs/research/ai-coding-assistant-conventions.md
    - docs/research/plugin-extension-architecture.md
---

## Key Findings

Only 5 of 15 platforms surveyed offer true lifecycle hooks that can block agent actions programmatically. The industry has converged on advisory instruction files (rules, AGENTS.md) but enforcement mechanisms remain fragmented and platform-specific. A cross-platform hook abstraction is not currently viable — the models differ too fundamentally — but AGENTS.md provides a portable advisory layer, and the Claude Code hook model (PreToolUse/PostToolUse with JSON stdin/stdout) is emerging as the de facto pattern adopted by Cursor, Windsurf, Cline, and Augment Code.

## Search Protocol

| # | Query | Platform | Results Used |
|---|-------|----------|-------------|
| 1 | "Claude Code hooks PreToolUse PostToolUse" | Web | 3 |
| 2 | "Claude Code hooks settings.json configuration" | Web | 2 |
| 3 | "Cursor IDE hooks rules enforcement" | Web | 4 |
| 4 | "Cursor third-party hooks Claude Code compatibility" | Web | 1 |
| 5 | "GitHub Copilot hooks custom instructions" | Web | 3 |
| 6 | "GitHub Copilot coding agent setup steps" | Web | 2 |
| 7 | "Windsurf Cascade hooks .windsurfrules" | Web | 3 |
| 8 | "Aider auto-lint auto-test hooks" | Web | 3 |
| 9 | "Continue dev rules hooks config" | Web | 2 |
| 10 | "Cline hooks .clinerules" | Web | 3 |
| 11 | "OpenAI Codex CLI execpolicy rules" | Web | 3 |
| 12 | "Devin Cognition hooks playbooks" | Web | 3 |
| 13 | "Amazon Q Developer project rules" | Web | 2 |
| 14 | "JetBrains AI Assistant project rules" | Web | 2 |
| 15 | "Sourcegraph Cody pre-instructions context filters" | Web | 2 |
| 16 | "Augment Code hooks PreToolUse rules" | Web | 3 |
| 17 | "Replit Agent replit.md hooks" | Web | 2 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/hooks | Hooks Reference | Anthropic | 2025 | T1 | verified |
| 2 | https://code.claude.com/docs/en/hooks-guide | Automate Workflows with Hooks | Anthropic | 2025 | T1 | verified |
| 3 | https://claude.com/blog/how-to-configure-hooks | How to Configure Hooks | Anthropic | 2025-12-11 | T1 | verified |
| 4 | https://cursor.com/docs/hooks | Cursor Hooks Documentation | Cursor (Anysphere) | 2026 | T1 | verified |
| 5 | https://cursor.com/docs/rules | Cursor Rules Documentation | Cursor (Anysphere) | 2026 | T1 | verified |
| 6 | https://cursor.com/docs/cloud-agent/automations | Cloud Agent Automations | Cursor (Anysphere) | 2026-03-05 | T1 | verified |
| 7 | https://cursor.com/docs/reference/third-party-hooks | Third-Party Hooks | Cursor (Anysphere) | 2026 | T1 | verified |
| 8 | https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot | Adding Custom Instructions | GitHub | 2026 | T1 | verified |
| 9 | https://docs.github.com/en/copilot/customizing-copilot/customizing-the-development-environment-for-copilot-coding-agent | Coding Agent Environment | GitHub | 2026 | T1 | verified |
| 10 | https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review | Using Copilot Code Review | GitHub | 2026 | T1 | verified |
| 11 | https://docs.windsurf.com/windsurf/cascade/hooks | Cascade Hooks | Windsurf (Codeium) | 2025 | T1 | verified |
| 12 | https://docs.windsurf.com/windsurf/cascade/skills | Cascade Skills | Windsurf (Codeium) | 2026 | T1 | verified |
| 13 | https://aider.chat/docs/usage/lint-test.html | Linting and Testing | Aider | 2026 | T1 | verified |
| 14 | https://aider.chat/docs/config/options.html | Configuration Options | Aider | 2026 | T1 | verified |
| 15 | https://aider.chat/docs/usage/conventions.html | Conventions | Aider | 2026 | T1 | verified |
| 16 | https://docs.continue.dev/customize/deep-dives/rules | Rules | Continue | 2026 | T1 | verified |
| 17 | https://docs.cline.bot/customization/hooks | Hooks | Cline | 2026 | T1 | verified |
| 18 | https://docs.cline.bot/customization/cline-rules | Cline Rules | Cline | 2026 | T1 | verified |
| 19 | https://developers.openai.com/codex/rules/ | Rules | OpenAI | 2025 | T1 | verified |
| 20 | https://developers.openai.com/codex/guides/agents-md/ | Custom Instructions with AGENTS.md | OpenAI | 2025 | T1 | verified |
| 21 | https://docs.devin.ai/product-guides/using-playbooks | Using Playbooks | Cognition (Devin) | 2026 | T1 | verified |
| 22 | https://docs.augmentcode.com/cli/hooks | Hooks | Augment Code | 2026 | T1 | verified |
| 23 | https://docs.augmentcode.com/cli/rules | Rules & Guidelines | Augment Code | 2026 | T1 | verified |
| 24 | https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/context-project-rules.html | Project Rules | AWS | 2025 | T1 | verified |
| 25 | https://www.jetbrains.com/help/ai-assistant/configure-project-rules.html | Configure Project Rules | JetBrains | 2025 | T1 | verified |
| 26 | https://sourcegraph.com/docs/cody/enterprise/features | Enterprise Features | Sourcegraph | 2026 | T1 | verified |
| 27 | https://docs.replit.com/replitai/replit-dot-md | replit.md | Replit | 2026 | T1 | verified |
| 28 | https://github.com/anthropics/claude-code/issues/11226 | Security Gap: Hooks Cannot Be Protected | GitHub Issue | 2025 | T4 | verified |

## Platform Analysis

### Platforms with Lifecycle Hooks (5 of 15)

#### Claude Code (Anthropic)

The most comprehensive hook system surveyed. **18 hook events** across the full agent lifecycle, with **4 handler types** (command, HTTP, prompt, agent).

**Hook events:**

| Event | Can Block? | Handler Types |
|-------|-----------|---------------|
| SessionStart | No | command |
| SessionEnd | No | command |
| InstructionsLoaded | No | command |
| UserPromptSubmit | Yes | all 4 |
| PreToolUse | Yes | all 4 |
| PostToolUse | No | all 4 |
| PostToolUseFailure | No | all 4 |
| PermissionRequest | Yes | all 4 |
| Notification | No | command |
| SubagentStart | No | command |
| SubagentStop | Yes | all 4 |
| Stop | Yes | all 4 |
| TeammateIdle | Yes | command |
| TaskCompleted | Yes | command |
| ConfigChange | Yes | command |
| WorktreeCreate | Yes | command |
| WorktreeRemove | No | command |
| PreCompact | No | command |

**Handler types:**
- **command** — shell script, JSON via stdin/stdout, exit code 0/2/other
- **HTTP** — POST to URL, JSON request/response, configurable headers
- **prompt** — single-turn LLM evaluation (Haiku default), returns ok/reason
- **agent** — multi-turn subagent with Read/Grep/Glob tools, up to 50 turns

**Blocking model:** PreToolUse exit code 2 blocks tool execution with stderr as error message. Can also modify tool inputs via `updatedInput`, auto-approve via `permissionDecision: "allow"`, or force user confirmation via `permissionDecision: "ask"`. Universal `continue: false` halts the entire session.

**Configuration:** JSON in `~/.claude/settings.json` (user), `.claude/settings.json` (project), `.claude/settings.local.json` (local), managed policy, plugin `hooks/hooks.json`, or skill/agent YAML frontmatter.

**Matchers:** Regex on tool name (PreToolUse/PostToolUse), session source (SessionStart), end reason (SessionEnd), notification type, agent type, compaction trigger, config source.

**Unique capabilities:** Prompt and agent handler types (LLM-evaluated hooks), HTTP hooks for external services, `updatedInput` for tool input modification, `updatedMCPToolOutput` for MCP output replacement, async hooks (`"async": true`), `once: true` for single-fire skill hooks, enterprise `allowManagedHooksOnly` policy.

#### Cursor (Anysphere)

**20 hook events** with a design closely mirroring Claude Code. Cursor explicitly loads hooks from Claude Code's `.claude/settings.json` files, translating event and tool names automatically.

**Hook events (beyond Claude Code overlap):**

| Event | Can Block? | Cursor-Only? |
|-------|-----------|-------------|
| beforeShellExecution | Yes | Yes |
| afterShellExecution | No | Yes |
| beforeMCPExecution | Yes | Yes |
| afterMCPExecution | No | Yes |
| beforeReadFile | Yes | Yes |
| afterFileEdit | No | Yes |
| beforeTabFileRead | Yes | Yes |
| afterTabFileEdit | No | Yes |
| beforeSubmitPrompt | Yes | Yes |
| afterAgentResponse | No | Yes |
| afterAgentThought | No | Yes |
| stop (with followup_message) | Auto-continue | Yes |

**Handler types:** command (shell scripts) and prompt (LLM-evaluated). No HTTP or agent types.

**Configuration:** `hooks.json` at enterprise (MDM), team (cloud dashboard), project (`.cursor/hooks.json`), or user (`~/.cursor/hooks.json`) levels. Version field required (`"version": 1`).

**Cross-platform compatibility:** Cursor reads Claude Code's `.claude/settings.json` and `.claude/settings.local.json` hook definitions, auto-translating event names and tool names. Requires "Third-party skills" enabled in settings.

**Unique capabilities:** `failClosed` option (block on hook failure), `loop_limit` for auto-continue loops, `followup_message` for chaining, cloud agent automations (GitHub/Slack/Linear/PagerDuty/webhook triggers), Tab-specific hooks (beforeTabFileRead, afterTabFileEdit).

#### Windsurf (Codeium)

**12 hook events** focused on tool-level pre/post interception.

**Hook events:**

| Event | Can Block? |
|-------|-----------|
| pre_read_code | Yes |
| pre_write_code | Yes |
| pre_run_command | Yes |
| pre_mcp_tool_use | Yes |
| pre_user_prompt | Yes |
| post_read_code | No |
| post_write_code | No |
| post_run_command | No |
| post_mcp_tool_use | No |
| post_cascade_response | No |
| post_cascade_response_with_transcript | No |
| post_setup_worktree | No |

**Handler type:** Command only. JSON via stdin with `agent_action_name`, `trajectory_id`, `execution_id`, `timestamp`, and tool-specific `tool_info`. Exit code 0 = proceed, 2 = block.

**Configuration:** `hooks.json` at system (`/Library/Application Support/Windsurf/hooks.json`), user (`~/.codeium/windsurf/hooks.json`), workspace (`.windsurf/hooks.json`), or enterprise cloud dashboard. All levels merge.

**Unique capabilities:** Transcript-inclusive hook (`post_cascade_response_with_transcript` with full JSONL), worktree setup hook, enterprise cloud dashboard distribution, granular file-operation hooks (separate read/write).

#### Cline

**8 hook events** with a clean JSON I/O model.

| Event | Can Block? |
|-------|-----------|
| TaskStart | Yes |
| TaskResume | Yes |
| TaskCancel | Yes |
| TaskComplete | Yes |
| PreToolUse | Yes |
| PostToolUse | Yes |
| UserPromptSubmit | Yes |
| PreCompact | Yes |

**I/O model:** JSON via stdin (task metadata, hook name, timestamp, workspace roots, user ID, model details). Output JSON with `cancel` (boolean), `contextModification` (optional text), `errorMessage`.

**Handler type:** Executable scripts (bash/shell on Unix, PowerShell on Windows). Must be `chmod +x`.

**Configuration:** Global (`~/Documents/Cline/Hooks/`) or project (`.clinerules/hooks/`). Global hooks execute first; either level can cancel.

**Cross-tool rule reading:** Cline also reads `.cursorrules`, `.windsurfrules`, and `AGENTS.md` files.

**Unique capabilities:** Task lifecycle hooks (TaskStart/Resume/Cancel/Complete), `contextModification` for injecting text into agent context, PostToolUse can also cancel (unlike other platforms where post-hooks are observational).

#### Augment Code

**3 hook events** that closely mirror Claude Code's architecture.

| Event | Can Block? |
|-------|-----------|
| PreToolUse | Yes (exit code 2) |
| PostToolUse | No |
| Stop | Yes |

**Handler type:** Command only. Same exit code convention as Claude Code (0 = proceed, 2 = block).

**Configuration:** `hooks/hooks.json`. Rules in `.augment/rules/` (workspace) or `~/.augment/rules/` (user). Three rule types: Always, Manual, Auto (model-decided).

**Additional enforcement:** Tool permissions — fine-grained allow/deny rules for specific tool names. Deny rules block operations regardless of hooks.

### Platforms with Advisory Systems Only (7 of 15)

#### GitHub Copilot

**No lifecycle hooks.** Instructions are purely advisory — Copilot reads them as context but cannot be forced to comply.

- `.github/copilot-instructions.md` — repository-wide advisory instructions
- `.github/instructions/*.instructions.md` — path-specific with `applyTo` globs and `excludeAgent` frontmatter
- `copilot-setup-steps.yml` — environment setup for coding agent (runs before agent starts, not a general hook)
- Content exclusion — the only true blocking mechanism (blocks suggestions for excluded file paths)
- Code review — always leaves "Comment" reviews, never "Approve" or "Request changes"
- AGENTS.md / CLAUDE.md / GEMINI.md — read by coding agent, advisory

#### Amazon Q Developer

**No hooks.** Project rules in `.amazonq/rules/*.md` are explicitly advisory: "output is advisory in nature and does not guarantee completeness, correctness, or enforcement."

#### JetBrains AI Assistant

**No hooks.** Project rules in `.aiassistant/rules/*.md` with three activation modes (Always, File pattern, Off). Known limitation: rules don't consistently override specialized AI Actions that use hidden system prompts.

#### Sourcegraph Cody

**No lifecycle hooks.** Admin pre-instructions (advisory), context filters (blocking — excluded repos inaccessible), deprecated guardrails (previously blocking for code attribution). Custom commands in `.vscode/cody.json`.

#### Replit Agent

**No hooks.** `replit.md` provides advisory context. Replit uses "decision-time guidance" — situational instructions injected at key moments rather than static rules. Reads AGENTS.md when present.

#### Tabnine

**No hooks.** Admin-managed Code Review rules (140+ predefined per language) flag violations on PRs with severity levels. Custom chat behavior via settings. Advisory only.

### Platforms with Alternative Enforcement Models (3 of 15)

#### OpenAI Codex CLI

**No lifecycle hooks per se, but a robust execution policy (execpolicy) system.** Rules evaluate commands before execution with three decisions: `allow`, `prompt` (require user approval), or `forbidden` (block). Most restrictive matching rule wins. Rules stored in `~/.codex/rules/` (TOML format). AGENTS.md read for instructions. This is true blocking enforcement but only at the command/shell level, not for file operations.

#### Aider

**No lifecycle hooks, but purpose-built lint/test automation.**
- `--auto-lint` (default on) — automatic linting after every AI edit using tree-sitter based linters
- `--lint-cmd` — custom linter, per-language configuration
- `--auto-test` — automatic test execution after AI edits
- `--git-commit-verify` — opt-in pre-commit hook enforcement (off by default)
- `--watch-files` — file monitor for AI comments (`AI!`, `AI?`)
- `CONVENTIONS.md` loaded via `--read` flag

Aider's approach is narrower but deeply integrated: linting and testing are first-class automation rather than generic hooks.

#### Devin (Cognition)

**Mixed model.** Playbooks and Knowledge are advisory. Admin-level deny/ask rules are blocking (persist even in bypass mode). Git pre-push hooks can block Devin's commits. CLI version (`.cognition/` directory) supports AGENTS.md.

## Cross-Platform Comparison

### Hook Taxonomy

Across all platforms with hooks, five categories emerge:

| Category | Events | Platforms Supporting |
|----------|--------|---------------------|
| **Tool lifecycle** | PreToolUse, PostToolUse | Claude Code, Cursor, Windsurf, Cline, Augment |
| **Session lifecycle** | SessionStart, SessionEnd, Stop | Claude Code, Cursor, Cline (as TaskStart/Complete) |
| **Prompt interception** | UserPromptSubmit, beforeSubmitPrompt | Claude Code, Cursor, Cline, Windsurf |
| **Agent/subagent** | SubagentStart, SubagentStop | Claude Code, Cursor |
| **File-specific** | beforeReadFile, afterFileEdit | Cursor, Windsurf (pre_read_code, post_write_code) |

### Enforcement Model Spectrum

| Level | Mechanism | Platforms |
|-------|-----------|-----------|
| **Hard block** (tool execution prevented) | PreToolUse hook exit code 2 | Claude Code, Cursor, Windsurf, Cline, Augment |
| **Command gate** (shell commands gated) | Execpolicy forbidden/prompt | OpenAI Codex CLI |
| **Admin deny** (org-level block) | Admin rules, managed hooks | Claude Code, Cursor, Devin |
| **Context exclusion** (files hidden) | Content exclusion, context filters | Copilot, Sourcegraph Cody |
| **Advisory** (instructions followed best-effort) | Rules, instructions, AGENTS.md | All 15 platforms |

### Configuration Convergence

| Pattern | Platforms Using It |
|---------|--------------------|
| `hooks.json` (JSON, stdin/stdout, exit codes) | Claude Code, Cursor, Windsurf, Augment |
| AGENTS.md (cross-platform instructions) | Claude Code, Cursor, Windsurf, Cline, Copilot, Codex CLI, Devin, Replit |
| `.platform/rules/*.md` (platform-specific rules dir) | Cursor, Windsurf, Cline, Continue, Amazon Q, JetBrains, Augment |
| YAML frontmatter on rules (globs, triggers) | Claude Code, Cursor, Windsurf, Continue, Cline, Copilot, JetBrains |

### Portability Assessment

**What's portable today:**
- AGENTS.md — read by 8+ platforms, under Linux Foundation governance (Agentic AI Foundation, Dec 2025)
- Advisory rules in markdown — every platform reads them, naming/location differs
- MCP servers — supported by Claude Code, Cursor, Windsurf, Continue, Cline, Copilot

**What's NOT portable:**
- Hook event names — even the closest platforms (Claude Code/Cursor) have different event sets
- Hook handler types — only Claude Code has HTTP/prompt/agent handlers
- Blocking semantics — exit code 2 is common but input/output JSON schemas differ
- Configuration locations — every platform has its own settings path
- Matcher syntax — varies (regex vs glob vs fixed strings)

## Challenge

### Counter-evidence and limitations

1. **Cursor's Claude Code hook compatibility may overstate portability.** Cursor translates Claude Code hook names, but the translation is one-directional and Cursor-specific. A `.claude/settings.json` hook works in Cursor, but Cursor-only events (afterFileEdit, beforeShellExecution) have no Claude Code equivalent. This is vendor adoption of a competitor's format, not a cross-platform standard.

2. **Hook counts may inflate perceived capability.** Claude Code's 18 events and Cursor's 20 events suggest comprehensive coverage, but many events are niche (WorktreeCreate, TeammateIdle, PreCompact). The core enforcement surface is narrower: PreToolUse and UserPromptSubmit are the two events that matter most for standards enforcement.

3. **Advisory rules may be "good enough."** The 10 platforms without blocking hooks all function in production. Advisory instructions combined with external enforcement (CI/CD, linters, pre-commit hooks) may provide equivalent outcomes without the complexity of agent-level hooks. Aider's auto-lint approach demonstrates this: deep integration with existing tools rather than building a new enforcement layer.

4. **AGENTS.md convergence is recent and fragile.** The Linux Foundation governance (Dec 2025) is less than 4 months old. Platforms implement varying subsets of the format. There is no formal specification for which frontmatter fields are recognized or how directory scoping works.

5. **Performance impact is under-documented.** Only Claude Code explicitly documents hook performance (parallel execution, deduplication, configurable timeouts). Blocking hooks add latency to every tool call — the cumulative impact on developer experience across a long session is not well-studied.

6. **Security implications cut both ways.** Hooks execute arbitrary code with user permissions. Claude Code's GitHub issue #11226 documents that Edit/Write tools can modify hook scripts despite `permissions.deny` rules. Enterprise `allowManagedHooksOnly` mitigates this but reduces flexibility.

## Findings

### Q1: What hook types exist across platforms?

Five categories of hooks have emerged across the landscape (HIGH — converging evidence from 5 platforms with hooks):

1. **Tool lifecycle hooks** (PreToolUse/PostToolUse) — the most common and impactful. Present in all 5 hook-capable platforms. Pre-hooks can block; post-hooks are observational (except Cline, where PostToolUse can also cancel).

2. **Session lifecycle hooks** (SessionStart/SessionEnd/Stop) — present in Claude Code, Cursor, and Cline (as TaskStart/TaskComplete). Used for setup, cleanup, and auto-continue loops.

3. **Prompt interception hooks** (UserPromptSubmit) — present in Claude Code, Cursor, Windsurf, and Cline. Can validate or reject user input before the agent processes it.

4. **Agent/subagent hooks** (SubagentStart/SubagentStop) — only Claude Code and Cursor. Controls spawning and completion of nested agents.

5. **File-specific hooks** (beforeReadFile/afterFileEdit) — Cursor and Windsurf split tool hooks into granular file operations. Claude Code handles these via PreToolUse matchers on tool names.

### Q2: How do enforcement models compare?

Three tiers of enforcement exist (HIGH — all sources converge):

- **Tier 1 — Blocking hooks:** Claude Code, Cursor, Windsurf, Cline, Augment Code. PreToolUse exit code 2 prevents tool execution. This is the strongest enforcement — the action never happens.
- **Tier 2 — Command gating:** OpenAI Codex CLI (execpolicy), Devin (admin deny rules). Block specific shell commands or operations at the policy level, not at individual tool calls.
- **Tier 3 — Advisory only:** Copilot, Amazon Q, JetBrains AI, Continue, Tabnine, Replit, Sourcegraph Cody. Instructions influence behavior but cannot prevent actions.

### Q3: What's the de facto hook architecture pattern?

The Claude Code model has become the de facto pattern (HIGH — adopted by 4 other platforms):

- **Event-based dispatch:** Named events fire at lifecycle points
- **Matcher filtering:** Regex/glob patterns select which tool or event triggers the hook
- **JSON stdin/stdout protocol:** Hook receives context as JSON, returns decisions as JSON
- **Exit code semantics:** 0 = proceed, 2 = block, other = error-but-continue
- **Multi-level configuration:** User, project, enterprise scopes with merge semantics

Cursor, Windsurf, Cline, and Augment all follow this pattern with minor variations (different event names, input/output schemas, configuration locations).

### Q4: Is cross-platform hook portability feasible?

**Not today, but the gap is narrowing** (MODERATE — mixed evidence):

**What works:** AGENTS.md provides a portable advisory layer across 8+ platforms. MCP provides portable tool integration. Cursor explicitly reads Claude Code hook definitions.

**What doesn't:** Hook event names, JSON schemas, matcher syntax, and configuration locations differ across every platform. A hook written for Claude Code requires adaptation for Windsurf (different event names), Cline (different I/O schema), or Augment (fewer events). There is no standard hook specification.

**What might work:** A thin abstraction layer that maps platform-specific events to a common vocabulary (PreToolUse → pre_write_code → PreToolUse) and normalizes JSON schemas. This would be valuable but doesn't exist yet.

### Q5: What's the right boundary between hook-enforced and skill-driven checks?

Based on the landscape analysis (MODERATE — inference from patterns):

| Check Type | Best Mechanism | Rationale |
|-----------|---------------|-----------|
| **Format validation** (frontmatter, naming) | Hook (PreToolUse on Write/Edit) | Fast, deterministic, blocking prevents bad state |
| **Content quality** (word count, structure) | Skill (on-demand) | Requires judgment, not binary pass/fail |
| **Index sync** | Hook (PostToolUse on Write) | Deterministic, should be automatic |
| **URL verification** | Skill (on-demand) | Slow, network-dependent, shouldn't block every write |
| **Timestamp updates** | Hook (PreToolUse on Write/Edit) | Mechanical, should be automatic |
| **Full audit** | Skill (on-demand) | Comprehensive, interactive, too heavy for hooks |

The principle: **hooks for fast, deterministic, binary checks; skills for judgment-requiring, interactive, or slow checks.**

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Claude Code has 18 hook event types | statistic | [1][2] | verified |
| 2 | Claude Code has 4 handler types (command, HTTP, prompt, agent) | statistic | [1][2] | verified |
| 3 | Cursor has 20+ hook events | statistic | [4] | verified |
| 4 | Cursor reads Claude Code hook definitions from .claude/settings.json | attribution | [7] | verified |
| 5 | Windsurf has 12 hook events | statistic | [11] | verified |
| 6 | Cline has 8 hook types | statistic | [17] | verified |
| 7 | Augment Code has 3 hook events (PreToolUse, PostToolUse, Stop) | statistic | [22] | verified |
| 8 | AGENTS.md is governed by the Linux Foundation's Agentic AI Foundation (Dec 2025) | attribution | [LF press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) | verified |
| 9 | Only 5 of 15 platforms have true lifecycle hooks | statistic | analysis | verified |
| 10 | Exit code 2 blocks tool execution across Claude Code, Cursor, Windsurf, and Augment | convention | [1][4][11][22] | verified |
| 11 | GitHub Copilot code review always leaves "Comment" reviews, never blocking | attribution | [10] | verified |
| 12 | Amazon Q explicitly states rules are "advisory in nature" | quote | [24] | verified |

## Takeaways

1. **The hook-capable platforms share a common architecture.** Claude Code's PreToolUse/PostToolUse model with JSON stdin/stdout and exit code semantics has been adopted (with variations) by Cursor, Windsurf, Cline, and Augment Code. This is the closest thing to a standard.

2. **Advisory rules are universal; blocking enforcement is rare.** All 15 platforms read instruction files. Only 5 support blocking hooks. For WOS's cross-platform story (`.agents/` export), advisory rules via AGENTS.md are the portable layer; hooks are platform-specific extensions.

3. **For WOS specifically:** Hook-enforced checks (frontmatter validation, index sync, timestamp updates) would improve the Claude Code experience but are not portable. The skill-driven approach (wos:audit, wos:validate-work) remains the right choice for cross-platform enforcement. Hooks could complement skills as a Claude Code-specific optimization.

4. **Cursor's Claude Code hook compatibility is the strongest portability signal.** If WOS ships hooks in `.claude/settings.json`, they work in both Claude Code and Cursor today. This covers a significant portion of the target audience without maintaining platform-specific configurations.

5. **AGENTS.md is the only true cross-platform standard.** Supported by 8+ platforms and governed by the Linux Foundation. Hooks, rules directories, and configuration formats remain fragmented. Any WOS investment in cross-platform standards enforcement should build on AGENTS.md, not hooks.
