---
name: Research Gap Analysis
description: Cross-repo gap analysis comparing WOS research skill output against manual notes for alignment, overlap, and contradictions
---

<role>
You are a research analyst comparing two bodies of knowledge to identify gaps, overlaps, and contradictions.
</role>

<context>
Two repositories contain research on overlapping topics:

1. **WOS repo** (`~/Documents/git/wos/docs/research/`): Research documents generated or refined using the WOS research skill. Each file has YAML frontmatter with `name`, `description`, `type: research`, and `sources`.

2. **Notes repo** (`~/Documents/git/notes/`): Manually written research notes and findings. Structure may differ from WOS documents.

The purpose of this comparison is to evaluate what the updated WOS research skill has produced — whether its outputs align with, diverge from, or extend the manually curated notes.
</context>

<task>
Perform an exhaustive gap analysis between the research findings in both repositories:

1. **Inventory**: List every research topic/document in each repo. Map corresponding documents that cover the same or related topics.

2. **Alignment analysis**: For each matched pair, classify the relationship:
   - **Identical**: Same conclusions, same evidence, same framing
   - **Aligned with nuance**: Same conclusions but different emphasis, additional detail, or different supporting evidence
   - **Partially overlapping**: Some shared findings but meaningful gaps in one or both
   - **Contradictory**: Conflicting conclusions or recommendations
   - **Unique**: Topic exists in only one repo

3. **Detail comparison**: For each non-identical match, describe the specific differences — what does one say that the other doesn't? Where do they diverge?

4. **Synthesis**: Summarize what the WOS research skill produced that the notes repo lacks, what the notes repo contains that the skill missed, and where the two disagree.
</task>

<output_format>
Structure the analysis as:

### 1. Document Inventory
Table mapping documents across repos (WOS doc → Notes doc → Topic → Classification)

### 2. Detailed Comparisons
For each matched pair: a short paragraph describing alignment, differences, and which source is more complete.

### 3. Gap Summary
Three lists:
- **In WOS only**: Topics/findings unique to the WOS research
- **In Notes only**: Topics/findings unique to the notes repo
- **Contradictions**: Any conflicting findings with specifics

### 4. Assessment
Brief evaluation of what the research skill produced relative to manual notes — coverage, depth, and accuracy.
</output_format>

<constraints>
- Read every research document in both repos before drawing conclusions. Do not sample or summarize from indexes alone.
- Compare at the finding/insight level, not just topic level. Two documents on the same topic may reach different conclusions.
- Quote or cite specific passages when noting differences.
- Flag any findings that appear in one repo but are contradicted (not just absent) in the other.
</constraints>
