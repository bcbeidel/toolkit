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
  - references/working-agreements-capture.md
license: MIT
---

# Wiki Setup

Initialize or update project context. Idempotent — safe to re-run.

> **Legacy markers auto-migrate.** If AGENTS.md still uses the pre-rename
> `<!-- wos:begin -->` / `<!-- wos:end -->` markers, this skill rewrites
> them to `<!-- wiki:* -->` in place. No user action is required beyond
> re-running `/wiki:setup`.

## Workflow

### 1. Check current state

Check which parts of the project structure already exist:

- `AGENTS.md` with managed-section markers (`<!-- wiki:begin -->` /
  `<!-- wiki:end -->`; legacy `<!-- wos:* -->` markers auto-migrate)
- `## Working Agreements` section (outside the markers)
- `CLAUDE.md` with `@AGENTS.md` reference

### 2. Update AGENTS.md

If `AGENTS.md` does not exist, create it with a `# AGENTS.md` heading.

Write the managed section between `<!-- wiki:begin -->` / `<!-- wiki:end -->`
markers. The managed section is intentionally minimal: a one-line pointer
to `RESOLVER.md` (when one exists) for directory-level routing.

Filing conventions and document standards are not encoded here —
projects that want them encode them in `RESOLVER.md` (routing) or
freeform sections of AGENTS.md (conventions). Project-wide behaviors
(workflow defaults, communication-style bullets) live in
`## Working Agreements` outside the markers (see Step 3).

The markers enable automated updates — never place managed content
outside them.

If markers already exist, the section is replaced with the latest
version.

### 3. Working Agreements

Capture or review the per-project `## Working Agreements` section. This
is the **single behavior section** — it covers both how the agent
collaborates on work (e.g., "Codify repetition") and any
communication-style bullets the user wants to add (e.g., "Be direct").

The seed is the **encouraged default** for every project. Show it; let
the user adopt, edit, or skip. Call `has_working_agreements(content)`
to pick the branch.

**If `has_working_agreements(content)` returns `False`** (section
absent):

Run the **Absent branch** in `references/working-agreements-capture.md`:

1. Show the seed list verbatim — `Codify repetition` and
   `Watch for patterns` are recommended for every project
2. Ask: adopt / edit / skip
3. On adopt or edit, append the section *after* the managed
   `<!-- wiki:end -->` marker (or at end of file if no markers
   present). Include a blank line before the heading.
4. On skip, write nothing.

**If `has_working_agreements(content)` returns `True`** (section
already exists anywhere in AGENTS.md, inside or outside markers):

Run the **Present branch** in `references/working-agreements-capture.md`:

1. Show the current section text verbatim
2. Ask: keep / edit / replace-with-seed
3. On keep, write nothing. On edit or replace, rewrite the existing
   section in place (same location, replacing the old content from
   the `## Working Agreements` heading through the next `##` heading
   or end of file).

The section is user-owned. The skill only writes what the user
approved in the current run.

### 4. CLAUDE.md pointer

If `CLAUDE.md` does not exist, create it with:

```markdown
@AGENTS.md
```

If `CLAUDE.md` exists but does not contain `@AGENTS.md`, add the reference
at the top of the file.

### 5. Resolver handoff

After scaffolding, decide whether the repo needs a `RESOLVER.md` and offer
the chain explicitly. This is the setup's last action.

1. **Skip silently** if `RESOLVER.md` already exists at the project root.
2. Otherwise, count top-level directories that contain ≥2 markdown files
   with valid YAML frontmatter. Ambient dirs (`.git`, `node_modules`,
   `.venv`, `dist`, `build`, etc.) are excluded.
3. **If the count meets the resolver threshold** (default 3; the user
   may pass a different threshold), prompt:

   > "This repo has N directories with markdown content
   > ({list}) but no `RESOLVER.md`. A resolver gives Claude a routing
   > table for filing new docs and loading context. Run
   > `/build:build-resolver` now? (yes / not yet / skip)"

   - **yes** — chain directly into `/build:build-resolver`. Do not
     re-run the working-agreements prompt.
   - **not yet / skip** — record the recommendation in the Report
     (Step 6) so the user can revisit it. Do not nag on subsequent
     re-runs once skipped within this session.
4. **If the count is below threshold**, do nothing. AGENTS.md alone
   suffices.

The default mirrors `/build:build-resolver`'s own primitive check
(`build-resolver/SKILL.md` Step 0). Both consult the same
`check_resolver_recommendation` helper in `wiki.project`, which accepts
a `threshold` argument — projects with different conventions can pass
their own value rather than relying on the default.

### 6. Report

Report what was done:

- **Created:** list any files that were created
- **Updated:** note if AGENTS.md managed section was refreshed (mention
  if legacy `wos:` markers were auto-migrated to `wiki:`)
- **Working Agreements:** note the outcome — adopted, edited, skipped (absent branch); kept, edited, replaced (present branch)
- **CLAUDE.md:** note if pointer was added or already present
- **Routing:** report the Step 5 outcome — resolver already present,
  threshold not crossed, chained into `/build:build-resolver`, or
  recommendation deferred
- **Already present:** note anything that was already in place

If everything was already set up, confirm: "Project context is up to date. No changes needed."

## Key Instructions

- **Won't overwrite content outside managed markers** — only the section between `<!-- wiki:begin -->` / `<!-- wiki:end -->` is managed; content the user wrote outside these markers is never touched

## Anti-Pattern Guards

1. **Running setup with uncommitted changes in the repo** — setup writes AGENTS.md and CLAUDE.md. Check for tracked modified files (`git diff --name-only HEAD`) before proceeding. Untracked-only changes are advisory — note them but do not block. If tracked modifications exist, warn the user: setup writes to AGENTS.md and CLAUDE.md, making the diff ambiguous and recovery harder if setup fails partway. Suggest `git stash` as remediation and wait for the user to decide whether to stash, continue anyway, or abort.
2. **Overwriting content outside managed markers** — only the section between `<!-- wiki:begin -->` and `<!-- wiki:end -->` markers is managed. Content written by the user outside these markers must not be touched. A full AGENTS.md rewrite is always wrong.
3. **Skipping the current-state check** — setup is idempotent, but it must check what already exists before writing.

## Handoff

**Receives:** Project root path (new or existing)
**Produces:** AGENTS.md with managed-region pointer to RESOLVER.md; CLAUDE.md with @AGENTS.md; optional `## Working Agreements` section
**Chainable to:** `/build:build-resolver` (when Step 5 detects threshold crossing without an existing resolver); `/wiki:lint` (audit content quality)
