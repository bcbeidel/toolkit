---
name: "Tool API Formats Are Incompatible Across OpenAI, Anthropic, and Gemini"
description: "OpenAI, Anthropic, and Gemini use incompatible tool definition formats, schema systems, and response structures at the API level — the only shared portable layer is JSON Schema for parameter definitions"
type: context
sources:
  - https://ai.google.dev/gemini-api/docs/function-calling
  - https://modelcontextprotocol.io/docs/concepts/tools
  - https://blog.langchain.com/tool-calling-with-langchain/
  - https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google
  - https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/
  - https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/mcp-vs-skill-format-abstraction-layers.context.md
  - docs/context/langchain-tool-abstraction-gaps.context.md
  - docs/context/open-source-runtime-tool-calling-gaps.context.md
  - docs/context/mcp-vs-function-calling-tradeoffs.context.md
---

# Tool API Formats Are Incompatible Across OpenAI, Anthropic, and Gemini

The three dominant cloud AI providers use fundamentally different API structures for tool definition, invocation, and response parsing. Direct API code written for one provider cannot run against another without structural changes. The only shared portable layer is JSON Schema for parameter definitions.

## API Format Comparison

**OpenAI:**
```json
{"type": "function", "function": {"name": "...", "parameters": {...}}}
```
Returns `tool_call.function.arguments` as a JSON *string* — callers must `json.loads()` to parse it.

**Anthropic:**
```json
{"name": "...", "input_schema": {...}}
```
Returns `block.input` as an already-parsed Python dict — no deserialization step required.

**Gemini:**
Uses Protocol Buffer types: `types.FunctionDeclaration(name=..., parameters=types.Schema(...))`. Returns proto objects requiring explicit `dict()` conversion. Recent Gemini models add a mandatory `id`-matching requirement where function call responses must include an `id` field matching the original function call — this is a Gemini-specific constraint not present in OpenAI or Anthropic.

LangChain's own documentation confirms: "All of these providers exposed slightly different interfaces (in particular: OpenAI, Anthropic, and Gemini, the three highest performing models are incompatible)."

## What Is Actually Portable

JSON Schema for parameter definitions is the one structural element all three providers accept in compatible form. This shared layer is what enables framework abstractions (LangChain `bind_tools`, LlamaIndex `FunctionTool`) to normalize tool definitions across providers internally.

Everything else — the outer wrapper format, the response parsing model, proto types vs. dicts, argument serialization — is provider-specific.

## Structured Output Divergence

The incompatibility extends to structured output (constrained generation). OpenAI, Anthropic, and Gemini each have different APIs for requesting structured responses, different constraint mechanisms, and different reliability profiles. A comparison across providers (Glukhov, 2025) found meaningful differences in formatting compliance rates and in which edge cases each provider handles correctly. This is a separate failure surface from tool definition incompatibility.

## Framework Abstraction as the Mitigation

LangChain's `bind_tools()` and LlamaIndex's `FunctionTool`/`ToolSpec` handle provider-specific wire format translation internally. Swapping providers requires substituting only the LLM class. This achieves portability for cloud providers (OpenAI, Anthropic, Gemini).

However, this abstraction is not complete: it does not cover open-source runtimes (see: open-source-runtime-tool-calling-gaps) and has a confirmed production failure mode with `bind_tools` + `with_structured_output` (see: langchain-tool-abstraction-gaps). The framework layer partially mitigates API incompatibility but does not eliminate it.

## Implications for WOS

WOS skills are not directly exposed as API-level tool definitions — they are SKILL.md files consumed at the prompt layer. But when WOS skills invoke underlying scripts that make API calls, or when WOS is integrated with LangChain/LlamaIndex for cross-runtime deployment, the API incompatibilities described here become load-bearing. Any WOS infrastructure that targets multiple providers must account for these structural differences.

---

**Takeaway:** OpenAI, Anthropic, and Gemini tool APIs are structurally incompatible — different outer formats, different return types, different schema systems. JSON Schema for parameters is the only shared layer. Framework abstractions (LangChain, LlamaIndex) mitigate this for cloud providers but not for open-source runtimes.
