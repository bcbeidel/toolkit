---
name: Subagent Skills Gap Audit and Repair
description: Audits build-subagent and check-subagent SKILL.md files against the subagent context corpus, produces a gap table, and makes targeted minimum edits to close each gap.
---

<context>
You are auditing two Claude Code skills against a corpus of context documents
that document subagent mechanics, behavior, and failure modes. Your task is to
find gaps and make the minimum edits to close them.

Read all of the following files before beginning the assessment.

Research:
- docs/research/2026-04-13-claude-code-subagent-mechanics-cross-platform.research.md
- docs/research/2026-04-14-subagent-authoring-best-practices.research.md

Context:
- docs/context/claude-code-subagent-definition-format.context.md
- docs/context/claude-code-subagent-body-structure.context.md
- docs/context/claude-code-subagent-description-field-authoring.context.md
- docs/context/claude-code-subagent-invocation-and-routing.context.md
- docs/context/claude-code-subagent-invocation-prompt-design.context.md
- docs/context/claude-code-subagent-context-isolation-model.context.md
- docs/context/claude-code-subagent-permission-and-security-model.context.md
- docs/context/claude-code-subagent-tool-selection-strategy.context.md
- docs/context/claude-code-subagent-authoring-antipatterns.context.md
- docs/context/subagent-cross-platform-format-comparison.context.md
- docs/context/skill-mcp-tool-subagent-taxonomy.context.md

Skills to audit:
- skills/build-subagent/SKILL.md
- skills/check-subagent/SKILL.md
</context>

<task>
**Step 1: Gap assessment**

For each skill, identify where the skill's guidance contradicts documented
mechanics, or where the context corpus documents a non-obvious constraint or
failure mode that the skill does not address.

A gap qualifies when:
- The skill says X but the context says not-X (contradiction), or
- The context documents a non-obvious behavior, constraint, or failure mode
  that following the skill's instructions would cause an author to miss

Not a gap:
- The skill omits detail the context covers, but the omission wouldn't cause
  the author to produce a wrong or incomplete subagent
- Phrasing differences with no behavioral consequence

Output as a table:

| Skill | Section | Gap description | Context source |

**Step 2: Targeted edits**

For each gap in the table, make the minimum edit to close it. Edit the skill
files directly using file editing tools.

- Edit only what the gap assessment identified. Do not refactor, restructure,
  or clean up adjacent text.
- Preserve all existing section headings and formatting conventions.
- Do not add commentary or explanation beyond what the specific gap requires.
</task>

<output_format>
1. Gap assessment table (all gaps, both skills)
2. Apply edits directly to the files — do not print diffs
3. Summary — one paragraph per skill: what changed and which context source
   justified each change

Before writing the summary: verify every gap in the table has a corresponding
edit, and every edit traces back to a row in the gap table.
</output_format>

<constraints>
Edit only what the gap assessment justifies. Do not refactor.
</constraints>
