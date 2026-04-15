---
name: "Claude Code Subagent Invocation Prompt Design"
description: "How to write the invocation prompt — the sole context channel from parent to subagent, requiring front-loaded context and no delegated synthesis"
type: context
sources:
  - https://github.com/Piebald-AI/claude-code-system-prompts
  - https://claude.com/blog/subagents-in-claude-code
  - https://www.morphllm.com/claude-subagents
  - https://github.com/anthropics/claude-code/issues/4908
related:
  - docs/research/2026-04-14-subagent-authoring-best-practices.research.md
  - docs/context/claude-code-subagent-context-isolation-model.context.md
  - docs/context/claude-code-subagent-invocation-and-routing.context.md
---

# Claude Code Subagent Invocation Prompt Design

The prompt string passed to the Agent tool is the only context channel from parent to subagent. No conversation history is inherited. No CLAUDE.md is loaded. No parent skills or project context carry over. What you write in the prompt is all the subagent has.

## The Core Principle: Brief Like a Colleague with Zero Context

Anthropic's internal invocation-writing guidance (extracted from Piebald-AI v2.1.94 — treat as directionally sound, version-specific, template variables not interpolated):

> "Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters."

Required elements:
- What you're trying to accomplish and why
- What you've already learned or ruled out
- Enough surrounding context for the agent to make judgment calls
- Explicit output format and length constraints ("report in under 200 words")

> "For fresh agents, terse command-style prompts produce shallow, generic work."

## Never Delegate Understanding

The most common invocation failure: writing "based on your findings, fix the bug" or "based on the research, implement it." These phrases push synthesis onto the subagent instead of doing it in the parent.

From Anthropic's internal guidance: "Write prompts that prove you understood: include file paths, line numbers, what specifically to change."

The parent has seen the full conversation. The parent understands why decisions were made. The parent should synthesize and pass specific, actionable context — not a vague directive that forces the subagent to re-derive everything.

## Scope the Return Format

The invocation prompt should explicitly constrain what the subagent returns. Without this, subagent output accumulates in the parent's context window unchecked.

- Specify length: "report in under 200 words"
- Specify format: "return a punch list — done vs. missing"
- Specify what to omit: "return a summary, not full file contents"

The official blog: "Specify what should be returned."

## Context Re-Discovery Cost

Without embedding context, subagents re-read files and re-discover architectural decisions the parent already knows. GitHub Issue #4908 documented: "Subagents re-discover information already available to the parent — Increased Latency & Token Cost." This is avoidable by embedding relevant context directly in the invocation prompt.

If a subagent needs file paths, error messages, architectural decisions, or output from a previous step, the parent must include it. There is no other way to pass context.

## Background Subagents Demand Extra Clarity

Background subagents execute immediately without any opportunity for mid-task clarification. Vague instructions plus zero interaction produce incorrect results with no recovery path. Every detail must be front-loaded.

## Worked Example Structure

A well-formed invocation prompt (from Anthropic's internal delegation examples) for a migration review:

> "Review migration 0042_user_schema.sql for safety. Context: we're adding a NOT NULL column to a 50M-row table. Existing rows get a backfill default. I want a second opinion on whether the backfill approach is safe under concurrent writes — I've checked locking behavior but want independent verification. Report: is this safe, and if not, what specifically breaks?"

This prompt includes: what to do, which file, the relevant constraints, what the parent already verified, and the explicit return format.

**Takeaway:** Treat every invocation prompt as a briefing for a context-free colleague. Front-load everything needed, prove you synthesized the findings, and constrain the output format. Never write "based on your findings..." — that synthesis is your job.
