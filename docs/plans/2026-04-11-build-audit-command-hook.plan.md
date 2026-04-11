---
name: /wos:build-command + /wos:audit-command + /wos:build-hook + /wos:audit-hook
description: Add 4 SKILL.md files completing the build/audit family for Claude Code commands and hooks (issue #229)
type: plan
status: executing
branch: feat/build-audit-command-hook
pr: TBD
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# /wos:build-command + /wos:audit-command + /wos:build-hook + /wos:audit-hook

Deliver the final two build/audit pairs — commands and hooks — completing
the five-primitive taxonomy for Claude Code (skills, rules, subagents,
commands, hooks).

## Goal

Users can scaffold well-structured `.claude/commands/<name>.md` files via
`/wos:build-command`, audit existing commands for clarity and overlap via
`/wos:audit-command`, create safety-validated hook scripts with settings
entries via `/wos:build-hook`, and inspect their hooks configuration for
coverage gaps and unsafe patterns via `/wos:audit-hook`. This closes the
build/audit family started in v0.38.0 and provides guided quality tooling
for both Claude Code extension points.

## Scope

**Must have:**
- `skills/build-command/SKILL.md` — scaffolds `.claude/commands/<name>.md`; checks for skill overlap before writing; HARD-GATE before saving
- `skills/audit-command/SKILL.md` — checks description clarity, argument handling, scope creep, and skill overlap
- `skills/build-hook/SKILL.md` — elicits event + handler type + goal; drafts hook artifact + settings.json entry; safety-validates (no destructive ops, idempotent, exit code correctness, async+blocking contradiction); Stop hook loop guard; CVE-2025-59536 security note; rule-overlap check; HARD-GATE before saving
- `skills/audit-hook/SKILL.md` — reads settings.json hooks; six checks: PreToolUse coverage, script safety, async+blocking contradiction, Stop hook loop risk, rule overlap, idempotency
- All 4 skills pass `python scripts/lint.py --root .` quality checks
- All 4 skills include a `## Handoff` section

**Won't have:**
- Python validator code for commands or hooks (skill is LLM-only instructions)
- Changes to `wos/validators.py` or `scripts/lint.py` (no automated checks added in this issue)
- Automated tests for skill behavior (skills are tested by invocation)
- A `/wos:build-settings` or similar settings management skill (out of scope)
- Deprecation of any existing skill

## Approach

Four SKILL.md files, no Python changes. Each skill is a pure LLM instruction
document following the conventions in `skills/lint/references/skill-authoring-guide.md`.
Tasks 1–2 (command pair) and Tasks 3–4 (hook pair) are independent and can
be authored in either order; each task verifies lint before committing.
The command pair outputs user-authored artifacts (`.claude/commands/`);
the hook pair interacts with `.claude/settings.json` and shell scripts.
Both build skills include a HARD-GATE: present the draft to the user before
writing any file to disk.

## File Changes

| File | Action | Notes |
|------|--------|-------|
| `skills/build-command/SKILL.md` | Create | Full skill definition — intake, overlap check, draft, review gate, save |
| `skills/audit-command/SKILL.md` | Create | Full skill definition — 4 checks, report |
| `skills/build-hook/SKILL.md` | Create | Full skill definition — elicit, draft, safety check, rule overlap, review gate, save |
| `skills/audit-hook/SKILL.md` | Create | Full skill definition — 4 checks, report |

No other files changed. Reindex runs automatically in validation.

---

## Chunk 1: Command pair

### Task 1 — `skills/build-command/SKILL.md`

Scaffold a `.claude/commands/<name>.md` with overlap detection and a
user-approval gate before writing.

**Files:**
- Create: `skills/build-command/SKILL.md`

**Required content:**

Frontmatter:
```yaml
---
name: build-command
description: >
  Scaffolds a Claude Code slash command file (.claude/commands/<name>.md)
  with description, argument handling, and prompt body. Use when the user
  wants to "create a command", "build a slash command", "scaffold a command",
  "add a custom /command", or needs a reusable prompt template.
argument-hint: "[command name] [purpose description]"
user-invocable: true
---
```

Required sections (in order):
1. `## Intake` — elicit command name, purpose, and optional argument hint; ask one question at a time
2. `## Overlap Check` — read `skills/*/SKILL.md` frontmatter names and `.claude/commands/` if it exists; if the proposed command duplicates an existing skill or command, surface the overlap and ask the user whether to proceed or rename
3. `## Draft` — produce `.claude/commands/<name>.md` with: YAML frontmatter (`description`, `argument-hint`), a clear prompt body, `$ARGUMENTS` placeholder for user-supplied input, and 1–2 inline usage examples
4. `## Review Gate` — present the draft in full; wait for explicit user approval before writing to disk; do not write anything before this gate passes
5. `## Save` — write the approved draft to `.claude/commands/<name>.md`; confirm the path to the user
6. `## Handoff` — Receives/Produces/Chainable-to

The HARD-GATE instruction must be present in `## Review Gate`:
> Present the draft and wait for user approval before writing any file to disk.

- [x] Create `skills/build-command/SKILL.md` with all six sections and compliant frontmatter <!-- sha:bf897d9 -->
- [x] Verify: markers present, lint clean <!-- sha:bf897d9 -->
- [x] Commit: `feat: add /wos:build-command skill` <!-- sha:bf897d9 -->

---

### Task 2 — `skills/audit-command/SKILL.md`

Audit `.claude/commands/` files for quality and redundancy.

**Files:**
- Create: `skills/audit-command/SKILL.md`

**Required content:**

Frontmatter:
```yaml
---
name: audit-command
description: >
  Audits Claude Code slash commands for description clarity, argument
  handling, scope creep, and overlap with existing skills. Use when the
  user wants to "audit commands", "review a command", "check commands",
  "improve a command", or "find redundant commands".
argument-hint: "[command name | path to command file]"
user-invocable: true
---
```

Required sections (in order):
1. `## Input` — accept a single command name (reads `.claude/commands/<name>.md`) or scan all files in `.claude/commands/` if no argument given; if `.claude/commands/` does not exist, report that and exit
2. `## Checks` — four named checks, each with description and example finding:
   - **Description clarity:** does the frontmatter `description` clearly state what the command does and when to use it?
   - **Argument handling:** is `$ARGUMENTS` used? are edge cases (no argument, unexpected input) handled or noted?
   - **Scope creep:** does the command do multiple unrelated things? (signal: conjunctions in the description, multiple unrelated `$ARGUMENTS` uses)
   - **Skill overlap:** does this duplicate a `/wos:skill`? read `skills/*/SKILL.md` names and descriptions to check
3. `## Report` — present findings per command in a table (command | check | finding | severity); include a summary count; if no issues found, confirm clean
4. `## Handoff` — Receives/Produces/Chainable-to

- [x] Create `skills/audit-command/SKILL.md` with all four sections and compliant frontmatter <!-- sha:2f98c9a -->
- [x] Verify: 4 checks present, lint clean <!-- sha:2f98c9a -->
- [x] Commit: `feat: add /wos:audit-command skill` <!-- sha:2f98c9a -->

---

## Chunk 2: Hook pair

### Task 3 — `skills/build-hook/SKILL.md`

Scaffold a Claude Code hook script + settings.json entry, with safety
validation and a user-approval gate before writing.

**Files:**
- Create: `skills/build-hook/SKILL.md`

**Required content:**

Frontmatter:
```yaml
---
name: build-hook
description: >
  Builds a Claude Code hook (event-driven quality gate) with a shell script
  and the corresponding settings.json hooks entry. Use when the user wants
  to "create a hook", "add a PostToolUse hook", "build a hook", "enforce
  quality on tool use", "set up automated quality gates", or "run a script
  after tool use".
argument-hint: "[hook event] [enforcement goal]"
user-invocable: true
---
```

Required sections (in order):
1. `## Elicit` — ask which hook event and what to enforce; one question at a time; confirm the enforcement goal in one sentence before drafting. Include the full documented event list for reference:
   - **Tool execution:** PreToolUse (fires before; can block), PostToolUse (fires after; cannot prevent execution), PostToolUseFailure
   - **Session lifecycle:** SessionStart, SessionEnd, UserPromptSubmit, PreCompact, PostCompact
   - **Agent coordination:** Stop, SubagentStop, SubagentStart
   - **Permission:** Notification (observability only), PermissionRequest, PermissionDenied
   Also ask which handler type: `command` (shell script), `http` (POST to endpoint), `prompt` (single-turn LLM evaluation), or `agent` (multi-turn subagent). Default to `command` for enforcement goals.
2. `## Draft` — produce two artifacts:
   - The hook artifact (shell script `#!/bin/bash` for `command` type, or equivalent for other types)
   - A `settings.json` `hooks:` entry snippet in the documented format:
     ```json
     { "hooks": { "PreToolUse": [{ "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": "/path/to/hook.sh", "timeout": 60 }] }] } }
     ```
   Include the `matcher` field (pipe-separated tool names, wildcard `*`, or regex) when the event is tool-scoped. Note: if the goal is to *block* something, the hook must use PreToolUse — PostToolUse fires after execution and cannot prevent it.
3. `## Safety Check` — verify the draft against four criteria:
   - **No destructive operations:** flag `rm -rf`, `git reset --hard`, `git checkout .`, `git push --force`
   - **Idempotent:** running the hook twice produces the same result (no state accumulation, no unbounded log appending)
   - **No unintended side effects** beyond the enforcement goal
   - **Exit code correctness:** blocking hooks must use `exit 2`; `exit 1` is non-blocking (shown in transcript, execution continues); `async: true` hooks can never block regardless of exit code — flag this combination as a bug
   If any criterion fails, revise before proceeding
4. `## Stop Hook Guard` — if the event is Stop or SubagentStop: the script must check `stop_hook_active` from stdin and exit 0 if true, to prevent an infinite loop. Draft this guard into the script. Example pattern:
   ```bash
   HOOK_ACTIVE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('stop_hook_active','false'))")
   [ "$HOOK_ACTIVE" = "True" ] && exit 0
   ```
   For non-Stop events, omit this section.
5. `## Security Note` — remind the user that `.claude/settings.json` is a repository file (CVE-2025-59536): any collaborator with commit access can inject malicious hooks that execute arbitrary commands. Treat hook changes in settings.json with the same code-review scrutiny as executable source files.
6. `## Rule Overlap` — check CLAUDE.md for instructions that already express the same enforcement goal; if overlap found, note it and ask the user whether the hook is still needed or adds enforcement teeth (hooks are deterministic; CLAUDE.md is advisory)
7. `## Review Gate` — present both artifacts (hook + settings snippet) in full; wait for user approval; do not write anything before this gate passes
8. `## Save` — write the approved hook to `.claude/hooks/<name>.sh` (or user-specified path); show the `settings.json` patch to apply manually (do not auto-patch settings.json — it may contain existing permission entries)
9. `## Handoff` — Receives/Produces/Chainable-to

The HARD-GATE instruction must be present in `## Review Gate`.
The `## Safety Check` section must explicitly name idempotency and exit code 2.
The `## Stop Hook Guard` section must be present and include the `stop_hook_active` check pattern.

- [x] Create `skills/build-hook/SKILL.md` with all nine sections and compliant frontmatter <!-- sha:a1b1c0e -->
- [x] Verify: all markers present, PreToolUse/PostToolUse distinction, CVE note, lint clean <!-- sha:a1b1c0e -->
- [x] Commit: `feat: add /wos:build-hook skill` <!-- sha:a1b1c0e -->

---

### Task 4 — `skills/audit-hook/SKILL.md`

Audit a project's hooks configuration for coverage gaps, unsafe patterns,
redundancy, and idempotency issues.

**Files:**
- Create: `skills/audit-hook/SKILL.md`

**Required content:**

Frontmatter:
```yaml
---
name: audit-hook
description: >
  Audits Claude Code hooks configuration for event coverage, script safety,
  rule overlap, and idempotency. Use when the user wants to "audit hooks",
  "check hooks", "review hooks", "check my hooks", "what quality gates are
  missing", or "are my hooks safe".
argument-hint: "[settings.json path]"
user-invocable: true
---
```

Required sections (in order):
1. `## Input` — read `.claude/settings.json` and `.claude/settings.local.json` hooks sections (both if present); if neither exists or neither has a `hooks:` key, report "No hooks configured" as a finding before running checks
2. `## Checks` — six named checks, each with description, signal, and example finding:
   - **Event coverage:** Is a PreToolUse hook present for blocking enforcement? PreToolUse is the only event that can block execution (exit code 2). PostToolUse fires after execution and cannot prevent it — a PostToolUse hook with blocking intent is a misconfiguration. Flag the absence of any PreToolUse hook as `warn`.
   - **Script safety:** For each hook command, check for destructive operations (`rm -rf`, `git reset --hard`, `git checkout .`, `git push --force`). Flag as `fail`.
   - **Async + blocking contradiction:** If a hook has `"async": true` but its script contains `exit 2` logic (or is described as a blocker), flag as `fail` — async hooks execute in the background and can never block regardless of exit code.
   - **Stop hook loop risk:** For any Stop or SubagentStop hook, check whether the script guards against `stop_hook_active`. A Stop hook that exits 2 without this check traps Claude in an infinite loop. Flag its absence as `fail`.
   - **Rule overlap:** Does the hook duplicate an instruction already in CLAUDE.md? Overlap is redundant; note it as `warn` — the rule and hook may both be intentional (belt-and-suspenders) or one may be stale.
   - **Idempotency:** Does the hook modify state in a non-idempotent way? (e.g., appending to a log file unboundedly, incrementing a counter). Flag as `warn`.
3. `## Report` — present findings in a table (hook event | check | finding | severity); summary count at top; if no issues found, confirm "Hooks look well-configured."
4. `## Handoff` — Receives/Produces/Chainable-to

The event coverage check must fire even when no hooks are configured at all.

- [x] Create `skills/audit-hook/SKILL.md` with all four sections and compliant frontmatter <!-- sha:8f32a3b -->
- [x] Verify: 6 checks present, PreToolUse/PostToolUse distinction, stop_hook_active guard, lint clean <!-- sha:8f32a3b -->
- [x] Commit: `feat: add /wos:audit-hook skill` <!-- sha:8f32a3b -->

---

## Validation

```bash
# 1. All four skills exist
ls skills/build-command/SKILL.md skills/audit-command/SKILL.md \
   skills/build-hook/SKILL.md skills/audit-hook/SKILL.md
# Expected: all four paths listed

# 2. All four have ## Handoff sections
grep -L "## Handoff" skills/build-command/SKILL.md skills/audit-command/SKILL.md \
  skills/build-hook/SKILL.md skills/audit-hook/SKILL.md
# Expected: empty (all have the section)

# 3. No lint failures for the new skills
python scripts/lint.py --root .
# Expected: zero failure-severity issues for any of the four new skills

# 4. audit-hook covers the no-hooks-configured case
grep -iE "No hooks|not configured|no.*hooks" skills/audit-hook/SKILL.md
# Expected: match found

# 5. audit-hook has all six checks including the two new ones
grep -E "Async.*blocking|Stop hook|stop_hook_active" skills/audit-hook/SKILL.md
# Expected: matches found

# 6. build-hook has stop_hook_active guard and exit code semantics
grep -E "stop_hook_active|exit 2" skills/build-hook/SKILL.md
# Expected: matches found

# 7. build-hook has CVE security note
grep -i "CVE\|attack surface\|code.review\|executable" skills/build-hook/SKILL.md
# Expected: match found

# 8. Full test suite unaffected
python -m pytest tests/ -v
# Expected: zero failures

# 9. Reindex clean
python scripts/reindex.py --root .
python scripts/lint.py --root . --no-urls
# Expected: no index sync failures
```

## Notes

- `.claude/settings.json` vs. `.claude/settings.local.json`: Claude Code writes
  permission approvals to `settings.local.json`. The `hooks:` key can live in
  either. `build-hook` instructs users to apply the patch manually rather than
  auto-patching — this avoids clobbering existing permission entries.
- Hook events (full set from docs): tool-execution (PreToolUse, PostToolUse,
  PostToolUseFailure), session lifecycle (SessionStart, SessionEnd,
  UserPromptSubmit, PreCompact, PostCompact), agent coordination (Stop,
  SubagentStop, SubagentStart), permission (Notification, PermissionRequest,
  PermissionDenied). Only PreToolUse can block via exit code 2.
- `async: true` disables blocking regardless of exit code. Hooks intended to
  enforce must be synchronous (default).
- `audit-command` scope: audits `.claude/commands/` only, not WOS skills. If
  a user wants to audit a skill, that is `/wos:audit-skill` (Task 10, separate
  worktree).
- Roadmap tracker: update Task 14 checkbox in
  `docs/plans/2026-04-10-roadmap-v036-v039.plan.md` with merge commit SHA when
  this PR lands.
