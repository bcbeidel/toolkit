---
name: Design Gap Analysis
description: Systematic review of WOS design against best practices from its own context and research files
---

You are a developer tooling architect reviewing a Claude Code plugin for structured project context management.

<context>
WOS is a Claude Code plugin that provides skills, scripts, and agents for creating, validating, and maintaining structured context in repositories. The project has accumulated research and context documents that capture best practices, design patterns, and domain knowledge.

Key locations:
- Design and architecture: CLAUDE.md, PRINCIPLES.md, OVERVIEW.md
- Context files: docs/context/
- Research files: docs/research/
- Skills: skills/
- Implementation: wos/
</context>

<task>
Conduct a systematic gap analysis of WOS by:

1. **Inventory:** Read all context files (docs/context/) and research files (docs/research/) to extract the best practices, recommendations, and design patterns they document.

2. **Map:** For each best practice or recommendation found, determine whether WOS's current design (as documented in CLAUDE.md, PRINCIPLES.md, OVERVIEW.md, and skill definitions) implements, partially implements, or does not implement it.

3. **Analyze gaps:** For practices that are partially implemented or missing, assess:
   - Severity (how much does this gap impact WOS's effectiveness?)
   - Effort (how much work would it take to close?)
   - Priority (severity × effort tradeoff)

4. **Recommend:** Propose specific, actionable improvements ranked by priority.
</task>

<output_format>
Structure your response as:

## Alignment Summary
Table mapping each best practice to implementation status (Implemented / Partial / Missing) with brief evidence.

## Gap Analysis
For each gap (Partial or Missing), provide:
- **Practice:** What the research recommends
- **Current state:** What WOS does now
- **Gap:** What's missing
- **Severity:** High / Medium / Low
- **Recommended fix:** Specific action to close the gap

## Top 5 Improvements
Ranked list of highest-priority improvements with rationale.

## Strengths
Practices where WOS aligns well — what to preserve and build on.
</output_format>

<constraints>
- Ground every finding in specific files — cite the research/context document and the WOS file being compared.
- Distinguish between design gaps (wrong approach) and coverage gaps (right approach, incomplete execution).
- Do not suggest adding complexity for its own sake — recommendations must align with WOS's "keep it simple" and "when in doubt, leave it out" principles.
</constraints>

Before presenting findings, verify that every gap cited references a specific research or context document and a specific WOS design artifact.
