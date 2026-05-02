---
name: help-skill build brief
description: Intent and scope for the build of the help-skill primitive pair (build-help-skill / check-help-skill)
type: brief
related:
  - https://github.com/bcbeidel/toolkit/issues/378
  - plugins/build/_shared/references/primitive-routing.md
  - plugins/build/_shared/references/skill-best-practices.md
  - plugins/build/_shared/references/readme-best-practices.md
---

## User ask (verbatim)

> Per-plugin help skill primitive — scaffold via new build-help-skill /
> check-help-skill pair. Give each toolkit plugin a `help` skill that orients
> a caller (agent or human) to what's in the plugin and how the skills compose
> — like `--help` for a CLI. Reachable as `/<plugin>:help` and as
> auto-triggered context when an agent asks "what's in this plugin / which
> skill fits". Build it as a primitive pair under `plugins/build/`, scaffolded
> via the existing `/build:build-skill-pair` meta-skill, so the four plugin
> instances stay consistent and auditable.

(Source: GitHub issue #378, edited 2026-05-02 to use precise primitive names
`build-help-skill` / `check-help-skill`.)

## So-what

Toolkit ships four plugins (`build`, `wiki`, `work`, `consider`) totalling 25+
skills. An agent or human entering one of those plugins cold has no in-plugin
landing page — they must grep `AGENTS.md`, scan `plugins/<x>/skills/`, or guess
which skill description matches their task. The Reddit `task-router` pattern
(global router skill + `UserPromptSubmit` hook reminding Claude to consult it)
solves the *post-compaction* version of this drift but at ~500 tokens/prompt
forever, with a hand-curated table that drifts from disk. A per-plugin
`help` skill is the *pull* alternative: on-demand (no token tax), scoped
(one description to triage, not 25), generated from disk (no drift), and
doubles as human UX (`/<plugin>:help` is a readable index). The pair codifies
the shape so all four plugin instances stay consistent and so future plugins
inherit the convention without re-inventing it.

## Scope boundaries

- **In:** A primitive-pair (`build-help-skill` + `check-help-skill`) under
  `plugins/build/`, sharing one distilled principles doc; produces a SKILL.md
  at `plugins/<plugin>/skills/help/SKILL.md` with a synopsis, disk-derived
  skill index, curated workflow chains, and entry-point pointers; auditor
  enforces coverage / freshness / fidelity (Tier-1) plus workflow curation,
  triage actionability, dual audience, scope discipline, and trigger quality
  (Tier-2).
- **Out:** A `UserPromptSubmit` hook that force-injects help every prompt
  (separate issue if drift proves real). A *global* router skill spanning
  plugins (per-plugin scoping is intentional; cross-plugin discovery lives
  in `AGENTS.md`). Auto-generating common-workflow chains (judgment, keep
  curated). Generating the four plugin `help` skills themselves (those
  follow this pair via `/build:build-help-skill` runs — separate work).

## Planned artifacts

- [x] `plugins/build/_shared/references/help-skill-best-practices.md`
- [x] `plugins/build/skills/build-help-skill/SKILL.md`
- [x] `plugins/build/skills/check-help-skill/SKILL.md`
- [x] `plugins/build/skills/check-help-skill/references/audit-dimensions.md`
- [x] `plugins/build/skills/check-help-skill/references/repair-playbook.md`
- [x] `plugins/build/_shared/references/primitive-routing.md` — append
      paragraph + Routing Test branch + route lines

## Planned handoffs

- [x] `/build:check-skill-pair help-skill` — pair-level integrity audit
      (clean after dropping `(WARN)` from playbook signal heading)
- [x] `/build:check-skill plugins/build/skills/build-help-skill/SKILL.md`
      (clean after fenced-block fix + D9 partition fix)
- [x] `/build:check-skill plugins/build/skills/check-help-skill/SKILL.md`
      (clean after fenced-block fix + D9 partition fix)
- [x] `/build:build-python-script` — produced
      `plugins/build/skills/build-help-skill/scripts/render_skill_table.py`
      (renders skill-index table from sibling frontmatter, stdlib-only)
- [x] `/build:check-python-script` (both scripts) — clean after
      `ruff format`; all 9 Tier-2 dimensions PASS; one INFO-level
      cross-entity duplication noted (acceptable per AGENTS.md
      "build scripts have no Python package")
- [x] `/build:build-python-script` (second invocation) — produced
      `plugins/build/skills/check-help-skill/scripts/check_help_skill.py`
      (~280 LOC; runs 19 Tier-1 deterministic checks, lint format,
      stdlib-only)

## Decisions log

- 2026-05-02 — primitive name finalized as `help-skill` (not `help`); chosen
  for parallelism with `build-readme` / `build-makefile` (named after artifact,
  not verb-object) and to avoid collision with the generic concept of "help".
- 2026-05-02 — routing-doc placement: **new top-level primitive class** under
  *What Each Primitive Was Designed For*. Rationale: a help-skill is a
  distinct artifact-typed sub-class of SKILL.md (like README is a sub-class
  of "markdown at repo root"), with its own scope concerns (orientation,
  triage, dual audience) that don't reduce to "a skill with these conventions."
  Treating it as a variant of `skill` would underweight what makes it
  distinct.
