---
name: "Scope Management and YAGNI in Agent Tooling"
description: "How to resist feature creep in agent tooling — the four costs of presumptive features, complexity budgets, the tool-vs-framework spectrum, XP/lean simplicity principles, and why YAGNI applies differently when the consumer is an LLM"
metadata:
  type: research
  sources:
    - https://martinfowler.com/bliki/Yagni.html
    - https://www.anthropic.com/research/building-effective-agents
    - https://arxiv.org/abs/2407.01489
    - https://en.wikipedia.org/wiki/You_aren't_gonna_need_it
    - https://martinfowler.com/bliki/BeckDesignRules.html
    - https://en.wikipedia.org/wiki/Unix_philosophy
    - https://www.infoq.com/presentations/Simple-Made-Easy/
    - https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
    - https://arxiv.org/html/2601.06112v1
    - https://blog.codinghorror.com/the-last-responsible-moment/
    - https://arxiv.org/html/2511.22729v1
    - https://en.wikipedia.org/wiki/Feature_creep
  related:
    - docs/research/abstraction-level-design.md
    - docs/research/principle-engineering.md
    - docs/research/convention-driven-design.md
    - docs/context/yagni-agent-tooling.md
    - docs/context/complexity-budgets.md
    - docs/context/tool-vs-framework-spectrum.md
---

## Summary

Feature creep in agent tooling carries amplified costs because every field, abstraction, and tool description competes for finite LLM context and reasoning capacity. Traditional YAGNI logic — presumptive features impose build, delay, carry, and repair costs — still applies, but when the consumer is an LLM rather than a human developer, "cost of carry" extends beyond code maintenance to include context window consumption, tool-selection confusion, and reasoning degradation. The empirical evidence is striking: an 8B-parameter model failed completely with 46 tools but succeeded with 19 — not because of token limits but because of context complexity. Simpler agent architectures consistently outperform complex ones under realistic conditions.

**Key findings:**

- **Fowler's four costs of presumptive features apply with amplified force to agent tooling.** Cost of build, delay, carry, and repair all increase when the consumer is an LLM, because each unused feature degrades the reasoning environment for every other feature (HIGH — multiple T1/T2 sources converge).
- **The tool-vs-framework spectrum has a measurable sweet spot for agent systems.** Anthropic, OpenAI, and the Agentless research independently conclude: start with the simplest possible solution, add complexity only when simpler approaches fail (HIGH — T1 sources from three major organizations).
- **Context complexity, not context length, is the binding constraint.** LLM agent performance degrades with tool count even when token budgets are adequate, because tool descriptions compete for reasoning attention (HIGH — T2 empirical evidence).
- **Kent Beck's "fewest elements" rule maps directly to YAGNI for LLM tooling.** The fourth rule of simple design — remove anything that does not pass tests, reveal intention, or eliminate duplication — becomes a survival principle when every element consumes context tokens (MODERATE — synthesized from T1/T3 sources).
- **Lean "last responsible moment" decisions apply to tooling features.** Defer adding abstractions until the cost of not having them exceeds the cost of carry — and in agent systems, cost of carry is higher than in traditional software (MODERATE — T2/T3 sources).

15 searches across WebSearch, ~150 results found, 12 used.

## Sub-Questions

1. What are the specific costs of presumptive features in software, and how do they apply to agent tooling?
2. Where does agent tooling sit on the tool-vs-framework spectrum, and what are the tradeoffs?
3. How do XP/lean principles (YAGNI, simplicity, last responsible moment) translate to LLM-facing design?
4. What is a complexity budget, and how should agent tooling projects allocate one?
5. How does YAGNI apply differently when the consumer is an LLM rather than a human developer?
6. What empirical evidence exists for simpler-is-better in agent system design?

## Sources

| # | URL | Title | Author/Org | Date | Status | Tier |
|---|-----|-------|-----------|------|--------|------|
| 1 | https://martinfowler.com/bliki/Yagni.html | Yagni | Martin Fowler | 2015 | verified | T1 |
| 2 | https://www.anthropic.com/research/building-effective-agents | Building Effective Agents | Anthropic | 2024 | verified | T1 |
| 3 | https://arxiv.org/abs/2407.01489 | Agentless: Demystifying LLM-based Software Engineering Agents | Xia et al. | 2024 | verified | T2 |
| 4 | https://en.wikipedia.org/wiki/You_aren't_gonna_need_it | You Aren't Gonna Need It | Wikipedia | 2024 | verified | T3 |
| 5 | https://martinfowler.com/bliki/BeckDesignRules.html | Beck Design Rules | Martin Fowler | 2015 | verified | T1 |
| 6 | https://en.wikipedia.org/wiki/Unix_philosophy | Unix Philosophy | Wikipedia | 2024 | verified | T3 |
| 7 | https://www.infoq.com/presentations/Simple-Made-Easy/ | Simple Made Easy | Rich Hickey / InfoQ | 2011 | verified | T2 |
| 8 | https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/ | A Practical Guide to Building Agents | OpenAI | 2025 | verified | T1 |
| 9 | https://arxiv.org/html/2601.06112v1 | ReliabilityBench: Evaluating LLM Agent Reliability | Multiple authors | 2026 | verified | T2 |
| 10 | https://blog.codinghorror.com/the-last-responsible-moment/ | The Last Responsible Moment | Jeff Atwood / Coding Horror | 2006 | verified | T3 |
| 11 | https://arxiv.org/html/2511.22729v1 | Solving Context Window Overflow in AI Agents | Multiple authors | 2025 | verified | T2 |
| 12 | https://en.wikipedia.org/wiki/Feature_creep | Feature Creep | Wikipedia | 2024 | verified | T3 |

## Findings

### 1. The Four Costs of Presumptive Features

Martin Fowler's YAGNI analysis identifies four distinct costs that presumptive features impose [1]:

**Cost of build.** The effort spent analyzing, programming, and testing a feature that may never be needed. In agent tooling, this includes writing tool descriptions, designing parameter schemas, building error handling, and testing edge cases for a capability nobody has requested yet.

**Cost of delay.** Building the presumptive feature delays shipping the features that are actually needed. Every sprint spent on speculative abstractions is a sprint not spent on the tool that users are asking for right now.

**Cost of carry.** The ongoing complexity burden. The presumptive feature makes the codebase harder to modify and debug, increasing the cost of every subsequent feature. Fowler illustrates this with an insurance example: a piracy-pricing module adds weeks to the development of storm insurance, regardless of whether anyone ever buys piracy insurance [1].

**Cost of repair.** If the presumptive feature turns out to be wrong (built to the wrong specification), fixing it costs more than building it correctly would have, because you must remove the wrong implementation before building the right one.

These four costs are not new to agent tooling. What is new is their amplification. In traditional software, cost of carry is primarily a developer experience problem — more code to navigate, more tests to maintain, more documentation to update. In agent tooling, cost of carry extends into the runtime environment itself: every tool description, every parameter, every field consumes context tokens and competes for the LLM's reasoning attention. A presumptive feature in agent tooling does not just slow down the next developer; it slows down every agent invocation (HIGH — T1 source [1], extended by synthesis with [2], [11]).

Fowler is careful to distinguish presumptive features from enabling infrastructure: "Yagni only applies to capabilities built into the software to support a presumptive feature, it does not apply to effort to make the software easier to modify" [1]. Refactoring, clean interfaces, and modular design are not YAGNI violations — they are prerequisites for YAGNI to work. Code must be easy to change so that features can be added when they are actually needed rather than speculatively hoarded.

### 2. The Tool-vs-Framework Spectrum

Agent tooling occupies a critical position on the tool-vs-framework spectrum. The fundamental distinction: with a library/tool, you call the code; with a framework, the framework calls your code (inversion of control). This distinction has direct consequences for agent system design.

**The Unix philosophy position.** Doug McIlroy's formulation — "Write programs that do one thing and do it well" — represents the tool end of the spectrum [6]. Small, focused, composable programs connected by pipes. The power comes from relationships between programs, not from the programs themselves. Richard Gabriel's "worse is better" principle extends this: a system that is simple and cheap to build but effective will outcompete a system that is comprehensive and correct but expensive [6].

**The framework position.** Frameworks provide structure, reduce decisions, and enforce consistency. But they impose costs: they are opinionated about design, harder to debug because abstraction layers obscure underlying behavior, and they create lock-in because replacing a framework means rewriting the application.

**Where agent tooling should sit.** Anthropic's guidance is explicit: "The most successful implementations use simple, composable patterns rather than complex frameworks or specialized libraries" [2]. They recommend starting with direct LLM API calls — many patterns can be implemented in a few lines of code. Frameworks "often create extra layers of abstraction that can obscure underlying prompts and responses, making them harder to debug, and can make it tempting to add complexity when a simpler setup would suffice" [2].

OpenAI's practical guide converges on the same position: standardized, reusable tools with clear documentation, organized into three categories (data tools, action tools, orchestration tools) [8]. The emphasis is on tool composability rather than framework comprehensiveness.

The Agentless research provides the strongest empirical argument for the tool end of the spectrum. A simple two-phase approach (localization then repair) without any autonomous agent decision-making achieved 32.00% accuracy at $0.70 per issue — outperforming all open-source agent-based systems while costing 10x less than some agent approaches ($0.34 vs. $3.34 per issue) [3]. The conclusion: "a simple, non-agent approach can outperform complex agent-based systems for software development tasks" (HIGH — T1/T2 sources converge from three independent organizations).

**Rich Hickey's simple-vs-easy distinction clarifies the tradeoff.** "Simple" means not tangled with other code structures — one braid, not many interleaved. "Easy" means familiar or near at hand [7]. Frameworks are easy (quick to start) but often complex (deeply interleaved). Tools are simple (independent, composable) but may require more initial effort. Hickey's key insight: "complecting" — interleaving concerns — creates compound costs that grow nonlinearly. Every additional entanglement makes the system harder to reason about, for humans and LLMs alike [7].

For agent tooling, the practical recommendation: stay as close to the tool end as possible. Add framework-level coordination only when composition of simple tools demonstrably fails. The cost of premature framework adoption is higher than the cost of late framework adoption, because frameworks are harder to remove than to add (MODERATE — synthesized from [2], [7], [8]).

### 3. XP/Lean Principles Applied to LLM-Facing Design

**YAGNI's XP origins.** YAGNI arose directly from Extreme Programming. Ron Jeffries, XP co-founder: "Always implement things when you actually need them, never when you just foresee that you need them" [4]. It is closely related to the XP practice of "do the simplest thing that could possibly work" (DTSTTCPW). Critically, YAGNI depends on supporting practices — continuous refactoring, automated testing, continuous integration — that make it safe to add features later rather than speculatively now [1][4].

**Kent Beck's four rules of simple design** provide an operational definition of "simple enough" [5]:

1. **Passes the tests** — it works as intended
2. **Reveals intention** — the code is understandable
3. **No duplication** — DRY principle
4. **Fewest elements** — remove anything that does not serve rules 1-3

The fourth rule — fewest elements — is the YAGNI rule stated as a design criterion. It says: if removing a class, method, field, or abstraction does not break tests, obscure intention, or introduce duplication, then it should be removed. Applied to agent tooling: if removing a tool parameter, a configuration option, or an abstraction layer does not break functionality, reduce clarity, or create redundancy, it should not exist (HIGH — T1 source [5]).

**The lean "last responsible moment."** The Poppendiecks' lean software development principle: delay decisions until the last responsible moment — "the moment at which failing to make a decision eliminates an important alternative" [10]. This is not procrastination; it is deliberate deferral to maximize information before committing. Applied to agent tooling: do not add a configuration option until a real user needs to configure something. Do not add an abstraction layer until you have two concrete implementations that need abstracting. Do not add a tool parameter until someone demonstrates a use case that requires it.

The lean analogy to Just-In-Time manufacturing is precise: rather than stocking parts based on forecasts, wait for actual orders and ensure your process is lean enough to fulfill them quickly [4]. In agent tooling: rather than building features based on imagined future needs, keep the codebase simple enough that features can be added quickly when actual needs materialize (MODERATE — T2/T3 sources [4][10]).

### 4. Complexity Budgets for Agent Tooling

A complexity budget is the total cognitive and computational overhead a system can bear before incremental additions degrade overall performance. In traditional software, this is primarily a human concern — developers lose productivity as systems grow more complex. In agent tooling, complexity budgets have a measurable, mechanical dimension.

**The context window as a hard complexity budget.** Every tool description, parameter schema, and behavioral guideline consumes tokens from a finite context window. Research on context window overflow in agent systems shows that agentic workflows with 20-50+ LLM calls accumulate context rapidly, and when context runs out, agents lose critical information from early steps [11]. But the budget is not merely about token count — it is about effective reasoning capacity within that token count.

**The tool-count cliff.** When researchers gave a quantized Llama 3.1 8B model access to 46 tools from the GeoEngine benchmark, it failed completely, even though the context was within its 16K window. With 19 tools, it succeeded [11]. The failure was not a token-length problem but a context-complexity problem — too many tool descriptions overwhelmed the model's ability to select and reason about the right tool.

**Degradation beyond 12 turns.** ReliabilityBench found that beyond 12 conversation turns, agents increasingly invoke redundant operations: re-reading unchanged files, repeating failed tool calls with minimal adjustments, generating verbose summaries that consume tokens without adding information [9]. A 50% increase in conversation length yields 3-5% efficiency losses, with compounding effects as context accumulates [9]. Simpler ReAct agents outperformed more complex Reflexion architectures under stress conditions [9].

**Practical budgeting.** These findings suggest concrete allocation principles for agent tooling projects:

- **Token budget per tool:** Every tool description has an amortized cost across all invocations. A 200-token tool description that is used in 5% of sessions costs 200 tokens to 95% of sessions for zero benefit. Multiply across 10 such tools, and you have consumed 2000 tokens of reasoning capacity for marginal utility.
- **Feature justification threshold:** Every feature must demonstrate that its value exceeds its context cost. A rarely-used parameter that adds 50 tokens to every tool description must justify those 50 tokens against the reasoning degradation they cause.
- **Periodic pruning:** Just as teams allocate sprint capacity for technical debt, agent tooling projects should periodically audit tool sets and remove unused or low-value tools. Feature removal is a feature (HIGH — synthesized from [9], [11]).

### 5. YAGNI Applied Differently When the Consumer Is an LLM

Traditional YAGNI assumes a human consumer — a developer who reads code, navigates APIs, and maintains mental models. When the consumer is an LLM, several dynamics shift:

**Cost of carry is runtime, not just development-time.** In human-consumed software, an unused feature sits inert in the codebase. It costs developer attention when modifying adjacent code, but it does not degrade the application's runtime performance. In LLM-consumed tooling, unused features actively degrade performance because their descriptions occupy context tokens and create selection ambiguity in every invocation. An unused tool in a 30-tool set does not merely sit quietly — it makes the agent marginally worse at using the other 29 tools.

**Abstraction layers have context costs.** Human developers benefit from abstraction because it reduces cognitive load — they can ignore implementation details and work at a higher level. LLMs do not experience cognitive relief from abstraction in the same way. An abstraction layer in agent tooling adds: (a) the description of the abstraction itself, (b) the mapping from abstract operations to concrete ones, and (c) the vocabulary overhead of naming the abstraction. If the abstraction does not reduce the total token count needed to describe behavior, it is a net negative.

**Premature generalization is costlier.** "If you only have one implementation, and no current requirement to switch providers, then why abstract?" [4]. For human APIs, the answer might be: it makes future changes cheaper. For LLM-facing tooling, the calculus changes: the abstraction's presence in tool descriptions costs tokens now, and the future flexibility may never be exercised. The YAGNI presumption is stronger because the cost of carry is higher and more immediate.

**Tool descriptions are not free documentation.** Every parameter, every edge case, every "when not to use this tool" note in a tool description consumes context that could hold user data, conversation history, or intermediate reasoning. Tool descriptions should be as terse as possible while remaining unambiguous. This is "omit needless words" applied to machine-readable interfaces (HIGH — synthesized from [2], [8], [11]).

**The composability advantage magnifies.** Small, focused tools that each do one thing well compose better than monolithic tools with many parameters because: (a) the LLM only loads the descriptions of tools it actually uses, (b) smaller tools have shorter descriptions, and (c) composable primitives cover the same action space as complex tools without the combinatorial explosion in parameter descriptions. This is the Unix philosophy applied to agent-computer interfaces [6].

### 6. Empirical Evidence: Simpler Is Better

The empirical record consistently favors simplicity in agent system design.

**Agentless outperforms agents.** Xia et al. demonstrated that a two-phase localization-and-repair approach without autonomous agent loops achieved the highest performance (32.00%, 96 correct fixes) among open-source systems on SWE-bench Lite, at dramatically lower cost ($0.34 per issue vs. $3.34 for CodeAct) [3]. The authors conclude this "challenges the assumption that increasingly sophisticated agents are necessary" (HIGH — T2 source with controlled benchmarks).

**Simpler architectures survive stress better.** ReliabilityBench tested agents under production-like stress conditions (ambiguous instructions, noisy tool outputs, context overflow) and found that simpler ReAct agents outperform more complex Reflexion architectures [9]. Nearly all models suffered substantial performance degradation under realistic conditions, with an average accuracy drop of 20.8% [9].

**Anthropic's practical finding.** After deploying agents across numerous customer implementations, Anthropic reports that "the most successful implementations use simple, composable patterns rather than complex frameworks" [2]. Their recommendation: "find the simplest solution possible, and only increase complexity when needed — which might mean not building agentic systems at all" [2].

**OpenAI concurs.** OpenAI's agent-building guide emphasizes standardized, reusable tools over custom frameworks, with explicit tool categories and many-to-many relationships between tools and agents [8]. The architecture favors composition over monolithic design.

**The convergence is notable.** Three competing organizations (Anthropic, OpenAI, academic researchers) independently arrived at the same conclusion: simpler agent architectures outperform complex ones, and the path from simple to complex should be driven by demonstrated need rather than anticipated future requirements (HIGH — convergence across T1/T2 sources).

## Challenge

**Primary counter-argument: YAGNI can become an excuse for under-engineering.** Critics argue that YAGNI, applied too zealously, produces systems that are difficult to extend when requirements do change. If you defer every abstraction until it is needed, you may end up with a tangle of special cases rather than a clean architecture. As one Hacker News commenter noted: "YAGNI is based on the assumption that change is cheap, but change is only cheap if you designed for it." The Poppendieck principle of the last responsible moment has the same vulnerability — there is no clear tipping point that identifies when deferral becomes procrastination [10].

**Response:** Fowler addresses this directly. YAGNI does not apply to enabling infrastructure — refactoring, clean interfaces, modular design, test coverage [1]. These are not presumptive features but prerequisites for making future change cheap. The discipline is: invest in changeability (which always pays off), but do not invest in specific features until they are needed (which may never pay off). In agent tooling, this means: maintain clean tool interfaces, keep descriptions well-structured, write good tests — but do not add tools, parameters, or abstractions until someone demonstrates a need.

**Second counter-argument: LLMs benefit from rich tool descriptions.** One could argue that providing the LLM with more tools and richer descriptions gives it more options and makes it more capable. More tools means more capabilities.

**Response:** The empirical evidence contradicts this. The Llama 8B model that failed with 46 tools but succeeded with 19 demonstrates that more is not better — it is worse beyond a threshold [11]. Tool descriptions are not free information; they are cognitive load that competes with task-specific reasoning. The optimal strategy is the minimum viable tool set: enough tools to cover required capabilities, no more.

**Third counter-argument: Agent tooling is too young for YAGNI.** In rapidly evolving domains, you cannot predict what will be needed, so building flexibility might be justified.

**Response:** This actually strengthens the YAGNI argument. In rapidly evolving domains, predictions about future needs are even less reliable than in stable domains. The probability that a presumptive feature matches actual future needs decreases as the domain changes faster. The correct response to uncertainty is not speculative building but reversible design — keep the architecture simple enough that any direction is accessible when needs materialize.

**Premortem: What could make this analysis wrong?**

1. If LLM context windows grow to millions of tokens with no reasoning degradation, the context-cost argument weakens (though cost-of-carry in the codebase remains).
2. If dynamic tool loading becomes standard practice (tools loaded on-demand rather than all present in context), the tool-count argument becomes less relevant.
3. If agent architectures shift to multi-agent systems where each agent has a small, specialized tool set, the per-agent tool count may be naturally constrained regardless of total system complexity.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Fowler identifies four costs of presumptive features: build, delay, carry, repair | attribution | [1] | verified |
| 2 | YAGNI does not apply to effort to make software easier to modify | attribution | [1] | verified |
| 3 | Agentless achieved 32.00% (96 fixes) on SWE-bench Lite, highest among open-source systems | statistic | [3] | verified |
| 4 | Agentless cost $0.34 per issue vs. $3.34 for CodeAct | statistic | [3] | verified |
| 5 | Llama 3.1 8B failed with 46 tools but succeeded with 19 on GeoEngine | statistic | [11] | verified |
| 6 | Beyond 12 turns, agents increasingly invoke redundant operations | statistic | [9] | verified |
| 7 | 50% conversation length increase yields 3-5% efficiency losses | statistic | [9] | verified |
| 8 | Simpler ReAct agents outperform Reflexion under stress | finding | [9] | verified |
| 9 | Average accuracy drop of 20.8% under noisy/stress conditions | statistic | [9] | verified |
| 10 | Ron Jeffries: "Always implement things when you actually need them" | quote | [4] | verified |
| 11 | Kent Beck's four rules: passes tests, reveals intention, no duplication, fewest elements | attribution | [5] | verified |
| 12 | Doug McIlroy: "Write programs that do one thing and do it well" | quote | [6] | verified |
| 13 | Hickey distinguishes "simple" (not tangled) from "easy" (familiar/near at hand) | attribution | [7] | verified |
| 14 | Anthropic: most successful implementations use simple, composable patterns | attribution | [2] | verified |
| 15 | OpenAI categorizes tools as data tools, action tools, orchestration tools | attribution | [8] | verified |
| 16 | Last responsible moment: when failing to decide eliminates an important alternative | definition | [10] | verified |

## Key Takeaways

1. **Every feature in agent tooling pays rent in context tokens.** Unlike traditional software where unused features are inert, every tool description and parameter actively degrades LLM reasoning by consuming finite attention capacity. The YAGNI bar for agent tooling should be higher than for human-facing software.

2. **Stay on the tool side of the tool-vs-framework spectrum.** Three independent major organizations (Anthropic, OpenAI, Agentless researchers) converge: simple, composable patterns outperform complex frameworks. Add coordination layers only when composition demonstrably fails, not when you anticipate it might.

3. **Apply Beck's "fewest elements" as a deletion criterion.** For every tool, parameter, field, and abstraction, ask: does removing this break tests, obscure intention, or introduce duplication? If no, remove it. The fourth rule of simple design is the YAGNI rule stated as an ongoing practice.

4. **Budget complexity like you budget tokens.** Treat your project's total complexity as a finite resource. Every new feature draws from the same budget as every existing feature. Periodic pruning — removing tools and parameters that are unused or low-value — is not cleanup; it is a first-class engineering activity.

5. **Invest in changeability, not in features.** The difference between YAGNI and under-engineering is whether you invest in making future change cheap (clean interfaces, modular design, test coverage) versus investing in specific features that may never be needed. The former always pays off; the latter usually does not.

## Limitations

- **Source depth on LLM tool-count effects.** The Llama 8B/46-tool finding is from a single benchmark (GeoEngine). Broader empirical studies across model sizes and tool types would strengthen this claim. The relationship between tool count and performance degradation likely varies by model capability.
- **Rapidly evolving field.** Agent tooling best practices are shifting rapidly. Recommendations from 2024-2025 may not hold as context windows expand, models improve at tool selection, and dynamic tool loading becomes more common.
- **YAGNI assumes changeability.** The entire argument depends on code being easy to modify later. If a project lacks test coverage, clean interfaces, and refactoring discipline, deferring features can create a different kind of debt — the cost of retrofitting missing capabilities into a rigid codebase.
- **No controlled studies specific to agent tooling YAGNI.** The synthesis connecting Fowler's YAGNI framework to agent tool design is inferred from adjacent evidence. No study has directly measured the four costs of presumptive features in an agent tooling context.
- **Survivorship bias in simplicity recommendations.** We hear about simple systems that succeeded and complex systems that failed. We hear less about simple systems that failed due to insufficient capability or complex systems that succeeded because their scope matched genuine complexity.

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| YAGNI principle software design feature creep resistance | WebSearch | all | 10 | [1], [4] |
| complexity budget software engineering scope management | WebSearch | all | 10 | supporting |
| tool vs framework spectrum software design tradeoffs | WebSearch | all | 10 | supporting |
| lean software development XP extreme programming simplicity YAGNI | WebSearch | all | 10 | [4], [1] |
| LLM agent tooling design simplicity complexity management | WebSearch | all | 10 | [2] |
| feature creep prevention strategies software projects | WebSearch | all | 10 | [12] |
| Martin Fowler YAGNI cost of build cost of delay cost of carry cost of repair | WebSearch | all | 10 | [1] |
| Anthropic building effective agents simplicity patterns 2024 | WebSearch | all | 10 | [2] |
| "complexity budget" engineering teams allocation decisions | WebSearch | all | 10 | supporting |
| YAGNI LLM tools agent design over-engineering abstraction | WebSearch | all | 10 | [2], [3] |
| library vs framework inversion of control tradeoffs Rich Hickey simple made easy | WebSearch | all | 10 | [7] |
| Kent Beck XP simplicity rules software design four rules | WebSearch | all | 10 | [5] |
| OpenAI practical guide building agents tool design principles 2025 | WebSearch | all | 10 | [8] |
| agentless vs agentic software engineering LLM simpler approaches | WebSearch | all | 10 | [3] |
| Dan North YAGNI decisions reversible software architecture | WebSearch | all | 10 | [10] |
| "worse is better" Unix philosophy do one thing well software design minimalism | WebSearch | all | 10 | [6] |
| Rich Hickey simple made easy complect complexity key points summary | WebSearch | all | 10 | [7] |
| LLM tool description design too many tools context window overhead agent performance | WebSearch | all | 10 | [11] |
| LLM agent tool count performance degradation fewer tools better results empirical | WebSearch | all | 10 | [9] |
| Poppendieck lean software development last responsible moment defer decisions | WebSearch | all | 10 | [10] |
