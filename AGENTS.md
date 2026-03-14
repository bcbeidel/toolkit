# AGENTS.md

<!-- wos:begin -->
## Context Navigation

Each directory has an `_index.md` listing all files with descriptions.
- `docs/context/_index.md` -- Project context documents covering domain knowledge, patterns, and conventions.
- `docs/designs/_index.md` -- No active designs.
- `docs/plans/_index.md` -- No active plans.
- `docs/research/_index.md` -- research
- `skills/_shared/references/_index.md` -- references
- `skills/_shared/references/distill/_index.md` -- distill
- `skills/_shared/references/research/_index.md` -- research
- `skills/audit-wos/_index.md` -- audit-wos
- `skills/brainstorm/_index.md` -- brainstorm
- `skills/brainstorm/references/_index.md` -- references
- `skills/distill/_index.md` -- distill
- `skills/execute-plan/_index.md` -- execute-plan
- `skills/execute-plan/references/_index.md` -- references
- `skills/finish-work/_index.md` -- finish-work
- `skills/init-wos/_index.md` -- init-wos
- `skills/principles/_index.md` -- principles
- `skills/refine-prompt/_index.md` -- refine-prompt
- `skills/report-issue/_index.md` -- report-issue
- `skills/research/_index.md` -- research
- `skills/retrospective/_index.md` -- retrospective
- `skills/validate-work/_index.md` -- validate-work
- `skills/write-plan/_index.md` -- write-plan
- `skills/write-plan/references/_index.md` -- references
- `skills/write-plan/references/examples/_index.md` -- examples
- `tests/fixtures/research/_index.md` -- research

Each `.md` file starts with YAML metadata (between `---` lines).
Read the `description` field before reading the full file.
Documents put key insights first and last; supplemental detail in the middle.

### Areas
| Area | Path |
|------|------|
| Project context documents covering domain knowledge, patterns, and conventions. | docs/context |
| No active designs. | docs/designs |
| No active plans. | docs/plans |
| research | docs/research |
| references | skills/_shared/references |
| distill | skills/_shared/references/distill |
| research | skills/_shared/references/research |
| audit-wos | skills/audit-wos |
| brainstorm | skills/brainstorm |
| references | skills/brainstorm/references |
| distill | skills/distill |
| execute-plan | skills/execute-plan |
| references | skills/execute-plan/references |
| finish-work | skills/finish-work |
| init-wos | skills/init-wos |
| principles | skills/principles |
| refine-prompt | skills/refine-prompt |
| report-issue | skills/report-issue |
| research | skills/research |
| retrospective | skills/retrospective |
| validate-work | skills/validate-work |
| write-plan | skills/write-plan |
| references | skills/write-plan/references |
| examples | skills/write-plan/references/examples |
| research | tests/fixtures/research |

### File Metadata Format
```yaml
---
name: Title
description: What this covers
type: research       # optional
sources: []          # required if type is research
related: []          # optional, file paths from project root
---
```

### Document Standards

**Structure:** Key insights first, detailed explanation in the middle, takeaways at the bottom.
LLMs lose attention mid-document — first and last sections are what agents retain.

**Conventions:**
- Context files target 200-800 words. Over 800, consider splitting.
- One concept per file. Multiple distinct topics should be separate files.
- Link bidirectionally — if A references B in `related`, B should reference A.

### Preferences
- **Directness:** Be direct. State problems and disagreements plainly without hedging or softening.
- **Verbosity:** Keep responses concise. Skip preamble and unnecessary elaboration.
- **Depth:** Explain the reasoning and principles behind recommendations. Help me learn, not just execute.
<!-- wos:end -->
