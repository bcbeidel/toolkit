---
name: "Tool Description Quality and Consolidation"
description: "Tool description quality is the single biggest lever for selection accuracy; consolidation (fewer, more capable tools) outperforms proliferation"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  - https://agentskills.io/specification
  - https://arxiv.org/html/2602.12430v3
related:
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/skill-mcp-tool-subagent-taxonomy.context.md
  - docs/context/cli-dual-mode-design-for-agents.context.md
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
---
Detailed tool descriptions are the single most important factor for tool selection accuracy. This holds across Claude Code skills, MCP tools, and function calling definitions. The description is the input the model uses to decide which tool to invoke. Schema completeness matters far less than description clarity.

**What a good description covers:**
- What the tool does (primary function)
- When to use it (specific trigger conditions)
- When NOT to use it (exclusions and edge cases)
- What each parameter means (not just the type)
- Caveats, constraints, rate limits, return format

Aim for 3-4 sentences minimum for simple tools; more for complex ones. Anthropic's guidance reports that "clarity improvements on benchmarks can be dramatic" — the description quality gap between a one-liner and a full explanation often exceeds the performance gap between different models.

**The consolidation principle.** Fewer, more capable tools outperform many narrow ones. Two mechanisms:

1. Group related operations under a single tool with an `action` parameter: `github_pr` with `action: "create" | "review" | "merge"` reduces three separate tools to one. The agent selects the tool once, then selects the action — two decisions instead of one routing decision from a crowded pool.

2. Prefer `schedule_event` (finds availability + creates) over `list_users` + `list_events` + `create_event`. Composing multiple API calls inside a single tool reduces the number of tool-selection decisions the model must make per workflow.

Excessive tools distract agents. The arxiv 2026 skill survey identifies a phase transition in selection accuracy as library size grows — routing degrades sharply past certain ecosystem sizes. The correct response is to consolidate, not to improve descriptions on 30 narrow tools.

**Naming conventions.** Namespace by service or resource: `asana_search`, `jira_search`, or `asana_projects_search`. Use semantic identifiers in tool names and responses — `user_slug` not `user_id`, slugs not UUIDs. Claude's tool name constraint: `^[a-zA-Z0-9_-]{1,64}$`.

**Response design matters too.** Return only high-signal information. Strip opaque internal IDs. Implement a `response_format` parameter for `"concise"` vs `"detailed"` — agents control their context budget. Unfiltered large responses degrade downstream reasoning quality because agents pay per token of context consumed.

**Anti-patterns:**
- Tool proliferation: overlapping tools with similar descriptions cause selection ambiguity
- Brute-force retrieval: returning all records forces token-by-token scanning; use filtered search
- Opaque errors: technical tracebacks waste context; structured errors with suggestions enable self-correction
- Description-as-documentation: tool descriptions are not man pages — they are routing signals; keep them agent-facing, not developer-facing
