---
name: "Audit Validation Enhancements Design"
description: "Design for issues #132 (min word count warning) and #133 (skill instruction density reporting)"
related:
  - docs/research/2026-03-05-skill-density-threshold.md
---

# Audit Validation Enhancements Design

**Issues:** #132, #133
**Branch:** feat/132-133-audit-validation-enhancements
**PR:** TBD (pending review)

## Issue #132: Minimum Word Count Warning

### Problem

`check_content()` warns when context files exceed `max_words` (default 800)
but has no floor. Files with 10 words pass validation despite being too
short to provide useful context.

### Design

Add `min_words` parameter to `check_content()` in `wos/validators.py`.

- **Default:** 100 words
- **Severity:** `warn`
- **Scope:** Only `docs/context/` files (same as max check)
- **Excludes:** `_index.md` files (same as max check)
- **CLI flag:** `--context-min-words N` on `scripts/audit.py`

Mirrors the existing max check — same function, same exclusions, same
pattern.

## Issue #133: Skill Instruction Density Reporting

### Problem

No visibility into skill instruction density. The research skill at ~5,750
words across 9 files is the largest, but there is no mechanism to detect
when skills approach degradation thresholds.

### Design

#### Metric: Instruction Lines

Count non-empty, non-structural lines after frontmatter stripping. This
is a closer proxy to "number of directives" than raw word count, aligning
with Claude Code's own documented guidance of 200 lines per instruction
file.

**Structural lines (excluded from count):**

- Blank lines
- Headers (`#`)
- Code fences (`` ``` ``)
- Table separators (`|---|`)
- Horizontal rules (`---`, `***`, `___`)

**Instructional lines (counted):**

Everything else — bullets, table data rows, prose, numbered steps,
code block contents, XML tags with content.

#### Threshold: 200 Instruction Lines (Default, Configurable)

- **CLI flag:** `--skill-max-lines N` overrides the default
- Default of 200 is anchored on Claude Code's documented guidance for
  instruction file size, not a hard empirical limit
- As models improve, the threshold can be raised
- Projects with legitimately complex skills can tune it up; projects
  wanting tighter discipline can tune it down
- Setting `--skill-max-lines 0` disables the threshold (summary table
  still prints)

**Research basis:**

- Claude Code docs recommend 200 lines per instruction file
  ([source](https://code.claude.com/docs/en/memory))
- Du et al. (2025) shows raw token count degrades performance
  independently of content
- IFScale shows more directives = worse compliance (directional support;
  units are incommensurable with skill instruction lines — IFScale
  constraints are single-keyword inclusions, not behavioral directives)

#### Reporting

Summary table always printed to stderr during audit (visibility even
below threshold). Breaks out SKILL.md lines vs. reference file lines.
Words reported alongside for secondary visibility.

```
Skill Instruction Density:
  research:       148 (SKILL) + 573 (refs) = 721 lines, 5750 words  [warn]
  refine-prompt:   62 (SKILL) + 173 (refs) = 235 lines, 2076 words  [warn]
  report-issue:    45 (SKILL) + 120 (refs) = 165 lines, 1061 words
  retrospective:   38 (SKILL) + 100 (refs) = 138 lines,  972 words
  audit:           96 (SKILL) +   0 (refs) =  96 lines,  731 words
  init:            42 (SKILL) +  59 (refs) = 101 lines,  671 words
  distill:         35 (SKILL) +  53 (refs) =  88 lines,  655 words
```

Threshold violations (`warn` severity) are added to the issues list.

#### Code Structure

**New module: `wos/skill_audit.py`**

Three functions:

- `strip_frontmatter(text: str) -> str` — remove YAML frontmatter
  (detect `---` fences at top, skip them)
- `count_instruction_lines(text: str) -> int` — count non-structural
  lines (5 exclusion checks, no regex, no imports)
- `check_skill_sizes(skills_dir: Path, max_lines: int = 200) -> tuple[list[dict], list[dict]]`
  — walk `skills/`, measure each skill (SKILL.md + references separately),
  return summary records and `list[dict]` issues for skills over threshold

**Called from `scripts/audit.py`** (not from `validate_project()`), since
it operates on `skills/` not `docs/`. Summary table printed to stderr,
threshold violations added to the issues list.

**Tests in `tests/test_skill_audit.py`:**

- `count_instruction_lines` — headers excluded, blank lines excluded,
  code fences excluded, table separators excluded, horizontal rules
  excluded, bullets counted, prose counted, table data rows counted
- `strip_frontmatter` — with frontmatter, without frontmatter,
  unclosed frontmatter
- `check_skill_sizes` — under threshold, over threshold, no skills dir,
  `_shared` excluded, configurable threshold, zero threshold disables
  warnings

## Decisions Log

| Decision | Rationale |
|----------|-----------|
| Instruction lines, not word count | Closer proxy to directives; aligns with Claude Code 200-line guidance |
| Words reported alongside | Du et al. shows raw size matters independently |
| 200 lines default (configurable) | Claude Code's own documented recommendation |
| `_shared` excluded from per-skill counts | Avoids double-counting shared references |
| New module `skill_audit.py` | Skills dir is a different concern from docs/ validation |
| Summary to stderr, issues to list | Visibility without polluting the issues list for healthy skills |
| IFScale not used for threshold | Constraints are single-keyword inclusions, incommensurable with behavioral skill instructions |
