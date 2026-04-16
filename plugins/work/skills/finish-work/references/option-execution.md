# Option Execution

Detailed procedures for each of the 4 integration options presented by
the finish-work skill.

## Option 1: Merge Locally

Merge the feature branch into the base branch on the local machine.

**Steps:**

1. Switch to the base branch:
   ```bash
   git checkout <base-branch>
   ```

2. Pull latest changes:
   ```bash
   git pull
   ```

3. Merge the feature branch:
   ```bash
   git merge <feature-branch>
   ```

4. Run the test suite on the merged result. If tests fail, the merge
   introduced a conflict or regression — report it and let the user
   decide how to proceed.

5. Delete the feature branch:
   ```bash
   git branch -d <feature-branch>
   ```

6. Clean up worktree if applicable (see Worktree Cleanup below).

**Report on completion:**
```
Merged <feature-branch> into <base-branch>.
Tests passing on merged result.
Branch <feature-branch> deleted.
```

## Option 2: Push and Create PR

Push the branch to the remote and create a pull request.

**Steps:**

1. Push the branch:
   ```bash
   git push -u origin <feature-branch>
   ```

2. Build the PR body:
   - **If plan exists:** use the plan's **Goal** section as the summary.
     Include a link to the plan file. Add task count
     (e.g., "5/5 tasks completed").
   - **If no plan:** use `git log <base-branch>..HEAD --oneline` to
     summarize commits.

3. Create the PR:
   ```bash
   gh pr create --title "<title>" --body "<body>"
   ```

4. Report the PR URL to the user.

5. Suggest returning to the main worktree:
   > "PR created. You may want to return to your main worktree:
   > `cd <main-worktree-path>`"

**Do not clean up the worktree.** The user may need it for PR review
feedback or follow-up changes.

## Option 3: Keep Branch

Leave the branch exactly as-is for the user to handle later.

**Steps:**

1. Confirm the branch name:
   ```
   Keeping branch <feature-branch>. No changes made.
   ```

2. If in a worktree, report the worktree path:
   ```
   Worktree preserved at <path>.
   ```

**Take no other action.** Do not push, merge, or clean up anything.

## Option 4: Discard

Delete the branch and all its changes. This is destructive and irreversible.

**Steps:**

1. Show what will be lost:
   ```
   This will permanently delete:
   - Branch: <feature-branch>
   - Commits: <list recent commits with one-line summaries>
   - Worktree: <path> (if applicable)
   ```

2. If a plan file exists, note that its status will be set to `abandoned`.

3. Require typed confirmation:
   ```
   Type 'discard' to confirm.
   ```

4. Wait for exact confirmation. If the user types anything other than
   "discard", cancel the operation.

5. If confirmed:
   - Switch to the base branch:
     ```bash
     git checkout <base-branch>
     ```
   - Delete the feature branch:
     ```bash
     git branch -D <feature-branch>
     ```
   - Update plan frontmatter to `status: abandoned` if a plan exists.
   - Clean up worktree if applicable (see Worktree Cleanup below).

**Report on completion:**
```
Branch <feature-branch> discarded.
All changes deleted.
```

## Worktree Cleanup

Worktree cleanup applies only to Options 1 (Merge) and 4 (Discard).

**Detection:** Check if the current working directory is inside a worktree:

```bash
git worktree list
```

If the current directory appears in the worktree list (and is not the
main working tree), it is a worktree that may need cleanup.

**Cleanup procedure:**

1. Switch to the main working tree first:
   ```bash
   cd <main-worktree-path>
   ```

2. Remove the worktree:
   ```bash
   git worktree remove <worktree-path>
   ```

3. If removal fails (e.g., untracked files), use `--force` only after
   confirming with the user.

**Options 2 and 3 do NOT trigger worktree cleanup.** The worktree is
preserved for continued work.

## Quick Reference

| Option | Merge | Push | Delete Branch | Cleanup Worktree | Plan Status |
|--------|-------|------|---------------|------------------|-------------|
| 1. Merge | Yes | No | Yes (`-d`) | Yes | completed |
| 2. PR | No | Yes | No | No | completed |
| 3. Keep | No | No | No | No | unchanged |
| 4. Discard | No | No | Yes (`-D`) | Yes | abandoned |
