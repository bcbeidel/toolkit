---
name: "finish-work skill design"
description: "Design spec for wos:finish-work — structured work termination with 4 integration options, safety gates, and optional retrospective"
type: plan
status: completed
related:
  - docs/plans/2026-03-11-validate-plan-skill-design.md
  - docs/plans/2026-03-11-execute-plan-skill-design.md
---

# finish-work Skill Design

## Context

Terminal step in the WOS plan lifecycle pipeline (brainstorm → write-plan →
execute-plan → validate-plan → **finish-work**). Replaces
`superpowers:finishing-a-development-branch` with a WOS-native skill that
integrates with plan lifecycle tracking.

Issue: #162

## Skill Metadata

```yaml
name: finish-work
description: >
  Use when implementation is complete and validated, to decide how to
  integrate the work. Presents structured options for merge, PR, keep,
  or discard with safety verification. Triggers on "finish", "done",
  "merge this", "create PR", "wrap up", "ship it".
argument-hint: "[plan file path]"
user-invocable: true
references:
  - references/option-execution.md
  - references/retrospective-format.md
  - ../_shared/references/preflight.md
  - ../_shared/references/plan-format.md
```

## Workflow

### Step 1: Verify Readiness

Run the project's test suite. Detect test command from the plan's Validation
section code blocks (if plan found), or from CLAUDE.md / project conventions.

Hard gate: if tests fail, stop and report failures. Do not present options
until tests pass.

### Step 2: Locate Plan (optional)

- If user provided a plan path, use it.
- Otherwise, use `plan_assess.py --scan` to search `docs/plans/` for plans
  with `status: executing` or `status: completed`.
- If exactly one found, use it. If multiple, ask which one. If none, proceed
  without plan (pure git workflow).
- If plan found and status is `executing`, update to `completed`. If already
  `completed`, leave it.
- If no plan, skip plan-related steps (status update, retrospective).

### Step 3: Determine Base Branch

Check `git merge-base HEAD main`, fall back to `master`. Confirm with user:
"This branch diverged from `main` — is that correct?"

### Step 4: Present 4 Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
```

No additional explanation — keep options concise.

### Step 5: Execute Chosen Option

Delegate to `option-execution.md` for detailed per-option behavior:

- **Merge**: checkout base, pull, merge, run tests on merged result, delete
  branch, cleanup worktree if applicable
- **PR**: push with `-u`, create PR (plan-derived body if plan exists, git
  log fallback), keep worktree, suggest returning to main worktree
- **Discard**: show what will be lost, require typed "discard" confirmation,
  update plan status to `abandoned` if plan exists, delete branch, cleanup
  worktree
- **Keep**: confirm branch name, no action, keep worktree

### Step 6: Optional Retrospective (plan only)

Offer only if a plan file was found: "Would you like to add a retrospective
to the plan?" If yes, add `## Retrospective` section per
`retrospective-format.md`.

## File Structure

```
skills/finish-work/
  SKILL.md
  references/
    option-execution.md
    retrospective-format.md
```

Plus shared references: `_shared/references/preflight.md`,
`_shared/references/plan-format.md`.

## Safety Gates

| Gate | Mechanism |
|------|-----------|
| Tests must pass | Hard stop in Step 1; no options presented until green |
| Discard confirmation | Typed "discard" required before destructive action |
| Worktree cleanup scope | Only on merge or discard; keep and PR preserve worktree |
| Plan status accuracy | Set `completed` only if executing; set `abandoned` only on discard |

## Anti-Pattern Guards

1. **Presenting options with failing tests** — hard gate prevents this
2. **Skipping discard confirmation** — must get typed "discard"
3. **Cleaning up worktree on keep/PR** — only on merge/discard
4. **Creating PR without plan context** — use plan Goal for PR body when available
5. **Forcing plan requirement** — skill works with or without a plan file

## Design Justification

| Decision | Source | Evidence |
|----------|--------|----------|
| Tests must pass before presenting options | Anthropic effective harnesses (2025) | Hard gates prevent shipping broken work |
| Exactly 4 structured options | Superpowers v5.0.0 audit | Proven pattern covering all terminal states |
| Typed discard confirmation | Destructive operation safety patterns | Prevents accidental work loss |
| Optional retrospective | Codex PLANS.md (OpenAI, 2025) | Living document retrospective, not post-hoc artifact |
| Plan-optional design | WOS convention | Skill works for plan-backed and ad-hoc branches |

## Acceptance Criteria

- [ ] SKILL.md written and under 500 lines
- [ ] Skill triggers on "finish", "done", "merge", "create PR"
- [ ] Tests verified before presenting options
- [ ] Exactly 4 options presented (merge/PR/keep/discard)
- [ ] Discard requires typed confirmation
- [ ] Plan status updated to `completed` (or `abandoned` on discard)
- [ ] Worktree cleanup handled correctly per option
- [ ] Optional retrospective offered (plan-only)
