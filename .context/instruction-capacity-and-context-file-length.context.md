---
name: "Instruction Capacity and Context File Length"
description: "Instruction capacity is finite and model-dependent; shorter higher-signal context files strictly better"
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://arxiv.org/abs/2507.11538
  - https://www.humanlayer.dev/blog/writing-a-good-claude-md
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  - https://code.claude.com/docs/en/best-practices
  - https://www.trychroma.com/research/context-rot
related:
  - docs/context/context-rot-and-window-degradation.context.md
  - docs/context/agent-facing-document-structure.context.md
  - docs/context/agent-context-file-quality-over-completeness.context.md
  - docs/context/prompt-design-principles-framing-and-emphasis.context.md
  - docs/research/2026-04-11-prompting-techniques-model-tiers.research.md
---
Instruction capacity is finite, model-dependent, and already partially consumed before you write a single line. Shorter, higher-signal context files strictly outperform comprehensive ones because instruction quality degrades as count increases.

## The Capacity Ceiling

Jaroslawicz et al. (2025) identified three distinct degradation archetypes across model architectures:

- **Threshold-decay models** (o3, Gemini 2.5 Pro): maintain near-perfect instruction following up to ~150-200 instructions, then collapse
- **Linear-decay models** (Claude Sonnet): degrade uniformly from instruction #1 — every instruction added reduces compliance with all instructions
- **Exponential-decay models** (smaller models): catastrophic degradation with modest instruction counts

Even the best frontier models achieve only 68% accuracy at 500 instructions. Claude Code's built-in system prompt already consumes approximately 50 instructions of this budget before any CLAUDE.md is loaded.

## The "Less Is More" Test

For every line in a context file, ask: "Would removing this cause the model to make mistakes?" If not, cut it. The degradation is uniform — adding low-value instructions degrades compliance with high-value ones. Every instruction competes with every other.

When a rule is consistently ignored, the file is probably too long. "Claude ignores half of it because important rules get lost in the noise."

## Practical Sizing Guidance

These are practitioner heuristics, not empirically derived thresholds — but they align with the capacity ceiling research:

- CLAUDE.md: under 200-300 lines; production examples run under 60 lines
- SKILL.md: under 500 lines before splitting into reference files
- Agent-facing files: max ~8,000 characters per file
- Reference files per directory: ~100 lines before hierarchical organization

The creator of Claude Code uses approximately 100 lines. HumanLayer's production CLAUDE.md is under 60 lines.

## What to Include vs. Exclude

**Include:** Bash commands the model cannot guess, code style rules differing from defaults, testing instructions and preferred test runners, architectural decisions specific to the project, developer environment quirks, common gotchas, repository etiquette.

**Exclude:** Standard language conventions the model already knows, anything derivable from reading code, lintable style rules ("never send an LLM to do a linter's job"), task-specific instructions (store separately), information that changes frequently, file-by-file codebase descriptions.

## Emphasis Markers Have a Cost

"IMPORTANT" and "YOU MUST" improve adherence on critical instructions, but Claude 4.6 is more responsive to system prompts than earlier versions — aggressive emphasis causes overtriggering. "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'" Dial back emphasis for newer frontier models.

## Progressive Disclosure

Skill and instruction files beyond ~500 lines should split into reference files loaded on demand. Every token competes with conversation history. Reference files should link directly from the main file (one level deep) to ensure complete reads. This is the structural solution to the capacity ceiling: don't front-load everything, load it just-in-time.

## Evidence Grounding for the Key Thresholds

The 200–300 line threshold for CLAUDE.md/skill instruction files is T4 practitioner consensus — derived from production observation, not controlled study. No academic paper establishes tier-differentiated instruction line count thresholds; the research literature addresses context length in tokens, not instruction lines as a discrete unit. The directional finding that smaller models degrade faster than larger ones is research-supported (Chroma Context Rot study, 18 models), but specific per-tier instruction counts ("Haiku can follow 100 instructions, Sonnet 150") are not grounded in T1 or T2 evidence. By contrast, Anthropic's 500-line SKILL.md limit is the only T2-grounded hard bound on skill instruction length. When presenting these thresholds, the 200–300 line heuristic should be described as conservative practitioner guidance; the 500-line limit should be described as the published official ceiling.
