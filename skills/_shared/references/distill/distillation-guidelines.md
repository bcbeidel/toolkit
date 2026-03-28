---
name: Distillation Guidelines
description: Quality criteria for context files distilled from research — atomic, actionable, traceable, concise
metadata:
  stage: write
  pipeline: distill
  tools: [Read, Write, Edit, Glob, Grep, Bash]
---

## Purpose
Quality criteria and constraints for context files distilled from research. Ensures files are atomic, actionable, traceable, and concise while carrying forward confidence levels and source attribution.

## Input

You receive via dispatch prompt:
- **Assigned findings** — specific findings to distill (from the approved mapping table)
- **Source research document paths** — where to read the full evidence
- **Target context file paths + areas** — where to write
- **Estimated word counts** — target length per file

# Distillation Guidelines

## What Makes a Good Context File

A context file distilled from research should be:

1. **Atomic** — one concept per file (Zettelkasten principle)
2. **Actionable** — reader knows what to do after reading
3. **Traceable** — sources link back to evidence
4. **Concise** — 200-800 words targets optimal RAG retrieval
5. **Structured** — key insight top, detail middle, takeaway bottom
6. **Complete** — verified findings preserved without loss or dilution

### Frontmatter Template

New context files use the `.context.md` compound suffix, which allows type
inference from the filename alone. Explicit `type: context` in frontmatter is
optional when using the compound suffix.

```yaml
---
name: [Descriptive title]
description: [One-sentence summary of the concept]
metadata:
  type: context
  sources:
    - [URLs carried forward from source research]
  related:
    - [source research document path]
    - [sibling context files from this batch]
---
```

## Splitting Heuristics

Split a finding into multiple files when:
- It covers more than one distinct concept
- Different aspects serve different audiences
- The finding has both a "what" and a "how" that are independently useful

Merge findings into a single file when:
- They're tightly coupled and don't make sense independently
- Combined they still fit under 800 words
- They serve the same audience with the same purpose

## Word Count Rationale

| Range | Use Case |
|-------|----------|
| <200 words | Too thin — probably needs more context or should be merged |
| 200-500 words | Ideal for focused reference files |
| 500-800 words | Good for explanatory context with examples |
| >800 words | Consider splitting — RAG retrieval degrades, attention loss risk |

## Confidence Mapping

When distilling, map research confidence levels to context file framing:

- **HIGH confidence** — state directly: "X works because Y"
- **MODERATE confidence** — qualify: "Evidence suggests X, based on Y"
- **LOW confidence** — flag: "Early evidence indicates X, but Z remains uncertain"

## Completeness Constraint

Accuracy and completeness are the primary constraints; document structure
is the goal. Verified findings must not be dropped or diluted to achieve
U-shape (key insight top, detail middle, takeaway bottom) or to meet
word count targets.

When a finding cannot fit the U-shape without information loss, preserve
the finding as-is. A complete but imperfectly structured file is better
than a well-structured file that silently dropped verified content.

Specifically:
- Every HIGH and MODERATE confidence finding from the source research
  must appear in the distilled output
- LOW confidence findings should be included with appropriate qualifying
  language, not omitted
- Confidence annotations must carry forward — do not upgrade a MODERATE
  finding to unqualified assertion during distillation
- If word count would exceed 800 words with all findings included,
  split into multiple files rather than cutting content

## Bidirectional Linking

Ensure all `related:` links are bidirectional:
- New context files link to their source research documents
- New context files link to sibling context files from the same batch
- If updating an existing context file, add the new `related:` link

## Reindex and Validate

```bash
python <plugin-scripts-dir>/reindex.py --root .
python <plugin-scripts-dir>/audit.py <file> --root . --no-urls
```

Run reindex to update `_index.md` files, then audit each written file.

## Output

Each context file must:
- Have valid frontmatter with `name`, `description`, `sources`, `related`
- Be 200-800 words (advisory — completeness takes priority)
- Pass audit validation
- Have bidirectional `related:` links

## Constraints

- Do not re-analyze the mapping — implement it as approved.
- Do not search for new sources (no WebSearch or WebFetch).
- Do not prompt the user for input.
