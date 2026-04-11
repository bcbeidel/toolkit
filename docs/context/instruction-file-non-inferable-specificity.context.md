---
name: "Instruction File Non-Inferable Specificity"
description: "Rules that state only what an agent cannot determine from reading the codebase add value; rules restating model defaults or code-readable conventions waste tokens without changing behavior"
type: context
sources:
  - https://code.claude.com/docs/en/best-practices
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://www.mindstudio.ai/blog/rules-file-ai-agents-standing-orders-claude-code
  - https://arxiv.org/abs/2602.11988
related:
  - docs/research/2026-04-10-rules-creation-and-curation.research.md
  - docs/context/agents-md-empirical-effectiveness-findings.context.md
  - docs/context/instruction-file-authoring-anti-patterns.context.md
  - docs/context/instruction-file-lifecycle-and-pruning.context.md
---

# Instruction File Non-Inferable Specificity

Non-inferable specificity is the decisive quality signal for instruction files. A rule earns its tokens only if it states something an agent cannot determine by reading the codebase — custom commands, non-default conventions, architecture constraints, environment quirks. Rules that restate model defaults or conventions already visible in code consume context without changing behavior.

## The Specificity Test

MindStudio's formulation: "If two different developers read your rules file and would make the same decision in the same situation, the rule is specific enough." If the rule produces consistent decisions, it's carrying information the agent needs. If the rule is so generic that any developer would behave the same way without it, it's noise.

A sharper operational test: would removing this line cause the agent to make a mistake? Claude Code's official docs make this explicit — "For each line, ask: 'Would removing this cause Claude to make mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions."

## Include / Exclude Reference

Claude Code's official docs provide this distinction verbatim:

**Include:**
- Bash commands Claude can't guess
- Code style rules that differ from defaults
- Testing instructions
- Repository etiquette
- Architectural decisions specific to your project
- Developer environment quirks
- Common gotchas or non-obvious behaviors

**Exclude:**
- Anything Claude can figure out by reading code
- Standard language conventions Claude already knows
- Detailed API documentation (link to docs instead)
- Information that changes frequently
- Long explanations or tutorials
- File-by-file descriptions of the codebase
- Self-evident practices like "write clean code"

## Why Redundancy Is the Primary Failure Mode

ETH Zurich (arXiv 2602.11988) found that LLM-generated context files reduce task success −0.5% to −2% and increase inference cost +20%. The critical exception: when existing project markdown documentation is stripped from repositories, the same generated files improve task success +2.7%. This isolates the failure mode — context files hurt when they duplicate what agents can already read from READMEs and project docs, not because context files are inherently harmful.

The implication for authoring: every rule should pass a redundancy check before it is written. If the convention is visible in the codebase, the README, or a linked doc, omit it.

## Practical Threshold

HumanLayer maintains their root instruction file at under 60 lines. Practitioner consensus converges on 300 lines as an upper bound; Claude Code's docs note that files that are too long cause important rules to get lost. The specificity filter — only stating what is non-inferable — is the mechanism that keeps files within these bounds without arbitrary line counting.
