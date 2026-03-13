---
name: Distillation Guidelines
description: Quality criteria for context files distilled from research — atomic, actionable, traceable, concise
stage: write
pipeline: distill
---

# Distillation Guidelines

## What Makes a Good Context File

A context file distilled from research should be:

1. **Atomic** — one concept per file (Zettelkasten principle)
2. **Actionable** — reader knows what to do after reading
3. **Traceable** — sources link back to evidence
4. **Concise** — 200-800 words targets optimal RAG retrieval
5. **Structured** — key insight top, detail middle, takeaway bottom
6. **Complete** — verified findings preserved without loss or dilution

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
