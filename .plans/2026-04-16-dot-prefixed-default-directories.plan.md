---
name: Dot-Prefixed Default Document Directories
description: Update all skill files so the separated layout defaults to dot-prefixed root dirs, then migrate toolkit's own docs/ content to match.
type: plan
status: executing
branch: feat/297-dot-prefixed-default-dirs
related:
  - docs/designs/2026-04-16-dot-prefixed-default-directories.design.md
---

# Dot-Prefixed Default Document Directories

## Goal

Change every hardcoded `docs/<type>/` path reference in the plugin skill files
to `.<type>/` so the `separated` layout default produces gitignore-friendly
directories at the repo root. Migrate toolkit's own `docs/` content to match,
so toolkit ships as a working example of its own convention.

Users gain per-type gitignore control (`.plans/`, `.designs/`, `.research/`,
`.context/`, `.prompts/`) without any new layout options or migration logic.

## Scope

Must have:
- `wiki:setup` `separated` layout creates `.plans/`, `.designs/`, `.research/`,
  `.context/`, `.prompts/` — not `docs/` subdirs
- All skill save-path examples updated (`scope-work`, `plan-work`, `research`,
  `refine-prompt`)
- `work:plan-work` checks `.plans/` for overlapping plans
- `work:start-work` branch derivation strips `.plans/` prefix
- Commit message template in execution-guide updated to reference `.plans/`
- Toolkit `docs/` dirs migrated; AGENTS.md areas table and context navigation updated

Won't have:
- `wiki/` renamed (committed knowledge base, not ephemeral)
- Auto-migration for existing projects with `docs/` layout
- New layout options (`co-located`, `flat` unchanged)
- Changes to `wiki:ingest` or `wiki:lint` (reference `wiki/`, not `docs/`)

## Approach

Two chunks: first update all plugin skill files (text changes only, no Python),
then migrate toolkit's own `docs/` directories with `git mv` and update AGENTS.md.

Chunk 1 is pure text edits — no tests, no Python, verification is grep-based.
Chunk 2 is the toolkit migration — uses `git mv` for tracked files and `mv`
for any untracked files, followed by AGENTS.md edits.

## File Changes

**Chunk 1 — Plugin skill files**

| Action | File |
|--------|------|
| Modify | `plugins/wiki/skills/setup/SKILL.md` |
| Modify | `plugins/wiki/skills/research/SKILL.md` |
| Modify | `plugins/wiki/skills/research/references/frame.md` |
| Modify | `plugins/wiki/skills/research/references/resumption.md` |
| Modify | `plugins/wiki/skills/research/references/gather-and-extract.md` |
| Modify | `plugins/work/skills/scope-work/SKILL.md` |
| Modify | `plugins/work/skills/scope-work/references/spec-format-guide.md` |
| Modify | `plugins/work/skills/plan-work/SKILL.md` |
| Modify | `plugins/work/_shared/references/plan-format.md` |
| Modify | `plugins/work/skills/plan-work/references/examples/small-plan.md` |
| Modify | `plugins/work/skills/start-work/SKILL.md` |
| Modify | `plugins/work/skills/start-work/references/execution-guide.md` |
| Modify | `plugins/build/skills/refine-prompt/SKILL.md` |

**Chunk 2 — Toolkit migration**

| Action | File |
|--------|------|
| Modify | `AGENTS.md` |
| Move | `docs/plans/` → `.plans/` |
| Move | `docs/designs/` → `.designs/` |
| Move | `docs/research/` → `.research/` |
| Move | `docs/context/` → `.context/` |
| Move | `docs/prompts/` → `.prompts/` |

## Tasks

## Chunk 1: Update plugin skill files

### Task 1: Update `wiki:setup` — separated layout dirs

**Files:** `plugins/wiki/skills/setup/SKILL.md`

- [ ] Update the `separated` layout description (step 2) to list `.plans/`, `.designs/`,
  `.research/`, `.context/`, `.prompts/` instead of `docs/context/`, `docs/plans/`,
  `docs/designs/`, `docs/research/`
- [ ] Update the directory creation instruction for `separated` (step 2) to match
- [ ] Verify: `grep -n "docs/plans\|docs/designs\|docs/research\|docs/context" plugins/wiki/skills/setup/SKILL.md` returns no matches
- [ ] Commit: `chore(skill/setup): update separated layout to dot-prefixed root dirs (#297)`

### Task 2: Update `wiki:research` — save path and references

**Files:**
- `plugins/wiki/skills/research/SKILL.md`
- `plugins/wiki/skills/research/references/frame.md`
- `plugins/wiki/skills/research/references/resumption.md`
- `plugins/wiki/skills/research/references/gather-and-extract.md`

- [ ] In `SKILL.md`: change `docs/research/` → `.research/` in the Output Document Format
  section (separated layout path and the `related:` frontmatter example)
- [ ] In `frame.md`: change `docs/research/YYYY-MM-DD-<slug>.research.md` →
  `.research/YYYY-MM-DD-<slug>.research.md` (step 8)
- [ ] In `resumption.md`: change `docs/research/{date}-{slug}.research.md` →
  `.research/{date}-{slug}.research.md`
- [ ] In `gather-and-extract.md`: change `docs/research/YYYY-MM-DD-slug.research.md` →
  `.research/YYYY-MM-DD-slug.research.md`
- [ ] Verify: `grep -rn "docs/research" plugins/wiki/skills/research/` returns no matches
- [ ] Commit: `chore(skill/research): update save paths to .research/ (#297)`

### Task 3: Update `work:scope-work` — save path and spec format guide

**Files:**
- `plugins/work/skills/scope-work/SKILL.md`
- `plugins/work/skills/scope-work/references/spec-format-guide.md`

- [ ] In `SKILL.md`: change `docs/designs/YYYY-MM-DD-<name>.design.md` →
  `.designs/YYYY-MM-DD-<name>.design.md` (step 4 save location, step 6 produces line)
- [ ] In `spec-format-guide.md`: change `docs/context/relevant-file.md` →
  `.context/relevant-file.md` in the frontmatter example
- [ ] Verify: `grep -rn "docs/designs\|docs/context" plugins/work/skills/scope-work/` returns no matches
- [ ] Commit: `chore(skill/scope-work): update save paths to .designs/ (#297)`

### Task 4: Update `work:plan-work` — save path, check path, and references

**Files:**
- `plugins/work/skills/plan-work/SKILL.md`
- `plugins/work/_shared/references/plan-format.md`
- `plugins/work/skills/plan-work/references/examples/small-plan.md`

- [ ] In `SKILL.md`: change `docs/plans/` → `.plans/` in step 1 (check for overlapping plans),
  step 3 (separated save location), step 3 produces line, and the Output Format section
- [ ] In `plan-format.md`: change `docs/plans/YYYY-MM-DD-<feature-name>.plan.md` →
  `.plans/YYYY-MM-DD-<feature-name>.plan.md` and `docs/designs/YYYY-MM-DD-<topic>.design.md`
  → `.designs/YYYY-MM-DD-<topic>.design.md`
- [ ] In `small-plan.md`: change `docs/designs/2026-03-11-status-field.design.md` →
  `.designs/2026-03-11-status-field.design.md`
- [ ] Verify: `grep -rn "docs/plans\|docs/designs" plugins/work/skills/plan-work/ plugins/work/_shared/` returns no matches
- [ ] Commit: `chore(skill/plan-work): update save paths to .plans/ (#297)`

### Task 5: Update `work:start-work` — branch derivation and commit template

**Files:**
- `plugins/work/skills/start-work/SKILL.md`
- `plugins/work/skills/start-work/references/execution-guide.md`

- [ ] In `SKILL.md`: change `strip docs/plans/` → `strip .plans/` and update the branch
  derivation example: `docs/plans/2026-03-11-skill-workflow.plan.md` →
  `.plans/2026-03-11-skill-workflow.plan.md`
- [ ] In `execution-guide.md`: change `Plan: docs/plans/YYYY-MM-DD-feature-name.plan.md` →
  `Plan: .plans/YYYY-MM-DD-feature-name.plan.md` in the commit message template
- [ ] Verify: `grep -rn "docs/plans" plugins/work/skills/start-work/` returns no matches
- [ ] Commit: `chore(skill/start-work): update plan path prefix to .plans/ (#297)`

### Task 6: Update `build:refine-prompt` — save path

**Files:** `plugins/build/skills/refine-prompt/SKILL.md`

- [ ] Change `/docs/prompts/` → `.prompts/` in step 4 (offer to save) — both the
  description and the directory creation instruction
- [ ] Verify: `grep -n "docs/prompts" plugins/build/skills/refine-prompt/SKILL.md` returns no matches
- [ ] Commit: `chore(skill/refine-prompt): update save path to .prompts/ (#297)`

---

## Chunk 2: Migrate toolkit

### Task 7: Update AGENTS.md — areas table and context navigation

Depends on: none (can be done before or after the file moves)

**Files:** `AGENTS.md`

- [ ] Update the Context Navigation section: replace `docs/context/`, `docs/plans/`,
  `docs/prompts/`, `docs/research/` with `.context/`, `.plans/`, `.prompts/`, `.research/`
- [ ] Update the Areas table: replace `docs/context`, `docs/plans`, `docs/prompts`,
  `docs/research` with `.context`, `.plans`, `.prompts`, `.research`
- [ ] Verify: `grep -n "docs/context\|docs/plans\|docs/prompts\|docs/research" AGENTS.md`
  returns no matches
- [ ] Commit: `chore(agents): update areas table and navigation to dot-prefixed paths (#297)`

### Task 8: Migrate toolkit docs/ directories

Depends on: Task 7 (AGENTS.md should reflect new paths before migration commit)

**Files:** `docs/plans/`, `docs/designs/`, `docs/research/`, `docs/context/`,
`docs/prompts/` → `.plans/`, `.designs/`, `.research/`, `.context/`, `.prompts/`

- [ ] Move tracked files: `git mv docs/plans .plans && git mv docs/designs .designs &&
  git mv docs/research .research && git mv docs/context .context &&
  git mv docs/prompts .prompts`
- [ ] Move any untracked files not captured by `git mv`:
  `mv docs/designs/* .designs/ && mv docs/research/* .research/ 2>/dev/null; true`
- [ ] Confirm `docs/` is empty: `ls docs/` should show empty or only the directory itself
- [ ] Remove `docs/` if empty: `rmdir docs/`
- [ ] Verify: `ls .plans/ .designs/ .research/ .context/ .prompts/` — all five dirs present
  with content
- [ ] Verify: `test -d docs && echo "docs still exists" || echo "docs removed"` → `docs removed`
- [ ] Commit: `chore(toolkit): migrate docs/ to dot-prefixed root dirs (#297)`

---

## Validation

- [ ] `grep -rn "docs/plans\|docs/designs\|docs/research\|docs/context\|docs/prompts" plugins/` —
  returns no matches
- [ ] `ls .plans/ .designs/ .research/ .context/ .prompts/` — all five dirs present with content
- [ ] `test -d docs` — exits 1 (directory removed)
- [ ] `grep -n "docs/context\|docs/plans\|docs/prompts\|docs/research" AGENTS.md` — returns no matches
