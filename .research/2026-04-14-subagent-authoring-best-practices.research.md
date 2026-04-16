---
name: "Claude Code Subagent Authoring Best Practices"
description: "Body writing follows identity→scope→constraints→workflow→output-contract; description 'use proactively' is aspirational not reliable; tool restrictions are hard constraints not prompt instructions; invocation prompts must front-load all context; key antipatterns documented with evidence."
type: research
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://github.com/Piebald-AI/claude-code-system-prompts
  - https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
  - https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/
  - https://www.morphllm.com/claude-subagents
  - https://github.com/anthropics/claude-code/issues/10504
  - https://github.com/anthropics/claude-code/issues/5688
  - https://github.com/anthropics/claude-code/issues/13627
  - https://github.com/anthropics/claude-code/issues/4908
  - https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/
  - https://johnsonlee.io/2026/03/02/claude-code-background-subagent.en/
  - https://github.com/vijaythecoder/awesome-claude-agents/blob/main/docs/best-practices.md
  - https://github.com/VoltAgent/awesome-claude-code-subagents
  - https://wmedia.es/en/writing/claude-code-subagents-guide-ai
  - https://claudelab.net/en/articles/claude-code/claude-code-custom-subagents-at-mention-guide
  - https://www.eesel.ai/blog/claude-code-subagents
  - https://docs.langchain.com/oss/python/deepagents/subagents
related:
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/subagent-cross-platform-format-comparison.context.md
  - docs/context/claude-code-subagent-body-structure.context.md
  - docs/context/claude-code-subagent-description-field-authoring.context.md
  - docs/context/claude-code-subagent-tool-selection-strategy.context.md
  - docs/context/claude-code-subagent-invocation-prompt-design.context.md
  - docs/context/claude-code-subagent-authoring-antipatterns.context.md
---

# Claude Code Subagent Authoring Best Practices


## Summary

Claude Code subagent authoring quality rests on five distinct decisions, each with different evidence strength. Body writing is well-supported: Anthropic's own built-in agents (Explore, Plan, general-purpose) follow a consistent structure of identity → scope → constraint block → numbered workflow → output contract, and the agent-creation-architect internal prompt confirms the design intent. Single-responsibility with explicit behavioral constraints is the principle; "comprehensive" (domain instructions) and "concise" (no project context in the body) are reconcilable, not contradictory.

Description field authoring has a critical caveat that official docs understate: "use proactively" phrasing is aspirational design, not reliable behavior. GitHub Issue #5688 (closed NOT_PLANNED) confirms the primary agent frequently ignores proactive directives entirely. The only reliable trigger is explicit invocation by name. The ~140-character length heuristic is practitioner-derived with no T1 backing; the real rule is to keep routing signals separate from behavioral instructions.

Tool selection is the clearest area: inherit-all is the dangerous default; restrict via `tools` allowlist or `disallowedTools` denylist; tool restrictions are hard constraints while body instructions are not. Three tiers cover most cases: read-only (`Read, Grep, Glob`), research (+ `WebFetch, WebSearch`), implementation (full set). Use `PreToolUse` hooks when you need conditional gating within a single tool.

Invocation prompt design is anchored by Anthropic's own internal guidance (extracted from Piebald-AI v2.1.94 — treat as directionally sound, potentially version-specific): brief like a smart colleague with zero context, front-load everything needed, never delegate understanding ("based on your findings, fix it" pushes synthesis to the agent), and scope the return format to avoid flooding the parent's context.

Key antipatterns: over-grant by omission, mixing routing signals with behavioral instructions in `description`, building workflows that assume auto-delegation, spawning parallel subagents on shared files without `isolation: worktree`, and the super-agent antipattern (one agent for everything) — balanced against the counter-antipattern of agent flooding (too many specialists fragmenting routing).

Documented gaps with no current guidance: `maxTurns` calibration, testing/validating that a subagent body was actually injected, `skills` preloading strategy, and `isolation: worktree` usage patterns for parallel-write scenarios.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://code.claude.com/docs/en/sub-agents | Create custom subagents | Anthropic | 2026 | T1 | verified |
| 2 | https://claude.com/blog/subagents-in-claude-code | How and when to use subagents in Claude Code | Anthropic | 2026 | T1 | verified |
| 3 | https://github.com/Piebald-AI/claude-code-system-prompts | claude-code-system-prompts (extracted prompts: writing-subagent-prompts, subagent-delegation-examples, subagent-prompt-writing-examples, agent-creation-architect, Explore, Plan, general-purpose) | Piebald-AI (community reverse-engineering) | Apr 2026 (v2.1.94) | T2 | verified |
| 4 | https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/ | Best practices for Claude Code subagents (Part I) | PubNub | 2026 | T2 | verified |
| 5 | https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/ | Best Practices with Claude Code Subagents Part II: Moving from Prompts to Pipelines | PubNub | 2026 | T2 | verified |
| 6 | https://www.morphllm.com/claude-subagents | Claude Code Subagents: How They Work, What They See & When to Use Them | MorphLLM | 2026 | T2 | verified |
| 7 | https://github.com/anthropics/claude-code/issues/10504 | [FEATURE] Subagent YAML frontmatter description field has UX and design issues | anthropics/claude-code GitHub Issues | 2025–2026 | T2 | verified |
| 8 | https://github.com/anthropics/claude-code/issues/5688 | Subagent Selection Failure: Primary Agent Ignores Proactive Directive | anthropics/claude-code GitHub Issues | 2025 | T2 | verified |
| 9 | https://github.com/anthropics/claude-code/issues/13627 | Bug: Custom agent body content not injected when spawned via Task tool | anthropics/claude-code GitHub Issues | 2025–2026 | T2 | verified |
| 10 | https://github.com/anthropics/claude-code/issues/4908 | Feature Request: Scoped Context Passing for Subagents | anthropics/claude-code GitHub Issues | 2025 | T2 | verified |
| 11 | https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/ | Claude Code Agents & Subagents: What They Actually Unlock | ksred.com (practitioner) | 2026 | T2 | verified |
| 12 | https://johnsonlee.io/2026/03/02/claude-code-background-subagent.en/ | Are You Using Claude Subagents Right? | Johnson Lee (practitioner) | Mar 2026 | T2 | verified |
| 13 | https://github.com/vijaythecoder/awesome-claude-agents/blob/main/docs/best-practices.md | awesome-claude-agents: best-practices.md | vijaythecoder (community) | 2026 | T3 | verified |
| 14 | https://github.com/VoltAgent/awesome-claude-code-subagents | awesome-claude-code-subagents (100+ subagent collection) | VoltAgent (community) | 2026 | T3 | verified |
| 15 | https://wmedia.es/en/writing/claude-code-subagents-guide-ai | Claude Code Subagents: Practical Guide with Real Agent Configs | wmedia.es (practitioner) | 2026 | T3 | verified |
| 16 | https://claudelab.net/en/articles/claude-code/claude-code-custom-subagents-at-mention-guide | Claude Code Custom Subagents: Complete Guide to @ Mention | Claude Lab | 2026 | T3 | verified |
| 17 | https://www.eesel.ai/blog/claude-code-subagents | 7 powerful Claude Code subagents you can build in 2025 | eesel AI | 2025 | T3 | verified |
| 18 | https://claudelog.com/mechanics/custom-agents/ | ClaudeLog — Custom Agents | ClaudeLog | 2026 | T3 | verified (403) |

## Extracts

### Sub-question 1: Effective system prompt body writing

**What principles and patterns make an effective subagent system prompt body? Structure, length, scope statements, behavioral constraint phrasing, generalist vs. specialist calibration.**

---

**[S1 — T1] Official docs: body becomes the full system prompt, receives minimal base context**

> "The body becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt." [1]

**[S1 — T1] Official best practices tip: focused single-task design**

> "Design focused subagents: each subagent should excel at one specific task" [1]

> "Write detailed descriptions: Claude uses the description to decide when to delegate" [1]

**[S1 — T1] Official built-in: Explore prompt structure** (verbatim extract from [3])

The Explore subagent body opens with:
- Identity line: "You are a file search specialist for Claude Code..."
- Capabilities summary: bullet list of strengths
- Constraint block (capitalized section header): "=== CRITICAL: READ-ONLY MODE — NO FILE MODIFICATIONS ===" with explicit enumeration of prohibited operations
- Behavioral guidelines: specific tool-use rules
- Performance directive: "NOTE: You are meant to be a fast agent that returns output as quickly as possible."
- Termination format: "Complete the user's search request efficiently and report your findings clearly."

**[S1 — T1] Official built-in: Plan prompt structure** (verbatim extract from [3])

The Plan subagent body follows a numbered workflow pattern:
1. "Understand Requirements" — "Focus on the requirements provided and apply your assigned perspective"
2. "Explore Thoroughly" — explicit tool-use rules per step
3. "Design Solution" — "Create implementation approach based on your assigned perspective"
4. "Detail the Plan" — "Provide step-by-step implementation strategy"

Required output section is explicit: "End your response with: ### Critical Files for Implementation / List 3-5 files..."

**[S1 — T1] Official built-in: general-purpose prompt structure** (verbatim extract from [3])

Opens with task-completion framing: "Complete the task fully — don't gold-plate, but don't leave it half-done. When you complete the task, respond with a concise report covering what was done and any key findings — the caller will relay this to the user, so it only needs the essentials."

Followed by: a named strengths list, guidelines, and explicit prohibitions ("NEVER create files unless absolutely necessary").

**[S1 — T2] Anthropic's own agent-creation architect prompt: how Anthropic thinks about bodies** (verbatim extract from [3])

The `agent-prompt-agent-creation-architect.md` (internal system prompt for generating new subagents) instructs:
1. "Extract Core Intent: Identify the fundamental purpose, key responsibilities, and success criteria"
2. "Design Expert Persona: Create a compelling expert identity that embodies deep domain knowledge"
3. "Architect Comprehensive Instructions: Develop a system prompt that:
   - Establishes clear behavioral boundaries and operational parameters
   - Provides specific methodologies and best practices for task execution
   - Anticipates edge cases and provides guidance for handling them
   - Defines output format expectations when relevant"
4. "Optimize for Performance: Include decision-making frameworks, quality control mechanisms and self-verification steps, efficient workflow patterns, clear escalation or fallback strategies"

**Key principle from [3]**: "Be specific rather than generic — avoid vague instructions. Include concrete examples when they would clarify behavior. Balance comprehensiveness with clarity — every instruction should add value."

**[S1 — T2] PubNub Part I: single-responsibility with explicit input/output contracts**

> "Give each subagent one clear goal, input, output, and handoff rule." [4]

Example structure: role definition, explicit output targets (file paths to write), and a stopping condition. The PM agent must "ask concise, numbered questions and WAIT for human answers" if criteria remain unclear. [4]

**[S1 — T2] PubNub Part II: concise and constraint-focused, not onboarding novels**

> "You are a senior engineer. Implement the plan and keep scope inside the ADR guardrails." [5]

The guidance: "keep prompts concise and constraint-focused. Avoid treating system prompts as onboarding novels. Instead, delegate detailed context to routable documents (plans, decision logs)." [5]

**[S1 — T2] awesome-claude-agents best-practices: micro-specification framework**

Body should follow:
- "Mission / Role — one sentence that nails the outcome"
- "Workflow — numbered steps Claude should always follow"
- "Output Contract — exact Markdown or JSON Claude must return"
- "Heuristics & Checks — bullet list of edge-cases, validations, scoring rubrics"

**Key principle:** "Keep it short but explicit; the prompt is re-parsed every invocation." Use active voice, imperative verbs; limit markdown headings to `###` or smaller. [13]

**[S1 — T2] claudelab: specialist-domain subagent structure**

The `dexie-specialist` example shows bodies should include:
- "Expertise declaration: 'You are an expert [Domain] specialist with deep knowledge of...'"
- "Critical first step: 'Before answering ANY question...you MUST: 1. Fetch... 2. Based on the task... 3. Only then proceed'"
- "Coverage areas: List specific domains"
- "Response format: Specify structure (cite documentation, explain approach, provide code, include error handling)"
- "Quality assurance section: Define verification standards" [16]

**[S1 — T3] eesel.ai: quality of system prompt determines quality of output**

> "The quality of your subagent's work depends entirely on the quality of its system prompt. Don't be vague." [17]

Effective prompts should be "a detailed instruction manual" including step-by-step processes, explicit rules, and examples of correct and incorrect approaches. The specialist-over-generalist principle: "The best subagents are specialists, not generalists...A dedicated `code-reviewer` will always do a better job." [17]

**Confidence: HIGH** — T1 official docs plus convergent T2 practitioner sources with working examples. All agree on: (1) focused single-task scope, (2) explicit behavioral constraints, (3) numbered workflow + output contract, (4) role identity opening.

---

### Sub-question 2: Description field authoring for routing effectiveness

**What makes a description field routing-effective vs. routing-invisible? Length, phrasing, trigger phrases, examples. What have practitioners found works vs. fails?**

---

**[S2 — T1] Official docs: description drives delegation**

> "Claude uses each subagent's description to decide when to delegate tasks. When you create a subagent, write a clear description so Claude knows when to use it." [1]

> "Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like 'use proactively' in your subagent's description field." [1]

The `description` field is officially documented as: "When Claude should delegate to this subagent" [1]

**[S2 — T1] Official examples of description content** (from official example subagents in [1])

- code-reviewer: `"Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."`
- debugger: `"Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues."`
- data-scientist: `"Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries."`

Pattern: `[Role] + [domain/specialty] + ["Use proactively"] + [trigger condition]`

**[S2 — T2] GitHub Issue #10504: description field has documented design problems**

Problems identified by practitioners:
1. Escaped newlines (`\n`) in YAML make descriptions hard to read; YAML literal block syntax (`|`) works but is undocumented
2. Descriptions violate the documented 1024-character limit without warnings (examples at 1297 and 1308 chars found)
3. Redundancy: descriptions duplicate content from the Markdown system prompt instead of serving as concise routing hints

**Recommended format from issue** (brief routing hint, ~140 chars):
```yaml
description: Expert Python code reviewer for FastAPI, async patterns, and backend features. Use after implementing or refactoring Python services.
```

**Bad pattern from issue** (over-length with examples):
```yaml
description: "Use this agent when...\\n\\nContext: User has...\\n<example>...</example>"
```

Issue closed as "not planned." [7]

**[S2 — T2] GitHub Issue #5688: proactive directive ignored**

A user created a subagent with description containing "You MUST use this agent PROACTIVELY whenever you want to run tests" (all-caps directive, extensive examples). The primary agent ignored it entirely. Users must explicitly invoke.

Root cause: "proactive subagent invocation based on description directives is not functioning." Workaround: explicit invocation by name. Issue closed as "not planned." [8]

**[S2 — T2] awesome-claude-agents best-practices: description targets the router, not the agent**

> "Never mix behavioural instructions meant for the agent into the `description` block." The description targets Claude's router; the prompt body targets the specialist agent. [13]

Mandatory language patterns:
- Include "MUST BE USED" or "use PROACTIVELY" phrases
- Embed action verbs: "review · analyze · optimize"
- State both **when** and **why** the agent should run [13]

**[S2 — T2] Johnson Lee: PROACTIVELY required for scheduling logic**

> "The worker agent's description needs to include 'PROACTIVELY.' Claude Code's scheduling logic reads this field to decide whether to proactively delegate. Without that word, the agent is 'available' but not 'proactive'." [12]

**[S2 — T2] ksred.com: auto-selection is unreliable**

> "Auto-selection of custom agents remains unreliable. Claude frequently handles tasks in the main session rather than delegating to a defined agent, which defeats the purpose of automatic routing. The only reliable trigger is explicit invocation." [11]

**[S2 — T3] claudelab: trigger-based language**

> "Use this agent when the task involves [Domain]...in any way" — include concrete scenarios, add versioning context where relevant. [16]

**[S2 — T3] wmedia.es: practitioner experience — explicit invocation often required**

> "The realistic thing is for you to invoke them explicitly, with clear instructions. If not, many times they stay gathering dust." Description should use "MUST BE USED when debugging errors" style language, though even this is no guarantee. [15]

**Contradiction noted:** T1 official docs and T2 practitioner posts both recommend "use proactively" language, but GitHub issues (T2) show this directive is frequently ignored by the model. The phrase signals intent but does not guarantee routing behavior. Explicit invocation is the only reliable path.

**Confidence: HIGH** on format patterns (T1 + convergent T2). MODERATE on reliability of auto-routing (T2 practitioner reports contradict T1 framing).

---

### Sub-question 3: Tool selection strategy

**Right strategy for granting tools. Risks from over-granting vs. under-granting. Least privilege. Documented cases of unexpected behavior from tool misconfiguration.**

---

**[S3 — T1] Official docs: tool inheritance default and override patterns**

> "By default, subagents inherit all tools from the main conversation, including MCP tools." [1]

> "To restrict tools, use either the `tools` field (allowlist) or the `disallowedTools` field (denylist)." [1]

> "If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed." [1]

Official quickstart explicitly states: "For a read-only reviewer, deselect everything except Read-only tools. If you keep all tools selected, the subagent inherits all tools available to the main conversation." [1]

**[S3 — T1] Official best practice tip**

> "Limit tool access: grant only necessary permissions for security and focus" [1]

**[S3 — T1] Official built-in tool assignments** (from [1] and [3])

- Explore subagent: `disallowedTools: R4, ExitPlanMode, Edit, Write, NotebookEdit` (read-only pattern)
- Plan subagent: same as Explore (read-only)
- general-purpose subagent: `tools: *` (inherits all)
- Official code-reviewer example: `tools: Read, Grep, Glob, Bash`
- Official debugger example: `tools: Read, Edit, Bash, Grep, Glob`
- Official data-scientist example: `tools: Bash, Read, Write`

**[S3 — T2] PubNub Part I: scope tools by agent role**

> "If you omit `tools`, the subagent inherits the thread's tools (including MCP). Whitelist when you need tight control." [4]

Guidance pattern:
- PM & Architect: Read-heavy (search, docs via MCP)
- Implementer: Edit, Write, Bash, plus UI testing
- Release: only what it needs [4]

**[S3 — T2] ksred.com: tool restrictions are hard constraints, not soft prompting**

> "A reviewer defined with only `Read, Grep, Glob` cannot write files. That's not a naming convention or a prompt instruction, it's a hard constraint." [11]

**[S3 — T2] awesome-claude-code-subagents collection: three-tier tool taxonomy**

Codified in the collection README:
- Read-only (reviewers/auditors): `Read, Grep, Glob`
- Research: add `WebFetch, WebSearch`
- Implementation: full `Read, Write, Edit, Bash, Glob, Grep` [14]

**[S3 — T2] awesome-claude-agents best-practices: tool granting scenarios**

| Scenario | Recommendation |
|----------|----------------|
| Broad prototyping | Omit `tools` field (inherit all) |
| Security-sensitive | Enumerate minimal set (e.g., `Read, Grep`) |
| Dangerous commands | Grant only to "trusted, well-scoped agents" |

> "Explicit descriptions generally out-perform code examples for guiding tool use." [13]

**[S3 — T2] Official docs: hooks as conditional tool gating**

The `PreToolUse` hook pattern enables fine-grained control beyond the `tools` field — e.g., allowing `Bash` generally but validating SQL to permit only SELECT queries. This is the recommended approach when "you need to allow some operations of a tool while blocking others." [1]

**[S3 — T2] PubNub: "prompt-only constraints are fragile"** (referenced in search results, confirmed convergent)

> "Natural language prompts can be ignored, misinterpreted, or overridden by the model. Tool restrictions and hooks are deterministic enforcement mechanisms." If you write "do not modify files" in the body without restricting tools, the constraint can be violated. [4]

**[S3 — T2] claudelab: allowed-tools restricts to read + fetch only**

The `dexie-specialist` example uses `allowed-tools: "Read, Grep, Glob, WebFetch"` — enabling documentation fetching without unnecessary write access. [16]

**Confidence: HIGH** — T1 official docs plus strong T2 practitioner convergence. All sources agree on the allowlist/denylist mechanism and the principle of least privilege. The hard-constraint framing (tools vs. prompt instruction) is distinctly stated by multiple T2 sources.

---

### Sub-question 4: Parent prompt / invocation prompt design

**How should a parent agent structure the invocation prompt — the sole context channel? What context must be embedded? What should be omitted? How to scope the ask?**

---

**[S4 — T1/T2] Anthropic's internal prompt-writing guidance** (verbatim from `system-prompt-writing-subagent-prompts.md`, [3])

This is Anthropic's actual system prompt injected when Claude writes a subagent invocation:

> "When spawning a fresh agent (with a `subagent_type`), it starts with zero context. Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters."
>
> - Explain what you're trying to accomplish and why.
> - Describe what you've already learned or ruled out.
> - Give enough context about the surrounding problem that the agent can make judgment calls rather than just following a narrow instruction.
> - If you need a short response, say so ("report in under 200 words").
> - Lookups: hand over the exact command. Investigations: hand over the question — prescribed steps become dead weight when the premise is wrong.
>
> "For fresh agents, terse command-style prompts produce shallow, generic work."
>
> **Never delegate understanding.** Don't write "based on your findings, fix the bug" or "based on the research, implement it." Those phrases push synthesis onto the agent instead of doing it yourself. Write prompts that prove you understood: include file paths, line numbers, what specifically to change.

**[S4 — T1/T2] Official delegation examples** (verbatim from `system-prompt-subagent-delegation-examples.md`, [3])

Example of a well-formed invocation prompt:

```
Agent({
  name: "ship-audit",
  description: "Branch ship-readiness audit",
  prompt: "Audit what's left before this branch can ship. Check: uncommitted changes,
           commits ahead of main, whether tests exist, whether the GrowthBook gate is
           wired up, whether CI-relevant files changed. Report a punch list — done vs.
           missing. Under 200 words."
})
```

Example of a migration review with context embedding:
```
Agent({
  name: "migration-review",
  description: "Independent migration review",
  subagent_type: "code-reviewer",
  prompt: "Review migration 0042_user_schema.sql for safety. Context: we're adding a
           NOT NULL column to a 50M-row table. Existing rows get a backfill default.
           I want a second opinion on whether the backfill approach is safe under
           concurrent writes — I've checked locking behavior but want independent
           verification. Report: is this safe, and if not, what specifically breaks?"
})
```

**[S4 — T2] MorphLLM: prompt is the only bridge**

> "If a subagent needs file paths, error messages, architectural decisions, or output from a previous subagent, the parent must include it in the Agent tool prompt. There is no other way to pass context." [6]

> "Front-load everything the subagent needs to start working immediately." [6]

**[S4 — T1] Official blog: scoping the ask**

> "Scope tasks clearly. 'Explore how payments work' beats 'explore everything.' Request parallelization explicitly. Say 'these can run in parallel' or 'work on all three simultaneously.' Specify what should be returned." [2]

Example of a well-scoped parallel research prompt from [2]:
> "Use subagents to explore this codebase in parallel: 1. Find all API endpoints... 2. Identify the database schema... 3. Map out the authentication flow... Return a summary of each, not the full file contents."

**[S4 — T2] GitHub Issue #4908: context re-discovery is a real cost**

Users documented: "Subagents re-discover information already available to the parent (e.g., analyzing git diffs, reading files) — Increased Latency & Token Cost." The current design forces this inefficiency because there is no declarative context inheritance. Proposed workaround: "pass context directly in invocation prompts." [10]

**[S4 — T2] PubNub Part I: hook-generated suggestion forces human glance**

> "Hooks suggest, humans approve: the hook prints 'Use the architect-review subagent on use-case-presets.' A human pastes it to proceed." [4]

This pattern prevents runaway chains while preserving velocity — structured invocation prompts as hook output, not ad-hoc composition.

**[S4 — T2] Johnson Lee: background subagents demand crystal-clear prompts**

> "Prompts must be crystal clear — vague instructions plus zero interaction equals disaster." Since background subagents execute immediately without intermediate clarification, every detail must be front-loaded. [12]

**[S4 — T2] Claude blog: what to return matters**

> "Specify what should be returned." The invocation prompt should constrain output length and format to avoid flooding the parent's context with verbose results. [2]

**Confidence: HIGH** — Anchored in Anthropic's verbatim internal system prompt (T2 extraction from official build) plus convergent T1 blog and T2 practitioner guidance.

---

### Sub-question 5: Authoring antipatterns

**Most common authoring mistakes. Failure modes practitioners have documented.**

---

**[S5 — T1] Official docs: common tool antipattern**

> "If you keep all tools selected, the subagent inherits all tools available to the main conversation." — Omitting the `tools` field is the default path to tool over-grant. [1]

**[S5 — T2] GitHub Issue #13627: body content silently dropped (version-specific bug)**

In Claude Code v2.0.58, "the body content is completely ignored" when a custom agent is spawned via the Task tool. Only YAML frontmatter was used. Subagent definitions appeared to work (metadata recognized), but behavioral instructions had no effect. All workarounds defeated the purpose of the system. Issue closed as "not planned." [9]

**Implication:** Authors testing subagents in a version with this bug would conclude their body was working when it was not. This creates authoring confusion at the version boundary.

**[S5 — T2] GitHub Issue #5688: proactive directive failure**

All-caps "MUST USE PROACTIVELY" directives in descriptions are ignored by the primary agent. Auto-delegation is not a reliable architectural assumption. Issue closed as "not planned." [8]

**[S5 — T2] GitHub Issue #10504: over-length descriptions as antipattern**

Descriptions exceeding ~140 characters start embedding behavioral instructions that belong in the body. Claude-generated agents were producing 1297–1308 character descriptions with embedded examples — confusing the routing signal with agent instructions. [7]

**[S5 — T2] GitHub Issue #4908: prompt-starvation antipattern**

Delegating without embedding context: writing "based on your findings, fix the bug" without providing the findings. Subagent must re-discover context at token cost and latency. [10]

**[S5 — T1] Official Anthropic prompt guidance: "never delegate understanding"**

> "Don't write 'based on your findings, fix the bug' or 'based on the research, implement it.' Those phrases push synthesis onto the agent instead of doing it yourself." [3]

**[S5 — T2] PubNub: "context rot" — noisy output in main thread**

> "Context becomes a landfill when noisy output accumulates in the main thread." Using subagents correctly avoids this; but delegating without subagent isolation (or running verbose tasks inline) defeats the architecture. [5]

**[S5 — T2] PubNub: "prompt glue" antipattern**

> "Repeating context and copy-pasting similar prompts across agents." The fix: define reusable Skills for shared context, not copy-pasted system prompts. [5]

**[S5 — T2] ksred.com: over-delegation antipattern**

> "Don't spawn agents because you can." Narrow scoping matters — subagents add coordination overhead, and "Opus will delegate to agents in situations where a direct approach would be faster and cheaper." [11]

**[S5 — T3] eesel.ai: "super-agent" antipattern**

> "The biggest antipattern is building one 'super-agent' that tries to do everything rather than focused specialists performing single jobs well." [17]

**[S5 — T1] Official blog: parallel subagents on coupled tasks**

> "Two subagents editing the same file in parallel is a recipe for conflict." [2]

> "It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable." [2]

**[S5 — T2] awesome-claude-agents: mixed instructions antipattern**

> "Embedding agent behavioral logic in the `description` field confuses the router." Keep routing signals in `description`, behavioral instructions in the body. [13]

**[S5 — T3] wmedia.es: hallucination risk underestimated**

> "They also hallucinate, over-analyze, add unnecessary complexity." Subagents executing autonomously without stop-and-verify steps amplify hallucination risk compared to interactive sessions. [15]

**[S5 — T3] wmedia.es: token overconsumption from unchained chaining**

> "Do not abuse chaining without a clear strategy, as they still devour tokens." [15]

**Confidence: HIGH** for antipatterns supported by multiple convergent T2 sources. The body-not-injected bug (#13627) is HIGH confidence for that specific version but may be resolved in later versions — note the caveat.

## Search Protocol

| # | Query | Source | Date | Results |
|---|-------|--------|------|---------|
| 1 | Claude Code subagents best practices authoring system prompt 2025 2026 | WebSearch | 2026-04-14 | 10 results; identified key URLs including official docs, PubNub posts, Medium guides |
| 2 | Claude Code custom agents description field routing effective | WebSearch | 2026-04-14 | 10 results; confirmed description field routing behavior, found claudelab and ksred.com sources |
| 3 | Claude Code subagent tool selection least privilege antipatterns | WebSearch | 2026-04-14 | 10 results; found GitHub issues #20264, #24316, awesome-claude-code-subagents |
| 4 | https://code.claude.com/docs/en/sub-agents | WebFetch | 2026-04-14 | Full official docs — frontmatter fields, tool control, permission modes, hooks, examples, best practices |
| 5 | https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/ | WebFetch | 2026-04-14 | Single-responsibility design, tool tier pattern, invocation hook pattern, antipatterns table |
| 6 | https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/ | WebFetch | 2026-04-14 | Forked context pattern, Skills as reuse unit, context rot / prompt glue antipatterns |
| 7 | https://claudefa.st/blog/guide/agents/sub-agent-best-practices | WebFetch | 2026-04-14 | 522 error — unreachable |
| 8 | https://claudelab.net/en/articles/claude-code/claude-code-custom-subagents-at-mention-guide | WebFetch | 2026-04-14 | Role-based structure, coverage areas, response format, antipatterns (context bleed, over-delegating) |
| 9 | https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/ | WebFetch | 2026-04-14 | Specialist over generalist, description routing, tool restriction |
| 10 | site:github.com/anthropics/claude-code subagent description authoring issues | WebSearch | 2026-04-14 | Found issues #10504, #5688, #13627, #4908, #19077 |
| 11 | https://github.com/anthropics/claude-code/issues/10504 | WebFetch | 2026-04-14 | Description field character limit violations, bad vs. good description examples, proposed solutions |
| 12 | https://github.com/anthropics/claude-code/issues/5688 | WebFetch | 2026-04-14 | Proactive directive ignored by primary agent, auto-delegation unreliable |
| 13 | https://github.com/anthropics/claude-code/issues/13627 | WebFetch | 2026-04-14 | Body content dropped when spawned via Task tool (v2.0.58 bug) |
| 14 | https://github.com/VoltAgent/awesome-claude-code-subagents | WebFetch | 2026-04-14 | Three-tier tool taxonomy, role-based naming patterns, description activation trigger language |
| 15 | https://medium.com/@richardhightower/claude-code-subagents-... | WebFetch | 2026-04-14 | 302 → 307 redirect chain to auth wall — skipped |
| 16 | https://www.eesel.ai/blog/claude-code-subagents | WebFetch | 2026-04-14 | System prompt quality principle, specialist-over-generalist, least privilege |
| 17 | https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/ | WebFetch | 2026-04-14 | Auto-selection unreliable, hard constraint framing, over-delegation warning |
| 18 | Claude Code subagent "invocation prompt" parent agent context passing delegation pattern | WebSearch | 2026-04-14 | Found morphllm.com source, confirmed official blog URL, found #4908 |
| 19 | https://www.morphllm.com/claude-subagents | WebFetch (×2) | 2026-04-14 | Prompt is only bridge, front-load context, task independence error, coordination limits |
| 20 | https://claude.com/blog/subagents-in-claude-code | WebFetch | 2026-04-14 | Trigger-based description language, scoped task articulation, parallel conflict antipattern, too-many-agents antipattern |
| 21 | https://github.com/anthropics/claude-code/issues/4908 | WebFetch | 2026-04-14 | Scoped context passing — re-discovery cost, explicit prompt as only channel |
| 22 | Claude Code subagent description "use proactively" routing trigger phrase effective pattern | WebSearch | 2026-04-14 | Confirmed "use proactively" pattern from docs and practitioners, found johnsonlee.io |
| 23 | https://johnsonlee.io/2026/03/02/claude-code-background-subagent.en/ | WebFetch | 2026-04-14 | PROACTIVELY keyword in scheduling logic, crystal-clear prompts for background agents, file boundary management |
| 24 | https://github.com/vijaythecoder/awesome-claude-agents/blob/main/docs/best-practices.md | WebFetch | 2026-04-14 | Micro-specification framework, description as router cue vs. agent instruction, tool scenarios table |
| 25 | https://wmedia.es/en/writing/claude-code-subagents-guide-ai | WebFetch | 2026-04-14 | Detailed role-based prompts, output structure, explicit invocation required, hallucination risk, token overconsumption |
| 26 | gh api repos/Piebald-AI/claude-code-system-prompts/contents/system-prompts/ | gh CLI | 2026-04-14 | Identified system-prompt-writing-subagent-prompts.md, system-prompt-subagent-delegation-examples.md, system-prompt-subagent-prompt-writing-examples.md, agent-prompt-agent-creation-architect.md, agent-prompt-explore.md, agent-prompt-plan-mode-enhanced.md, agent-prompt-general-purpose.md |
| 27 | system-prompt-writing-subagent-prompts.md | gh CLI fetch | 2026-04-14 | Anthropic's internal invocation prompt-writing guidance: "brief like a smart colleague," never delegate understanding, terse prompts produce shallow work |
| 28 | system-prompt-subagent-delegation-examples.md | gh CLI fetch | 2026-04-14 | Verbatim examples: ship-audit and migration-review delegation prompts with commentary |
| 29 | agent-prompt-agent-creation-architect.md | gh CLI fetch | 2026-04-14 | Anthropic's internal framework for authoring subagent bodies: expert persona, behavioral boundaries, decision frameworks, output format, identifier design |
| 30 | agent-prompt-explore.md, agent-prompt-plan-mode-enhanced.md, agent-prompt-general-purpose.md | gh CLI fetch | 2026-04-14 | Built-in subagent body structures from Anthropic: constraint blocks, numbered workflows, output contracts, performance directives |

## Challenge

### Contradictions and Source Reliability Issues

**"Use proactively" works (T1) vs. is ignored (T2 GitHub issues)**

The official docs (S2, T1) state: "To encourage proactive delegation, include phrases like 'use proactively' in your subagent's description field." GitHub Issue #5688 (T2) directly contradicts this: a user with "You MUST use this agent PROACTIVELY" in all-caps saw the primary agent ignore it entirely. Both issues #5688 and the workaround consensus from practitioners (ksred.com, wmedia.es, Johnson Lee) confirm that auto-delegation is unreliable even with correct phrasing.

Verdict: the official docs describe the intended design; the GitHub issues describe observed behavior. These are not reconcilable — the feature is documented but unreliable. The T1 claim is aspirational framing, not an empirical guarantee. The T2 GitHub issue is the stronger evidence for what actually happens in practice. Both should be cited, and the extracts already note this contradiction — but the confidence rating ("HIGH on format patterns, MODERATE on reliability") underweights the gap. The routing mechanism is a soft preference signal, not a hard rule, and Issue #5688 was closed "not planned," meaning Anthropic acknowledged the gap and chose not to fix it.

**Piebald-AI source reliability**

The research classifies Piebald-AI extracts as T2 with "verified" status. Several caveats are not surfaced:

1. The extraction is from the compiled JavaScript bundle of the Claude Code npm package, not from Anthropic's source repository or public API. The methodology is reverse-engineering, not official disclosure.
2. The repository's own `CLAUDE.md` notes that "template variables like `${BASH_TOOL_NAME}` are interpolated at runtime" — the extracted files contain literal placeholder strings, not the exact prompts the model receives. Downstream readers may treat quoted text as verbatim when it is not.
3. Piebald-AI has no stated affiliation with Anthropic. The 8,709+ GitHub stars (as of April 2026) indicate community acceptance, but community acceptance is not the same as accuracy.
4. Prompts are version-tagged (v2.1.94 used for this research), and prompts can change with every release. The "agent-creation-architect" guidance and the "smart colleague" invocation guidance should be treated as "accurate for that version, potentially outdated" — not as stable Anthropic doctrine.

Revised classification: T2-extraction is appropriate but should be qualified as "community reverse-engineering — verbatim text accurate as of version cited, not guaranteed stable, template variables not interpolated." The confidence assertions built on these extracts (particularly S4's "anchored in Anthropic's verbatim internal system prompt") should be softened to reflect that the prompts are real but may shift across versions.

**"Body is the full system prompt" vs. Issue #13627 silent body drop**

The T1 official docs confirm: "The body becomes the system prompt that guides the subagent's behavior." Issue #13627 (December 2025, v2.0.58) documented a bug where the body was silently dropped when spawning via the Task tool (now renamed Agent tool). The issue was closed "not planned," and no changelog entry explicitly marks it resolved.

This is unresolved ambiguity. "Closed not planned" on a bug report means Anthropic chose not to fix it as described, not that it was fixed. The current official docs (April 2026) do confirm the body becomes the system prompt in present tense, which is either (a) a post-fix state where the claim is now accurate, or (b) aspirational documentation that predated or coexisted with the bug. The docs were retrieved as live on April 14, 2026, making (a) the more likely interpretation — but there is no explicit confirmation that the specific v2.0.58 regression was resolved. Authors should test body injection in their current version rather than assuming either the bug is gone or the docs are wrong.

---

### Challenged Recommendations

**"Keep descriptions to ~140 chars"**

This recommendation originates from GitHub Issue #10504 (T2, practitioner-reported). There is no T1 documentation supporting a 140-character guideline. The official docs do not state a character limit or recommend a target length. The 1024-character limit mentioned in Issue #10504 is itself practitioner-observed (descriptions were found at 1297–1308 chars without warnings), not confirmed as a hard system limit in official documentation.

The ~140-character heuristic is a reasonable practitioner inference — descriptions at that length are concise enough to serve as routing signals without bleeding into agent-instruction territory. But it should be marked as community-derived guidance rather than T1 evidence. There is no empirical study comparing routing effectiveness at 80 chars vs. 140 chars vs. 300 chars. The real constraint is functional: descriptions that embed behavioral instructions (examples, conditions) confuse the routing signal. Length is a proxy for that failure mode, not the root cause.

**"Be concise, not onboarding novels" vs. "comprehensive instructions"**

PubNub Part II (S1, T2) advises keeping prompts "concise and constraint-focused," avoiding "onboarding novels." The Piebald-AI agent-creation-architect prompt (S1, T2 extraction) instructs authors to "Architect Comprehensive Instructions" covering behavioral boundaries, methodologies, edge cases, and output formats. These appear in tension but are reconcilable:

The PubNub guidance addresses a specific antipattern — repeating project context (plans, decision logs) in the system prompt body rather than routing to external documents. The agent-creation-architect guidance addresses what to include when writing the domain-specific instructions themselves.

"Comprehensive" and "concise" operate on different scopes: comprehensive domain instructions within the agent's specialty vs. concise invocation context that shouldn't be embedded in the body at all. The apparent contradiction dissolves when framed as: write comprehensive instructions about what the agent does, but do not embed project-specific context that belongs in the invocation prompt. Neither source provides empirical evidence for a threshold (e.g., optimal body word count). The current official docs' code-reviewer example body is ~150 words — structured but not verbose — suggesting brevity is preferred in practice.

**"Brief like a smart colleague who just walked into the room" — first-party or community extraction?**

This phrasing originates from `system-prompt-writing-subagent-prompts.md` in the Piebald-AI repository. It is not Anthropic's published guidance — it is extracted from Claude Code's compiled JavaScript at a specific version. The research classifies this as T1/T2 (citing both the official docs and the extraction), but the dual-tier label is misleading. The extraction is T2: it reflects Anthropic's internal implementation, not a publicly stated policy. Anthropic has not endorsed the Piebald-AI extraction or confirmed the extracted text as its intended guidance.

Practical weight: the "smart colleague" framing is actionable and consistent with Anthropic's broader published guidance on context-setting for agentic tasks (e.g., the official blog's "scope tasks clearly" advice). It should be cited as observed internal guidance — valuable, directionally sound, but potentially version-specific and not formally endorsed.

**"Specialist over generalist" — empirical validation**

Every source in the extracts endorses specialist-over-generalist, but all are practitioner opinion, community convention, or Anthropic design intent — not empirical benchmark comparisons. The 2026 AI agent benchmarking landscape confirms the specialist trend is real (industry shift toward model fleets with specialist roles), but also notes that "generalist LLMs excel at breadth, ambiguity, language, and creative synthesis" and remain the preferred escalation path when tasks are open-ended.

For Claude Code subagents specifically: the "super-agent antipattern" (eesel.ai) and the official blog's "too many specialist agents...flooding Claude with options" antipattern are both real. These are in tension: too general means poor performance on specialized tasks; too specialized means routing fragmentation. The current docs themselves acknowledge this with "use a subagent when the work is self-contained and can return a summary" — implicitly endorsing a generalist main conversation for tasks requiring iteration. No empirical threshold exists for when specialization improves over a well-prompted generalist. The recommendation stands as conventional wisdom with directional support, not a validated principle.

---

### Coverage Gaps

**maxTurns calibration**: The official docs confirm `maxTurns` exists as a frontmatter field ("Maximum number of agentic turns before the subagent stops") but provide no guidance on how to calibrate it — no default value documented, no examples of when to set it low vs. high, no discussion of what happens at the limit (does the subagent return partial results or fail silently?). Search results confirm a community best practice exists ("set maxTurns to prevent runaway sessions") but no evidence of principled calibration guidance from Anthropic. This is a genuine gap.

**Worktree isolation (`isolation: worktree`)**: The official docs confirm this field exists and describe its function precisely: "Set to `worktree` to run the subagent in a temporary git worktree, giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes." The extracts do not mention `isolation` at all. This is a significant omission for any destructive or parallel-write subagent — it is the primary mechanism for preventing parallel file conflicts. Search results confirm practitioners have documented it, but none of the sources in the extracts surface it.

**Testing and validating a subagent**: No source in the extracts addresses how to verify a subagent works as authored. The official docs provide no testing workflow. The `/agents` command quickstart says "Try it: Use the code-improver agent to suggest improvements" — an informal smoke test, not a validation protocol. Issue #13627 (body silently dropped) demonstrates that subagents can appear to work (metadata recognized) while behavioral instructions are completely ignored. There is no documented pattern for confirming that: (1) the body was injected, (2) the tool restrictions are actually enforced, (3) the routing trigger fires as expected. This gap is consequential for practitioners writing production subagents.

**Naming conventions**: The official docs state `name` must use "lowercase letters and hyphens" but provide no guidance on naming patterns — functional vs. role-based vs. action-based names, team naming consistency, avoiding collisions. The VoltAgent collection uses a `[role]-[domain]` pattern (e.g., `code-reviewer`, `db-reader`, `browser-tester`) that has become a de facto community standard, but this is not formally documented. Search results indicate `.claude/agents/` stores subagents as files, where the filename-derived identifier vs. the `name` frontmatter field relationship is not clearly explained in the extracts.

**Optimal body length (line/word count)**: No source provides empirical data on optimal body length. The official code-reviewer example is approximately 150 words. The PubNub "you are a senior engineer" example is 2 sentences. The Piebald-AI Explore subagent body is several hundred words with structured sections. The range spans roughly 20–500+ words across examples with no guidance on where diminishing returns begin. The wos skill quality validator uses 500 lines as a SKILL.md ceiling — a rule of thumb derived from maintainability concerns, not LLM performance evidence.

**`skills` field and preloading context**: The official docs document a `skills` field that "injects skill content into a subagent's context at startup." This is not mentioned in any source in the extracts. It is a non-trivial authoring decision: skills preloaded at startup consume context immediately; skills loaded on-demand are more efficient for rarely-needed domain knowledge. The interaction between `skills` preloading and the subagent's body length ceiling is not discussed anywhere.

---

### Additional Findings

**Issue #13627 is closed "not planned" — resolution status remains ambiguous**: Direct fetch of the issue confirms it was marked stale and closed without a fix being logged. The current live official docs (fetched April 14, 2026) describe the body-as-system-prompt behavior in present tense without caveats, suggesting the regression may have been silently resolved in a later version. However, no changelog entry was found explicitly confirming this. Authors should test body injection empirically on their installed version rather than relying on either the bug report or the docs alone.

**Official docs now explicitly confirm `isolation: worktree` and `maxTurns`**: The current docs include both fields in the supported frontmatter table. The `isolation: worktree` description includes the automatic cleanup behavior (worktree cleaned if no changes made). These features are documented but absent from the research extracts — a gap in the original search coverage, not a gap in Anthropic's documentation.

**Piebald-AI extraction confirmed automated and version-tagged**: The repository is extracted via script from the npm package compiled JavaScript, updated within minutes of each Claude Code release, version-tagged across 110 CHANGELOG versions (v2.0.14–v2.1.107). Template variables (`${BASH_TOOL_NAME}` style) appear as literal strings in the extracted files and are interpolated at runtime — quoted text from these extracts may not be what the model sees verbatim. The repository has 8,709+ stars (as of April 2026) and tracks changes via CHANGELOG.md. For sourcing purposes: reliable for structural and directive content, unreliable for exact phrasing of runtime-interpolated strings.

**No empirical evidence found for ~140-char description optimum**: Additional searching found no A/B tests, ablation studies, or structured practitioner comparisons on description length and routing accuracy. The 140-char guideline is practitioner heuristic only.

**Generalist agent counter-evidence is domain-dependent**: The 2026 benchmarking landscape shows generalist models remain preferred for open-ended, ambiguous, and cross-domain tasks. The specialist-over-generalist principle holds for well-scoped repeatable tasks but does not apply universally. The Claude Code main conversation is itself a generalist agent, and the official docs explicitly recommend using it (not a subagent) for iterative, multi-phase, or context-heavy tasks — a built-in acknowledgment that generalist handling is sometimes the right call.

## Findings

### SQ1: Effective System Prompt Body Writing

**Structure: identity → scope → constraints → workflow → output contract** (HIGH — T1 official built-ins + T2 practitioner convergence)

Anthropic's own built-in subagents (Explore, Plan, general-purpose, extracted from v2.1.94 via Piebald-AI) follow a consistent pattern:
1. **Identity line** — one sentence establishing role and domain: "You are a [role] specialist for [domain]..."
2. **Scope/capabilities block** — what the agent does well, as a bullet list
3. **Constraint block** — explicit prohibitions in a named section (e.g., `=== CRITICAL: READ-ONLY MODE ===`), enumerated not implied
4. **Behavioral workflow** — numbered steps for how to execute the task
5. **Output contract** — explicit format for what to return, including any required sections

Anthropic's agent-creation-architect prompt (T2-extraction, v2.1.94) articulates the authoring intent: (1) extract core intent and success criteria, (2) design expert persona with deep domain knowledge, (3) write comprehensive instructions covering behavioral boundaries, edge cases, and output format, (4) include decision-making frameworks and fallback strategies.

**Single-responsibility, not single-topic** (HIGH — T1 + convergent T2)

Official docs: "each subagent should excel at one specific task." PubNub: "Give each subagent one clear goal, input, output, and handoff rule." eesel.ai: "A dedicated `code-reviewer` will always do a better job" than a general-purpose reviewer. The specialist principle holds for well-scoped repeatable tasks; the main conversation remains the right choice for open-ended or iterative work.

**"Comprehensive" vs. "concise" — reconciled** (MODERATE — T2 sources, reconciled through challenger analysis)

The apparent tension between "comprehensive instructions" (agent-creation-architect) and "not onboarding novels" (PubNub) resolves on scope: write comprehensive instructions about the agent's domain behavior; do not embed project-specific context (plans, decision logs, prior session findings) in the body. That context belongs in the invocation prompt. The official code-reviewer example body is ~150 words — structured but not verbose.

**No empirical body length guidance exists** (HIGH — gap confirmed by challenger)

No source provides empirical data on optimal body length. Observed range: 20 words (PubNub "senior engineer" example) to 500+ words (Piebald-AI Explore agent). The WOS skill validator uses 500 lines as a ceiling for SKILL.md — a maintainability heuristic, not a performance-grounded limit. Practitioner convention suggests 100–300 words for focused agents; no studies confirm this.

---

### SQ2: Description Field Authoring for Routing Effectiveness

**Format pattern: [Role] + [domain] + trigger phrase + trigger condition** (HIGH — T1 official examples + T2 convergence)

All three official example descriptions follow this structure:
- `"Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."`
- `"Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues."`

Community patterns confirm: action verbs + named domain + explicit "when" + "use proactively" phrasing. Target the router, not the agent — behavioral instructions belong in the body.

**Critical caveat: "use proactively" is aspirational, not reliable** (HIGH — T2 issue reports, confirmed closed NOT_PLANNED)

GitHub Issue #5688 documents a user with "You MUST use this agent PROACTIVELY" in all-caps who saw the primary agent ignore the directive entirely. Issue closed "not planned." Practitioner consensus (ksred.com, wmedia.es, Johnson Lee): auto-delegation is a soft preference signal, not a hard rule. The official docs describe intended behavior; the issue reports describe observed behavior. **The only reliable trigger is explicit invocation by name (@-mention or `subagent_type` parameter).**

This is not a MODERATE contradiction — it is a fundamental reliability gap. Design workflows around explicit invocation; treat auto-delegation as a convenience, not a guarantee.

**~140-char description length: practitioner heuristic, no T1 support** (MODERATE — T2 only, challenger confirmed no empirical evidence)

The 140-character guideline originates from GitHub Issue #10504 (T2), where Claude-generated descriptions at 1297–1308 characters were found to embed behavioral logic in the routing field. The real failure mode is mixing routing signals with agent instructions, not length per se. Length is a proxy indicator. No empirical comparison of routing accuracy at different lengths was found.

**Do not mix routing signals with agent instructions** (HIGH — T2 convergence)

awesome-claude-agents: "Never mix behavioural instructions meant for the agent into the `description` block." The description field targets Claude's router; the body targets the specialist. Instructions in the description field either bloat the routing pool or are silently ignored.

---

### SQ3: Tool Selection Strategy

**Principle of least privilege via hard constraints** (HIGH — T1 + T2 convergence)

Official docs: "Limit tool access: grant only necessary permissions for security and focus." ksred.com: "A reviewer defined with only `Read, Grep, Glob` cannot write files. That's not a naming convention or a prompt instruction, it's a hard constraint." Tool restrictions are deterministic enforcement; body instructions are not. If your body says "do not modify files" without restricting the tools, the constraint can be violated.

**Default inherits everything — the over-grant default** (HIGH — T1)

Omitting `tools` means the subagent inherits all tools from the main conversation, including MCP tools. This is the default over-grant path. Explicit restriction via `tools` allowlist or `disallowedTools` denylist is required for any security-sensitive or role-scoped agent.

**Three-tier tool taxonomy** (MODERATE — T2 community, consistent with T1 examples)

Community consensus codified in VoltAgent collection + awesome-claude-agents:
- **Read-only** (reviewers, auditors): `Read, Grep, Glob`
- **Research** (adds external access): `Read, Grep, Glob, WebFetch, WebSearch`
- **Implementation** (full execution): `Read, Write, Edit, Bash, Glob, Grep`

Official built-in examples align: Explore and Plan subagents use `disallowedTools` to strip Write/Edit; the debugger example uses `Read, Edit, Bash, Grep, Glob`.

**Hooks for conditional tool gating within a tool** (HIGH — T1)

When you need to allow some operations of a tool while blocking others (e.g., allow `Bash` but only for SELECT queries), use a `PreToolUse` hook rather than removing the tool entirely. The `tools` field grants/denies at the tool level; hooks enforce at the operation level.

---

### SQ4: Parent Prompt / Invocation Prompt Design

**The prompt is the only channel: front-load everything** (HIGH — T1 blog + T2 Piebald-AI extraction + T2 practitioner convergence)

MorphLLM: "If a subagent needs file paths, error messages, architectural decisions, or output from a previous subagent, the parent must include it in the Agent tool prompt. There is no other way to pass context."

Anthropic's internal invocation guidance (Piebald-AI v2.1.94 extraction — T2, treat as directionally sound, not guaranteed stable across versions): "Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters. Explain what you're trying to accomplish and why. Describe what you've already learned or ruled out."

**Never delegate understanding** (HIGH — T1 blog framing + Piebald-AI extraction)

The internal guidance is explicit: "Don't write 'based on your findings, fix the bug' or 'based on the research, implement it.' Those phrases push synthesis onto the agent instead of doing it yourself. Write prompts that prove you understood: include file paths, line numbers, what specifically to change."

**Scope the output explicitly** (HIGH — T1 blog + T2 convergence)

Official blog: "Specify what should be returned." Johnson Lee: "Prompts must be crystal clear — vague instructions plus zero interaction equals disaster." Specify return format and length (e.g., "Report: under 200 words, bullet list") to prevent flooding the parent's context with verbose output. Background subagents especially require complete prompts since no clarifying questions are possible mid-execution.

**Context re-discovery is a real cost** (MODERATE — T2 GitHub Issue #4908)

Without explicit context embedding, subagents will re-read files, re-analyze git diffs, and re-discover architectural context already known to the parent. This is latency and token cost, not a failure — but it's avoidable. Pass the specific findings, paths, and decisions the subagent needs rather than having it start from scratch.

---

### SQ5: Authoring Antipatterns

**1. Over-grant by omission** (HIGH — T1)
Omitting `tools` inherits everything. Default-to-restrict for any role-scoped subagent.

**2. Mixed-field instructions** (HIGH — T2)
Embedding behavioral instructions in `description` confuses the router. Description is a routing cue, not an instruction channel.

**3. Delegating without understanding** (HIGH — T1 + Piebald-AI extraction)
"Based on your findings, fix it" — synthesis not included. The parent must synthesize and pass specific context, not offload the synthesis to the subagent.

**4. Proactive-directive assumption** (HIGH — T2 GitHub issues, closed NOT_PLANNED)
Building a workflow that assumes "use proactively" will fire reliably. It won't. Design for explicit invocation; treat auto-delegation as a bonus.

**5. Super-agent antipattern** (MODERATE — T2/T3 convergence)
One agent that does everything. Quality degrades vs. focused specialists for well-defined, repeatable tasks. Counter-balance: too many narrow specialists increases routing fragmentation (official blog: "flooding Claude with options makes automatic delegation less reliable").

**6. Parallel write conflict** (HIGH — T1 official blog)
Two subagents editing the same file in parallel causes conflicts. Use `isolation: worktree` to give each subagent a separate git worktree for file-modifying parallel work.

**7. Over-delegation** (MODERATE — T2)
Spawning agents for work that would be faster inline. ksred.com: "Opus will delegate to agents in situations where a direct approach would be faster and cheaper." Each delegation adds coordination overhead.

**8. Context rot / prompt glue** (MODERATE — T2 PubNub)
Context rot: letting verbose subagent output accumulate in the main conversation thread. Prompt glue: copy-pasting context across agent definitions instead of using Skills for shared reusable context.

**9. Body-injection bug (version-specific)** (MODERATE — T2 GitHub issue #13627, resolution ambiguous)
In Claude Code v2.0.58, body content was silently dropped when spawning via the Task tool — metadata recognized, behavioral instructions ignored. The issue is closed "not planned" without an explicit fix being logged. Current docs describe body injection in present tense. Test empirically in your installed version rather than assuming the bug is resolved.

---

### Coverage Gaps (Not Well-Sourced)

- **`isolation: worktree`** — documented in T1 docs, absent from extracts; primary mechanism for parallel subagents writing files without conflict
- **`maxTurns` calibration** — field exists, no guidance on how to set it; what happens at the limit is undocumented
- **Testing/validating subagent authoring** — no documented protocol for confirming body injection, tool restrictions enforcement, or routing trigger behavior
- **`skills` preloading** — the `skills` frontmatter field injects skill content at startup; interaction with body length and context budget is undiscussed
- **Naming conventions** — community [role]-[domain] pattern is de facto standard; not T1-documented

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "The body becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt." | quote | [1] | verified |
| 2 | "By default, subagents inherit all tools from the main conversation, including MCP tools." | quote | [1] | verified |
| 3 | "If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed." | quote | [1] | verified |
| 4 | description field officially documented as "When Claude should delegate to this subagent" | attribution | [1] | verified |
| 5 | Official code-reviewer description: `"Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code."` | quote | [1] | verified |
| 6 | Official debugger description: `"Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues."` | quote | [1] | verified |
| 7 | Official data-scientist description: `"Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries."` | quote | [1] | verified |
| 8 | Official code-reviewer example: `tools: Read, Grep, Glob, Bash`; debugger: `tools: Read, Edit, Bash, Grep, Glob`; data-scientist: `tools: Bash, Read, Write` | attribution | [1] | verified |
| 9 | Explore subagent: `disallowedTools: R4, ExitPlanMode, Edit, Write, NotebookEdit` (read-only pattern) | attribution | [1] [3] | verified — Piebald-AI extraction (v2.1.84/2.1.105) confirms; `R4` is the current name (formerly `Agent`), as noted in docs changelog (v2.1.63 rename) |
| 10 | Issue #10504: descriptions found at 1297 and 1308 characters, violating documented 1024-character limit | statistic | [7] | verified — issue text shows "python-code-reviewer.md: 1297 characters" and "react-ui-reviewer.md: 1308 characters" |
| 11 | Issue #5688 closed as NOT_PLANNED | attribution | [8] | verified |
| 12 | Issue #13627 (body content silently dropped, Claude Code v2.0.58) closed as NOT_PLANNED | attribution | [9] | verified — stateReason is NOT_PLANNED; version v2.0.58 confirmed in issue body |
| 13 | Issue #10504 closed as NOT_PLANNED | attribution | [7] | verified |
| 14 | Piebald-AI repo has 5,900+ GitHub stars | statistic | [3] | corrected: 8,709 stars as of April 2026 (repository has grown significantly) |
| 15 | Piebald-AI tracks 149+ versions | statistic | [3] | corrected: CHANGELOG contains 110 version entries from v2.0.14 to v2.1.107 (30 formal releases); "149+" appears in the repo README as a running count that may reflect total Claude Code releases tracked, but CHANGELOG entries total 110 — human-review recommended |
| 16 | Piebald-AI prompts extracted from "compiled JavaScript bundle" of the Claude Code npm package | attribution | [3] | verified — repo describes extraction from "compiled source code" / "minified JS file" of the npm package |
| 17 | "Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters." | quote | [3] | verified — exact text present in `system-prompt-writing-subagent-prompts.md` (ccVersion 2.1.94) |
| 18 | "For fresh agents, terse command-style prompts produce shallow, generic work." | quote | [3] | corrected: actual text is `"For fresh agents, terse command-style prompts produce shallow, generic work."` — verified, with the caveat that the source file uses a conditional template: `${HAS_SUBAGENT_TYPE?"For fresh agents, terse":"Terse"}` — the "fresh agents" phrasing only renders when a subagent_type is specified |
| 19 | "Never delegate understanding. Don't write 'based on your findings, fix the bug'…" | quote | [3] | verified — exact text present in `system-prompt-writing-subagent-prompts.md` |
| 20 | "Two subagents editing the same file in parallel is a recipe for conflict." | quote | [2] | verified |
| 21 | "Too many specialist agents...flooding Claude with options makes automatic delegation less reliable." | quote | [2] | corrected: actual text is "It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable." — no leading "Too many specialist agents" fragment in source |
| 22 | "Auto-selection of custom agents remains unreliable. Claude frequently handles tasks in the main session rather than delegating to a defined agent, even when the agent is explicitly relevant and its description matches the task. The only reliable trigger is explicit invocation." | quote | [11] | corrected: source omits "even when the agent is explicitly relevant and its description matches the task" — actual text ends "...rather than delegating to a defined agent" then separately: "The only reliable trigger is explicit invocation, which defeats the purpose of automatic routing." |
| 23 | "A reviewer defined with only `Read, Grep, Glob` cannot write files. That's not a naming convention or a prompt instruction, it's a hard constraint." | quote | [11] | verified |
| 24 | "Prompts must be crystal clear — vague instructions plus zero interaction equals disaster." | quote | [12] | verified — source uses em dash: "crystal clear – vague instructions plus zero interaction equals disaster" (minor punctuation difference) |
| 25 | agent-creation-architect prompt instructs: "Extract Core Intent", "Design Expert Persona", "Architect Comprehensive Instructions", "Optimize for Performance" | attribution | [3] | verified — all four steps present in `agent-prompt-agent-creation-architect.md` (ccVersion 2.0.77) |
