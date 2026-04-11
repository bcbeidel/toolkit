---
name: "Skill Chaining: Definition and Vocabulary"
description: "No settled standard exists for 'skill chaining'; practitioner consensus converges on coordinated sequential outputs, while the 2025 academic SoK four-tuple definition is stricter and wos SKILL.md satisfies it only partially."
type: context
sources:
  - https://www.anthropic.com/research/building-effective-agents
  - https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
  - https://www.promptingguide.ai/techniques/prompt_chaining
  - https://arxiv.org/html/2602.20867
  - https://orq.ai/blog/llm-orchestration
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/context/skill-chain-sequential-and-recursive-design-rules.context.md
---

# Skill Chaining: Definition and Vocabulary

**The field is mid-consolidation — no single authoritative standard exists (MODERATE confidence).** The dominant practical vocabulary is "prompt chaining" or "sequential orchestration": decomposing a task into subtasks where each LLM call processes the output of the previous one. The terminology varies across frameworks; the underlying concept is stable.

## Practitioner Consensus

Sources converge on a core definition: skill chaining is "a coordinated sequence of skills where each skill consumes the prior skill's structured output." Specific framings vary:

- Anthropic: "workflows" where "LLMs and tools are orchestrated through predefined code paths," with prompt chaining as "sequential steps where each LLM call processes the output of the previous one."
- Microsoft Azure: "sequential orchestration pattern — agents organized in a pipeline where each processes the output from the previous agent." Also called: pipeline, prompt chaining, linear delegation.
- LangChain: four-unit composition vocabulary — subagents, skills, handoffs, and routers — where chains emerge from their combination.
- DAIR.AI/Prompt Engineering Guide: chaining "breaks complex tasks into subtasks where each LLM response feeds into the next prompt."

Terms used interchangeably in practice: prompt chaining, skill chaining, agent pipeline, sequential orchestration, chain-of-thought, workflow composition.

## Academic Definition (Stricter)

The SoK paper (arXiv 2602.20867, Feb 2025) proposes a formal four-tuple: a skill is ⟨C, π, T, R⟩ — applicability condition, policy, termination condition, reusable interface. This explicitly distinguishes skills from tools, memory, and prompt templates. It is stricter than any framework definition.

Under this definition, skills are composable units with first-class termination conditions (T) and applicability conditions (C) — the skill specifies when it can run and when it should stop.

## Where wos Stands

wos's SKILL.md concept maps to the academic definition partially:

- **Policy (π)**: present — the SKILL.md body defines execution logic.
- **Reusable interface (R)**: present — SKILL.md frontmatter + trigger description.
- **Termination condition (T)**: absent as a first-class property — skills complete when Claude finishes, but no explicit halting criterion is declared.
- **Applicability condition (C)**: absent as a first-class property — description-driven routing approximates this but does not enforce it.

wos aligns with the practitioner mainstream. The academic standard requires richer first-class structure that current SKILL.md does not capture.

**Bottom line:** Skill chaining in wos = a coordinated sequence of skill invocations where each skill's output feeds the next. The vocabulary is stable at the practical level; the formal academic standard is stricter than what wos currently implements.
