---
name: Execute Plan Skill Design
description: Design spec for wos:execute-plan skill — plan execution with lifecycle gates, parallel dispatch, and deterministic assessment
type: plan
status: approved
related:
  - docs/plans/2026-03-11-plan-document-format-design.md
  - docs/plans/2026-03-11-write-plan-skill.md
  - docs/plans/2026-03-11-brainstorm-skill.md
---

# Execute Plan Skill Design

## Purpose

WOS-native skill for executing approved implementation plans. Replaces
`superpowers:executing-plans` with lifecycle-aware execution, deterministic
plan assessment, platform-agnostic parallel dispatch, and multi-session
resumption.

## Skill Directory Structure

```
skills/execute-plan/
├── SKILL.md                          (~170 lines)
├── scripts/
│   └── plan_assess.py                (PEP 723 CLI wrapper)
└── references/
    ├── execution-guide.md            (~100 lines)
    ├── parallel-dispatch.md          (~100 lines)
    ├── recovery-patterns.md          (~90 lines)
    └── multi-session-resumption.md   (~80 lines)
```

Supporting module:

```
wos/plan/
├── __init__.py
└── assess_plan.py
tests/test_plan_assess.py
```

## SKILL.md Workflow

### Metadata

```yaml
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
```

### Step 1: Load Plan

Run the preflight check (per `preflight.md`), then the entry script:

```bash
uv run <plugin-scripts-dir>/check_runtime.py
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --file <path>
```

Read the plan file. Parse the JSON output for status, task state, file
boundaries, and readiness.

### Step 2: Approval Gate

Enforce status requirements:

| Status | Action |
|--------|--------|
| `draft` | Refuse. Suggest getting approval first. |
| `approved` | Proceed. Update to `status: executing`. |
| `executing` | Resume. Consult multi-session-resumption reference. |
| `completed` | Refuse. Plan already finished. |
| `abandoned` | Refuse. Plan was intentionally stopped. |
| missing | Warn. Treat as legacy plan, proceed with caution. |

### Step 3: Choose Execution Mode

- **Sequential** (default) — execute tasks in order.
- **Parallel** (opt-in) — requires ALL:
  - 3+ independent tasks
  - No file overlap (confirmed by entry script's `overlapping_tasks: []`)
  - User explicitly opts in

If parallel eligible, present the option. If not, state why and proceed
sequentially. Consult parallel-dispatch reference for protocol.

### Step 4: Execute Tasks

For each task:

1. Implement the task
2. Run verification — identify type (automated, structural, reasoning)
   and apply matching protocol from execution guide
3. Update checkbox `- [ ]` → `- [x]` in plan file
4. Append commit SHA to checkbox: `- [x] Task N: title <!-- sha:abc1234 -->`
5. Git commit with message: `feat(plan): task N — title`

On failure: consult recovery-patterns reference.

### Step 5: Validate

Invoke `wos:validate-plan`. If validation passes, update plan
`status: completed`.

### Step 6: Finish

Invoke `wos:finish-work`.

### Key Instructions

- **Commit per task creates rollback boundaries.** Every completed task
  gets its own git commit. On failure, diff against the last passing
  commit SHA.
- **Plan file is source of truth.** Checkbox state + commit SHAs are the
  execution record. Don't rely on conversation context.
- **Don't check boxes without proof.** Every `[x]` requires verification
  evidence — command output, structural check, or reasoning trace.
- **Intermediates go to disk.** Write discovered decisions, edge cases,
  and API findings to the plan file or a companion notes file.
- **Execute the plan as written.** Don't add features, refactor adjacent
  code, or expand scope during execution.

### Anti-Pattern Guards

1. **Checking boxes without verification** — the plan file becomes
   unreliable; resumption breaks.
2. **Skipping the approval gate** — executing draft plans wastes work
   on unapproved designs.
3. **Autonomous recovery beyond 2 retries** (3 total attempts) —
   escalate to user with evidence, not infinite loops.
4. **Modifying plan scope during execution** — if the plan needs changes,
   pause and discuss with the user.
5. **Relying on conversation context** — sessions end; plan files persist.

## Entry Script Design

### CLI Interface

```bash
# Assess a single plan
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --file <path>

# Find all executing plans (for session resumption)
uv run <plugin-skills-dir>/execute-plan/scripts/plan_assess.py --scan --root <project-root>
```

Modes are mutually exclusive. `--scan` searches `docs/plans/` for plans
with `status: executing` and returns a list of plan summaries.

### Module: `wos/plan/assess_plan.py`

**Functions:**

- `assess_file(path: str) -> dict` — full plan assessment (single file)
- `scan_plans(root: str) -> list[dict]` — find plans with `status: executing`
- `_parse_tasks(content: str) -> list[dict]` — extract checkbox items
  with index, title, completion state, and optional SHA
- `_detect_sections(content: str) -> dict[str, bool]` — check for 6
  required section headings (Goal, Scope, Approach, File Changes,
  Tasks, Validation)
- `_extract_file_changes(content: str) -> list[str]` — parse File
  Changes section for file paths
- `_map_task_files(tasks, file_changes, content) -> dict` — map tasks to
  files using the File Changes section structure. Plans list files under
  task headings (e.g., `### Task 1` → file list). If the plan uses a flat
  file list without per-task grouping, all files are assigned to all tasks
  (conservative: forces sequential execution)
- `_find_overlaps(task_file_map: dict) -> list[tuple]` — identify task
  pairs that modify the same files

### Output JSON

```json
{
  "file": "docs/plans/2026-03-11-feature.md",
  "exists": true,
  "frontmatter": {
    "name": "Feature Name",
    "status": "approved",
    "type": "plan"
  },
  "sections": {
    "goal": true,
    "scope": true,
    "approach": true,
    "file_changes": true,
    "tasks": true,
    "validation": true,
    "all_present": true
  },
  "tasks": {
    "total": 8,
    "completed": 3,
    "pending": 5,
    "items": [
      {"index": 1, "title": "Create package", "completed": true, "sha": "a1b2c3d"},
      {"index": 2, "title": "Write tests", "completed": true, "sha": "e4f5g6h"},
      {"index": 3, "title": "Implement parser", "completed": true, "sha": "i7j8k9l"},
      {"index": 4, "title": "Add validation", "completed": false, "sha": null}
    ]
  },
  "file_changes": {
    "files": ["wos/plan/__init__.py", "wos/plan/assess_plan.py"],
    "task_file_map": {
      "1": ["wos/plan/__init__.py"],
      "2": ["tests/test_plan_assess.py"]
    },
    "overlapping_tasks": []
  },
  "readiness": {
    "status_ok": true,
    "sections_complete": true,
    "has_pending_tasks": true,
    "parallel_eligible": true,
    "issues": []
  }
}
```

### Constraints

- stdlib-only, Python 3.9+ (`from __future__ import annotations`)
- Read-only — observes, never modifies
- Uses existing `wos.document.parse_document()` for frontmatter
- Plugin root discovery via `CLAUDE_PLUGIN_ROOT` env var with
  `__file__` parent chain fallback

### Task Checkbox Format

```markdown
- [ ] Task 1: Create package structure
- [x] Task 2: Write tests <!-- sha:a1b2c3d -->
```

The entry script parses both formats. SHA is optional — its absence on
a checked task is a warning during resumption (checkbox may be unreliable).

## Reference File Design

### `references/execution-guide.md` (~100 lines)

Core execution loop guidance:

- **Task execution protocol:** implement → verify → checkbox → SHA → commit
- **Commit discipline:** one commit per task, message format
  `feat(plan): task N — title`, references plan file path.
  For 10+ task plans with chunk boundaries, also commit at chunk
  transitions (chunk commits are supplementary, not a replacement
  for per-task commits)
- **Three-tier verification model:**

  | Type | Signal | Example | How to verify |
  |------|--------|---------|---------------|
  | Automated | Command exit code + output | `pytest tests/test_foo.py` | Run it, confirm expected output |
  | Structural | Observable file/code state | "Function exists in module" | Read the file, confirm the fact |
  | Reasoning | Intent alignment | "Gate refuses draft plans" | Trace implementation against Goal/Approach |

- **Verification protocol:** For each task, identify which type applies.
  Automated → run. Structural → check. Reasoning → trace and confirm.
  Only mark `[x]` with evidence.
- **Chunk boundaries:** For 10+ task plans, commit at chunk boundaries too.
- **Scope discipline:** Execute as written. No feature additions, no
  adjacent refactoring, no scope expansion.
- **When to stop:** Unclear instructions, missing dependencies, repeated
  verification failures (after 2 retries / 3 total attempts).

### `references/parallel-dispatch.md` (~100 lines)

Platform-agnostic parallel execution protocol:

- **Eligibility:** 3+ independent tasks, no file overlap (entry script
  confirms), user opt-in required.
- **File-boundary analysis:** Interpret `overlapping_tasks` from entry
  script. If non-empty, fall back to sequential or wave-based execution.
- **Wave-based execution:** Group independent tasks into waves. Execute
  each wave in parallel, sequential between waves.
- **Dispatch pattern (abstract):** Each subagent gets:
  - Isolated workspace (git worktree)
  - Full task context in payload: description, file paths, expected
    outcomes, verification commands
  - Not file references — full text, so subagent doesn't consume context
    reading the plan
- **3-status protocol:**
  - `DONE` — task complete, verification passed (optional concerns field)
  - `NEEDS_HELP` — cannot proceed without guidance
  - `BLOCKED` — external dependency or unresolvable error
- **Merge:** Integrate worktree changes back to working branch. If merge
  conflicts occur, escalate to user.
- **No platform-specific API calls.** Describes the pattern; users map
  to their tool's dispatch mechanism.

### `references/recovery-patterns.md` (~90 lines)

What to do when things go wrong:

- **Task splitting on partial completion:** Convert incomplete task into
  done + remaining sub-items in the plan file. The done portion gets
  its own `[x]` and SHA.
- **Retry protocol:** Feed failure output back, retry up to 2 times.
  Escalate after exhaustion.
- **Escalation format:** What was tried, evidence (logs/diffs), options
  with tradeoffs, recommendation with confidence level.
- **Git-based rollback:** Diff against last passing commit SHA (from
  checkbox annotation). Revert if needed.
- **Task-pass / plan-fail:** When all tasks pass but plan-level
  validation fails, add new tasks to address gaps — do NOT mark the
  plan as failed. Plan stays `executing` with appended tasks.
- **Transient vs. non-transient:** Flaky tests or network errors are
  transient (retry). Missing APIs or wrong architecture are
  non-transient (escalate immediately).

### `references/multi-session-resumption.md` (~80 lines)

How to pick up where you left off:

- **Session start protocol:**
  1. Run entry script → read JSON
  2. Identify next pending task (first unchecked item)
  3. Read recent git log (last 10 commits) for context
  4. Confirm SHAs on checked tasks match git history
  5. Resume execution from next pending task
- **Plan file is source of truth.** Git history is secondary confirmation.
- **Don't rely on conversation context.** Previous session is gone.
- **Orientation sequence:** Check working directory, read plan assessment,
  review recent commits, identify current task.
- **Stale executing state:** If plan says `executing` but no recent
  commits match task SHAs, investigate before resuming — someone may
  have checked boxes without committing.
- **SHA mismatch handling:** If a checked task's SHA doesn't exist in
  git log, treat the task as unreliable — re-verify before proceeding.

## Design Decisions

| Decision | Justification | Source |
|----------|---------------|--------|
| Workflow-first SKILL.md | Agent spends 95% of time in execution loop; gates are compact conditions, not the organizing principle | Superpowers audit: 70-line skill flagged as gap; effective skills delegate detail to references |
| 4 discrete reference files | WOS convention: avg 86 lines/reference; discrete concerns (execution, dispatch, recovery, resumption) each warrant focused guidance | Reference file analysis across all WOS skills |
| Entry script with file-boundary analysis | Deterministic validation enables reliable parallel eligibility checks; follows research skill pattern | Per-skill entry scripts plan; research skill prototype |
| Commit SHA on checkboxes | Creates verifiable rollback targets; detects unreliable checkbox state during resumption | Plan execution research: "don't check without proof" |
| Three-tier verification model | Tests alone miss intent alignment; reasoning verification catches task-pass/plan-fail | Plan execution research: agents achieve 100% task completion but 13% recall |
| Platform-agnostic dispatch | Platform bindings go stale; abstract patterns (worktree isolation, status protocol) are durable | Subagent dispatch research: git worktree is universal mechanism |
| Sequential-by-default | 64.7% vs 45.1% completion rates; parallel opt-in prevents default-path failures | Subagent dispatch research: SWE-bench benchmarks |
| Assume downstream skills exist | wos:validate-plan and wos:finish-work are next in the dependency chain (#161, #162) | Issue dependency chain #157-#164 |

## Acceptance Criteria

From issue #160:

- [ ] SKILL.md written and under 500 lines
- [ ] Skill triggers on "execute", "run the plan", "implement this plan"
- [ ] Approval gate enforced for all 5 status values + missing field
- [ ] Status transitions happen at correct points
- [ ] Checkboxes updated in plan file as tasks complete
- [ ] Git commit after each completed task
- [ ] Multi-session resumption reads plan checkbox state + git log
- [ ] Partially-completed tasks split into done/remaining on failure
- [ ] Parallel mode: file-boundary analysis prevents merge conflicts
- [ ] Parallel mode: subagents use isolated working copies
- [ ] Parallel mode: 3-status protocol (DONE/NEEDS_HELP/BLOCKED)
- [ ] Invokes wos:validate-plan before completing
- [ ] Invokes wos:finish-work after validation passes

Design additions (beyond issue #160):

- [ ] Commit SHA appended to checkbox annotations
- [ ] Entry script: validates status, counts tasks, checks sections
- [ ] Entry script: parses task SHAs for resumption
- [ ] Entry script: file-boundary analysis for parallel eligibility
- [ ] Entry script: --scan mode for finding executing plans
- [ ] Three-tier verification model documented in execution guide
- [ ] Preflight check before entry script invocation
