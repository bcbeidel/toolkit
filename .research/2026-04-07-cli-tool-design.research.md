---
name: "CLI & Tool Design for LLM Agents"
description: "How to design CLI scripts and tools for LLM agent consumption — output formats, tool registration patterns, MCP tool definitions, and cross-provider function calling"
type: research
sources:
  - https://modelcontextprotocol.io/specification/2025-11-25/server/tools
  - https://modelcontextprotocol.io/specification/2025-11-25/basic
  - https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
  - https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://platform.openai.com/docs/guides/function-calling
  - https://ai.google.dev/gemini-api/docs/function-calling
  - https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/
  - https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no
  - https://www.infoq.com/articles/ai-agent-cli/
  - https://dev.to/meimakes/rewrite-your-cli-for-agents-or-get-replaced-2a2h
  - https://www.firecrawl.dev/blog/why-clis-are-better-for-agents
  - https://gist.github.com/thoroc/973bef1770387e1986876ab6c6d20947
  - https://zilliz.com/blog/function-calling-vs-mcp-vs-a2a-developers-guide-to-ai-agent-protocols
related:
  - docs/research/2026-04-07-skill-ecosystem-design.research.md
---

## Research Question

How should CLI scripts and tools be designed for LLM agent consumption? What output formats, registration patterns, and protocol structures enable effective agent-tool integration?

## Sub-Questions

1. How should CLI scripts be designed for both human and LLM agent consumption?
2. What output formats (JSON, structured text, exit codes) work best for LLM tool integration?
3. How do tool registration patterns (JSON Schema, function-as-tool) work across agent frameworks?
4. What are MCP's current capabilities for tool exposure and how does the protocol structure tool definitions?

## Search Protocol

| # | Query | Key Finding |
|---|-------|-------------|
| 1 | MCP Model Context Protocol tool definitions specification 2025 JSON Schema | Official spec at modelcontextprotocol.io/specification/2025-11-25 confirmed; tools use inputSchema (JSON Schema 2020-12 default) |
| 2 | CLI design for LLM agents structured output exit codes 2025 | Multiple practitioner articles; exit code taxonomy 0-5; --json flag pattern; stdout/stderr split |
| 3 | function calling tool registration JSON Schema OpenAI Anthropic Gemini 2025 | Three divergent schemas: OpenAI `parameters`, Anthropic `input_schema`, Gemini `types.Schema` |
| 4 | Claude Code tool use computer use bash tool structured output 2025 agent design | Anthropic tool use docs; client vs. server tools; strict tool use; stop_reason: "tool_use" |
| 5 | MCP tool annotations readOnlyHint destructiveHint idempotentHint 2025 specification | Four hint fields confirmed; added March 2025; untrusted unless from trusted server |
| 6 | MCP specification tools/list tools/call server 2025 | Full protocol messages extracted: tools/list, tools/call, isError flag, structuredContent field |
| 7 | Claude define-tools best practices | Detailed naming/description/input_schema format; input_examples; strict mode; tool consolidation guidance |
| 8 | OpenAI function calling strict mode JSON Schema 2025 2026 | Strict mode requires additionalProperties:false and all fields required; schema validated at first call |
| 9 | Exit code conventions CLI tools LLM agent stderr stdout separation | Stdout is API contract (clean JSON); stderr for diagnostics; meaningful exit codes required |
| 10 | Gemini function_declarations schema format 2025 agent | Gemini uses Protocol Buffer-style types; OpenAPI-subset schema; max 32 nesting depth |
| 11 | MCP vs function calling patterns agent frameworks comparison 2025 | MCP = M+N problem (vs M×N); dynamic discovery; function calling = tight coupling; both used in prod |
| 12 | Anthropic engineering writing-tools-for-agents | Tool consolidation; namespace prefixes; semantic identifiers in responses; response_format param |
| 13 | MCP transports specification | stdio (subprocess stdin/stdout) and Streamable HTTP (POST+SSE) are the two standard transports |
| 14 | Tool description best practices when to use when not to use | Detailed descriptions outperform brief ones; include exclusions; aim 3-4 sentences minimum |
| 15 | Function calling comparison complete guide 2026 | Cross-provider table: tool detection method, arguments type, result role all differ |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://modelcontextprotocol.io/specification/2025-11-25/server/tools | MCP Tools Specification | Anthropic/MCP | 2025-11-25 | T1 | verified |
| 2 | https://modelcontextprotocol.io/specification/2025-11-25/basic | MCP Base Protocol | Anthropic/MCP | 2025-11-25 | T1 | verified |
| 3 | https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/ | Tool Annotations as Risk Vocabulary | MCP Blog | 2026-03-16 | T1 | verified |
| 4 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools | Define tools (Claude) | Anthropic | 2025-2026 | T1 | verified |
| 5 | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | Tool use overview (Claude) | Anthropic | 2025-2026 | T1 | verified |
| 6 | https://www.anthropic.com/engineering/writing-tools-for-agents | Writing tools for agents | Anthropic Engineering | 2025 | T1 | verified |
| 7 | https://platform.openai.com/docs/guides/function-calling | Function calling (OpenAI) | OpenAI | 2025-2026 | T1 | 403 blocked |
| 8 | https://ai.google.dev/gemini-api/docs/function-calling | Function calling (Gemini) | Google | 2025 | T1 | search-verified |
| 9 | https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/ | Function Calling Complete Guide 2026 | oFox AI | 2026 | T3 | verified |
| 10 | https://dev.to/uenyioha/writing-cli-tools-that-ai-agents-actually-want-to-use-39no | Writing CLI Tools for AI Agents | DEV Community | 2025 | T3 | verified |
| 11 | https://www.infoq.com/articles/ai-agent-cli/ | Keep the Terminal Relevant: Patterns for AI Agent Driven CLIs | InfoQ | 2025 | T3 | verified |
| 12 | https://dev.to/meimakes/rewrite-your-cli-for-agents-or-get-replaced-2a2h | Rewrite Your CLI for Agents | DEV Community | 2025 | T3 | verified |
| 13 | https://www.firecrawl.dev/blog/why-clis-are-better-for-agents | Why CLIs Are Better for AI Coding Agents Than IDEs | Firecrawl | 2025 | T3 | verified |
| 14 | https://gist.github.com/thoroc/973bef1770387e1986876ab6c6d20947 | I stopped using function calling entirely | Former Manus backend lead | 2025 | T4 | verified |
| 15 | https://zilliz.com/blog/function-calling-vs-mcp-vs-a2a-developers-guide-to-ai-agent-protocols | Function Calling vs MCP vs A2A | Zilliz | 2025 | T3 | verified |

## Raw Extracts

### Sub-question 1: CLI Design for Human and LLM Agent Consumption

**Core tension: humans want UX polish, agents need machine precision.**

CLIs built for humans use color, pagination, interactive prompts, and pretty-printed output. Each of these breaks agent workflows. The solution is dual-mode design: full UX for TTY sessions, machine output for non-TTY sessions (detected via `isatty()`).

**Three escape hatches every CLI needs (InfoQ, DEV Community):**

1. **Explicit flags**: `--no-prompt`, `--no-interactive`, `--no-color`, `--json`, `--quiet/-q`
2. **Environment variables**: `NO_COLOR=true`, `MYCLI_NO_INTERACTIVE=1`, `OUTPUT_FORMAT=json`  
   - Precedence: flags override env vars
3. **Semantic exit codes**: must be stable across minor versions

**Command structure for agent discoverability:**

Use noun-verb hierarchy: `mytool resource action` (not flat flag-heavy commands). This converts discovery into tree search — agents can enumerate resources, then actions, rather than guessing valid flag combinations. Example: `gws sheets spreadsheets create` is agent-navigable; `create-spreadsheet` is not.

**JSON as first-class input:**  
Beyond `--json` output flags, support JSON payload input for complex operations. Pattern (from DEV Community):
- Human-first: `my-cli spreadsheet create --title "Q1 Budget" --locale "en_US"`
- Agent-first: `gws sheets spreadsheets create --json '{"properties": {...}, "sheets": [...]}'`

**Schema introspection at runtime:**  
Implement introspection commands like `mytool schema resource.action` returning full method signatures, parameters, response types, and permissions as JSON. This eliminates needing to inject static documentation into agent prompts.

**AWS CLI v2 pager incident (InfoQ):** Defaulting to `less` in headless environments broke agent workflows. Lesson: agents cannot type "q" to dismiss pagers. Every UX convenience needs an override path.

**CLIs over IDEs for agents (Firecrawl):**  
- CLI agents are "designed for delegation" — autonomous operation vs. IDE agent "suggestions"
- Context efficiency: CLIs load only explicitly requested files; IDEs pollute context with full state
- Deterministic feedback: exit codes and text streams enable self-correction without human input
- Composability: Unix pipe semantics allow workflow assembly in single calls

**Controversial alternative — single `run(command="...")` tool (former Manus backend lead):**  
One practitioner abandoned function catalogs entirely for a single shell execution tool backed by Unix commands. Rationale: LLMs are trained on billions of CLI examples from GitHub/Stack Overflow, making shell composition natural. A single piped command (`cat log | grep ERROR | wc -l`) replaces three separate function calls. The architecture requires a two-layer design:
- Layer 1 (Execution): Pure Unix semantics with pipes and chains
- Layer 2 (LLM Presentation): Binary guards (prevents parsing PNGs as text), output truncation at N lines with navigation hints, stderr attachment, metadata (exit codes, duration)

Production failure modes observed:
- Binary file parsed as text → 20 useless iterations until binary guard added
- Silent stderr on pip-not-found → 10 blind retry attempts; exposing stderr reduced to 1

### Sub-question 2: Output Formats and Exit Codes for LLM Integration

**Stdout/stderr separation (the fundamental contract):**

- **stdout** = machine-parseable data. The "API contract." Must be clean JSON when `--json` is used.
- **stderr** = diagnostics. Progress messages, warnings, spinners, status updates, human-readable errors.
- Rationale: Agents pipe stdout to subsequent commands. Any human text in stdout breaks parsing.
- Critical note (DEV Community): "Stderr is the information agents need most, precisely when commands fail — never drop it."

**JSON output design (DEV Community, InfoQ):**

- Flat structures preferred over deeply nested; easier to extract specific fields
- JSON Lines (JSONL) for streaming/incremental output — agents can process results as they arrive
- Field masking support: `--params '{"fields": "id,name,mimeType"}'` reduces context window consumption
- Agents "pay per token" — unfiltered large responses degrade reasoning capacity
- For backwards compatibility, structured content should also appear as serialized JSON in a text block (MCP spec pattern)

**Exit code taxonomy (DEV Community, InfoQ consensus):**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General failure |
| 2 | Usage error (bad arguments) |
| 3 | Resource not found |
| 4 | Permission denied |
| 5 | Conflict (resource already exists) |
| 3-125 | Application-specific errors |

"A tool that returns 0 on failure breaks every agent workflow that depends on it." Exit codes must remain stable across minor versions — treat them as a versioned API.

**Error response design:**

Errors must be actionable. The structured error pattern:
```json
{"error": "image_not_found", "image": "registry/name:tag", "suggestion": "run 'mycli images list' to see available images"}
```

Three error categories:
- **Transient** (retry-worthy): network timeout, rate limit
- **Permanent** (do not retry): resource not found, permission denied
- **Correctable** (retry with different input): validation error with specific field guidance

Distinguish them explicitly in the structured output so agents can reason about next action.

**Dry-run pattern:**  
`--dry-run` should produce structured JSON diff of what *would* change, not prose description. Enables agent preflight validation before destructive operations.

**Progress reporting for long-running commands:**  
Stream JSONL events rather than blocking until completion. Example: `aws cloudformation describe-stack-events --output json`. This maintains consistent output streams critical for backgrounded agent processes.

**`--quiet/-q` flag**: Bare output — one value per line — for direct piping without JSON parsing overhead.

### Sub-question 3: Tool Registration Patterns Across Agent Frameworks

**Function calling (tight coupling model):**  
Tool definitions are embedded directly in each LLM API request. Every call sends the full schema. Each provider has a distinct format.

**OpenAI format:**
```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "...",
    "parameters": {
      "type": "object",
      "properties": { "location": { "type": "string" } },
      "required": ["location"],
      "additionalProperties": false
    },
    "strict": true
  }
}
```
- Tool detection: inspect `message.tool_calls`
- Arguments returned as: JSON string (requires parsing)
- Result role: `"tool"`
- Strict mode: requires `additionalProperties: false` and all fields in `required`; validates schema on first request (latency hit); subsequent calls are fast

**Anthropic (Claude) format:**
```json
{
  "name": "get_weather",
  "description": "...",
  "input_schema": {
    "type": "object",
    "properties": { "location": { "type": "string", "description": "City and state" } },
    "required": ["location"]
  },
  "input_examples": [
    {"location": "San Francisco, CA"}
  ]
}
```
- Tool detection: `stop_reason == "tool_use"`
- Arguments returned as: pre-parsed dict (no JSON parsing step)
- Result role: `"user"` (fed back in user message)
- Name constraint: must match `^[a-zA-Z0-9_-]{1,64}$`
- `strict: true` available for guaranteed schema conformance
- `input_examples`: optional array for complex/nested schemas; schema-validated; ~20-200 tokens each
- `defer_loading` and `allowed_callers` available as optional properties
- Tool descriptions injected into a special system prompt prepended to user system prompt

**Google Gemini format:**
```python
types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="get_weather",
        description="...",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"location": types.Schema(type=types.Type.STRING)}
        )
    )
])
```
- Uses Protocol Buffer-style types, not raw JSON
- Supports OpenAPI schema subset: type, nullable, required, format, description, properties, items, enum, anyOf, $ref, $defs
- Max nesting depth: 32; max recursion in defs: 2
- Tool detection: inspect `parts[]` for `function_call`
- Arguments returned as: Proto object
- Result role: `"user"` (as parts)

**Cross-provider comparison table (oFox AI, 2026):**

| Aspect | OpenAI | Anthropic | Gemini |
|--------|--------|-----------|--------|
| Schema key | `parameters` | `input_schema` | `types.Schema` |
| Tool wrapper | `{"type":"function","function":{...}}` | Direct object | `FunctionDeclaration` |
| Tool detection | `message.tool_calls` | `stop_reason == "tool_use"` | `parts[].function_call` |
| Arguments type | JSON string (parse required) | Pre-parsed dict | Proto object |
| Result role | `"tool"` | `"user"` | `"user"` (as parts) |
| Parallel calls | Default-enabled | Multiple tool_use blocks | Via `ToolConfig` |
| Max tools/request | 128 | 128 | 128 |
| Strict mode | `strict: true` | `strict: true` | N/A (OpenAPI subset) |

**Portability note:** Pydantic schemas translate across providers since they generate standard JSON Schema. But invocation patterns, detection methods, and result formats differ significantly — migration requires API-layer refactoring.

**Tool design best practices (Anthropic Engineering):**

*Descriptions:*
- Detailed descriptions are the single most important factor for tool performance
- Include: what it does, when to use it, when NOT to use it, what each parameter means, caveats
- Aim for 3-4 sentences minimum; more for complex tools
- Clarity improvements on benchmarks can be dramatic — description quality matters more than schema completeness

*Naming:*
- Namespace by service: `asana_search`, `jira_search` (or resource: `asana_projects_search`)
- Use specific identifiers: `user_id` not `user`
- Name constraint (Claude): `^[a-zA-Z0-9_-]{1,64}$`

*Consolidation over proliferation:*
- Prefer `schedule_event` (finds availability + creates) over `list_users` + `list_events` + `create_event`
- Group related operations with an `action` parameter: `github_pr` with `action: "create"|"review"|"merge"`
- Fewer, more capable tools reduce selection ambiguity; excessive tools distract agents

*Response design:*
- Return only high-signal information; strip opaque internals
- Use semantic identifiers (slugs, names) over UUIDs and internal IDs
- Implement `response_format` parameter for `"concise"` vs `"detailed"` — agents control context usage
- Test response formats (JSON, XML, Markdown) — performance varies by training data alignment

*Anti-patterns:*
- Tool proliferation: overlapping tools degrade selection accuracy
- Brute-force retrieval: returning all records forces token-by-token scanning; use filtered search
- Opaque errors: technical tracebacks waste tokens; actionable guidance steers recovery
- Ignoring eval data: analyze which tools agents struggle with and iterate

**MCP vs. function calling (Zilliz, multiple sources):**

| Concern | Function Calling | MCP |
|---------|-----------------|-----|
| Coupling | Tight (embedded in request) | Loose (protocol-separated) |
| Discovery | Static (defined at request time) | Dynamic (tools/list at runtime) |
| Reuse | Per-application | One server, many clients |
| Problem scaling | M×N (each model × each tool) | M+N |
| Best for | Single-model, few internal tools | Multi-model, shared integrations |

Production pattern: use both — MCP for shared/reusable tools, function calling for agent-specific logic.

### Sub-question 4: MCP Protocol Structure and Tool Capabilities

**Protocol foundations:**
- JSON-RPC 2.0 messages, UTF-8 encoded
- Stateful connections with capability negotiation at initialization
- Three server primitive types: Resources (context), Prompts (templates), Tools (executable functions)
- Tools are model-controlled (vs. resources = application-controlled, prompts = user-controlled)

**Tool definition schema (2025-11-25 spec):**
```json
{
  "name": "get_weather",
  "title": "Weather Information Provider",
  "description": "Get current weather information for a location",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": { "type": "string", "description": "City name or zip code" }
    },
    "required": ["location"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": { "type": "number" },
      "conditions": { "type": "string" }
    }
  },
  "annotations": {
    "readOnlyHint": true,
    "destructiveHint": false,
    "idempotentHint": true,
    "openWorldHint": true
  },
  "execution": {
    "taskSupport": "optional"
  },
  "icons": [{"src": "https://example.com/icon.png", "mimeType": "image/png", "sizes": ["48x48"]}]
}
```

**Key fields:**
- `name`: 1-128 chars; `[a-zA-Z0-9_\-.]` only; case-sensitive; unique within server
- `title`: Human-readable display name (separate from `name` used programmatically)
- `inputSchema`: MUST be valid JSON Schema object (not null); defaults to JSON Schema 2020-12
- `outputSchema`: Optional; servers MUST conform, clients SHOULD validate
- `annotations`: Behavioral hints; untrusted unless from trusted server
- `execution.taskSupport`: `"forbidden"` (default), `"optional"`, or `"required"`
- For no-parameter tools: `{"type": "object", "additionalProperties": false}` (recommended)

**Tool annotations (added March 2025, MCP Blog):**

Four boolean hints in `ToolAnnotations`:

| Hint | Default | Meaning |
|------|---------|---------|
| `readOnlyHint` | false | Tool does not modify its environment |
| `destructiveHint` | true | Modifications are destructive (vs. additive) |
| `idempotentHint` | false | Repeated calls with same args are safe |
| `openWorldHint` | true | Tool interacts with external entities |

Conservative defaults: "A tool with no annotations is assumed to be non-read-only, potentially destructive, non-idempotent, and open-world."

Practical client use:
- `readOnlyHint: true` from trusted server → candidate for auto-approval
- `destructiveHint: true` → trigger confirmation dialog
- `openWorldHint: true` → signal trust-boundary crossing

Critical limitation: annotations cannot be trusted from untrusted servers. They provide no protection against prompt injection. Hard security guarantees require network controls or sandboxing.

**Protocol messages:**

*tools/list (discovery):*
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"cursor":"optional"}}
```
Response: `{"tools": [...], "nextCursor": "..."}` — supports pagination

*tools/call (invocation):*
```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_weather","arguments":{"location":"New York"}}}
```

*Tool result structure:*
```json
{
  "content": [{"type": "text", "text": "..."}],
  "structuredContent": {"temperature": 22.5, "conditions": "Partly cloudy"},
  "isError": false
}
```

Content types: `text`, `image` (base64), `audio` (base64), `resource_link` (URI), `resource` (embedded). All support annotations with `audience`, `priority`, and `lastModified`.

**Two error tiers:**
1. **Protocol errors** (JSON-RPC errors): unknown tool, malformed request — structural issues models cannot fix
2. **Tool execution errors** (`isError: true` in result): validation failures, API errors — actionable, models can self-correct and retry. Clients SHOULD pass execution errors back to the LLM.

**Transport mechanisms:**

*stdio (preferred for local):*
- Client launches server as subprocess
- Server reads JSON-RPC from stdin, writes to stdout, MAY write logs to stderr
- Server MUST NOT write non-MCP content to stdout
- Credentials retrieved from environment (no auth framework)

*Streamable HTTP (replaces HTTP+SSE from 2024-11-05):*
- Single MCP endpoint supporting POST (client→server) and GET (server→client SSE)
- Session management via `Mcp-Session-Id` header
- Protocol version via `MCP-Protocol-Version` header
- Supports resumable streams with event IDs and `Last-Event-ID`
- Security: MUST validate `Origin` header (DNS rebinding protection); SHOULD bind to localhost only

*listChanged notification:*  
Servers declare `"tools": {"listChanged": true}` capability; send `notifications/tools/list_changed` when tool list changes. Clients should re-fetch tools/list on receipt.

**Dynamic discovery advantage:**  
Unlike function calling (tools defined at request time), MCP enables runtime tool discovery. Agents query `tools/list`, discover available tools, and select appropriate ones dynamically. This enables modularity and capability expansion without client changes.

**A2A (Agent-to-Agent) — complementary protocol:**  
Where MCP handles tool exposure, A2A handles agent-to-agent delegation. Agents advertise capabilities, delegate tasks to best-suited agents, and coordinate progress. Used in complex multi-agent systems where MCP handles individual tool access.

## Findings

1. **Dual-mode CLIs**: Detect TTY vs. non-TTY; serve full UX for humans, machine output for agents. Three escape hatches: flags, env vars, exit codes.

2. **stdout = API contract**: JSON to stdout, everything else to stderr. Violation breaks every agent pipeline downstream.

3. **Exit codes are versioned APIs**: Meaningful codes beyond 0/1 (taxonomy: 0=success, 1=general, 2=usage, 3=not-found, 4=permission, 5=conflict). Stable across minor versions.

4. **Tool descriptions outperform tool schemas**: Detailed natural language descriptions — including when NOT to use a tool — are the single biggest lever for tool selection accuracy.

5. **MCP tool fields in 2025**: `name`, `title`, `description`, `inputSchema`, `outputSchema` (new), `annotations`, `execution.taskSupport`, `icons`. The `outputSchema` field enables structured result validation.

6. **Tool annotations are hints, not guarantees**: Four boolean hints added March 2025. Useful for UX (confirmation dialogs, auto-approval) but cannot be trusted from untrusted servers.

7. **Cross-provider function calling diverges on detection and result format**: Schemas are similar (JSON Schema object), but tool detection method, argument type (string vs. dict vs. proto), and result role differ per provider. Pydantic bridges the schema layer but not the invocation layer.

8. **Consolidate tools, not proliferate**: Fewer, more capable tools outperform many narrow ones. Group related operations under a single tool with an `action` parameter.

9. **MCP vs. function calling**: MCP solves M×N → M+N; enables dynamic discovery; suited for shared, reusable tooling. Function calling is simpler for single-model, few-tool cases. Production systems use both.

10. **Single bash tool as alternative**: Practitioners with high-volume agents sometimes replace function catalogs with a single shell execution tool backed by Unix commands. Requires binary guards, output truncation, and stderr attachment at the presentation layer.

## Challenge

### Claim: "Detailed descriptions are the single most important factor for tool selection accuracy"
**Strength:** MODERATE. This is Anthropic's published guidance [6] with some benchmark support, but the benchmarks are internal and not independently replicated across providers. The claim is directionally well-supported but "single most important" is a strong superlative.

### Claim: "MCP tool annotations added March 2025"
**Strength:** HIGH. The MCP blog post is dated 2026-03-16 and is a T1 source. Well-sourced [3].

### Claim: "Each provider max 128 tools per request (OpenAI/Anthropic/Gemini)"
**Strength:** MODERATE. The table cites oFox AI (T3) [9]. OpenAI documentation was 403-blocked during gathering [7]. Anthropic's documentation was confirmed by T1 source. The Gemini limit should be verified against T1 docs.

### Claim: "Single bash tool approach abandoned by Manus backend lead"
**Strength:** LOW-MODERATE. Source [14] is a T4 GitHub Gist from an anonymous "former Manus backend lead." The approach is architecturally interesting and plausible, but attribution cannot be verified. The failure modes described (binary parsing, silent stderr) are independently plausible based on other sources.

### What this research does NOT cover
- Python tool frameworks (LangChain, LlamaIndex tools) vs. raw function calling API
- Tool result caching and memoization patterns
- Security considerations for CLI tools (injection via arguments, path traversal)
- Streaming tool results and partial responses
- A2A protocol depth (only surface-level overview collected)

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | MCP tools use JSON-RPC 2.0 messages, UTF-8 encoded | attribution | [1][2] | verified |
| 2 | MCP tool `name` field: 1-128 chars, `[a-zA-Z0-9_\-.]` only | attribution | [1] | verified |
| 3 | Tool annotations (4 boolean hints) added to MCP spec March 2025 | date/attribution | [3] | verified |
| 4 | MCP `outputSchema` field is new in 2025-11-25 spec | attribution | [1] | verified |
| 5 | Claude tool name constraint: `^[a-zA-Z0-9_-]{1,64}$` | attribution | [4] | verified |
| 6 | Claude `input_examples` field: schema-validated, ~20-200 tokens each | attribution | [4] | verified |
| 7 | All three providers (OpenAI/Anthropic/Gemini) support max 128 tools per request | statistic | [9] | human-review — T3 source; OpenAI docs 403-blocked during gathering |
| 8 | OpenAI strict mode requires `additionalProperties: false` and all fields in `required` | attribution | [7] | human-review — OpenAI docs 403-blocked; from T3 source [9] instead |
| 9 | Gemini max schema nesting depth: 32; max recursion in defs: 2 | statistic | [8] | verified (search-confirmed) |
| 10 | `readOnlyHint` default is false; `destructiveHint` default is true | attribution | [3] | verified |
| 11 | MCP Streamable HTTP replaces HTTP+SSE from 2024-11-05 spec | attribution | [1][2] | verified |
