---
name: resolver build brief
description: Intent and scope for the (retroactive) build of the resolver primitive pair
type: brief
related:
  - plugins/build/_shared/references/resolver-best-practices.md
---

## User ask (verbatim)

(retroactive) — capture intent for the existing resolver primitive
pair (`build-resolver` + `check-resolver`) so its self-audit
produces zero `warn` findings on the new
`brief-presence-and-content` dimension.

## So-what

Filing conventions in this repo were tribal knowledge — researchers
filed into `.context/`, plans landed in `.designs/`, prompts ended
up wherever. AGENTS.md tried to capture filing rules but couldn't
keep up as new directories accreted. The resolver pair makes
filing rules first-class: a machine-managed `RESOLVER.md` derives
the filing table from disk scan, a context table bundles
recurring-task doc loads, and `.resolver/evals.yml` proves the
routing works (positive and negative cases). The audit half catches
dark capabilities (directories not classified) and managed-region
drift before they cause filing decisions to silently go wrong.

## Scope boundaries

- In: `resolver` primitive — `RESOLVER.md` at a repo-or-target root
  with managed-region markers, sibling `.resolver/evals.yml`, and an
  AGENTS.md pointer line. Audit dimensions cover Tier-1
  deterministic checks (pointer presence, path resolution, marker
  integrity, eval parsing), Tier-2 semantic dimensions (filing
  coverage, context actionability, eval representativeness, brief
  presence and content), and Tier-3 cross-artifact checks
  (dark-capability scan, mtime staleness, eval execution).
- Out: skill-dispatch routing (intent → which skill runs; handled by
  SKILL.md `description`), per-skill `_shared/references/` wiring
  hygiene, nested-resolver delegation rules beyond depth 1–2.

## Planned artifacts

- [x] `plugins/build/_shared/references/resolver-best-practices.md`
- [x] `plugins/build/skills/build-resolver/SKILL.md`
- [x] `plugins/build/skills/check-resolver/SKILL.md`
- [x] `plugins/build/skills/check-resolver/references/audit-dimensions.md`
- [x] `plugins/build/skills/check-resolver/references/repair-playbook.md`
- [x] `plugins/build/skills/check-resolver/scripts/check_pointer.py`
- [x] `plugins/build/skills/check-resolver/scripts/check_resolver.py`
- [x] `plugins/build/skills/check-resolver/scripts/check_evals.py`
- [x] `plugins/build/_shared/references/primitive-routing.md` registration

## Planned handoffs

- [x] `/build:check-skill-pair resolver` — pair-level integrity
- [x] `/build:check-skill` on each half — per-SKILL.md quality
- [x] `/build:check-python-script` on the three Tier-1 scripts

## Decisions log

- 2026-05-01 — retroactive brief authored to satisfy the new
  `brief-presence-and-content` audit dimension introduced in PR
  for issue #379. All checklists marked complete since the artifacts
  predate this brief.
