# AGENTS.md

<!-- wiki:begin -->
## Context Navigation

- `.context/` -- Project context documents covering domain knowledge, patterns, and conventions.
- `.plans/` -- Implementation plans for toolkit features.
- `.prompts/` -- Saved and refined prompts for skill development and maintenance tasks.
- `.research/` -- Research investigations using the SIFT framework.

Each `.md` file starts with YAML metadata (between `---` lines).
Read the `description` field before reading the full file.
Documents put key insights first and last; supplemental detail in the middle.

### Plugin Structure

| Plugin | Path | Skills |
|--------|------|--------|
| `build` | `plugins/build/` | `build-skill`, `build-rule`, `build-hook`, `build-subagent`, `refine-prompt`, `check-skill`, `check-rule`, `check-hook`, `check-subagent`, `check-skill-chain` |
| `wiki` | `plugins/wiki/` | `setup`, `research`, `ingest`, `lint` |
| `work` | `plugins/work/` | `scope-work`, `plan-work`, `start-work`, `verify-work`, `finish-work` |
| `consider` | `plugins/consider/` | 16 mental models + meta |

Each plugin's skills live at `plugins/<plugin>/skills/<name>/SKILL.md`.
Python package: `plugins/wiki/src/wiki/` (editable install).
Shared scripts: `plugins/wiki/scripts/`.

### Areas
| Area | Path |
|------|------|
| Project context documents covering domain knowledge, patterns, and conventions. | .context |
| Implementation plans for toolkit features. | .plans |
| Saved and refined prompts for skill development and maintenance tasks. | .prompts |
| Research investigations using the SIFT framework. | .research |

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
<!-- wiki:end -->

## Working Agreements

- **Codify repetition.** If something will happen again, do it manually
  once on 3–10 items and show the output. If I approve, codify into a
  skill, hook, or cron. The test: if I have to ask twice, you failed.
- **Watch for patterns.** When you notice recurring work across
  sessions, propose codifying it proactively — don't wait to be asked.
