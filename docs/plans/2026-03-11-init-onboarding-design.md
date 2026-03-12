---
name: Init Onboarding Enhancement
description: Extend wos:init to guide new-repo onboarding with .gitignore, README.md, and first-action suggestion
type: design
status: approved
related:
  - skills/init/SKILL.md
---

# Init Onboarding Enhancement

## Purpose

Extend `wos:init` to bootstrap empty repos with `.gitignore`, `README.md`,
and a guided first-action suggestion — so users land in a productive state,
not just a scaffolded one.

## Behavior

After creating missing directories (step 2), init checks if the repo looks
empty (no `README.md`, no `.gitignore`, no source files beyond what WOS just
created). If empty, offers three optional steps in sequence. Each is
skippable. If the repo is not empty, these steps are skipped entirely —
existing behavior unchanged.

### Step 2.5 — `.gitignore`

If no `.gitignore` exists, offer to create one with Python defaults:

- `.venv/`
- `__pycache__/`
- `*.pyc`
- `dist/`
- `*.egg-info/`
- `.eggs/`
- `.mypy_cache/`
- `.ruff_cache/`
- `.pytest_cache/`
- `.env`

User can accept, modify, or skip.

### Step 2.6 — `README.md`

If no `README.md` exists, ask "What is this project?" (one question).
Generate a stub with project name, one-line description, and placeholder
sections (Overview, Getting Started, Usage). User can accept, modify,
or skip.

### Step 2.7 — Guided first action

Ask "What problem are you trying to solve?" Based on the answer, suggest
a concrete skill sequence:

- **Research-oriented** — `brainstorm` then `research` then `distill`
- **Implementation-oriented** — `brainstorm` then `write-plan` then `execute-plan`
- **Exploratory/unsure** — `brainstorm` to start

## Constraints

- All three steps gated on user confirmation
- Non-empty repos unaffected
- No new scripts, no new reference files
- `.gitignore` assumes Python defaults
