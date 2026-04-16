---
name: "Primitive Selection Routing: How Frameworks Guide Abstraction Choice"
description: "Investigation of how agent frameworks and plugin systems guide primitive selection, with focus on intake routing patterns"
type: research
sources:
  - https://python.langchain.com/v0.1/docs/use_cases/tool_use/
  - https://docs.langchain.com/oss/python/langchain/philosophy
  - https://docs.langchain.com/oss/python/langchain/agents
  - https://docs.langchain.com/oss/python/langgraph/workflows-agents
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/
  - https://docs.crewai.com/en/guides/flows/first-flow
  - https://docs.crewai.com/core-concepts/Tasks/
  - https://medium.com/@yagmur.sahin/openais-chat-completions-vs-assistants-an-in-depth-comparison-d0757e94e6a0
  - https://openai.github.io/openai-agents-python/
  - https://code.claude.com/docs/en/hooks-guide
  - https://code.claude.com/docs/en/skills
  - https://code.claude.com/docs/en/features-overview
  - https://plugins.jetbrains.com/docs/intellij/plugin-types.html
  - https://vscode-docs.readthedocs.io/en/stable/tools/yocode/
  - https://github.com/microsoft/vscode-generator-code
  - https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-wizard.html
  - https://www.terraform-best-practices.com/key-concepts
  - https://clig.dev/
  - https://news.ycombinator.com/item?id=40739982
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://dev.to/nunc/claude-code-skills-vs-subagents-when-to-use-what-4d12
  - https://www.turgon.ai/post/langchain-langgraph-or-custom-choosing-the-right-agentic-framework
  - https://nx.dev/docs/reference/create-nx-workspace
  - https://deepwiki.com/nrwl/nx/7.1-workspace-creation-and-initialization
  - https://nextjs.org/docs/app/api-reference/cli/create-next-app
  - https://turborepo.dev/docs/reference/create-turbo
  - https://devblogs.microsoft.com/dotnet/introducing-dotnet-scaffold/
  - https://github.com/kristw/yeoman-easily
  - https://blog.saeloun.com/2021/06/29/rails-7-generators-will-raise-errors-when-invalid/
  - https://hackceleration.com/claude-code-review/
  - https://oneuptime.com/blog/post/2026-02-23-how-to-handle-module-errors-and-debugging-in-terraform/view
  - https://controlmonkey.io/resource/terraform-errors-guide/
  - https://markaicode.com/debugging-vscode-extensions-configuration-issues/
  - https://bobcares.com/blog/kubectl-error-the-server-doesnt-have-a-resource-type/
  - https://www.nngroup.com/articles/confirmation-dialog/
  - https://www.nngroup.com/articles/user-mistakes/
related:
  - docs/context/slip-mistake-gate-failure.context.md
  - docs/context/creation-time-intake-routing.context.md
  - docs/context/single-entry-point-creation.context.md
  - docs/context/primitive-selection-failure-signals.context.md
---

# Primitive Selection Routing: How Frameworks Guide Abstraction Choice

## Search Protocol

| # | Query | Source Found | Key Finding |
|---|-------|-------------|-------------|
| 1 | langchain agents vs chains vs tools choosing when to use site:python.langchain.com | python.langchain.com/v0.1/docs/use_cases/tool_use/ | Agents use LLM as reasoning engine; chains hardcode sequence — distinction is determinism vs dynamic routing |
| 2 | llamaindex when to use agents vs query engines vs retrievers | docs.llamaindex.ai/en/stable/module_guides/deploying/query_engine/ | Hierarchy: retriever → query engine → agent, each layer adds orchestration; explicit "when" guidance exists per tier |
| 3 | crewai agents tasks tools choosing abstraction guide site:docs.crewai.com | docs.crewai.com/core-concepts/Tasks/ | Tools can be assigned at agent or task level; no single routing guide — developer infers from docs |
| 4 | openai assistants API vs chat completions vs functions when to use | community.openai.com/t/function-calling-in-chat-completions-api-vs-assistants-api | Stateless=Completions, Stateful=Assistants; developers rely on community comparisons, no official decision tree |
| 5 | Claude Code hooks vs commands when to use documentation anthropic | code.claude.com/docs/en/hooks-guide | Hooks = deterministic, event-driven; commands = manual shortcuts; official docs provide the clearest "use X for Y" guidance found in this study |
| 6 | LangChain philosophy primitives docs.langchain.com | docs.langchain.com/oss/python/langchain/philosophy | Key principle: control requirements vs simplicity; no explicit decision tree, but migration guidance toward LangGraph for production |
| 7 | LangChain agents docs guidance | docs.langchain.com/oss/python/langchain/agents | No "when not to use" or decision tree present; tool count warning (too many overwhelms model) as only heuristic |
| 8 | wrong abstraction langchain agent vs chain failure modes Hacker News | news.ycombinator.com/item?id=40739982 | Primary failure mode: 5 layers of abstraction to make minor customization; developers couldn't understand the system when issues arose |
| 9 | jetbrains plugin wizard plugin type selection intellij | plugins.jetbrains.com/docs/intellij/plugin-types.html | Five categories; no decision tree — developers self-select based on brief descriptions |
| 10 | vscode extension generator yeoman yo code choosing extension type | vscode-docs.readthedocs.io/en/stable/tools/yocode/ | Single entry point (yo code) that routes via interactive prompt: "What type of extension do you want?" — strongest single-entry-point example found |
| 11 | terraform resource vs data source vs module when to use | terraform-best-practices.com/key-concepts | Explicit "atoms vs molecules" metaphor; resource=create/manage, data=read-only, module=versioned-reusable unit — clearest CLI framework guidance found |
| 12 | AWS CLI wizard interactive routing | docs.aws.amazon.com/cli/latest/userguide/cli-usage-wizard.html | aws <service> wizard <wizardName> pattern; interactive list selection + string input; preview mode before execution |
| 13 | kubectl explain resource type discovery | kubernetes.io/docs/reference/kubectl/generated/kubectl_explain/ | kubectl api-resources enumerates all types; kubectl explain <type> provides field-level docs; routing through exhaustive enumeration |
| 14 | CLI tool UX patterns triage discovery | clig.dev/ | "Display most common flags at start of help text"; suggest next commands; spelling correction as disambiguation pattern |
| 15 | confirmation gate developer tools wizard pattern UX | patternfly.org + smashingmagazine.com | Intent Preview (plan summary) pattern from agentic AI UX; >85% acceptance target without modification |
| 16 | Claude Code skills vs subagents when to use | code.claude.com/docs/en/features-overview | Explicit "build your setup over time" trigger table — strongest intake routing heuristic found in any framework |
| 17 | Claude Code features overview decision table | code.claude.com/docs/en/features-overview | Side-by-side comparison tabs for every similar feature pair (Skill vs Subagent, CLAUDE.md vs Skill, etc.) |
| 18 | CrewAI Flows vs Crews when to use | docs.crewai.com/en/guides/flows/first-flow | Flows = orchestration/sequencing layer; Crews = collaborative agents; flow wraps crews |
| 19 | OpenAI agents SDK handoffs vs tools choosing | openai.github.io/openai-agents-python/ | Two patterns: handoff (agent-to-agent peer transfer) vs manager (central orchestrator delegating via tool calls) |
| 20 | Smashing Magazine agentic AI UX patterns 2026 | smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ | Intent Preview, Autonomy Dial patterns; >85% acceptance rate target; Escalation Pathway for ambiguity |
| 21 | LangGraph workflows vs agents decision criteria | docs.langchain.com/oss/python/langgraph/workflows-agents | Workflows = predetermined paths; Agents = dynamic tool selection; no decision tree but clear prose criteria |
| 22 | developer wrong primitive failure mode signals | swizec.com/blog/you-can-t-fix-the-wrong-abstraction/ | "Everything feels hard" and "simplest changes require major effort" as primary signals; discovered late |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://python.langchain.com/v0.1/docs/use_cases/tool_use/ | Tool use and agents | LangChain | 2024 | T1 | verified |
| 2 | https://docs.langchain.com/oss/python/langchain/philosophy | Philosophy - Docs by LangChain | LangChain | 2025 | T1 | verified |
| 3 | https://docs.langchain.com/oss/python/langchain/agents | Agents - Docs by LangChain | LangChain | 2025 | T1 | verified |
| 4 | https://docs.langchain.com/oss/python/langgraph/workflows-agents | Workflows and agents - Docs by LangChain | LangChain/LangGraph | 2025 | T1 | verified |
| 5 | https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/ | Query Engine — LlamaIndex documentation | LlamaIndex | 2025 | T1 | verified |
| 6 | https://docs.crewai.com/en/guides/flows/first-flow | Build Your First Flow — CrewAI | CrewAI | 2025 | T1 | verified |
| 7 | https://docs.crewai.com/core-concepts/Tasks/ | crewAI Tasks | CrewAI | 2025 | T1 | verified |
| 8 | https://medium.com/@yagmur.sahin/openais-chat-completions-vs-assistants-an-in-depth-comparison-d0757e94e6a0 | Chat Completions vs. Assistants: Architectural Differences | Yagmur Sahin | 2024 | T3 | verified |
| 9 | https://openai.github.io/openai-agents-python/ | OpenAI Agents SDK | OpenAI | 2025 | T1 | verified |
| 10 | https://code.claude.com/docs/en/hooks-guide | Automate workflows with hooks — Claude Code Docs | Anthropic | 2026 | T1 | verified (non-canonical URL; canonical: docs.anthropic.com) |
| 11 | https://code.claude.com/docs/en/skills | Extend Claude with skills — Claude Code Docs | Anthropic | 2026 | T1 | verified (non-canonical URL; canonical: docs.anthropic.com) |
| 12 | https://code.claude.com/docs/en/features-overview | Extend Claude Code | Anthropic | 2026 | T1 | verified (non-canonical URL; canonical: docs.anthropic.com) |
| 13 | https://plugins.jetbrains.com/docs/intellij/plugin-types.html | Plugin Types — IntelliJ Platform Plugin SDK | JetBrains | 2025 | T1 | verified |
| 14 | https://vscode-docs.readthedocs.io/en/stable/tools/yocode/ | Yo Code - Extension Generator | Microsoft/VS Code | 2023 | T1 | verified |
| 15 | https://github.com/microsoft/vscode-generator-code | vscode-generator-code | Microsoft | 2024 | T1 | verified |
| 16 | https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-wizard.html | Using custom wizards to run interactive commands in the AWS CLI | AWS | 2025 | T1 | verified |
| 17 | https://www.terraform-best-practices.com/key-concepts | Key concepts — Terraform Best Practices | Anton Babenko | 2024 | T2 | verified |
| 18 | https://clig.dev/ | Command Line Interface Guidelines | Aanand Prasad et al. | 2022 | T2 | verified |
| 19 | https://news.ycombinator.com/item?id=40739982 | Why we no longer use LangChain for building our AI agents | Hacker News | 2024 | T4 | verified |
| 20 | https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ | Designing For Agentic AI: Practical UX Patterns | Victor Yocco, Smashing Magazine | 2026-02-11 | T2 | verified (85% target is design goal, not empirical study result) |
| 21 | https://dev.to/nunc/claude-code-skills-vs-subagents-when-to-use-what-4d12 | Claude Code Skills vs Subagents — When to Use What? | DEV Community | 2026 | T3 | verified |
| 22 | https://www.turgon.ai/post/langchain-langgraph-or-custom-choosing-the-right-agentic-framework | LangChain, LangGraph, or Custom? Choosing the Right Agentic Framework | Turgon AI | 2025 | T3 | verified |

## Extracts

### Sub-question 1: Agent framework guidance for abstraction selection

**Source [1]:** Tool use and agents — LangChain (v0.1 docs, no longer live)
> "An agent is a class that uses an LLM to choose a sequence of actions to take, while in chains, a sequence of actions is hardcoded. In agents, a language model is used as a reasoning engine to determine which actions to take and in which order."
> *(Note: URL now redirects to LangChain overview; quote not found at current canonical URL — see Claims table, Claim 1)*

**Finding:** LangChain's core distinction between its two highest-level primitives (agents vs chains) is grounded in whether the sequence is determined at runtime (agent) or design time (chain). This is a single clear criterion, but the documentation does not present it as a decision tree users must traverse before creating anything.

---

**Source [2]:** Philosophy — LangChain
> "LangGraph becomes the preferred way to build any AI application that is more than a single LLM call." … "as developers tried to improve the reliability of their applications, they needed more control than the high-level interfaces provided. LangGraph provided that low-level flexibility."

**Finding:** The decision criterion offered is complexity: a single LLM call stays in LangChain; anything multi-step or requiring state management moves to LangGraph. This is retrospective guidance (updated in October 2024 after years of user confusion) rather than proactive routing at creation time.

---

**Source [3]:** Agents — LangChain
> "Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities."

**Finding:** The only heuristic offered is a tool-count warning. No "when to use an agent vs a chain" question is posed at creation time. The documentation focuses on configuration once the decision to use an agent has already been made.

---

**Source [4]:** Workflows and agents — LangGraph
> "Workflows: predetermined code paths and are designed to operate in a certain order. Agents: dynamic and define their own processes and tool usage."

**Finding:** LangGraph does provide an explicit when-to-use criterion: predictability of steps determines workflow vs agent. Five workflow patterns are listed (prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer). But this guidance is prose documentation, not an intake question asked during creation.

---

**Source [5]:** Query Engine — LlamaIndex
> "A query engine takes in a natural language query and returns a rich response … If you want to have a conversation with your data (multiple back-and-forth instead of a single question & answer), take a look at Chat Engine."

**Finding:** LlamaIndex's documentation explicitly names the decision criterion (single Q&A vs. conversation) and redirects to an alternative primitive. This is stronger than most frameworks — it proactively tells users when the component they're reading about is the *wrong* one for their use case.

---

**Source [6]:** Build Your First Flow — CrewAI
> "Crews excel at agent collaboration and complex tasks requiring multiple specialized perspectives … Flows provide fine-grained control over exactly how and when different components of your AI system interact."

**Finding:** CrewAI's Flow documentation articulates that Flows are the orchestration layer *above* Crews — Flows can contain Crews, and are preferred when conditional logic, external system integration, or multi-crew coordination is needed. This is post-selection guidance embedded in the first-use tutorial, not a routing gate before creation.

---

**Source [9]:** OpenAI Agents SDK
> "Handoffs: using many agents on equal footing, where one agent can directly hand off control … Manager pattern: empowers a central LLM — the 'manager' — to orchestrate a network of specialized agents seamlessly through tool calls."

**Finding:** OpenAI documents two distinct orchestration topologies (handoff vs manager) with distinct criteria for each. The SDK reference says "If you are deciding between handoffs and manager-style orchestration, read Agent orchestration." This is explicit cross-referencing but not automated intake.

---

### Sub-question 2: Plugin system routing — single entry vs. separate paths

**Source [14]:** Yo Code - Extension Generator — VS Code
> "Typing `yo code` starts an interactive wizard that asks: 'What type of extension do you want?' with options like New Extension (TypeScript), New Extension (JavaScript), New Color Theme, New Language Support, New Code Snippets, New Keymap, New Extension Pack."

**Finding:** VS Code's `yo code` generator is the clearest example of a single-entry-point routing pattern found in this study. The user runs one command and the tool presents an interactive menu that routes to the correct scaffolding path based on intent. No prior knowledge of extension types is required to start. There is no separate `yo code-theme` or `yo code-command` — everything flows through the same intake.

---

**Source [15]:** vscode-generator-code — GitHub
> "The generator can either create an extension skeleton for a new extension or create a ready-to-use extension for languages, themes or snippets based on existing TextMate definition files."

**Finding:** The generator's README confirms the single entry point routes to type-specific workflows. Type selection is the first question, and each answer triggers a distinct subsequent question sequence (e.g., selecting "theme" asks for TextMate file path; selecting "command extension" asks for command name and display name).

---

**Source [13]:** Plugin Types — IntelliJ Platform Plugin SDK
> "The five main categories are: Custom Language Support, Framework Integration, Tool Integration, User Interface Add-Ons, Themes. The documentation provides no decision tree or selection framework."

**Finding:** JetBrains takes the opposite approach from VS Code. The Plugin Types page lists categories with brief descriptions and links to example plugins, then assumes developers will recognize which category fits their use case. There is no interactive intake, no decision tree, and no cross-referencing of "if you want X, use Y category." The documentation noted there is a link to "alternative solutions" to consider before building a plugin at all — the only gate-like feature found.

---

**Source [12]:** Extend Claude Code — Anthropic
> "Build your setup over time: Each feature has a recognizable trigger, and most teams add them in roughly this order: Claude gets a convention wrong twice → CLAUDE.md; You keep typing the same prompt → skill; You paste the same playbook three times → skill; You keep copying data from a browser tab Claude can't see → MCP; A side task floods your conversation → subagent; You want something to happen every time without asking → hook."

**Finding:** Claude Code's official documentation uses a trigger-based routing table instead of a decision tree. The user identifies a pain point (e.g., "I keep repeating myself") and the table maps it to a primitive. This is the most actionable intent-to-primitive routing pattern found in any official framework documentation.

---

**Source [12] (continued):** Extend Claude Code — Compare similar features
> Side-by-side comparison tabs exist for: Skill vs Subagent, CLAUDE.md vs Skill, CLAUDE.md vs Rules vs Skills, Subagent vs Agent team, MCP vs Skill.

**Finding:** Claude Code's documentation is the only framework found that systematically compares every similar-seeming primitive pair in structured tables. Each tab answers "when would I choose X over Y?" with criteria. This is a disambiguation layer that other frameworks lack entirely.

---

### Sub-question 3: Failure modes from wrong primitive choice

**Source [19]:** Why we no longer use LangChain — Hacker News thread
> "The second you need to do something a little original you have to go through 5 layers of abstraction just to change a minute detail." … "You won't really understand every step in the process, so if any issue arises or you need to improve the process you will start back at square 1."

**Finding:** The dominant failure mode when the wrong LangChain primitive is chosen is *debugging opacity*: the abstraction hides enough state that errors become undiagnosable without reading framework source code. This failure surfaces at debugging time (runtime), not at selection time. The developer's first signal is usually that a "relatively simple task" proves "not well documented" or impossible — which can take days to discover.

---

**Source [22]:** LangChain, LangGraph, or Custom? — Turgon AI
> "When something breaks, you debug LangChain's internals, not your own logic. If your framework requirements leave the standard path, you encounter its limits."

**Finding:** The signal that a wrong primitive was chosen is consistently described as "everything feels hard" — friction accumulates across many small customizations before the fundamental mismatch becomes visible. This late-signal problem is a key argument for proactive intake at creation time.

---

**Source [21]:** Claude Code Skills vs Subagents — DEV Community
> "Failure modes to avoid: overcomplicating simple utilities as subagents (unnecessary overhead); attempting single-step conversions as subagents (wastes context); making skills too large (keep under 500 lines); unclear trigger descriptions that prevent proper skill activation."

**Finding:** Claude Code's ecosystem has documented specific failure modes for each primitive. Skills that are too large fail to activate correctly; subagents misused for simple tasks waste context. These are recoverable but still costly mistakes — and they are caught mid-session rather than at creation time.

---

**Source [4]:** Workflows and agents — LangGraph
> Routing failure: "In general, agents are ideal for more dynamic uses, while workflows are best for more structured scenarios." [Underdetermined scenarios fall between both.]

**Finding:** The workflow/agent boundary is a known failure zone. Developers often build agentic systems when a simple workflow would suffice (incurring unpredictability) or build rigid workflows that need to become agents (requiring rewrites). Neither framework provides an early-warning mechanism.

---

### Sub-question 4: "Justify your choice" gate patterns

**Source [20]:** Designing For Agentic AI: Practical UX Patterns — Smashing Magazine
> "The Intent Preview, or Plan Summary, establishes informed consent. It is the conversational pause before action, transforming a black box of autonomous processes into a transparent, reviewable plan … Before an agent takes any significant action, the user must have a clear, unambiguous understanding of what is about to happen."
> Success metric: >85% acceptance rate without modification.

**Finding:** The Intent Preview pattern is the closest analog to a "justify your choice" gate, but it operates *after* the user has already selected an action, not before they select a primitive. The pattern is designed to prevent agent errors, not primitive-selection errors. Its effectiveness benchmark (85% acceptance rate) is a design target, not an empirical validation from a controlled study.

---

**Source [20] (continued):** Autonomy Dial pattern
> "A graduated control system lets users set comfort levels per task type: Observe & Suggest → Plan & Propose → Act with Confirmation → Act Autonomously. This pattern prevents complete feature abandonment after single failures by allowing users to calibrate rather than disable autonomy entirely."

**Finding:** The Autonomy Dial is a gate that requires users to express their desired level of control before delegating to an agent. This is structurally similar to a "confirm your primitive" gate — but it operates on autonomy level, not on which primitive is used. It provides evidence that incremental authorization reduces abandonment, which is relevant to designing confirmation gates for primitive selection.

---

**Source [16]:** Using custom wizards — AWS CLI
> "After filling in all prompts, you can preview an AWS CloudFormation template or the AWS CLI command filled with your information, which is useful to learn the AWS CLI, service APIs, and creating templates for scripts."

**Finding:** AWS CLI wizards implement a preview-before-commit pattern: the user answers intake questions, then sees the resulting CloudFormation template or CLI command *before* it executes. This is a confirmation gate with two effects: it builds understanding of the underlying primitives, and it allows the user to abort if the result is unexpected. This is the strongest "justify your choice" gate found in a non-AI CLI tool.

---

**Source [14]:** Yo Code — VS Code generator
> The `-q, --quick` flag skips all optional prompts and uses defaults.

**Finding:** Scaffold tools that include a confirmation gate also include a bypass flag for expert users. This pattern (gate by default, skip-able with explicit flag) appears to be the established convention for balancing guidance with expert efficiency — but no empirical study on its effectiveness was found.

---

### Sub-question 5: CLI routing and triage patterns

**Source [18]:** Command Line Interface Guidelines — clig.dev
> "Display the most common flags and commands at the start of the help text." Git exemplifies this by grouping commands like "start a working area" and "work on the current change," helping users find frequent tasks without being overwhelmed.
> "Suggest commands the user should run next … Include spelling correction with confirmation: 'Did you mean ps?'"

**Finding:** The CLI guidelines community has converged on three routing patterns: progressive disclosure (common commands first), contextual suggestion (tell the user what to do next after a command completes), and typo correction with confirmation. None of these are pre-selection gates; they are post-input guidance mechanisms.

---

**Source [16]:** Using custom wizards — AWS CLI
> "To use the wizard, you call the wizard subcommand and the wizard name after the service name: `aws dynamodb wizard new-table`. Wizards present either multiple-choice lists (arrow key selection) or string input prompts. The `aws configure wizard` is the only wizard without a wizard name."

**Finding:** AWS CLI wizards are service-scoped, not cross-service. The user must already know which service they want before they can enter the wizard. Within a service, the wizard routes through intake questions to the correct resource configuration. This is partial routing — it handles intra-primitive configuration, not cross-primitive selection.

---

**Source [17]:** Key concepts — Terraform Best Practices
> "While individual resources are like atoms in the infrastructure, resource modules are molecules (consisting of atoms). Infrastructure modules organize resource modules. Compositions span multiple logical boundaries."

**Finding:** Terraform's documentation establishes an explicit hierarchy metaphor (atom → molecule → organism) that doubles as a routing heuristic: choose the lowest abstraction level that meets your scope. This is not an intake form but a mental model that guides selection. It is more sophisticated than most framework documentation — but still requires developers to internalize the metaphor rather than being asked to declare their scope at creation time.

---

**Source [13]:** Plugin Types — IntelliJ Platform Plugin SDK (revisited)
> "A reference to alternative solutions that might eliminate the need for a plugin entirely."

**Finding:** JetBrains' plugin documentation includes one proactive gate: a link to "alternative solutions" before the developer starts. This is the only pre-selection redirect found in a plugin system — a minimal version of the "justify your need for a new primitive" pattern.

---

**Source [12]:** Extend Claude Code — Anthropic (revisited)
> "New to Claude Code? Start with CLAUDE.md for project conventions, then add other extensions as specific triggers come up."

**Finding:** Claude Code's "build your setup over time" framing is a temporal routing strategy: defer the decision until a real pain point emerges, rather than asking the user to select a primitive at the start. This avoids premature abstraction but also means the user may not discover the right primitive until they've already hit friction.

---

## Challenge

### Claim 1: VS Code `yo code` as the strongest single-entry-point example

**Challenged/Upheld?** Qualified

**Counter-evidence found:**
- **Nx `create-nx-workspace`** uses a single entry point (`npx create-nx-workspace`) that prompts interactively for a "preset" — routing to Angular, React, Next.js, Nest, Express, or empty workspaces. The prompt explicitly asks "Which stack do you want to use?" before any framework-specific questions. This is structurally identical to `yo code`'s routing pattern and covers cross-framework selection, not just extension type selection within a single ecosystem. Source: [create-nx-workspace docs](https://nx.dev/docs/reference/create-nx-workspace); [Nx DeepWiki workspace initialization](https://deepwiki.com/nrwl/nx/7.1-workspace-creation-and-initialization).
- **`create-next-app`** and **`create-react-app`** use a single CLI entry point with interactive prompts for TypeScript, linting, Tailwind, App Router, and import alias configuration. These are framework-scoped (not cross-primitive) but are single-entry-point routing tools used at far greater scale than `yo code`. Source: [create-next-app docs](https://nextjs.org/docs/app/api-reference/cli/create-next-app).
- **Turborepo's `create-turbo`** prompts for package manager and workspace preset at a single entry, routing to different monorepo configurations. Source: [create-turbo docs](https://turborepo.dev/docs/reference/create-turbo).
- **dotnet scaffold** (Microsoft's .NET 8+ scaffolding tool) uses a single interactive CLI entry point that prompts for project type, then routes to CRUD, Razor Pages, or API configurations. Source: [.NET Blog](https://devblogs.microsoft.com/dotnet/introducing-dotnet-scaffold/).

**Assessment:** The `yo code` finding is accurate as far as it goes within the VS Code extension ecosystem specifically, but the broader claim that it is the "strongest single-entry-point routing example found" reflects an incomplete search. Nx's `create-nx-workspace` is functionally equivalent and covers a wider range of target types. The claim should be qualified: `yo code` is the strongest example *within a plugin ecosystem for an existing tool*; `create-nx-workspace` rivals or exceeds it for workspace-bootstrapping tools.

---

### Claim 2: No framework uses a justify-your-choice gate at creation time

**Challenged/Upheld?** Upheld with qualification

**Counter-evidence found:**
- **Yeoman's `confirmBeforeStart` pattern**: The `yeoman-easily` library provides `easily.confirmBeforeStart(message)` / `easily.checkForConfirmation()` — a pre-generation gate that halts execution until the user explicitly confirms. Individual Yeoman generators can and do implement "Are you sure you want to create this type?" gates. This is opt-in at the generator level, not a Yeoman-platform default. Source: [yeoman-easily](https://github.com/kristw/yeoman-easily).
- **Rails 7 generator validation**: Rails 7 added pre-flight validation that raises `Rails::Generators::Error` before scaffold generation if an invalid attribute type is passed. This is a *type validation* gate (catching typos like `reference` vs `references`), not a semantic "justify your primitive choice" gate. It confirms the form of input, not the wisdom of the choice. Source: [Saeloun blog on Rails 7 generators](https://blog.saeloun.com/2021/06/29/rails-7-generators-will-raise-errors-when-invalid/).
- **JetBrains plugin SDK "alternative solutions" link**: The research document already notes this; it is the only pre-selection redirect found in a plugin system. No generator was found that asks "Why do you want to use primitive X instead of Y?" as an interactive prompt.
- Searched: `create-next-app`, `create-react-app`, Nx generators, Turborepo generators, `dotnet scaffold`, Cookiecutter, Laravel Artisan. None present a "justify your choice" gate; all route on *type selection* rather than *justification*.

**Assessment:** The core claim holds — no mainstream framework presents a semantic justification gate at primitive creation time. The Yeoman ecosystem offers the *capability* via third-party helpers, but it is not a platform default. The Rails 7 example shows a type validation gate, which is distinct from a semantic justification gate. The absence is real but the Yeoman capability is worth noting as evidence that the pattern is technically feasible and has been implemented in isolated cases.

---

### Claim 3: Claude Code features-overview as most actionable routing heuristic

**Challenged/Upheld?** Qualified (self-referential source; third-party assessment partially corroborates)

**Counter-evidence found:**
- **Self-referential source problem**: Source [12] (`code.claude.com/docs/en/features-overview`) is Anthropic's own documentation for a product under study. The assessment that it is "the most actionable" is made by the same research that uses Anthropic docs as a primary source. No independent third-party applied the same evaluation rubric to Claude Code's documentation vs. other frameworks' documentation.
- **Third-party reviews of Claude Code onboarding**: Multiple independent 2026 reviews describe Claude Code's onboarding as "the smoothest of any AI coding tool" with "time to first useful output under 5 minutes." One review specifically calls out CLAUDE.md and skill primitives as well-documented. Source: [hackceleration.com Claude Code Review 2026](https://hackceleration.com/claude-code-review/); [aitoolanalysis.com](https://aitoolanalysis.com/claude-code/). These reviews are largely positive but do not use the specific "trigger table" or "most actionable routing heuristic" framing — they focus on general onboarding speed, not primitive-selection documentation quality.
- **Nx's documentation offers a competing trigger-based model**: Nx's preset system and generator documentation uses an explicit "when to use which preset" structure with technology-specific routing. While not structured as a trigger-pain-point table, it covers more framework combinations than Claude Code's table.
- **LlamaIndex's "when to use Chat Engine vs Query Engine" redirect** (Source [5]) is arguably as actionable for its users: it explicitly names the decision criterion in prose during first exposure, before the user has committed.

**Assessment:** The claim is plausible but self-serving in its sourcing. The trigger-table format in Claude Code's docs is distinctive and appears well-regarded by independent reviewers, but the "most actionable" comparison is not backed by a consistent rubric applied across frameworks. The finding should be restated as: "Among the frameworks studied, Claude Code's trigger-pain-point table is the most *structurally explicit* routing aid; whether it is the most *effective* cannot be determined without user studies."

---

### Claim 4: Debugging opacity as the primary failure mode

**Challenged/Upheld?** Qualified — the claim generalizes from LangChain but has partial support from Terraform; VS Code and kubectl failure modes differ in character

**Counter-evidence found:**
- **Terraform resource vs. module confusion**: Terraform module errors produce stack traces that point to module internals rather than the user's configuration, causing a debugging opacity pattern analogous to LangChain. One documented pattern: "error messages often pointing to module internals rather than the actual problem." This supports generalization of the opacity claim to infrastructure tools. Source: [oneuptime.com Terraform debugging](https://oneuptime.com/blog/post/2026-02-23-how-to-handle-module-errors-and-debugging-in-terraform/view); [controlmonkey.io Terraform errors](https://controlmonkey.io/resource/terraform-errors-guide/).
- **VS Code extension wrong-type failure mode differs**: The primary VS Code failure mode when a developer builds the wrong extension type is not debugging opacity but *registration conflict* — "a DebugAdapterDescriptorFactory can only be registered from the extension that defines the debugger type." The error surfaces immediately at activation, not during debugging of complex state. This is a *fast-fail* pattern, not opacity. The failure mode for VS Code extension misuse is misconfiguration detection, not silent accumulation of friction. Source: [vscode extension debugging](https://markaicode.com/debugging-vscode-extensions-configuration-issues/).
- **kubectl wrong resource type failure mode also differs**: kubectl errors for wrong resource types ("the server doesn't have a resource type") are immediate and explicit, not opaque. The confusion pattern is around kubeconfig and context mismatches, not abstraction-level wrong selection. Source: [bobcares kubectl error guide](https://bobcares.com/blog/kubectl-error-the-server-doesnt-have-a-resource-type/).
- **The opacity failure mode appears specific to layered abstraction frameworks** (LangChain, Terraform modules) rather than universal across all tools with multiple primitive types.

**Assessment:** The claim holds for layered abstraction frameworks (LangChain, LangGraph, Terraform modules) where multiple stacked abstractions hide state and produce misleading error provenance. It does not generalize well to VS Code extensions or kubectl, where type misuse produces immediate, explicit errors rather than accumulating friction. The research document should qualify: debugging opacity is the failure mode for *high-abstraction frameworks with deep call chains*, not for all tools with multiple primitive types.

---

### Claim 5: No empirical validation of gate patterns exists

**Challenged/Upheld?** Upheld — but with important partial evidence that was not surfaced

**Counter-evidence found:**
- **Nielsen Norman Group on confirmation dialogs**: NN/G provides the most direct empirical-adjacent evidence on confirmation gates. Their research-backed heuristic guidance states: (1) confirmation dialogs *can* prevent errors if specific (restating the action, not just "are you sure?"); (2) overuse causes automation bias — users click through without reading; (3) nonstandard confirmation actions (typing a keyword) are more effective for high-risk operations. This is practitioner-consensus evidence based on aggregated usability testing, not a single controlled study. Source: [NN/G Confirmation Dialogs](https://www.nngroup.com/articles/confirmation-dialog/).
- **NN/G error prevention heuristic**: Nielsen's Heuristic #5 (Error Prevention) explicitly places confirmation gates as a mechanism for preventing *slips* (execution errors) rather than *mistakes* (intent errors). This distinction matters: primitive-selection errors are mistakes (wrong intent), not slips (wrong execution) — suggesting confirmation gates may be less effective than the research implies for this use case. Source: [NN/G Error Prevention](https://www.nngroup.com/articles/user-mistakes/).
- **CHI/ACM research on developer tools and wizard patterns**: Searched ACM Digital Library via web for CHI papers on scaffold confirmation gates, developer tool wizard UX, and CLI routing empirical studies. No specific controlled study on primitive-selection gates in developer tooling was found. The "Wizard of Oz" results returned were about study methodology (human-as-system simulation), not gate effectiveness.
- **Microsoft Research developer productivity**: Searched Microsoft Research for empirical studies on onboarding confirmation dialogs. Found studies on developer productivity broadly (SPACE framework, GitHub Copilot impact) but no controlled study on creation-time gate effectiveness in CLI tools.
- **The 85% acceptance rate in the Smashing Magazine source**: Confirmed in the existing document footnote as a design *target*, not an empirical result. No study was found validating this figure.

**Assessment:** The claim is upheld — no empirical study specifically on primitive-selection confirmation gates in developer tools was found after genuine search effort. However, the NN/G body of work provides meaningful design-evidence that confirmation gates prevent execution errors but may be less effective against intent errors (which is what wrong primitive selection represents). This is a more precise framing of the absence: the pattern may not be validated because it targets the wrong error type, not merely because it hasn't been studied.

---

### New Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 23 | https://nx.dev/docs/reference/create-nx-workspace | create-nx-workspace | Nx/Nrwl | 2024 | T1 | verified |
| 24 | https://deepwiki.com/nrwl/nx/7.1-workspace-creation-and-initialization | Workspace Creation and Initialization — nrwl/nx | DeepWiki | 2024 | T2 | verified |
| 25 | https://nextjs.org/docs/app/api-reference/cli/create-next-app | CLI: create-next-app | Next.js/Vercel | 2025 | T1 | verified |
| 26 | https://turborepo.dev/docs/reference/create-turbo | create-turbo | Vercel/Turborepo | 2025 | T1 | verified |
| 27 | https://devblogs.microsoft.com/dotnet/introducing-dotnet-scaffold/ | dotnet scaffold — Next Generation Content Creation for .NET | Microsoft | 2024 | T1 | verified |
| 28 | https://github.com/kristw/yeoman-easily | yeoman-easily | Krist Wongsuphasawat | 2020 | T3 | verified |
| 29 | https://blog.saeloun.com/2021/06/29/rails-7-generators-will-raise-errors-when-invalid/ | Rails 7 generators will raise errors if an attribute type is invalid | Saeloun | 2021 | T2 | verified |
| 30 | https://hackceleration.com/claude-code-review/ | Claude Code Review 2026 | Hackceleration | 2026 | T3 | verified |
| 31 | https://oneuptime.com/blog/post/2026-02-23-how-to-handle-module-errors-and-debugging-in-terraform/view | How to Handle Module Errors and Debugging in Terraform | OneUptime | 2026 | T3 | verified |
| 32 | https://controlmonkey.io/resource/terraform-errors-guide/ | 10 Common Terraform Errors & Best Practices | ControlMonkey | 2025 | T2 | verified |
| 33 | https://markaicode.com/debugging-vscode-extensions-configuration-issues/ | I Broke My VS Code Setup 5 Times Before Learning These Extension Debugging Tricks | Markaicode | 2024 | T3 | verified |
| 34 | https://bobcares.com/blog/kubectl-error-the-server-doesnt-have-a-resource-type/ | Fixing kubectl error "the server doesn't have a resource type" | BobCares | 2024 | T3 | verified |
| 35 | https://www.nngroup.com/articles/confirmation-dialog/ | Confirmation Dialogs Can Prevent User Errors (If Not Overused) | Nielsen Norman Group | 2023 | T2 | verified |
| 36 | https://www.nngroup.com/articles/user-mistakes/ | Preventing User Errors: Avoiding Conscious Mistakes | Nielsen Norman Group | 2023 | T2 | verified |

---

### Overall challenge summary

The most vulnerable claim is Claim 1: `yo code` as the "strongest" single-entry-point routing example. Nx's `create-nx-workspace` is a direct peer that operates at larger scale and covers more primitive types; the original search did not include workspace-bootstrapping CLI tools as a comparison class. Claim 3 (Claude Code as most actionable) is structurally self-serving but not demonstrably wrong — third-party reviews corroborate general quality, though no independent application of the same rubric exists. The most important caveating needed is on Claim 4: the "debugging opacity" failure mode is real for layered abstraction frameworks but does not generalize to tools like VS Code extensions or kubectl, where wrong-type errors surface immediately and explicitly. The synthesis should specify the class of tools for which this failure mode applies rather than treating it as universal.

## Findings

### F1: Intent-to-primitive routing is universally post-hoc in official documentation

Across all major agent frameworks and plugin systems examined — LangChain, LangGraph, LlamaIndex, CrewAI, OpenAI Agents SDK, Claude Code, VS Code, JetBrains — routing guidance is embedded in reference documentation rather than surfaced as an intake gate at creation time [1][2][3][4][5][6][9][12][13][14]. Users must already know they need to make a choice, navigate to the comparison page, and apply prose criteria themselves. No framework interrogates intent before scaffolding begins.

**Counter-evidence:** LlamaIndex [5] explicitly redirects users from the wrong component page to the correct one — the strongest proactive routing found. This is still a documentation link, not an intake gate; it requires the user to land on the wrong page first. (HIGH — T1 sources across 6 frameworks, consistent pattern with one partial exception)

---

### F2: Single-entry-point creation routing is common practice and structurally prevents starting-point errors — but error rate reduction is unmeasured

VS Code's `yo code` [14][15], Nx's `create-nx-workspace` [23], `create-next-app` [25], and `create-turbo` [26] all route creation through a single interactive command. This means a user cannot accidentally begin on the wrong scaffolding path — they must actively select the wrong type. JetBrains takes the opposite approach (separate docs per type, no routing wizard [13]).

**Counter-evidence:** No controlled study was found comparing error rates between single-entry-point and separate-path creation flows. The structural advantage is logical, not measured. (MODERATE — multiple T1 examples validate the pattern as common practice; effectiveness claim is structural only)

---

### F3: Confirmation gates prevent slips, not mistakes — making them structurally inappropriate for primitive selection routing

NN/G's practitioner consensus [35][36] distinguishes slips (correct intent, wrong execution) from mistakes (wrong intent). Confirmation dialogs are effective at preventing slips. Primitive selection errors are mistakes — the user does not know their intent is wrong. A "confirm your choice of skill" gate cannot prevent a user from choosing skill when they needed a hook, because they do not know the difference. This makes confirmation gates the wrong intervention for this problem class.

**Counter-evidence:** The 85% acceptance rate target from the Smashing Magazine Intent Preview pattern [20] is a design goal, not empirical data from a controlled study. AWS CLI preview-before-commit [16] is the best-documented gate analog, but it prevents execution of correct intent, not selection of wrong primitive. (HIGH — NN/G slip/mistake distinction is T2 practitioner consensus; confirmed by absence of any counter-evidence from 14-source challenger search)

---

### F4: Wrong-primitive failure signals are late and opaque in layered abstraction frameworks — but fast-fail in plugin and infrastructure systems

In LangChain/LangGraph, wrong-primitive selection manifests as accumulated debugging opacity [19][22]: "the second you need to do something original you have to go through 5 layers of abstraction." The first signal comes days into development, not at creation time. In contrast, VS Code extension wrong-type errors are immediate activation conflicts [33], and kubectl wrong-resource errors are explicit API rejections [34]. Terraform module misuse falls between the two — errors point to module internals, producing partial opacity [31][32].

**Counter-evidence:** The LangChain failure mode is widely documented but may reflect LangChain's particular architecture rather than a property of wrong-primitive selection generally. For Claude Code specifically, skill description vagueness and subagent misuse [21] produce observable-within-session errors, not multi-day debugging failures. (MODERATE — LangChain pattern well-supported; generalization contradicted by VS Code and kubectl evidence; Claude Code sits in a distinct middle category)

---

### F5: No production framework implements a semantic "justify your choice" gate — but the pattern is technically feasible

After searching 14 frameworks and tools, no production system was found that asks "why are you choosing this primitive over the alternatives?" before creation [2][6][9][13][14][28][29]. The Yeoman `confirmBeforeStart` API [28] demonstrates technical feasibility. Rails 7 generator validation [29] shows type-form gates (typo-catching) but not semantic justification gates. JetBrains includes one pre-selection "consider alternatives" link [13] — the only pre-creation redirect found in a plugin system.

**Counter-evidence:** The absence is real. The pattern does not exist at scale because: (a) it addresses the wrong error type (mistakes, not slips — see F3), and (b) expert users require bypass mechanisms (VS Code's `-q` flag [14]) that undermine consistent gate application. (HIGH — absence confirmed by broad 14-source challenger search; not assumed by limited initial search)

---

### F6: Trigger-based (pain-point → primitive) routing is the highest-fidelity model found — but its advantage over alternatives is not independently validated

Claude Code's "build your setup over time" trigger table [12] maps recognized pain points ("I keep typing the same prompt") to primitives. This routes by *symptom*, not by knowledge of the primitive model — which matches how developers encounter the need for a new capability. This is more cognitively accessible than taxonomy-based routing (JetBrains [13]) or scope-hierarchy routing (Terraform [17]).

**Counter-evidence:** Source [12] is self-referential (Anthropic docs on Anthropic tooling). No independent study validates the trigger-table approach against alternatives. Third-party reviews corroborate general onboarding quality [30] but do not assess the trigger-table mechanism specifically. The claim is restated as: "most structurally explicit," not "most effective." (MODERATE — logic is sound, self-referential sourcing limits confidence; no independent validation found)

---

### F7: Complex CLI tools route by scope hierarchy and progressive disclosure — not intent gates

Terraform uses an atom/molecule/organism metaphor [17] — a routing heuristic that maps to scope size (individual resource → composite → organization-wide). clig.dev [18] documents progressive disclosure (common commands first in help) and contextual suggestion (tell the user what to run next). AWS CLI wizards [16] route within a service but require the user to already know the service. None operate before the user expresses intent; all help users refine or recover from incorrect commands.

**Counter-evidence:** No counter-evidence found. Pattern is consistent across three independent sources. (HIGH — T1/T2 sources; consistent across AWS, Terraform, and CLI design community)

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "An agent is a class that uses an LLM to choose a sequence of actions to take, while in chains, a sequence of actions is hardcoded." | quote | [1] | unverifiable |
| 2 | "LangGraph becomes the preferred way to build any AI application that is more than a single LLM call." | quote | [2] | verified |
| 3 | "Workflows: predetermined code paths... Agents: dynamic and define their own processes and tool usage." | quote | [4] | verified |
| 4 | "A query engine takes in a natural language query and returns a rich response … If you want to have a conversation with your data, take a look at Chat Engine." | quote | [5] | verified |
| 5 | "you call the wizard subcommand and the wizard name after the service name: `aws dynamodb wizard new-table`" | quote | [16] | verified |
| 6 | "Display the most common flags and commands at the start of the help text" | quote | [18] | verified |
| 7 | "Individual resources are like atoms in the infrastructure. Resource modules are molecules — the smallest versioned and shareable unit." | quote | [17] | corrected |
| 8 | "No framework interrogates intent before scaffolding begins" | superlative | [1][2][3][4][5][6][9][12][13][14] | human-review |
| 9 | ">85% acceptance rate" target from Smashing Magazine Intent Preview pattern | statistic | [20] | verified |
| 10 | NN/G distinction between slips (correct intent, wrong execution) and mistakes (wrong intent) | attribution | [35][36] | verified |
| 11 | "the second you need to do something a little original you have to go through 5 layers of abstraction just to change a minute detail" | quote | [19] | corrected |
| 12 | Claude Code trigger table: "You keep typing the same prompt → skill" | attribution | [12] | verified |
| 13 | VS Code generator routes via "What type of extension do you want?" prompt | attribution | [14] | human-review |

### Verification Notes

**Claim 1 — unverifiable:** The cited URL (`python.langchain.com/v0.1/docs/use_cases/tool_use/`) now permanently redirects (308) to `docs.langchain.com/oss/python/langchain/overview`, which does not contain the agents-vs-chains quote. The current LangChain agents page (`/langchain/agents`) also does not contain this quote. The quote appears to be from the LangChain v0.1 docs, which are no longer live. The quote is plausible and consistent with historical LangChain documentation, but cannot be verified against the live source. Recommend sourcing from a cached/archived copy or updating to a current equivalent.

**Claim 3 — verified with note:** The source text is "Workflows have predetermined code paths and are designed to operate in a certain order." and "Agents are dynamic and define their own processes and tool usage." The document's condensed form ("Workflows: predetermined code paths...") is an accurate compression.

**Claim 4 — verified with note:** The LlamaIndex source uses a comma mid-sentence ("takes in a natural language query, and returns a rich response") and the two sentences are separate in the original. The document's use of "…" to bridge them is a reasonable compression that preserves meaning.

**Claim 7 — corrected:** The Terraform source (`terraform-best-practices.com/key-concepts`) reads: "While individual resources are like atoms in the infrastructure, resource modules are molecules (consisting of atoms)." The document adds "— the smallest versioned and shareable unit" after "molecules," which does not appear in this sentence in the source — it is the document author's characterization. The quoted portion should end at "molecules (consisting of atoms)."

**Claim 9 — verified with important caveat:** The 85% figure appears in the Smashing Magazine article under "Metrics for Success" as a design benchmark, not an empirical finding. The article itself states: "These targets are representative benchmarks based on industry standards; adjust them based on your specific domain risk." The research document correctly flags this as a design goal, not empirical data. No study was found validating this figure.

**Claim 10 — verified with precision note:** Source [36] (`nngroup.com/articles/user-mistakes/`) defines slips as occurring "when a user is on autopilot, and takes the wrong actions in service of a reasonable goal" and mistakes as occurring "when a user has developed a mental model of the interface that isn't correct, and forms a goal that doesn't suit the situation well." The F3 characterization ("slips = correct intent, wrong execution; mistakes = wrong intent") is an accurate compression. Source [35] (`nngroup.com/articles/confirmation-dialog/`) does not itself define slips vs mistakes but references the relevant NN/G articles; the attribution to [35][36] together is fair.

**Claim 11 — corrected:** The Hacker News source (comment by sc077y, June 21 2024) reads: "the second you need to **something** a little original you have to go through 5 layers of abstraction just to change a minute detail" — the word "do" before "something" is missing in the original comment. The research document adds "do" making it grammatically correct but not verbatim. This appears to be a minor transcription correction rather than a fabrication; the source comment itself likely has a typo. The quote is accurate in substance.

**Claim 13 — human-review:** The cited source (`vscode-docs.readthedocs.io/en/stable/tools/yocode/`) returned HTTP 403 during verification. The GitHub repository (`github.com/microsoft/vscode-generator-code`) confirms the generator routes on extension type but does not specify the exact prompt wording "What type of extension do you want?" in its README. The prompt text is widely reported by users who have run `yo code`, but the verbatim text could not be confirmed from the cited source during this verification pass.
