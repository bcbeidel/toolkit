---
name: start-work
description: >
  Use when you have an approved implementation plan to execute.
  Handles sequential execution, progress tracking, and recovery.
  Enforces the approval gate. Use when the
  user wants to "execute the plan", "run the plan", "implement this
  plan", "start work", or "start building".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[plan file path]"
user-invocable: true
references:
  - references/execution-guide.md
  - references/recovery-patterns.md
  - references/multi-session-resumption.md
license: MIT
---

# Start Work

Execute approved implementation plans with lifecycle enforcement, progress
tracking, and multi-session resumption.

**Announce at start:** "I'm using the start-work skill to implement this plan."

## Workflow

### 1. Load Plan

Run the entry script:

```bash
python <plugin-skills-dir>/start-work/scripts/plan_assess.py --file <path>
```

If no plan path was provided, use `--scan` mode to find executing plans:

```bash
python <plugin-skills-dir>/start-work/scripts/plan_assess.py --scan --root <project-root>
```

Read the plan file. Parse the JSON output for status, task state, file
boundaries, and readiness. Present a summary to the user:

> "Plan: **[name]** — [completed]/[total] tasks complete, status: [status]"

### 2. Approval Gate

Enforce status requirements before proceeding:

| Status | Action |
|--------|--------|
| `draft` | **Refuse.** "This plan hasn't been approved yet. Get approval first, then come back." |
| `approved` | **Proceed.** Update frontmatter to `status: executing`. |
| `executing` | **Resume.** Consult [multi-session resumption](references/multi-session-resumption.md) to find where to pick up. |
| `completed` | **Refuse.** "This plan is already finished." |
| `abandoned` | **Refuse.** "This plan was intentionally stopped." |
| missing | **Warn.** "No status field — treating as legacy plan." Proceed with caution. |

### 3. Branch Setup

Before executing tasks, ensure work happens on a feature branch.

1. Check if currently on the default branch (`main` or `master`).
2. If on default branch:
   - Derive a branch name from the plan filename: strip `.plans/` and
     the date prefix. E.g., `.plans/2026-03-11-skill-workflow.plan.md` →
     `skill-workflow`.
   - Present to user: "This plan should be implemented on a branch.
     Suggested: `<name>` — use this, or provide a different name?"
   - Wait for user confirmation.
   - Create and checkout the branch: `git checkout -b <name>`
   - Write the branch name to the plan's `branch:` frontmatter field.
3. If already on a feature branch:
   - Present to user: "Currently on branch `<name>` — use this for
     the plan?"
   - On confirmation, write the branch name to the plan's `branch:`
     field if not already set.

### 4. Choose Execution Mode

Execute tasks sequentially in the order listed.

For research tasks, invoke `/wiki:research` per task; the skill manages
its own pipeline and validation internally.

### 5. Execute Tasks

For each pending task:

1. **Implement** the task as described in the plan
2. **Verify** — identify verification type and apply the matching protocol
   from the [execution guide](references/execution-guide.md):
   - **Automated:** Run the command, confirm expected output
   - **Structural:** Read files, confirm observable facts
   - **Reasoning:** Trace implementation against the plan's Goal/Approach
3. **Git commit** the implementation: `feat(plan): task N — title`
4. **Update checkbox** `- [ ]` → `- [x]` with the SHA from step 3:
   `- [x] Task N: title <!-- sha:abc1234 -->`
5. **Commit plan update** (or fold into the next task's implementation commit)

On failure, consult [recovery patterns](references/recovery-patterns.md).

### 6. Validate

When all tasks are checked, present to user: "All tasks complete. Ready
to invoke `/work:verify-work` to verify the plan succeeded — proceed?"

Wait for user confirmation before invoking the skill.

- **User confirms** — invoke `/work:verify-work`, which runs validation
  and handles the `status: completed` transition on success.
- **User declines** — update frontmatter to `status: completed` directly.
  The user accepts responsibility for skipping plan-level validation.

### 7. Finish

Present to user: "Validation passed. Ready to invoke `/work:finish-work`
to integrate — proceed?"

Wait for user confirmation before invoking the skill.

## Key Instructions

- **Commit per task creates rollback boundaries.** Every completed task
  gets its own git commit. On failure, diff against the last passing
  commit SHA from the checkbox annotation.
- **Plan file is source of truth.** Checkbox state + commit SHAs are the
  execution record. Do not rely on conversation context for state.
- **Don't check boxes without proof.** Every `[x]` requires verification
  evidence — command output, structural check, or reasoning trace.
- **Intermediates go to disk.** Write discovered decisions, edge cases,
  and API findings to the plan file or a companion notes file. Context
  resets; files persist.
- **Execute the plan as written.** Don't add features, refactor adjacent
  code, or expand scope during execution. If the plan needs changes,
  pause and discuss with the user.

## Anti-Pattern Guards

1. **Checking boxes without a commit SHA** — `[x]` without `<!-- sha:abc1234 -->` is a lost-update anti-pattern. A new session cannot verify what was done or roll back to a known-good state. Every checkbox requires both verification evidence and a commit SHA.
2. **Skipping the approval gate** — executing draft plans wastes work
   on unapproved designs. Always check status first.
3. **Autonomous recovery beyond 2 retries** (3 total attempts) —
   escalate to user with evidence, not infinite loops.
4. **Modifying plan scope during execution** — if the plan needs
   changes, pause and discuss with the user.
5. **Relying on conversation context** — sessions end; plan files
   persist. Always read the plan file and git log to orient.
6. **Skipping per-task commits** — the commit after each task IS the checkpoint. Without it, a failure forces a full restart rather than a partial rollback. "I'll commit at the end" negates the rollback boundary that per-task commits create.

## Handoff

**Receives:** Plan file path (`.plan.md`) with `status: approved`
**Produces:** Implemented code and files per plan; plan tasks marked `[x]` with commit SHAs
**Chainable to:** verify-work
