---
name: setup
description: >
  Initialize or update project context. Use when starting a new project,
  setting up context structure, configuring project documentation,
  or re-run to verify and repair an existing setup. Idempotent — safe to
  run multiple times.
argument-hint: "[project root — defaults to CWD]"
user-invocable: true
references:
  - references/capture-workflow.md
  - references/working-agreements-capture.md
---

# Wiki Setup

Initialize or update project context. Idempotent — safe to re-run.

> **Legacy markers auto-migrate.** If AGENTS.md still uses the pre-rename
> `<!-- wos:begin -->` / `<!-- wos:end -->` / `<!-- wos:layout: ... -->`
> markers, this skill rewrites them to `<!-- wiki:* -->` in place. No
> user action is required beyond re-running `/wiki:setup`.

## Workflow

### 1. Check current state

Check which parts of the project structure already exist:

- `AGENTS.md` with managed-section markers (`<!-- wiki:begin -->` /
  `<!-- wiki:end -->`; legacy `<!-- wos:* -->` markers auto-migrate)
- `### Preferences` subsection in the managed section
- Layout hint (`<!-- wiki:layout: ... -->`) in the managed section
- `CLAUDE.md` with `@AGENTS.md` reference
- `.gitignore`
- `README.md`
- Any existing `docs/` directory structure

Also check whether the repo is **empty** — no source files, no `README.md`,
no `.gitignore` beyond what this skill just created. If the repo is empty,
steps 2.5–2.7 below will activate. If the repo already has content, skip them.

### 2. Choose layout pattern

If no layout hint exists in AGENTS.md, present the four layout patterns:

> "How would you like to organize your project documents?"
>
> 1. **Separated** — Group by artifact type: `.context/`, `.plans/`,
>    `.designs/`, `.research/`, `.prompts/`. Dot-prefixed at repo root — easy to gitignore. Good for teams wanting clear separation.
> 2. **Co-located** — All artifacts for a feature live together:
>    `docs/{feature}/`. Good for feature-driven work.
> 3. **Flat** — Everything in `docs/`. Rely on file suffixes (`.plan.md`,
>    `.research.md`) to distinguish types. Good for small projects.
> 4. **None** — No initial directory structure. Build organically as you go.

Wait for user selection. Record the choice (used in step 4 for the layout hint).

Create initial directory structure based on selection:
- **separated**: Create `.context/`, `.plans/`, `.designs/`, `.research/`, `.prompts/` at repo root
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

Based on the response, suggest a concrete skill sequence:

- **Research-oriented** (exploring a domain, comparing options, investigating):
  `/wiki:research` → `/wiki:ingest`
- **Implementation-oriented** (building a feature, fixing something, clear goal):
  `/work:scope-work` → `/work:plan-work` → `/work:start-work`
- **Exploratory / unsure**:
  Start with `/work:scope-work` to clarify the problem space

If the user declines or skips, move on without suggesting.

### 2.8. Initialize wiki infrastructure

Create the wiki directory and required seed files if they do not exist:

1. Create the `wiki/` directory if missing.
2. Create `wiki/SCHEMA.md` from `references/wiki-schema-template.md` if missing.
3. Create `wiki/_index.md` with an empty page inventory if missing:

```markdown
# Wiki Index

| Page | Description | File |
|------|-------------|------|
```

Idempotent — skip any file that already exists. Never overwrite existing content.

### 3. Reindex

Run: `python3 <plugin-scripts-dir>/reindex.py --root .`

Creates `_index.md` files in each directory registered in the AGENTS.md
areas table. On first run (no areas registered yet), scans the `docs/`
subtree as a fallback. Also refreshes the AGENTS.md areas table,
preserving any human-written area descriptions.

### 4. Update AGENTS.md

If `AGENTS.md` does not exist, create it with a `# AGENTS.md` heading.

Write the managed section between `<!-- wiki:begin -->` / `<!-- wiki:end -->`
markers. This section includes:
- Layout hint comment (`<!-- wiki:layout: <pattern> -->`)
- Context navigation (dynamically generated from discovered document locations)
- Areas table
- File metadata format
- Document standards
- Preferences

The markers enable automated updates — never place managed content
outside them.

If markers already exist, the section is replaced with the latest version
(picking up any new areas, layout changes, or standards).

### 5. Preferences

Capture or review communication preferences.

**If no `### Preferences` subsection exists** in the managed section:

Run the full capture workflow in `references/capture-workflow.md`:
1. Ask the freeform communication style question
2. Map response to dimensions
3. Confirm with user
4. Write to AGENTS.md via `python3 <plugin-scripts-dir>/update_preferences.py --root .`

**If preferences already exist:**

Show the current settings to the user. Ask: "Want to change any of these?"
- If yes → re-run the capture workflow
- If no → move on

### 6. Working Agreements

Capture or skip per-project Working Agreements.

**If `has_working_agreements(content)` returns `True`** (section already
exists anywhere in AGENTS.md, inside or outside markers):

No-op. Skip this step entirely — do not prompt, do not diff, do not
overwrite.

**If no `## Working Agreements` section exists:**

Run the capture workflow in `references/working-agreements-capture.md`:

1. Show the seed list verbatim
2. Ask: adopt / edit / skip
3. On adopt or edit, append the section *after* the managed
   `<!-- wiki:end -->` marker (or at end of file if no markers
   present). Include a blank line before the heading.
4. On skip, write nothing.

The section is user-owned after the first write. The skill never
re-renders it.

### 7. CLAUDE.md pointer

If `CLAUDE.md` does not exist, create it with:

```markdown
@AGENTS.md
```

If `CLAUDE.md` exists but does not contain `@AGENTS.md`, add the reference
at the top of the file.

### 8. Report

Report what was done:

- **Layout:** note the selected pattern
- **Created:** list any directories or files that were created
- **Updated:** note if AGENTS.md managed section was refreshed (mention
  if legacy `wos:` markers were auto-migrated to `wiki:`)
- **Preferences:** note if preferences were set or unchanged
- **Working Agreements:** note if seed was adopted, edited, skipped, or already present
- **CLAUDE.md:** note if pointer was added or already present
- **Onboarding:** note if `.gitignore`, `README.md` were created or skipped
- **Next step:** note the suggested skill sequence, if any
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "Project context is up to date. No changes needed."

## Key Instructions

- **Won't overwrite content outside managed markers** — only the section between `<!-- wiki:begin -->` / `<!-- wiki:end -->` is managed; content the user wrote outside these markers is never touched
- **Won't silently select a layout** — layout choice requires explicit user confirmation; no default is applied without asking

## Anti-Pattern Guards

1. **Running setup with uncommitted changes in the repo** — setup writes AGENTS.md and CLAUDE.md. Check for tracked modified files (`git diff --name-only HEAD`) before proceeding. Untracked-only changes are advisory — note them but do not block. If tracked modifications exist, warn the user: setup writes to AGENTS.md and CLAUDE.md, making the diff ambiguous and recovery harder if setup fails partway. Suggest `git stash` as remediation and wait for the user to decide whether to stash, continue anyway, or abort.
2. **Silent layout selection** — if no layout hint exists, always present the four layout options and wait for explicit selection. Applying a default layout without asking embeds a structural decision that is costly to reverse once docs have been created.
3. **Overwriting content outside managed markers** — only the section between `<!-- wiki:begin -->` and `<!-- wiki:end -->` markers is managed. Content written by the user outside these markers must not be touched. A full AGENTS.md rewrite is always wrong.
4. **Skipping the current-state check** — setup is idempotent, but it must check what already exists before writing. Presenting layout options when a layout hint already exists confuses the user; showing the current layout and asking if it should change is the correct flow.

## Handoff

**Receives:** Project root path (new or existing); optional communication preferences
**Produces:** Initialized project structure — AGENTS.md, docs/ directories, `_index.md` files
**Chainable to:** lint
