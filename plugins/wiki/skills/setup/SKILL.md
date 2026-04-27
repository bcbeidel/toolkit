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
- `## Working Agreements` section (outside the markers)
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

### 3. Update AGENTS.md

If `AGENTS.md` does not exist, create it with a `# AGENTS.md` heading.

Write the managed section between `<!-- wiki:begin -->` / `<!-- wiki:end -->`
markers. This section includes:
- Layout hint comment (`<!-- wiki:layout: <pattern> -->`)
- Context navigation (RESOLVER.md pointer + Glob/frontmatter discovery convention)
- File metadata format
- Document standards

Directory-level routing is owned by `RESOLVER.md`, not this section
(see [Step 6 — Resolver handoff](#6-resolver-handoff)). Project-wide
behaviors (workflow defaults like *Codify repetition*, communication-style
bullets) live in `## Working Agreements` outside the markers (Step 4).

The markers enable automated updates — never place managed content
outside them.

If markers already exist, the section is replaced with the latest version
(picking up any layout changes or standards updates).

### 4. Working Agreements

Capture or review the per-project `## Working Agreements` section. This
is the **single behavior section** — it covers both how the agent
collaborates on work (e.g., "Codify repetition") and any
communication-style bullets the user wants to add (e.g., "Be direct").
There is no separate Preferences capture flow.

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

### 5. CLAUDE.md pointer

If `CLAUDE.md` does not exist, create it with:

```markdown
@AGENTS.md
```

If `CLAUDE.md` exists but does not contain `@AGENTS.md`, add the reference
at the top of the file.

### 6. Resolver handoff

After scaffolding, decide whether the repo needs a `RESOLVER.md` and offer
the chain explicitly. This is the setup's last action on a non-empty repo.

1. **Skip silently** if `RESOLVER.md` already exists at the project root.
2. **Skip silently** if the repo is empty (steps 2.5–2.7 ran) — there are
   no filing dirs to route yet.
3. Otherwise, count top-level directories that follow a filing convention:
   ≥2 markdown files matching `*.context.md`, `*.plan.md`, `*.design.md`,
   or `*.research.md`. Ambient dirs (`.git`, `node_modules`, `.venv`,
   `dist`, `build`, etc.) are excluded.
4. **If the count is ≥3** (or there are ≥5 cross-skill reference docs
   worth bundling), prompt:

   > "This repo has N directories with filing conventions
   > ({list}) but no `RESOLVER.md`. A resolver gives Claude a routing
   > table for filing new docs and loading context. Run
   > `/build:build-resolver` now? (yes / not yet / skip)"

   - **yes** — chain directly into `/build:build-resolver`. Do not
     re-run the layout or working-agreements prompts.
   - **not yet / skip** — record the recommendation in the Report
     (Step 7) so the user can revisit it. Do not nag on subsequent
     re-runs once skipped within this session.
5. **If the count is below threshold**, do nothing — the project
   doesn't cross the primitive bar. AGENTS.md alone suffices.

The threshold mirrors `/build:build-resolver`'s own primitive check
(`build-resolver/SKILL.md` Step 0). Keep the two in sync — if the
threshold there changes, change it here.

### 7. Report

Report what was done:

- **Layout:** note the selected pattern
- **Created:** list any directories or files that were created
- **Updated:** note if AGENTS.md managed section was refreshed (mention
  if legacy `wos:` markers were auto-migrated to `wiki:`)
- **Working Agreements:** note the outcome — adopted, edited, skipped (absent branch); kept, edited, replaced (present branch)
- **CLAUDE.md:** note if pointer was added or already present
- **Onboarding:** note if `.gitignore`, `README.md` were created or skipped
- **Routing:** report the Step 6 outcome — resolver already present,
  threshold not crossed, chained into `/build:build-resolver`, or
  recommendation deferred
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
**Produces:** Initialized project structure — AGENTS.md (with RESOLVER pointer), docs/ directories, optional `wiki/` subtree
**Chainable to:** `/build:build-resolver` (when Step 7 detects threshold crossing without an existing resolver); `/wiki:lint` (audit content quality)
