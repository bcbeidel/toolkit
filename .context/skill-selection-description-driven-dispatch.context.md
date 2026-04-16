---
name: "Skill Selection Uses Description-Driven Dispatch, Not a Classifier"
description: "Skill selection is driven entirely by LLM reasoning over description field text — no embedding, classifier, or algorithmic routing — and this pattern generalizes across all Agent Skills runtimes"
type: context
sources:
  - https://code.claude.com/docs/en/skills
  - https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
  - docs/context/skill-routing-failure-modes-and-pushy-heuristic.context.md
  - docs/context/skill-description-authoring-cross-platform.context.md
---

# Skill Selection Uses Description-Driven Dispatch, Not a Classifier

Claude Code performs no embedding lookup, vector similarity search, or intent classifier to select skills. Skill selection is entirely within Claude's LLM reasoning process, based on reading the `description` field of available skills and deciding which one matches the user's intent. This is the generalizable pattern across all Agent Skills implementations — it is what makes description quality the primary determinant of selection accuracy.

## How Dispatch Works

When a user sends a message, Claude receives L1 metadata (skill names and descriptions) injected into its context. It reads these descriptions and reasons about which skill, if any, matches the user's intent. No algorithmic shortcut precedes this reasoning.

The implication: descriptions must be written as explicit trigger conditions, not passive summaries. "Use when the user wants to conduct a structured investigation" outperforms "Conducts investigations" because the former gives Claude a decision rule, not a label.

Skill description quality directly determines selection accuracy. Ambiguous or overlapping descriptions cause missed triggers and incorrect routing. This is why WOS enforces description length minimums and discourages passive-voice phrasing.

## What Is Claude Code-Specific vs. Generalizable

**Generalizable:** The description-driven dispatch pattern applies to all Agent Skills runtimes. Copilot CLI, Gemini CLI, and Codex all use LLM reasoning over `description` fields to route skill invocation. There is no runtime that uses a separate classifier.

**Claude Code-specific implementation details:**
- The character budget for skill metadata scales dynamically at 1% of the context window, with a fallback of 8,000 characters. One practitioner source cites 15,000 characters as a default, which may describe a different context size configuration; the 8,000 fallback is confirmed from Claude Code documentation.
- The `<available_skills>` injection block format and truncation behavior are Claude Code implementation details.
- The `isMeta` flag (used internally by Claude Code to mark meta-skills) is a Claude Code implementation detail not present in the open spec.

## Authoring Guidance That Generalizes

Because description-driven dispatch is universal across Agent Skills runtimes, authoring guidance grounded in it transfers:

- Write descriptions as conditional trigger phrases ("Use when...")
- Avoid overlapping trigger conditions across skills in the same catalog
- Keep descriptions dense with distinguishing signal, not generic capability labels
- Test selection by presenting a user request and checking which description Claude would match

This guidance applies equally to WOS skills targeting Claude Code and to the subset of WOS skill descriptions authored for portability.

---

**Takeaway:** All Agent Skills runtimes select skills through LLM reasoning over `description` text — no classifier or embedding. Description quality is the primary lever for selection accuracy. This pattern and the authoring practices it implies transfer across runtimes; only the character budget and injection mechanics are Claude Code-specific.
