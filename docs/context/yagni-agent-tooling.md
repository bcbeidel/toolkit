---
name: "YAGNI for Agent Tooling"
description: "Why You Aren't Gonna Need It applies with amplified force when the consumer is an LLM — four costs of presumptive features, Beck's fewest elements rule, last responsible moment, and LLM-specific cost-of-carry dynamics"
type: reference
sources:
  - https://martinfowler.com/bliki/Yagni.html
  - https://martinfowler.com/bliki/BeckDesignRules.html
  - https://en.wikipedia.org/wiki/You_aren't_gonna_need_it
  - https://blog.codinghorror.com/the-last-responsible-moment/
  - https://www.anthropic.com/research/building-effective-agents
  - https://arxiv.org/html/2511.22729v1
related:
  - docs/research/scope-management-yagni.md
  - docs/context/complexity-budgets.md
  - docs/context/tool-vs-framework-spectrum.md
  - docs/context/tool-design-for-llms.md
  - docs/context/context-window-management.md
---

YAGNI — You Aren't Gonna Need It — is stronger medicine in agent tooling than in traditional software. Every presumptive feature degrades the reasoning environment for every other feature, because tool descriptions compete for finite LLM attention. The bar for adding anything should be higher when the consumer is a language model.

## The Four Costs, Amplified

Martin Fowler identifies four costs of presumptive features: **build** (effort spent on something nobody asked for), **delay** (deferred delivery of what is actually needed), **carry** (ongoing complexity burden), and **repair** (removing a wrong guess before building the right thing).

In traditional software, cost of carry is a developer experience problem — more code to navigate, more tests to maintain. In agent tooling, cost of carry extends into runtime: every tool description, parameter, and field consumes context tokens in every invocation. An unused tool in a 30-tool set does not sit inert. It makes the agent marginally worse at using the other 29 tools. A 200-token tool description used in 5% of sessions costs 200 tokens to 95% of sessions for zero benefit.

## Beck's Fewest Elements as a Deletion Criterion

Kent Beck's fourth rule of simple design — fewest elements — states: remove anything that does not pass tests, reveal intention, or eliminate duplication. Applied as an ongoing practice: for every tool, parameter, field, and abstraction, ask whether removing it breaks tests, obscures intention, or introduces duplication. If the answer is no to all three, remove it.

This is not minimalism for its own sake. It is the YAGNI rule stated as a design criterion with concrete decision logic. When every element consumes context tokens, the fourth rule becomes a survival principle.

## Last Responsible Moment

The lean principle: defer decisions until failing to decide eliminates an important alternative. Do not add a configuration option until a real user needs to configure something. Do not add an abstraction layer until two concrete implementations need abstracting. Do not add a tool parameter until someone demonstrates a use case requiring it.

This is not procrastination. It is deliberate deferral to maximize information before committing. In agent tooling, where predictions about future needs are unreliable and cost of carry is immediate, the case for deferral is stronger than in stable domains.

## LLM-Specific Dynamics

Three shifts distinguish YAGNI in agent tooling from its traditional application:

**Cost of carry is runtime, not just development-time.** In human-consumed software, unused features sit inert. In LLM-consumed tooling, they actively degrade performance by consuming context and creating selection ambiguity in every invocation.

**Abstraction layers have context costs.** Human developers benefit from abstraction because it reduces cognitive load. LLMs do not experience cognitive relief the same way. An abstraction that does not reduce total token count is a net negative — it adds its own description, its mapping to concrete operations, and vocabulary overhead.

**Tool descriptions are not free documentation.** Every parameter, edge case, and "when not to use this tool" note consumes context that could hold user data or intermediate reasoning. Descriptions should be as terse as possible while remaining unambiguous.

## The Critical Distinction

YAGNI does not apply to enabling infrastructure. Refactoring, clean interfaces, modular design, and test coverage are not presumptive features — they are prerequisites for YAGNI to work. Invest in changeability (which always pays off), not in specific features that may never be needed (which usually do not). The discipline is keeping code easy to change so features can be added when actually needed rather than speculatively hoarded.
