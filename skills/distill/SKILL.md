---
name: distill
description: >
  Converts research artifacts into focused context documents. Use when the
  user wants to "distill research", "extract findings", "create context
  from research", "summarize research into context files", or
  "operationalize research".
argument-hint: "[path to research artifact]"
user-invocable: true
references:
  - references/distillation-guidelines.md
  - ../_shared/references/preflight.md
---

# Distill

Convert research artifacts into focused context files.

**Prerequisite:** Before running any `uv run` command below, follow the preflight check in the [preflight reference](../_shared/references/preflight.md).

## Workflow

### 1. Input

Accept a research artifact path from the user. If none provided, scan
`docs/research/` for the most recently modified `.md` file and confirm.

### 2. Analyze

Read the research document and identify discrete findings:
- Each finding should be a self-contained insight
- Note confidence level (HIGH, MODERATE, LOW) based on evidence strength
- Note evidence type (empirical, expert consensus, case study, theoretical)

### 3. Propose

Present a distillation plan as a table:

| # | Finding | Target Area | Filename | Words (est.) |
|---|---------|-------------|----------|--------------|
| 1 | Key finding one | docs/context/area/ | finding-one.md | ~400 |

User approves, edits, or rejects individual rows.

### 4. Generate

For each approved finding:

1. Write a 200-800 word context file with frontmatter:
   ```yaml
   ---
   name: [Concise title]
   description: [One-sentence summary]
   type: reference
   sources:
     - [Carry forward relevant URLs from research]
   related:
     - [Path to source research artifact]
     - [Path to other context file from this batch]
     - [Path to existing context file in the same area]
   ---
   ```

   Every distilled file should link to at least one sibling context file in
   `related:`, not just the source research document. When distilling a batch,
   include cross-references between thematically adjacent files.

2. Follow the document standards in AGENTS.md for structure, frontmatter,
   and word count guidance.

### 5. Integrate

1. Run `uv run <plugin-scripts-dir>/reindex.py --root .`
2. Update the source research artifact's `related:` field to link
   forward to the new context files
3. Run `uv run <plugin-scripts-dir>/audit.py --root . --no-urls` to verify

## Key Constraints

- **User controls granularity.** They pick which findings become standalone
  files vs. which get folded into existing files. Propose, don't decide.
- **Context files target 200-800 words.** This is advisory. If a finding
  needs more space, note it and proceed.
- **Carry forward sources.** Each context file should trace back to the
  original evidence via `sources:` URLs.
- **Bidirectional linking.** New files link to research via `related:`.
  Research links to new files via `related:`. Ask before modifying.
