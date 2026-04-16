---
name: "Instruction File Lifecycle and Pruning"
description: "Treat instruction files like code: version in git, add rules when mistakes recur, prune on schedule using a four-tier audit filter — stale rules actively mislead agents and are worse than no rules"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/best-practices
  - https://cursor.com/blog/agent-best-practices
  - https://www.mindstudio.ai/blog/rules-file-ai-agents-standing-orders-claude-code
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://factory.ai/news/using-linters-to-direct-agents
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/instruction-file-non-inferable-specificity.context.md
  - docs/context/instruction-file-extraction-techniques.context.md
  - docs/context/instruction-file-authoring-anti-patterns.context.md
---
# Instruction File Lifecycle and Pruning

Treat instruction files like code: version in git, review changes in PRs, and prune on a schedule. A stale rules file is worse than no rules file — it tells agents to do things that are no longer true about the project, actively misleading rather than guiding.

## When to Add a Rule

Add a rule when the agent makes the same mistake twice. This is the iterative correction loop recommended by both Claude Code and Cursor official docs. The trigger is a recurrence, not a first occurrence — a single mistake may be a prompt issue; a repeated mistake indicates a structural gap in the instruction file.

Convert the correction into a specific rule: "Never instantiate PrismaClient directly — import from `../db`" rather than "use the project's database abstraction." Agent Rules Builder frames this accumulation as the core growth mechanism: "The most effective rules files are built over months of real AI-assisted development."

## When to Remove a Rule

Remove a rule when the behavior it guards is no longer a failure mode — because the model default has improved, the codebase pattern has changed, or the constraint has moved into tooling. MindStudio: "A stale rules file is worse than no rules file in some cases — it tells the agent to do things that are no longer true about the project."

Diagnostic: if the agent keeps doing something you don't want despite a rule against it, the file is probably too long and the rule is getting lost. If the agent asks questions answered in the file, the phrasing is ambiguous. Both indicate pruning is overdue.

## Four-Tier Audit Filter

When auditing an instruction file for pruning, classify each rule into one of four tiers:

| Tier | Criteria | Action |
|---|---|---|
| **Essential** | Architecture decisions, non-inferable constraints, custom tooling | Keep |
| **Helpful** | Measurably improves agent output, has demonstrated value | Keep |
| **Redundant** | Model already does this, convention visible in code | Delete |
| **Move-to-tooling** | Belongs in linter, formatter, or CI config | Move, then delete |

Author anecdote (Alex Efimenko): trimming from 200+ lines to 80 using this filter produced "noticeably better agent performance with fewer, sharper directives."

## Linters vs. Instruction Files

Instruction files are advisory: agents can choose to ignore documentation. Linters are deterministic: agents cannot ignore linting errors in CI. Factory.ai's principle: "AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline."

Use instruction files for context and rationale — the "why." Use linters, formatters, and CI checks for deterministic style enforcement — the "how." When a rule in the instruction file is purely mechanical (indentation, import order, semicolons), move it to tooling and delete it from the instruction file. This keeps the file dense with non-inferable context and avoids wasting rule-following headroom on things a linter handles for free.

## Git and Review Practices

- Check instruction files into git; changes compound in value over time
- Review instruction file changes in PRs the same way you review code changes
- Schedule periodic audits (e.g., after major framework upgrades, at quarterly reviews)
- Cursor's official docs: "When you see the agent make a mistake, update the rule" — treat the file as a living document, not a one-time artifact
