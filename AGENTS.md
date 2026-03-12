# AGENTS.md

<!-- wos:begin -->
## Context Navigation

Each directory has an `_index.md` listing all files with descriptions.
- `docs/context/_index.md` -- all topic areas

Each `.md` file starts with YAML metadata (between `---` lines).
Read the `description` field before reading the full file.
Documents put key insights first and last; supplemental detail in the middle.

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
