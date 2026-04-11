---
name: WORKFLOW.md Lifecycle Guide
description: Create WORKFLOW.md at project root documenting the canonical WOS workflows — development lifecycle, knowledge management, self-improvement loop, skill chain design, and primitive taxonomy.
type: plan
status: completed
branch: feat/workflow-doc
pr: ~
related:
  - docs/plans/2026-04-10-roadmap-v036-v039.plan.md
---

# WORKFLOW.md Lifecycle Guide

Close issue bcbeidel/wos#232: create `WORKFLOW.md` at the project root.

## Goal

Write a `WORKFLOW.md` that makes WOS understandable as a coherent system — showing
how its skills connect across five workflow patterns: development lifecycle,
knowledge management lifecycle, self-improvement loop, skill chain design, and a
primitive taxonomy table. Target audience is a developer orienting to WOS for
the first time, and an agent resuming work with zero conversation context.

## Scope

### Must have

- `WORKFLOW.md` at project root with WOS frontmatter
- Five sections matching the issue spec: development lifecycle, knowledge
  management lifecycle, self-improvement loop, skill chain design, primitive
  taxonomy table
- Text chain diagrams at each lifecycle section showing skill sequence
- Gate/decision descriptions at each lifecycle arrow
- Every active skill appears in at least one section (see list in Tasks)
- Passes `python scripts/lint.py --root . --no-urls`

### Won't have

- New Python code, tests, or scripts — documentation only
- Changes to any existing SKILL.md, OVERVIEW.md, or other file
- `/wos:audit` skill implementation — that is Task 17 (issue #231), parallel work
- `challenge`, `principles`, `report-issue` skill implementations — not present
  in the v0.38.x skills directory; if they exist at ship time, add them

## Approach

`WORKFLOW.md` complements `OVERVIEW.md`. OVERVIEW.md describes *layers*;
WORKFLOW.md shows *how to work* — which skills to invoke, in what order, with
what gates between them.

The document is agent-facing as well as human-facing. Key insight goes first and
last; reference detail in the middle.

**Section design:**

1. **Development lifecycle** — primary pipeline (`brainstorm → write-plan →
   execute-plan → validate-work → finish-work`) with supporting skills
   (`consider`, `refine-prompt`, `challenge`) as annotated side-uses at
   appropriate stages.

2. **Knowledge management lifecycle** — two paths: fast path (`ingest`) and
   high-rigor path (`research → distill → ingest`). Followed by `lint` as the
   ongoing health check. Include `setup` as the prerequisite that creates the
   required directory structure.

3. **Self-improvement loop** — `/wos:audit` as the entry point (coming in
   v0.39.0 Task 17, shipped in the same release). Identify gaps → apply the
   appropriate build/audit pair → `/wos:audit-chain` to validate chains are
   clean.

4. **Skill chain design** — `/wos:audit-chain` dual-mode: goal → manifest
   creation, manifest → repair loop. Reference `*.chain.md` as the artifact.

5. **Primitive taxonomy table** — the table from the issue spec, expanded with
   `build-subagent`/`audit-subagent` and `build-command`/`audit-command`
   /`build-hook`/`audit-hook` rows.

**Active skills to cover (all must appear in at least one section):**
`setup`, `lint`, `research`, `distill`, `ingest`, `brainstorm`, `write-plan`,
`execute-plan`, `validate-work`, `finish-work`, `refine-prompt`, `consider`,
`audit`, `audit-chain`, `build-skill`, `audit-skill`, `build-rule`,
`audit-rule`, `build-subagent`, `audit-subagent`, `build-command`,
`audit-command`, `build-hook`, `audit-hook`

**Deprecated skills** (`retrospective`, `check-rules`, `extract-rules`) get a
single footnote line — no lifecycle sections of their own.

## File Changes

| Action | File |
|--------|------|
| Create | `WORKFLOW.md` |

## Tasks

### Task 1 — Read skill handoff contracts

Read the `## Handoff` section from each active skill's SKILL.md. Capture what
each skill receives and produces — this informs the gate descriptions at
lifecycle arrows.

Skills to read (from `skills/*/SKILL.md`):
`brainstorm`, `write-plan`, `execute-plan`, `validate-work`, `finish-work`,
`research`, `distill`, `ingest`, `lint`, `setup`, `refine-prompt`,
`audit-chain`, `build-skill`, `audit-skill`, `build-rule`, `audit-rule`,
`build-subagent`, `audit-subagent`, `build-command`, `audit-command`,
`build-hook`, `audit-hook`

**Verification:** All handoff contracts reviewed before writing begins.
No commit — reading only.

### Task 2 — Write WORKFLOW.md

Create `WORKFLOW.md` at the project root with WOS frontmatter and all five
sections. Each lifecycle section must:
- Open with a text chain diagram showing the skill sequence
- Follow with a short description of each arrow's gate or decision point
- Name every skill used in that path

**Content requirements:**
- Development lifecycle: full pipeline + `consider` at brainstorm/design stage,
  `refine-prompt` for prompt/plan quality review
- Knowledge management: `setup` (prerequisite), fast path via `ingest`, high-
  rigor path via `research → distill → ingest`, `lint` for ongoing validation
- Self-improvement loop: `/wos:audit` → gap identification → build/audit pair
  → `/wos:audit-chain` → clean
- Skill chain design: `/wos:audit-chain` dual-mode (goal → manifest, manifest
  → repair loop)
- Primitive taxonomy: table from issue spec + subagent, command, hook rows

**Verification:**
```bash
# File exists
ls WORKFLOW.md

# All active skills mentioned
for skill in setup lint research distill ingest brainstorm write-plan \
  execute-plan validate-work finish-work refine-prompt consider audit \
  audit-chain build-skill audit-skill build-rule audit-rule build-subagent \
  audit-subagent build-command audit-command build-hook audit-hook; do
  grep -q "$skill" WORKFLOW.md || echo "MISSING: $skill"
done
# Expected: no output

# All five required sections present
for section in "Development lifecycle" "Knowledge management" \
  "Self-improvement" "Skill chain design" "Primitive taxonomy"; do
  grep -qi "$section" WORKFLOW.md || echo "MISSING SECTION: $section"
done
# Expected: no output
```

**Commit:**
```bash
git add WORKFLOW.md
git commit -m "feat: add WORKFLOW.md lifecycle guide (closes #232)"
```

### Task 3 — Run lint and fix issues

```bash
python scripts/lint.py --root . --no-urls
```

Fix any failures. Common issues: missing `name`/`description` frontmatter,
content length outside 100–800 words if WORKFLOW.md is picked up as a context
document, index sync errors.

**Verification:**
```bash
python scripts/lint.py --root . --no-urls
# Expected: zero failures; warnings acceptable
```

**Commit:** only if lint fixes were required:
```bash
git add WORKFLOW.md
git commit -m "fix: address lint issues in WORKFLOW.md"
```

### Task 4 — Update roadmap Task 18 checkbox

After the PR merges, update `docs/plans/2026-04-10-roadmap-v036-v039.plan.md`
Task 18 checkbox with the merge commit SHA:

```markdown
- [x] Task 18: Implement #232 — `WORKFLOW.md` at project root covering development
  lifecycle, knowledge management lifecycle, self-improvement loop, and primitive
  taxonomy table <!-- sha:MERGE_SHA -->
```

This task executes on `main` after merge, not on the feature branch.

**Verification:**
```bash
grep "Task 18" docs/plans/2026-04-10-roadmap-v036-v039.plan.md
# Expected: `- [x] Task 18: ...` with sha filled in
```

**Commit:**
```bash
git add docs/plans/2026-04-10-roadmap-v036-v039.plan.md
git commit -m "chore: mark roadmap Task 18 complete"
```

## Validation

```bash
# WORKFLOW.md exists at project root
ls WORKFLOW.md
# Expected: WORKFLOW.md

# All active skills are mentioned
for skill in setup lint research distill ingest brainstorm write-plan \
  execute-plan validate-work finish-work refine-prompt consider audit \
  audit-chain build-skill audit-skill build-rule audit-rule build-subagent \
  audit-subagent build-command audit-command build-hook audit-hook; do
  grep -q "$skill" WORKFLOW.md || echo "MISSING: $skill"
done
# Expected: no output

# All five required sections present
for section in "Development lifecycle" "Knowledge management" \
  "Self-improvement" "Skill chain design" "Primitive taxonomy"; do
  grep -qi "$section" WORKFLOW.md || echo "MISSING SECTION: $section"
done
# Expected: no output

# Lint passes
python scripts/lint.py --root . --no-urls
# Expected: zero failures
```
