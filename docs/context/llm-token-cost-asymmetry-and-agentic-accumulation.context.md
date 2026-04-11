---
name: LLM Token Cost Asymmetry and Agentic Accumulation
description: Output tokens cost 5–8x input tokens for flagship models; multi-step agentic calls are the dominant cost driver via accumulated context re-sends on every step.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://platform.claude.com/docs/en/build-with-claude/prompt-caching
  - https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025
  - https://redis.io/blog/llm-token-optimization-speed-up-apps/
  - https://medium.com/elementor-engineers/optimizing-token-usage-in-agent-based-assistants-ffd1822ece9c
  - https://blog.langchain.com/context-management-for-deepagents/
related:
  - docs/context/llm-caching-and-tiering-savings-with-failure-modes.context.md
  - docs/context/context-rot-and-window-degradation.context.md
  - docs/context/agent-memory-tier-taxonomy-and-implementation-gaps.context.md
---
# LLM Token Cost Asymmetry and Agentic Accumulation

Output tokens cost 5–8x more than input tokens for flagship models. GPT-5.2 is 8x ($1.75 input / $14.00 output per million tokens), Claude Sonnet 4.6 is 5x ($3.00 / $15.00), Gemini 3.1 Pro is 6x ($2.00 / $12.00). The commonly cited "4–5x" understates the ratio for current flagship models.

This asymmetry has a direct design implication: optimizing output volume matters more than compressing input tokens. Every unnecessary sentence in a generated response is more expensive than every unnecessary sentence in the prompt.

## Multi-Step Agent Calls Are the Real Cost Driver

The per-token price is not the primary cost concern in agentic systems. Context accumulation is.

In a multi-step agent task, every step re-sends the full accumulated context. A 10-step task with a growing 20K-token context does not consume 20K input tokens — it accumulates toward 200K+ input tokens across all steps. The agentic cost multiplier is proportional to step count times average context size, not just per-task token volume.

Agent design must treat per-step context accumulation as a first-class cost concern:
- Prefer fewer, more capable agent steps over many cheap steps
- Offload large tool results to the filesystem (LangChain's Deep Agents SDK triggers this automatically at 85% context utilization: tool responses over 20K tokens are moved to disk, replaced with a file path and 10-line preview)
- Filter available tools before sending to the model — unused tools still consume input tokens
- Set hard `max_tokens` caps to prevent runaway inference

## Reasoning Models Are a Hidden Cost Tier

OpenAI o1/o3 and Gemini 2.5 Pro (thinking mode) generate internal chain-of-thought tokens billed as output tokens at full output price — but these tokens are not returned in the API response. A single evaluation suite for o1 consumed 44 million tokens at $2,767. Effective per-task cost for reasoning models can be 10–25x higher than visible token pricing implies.

This creates a hidden cost cliff when agent workflows adopt reasoning models without accounting for invisible tokens. Standard cost monitoring tools often do not surface reasoning token usage correctly.

## Context Optimization Patterns

**Lazy tool loading:** Conditionally include system prompt sections only when the corresponding tool category is active. Unused tool definitions still consume tokens on every call.

**Structured output schemas:** Replace verbose example prompts with compact schemas. The information content is equivalent; the token cost is not.

**Structured error messages:** Return structured, actionable error messages instead of verbose failures. Each retry incurs full token charges — a retry-prone agent multiplies its own cost.

**Serialization efficiency:** Data serialization waste consumes 40–70% of available tokens in RAG architectures. Semantic chunking based on meaning rather than character counts reduces this.

**The takeaway:** In agent systems, the cost model is accumulation, not per-call pricing. Design agents to minimize turns. Offload large outputs to disk. Treat context growth as a cost function that compounds with each step.
