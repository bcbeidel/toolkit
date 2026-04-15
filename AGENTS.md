# AGENTS.md

<!-- wos:begin -->
## Context Navigation

- `docs/context/` -- Project context documents covering domain knowledge, patterns, and conventions.
- `docs/plans/` -- Implementation plans for toolkit features.
- `docs/prompts/` -- Saved and refined prompts for skill development and maintenance tasks.
- `docs/research/` -- Research investigations using the SIFT framework.

Each `.md` file starts with YAML metadata (between `---` lines).
Read the `description` field before reading the full file.
Documents put key insights first and last; supplemental detail in the middle.

### Plugin Structure

| Plugin | Path | Skills |
|--------|------|--------|
| `build` | `tools/build/` | `skill`, `rule`, `hook`, `subagent`, `refine-prompt` |
| `check` | `tools/check/` | `skill`, `rule`, `hook`, `subagent`, `skill-chain` |
| `wiki` | `tools/wiki/` | `setup`, `research`, `ingest`, `lint` |
| `work` | `tools/work/` | `scope`, `plan`, `start`, `verify`, `finish`, `audit`, `retro` |
| `consider` | `tools/consider/` | 16 mental models + meta |

Each plugin's skills live at `tools/<plugin>/skills/<name>/SKILL.md`.
Python packages: `tools/wiki/wiki/` and `tools/check/check/` (editable installs).
Shared scripts: `tools/wiki/scripts/`.

### Areas
| Area | Path |
|------|------|
| Project context documents covering domain knowledge, patterns, and conventions. | docs/context |
| Implementation plans for toolkit features. | docs/plans |
| Saved and refined prompts for skill development and maintenance tasks. | docs/prompts |
| Research investigations using the SIFT framework. | docs/research |

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
