# Skill Authoring Guide

How to write effective skills for Claude Code. This guide covers
structure, conventions, and quality criteria. It also serves as the
rubric when `/wos:audit-wos` evaluates skill quality.

## The Loading Model

Skills load progressively in three levels:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| L1: Metadata | Always (startup) | ~100 tokens | `name` + `description` from frontmatter |
| L2: Instructions | When triggered | <5K tokens | SKILL.md body |
| L3: Resources | As needed | Unbounded | Reference files, scripts, assets |

Only L1 is always in context. L2 loads when Claude decides the skill
is relevant — based entirely on the description. L3 loads only when
SKILL.md references a file and the task needs it.

## Required Frontmatter

Every SKILL.md starts with YAML frontmatter:

```yaml
---
name: my-skill-name
description: >
  Performs specific actions on target artifacts. Use when the user
  wants to "do X", "run Y", or "check Z".
argument-hint: "[optional hint for slash command input]"
user-invocable: true
references:
  - references/detailed-guide.md
---
```

### `name` (required)

- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Cannot contain "anthropic" or "claude"
- Should describe the action, not the target: `audit-wos` not `audit-documents`

### `description` (required)

The most important field. Claude uses it to decide whether to load
the skill from 100+ available skills. Must include:

1. **What** the skill does (lead with this)
2. **When** to use it (trigger phrases)

Conventions:
- Third person voice: "Converts research into..." not "You can use this to..."
- Maximum 1024 characters
- No XML tags
- Be specific — vague descriptions prevent discovery

**Good:**
```yaml
description: >
  Converts research artifacts into focused context documents. Use when
  the user wants to "distill research", "extract findings", or "create
  context from research".
```

**Bad:**
```yaml
description: Helps with documents
```

## SKILL.md Body

The body contains instructions Claude follows when the skill triggers.

### Size Limits

- **≤500 non-blank lines** in SKILL.md body
- **≤200 instruction lines** across SKILL.md + all references (configurable)
- If approaching either limit, split content into reference files

### Writing Style

- **Imperative voice:** "Read the document" not "The document should be read"
- **Consistent terminology:** Pick one term and use it throughout
- **No time-sensitive information**
- **Adapt to audience:** Consider the likely technical range of users.
  Briefly explain domain-specific terms (e.g., "assertion", "JSON")
  when context cues suggest the user may not know them. Don't
  over-explain for expert audiences.

### The Token-Earning Test

Every instruction should earn its place. Two questions to ask:

1. **"Does Claude already know this?"** — A paragraph explaining what
   PDFs are wastes tokens. A line showing which library to use earns
   its place.
2. **"Is this pulling its weight?"** — An instruction can be correct
   and still not help. If removing a section wouldn't change output
   quality, the section is dead weight. Lean skills outperform verbose
   ones because signal isn't diluted by noise.

### Freedom Matches Fragility

Match instruction specificity to how fragile the operation is:

| Fragility | Freedom | Example |
|-----------|---------|---------|
| High (exact sequence matters) | Low — exact commands | Database migrations, phase gates |
| Medium (preferred pattern) | Medium — pseudocode | Report generation with parameters |
| Low (many valid approaches) | High — general guidance | Code review, analysis |

## Reference Files

Additional files in `references/` that SKILL.md links to:

- **One level deep from SKILL.md** — Claude may partially read nested
  references. Never reference a file from another reference file.
- **Table of contents** for files >100 lines
- **Domain-organized** — split by topic, not by arbitrary size cuts
- File names should describe content: `source-evaluation.md` not `ref2.md`

## Examples Beat Explanations

One concrete example often replaces a paragraph of description. When
steering output format or depth, show an input/output pair rather than
describing the expected result.

Use `<example>` tags for examples in skill instructions. 3-5 diverse
examples is the sweet spot for output-sensitive skills.

## Canonical Example: `distill`

The `distill` skill demonstrates these conventions:

**Frontmatter:** Third-person description with trigger phrases, 63
instruction lines total (well under threshold).

**Body:** 5 sequential workflow phases, each 3-6 lines. High-freedom
for judgment calls (what to distill), low-freedom for integration
steps (exact `python` commands).

**Reference:** One file (`distillation-guidelines.md`) at 41 lines,
covering splitting heuristics and word count rationale.

**What makes it effective:**
- Every instruction earns its tokens — no explaining what "distill" means
- Freedom varies: user controls granularity (high), but integration
  runs exact commands (low)
- Concise constraints section uses bold keywords for scannability

## Evaluation Criteria

When evaluating a skill, check these criteria:

### Automated (Python — checked by `audit.py`)

| Check | Severity | Standard |
|-------|----------|----------|
| `name` format | fail | lowercase, hyphens, ≤64 chars |
| `name` reserved words | fail | no "anthropic" or "claude" |
| `description` length | warn | ≤1024 characters |
| `description` XML tags | warn | none present |
| `description` voice | warn | third person (no "you can", "I can") |
| SKILL.md body size | warn | ≤500 non-blank lines |
| Instruction density | warn | ≤200 instruction lines (configurable) |

### Judgment (Claude — guided by this document)

| Check | What to evaluate |
|-------|-----------------|
| Description triggers | Does it include both what + when? |
| Description breadth | Does it cast a wide enough net? Claude undertriggers — descriptions should be slightly "pushy", covering adjacent phrasings and contexts even when the user doesn't name the skill explicitly. |
| Freedom ↔ fragility | Do guardrail vs. guidance levels match the task? |
| Rationale over rigidity | Does the skill explain *why* behind instructions, or rely on rigid ALL-CAPS directives (MUST, NEVER, ALWAYS)? Explaining reasoning produces more intelligent adaptation than rigid commands. |
| Unnecessary context | Does the skill explain things Claude already knows? |
| Token-earning | Is every instruction pulling its weight, or could sections be removed without affecting output quality? |
| Generality | Is the skill written for broad use, or narrowly overfit to specific examples? Constraints should serve the general purpose, not patch individual test cases. |
| Examples quality | Are examples concrete and demonstrate expected depth? |
| Terminology consistency | Is vocabulary consistent throughout? |
| Reference depth | Are all references one level deep from SKILL.md? |
