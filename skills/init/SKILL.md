---
name: init
description: >
  Initialize or update WOS project context. Use when starting a new project
  with WOS, setting up context structure, configuring project documentation,
  or re-run to verify and repair an existing setup. Idempotent — safe to
  run multiple times.
argument-hint: ""
user-invocable: true
references:
  - ../_shared/references/preflight.md
  - references/capture-workflow.md
---

# Init WOS

Initialize or update WOS project context. Idempotent — safe to re-run.

**Prerequisite:** Before running any `uv run` command below, follow the
preflight check in the [preflight reference](../_shared/references/preflight.md).

## Workflow

### 1. Check current state

Check which parts of the WOS structure already exist:

- `docs/context/` directory
- `docs/research/` directory
- `docs/plans/` directory
- `docs/designs/` directory
- `AGENTS.md` with WOS markers (`<!-- wos:begin -->` / `<!-- wos:end -->`)
- `### Preferences` subsection in the WOS-managed section
- `CLAUDE.md` with `@AGENTS.md` reference
- `.gitignore`
- `README.md`

Also check whether the repo is **empty** — no source files, no `README.md`,
no `.gitignore` beyond what WOS just created. If the repo is empty, steps
2.5–2.7 below will activate. If the repo already has content, skip them.

### 2. Create missing directories

Create any missing directories:

```
docs/
  context/
  research/
  plans/
  designs/
```

### 2.5. `.gitignore` (empty repos only)

If the repo is empty and no `.gitignore` exists, offer to create one with
Python defaults:

```
.venv/
__pycache__/
*.pyc
dist/
*.egg-info/
.eggs/
.mypy_cache/
.ruff_cache/
.pytest_cache/
.env
```

Ask: "Want me to create a `.gitignore` with Python defaults? (yes / modify / skip)"

- **yes** — create the file as shown
- **modify** — ask what to add or remove, then create
- **skip** — move on

### 2.6. `README.md` (empty repos only)

If the repo is empty and no `README.md` exists, ask:

> "What is this project? (one sentence is fine)"

From the response, generate a stub `README.md` with:

- `# <Project Name>` heading
- One-line description
- Placeholder sections: Overview, Getting Started, Usage

Present the stub and ask: "Look good? (yes / modify / skip)"

### 2.7. Guided first action (empty repos only)

After scaffolding is complete, ask:

> "What problem are you trying to solve with this project?"

Based on the response, suggest a concrete WOS skill sequence:

- **Research-oriented** (exploring a domain, comparing options, investigating):
  `/wos:brainstorm` → `/wos:research` → `/wos:distill`
- **Implementation-oriented** (building a feature, fixing something, clear goal):
  `/wos:brainstorm` → `/wos:write-plan` → `/wos:execute-plan`
- **Exploratory / unsure**:
  Start with `/wos:brainstorm` to clarify the problem space

If the user declines or skips, move on without suggesting.

### 3. Reindex

Run: `uv run <plugin-scripts-dir>/reindex.py --root .`

This creates `_index.md` files in each directory and updates the AGENTS.md
areas table if AGENTS.md exists.

### 4. Update AGENTS.md

If `AGENTS.md` does not exist, create it with a `# AGENTS.md` heading.

Write the WOS-managed section between `<!-- wos:begin -->` / `<!-- wos:end -->`
markers. This section includes context navigation, areas table, file metadata
format, document standards, and preferences. The markers enable automated
updates — never place WOS-managed content outside them.

If markers already exist, the section is replaced with the latest version
(picking up any new standards or areas).

### 5. Preferences

Capture or review communication preferences.

**If no `### Preferences` subsection exists** in the WOS section:

Run the full capture workflow in `references/capture-workflow.md`:
1. Ask the freeform communication style question
2. Map response to dimensions
3. Confirm with user
4. Write to AGENTS.md via `uv run <plugin-scripts-dir>/update_preferences.py --root .`

**If preferences already exist:**

Show the current settings to the user. Ask: "Want to change any of these?"
- If yes → re-run the capture workflow
- If no → move on

### 6. CLAUDE.md pointer

If `CLAUDE.md` does not exist, create it with:

```markdown
@AGENTS.md
```

If `CLAUDE.md` exists but does not contain `@AGENTS.md`, add the reference
at the top of the file.

### 7. Report

Report what was done:

- **Created:** list any directories or files that were created
- **Updated:** note if AGENTS.md WOS section was refreshed
- **Preferences:** note if preferences were set or unchanged
- **CLAUDE.md:** note if pointer was added or already present
- **Onboarding:** note if `.gitignore`, `README.md` were created or skipped
- **Next step:** note the suggested skill sequence, if any
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "WOS is up to date. No changes needed."
