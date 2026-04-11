---
name: audit-skill
description: >
  Audit an existing SKILL.md for quality issues. Use when the user wants
  to "audit a skill", "review a skill", "check skill quality", "find
  problems in a skill", or "improve a skill".
argument-hint: "[path/to/SKILL.md — omit to audit all skills]"
user-invocable: true
---

# Audit Skill

Audit one skill or all skills against ten research-backed quality criteria,
then offer an opt-in repair loop.

## Workflow

### 1. Determine Scope

- **Argument provided** — audit that single SKILL.md
- **No argument** — walk `skills/` and audit all non-`_shared` subdirectories

### 2. Run Static Checks

```bash
python scripts/lint.py --root <project-root> --no-urls
```

Extract findings for the target skill(s). Static checks cover two of the
ten criteria (body length, ALL-CAPS density) and run deterministically —
always run these before LLM checks.

### 3. Run LLM Checks

For each skill, read the SKILL.md body and assess the remaining eight criteria:

**Structural checks:**

| # | Check | Pass condition |
|---|-------|---------------|
| 3 | Handoff completeness | `## Handoff` section present; all three fields populated (Receives / Produces / Chainable-to) |
| 4 | Anti-pattern guards | `## Anti-Pattern Guards` section present with at least one guard |
| 5 | Gate checks | At least one explicit gate (user approval, lint verification, precondition) before a consequential step |
| 6 | Examples | At least one concrete example — illustrative invocation, sample output, or table row with a real case |
| 7 | Description routing quality | First sentence front-loads the primary trigger phrase; no second-person ("you can", "you should") or passive voice |

**Content-quality checks (from HIGH-evidence research anti-patterns):**

| # | Check | Pass condition |
|---|-------|---------------|
| 8 | Vagueness | Each rule produces a consistent decision; two developers reading it would make the same choice in the same situation |
| 9 | Removal test | Each significant rule would cause a mistake if removed; rules that restate model defaults or code-visible conventions are noise |
| 10 | Persona framing | No "act as X" or "you are a senior X expert" constructions; OpenSSF 2025 found persona framing reduces performance on the intended tasks |

**Note on directive density (check #2):** newer frontier models are more
responsive to normal prompting than earlier versions — aggressive emphasis
(must/never/always-style directives) causes overtriggering more than it
enforces compliance. Flag ≥3 per skill body as a warning, same as `scripts/lint.py`.

### 4. Report Findings

Output a findings table:

```
| File | Issue | Severity |
|------|-------|----------|
| skills/foo/SKILL.md | Missing ## Handoff section | warn |
```

Summary line at top and bottom: `N fail, N warn` across N skills.
Sort: fail before warn; structural (checks 3–7) before content-quality (8–10).

### 5. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding:
1. Read the relevant section of the SKILL.md
2. Propose a minimal specific edit — fix the finding without restructuring surrounding content
3. Show the diff
4. Write the change only on user confirmation
5. Re-run `scripts/lint.py` after each applied fix

## Anti-Pattern Guards

1. **Running LLM checks before `scripts/lint.py`** — static checks are deterministic and fast; always run them first
2. **Applying all fixes at once** — per-change confirmation is required; bulk application removes the user's ability to review individual changes
3. **Auditing `skills/_shared/`** — this directory holds shared references, not invocable skills; exclude it from all-skill audits

## Handoff

**Receives:** Path to a SKILL.md (or no argument for all-skills audit)
**Produces:** Structured findings table in `scripts/lint.py` format (file, issue, severity); optionally, targeted edits applied to the audited skill(s)
**Chainable to:** build-skill (to create a replacement), execute-plan (for bulk repair across skills)

## Key Instructions

- Exclude `skills/_shared/` from all-skill audits
- Do not modify `wos/skill_audit.py` — the static checks are authoritative; this skill adds LLM-level judgment on top
- When proposing edits, keep changes minimal — fix the finding without restructuring surrounding content
- Checks 8 and 9 (vagueness, removal test) are the highest-value content-quality checks; prioritize surfacing them clearly
