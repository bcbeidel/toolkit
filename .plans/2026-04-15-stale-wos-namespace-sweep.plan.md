---
name: Stale wos: Namespace Sweep
description: Replace all /wos:X skill invocations in plugins/ SKILL.md files with correct /plugin:X namespaces
type: plan
status: completed
branch: fix/stale-wos-namespace-sweep
related:
  - docs/designs/2026-04-15-stale-wos-namespace-sweep.design.md
---

# Stale wos: Namespace Sweep

## Goal

Replace every `/wos:X` skill invocation across all SKILL.md files with the
correct `/plugin:X` namespace. Fourteen files affected; one removal
(`/wos:retrospective`). No logic changes — mechanical find-and-replace only.

## Scope

Must have:
- All `/wos:X` invocations updated per the replacement mapping below
- `/wos:check-work` → `/work:verify-work` (skill was renamed, not just re-namespaced)
- Sentence invoking `/wos:retrospective` removed from `finish-work/SKILL.md`

Won't have:
- Changes to `<!-- wos:begin -->`, `<!-- wos:end -->`, `<!-- wos:layout: ... -->` structural markers
- Changes to prose that mentions "WOS" as a product/system name (non-invocation)
- Any changes to skill logic, workflow steps, or Python code

## Approach

Work plugin-by-plugin: wiki → work → build. Each chunk is a single commit.
All changes are in SKILL.md files only. The acceptance gate is a grep that
returns zero `/wos:` skill invocations across all SKILL.md files.

**Replacement mapping:**

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
| `/wos:retrospective` | *(remove sentence entirely)* |

## File Changes

- Modify: `plugins/wiki/skills/lint/SKILL.md`
- Modify: `plugins/wiki/skills/ingest/SKILL.md`
- Modify: `plugins/wiki/skills/setup/SKILL.md`
- Modify: `plugins/work/skills/plan-work/SKILL.md`
- Modify: `plugins/work/skills/scope-work/SKILL.md`
- Modify: `plugins/work/skills/start-work/SKILL.md`
- Modify: `plugins/work/skills/finish-work/SKILL.md`
- Modify: `plugins/build/skills/build-subagent/SKILL.md`
- Modify: `plugins/build/skills/check-subagent/SKILL.md`
- Modify: `plugins/build/skills/check-rule/SKILL.md`
- Modify: `plugins/build/skills/build-hook/SKILL.md`
- Modify: `plugins/build/skills/check-skill-chain/SKILL.md`
- Modify: `plugins/build/skills/build-skill/SKILL.md`
- Modify: `plugins/build/skills/build-rule/SKILL.md`

## Tasks

---

### Chunk 1: wiki plugin

---

### Task 1: Fix wiki/skills/lint/SKILL.md

Replace all three `/wos:setup` references with `/wiki:setup`.

**Occurrences (3):**
- Line ~120: `Offer to run /wos:setup to initialize`
- Line ~122: `Offer to run /wos:setup to add`
- Line ~161: `Use /wos:setup to initialize missing project structure`

- [ ] Replace all three `/wos:setup` → `/wiki:setup`
- [ ] Verify: `grep "wos:" plugins/wiki/skills/lint/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(wiki): update stale wos: invocations in lint skill`

---

### Task 2: Fix wiki/skills/ingest/SKILL.md

Replace one `/wos:research` reference with `/wiki:research`.

**Occurrence (1):**
- Line ~200: `Invoke /wos:research with the document to validate sources`

- [ ] Replace `/wos:research` → `/wiki:research`
- [ ] Verify: `grep "wos:" plugins/wiki/skills/ingest/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(wiki): update stale wos: invocations in ingest skill`

---

### Task 3: Fix wiki/skills/setup/SKILL.md

Replace six invocation references across the file.

**Occurrences (6):**
- `/wos:research` → `/wiki:research` (×1, line ~109)
- `/wos:ingest` → `/wiki:ingest` (×1, line ~109)
- `/wos:scope-work` → `/work:scope-work` (×2, lines ~111, ~113)
- `/wos:plan-work` → `/work:plan-work` (×1, line ~111)
- `/wos:start-work` → `/work:start-work` (×1, line ~111)

- [ ] Apply all six replacements
- [ ] Verify: `grep "wos:" plugins/wiki/skills/setup/SKILL.md` returns only structural marker lines (`<!-- wos:begin -->`, `<!-- wos:end -->`, `<!-- wos:layout: -->`) — zero `/wos:X` skill invocations
- [ ] Commit: `fix(wiki): update stale wos: invocations in setup skill`

---

### Chunk 2: work plugin

---

### Task 4: Fix work/skills/plan-work/SKILL.md

**Occurrences (2):**
- `wos:scope-work` → `/work:scope-work` (×1, line ~79, missing leading slash)
- `/wos:start-work` → `/work:start-work` (×1, line ~111)

- [ ] Apply both replacements
- [ ] Verify: `grep "wos:" plugins/work/skills/plan-work/SKILL.md` returns only structural marker lines — zero skill invocations
- [ ] Commit: `fix(work): update stale wos: invocations in plan-work skill`

---

### Task 5: Fix work/skills/scope-work/SKILL.md

**Occurrences (2):**
- `/wos:plan-work` → `/work:plan-work` (×1, line ~90)
- `<!-- wos:layout: ... -->` — structural marker, do NOT change

- [ ] Replace `/wos:plan-work` → `/work:plan-work`
- [ ] Verify: `grep "wos:" plugins/work/skills/scope-work/SKILL.md` returns only structural marker lines — zero skill invocations
- [ ] Commit: `fix(work): update stale wos: invocations in scope-work skill`

---

### Task 6: Fix work/skills/start-work/SKILL.md

**Occurrences (3):**
- `/wos:check-work` → `/work:verify-work` (×2, lines ~105, ~109) — note: skill was renamed
- `/wos:finish-work` → `/work:finish-work` (×1, line ~116)

- [ ] Apply all three replacements, using `/work:verify-work` (not `/work:check-work`)
- [ ] Verify: `grep "wos:" plugins/work/skills/start-work/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(work): update stale wos: invocations in start-work skill`

---

### Task 7: Fix work/skills/finish-work/SKILL.md

**Occurrences (2):**
- `/wos:retrospective` (×2, lines ~121, ~123) — remove the sentence(s) that invoke it

The two lines to remove are:
```
> "Work is integrated. Would you like to run a retrospective? Invoke `/wos:retrospective` to review this session."

Do not embed the retrospective workflow here — it lives in `/wos:retrospective`.
```

Remove the retrospective offer block entirely. The step should end after "After integration completes, offer:" with no follow-on content, or the step itself can be removed if it has no remaining content.

- [ ] Remove retrospective offer block
- [ ] Verify: `grep "wos:" plugins/work/skills/finish-work/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(work): remove stale wos:retrospective from finish-work skill`

---

### Chunk 3: build plugin

---

### Task 8: Fix build/skills/build-subagent/SKILL.md

**Occurrences (2):**
- `/wos:build-skill` → `/build:build-skill` (×2, lines ~39, ~224)

- [ ] Replace both occurrences
- [ ] Verify: `grep "wos:" plugins/build/skills/build-subagent/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in build-subagent skill`

---

### Task 9: Fix build/skills/check-subagent/SKILL.md

**Occurrences (1):**
- `/wos:build-subagent` → `/build:build-subagent` (×1, line ~234)

- [ ] Replace the occurrence
- [ ] Verify: `grep "wos:" plugins/build/skills/check-subagent/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in check-subagent skill`

---

### Task 10: Fix build/skills/check-rule/SKILL.md

**Occurrences (2):**
- `# /wos:check-rule` → `# /build:check-rule` (header, line ~11)
- `/wos:check-rule` in example (line ~121)

- [ ] Replace both occurrences
- [ ] Verify: `grep "wos:" plugins/build/skills/check-rule/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in check-rule skill`

---

### Task 11: Fix build/skills/build-hook/SKILL.md

**Occurrences (3):**
- `/wos:build-skill` → `/build:build-skill` (×1, line ~29)
- `/wos:build-rule` → `/build:build-rule` (×1, line ~31)
- `/wos:check-hook` → `/build:check-hook` (×1, line ~354)

- [ ] Apply all three replacements
- [ ] Verify: `grep "wos:" plugins/build/skills/build-hook/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in build-hook skill`

---

### Task 12: Fix build/skills/check-skill-chain/SKILL.md

**Occurrences (2):**
- `/wos:start-work` → `/work:start-work` (×1, line ~39)
- `/wos:build-skill` → `/build:build-skill` (×1, line ~60)

- [ ] Apply both replacements
- [ ] Verify: `grep "wos:" plugins/build/skills/check-skill-chain/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in check-skill-chain skill`

---

### Task 13: Fix build/skills/build-skill/SKILL.md

**Occurrences (3):**
- `/wos:build-hook` → `/build:build-hook` (×1, line ~67)
- `/wos:build-rule` → `/build:build-rule` (×1, line ~68)
- `/wos:build-subagent` → `/build:build-subagent` (×1, line ~69)

- [ ] Apply all three replacements
- [ ] Verify: `grep "wos:" plugins/build/skills/build-skill/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in build-skill skill`

---

### Task 14: Fix build/skills/build-rule/SKILL.md

**Occurrences (2):**
- `/wos:build-hook` → `/build:build-hook` (×1, line ~29)
- `/wos:build-skill` → `/build:build-skill` (×1, line ~30)

- [ ] Apply both replacements
- [ ] Verify: `grep "wos:" plugins/build/skills/build-rule/SKILL.md` returns no skill invocations
- [ ] Commit: `fix(build): update stale wos: invocations in build-rule skill`

---

## Validation

- [ ] `grep -r "wos:" plugins/ --include="SKILL.md" -n` — output contains only structural marker lines (`<!-- wos:begin -->`, `<!-- wos:end -->`, `<!-- wos:layout:`); zero `/wos:X` skill invocations remain
- [ ] `python3 -m pytest plugins/wiki/tests/ -v` — all tests pass (no skill files touched by Python tests, but confirms no regressions)
