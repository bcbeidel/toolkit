---
name: build-skill
description: >
  Scaffold a new SKILL.md from a description and I/O contract. Use when
  the user wants to "create a skill", "add a skill", "build a skill",
  "scaffold a skill", "new skill for [X]", or "write a skill that does X".
argument-hint: "[skill name and description]"
user-invocable: true
---

# Build Skill

Scaffold a new, lint-passing SKILL.md from user intent.

## Workflow

### 1. Elicit

Gather before drafting anything:

| Field | What to ask |
|-------|------------|
| Name | Lowercase, hyphens only (e.g., `data-enricher`) |
| Description | What does the user say to trigger it? First sentence is the routing signal. |
| Receives | What input does this skill accept? |
| Produces | What does this skill write to disk? |
| Won't do | What should it explicitly refuse or skip? |
| Context files | Any `docs/context/` files to consult during drafting? |

If the user provided the skill name as an argument, use it — don't re-ask.

### 2. Read Context

Before drafting, read:
- `docs/context/instruction-file-authoring-anti-patterns.context.md`
- `docs/context/instruction-file-non-inferable-specificity.context.md`
- Any user-specified context files from step 1

### 3. Draft SKILL.md

Write the draft in conversation (not to disk yet). Required sections in order:

**Frontmatter:**
- `name:` — lowercase, hyphens only, under 64 chars, no reserved words (`anthropic`, `claude`)
- `description:` — first sentence front-loads the trigger phrase; Claude Code truncates at 250 chars, so the key use case must appear in the first sentence; imperative or trigger-phrase form, not second-person
- `argument-hint:` — one-line hint for the expected argument
- `user-invocable: true`

**Body (in order):**
1. One-sentence summary of what the skill does
2. `## Workflow` — numbered steps; each step is an observable outcome, not an implementation prescription
3. `## Anti-Pattern Guards` — at least one guard covering the most relevant failure modes
4. `## Handoff` — Receives / Produces / Chainable-to
5. `## Key Instructions` — only rules that pass the removal test: "Would removing this line cause a mistake?" Cut anything that fails

**Won't-have constraints** must appear explicitly in `## Key Instructions`. Missing negative rules leave scope undefined and are a documented anti-pattern — do not omit them.

**Avoid:**
- Persona framing (`"act as a senior X expert"`) — prefer specific rules; OpenSSF 2025 found persona framing reduces performance
- XML tags in body — use plain markdown
- Prescribing implementation details — state observable outcomes

### 4. Run Lint

```bash
python scripts/lint.py --root <project-root> --no-urls
```

Show any skill quality findings. Fix before writing to disk.

### 5. Present for Approval

Show the draft to the user. Iterate on feedback. Do not write the file until the user approves.

### 6. Write and Reindex

```bash
# Write to:
skills/<name>/SKILL.md

# Then reindex:
python scripts/reindex.py --root <project-root>
```

## Anti-Pattern Guards

1. **Writing to disk before lint** — verify the draft passes `scripts/lint.py` quality checks before writing
2. **Skipping elicitation** — guessing the I/O contract or won't-haves produces a skill that reflects the scaffolder's assumptions, not the user's intent
3. **Omitting won't-haves** — missing negative rules leave scope undefined; `## Key Instructions` must include at least one explicit exclusion
4. **Persona framing** — "act as a senior X expert" reduces quality on the tasks the persona intends to improve; write specific rules instead
5. **Description that buries the trigger phrase** — a description that front-loads capabilities ("Provides comprehensive support for...") will be misrouted; the first sentence is the routing signal

## Handoff

**Receives:** Skill name, description, I/O contract, and won't-haves from the user (via conversation or argument)
**Produces:** `skills/<name>/SKILL.md` that passes `scripts/lint.py` quality checks
**Chainable to:** audit-skill, execute-plan

## Key Instructions

- One skill per invocation — do not scaffold multiple skills in one pass
- Do not create `skills/<name>/references/` sub-files unless the SKILL.md body exceeds ~120 instruction lines
- Description must front-load the primary trigger phrase — routing truncates at 250 chars
- Do not modify `scripts/lint.py` thresholds to make the skill pass
