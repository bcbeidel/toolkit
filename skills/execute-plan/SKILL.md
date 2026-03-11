---
name: execute-plan
description: >
  Use when you have an approved implementation plan to execute.
  Handles sequential execution, parallel subagent dispatch, progress
  tracking, and recovery. Enforces the approval gate. Use when the
  user wants to "execute the plan", "run the plan", "implement this
  plan", or "start building".
argument-hint: "[plan file path]"
user-invocable: true
references:
  - ../_shared/references/preflight.md
  - references/execution-guide.md
  - references/parallel-dispatch.md
  - references/recovery-patterns.md
  - references/multi-session-resumption.md
---

# Execute Plan

Execute approved implementation plans with lifecycle enforcement, progress
tracking, and multi-session resumption.

**Announce at start:** "I'm using the execute-plan skill to implement this plan."

## Workflow

### 1. Load Plan

Run the preflight check (per `preflight.md`), then the entry script:

```bash
uv run <plugin-scripts-dir>/check_runtime.py
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --file <path>
```

If no plan path was provided, use `--scan` mode to find executing plans:

```bash
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --scan --root <project-root>
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

### 3. Choose Execution Mode

**Sequential** (default) — execute tasks in order.

**Parallel** (opt-in) — requires ALL of these conditions:
- 3+ pending tasks
- No file overlap (entry script's `overlapping_tasks` is empty)
- User explicitly opts in when asked

If the entry script reports `parallel_eligible: true`, present the option:

> "This plan has [N] independent tasks with no file overlap.
> Execute sequentially (default) or in parallel?"

If not eligible, state why and proceed sequentially. Consult
[parallel dispatch](references/parallel-dispatch.md) for the full protocol.

### 4. Execute Tasks

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

### 5. Validate

When all tasks are checked, recommend running `wos:validate-plan` to
verify the plan succeeded end-to-end. Ask the user for confirmation.

- **User confirms** — invoke `wos:validate-plan`, which runs validation
  and handles the `status: completed` transition on success.
- **User declines** — update frontmatter to `status: completed` directly.
  The user accepts responsibility for skipping plan-level validation.

### 6. Finish

Invoke `wos:finish-work`.

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

1. **Checking boxes without verification** — the plan file becomes
   unreliable and resumption breaks. Every `[x]` needs proof.
2. **Skipping the approval gate** — executing draft plans wastes work
   on unapproved designs. Always check status first.
3. **Autonomous recovery beyond 2 retries** (3 total attempts) —
   escalate to user with evidence, not infinite loops.
4. **Modifying plan scope during execution** — if the plan needs
   changes, pause and discuss with the user.
5. **Relying on conversation context** — sessions end; plan files
   persist. Always read the plan file and git log to orient.
