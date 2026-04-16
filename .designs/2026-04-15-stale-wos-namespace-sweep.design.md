---
name: Stale wos: Namespace Sweep
description: Replace all /wos:X skill invocations across plugins/ with correct /plugin:X namespaces
type: design
status: draft
related: []
---

# Stale wos: Namespace Sweep

## Purpose

The toolkit was migrated from a monolithic `wos` namespace to per-plugin
namespaces (`wiki:`, `work:`, `build:`). Skill SKILL.md files still contain
invocation references using the old `/wos:X` form. These produce wrong routing
at invocation time and mislead users reading the skills.

## Behavior

Each stale `/wos:X` reference is replaced with the correct `/plugin:X` form.
No logic changes — mechanical find-and-replace only.

## Replacement Mapping

| Old | New |
|-----|-----|
| `/wos:setup` | `/wiki:setup` |
| `/wos:research` | `/wiki:research` |
| `/wos:ingest` | `/wiki:ingest` |
| `/wos:scope-work` | `/work:scope-work` |
| `/wos:plan-work` | `/work:plan-work` |
| `/wos:start-work` | `/work:start-work` |
| `/wos:finish-work` | `/work:finish-work` |
| `/wos:check-work` | `/work:verify-work` |
| `/wos:build-skill` | `/build:build-skill` |
| `/wos:build-rule` | `/build:build-rule` |
| `/wos:build-hook` | `/build:build-hook` |
| `/wos:build-subagent` | `/build:build-subagent` |
| `/wos:check-hook` | `/build:check-hook` |
| `/wos:check-rule` | `/build:check-rule` |
| `/wos:check-subagent` | `/build:check-subagent` |
| `/wos:retrospective` | *(remove sentence)* |

## Files Affected

| File | Changes |
|------|---------|
| `plugins/wiki/skills/lint/SKILL.md` | `/wos:setup` ×3 |
| `plugins/wiki/skills/ingest/SKILL.md` | `/wos:research` ×1 |
| `plugins/wiki/skills/setup/SKILL.md` | `/wos:research`, `/wos:ingest`, `/wos:scope-work` ×2, `/wos:plan-work`, `/wos:start-work` |
| `plugins/work/skills/plan-work/SKILL.md` | `wos:scope-work` ×1, `/wos:start-work` ×1 |
| `plugins/work/skills/scope-work/SKILL.md` | `/wos:plan-work` ×1 |
| `plugins/work/skills/start-work/SKILL.md` | `/wos:check-work` ×2, `/wos:finish-work` ×1 |
| `plugins/work/skills/finish-work/SKILL.md` | `/wos:retrospective` — remove sentence |
| `plugins/build/skills/build-subagent/SKILL.md` | `/wos:build-skill` ×2 |
| `plugins/build/skills/check-subagent/SKILL.md` | `/wos:build-subagent` ×1 |
| `plugins/build/skills/check-rule/SKILL.md` | `/wos:check-rule` ×2 (self-references in header/examples) |
| `plugins/build/skills/build-hook/SKILL.md` | `/wos:build-skill`, `/wos:build-rule`, `/wos:check-hook` |
| `plugins/build/skills/check-skill-chain/SKILL.md` | `/wos:start-work`, `/wos:build-skill` |
| `plugins/build/skills/build-skill/SKILL.md` | `/wos:build-hook`, `/wos:build-rule`, `/wos:build-subagent` |
| `plugins/build/skills/build-rule/SKILL.md` | `/wos:build-hook`, `/wos:build-skill` |

## Out of Scope

- `<!-- wos:begin -->`, `<!-- wos:end -->`, `<!-- wos:layout: ... -->` — structural
  markers written into user AGENTS.md files. Renaming these breaks existing projects.
- Prose references to "WOS" as a product/system name (not invocations).

## Acceptance Criteria

- `grep -r "wos:" plugins/ --include="SKILL.md"` returns only structural marker
  references (`<!-- wos:begin -->`, `<!-- wos:end -->`, `<!-- wos:layout:`) — zero
  `/wos:X` skill invocations
- All 14 affected files read correctly with updated references
- No changes to skill logic, workflow steps, or non-invocation content
