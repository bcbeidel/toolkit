---
name: hook build brief
description: Intent and scope for the (retroactive) build of the hook primitive pair
type: brief
related:
  - plugins/build/_shared/references/hook-best-practices.md
---

## User ask (verbatim)

(retroactive) — capture intent for the existing hook primitive
pair (`build-hook` + `check-hook`) so its self-audit produces zero
`warn` findings on the new `brief-presence-and-content` dimension.

## So-what

CLAUDE.md instructions are advisory; the agent can argue around
them. Hooks are the deterministic enforcement layer — they fire on
specific lifecycle events (PreToolUse, PostToolUse, Stop, etc.)
regardless of LLM judgment. Authors kept conflating hooks with
permissions (`permissions.deny` is for unconditional blocks) and
with rules (`/build:build-rule` is for semantic-judgment file
content checks). The hook pair codifies when a hook is actually the
right primitive, the script anatomy that makes it auditable, and
the safety patterns (Stop loop guards, exit-code contract) that
prevent the most-cited failure modes.

## Scope boundaries

- In: `hook` primitive (event-driven script + settings.json entry,
  with the audit dimensions covering exit-code contract,
  async/blocking coherence, Stop-loop guards, injection safety, jq
  handling, shell hygiene).
- Out: `permissions.deny` rules (different primitive),
  `/build:build-rule` (semantic file-content checks),
  cross-platform hook portability (separate concern in
  platform-limitations.md).

## Planned artifacts

- [x] `plugins/build/_shared/references/hook-best-practices.md`
- [x] `plugins/build/skills/build-hook/SKILL.md`
- [x] `plugins/build/skills/check-hook/SKILL.md`
- [x] `plugins/build/skills/check-hook/references/audit-dimensions.md`
- [x] `plugins/build/skills/check-hook/references/repair-playbook.md`
- [x] `plugins/build/skills/check-hook/references/platform-limitations.md`
- [x] `plugins/build/_shared/references/primitive-routing.md` registration

## Planned handoffs

- [x] `/build:check-skill-pair hook` — pair-level integrity
- [x] `/build:check-skill` on each half — per-SKILL.md quality

## Decisions log

- 2026-05-01 — retroactive brief authored to satisfy the new
  `brief-presence-and-content` audit dimension introduced in PR
  for issue #379. All checklists marked complete since the artifacts
  predate this brief.
