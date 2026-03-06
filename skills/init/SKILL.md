---
name: init
description: >
  Initialize or update WOS project context. Use when starting a new project
  with WOS, or re-run to verify and repair an existing setup. Idempotent —
  safe to run multiple times.
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
- `AGENTS.md` with WOS markers (`<!-- wos:begin -->` / `<!-- wos:end -->`)
- `### Preferences` subsection in the WOS-managed section
- `CLAUDE.md` with `@AGENTS.md` reference

### 2. Create missing directories

Create any missing directories:

```
docs/
  context/
  research/
  plans/
```

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
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "WOS is up to date. No changes needed."
