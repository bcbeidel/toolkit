---
name: "Skill Instruction Density Threshold"
description: "Evidence-based default threshold for skill instruction density warnings — 200 instruction lines recommended, anchored on Claude Code documentation guidance, with IFScale and Du et al. as directional support"
type: research
sources:
  - https://arxiv.org/html/2507.11538v1
  - https://arxiv.org/abs/2510.05381
  - https://code.claude.com/docs/en/memory
related:
  - docs/research/2026-03-04-instructional-design.md
  - docs/plans/2026-03-06-audit-validation-enhancements-design.md
---

# Skill Instruction Density Threshold

## Summary

**Recommended default threshold: 200 instruction lines per skill
(configurable via `--skill-max-lines`).**

An "instruction line" is a non-empty, non-structural line after
frontmatter stripping — lines that carry directives, explanations, or
examples. Structural lines (headers, code fences, table separators,
horizontal rules, blank lines) are excluded.

The threshold is anchored on Claude Code's own documented guidance: "target
under 200 lines per CLAUDE.md file. Longer files consume more context and
reduce adherence." IFScale and Du et al. provide directional support but
measure different things (keyword-inclusion constraints and context padding,
respectively) — neither provides a directly transferable threshold number.

## Sub-Questions

1. What does IFScale tell us about instruction density limits?
2. What does Du et al. tell us about context length degradation?
3. What do existing tools use as size limits or warnings?
4. What is the current skill size distribution in WOS?
5. What metric best captures "instruction density"?

## Analysis

### IFScale: Directional Support Only (HIGH confidence in findings, LOW applicability)

The IFScale benchmark (Jaroslawicz et al., 2025) tested 20 frontier models
at 10 to 500 simultaneous **constraints**:

| Constraints | Accuracy | Implication |
|-------------|----------|-------------|
| 10 | 94-100% | Safe operating range |
| 100 | 94-98% | Reliable with careful design |
| 250 | 80-85% | Significant compliance gaps |
| 500 | 68% best | One-third of instructions missed |

**IFScale constraints are not skill instructions.** Each IFScale constraint
is a single-keyword inclusion directive (e.g., "Include the exact word:
'ESG'.") — approximately 8 words encoding a trivial check. Skill file
instructions are behavioral directives with conditional logic, structural
requirements, and workflow sequencing. A single skill instruction line may
be equivalent to multiple IFScale constraints in complexity.

The IFScale source code ([distylai/distylai.github.io](https://github.com/distylai/distylai.github.io/blob/main/src/runner.py))
confirms constraints are drawn from a 500-word business vocabulary and
formatted as a numbered list of keyword-inclusion rules.

**What transfers:** More simultaneous directives degrade compliance.
**What does not transfer:** Any specific threshold number. The units
(keyword inclusions vs. behavioral instructions) are incommensurable.

### Du et al.: Raw Size Degrades Performance (HIGH confidence)

Du et al. (2025, arXiv:2510.05381) proved that context length alone —
even whitespace padding with zero semantic content — degrades LLM
performance. Key findings:

- Open-source 7-8B models: measurable degradation at 3,750 tokens
  (~2,800 words), severe by 7,500 tokens
- Frontier models (GPT-4o, Gemini-2.0): minimal degradation even at
  30,000 tokens on most tasks
- Claude-3.5 Sonnet: anomalous -41.7% on MMLU at 7,500 tokens, but
  only 3-6% on other tasks

**What transfers:** Raw size matters independently of content quality.
Reporting word count alongside instruction lines captures this effect.
**What does not transfer:** Specific token thresholds — Du et al. pads
context around a task, not within instructions.

### Ecosystem Precedent: Claude Code's 200-Line Guidance

Survey of instruction size limits across the ecosystem:

| Platform | Limit | Unit | Type |
|----------|-------|------|------|
| **Claude Code CLAUDE.md** | **200** | **lines** | **documented recommendation** |
| Claude Code CLAUDE.md | 40,000 | characters | warning displayed |
| OpenAI Custom GPTs | 8,000 | characters | hard limit |
| Cursor | 500 | lines | community guidance |
| GitHub Copilot | 1,000 | lines | docs recommendation |
| GitHub Copilot code review | 4,000 | characters | silent truncation |
| Windsurf | 12,000 | characters | silent truncation |
| Amazon Bedrock Agents | 4,000 | characters | hard limit |
| PromptLayer | 2,000 | tokens | blog recommendation |

Claude Code's guidance is the most directly applicable: same ecosystem,
same tool type (instruction files loaded into context at session start),
same failure mode (reduced adherence as size increases). The 200-line
recommendation comes from Anthropic's own documentation, derived from
practitioner experience with Claude models.

Source: [How Claude remembers your project](https://code.claude.com/docs/en/memory)

### Metric: Instruction Lines, Not Word Count

Skill files contain a mix of structural formatting and actual directives.
Raw line count or word count conflates the two. Instruction lines
(non-empty, non-structural) isolate the content that the model must
attend to as directives.

**Structural lines excluded:**
- Blank lines (formatting)
- Headers (`#`) — organizational, not directive
- Code fences (`` ``` ``) — delimiters, not instructions
- Table separators (`|---|`) — formatting
- Horizontal rules (`---`) — formatting

**Rationale for excluding headers:** CLT research identifies well-structured
instructions as "germane load" (productive structure that aids
comprehension). Headers reduce cognitive load by organizing directives
into scannable sections. Counting them would penalize well-structured
skills.

Words are reported alongside instruction lines for secondary visibility,
capturing the Du et al. finding that raw size matters independently.

### Current WOS Skill Distribution

| Skill | Instruction Lines | Words | Files |
|-------|-------------------|-------|-------|
| research | ~721 | 5,750 | 9 |
| refine-prompt | ~235 | 2,076 | 3 |
| report-issue | ~165 | 1,061 | 3 |
| retrospective | ~138 | 972 | 2 |
| audit | ~96 | 731 | 1 |
| init | ~101 | 671 | 2 |
| distill | ~88 | 655 | 2 |

At 200 lines, two skills trigger: research (3.6x threshold) and
refine-prompt (1.2x threshold). The remaining five are comfortably below.

## Challenge

### Assumptions Check

| Assumption | Risk if Wrong |
|------------|---------------|
| Claude Code's 200-line guidance applies to skill files | Low — same ecosystem, same loading mechanism, same model |
| Instruction lines are a better proxy than words | Low — either metric catches the same skills; lines just exclude formatting noise |
| Structural line detection is accurate enough | Low — edge cases (XML tags, inline HTML) affect all skills equally |
| Reference files compound with SKILL.md | Medium — Claude Code may load references selectively in some cases |

### Premortem

- **Threshold too low:** refine-prompt (235 lines) barely triggers. If
  the skill is functional, the warning is noise. Mitigation: severity
  is `warn`, not `fail`. Threshold is configurable via `--skill-max-lines`.
- **Threshold too high:** Future skills creep to 190 lines without
  warning. Mitigation: summary table always prints, providing visibility
  even below threshold.
- **Metric gaming:** Authors could pack more content per line to stay
  under threshold. Mitigation: words reported alongside; obvious
  gaming is visible in the summary.

## Findings

1. **200 instruction lines is the recommended default (configurable).**
   (HIGH confidence) Anchored on Claude Code's own documented guidance
   for instruction file size. Catches the two known-heavy skills while
   leaving well-designed skills alone.

2. **Instruction lines, not words or raw lines, are the right metric.**
   (MODERATE confidence) Instruction lines exclude structural formatting,
   providing a cleaner measure of directive density. Words reported
   alongside for the secondary size effect.

3. **IFScale does not provide a transferable threshold.** (HIGH
   confidence) IFScale constraints are single-keyword inclusions, not
   behavioral directives. The "more = worse" direction transfers; no
   specific number does.

4. **The threshold must be configurable.** (HIGH confidence) Model
   capabilities improve over time, skill complexity varies by domain,
   and the 200-line anchor is practitioner guidance, not an empirical
   cliff. `--skill-max-lines N` allows tuning; `--skill-max-lines 0`
   disables warnings while preserving the summary table.

## Sources

| # | URL | Tier | Status |
|---|-----|------|--------|
| 1 | https://arxiv.org/html/2507.11538v1 | T3 | verified |
| 2 | https://arxiv.org/abs/2510.05381 | T3 | verified |
| 3 | https://code.claude.com/docs/en/memory | T1 | verified |

Pre-existing WOS research used as foundation:
- `docs/research/2026-03-04-instructional-design.md` (bcbeidel/notes)
- `docs/context/instructional-design/instruction-density-limits.md` (bcbeidel/notes)
- `docs/context/instructional-design/cognitive-load-in-instructions.md` (bcbeidel/notes)

Ecosystem survey (platforms checked):
- Claude Code, OpenAI Custom GPTs, Cursor, GitHub Copilot, Windsurf,
  Amazon Bedrock, Microsoft Copilot Studio, LangChain, LlamaIndex,
  PromptLayer, Humanloop, Braintrust, DSPy, Aider

## Search Protocol

| Query | Source | Found | Used |
|-------|--------|-------|------|
| (leveraged existing research from bcbeidel/notes) | github api | 3 | 3 |
| IFScale benchmark instruction density threshold | arxiv | 1 | 1 |
| IFScale constraint definition and source code | github | 1 | 1 |
| Du et al. context length alone hurts | arxiv | 1 | 1 |
| Chroma context rot research | web | 1 | 0 (no exact numbers published) |
| Skill/prompt size limits across AI tools ecosystem | web | 12 | 8 |
| Claude Code CLAUDE.md 200 lines recommendation | docs | 1 | 1 |
