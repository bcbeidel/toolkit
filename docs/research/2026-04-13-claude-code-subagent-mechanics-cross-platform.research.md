---
name: "Claude Code Subagent Mechanics and Cross-Platform Comparison"
description: "Claude Code subagents use a 16-field Markdown+YAML format with fresh context isolation (no parent history, CLAUDE.md, or skills inherited); auto-delegation by description is documented but unreliable; Cursor is the closest cross-platform analog and explicitly reads .claude/agents/; GitHub Copilot uses the same Markdown-body structure but runs in ephemeral cloud environments; Codex CLI is TOML-only with explicit-only invocation."
type: research
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://code.claude.com/docs/en/how-claude-code-works
  - https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot
  - https://developers.openai.com/codex/subagents
  - https://cursor.com/docs/subagents
  - https://docs.windsurf.com/windsurf/cascade/agents-md
  - https://claude.com/blog/subagents-in-claude-code
  - https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5
  - https://www.morphllm.com/claude-subagents
  - https://github.com/anthropics/claude-code/issues/6825
  - https://github.com/anthropics/claude-code/issues/8501
  - https://github.com/anthropics/claude-code/issues/5456
  - https://github.com/anthropics/claude-code/issues/14714
  - https://github.com/anthropics/claude-code/issues/20264
  - https://github.com/anthropics/claude-code/issues/22665
  - https://github.com/anthropics/claude-code/issues/25000
  - https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/
  - https://www.ibuildwith.ai/blog/task-tool-vs-subagents-how-agents-work-in-claude-code/
related:
  - docs/research/2026-04-07-agent-frameworks.research.md
  - docs/research/2026-04-07-multi-agent-coordination.research.md
---

# Claude Code Subagent Mechanics and Cross-Platform Comparison


## Summary

Claude Code subagents are defined by Markdown files with YAML frontmatter stored in `.claude/agents/` (project) or `~/.claude/agents/` (user-global). Sixteen fields are supported; only `name` and `description` are required. The key design principles: (1) **complete context isolation** — spawned subagents receive only their own system prompt, the task prompt string from the Agent tool call, and environment basics; no parent conversation history, CLAUDE.md, or skills are inherited; (2) **tool registry inheritance by default**, but the session-runtime permission allowlist is not inherited by design (NOT_PLANNED); (3) **auto-delegation by description is documented but unreliable in practice** — explicit @-mention is the only reliable invocation path; (4) **subagents cannot spawn other subagents** — enforced at the tool level.

Key model resolution order: `CLAUDE_CODE_SUBAGENT_MODEL` env var > per-invocation parameter > frontmatter `model` field > parent model. Parent `bypassPermissions` mode propagates to subagents and cannot be overridden. Plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode` for security reasons.

Cross-platform: Cursor is the closest analog, using the same Markdown+YAML format and explicitly reading `.claude/agents/` for cross-compatibility. GitHub Copilot uses the same Markdown-body architecture but runs in ephemeral cloud environments (GitHub Actions), scoped to one repository per run, with task assignment through GitHub interfaces rather than terminal. Codex CLI uses TOML format and explicit-only invocation. Windsurf's AGENTS.md is a rules/instructions file, not an agent definition format — a fundamentally different primitive.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/sub-agents | Create custom subagents | Anthropic | 2026 | T1 primary | reachable |
| 2 | https://code.claude.com/docs/en/how-claude-code-works | How Claude Code works | Anthropic | 2026 | T1 primary | reachable |
| 3 | https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot | About assigning tasks to Copilot | GitHub | 2026 | T1 primary | reachable |
| 4 | https://developers.openai.com/codex/subagents | Subagents – Codex | OpenAI | 2026 | T1 primary | reachable |
| 5 | https://cursor.com/docs/subagents | Subagents – Cursor Docs | Cursor | 2026 | T1 primary | reachable |
| 6 | https://docs.windsurf.com/windsurf/cascade/agents-md | AGENTS.md – Windsurf Docs | Windsurf | 2026 | T1 primary | reachable |
| 7 | https://claude.com/blog/subagents-in-claude-code | How and when to use subagents in Claude Code | Anthropic blog | 2026 | T1 primary | reachable |
| 8 | https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5 | Tracing Claude Code's LLM Traffic: Agentic loop, sub-agents, tool use, prompts | George Sung / Medium | 2025 | T2 practitioner | reachable |
| 9 | https://www.morphllm.com/claude-subagents | Claude Code Subagents: How They Work, What They See & When to Use Them | MorphLLM | 2026 | T2 practitioner | reachable |
| 10 | https://github.com/anthropics/claude-code/issues/6825 | Allow configurable inheritance of system prompt and memory for subagents | anthropics/claude-code GitHub | 2025 | T2 issue report | reachable |
| 11 | https://github.com/anthropics/claude-code/issues/8501 | [BUG] Claude Code subagent YAML Frontmatter authoritative documentation | anthropics/claude-code GitHub | 2025-2026 | T2 issue report | reachable (closed, not planned) |
| 12 | https://github.com/anthropics/claude-code/issues/5456 | [BUG] Sub-agents Don't Inherit Model Configuration in Task Tool | anthropics/claude-code GitHub | 2025 | T2 issue report | reachable |
| 13 | https://github.com/anthropics/claude-code/issues/14714 | Subagents (Task tool) don't inherit parent conversation's allowed tools | anthropics/claude-code GitHub | 2025 | T2 issue report | reachable |
| 14 | https://github.com/anthropics/claude-code/issues/20264 | [FEATURE] Allow restrictive permission modes for subagents even when parent uses bypassPermissions | anthropics/claude-code GitHub | 2025-2026 | T2 issue report | reachable |
| 15 | https://github.com/anthropics/claude-code/issues/22665 | Subagent (Task tool) does not inherit permission allowlist from settings.json | anthropics/claude-code GitHub | 2026 | T2 issue report | reachable |
| 16 | https://github.com/anthropics/claude-code/issues/25000 | [BUG] Sub-agents bypass permission deny rules and per-command approval — security risk | anthropics/claude-code GitHub | 2026 | T2 issue report | reachable |
| 17 | https://www.ibuildwith.ai/blog/task-tool-vs-subagents-how-agents-work-in-claude-code/ | Task Tool vs. Subagents: How Agents Work in Claude Code | iBuildWith.ai | 2026 | T2 practitioner | reachable |
| 18 | https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/ | Claude Code Agents & Subagents: What They Actually Unlock | ksred.com | 2026 | T2 practitioner | reachable |
| 19 | https://docs.anthropic.com/en/docs/claude-code/sub-agents | Create custom subagents (docs.anthropic.com redirect) | Anthropic | 2026 | T1 primary | redirects to code.claude.com/docs/en/sub-agents |

## Extracts

### Sub-question 1: Complete .claude/agents/*.md file format

**Source: code.claude.com/docs/en/sub-agents (S1) — authoritative**

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown. Only `name` and `description` are required.

Complete supported frontmatter fields table (from official docs):

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Unique identifier using lowercase letters and hyphens |
| `description` | Yes | When Claude should delegate to this subagent |
| `tools` | No | Tools the subagent can use. Inherits all tools if omitted |
| `disallowedTools` | No | Tools to deny, removed from inherited or specified list |
| `model` | No | Model to use: `sonnet`, `opus`, `haiku`, a full model ID (e.g., `claude-opus-4-6`), or `inherit`. Defaults to `inherit` |
| `permissionMode` | No | Permission mode: `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, or `plan` |
| `maxTurns` | No | Maximum number of agentic turns before the subagent stops |
| `skills` | No | Skills to load into the subagent's context at startup. Full skill content is injected. Subagents don't inherit skills from parent. |
| `mcpServers` | No | MCP servers available to this subagent (name references or inline definitions) |
| `hooks` | No | Lifecycle hooks scoped to this subagent |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local` |
| `background` | No | Set to `true` to always run as a background task. Default: `false` |
| `effort` | No | Effort level: `low`, `medium`, `high`, `max` (Opus 4.6 only). Overrides session effort |
| `isolation` | No | Set to `worktree` to run in a temporary git worktree |
| `color` | No | Display color: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan` |
| `initialPrompt` | No | Auto-submitted as first user turn when agent runs as main session agent via `--agent` or `agent` setting |

> "Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown."

> "The frontmatter defines the subagent's metadata and configuration. The body becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt."

**Minimal valid example from docs:**
```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

**Note on `color` field (S11 — Issue #8501):** The `color` field was generated by `/agents` but missing from official docs. The issue was closed as "not planned," suggesting the table above (from the current live docs) is the resolution — `color` is now documented.

**Note on `--agents` CLI flag (S1):** Agents can also be passed as JSON via `--agents` flag. The JSON uses `prompt` instead of a markdown body, but otherwise accepts all the same frontmatter fields.

**Restriction on plugin subagents (S1):** "For security reasons, plugin subagents do not support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin."

---

### Sub-question 2: Agent discovery and loading

**Source: S1 (official docs)**

**Scope and priority hierarchy:**

| Location | Scope | Priority |
|---|---|---|
| Managed settings | Organization-wide | 1 (highest) |
| `--agents` CLI flag | Current session | 2 |
| `.claude/agents/` | Current project | 3 |
| `~/.claude/agents/` | All your projects | 4 |
| Plugin's `agents/` directory | Where plugin is enabled | 5 (lowest) |

> "When multiple subagents share the same name, the higher-priority location wins."

> "Subagents are loaded at session start. If you create a subagent by manually adding a file, restart your session or use `/agents` to load it immediately."

> "Project subagents are discovered by walking up from the current working directory. Directories added with `--add-dir` grant file access only and are not scanned for subagents."

> "To share subagents across projects, use `~/.claude/agents/` or a plugin."

**Note:** Built-in subagents (Explore, Plan, general-purpose, statusline-setup, Claude Code Guide) are bundled — not file-based. They appear in `/agents` alongside custom ones.

**CLI listing:** `claude agents` (without starting a session) lists all configured subagents grouped by source, indicating which are overridden by higher-priority definitions.

---

### Sub-question 3: Context flow from parent to subagent

**Source: S1, S8, S9 (official docs + practitioner traces)**

**What subagents receive in their context window (S9 — MorphLLM):**

> "A subagent's context window contains only four components:
> 1. System Prompt – From the markdown body of the agent file
> 2. Task Context – The prompt string from the Agent tool call
> 3. Environment – Working directory, platform, shell
> 4. Skills – Only those listed in the skills frontmatter field"

**What subagents do NOT receive (S9):**

> "Explicitly excluded from subagent context:
> - Parent's conversation history
> - Parent's prior tool calls and results
> - Parent's full Claude Code system prompt
> - Skills loaded in the parent session
> - MCP server tool descriptions (unless configured)
> - Other subagents' outputs"

**Communication channel (S9):**

> "The prompt string is the only channel. If a subagent needs file paths, error messages, architectural decisions, or output from a previous subagent, the parent must include it in the Agent tool prompt."

**From official docs (S1):**

> "Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt."

**From Anthropic blog (S7):**

> "Each subagent starts fresh, unburdened by the history of the conversation or invoked skills."

**Agent tool call parameters (S8 — practitioner trace):** When spawning a subagent, the parent uses the Agent tool with:
1. `description`: 3-5 word task summary
2. `prompt`: detailed instructions for the subagent
3. `subagent_type`: specifies the agent type (e.g., "Explore")

**Working directory (S1):**

> "A subagent starts in the main conversation's current working directory. Within a subagent, `cd` commands do not persist between Bash or PowerShell tool calls and do not affect the main conversation's working directory."

---

### Sub-question 4: CLAUDE.md and settings inheritance

**Source: S1, S2, S10**

**CLAUDE.md behavior (S2 — how-claude-code-works + S1 session-wide agent mode):**

> "CLAUDE.md files and project memory still load through the normal message flow." (When running a subagent as main session via `--agent`)

> "Each subagent starts fresh, unburdened by the history of the conversation or invoked skills." (Anthropic blog, S7)

The official docs state that a subagent's body "becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt."

**Implication:** CLAUDE.md appears to NOT be automatically loaded for subagents spawned via the Agent tool, since they receive only their own system prompt + environment. However, when running as main session via `--agent`, CLAUDE.md does load normally.

**Issue #6825 (S10) — enhancement request for configurable inheritance:**

> Current behavior: "Subagents currently inherit: The parent agent's system prompt, User memory (personal context), Project memory (project-level history). This inheritance is not configurable and applies to all subagents automatically."

Note: This was an older report. The current docs say subagents receive only their own system prompt + environment, suggesting behavior may have changed. The #6825 description may reflect an earlier implementation.

**Token overhead concern (S10):**

A "tiny" subagent that only runs `echo success` consumed ~60k tokens due to inherited context in one report, vs ~3k tokens in a clean environment. This was the motivation for the #6825 feature request for configurable inheritance.

**Skills inheritance (S1):**

> "Subagents don't inherit skills from the parent conversation; you must list them explicitly [in the `skills` frontmatter field]."

**Settings.json inheritance issues (S13, S15):**

Multiple open issues report that subagents don't properly inherit permission allowlists from settings.json:
- Issue #14714: "Subagents (Task tool) don't inherit parent conversation's allowed tools"
- Issue #22665: "Subagent (Task tool) does not inherit permission allowlist from settings.json"
These result in re-prompting for pre-approved tools.

---

### Sub-question 5: Tool permission model

**Source: S1 (official docs), S13, S14, S15, S16**

**Default tool inheritance (S1):**

> "By default, subagents inherit all tools from the main conversation, including MCP tools."

**Allowlist via `tools` field (S1):**

> "To restrict tools, use either the `tools` field (allowlist) or the `disallowedTools` field (denylist)."

Example — allowlist only Read, Grep, Glob, Bash:
```yaml
tools: Read, Grep, Glob, Bash
```

**Denylist via `disallowedTools` (S1):**
```yaml
disallowedTools: Write, Edit
```

**Both set (S1):**

> "If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed."

**Spawning restrictions — `Agent(agent_type)` syntax (S1):**

> "To restrict which subagent types it [an agent running as main thread] can spawn, use `Agent(agent_type)` syntax in the `tools` field."
> "This is an allowlist: only the listed subagents can be spawned."
> "Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions."

**Permission mode interaction with parent (S1):**

> "If the parent uses `bypassPermissions`, this takes precedence and cannot be overridden."
> "If the parent uses auto mode, the subagent inherits auto mode and any `permissionMode` in its frontmatter is ignored."

**Known issues with inheritance (S13, S14, S15, S16):**
- Issue #14714: Task-spawned subagents don't inherit allowed tools from parent session
- Issue #22665: Permission allowlist from settings.json not inherited
- Issue #20264: Request to allow restrictive modes even when parent uses `bypassPermissions`
- Issue #25000: "Sub-agents bypass permission deny rules and per-command approval — security risk"

**Built-in subagent restrictions (S1):**
- Explore: denied access to Write and Edit tools; uses Haiku model
- Plan: read-only tools; inherits model from main conversation
- General-purpose: all tools; inherits model from main conversation

---

### Sub-question 6: Autonomous vs explicit invocation

**Source: S1, S17, S18**

**Three invocation patterns (S1):**

> "Three patterns escalate from a one-off suggestion to a session-wide default:
> - Natural language: name the subagent in your prompt; Claude decides whether to delegate
> - @-mention: guarantees the subagent runs for one task
> - Session-wide: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting"

**Automatic delegation mechanics (S1):**

> "Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like 'use proactively' in your subagent's description field."

**@-mention behavior (S1):**

> "Your full message still goes to Claude, which writes the subagent's task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives."

**Reliability caveat (S17 — practitioner report):**

> "Auto-selection of custom agents remains unreliable. Claude frequently handles tasks in the main session rather than delegating to a defined agent, even when the agent is explicitly relevant and its description matches the task. The only reliable trigger is explicit invocation, which defeats the purpose of automatic routing for anyone who wants a seamless workflow."

**Task tool vs subagents relationship (S17):**

> "Task tool: The foundational parallel processing engine. Subagents: The management layer built on top of Task tools."

Note: In Claude Code v2.1.63, the Task tool was renamed to Agent tool. Existing `Task(...)` references still work as aliases.

**Background vs foreground (S1):**

> "Foreground subagents block the main conversation until complete. Permission prompts and clarifying questions are passed through to you."
> "Background subagents run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need."

---

### Sub-question 7: Output flow back to parent

**Source: S1, S8, S9**

**Return mechanism (S8 — practitioner trace):**

> "When a subagent completes (indicated by `stop_reason: end_turn`), its output returns as a `tool_result` in the parent's message history. The response includes the agent's final markdown report plus: `agentId: a09479d (for resuming to continue this agent's work if needed)`"

**Isolation of intermediate steps (S9):**

> "One string in, one string out. The subagent has no access to the parent's conversation, and the parent has no visibility into the subagent's intermediate steps."

> "Final subagent messages return as the Agent tool result. Intermediate reasoning and tool outputs remain isolated within the subagent's context window."

**Summarization (S7 — Anthropic blog):**

> "return only the relevant results to the main conversation rather than dumping raw data. The guidance emphasizes requesting specific output formats: 'Summaries, specific findings, or recommendations. Naming the output format helps Claude deliver it.'"

**Warning from docs (S1):**

> "When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context."

**Transcript persistence (S1):**

> "Each transcript is stored as `agent-{agentId}.jsonl` at `~/.claude/projects/{project}/{sessionId}/subagents/`. Subagent transcripts persist independently of the main conversation."

**Resumption (S1):**

> "Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh."

---

### Sub-question 8: model: field behavior

**Source: S1 (official docs)**

**Valid values (S1):**
- `sonnet` — model alias
- `opus` — model alias
- `haiku` — model alias
- Full model ID: e.g., `claude-opus-4-6`, `claude-sonnet-4-6`
- `inherit` — use the same model as the main conversation
- Omitted — defaults to `inherit`

**Resolution order (S1):**

> "When Claude invokes a subagent, it can also pass a `model` parameter for that specific invocation. Claude Code resolves the subagent's model in this order:
> 1. The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable, if set
> 2. The per-invocation `model` parameter
> 3. The subagent definition's `model` frontmatter
> 4. The main conversation's model"

**Environment variable override (S1):**

The `CLAUDE_CODE_SUBAGENT_MODEL` env var overrides all other model settings for subagents.

**Known bug (S12 — Issue #5456):**

> "[BUG] Sub-agents Don't Inherit Model Configuration in Task Tool" — when using the Task tool to spawn sub-agents, they may default to Claude Sonnet 4 instead of inheriting the configured model from both global and local settings.

**Effort field interaction (S1):**

The `effort` field is related to model behavior: it overrides the session effort level. `max` effort is only available for Opus 4.6.

**Built-in subagent model assignments (S1):**
- Explore: Haiku (fast, low-latency)
- Plan: inherits from main conversation
- General-purpose: inherits from main conversation
- statusline-setup: Sonnet
- Claude Code Guide: Haiku

---

### Sub-question 9: GitHub Copilot equivalent

**Source: S3 (official GitHub docs), search results**

**Core architecture (S3 — GitHub docs):**

> "GitHub Copilot can work independently in the background to complete tasks, just like a human developer."

> "The agent operates within 'its own ephemeral development environment, powered by GitHub Actions, where it can explore your code, make changes, execute automated tests and linters and more.'"

**Task assignment entry points (S3):**
- Agents panel on GitHub.com
- GitHub Issues
- Visual Studio Code
- Pull request comments (mentioning `@copilot`)
- Security campaign alerts

**Context isolation (S3):**

> "By default, Copilot can only access context in the repository specified when you start a task."

> "Copilot can only make changes in the repository specified when you start a task. Copilot cannot make changes across multiple repositories in one run."

**Extending context (S3):** Can be expanded through Model Context Protocol (MCP) server configuration.

**Model selection (S3):**

> "Users may select different AI models depending on how tasks are started, as 'different models perform better...depending on the type of tasks.'"

**Definition format (search results):**

GitHub Copilot cloud agent does not use file-based agent definitions in the way Claude Code does. Copilot's customization is primarily through:
- Repository-level instructions in `.github/copilot-instructions.md`
- Copilot "extensions" for tool integration
- Model selection per-task

Custom agent creation via `.agent.md` files (per search results): "Custom agents can be created via .agent.md files with specified tools, MCP servers, and instructions." However, official GitHub docs (S3) do not confirm this format — this detail comes from a comparison article and may reflect a planned or unreleased feature.

**Built-in Copilot specialist agents (search results):**
Copilot auto-delegates to:
- Explore (fast codebase analysis)
- Task (builds and tests)
- Code Review (high-signal change review)
- Plan (implementation planning)

**Key differences from Claude Code:**
- Copilot operates in ephemeral cloud environments (GitHub Actions); Claude Code runs in the developer's local environment
- Copilot is scoped to one repository per run; Claude Code can access multiple directories
- Copilot assigns tasks through GitHub interfaces; Claude Code is terminal-first
- No user-defined file-based agent format confirmed for Copilot (unlike `.claude/agents/*.md`)

---

### Sub-question 10: Other platform equivalents (Cursor, Codex CLI, Windsurf)

#### Cursor Subagents

**Source: S5 (cursor.com/docs/subagents)**

**File format (S5):**
```markdown
---
name: agent-name        # optional; defaults to filename
description: ...        # used for automatic delegation routing
model: inherit          # inherit | fast | specific model ID
readonly: false         # true restricts write permissions
is_background: false    # true runs without blocking parent
---
System prompt here...
```

**Storage locations (S5):**
- `.cursor/agents/` — project scope (also checks `.claude/agents/` and `.codex/agents/`)
- `~/.cursor/agents/` — user scope (also checks `~/.claude/agents/` and `~/.codex/agents/`)
- Project-level takes precedence over user-level

**Context isolation (S5):**

> "Subagents start with a clean context. The parent agent includes relevant information in the prompt since subagents don't have access to prior conversation history."

**Built-in subagents (S5):**
1. Explore — searches codebases; uses faster model for parallel analysis
2. Bash — executes shell commands; isolates verbose output
3. Browser — controls browsers via MCP; filters DOM snapshots

**Delegation mechanics (S5):**
- Automatic based on description + task complexity
- Explicit via `/name syntax` (e.g., `/verifier confirm auth flow`) or natural language mention
- Resumption via agent ID

**Key differences from Claude Code:**
- Fewer frontmatter fields (no `hooks`, `mcpServers`, `memory`, `effort`, `isolation`, `initialPrompt` equivalents)
- `readonly` boolean vs Claude Code's granular `tools`/`disallowedTools`
- `fast` model alias instead of `haiku`
- Cross-compatible with `.claude/agents/` and `.codex/agents/` directories

---

#### OpenAI Codex CLI

**Source: S4 (developers.openai.com/codex/subagents)**

**File format (S4) — TOML files, not Markdown:**
- `~/.codex/agents/` — personal agents
- `.codex/agents/` — project-scoped agents

Required fields:
- `name` — identifier for spawning
- `description` — human-facing selection guidance
- `developer_instructions` — core behavioral instructions (equivalent to markdown body in Claude Code)

Optional fields (inherit from parent when omitted):
- `model`
- `model_reasoning_effort`
- `sandbox_mode`
- `mcp_servers`
- `skills.config`
- `nickname_candidates` — presentation-only alternate names for distinguishing multiple instances

**Delegation mechanics (S4):**

> "Codex only spawns subagents when explicitly requested." (No automatic delegation based on description matching)

Built-in agents: `default`, `worker` (execution-focused), `explorer` (read-heavy).

**Orchestration (S4):**

> "Codex handles orchestration across agents, including spawning new subagents, routing follow-up instructions, waiting for results, and closing agent threads."

> "When many agents are running, Codex waits until all requested results are available, then returns a consolidated response."

**Nesting limits (S4):**

`max_depth` setting (default: 1) prevents deeper nesting recursion. `max_threads` (default: 6) caps concurrent open threads.

**Batch workflows (S4):**

`spawn_agents_on_csv` maps CSV rows to individual workers; each worker must call `report_agent_job_result` once.

**Key differences from Claude Code:**
- TOML format vs Markdown+YAML
- Explicit-only invocation (no automatic delegation)
- Depth/thread limits are global config settings, not per-agent
- No `permissionMode`, `hooks`, `memory`, `color`, `background`, `isolation` equivalents
- AGENTS.md (separate from agent definitions) provides repository navigation instructions

---

#### Windsurf / Cascade

**Source: S6 (docs.windsurf.com/windsurf/cascade/agents-md), search results**

**AGENTS.md format (S6):**

> "AGENTS.md files use plain markdown with no special frontmatter required."

This is fundamentally different from the other platforms — Windsurf's AGENTS.md is a plain instruction file, not an agent definition. It is part of the Rules engine, not a subagent spawning mechanism.

**Discovery (S6):**
- Root-level AGENTS.md: "Treated as an always-on rule — the full content is included in Cascade's system prompt on every message"
- Subdirectory AGENTS.md: "Treated as a glob rule with an auto-generated pattern of `<directory>/**`"
- Discovered throughout workspace and parent directories up to git root

**Subagent mechanism (search results):**

Windsurf has an experimental `#runSubagent` tool that allows running custom agents in isolated context from the main agentic session. Workflow agents are stored in `.windsurf/workflows/` as separate files. Windsurf's "Fast Context subagent" is a built-in specialist.

**Key differences from Claude Code:**
- AGENTS.md is a rules/instructions file, not an agent definition format
- No YAML frontmatter agent definition format confirmed for custom agents
- Subagent spawning is experimental and less documented
- Context isolation is present but implementation differs

---

## Platform Comparison Summary Table

| Feature | Claude Code | Cursor | Codex CLI | Windsurf |
|---|---|---|---|---|
| Agent definition format | Markdown + YAML frontmatter | Markdown + YAML frontmatter | TOML | No formal format (AGENTS.md = plain instructions) |
| Definition location | `.claude/agents/` | `.cursor/agents/` (also reads `.claude/agents/`) | `.codex/agents/` | `.windsurf/workflows/` |
| Required fields | `name`, `description` | none required | `name`, `description`, `developer_instructions` | N/A |
| Model field | `inherit`/alias/full ID/omit | `inherit`/`fast`/full ID | Optional, inherits parent | Not specified |
| Tool restriction | `tools` allowlist + `disallowedTools` denylist | `readonly` boolean | `sandbox_mode` | Not specified |
| Automatic delegation | Yes (description-based, unreliable) | Yes (description-based) | No (explicit only) | Experimental |
| Context isolation | Fresh context per subagent | Fresh context per subagent | Fresh context | Isolated context |
| CLAUDE.md / equivalent | Not inherited by subagents | N/A | AGENTS.md (separate) | AGENTS.md (rules engine) |
| Hooks in agent definition | Yes (`hooks` field) | No | No | No |
| Persistent memory | Yes (`memory` field) | No | No | No |
| Nesting depth | No nesting (subagents cannot spawn subagents) | Not specified | `max_depth` (default 1) | Not specified |

---

## Search Protocol

| # | Query / URL | Database | Date | Results |
|---|------------|----------|------|---------|
| 1 | WebFetch https://docs.anthropic.com/en/docs/claude-code/sub-agents | WebFetch | 2026-04-13 | Redirected to https://code.claude.com/docs/en/sub-agents |
| 2 | WebFetch https://code.claude.com/docs/en/sub-agents | WebFetch | 2026-04-13 | Full page content retrieved (51KB); complete frontmatter field table, examples, permission modes, model field, discovery, hooks, memory |
| 3 | WebFetch https://code.claude.com/docs/en/sub-agents.md | WebFetch | 2026-04-13 | Same content as #2 (same page, .md suffix variant) |
| 4 | WebFetch https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot | WebFetch | 2026-04-13 | Copilot agent overview — execution environment, task assignment, context isolation |
| 5 | WebSearch "Claude Code .claude/agents frontmatter fields model tools description 2026" | WebSearch | 2026-04-13 | 10 results — confirmed key fields, surfaced community articles and issue tracker |
| 6 | WebSearch "Claude Code subagent context isolation CLAUDE.md inheritance settings" | WebSearch | 2026-04-13 | 10 results — context isolation confirmed, issue #6825 surfaced, inheritance behavior described |
| 7 | WebSearch "Claude Code subagents tool permissions parent agent inherit restrict allowlist denylist" | WebSearch | 2026-04-13 | 10 results — tool permission model, known issues #14714, #20264, #22665, #25000 |
| 8 | WebSearch "Claude Code custom agents automatic invocation vs explicit Task tool spawn" | WebSearch | 2026-04-13 | 10 results — automatic vs explicit patterns, reliability caveat from practitioners |
| 9 | WebSearch "Claude Code subagent output return parent format summarization raw text result" | WebSearch | 2026-04-13 | 10 results — tool_result format, one-string-out pattern, Anthropic blog post |
| 10 | WebSearch "GitHub Copilot agent mode vs Claude Code subagents comparison definition format 2026" | WebSearch | 2026-04-13 | 10 results — comparison articles, Copilot .agent.md mention (unverified in official docs) |
| 11 | WebSearch "Cursor agent mode subagent definition file format custom agents configuration" | WebSearch | 2026-04-13 | 10 results — Cursor docs surfaced, frontmatter fields identified |
| 12 | WebSearch "Codex CLI agent delegation custom agents format OpenAI 2026" | WebSearch | 2026-04-13 | 10 results — Codex subagents page, TOML format, AGENTS.md |
| 13 | WebFetch https://code.claude.com/docs/en/how-claude-code-works | WebFetch | 2026-04-13 | Full page — agentic loop, CLAUDE.md loading, context window, subagent isolation summary |
| 14 | WebFetch https://github.com/anthropics/claude-code/issues/6825 | WebFetch | 2026-04-13 | Configurable inheritance request — token overhead details, proposed includes field, open enhancement |
| 15 | WebSearch "Windsurf agent mode subagent delegation custom agent definition format 2026" | WebSearch | 2026-04-13 | 10 results — AGENTS.md docs surfaced, experimental #runSubagent tool, .windsurf/workflows |
| 16 | WebFetch https://developers.openai.com/codex/subagents | WebFetch | 2026-04-13 | Codex subagent mechanics — TOML format, explicit-only invocation, orchestration, batch workflows |
| 17 | WebFetch https://cursor.com/docs/subagents | WebFetch | 2026-04-13 | Cursor subagent full reference — frontmatter table, context isolation, built-in agents, delegation |
| 18 | WebSearch "site:code.claude.com subagents model field OR inherit OR context flow OR CLAUDE.md" | WebSearch | 2026-04-13 | 10 results — confirmed model field, CLAUDE.md loading via normal message flow for --agent mode |
| 19 | WebFetch https://claude.com/blog/subagents-in-claude-code | WebFetch | 2026-04-13 | Anthropic blog — context isolation, CLAUDE.md consistency, permission modes per subagent |
| 20 | WebFetch https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5 | WebFetch | 2026-04-13 | Practitioner trace — Agent tool parameters, tool_result return format, agentId in output |
| 21 | WebFetch https://www.morphllm.com/claude-subagents | WebFetch | 2026-04-13 | Practitioner analysis — explicit 4-component context list, what subagents don't see, one-string-in-one-string-out model |
| 22 | WebFetch https://github.com/anthropics/claude-code/issues/8501 | WebFetch | 2026-04-13 | Bug report on undocumented color field — closed as not planned; color now appears in official docs |
| 23 | WebFetch https://docs.windsurf.com/windsurf/cascade/agents-md | WebFetch | 2026-04-13 | Windsurf AGENTS.md — plain markdown, no frontmatter, rules engine integration |

## Findings

### 1. The `.claude/agents/*.md` file format — 16 fields, 2 required

The subagent definition file is Markdown with YAML frontmatter. Only `name` and `description` are required; all other fields have defined defaults. The complete field set as of 2026 (HIGH — T1 official docs):

| Field | Default | Key semantic |
|---|---|---|
| `name` | required | Unique slug (lowercase, hyphen-separated) |
| `description` | required | Routing signal — when Claude should delegate to this agent |
| `tools` | inherit all | Allowlist of tools the subagent can use |
| `disallowedTools` | none | Denylist (applied before `tools` allowlist; a tool in both is removed) |
| `model` | `inherit` | `sonnet`/`opus`/`haiku`, full model ID, or `inherit` |
| `permissionMode` | `default` | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | unbounded | Stops the subagent after N agentic turns |
| `skills` | none | Skills to inject into subagent context at startup |
| `mcpServers` | inherit | MCP servers available to this subagent |
| `hooks` | none | Lifecycle hooks scoped to this subagent |
| `memory` | none | Persistent memory scope: `user`, `project`, or `local` |
| `background` | `false` | `true` runs concurrently; `false` blocks parent |
| `effort` | inherit | `low`/`medium`/`high`/`max` (Opus 4.6 only) |
| `isolation` | none | `worktree` runs in a temporary git worktree |
| `color` | system default | Display color for the agent panel |
| `initialPrompt` | none | Auto-submitted as first user turn in `--agent` session-wide mode only |

**Security restriction:** Plugin subagents (from `agents/` in a plugin) cannot use `hooks`, `mcpServers`, or `permissionMode` — these fields are silently ignored for security reasons. (HIGH — T1 docs)

**Challenge verdict:** Confirmed in full. The challenger verified the official docs field table; the `color` field was previously undocumented but is now official.

---

### 2. Discovery hierarchy — 5 priority tiers, session-start loading

Subagents are discovered at session start, not on-demand. The priority order (HIGH — T1 docs):

1. Managed settings (organization-wide)
2. `--agents` CLI flag (current session)
3. `.claude/agents/` (current project)
4. `~/.claude/agents/` (all your projects)
5. Plugin's `agents/` directory (where plugin is enabled)

When names conflict, higher-priority location wins. New files added during a session require a restart or `/agents` command to load. Project discovery walks upward from the CWD; `--add-dir` directories grant file access only and are not scanned for agents.

---

### 3. Context flow — "prompt string is the only channel"

Spawned subagents (via the Agent tool) receive exactly four components in their context window (HIGH — T1 docs + T2 practitioner traces converge):

1. **System prompt** — the Markdown body of the agent definition file
2. **Task context** — the prompt string from the Agent tool call
3. **Environment** — working directory, platform, shell
4. **Listed skills only** — skills in the `skills` frontmatter field; NOT skills active in the parent session

**Explicitly excluded** from subagent context (HIGH):
- Parent's conversation history and prior tool calls
- Parent's full Claude Code system prompt
- Skills loaded in the parent session (must be listed explicitly)
- Other subagents' outputs
- MCP server tool descriptions (unless configured in `mcpServers`)

"The prompt string is the only channel. If a subagent needs file paths, error messages, or architectural decisions, the parent must include it in the Agent tool prompt." (T2 MorphLLM, consistent with T1 docs)

**CLAUDE.md inheritance nuance** (QUALIFIED — challenger verdict): For Agent-tool-spawned subagents, CLAUDE.md is NOT inherited — current docs confirm isolation. In session-wide `--agent` mode, CLAUDE.md loads through normal message flow. The mechanism of CLAUDE.md injection (message-flow vs. system prompt) leaves room for ambiguity in edge cases; the spawned-subagent isolation path is better supported by current docs.

---

### 4. Tool permission model — registry vs. runtime allowlist distinction

Two separate concepts with different inheritance behaviors (HIGH — T1 docs + challenger resolution):

**Tool registry** (which tools are available): Subagents inherit all tools from the global tool registry by default. Restrict via `tools` allowlist or `disallowedTools` denylist. If both are set, `disallowedTools` is applied first.

**Permission allowlist** (session-runtime approvals): NOT inherited by subagents — by design, not a bug. The four GitHub issues (#14714, #22665, #20264, #25000) that appeared to report this as a bug are all now closed; root issue #5465 was closed as NOT_PLANNED, confirming intentional design. Pre-approved tool calls in the parent session require re-prompting in subagents.

**Parent mode takes precedence**: If the parent uses `bypassPermissions`, this overrides the subagent's `permissionMode` — the subagent cannot restrict its own permissions below the parent's level. If the parent uses auto mode, the subagent inherits auto mode and its `permissionMode` frontmatter is ignored.

**MCP tools**: Fixed in v2.1.101 — subagents now properly inherit MCP tools from dynamically-injected servers.

**Agent spawning restriction**: The `Agent(agent_type)` syntax in a `tools` field restricts which subagent types a main-session agent can spawn. This syntax has no effect inside subagent definitions — subagents cannot spawn other subagents. The restriction is enforced at the tool level. A `claude -p` Bash subprocess workaround exists but is unofficial and loses orchestration visibility. (HIGH — T1 docs confirmed, challenger CONFIRMED)

---

### 5. Invocation patterns — auto-delegation is documented but unreliable

Three invocation patterns (HIGH — T1 docs):

| Pattern | Mechanism | Reliability |
|---|---|---|
| Natural language (auto) | Claude matches task to agent description | LOW — frequently fails in practice |
| @-mention | Guarantees the agent runs for one task | HIGH |
| Session-wide (`--agent`) | Full session uses agent's system prompt + tools + model | HIGH |

**Auto-delegation reliability gap** (CONFIRMED — challenger verdict): The practitioner concern is well-supported and not contradicted by official sources. Official docs acknowledge the issue implicitly by recommending "use proactively" in descriptions as a workaround. Multiple practitioner reports confirm Claude frequently handles tasks in the main session rather than delegating even when the agent matches. Explicit @-mention is the only reliable routing mechanism. (MODERATE confidence — T1 docs aspirational, T2-T4 practitioners report failure)

**The `description` field is the routing signal** for auto-delegation. Writing descriptions like routing rules (specific trigger phrases, "use proactively" for proactive delegation) improves but does not guarantee auto-selection.

---

### 6. Output flow — one string out, transcripts persist

Subagent output returns as a `tool_result` in the parent's message history when the subagent's `stop_reason` is `end_turn`. (HIGH — T2 practitioner trace, consistent with T1 docs)

**What returns:** The subagent's final Markdown output as a single string. Intermediate reasoning, tool calls, and results remain isolated within the subagent's context window — the parent has no visibility into intermediate steps.

**Context consumption warning**: Multiple subagents each returning detailed results can rapidly consume the parent's context window. Official docs recommend requesting specific output formats ("summaries, specific findings, or recommendations") rather than raw data.

**Transcript persistence**: Each subagent's full transcript is stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`. Subagents can be resumed, retaining their full conversation history exactly where they stopped.

**Background vs foreground**: Foreground subagents block the main conversation until complete; permission prompts pass through to the user. Background subagents run concurrently; Claude Code prompts for all needed tool permissions before launching.

---

### 7. model: field — 4-level resolution order, env var wins

The `model` field accepts: `sonnet`, `opus`, `haiku` (aliases), full model IDs (e.g., `claude-opus-4-6`), or `inherit`. Omitting defaults to `inherit`. (HIGH — T1 docs)

Resolution order when the model is determined (highest priority first):
1. `CLAUDE_CODE_SUBAGENT_MODEL` environment variable
2. Per-invocation `model` parameter from the parent's Agent tool call
3. Subagent definition's `model` frontmatter
4. Main conversation's model

`effort` overrides the session effort level; `max` effort is Opus 4.6 only. Built-in subagents use fixed models: Explore → Haiku, statusline-setup → Sonnet, Claude Code Guide → Haiku, Plan/general-purpose → inherit.

---

### 8. GitHub Copilot custom agents — confirmed `.agent.md` format

GitHub Copilot has an officially documented custom agent format (HIGH — T1 GitHub docs, challenger CONFIRMED; initial draft was overly skeptical):

**File format**: Markdown with YAML frontmatter, stored in `.github/agents/AGENT-NAME.md` (repo-level) or `/agents/AGENT-NAME.md` in a `.github-private` repo (org/enterprise level).

**Confirmed frontmatter fields**: `name` (optional, deduced from filename), `description` (required — the only required field), `tools`, `model`, `target`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`. Agent instructions go in the **Markdown body** (up to 30,000 characters) — the same structure as Claude Code. There is no `prompt` frontmatter key.

**Key architectural differences from Claude Code**:
- Copilot runs in an **ephemeral cloud environment** (GitHub Actions), not the developer's local machine
- Scoped to **one repository per run** (no multi-directory access)
- Task assignment through GitHub interfaces (Issues, PRs, Agents panel) — not terminal-first
- No `permissionMode`, `hooks`, `memory`, `isolation`, `background`, `effort`, or `color` equivalents
- No configurable tool allowlist at the per-tool level (only broad `tools` categories)

---

### 9. Cross-platform comparison — Cursor closest, Codex TOML, Windsurf different primitive

**Cursor** is the closest structural analog to Claude Code subagents (HIGH — T1 Cursor docs, challenger CONFIRMED):
- Same Markdown + YAML format
- Explicitly reads `.claude/agents/` and `.codex/agents/` in addition to `.cursor/agents/` (intentional cross-compatibility)
- `readonly` boolean as a simplified alternative to Claude Code's `tools`/`disallowedTools`
- Fewer fields: no `hooks`, `mcpServers`, `memory`, `effort`, `isolation`, `initialPrompt` equivalents
- `fast` model alias instead of `haiku`

**Codex CLI** (TOML format, explicit-only invocation):
- TOML files in `.codex/agents/` — fundamentally different from Markdown
- No automatic delegation — explicit invocation only; described as a deliberate design choice
- Global depth (`max_depth`, default 1) and thread (`max_threads`, default 6) limits as config settings
- `sandbox_mode` as the tool restriction mechanism (vs. per-tool lists)
- Batch workflow support via `spawn_agents_on_csv`

**Windsurf**: AGENTS.md is a **rules/instructions file**, not a subagent definition format. It is part of the Rules engine and is included in Cascade's system prompt — fundamentally a different primitive. Custom agent spawning via `#runSubagent` is experimental and less documented.

---

## Challenge

### Claim 1: CLAUDE.md / system prompt inheritance

**Claim:** The draft states that CLAUDE.md appears NOT to be automatically loaded for subagents spawned via the Agent tool, and cites Issue #6825 (S10) as an older report that may reflect a prior implementation — implying the current behavior is isolation (only own system prompt + environment).

**Evidence for (isolation is current behavior):**
- S1 (official docs, re-fetched 2026-04-13): "Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt." This language is unambiguous and present in the current live docs.
- S7 (Anthropic blog): "Each subagent starts fresh, unburdened by the history of the conversation or invoked skills."
- S9 (MorphLLM, 2026): Explicitly lists four components only; parent system prompt and memory are in the "explicitly excluded" list.

**Counter-evidence (inheritance may still occur at some layer):**
- Issue #6825 body (filed 2025-08-29, closed 2025-08-29 as duplicate of #4908): States explicitly that "Subagents currently inherit: The parent agent's system prompt, User memory (personal context), Project memory (project-level history)." Token data supports this: a trivial subagent consumed ~60k tokens with memory loaded vs ~3k tokens without. This was a user-observed empirical measurement, not an inference.
- The issue was closed as a duplicate, not as "not planned" or "by design," which leaves ambiguous whether the behavior was changed or the duplicate issue tracked the resolution.
- A first-party search result (for "Claude Code subagents CLAUDE.md inherit system prompt 2026") returned: "CLAUDE.md files and project memory still load through the normal message flow" — echoing language from the session-wide `--agent` mode docs, but potentially misapplying it to spawned subagents.

**Assessment:** The contradiction is real but likely reflects a version boundary. Issue #6825 was filed in August 2025 and the token evidence is persuasive. The current official docs (2026) consistently describe isolation. Most likely: the behavior was isolation-by-design from the beginning for the Agent-tool-spawned path, but CLAUDE.md was injected via a different mechanism (the "normal message flow" described in the `--agent` session-wide docs). The #6825 reporter may have measured a different code path (session-wide `--agent` mode, where docs confirm CLAUDE.md loads). The "not fully resolved" risk: if CLAUDE.md is injected via the user-turn message flow rather than the system prompt, it could still be present in subagent context even though "the Claude Code system prompt" is not inherited.

**Verdict:** QUALIFIED — isolation is the documented current behavior, but the mechanism of CLAUDE.md injection (message-flow vs system prompt) leaves room for ambiguity. The draft correctly flags #6825 as potentially outdated but should note that CLAUDE.md may still reach subagents via message-flow injection even under the current model.

**Confidence adjustment:** Slight downward on certainty of complete isolation. CLAUDE.md may still be present via message-flow injection for `--agent` session mode; the spawned-subagent path is better supported as truly isolated.

---

### Claim 2: GitHub Copilot `.agent.md` format

**Claim:** The draft notes "Custom agents can be created via .agent.md files" but flags this as coming from a comparison article rather than official GitHub docs, and therefore unverified.

**Evidence for (format is real and official):**
- GitHub's official custom agents reference page (`docs.github.com/en/copilot/reference/custom-agents-configuration`, fetched 2026-04-13) explicitly states: "The configuration file's name (minus `.md` or `.agent.md`) is used for deduplication between levels so that the lowest level configuration takes precedence." This confirms `.agent.md` is an officially supported extension.
- GitHub's `about-custom-agents` page confirms the format: Markdown files with YAML frontmatter, stored in `.github/agents/AGENT-NAME.md` (repo level) or `/agents/AGENT-NAME.md` in a `.github-private` repo (org/enterprise level).
- Supported frontmatter fields confirmed in official docs: `name` (optional), `description` (required), `prompt` (required), `tools` (optional), `model` (optional), `target`, `disable-model-invocation`, `user-invocable`, `mcp-servers`, `metadata`.

**Counter-evidence:** None. The draft's skepticism was appropriate given the original search only surfaced comparison articles, but the official docs do confirm the format.

**Verdict:** CONTRADICTED (the draft's skepticism is wrong) — `.agent.md` is a real, officially documented format for GitHub Copilot custom agents. The draft should upgrade this from "unverified" to "confirmed."

**Confidence adjustment:** High confidence upgrade. Replace the "unverified" hedge with the official docs citation.

---

### Claim 3: Tool inheritance gap

**Claim:** Official docs say subagents "inherit all tools if `tools` omitted," but four open GitHub issues (#14714, #20264, #22665, #25000) report tools are NOT inherited.

**Evidence for (gap exists or existed):**
- Issues #14714 and #22665 describe concrete failures: spawned subagents did not inherit allowed tools from parent session, causing re-prompting for pre-approved tools.
- Issue #25000 described a security risk where deny rules were bypassed.
- Issue #20264 requested ability to restrict permission modes.

**Counter-evidence (gap narrowed or closed):**
- Issue #14714: CLOSED as DUPLICATE (2025-12-23) of #5465. #5465 itself was CLOSED as NOT_PLANNED (2026-01-04) — suggesting the "inherit from session allowlist" behavior was not going to be implemented as requested; the design intent may be that subagents inherit the global tool list, not the session-runtime allowlist.
- Issue #22665: CLOSED as DUPLICATE (2026-02-06).
- Issue #25000: CLOSED as DUPLICATE (2026-02-15).
- Issue #20264: CLOSED as NOT_PLANNED (2026-02-28).
- Claude Code changelog v2.1.101: "Fixed subagents not inheriting MCP tools from dynamically-injected servers" — a specific MCP tool inheritance fix was shipped.
- The official docs distinction matters: "inherits all tools from the main conversation" likely refers to the global tool registry, not the runtime-approved tool allowlist in `settings.json`. These are separate concepts.

**Assessment:** The four issues are all closed, most as duplicates. The underlying root issue (#5465) was closed NOT_PLANNED, indicating the behavior (subagents not inheriting the session-runtime permission allowlist) was not considered a bug to fix — it was a design choice. The "tools if omitted" language in official docs refers to the tool registry (which tools are available), not the permission approval state. The MCP tool inheritance fix in v2.1.101 addresses a separate gap (dynamically added MCP servers). The framing in the draft — "4 open GitHub issues report tools are NOT inherited" — is now outdated; all four are closed.

**Verdict:** QUALIFIED — the tool registry inheritance works as documented. The gap was in permission-allowlist inheritance (session approvals not carrying over), which was intentional by design, not a bug. The draft should update "4 open issues" to "4 issues, all now closed" and clarify the distinction between tool registry inheritance vs runtime permission allowlist inheritance.

**Confidence adjustment:** Moderate upward confidence in the official docs claim, with a clarification that permission allowlist inheritance is by design not inherited (not a bug).

---

### Claim 4: Auto-delegation reliability

**Claim:** Official docs say "Claude automatically delegates based on description." Practitioner (S17) says "auto-selection remains unreliable."

**Evidence for (reliability is limited):**
- S17 (iBuildWith.ai): "Auto-selection of custom agents remains unreliable. Claude frequently handles tasks in the main session rather than delegating to a defined agent, even when the agent is explicitly relevant."
- Multiple additional practitioner sources found in search: "You will need to benchmark how reliable the task routing is within your setup, especially if you flood Claude with too many custom agent options."
- Community guidance consistently frames explicit invocation (@ mention) as the reliable path.

**Evidence for (reliability improving):**
- Official docs acknowledge the issue and provide actionable guidance: write descriptions "like a routing rule" with specific trigger phrases; include "use proactively" for agents that should be invoked without being asked.
- One practitioner source (claudefa.st): "Claude delegates to custom subagents automatically whenever a task matches its description, no prompting required" — a more optimistic framing.

**Counter-evidence (against the unreliability claim):** No published sources in 2026 report that auto-delegation has been made reliable. The official docs' own guidance to include "use proactively" implicitly acknowledges that automatic delegation is not guaranteed.

**Verdict:** CONFIRMED — the practitioner reliability concern is well-supported and not contradicted by official sources. The official docs are aspirational ("Claude automatically delegates") while practitioners report it frequently fails. The draft accurately captures this tension.

**Confidence adjustment:** No change needed. The claim as stated (auto-delegation is documented but unreliable in practice) is accurate.

---

### Claim 5: Cursor cross-compatibility with `.claude/agents/`

**Claim:** S5 claims Cursor reads `.claude/agents/` and `.codex/agents/` in addition to `.cursor/agents/`.

**Evidence for (cross-compatibility is real):**
- Cursor docs (cursor.com/docs/subagents, fetched 2026-04-13) explicitly list three directories for project-level subagents: `.cursor/agents/`, `.claude/agents/`, `.codex/agents/`. The docs state this is for "Claude compatibility" and "Codex compatibility" respectively.
- User-level equivalents also cross-compatible: `~/.cursor/agents/`, `~/.claude/agents/`, `~/.codex/agents/`.
- Priority: `.cursor/` takes precedence when naming conflicts arise.

**Counter-evidence:** None found. The Cursor docs are unambiguous.

**Verdict:** CONFIRMED — Cursor explicitly reads all three directory formats. The cross-compatibility is intentional and officially documented by Cursor, not just inferred from a comparison article.

**Confidence adjustment:** High confidence upgrade. The draft's phrasing "also checks .claude/agents/ and .codex/agents/" is correct and supported by the primary Cursor docs.

---

### Claim 6: Subagents cannot spawn subagents

**Claim:** Docs state "Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions."

**Evidence for (restriction is real):**
- S1 (official docs): Explicitly states "Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions."
- Search results confirm: "Claude Code's native Task tool blocks subagents from spawning other subagents by filtering the Agent tool out."
- Issue #4182 (Sub-Agent Task Tool Not Exposed When Launching Nested Agents) confirms the restriction exists.
- Issue #32731 documents that Teammates also have reduced tool access and cannot spawn, with the note that "restriction is broader than documented."

**Counter-evidence / qualifications:**
- Community workaround exists: subagents can call `claude -p` via the Bash tool to spawn headless Claude instances. This bypasses the restriction at the tool level using a shell subprocess. However, this loses visibility, complicates error handling, and produces separate processes outside Claude Code's orchestration.
- A community project (`gruckion/nested-subagent`) exists specifically to enable nested subagents via this workaround, confirming the workaround is used in practice.
- Issue #32731 flags that the documented restriction ("subagents cannot spawn subagents") understates the actual scope — Teammates (a related concept) are also restricted from spawning anything, and this broader restriction is not clearly documented.

**Verdict:** CONFIRMED — the nesting restriction is real and enforced at the tool level. The workaround via `claude -p` in Bash exists but is unofficial. The draft's claim is accurate. A minor qualification: the restriction scope may be broader than documented (affecting Teammates too), and the Bash subprocess workaround makes the restriction bypassable for determined users.

**Confidence adjustment:** No change for the core claim. Add a note that the `claude -p` bash workaround exists and that Issue #32731 suggests the restriction is broader than documented.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Only `name` and `description` are required" | attribution | [S1] | verified — confirmed verbatim in live S1 docs: "Only `name` and `description` are required." |
| 2 | "15 fields total in the frontmatter" (section header: "15 fields, 2 required") | statistic | [S1] | corrected — live S1 docs table has **16 fields**: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation, color, initialPrompt. The Extracts and Findings tables both omit `initialPrompt`. Count should be 16. |
| 3 | "Plugin subagents cannot use `hooks`, `mcpServers`, or `permissionMode`" | specific | [S1] | verified — confirmed verbatim in live S1 docs: "For security reasons, plugin subagents do not support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin." |
| 4 | "Subagents cannot spawn other subagents" | specific | [S1] | verified — confirmed verbatim in live S1 docs: "Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions." Also confirmed in built-in agent descriptions and in a Note element. |
| 5 | "Root issue #5465 was closed as NOT_PLANNED" | specific | GitHub issue tracker | verified — #5465 state confirmed as CLOSED / NOT_PLANNED via gh CLI. Note: the issue title is "[BUG] Task subagents fail to inherit permissions in MCP server mode (affects both WSL and native Windows)" — narrower scope than the document implies (which frames it as the root of the general permission-allowlist inheritance gap). The NOT_PLANNED resolution status is correct. |
| 6 | "MCP tool inheritance fix shipped in v2.1.101" | specific | GitHub releases | verified — v2.1.101 release notes confirmed via gh API: "Fixed subagents not inheriting MCP tools from dynamically-injected servers." |
| 7 | "Cursor explicitly reads `.claude/agents/`" | specific | [S5] | verified — confirmed in live Cursor docs: "`.claude/agents/` — Current project only (Claude compatibility)" listed explicitly in the file locations table alongside `.cursor/agents/` and `.codex/agents/`. |
| 8 | "GitHub Copilot `prompt` field is required" | specific | [S3 + reference docs] | corrected — `prompt` is **not a frontmatter field** in GitHub Copilot custom agents. Per `docs.github.com/en/copilot/reference/custom-agents-configuration`, agent instructions go in the **Markdown body** (up to 30,000 chars), exactly like Claude Code. The only required frontmatter field is `description`. The document's Findings section incorrectly lists `prompt` as "required — inline system prompt; no separate markdown body like Claude Code" — this is the opposite of the truth: Copilot uses a markdown body, not a `prompt` frontmatter key. |
| 9 | "`CLAUDE_CODE_SUBAGENT_MODEL` env var overrides all other model settings" | specific | [S1] | verified — confirmed verbatim in live S1 docs, listed as priority 1 in the model resolution order: "The `CLAUDE_CODE_SUBAGENT_MODEL` environment variable, if set." |
| 10 | "Transcripts stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`" | specific | [S1] | verified — confirmed in live S1 docs: "find IDs in the transcript files at `~/.claude/projects/{project}/{sessionId}/subagents/`. Each transcript is stored as `agent-{agentId}.jsonl`." Note: the Medium article (S8) is cited as the source in the Extracts section but does **not** confirm this path — it only mentions agentId in output. The actual source is S1. |

### URL Verification

| # | URL | Status | Notes |
|---|-----|--------|-------|
| 1 | https://code.claude.com/docs/en/sub-agents | reachable | Full 51KB page retrieved; authoritative source confirmed |
| 2 | https://code.claude.com/docs/en/how-claude-code-works | reachable | Referenced in search protocol entry #13 |
| 3 | https://docs.github.com/en/copilot/using-github-copilot/coding-agent/about-assigning-tasks-to-copilot | reachable | Page title is "About GitHub Copilot cloud agent"; does not detail custom agent file format |
| 4 | https://developers.openai.com/codex/subagents | reachable | Page accessible; TOML format and required fields confirmed |
| 5 | https://cursor.com/docs/subagents | reachable | Cross-directory compatibility with `.claude/agents/` confirmed |
| 6 | https://docs.windsurf.com/windsurf/cascade/agents-md | reachable | Plain markdown rules file, no frontmatter; confirmed as rules engine, not agent definitions |
| 7 | https://claude.com/blog/subagents-in-claude-code | reachable | "How and when to use subagents in Claude Code" by Anthropic; context isolation and CLAUDE.md confirmed |
| 8 | https://medium.com/@georgesung/tracing-claude-codes-llm-traffic-agentic-loop-sub-agents-tool-use-prompts-7796941806f5 | reachable | Page accessible; does NOT confirm the transcript storage path (claims in document attribute this to S8 incorrectly — source is S1) |
| 9 | https://www.morphllm.com/claude-subagents | reachable | "Claude Code Subagents: How They Work, What They See, and When to Use Them (2026)" |
| 10 | https://github.com/anthropics/claude-code/issues/6825 | reachable | CLOSED / COMPLETED (not DUPLICATE or NOT_PLANNED as might be inferred from context) |
| 11 | https://github.com/anthropics/claude-code/issues/8501 | reachable | CLOSED / NOT_PLANNED — confirmed |
| 12 | https://github.com/anthropics/claude-code/issues/5456 | reachable | CLOSED / DUPLICATE (not the root issue; root is #5465 which is CLOSED / NOT_PLANNED) |
| 13 | https://github.com/anthropics/claude-code/issues/14714 | reachable | CLOSED / DUPLICATE |
| 14 | https://github.com/anthropics/claude-code/issues/20264 | reachable | CLOSED / NOT_PLANNED |
| 15 | https://github.com/anthropics/claude-code/issues/22665 | reachable | CLOSED / DUPLICATE |
| 16 | https://github.com/anthropics/claude-code/issues/25000 | reachable | CLOSED / DUPLICATE |
| 17 | https://www.ibuildwith.ai/blog/task-tool-vs-subagents-how-agents-work-in-claude-code/ | reachable | "Task Tool vs. Subagents: How Agents Work in Claude Code"; published September 4, 2025 |
| 18 | https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/ | reachable | "Claude Code Agents & Subagents: What They Actually Unlock" |
| 19 | https://docs.anthropic.com/en/docs/claude-code/sub-agents | redirect | 301 redirect to https://code.claude.com/docs/en/sub-agents — confirmed reachable via redirect |
