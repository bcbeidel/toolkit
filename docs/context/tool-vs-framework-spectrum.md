---
name: "Tool vs. Framework Spectrum"
description: "Where agent tooling should sit on the tool-vs-framework spectrum — empirical evidence from Anthropic, OpenAI, and Agentless research converges on simple, composable patterns over complex frameworks"
type: reference
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
  - https://arxiv.org/abs/2407.01489
  - https://www.infoq.com/presentations/Simple-Made-Easy/
  - https://en.wikipedia.org/wiki/Unix_philosophy
related:
  - docs/research/scope-management-yagni.md
  - docs/context/yagni-agent-tooling.md
  - docs/context/complexity-budgets.md
  - docs/context/tool-design-for-llms.md
  - docs/context/abstraction-level-design.md
---

The fundamental distinction: with a tool, you call the code; with a framework, the framework calls your code. Where agent tooling sits on this spectrum has direct consequences for performance, debuggability, and long-term maintenance. The empirical evidence points clearly toward the tool end.

## Three Organizations, One Conclusion

**Anthropic:** "The most successful implementations use simple, composable patterns rather than complex frameworks or specialized libraries." Frameworks "create extra layers of abstraction that can obscure underlying prompts and responses, making them harder to debug, and can make it tempting to add complexity when a simpler setup would suffice." Their recommendation: start with direct LLM API calls — many patterns can be implemented in a few lines of code.

**OpenAI:** Standardized, reusable tools with clear documentation, organized into three categories (data tools, action tools, orchestration tools). The emphasis is on tool composability rather than framework comprehensiveness. Many-to-many relationships between tools and agents, not monolithic designs.

**Agentless research:** A two-phase localization-then-repair approach without autonomous agent decision-making achieved 32.00% accuracy on SWE-bench Lite at $0.34 per issue — outperforming all open-source agent-based systems while costing 10x less than some agent approaches. The conclusion: "a simple, non-agent approach can outperform complex agent-based systems for software development tasks."

The convergence across three competing organizations is the strongest signal. This is not one team's opinion — it is an independently replicated finding.

## Simple vs. Easy

Rich Hickey's distinction clarifies why frameworks feel appealing but create problems. "Simple" means not tangled with other structures — one braid, not many interleaved. "Easy" means familiar or near at hand. Frameworks are easy (quick to start) but often complex (deeply interleaved). Tools are simple (independent, composable) but may require more initial effort.

The key insight: complecting — interleaving concerns — creates compound costs that grow nonlinearly. Every additional entanglement makes the system harder to reason about, for humans and LLMs alike. A framework that interleaves configuration, routing, error handling, and state management may be easy to start with but becomes exponentially harder to debug as problems span abstraction boundaries.

## The Unix Philosophy Position

Doug McIlroy's formulation — "Write programs that do one thing and do it well" — represents the tool end of the spectrum. Small, focused, composable programs connected by standard interfaces. The power comes from relationships between programs, not from the programs themselves.

Applied to agent tooling: small tools with clear interfaces compose better than monolithic tools with many parameters because the LLM only loads descriptions of tools it actually uses, smaller tools have shorter descriptions, and composable primitives cover the same action space without combinatorial explosion in parameter descriptions.

## Practical Guidance

Stay as close to the tool end as possible. Add framework-level coordination only when composition of simple tools demonstrably fails — not when you anticipate it might fail. The cost of premature framework adoption is higher than the cost of late framework adoption, because frameworks are harder to remove than to add.

The test: if you can accomplish the same outcome by composing existing simple tools, do that. Build a new abstraction layer only after you have concrete evidence that composition is failing in practice.
