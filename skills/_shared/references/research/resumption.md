---
name: Research Resumption
description: How to detect the current research phase from disk state after a context reset
stage: shared
pipeline: research
---

# Resuming After Context Reset

If `docs/research/{date}-{slug}.md` exists with `<!-- DRAFT -->`, read
it to determine the current phase:

- Has `sources:` in frontmatter but extracts missing for some sub-questions → resume at Phase 2 (pick up at the first sub-question without extracts)
- Has sources with updated statuses (verified/removed) but no tier annotations → resume at Phase 4
- Has tier annotations but no `## Challenge` section → resume at Phase 5
- Has `## Challenge` but no `## Findings` → resume at Phase 6
- Has `## Findings` but no `## Claims` → resume at Phase 7
- Has `## Claims` with `unverified` entries → resume at Phase 8
- Has `## Claims` fully resolved, still `<!-- DRAFT -->` → resume at Phase 9

Read the document fully to recover context before continuing.
