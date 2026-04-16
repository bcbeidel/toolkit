---
name: "Claude Code Subagent Authoring Antipatterns"
description: "9 common authoring mistakes when building Claude Code subagents, with evidence strength for each and explicit tension between opposing failure modes"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://github.com/anthropics/claude-code/issues/5688
  - https://github.com/anthropics/claude-code/issues/13627
  - https://www.pubnub.com/blog/best-practices-claude-code-subagents-part-two-from-prompts-to-pipelines/
  - https://www.ksred.com/claude-code-agents-and-subagents-what-they-actually-unlock/
related:
  - docs/research/2026-04-14-subagent-authoring-best-practices.research.md
  - docs/context/claude-code-subagent-permission-and-security-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
---

# Claude Code Subagent Authoring Antipatterns

Nine failure modes documented across official sources and practitioner reports, each with an evidence rating. Antipatterns 5 and 6 pull in opposite directions — both are real.

## 1. Over-Grant by Omission (HIGH — T1)

Omitting the `tools` field causes the subagent to inherit all tools from the main conversation, including MCP tools. For any role-scoped agent, this is an unintended capability grant. The official quickstart states this explicitly. Default to restriction; inherit-all only for explicitly general-purpose agents.

## 2. Mixed-Field Instructions (HIGH — T2)

Embedding behavioral logic in `description` confuses the routing signal. The `description` field is read by the router to decide which agent to invoke; it is not read during the agent's execution. Instructions placed there are both routing noise and dead code. Keep routing cues in `description`; behavioral instructions in the body.

## 3. Delegating Without Understanding (HIGH — T1 + Piebald-AI)

Writing "based on your findings, fix it" or "based on the research, implement it" pushes synthesis onto the subagent. Anthropic's internal guidance states: "Those phrases push synthesis onto the agent instead of doing it yourself. Write prompts that prove you understood: include file paths, line numbers, what specifically to change." The parent has full context; the subagent has none. Synthesis belongs in the parent.

## 4. Proactive-Directive Assumption (HIGH — T2 closed NOT_PLANNED)

Building workflows that depend on "use proactively" auto-firing reliably. GitHub Issue #5688 documented all-caps "MUST USE PROACTIVELY" directives being ignored entirely by the primary agent. The issue was closed NOT_PLANNED — Anthropic acknowledged the gap and chose not to fix it. Auto-delegation is a soft preference signal, not a hard rule. Explicit invocation is the only reliable trigger.

## 5. Super-Agent Antipattern (MODERATE — T2/T3)

Building one agent that handles everything. A dedicated `code-reviewer` will consistently outperform a general agent on review tasks. The single-responsibility principle applies: one clear goal, one input type, one output type. This is the "one agent for everything" failure.

## 6. Agent Flooding (MODERATE — T1 official blog)

Defining a custom subagent for every task. From the official blog: "It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable." Too many narrow specialists fragment routing reliability and increase coordination overhead.

**The tension:** Antipatterns 5 and 6 both hold simultaneously. Too broad degrades quality; too narrow degrades routing. The practical resolution: create agents for well-defined, repeatable, high-value roles — not for every one-off task.

## 7. Parallel Write Conflict (HIGH — T1)

Spawning two subagents that modify the same file in parallel. From the official blog: "Two subagents editing the same file in parallel is a recipe for conflict." For file-modifying parallel work, use `isolation: worktree` to give each subagent its own working copy.

## 8. Context Rot / Prompt Glue (MODERATE — T2)

Two related failures: (a) verbose subagent output accumulating in the main thread until context becomes a "landfill," and (b) copy-pasting similar prompts and context blocks across agent definitions instead of using Skills for reuse. Fix: scope return format in the invocation prompt to constrain output; use Skills for shared context instead of duplicating it.

## 9. Body-Injection Bug Assumption (MODERATE — T2, resolution ambiguous)

In Claude Code v2.0.58, body content was silently dropped when spawning via the Task tool (now renamed Agent tool). Subagent metadata was recognized, but behavioral instructions had no effect. GitHub Issue #13627 was closed NOT_PLANNED without an explicit fix statement. The current official docs (April 2026) describe body injection in present tense, suggesting the bug may be resolved — but no changelog entry confirms it. Test body injection empirically in your current version rather than assuming either the bug is gone or that the docs are accurate.

**Takeaway:** The highest-risk antipatterns are over-grant by omission (#1), delegating without synthesizing context (#3), and parallel write conflicts (#7) — all with T1 evidence. The super-agent vs. agent flooding tension (#5/#6) is real and requires judgment, not a rule.
