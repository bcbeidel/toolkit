---
name: "Tool Design for LLM Agents"
description: "How to design tool interfaces that LLM agents can select, invoke, and recover from reliably: schemas, descriptions, error signaling, idempotency, and scaling"
metadata:
  type: reference
  sources:
    - https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
    - https://developers.openai.com/docs/guides/function-calling
    - https://modelcontextprotocol.io/docs/concepts/tools
    - https://arxiv.org/abs/2305.15334
    - https://www.anthropic.com/engineering/building-effective-agents
  related:
    - docs/research/tool-design-for-llms.md
    - docs/context/prompt-engineering.md
    - docs/context/llm-capabilities-limitations.md
---

Tool design for LLM agents differs from traditional API design in one
fundamental way: the consumer reads the interface definition at decision
time. There is no separate documentation step. The tool's schema and
description are the only information the model has when deciding whether
and how to call it.

## The Three-Layer Contract

Claude, OpenAI, and MCP all converge on the same layered structure:

1. **Metadata layer** (name, description, annotations) -- the model reads
   this to decide whether to call the tool.
2. **Schema layer** (JSON Schema for inputs, optionally outputs) -- the
   runtime validates this.
3. **Protocol layer** (correlation IDs, stop reasons, content types) --
   the orchestrator routes on this.

JSON Schema is the universal interface definition language across all three
systems. Enabling `strict: true` (supported by both Claude and OpenAI)
guarantees schema conformance, eliminating type mismatches, missing fields,
and unexpected parameters. For production agents, strict mode is the single
most impactful reliability setting.

## Descriptions Drive Tool Selection

Models select tools based on natural language descriptions, not schema
structure. A tool with a perfect schema but a vague description will be
misused; a tool with a clear description and a loose schema often works.

Effective descriptions follow the "intern test" (OpenAI's framing): could
someone unfamiliar with your system use the tool correctly from the
description alone? Concrete guidance:

- State what the tool does, not how it works internally.
- Specify exact formats for parameters (e.g., "ISO 8601 date string").
- Use enums instead of describing valid values in prose.
- Document edge cases ("Returns empty array if no results found").
- Be precise but not verbose -- excessive description text adds token cost
  without improving selection accuracy.

The Gorilla paper demonstrates that models hallucinate wrong API calls when
descriptions are inadequate, and retrieval-augmented approaches (injecting
current docs at inference time) significantly reduce this.

## Error Signaling

Tool errors must be in-band (returned in the normal response flow), not
exceptions. The agent needs to see the error in its context to reason about
recovery.

MCP's two-tier model is the most mature: protocol errors (wrong tool name,
malformed request) are distinct from execution errors (rate limits, invalid
data). This matters because protocol errors indicate bugs in reasoning while
execution errors suggest transient or input-dependent problems worth retrying.

Every error should include: what failed, why it failed, and whether retry
is appropriate. "Rate limit exceeded. Retry after 30 seconds" enables
intelligent recovery. "Error occurred" does not.

## Idempotency and Mutation Safety

Agents that fail mid-loop need to know which tools are safe to re-invoke.
MCP formalizes this with annotations: `readOnlyHint`, `destructiveHint`,
`idempotentHint`, and `openWorldHint`. Claude and OpenAI lack native
annotations, so safety properties must be encoded in descriptions.

At minimum, every tool should declare its mutation profile: read-only tools
say so explicitly, idempotent writes note that repeated calls produce the
same result, and non-idempotent writes warn against blind retries.

## Scaling: Keep the Active Set Small

Tool count degrades selection accuracy. OpenAI recommends starting under
20 tools. Both OpenAI (tool search, namespaces) and MCP (pagination,
`listChanged` notifications) provide deferred loading mechanisms. The limit
is about concurrent context, not total available tools -- with proper
deferred loading, large tool sets (100+) can work effectively.

## Anti-Patterns

Six patterns reliably degrade agent tool use: ambiguous output formats that
force text parsing, hidden side effects not declared in descriptions,
missing parameter documentation that causes hallucinated values, excessive
concurrent tool count, opaque errors without recovery guidance, and
schema-description mismatches where the schema allows values the tool
rejects.
