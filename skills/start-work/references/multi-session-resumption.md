---
name: Multi-Session Resumption
description: Session recovery protocol — plan file reading, SHA verification, stale state detection
---

# Multi-Session Resumption

How to pick up plan execution after a session ends. Consult this when
Step 2 of the workflow encounters `status: executing`.

## Session Start Protocol

When resuming an executing plan:

1. **Run the entry script** — get the current plan state as JSON
2. **Identify the next pending task** — the first unchecked item
3. **Read recent git log** — last 10 commits for context on what
   was done recently
4. **Confirm SHA integrity** — verify that checked tasks' SHAs
   exist in the git history
5. **Resume execution** from the next pending task

Do NOT rely on conversation context from a previous session. The
previous session is gone — the plan file and git history are your
only sources of truth.

## Orientation Sequence

Before resuming task execution, orient yourself:

1. **Check working directory** — `pwd`, confirm you're in the
   right project
2. **Read plan assessment** — the entry script JSON tells you
   exactly where things stand
3. **Review recent commits** — `git log --oneline -10` to see
   what was recently completed
4. **Identify current task** — the first unchecked checkbox
5. **Read the task context** — understand what the task requires
   before starting

This sequence prevents wasted work from misunderstanding the
current state.

## Plan File as Source of Truth

The plan file is the primary state record:

- **Checked tasks** (`[x]`) — work that is done
- **SHA annotations** (`<!-- sha:abc1234 -->`) — which commits
  contain the work
- **Unchecked tasks** (`[ ]`) — work that remains
- **Status field** — overall plan lifecycle state

Git history is the secondary confirmation. If the plan file and
git history disagree, investigate before proceeding.

## Stale Executing State

If the plan says `status: executing` but:

- **No recent commits match task SHAs** — someone may have checked
  boxes without committing, or commits were on a different branch.
  Investigate before resuming.
- **All tasks are checked but status is still executing** — the
  previous session may have completed all tasks but not transitioned
  the status. Run validation and update to `completed` if it passes.
- **The branch doesn't exist** — the work may have been merged or
  lost. Check `git branch -a` and the main branch history.

## SHA Mismatch Handling

For each checked task with a SHA annotation:

- **SHA exists in git log** — task is confirmed complete
- **SHA does not exist** — the checkbox is unreliable. Options:
  - Re-verify the task's work independently
  - If the work is present (files exist, tests pass), add the
    correct SHA
  - If the work is missing, uncheck the task and re-execute

**Checked task without SHA** — a warning, not an error. The task
may have been completed in an older session before SHA tracking
was adopted. Verify the work is present before proceeding.

## Context Window Efficiency

The entry script's JSON output is designed to save tokens during
resumption. Instead of reading the entire plan file and git log
to figure out where you are, the JSON gives you:

- Task counts (total, completed, pending)
- Per-task completion state with SHAs
- Readiness assessment with issues

Read the JSON first. Only read the full plan file when you need
task details for the next task to execute.
