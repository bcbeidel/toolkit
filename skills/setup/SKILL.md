---
name: setup
description: >
  Initialize or update WOS project context. Use when starting a new project
  with WOS, setting up context structure, configuring project documentation,
  or re-run to verify and repair an existing setup. Idempotent — safe to
  run multiple times.
argument-hint: ""
user-invocable: true
references:
  - references/capture-workflow.md
---

# Init WOS

Initialize or update WOS project context. Idempotent — safe to re-run.

## Workflow

### 1. Check current state

Check which parts of the WOS structure already exist:

- `AGENTS.md` with WOS markers (`<!-- wos:begin -->` / `<!-- wos:end -->`)
- `### Preferences` subsection in the WOS-managed section
- Layout hint (`<!-- wos:layout: ... -->`) in the WOS section
- `CLAUDE.md` with `@AGENTS.md` reference
- `.gitignore`
- `README.md`
- Any existing `docs/` directory structure

Also check whether the repo is **empty** — no source files, no `README.md`,
no `.gitignore` beyond what WOS just created. If the repo is empty, steps
2.5–2.7 below will activate. If the repo already has content, skip them.

### 2. Choose layout pattern

If no layout hint exists in AGENTS.md, present the four layout patterns:

> "How would you like to organize your project documents?"
>
> 1. **Separated** — Group by artifact type: `docs/context/`, `docs/plans/`,
>    `docs/designs/`, `docs/research/`. Good for teams wanting clear separation.
> 2. **Co-located** — All artifacts for a feature live together:
>    `docs/{feature}/`. Good for feature-driven work.
> 3. **Flat** — Everything in `docs/`. Rely on file suffixes (`.plan.md`,
>    `.research.md`) to distinguish types. Good for small projects.
> 4. **None** — No initial directory structure. Build organically as you go.

Wait for user selection. Record the choice (used in step 4 for the layout hint).

Create initial directory structure based on selection:
- **separated**: Create `docs/context/`, `docs/plans/`, `docs/designs/`, `docs/research/`
- **co-located**: Create `docs/` only (subdirs created per-feature later)
- **flat**: Create `docs/`
- **none**: Skip directory creation

If a layout hint already exists, show it to the user and ask:
"Current layout: **[pattern]**. Want to change it?"

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
.worktrees/
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

Run: `python <plugin-scripts-dir>/reindex.py --root .`

This creates `_index.md` files in directories with managed documents and
updates the AGENTS.md areas table if AGENTS.md exists.

### 4. Update AGENTS.md

If `AGENTS.md` does not exist, create it with a `# AGENTS.md` heading.

Write the WOS-managed section between `<!-- wos:begin -->` / `<!-- wos:end -->`
markers. This section includes:
- Layout hint comment (`<!-- wos:layout: <pattern> -->`)
- Context navigation (dynamically generated from discovered document locations)
- Areas table
- File metadata format
- Document standards
- Preferences

The markers enable automated updates — never place WOS-managed content
outside them.

If markers already exist, the section is replaced with the latest version
(picking up any new areas, layout changes, or standards).

### 5. Preferences

Capture or review communication preferences.

**If no `### Preferences` subsection exists** in the WOS section:

Run the full capture workflow in `references/capture-workflow.md`:
1. Ask the freeform communication style question
2. Map response to dimensions
3. Confirm with user
4. Write to AGENTS.md via `python <plugin-scripts-dir>/update_preferences.py --root .`

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

- **Layout:** note the selected pattern
- **Created:** list any directories or files that were created
- **Updated:** note if AGENTS.md WOS section was refreshed
- **Preferences:** note if preferences were set or unchanged
- **CLAUDE.md:** note if pointer was added or already present
- **Onboarding:** note if `.gitignore`, `README.md` were created or skipped
- **Next step:** note the suggested skill sequence, if any
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "WOS is up to date. No changes needed."
