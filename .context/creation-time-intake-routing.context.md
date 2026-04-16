---
name: "Creation-Time Intake Routing: Why Frameworks Don't Do It"
description: "No framework routes by intent at primitive creation time — routing guidance is universally post-hoc, and trigger-based pain-point mapping is the highest-fidelity alternative found"
type: context
sources:
  - https://code.claude.com/docs/en/features-overview
  - https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/
  - https://docs.langchain.com/oss/python/langgraph/workflows-agents
  - https://plugins.jetbrains.com/docs/intellij/plugin-types.html
  - https://clig.dev/
  - https://www.terraform-best-practices.com/key-concepts
  - https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-wizard.html
related:
  - docs/research/2026-04-11-primitive-selection-routing.research.md
  - docs/context/skill-progressive-loading-and-routing.context.md
  - docs/context/single-entry-point-creation.context.md
---

Across every major agent framework and plugin system surveyed — LangChain, LangGraph, LlamaIndex, CrewAI, OpenAI Agents SDK, Claude Code, VS Code, JetBrains — routing guidance is embedded in reference documentation rather than surfaced as an intake question at creation time. Users must already know a choice exists, navigate to the comparison page, and apply prose criteria themselves. No framework interrogates intent before scaffolding begins. (HIGH confidence — T1 sources across 6+ frameworks, consistent pattern.)

The strongest proactive routing found in any framework is LlamaIndex's query engine documentation, which explicitly redirects users: "If you want to have a conversation with your data, take a look at Chat Engine." This is still a documentation link, not a creation-time gate. It requires the user to land on the wrong page first, read far enough to encounter the redirect, and then follow it. It is the best available example of what proactive routing looks like when it does exist — and it falls short of an intake gate.

LangGraph provides explicit prose criteria: "Workflows = predetermined code paths; Agents = dynamic." This is clear, but it lives in reference docs, not at `langgraph new`. JetBrains lists five plugin categories with brief descriptions; developers self-select based on whether descriptions match their intent. No cross-referencing, no decision tree.

**Trigger-based routing: the highest-fidelity model found**

Claude Code's "build your setup over time" trigger table maps recognized pain points to primitives:

- Claude gets a convention wrong twice → CLAUDE.md
- You keep typing the same prompt → skill
- You paste the same playbook three times → skill
- You keep copying data from a browser tab → MCP
- A side task floods your conversation → subagent
- You want something to happen every time without asking → hook

This routes by symptom, not by knowledge of the primitive taxonomy. Users don't need to know what a "hook" is — they need to recognize "I want something to happen every time without asking." This is cognitively accessible in a way that taxonomy-based routing (JetBrains categories) or scope-hierarchy routing (Terraform atoms/molecules) is not. The source is self-referential (Anthropic's own docs on Anthropic's tool), and no independent study validates trigger-table routing against alternatives. The finding is restated as: most structurally explicit routing aid found, not most effective.

**CLI tools route post-input, not pre-selection**

clig.dev's CLI design guidelines document three routing patterns: progressive disclosure (common commands first), contextual suggestion (tell the user what to do next), and typo correction. None operate before the user expresses intent. AWS CLI wizards are service-scoped — the user must already know which service they want before entering the wizard, which handles intra-primitive configuration, not cross-primitive selection. Terraform's atom/molecule hierarchy is a routing metaphor developers must internalize, not an intake question asked at `terraform init`.

**What creation-time routing would require**

A creation-time intake gate would need to ask "what pain are you trying to solve?" before routing to the correct primitive. This is structurally different from "what type of thing do you want to create?" (the single-entry-point pattern). The former routes on intent; the latter routes on declared type — and declared type requires users to already know the taxonomy.

The trigger-pain-point table is the closest approximation: it converts intent-routing into symptom-recognition, which is something users can do without knowing the primitive model.

**Takeaway:** The absence of creation-time intake routing across all surveyed frameworks is not a gap to fill with a confirmation gate — it reflects the difficulty of routing before the user can express a symptom. Trigger-based symptom mapping is the most practical alternative found.
