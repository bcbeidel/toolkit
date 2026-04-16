---
name: AI Pair Programming — Explore-Plan-Implement-Commit Workflow
description: The Explore-Plan-Implement-Commit workflow is the highest-confidence structural pattern for AI coding; providing tests upfront is the single top quality lever.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/best-practices
  - https://codescene.com/blog/agentic-ai-coding-best-practice-patterns-for-speed-with-quality
  - https://hamy.xyz/blog/2025-07_ai-checkpointing
  - https://trackmind.com/ai-agent-handoff-protocols/
related:
  - docs/context/ai-pair-programming-asymmetry-and-context-as-resource.context.md
  - docs/context/agentic-planning-hybrid-global-plan-local-react.context.md
  - docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md
  - docs/context/skill-chain-recovery-and-state-checkpointing.context.md
---
# AI Pair Programming — Explore-Plan-Implement-Commit Workflow

The Explore-Plan-Implement-Commit workflow is the most-cited high-leverage structural pattern for AI pair programming. It is documented in Anthropic's official Claude Code best practices and independently corroborated by multiple practitioner sources.

The problem it solves: "Letting Claude jump straight to coding can produce code that solves the wrong problem." Separating research from execution eliminates the most common AI coding failure mode — confident implementation of the wrong thing.

## The Four Phases

**Explore** — read files, understand the codebase, map dependencies. No changes. This phase establishes shared context between the human and the AI before any implementation decisions are made. Use Plan Mode to separate this phase from execution.

**Plan** — produce a detailed implementation plan. This is reviewable, editable (Ctrl+G in Claude Code), and correctable before any code changes occur. The human reviews and approves or modifies the plan. This is the decision boundary: human judgment at planning time, not at code review time.

**Implement** — execute the plan with built-in verification. The quality lever here is tests-first: provide tests, screenshots, or expected outputs upfront so the AI can verify its own work as it implements. This is the single highest-leverage quality practice in the literature — it converts the AI from a generator into a generator + verifier.

**Commit** — finalize with an atomic commit and PR message. Code-level checkpoints via atomic git commits before and after each logical task enable cross-session recovery and make the work legible in the history.

## Handoff Autonomy Is Graduated, Not Binary

Before delegating any task, calibrate the appropriate autonomy level based on:
- **Risk** — error cost and reversibility
- **Explainability** — auditability requirements
- **Accuracy confidence** — how well the AI understands the scope
- **Consequence severity** — downstream impact of an error
- **Time sensitivity** — urgency vs. validation time trade-off

Level 1 (full supervision, AI proposes then human approves) is appropriate for schema changes, security changes, and anything irreversible. Level 3–4 (monitored or periodic review) is appropriate for high-volume reversible tasks. Default to Level 1 for anything multi-file or architectural.

## Checkpoint-Based Delegation for Cross-Session Work

Project checkpoints serve as quest trackers for AI sessions. Effective checkpoints contain:
- RFC or design documents with business context and implementation approach
- A task description file specifying the current work requirements
- A task tracking file with the AI's documented understanding, current plan, and progress state

"With the task description and tracking files in place, I'm never worried about spinning up a new AI session if the old one gets stuck — the new AI can catch up."

This pattern has no analog in traditional pair programming. It extends the collaboration surface across session boundaries, enabling seamless handoff and recovery.

## Write/Review Parallel Session Pattern

A documented high-quality pattern separates implementation from review into two independent sessions: Session A (Writer) implements the feature; Session B (Reviewer) reviews from fresh context without implementation bias. "Claude won't be biased toward code it just wrote."

**The takeaway:** Always Explore and Plan before implementing. Provide tests and expected outputs upfront — this is the single top quality lever. Calibrate autonomy per task type rather than defaulting to full delegation. Checkpoint work for cross-session recovery.
