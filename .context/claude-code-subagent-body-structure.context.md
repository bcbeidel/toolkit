---
name: "Claude Code Subagent Body Structure"
description: "How to write an effective subagent system prompt body — the 5-part structure from Anthropic's built-in agents and the agent-creation-architect design framework"
type: context
sources:
  - https://code.claude.com/docs/en/sub-agents
  - https://claude.com/blog/subagents-in-claude-code
  - https://github.com/Piebald-AI/claude-code-system-prompts
  - https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/
related:
  - docs/research/2026-04-14-subagent-authoring-best-practices.research.md
  - docs/context/claude-code-subagent-definition-format.context.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
---

# Claude Code Subagent Body Structure

The subagent body becomes the full system prompt. The agent receives this plus basic environment details (working directory) and nothing else — no parent conversation history, no CLAUDE.md, no project context. What you write here is the agent's entire operating model.

## The 5-Part Structure

Anthropic's own built-in agents (Explore, Plan, general-purpose) follow a consistent structure. This is observable from Piebald-AI's extraction of the Claude Code npm bundle (v2.1.94 — treat as directionally sound, version-specific, template variables not interpolated):

1. **Identity line** — One sentence establishing the agent's role and owner context. Example from Explore: "You are a file search specialist for Claude Code..."

2. **Scope / capabilities block** — A short list of what this agent does well. Sets expectations for the agent itself and provides a self-check anchor.

3. **Constraint block** — A named section with an explicit enumeration of prohibited operations. Explore uses a capitalized header: `=== CRITICAL: READ-ONLY MODE — NO FILE MODIFICATIONS ===` followed by a bullet list of what cannot be done. This is not a soft guideline — it works in conjunction with tool restrictions to create layered enforcement.

4. **Numbered behavioral workflow** — Ordered steps the agent must follow. Plan uses: (1) Understand Requirements, (2) Explore Thoroughly, (3) Design Solution, (4) Detail the Plan — each with tool-use rules per step.

5. **Output contract** — Explicit statement of what the response must contain and how. Plan ends with: "End your response with: ### Critical Files for Implementation / List 3-5 files..."

## The Agent-Creation-Architect Framework

Anthropic's internal system prompt for generating new subagents (extracted from Piebald-AI v2.1.94) describes the design intent:

1. **Extract Core Intent** — identify the fundamental purpose, key responsibilities, and success criteria
2. **Design Expert Persona** — create a compelling expert identity that embodies deep domain knowledge
3. **Architect Comprehensive Instructions** — establish behavioral boundaries, specific methodologies, edge case handling, and output format expectations
4. **Optimize for Performance** — include decision-making frameworks, quality control mechanisms, self-verification steps, efficient workflow patterns, and fallback strategies

Key principle from this source: "Be specific rather than generic — avoid vague instructions. Include concrete examples when they would clarify behavior. Balance comprehensiveness with clarity — every instruction should add value."

## Single-Responsibility Principle

Each subagent should have one clear goal, one input type, one output type, and one handoff rule. This is not about brevity — it is about scope clarity. A well-scoped body prevents the agent from improvising on adjacent tasks it was not designed for.

## Reconciling "Comprehensive" vs. "Concise"

These are not contradictory:

- **Comprehensive** applies to domain instructions — behavioral boundaries, edge cases, methodologies. Do not be vague about what the agent should do.
- **Concise** applies to project context — do not embed project-specific background, existing decisions, or conversation history in the body. That context belongs in the invocation prompt, not the body.

The general-purpose built-in agent illustrates this: it opens with task-completion framing and explicit prohibitions ("NEVER create files unless absolutely necessary"), but has no project-specific content.

## Length

No empirical body length guidance exists in official documentation. The official code-reviewer example is approximately 150 words. The range observed across community examples spans 20 to 500+ words. Length should be determined by what the agent needs to operate correctly — not by a word count target.

**Takeaway:** Write identity → scope → constraint block → numbered workflow → output contract. Comprehensive means covering domain behaviors and edge cases; concise means no project context in the body. No length target exists — size to the agent's operational needs.
