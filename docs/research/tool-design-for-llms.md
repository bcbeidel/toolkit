---
name: "Tool Design for LLM Agents"
description: "Technical investigation of tool interface design for LLM agents: input/output contracts, error signaling, idempotency, and how tool design affects agent reasoning, with patterns from Claude, OpenAI, and MCP"
metadata:
  type: research
  sources:
    - https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
    - https://developers.openai.com/docs/guides/function-calling
    - https://modelcontextprotocol.io/docs/concepts/tools
    - https://arxiv.org/abs/2305.15334
    - https://arxiv.org/abs/2304.08354
    - https://developers.openai.com/docs/guides/tools-tool-search
    - https://www.anthropic.com/engineering/building-effective-agents
  related:
    - docs/research/prompt-engineering.md
    - docs/research/llm-capabilities-limitations.md
    - docs/context/tool-design-for-llms.md
---

## Summary

Technical investigation of what makes a good tool interface for LLM agents, drawn from
7 sources including official documentation from Anthropic and OpenAI, the MCP specification,
and academic research on tool-augmented language models.

**Key findings:**

- **Schema is the contract.** Both Claude and OpenAI converge on JSON Schema as the
  universal tool interface language. Strict mode (both providers) guarantees schema
  conformance, eliminating a class of runtime failures (HIGH).
- **Descriptions drive tool selection.** Models choose tools primarily from natural
  language descriptions, not schema structure. Description quality directly determines
  whether an agent selects the right tool (HIGH).
- **Error signaling must be in-band.** Tools should return errors as structured content
  (not exceptions), with enough context for the agent to reason about recovery. MCP
  formalizes this with `isError: true` (HIGH).
- **Idempotency annotations enable safe retries.** MCP's tool annotations
  (`idempotentHint`, `destructiveHint`, `readOnlyHint`) represent the emerging standard
  for communicating safety properties to agents (MODERATE).
- **Tool count degrades performance.** Both providers recommend starting under 20 tools.
  Deferred loading (OpenAI tool search, MCP pagination) addresses scaling (HIGH).
- **Constrain inputs to prevent invalid states.** Enums, required fields, and strict
  schemas are more effective than describing constraints in text (HIGH).

## Research Brief

**Mode:** Technical | **Intensity:** High

**Sub-questions:**
1. What input/output contracts make tools reliably usable by LLM agents?
2. How should tools signal errors to agents, and how does error design affect recovery?
3. What role does idempotency play in agent tool use, and how should it be designed?
4. How does tool description quality affect agent reasoning and tool selection?
5. What patterns emerge from comparing Claude, OpenAI, and MCP tool interfaces?
6. What anti-patterns in tool design degrade agent performance?

## Search Protocol

| # | Query | Source | Hits | Useful |
|---|-------|--------|------|--------|
| 1 | Claude tool use documentation | platform.claude.com | 1 | 1 |
| 2 | OpenAI function calling guide | developers.openai.com | 1 | 1 |
| 3 | MCP tools specification | modelcontextprotocol.io | 1 | 1 |
| 4 | Gorilla LLM tool use paper | arxiv.org | 1 | 1 |
| 5 | Tool learning foundation models | arxiv.org | 1 | 1 |
| 6 | OpenAI tool search deferred loading | developers.openai.com | 1 | 1 |
| 7 | Building effective agents Anthropic | anthropic.com | 1 | 1 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview | Tool Use with Claude | Anthropic | 2025 | T1 | verified |
| 2 | https://developers.openai.com/docs/guides/function-calling | Function Calling | OpenAI | 2025 | T1 | verified |
| 3 | https://modelcontextprotocol.io/docs/concepts/tools | MCP Tools | Anthropic / MCP | 2025 | T1 | verified |
| 4 | https://arxiv.org/abs/2305.15334 | Gorilla: Large Language Model Connected with Massive APIs | UC Berkeley | 2023 | T2 | verified |
| 5 | https://arxiv.org/abs/2304.08354 | Tool Learning with Foundation Models | Qin et al. | 2023 | T2 | verified |
| 6 | https://developers.openai.com/docs/guides/tools-tool-search | Tool Search | OpenAI | 2025 | T1 | verified |
| 7 | https://www.anthropic.com/engineering/building-effective-agents | Building Effective Agents | Anthropic | 2024 | T1 | verified |

## Extracts

### Sub-question 1: What input/output contracts make tools reliably usable by LLM agents?

**From [1] Anthropic Tool Use:**
- Tools are defined with `name`, `description`, and `input_schema` (JSON Schema object)
- Properties have types, descriptions, enums, and required arrays
- Claude returns `tool_use` blocks with `id`, `name`, and `input` fields
- Results return as `tool_result` blocks with `tool_use_id` and `content`
- `strict: true` enables guaranteed schema validation for tool inputs
- "Each tool defines a contract: you specify what operations are available and what they return; Claude decides when and how to call them"

**From [2] OpenAI Function Calling:**
- Functions defined with `name`, `description`, `parameters` (JSON Schema), and optional `strict: true`
- Response contains `tool_calls` array with `id`, `function.name`, `function.arguments`
- Results returned as strings (JSON, plain text, or error codes)
- Strict mode requires `additionalProperties: false` and all properties marked `required`
- Optional fields represented by adding `null` as a type option

**From [3] MCP Tools:**
- Tools have `name`, `title` (display), `description`, `inputSchema`, optional `outputSchema`, and `annotations`
- Input and output both defined via JSON Schema
- Results returned as `content` array (text, image, audio, resource links, embedded resources)
- `structuredContent` field for typed JSON responses alongside unstructured text
- Output schema enables strict validation: "Servers MUST provide structured results that conform to this schema"

**Convergent pattern:** All three systems use JSON Schema as the interface definition language. All separate tool metadata (name, description) from the schema itself. All use a request/response cycle with correlation IDs.

### Sub-question 2: How should tools signal errors to agents, and how does error design affect recovery?

**From [1] Anthropic:**
- Tool results support an `is_error` flag to indicate failure
- Error content returned as text in the `tool_result` block
- The agent sees the error message and can reason about it, retry, or try a different approach
- No structured error codes — the error is a natural language string

**From [2] OpenAI:**
- Results are strings; error codes can be returned as plain text
- "Return success/failure strings for functions with no explicit output"
- Model interprets result format contextually
- No formal error schema — relies on the model to parse error text

**From [3] MCP:**
- Two-tier error system: protocol errors (JSON-RPC error codes) vs tool execution errors (`isError: true`)
- Protocol errors: unknown tool (-32602), invalid arguments, server errors
- Tool execution errors: returned in the result with `isError: true` and descriptive text
- Clear separation: infrastructure failures vs business logic failures

**Key insight:** MCP's two-tier approach is the most mature. Protocol errors (wrong tool name, malformed request) are distinct from tool execution errors (API rate limit, invalid input). This distinction matters because the agent should handle them differently: protocol errors suggest a bug in the agent's reasoning; execution errors suggest a transient or input-dependent problem worth retrying.

### Sub-question 3: What role does idempotency play in agent tool use?

**From [3] MCP Tool Annotations:**
- `readOnlyHint`: tool does not modify state (default false)
- `destructiveHint`: tool may perform destructive updates (default true)
- `idempotentHint`: calling repeatedly with same args has no additional effect (default false)
- `openWorldHint`: tool interacts with external entities (default true)
- These are hints, not guarantees — "clients MUST consider tool annotations to be untrusted unless they come from trusted servers"

**From [1] Anthropic:**
- No explicit idempotency annotations in the Claude API
- Agent loops handle retry logic at the orchestration layer
- `pause_turn` stop reason for server tools that hit iteration limits — implies retry is safe

**From [2] OpenAI:**
- No formal idempotency markers
- `parallel_tool_calls: false` can enforce sequential execution, reducing duplicate calls
- Tool choice `required` vs `auto` controls invocation frequency

**Key insight:** MCP is the only system that formally annotates idempotency. Claude and OpenAI leave this to the tool implementer and orchestrator. For agent frameworks, idempotency annotations are critical: an agent that fails mid-loop needs to know which tools are safe to re-invoke. Without this metadata, agents must be conservative (assume destructive) or rely on the system prompt to communicate safety properties.

### Sub-question 4: How does tool description quality affect agent reasoning and tool selection?

**From [1] Anthropic:**
- Claude Opus "thinks before it answers" to determine if a tool is necessary, which to use, and parameters
- Claude Sonnet/Haiku are "prompted to try to use tools as much as possible" — more likely to call unnecessary tools
- Chain-of-thought prompting improves tool selection for smaller models
- Missing parameters: Opus asks for clarification, Sonnet guesses

**From [2] OpenAI:**
- "Write clear and detailed function names, parameter descriptions, and instructions"
- Apply the "intern test" — could someone unfamiliar use the function correctly from docs alone?
- Use system prompts to specify when/when not to use functions
- Examples and edge cases help but may reduce reasoning model performance
- Start with fewer than 20 functions — performance degrades with count

**From [4] Gorilla:**
- Models "hallucinate the wrong usage of an API call" — wrong parameters, wrong API entirely
- Retrieval-augmented approach improves accuracy: pairing the model with current documentation
- API documentation quality directly correlates with call accuracy

**From [5] Tool Learning with Foundation Models:**
- Models must "decompose a complex task into several subtasks, dynamically adjust their plan through reasoning, and effectively conquer each sub-task by selecting appropriate tools"
- Tool selection depends on description clarity and schema expressiveness

**Key insight:** Description quality is the single highest-leverage lever for tool design. The model has no way to "try" a tool to see what it does — it must select based on the description alone. Both providers' documentation emphasizes this. The Gorilla paper demonstrates that poor documentation causes hallucinated API calls, and retrieval-augmented approaches (providing relevant documentation at inference time) significantly improve accuracy.

### Sub-question 5: What patterns emerge from comparing Claude, OpenAI, and MCP?

**Convergent patterns (all three systems):**
- JSON Schema as interface definition language
- Natural language descriptions as primary selection signal
- Request/response correlation IDs for multi-turn tracking
- Structured input, flexible output (text, images, errors all in result)
- Tool definitions consume context window tokens

**Divergent patterns:**

| Feature | Claude | OpenAI | MCP |
|---------|--------|--------|-----|
| Error signaling | `is_error` flag | String-based | `isError` + JSON-RPC errors |
| Strict mode | `strict: true` | `strict: true` | Output schema validation |
| Parallel calls | Default on | Default on, disable with flag | N/A (protocol-level) |
| Tool annotations | None | None | `readOnlyHint`, `destructiveHint`, `idempotentHint` |
| Deferred loading | N/A | Tool search | `tools/list` with pagination + `listChanged` |
| Output schema | No formal output schema | No formal output schema | `outputSchema` field |
| Namespacing | No | Namespace objects | N/A |
| Tool count guidance | Not documented | Under 20 | N/A |

**From [6] OpenAI Tool Search:**
- Deferred loading reduces token usage: tools loaded only when needed
- Namespace grouping with `defer_loading: true`
- "Loaded tools are injected at the context window's end, preserving the model's cache"
- Fewer than 10 functions per namespace for efficiency

### Sub-question 6: What anti-patterns in tool design degrade agent performance?

**From [1] Anthropic:**
- Not providing enough context for Claude to determine parameter values
- Using tools when direct prompting would suffice
- Overloading tool count without organization

**From [2] OpenAI:**
- Requiring the model to fill arguments the caller already knows
- Exposing all tools upfront rather than deferring
- Vague descriptions that fail the "intern test"
- Overusing examples with reasoning models (can reduce performance)
- Not using enums when the valid set is known

**From [4] Gorilla:**
- Hallucinated API calls — models invent endpoints or parameters
- API version drift — tools change but descriptions don't update
- Lack of retrieval augmentation for large API surfaces

**Synthesized anti-patterns:**
1. **Ambiguous output format** — returning unstructured strings when the agent needs to parse specific values
2. **Hidden side effects** — tools that modify state without indicating it in the description
3. **Missing required context** — descriptions that don't explain what input formats are expected
4. **Excessive tool count** — degrading selection accuracy by forcing the model to choose among too many options
5. **Opaque errors** — returning "error" instead of explaining what went wrong and what to try
6. **Schema-description mismatch** — the schema allows values the tool cannot handle

## Challenge

**Counter-evidence to "descriptions drive tool selection":**
OpenAI notes that examples may "reduce reasoning model performance" — suggesting that
more description content is not always better. There is a point of diminishing returns
where verbose descriptions add token cost without improving selection accuracy. The
optimal description is precise but concise (MODERATE — based on OpenAI guidance,
not empirical measurement).

**Counter-evidence to "strict mode solves schema conformance":**
Strict mode requires all properties to be `required` and `additionalProperties: false`.
This means optional parameters must be represented as nullable types rather than
omitted. For tools with many optional parameters, this creates verbose schemas that
consume additional tokens. The trade-off is between schema safety and token efficiency
(MODERATE — architectural trade-off, not failure evidence).

**Counter-evidence to "MCP annotations are the emerging standard":**
MCP annotations are explicitly "hints" that "clients MUST consider untrusted unless
they come from trusted servers." A malicious or buggy server could mark destructive
tools as `readOnlyHint: true`. The annotations provide no guarantee — they are
metadata that the client must validate independently. Neither Claude nor OpenAI has
adopted this pattern in their native APIs (MODERATE — adoption risk).

**Counter-evidence to "under 20 tools":**
OpenAI's tool search feature is designed for tool sets that far exceed 20. The
recommendation is "start" under 20, not "stay" under 20. With proper deferred
loading, large tool sets (100+) can work effectively. The limit is about concurrent
context, not total available tools (MODERATE — the guidance is about starting
configuration, not hard limit).

## Findings

### What input/output contracts make tools reliably usable by LLM agents?

The industry has converged on JSON Schema as the universal tool interface contract.
All three major systems (Claude API, OpenAI API, MCP) use JSON Schema for input
definition, with MCP extending this to output schemas as well [1][2][3].

The effective contract has three layers (HIGH — T1 sources converge):
1. **Metadata layer**: name, description, annotations — the model reads these to decide
   whether to call the tool
2. **Schema layer**: JSON Schema defining valid inputs and (optionally) expected outputs —
   the runtime validates these
3. **Protocol layer**: correlation IDs, stop reasons, content types — the orchestrator
   uses these to route messages

Strict mode is the strongest contract mechanism available. Both Anthropic and OpenAI
support `strict: true`, which guarantees that model-generated tool calls conform to the
defined schema [1][2]. This eliminates type mismatches, missing fields, and unexpected
parameters. For production agents, strict mode is the single most impactful reliability
improvement (HIGH — both T1 sources recommend this for production).

The output side is less standardized. Claude and OpenAI return results as strings or
content arrays with no formal output schema. MCP introduces `outputSchema` and
`structuredContent`, allowing bidirectional schema validation [3]. This asymmetry
means agents must currently be robust to unpredictable output formats even when inputs
are strictly typed (MODERATE — only MCP addresses this).

### How should tools signal errors to agents?

Error design directly affects whether an agent can recover from failures or enters a
failure loop. The critical design decision is **in-band vs out-of-band** error signaling.

MCP's two-tier approach represents the most mature pattern [3] (HIGH — formal specification):
- **Protocol errors** (JSON-RPC codes): unknown tool, invalid arguments, server unavailable.
  These indicate bugs in the agent's reasoning or infrastructure failures.
- **Tool execution errors** (`isError: true`): API rate limits, invalid input data,
  business logic failures. These indicate the tool was called correctly but could not
  complete.

Both Claude and OpenAI use simpler models. Claude supports an `is_error` flag on
`tool_result` blocks [1]. OpenAI expects error information as plain text strings [2].
Neither provides structured error codes or categories (MODERATE — observed from
documentation, may have undocumented features).

**Design recommendation:** Tool errors should include three components:
1. **What failed** — a machine-parseable category (not just a message)
2. **Why it failed** — enough context for the agent to reason about the cause
3. **What to do** — whether retry is appropriate, with what changes

Tools that return only "Error occurred" give the agent no basis for recovery. Tools that
return "Rate limit exceeded. Retry after 30 seconds" enable intelligent backoff (HIGH —
convergent guidance from all sources).

### What role does idempotency play in agent tool use?

Idempotency determines whether an agent can safely retry a failed tool call — one of
the most common operations in agentic loops. MCP is the only system that formally
annotates this property [3] (HIGH — specification-level).

MCP defines four behavioral annotations:
- `readOnlyHint`: no state modification (safe to call freely)
- `destructiveHint`: may modify or delete data (requires confirmation)
- `idempotentHint`: repeated calls with same args produce same effect (safe to retry)
- `openWorldHint`: interacts with external systems beyond the server

These annotations are additive. A tool can be both `idempotentHint: true` and
`destructiveHint: true` (e.g., a PUT endpoint that overwrites a resource) [3].

Neither Claude nor OpenAI provides native idempotency annotations [1][2]. Agents using
these APIs must encode safety properties in tool descriptions or system prompts, which
is less reliable than structured metadata (MODERATE — functional gap, but workarounds
exist).

**Design recommendation:** Every tool should declare its mutation profile. At minimum:
- **Read-only tools**: explicitly state "This tool does not modify any state"
- **Idempotent write tools**: state "Calling this tool multiple times with the same
  input produces the same result"
- **Non-idempotent write tools**: state "Each call creates a new resource; do not retry
  without confirming the previous call failed"

Without these declarations, agents default to conservative behavior (avoid retries),
which reduces reliability for transient failures (MODERATE — inferred from agent
behavior patterns, not empirically measured).

### How does tool description quality affect agent reasoning?

Tool descriptions are the primary signal an LLM uses to decide whether and how to call
a tool. This is unlike traditional API design where the developer reads documentation
separately from the interface definition — for agents, the description is the only
documentation they see at decision time [1][2][4].

Both Anthropic and OpenAI document that model capability varies with description
quality (HIGH — T1 sources converge):
- Claude Opus performs chain-of-thought reasoning before tool selection, evaluating
  relevance and parameter availability. Claude Sonnet/Haiku are more aggressive, often
  calling tools without sufficient analysis [1].
- OpenAI recommends the "intern test": could someone unfamiliar with your system use
  the function correctly from the description alone? [2]

The Gorilla paper [4] demonstrates that models "hallucinate the wrong usage of an API
call" when descriptions are inadequate. Their retrieval-augmented approach — injecting
current API documentation at inference time — significantly reduces hallucination.
This suggests that static descriptions may drift from actual tool behavior, and
dynamic documentation retrieval can compensate (MODERATE — academic, single study).

**Design recommendations for descriptions:**
1. State what the tool does, not how it works internally
2. Specify the exact format expected for each parameter (e.g., "ISO 8601 date string")
3. Use enums instead of describing valid values in text
4. Include the edge case behavior ("Returns empty array if no results found")
5. Keep under the "intern test" threshold — precise but not verbose

### What patterns emerge across implementations?

Three structural convergences stand out across Claude, OpenAI, and MCP (HIGH — all
T1 sources):

**1. Schema-first tool definition.** All three systems define tools via JSON Schema.
This is not accidental — JSON Schema provides machine-parseable type information
that models can reason about structurally. The schema serves double duty: runtime
validation and model comprehension.

**2. Natural language as the selection mechanism.** Despite having formal schemas,
models select tools based on the `description` field, not schema analysis. This means
a tool with a perfect schema but a poor description will be used incorrectly, while a
tool with a good description and a loose schema may work fine (assuming the model
generates valid JSON).

**3. In-band error signaling.** All three systems return errors within the normal
response flow rather than as exceptions or out-of-band signals. This is essential
for agentic loops: the agent needs to see the error in its context to reason about
next steps.

Key divergences:

**Output typing:** MCP supports formal output schemas; Claude and OpenAI do not. This
means agents consuming Claude/OpenAI tools must be robust to arbitrary output formats.

**Tool metadata:** MCP provides behavioral annotations (read-only, destructive,
idempotent); Claude and OpenAI rely on descriptions alone for behavioral hints.

**Scaling patterns:** OpenAI addresses tool proliferation with tool search and
namespaces [6]. MCP uses pagination and `listChanged` notifications [3]. Claude
has no documented scaling mechanism for large tool sets.

### What anti-patterns degrade agent performance?

Six anti-patterns emerge from cross-referencing sources (HIGH for 1-3, MODERATE for 4-6):

**1. Ambiguous output format.** Returning unstructured strings when the agent needs
to extract specific values. The agent must parse free text, which is unreliable.
Use structured JSON or MCP's `structuredContent` instead [2][3].

**2. Hidden side effects.** Tools that modify state without indicating it in the
description or annotations. An agent may call a "get" tool that silently creates
a log entry, then be surprised by rate limits or audit trails [3].

**3. Missing parameter documentation.** Descriptions that say "pass the ID" without
specifying format, length, or where to obtain it. Models either hallucinate values
or ask unnecessary clarifying questions [1][4].

**4. Excessive tool count.** Exposing more than 20 tools simultaneously degrades
selection accuracy. Use deferred loading, namespacing, or tool search to keep the
active set small [2][6].

**5. Opaque errors.** Returning "Error" or "Failed" without context. The agent has
no basis for deciding whether to retry, use a different tool, or ask the user.
Include the error category and recovery guidance [3].

**6. Schema-description mismatch.** The schema allows `string` for a date field but
the tool actually requires ISO 8601 format. The model generates a natural language
date, the tool fails, and the agent enters a retry loop. Use `format` or `pattern`
in the schema, or add the constraint to the description [2].

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Tool access is one of the highest-leverage primitives you can give an agent" | quote | [1] | verified |
| 2 | Adding tools produces "outsized capability gains, often surpassing human expert baselines" on LAB-Bench and SWE-bench | statistic | [1] | verified |
| 3 | OpenAI recommends starting with fewer than 20 functions | recommendation | [2] | verified |
| 4 | Both Claude and OpenAI support `strict: true` for schema conformance | feature | [1][2] | verified |
| 5 | MCP defines four tool annotations: readOnlyHint, destructiveHint, idempotentHint, openWorldHint | specification | [3] | verified |
| 6 | Gorilla "surpasses the performance of GPT-4 on writing API calls" | attribution | [4] | verified |
| 7 | Models "hallucinate the wrong usage of an API call" | quote | [4] | verified |
| 8 | Tool Learning paper covers 18 representative tools | statistic | [5] | corrected (source says "experimentation with representative tools" — exact count from abstract summary, not direct quote) |
| 9 | OpenAI tool search preserves model cache by injecting at context window end | feature | [6] | verified |
| 10 | MCP annotations are explicitly hints that "clients MUST consider untrusted" | quote | [3] | verified |

## Takeaways

For WOS tool/skill design, these findings suggest:

1. **Every tool needs a precise, concise description.** This is the single highest-ROI
   investment in tool quality. Apply the "intern test."
2. **Use JSON Schema strictly.** Constrain inputs with enums, required fields, and
   format specifiers. Enable strict mode in production.
3. **Return structured errors with recovery guidance.** Never return bare "Error" strings.
   Include what failed, why, and what to do next.
4. **Annotate mutation properties.** Even without formal annotation support, declare
   read-only, idempotent, and destructive behaviors in descriptions.
5. **Keep active tool sets small.** Use deferred loading or skill routing to avoid
   overwhelming the model with choices.
6. **Define output contracts.** Even if the API does not enforce output schemas, document
   the expected return format so consuming agents can parse reliably.
