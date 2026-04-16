---
name: "Primitive Selection Failure Signals by Framework Architecture"
description: "How quickly wrong-primitive selection surfaces varies by framework: late and opaque in layered abstraction systems, fast-fail in plugin and infrastructure systems, mid-session in Claude Code"
type: context
sources:
  - https://news.ycombinator.com/item?id=40739982
  - https://www.turgon.ai/post/langchain-langgraph-or-custom-choosing-the-right-agentic-framework
  - https://markaicode.com/debugging-vscode-extensions-configuration-issues/
  - https://bobcares.com/blog/kubectl-error-the-server-doesnt-have-a-resource-type/
  - https://oneuptime.com/blog/post/2026-02-23-how-to-handle-module-errors-and-debugging-in-terraform/view
  - https://dev.to/nunc/claude-code-skills-vs-subagents-when-to-use-what-4d12
related:
  - docs/research/2026-04-11-primitive-selection-routing.research.md
  - docs/context/skill-chain-failure-modes-and-antipatterns.context.md
---

How costly a wrong-primitive selection is depends on when the error signals. Signal latency varies significantly by framework architecture and directly affects how much intake routing is worth investing in.

**Late signal: layered abstraction frameworks**

LangChain/LangGraph wrong-primitive selection manifests as accumulated debugging opacity. The Hacker News thread on LangChain abandonment documents the pattern: "the second you need to do something a little original you have to go through 5 layers of abstraction just to change a minute detail." The first recognizable signal — "everything feels hard" — arrives days into development, after multiple failed customization attempts. Turgon AI describes the failure mode as: "When something breaks, you debug LangChain's internals, not your own logic." The user doesn't know whether the problem is their code or the framework's abstraction. This late-signal, high-opacity pattern is the strongest argument for proactive intake routing: by the time the error surfaces, the developer has significant sunk cost. (MODERATE — LangChain pattern well-documented but may reflect its specific architecture rather than layered abstractions generally.)

**Fast-fail: plugin and infrastructure systems**

VS Code extension wrong-type errors surface at activation, not during debugging. A DebugAdapterDescriptorFactory registered from the wrong extension type produces an immediate registration conflict with an explicit error message. The failure mode is misconfiguration detection, not silent friction accumulation. kubectl wrong-resource errors are equally immediate and explicit: "the server doesn't have a resource type" is an API rejection, not a debugging puzzle. These tools fail fast because type is enforced at the system boundary — there is no abstraction layer between the user's code and the type contract.

**Middle tier: Terraform module misuse**

Terraform falls between the two. Module misuse produces stack traces that point to module internals rather than the user's configuration, causing partial opacity. Errors surface within hours rather than days, and they point toward the right area, but the debugging path passes through module source code. This is a constrained version of the LangChain opacity pattern.

**Middle tier: Claude Code**

Claude Code wrong-primitive selection sits in a distinct category. Skills that are too large fail to activate correctly; subagents misused for simple tasks waste context. These failures are observable within a session — the skill doesn't activate, the subagent output is discarded — but they are not multi-day debugging failures. The cost is wasted session context and rework, not blocked development over multiple days.

**Implication for intake routing**

Signal latency affects how much an intake gate is worth. For LangChain, where errors arrive days later with high sunk cost, proactive routing has high leverage. For VS Code extensions, where errors arrive within seconds at activation, the fast-fail system already provides the correction signal — intake routing is lower-value. Claude Code's middle position means intake routing is beneficial but not as critical as in deep-abstraction frameworks.

**Takeaway:** Debugging opacity as a wrong-primitive failure mode is real for layered abstraction frameworks, but does not generalize. VS Code and kubectl produce fast, explicit failures. The case for proactive routing is strongest where signal latency is highest.
