---
name: check-subagent
description: >
  Audits Claude Code custom subagent definitions against deterministic
  Tier-1 checks (location, frontmatter shape, naming, `tools`
  hygiene, prompt size, body structure, secret patterns) and seven
  judgment dimensions (scope discipline, routing-description quality,
  tool proportionality, output contract, voice & framing, failure
  behavior, injection surface). Use when the user wants to "audit a
  subagent", "check my agents", "review agent permissions", "validate
  a subagent definition", or "are my subagents well-formed". Not for
  skills (route to `/build:check-skill`), hooks (route to
  `/build:check-hook`), or rules (route to `/build:check-rule`).
argument-hint: "[path]"
user-invocable: true
references:
  - ../../_shared/references/subagents-best-practices.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
---

# Check Subagent

Audit Claude Code custom subagent definitions for structural
soundness, tool-scope hygiene, routing-contract clarity, and safety
posture. The rubric — what makes a subagent load-bearing, the file
anatomy, the patterns that work — lives in
[subagents-best-practices.md](../../_shared/references/subagents-best-practices.md).
This skill is the audit workflow; the principles doc is what it
audits against.

The audit runs in three tiers. **Tier-1** is deterministic — seven
shell scripts run per target and emit fixed-format findings.
**Tier-2** is a single locked-rubric LLM call per target evaluating
all seven [audit dimensions](references/audit-dimensions.md) at once;
dimensions that do not apply return PASS silently. **Tier-3** is
cross-entity collision detection — when the scope holds multiple
subagents in the same directory, pairwise description similarity
flags overlapping routing surface.

Read-only by default. The opt-in repair loop applies fixes only after
per-finding confirmation.

## Workflow

1. Scope → 2. Tier-1 Deterministic Checks → 3. Tier-2 Judgment
Checks → 4. Tier-3 Description Collision → 5. Report → 6. Opt-In
Repair Loop.

### 1. Scope

Read `$ARGUMENTS`:

- **Single path to a `.md` file under an `agents/` directory** —
  audit that file.
- **Directory path** — walk the directory, audit every `.md` file at
  the top level. Do not recurse — subagent definitions are top-level
  by convention.
- **Empty** — default to `.claude/agents/` in the current working
  directory. If it does not exist or is empty, state the absence and
  exit.

Confirm the scope aloud before proceeding ("Auditing <path> (N
subagent(s) found)").

### 2. Tier-1 Deterministic Checks

Run seven scripts in sequence against each target. Each exits `0` on
clean / WARN / INFO / HINT and `1` on one or more FAIL; do not stop
on any script's FAIL — all seven contribute to the merged report.

```bash
SCRIPTS="${SKILL_DIR}/scripts"   # resolved by Claude at invocation
TARGETS="$ARGUMENTS"

bash "$SCRIPTS/check_secrets.sh"     $TARGETS   # FAIL: secret patterns — excludes from Tier-2
bash "$SCRIPTS/check_location.sh"    $TARGETS   # FAIL: wrong directory / wrong extension
bash "$SCRIPTS/check_frontmatter.sh" $TARGETS   # FAIL: missing delimiter / name / description; description >1024 chars
bash "$SCRIPTS/check_naming.sh"      $TARGETS   # FAIL: name ≠ filename stem; WARN: non-kebab-case; HINT: generic filename
bash "$SCRIPTS/check_tools.sh"       $TARGETS   # FAIL: wildcard tool entry; WARN: omitted tools / Agent listed / parallel-write risk
bash "$SCRIPTS/check_size.sh"        $TARGETS   # WARN: body ≥6,000 chars (~1,500 tokens); FAIL: ≥12,000 chars (~3,000 tokens)
bash "$SCRIPTS/check_structure.sh"   $TARGETS   # WARN: no body headings; INFO: scope section absent
```

The scripts live next to `SKILL.md` under `scripts/` and are
executable. Claude resolves `${SKILL_DIR}` from the skill's own
directory at invocation time — hooks use `$CLAUDE_PLUGIN_ROOT`, but
skills do not.

**Script-to-check map:**

| Script | Checks |
|---|---|
| `check_secrets.sh` | API key / token / private-key-header patterns in frontmatter and body; wraps `gitleaks` when present, falls back to inline regex when absent |
| `check_location.sh` | File is under `.claude/agents/`, `~/.claude/agents/`, or `plugins/<plugin>/agents/`; extension is `.md` |
| `check_frontmatter.sh` | `---`-delimited YAML block present at file head; `name` and `description` keys present and non-empty; `description` ≤1,024 chars (spec truncation cap); plugin-subagent no-op detection (`permissionMode`/`hooks`/`mcpServers` set in a plugin path); `memory:` + narrow `tools` implicit Read/Write/Edit expansion |
| `check_naming.sh` | `name` is kebab-case (`^[a-z][a-z0-9]*(-[a-z0-9]+)*$`); filename stem equals `name`; filename is not generic (`agent.md`, `helper.md`) |
| `check_tools.sh` | `tools` declared explicitly; no wildcards (`*`, `all`, `all_tools`); `Agent` not listed in a subagent-scope definition; `background: true` + Write/Edit without `isolation: worktree` |
| `check_size.sh` | Body character count — WARN ≥6,000 chars (~1,500 tokens), FAIL ≥12,000 chars (~3,000 tokens) |
| `check_structure.sh` | Body has at least one `##` heading; presence of a Scope / Out-of-scope heading |

**Exit-code contract every script honors:** `0` on clean / WARN /
INFO / HINT-only; `1` on one or more FAIL; `64` on argument error;
`69` on missing optional dependency (e.g., `gitleaks`) — coverage
degrades gracefully.

**FAIL findings that exclude the file from Tier-2:**

- Any `check_secrets.sh` FAIL (secrets present — evaluation unsafe).
- `check_location.sh` FAIL (file is not a subagent definition).
- `check_frontmatter.sh` FAIL on missing delimiter or missing
  `name` / `description` (the routing contract does not exist).
- `check_tools.sh` wildcard FAIL (effective tool set is unresolvable).

**FAIL findings that do NOT exclude from Tier-2:** description
over-length, name-stem mismatch, body-size hard-fail — the file is
still parseable and the judgment rubric can evaluate productively.

**WARN / INFO / HINT findings never exclude.** They surface in the
report alongside Tier-2 findings.

### 3. Tier-2 Judgment Checks

For each file that passed the Tier-2-exclusion filter, make a single
LLM call against the rubric in
[audit-dimensions.md](references/audit-dimensions.md). All seven
dimensions run together — no trigger gating. A dimension that does
not apply (e.g., D7 Injection Surface on a subagent that does not
interpolate user input) returns PASS silently.

The seven dimensions:

| Dimension | What it judges |
|---|---|
| D1 Scope Discipline | Single responsibility; scope and out-of-scope stated explicitly; workflow does not mix unrelated concerns |
| D2 Description as Router Prompt | Verb-phrase capability opener; explicit trigger conditions; at least one exclusion; stated return/output; proactive-invocation signal when the workflow implies self-delegation |
| D3 Tool Proportionality | Effective tool set matches the described workflow; `Bash` / `Write` / `Edit` grants carry body-level scoping; path constraints on file-modifying tools where the tool supports them |
| D4 Output Contract | Output format is mandated and machine-parsable; one concrete example supplied at points of genuine ambiguity |
| D5 Voice & Framing | Imperative mood throughout; consistent terminology; no hedging (`try your best`, `if possible`, `might want to`) or apology language |
| D6 Failure Behavior | Explicit handling for blockers (bad input, missing access, ambiguous request); deterministic exit — no silent workarounds |
| D7 Injection Surface | User input not interpolated raw into the prompt; external text treated as data, not instructions |

Feed the file contents (and any Tier-1 HINT lines — none currently
emitted by the default script set) into the prompt. Parse the
response into the fixed lint format (one finding per dimension at
most; PASS produces no finding).

### 4. Tier-3 Description Collision

When the scope holds multiple subagent files, run description
collision detection:

```bash
bash "$SCRIPTS/check_collision.sh" $TARGETS   # WARN: pairwise description Jaccard ≥0.6
```

Pairwise token-set Jaccard similarity across every
`.claude/agents/*.md` pair; flag any pair scoring ≥0.6 as a
routing-collision risk. Overlapping descriptions produce
non-deterministic routing — the main agent has no basis to pick
between two agents that claim the same trigger surface.

Report collisions as WARN findings, named pairwise (`file-a.md`
vs. `file-b.md`, similarity 0.71). Single-file scope skips this tier.

### 5. Report

Emit a unified findings table sorted by severity (FAIL > WARN > INFO
> HINT), then by file path, then by check. Summary line at top and
bottom:

```
N fail, N warn, N info across N subagent(s)
```

Lint format:

```
SEVERITY  <path> — <check>: <detail>
  Recommendation: <specific change>
```

If any file was excluded from Tier-2, name it and the exclusion-
trigger finding.

### 6. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated
> finding numbers."

For each selected finding, follow the recipe in
[repair-playbook.md](references/repair-playbook.md):

1. Read the relevant section of the target file.
2. Propose a minimal specific edit — fix the finding without
   restructuring surrounding content.
3. Show the diff.
4. Write the change only on explicit user confirmation.
5. Re-run the Tier-1 script (or the relevant Tier-2 dimension) that
   produced the finding; confirm the fix holds.

Per-change confirmation is non-negotiable. Bulk application removes
the user's ability to review individual edits. Canonical-category
findings (spec-documented FAILs) should be applied first;
judgment-dimension findings may be skipped without regret.

## Anti-Pattern Guards

1. **Running Tier-2 before Tier-1** — deterministic checks are cheap
   and authoritative; running them first avoids spending LLM calls on
   files that should have been excluded.
2. **Trigger-gating Tier-2 dimensions** — all seven dimensions run on
   every non-excluded file. A dimension that doesn't apply returns
   PASS silently. Conditional dimensions produce inconsistent
   rubrics across runs.
3. **Applying all repair fixes in one batch** — per-finding
   confirmation is required.
4. **Recursing into agent subdirectories** — subagent definitions
   are top-level by convention. Recursion pulls in unrelated `.md`
   files the rubric does not model.
5. **Skipping Tier-3 on multi-file scope** — description-collision
   detection is cheap and catches a documented failure mode that no
   single-file check can see.
6. **Silent-pass on generic filenames** — `agent.md` or `helper.md`
   are HINT-level under `check_naming.sh`; surface them rather than
   dropping them from the report.
7. **Flagging broad tool sets by absolute count** — Tool
   Proportionality anchors to the workflow description, not a fixed
   allowlist ceiling.

## Key Instructions

- Tier-1 scripts run first and always. Tier-2 runs only on files
  that passed the Tier-2-exclusion filter.
- All seven Tier-2 dimensions are evaluated on every non-excluded
  file. A dimension that does not apply returns PASS silently.
- Repairs require per-finding confirmation — each change writes
  individually and waits for explicit approval before the next.
- When a Tier-1 script reports a missing optional dependency (exit
  69 from `check_secrets.sh` without `gitleaks`), surface the
  dependency name and install hint; the audit continues with the
  regex fallback.
- Won't modify files without per-change confirmation — the audit is
  read-only by default.
- Won't audit paths outside `$ARGUMENTS` — the scope the user named
  is the only scope.
- Won't audit `.md` files outside an `agents/` directory — route
  other `.md` audits to `/build:check-skill` (for SKILL.md) or
  `/build:check-rule` (for rules).
- Recovery if a repair edit produces a worse state: the edit is a
  single file change; revert with `git checkout -- <path>` or the
  editor's undo.

## Handoff

**Receives:** Path to a single subagent definition (a `.md` file
under an `agents/` directory) or a directory holding such files at
the top level. Empty `$ARGUMENTS` defaults to `.claude/agents/`.
**Produces:** Structured findings table in the lint format
(`SEVERITY  <path> — <check>: <detail>` with a `Recommendation:`
follow-up line); optionally, targeted edits applied after
per-finding confirmation.
**Chainable to:** `/build:build-subagent` (rebuild or respec after
flagged repairs when the findings surface structural issues bigger
than point fixes).
