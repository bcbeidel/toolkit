---
name: "Open-Source Runtimes Lack Native Tool Calling"
description: "Ollama and vLLM-based open-source model runtimes lack native tool calling and require JSON-prompting workarounds — a distinct portability class separate from cloud providers"
type: context
sources:
  - https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/
  - https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a
  - https://blog.langchain.com/tool-calling-with-langchain/
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/tool-api-incompatibility-cloud-providers.context.md
  - docs/context/langchain-tool-abstraction-gaps.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
---

# Open-Source Runtimes Lack Native Tool Calling

Open-source model runtimes (Ollama, vLLM, llama.cpp) represent a distinct portability class from cloud providers. Many lack native tool calling entirely and require system-prompt engineering to produce structured JSON output. This is not a minor adaptation gap — it is a fundamental architectural difference that requires a separate integration approach.

## The Cloud vs. Open-Source Divide

Cloud providers (OpenAI, Anthropic, Gemini) all implement native tool calling: the model runtime has built-in mechanisms for receiving tool definitions and returning structured tool invocation responses. Despite their API format incompatibilities (see: tool-api-incompatibility-cloud-providers), they share this foundational capability.

Open-source runtimes do not have a unified story:

- **Models with native tool calling:** Llama 3.1+, Mistral 7B/8x7B, some Qwen variants have fine-tuned tool calling capability when served via Ollama or vLLM with appropriate model variants
- **Models without native tool calling:** Many open-source models "require prompting to emit JSON with no native tools" — the application must engineer a system prompt that describes the desired output schema and hope the model complies
- **Runtime layer vs. model layer:** Even when the model supports tool calling, the serving runtime (Ollama, vLLM, llama.cpp) may not expose it through a standard tool-calling API, requiring application-layer adaptation

## The LangChain Signal

LangChain's `ChatOllama` and `MLXPipeline` raise `NotImplementedError` on `bind_tools()`. This is not a LangChain bug — it reflects the reality that the underlying runtimes do not consistently implement native tool calling. LangChain's abstraction boundary stops at cloud providers precisely because open-source runtimes lack the foundational capability the abstraction assumes.

## WOS Implications

A WOS skill targeting open-source runtimes would need to:
1. Detect whether the runtime supports native tool calling
2. Fall back to explicit schema description in the system prompt for runtimes that do not
3. Handle the response as free-form text rather than a parsed tool call structure
4. Manage the substantially higher failure rate and inconsistency of prompt-engineered structured output vs. native tool calling

WOS's current guidance does not address open-source runtime targets. The entire WOS skill architecture (L1/L2/L3 loading, `allowed-tools`, `context: fork`) assumes a runtime with Claude Code's capabilities. Open-source runtimes are not just a harder version of the cloud-provider portability problem — they require a different approach.

## Confidence Note

The finding that open-source runtimes "often require prompting to emit JSON with no native tools" comes from challenger-phase search result summaries, not a directly fetched primary source. It is consistent with the known LangChain `NotImplementedError` behavior (T1 sourced) and with the structured output comparison across providers (T5 source). The characterization is directionally reliable but the specific framing should be treated as indicative rather than empirically measured.

---

**Takeaway:** Open-source model runtimes (Ollama, vLLM) are a distinct portability class from cloud providers. Many lack native tool calling and require JSON-prompting workarounds. LangChain's `NotImplementedError` on `ChatOllama` reflects this reality. WOS does not currently address open-source runtime targets, and extending to them requires a fundamentally different integration approach.
