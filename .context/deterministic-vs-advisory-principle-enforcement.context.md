---
name: "Deterministic vs Advisory Principle Enforcement"
description: "Enforce principles deterministically (hooks/linters) where mechanically verifiable; advisory text in docs is not a substitute for a linter"
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://martinfowler.com/bliki/ArchitectureDecisionRecord.html
  - https://www.anthropic.com/research/building-effective-agents
related:
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/agent-facing-document-structure.context.md
  - docs/context/context-file-content-selection-and-coverage-threshold.context.md
---
Advisory guidance and deterministic enforcement are not interchangeable. The failure mode of conflating them is well-documented: a CLAUDE.md rule that says "NEVER edit .env files" is a suggestion the model weighs against other signals. A hook that blocks `.env` edits via exit code 2 is a wall. Only one of these is enforcement.

The practical rule is simple: if a principle can be mechanically verified, use a tool. Never send an LLM to do a linter's job.

## The Enforcement Decision Matrix

Ask two questions for any principle:

1. **Is it mechanically verifiable?** Can a script check compliance without judgment?
2. **What is the cost of a violation?** Data loss, security breach, broken build, or stylistic preference?

If both answers point toward "yes" and "high cost," the principle belongs in a hook or CI check, not in a context file. Advisory text handles the remainder: architectural decisions, engineering philosophy, naming conventions, and guidance where legitimate edge cases exist.

| Deterministic (hooks, linters, CI) | Advisory (CLAUDE.md, AGENTS.md) |
|------------------------------------|----------------------------------|
| Running formatters and linters | Architectural decisions |
| Blocking dangerous commands | Engineering philosophy |
| Protecting sensitive files | Naming conventions and preferences |
| Pre-commit validation gates | Technology stack context |
| Schema or frontmatter format checks | Guidance with legitimate edge cases |

## Why Advisory Instructions Fail as Enforcement

Three documented failure modes for advisory guidance:

1. **Context dilution** — important rules buried in a long context file get lost as the session fills. The model stops attending to them under attention pressure.
2. **Probabilistic compliance** — instructions are weighed against other signals. A sufficiently urgent user request can override a soft instruction.
3. **LLM interpretation** — agents process advisory text with judgment, not as a rule engine. They exercise discretion about when rules apply.

Advisory instructions that keep being violated are a signal: convert them to hooks. If a principle is important enough to state, it is important enough to enforce mechanically when possible.

## Architecture Decision Records Capture the Why

ADRs (Architecture Decision Records) formalize the reasoning history behind principles. Short documents — one decision per ADR, with context, alternatives considered, and consequences — stored in source control, numbered monotonically, immutable once accepted (superseded rather than edited). The act of writing an ADR clarifies the reasoning; the record explains to future agents and developers why the system is built as it is.

ADRs are not enforcement — they are the advisory layer for decisions that cannot be mechanically verified. They prevent the failure mode where an important constraint is lost when the person who made it leaves or forgets the reasoning.

## The Three-Tier Boundary System

Structuring advisory guidance into three tiers reduces ambiguity:
- **NEVER** — hard prohibitions the agent should treat as non-negotiable in advisory context
- **ASK** — actions requiring human escalation before proceeding
- **ALWAYS** — proactive requirements the agent should apply by default

This structure acknowledges that advisory guidance operates on a spectrum and makes the enforcement boundary explicit. Principles in the NEVER tier are candidates for mechanical enforcement if they can be expressed as a linter rule.

Note: prohibitive framing has a documented failure mode ("Pink Elephant Problem") — telling agents what NOT to do front-loads the forbidden concept in their attention and can increase the probability of the forbidden action. Where possible, fix the structural friction that makes the prohibited action attractive rather than relying on the prohibition alone.
