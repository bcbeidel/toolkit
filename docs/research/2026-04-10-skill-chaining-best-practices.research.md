---
name: "Skill Chaining Best Practices"
description: "Skill chaining best practices: output contracts and boundary validation are the highest-leverage interventions; multi-agent sequential chains are not automatically better than single agents; most failures are structural design failures, not prompt failures. Includes framework survey (LangChain, Semantic Kernel, LlamaIndex, Claude Code, n8n), failure mode taxonomy, evaluation guidance, and six concrete wos tooling implications."
type: research
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/chain-prompts
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
  - https://blog.langchain.com/choosing-the-right-multi-agent-architecture/
  - https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
  - https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent/
  - https://openai.github.io/openai-agents-python/multi_agent/
  - https://blog.n8n.io/ai-agentic-workflows/
  - https://www.promptingguide.ai/techniques/prompt_chaining
  - https://www.promptingguide.ai/techniques/react
  - https://arxiv.org/html/2503.13657v1
  - https://galileo.ai/blog/why-multi-agent-systems-fail
  - https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/
  - https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows
  - https://www.mindstudio.ai/blog/how-to-build-claude-code-skill-chain-business-workflow
  - https://dextralabs.com/blog/recursive-language-models-rlm/
  - https://orq.ai/blog/llm-orchestration
  - https://arxiv.org/html/2512.08296v1
  - https://arxiv.org/html/2604.02460v1
  - https://arxiv.org/html/2510.04265v1
  - https://arxiv.org/html/2602.20867
  - https://arxiv.org/html/2602.22302
  - https://arxiv.org/html/2602.12670v1
  - https://runloop.ai/blog/i-have-opinions-on-pass-k-you-should-too
related: []
---

# Skill Chaining Best Practices

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | LLM agent orchestration patterns skill chaining definition 2024 2025 | web | 10 |
| 2 | prompt chaining best practices Anthropic OpenAI sequential LLM | web | 10 |
| 3 | LangChain chain composition design patterns sequential agent handoff | web | 10 |
| 4 | Semantic Kernel pipeline orchestration skill chaining Microsoft | web | 10 |
| 5 | recursive agent patterns termination conditions depth limits LLM guardrails | web | 10 |
| 6 | LLM agent failure modes antipatterns prompt chaining context poisoning infinite loop | web | 10 |
| 7 | LlamaIndex workflow orchestration agent skill composition patterns | web | 10 |
| 8 | n8n Zapier workflow automation design patterns chaining nodes failure handling | web | 10 |
| 9 | ReAct chain-of-thought compositional agent pattern academic paper skill chaining | web | 10 |
| 10 | agent skill evaluation testing debugging validation techniques LLM workflow | web | 10 |
| 11 | Claude Code skill plugin architecture chaining handoff design | web | 10 |
| 12 | output contracts state passing LLM agent handoff schema validation structured outputs | web | 10 |
| 13 | agent skill design output schema contract idempotency retry sequential pipeline best practices 2025 | web | 10 |
| 14 | Tree of Thought agent orchestration decomposition compositional reasoning LLM | web | 10 |
| 15 | wos Claude Code plugin skill invocation chain sequential workflow | web | 10 |
| 16 | Fetch: https://www.anthropic.com/research/building-effective-agents | fetch | full |
| 17 | Fetch: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/chain-prompts | fetch | full (redirected to prompting-best-practices) |
| 18 | Fetch: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | fetch | full |
| 19 | Fetch: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | fetch | full |
| 20 | Fetch: https://blog.langchain.com/choosing-the-right-multi-agent-architecture/ | fetch | full |
| 21 | Fetch: https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/ | fetch | full |
| 22 | Fetch: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns | fetch | full (large) |
| 23 | Fetch: https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent/ | fetch | full |
| 24 | Fetch: https://openai.github.io/openai-agents-python/multi_agent/ | fetch | full |
| 25 | Fetch: https://blog.n8n.io/ai-agentic-workflows/ | fetch | full |
| 26 | Fetch: https://www.promptingguide.ai/techniques/prompt_chaining | fetch | full |
| 27 | Fetch: https://arxiv.org/html/2503.13657v1 | fetch | full |
| 28 | Fetch: https://galileo.ai/blog/why-multi-agent-systems-fail | fetch | full |
| 29 | Fetch: https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/ | fetch | full |
| 30 | Fetch: https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows | fetch | full |
| 31 | Fetch: https://www.mindstudio.ai/blog/how-to-build-claude-code-skill-chain-business-workflow | fetch | full |
| 32 | Fetch: https://dextralabs.com/blog/recursive-language-models-rlm/ | fetch | full |
| 33 | Fetch: https://towardsdatascience.com/the-multi-agent-trap/ | fetch | failed (JS-rendered content not returned) |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | 2024 | T1 | verified |
| 2 | https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/chain-prompts | Prompting Best Practices (chain-prompts redirects here) | Anthropic | 2025–2026 | T1 | verified |
| 3 | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview | Agent Skills Overview | Anthropic | 2025–2026 | T1 | verified |
| 4 | https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Demystifying Evals for AI Agents | Anthropic Engineering | 2025 | T1 | verified |
| 5 | https://blog.langchain.com/choosing-the-right-multi-agent-architecture/ | Choosing the Right Multi-Agent Architecture | LangChain | 2024–2025 | T1 | verified |
| 6 | https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-orchestration/ | Semantic Kernel Agent Orchestration | Microsoft | 2025 | T1 | verified |
| 7 | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns | AI Agent Orchestration Patterns | Microsoft Azure | 2026-02-12 | T1 | verified |
| 8 | https://developers.llamaindex.ai/python/framework/understanding/agent/multi_agent/ | Multi-Agent Patterns in LlamaIndex | LlamaIndex | 2025 | T1 | verified |
| 9 | https://openai.github.io/openai-agents-python/multi_agent/ | Agent Orchestration — OpenAI Agents SDK | OpenAI | 2025 | T1 | verified |
| 10 | https://blog.n8n.io/ai-agentic-workflows/ | AI Agentic Workflows: A Practical Guide for n8n Automation | n8n | 2025 | T2 | verified |
| 11 | https://www.promptingguide.ai/techniques/prompt_chaining | Prompt Chaining | Prompt Engineering Guide (DAIR.AI) | 2024 | T2 | verified |
| 12 | https://www.promptingguide.ai/techniques/react | ReAct Prompting | Prompt Engineering Guide (DAIR.AI) | 2024 | T2 | verified |
| 13 | https://arxiv.org/html/2503.13657v1 | Why Do Multi-Agent LLM Systems Fail? | Academic (arXiv) | 2025-03 | T1 | verified |
| 14 | https://galileo.ai/blog/why-multi-agent-systems-fail | Are Your Multi-Agent Systems Failing for These 7 Reasons? | Galileo AI | 2025 | T2 | verified |
| 15 | https://github.blog/ai-and-ml/generative-ai/multi-agent-workflows-often-fail-heres-how-to-engineer-ones-that-dont/ | Multi-Agent Workflows Often Fail. Here's How to Engineer Ones That Don't. | GitHub Blog | 2025 | T2 | verified |
| 16 | https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows | Claude Code Skill Collaboration: How to Chain Skills Into End-to-End Workflows | MindStudio | 2025 | T3 | verified |
| 17 | https://www.mindstudio.ai/blog/how-to-build-claude-code-skill-chain-business-workflow | How to Build a Claude Code Skill That Chains Into a Full Business Workflow | MindStudio | 2025 | T3 | verified |
| 18 | https://dextralabs.com/blog/recursive-language-models-rlm/ | Why Recursive Language Models (RLMs) Beat Long-Context LLMs | DextraLabs | 2025 | T3 | verified |
| 19 | https://orq.ai/blog/llm-orchestration | LLM Orchestration in 2025: Frameworks + Best Practices | orq.ai | 2025 | T3 | verified |
| 20 | https://arxiv.org/pdf/2210.03629 | ReAct: Synergizing Reasoning and Acting in Language Models | Yao et al. (NeurIPS 2022) | 2022 | T1 | verified |

## Extracts by Sub-Question

### SQ1: How do practitioners and frameworks define "skill chaining"?

**Core definition — prompt/skill chaining:**
"Prompt chaining breaks complex tasks into subtasks, where each LLM response feeds into the next prompt ... a task is split into subtasks with the idea to create a chain of prompt operations." [11]

"Chaining refers to a sequence of calls that connect multiple LLMs to combine their outputs to achieve more nuanced results (also known as prompt chaining)." [19]

**Skill as unit of chaining:**
"A skill is a bundle that can include instructions, workflow guidance, executable scripts, reference documentation, and metadata, all organized to be dynamically loaded when relevant ... many real-world tasks require not a single tool call but a coordinated sequence of decisions informed by domain-specific procedural knowledge." [19 / search synthesis]

**Sequential pattern definition (Anthropic):**
Anthropic's canonical framing describes "workflows" as "LLMs and tools are orchestrated through predefined code paths" versus "agents" as "systems where LLMs dynamically direct their own processes and tool usage." Prompt chaining is identified as decomposing tasks into sequential steps where "each LLM call processes the output of the previous one." [1]

**Azure/Microsoft sequential pattern definition:**
"The sequential orchestration pattern chains AI agents in a predefined, linear order. Each agent processes the output from the previous agent in the sequence, which creates a pipeline of specialized transformations. Also known as: pipeline, prompt chaining, linear delegation." [7]

**LangChain four-pattern vocabulary:**
LangChain identifies four architectural units that can compose into chains: subagents (orchestrator calls specialist as tool), skills (dynamic persona loading), handoffs (active agent transfers control via tool call), and routers (input-directed dispatch). [5]

**Shared vocabulary in the field (2025):**
Terms used interchangeably across sources: prompt chaining, skill chaining, agent pipeline, sequential orchestration, chain-of-thought, workflow composition. The closest to a shared standard is the Microsoft Azure taxonomy: sequential, concurrent, handoff, group-chat, and magentic (generalist multi-agent). [7]

**ReAct as compositional academic framing:**
"ReAct is an AI agent framework that combines chain of thought (CoT) reasoning with external tool use ... First introduced in the 2023 paper 'ReACT: Synergizing Reasoning and Acting in Language Models'." ReAct's Thought–Action–Observation loop is the academic precursor to modern skill-chain design. [12, 20]

---

### SQ2: Design principles for clean handoffs between skills

**Three essential components for handoffs (MindStudio/Claude Code):**
"Three essential components enable [skill chaining]: (1) a shared state layer — files, JSON objects, or environment variables pass data between skills; (2) an orchestrator — decides which skill runs next and with what inputs; (3) output contracts — each skill produces predictable, consumable formats." [16]

**Loose coupling via output contracts:**
"Define what fields a skill _must_ include in its output, and let it include additional fields freely. Downstream skills only read required fields, preventing breakage from minor changes." Use structured JSON, not plain text: "Plain text is hard to parse reliably." [16]

**Typed schemas are non-negotiable (GitHub Engineering):**
"Typed schemas are table stakes in multi-agent workflows. Without them, nothing else works." The recommendation is to implement strict TypeScript-like contracts and exhaustive, mutually-exclusive action schemas to prevent agents from "inventing their own interpretation of intent." [15]

**MCP enforces contracts at the boundary:**
"Anthropic's Model Context Protocol (MCP) enforces schema-validated messages using JSON-RPC 2.0, giving every message an explicit type, validated payload, and clear intent." MCP validates schemas before execution, preventing invalid state from reaching production systems. [15 / search synthesis]

**Single source of truth for state:**
"Write to a single source of truth. Avoid multiple files for different stages. Log each transition with timestamp and skill name for debugging. Each skill should write an error field to state if it encounters a problem." [16]

**Anthropic's XML tagging for inter-prompt handoffs:**
Anthropic recommends "structuring handoffs with XML tags to pass outputs between prompts" and ensuring "each subtask has a single, clear objective." [2]

**Compact returns prevent context bloat:**
Skills should return "only what the next step needs, not a full transcript of what happened internally. Store verbose outputs in a separate registry; Claude receives minimal references." [17]

**OpenAI SDK — structured input on handoffs:**
"Handoffs support structured inputs through the input_type parameter. This allows the LLM to provide structured data when performing a handoff ... The SDK validates this and passes the structured object to the on_handoff callback." [9]

**Semantic Kernel — unified interface:**
"All orchestration patterns share a unified interface for construction and invocation. No matter which orchestration you choose, you: define your agents and their capabilities; create an orchestration by passing the agents; optionally provide callbacks or transforms for custom input/output handling; start a runtime and invoke the orchestration with a task." [6]

---

### SQ3: Best practices for sequential skill chains

**Validate at every boundary:**
"Validate agent output before passing it to the next agent — low-confidence, malformed, or off-topic responses can cascade through a pipeline, so the orchestrator or receiving agent should check output quality and either retry, request clarification, or halt the workflow." [search synthesis / 7]

**When to use sequential over concurrent (Azure):**
Use sequential when: stages have clear linear dependencies; data transformation requires each stage to add value the next depends on; workflow stages cannot be parallelized; progressive refinement (draft → review → polish) is required. Avoid when stages are embarrassingly parallel, when early stages may fail with no guard on later steps consuming bad output, or when dynamic routing is needed. [7]

**Start simple, increase complexity only when justified (Anthropic):**
"Only increase complexity when it demonstrably improves outcomes. Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs." [1]

**Azure complexity ladder:**
Before multi-agent sequential chains, verify whether a direct model call or single agent with tools suffices. The ladder: direct model call → single agent with tools → multi-agent orchestration. [7]

**Idempotency for retry safety:**
"Side-effectful tools should accept idempotency tokens and be safe under retries; read paths should be pure, making recovery from partial failures predictable and supporting exactly-once semantics at the orchestration layer." [search synthesis] In skill chains: "Always check completed_steps before re-executing." [17]

**Failure propagation via error fields, not exceptions:**
Return failure states: "This allows Claude to reason about failures and decide whether to retry, skip, or escalate — rather than crashing with no recovery path." [17]

**n8n sequential pattern guidance:**
"Each step in the chain is well-defined and outputs data in a format that the next step can use." Each step can be refined independently; implement error handling between steps; use flow control nodes (Filter, IF, Loop, Merge). [10]

**Anthropic self-correction chain:**
"The most common chaining pattern with Claude is self-correction: generate a draft → have Claude review it against criteria → have Claude refine based on the review, with each step as a separate API call so you can log, evaluate, or branch at any point." [2]

**Context window management across a chain:**
"Monitor token usage across the chain. Each skill's output consumes context, so use structured JSON returns and avoid verbose API responses re-appended to Claude's context window." [17]

---

### SQ4: Best practices for recursive skill patterns

**Five-layer bounded recursion guardrails:**
"Bounded recursion uses five concentric guardrails (depth limit, PATH scrubbing, call count, budget, timeout) to guarantee termination. The system prompt also installs cognitive pressure: deeper agents are told to be more conservative, preferring direct action over spawning more children." [search synthesis / recursive agent literature]

**Layered termination conditions:**
"Termination conditions are layered: the model produces a response with no tool calls, the maximum turn limit is exceeded, the token budget is exhausted, a guardrail tripwire fires, the user interrupts, or a safety refusal is returned." [search synthesis]

**Production RLM design requirements:**
"Production RLM systems include guardrails, depth limits, confidence thresholds, audit logging, and access controls, ensuring predictable behavior, data security, and compliance with enterprise governance requirements." [18]

**Always set termination conditions and retry limits:**
"Always set termination conditions and retry limits to prevent infinite loops, limit iterations to prevent runaway execution, and monitor execution using observability features to track iteration counts and performance." [search synthesis]

**Tree of Thought as recursive reasoning pattern:**
ToT "maintains a tree of thoughts, where thoughts represent coherent language sequences that serve as intermediate steps toward solving a problem" and enables "systematic exploration of thoughts with lookahead and backtracking." Combined with BFS/DFS search algorithms, it provides deliberate multi-path recursion. [search synthesis]

**RLM multi-stage reasoning:**
RLMs enable "multi-stage recursive reasoning, allowing the model to revisit retrieved context, refine conclusions, and maintain global coherence across large knowledge spaces." Reliability assessment for recursive systems includes: "reasoning consistency, traceability of intermediate steps, hallucination resistance, recursion stability, and human-in-the-loop validation." [18]

**Anthropic's evaluator-optimizer as bounded recursion:**
"In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop." This works when "LLM responses can be demonstrably improved when a human articulates their feedback." The implicit bound is convergence on quality criteria. [1]

**Subagent spawn control (Claude Code):**
Claude Opus 4.6 "has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice." Guidance: "Use subagents when tasks can run in parallel, require isolated context, or involve independent workstreams that don't need to share state. For simple tasks, sequential operations, single-file edits, or tasks where you need to maintain context across steps, work directly rather than delegating." [2]

---

### SQ5: Antipatterns and failure modes

**Error amplification in chains:**
"When you connect multiple LLM agents in a chain or loop, each agent's small hallucination becomes another agent's incorrect input. Unstructured multi-agent networks amplify errors up to 17.2 times compared to single-agent baselines." [search synthesis / multi-agent failure literature]

**MASFT taxonomy — 14 failure modes in 3 categories:**
Academic research identified 14 distinct failure modes: (FC1) specification/system design failures (role confusion, step repetition, unaware of termination); (FC2) inter-agent misalignment (context resets, task derailment, reasoning-action mismatch); (FC3) task verification and termination (premature termination, insufficient verification). [13]

**Root cause: organizational design, not individual agents:**
"Failures stem from organizational design flaws rather than individual agent limitations ... interventions like improved prompts and topology redesign yielded only +14% improvement in ChatDev, demonstrating that tactical fixes are insufficient." Structural changes — standardized protocols, comprehensive verification — are required. [13]

**Coordination cost explosion:**
"Coordination costs scale exponentially: 4 agents create 6 potential failure points, 10 agents create 45. Each interaction introduces opportunities for context loss, misalignment, and conflicting decisions." [14]

**Context poisoning:**
"Context poisoning manipulates multi-turn conversation state to bias future decisions — a persistent attack on agent memory. Sequential chains compress earlier messages, eroding information fidelity with each hop." [search synthesis]

**Seven production failure categories (Galileo):**
(1) Agent coordination breakdowns (role drift, suggestions lost between turns); (2) Lost context across handoffs (critical details vanish when context window exceeded); (3) Endless loops from missing termination criteria; (4) Runtime coordination failures (sequential bottlenecks, parallel race conditions); (5) Single agent failure cascading downstream; (6) Role confusion and boundary violations; (7) Inadequate observability ("failures that appear random yet often stem from a single missed handshake"). [14]

**"Goldilocks dilemma" in context passing:**
Too much context dilutes instruction density; too little risks "lossy compression, where critical edge-case details are smoothed out and lost." [14]

**Write conflict amplification:**
"Agent A creates a user profile structure. Agent B, unaware, creates a different structure" — this produces "three incompatible representations of the same concept." Unlike read operations, "write conflicts cascade." [14]

**Infinite loop cost:**
"An agent in an infinite loop can burn thousands of dollars of API credits in minutes." [search synthesis / orq.ai]

**Three most common production failure modes (AWS/dev.to):**
Context window overflow (tool returns more data than the LLM can process), MCP tool timeouts (external APIs block agent indefinitely), and reasoning loops (agent repeats the same tool call without progress). [search synthesis]

**Skills antipatterns (MindStudio):**
(1) Synchronous API calls without timeouts blocking entire chains; (2) unstructured text outputs that downstream skills cannot parse reliably; (3) vague skill descriptions causing missed or incorrect invocations; (4) single skills attempting multiple responsibilities, making debugging opaque. [17]

**Framework abstraction hides bugs:**
Anthropic warns that frameworks "often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug." [1]

---

### SQ6: Framework implementations — LangChain, Semantic Kernel, LlamaIndex, Claude Code, n8n/Zapier

**LangChain — four pattern vocabulary:**
LangChain's multi-agent architecture identifies four canonical patterns: (1) subagents (supervisor calls specialist as tool, maintains context); (2) skills (agent loads specialized prompts on-demand, context accumulates); (3) handoffs (active agent changes dynamically via tool calling, state-driven); (4) routers (classify and dispatch in parallel, stateless). Handoffs "save 40-50% of calls on repeat requests by maintaining context." Handoffs must execute sequentially. [5]

**LangGraph Command object:**
LangGraph introduced the `create_handoff_tool` function: "Each handoff tool specifying the target agent and including a description of when to use it," plus a `Command` object to enable richer multi-agent transitions. [5]

**Semantic Kernel — five orchestration patterns:**
Microsoft's SK supports: Concurrent (broadcast + collect), Sequential (pipeline), Handoff (dynamic control transfer), Group Chat (coordinated conversation with manager), and Magentic (generalist multi-agent). "All orchestration patterns share a unified interface." Sequential is described as: "Agents are organized in a pipeline. Each agent processes the task in turn, passing its output to the next agent in the sequence." [6, 7]

**Semantic Kernel shared context:**
"While the pipeline or chain is executing, a common context is provided by the kernel so data can be shared and passed between those underlying tasks." [search synthesis]

**LlamaIndex — three-tier progressive pattern:**
(1) AgentWorkflow (minimal code, linear swarm with built-in handoff logic — root agent hands off to peers); (2) Orchestrator agent (top-level agent exposes sub-agents' `run()` methods as callable tools, all decisions flow through one place); (3) Custom Planner (LLM generates XML/JSON execution plan, Python code executes imperatively). Recommendation: "Start with AgentWorkflow, migrate to Orchestrator when sequencing complexity increases, adopt Custom Planner only when preceding patterns lack necessary expressiveness." [8]

**LlamaIndex shared state:**
"Tools and functions in an AgentWorkflow have access to the global workflow Context, allowing agents to retrieve and modify shared state across tool executions." [8]

**OpenAI Agents SDK — two orchestration modes:**
(1) LLM-driven: "allows the LLM to make decisions: plan, reason, and decide on what steps to take"; (2) Code-based: "determining the flow of agents via your code," offering greater predictability. Agents-as-tools vs. handoffs distinction: use agents-as-tools when "one agent should own the final answer"; use handoffs "when the specialist should respond directly." [9]

**Claude Code skills — three-level progressive disclosure:**
Level 1 (metadata, always loaded, ~100 tokens): YAML frontmatter for discovery. Level 2 (instructions, loaded on trigger, under 5k tokens): SKILL.md body. Level 3 (resources/code, loaded as needed): scripts and reference files, no context penalty until accessed. "This filesystem-based architecture enables progressive disclosure: Claude loads information in stages as needed, rather than consuming context upfront." [3]

**Claude Code orchestration — description-driven routing:**
"Claude decides the sequence — you don't hard-code it." Skill descriptions serve as the routing contract. "Descriptions are critical for orchestration ... treat descriptions as 'the skill's contract.'" [17]

**n8n — four agentic workflow patterns:**
(1) Chained requests: sequential AI calls with defined outputs at each step; (2) Single agent: one agent with memory maintains state; (3) Multi-agent with gatekeeper: hierarchical, primary coordinates specialists; (4) Multi-agent teams: distributed collaborative mesh. Key principle: "Each step in the chain is well-defined and outputs data in a format that the next step can use." [10]

**n8n failure handling:**
"Implement error handling between steps to manage potential failures in the chain. The most important n8n production setup step is to set up an Error Workflow." [10]

**Zapier vs n8n:**
Zapier is simpler app-to-app recipes; n8n is "aimed more directly at users who need flexibility, logic, and control." n8n is preferred "when workflows need deeper logic, custom API work, coding flexibility, AI orchestration, or self-hosting." [search synthesis]

---

### SQ7: Tooling and evaluation techniques

**Evaluation framework components (Anthropic):**
Tasks (single test with input + success criteria), Trials (multiple attempts for variance), Transcripts (complete records including tool calls and intermediate results), Outcomes (final environmental state). Three grader types: code-based (fast, cheap, brittle), model-based (flexible, requires calibration), human (gold-standard, expensive). [4]

**Two critical multi-step metrics:**
pass@k: "Measures the likelihood that an agent gets at least one correct solution in k attempts." pass^k: "Measures the probability that all k trials succeed." These diverge significantly: at k=10, pass@k approaches 100% while pass^k falls to 0%. [4]

**Grade outcomes not paths:**
"Agents regularly find valid approaches that eval designers didn't anticipate. So as not to unnecessarily punish creativity, it's often better to grade what the agent produced, not the path it took." [4]

**Three-tier testing strategy:**
Unit tests (individual tools in isolation), Integration tests (multi-step journey for a single agent), End-to-end tests (full workflow including environmental outcomes). [search synthesis]

**Observability as primary debugging tool:**
"Traces allow you to step into every step of the process and figure out exactly what went wrong; when a user reports a bug, you can see in the trace the exact conversation history and context, what the agent decided at each step, and where specifically it went wrong." [search synthesis / LangChain]

**LLM-as-judge calibration:**
"LLM-as-judge graders should be closely calibrated with human experts. Start with human experts to create a small, high-quality 'golden dataset,' then use that data to fine-tune an LLM-as-judge until its scores align." [search synthesis]

**Isolate trials:**
"Each trial should be 'isolated' by starting from a clean environment to eliminate infrastructure noise." [4]

**Read transcripts:**
"When a task fails, the transcript tells you whether the agent made a genuine mistake or whether your graders rejected a valid solution." [4]

**Continuous evaluation pipeline:**
Automated evals pre-launch and in CI/CD; production monitoring post-launch for distribution drift; A/B testing for significant changes; user feedback and transcript review as ongoing practices. [search synthesis]

**Schema-first debugging:**
"Fail fast on schema violations rather than propagating bad data. Monitor intermediate state to detect when assumptions break." Most agent failures are "action failures" — enforce typed contracts at every boundary. [15]

**State logging for sequential chains:**
"Log each transition with timestamp and skill name for debugging." Use structured JSON for test results and task status; use freeform text for progress notes; use git for state tracking across sessions. [2, 16]

---

### SQ8: Implications for wos tooling

**wos skill ecosystem — current state:**
wos provides 13+ skills that naturally form sequential patterns (wos:research → wos:distill → wos:audit-wos; wos:brainstorm → wos:write-plan → wos:execute-plan → wos:validate-work → wos:finish-work). These are currently invoked by description-matching, not by explicit chain definitions. There are no documented output contracts between skills, no shared state schema, and no chain-level validation tooling.

**What the evidence implies wos needs:**

1. **Output contract documentation per skill.** Each skill's SKILL.md or a companion CONTRACTS.md should declare what structured output it produces and what it expects as input. This is the single most cited requirement across all sources — "Typed schemas are table stakes." [15] Currently wos skills produce free-text; the research → distill handoff relies on Claude interpreting unstructured output.

2. **Chain composition guide.** The evidence shows frameworks (LlamaIndex, LangChain) provide explicit pattern selection guidance. wos should document the known chain patterns (linear sequential, evaluator-optimizer loop, gatekeeper-with-specialists) and when each applies to context-building workflows.

3. **Idempotency markers.** The evidence recommends checking completed_steps before re-executing any step. [17] wos plans track checkboxes; skills should be designed to read that plan state and skip already-completed stages rather than re-running from scratch.

4. **Shared state schema.** For multi-skill workflows (the research pipeline being the canonical example), wos should define a lightweight JSON schema for workflow state — analogous to the WorkflowContext pattern [17] — that survives across skill invocations within a session.

5. **Chain-level audit.** The audit-wos skill checks individual document quality. There is no equivalent check that a skill chain was invoked correctly (e.g., distill was run on a research doc that has passed verification, not a draft). A chain-level validator would mirror the "validate every agent boundary" principle. [15]

6. **Transition logging.** The evidence is unambiguous: "log each transition." [16] wos plan files track task checkboxes but not when each step produced its output, what it handed off, or whether the handoff was valid. A structured transition log in the plan file would enable debugging of failed chains.

7. **Skill description precision.** Claude Code routes skill invocations purely by description matching. "Descriptions are critical for orchestration ... treat descriptions as 'the skill's contract.'" [17] wos skill descriptions should explicitly state: what structured output is produced, what inputs are required, and which skill should logically follow.

8. **Evaluation harness for skill chains.** The evidence recommends unit tests (individual skill in isolation), integration tests (two-skill handoff), and end-to-end tests (full chain). wos has pytest coverage for validators but no evaluation harness for skill chain behavior. Given that the research pipeline spans 4+ skills, a golden-dataset eval suite for the chain would significantly increase reliability confidence before deployment changes.

---

## Challenge

### Contested Claims

**Claim: "Unstructured multi-agent networks amplify errors up to 17.2 times compared to single-agent baselines." [SQ5]**

The document presents this as a general property of multi-agent chaining. The original source (Towards a Science of Scaling Agent Systems, Google DeepMind, arXiv 2512.08296, 2025) tells a more specific story: 17.2× applies *only* to fully independent multi-agent architectures — systems with zero inter-agent communication. Centralized coordination yields 4.4×; hybrid architectures yield 5.1×; decentralized architectures yield 7.8×. The number was measured across 180 configurations spanning four benchmarks with multiple model families, making it aggregate rather than task-specific. The research document presents this figure without the architectural qualifier, which risks it being read as "chaining amplifies errors 17x" rather than "the absence of coordination does." A sequential skill chain with boundary validation is not the same regime as the "bag of agents" being indicted. The 17.2× figure does not apply to the wos use case unless wos skills run without any handoff validation — which the same evidence argues against. **Verdict: The figure is real but the presentation omits its most important caveat. It should be hedged to: "independent, uncoordinated MAS architectures amplify errors up to 17.2×; structured sequential chains with boundary validation face substantially lower risk."**

**Claim: "Typed schemas are table stakes in multi-agent workflows. Without them, nothing else works." [SQ2]**

The document treats this as settled engineering consensus. In practice, the gap between schema aspirations and production enforcement is wide. Agent Behavioral Contracts research (Rath, 2026, arXiv 2602.22302) finds that behavioral drift — progressive divergence of agent outputs from intended specifications — occurs in deployed multi-agent systems even with typed schemas in place. The more fundamental problem is that token budgets are only known *after* an LLM call completes, meaning contracts cannot prevent a single expensive or malformed call from exceeding bounds; they can only prevent subsequent calls after violation. LLM output drift in financial workflows (Hacker News thread citing arXiv work on schema drift, 2025) shows that schema failures in practice are driven by prompt drift and distribution shift, not just missing type annotations. MCP's schema enforcement is also described as opt-in: "MCP embraces a pragmatic approach to schema adherence... providing structure without sacrificing flexibility." Zero unauthorized invocations were reported in enterprise deployments — but only "when schema checking was active." The document's quote from GitHub Engineering ("typed schemas are table stakes") comes from a practitioner blog post (Source 15, Tier T2), not a production case study. **Verdict: The directional recommendation (use typed schemas) is sound. The categorical framing ("without them, nothing else works") overstates what schemas alone can guarantee. They are necessary but not sufficient — behavioral drift and output distribution shift remain unsolved problems.**

**Claim: "ReAct's Thought–Action–Observation loop is the academic precursor to modern skill-chain design." [SQ1]**

The document positions ReAct (Yao et al., 2022) as the foundational lineage. This is contested terrain. ReAct has documented failure modes that skill-chaining literature treats as solved: context drift (loss of original goal across long chains), ungrounded thought (intermediate reasoning without a consistent belief state), and local optimization traps (myopic subgoal pursuit that diverges from global intent). These are not incidental bugs in ReAct — they are structural properties of the Thought–Action–Observation formulation that have prompted successor architectures (Focused ReAct, REST-meets-ReAct, ReAct&Plan). The document cites ReAct approvingly without noting that the framework's limitations are precisely the failure modes SQ5 documents. The lineage claim is not wrong, but presenting ReAct as *precursor* without noting that its shortcomings motivated the design principles in SQ3 and SQ4 weakens the causal chain. **Verdict: The claim survives but needs the failure-mode context to be intellectually honest about why later practices differ from ReAct.**

**Claim: Sequential best practices (validate at boundaries, idempotency, error fields) transfer generically across domains. [SQ3]**

The document implies these practices are universal. Domain-specific evidence is more nuanced. In regulated domains (healthcare, legal, financial services), sequential chaining introduces additional governance constraints that generic best practices do not address: regulatory audit requirements for every step, mandatory human-in-the-loop gates, non-negotiable halt conditions when confidence thresholds are not met, and chain-provenance attestation. Singapore's 2026 Agentic AI Framework, Hogan Lovells' analysis of financial services agentic AI (2025), and the FINOS AI Governance Framework all document domain-specific constraints that override generic engineering patterns. The implication is not that the SQ3 practices are wrong — they are correct within their scope — but that "validate at every boundary" in a healthcare context is a compliance requirement with legal consequences, not just an engineering preference. **Verdict: The practices are sound for general software contexts. The document does not acknowledge that regulated-domain deployments require additional constraints that change the architecture significantly.**

**Claim: pass@k and pass^k are the "two critical multi-step metrics" for skill chain evaluation. [SQ7]**

The document presents pass@k and pass^k as the primary evaluation framework for multi-step agents, citing Anthropic's eval guide. Multiple independent sources challenge this framing. "Don't Pass@k: A Bayesian Framework for LLM Evaluation" (arXiv 2510.04265, 2025, accepted at OpenReview) demonstrates that pass@k yields unstable rankings with high variance, is sensitive to noise in small benchmarks, lacks uncertainty quantification, and has no principled decision rule for whether observed gaps are meaningful. The paper proposes Bayes@N (posterior mean estimation with credible intervals) as a more statistically rigorous alternative. Separately, Runloop's engineering blog documents that pass@1 optimization creates perverse incentives — models develop conservative strategies avoiding creative solutions — and that the metric does not capture solution diversity. Pass^k (all k trials succeed) is not mentioned or discussed in any of the counter-sources found, suggesting it is either a fringe proposal or so new it has not been evaluated against alternatives. **Verdict: pass@k is widely used but has recognized statistical weaknesses. pass^k has no corroborating adoption evidence beyond the Anthropic eval guide. The section should hedge: "pass@k is the dominant metric, but Bayesian alternatives (Bayes@N) show better stability and should be evaluated for production harnesses."**

**Claim: Multi-agent sequential chains outperform single agents for complex tasks. [SQ3, implicit throughout]**

The document's framing throughout assumes multi-agent chaining provides meaningful improvement over single agents when tasks are complex. A 2026 empirical study (arXiv 2604.02460, April 2026) directly challenges this: "under matched thinking-token budgets, single-agent systems consistently match or outperform multi-agent systems on multi-hop reasoning tasks." The key finding: MAS advantages reported in prior literature frequently stem from unaccounted computation differences rather than architectural benefits. The paper shows single agents are the strongest default architecture for multi-hop reasoning when computation is controlled. MAS becomes competitive only when a single agent's effective context degrades — through deletion, masking, or distraction injection. Separately, economic analysis (Iterathon 2026) suggests that for 70% of use cases, a well-prompted single agent delivers equivalent results at one-third the cost. **Verdict: This is a significant omission. The document implicitly treats multi-agent sequential chains as the correct architecture for complex tasks. The 2026 evidence argues for a more conditional claim: MAS is justified when context degradation is expected or when tasks are genuinely parallelizable — not as a general upgrade from single agents.**

---

### Missing Angles

**1. The "skill" vocabulary is not settled — it is actively contested by recent academic work.**

The document treats "skill" as a usable term with rough consensus. In reality, the field is mid-consolidation. The SoK paper (arXiv 2602.20867, Feb 2025) proposes a formal four-tuple definition (S = ⟨C, π, T, R⟩: applicability condition, policy, termination condition, reusable interface) and explicitly distinguishes skills from tools, plans, memory, and prompt templates. Anthropic released skills as an open standard in December 2025. SkillsBench (arXiv 2602.12670) finds that skill usage in realistic settings lags behind benchmark performance, and the gap is large. The document does not reflect any of this 2025–2026 academic scaffolding, which directly addresses SQ1. The practical consequence: wos's "skill" concept (a SKILL.md + scripts bundle) maps to the academic definition only partially — it lacks explicit termination conditions and applicability conditions as first-class properties.

**2. Behavioral drift is not covered under any sub-question.**

Agent Behavioral Contracts (Rath, 2026, arXiv 2602.22302) introduces the Agent Stability Index and finds that multi-agent LLM systems exhibit *measurable behavioral degradation over extended interactions* — outputs drift from intended specifications even when schemas are in place. This is a distinct failure mode from any of the 14 MASFT categories in SQ5 and is not addressed in the document. For wos, this matters for long-running research pipelines where wos:research → wos:distill → wos:write-plan chains may span multiple sessions: accumulated behavioral drift across sessions is not something the current wos architecture monitors.

**3. Economic cost of chaining is absent.**

The document contains no cost analysis. Documented production incidents include: a two-agent recursive loop running 11 days undetected ($47,000 API bill); multi-agent coordination overhead costing $24,700/month for a 2.1% accuracy gain over single agents. The document recommends adding chain-level auditing, shared state schemas, and evaluation harnesses — all reasonable — but does not address the engineering economics. For wos, where chains are interactive rather than automated batch processes, the cost vector is different (latency per invocation rather than runaway API bills), but token economics of shared state and transition logs are non-trivial at the skill level.

**4. Cross-runtime portability of skill chains is absent.**

The document focuses on Claude Code as the runtime, but skills are now described as working across Claude Code, Cursor, Gemini CLI, Codex CLI, and other agents (as of March 2026). The SQ6 framework comparison does not address how skill chaining conventions differ across runtimes or whether wos chain patterns would compose correctly in non-Claude Code environments. This is relevant because wos's CLAUDE.md notes a cross-runtime portability goal.

**5. SkillsBench performance gap — skills underperform in realistic conditions.**

SkillsBench (arXiv 2602.12670, Feb 2025) benchmarks LLM skill usage in realistic settings and finds that performance significantly lags behind controlled benchmarks. The document does not cite any empirical evaluation of skill chaining under realistic conditions — only framework documentation and engineering blog posts. This is a meaningful gap for SQ7 (evaluation tooling), where the document recommends building evaluation harnesses but does not cite the emerging benchmarking literature.

---

### Confidence Adjustments

**High confidence (evidence is strong and multi-sourced; challenges do not materially alter the finding):**

- **SQ2 directional claim: use structured outputs for inter-skill handoffs.** The recommendation to use structured JSON over plain text is supported by multiple T1 sources (Anthropic, OpenAI, Microsoft). Challenges to typed contracts affect *guarantees*, not the directional recommendation. This holds.
- **SQ3: validate at every boundary, use error fields over exceptions, monitor context budget.** Supported by Anthropic, Microsoft Azure, and LangChain documentation with consistent framing. These practices are not domain-universal (see regulated-domain caveat) but are sound engineering defaults.
- **SQ5: coordination design determines error amplification magnitude.** The 17.2× figure is real; the caveat is that it applies to uncoordinated independent architectures, not structured sequential chains. The practical lesson — design coordination explicitly — is well-supported.
- **SQ6: framework landscape is moving fast.** LangGraph hit v1.0 in October 2025; Semantic Kernel shipped first-class MCP support in v1.28.1. The document's framework descriptions are directionally accurate but may already be one version behind. The comparative patterns (sequential, handoff, concurrent) are stable; specific API details are not.

**Moderate confidence (evidence supports the direction but the mechanism or degree is uncertain):**

- **SQ4: bounded recursion guardrails work.** The five-layer guardrail framing is synthesis, not verified production evidence. The $47,000 incident cited in search results shows that depth limits can fail (the loop ran 11 days). The claim that bounded recursion "guarantees termination" is aspirational — wall-clock timeouts and budget limits are the only hard guarantees; depth limits depend on correct propagation.
- **SQ7: pass@k / pass^k as primary eval metrics.** Pass@k has documented statistical weaknesses (unstable rankings, variance problems). Pass^k has no independent corroboration of adoption. The directional recommendation (measure both one-success and all-success rates) survives, but the specific metrics should be supplemented with Bayesian alternatives for production harnesses.
- **SQ8: wos implications.** The eight recommendations are logically derived from the evidence. They have not been validated against wos's actual failure modes — no wos failure postmortem is cited. The recommendations may be correct but could be over-engineered for a plugin whose chains are short (4–5 skills), interactive (human in the loop at every step), and revision-driven rather than automated batch pipelines.

**Lower confidence (evidence is thin, contested, or from low-tier sources):**

- **SQ1: Microsoft Azure taxonomy as "closest to a shared standard."** The Azure taxonomy (sequential, concurrent, handoff, group-chat, magentic) is one proprietary framework's vocabulary. The SoK paper (arXiv 2602.20867) offers a more academically grounded taxonomy. Neither has been adopted as a standards-body specification. The claim of "closest to shared standard" has no comparative evidence.
- **SQ4: five-layer bounded recursion guardrails.** The framing is attributed to "search synthesis / recursive agent literature" with no specific paper citation. The DextraLabs blog post (Source 18, Tier T3) is the primary cited source. The guardrail list reads as reasonable engineering advice but lacks empirical validation.
- **SQ3: sequential chaining best practices transfer across domains.** Partial — regulated domains impose additional constraints that change the architecture. The practices hold within general software development contexts (which is the wos use case) but cannot be cited as universal.

---

### Additional Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 21 | https://arxiv.org/html/2512.08296v1 | Towards a Science of Scaling Agent Systems | Google DeepMind | 2025-12 | T1 | verified |
| 22 | https://arxiv.org/html/2604.02460v1 | Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets | Academic (arXiv) | 2026-04 | T1 | verified |
| 23 | https://arxiv.org/html/2510.04265v1 | Don't Pass@k: A Bayesian Framework for Large Language Model Evaluation | Academic (arXiv) | 2025-10 | T1 | verified |
| 24 | https://arxiv.org/html/2602.20867 | SoK: Agentic Skills — Beyond Tool Use in LLM Agents | Academic (arXiv) | 2025-02 | T1 | verified |
| 25 | https://arxiv.org/html/2602.22302 | Agent Behavioral Contracts: Formal Specification and Runtime Enforcement | Academic (arXiv) | 2026-02 | T1 | verified |
| 26 | https://arxiv.org/html/2602.12670v1 | SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks | Academic (arXiv) | 2025-02 | T1 | verified |
| 27 | https://runloop.ai/blog/i-have-opinions-on-pass-k-you-should-too | I have Opinions on Pass@K | Runloop Engineering | 2025 | T2 | verified |

## Findings

### SQ1: How do practitioners and frameworks define "skill chaining"?

No single authoritative standard exists yet, but the field is mid-consolidation (MODERATE confidence). The dominant practical vocabulary is **prompt chaining / sequential orchestration**: decomposing a task into subtasks where each LLM call processes the output of the previous one [1, 11]. Microsoft Azure's taxonomy — sequential, concurrent, handoff, group-chat, magentic — is the closest to a cross-vendor framework vocabulary [7], though it reflects one vendor's architecture, not a standards-body definition.

Academically, the field moved in 2025 toward a formal four-tuple definition (SoK, arXiv 2602.20867): a skill is ⟨C, π, T, R⟩ — applicability condition, policy, termination condition, reusable interface [24]. This is stricter than any framework definition and explicitly distinguishes skills from tools, memory, and prompt templates. wos's SKILL.md concept maps to this partially but lacks explicit termination conditions and applicability conditions as first-class properties.

**Bottom line:** Skill chaining = a coordinated sequence of skills where each skill consumes the prior skill's structured output. The vocabulary varies by framework; the underlying concept is stable. wos's definition aligns with the practitioner mainstream but is incomplete against the emerging academic standard.

---

### SQ2: Design principles for clean handoffs

Three components are necessary for clean handoffs: (1) **output contracts** — each skill declares what structured fields it produces; (2) **shared state** — a single source of truth persists across skill invocations; (3) **an orchestrator** — something decides what runs next and validates the handoff [16]. These are directional requirements with HIGH confidence (T1 sources from Anthropic, OpenAI, Microsoft all converge [2, 6, 9]).

The dominant practical recommendation is structured JSON over plain text [15, 16]. Every framework surveyed (SK, LlamaIndex, OpenAI Agents SDK) provides a mechanism for passing typed structures between agents. Plain text handoffs are universally described as fragile.

Important caveat (from the challenge): typed schemas are necessary but not sufficient. Behavioral drift — progressive divergence of agent output from intended specifications — occurs even when schemas are in place (Agent Behavioral Contracts, arXiv 2602.22302 [25]). Schemas prevent structural malformation; they cannot prevent semantic drift over extended chains.

Two operational rules hold at HIGH confidence: compact returns (pass only what the next step needs, not a full transcript [17]) and single-source-of-truth state (avoid multiple files, log transitions with timestamps [16]).

**Bottom line:** The handoff contract between skills is more important than the skill's internal logic. Define what every skill produces and what it requires before implementing the skill itself.

---

### SQ3: Best practices for sequential skill chains

Four practices hold at HIGH confidence for general software development contexts [1, 2, 7, 15, 17]:

1. **Start simple.** Direct model call → single agent with tools → multi-agent chain. Add stages only when simpler approaches demonstrably fail [1, 7]. A 2026 empirical study (arXiv 2604.02460 [22]) found that single agents match or outperform multi-agent systems on multi-hop reasoning when compute is controlled. Multi-agent chaining is not automatically better for complex tasks.

2. **Validate at every boundary.** The orchestrator checks output quality before passing to the next skill. Malformed, low-confidence, or off-topic outputs must be retried or halted — not propagated [7].

3. **Use error fields, not exceptions.** Skills should write failure state into their output rather than crashing. This lets the orchestrator decide whether to retry, skip, or escalate [17].

4. **Design for idempotency.** Side-effectful skills accept idempotency tokens and check already-completed steps before re-executing [16, 17]. This enables safe retries after partial failures.

Two additional practices hold at MODERATE confidence: context window management (track token usage across the chain; structured JSON returns minimize context bloat [17]) and the Anthropic self-correction loop as a validated sequential pattern (generate → review → refine as three separate calls, each checkpointable [2]).

**Bottom line:** Sequential chaining best practices reduce to three engineering rules: validate boundaries, fail explicitly, and remain idempotent. Everything else is application of these.

---

### SQ4: Best practices for recursive skill patterns

Recursive skill patterns (evaluator-optimizer loops, recursive decomposition, Tree of Thought) require explicit termination machinery. The recommended approach is layered guardrails: depth limit, call count, token budget, wall-clock timeout, and an explicit base case [1, 18]. Of these, budget and timeout are the only hard guarantees — depth limits depend on correct propagation and can fail if skill implementations bypass the orchestrator (the $47,000 incident cited in search results involved an 11-day loop, showing that soft limits are insufficient alone).

Anthropic's evaluator-optimizer is the most validated recursive pattern in production: one skill generates, another evaluates against criteria, the loop continues until a quality threshold is met [1]. The implicit bound is convergence, not depth. This works when "LLM responses can be demonstrably improved when a human articulates their feedback" — i.e., when quality criteria are precise enough to drive convergence.

Subagent spawn depth requires explicit management: Claude's tendency to spawn subagents in situations where direct action suffices is a documented behavior [2]. The guidance is direct: subagents for parallel isolated workstreams; sequential execution for tasks requiring shared context.

MODERATE confidence overall — the five-layer guardrail framing is synthesis from engineering literature (T3 source), not validated empirical evidence.

**Bottom line:** For any recursive skill pattern, implement both a semantic bound (convergence criterion) and a hard mechanical bound (budget or timeout). Depth limits alone are not sufficient.

---

### SQ5: Antipatterns and failure modes

Fourteen failure modes are documented across three categories (MASFT taxonomy, arXiv 2503.13657 [13]): specification failures (role confusion, step repetition, unaware of termination), inter-agent misalignment (context resets, task derailment, reasoning-action mismatch), and verification failures (premature termination, insufficient verification). The key finding: these failures stem from organizational design flaws, not individual agent quality — tactical prompt fixes yield only +14% improvement, structural redesigns are required [13].

Four failure modes have the highest practical cost in skill chains:

- **Context poisoning / lossy compression:** Sequential chains compress earlier messages across hops. The "Goldilocks dilemma" — too much context dilutes instruction density, too little loses critical detail — has no clean solution beyond compact, structured handoffs [14].
- **Write conflicts:** Two skills creating incompatible representations of the same concept, amplifying downstream [14].
- **Coordination cost explosion:** 4 agents = 6 failure points; 10 agents = 45. Complexity scales faster than benefit [14].
- **Missing observability:** "Failures that appear random often stem from a single missed handshake" [14]. Without traces, debugging sequential failures is practically intractable.

Error amplification (17.2×) is real but applies to *uncoordinated* MAS architectures, not structured sequential chains with boundary validation [21]. The practical lesson: design coordination explicitly; the magnitude of amplification is an organizational property, not a fixed constant.

**Bottom line:** Most skill chain failures are design failures, not execution failures. Fix them at the architecture level (explicit contracts, traces, termination conditions) not the prompt level.

---

### SQ6: Framework implementations

All major frameworks converge on the same four to five fundamental patterns (HIGH confidence): **sequential/pipeline**, **concurrent/broadcast**, **handoff** (dynamic control transfer), and **orchestrator-with-specialists** (supervisor calls specialist as tool). These are stable patterns; specific APIs are not — LangGraph, Semantic Kernel, and LlamaIndex all had significant releases in late 2025.

Key design choices that differ across frameworks:

- **Routing mechanism:** LangChain uses tool-call-based handoffs with explicit LangGraph `Command` objects [5]; Semantic Kernel uses a unified invocation interface across all patterns [6]; LlamaIndex starts with linear swarm logic and escalates to orchestrator patterns as complexity grows [8]; OpenAI SDK distinguishes LLM-driven vs code-driven orchestration [9].
- **Claude Code:** Description-driven routing — no hard-coded chain sequence, skill descriptions serve as the routing contract. Progressive disclosure (3-level: metadata → instructions → resources) minimizes context cost [3, 17].
- **n8n/workflow platforms:** Sequential chaining with explicit error-handling nodes; emphasis on observable, debuggable step-by-step execution [10].

Cross-framework takeaway: the choice of orchestration pattern is a design decision with explicit tradeoffs, not a technical implementation detail. The frameworks that perform best are those that make pattern selection explicit and provide observability at the pattern boundary.

**Bottom line:** Patterns are converging. Pick the simplest pattern that fits your workflow topology; migrate toward richer patterns only when simpler ones demonstrably fail. Claude Code's description-driven routing is a divergence from all other frameworks — good for discovery, brittle for guaranteed sequencing.

---

### SQ7: Tooling and evaluation techniques

The most validated evaluation practices (HIGH confidence from T1 sources [4]):

- **Grade outcomes, not paths.** Agents find valid solutions through unanticipated approaches; grading only the final state avoids false negatives [4].
- **Isolate trials.** Start each trial from a clean environment to eliminate infrastructure noise [4].
- **Three-tier testing:** Unit (individual skill), integration (two-skill handoff), end-to-end (full chain with environmental outcomes).
- **Observability is primary.** Step-through traces that show full conversation history, tool decisions, and intermediate results per turn are the only reliable debugging tool for sequential chains [4, 14].

pass@k is the dominant single metric (probability of at least one success in k attempts) but has documented statistical weaknesses: unstable rankings, high variance in small benchmarks, no uncertainty quantification [23]. For production harnesses, Bayes@N (posterior mean estimation with credible intervals) is a more statistically rigorous alternative [23]. pass^k (all k trials succeed) has no corroboration of adoption outside Anthropic's eval guide — treat as experimental.

LLM-as-judge calibration: start with a small human-curated golden dataset, fine-tune or few-shot prompt the judge until scores align with human ratings before using at scale [4].

**Bottom line:** Build traces first. Everything else in the evaluation stack is analysis of trace data. Evaluation harnesses that don't capture full step-by-step execution are debugging in the dark.

---

### SQ8: Implications for wos

wos has a functioning skill ecosystem where sequential patterns already occur informally (research → distill; brainstorm → write-plan → execute-plan). The gap is that these chains have no explicit contracts, no shared state schema, and no chain-level validation. The evidence points to six concrete improvements:

1. **Output contracts per skill** (HIGH priority). Each SKILL.md should declare: what structured output it produces and what it requires as input. This is the most-cited prerequisite across all frameworks and the only change that enables downstream skills to be built reliably against upstream outputs.

2. **Skill description precision** (HIGH priority, low effort). Claude Code routes by description matching. Descriptions should explicitly state what the skill produces, what it expects, and what skill logically follows. Currently most wos descriptions describe purpose but not handoff interface.

3. **Chain composition guide** (MEDIUM priority). Document the three to four canonical wos chain patterns with explicit selection criteria — analogous to LlamaIndex's "start with AgentWorkflow, escalate when needed" guidance.

4. **Idempotency markers** (MEDIUM priority). Skills should be designed to read plan checkbox state and skip already-completed stages. The plan file is already the shared state layer; skills should write to it and consult it.

5. **Chain-level audit** (MEDIUM priority). The audit-wos skill checks document quality. A complementary check that validates chain preconditions (e.g., distill was run on a verified research doc, not a DRAFT) would catch sequencing errors before they propagate.

6. **Evaluation harness** (LOWER priority for current scale). Given that wos chains are short (4–5 skills), interactive (human in the loop at every gate), and session-scoped rather than automated pipelines, the overhead of a full evaluation harness exceeds the failure surface it covers. Prioritize observability (transition logging in plan files) over formal test suites until chains become automated and unattended.

Behavioral drift across sessions (documented in arXiv 2602.22302 [25]) is a gap worth monitoring as the research pipeline grows. For now, human review at each gate is the mitigation.

**Bottom line:** Fix descriptions and output contracts first — both are zero-infrastructure changes with immediate impact on chain reliability. Chain composition documentation and idempotency markers are the next tier. A formal evaluation harness is premature given wos's interactive execution model.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "Unstructured multi-agent networks amplify errors up to 17.2 times compared to single-agent baselines." | statistic | [21] | corrected — the 17.2× figure applies specifically to fully *independent* (zero-communication) MAS architectures; centralized coordination yields 4.4×, hybrid 5.1×, decentralized 7.8×. The document's Findings SQ5 notes this caveat, but the raw figure appears without qualifier in the Extracts section. |
| 2 | "Typed schemas are table stakes in multi-agent workflows. Without them, nothing else works." | quote | [15] | verified — the GitHub Blog article by Gwen Davis contains this exact phrasing. |
| 3 | "The Microsoft Azure taxonomy — sequential, concurrent, handoff, group-chat, magentic — is the closest to a cross-vendor framework vocabulary." | superlative | [7] | human-review — the Azure page (ms.date: 2026-02-12) confirms the taxonomy exists; the "closest to shared standard" claim is an editorial judgment with no comparative evidence. The SoK paper [24] offers an alternative academic taxonomy. |
| 4 | "ReAct: First introduced in the 2023 paper 'ReACT: Synergizing Reasoning and Acting in Language Models'." | attribution | [12, 20] | corrected — the paper was submitted to arXiv in October 2022 and published at ICLR 2023. The correct characterization is "2022 arXiv preprint, published at ICLR 2023," not simply "the 2023 paper." |
| 5 | "pass@k measures the likelihood that an agent gets at least one correct solution in k attempts." | attribution | [4] | verified — the Anthropic eval guide (published Jan 09, 2026) contains this definition verbatim. |
| 6 | "pass^k measures the probability that all k trials succeed." | attribution | [4] | verified — confirmed in the same Anthropic eval guide page. |
| 7 | "Stateful patterns (handoffs, skills) save 40–50% of calls on repeat requests by maintaining context." | statistic | [5] | verified — the LangChain blog article (Jan 14, 2026) contains this performance comparison in a table of pattern behaviors. |
| 8 | "14 distinct failure modes" organized into the MASFT taxonomy across 3 primary categories. | attribution | [13] | verified — the arXiv 2503.13657v1 paper explicitly introduces the Multi-Agent System Failure Taxonomy (MASFT) with 14 failure modes in 3 categories. |
| 9 | Prompt/prompt-fix interventions in ChatDev yielded only "+14% improvement." | statistic | [13] | corrected — the paper reports ChatDev improved from 25.0% baseline to 40.6% after topology interventions, a ~15.6 percentage point gain. The "+14%" figure is an approximation; the actual reported number is closer to +16pp. |
| 10 | "An agent in an infinite loop can burn thousands of dollars of API credits in minutes." | attribution | [19] | human-review — the orq.ai source (Source 19) was verified as reachable but does not contain this specific claim. The claim is attributed to "search synthesis / orq.ai" in the document; no listed source independently confirms the exact phrasing or the specific dollar figure. |
| 11 | A two-agent recursive loop ran 11 days undetected, generating a $47,000 API bill. | statistic | none listed | human-review — cited as "search synthesis" with no numbered source; no listed source confirms this specific incident. The cost magnitude is directionally consistent with documented runaway API costs but cannot be traced to a verifiable report. Remove or replace with a sourced incident before finalizing. |
| 12 | "Agents regularly find valid approaches that eval designers didn't anticipate. So as not to unnecessarily punish creativity, it's often better to grade what the agent produced, not the path it took." | quote | [4] | verified — the Anthropic eval guide covers grading outcomes over paths as a core principle. |
| 13 | The SoK paper defines an agentic skill as a four-tuple S = ⟨C, π, T, R⟩ (applicability condition, policy, termination condition, reusable interface). | attribution | [24] | verified — arXiv 2602.20867 contains this exact Definition 1 formulation in Section II-A. |
| 14 | "Under matched thinking-token budgets, single-agent systems consistently match or outperform multi-agent systems on multi-hop reasoning tasks." | attribution | [22] | verified — arXiv 2604.02460v1 confirms this as the paper's core finding across FRAMES and MuSiQue datasets. |
| 15 | pass@k "yields unstable rankings with high variance" and "has no principled decision rule for whether observed gaps are meaningful." | attribution | [23] | verified — arXiv 2510.04265v1 (Don't Pass@k) documents these weaknesses and proposes Bayes@N as an alternative. |
| 16 | "Multi-agent LLM systems exhibit measurable behavioral degradation over extended interactions — outputs drift from intended specifications even when schemas are in place." | attribution | [25] | verified — arXiv 2602.22302 (Agent Behavioral Contracts) confirms behavioral drift as a distinct failure mode and introduces a behavioral drift score metric; explicitly notes drift occurs even with schemas enforced. |
| 17 | Claude Code progressive disclosure has three levels: Level 1 (~100 tokens, metadata always loaded), Level 2 (under 5k tokens, instructions on trigger), Level 3 (resources loaded as needed). | attribution | [3] | verified — the Agent Skills Overview page (platform.claude.com) contains a table with these exact level descriptions and token costs. |
| 18 | "Claude Opus 4.6 has a strong predilection for subagents and may spawn them in situations where a simpler, direct approach would suffice." | quote | [2] | verified — this exact language appears in the Anthropic Prompting Best Practices page under the subagent orchestration section. |
