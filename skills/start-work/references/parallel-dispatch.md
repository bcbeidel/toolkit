---
name: Parallel Dispatch
description: Platform-agnostic parallel execution protocol — eligibility, file boundaries, status protocol, merge
---

# Parallel Dispatch

Platform-agnostic protocol for executing independent tasks in parallel.
Consult this when Step 3 of the workflow identifies parallel eligibility.

## Eligibility Criteria

Parallel execution requires ALL of these conditions:

1. **3+ pending tasks** — overhead is not justified for fewer
2. **No file overlap** — entry script's `overlapping_tasks` must be empty
3. **User explicitly opts in** — never default to parallel

If any condition fails, explain why and proceed sequentially.

## File-Boundary Analysis

The entry script's `file_changes.overlapping_tasks` field reports task
pairs that modify the same files. Interpret the results:

- **Empty list** — tasks are independent, parallel is safe
- **Non-empty list** — shared files exist, options:
  - **Sequential** — execute all tasks in order (safest)
  - **Wave-based** — group non-overlapping tasks into waves, execute
    each wave in parallel, run waves sequentially

### Wave-Based Execution

1. Build a dependency graph from `overlapping_tasks`
2. Group tasks that share no files into waves
3. Execute each wave's tasks in parallel
4. Wait for all tasks in a wave to complete before starting the next
5. Merge results between waves

## Dispatch Pattern

Each parallel task needs an isolated environment. The pattern is
platform-agnostic — map these concepts to your tool's dispatch mechanism.

**Per-task payload:** Provide each subagent with:

- **Full task text** — description, steps, verification commands
  (not a file reference — include the actual content so the subagent
  doesn't consume context reading the plan file)
- **File paths** — which files to create or modify
- **Expected outcomes** — what success looks like
- **Verification commands** — how to confirm completion

**Isolation mechanism:** Each subagent works in a git worktree
(or equivalent isolated copy) so changes don't conflict during
parallel execution.

**No platform-specific API calls.** This document describes the
abstract pattern. Users map to their platform's dispatch mechanism
(e.g., Claude Code's Agent tool with `isolation: worktree`, Codex
multi-agent, Copilot /fleet).

## Status Protocol

Each subagent reports one of three statuses:

| Status | Meaning | Action |
|--------|---------|--------|
| `DONE` | Task complete, verification passed | Merge changes. Optional: note any concerns. |
| `NEEDS_HELP` | Cannot proceed without guidance | Read the subagent's report. Provide additional context or clarification, then re-dispatch. |
| `BLOCKED` | External dependency or unresolvable error | Investigate the blocker. May require user intervention or plan modification. |

If a subagent reports no status (timeout, crash), treat as `BLOCKED`.

## Merge Protocol

After all tasks in a wave complete:

1. Integrate each subagent's worktree changes back to the working branch
2. Run verification commands for each completed task
3. Update checkboxes and append SHAs in the plan file
4. Commit the plan file update
5. Clean up worktrees and branches for merged tasks

**If merge conflicts occur** (the file-boundary analysis should prevent
this, but it's not infallible): escalate to the user. Do not attempt
automatic conflict resolution — the risk of introducing subtle bugs
outweighs the convenience.

## Worktree Location

Use `.worktrees/` in the project root as the default worktree directory.
This is model-agnostic — it works the same regardless of which AI coding
tool dispatches the subagents.

Ensure `.worktrees/` is in the project's `.gitignore` (the `wos:init`
skill includes this automatically for new projects).

**Platform overrides:** Some platforms default to vendor-specific paths
(e.g., `.claude/worktrees/`). When dispatching, prefer specifying
`.worktrees/<branch-name>` explicitly so worktrees land in a consistent
location across tools.

## Worktree Cleanup

After merging a worktree's changes, remove the worktree and its branch
immediately. Do not defer cleanup to the end of the plan.

For each merged worktree:

```bash
git worktree remove <worktree-path>
git branch -d <worktree-branch>
```

Example:

```bash
git worktree remove .worktrees/task-3
git branch -d worktree-task-3
```

If `git worktree remove` fails because of untracked files, use
`--force` only after confirming the merge was successful. If
`git branch -d` fails because the branch is not fully merged,
investigate before using `-D` — this usually indicates a merge problem.
