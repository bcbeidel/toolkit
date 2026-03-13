---
name: "Agent Directory Conventions Across AI Tools and Frameworks"
description: "How AI coding tools and agent frameworks define reusable autonomous subagents through directory conventions, file formats, and dispatch patterns — covering Claude Code, Copilot, Gemini CLI, CrewAI, Semantic Kernel, AG2, and emerging standards (A2A, AgentSpec)"
type: research
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents
  - https://docs.github.com/en/copilot/reference/custom-agents-configuration
  - https://geminicli.com/docs/core/subagents/
  - https://docs.crewai.com/en/concepts/agents
  - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-templates
  - https://github.com/oracle/agent-spec
  - https://agent2agent.info/docs/concepts/agentcard/
  - https://docs.cline.bot/features/subagents
  - https://blogs.oracle.com/ai-and-datascience/introducing-open-agent-specification
related:
  - docs/context/agent-framework-portability.md
  - docs/context/skill-command-system-landscape.md
  - docs/context/plugin-extension-architecture.md
  - docs/context/multi-agent-coordination.md
---

## Summary

A convergent pattern has emerged across AI coding tools: **agents are markdown files with YAML frontmatter, stored in a conventional directory, discovered automatically, and dispatched via description-based routing**. Claude Code, GitHub Copilot, and Gemini CLI independently arrived at nearly identical conventions — `.claude/agents/`, `.github/agents/`, `.gemini/agents/` respectively — each using markdown body as system prompt and YAML frontmatter for metadata (name, description, tools, model). Agent frameworks (CrewAI, Semantic Kernel, AG2) take a code-first approach but are converging toward declarative definitions through YAML configs and Oracle's AgentSpec. The Agent2Agent protocol introduces a network-level agent discovery mechanism via JSON Agent Cards at `.well-known/agent-card.json`.

The key architectural distinction across all systems is: **skills/tools are capabilities an agent uses; agents are autonomous actors with their own identity, context, and instruction set that can be dispatched to perform work independently**.

<!-- search-protocol [{"query":"Claude Code agents directory AGENT.md subagent definition convention 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":3},{"query":"OpenAI Codex agents directory agent definition file convention 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"Cursor AI agent definition rules convention directory 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":1},{"query":"GitHub Copilot custom agent definition extension convention 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":3},{"query":"Gemini CLI agent definition convention directory AGENT.md 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"CrewAI agent definition YAML file convention agents directory 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"AutoGen AG2 agent definition configuration file convention 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":1},{"query":"LangGraph agent definition configuration reusable agent pattern 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":1},{"query":"Semantic Kernel agent definition configuration reusable agents pattern 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"agent card agent protocol standard specification declarative agent definition 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":3},{"query":"AgentSpec Oracle declarative agent definition specification portable YAML JSON 2025","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"Claude Code plugin agents directory convention plugin subagents 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":2},{"query":"Aider Cline agent definition convention reusable subagent 2025 2026","source":"google","date_range":"2025-2026","results_found":10,"results_used":1}] -->

## Findings

### 1. AI Coding Tools: Convergent Directory-Based Agent Definitions

Three major AI coding tools have independently converged on nearly identical conventions for defining reusable subagents (HIGH — three independent T1 sources converge):

| Tool | Directory | File Format | Discovery | Dispatch |
|------|-----------|-------------|-----------|----------|
| **Claude Code** | `.claude/agents/`, `~/.claude/agents/`, plugin `agents/` | Markdown + YAML frontmatter | Auto-loaded at session start | Description-based routing by main agent |
| **GitHub Copilot** | `.github/agents/` | Markdown + YAML frontmatter (`.agent.md`) | Available after commit to default branch | User selects from dropdown; `disable-model-invocation` controls auto-routing |
| **Gemini CLI** | `.gemini/agents/`, `~/.gemini/agents/` | Markdown + YAML frontmatter | Exposed as tools matching agent `name` | Main agent calls agent-as-tool |

All three share these structural properties:
- **YAML frontmatter** for metadata: `name`, `description`, `tools` (allowlist), `model` (override or inherit)
- **Markdown body** as the agent's system prompt / instructions
- **Directory-scoped**: project-level (team-shared), user-level (personal), and plugin/extension-level
- **Priority ordering**: closer scope overrides broader scope

#### Claude Code: Most Mature Agent Convention

Claude Code's subagent system is the most feature-complete (T1: official docs). Key properties:

- **Frontmatter fields**: `name`, `description` (required); `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `isolation` (all optional)
- **Three scopes**: project (`.claude/agents/`), user (`~/.claude/agents/`), plugin (`agents/` at plugin root)
- **Plugin distribution**: plugins bundle agents alongside skills, commands, and hooks — agents at plugin root `agents/` directory
- **Skill injection**: `skills` frontmatter field loads skill content into agent context at startup — agent controls the system prompt, skill provides domain knowledge
- **Persistent memory**: `memory` field gives agents a cross-session knowledge directory (`user`, `project`, or `local` scope)
- **Tool restriction**: `tools` (allowlist) and `disallowedTools` (denylist); `Agent(worker, researcher)` syntax restricts which subagents an agent can spawn
- **Foreground/background**: agents run blocking or concurrent; `background: true` in frontmatter forces background
- **Worktree isolation**: `isolation: worktree` gives agent its own git worktree copy
- **Hooks**: `PreToolUse`, `PostToolUse`, `Stop` hooks scoped to agent lifecycle
- **No nesting**: subagents cannot spawn other subagents

**Critical design decision**: agents receive only their own system prompt plus basic environment details — NOT the full Claude Code system prompt. This makes them self-contained by construction.

#### GitHub Copilot: Agent Profiles

Copilot's custom agents (T1: official docs) are stored at `.github/agents/[name].agent.md`. Key differences from Claude Code:

- **File naming**: `.agent.md` suffix convention (not arbitrary `.md`)
- **Dispatch**: users select agents from a dropdown menu; `disable-model-invocation: true` prevents automatic selection
- **`user-invocable`**: boolean controlling whether users can directly select the agent
- **`target`**: restricts agent to `vscode` or `github-copilot` environment
- **`metadata`**: arbitrary annotation object (GitHub.com only)
- **30,000 character prompt limit** explicitly documented
- **Organization/enterprise scope**: `.github-private` repo's `agents/` folder for org-wide agents
- **No persistent memory, hooks, or isolation** — simpler model than Claude Code

#### Gemini CLI: Agents as Tools

Gemini CLI (T1: official docs, experimental) defines agents similarly but with a distinctive dispatch model:

- **Agents are exposed as tools**: "Subagents are exposed to the main agent as a tool of the same name"
- **Additional frontmatter**: `kind` (local/remote), `temperature`, `max_turns`, `timeout_mins`
- **Explicit opt-in**: requires `"experimental": {"enableAgents": true}` in settings
- **Built-in agents**: `codebase_investigator`, `cli_help`, `generalist_agent`, `browser_agent`
- **Remote agents**: supports A2A protocol for network-based agent dispatch
- **YOLO mode warning**: agents may execute tools without user confirmation

### 2. Cursor, Codex, Aider, Cline: No Dedicated Agent Convention

Not all tools have an agent directory convention (MODERATE — absence documented across multiple sources):

- **Cursor**: uses `.cursor/rules/` for rules and AGENTS.md for conventions, but has no `agents/` directory or subagent dispatch. Rules are contextual instructions, not autonomous actors.
- **OpenAI Codex**: reads AGENTS.md for instructions and has a `skills/` directory, but no documented `agents/` convention for reusable subagent definitions.
- **Aider**: no subagent concept. CONVENTIONS.md for instructions. Philosophy emphasizes simplicity — "thinks in git."
- **Cline**: has subagents (experimental) but they are read-only research agents spawned programmatically, not defined in directory files. Subagents "cannot write files, apply patches, use the browser, access MCP servers, or perform web searches" (T1: official docs).

### 3. Agent Frameworks: Code-First with Declarative Convergence

Agent frameworks approach agent definition differently from coding tools — starting code-first but converging toward declarative formats (HIGH — multiple T1 sources):

#### CrewAI: YAML Config Convention

CrewAI has the strongest file-based convention among frameworks (T1: official docs):
- **Location**: `src/[project]/config/agents.yaml` and `tasks.yaml`
- **Fields per agent**: `role`, `goal`, `backstory` (all string, support `>` folding)
- **Variable interpolation**: `{topic}` placeholders replaced at runtime via `crew.kickoff(inputs={})`
- **Code binding**: YAML keys must match Python method names decorated with `@agent`
- **Tools assigned in code**: `tools=[SerperDevTool()]` in Python, not in YAML
- **29+ parameters**: including `max_iter`, `max_execution_time`, `allow_code_execution`, `respect_context_window`

CrewAI's model: YAML defines *identity* (role, goal, backstory); Python defines *capabilities* (tools, model, execution controls).

#### Semantic Kernel: Template-Based Agents

Microsoft's Semantic Kernel uses YAML prompt templates for reusable agent definitions (T1: official docs):
- **Format**: standard Prompt Template Config YAML (`name`, `template`, `template_format`, `description`, `input_variables`)
- **Reuse pattern**: "a single assistant definition can be created and reused multiple times, each time with different parameter values"
- **Variable override**: `KernelArguments` can override template parameters at invocation
- **No directory convention**: templates are loaded from arbitrary file paths, not auto-discovered

Semantic Kernel's model: agents are *parameterized prompt templates* — the same definition serves different contexts through variable substitution.

#### AG2 (AutoGen): Code-First with AgentSpec Bridge

AG2 primarily defines agents in code (T1: GitHub repo):
- `ConversableAgent` with `name`, `system_message`, `llm_config`
- **AutoGen Studio**: declarative JSON workflow definitions for visual composition
- **AgentSpec integration**: Oracle's open spec for portable agent definitions can be loaded into AG2's runtime

AG2's model: agents are Python objects. Declarative definitions exist for serialization and Studio, not as the primary authoring format.

#### LangGraph: Graph-Based Agent Composition

LangGraph agents are graph nodes, not files (T1: GitHub repo):
- Agents defined as `StateGraph` compositions with tool nodes
- Reusable through class inheritance (e.g., `AnalyzerAgent` base class)
- **LangGraph Studio**: visual prototyping with runtime configuration changes
- No file-based agent convention — reuse through code patterns

### 4. Emerging Standards: AgentSpec and Agent2Agent

Two standards are formalizing agent definitions at different levels (MODERATE — standards are early but backed by major organizations):

#### Oracle AgentSpec (Portable Agent Definitions)

AgentSpec is "a framework-agnostic declarative language for defining agentic systems" (T1: GitHub repo + Oracle blog, October 2025):
- **Five logical components**: LLM, Flow, Node, Tool, Agent — extensible with custom components
- **Two runnable primitives**: Agents (conversational, ReAct-style) and Flows (structured workflows)
- **Format**: JSON/YAML serializable via PyAgentSpec Python SDK
- **Properties**: system prompts, LLM configurations, typed inputs/outputs, tool declarations
- **MCP integration**: supports MCP servers for standardized tool access, "reducing the need for custom adapters for every external API" (T1: Oracle blog)
- **Runtime adapters**: WayFlow (reference), LangGraph, CrewAI, AutoGen — "each runtime exposing as much of the Agent Spec's functionality as it can support" (T1: Oracle blog)
- **ONNX analogy**: explicitly inspired by ONNX for ML models — same portability model applied to agents
- **Portability**: same definition runs on AG2, LangGraph, CrewAI, or OCI Agents without rewriting
- **Status**: v26.1.0 released; AG-UI integration announced (2026)

#### Agent2Agent Protocol (Network-Level Discovery)

Google's A2A protocol defines how agents discover and communicate across networks (T1: A2A specification):
- **Agent Card**: JSON at `/.well-known/agent-card.json` advertising capabilities
- **Fields**: `name`, `description`, `url`, `version`, `provider`, `capabilities`, `authentication`, `skills[]`
- **Skills in A2A**: discrete capability units with `id`, `name`, `description`, `tags`, `examples`
- **Task lifecycle**: agents communicate to complete tasks with defined states
- **Governance**: Linux Foundation, 150+ organizations, v0.3 (July 2025) added gRPC
- **Gemini CLI integration**: remote subagents can use A2A for network dispatch

A2A's "skills" are closer to WOS's tools/capabilities — units of work an agent can perform. The Agent Card is the agent's identity and capability advertisement.

### 5. Key Architectural Distinction: Agents vs. Skills vs. Tools

Across all systems, a consistent three-level hierarchy emerges (HIGH — convergent across independent implementations):

| Concept | What it is | Context | Invocation |
|---------|-----------|---------|------------|
| **Tool** | A function with schema | Runs in caller's context | Direct function call |
| **Skill** | Reusable instructions/knowledge | Injected into caller's context | Loaded, not dispatched |
| **Agent** | Autonomous actor with own identity | Runs in own context window | Dispatched with a task, returns results |

Critical differences:
- **Skills enrich an agent's context**; agents have their own context. Claude Code's `skills` frontmatter field makes this explicit: skill content is *injected into* the agent, not invoked by it.
- **Tools execute in the caller's context**; agents execute independently. Gemini CLI makes this visible: agents are "exposed as a tool of the same name" but run in isolation.
- **Agents can be scoped, permissioned, and model-selected independently**. Skills and tools inherit these from their host.

### 6. Dispatch Patterns

Three distinct dispatch patterns have emerged (HIGH — documented across multiple T1 sources):

**Description-based auto-routing** (Claude Code): The main agent reads subagent descriptions and decides when to delegate. "Claude uses each subagent's description to decide when to delegate tasks" (T1). The user doesn't choose — the agent routes based on task fit.

**User-selected** (GitHub Copilot): Users pick an agent from a dropdown. The agent runs for the duration of the conversation. `disable-model-invocation` prevents automatic selection.

**Agent-as-tool** (Gemini CLI): Agents are registered as tools. The main agent calls them like any other tool, passing a task description as input. "When the main agent calls the tool, it delegates the task to the subagent" (T1).

All three share: the dispatched agent runs in its own context, receives a task, and returns results to the dispatcher.

### 7. Plugin Distribution of Agents

Only Claude Code has a documented convention for distributing agents via plugins (HIGH — T1, single source):

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/           # ← agents at plugin root
│   └── specialist.md
├── skills/
│   └── my-skill/
│       └── SKILL.md
└── .mcp.json
```

Plugin agents have lowest priority (below project and user agents). This means plugins can provide default agents that projects or users can override with same-named definitions.

GitHub Copilot has organization-level agents (`.github-private` repo) but no plugin packaging model for third-party distribution.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|---|---|---|---|
| Markdown+YAML is the converged format for agent definitions | Claude Code, Copilot, Gemini CLI all use it independently | CrewAI uses separate YAML (not frontmatter); AgentSpec uses JSON/YAML objects | Low — the file-level convention still converges; framework-level differs |
| Agents are fundamentally different from skills/tools | All three coding tools maintain separate directories; Claude Code explicitly prevents skill injection from replacing agent identity | Gemini CLI exposes agents *as* tools; the boundary is blurry | High — if agents collapse into tools, a separate `agents/` directory is unnecessary |
| Description-based routing is the dominant dispatch pattern | Claude Code uses it; it's the most autonomous model | Copilot uses user-selection; Gemini uses agent-as-tool | Medium — WOS could use any pattern; the architectural choice matters |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|---|---|---|
| Agent conventions are too new and may not stabilize | Medium — Gemini CLI is experimental; Copilot agents are recent | Qualifies urgency: adopt the pattern, but expect evolution in frontmatter fields |
| WOS as a plugin doesn't need its own agent convention — it can use Claude Code's native `agents/` directory | High — WOS already runs as a Claude Code plugin with access to the Agent tool | Reframes the question: WOS doesn't need to invent a convention; it should use Claude Code's existing one |
| No nesting constraint limits reuse | Medium — Claude Code subagents cannot spawn other subagents | May limit complex orchestration; but execute-plan dispatches from foreground, not from a subagent |

## Claims

| # | Claim | Type | Source | Status |
|---|---|---|---|---|
| 1 | Claude Code subagents are defined as "Markdown files with YAML frontmatter" | quote | [1] | verified |
| 2 | Claude Code supports three agent scopes: project, user, plugin | attribution | [1] | verified |
| 3 | "Subagents are exposed to the main agent as a tool of the same name" (Gemini CLI) | quote | [4] | verified |
| 4 | GitHub Copilot agents stored at `.github/agents/[name].agent.md` | attribution | [2] | verified |
| 5 | "Claude uses each subagent's description to decide when to delegate tasks" | quote | [1] | verified |
| 6 | Copilot prompt limit is 30,000 characters | statistic | [3] | verified |
| 7 | Gemini CLI requires `enableAgents: true` in settings | attribution | [4] | verified |
| 8 | CrewAI uses `src/[project]/config/agents.yaml` | attribution | [5] | verified |
| 9 | Semantic Kernel supports "a single assistant definition can be created and reused multiple times" | quote | [6] | verified |
| 10 | AgentSpec is "a framework-agnostic declarative language for defining agentic systems" | quote | [7] | verified |
| 11 | A2A protocol Agent Card hosted at `/.well-known/agent-card.json` | attribution | [8] | verified |
| 12 | A2A protocol has 150+ supporting organizations as of v0.3 | statistic | [8] | verified |
| 13 | Cline subagents "cannot write files, apply patches, use the browser, access MCP servers, or perform web searches" | quote | [9] | verified |
| 14 | Claude Code subagents "cannot spawn other subagents" | quote | [1] | verified |
| 15 | Claude Code agents receive "only this system prompt (plus basic environment details), not the full Claude Code system prompt" | quote | [1] | verified |
| 16 | AgentSpec is "inspired by the success of representations like Open Neural Network Exchange (ONNX) for ML models" | quote | [10] | verified |
| 17 | AgentSpec logical components are "LLM, Flow, Node, Tool, Agent" | attribution | [10] | verified |
| 18 | AgentSpec runtime adapters exist for "WayFlow, LangGraph, CrewAI, AutoGen" | attribution | [10] | verified |
| 19 | AgentSpec supports MCP servers, "reducing the need for custom adapters for every external API" | quote | [10] | verified |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/sub-agents | Create custom subagents | Anthropic | 2026 | T1 | verified |
| 2 | https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents | Creating custom agents for Copilot | GitHub | 2025 | T1 | verified |
| 3 | https://docs.github.com/en/copilot/reference/custom-agents-configuration | Custom agents configuration | GitHub | 2025 | T1 | verified |
| 4 | https://geminicli.com/docs/core/subagents/ | Subagents (experimental) | Google / Gemini CLI | 2025 | T1 | verified |
| 5 | https://docs.crewai.com/en/concepts/agents | Agents - CrewAI | CrewAI | 2025 | T1 | verified |
| 6 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-templates | Create an Agent from a Template | Microsoft | 2026 | T1 | verified |
| 7 | https://github.com/oracle/agent-spec | Open Agent Spec | Oracle | 2025 | T1 | verified |
| 8 | https://agent2agent.info/docs/concepts/agentcard/ | AgentCard – A2A Protocol | A2A Project / Linux Foundation | 2025 | T1 | verified |
| 9 | https://docs.cline.bot/features/subagents | Subagents - Cline | Cline | 2025 | T1 | verified |
| 10 | https://blogs.oracle.com/ai-and-datascience/introducing-open-agent-specification | Introducing the Open Agent Specification | Oracle Labs (Hong, Ravi, Patra) | 2025-10-07 | T1 | verified (403, content from PDF) |

## Key Takeaways

1. **The convention has converged**: markdown files with YAML frontmatter in an `agents/` directory is the pattern across Claude Code, Copilot, and Gemini CLI. WOS doesn't need to invent a new convention.

2. **Agents ≠ skills**: every system that has both maintains a clear separation. Skills are knowledge injected into context; agents are autonomous actors with their own context window. This distinction is architecturally load-bearing.

3. **Claude Code's convention is the richest and most relevant**: as a Claude Code plugin, WOS should use Claude Code's native `agents/` directory with its standard frontmatter fields (name, description, tools, model, skills, background, isolation).

4. **The "no nesting" constraint matters**: Claude Code subagents cannot spawn other subagents. This means WOS's execute-plan (which dispatches research workers) must run in the foreground — it can dispatch subagents, but those subagents can't dispatch further. This matches WOS's current architecture.

5. **Skill injection is the bridge**: Claude Code's `skills` frontmatter field lets agents load skill content at startup. A research-worker agent could load the research skill's methodology as injected knowledge, rather than duplicating it as a separate payload.

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| Claude Code agents directory convention | google | 2025-2026 | 10 | 3 |
| OpenAI Codex agents directory convention | google | 2025-2026 | 10 | 2 |
| Cursor AI agent definition rules | google | 2025-2026 | 10 | 1 |
| GitHub Copilot custom agent convention | google | 2025-2026 | 10 | 3 |
| Gemini CLI agent definition convention | google | 2025-2026 | 10 | 2 |
| CrewAI agent definition YAML | google | 2025-2026 | 10 | 2 |
| AG2 AutoGen agent configuration | google | 2025-2026 | 10 | 1 |
| LangGraph agent definition | google | 2025-2026 | 10 | 1 |
| Semantic Kernel agent templates | google | 2025-2026 | 10 | 2 |
| Agent card protocol specification | google | 2025-2026 | 10 | 3 |
| AgentSpec Oracle specification | google | 2025-2026 | 10 | 2 |
| Claude Code plugin agents directory | google | 2025-2026 | 10 | 2 |
| Aider Cline agent convention | google | 2025-2026 | 10 | 1 |

13 searches across 1 source, 130 found, 25 used.
