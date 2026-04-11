---
name: Deprecate /wos:retrospective
description: Add deprecation header and notice to the retrospective skill, update OVERVIEW.md and README.md to reflect deprecated status ahead of removal in v0.39.0
type: plan
status: executing
branch: feat/deprecate-retrospective
pr: ~
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# Deprecate /wos:retrospective

## Goal

Mark `/wos:retrospective` as deprecated in v0.38.0 so users migrate to
`/wos:finish-work` Step 6, which already covers the same functionality.
The skill stays functional but emits a visible notice; full removal is
scheduled for v0.39.0.

## Scope

**Must have:**
- Deprecation blockquote at the top of `skills/retrospective/SKILL.md` body
- Instruction to emit the deprecation notice when the skill is invoked
- `OVERVIEW.md` Feedback Layer description and Skills Reference table updated to reflect deprecated status
- `README.md` active skill count updated (13 → 12)

**Won't have:**
- Removal of the skill or any of its references — that is v0.39.0 work
- Changes to `finish-work` — Step 6 already covers the retrospective flow

## Approach

Three files change. No Python, no tests, no new files.

1. **`skills/retrospective/SKILL.md`** — insert the deprecation blockquote
   immediately after the frontmatter block, then add an explicit first step
   in the Workflow section instructing the agent to emit the notice before
   continuing.

2. **`OVERVIEW.md`** — two edits:
   - In the Feedback Layer prose description, append `(deprecated — use /wos:finish-work Step 6)` after "Retrospective".
   - In the Skills Reference table, append ` *(deprecated)*` to the retrospective row's Purpose cell.

3. **`README.md`** — change "13 skills" to "12 active skills" (retrospective
   is deprecated, not active).

Each task ends with a commit so rollback boundaries are clean.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `skills/retrospective/SKILL.md` | Modify | Add deprecation blockquote header + emit-notice instruction |
| `OVERVIEW.md` | Modify | Mark retrospective deprecated in Feedback Layer and Skills Reference |
| `README.md` | Modify | Adjust skill count from 13 to 12 |
| `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` | Modify | Check off Task 15 with merge commit SHA |

## Tasks

- [x] Task 1: Add deprecation header and emit-notice instruction to `skills/retrospective/SKILL.md` <!-- sha:531d20b -->
- [x] Task 2: Mark retrospective deprecated in `OVERVIEW.md` (Feedback Layer + Skills Reference) <!-- sha:a2c9970 -->
- [x] Task 3: Update `README.md` skill count from 13 to 12 active <!-- sha:87e6981 -->

### Task 1 — Add deprecation header and emit-notice instruction to SKILL.md

Edit `skills/retrospective/SKILL.md`:

1. Insert the following blockquote immediately after the closing `---` of the
   frontmatter (before `# Retrospective Skill`):

   ```
   > **Deprecated as of v0.38.0.** The retrospective step is available in
   > `/wos:finish-work` (Step 6). This skill continues to work but will be
   > removed in v0.39.0. Migrate to `/wos:finish-work`.
   ```

2. Add an explicit first step to the Workflow section — before the existing
   single-line reference to `references/retrospective-workflow.md`:

   ```
   Before continuing, emit this notice to the user:
   > **Deprecation notice:** `/wos:retrospective` is deprecated as of v0.38.0.
   > The same functionality is built into `/wos:finish-work` Step 6.
   > This skill will be removed in v0.39.0.
   ```

Commit:
```bash
git add skills/retrospective/SKILL.md
git commit -m "chore: add deprecation header and notice to /wos:retrospective (#230)"
```

**Verification:**
```bash
grep -c "Deprecated" skills/retrospective/SKILL.md
# Expected: 2 (one in blockquote header, one in emit-notice step)
python scripts/lint.py --root . --no-urls
# Expected: clean pass, no new issues
```

---

### Task 2 — Update OVERVIEW.md

Edit `OVERVIEW.md` in two places:

1. **Feedback Layer prose** (line ~78): change
   ```
   - **Retrospective** — reviews the current session and submits structured feedback as a GitHub Issue
   ```
   to
   ```
   - **Retrospective** *(deprecated — use `/wos:finish-work` Step 6)* — reviews the current session and submits structured feedback as a GitHub Issue
   ```

2. **Skills Reference table** (line ~96): change
   ```
   | `/wos:retrospective` | Session review and feedback submission |
   ```
   to
   ```
   | `/wos:retrospective` | *(deprecated)* Session review and feedback submission |
   ```

Commit:
```bash
git add OVERVIEW.md
git commit -m "chore: mark /wos:retrospective deprecated in OVERVIEW.md (#230)"
```

**Verification:**
```bash
grep "deprecated" OVERVIEW.md
# Expected: 2 matches — one in Feedback Layer prose, one in Skills Reference table
python scripts/lint.py --root . --no-urls
# Expected: clean pass
```

---

### Task 3 — Update README.md skill count

Edit `README.md` line ~29: change
```
WOS provides 13 skills organized into four layers
```
to
```
WOS provides 12 active skills organized into four layers (plus 1 deprecated)
```

Commit:
```bash
git add README.md
git commit -m "chore: update skill count to 12 active (retrospective deprecated) (#230)"
```

**Verification:**
```bash
grep "12 active skills" README.md
# Expected: 1 match
python scripts/lint.py --root . --no-urls
# Expected: clean pass
```

---

### Task 4 — Mark Task 15 complete in roadmap (post-merge)

After the PR merges, update Task 15 in `docs/plans/2026-04-10-roadmap-v036-v039.plan.md`
from unchecked to checked with the merge SHA.

**Note:** This step runs on `main` after the PR merges, not on this branch.

## Validation

```bash
# 1. Deprecation header is present in SKILL.md
grep -c "Deprecated" skills/retrospective/SKILL.md
# Expected: 2

# 2. Emit-notice instruction is present
grep "Deprecation notice" skills/retrospective/SKILL.md
# Expected: 1 match

# 3. OVERVIEW.md has two deprecated markers
grep -c "deprecated" OVERVIEW.md
# Expected: 2

# 4. README reflects 12 active skills
grep "12 active skills" README.md
# Expected: 1 match

# 5. Full lint pass — no new issues
python scripts/lint.py --root . --no-urls
# Expected: zero failures, zero new warnings

# 6. Full test suite clean
python -m pytest tests/ -v
# Expected: all pass
```
