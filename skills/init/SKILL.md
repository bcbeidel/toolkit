---
name: wos:init
description: >
  Initialize or update WOS project context. Use when starting a new project
  with WOS, or re-run to verify and repair an existing setup. Idempotent —
  safe to run multiple times.
argument-hint: ""
user-invocable: true
references:
  - ../_shared/references/preflight.md
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
format, document standards, and any existing preferences. The markers enable
automated updates — never place WOS-managed content outside them.

If markers already exist, the section is replaced with the latest version
(picking up any new standards or areas).

### 5. Report

Report what was done:

- **Created:** list any directories or files that were created
- **Updated:** note if AGENTS.md WOS section was refreshed
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "WOS is up to date. No changes needed."
