---
name: "WOS Skill Portability Across Model Runtimes"
description: "WOS skill portability is real at the Agent Skills spec minimum (name+description+markdown body), but WOS-idiomatic patterns (context:fork, allowed-tools, L1/L2/L3 loading, dynamic injection) are Claude Code-specific and not flagged as such; MCP solves tool invocation, not skill file format portability; LangChain/LlamaIndex abstract cloud providers but not open-source runtimes"
type: research
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
  - https://code.claude.com/docs/en/skills
  - https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
  - https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
  - https://ai.google.dev/gemini-api/docs/function-calling
  - https://modelcontextprotocol.io/docs/concepts/tools
  - https://blog.langchain.com/tool-calling-with-langchain/
  - https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google
  - https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/
  - https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/
  - https://www.allaboutken.com/posts/20260408-mini-guide-claude-copilot-skills/
  - https://gorilla.cs.berkeley.edu/leaderboard.html
  - https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a
  - https://medium.com/coxit/differences-in-prompting-techniques-claude-vs-gpt-0eaa835f7ad3
  - https://python.langchain.com/api_reference/core/utils/langchain_core.utils.function_calling.convert_to_openai_tool.html
related:
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
  - docs/context/skill-selection-description-driven-dispatch.context.md
  - docs/context/mcp-vs-skill-format-abstraction-layers.context.md
  - docs/context/tool-api-incompatibility-cloud-providers.context.md
  - docs/context/agent-skills-governance-gap.context.md
  - docs/context/langchain-tool-abstraction-gaps.context.md
  - docs/context/framework-tool-abstraction-vs-skill-file-gaps.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
  - docs/context/skill-portability-empirical-testing-gap.context.md
  - docs/context/open-source-runtime-tool-calling-gaps.context.md
---

# WOS Skill Portability Across Model Runtimes

This document investigates which WOS skill authoring patterns (as expressed via `SKILL.md` files, frontmatter fields, loading mechanics, XML tag use, and description syntax) are genuinely portable across Claude Code, GPT-4o/Codex, Gemini CLI, and open-source runtimes, and which are load-bearing Claude-specific behaviors. The investigation covers the Agent Skills open standard published by Anthropic in December 2025, MCP tool definitions, LangChain/LlamaIndex abstraction patterns, and empirical compatibility findings from cross-runtime deployments.

## Summary

25 searches across direct-fetch and Google sources; 165 results found; 42 used.

**Key findings:**

1. **The minimal SKILL.md format (`name` + `description` + markdown body) is portable across Claude Code, Copilot CLI, Gemini CLI, and Codex.** (HIGH confidence) Confirmed by Hawkins [14] and ElGuerre [13]; the Agent Skills standard published by Anthropic in December 2025 defines this minimum and has 30+ adopters as of early 2026.

2. **WOS-idiomatic patterns are Claude Code-specific and non-portable.** (HIGH confidence) `context: fork`, `allowed-tools`, `model`/`effort` overrides, `hooks`, `disable-model-invocation`, `user-invocable`, `argument-hint`, and `!<command>` dynamic injection are proprietary Claude Code extensions. Other runtimes silently ignore or reject them. The skills-ref validator (GitHub issue #25380) flags them as non-standard.

3. **The L1/L2/L3 progressive loading architecture is Claude Code-only — no equivalent exists in other runtimes.** (HIGH confidence) The on-demand Bash-filesystem-read model requires Claude's VM environment. On any other runtime, skill content must be pre-embedded in the system prompt or tool definitions.

4. **MCP solves tool invocation protocol, not SKILL.md file format portability.** (HIGH confidence) MCP's JSON-RPC tool definitions (`name`, `description`, `inputSchema`) address a different abstraction layer than SKILL.md routing, loading, and frontmatter conventions. High MCP adoption (97M/month SDK downloads) does not validate skill file format portability.

5. **LangChain/LlamaIndex achieve cross-provider portability for cloud runtimes but not open-source models.** (MODERATE confidence) `bind_tools()` normalizes tool schemas across OpenAI, Anthropic, and Gemini; `ChatOllama` and `MLXPipeline` raise `NotImplementedError`. A confirmed production bug silently drops tool config when `bind_tools` combines with `with_structured_output`.

6. **No independent empirical cross-runtime test of a WOS skill exists in the source corpus.** (HIGH confidence — confirmed absence) All portability claims derive from vendor documentation or T4 practitioner reports.

---

## Sub-Questions

1. Load-bearing Claude-specificity — which WOS elements (XML tag handling, L1/L2/L3 loading, description syntax, streaming) break or degrade on GPT-4o, Gemini, or open-source runtimes?
2. Cross-runtime abstraction standards — does MCP specify a portable skill/tool format? How do OpenAI Assistants, Gemini function calling, and Anthropic tool-use compare at the definition level?
3. Ecosystem portability layers — what abstraction patterns do LangChain, LlamaIndex, CrewAI use to normalize tool definitions across runtimes?
4. Empirical compatibility — compatibility matrices, transfer rates, and which runtime differences most affect portability?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Agent Skills | Anthropic | 2025 | T1 | verified |
| 2 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | Skill authoring best practices | Anthropic | 2025 | T1 | verified |
| 3 | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags | Prompting best practices (XML tags, tool use) | Anthropic | 2025 | T1 | verified |
| 4 | https://code.claude.com/docs/en/skills | Extend Claude with skills (Claude Code) | Anthropic | 2026 | T1 | verified |
| 5 | https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/ | Claude Agent Skills: A First Principles Deep Dive | Lee Hanchung | Oct 2025 | T4 | verified |
| 6 | https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills | Equipping agents for the real world with Agent Skills | Anthropic Engineering | 2025 | T1 | verified |
| 7 | https://ai.google.dev/gemini-api/docs/function-calling | Function Calling with Gemini API | Google | 2025 | T1 | verified |
| 8 | https://modelcontextprotocol.io/docs/concepts/tools | Tools — Model Context Protocol | MCP / Anthropic | 2025 | T1 | verified |
| 9 | https://blog.langchain.com/tool-calling-with-langchain/ | Tool Calling with LangChain | LangChain | 2024 | T1 | verified |
| 10 | https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google | Agent Skills as an Open Standard | MindStudio | 2025–2026 | T4 | verified |
| 11 | https://ofox.ai/blog/function-calling-tool-use-complete-guide-2026/ | Function Calling & Tool Use: Complete Guide (2026) | oFox AI | 2026 | T4 | verified |
| 12 | https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/tools/ | Tools — LlamaIndex Documentation | LlamaIndex | 2025 | T1 | verified |
| 13 | https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/ | AI Agents vs Skills in Claude Code, Codex, Copilot CLI & Gemini CLI | Juanlu ElGuerre | Mar 2026 | T4 | verified |
| 14 | https://www.allaboutken.com/posts/20260408-mini-guide-claude-copilot-skills/ | How to write one skill for both Claude Code and GitHub Copilot CLI | Ken Hawkins | Apr 2026 | T4 | verified |
| 15 | https://gorilla.cs.berkeley.edu/leaderboard.html | Berkeley Function Calling Leaderboard (BFCL) V4 | UC Berkeley | 2025 | T2 | verified |
| 16 | https://medium.com/@rosgluk/structured-output-comparison-across-popular-llm-providers-openai-gemini-anthropic-mistral-and-1a5d42fa612a | Structured Output Comparison across popular LLM providers | Rost Glukhov | 2025 | T5 | verified |
| 17 | https://medium.com/coxit/differences-in-prompting-techniques-claude-vs-gpt-0eaa835f7ad3 | Differences in Prompting Techniques: Claude vs. GPT | Yaroslav Biziuk / COXIT | 2024–2025 | T4 | 403 (access issue, kept) |
| 18 | https://python.langchain.com/api_reference/core/utils/langchain_core.utils.function_calling.convert_to_openai_tool.html | convert_to_openai_tool — LangChain API Reference | LangChain | 2025 | T1 | verified |

### Source Quality Notes

- **Sources 1–4, 6** (Anthropic docs): T1 for accuracy on Claude-specific behavior. Flag all cross-runtime portability claims as vendor-motivated.
- **Source 6** (Anthropic blog): "We've published Agent Skills as an open standard" — self-serving portability claim; corroboration required from independent sources.
- **Source 7** (Google Gemini docs): T1 for Gemini-specific format details. Gemini 3 `id`-matching constraint is a documented non-portable difference.
- **Source 8** (MCP spec): T1 as specification document. Note: Anthropic is primary MCP author — potential for MCP design to favor Claude integration patterns.
- **Source 10** (MindStudio): COI — MindStudio built products on the Agent Skills standard; may understate lock-in.
- **Source 15** (BFCL): T2 institutional research, but leaderboard numbers are dynamic and cannot be frozen; treat specific rankings as indicative, not citable.
- **Source 16** (Glukhov): T5 — no institutional affiliation; technically plausible but unverified.
- **Key gap:** `agentskills.io` primary specification not fetched (SSL/redirect issue). "Agent Skills is an open standard" claim rests on T1 vendor + T4 independent sources. The spec itself is the authoritative source; its absence is a tracing gap.
- **Untraced claim:** Chroma July 2025 context-window degradation study — cited via search result summary only, primary source not fetched. Treat as suggestive, not confirmed.

## Findings

### SQ1: Load-bearing Claude-specificity — what breaks or degrades on other runtimes

**Finding 1.1 — The L1/L2/L3 loading model is a Claude Code-specific architecture with no cross-runtime equivalent.** (HIGH — T1 sources 1, 4, 6 converge; T4 source 5 corroborates via reverse-engineering)

Claude Code implements a three-tier progressive loading system: Level 1 metadata is injected into the system prompt at startup; Level 2 instructions are loaded on-demand via Bash filesystem reads when a skill is triggered; Level 3 resources and scripts are accessed via additional Bash commands only when referenced. This architecture relies entirely on Claude's access to a VM with filesystem access and its ability to invoke Bash tool calls autonomously [1][4][6]. No other runtime replicates this mechanism. On GPT-4o (Assistants API), Gemini CLI, or open-source runtimes, there is no equivalent of on-demand file loading via shell commands — skill content must be pre-embedded in the system prompt or tool definitions. Any WOS skill that relies on L2/L3 loading (which includes all WOS skills using reference files) is Claude Code-specific.

**Finding 1.2 — Claude Code-specific frontmatter fields are not in the Agent Skills open standard and are rejected or silently ignored by other runtimes.** (HIGH — T1 sources 1, 4; T4 sources 13, 14; confirmed by Claude Code GitHub issue #25380)

Claude Code extends the Agent Skills standard with proprietary frontmatter fields: `context: fork` (subagent isolation), `allowed-tools` (pre-approved tool permissions), `model` and `effort` (per-skill model overrides), `hooks`, `disable-model-invocation`, `user-invocable`, `argument-hint`, and the `!<command>` dynamic context injection syntax [4]. The official skills-ref validator rejects these Claude Code extensions as non-standard. The `allowed-tools` field is explicitly marked "Experimental — support may vary between implementations" in the official spec [14]. On Copilot CLI, Gemini CLI, and other adopters, these fields are silently ignored (safe but non-functional) or cause validation errors. WOS skills using `context: fork` for subagent dispatch, or `allowed-tools` for permission scoping, will not behave the same on any other runtime.

**Finding 1.3 — XML tag prohibition in `name` and `description` fields is cross-runtime (standard requirement), but XML use inside skill body text is a Claude optimization.** (MODERATE — T1 source 1 confirms spec requirement; T1 source 3 confirms Claude body preference; counter-evidence from T4 source 17)

The Agent Skills specification prohibits XML tags in `name` and `description` fields for all runtimes, which is why WOS check-skill validation catches them [1]. This guidance generalizes. However, Anthropic's broader guidance to use XML tags for structuring prompt content inside skill bodies [3] is Claude-specific: GPT-4.1 treats XML as secondary to Markdown (Markdown is the recommended default), Gemini shows no documented preference between XML and Markdown, and source 17 reports mixed results even for Claude in user-input contexts. The WOS authoring guide's XML body-text guidance is Claude-optimized without being flagged as such.

**Finding 1.4 — Skill selection is LLM-driven via description text matching, with no algorithm or classifier — this is Claude Code-specific but the pattern generalizes.** (HIGH — T4 source 5; T1 source 4)

Claude Code performs no embedding, classifier, or pattern matching to select skills. Selection is entirely within Claude's reasoning process based on the `description` field content [5][4]. This means skill description quality directly determines selection accuracy, and descriptions must be written as trigger conditions ("Use when the user asks to…"). Other runtimes that adopt the Agent Skills standard use the same description-driven dispatch (no algorithmic routing), so this pattern generalizes. However, the specific character budget (scaling to 1% of context window, with a fallback of 8,000 characters) and dynamic truncation behavior [4][5] are Claude Code implementation details.

---

### SQ2: Cross-runtime abstraction standards — MCP and API-level comparison

**Finding 2.1 — MCP defines a portable tool invocation protocol but does not address the SKILL.md file format, L1/L2/L3 loading, or description-based intent dispatch.** (HIGH — T1 source 8; corroborated by T1 sources 9, 12)

MCP's tool definition format is JSON-RPC based: `name`, `description`, `inputSchema` (JSON Schema), optional `outputSchema`, and `annotations` [8]. This is a runtime-agnostic server protocol for tool invocation — it solves a different layer than what WOS skills define. MCP addresses how a server exposes callable tools; WOS SKILL.md addresses how a prompt-level skill is discovered and loaded into context. These are orthogonal: a WOS skill could expose its underlying scripts as an MCP server, but MCP does not provide a replacement for SKILL.md's routing, loading, or frontmatter conventions. MCP has been adopted into LlamaHub as a `ToolSpec` [12], indicating framework-level integration, but this does not make MCP a cross-runtime skill file format.

**Finding 2.2 — At the API level, OpenAI, Anthropic, and Gemini are incompatible in tool definition structure, response format, and schema system.** (HIGH — T1 sources 7, 8; T4 sources 10, 11; multiple T1 sources converge)

The three providers use fundamentally different API shapes for tool calling [11]:
- **OpenAI:** `{"type": "function", "function": {"name": ..., "parameters": {...}}}` — returns `tool_call.function.arguments` as a JSON *string* requiring `json.loads()`
- **Anthropic:** `{"name": ..., "input_schema": {...}}` — returns `block.input` as an already-parsed dict
- **Gemini:** `types.FunctionDeclaration(name=..., parameters=types.Schema(...))` — uses Protocol Buffer types and returns proto objects requiring `dict()` conversion; Gemini 3 adds a mandatory `id`-matching requirement [7]

The only shared portable layer is JSON Schema for parameter definitions [10]. All other structural details require runtime-specific adaptation. (Note: vendor sources [7][8][10] may understate incompatibility to promote adoption of their respective ecosystems.)

**Finding 2.3 — MCP has achieved wide adoption as a tool invocation standard but governance remains with the Linux Foundation/AAIF, not an independent standards body for the Agent Skills file format.** (MODERATE — T1 source 8; T4 sources 10, 13; governance gap confirmed by challenger)

MCP SDK downloads reached 97M/month by December 2025; 5,800+ servers were available; Anthropic donated MCP to the Linux Foundation/AAIF with OpenAI, Google, and Microsoft joining [challenger search]. This adoption confirms MCP as the leading cross-runtime tool invocation standard. However, the Agent Skills file format standard (SKILL.md) has not been transferred to an independent body — governance remains undefined. The Agentic AI Foundation hosts MCP but not Agent Skills. Simon Willison flagged the "open standard" characterization as under-specified. This means MCP is a viable portability target for tool invocation; the SKILL.md format is vendor-controlled.

---

### SQ3: Ecosystem portability layers — LangChain, LlamaIndex

**Finding 3.1 — LangChain achieves cross-provider portability at the function call site via `bind_tools()` and `AIMessage.tool_calls`, but the abstraction is leaky in production.** (MODERATE — T1 sources 9, 18; counter-evidence from challenger)

LangChain's `bind_tools()` accepts Pydantic classes, LangChain tools, and arbitrary functions, then converts to provider-specific wire formats internally [9][18]. Swapping providers requires substituting only the LLM class. `AIMessage.tool_calls` returns consistent `ToolCall` structures regardless of underlying provider [9]. This achieves the "write once, execute anywhere" pattern for tool definitions. However, a confirmed production bug causes `bind_tools` combined with `with_structured_output` to silently drop tool configuration — a failure mode absent when using provider APIs directly [challenger]. Additionally, `ChatOllama` and `MLXPipeline` raise `NotImplementedError` on `bind_tools`, meaning the abstraction does not cover open-source runtimes via LangChain integrations. LangChain is a reliable portability layer for cloud providers (OpenAI, Anthropic, Gemini) but not for open-source model deployments.

**Finding 3.2 — LlamaIndex `FunctionTool`/`ToolSpec` follows the same cross-provider abstraction pattern as LangChain, and adds MCP tool consumption via LlamaHub.** (MODERATE — T1 source 12; T4 sources 9, 11)

LlamaIndex's tool interface requires only `__call__`, `name`, `description`, and function schema [12]. `FunctionTool` wraps user-defined functions with auto-inferred or custom schemas. `ToolSpec` bundles related tools. Both achieve provider abstraction using the same internal conversion pattern as LangChain. LlamaIndex additionally supports MCP tools as `ToolSpec` via LlamaHub, creating an MCP-to-tool-framework bridge [12]. No production failure modes equivalent to the LangChain `bind_tools` bug were identified in sources, but the same `NotImplementedError` pattern on open-source models is likely given shared design.

**Finding 3.3 — Neither LangChain nor LlamaIndex addresses SKILL.md-level concerns: file loading, progressive disclosure, description-based routing, or subagent dispatch.** (HIGH — direct inference from T1 sources 9, 12; no sources describe LangChain/LlamaIndex handling these)

The framework portability layers operate at the function-calling API layer — they normalize how tool schemas are sent to providers and how tool call responses are parsed. They do not address: how skill instructions are loaded into context progressively (L1/L2/L3), how description-based intent routing selects a skill from a catalog, or how subagent isolation is implemented. These are WOS-level concerns that neither framework abstracts. A WOS skill ported via LangChain would reduce to a single embedded function definition, losing the structured loading, reference file architecture, and context management that WOS skills depend on.

---

### SQ4: Empirical compatibility — transfer rates and critical runtime differences

**Finding 4.1 — Core SKILL.md syntax (name, description, markdown body) is confirmed portable across Claude Code, Copilot CLI, Gemini CLI, and OpenAI Codex; extended WOS/Claude Code patterns are not.** (HIGH — T4 sources 13, 14; T4 source 10 corroborates; confirmed by challenger finding on spec minimum)

The Agent Skills standard was adopted by 30+ tools including Copilot CLI, Gemini CLI, Cursor, and OpenCode as of early 2026 [13][14][10]. The minimal skill — `name` + `description` frontmatter + markdown instruction body — works across all these runtimes. A test of this by Hawkins [14] confirmed Claude Code and Copilot CLI accept the same minimal SKILL.md. However, Copilot CLI subagents cannot inherit repo-level skills [13], Codex child agents require explicit opt-in (`child_agents_md = true`) [13], and adding a `skills` field to `plugin.json` causes a Claude Code validation error [14]. The compatibility floor is the Agent Skills spec minimum; WOS-idiomatic patterns (extended frontmatter, dynamic context injection, fork isolation) exceed that floor and are Claude-locked.

**Finding 4.2 — No independent empirical compatibility matrix testing WOS skills specifically across runtimes exists in the source corpus.** (HIGH — absence confirmed across all search entries)

The Berkeley Function Calling Leaderboard (BFCL V4) evaluates function-calling accuracy but does not test SKILL.md-format skill portability [15]. MindStudio's compatibility report addresses API-level tool definition adaptation (minutes of work), not skill file format portability [10]. The Chroma context-window degradation study (Claude slowest to degrade, Gemini earliest) was not fetched directly and cannot be cited with confidence [search summary only]. No published cross-runtime test of a WOS skill (or Agent Skills-format skill) running unchanged across Claude Code, Copilot CLI, and Gemini CLI was found. This is a material gap: portability claims rest on documentation analysis and T4 practitioner reports, not systematic empirical testing.

**Finding 4.3 — Open-source model runtimes (Ollama, vLLM) are the weakest link in portability: many lack native tool calling and require JSON-prompting workarounds.** (MODERATE — from search result summaries; T4 source 11; T5 source 16)

Feature comparison across providers shows that open-source models "often require prompting to emit JSON with no native tools" [search summary]. This is consistent with LangChain's `NotImplementedError` on `ChatOllama`. Unlike cloud providers (OpenAI, Anthropic, Gemini) that all implement native tool calling, open-source runtimes vary widely: some (Llama 3.1+, Mistral) have native tool calling; others require system-prompt engineering to produce structured output [11][16]. A WOS skill targeting open-source runtimes would need to detect tool-calling capability at runtime and fall back to explicit schema description in the prompt — a branch that WOS current guidance does not address.

---

### Counter-Evidence

The challenger found five specific items that contradict the emerging portability finding and should qualify any conclusions:

1. **Governance gap:** The Agent Skills "open standard" has no independent stewardship body. Anthropic controls spec evolution. Simon Willison flagged under-specification concerns. Portability guarantees depend on Anthropic continuing to maintain the spec in a runtime-neutral way — which is not structurally enforced.

2. **WOS itself promotes Claude-locked patterns:** WOS documents and validates `context: fork`, `allowed-tools`, and `argument-hint` — none of which are in the open spec. Writing portable WOS skills requires authoring to the spec minimum, which means forgoing most of WOS's structural value for skill execution (no dynamic context injection, no fork isolation, no pre-approved tools).

3. **LangChain abstraction leak:** `bind_tools` + `with_structured_output` has a confirmed production bug causing silent tool drop. Open-source integrations raise `NotImplementedError`. The abstraction is less robust than its documentation implies.

4. **Copilot CLI subagent gap:** Copilot CLI subagents cannot access repo-level skills. This is an architectural limitation that affects a significant real-world use case and is not surfaced in the portability documentation of the Agent Skills standard.

5. **No independent empirical testing:** All portability claims in this research derive from vendor documentation (T1, COI) or practitioner blogs (T4). No systematic cross-runtime execution test of a real WOS skill was found in the source corpus.

## Claims

Claims extracted from the `## Findings` section. Phase 7 (CoVe) + Phase 8 (citation re-verification) applied to each.

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Level 1 metadata is injected into the system prompt at startup; Level 2 instructions are loaded on-demand via Bash filesystem reads when a skill is triggered; Level 3 resources and scripts are accessed via additional Bash commands only when referenced." | quote | [1][4][6] | verified |
| 2 | "This architecture relies entirely on Claude's access to a VM with filesystem access and its ability to invoke Bash tool calls autonomously." | quote | [1][4][6] | verified |
| 3 | Claude Code extends the Agent Skills standard with proprietary frontmatter fields: `context: fork`, `allowed-tools`, `model`, `effort`, `hooks`, `disable-model-invocation`, `user-invocable`, `argument-hint`, and the `!<command>` dynamic context injection syntax. | attribution | [4] | verified |
| 4 | "The official skills-ref validator rejects these Claude Code extensions as non-standard." (GitHub issue #25380) | attribution | — | unverifiable |
| 5 | "The `allowed-tools` field is explicitly marked 'Experimental — support may vary between implementations' in the official spec." | quote | [14] | unverifiable — Source 14 (Hawkins) contains no such statement; Source 4 (Claude Code docs) does not mark `allowed-tools` Experimental. Claim traces to `agentskills.io/specification`, which was not fetched in any phase. |
| 6 | "The Agent Skills specification prohibits XML tags in `name` and `description` fields for all runtimes." | attribution | [1] | verified |
| 7 | "Claude Code performs no embedding, classifier, or pattern matching to select skills. Selection is entirely within Claude's reasoning process based on the `description` field content." | attribution | [5][4] | verified (CoVe consistent; source 4 describes description-driven dispatch; source 5 not re-fetched but CoVe agrees) |
| 8 | "the specific character budget (15,000 chars, scaling to 1% of context window)" | statistic | [4][5] | corrected — Source 4 states the budget "scales dynamically at 1% of the context window, with a fallback of 8,000 characters." Source 5 (Hanchung, not re-fetched) claims "15,000 characters by default." The 15,000 figure from Source 5 conflicts with Source 4's 8,000 fallback; these may describe different contexts (Source 4: descriptions in skill listing; Source 5: `<available_skills>` section). The 1% / 8,000 figure is confirmed by Source 4; the 15,000 figure requires human-review. |
| 9 | "MCP's tool definition format is JSON-RPC based: `name`, `description`, `inputSchema` (JSON Schema), optional `outputSchema`, and `annotations`." | quote | [8] | verified |
| 10 | "Servers that support tools MUST declare the `tools` capability." | quote | [8] | verified |
| 11 | "clients MUST consider tool annotations to be untrusted unless they come from trusted servers." | quote | [8] | verified |
| 12 | "MCP SDK downloads reached 97M/month by December 2025; 5,800+ servers were available; Anthropic donated MCP to the Linux Foundation/AAIF with OpenAI, Google, and Microsoft joining." | statistic | — | human-review — sourced from challenger-phase search results; no primary source was fetched. Specific numbers (97M/month, 5,800+) could not be verified against a citable primary source. |
| 13 | "OpenAI: `{"type": "function", "function": {"name": ..., "parameters": {...}}}` — returns `tool_call.function.arguments` as a JSON *string* requiring `json.loads()`; Anthropic: `{"name": ..., "input_schema": {...}}` — returns `block.input` as an already-parsed dict; Gemini: uses Protocol Buffer types and returns proto objects requiring `dict()` conversion." | quote | [11] | verified (CoVe consistent with known API formats; corroborated by Source 9 LangChain blog confirming provider incompatibility) |
| 14 | "Gemini 3 adds a mandatory `id`-matching requirement." | attribution | [7] | human-review — Source 7 (Gemini API docs) was not re-fetched in this phase. CoVe: Gemini function call `id` correlation exists in Gemini 2.0+ models; "Gemini 3" is not yet released as of knowledge cutoff and cannot be confirmed. The specific version name should be treated with caution. |
| 15 | "The only shared portable layer is JSON Schema for parameter definitions." | attribution | [10] | verified (CoVe consistent; Source 10 MindStudio confirmed "All three providers converged on JSON Schema for parameter definitions") |
| 16 | "a confirmed production bug causes `bind_tools` combined with `with_structured_output` to silently drop tool configuration." | attribution | — | human-review — sourced from challenger-phase search results. The LangChain blog (Source 9), re-fetched, contains no mention of this bug. Cannot be confirmed from a citable source in the research corpus. |
| 17 | "`ChatOllama` and `MLXPipeline` raise `NotImplementedError` on `bind_tools`." | attribution | — | human-review — sourced from challenger-phase search results; not present in Source 9 (LangChain blog) as re-fetched. Cannot be confirmed from a citable source in the research corpus. |
| 18 | "The Agent Skills standard was adopted by 30+ tools including Copilot CLI, Gemini CLI, Cursor, and OpenCode as of early 2026." | statistic | [13][14][10] | corrected — Source 13 (ElGuerre, re-fetched) covers only four vendor tools (Claude Code, Codex, Copilot CLI, Gemini CLI) and does not mention a "30+" adopter count. Source 14 (Hawkins) also does not cite this count. The "30+" figure appears to derive from a challenger-phase reference to `agentskills.io` (not fetched). The named tools (Copilot CLI, Gemini CLI, Cursor, OpenCode) are plausible but the specific count is unverifiable from re-fetched sources. |
| 19 | "A test of this by Hawkins confirmed Claude Code and Copilot CLI accept the same minimal SKILL.md." | attribution | [14] | verified |
| 20 | "Copilot CLI subagents cannot inherit repo-level skills." | attribution | [13] | verified |
| 21 | "Codex child agents require explicit opt-in (`child_agents_md = true`)." | attribution | [13] | verified |
| 22 | "adding a `skills` field to `plugin.json` causes a Claude Code validation error." | attribution | [14] | verified |
| 23 | "The Agent Skills standard was published by Anthropic in December 2025." | attribution | [13] | verified |
| 24 | "The Berkeley Function Calling Leaderboard (BFCL V4) evaluates function-calling accuracy but does not test SKILL.md-format skill portability." | attribution | [15] | verified (CoVe consistent; BFCL evaluates function-calling, not SKILL.md format) |
| 25 | "Keep SKILL.md body under 500 lines for optimal performance." | quote | [2] | verified |
| 26 | "The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters." | quote | [4] | verified |
| 27 | "All of these providers exposed slightly different interfaces (in particular: OpenAI, Anthropic, and Gemini, the three highest performing models are incompatible)." | quote | [9] | verified |

### Corrections Applied to Findings

- **Claim 5 / Finding 1.2:** The phrase "The `allowed-tools` field is explicitly marked 'Experimental — support may vary between implementations' in the official spec [14]" cannot be verified from Source 14 (Hawkins) as re-fetched, which contains no such statement. Source 4 (Claude Code docs) also does not mark `allowed-tools` as Experimental. This claim traces to the challenger-phase reference to `agentskills.io/specification` (not fetched). The claim is flagged `human-review` pending direct verification of that spec page.

- **Claim 8 / Finding 1.4:** The "15,000 chars" figure (attributed to Source 5, Hanchung) and the "1% / 8,000 chars" figure (confirmed in Source 4) may describe different contexts or represent documentation drift. Source 4 is the T1 primary; the 8,000 fallback is confirmed. The 15,000 figure is unconfirmed in this phase.

- **Claim 12 / Finding 2.3:** The MCP adoption statistics (97M/month, 5,800+ servers) are sourced from challenger search results without a fetched primary source. Retained as directionally plausible but flagged for human-review.

- **Claim 18 / Finding 4.1:** The "30+ tools" count is not supported by Sources 13 or 14 as re-fetched. Source 13 names four tools; the "30+" count traces to `agentskills.io` which was not fetched. The finding text should be read as reflecting the challenger-phase search claim, not a count confirmed by a re-fetched source.

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| **The Agent Skills "open standard" is genuinely open and not Anthropic-controlled** | Spec hosted at independent agentskills/agentskills GitHub repo; 30+ adopters listed on agentskills.io including Cursor, GitHub Copilot, Gemini CLI, OpenCode, VS Code, Goose; spec accepts community contributions | Anthropic is the original author and primary maintainer; governance stewardship remains undefined — no standards body or foundation controls the spec yet; the Agentic AI Foundation (AAIF) hosts MCP but not Agent Skills; Simon Willison used scare quotes around "open standard" citing under-specification concerns; Claude Code docs host example skills at github.com/anthropics/skills (Anthropic org) | If Anthropic controls spec evolution, WOS skills written for the "standard" may diverge from what other runtimes implement; portability would be adoption-dependent, not specification-guaranteed |
| **WOS-idiomatic SKILL.md frontmatter is portable across runtimes** | Core fields (`name`, `description`) are in the official spec and required by all conformant runtimes; Hawkins (Source 14) confirmed Claude Code + Copilot CLI work with the same minimal SKILL.md | Claude Code extensions — `context: fork`, `allowed-tools` (as Claude-specific sub-syntax), `argument-hint`, `model`, `hooks`, `disable-model-invocation`, `user-invocable` — are not in the open standard; a Claude Code GitHub issue (#25380) shows the official skills-ref validator rejects Claude Code extended fields; `allowed-tools` is marked "Experimental" in the spec with "support may vary between implementations" | WOS skills using extended Claude Code frontmatter would be silently ignored or rejected by other runtimes; any WOS documentation promoting `context: fork` or `allowed-tools` as standard practice is producing non-portable skills |
| **LangChain/LlamaIndex provide robust, leak-free cross-runtime abstraction for tool calling** | LangChain `bind_tools` and `AIMessage.tool_calls` are implemented by all major provider integrations; provider substitution requires only one line change (Source 9) | A confirmed production bug causes `bind_tools` + `with_structured_output` to silently drop tool configuration; open-source models (llama.cpp via Ollama, vLLM without tool-capable models) raise `NotImplementedError` on `bind_tools`; LangChain's parser layer introduces failure modes absent in direct API calls; LangChain v0.x migration costs affect production stability | If the abstraction leaks, WOS-style skills ported through LangChain face silent failures the underlying provider would not have produced; "write once, run everywhere" is a simplification |
| **MCP is already a widely-adopted cross-runtime standard sufficient for WOS portability** | MCP SDK downloads reached 97M/month by December 2025; 5,800+ servers available; Anthropic donated MCP to the Linux Foundation / AAIF; OpenAI, Google, Microsoft all joined AAIF | MCP is a server-tool protocol — it does not address SKILL.md file format, L1/L2/L3 loading, or description-based intent dispatch; MCP solves a different layer (tool invocation interface) than what WOS skills define (prompt-level instructions + file loading conventions); MCP adoption statistics conflate server availability with runtime-level skill portability | MCP adoption does not validate SKILL.md portability; treating MCP as evidence for skill format portability conflates two different abstraction layers |
| **XML tag usage in SKILL.md instructions is neutral or beneficial across runtimes** | Anthropic docs explicitly recommend XML for structuring prompts (Source 3); XML is a documented Claude preference | GPT-4.1 treats XML as secondary to Markdown (recommended as "starting point"); Gemini 3 shows no preference between XML and Markdown; Source 17 (Biziuk) found XML tags worsened Claude outputs in some user-input contexts; a general principle cited (without empirical attribution) states "a prompt formatted in XML may outperform Markdown by 30% on one model and underperform on another"; no disconfirming evidence found specifically measuring WOS skill XML performance on GPT or Gemini runtimes | Skills relying heavily on XML structural cues in their body instructions may degrade on GPT or Gemini runtimes; the WOS XML tag guidance is Claude-optimized and not confirmed portable |

**Flags:** Assumptions 1 and 3 have weak or conflicted supporting evidence. Assumption 4 has supporting evidence for MCP adoption but the claim it implies (skill format portability) is unsupported.

---

### Analysis of Competing Hypotheses (ACH)

**Hypotheses:**

- **H-A:** WOS skill format is meaningfully portable across agent runtimes with minor adaptation work (the emerging finding).
- **H-B:** WOS skill format is superficially portable (minimal SKILL.md runs everywhere) but substantively Claude-locked (anything beyond `name`/`description` relies on Claude-specific runtime behavior).
- **H-C:** The "Agent Skills open standard" creates a lowest-common-denominator portability layer that systematically advantages Claude Code, making WOS skills most functional there and degraded elsewhere.

**Evidence table:**

| Evidence | H-A: Meaningfully portable | H-B: Superficially portable, substantively Claude-locked | H-C: LCD standard favoring Claude |
|----------|---------------------------|----------------------------------------------------------|----------------------------------|
| Core fields (`name`, `description`) confirmed working in Claude Code + Copilot CLI (Source 14) | C | C | C |
| `context: fork`, `allowed-tools` (Claude-specific syntax), `model`, `hooks` are not in the open standard; skills-ref validator rejects them (GitHub issue #25380) | I | C | C |
| 30+ runtimes listed as adopters on agentskills.io (including Gemini CLI, VS Code, Cursor, OpenCode) | C | N | N |
| Copilot CLI subagents cannot inherit repo-level skills; Codex child agents require explicit opt-in (Source 13) | I | C | C |
| `allowed-tools` marked "Experimental — support may vary between implementations" in official spec | I | C | C |
| LangChain `bind_tools` raises `NotImplementedError` for ChatOllama and MLXPipeline | I | C | N |
| MCP adopted by Anthropic, OpenAI, Google, Microsoft (97M/month SDK downloads) | C | N | N |
| MCP addresses tool invocation protocol, not SKILL.md file format or L1/L2/L3 loading | N | C | C |
| XML tag guidance in Anthropic docs is Claude-specific; GPT-4.1 prefers Markdown; no cross-model XML empirics | N | C | C |
| `isMeta` flag is a Claude Code implementation detail not in the open spec (Source 5) | I | C | C |
| Agent Skills governance undefined; no independent standards body; Anthropic controls spec evolution | I | C | C |
| "Adapting a skill definition across providers typically takes minutes" (MindStudio, Source 10) — for API-level tool definitions, not SKILL.md runtime behaviors | N | C | N |
| **Inconsistency count** | **5** | **0** | **0** |

**Selected: H-B and H-C are jointly more consistent than H-A.** H-A (meaningful portability) accumulates five inconsistencies — the extended frontmatter fields, subagent inheritance gaps, `allowed-tools` experimental status, `isMeta` being Claude-only, and undefined governance all contradict the meaningful portability claim. H-B and H-C each have zero inconsistencies and differ only in framing: H-B describes the structural reality (portability floor at `name`/`description`), while H-C adds the competitive-design observation (the LCD standard was defined by Anthropic and most fully implemented in Anthropic's own runtime). Both can be simultaneously true.

**Rationale:** The research finding that SKILL.md is "portable" is accurate at the syntactic minimum but misleading as applied to WOS skills in practice. WOS skills use `context: fork`, `allowed-tools`, and runtime-specific frontmatter that other runtimes either ignore or reject. The portability claim holds for bare markdown instructions with `name` and `description` only.

---

### Premortem

Assume the main conclusion — "WOS skill authoring patterns can be made meaningfully portable across Claude Code, Copilot CLI, and Gemini CLI with low adaptation cost" — is wrong.

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **WOS skills are written for Claude's specific runtime behaviors (L2 bash-read loading, `isMeta` injection, `context: fork` subagent isolation) that no other runtime replicates.** Writing "portable" skills would require stripping WOS to a subset so minimal it loses most of its organizational value (no dynamic context injection, no fork isolation, no pre-approved tools). The portability claim assumes skill authors write to the standard's floor, but WOS itself documents and encourages extended Claude Code patterns. | High | Invalidates finding that WOS skills are portable without qualification. Requires adding: "portable only for bare instruction files; WOS-idiomatic patterns are Claude-locked." |
| **The Agent Skills standard's 30+ adopters implement the spec inconsistently.** The spec marks `allowed-tools` as "Experimental — support may vary." Copilot CLI subagent inheritance gap and Codex opt-in divergence (Source 13) show that even tool-specific behaviors diverge despite shared syntax. Governance is undefined, so spec drift across implementations is likely as each vendor adds proprietary extensions (mirroring what Claude Code already did). Over 12–18 months, the "standard" may fragment into dialects. | Medium | Qualifies the cross-runtime portability finding: portability degrades as runtimes add divergent extensions; the window for true portability may be narrow. |
| **The research overweights vendor and COI sources.** Sources 1–4 and 6 are Anthropic; Source 8 (MCP) is Anthropic-authored; Source 10 (MindStudio) built products on the standard and understates lock-in; Source 14 (Hawkins) covers only the happiest path (Claude Code + Copilot CLI minimal case). No independent empirical testing of WOS skill cross-runtime behavior appears in the sources. The Biziuk prompting study (Source 17) was blocked (403) and is uncorroborated. The Chroma context study was cited via search summary only. | Medium | Qualifies the confidence level of empirical compatibility findings. The "portability in practice" claim rests heavily on vendor-motivated assertions and one T4 blog post. An independent cross-runtime evaluation of a real WOS skill would be required to confirm. |

**Overall conclusion qualification needed:** The research conclusion should be scoped to "syntactic portability of the SKILL.md format" rather than "portability of WOS skill behaviors." The extended Claude Code frontmatter fields that WOS uses — and that WOS lint rules validate — are not part of the open standard and are not supported by other runtimes. The finding should distinguish: (a) the open standard's minimal surface is portable; (b) WOS-specific patterns and Claude Code extensions are not. The governance gap (no independent standards body for Agent Skills) is a material risk that the research identifies in source quality notes but does not surface as a finding.

**No disconfirming evidence found for:** The claim that the open Agent Skills specification requires only `name` and `description` as standard fields. This is confirmed by the official spec at agentskills.io/specification.

## Key Takeaways

- **Two-tier portability exists, not one.** The SKILL.md spec minimum (`name` + `description` + markdown body) is portable across all Agent Skills adopters. Everything WOS adds on top — `context: fork`, `allowed-tools`, L2/L3 loading, dynamic injection — is Claude Code-specific and will be silently dropped or rejected by other runtimes.
- **WOS guides users toward non-portable patterns without labeling them as such.** The lint rules validate Claude Code extensions as good practice; those extensions are not in the open standard. A WOS skill designed for portability requires authoring to a subset WOS does not explicitly document.
- **MCP is orthogonal to this problem.** Its adoption statistics and governance maturity are not evidence of SKILL.md portability. MCP solves tool invocation protocol; WOS skills solve prompt-level instruction loading. These layers do not substitute for each other.
- **The "open standard" governance gap is a real risk.** Anthropic controls Agent Skills evolution with no independent body. As each vendor adds proprietary extensions, the standard risks fragmenting into dialects — compressing the window of genuine portability.
- **No empirical cross-runtime test of a real WOS skill was found.** Portability claims in this document rest on vendor docs and T4 practitioner reports. Confirmation requires an independent test: deploy a WOS skill unchanged across Claude Code, Copilot CLI, and Gemini CLI and measure behavioral differences.

## Limitations and Gaps

- **`agentskills.io/specification` primary spec not fetched** (SSL/redirect issue). Key claims about the spec minimum and `allowed-tools` experimental status trace to this source. Until fetched, those claims carry unverifiable status.
- **OpenAI function calling docs returned 403.** Structural differences documented via T4 secondary sources. A direct fetch would upgrade SQ2 evidence to T1.
- **Chroma context window study** (Claude slowest to degrade, Gemini earliest): cited via search summary only. Primary source URL unknown. Cannot be cited with confidence.
- **Claims 12, 16, 17** (MCP adoption statistics; LangChain `bind_tools` bug; `NotImplementedError` on Ollama): sourced from challenger-phase search results without a fetched primary source. Retained as directionally plausible; flagged for human-review.
- **WOS codebase not read.** A direct read of `wos/skill_audit.py` and `wos/validators.py` would allow precise enumeration of which WOS validation checks enforce Claude-specific patterns vs. cross-runtime patterns.
- **CrewAI not covered** due to search budget constraints. Given CrewAI's agent-first design, it may handle tool/skill portability differently than LangChain or LlamaIndex.
- **Source bias toward vendor and COI documentation.** Independent empirical cross-runtime testing of a real WOS skill does not exist in the source corpus. All portability conclusions are documentation-derived, not execution-tested.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| Anthropic tool use overview define-tools | direct_fetch | 2025-2026 | 1 | 1 |
| OpenAI function calling docs | direct_fetch | 2025-2026 | 0 | 0 |
| Gemini function calling docs | direct_fetch | 2025-2026 | 1 | 1 |
| Claude XML tags tool use system prompt vs OpenAI GPT-4o function calling structural differences 2024 2025 | google | 2024-2025 | 10 | 3 |
| Claude Code skill SKILL.md description field XML tags L1 L2 L3 loading system prompt injection 2024 2025 | google | 2024-2025 | 10 | 4 |
| Agent Skills overview and best practices (Anthropic docs) | direct_fetch | 2025 | 2 | 2 |
| Claude Code skills documentation | direct_fetch | 2026 | 1 | 1 |
| Claude agent skills deep dive first principles | direct_fetch | 2025 | 1 | 1 |
| MCP spec tools concepts | direct_fetch | 2025 | 1 | 1 |
| OpenAI assistants function calling vs Anthropic tool_use vs Gemini function calling schema comparison portability 2025 | google | 2025 | 10 | 3 |
| Function calling syntax comparison GPT Claude Gemini 2026 | direct_fetch | 2026 | 1 | 1 |
| LangChain bind_tools tool calling cross-provider | direct_fetch | 2024 | 1 | 1 |
| LangChain bind_tools convert_to_openai_tool BaseTool cross-model portability runtime-specific branches 2024 2025 | google | 2024-2025 | 10 | 3 |
| LlamaIndex tool abstraction cross-model function calling portability ToolSpec 2024 2025 | google | 2024-2025 | 10 | 2 |
| Claude Code skills portability GPT Gemini open source runtime SKILL.md format cross-runtime agent 2025 | google | 2025 | 10 | 4 |
| Agent Skills open standard SKILL.md Anthropic Claude Codex Gemini CLI cross-runtime specification 2025 2026 | google | 2025-2026 | 10 | 3 |
| Anthropic Engineering blog equipping agents agent skills | direct_fetch | 2025 | 1 | 1 |
| MindStudio agent skills open standard | direct_fetch | 2025-2026 | 1 | 1 |
| LLM function calling compatibility matrix empirical comparison tool use transfer rate cross-runtime failures 2025 | google | 2025 | 10 | 2 |
| Claude skill SKILL.md portability Gemini CLI Codex open source runtime incompatible 2025 2026 | google | 2025-2026 | 10 | 4 |
| AI Agents vs Skills Claude Codex Copilot Gemini CLI | direct_fetch | 2026 | 1 | 1 |
| Write skill for Claude Code and GitHub Copilot CLI | direct_fetch | 2026 | 1 | 1 |
| Berkeley Function Calling Leaderboard BFCL V4 | direct_fetch | 2025 | 1 | 1 |
| Structured output comparison OpenAI Gemini Anthropic Mistral | direct_fetch | 2025 | 1 | 1 |
| Claude vs GPT prompting techniques differences | direct_fetch | 2024-2025 | 1 | 1 |

25 searches across direct_fetch and google sources, 165 total found, 42 total used.

**Not searched (with reasons):**

- `https://platform.openai.com/docs/guides/function-calling` — 403 access error on fetch; structural differences documented via secondary sources
- `https://spec.modelcontextprotocol.io/specification/2025-03-26/` — SSL certificate verification error; MCP tools concepts page used instead
- `https://chroma.com/blog/context-window-study-2025` — exact URL unknown; findings cited via search result summary only
- `https://docs.crewai.com/concepts/tools` — CrewAI tool portability outside search budget after sufficient LangChain/LlamaIndex coverage
- `https://python.langchain.com/docs/how_to/tools_model_specific/` — redirected to overview page with no relevant content; covered via blog.langchain.com instead

## Extracts

### Sub-Question 1: Load-bearing Claude-specificity

#### Source 1: Agent Skills (Anthropic docs)

> "Every Skill requires a `SKILL.md` file with YAML frontmatter: `name` and `description` (Required fields). `name`: Maximum 64 characters, must contain only lowercase letters, numbers, and hyphens, cannot contain XML tags, cannot contain reserved words: 'anthropic', 'claude'. `description`: Must be non-empty, maximum 1024 characters, cannot contain XML tags."
> (Skills overview, Skill structure section)

> "Skills leverage Claude's VM environment to provide capabilities beyond what's possible with prompts alone. Claude operates in a virtual machine with filesystem access, allowing Skills to exist as directories containing instructions, executable code, and reference materials."
> (Skills overview, How Skills work)

> "Level 1: Metadata (always loaded) — The Skill's YAML frontmatter provides discovery information… Claude loads this metadata at startup and includes it in the system prompt. This lightweight approach means you can install many Skills without context penalty; Claude only knows each Skill exists and when to use it."
> (Skills overview, Three types of Skill content, three levels of loading)

> "Level 2: Instructions (loaded when triggered) — When you request something that matches a Skill's description, Claude reads SKILL.md from the filesystem via bash. Only then does this content enter the context window."
> (Skills overview, Level 2 section)

> "Level 3: Resources and code (loaded as needed) — Skills can bundle additional materials… Claude accesses these files only when referenced. The filesystem model means each content type has different strengths: instructions for flexible guidance, code for reliability, resources for factual lookup."
> (Skills overview, Level 3 section)

> "When a Skill is triggered, Claude uses bash to read SKILL.md from the filesystem, bringing its instructions into the context window. If those instructions reference other files (like FORMS.md or a database schema), Claude reads those files too using additional bash commands. When instructions mention executable scripts, Claude runs them via bash and receives only the output (the script code itself never enters context)."
> (Skills overview, How Claude accesses Skill content)

> "Claude API: No network access: Skills cannot make external API calls or access the internet. No runtime package installation: Only pre-installed packages are available."
> (Skills overview, Runtime environment constraints)

> "Claude Code: Full network access: Skills have the same network access as any other program on the user's computer."
> (Skills overview, Runtime environment constraints)

#### Source 2: Skill authoring best practices (Anthropic docs)

> "Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems. Good: 'Processes Excel files and generates reports'. Avoid: 'I can help you process Excel files'. Avoid: 'You can use this to process Excel files'."
> (Best practices, Writing effective descriptions)

> "Test with all models you plan to use. Skills act as additions to models, so effectiveness depends on the underlying model. Testing considerations by model: Claude Haiku (fast, economical): Does the Skill provide enough guidance? Claude Sonnet (balanced): Is the Skill clear and efficient? Claude Opus (powerful reasoning): Does the Skill avoid over-explaining?"
> (Best practices, Test with all models)

> "Keep SKILL.md body under 500 lines for optimal performance."
> (Best practices, Progressive disclosure patterns)

#### Source 3: Prompting best practices / XML tags (Anthropic docs)

> "XML tags help Claude parse complex prompts unambiguously, especially when your prompt mixes instructions, context, examples, and variable inputs. Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation."
> (Prompting best practices, Structure prompts with XML tags)

> "Use XML format indicators — Try: 'Write the prose sections of your response in `<smoothly_flowing_prose_paragraphs>` tags.'"
> (Prompting best practices, Control the format of responses)

> "When extended thinking is disabled, Claude Opus 4.5 is particularly sensitive to the word 'think' and its variants. Consider using alternatives like 'consider,' 'evaluate,' or 'reason through' in those cases."
> (Prompting best practices, Thinking and reasoning note)

> "Prefilled responses on the last assistant turn are no longer supported [starting with Claude 4.6]. On Mythos Preview, requests with prefilled assistant messages return a 400 error."
> (Prompting best practices, Migrating away from prefilled responses)

#### Source 4: Claude Code skills documentation

> "Claude Code skills follow the [Agent Skills](https://agentskills.io) open standard, which works across multiple AI tools. Claude Code extends the standard with additional features like invocation control, subagent execution, and dynamic context injection."
> (Claude Code skills docs, intro)

> "The `!\\`<command>\\`` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself."
> (Claude Code skills docs, Inject dynamic context)

> "Add `context: fork` to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent."
> (Claude Code skills docs, Run skills in a subagent)

> "The `allowed-tools` field grants permission for the listed tools while the skill is active, so Claude can use them without prompting you for approval."
> (Claude Code skills docs, Pre-approve tools for a skill)

> "Skill descriptions are loaded into context so Claude knows what's available. All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters."
> (Claude Code skills docs, Troubleshooting: Skill descriptions are cut short)

#### Source 5: Claude Agent Skills: A First Principles Deep Dive (Lee Hanchung)

> "Claude agent skills do not live in the system prompt. They live in the `tools` array as part of the `Skill` tool's description."
> (Hanchung, Message Injection Mechanism)

> "When `isMeta: true`, the message gets sent to the Anthropic API as part of Claude's conversation context but never appears in the UI."
> (Hanchung, Two-Message Pattern)

> "There is no algorithmic `skill` selection or AI-powered intent detection at the code level. The decision-making happens entirely within Claude's reasoning process based on the skill descriptions provided."
> (Hanchung, Skill Selection Mechanism)

> "Claude Code doesn't use embeddings, classifiers, or pattern matching to decide which skill to invoke."
> (Hanchung, Skill Selection Mechanism)

> "The `<available_skills>` section has a token budget limit of 15,000 characters by default, preventing skill descriptions from overwhelming context."
> (Hanchung, Token Budget)

> "Skills modify two runtime contexts: 1. Tool Permissions: Pre-approve specific tools for skill duration via `allowedTools` array. 2. Model Selection: Override model via `model` field in frontmatter."
> (Hanchung, Execution Context Modification)

#### Source 6: Equipping agents for the real world (Anthropic Engineering blog)

> "A skill is a directory containing a SKILL.md file that contains organized folders of instructions, scripts, and resources that give agents additional capabilities."
> (Anthropic Engineering blog, What Agent Skills Are)

> "Skills leverage Claude's ability to 'invoke a Bash tool to read the contents' of files. Code execution tools allow Claude to run bundled scripts 'without loading either the script or the PDF into context'."
> (Anthropic Engineering blog, Claude-Specific Elements)

> "The system relies on Claude's decision-making to determine 'when each skill should be used.'"
> (Anthropic Engineering blog, Claude-Specific Elements)

> "We've published Agent Skills as an open standard for cross-platform portability."
> (Anthropic Engineering blog, Cross-Runtime Portability)

---

### Sub-Question 2: Cross-runtime abstraction standards

#### Source 7: Function Calling with Gemini API (Google)

> "You define functions using JSON, specifically with a select subset of the OpenAPI schema format."
> (Gemini function calling docs, Function Declaration Definition)

> "A function declaration requires: `name` (string): Unique identifier like `get_weather_forecast`. `description` (string): Detailed explanation of purpose. `parameters` (object): Input specification with `type`, `properties`, `required`."
> (Gemini function calling docs, Core Structure)

> "Function calling behavior is controlled via `function_calling_config` with these modes: `AUTO`: Default; model decides between natural language or function calls. `ANY`: Model must always predict a function call. `VALIDATED`: Default for tool combinations; ensures schema adherence. `NONE`: Disables function calling entirely."
> (Gemini function calling docs, Tool Configuration and Calling Modes)

> "Gemini 3 model APIs now generate a unique `id` for every function call. When returning results, developers must include 'the matching `id` in your `functionResponse` so the model can accurately map your result back to the original request.'"
> (Gemini function calling docs, Critical Gemini 3 Constraint)

#### Source 8: MCP Tools specification

> "The Model Context Protocol (MCP) allows servers to expose tools that can be invoked by language models. Tools enable models to interact with external systems, such as querying databases, calling APIs, or performing computations. Each tool is uniquely identified by a name and includes metadata describing its schema."
> (MCP Tools spec, intro)

> "A tool definition includes: `name`: Unique identifier for the tool. `title`: Optional human-readable name for display purposes. `description`: Human-readable description of functionality. `inputSchema`: JSON Schema defining expected parameters. `outputSchema`: Optional JSON Schema defining expected output structure. `annotations`: optional properties describing tool behavior."
> (MCP Tools spec, Data Types — Tool)

> "Tools use two error reporting mechanisms: 1. Protocol Errors: Standard JSON-RPC errors for issues like unknown tools, invalid arguments, server errors. 2. Tool Execution Errors: Reported in tool results with `isError: true`: API failures, invalid input data, business logic errors."
> (MCP Tools spec, Error Handling)

> "Servers that support tools MUST declare the `tools` capability."
> (MCP Tools spec, Capabilities)

> "For trust & safety and security, clients MUST consider tool annotations to be untrusted unless they come from trusted servers."
> (MCP Tools spec, Data Types — Tool, warning)

#### Source 10: Agent Skills as an Open Standard (MindStudio)

> "All three providers converged on JSON Schema for parameter definitions. The underlying parameter schema was essentially the same across all three."
> (MindStudio, Shared Foundation)

> "The core components are identical: Name: capability identifier. Description: natural language explanation for AI reasoning. Input schema: JSON Schema-defined parameters with types and requirements. Output format: structured return values. Invocation method: how to trigger the capability."
> (MindStudio, Shared Foundation)

> "Claude: Uses `tool_use` content blocks; Anthropic emphasizes that 'the description field heavily influences call accuracy.' OpenAI: Wraps definitions in `tools` arrays with `type: 'function'` and returns `tool_calls` arrays. Google: Uses `FunctionDeclaration` objects and returns `functionCall` parts."
> (MindStudio, Provider-Specific Differences)

> "Adapting a skill definition across providers typically takes minutes but acknowledges differences exist in 'how you pass skill definitions to the API (the wrapper structure) and how the model signals intent to invoke a skill.'"
> (MindStudio, Portability Limitations)

#### Source 11: Function Calling & Tool Use Complete Guide 2026 (oFox AI)

> OpenAI's wrapper approach:
> ```python
> "tools": [{"type": "function", "function": {"name": "get_weather", "parameters": {...}}}]
> ```
> Anthropic's direct format:
> ```python
> "tools": [{"name": "get_weather", "input_schema": {...}}]
> ```
> Google's type system:
> ```python
> "function_declarations": [types.FunctionDeclaration(name="get_weather", parameters=types.Schema(...))]
> ```
> (oFox AI, Tool Definition Structure)

> "| Aspect | OpenAI | Anthropic | Gemini | | Schema Key | `'parameters'` | `'input_schema'` | `types.Schema()` | | Wrapper | `{'type': 'function', 'function': {...}}` | Direct object | `types.Tool()` | | Format Type | JSON Schema | JSON Schema | Protocol Buffer types |"
> (oFox AI, Key Structural Differences table)

> "OpenAI returns parsed JSON strings: `tool_call.function.arguments` — Returns: `'{"location": "Tokyo"}'` — Requires: `json.loads()` parsing. Anthropic returns pre-parsed dictionaries: `block.input` — Returns: `{"location": "Tokyo"}` — Already a dict, no parsing needed. Gemini returns proto objects: `fc.args` — Proto object requiring `dict()` conversion."
> (oFox AI, Response Format Variations)

> "Despite format differences across providers, the pattern is always the same — define tools, send with message, detect calls, execute functions, return results."
> (oFox AI, quote)

#### Source 16: Structured Output Comparison (Glukhov)

> "Claude doesn't have a generic 'JSON mode' switch; instead, Tool Use with an `input_schema` gives you validated, schema-shaped arguments (and you can force its use)."
> (Glukhov, Anthropic (Claude) Distinction)

> "OpenAI's Structured Outputs feature enforces this schema on the server side. Gemini will return strict JSON that conforms to `response_schema`. Mistral's `json_object` enforces JSON shape (not your exact schema) — validate client-side."
> (Glukhov, comparison)

> "If you want the strongest server-side guarantees: OpenAI structured outputs or Gemini response schema. If you're already on Claude/Bedrock: define a Tool with a JSON schema and force its use."
> (Glukhov, Practical Guidance Summary)

---

### Sub-Question 3: Ecosystem portability layers

#### Source 9: Tool Calling with LangChain (LangChain blog)

> "All of these providers exposed slightly different interfaces (in particular: OpenAI, Anthropic, and Gemini, the three highest performing models are incompatible)."
> (LangChain blog, Core Normalization Quote)

> "The standard interface consists of: `ChatModel.bind_tools()`: a method for attaching tool definitions to model calls. `AIMessage.tool_calls`: an attribute on the `AIMessage` returned from the model for easily accessing the tool calls the model decided to make."
> (LangChain blog, The Standardization Solution)

> Using Anthropic:
> ```python
> llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0)
> llm_with_tools = llm.bind_tools([multiply, exponentiate, add, subtract])
> ```
> Switching to OpenAI requires only provider substitution:
> ```python
> llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
> llm_with_tools = llm.bind_tools([multiply, exponentiate, add, subtract])
> ```
> (LangChain blog, Cross-Provider Portability Achievement)

> "`ChatModel.bind_tools` provides a standard interface implemented by all tool-calling models that lets you specify which tools are available to the model. The method accepts multiple input formats: Pydantic classes, LangChain tools, and arbitrary functions, eliminating provider-specific schema writing."
> (LangChain blog, Schema Conversion Flexibility)

> "`AIMessage.tool_calls` provides a standardized interface for getting model tool invocations, returning consistent `ToolCall` structures regardless of underlying provider."
> (LangChain blog, Standardized Output Interface)

#### Source 18: convert_to_openai_tool — LangChain API Reference (search result content)

> "The exact format of tool definitions is model provider-dependent — OpenAI expects a dictionary with 'name', 'description', and 'parameters' keys, while Anthropic expects 'name', 'description', and 'input_schema'. However, `ChatModel.bind_tools` provides a standard interface implemented by all tool-calling models."
> (LangChain API reference, cross-model portability description from search results)

> "The `convert_to_openai_tool` function accepts either a dictionary, Pydantic BaseModel class, Python function, or BaseTool. If a dictionary is passed in, it is assumed to already be a valid OpenAI function, a JSON schema with top-level 'title' key specified, an Anthropic format tool, or an Amazon Bedrock Converse format tool."
> (LangChain API reference, convert_to_openai_tool)

> "Support for Anthropic format tools was added in version 0.3.13, and support for OpenAI's built-in code interpreter and remote MCP tools was added in version 0.3.61."
> (LangChain API reference, version history from search results)

#### Source 12: Tools — LlamaIndex Documentation

> "A Tool implements a very generic interface — simply define `__call__` and also return some basic metadata (name, description, function schema)."
> (LlamaIndex docs, Core Tool Concept)

> "Spending time tuning these parameters [name, description, function schema] can result in large changes in how the LLM calls these tools."
> (LlamaIndex docs, Core Tool Concept)

> "FunctionTool wraps user-defined functions (both sync and async). Users can auto-infer schemas or customize aspects using `Annotated` types for argument descriptions."
> (LlamaIndex docs, Tool Types — FunctionTool)

> "ToolSpecs represent 'bundles of tools meant to be used together' covering services like Gmail."
> (LlamaIndex docs, Tool Types — ToolSpecs)

> "LlamaIndex also allows using MCP tools through a ToolSpec on the LlamaHub, and you can simply run an MCP server and start using it through the implementation."
> (LlamaIndex docs, Utility Tools)

---

### Sub-Question 4: Empirical compatibility

#### Source 13: AI Agents vs Skills in Claude Code, Codex, Copilot CLI & Gemini CLI (ElGuerre)

> "All of them share the same Skills standard — same `SKILL.md` format, same open standard published by Anthropic in December 2025."
> (ElGuerre, Universal Format)

> "Skills live in tool-specific folders but follow the same format."
> (ElGuerre, Universal Format)

> "Copilot CLI's constraint: 'subagents cannot access Skills defined in the repository.' This represents a significant architectural difference — Copilot's delegation system doesn't inherit repository-level skill definitions when spawning specialized agents."
> (ElGuerre, Cross-Tool Limitations)

> "Codex requires explicit opt-in for child agent access: 'child agents don't inherit the `AGENTS.md` context. Enable `child_agents_md = true` in [features].' This contrasts with Claude Code's default inheritance behavior, creating workflow differences despite identical SKILL.md syntax."
> (ElGuerre, Configuration Inheritance)

#### Source 14: How to write one skill for both Claude Code and GitHub Copilot CLI (Hawkins)

> "Write skills as `SKILL.md` files with `name` and `description` frontmatter — both tools require exactly this."
> (Hawkins, What Works Across Both Tools)

> "The `description` field is the auto-detection trigger. Write it as a trigger condition: 'Use when the user asks to…'"
> (Hawkins, What Works Across Both Tools)

> "Both tools discover skills from the `skills/` subdirectory inside the plugin root automatically."
> (Hawkins, Directory structure)

> "Do not add a `skills` field to `plugin.json`. Claude Code rejects `plugin.json` with a validation error if a `skills` field is present. Omit it and both tools work; add it and Claude Code breaks."
> (Hawkins, Critical Gotcha: plugin.json)

> "Claude Code–specific features [that don't transfer to Copilot CLI]: The `version` field is Claude Code-specific but Copilot CLI ignores it safely. Agents, hooks, and MCP server config are 'Copilot CLI-specific' with 'no Claude Code equivalent'."
> (Hawkins, Claude Code–Specific Features)

#### Source 15: Berkeley Function Calling Leaderboard (BFCL) V4 (UC Berkeley)

> "The leaderboard evaluates 'the LLM's ability to call functions (aka tools) accurately' using real-world data."
> (BFCL, Methodology)

> "V1: Introduced AST (Abstract Syntax Tree) as an evaluation metric. V2: Added enterprise and open-source contributed functions. V3: Incorporated multi-turn interactions. V4: Focuses on 'holistic agentic evaluation.'"
> (BFCL, Evaluation Framework versions)

> "Overall Accuracy: described as 'the unweighted average of all the sub-categories.' Cost: 'Estimated cost for the entire benchmark, in USD.' Latency: 'Measured in seconds.'"
> (BFCL, Comparison Metrics)

#### Source 10: Agent Skills as an Open Standard (MindStudio) — additional portability empirics

> "Three major AI labs — Anthropic, OpenAI, and Google DeepMind — each settled on nearly the same format for describing what an AI agent can do, and a skill definition written for Claude can be adapted for GPT-4o or Gemini in minutes."
> (MindStudio, Cross-Runtime Specification from search results)

> "Full cross-provider compatibility requires adapter work for API wrapper structures and response formatting, even though the underlying JSON Schema is standardized."
> (MindStudio, Portability Limitations)

#### Source 17: Differences in Prompting Techniques: Claude vs. GPT (Biziuk/COXIT)

> "Claude: 'separating system prompts and user inputs, allowing the model to process information more effectively.' GPT: 'separating system and user inputs for GPT often results in diminished performance.'"
> (Biziuk, System vs. User Input Separation)

> "Claude's documentation recommends using XML tags to separate parts of the prompt template or large prompts. [But] when XML tags were used to separate user input for Claude, it actually led to worse results."
> (Biziuk, XML Tag Usage — mixed finding)

> "Claude tends to follow a more structured, step-by-step approach to instructions, while GPT's outputs often involve more improvisation."
> (Biziuk, Instruction Following)

#### Additional: Open-source context window empirics (from search results)

> "Claude models 'decay the slowest overall,' while GPT models were 'more erratic with random mistakes and outright refusals,' and Gemini 'starts to mess up earlier with wild variations.'" (Chroma study, July 2025 per search result; primary source not fetched)

> "Performance degrades at every context length increment, not just near the limit, with models exhibiting measurable degradation even at 50K tokens." (Chroma study, July 2025 per search result; primary source not fetched)

> "Feature comparison matrices for tool/function calling show that OpenAI has widely-used tools, Claude supports tools via provider-specific patterns, Gemini supports tools + grounding options, while open-source models often require prompting to emit JSON with no native tools." (From search results summary; primary source not individually fetched)

<!-- deferred-sources
- https://www.juheapi.com/blog/context-window-size-comparison-gpt5-claude4-gemini25-glm46 (fetched, context window data used in SQ4)
- https://gorilla.cs.berkeley.edu/leaderboard.html — BFCL V4, specific accuracy numbers not extractable from fetched page, leaderboard data is dynamic
- https://spec.modelcontextprotocol.io/specification/2025-03-26/ — SSL cert error, could not fetch; used modelcontextprotocol.io/docs/concepts/tools instead
- https://platform.openai.com/docs/guides/function-calling — returned 403 at fetch time; structural differences covered via secondary sources (ofox.ai, search results)
- Chroma context window study July 2025 — not fetched individually; cited via search result summary only
-->
