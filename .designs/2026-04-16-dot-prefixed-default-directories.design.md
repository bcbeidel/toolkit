---
name: Dot-Prefixed Default Document Directories
description: Change default working-artifact directories from docs/<type>/ to .<type>/ at repo root so they are easy to gitignore; migrate toolkit itself to match.
type: design
status: draft
related:
  - docs/context/
---

# Dot-Prefixed Default Document Directories

## Purpose

Change the default working-artifact directories from `docs/<type>/` to `.<type>/` at the
repo root, so new projects using the `separated` layout get paths that are easy to gitignore
by default. Migrate toolkit itself to match the new convention.

Ephemeral working documents (plans, designs, research notes, context drafts, prompts) should
stay out of git history unless a team explicitly chooses to commit them. Dot-prefixed
directories at the repo root follow the established convention for tool-generated artifacts
(`.github/`, `.vscode/`) and make selective gitignoring straightforward.

## Behavior

`wiki:setup` `separated` layout creates: `.plans/`, `.designs/`, `.research/`, `.context/`,
`.prompts/` at repo root.

All skill save-path logic resolves `separated` to the new paths:

| Skill | New default save path |
|---|---|
| `work:scope-work` | `.designs/YYYY-MM-DD-<name>.design.md` |
| `work:plan-work` | `.plans/YYYY-MM-DD-<name>.plan.md` |
| `wiki:research` | `.research/YYYY-MM-DD-<slug>.research.md` |
| `build:refine-prompt` | `.prompts/` |

`work:start-work` branch derivation strips `.plans/` prefix (was `docs/plans/`).

`work:plan-work` checks `.plans/` for overlapping or related plans (was `docs/plans/`).

Toolkit's own `docs/` content moves to the new root dirs. AGENTS.md areas table and
context navigation updated to reflect new paths.

Existing projects with an old `docs/` layout are not touched. The
`<!-- wos:layout: separated -->` hint continues to work — `separated` now resolves to
the new paths.

## Components / Files Changed

| File | Change |
|---|---|
| `plugins/wiki/skills/setup/SKILL.md` | Update `separated` layout dir list |
| `plugins/wiki/skills/research/SKILL.md` | Update save path |
| `plugins/wiki/skills/research/references/frame.md` | Update path example |
| `plugins/wiki/skills/research/references/resumption.md` | Update path reference |
| `plugins/wiki/skills/research/references/gather-and-extract.md` | Update path reference |
| `plugins/work/skills/scope-work/SKILL.md` | Update save path |
| `plugins/work/skills/scope-work/references/spec-format-guide.md` | Update path example |
| `plugins/work/skills/plan-work/SKILL.md` | Update save path + check path |
| `plugins/work/_shared/references/plan-format.md` | Update path reference |
| `plugins/work/skills/plan-work/references/examples/small-plan.md` | Update example path |
| `plugins/work/skills/start-work/SKILL.md` | Update branch derivation strip prefix |
| `plugins/work/skills/start-work/references/execution-guide.md` | Update example path |
| `plugins/build/skills/refine-prompt/SKILL.md` | Update save path |
| `AGENTS.md` (toolkit) | Update areas table + context navigation |
| `docs/` → root dot-dirs (toolkit migration) | Move all five directories |

## Constraints

- `wiki/` is not renamed — it is a committed knowledge base, not an ephemeral artifact
- `co-located` and `flat` layouts are unchanged
- No auto-migration for existing projects that already have `docs/` paths
- Toolkit's `docs/` move is a single atomic commit — no history rewrite

## Acceptance Criteria

1. `wiki:setup` with `separated` creates `.plans/`, `.designs/`, `.research/`, `.context/`,
   `.prompts/` at repo root — not under `docs/`
2. `work:scope-work` saves designs to `.designs/YYYY-MM-DD-<name>.design.md`
3. `work:plan-work` saves plans to `.plans/YYYY-MM-DD-<name>.plan.md` and checks `.plans/`
   for overlapping plans
4. `wiki:research` saves to `.research/YYYY-MM-DD-<slug>.research.md`
5. `build:refine-prompt` saves to `.prompts/`
6. `work:start-work` derives branch name correctly from `.plans/` paths
7. Toolkit `docs/` dirs are empty or removed; content lives under `.plans/`, `.designs/`,
   `.research/`, `.context/`, `.prompts/`
8. Toolkit AGENTS.md areas table and context navigation reflect new paths
