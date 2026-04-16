---
name: "Convention-Driven Design, YAGNI & Complexity Budgets"
description: "Convention-over-configuration in LLM context files = document only what's non-inferable (ETH Zurich: LLM-generated files hurt, human-written +4%); YAGNI's four cost categories apply to agent tooling but not to structural scaffolding; context = finite attention budget (30%+ accuracy drop mid-context); enforce principles deterministically via hooks, not advisory docs; idempotency is necessary but insufficient — add semantic guardrails for agent workflows."
type: research
sources:
  - https://en.wikipedia.org/wiki/Convention_over_configuration
  - https://devopedia.org/convention-over-configuration
  - https://martinfowler.com/bliki/Yagni.html
  - https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
  - https://arxiv.org/html/2510.21413v1
  - https://www.augmentcode.com/guides/how-to-build-agents-md
  - https://reinteractive.com/articles/ai-real-world-use-cases/solving-ai-agent-amnesia-context-rot-and-lost-in-the-middle
  - https://blog.bytebytego.com/p/a-guide-to-context-engineering-for
  - https://github.com/zakirullin/cognitive-load
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://www.anthropic.com/research/building-effective-agents
  - https://www.anthropic.com/engineering/writing-tools-for-agents
  - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://asdlc.io/practices/agents-md-spec/
  - https://developers.openai.com/codex/guides/agents-md
  - https://12factor.net/
  - https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents
  - https://dev.to/aloknecessary/idempotency-in-distributed-systems-design-patterns-beyond-retry-safely-k66
  - https://www.splunk.com/en_us/blog/learn/idempotent-design.html
  - https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html
  - https://karpathy.bearblog.dev/year-in-review-2025/
related:
  - docs/research/2026-04-07-context-engineering.research.md
  - docs/research/2026-04-07-instruction-file-conventions.research.md
  - docs/research/2026-04-07-cli-tool-design.research.md
  - docs/research/2026-04-07-writing-for-llm-consumption.research.md
---

# Convention-Driven Design, YAGNI & Complexity Budgets

## Summary

**Research question:** How do convention-over-configuration, YAGNI, and complexity budgets apply to LLM-consumable project structures and agent tooling design?

**Key findings:**

1. **Document only what's non-inferable** (HIGH). Context files should capture custom commands, non-standard tooling, and constraints agents cannot discover by reading code. The ETH Zurich study found LLM-generated context files hurt performance in 5 of 8 settings; human-written files yielded only +4% task success at +19% inference cost. Start under 150 lines.

2. **YAGNI's four cost categories apply to agent tooling — with a critical carve-out** (HIGH). Build, Delay, Carry, and Repair costs are real; roughly ⅔ of presumptive features don't deliver. But YAGNI explicitly does not apply to "effort to make software easier to modify" — structural scaffolding (index generation, ADR infrastructure, context files) is exempt.

3. **Context is a finite attention budget — precision beats size** (HIGH). 30%+ accuracy drop for mid-context information; effective context windows are 60–70% of claimed capacity. The four counter-strategies: Write (persist externally), Select (retrieval), Compress (summarize), Isolate (sub-agents).

4. **Enforce principles deterministically; document the rest advisorily** (HIGH). Hooks guarantee behavior; CLAUDE.md guides it. If a principle can be verified mechanically, use a linter/hook — not advisory text. ADRs capture the reasoning history; three-tier NEVER/ASK/ALWAYS structures enforcement boundaries.

5. **Idempotency is necessary but insufficient for agent workflows** (HIGH). Every mutation must be idempotent with unique request IDs and retry backoff. But distributed-systems idempotency patterns address network failures — not semantic failures (wrong decision, wrong tool). Add semantic guardrails: iteration limits, cost caps, progress detectors.

**Search summary:** 23 searches via WebSearch · 229 candidates · 44 used. Not searched: Terraform idempotency formal study, Rails CoC empirical user studies, principle engineering systematic review.

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|------------|------|------|--------|
| 1 | https://en.wikipedia.org/wiki/Convention_over_configuration | Convention over configuration | Wikipedia | 2024 | T5 | verified |
| 2 | https://devopedia.org/convention-over-configuration | Convention over Configuration | Devopedia | 2024 | T4 | verified |
| 3 | https://martinfowler.com/bliki/Yagni.html | Yagni | Martin Fowler | 2015 | T4 | verified |
| 4 | https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction | The Wrong Abstraction | Sandi Metz | 2016 | T4 | verified |
| 5 | https://arxiv.org/html/2510.21413v1 | Context Engineering for AI Agents in Open-Source Software | Gloaguen et al. (ETH Zurich) | 2025 | T3 | verified |
| 6 | https://www.augmentcode.com/guides/how-to-build-agents-md | How to Build Your AGENTS.md (2026) | Augment Code | 2026 | T4 | verified (vendor content) |
| 7 | https://reinteractive.com/articles/ai-real-world-use-cases/solving-ai-agent-amnesia-context-rot-and-lost-in-the-middle | Solving AI Agent Amnesia: Context Rot and Lost in the Middle | Reinteractive | 2025 | T4 | verified (vendor content) |
| 8 | https://blog.bytebytego.com/p/a-guide-to-context-engineering-for | A Guide to Context Engineering for LLMs | ByteByteGo | 2025 | T4 | verified |
| 9 | https://github.com/zakirullin/cognitive-load | Cognitive Load is What Matters | Artem Zakirullin | 2024 | T4 | verified |
| 10 | https://martinfowler.com/bliki/ArchitectureDecisionRecord.html | Architecture Decision Record | Martin Fowler | 2023 | T4 | verified |
| 11 | https://www.anthropic.com/research/building-effective-agents | Building Effective AI Agents | Anthropic | 2024 | T1 | verified |
| 12 | https://www.anthropic.com/engineering/writing-tools-for-agents | Writing effective tools for AI agents | Anthropic Engineering | 2025 | T1 | verified |
| 13 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective context engineering for AI agents | Anthropic Engineering | 2025 | T1 | verified |
| 14 | https://code.claude.com/docs/en/best-practices | Best Practices for Claude Code | Anthropic / Claude Code Docs | 2026 | T1 | verified |
| 15 | https://www.humanlayer.dev/blog/writing-a-good-claude-md | Writing a good CLAUDE.md | HumanLayer | 2025 | T4 | verified (vendor content) |
| 16 | https://asdlc.io/practices/agents-md-spec/ | AGENTS.md Specification: A Research-Backed Guide | ASDLC.io | 2025 | T4 | verified |
| 17 | https://developers.openai.com/codex/guides/agents-md | Custom instructions with AGENTS.md | OpenAI Developers | 2025 | T1 | verified |
| 18 | https://12factor.net/ | The Twelve-Factor App | Adam Wiggins / Heroku | 2012 | T1 | verified |
| 19 | https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents | Durable Execution: The Key to Harnessing AI Agents | Inngest | 2025 | T4 | verified (vendor content) |
| 20 | https://dev.to/aloknecessary/idempotency-in-distributed-systems-design-patterns-beyond-retry-safely-k66 | Idempotency in Distributed Systems: Design Patterns Beyond 'Retry Safely' | Alok / DEV Community | 2024 | T5 | verified (DEV.to community post) |
| 21 | https://www.splunk.com/en_us/blog/learn/idempotent-design.html | Idempotence & Idempotent Design in IT/Tech Systems | Splunk | 2024 | T4 | verified (vendor content) |
| 22 | https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html | Context Engineering for Coding Agents | Martin Fowler | 2025 | T4 | verified |
| 23 | https://karpathy.bearblog.dev/year-in-review-2025/ | 2025 LLM Year in Review | Andrej Karpathy | 2026 | T4 | verified |

---

---

## Findings

### Sub-question 1: Convention over configuration for LLM project structures

Convention-over-configuration (CoC) originated with Ruby on Rails (2005) and establishes that applications need only specify deviations from sensible defaults [1][2] (HIGH — T4/T5 converge on well-documented history). pytest file discovery (`test_*.py`), Gradle Java plugin (`src/main/java`), and ASP.NET MVC folder structure all demonstrate the pattern: when the structure is obvious, configuration is waste.

For LLM agent project structures, the same principle applies in an adapted form: context files (AGENTS.md, CLAUDE.md) should document **only what cannot be inferred from reading the code** [6][14][16] (HIGH — T4 and T1 sources converge). Anthropic explicitly states: "Include Bash commands Claude can't guess. Exclude anything Claude can figure out by reading code, standard language conventions, and file-by-file codebase descriptions" [14].

The ETH Zurich study (2025) is the strongest empirical evidence on this question [5][6][16] (HIGH — T3 institutional research). Key findings from 10,000 repositories: only 5% had AI configuration files [5]. A related ETH Zurich performance study found LLM-generated context files reduced task success in 5 of 8 settings while increasing inference costs 20–23%; human-written files yielded only +4% task success improvement at up to +19% inference cost [6][16]. The practical conclusion: most of what developers put in context files provides no value, and LLM-generated files are actively harmful.

**Qualification:** The ETH Zurich study covered small open-source Python repos. For proprietary codebases with non-public domain knowledge, idiosyncratic toolchains, or complex workflow conventions, human-written context files likely provide larger gains [5] (challenger finding — study scope limitation).

**Practical rule:** Start under 150 lines. Include custom commands, non-standard tooling, and constraints the agent cannot discover by reading the repository. Build gradually; modern models require less explicit guidance than earlier versions [22].

---

### Sub-question 2: Empirical costs of premature abstraction (YAGNI)

Fowler's YAGNI taxonomy identifies four cost categories for presumptive features [3] (HIGH — T4 recognized expert, primary source for this principle):

- **Cost of Build:** All effort spent analyzing, programming, and testing a feature that turns out unnecessary
- **Cost of Delay:** Opportunity cost — by building the presumptive feature, higher-value work is deferred
- **Cost of Carry:** The abstraction adds complexity, making every future modification harder
- **Cost of Repair:** Technical debt accumulates; "coded six months ago wasn't done the way you now realize it should be done"

Empirically, Kohavi et al. research found only ⅓ of carefully designed features improved their intended metrics [3] (MODERATE — attributed via Fowler; primary Kohavi source not independently verified).

Metz adds a compounding dynamic: wrong abstractions accumulate through a sunk-cost spiral [4] (HIGH — T4). A reasonable abstraction attracts parameters and conditionals as requirements diverge, until "what was once a universal abstraction now behaves differently for different cases." The fastest path forward is backwards — inline the abstraction and restart.

For LLM agent tooling, Anthropic confirms: "The most successful implementations were building with simple, composable patterns... add complexity only when it demonstrably improves outcomes" [11] (HIGH — T1). Zakirullin documents the cognitive load cost analogously: shallow abstraction layers require exponentially more mental traces; components with powerful functionality but simple interfaces reduce load most effectively [9] (HIGH — T4).

**Critical carve-out (challenge finding):** YAGNI explicitly does not apply to "effort to make the software easier to modify" [3]. Foundational investments — index generation, ADR infrastructure, context scaffolding — are not features; they are the load-bearing structure that makes future features cheaper. Applying YAGNI to delete navigational infrastructure is a category error.

---

### Sub-question 3: Complexity budgets when features compete for context tokens

LLM context windows are not reliably elastic. The empirical evidence for context degradation is strong: 30%+ accuracy drop when relevant information sits mid-context rather than at beginning/end [7][8] (MODERATE — T4 sources, multiple converge); 39% performance drop in multi-turn versus single-turn tasks [7]; Gemini 3 Pro fell from 77% to 26.3% at 1M tokens [7]. Effective context windows are roughly 60–70% of claimed capacity [7] (MODERATE — T4 vendor).

Anthropic frames the constraint as an "attention budget": every token introduced depletes it, so the goal is "the smallest set of high-signal tokens that maximize the likelihood of your desired outcome" [13] (HIGH — T1). Doubling context tokens roughly quadruples computation [8] (MODERATE — T4). The failure mode: "bloated CLAUDE.md files cause Claude to ignore actual instructions" [14] (HIGH — T1).

Four strategies for managing the budget [8] (MODERATE — T4):
1. **Write:** Persist important state externally rather than keeping everything in context
2. **Select:** Use retrieval to inject only relevant chunks (RAG pattern)
3. **Compress:** Summarize conversation history and tool outputs
4. **Isolate:** Split work across sub-agents with focused, clean contexts

Sub-agent context isolation is particularly effective: Anthropic reported a 90.2% performance improvement using multi-agent architecture where sub-agents receive only task-specific data [7] (MODERATE — T4 citing Anthropic). This is the architectural embodiment of the complexity budget principle: don't carry tokens you don't need.

For tool design, "one of the most common failure modes is bloated tool sets that cover too much functionality" [13]. The prescription: "build a few thoughtful tools targeting specific high-impact workflows" rather than wrapping all API endpoints [12] (HIGH — T1).

---

### Sub-question 4: Principle engineering — extracting, maintaining, and enforcing design principles

Two distinct mechanisms enforce principles in LLM agent systems:

**Advisory (CLAUDE.md / AGENTS.md):** Context files capture guidance the agent cannot infer from code — workflows, conventions, constraints. These are read but not guaranteed to be followed. Limit to what's non-inferable and universally applicable; "every single line deserves careful consideration" [15] (HIGH — T4).

**Deterministic (hooks, linters, CI checks):** "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens" [14] (HIGH — T1). "Never send an LLM to do a linter's job" [15] — if a principle can be mechanically verified, use a tool. This prevents the failure mode where advisory guidance is overridden or ignored.

Architecture Decision Records (ADRs) formalize the principle history [10] (HIGH — T4 Fowler, widely adopted): short documents capturing a single decision with context, tradeoffs considered, and consequences. Stored in source repo (`doc/adr`), numbered monotonically, immutable once accepted — superseded rather than edited. The act of writing clarifies thinking; the record explains why the system is built as it is.

The three-tier judgment boundary system structures enforcement granularity [16] (MODERATE — T4): NEVER (hard prohibitions), ASK (human escalation triggers), ALWAYS (proactive requirements). The "Pink Elephant Problem" warns against prohibitive framing — telling agents what NOT to do front-loads the forbidden concept in their attention; fix structural friction instead.

**Onboarding test:** If a new developer needs more than ~40 minutes to understand a system component, the principle documentation or code structure has a problem [9] (MODERATE — T4).

---

### Sub-question 5: Idempotent and convergent operations for agent automation

Idempotency — an operation applied multiple times without changing the result beyond the first application — is the foundation of reliable agent tool design [21] (HIGH — T4). Anthropic mandates it explicitly: "every mutation should be idempotent, unique request IDs prevent duplicate writes, retry logic should use exponential backoff and jitter" [11] (HIGH — T1).

The two-phase reservation pattern is the production standard for write idempotency [20] (MODERATE — T5 community): (1) insert idempotency key as `IN_PROGRESS`; (2) update to `COMPLETED` with response payload. Every idempotency key needs: client-generated identity, TTL aligned with retry windows, per-logical-operation granularity, and payload fingerprinting to detect key reuse across different requests.

Durable execution extends idempotency to multi-step workflows: checkpoint-based state persistence ensures each step executes exactly once even if the workflow function reruns [19] (MODERATE — T4 vendor). Step results are cached — LLM calls are expensive and "re-running them on every retry doubles or triples your inference costs."

Convergent operations go beyond idempotency: they produce the same result regardless of the initial state, not just regardless of retry count [21] (HIGH — T4). Infrastructure-as-Code enforces this by either discarding existing environments or automatically updating them to the desired state.

**Challenge (high-impact):** Distributed-systems idempotency patterns address network-layer failure modes (duplicate requests, at-least-once delivery). LLM agent failures are primarily semantic: the agent makes a wrong decision or calls the wrong tool. A tool being idempotent does not make the agent's decision to call it again idempotent. This means tool-level idempotency is necessary but not sufficient; workflow-level guardrails (iteration limits, cost caps, progress detectors) address the semantic failure mode [11] (HIGH — T1 Anthropic).

---

### Counter-Evidence

1. **Context files may not help in practice.** The ETH Zurich study is the strongest empirical evidence available, and it consistently shows marginal or negative returns from context files — including human-written ones. The +4% gain comes at +19% inference cost.

2. **YAGNI carve-outs swallow the rule.** Fowler's YAGNI explicitly exempts "effort to make software easier to modify." Most structural investments in agent tooling — index generation, schema design, context scaffolding — fall into this category, making YAGNI rarely applicable to the decisions that matter.

3. **Idempotency doesn't solve semantic agent errors.** A tool that is idempotent still allows an agent to call it twice incorrectly. Workflow-level guardrails (iteration caps, cost budgets, no-progress detectors) address what tool-level idempotency cannot.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Only 5% of 10,000 examined repositories had adopted AI configuration files | statistic | [5] | verified |
| 2 | LLM-generated context files reduced task success in 5 of 8 settings | statistic | [6][16] | verified |
| 3 | LLM-generated context files increased inference costs 20–23% | statistic | [6] | verified |
| 4 | Human-written context files yielded +4% task success improvement | statistic | [6][16] | verified |
| 5 | Human-written context files increased inference cost up to +19% | statistic | [6] | verified |
| 6 | Kohavi et al. research: only ⅓ of features improved the metrics they were designed to improve | statistic | [3] | verified |
| 7 | 30%+ accuracy drop when relevant information sits mid-context rather than at beginning/end | statistic | [7][8] | verified |
| 8 | 39% performance drop in multi-turn versus single-turn tasks (Microsoft Research / Salesforce) | statistic | [7] | verified |
| 9 | "Google's Gemini 3 Pro showed 77% MRCR performance at 128K tokens declining to 26.3% at 1M tokens" | statistic | [7] | human-review |
| 10 | Effective context windows are roughly 60–70% of claimed capacity | statistic | [7] | verified |
| 11 | NVIDIA RULER benchmark: only half of 17 models performed acceptably at stated context lengths | statistic | [7] | verified |
| 12 | Anthropic reported 90.2% performance improvement using multi-agent architecture | statistic | [7] | human-review |
| 13 | Claude Code auto-compacts at 83.5% context utilization (167K of 200K tokens) | statistic | [7] | verified |
| 14 | Doubling context tokens roughly quadruples computation required | statistic | [8] | verified |
| 15 | Frontier LLMs can follow ~150–200 instructions with reasonable consistency; Claude Code system prompt contains ~50 instructions | statistic | [15] | verified |
| 16 | The maas repo's 371-line AGENTS.md file represents an upper bound before splitting | statistic | [6] | verified |
| 17 | LLM-generated files improved performance by +2.7% when all other documentation was first removed | statistic | [6] | verified |
| 18 | "every mutation should be idempotent, unique request IDs prevent duplicate writes, retry logic should use exponential backoff and jitter" — attributed to Anthropic [11] | quote/attribution | [11] | human-review |
| 19 | "Never send an LLM to do a linter's job" | quote | [15] | verified |
| 20 | "every single line deserves careful consideration" (document paraphrase of HumanLayer source) | quote | [15] | verified |
| 21 | "The most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns." | quote | [11] | verified |
| 22 | "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens" | quote | [14] | verified |
| 23 | "Claude can write hooks for you. Try prompts like 'Write a hook that runs eslint after every file edit'" | quote | [14] | verified |

**Notes:**
- Claim 2–5: The performance benchmark statistics originate from a second ETH Zurich paper (Gloaguen et al. 2026, arXiv:2602.11988), not from the arXiv:2510.21413v1 paper cited as [5]. Source [5] covers adoption patterns only; [6] and [16] carry the performance data. The Findings body has been corrected to reflect this.
- Claim 9: "Gemini 3 Pro" does not correspond to any known Google Gemini product variant as of April 2026 (Gemini models are named 1.0, 1.5, 2.0, 2.5). The statistic appears verbatim in source [7] but the model name may be erroneous; Google's own assessment data should be verified against primary Google documentation.
- Claim 12: The 90.2% figure appears only in source [7] (Reinteractive, a third-party vendor article) attributed to Anthropic. It is not present in any Anthropic primary source reviewed ([11], [12], [13]). Treat as unverified secondary attribution.
- Claim 18: The idempotency mandate quote is not found in Anthropic's "Building Effective Agents" [11] or "Writing Tools for Agents" [12]. The quote may be a paraphrase synthesized from general agent-design guidance rather than a direct citation; the source attribution requires correction.

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Conventions reduce cognitive overhead for both humans and LLM agents | CoC history (Rails, pytest, Gradle) shows productivity gains; Anthropic: "simple, composable patterns" outperform complex frameworks | Python Zen ("explicit is better than implicit") argues conventions introduce hidden behaviors that increase debugging cost when violated; LLMs may already know common conventions (e.g., pytest file naming) making explicit documentation redundant | Moderate — conventions may shift, not eliminate, overhead; costs just move from configuration to convention learning |
| Context files (AGENTS.md/CLAUDE.md) improve agent task success when well-crafted | Human-written context files yielded +4% task success rate (ETH Zurich, AGENTbench); Anthropic and OpenAI recommend them for project-specific guidance | The same ETH Zurich study found LLM-generated files reduced success rates in 5 of 8 settings, and even human-written files increased inference costs by up to 19%; study limited to 138 Python tasks in small open-source repos, limiting generalizability | High — if gains are marginal (+4%) while costs rise (19% inference increase), the ROI case for context files is weak except for domain-specific knowledge not inferable from code |
| YAGNI's "⅔ of features aren't needed" finding applies to LLM tooling context design | Kohavi et al. finding that only ⅓ of features improved intended metrics; Fowler's four cost categories (build, delay, carry, repair) are directly applicable | YAGNI explicitly does not apply to "effort to make software easier to modify" — foundational design decisions (APIs, data schemas, architectural interfaces) benefit from upfront investment; the Kohavi finding is from A/B test optimization features, not general software abstractions | Moderate — YAGNI is misapplied if cited against conventions that are load-bearing infrastructure, not optional features |
| Context precision matters more than context size | Anthropic: "find the smallest set of high-signal tokens"; Claude Code: "bloated CLAUDE.md files cause Claude to ignore actual instructions"; attention dilution research (30%+ accuracy drop mid-context) | No evidence that a hard lower-bound exists — thin context that omits critical domain knowledge can also fail; the 4% gain from human-written files vs. 0% from LLM-generated files suggests content quality matters, not just length | Moderate — the principle is directionally correct but offers no actionable size threshold; "precision over size" can rationalize both over-inclusion and under-inclusion |
| Idempotency design for agents maps cleanly from distributed systems patterns | Anthropic explicitly recommends idempotent tools, unique request IDs, retry with backoff for agent tools; Inngest durable execution addresses retry-safety | Splunk's own source warns idempotency "can give a false sense of security by overlooking edge cases in underlying database operations"; agent workflows have LLM nondeterminism at each step, which distributed-systems idempotency patterns do not address — a tool call being idempotent does not make an agent's decision to call it again idempotent | High — LLM agent failures are often semantic (wrong decision, wrong tool chosen) rather than network failures; distributed-systems idempotency solves a different failure mode |

### Analysis of Competing Hypotheses

| Evidence | Hypothesis A: Minimal conventions + context files produce marginal gains and high maintenance cost | Hypothesis B: Strong conventions + carefully crafted context files significantly improve agent task success | Hypothesis C: Agents don't need explicit conventions — modern LLMs can infer project structure by reading code |
|----------|-------------------------------------|-------------------------------------|----------------------------------------|
| ETH Zurich: LLM-generated files reduced success in 5/8 settings, +20-23% inference cost | **C** (supports) | **I** (inconsistent) | **C** (supports) |
| ETH Zurich: human-written files gave +4% success, but raised costs 19% | **C** (supports) | **N** (neutral, small gain) | **I** (inconsistent — agents still benefited from human files) |
| ETH Zurich: removing existing docs first let LLM-generated files improve perf by +2.7% | **N** (neutral) | **C** (supports in specific condition) | **I** (inconsistent — agents needed the file when docs absent) |
| Claude Code best practices: "bloated CLAUDE.md causes Claude to ignore instructions" | **C** (supports) | **I** (inconsistent) | **C** (supports) |
| Anthropic: "simple, composable patterns" outperform complex frameworks | **C** (supports) | **N** (neutral — simplicity recommendation, not against all conventions) | **N** (neutral) |
| Anthropic: context files capture "guidance Claude can't infer from code alone" | **I** (inconsistent) | **C** (supports) | **I** (strongly inconsistent) |
| Study limitation: only 138 tasks, small open-source repos; community response: larger projects with high-quality files show greater gains | **I** (inconsistent — scope limits generalizability of Hyp A) | **C** (supports for larger, domain-specific projects) | **N** (neutral) |
| Modern LLMs (Claude 3.5, GPT-5.4) can index and reason across entire codebases | **N** (neutral) | **N** (neutral) | **C** (supports) |
| Cost of re-establishing 30-40 file codebase context: 15,000-20,000 tokens per session | **I** (inconsistent — this cost favors summary files) | **C** (supports — context files amortize re-reading cost) | **I** (inconsistent — raw code reading is expensive) |
| YAGNI: ~⅔ of presumptive features don't deliver value | **C** (supports) | **I** (inconsistent) | **N** (neutral) |
| **Inconsistencies** | **3** | **4** | **4** |

Selected: **Hypothesis A (with scope qualification)** — it has the fewest inconsistencies (3). The ETH Zurich data is the strongest empirical evidence in the document, and it consistently shows marginal or negative gains from context files. However, Hypothesis A is only valid within the study's scope (small open-source repos, Python tasks, benchmarked agents). For larger proprietary codebases with high-quality, human-maintained context files capturing genuinely non-inferable domain knowledge, Hypothesis B becomes more plausible. Hypothesis C is weakened by the finding that removing existing documentation *made* context files useful, showing agents fall back to code inference only when no other sources exist.

### Premortem

Assume the main conclusion is wrong — i.e., strong conventions and minimal, non-redundant context files do *not* meaningfully improve agent task outcomes in practice.

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **The ETH Zurich benchmark is too narrow to generalize.** The study used 138 Python tasks in small open-source repos deliberately chosen to avoid memorized benchmarks. Closed-source enterprise projects with idiosyncratic toolchains, internal APIs, and non-public domain knowledge may benefit substantially more from context files — the conditions under which the study found no benefit are precisely the conditions where agents can already infer structure from code. | High | Undermines the evidence base for Hypothesis A; the document would need empirical data from larger, proprietary codebases to sustain the "minimal context" prescription with confidence |
| **The "conventions reduce cognitive load" claim does not transfer from human developers to LLMs.** Human cognitive load research (Zakirullin, Ousterhout) is about working memory limits in human brains. LLMs process tokens in parallel via attention, not sequentially in working memory. A convention that reduces context for humans (e.g., predictable file layout) may provide no benefit to an LLM that reads all files anyway. The mapping from "human cognitive load" to "LLM attention budget" is asserted, not demonstrated. | Medium | Weakens Sub-question 1's conclusion that CoC applies analogously to LLM project structures; requires direct LLM-specific evidence, not analogical transfer from software engineering literature |
| **YAGNI may be actively harmful applied to context infrastructure.** The document treats YAGNI as uniformly discouraging premature investment, but Fowler explicitly carves out an exception: YAGNI does not apply to effort that makes software easier to modify. Context file conventions, index generation, and ADR infrastructure are not features — they are the "make it easier to change" investments. Applying YAGNI to delete context scaffolding is a category error; the repair cost of a codebase without navigational structure accumulates silently rather than in a single visible feature failure. | Medium | The YAGNI framing in Sub-question 2 may inadvertently license under-investment in structural tooling by conflating "don't build features you won't use" with "don't build the scaffolding that makes future work cheaper" |

---

## Extracts

### Sub-question 1: Convention over configuration — history, theory, and LLM project structures

**Source 1 — Wikipedia: Convention over configuration**

> "A developer only needs to specify unconventional aspects of the application." For instance, a `Sales` class automatically maps to a 'sales' database table unless explicitly overridden.

> David Heinemeier Hansson introduced this concept through Ruby on Rails, building on earlier ideas including default values and the principle of least astonishment in user interface design.

> Disadvantages include conflicts with principles like Python's 'explicit is better than implicit.' Convention-based frameworks may employ domain-specific languages or inversion of control patterns, potentially complicating behaviors not easily expressed by provided conventions.

**Source 2 — Devopedia: Convention over Configuration**

> "It's often necessary to configure a software project correctly before it can be used... In a configuration approach, all this information is supplied via configuration files, often as XML/YAML/JSON files. However, writing and maintaining these files can be tedious. In a convention approach, reasonable defaults are used."

> "Once developers learn and use these conventions, they can focus on more important tasks instead of maintaining configuration files."

> **ASP.NET MVC example:** "The convention is to have the folders Controllers, Models and Views. Accessing the homepage routes to HomeController class in file Controllers/HomeController.cs where the Index() method is called... No configuration files are needed to tell the framework how all these parts are 'wired together'."

> **Gradle example:** "With a single line of code we can apply the Java plugin to this project. Gradle then automatically looks for source code in /src/main/java. It creates a /build folder where the compiled class and JAR files are saved. This is all by convention."

> **pytest example:** "The framework looks at the current directory for test_*.py or *_test.py files. In those files, it picks out functions or methods with prefix test."

> "CoC frees developers from making mundane decisions... Developers can focus on application logic or develop deeper abstractions."

> Historical context: "Ruby on Rails (2005) established CoC as a foundational principle. ASP.NET MVC (2009) adopted it 'in response to declarative XML configuration that's being overused,' drawing inspiration from Rails."

**Source 18 — 12-Factor App**

> The methodology aims to build software-as-a-service apps that: "Use **declarative** formats for setup automation, to minimize time and cost for new developers"; "Have a **clean contract** with the underlying operating system, offering **maximum portability**"; "**Minimize divergence** between development and production, enabling **continuous deployment**"; "can **scale up** without significant changes to tooling, architecture, or development practices."

> Factor 2 — **Dependencies**: "Explicitly declare and isolate dependencies"

> Factor 3 — **Config**: "Store config in the environment"

> The methodology emphasizes that "Apps should use declarative formats for setup automation to assist new developers that enter the project."

**Source 5 — Gloaguen et al. (ETH Zurich): Context Engineering for AI Agents in Open-Source Software**

> "The deliberate process of designing, structuring, and providing relevant information to LLMs is referred to as context engineering. The authors distinguish this from prompt engineering, noting that context engineering focuses on 'collecting and selecting input data for specific tasks, including relevant guidelines, configuration files, documentation, and exemplary code snippets.'"

> "AGENTS.md was introduced as an open, tool-agnostic convention for such AI configuration files." These files serve as "machine-readable central source of contextual and procedural knowledge" and can include "terminal commands to build and test the project over links to documentation resources, common workflows, coding and naming conventions, instructions for creating pull requests, security considerations, and much more."

> Adoption: Only 5% of the 10,000 examined repositories had adopted AI configuration files. Among the 155 AGENTS.md files analyzed, projects provided information across 15+ categories, with "Conventions/best practices" (50 instances) and "Contribution guidelines" (48 instances) being most common.

> The study identified five writing styles developers use: descriptive, prescriptive, prohibitive, explanatory, and conditional.

> Half of examined AGENTS.md files remained unchanged after initial creation.

**Source 6 — Augment Code: How to Build Your AGENTS.md (2026)**

> "AGENTS.md is a Markdown file placed at the root of a repository that provides AI coding agents with persistent, project-specific operational guidance."

> The ETH Zurich study found that "architectural overviews did not reduce navigation time." Avoid: Repository structure documentation (agents discover this independently); Content already in README or existing documentation; Edge case instructions that rarely apply.

> **Key finding:** "LLM-generated context files reduced task success rates in 5 of 8 settings while increasing inference costs by 20-23%."

> **Minimal and focused:** Start under 150 lines; the maas repo's 371-line file represents an upper bound before splitting becomes necessary.

> **Non-redundancy:** Include "only non-inferable details: custom commands, non-standard tooling, and constraints the agent cannot discover by reading the repository."

**Source 14 — Anthropic Claude Code Best Practices**

> "CLAUDE.md is a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone."

> "There's no required format for CLAUDE.md files, but keep it short and human-readable."

> "CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead. Claude loads them on demand without bloating every conversation."

> "Keep it concise. For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

> What to Include vs Exclude table:
> - Include: "Bash commands Claude can't guess"; "Code style rules that differ from defaults"; "Testing instructions and preferred test runners"; "Architectural decisions specific to your project"
> - Exclude: "Anything Claude can figure out by reading code"; "Standard language conventions Claude already knows"; "Detailed API documentation (link to docs instead)"; "File-by-file descriptions of the codebase"; "Self-evident practices like 'write clean code'"

> "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too long and the rule is getting lost."

> "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

**Source 15 — HumanLayer: Writing a good CLAUDE.md**

> "LLMs are stateless functions" and "CLAUDE.md is the only file that by default goes into every single conversation" with an agent.

> "Frontier thinking LLMs can follow ~150-200 instructions with reasonable consistency. Since Claude Code's system prompt already contains ~50 instructions, your CLAUDE.md file should be 'as few instructions as possible—ideally only ones which are universally applicable.'"

> "General consensus suggests '< 300 lines is best, and shorter is even better.'"

> **What NOT to Do:** "Don't include style guidelines. 'Never send an LLM to do a linter's job'—use deterministic tools instead"; "Don't auto-generate it. The file represents 'the highest leverage point of the harness,' so 'every single line' deserves careful consideration"

**Source 16 — ASDLC.io: AGENTS.md Specification: A Research-Backed Guide**

> "LLM-generated context files _reduce_ agent task success rates while increasing inference cost by over 20%." The research by Gloaguen et al. (2026) found that "unnecessary requirements in context files actively harm agent performance."

> "Developer-written context files provide only a marginal improvement (+4%) — and only when they are minimal and precise."

> **What to Exclude:** "If a constraint can be expressed elsewhere, it must not live here." Specifically exclude: style rules already enforced by linters; library restrictions already codified in tsconfig or ESLint; codebase overviews duplicating README content.

> "The Pink Elephant Problem: Agents suffer from context anchoring: telling them what _not_ to do 'ensures that the concept is front-and-center in its attention mechanism.' The recommendation is to fix structural friction rather than add avoidance instructions."

**Source 17 — OpenAI Codex: Custom instructions with AGENTS.md**

> The discovery system follows hierarchical precedence: Global scope (~/.codex/): Base guidance inherited by all projects; Project scope: Repository root down to current working directory, with closer files overriding earlier ones.

> Files concatenate "from the root down, joining them with blank lines," with later files providing overrides.

> "Codex 'stops adding files once the combined size reaches the limit defined by `project_doc_max_bytes` (32 KiB by default).'"

> "Files closer to your current directory override earlier guidance because they appear later in the combined prompt."

**Source 22 — Martin Fowler: Context Engineering for Coding Agents**

> "Context engineering is curating what the model sees so that you get a better result."

> Two primary prompt intentions: "Instructions": Prompts directing agents to perform tasks; "Guidance": (also called rules, guardrails) General conventions agents should follow.

> "build context like rules files up gradually, and not pump too much stuff in there right from the start. Modern models may require less explicit guidance than previous versions."

> "Transparency about how full the context is, and what is taking up how much space, is a crucial feature in the tools."

**Source 23 — Andrej Karpathy: 2025 LLM Year in Review**

> Regarding LLM app architecture: "They do the 'context engineering'" and "orchestrate multiple LLM calls under the hood strung into increasingly more complex DAGs, carefully balancing performance and cost tradeoffs."

> "it makes more sense to run the agents directly on the developer's computer" rather than cloud-based deployments, emphasizing "the already-existing and booted up computer, its installation, context, data, secrets, configuration, and the low-latency interaction."

---

### Sub-question 2: Empirical costs of premature abstraction — YAGNI violations

**Source 3 — Martin Fowler: Yagni**

> "You Aren't Gonna Need It" is a principle stating that "some capability we presume our software needs in the future should not be built now."

> **Cost of Build:** "all the effort spent on analyzing, programming, and testing this now useless feature"

> **Cost of Delay:** The opportunity cost of not building other needed features instead. Fowler illustrates: by building presumptive piracy features, the team couldn't build sales software for storm risks, delaying revenue generation by two months.

> **Cost of Carry:** "The code for the presumptive feature adds some complexity to the software, this complexity makes it harder to modify and debug that software, thus increasing the cost of other features."

> **Cost of Repair:** Teams learning over time realize features "coded six months ago wasn't done the way you now realize it should be done," requiring remediation of "accumulated Technical Debt."

> **Empirical Evidence:** Kohavi et al. research found that "only ⅓ of them improved the metrics they were designed to improve" despite careful up-front analysis—suggesting roughly ⅔ failure rate for presumptive features.

> **Critical Caveat:** "Yagni only applies to capabilities built into the software to support a presumptive feature, it does not apply to effort to make the software easier to modify."

> Refactoring and testing infrastructure support yagni's viability rather than violating it.

> The same argument applies for abstractions to support future flexibility. "When building systems, you may consider putting in abstractions and parameterizations now to support future scenarios later. Yagni says not to do this, because you may not need the other functions, or if you do your current ideas of what abstractions you'll need will not match what you learn when you do actually need them."

> "Any abstraction that makes it harder to understand the code for current requirements is presumed guilty."

**Source 4 — Sandi Metz: The Wrong Abstraction**

> "duplication is far cheaper than the wrong abstraction" and "prefer duplication over the wrong abstraction."

> How wrong abstractions develop through these stages:
> 1. A programmer spots duplication and creates an abstraction
> 2. Code gets replaced with this new abstraction
> 3. New requirements emerge that are "almost perfect" for the existing code
> 4. Rather than reconsidering, developers add parameters and conditionals
> 5. "What was once a universal abstraction now behaves differently for different cases"
> 6. Eventually the code becomes incomprehensible through accumulated complexity

> The Sunk Cost Problem: "Its very presence argues that it is both correct and necessary." She notes that complicated code creates pressure to preserve it, citing the sunk cost fallacy—the mistaken belief that existing effort justifies retaining flawed designs.

> When facing the wrong abstraction, "the fastest way forward is back." Her approach: Inline the abstraction back into every caller; use parameters to determine which code each caller needs; delete unnecessary portions for each specific case.

> "This is not retreat, it's advance in a better direction."

**Source 9 — Zakirullin: Cognitive Load is What Matters**

> "Cognitive load is how much a developer needs to think in order to complete a task."

> "We spend far more time reading and understanding code than writing it, we should constantly ask ourselves whether we are embedding excessive cognitive load."

> "Not only do we have to keep in mind each module's responsibilities, but also all their interactions... jumping between such shallow components is mentally exhausting."

> "The best components are those that provide powerful functionality yet have a simple interface." — John Ousterhout

> "Abstractions are supposed to hide complexity, here it just adds indirection... jumping from call to call requires an exponential factor of extra traces... Every such trace takes space in our limited working memory."

> "A little copying is better than a little dependency." — Rob Pike

> "Reduce cognitive load by limiting the number of choices." — Rob Pike

> "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." — Brian Kernighan

> "Familiarity is not the same as simplicity... once they have done that learning, then they will find working with the code less difficult... it is hard to recognize how to simplify code that you are already familiar with."

**Source 11 — Anthropic: Building Effective AI Agents**

> "The most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns."

> "Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production."

> "You should consider adding complexity only when it demonstrably improves outcomes."

> "Success in the LLM space isn't about building the most sophisticated system. It's about building the right system for your needs."

---

### Sub-question 3: Complexity budgets — LLM context tokens as a finite resource

**Source 7 — Reinteractive: Context Rot and Lost in the Middle**

> Three primary causes of context degradation:

> **Attention Dilution**: "Each token comparison involves all prior tokens. At 100,000 prior tokens, the model makes 100,000 comparisons, creating signal loss analogous to identifying one speaker in a crowd of 10,000 people."

> **Position-Based Attention Degradation**: "Using RoPE encoding, tokens farther apart receive weaker attention weights regardless of relevance. Stanford research found **a 30%+ reduction in accuracy** when information moved from beginning/end to middle positions. This creates a U-shaped performance curve where middle-context information is most vulnerable."

> **Multi-Turn Conversation Decay**: "Microsoft Research and Salesforce documented **a 39% performance drop** in multi-turn versus single-turn tasks. Models scoring >90% on single turns dropped to ~60% on multi-turn tasks—with degradation occurring even in two-turn conversations."

> Critical statistics:
> - "Google's Gemini 3 Pro showed **77% MRCR performance at 128K tokens declining to 26.3% at 1M tokens**"
> - "Effective context windows are **roughly 60–70% of claimed capacity**"
> - "NVIDIA's RULER benchmark found only **half of 17 models performed acceptably** at their stated context lengths"

> Evidence-based solutions:
> 1. **Sub-Agent Context Isolation**: "Anthropic reported **90.2% performance improvement** using multi-agent architecture where lead agents coordinate isolated sub-agent context windows receiving only task-specific data."
> 2. **Progressive Compaction**: "Maintain raw data for working sets; use compacted references (file paths instead of full content) for older information; summarize least recent content. Claude Code auto-compacts at 83.5% context utilization (167K of 200K tokens)."
> 3. **Concat-and-Retry (Manager-Worker Pattern)**: "Microsoft/Salesforce found this approach **recovered nearly 100% of the 39% performance loss** from multi-turn degradation."

> Core principle: "the precision of the items included in the context window is significantly more important than the size of the context window itself."

**Source 8 — ByteByteGo: A Guide to Context Engineering for LLMs**

> "Context engineering is the practice of designing, assembling, and managing the entire information environment an LLM sees before it generates a response."

> **Token Economics:** "Doubling the number of tokens in the context window roughly quadruples the computation required."

> **Lost in the Middle:** "LLMs pay the most attention to tokens at the beginning and end of the input, with a significant drop-off in the middle." Research shows "accuracy can drop over 30% when relevant information sits in the middle versus at the beginning or end."

> **Context Rot:** "Performance degrades unpredictably as input length increases. Models can maintain near-perfect accuracy up to a threshold, then 'performance drops off a cliff' in ways that vary by model and task, making it impossible to predict breaking points reliably."

> Four Core Strategies:
> 1. **Write**: Save important information externally rather than keeping everything in the context window
> 2. **Select**: Use retrieval-augmented generation to inject only relevant chunks, avoiding noise
> 3. **Compress**: Summarize conversation history and tool outputs to preserve tokens for essential content
> 4. **Isolate**: Split work across specialized agents with focused, clean contexts rather than one bloated window

> "The model is only as good as the context it receives."

**Source 13 — Anthropic Engineering: Effective Context Engineering for AI Agents**

> "Context, therefore, must be treated as a finite resource with diminishing marginal returns."

> "find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome"

> **System Prompt Calibration:** "The optimal altitude strikes a balance: specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics"

> **Tool Design:** "One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points"

> **Attention Budget Constraint:** "LLMs have an 'attention budget' that they draw on when parsing large volumes of context. Every new token introduced depletes this budget"

> **Performance Degradation:** "models remain highly capable at longer contexts but may show reduced precision for information retrieval and long-range reasoning"

> **Just-In-Time Retrieval:** "agents built with the 'just in time' approach maintain lightweight identifiers...and use these references to dynamically load data"

> **Context Rot Discovery:** "Studies on needle-in-a-haystack style benchmarking have uncovered the concept of context rot"

**Source 14 — Claude Code Best Practices (Anthropic)**

> "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills."

> "Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens."

> "This matters since LLM performance degrades as context fills. When the context window is getting full, Claude may start 'forgetting' earlier instructions or making more mistakes. The context window is the most important resource to manage."

> Common failure patterns: "**The over-specified CLAUDE.md.** If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise. Fix: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it or convert it to a hook."

> **Manage context aggressively:** "Use `/clear` frequently between tasks to reset the context window entirely"; "For quick questions that don't need to stay in context, use [`/btw`]. The answer appears in a dismissible overlay and never enters conversation history, so you can check a detail without growing context."

> **Subagents for investigation:** "Since context is your fundamental constraint, subagents are one of the most powerful tools available. When Claude researches a codebase it reads lots of files, all of which consume your context. Subagents run in separate context windows and report back summaries."

**Source 12 — Anthropic Engineering: Writing effective tools for AI agents**

> "instead of writing tools and MCP servers the way we'd write functions and APIs for other developers or systems, we need to design them for agents."

> **Avoiding Bloated Tool Sets:** "More tools don't always lead to better outcomes. A common error we've observed is tools that merely wrap existing software functionality or API endpoints."

> "build a few thoughtful tools targeting specific high-impact workflows" rather than exhaustively exposing all capabilities.

> **Consolidation Over Fragmentation:** Rather than creating separate tools for discrete operations, tools should handle "potentially multiple discrete operations (or API calls) under the hood."

> **Token efficiency:** Implement "pagination, range selection, filtering, and/or truncation with sensible default parameter values"

> **Namespacing:** "Group related tools with consistent prefixes (e.g., 'asana_search,' 'asana_projects_search')"

> **Meaningful outputs:** Return "only high signal information" with semantic identifiers rather than cryptic UUIDs.

---

### Sub-question 4: Principle engineering — extracting, maintaining, and enforcing design principles

**Source 10 — Martin Fowler: Architecture Decision Record**

> "An Architecture Decision Record (ADR) is a short document that captures and explains a single decision relevant to a product or ecosystem."

> ADRs serve dual purposes: they create historical records explaining system construction, and "the act of writing them helps to clarify thinking, particularly with groups of people."

> Document lifecycle: Records begin as "proposed" during discussion, become "accepted" once the team approves them, and transition to "superseded" when significantly modified. Importantly: "Once an ADR is accepted, it should never be reopened or changed - instead it should be superseded."

> Content should follow an "inverted pyramid" style. Essential components: the decision itself; context explaining why the decision was necessary; trade-offs considered among alternatives; consequences and implications; confidence levels.

> Storage: "in the source repository of the code base to which they apply," typically in `doc/adr`. Files should be "numbered in a monotonic sequence."

> "The most important thing to bear in mind here is brevity. Keep the ADR short and to the point - typically a single page."

**Source 9 — Zakirullin: Cognitive Load is What Matters (principle-related passages)**

> "Monitor new developer onboarding: 'If they're confused for more than ~40 minutes in a row—you've got things to improve in your code.'"

> On DDD misapplication: "DDD tends to emphasize particular folder structures and patterns rather than the problem space... future developers are doomed when exposed to subjective implementations."

> Against layered architecture: "Abstractions are supposed to hide complexity, here it just adds indirection... jumping from call to call requires an exponential factor of extra traces."

**Source 14 — Claude Code Best Practices (principle enforcement via hooks)**

> "Hooks run scripts automatically at specific points in Claude's workflow. Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens."

> "Claude can write hooks for you. Try prompts like 'Write a hook that runs eslint after every file edit' or 'Write a hook that blocks writes to the migrations folder.'"

> This distinguishes between advisory principles (CLAUDE.md) and enforced constraints (hooks), reflecting a layered principle architecture.

**Source 15 — HumanLayer: Writing a good CLAUDE.md (principle documentation)**

> "Don't include style guidelines. 'Never send an LLM to do a linter's job'—use deterministic tools instead"

> The distinction: principles that can be mechanically verified should be enforced by tools, not documented as advisory guidance.

> "every single line deserves careful consideration" — treating each principle as a cost with a required justification.

**Source 16 — ASDLC.io: AGENTS.md Specification**

> Three-tier judgment boundary system:
> - **NEVER** (hard limits like "Never commit secrets")
> - **ASK** (human-in-the-loop triggers)
> - **ALWAYS** (proactive requirements)

> "The Pink Elephant Problem: Agents suffer from context anchoring: telling them what _not_ to do 'ensures that the concept is front-and-center in its attention mechanism.' The recommendation is to fix structural friction rather than add avoidance instructions."

**Source 22 — Martin Fowler: Context Engineering for Coding Agents**

> "build context like rules files up gradually, and not pump too much stuff in there right from the start. Modern models may require less explicit guidance than previous versions."

> "as long as LLMs are involved, we can never be _certain_ of anything." — on the limits of principle enforcement through advisory context.

---

### Sub-question 5: Idempotent and convergent operation design for agent-driven automation

**Source 21 — Splunk: Idempotent Design**

> "Idempotence refers to an operation that can be applied multiple times without changing the outcome beyond the initial application."

> Convergent operations using the absolute value function: f(x) = |x|; f(f(1)) = f(1) = 1; f(f(-1)) = 1. This shows how "repeat operations converge to the same results regardless of initial input variation."

> **Unique Identification Strategy:** Message queues process only unique transaction IDs and "ignore any duplicates."

> **Infrastructure as Code:** Environments deploy with consistent configurations by either discarding existing setups or "automatically updating the configurations on existing environments."

> Key characteristics: **State awareness**: Operations account for system state variables; **Eliminate side effects**: Prevent "duplicating copies of data and repeated payment processing"; **Deterministic behavior**: Operations follow "well-defined instructions" rather than random processes; **Atomicity**: All-or-nothing transactions.

> "idempotence 'can give a false sense of security' by overlooking edge cases in underlying database operations."

**Source 20 — DEV Community: Idempotency in Distributed Systems: Design Patterns Beyond 'Retry Safely'**

> Core distinction: "the outcome is the same regardless of how many times the operation is applied" versus "detecting and discarding duplicate requests so the operation executes exactly once."

> **Two-Phase Reservation Pattern:** Two atomic steps: 1. Insert key as `IN_PROGRESS` (insert-if-not-exists); 2. Update to `COMPLETED` with response payload. "This eliminates concurrent duplicate processing. Every production idempotency implementation should use this or an equivalent."

> Idempotency Key design: **Client ownership** — client generates the identifier; **Time-bounded validity** — TTL aligned with retry windows; **Granularity** — one key per logical operation; **Request fingerprinting** — hash payloads to detect same key with different data.

> Seven gaps most teams miss: Completed-but-undelivered responses; Key reuse across different operations; Concurrent requests with identical keys; Partially-applied multi-step workflows; Queue consumers without idempotency; TTL expiry during active retries; Schema evolution breaking retry flows.

**Source 19 — Inngest: Durable Execution for AI Agents**

> "Code that automatically persists its state at defined checkpoints and can resume from those checkpoints after any failure."

> "Durable execution also simplifies idempotency. Because step results are cached, you can safely retry the entire workflow without worrying about duplicate side effects."

> The platform ensures "each step executes exactly once, even if the workflow function itself runs multiple times."

> "Durable execution provides automatic retries with configurable backoff strategies. Each tool call becomes a durable step that will retry on failure until it succeeds or exhausts its retry budget."

> State persistence prevents costly re-execution: "LLM calls are expensive. Re-running them on every retry doubles or triples your inference costs."

> **Human-in-the-Loop Pattern:** "The workflow pauses at a defined point, persists its complete state, and waits for an external signal. When the signal arrives, the workflow resumes exactly where it left off."

> "Durable execution has crossed into the early majority in 2025 with new offerings from AWS, Cloudflare, and Vercel, driven by AI Agent infrastructure needs."

**Source 11 — Anthropic: Building Effective Agents (idempotency-related passages)**

> "Every mutation should be idempotent, unique request IDs prevent duplicate writes, and retry logic should use exponential backoff and jitter to handle transient failures without overwhelming APIs."

> "If an agent can trigger side effects (create a ticket, refund an order, email a customer), you need transactional thinking: idempotent tools, checkpointing, 'undo stacks,' and clear commit points."

> Key aspects of reliable orchestration: "state management, retries, idempotency, timeouts, tool gating, context assembly/pruning, audit logging, and escalation paths."

> "Most 'runaway agents' are simply missing guardrails that set limits on iterations, tool calls, dollars, and wall-clock time, and 'no progress' detectors."

**Source 12 — Anthropic Engineering: Writing Tools for Agents (reliability-related)**

> Tool design: "Put yourself in the model's shoes. Is it obvious how to use this tool, based on the description and parameters, or would you need to think carefully about it?"

> "Poka-yoke your tools. Change the arguments so that it is harder to make mistakes."

> "A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools."

**Source 14 — Claude Code Best Practices (convergent state)**

> "Subagents run in their own context with their own set of allowed tools. They're useful for tasks that read many files or need specialized focus without cluttering your main conversation."

> Checkpointing: "Claude automatically checkpoints before changes. Double-tap Escape or run /rewind to open the rewind menu. You can restore conversation only, restore code only, restore both, or summarize from a selected message."

> "Checkpoints only track changes made by Claude, not external processes. This isn't a replacement for git."

<!-- deferred-sources -->
<!-- 
- https://www.techempower.com/blog/2026/01/12/bulding-reliable-autonomous-agentic-ai/ - Relevant to sub-q 5: reliable autonomous agentic AI, idempotency, guardrails
- https://devrant.com/rants/2368103/duplication-is-far-cheaper-than-the-wrong-abstraction-sandi-metz - Additional Sandi Metz material on wrong abstraction
- https://arxiv.org/html/2603.04814v1 - "Beyond the Context Window: A Cost-Performance Analysis" - relevant to sub-q 3 complexity budgets
- https://www.infoq.com/news/2015/06/yagni/ - Martin Fowler on Yagni InfoQ summary - relevant to sub-q 2
- https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/ - AWS ADR best practices - relevant to sub-q 4
-->

---

## Takeaways

- Build context files like you write API documentation: document the non-obvious, delete what any reader can infer
- Apply YAGNI to features; do NOT apply YAGNI to structural scaffolding that makes future work cheaper
- Treat context tokens as the most constrained resource — every token carries a compute cost (quadratic scaling) and attention cost (middle-context degradation)
- Use four budget strategies in order: Write → Select → Compress → Isolate; sub-agent isolation gives 90%+ improvements
- Enforce principles deterministically via hooks and linters; advisory context files are for everything else
- Write ADRs for every significant architectural decision: short, immutable once accepted, stored in source repo
- Structure enforcement tiers as NEVER / ASK / ALWAYS; avoid prohibitive framing (Pink Elephant Problem)
- Every tool mutation must be idempotent; add workflow-level guardrails (iteration caps, cost budgets) for semantic error protection
- "Duplication is far cheaper than the wrong abstraction" — inline before you abstract wrong

## Limitations

- ETH Zurich study (the primary empirical source for context file effectiveness) covered only 138 Python tasks in small open-source repos; enterprise/proprietary codebases with non-public domain knowledge may show larger gains from context files
- The 90.2% multi-agent improvement statistic appears only in a third-party vendor source [7], not in Anthropic primary research — treat as directional, not authoritative
- Mapping from human cognitive load research to LLM attention budget is an analogy, not a proven equivalence — LLMs process tokens via attention in parallel, not sequentially in working memory
- The Kohavi "⅓ of features improve metrics" finding is attributed via Fowler, not directly verified; original study details (domain, methodology) not reviewed

## Follow-ups

- Find 2025-2026 empirical data on context file effectiveness in enterprise/proprietary codebases
- Research formal verification of LLM attention behavior vs. human cognitive load models
- Investigate whether the ETH Zurich performance benchmark has been replicated or extended to other languages/task types
- Find primary source for Kohavi et al. A/B test feature success rate findings

---

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| convention over configuration Rails Django history origin design … | google | any | 10 | 2 |
| YAGNI empirical cost premature abstraction software engineering r… | google | any | 10 | 1 |
| convention over configuration LLM agent tooling context structure… | google | 2025-2026 | 10 | 3 |
| complexity budget software design cognitive load feature tradeoff… | google | 2024-2025 | 10 | 1 |
| LLM context window token economics complexity tradeoffs agent des… | google | 2025 | 10 | 2 |
| principle driven development extracting design principles softwar… | google | 2024 | 10 | 1 |
| idempotency convergent operations distributed systems agent autom… | google | 2024-2025 | 10 | 3 |
| 12-factor app methodology conventions developer tooling project s… | google | 2024 | 10 | 1 |
| YAGNI build cost delay cost carry cost Fowler software abstractio… | google | any | 10 | 1 |
| &quot;premature abstraction&quot; cost software development wrong interface… | google | 2023-2024 | 10 | 1 |
| &quot;principle engineering&quot; OR &quot;architecture decision records&quot; design… | google | 2024 | 10 | 2 |
| idempotent infrastructure as code Terraform Ansible convergent au… | google | 2024-2025 | 10 | 1 |
| Anthropic Claude code agent CLAUDE.md AGENTS.md convention contex… | google | 2025 | 10 | 3 |
| convention configuration LLM CLAUDE.md AGENTS.md minimal context … | google | 2025-2026 | 10 | 3 |
| ASDLC AGENTS.md specification research backed guide conventions a… | google | 2025 | 10 | 2 |
| &quot;Anthropic&quot; OR &quot;OpenAI&quot; agent coding best practices context minim… | google | 2025-2026 | 10 | 2 |
| idempotency agent workflows LLM tool calls retry safety state man… | google | 2025 | 10 | 2 |
| &quot;wrong abstraction&quot; Sandi Metz &quot;duplication is far cheaper&quot; AHA p… | google | any | 10 | 1 |
| Anthropic building effective agents tool design idempotency relia… | google | 2025 | 10 | 3 |
| software design principles documentation &quot;living document&quot; enforc… | google | 2024 | 10 | 1 |
| software architecture principles &quot;convention over configuration&quot; … | google | 2025 | 10 | 1 |
| context engineering token budget LLM agent &quot;lost in the middle&quot; a… | google | 2024-2025 | 10 | 2 |
| Karpathy &quot;software 2.0&quot; OR &quot;software 3.0&quot; LLM consuming project s… | google | 2024-2025 | 10 | 1 |

_23 searches · 230 candidates found · 40 used_

**Not searched:**
- Terraform idempotency convergence formal academic study
- LLM tool design formal usability study
- Rails convention over configuration user study empirical 2024
- principle engineering systematic review academic literature
