---
name: finish-work
description: >
  Use when implementation is complete and validated, to decide how to
  integrate the work. Presents structured options for merge, PR, keep,
  or discard with safety verification. Use when the user wants to
  "finish", "done", "merge this", "create PR", "wrap up", "ship it",
  or after completing all tasks and validation in a plan.
argument-hint: "[plan file path]"
user-invocable: true
disable-model-invocation: true
references:
  - references/option-execution.md
  - ../../_shared/references/plan-format.md
---

# Finish Work

Decide how to integrate completed work — merge, PR, keep, or discard —
with safety verification and optional plan lifecycle updates.

**Announce at start:** "I'm using the finish-work skill to complete this work."

## Workflow

### 1. Verify Readiness

Run the project's test suite before anything else. Detect the test command
from:

1. The plan's **Validation** section code blocks (if a plan is found in
   Step 2 — read ahead to locate it first)
2. CLAUDE.md or project conventions (e.g., `package.json` scripts, pytest
   configuration)
3. Ask the user if no test command is discoverable

```
Tests passing (N passed). Proceeding to integration options.
```

**Hard gate:** if tests fail, stop and report failures. Do not present
options until tests pass.

```
Tests failing (N failures). Must fix before completing:

[Show failures]

Cannot proceed until tests pass.
```

### 2. Locate Plan (optional)

If the user provided a plan path as an argument, use it. Otherwise, search
for a plan file:

```bash
python <plugin-skills-dir>/start-work/scripts/plan_assess.py --scan --root <project-root>
```

Parse the JSON output to find plans with `status: executing` or
`status: completed`.

| Result | Action |
|--------|--------|
| Exactly one plan found | Use it |
| Multiple plans found | Ask the user which one applies |
| No plans found | Proceed without plan — skip plan-related steps |

If a plan is found with `status: executing`, update frontmatter to
`status: completed`. If already `completed`, leave it unchanged.

### 3. Determine Base Branch

Identify the branch this work should integrate into:

```bash
git merge-base HEAD main
```

If that fails, try `master`. Confirm with the user:

> "This branch diverged from `main` — is that correct?"

### 4. Present 4 Options

Present these options, distinguishing the irreversible action:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work (irreversible)
```

### 5. Execute Chosen Option

Follow the detailed procedures in
[option-execution](references/option-execution.md) for the chosen option.

Summary:

- **Option 1 — Merge locally:** checkout base branch, pull latest, merge
  feature branch, verify tests on merged result, delete feature branch,
  clean up worktree if applicable.
- **Option 2 — Push and create PR:** push branch with `-u`, create PR
  using plan Goal as body (or git log if no plan), keep worktree, suggest
  returning to main worktree.
- **Option 3 — Keep branch:** confirm branch name, take no action, keep
  worktree.
- **Option 4 — Discard:** show what will be lost, require typed "discard"
  confirmation, update plan status to `abandoned` if plan exists, delete
  branch, clean up worktree.

## Key Instructions

- **Won't present integration options until tests pass** — the hard gate in Step 1 enforces this; failing tests must be fixed before continuing
- **Won't discard without typed "discard" confirmation** — Option 4 is irreversible; no shortcut, no yes/no prompt
- **Plan is optional.** The skill works for both plan-backed branches and
  ad-hoc feature branches. Skip plan-related steps when no plan exists.
- **Worktree cleanup follows the option.** Only clean up worktrees on
  merge (Option 1) or discard (Option 4). Keep and PR preserve the
  worktree for continued access.
- **Plan status must be accurate.** Set `completed` only when transitioning
  from `executing`. Set `abandoned` only on discard. Never overwrite a
  status that's already terminal.

## Anti-Pattern Guards

1. **Presenting options with failing tests** — the hard gate prevents
   this, but if you discover test failures after Step 1, stop and report
   them before continuing.
2. **Skipping discard confirmation** — every discard must get typed
   "discard" from the user. No shortcuts, no "are you sure?" yes/no.
3. **Cleaning up worktree on keep or PR** — Options 2 and 3 preserve
   the worktree. Only Options 1 and 4 trigger cleanup.
4. **Creating PR without plan context** — when a plan exists, use its
   Goal section for the PR body. Fall back to git log only when no plan
   is available.
5. **Forcing plan requirement** — if no plan is found, proceed with the
   pure git workflow. Do not ask the user to create a plan just to finish
   their work.
6. **Presenting options without reversibility context** — Options 1-4 are not equivalent. Discard is irreversible; the others are not. When presenting options, ensure the user understands which actions cannot be undone. Never normalize an irreversible action by presenting it in a flat list alongside reversible ones without distinction.

## Handoff

**Receives:** Plan file path; completed, validated implementation on a feature branch
**Produces:** PR opened or merge completed; branch cleaned up; roadmap checkbox updated
**Chainable to:** —
