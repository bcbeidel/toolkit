---
name: skill-pair build brief
description: Intent and scope for the (retroactive) build of skill-pair
type: brief
related:
  - plugins/build/_shared/references/skill-pair-best-practices.md
---

## User ask (verbatim)

(retroactive) — capture intent for the existing skill-pair primitive
so its self-audit produces zero `warn` findings on the new
`brief-presence-and-content` dimension.

## So-what

`skill-pair` is the meta-pair every other primitive pair in the
toolkit derives from. Authors kept producing one half of a pair
(scaffolder OR auditor) and forgetting the other, leaving dangling
rubrics or unenforced principles. The skill-pair primitive locks
both halves to a single distilled principles doc so creation and
review never drift, and its registration in `primitive-routing.md`
makes new pairs discoverable rather than grep-only.

## Scope boundaries

- In: `skill-pair` primitive (the build/check pair pattern + shared
  principles doc + audit-dimensions + repair-playbook + routing-doc
  registration).
- Out: single-skill scaffolds (handled by `/build:build-skill`),
  single-SKILL.md audits (handled by `/build:check-skill`),
  Tier-1 deterministic scripts (delegated to script-builder skills
  per Language Selection in `primitive-routing.md`).

## Planned artifacts

- [x] `plugins/build/_shared/references/skill-pair-best-practices.md`
- [x] `plugins/build/skills/build-skill-pair/SKILL.md`
- [x] `plugins/build/skills/check-skill-pair/SKILL.md`
- [x] `plugins/build/skills/check-skill-pair/references/audit-dimensions.md`
- [x] `plugins/build/skills/check-skill-pair/references/repair-playbook.md`
- [x] `plugins/build/_shared/references/primitive-routing.md` registration

## Planned handoffs

- [x] `/build:check-skill-pair skill-pair` — pair-level integrity self-audit
- [x] `/build:check-skill` on each half — per-SKILL.md quality
- [x] `/build:check-python-script` on `audit_pair.py` — Tier-1 script audit

## Decisions log

- 2026-05-01 — retroactive brief authored to satisfy the new
  `brief-presence-and-content` audit dimension introduced in PR
  for issue #379. All checklists marked complete since the artifacts
  predate this brief.
