# Research Skill Consolidation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Consolidate the research skill from 8 reference files (592 instruction lines) to 7 self-contained reference files targeting ≤250 instruction lines, with a clean 9-phase workflow replacing the current 6-phase (with 5.5a/5.5b) structure.

**Architecture:** Flatten the hub-and-spoke structure (where research-workflow.md summarizes every other file) into self-contained reference files that each serve specific phases. Each reference maps to 1-2 phases and loads only when those phases are active — critical for the resume-after-context-reset pattern. The workflow becomes a skeleton with resume detection, phase gates, and write-to-disk checkpoints. Phase renumbering splits old Phase 3 into two (mechanical URL checking vs SIFT judgment) and promotes 5.5a/5.5b to full phases.

**Branch:** `feat/research-skill-consolidation`
**PR:** TBD

---

## Phase Mapping (Old → New)

| Old | New | Name | Change |
|-----|-----|------|--------|
| 1 | 1 | Frame | unchanged |
| 2 | 2 | Gather | unchanged |
| 3 | 3 | Verify Sources | split — mechanical URL checking only |
| — | 4 | Evaluate Sources | split — SIFT judgment, tier classification |
| 4 | 5 | Challenge | renumbered |
| 5 | 6 | Synthesize | renumbered |
| 5.5a | 7 | Self-Verify Claims (CoVe) | promoted to full phase |
| 5.5b | 8 | Citation Re-Verify | promoted to full phase |
| 6 | 9 | Finalize | renumbered |

## File Mapping (Old → New)

| Old File | Disposition | New File |
|----------|------------|----------|
| `research-workflow.md` | Rewrite | `research-workflow.md` (skeleton, deduplicated) |
| `sift-framework.md` | Merge → | `source-quality.md` |
| `source-evaluation.md` | Merge → | `source-quality.md` |
| `source-verification.md` | Merge → | `source-quality.md` |
| `challenge-phase.md` | Rewrite → | `challenge.md` |
| `claim-verification.md` | Rewrite → | `claim-verification.md` (same name, trimmed) |
| `research-modes.md` | Update | `research-modes.md` (phase numbers updated) |
| `python-utilities.md` | Trim | `python-utilities.md` |
| — | Create | `synthesis-guide.md` (extracted from workflow Phase 6) |

## Reference → Phase Mapping

| File | Serves Phases | Loads When Resuming At |
|------|--------------|----------------------|
| `research-workflow.md` | All — skeleton, resume, gates | Always (it's the entry point) |
| `source-quality.md` | 3 (URL verify), 4 (SIFT + tiers) | Phase 3 or 4 |
| `challenge.md` | 5 (assumptions, ACH, premortem) | Phase 5 |
| `synthesis-guide.md` | 6 (confidence, counter-evidence) | Phase 6 |
| `claim-verification.md` | 7 (CoVe), 8 (citation re-verify) | Phase 7 or 8 |
| `research-modes.md` | 1, 4, 5 (mode detection, intensity) | Phase 1, 4, or 5 |
| `python-utilities.md` | 3, 9 (CLI commands) | Phase 3 or 9 |

## Line Budget

Target: ≤250 total instruction lines (SKILL.md body + all references).
Current: 592. Reduction: 58%.

| File | Target | Current Source | Notes |
|------|--------|---------------|-------|
| SKILL.md body | ~85 | 101 | Trim Key Rules that restate references |
| research-workflow.md | ~55 | ~220 | Skeleton only; Phases 3-8 are 3-5 lines each |
| source-quality.md | ~25 | ~125 (3 files) | Compress tiers, trim SIFT prose |
| challenge.md | ~25 | ~70 | Procedures + table templates only |
| synthesis-guide.md | ~15 | (inline in workflow) | Confidence table + writing constraints |
| claim-verification.md | ~25 | ~80 | Procedures + status tables only |
| research-modes.md | ~20 | ~55 | Drop mode descriptions covered by matrix |
| python-utilities.md | ~15 | ~35 | Commands only, drop sample output |
| **Total** | **~265** | **592** | ~15 lines over; spread cuts during execution |

If total exceeds 250 after execution, reassess whether further reference
splits are needed rather than compressing content.

---

## Task 1: Create branch

**Files:** None

**Step 1: Create feature branch**

```bash
git checkout -b feat/research-skill-consolidation
```

**Step 2: Verify clean state**

```bash
git status
```

Expected: clean working tree on new branch.

---

## Task 2: Measure baseline instruction density

**Files:**
- Read: `skills/research/SKILL.md`
- Read: `skills/research/references/*.md`

**Step 1: Record current metrics**

```bash
python3 << 'PYEOF'
from pathlib import Path
from wos.skill_audit import check_skill_sizes, check_skill_meta

summaries, issues = check_skill_sizes(Path('skills'))
for s in summaries:
    if s['name'] == 'research':
        print(f"skill_lines={s['skill_lines']} ref_lines={s['ref_lines']} total={s['total_lines']} words={s['words']}")
        for f in s['files']:
            print(f"  {f}")

meta_issues = check_skill_meta(Path('skills/research'))
for i in meta_issues:
    print(f"  [{i['severity']}] {i['issue']}")
PYEOF
```

Expected: total ~592 instruction lines, 0 meta issues.

Record the exact numbers as the "before" baseline.

---

## Task 3: Create `source-quality.md`

**Files:**
- Read: `skills/research/references/sift-framework.md`
- Read: `skills/research/references/source-evaluation.md`
- Read: `skills/research/references/source-verification.md`
- Create: `skills/research/references/source-quality.md`

Merges three files into one self-contained reference for Phases 3 and 4.

**Step 1: Write `source-quality.md`**

Content structure:

```markdown
# Source Quality Reference

Used during Phase 3 (Verify Sources) and Phase 4 (Evaluate Sources).

## URL Verification (Phase 3)

[From source-verification.md. Include the uv run check_url command
and the 3-tier result handling (drop 404/0, keep 403/5xx, stop if
all removed). ~5 lines.]

## SIFT Steps (Phase 4)

[From sift-framework.md. Four steps: Stop, Investigate, Find better,
Trace. Keep only the agent action bullets — trim the general
"ask yourself" descriptions that Claude already understands. ~8 lines.]

## SIFT Intensity by Mode

[Table from sift-framework.md — keep as-is, compact lookup.]

## Source Hierarchy (T1-T6)

[From source-evaluation.md. Compress each tier to one line:
"T1 — Official docs (Python docs, RFCs, AWS docs)". Drop the
sub-bullets listing what qualifies. ~7 lines.]

## Authority Annotation Format

[From source-evaluation.md. Keep the inline annotation example. ~3 lines.]

## Red Flags

[From source-evaluation.md. Keep bullet list. ~5 lines.]
```

**Target: ~25 instruction lines.**

**Deduplication:** SIFT "Investigate" step references tier classification —
in the merged file, this is just "Classify into tier (see Source Hierarchy
below)" instead of explaining what tiers are.

**Step 2: Verify self-contained**

Read end-to-end. No references to other reference files.

---

## Task 4: Create `challenge.md`

**Files:**
- Read: `skills/research/references/challenge-phase.md`
- Create: `skills/research/references/challenge.md`

Self-contained reference for Phase 5 only.

**Step 1: Write `challenge.md`**

Content structure:

```markdown
# Challenge Reference

Used during Phase 5 (Challenge). Three sub-steps, applied based on
research mode (see research-modes.md for which apply per mode).

## Assumptions Check (All Modes)

[From challenge-phase.md. Keep the 4-step procedure and the output
table template (Assumption | Supporting | Counter | Impact). ~8 lines.]

## Analysis of Competing Hypotheses (Mode-Conditional)

[From challenge-phase.md. Triggered for: deep-dive, options,
competitive, feasibility. Keep the anti-anchoring step, evidence
matrix format (C/I/N), selection rule (fewest inconsistencies).
~10 lines.]

## Premortem (All Modes)

[From challenge-phase.md. Keep the 3-step procedure and output table.
~6 lines.]
```

**Target: ~25 instruction lines.**

**Deduplication:** Remove "When to Run" section (workflow owns timing).
Remove mode-conditional list (research-modes.md owns this).

**Step 2: Verify self-contained**

Read end-to-end. Only external reference is research-modes.md (for
which modes trigger ACH) — this is acceptable since it's a lookup.

---

## Task 5: Create `synthesis-guide.md`

**Files:**
- Read: `skills/research/references/research-workflow.md` (current Phase 5 section)
- Create: `skills/research/references/synthesis-guide.md`

Extracted from the workflow's Phase 5 (becomes Phase 6). Self-contained
reference for the judgment-heavy synthesis phase.

**Step 1: Write `synthesis-guide.md`**

Content structure:

```markdown
# Synthesis Guide

Used during Phase 6 (Synthesize). Organize verified evidence into
findings, annotate confidence, and connect to the user's context.

## Confidence Levels

[Table from current workflow Phase 5: HIGH/MODERATE/LOW criteria.
Keep as-is — it's a compact lookup used inline during writing.]

## Writing Constraints

[From current workflow Phase 5 step 9: every quote, statistic,
attribution, and superlative must be traceable to a cited source.
General observations don't need citations. ~3 lines.]

## Counter-Evidence

[From current workflow: if mode requires counter-evidence, dedicate a
section to arguments that challenge the main findings. ~2 lines.]
```

**Target: ~15 instruction lines.**

This is intentionally small. The synthesis phase is primarily judgment —
Claude knows how to organize findings. This reference provides the
specific constraints (confidence criteria, citation rules) that aren't
obvious.

**Step 2: Verify self-contained**

Read end-to-end. No references to other reference files.

---

## Task 6: Rewrite `claim-verification.md`

**Files:**
- Read: `skills/research/references/claim-verification.md` (current)
- Rewrite: `skills/research/references/claim-verification.md`

Self-contained reference for Phase 7 and Phase 8. Keeps the same
filename but trimmed and renumbered.

**Step 1: Rewrite `claim-verification.md`**

Content structure:

```markdown
# Claim Verification Reference

Used during Phase 7 (Self-Verify Claims) and Phase 8 (Citation
Re-Verify).

## Claim Types

[Keep the 4-type table (quote, statistic, attribution, superlative)
with one-line definitions. ~5 lines.]

## Claims Table Format

[Keep table format and source reference convention. ~4 lines.]

## Resolution Statuses

[Keep the 5-status table (verified, corrected, removed, unverifiable,
human-review). ~6 lines.]

## CoVe Procedure (Phase 7)

[Renumber from Phase 5.5a → Phase 7. Keep the 4-step procedure.
State the critical constraint: CoVe runs WITHOUT the draft document
in context. ~6 lines.]

## Citation Re-Verification (Phase 8)

[Renumber from Phase 5.5b → Phase 8. Keep the 4-step status
assignment procedure. ~5 lines.]

## Contradiction Resolution

[Keep the decision tree. Compress from flowchart-style to a compact
3-line rule: cited source → escalate to Phase 8 → source is
tiebreaker. No source → human-review. ~4 lines.]

## human-review Triggers

[Keep the 4 bullet triggers list. ~4 lines.]
```

**Target: ~25 instruction lines.**

**Deduplication:** Remove phase gate text (workflow owns gates). Remove
the Phase 5.5a/5.5b headers and "Gate out" lines. Keep procedures and
lookup tables only.

**Step 2: Verify self-contained**

Read end-to-end. Phase numbers use new 1-9 scheme. No references to
other reference files.

---

## Task 7: Update `research-modes.md`

**Files:**
- Modify: `skills/research/references/research-modes.md`

**Step 1: Update phase references**

Update any phase number references:
- "Phase 3" → context-dependent (3 or 4 in new scheme)
- "Phase 4" → "Phase 5"
- "Phase 5" → "Phase 6"

Verify mode matrix columns still map correctly:
- "Challenge" → Phase 5
- "Claim Verification" → Phases 7-8

**Step 2: Trim mode descriptions**

The mode descriptions (lines 36-87) repeat information from the matrix
tables. For each mode, check: does the description add anything the
matrix row doesn't already show? If a description only says "High SIFT,
counter-evidence required" and the table already shows that, delete it.

Keep descriptions only when they add methodology guidance not captured
in the matrix (e.g., feasibility's "identify blockers, risks, and
prerequisites").

**Target: ~20 instruction lines** (down from ~55).

---

## Task 8: Trim `python-utilities.md`

**Files:**
- Modify: `skills/research/references/python-utilities.md`

**Step 1: Remove sample output**

Keep the command syntax and brief description. Remove the "Output on
success" and "Output on failure" examples — Claude can interpret
command output without being shown examples.

Remove the Document Model table — this is documented in the codebase
and AGENTS.md, not needed in the research skill reference.

**Target: ~15 instruction lines** (down from ~35).

---

## Task 9: Rewrite `research-workflow.md`

**Files:**
- Rewrite: `skills/research/references/research-workflow.md`
- Read: all new reference files created in Tasks 3-6

This is the largest task. The current file is ~220 instruction lines.
The rewrite makes it a skeleton: resume detection, then each phase
with its write-to-disk checkpoint and a pointer to the relevant
reference. Detail lives in the reference files.

**Step 1: Write the new `research-workflow.md`**

Content structure:

```markdown
# Research Workflow

Nine-phase process. Each phase writes to disk so work survives
context resets.

## Resuming After Context Reset

If `docs/research/{date}-{slug}.md` exists with `<!-- DRAFT -->`,
read it to determine current phase:

- Has `sources:` but no tier annotations → Phase 3
- Has tier annotations but no `## Challenge` → Phase 5
- Has `## Challenge` but no `## Findings` → Phase 6
- Has `## Findings` but no `## Claims` → Phase 7
- Has `## Claims` with `unverified` entries → Phase 8
- Has `## Claims` resolved, still `<!-- DRAFT -->` → Phase 9

Read the document fully before continuing.

## Phase 1: Frame the Question

[Keep: restate question, detect mode, break into 2-4 sub-questions,
confirm with user, declare search protocol. Include the search
protocol JSON initialization. Keep source diversity note.
~15 lines — this phase has no reference file.]

## Phase 2: Gather Sources

[Keep: breadth-first search, 10-20 candidates, log searches as
JSON, fetch failure handling, write initial DRAFT to disk. Include
the DRAFT template (frontmatter + sources table + search protocol
comment). ~20 lines — this phase has no reference file.]

## Phase 3: Verify Sources

Collect URLs from frontmatter. Run URL verification (see
source-quality.md). Drop unreachable (404/0), keep 403/5xx with note.
Update document on disk.
[~3 lines.]

## Phase 4: Evaluate Sources

Apply SIFT at mode's intensity level (see source-quality.md for steps
and intensity table). Classify each source T1-T6. Drop below T5,
never cite T6. Update document on disk with tier annotations.
[~4 lines.]

## Phase 5: Challenge

Run sub-steps based on mode: assumptions check (all), ACH (conditional),
premortem (all). See challenge.md for procedures and output templates.
See research-modes.md for which sub-steps apply. Update document with
## Challenge section.
[~4 lines.]

## Phase 6: Synthesize

Organize findings by sub-question. Annotate confidence levels, include
counter-evidence if mode requires. See synthesis-guide.md for criteria
and writing constraints. Update document with ## Findings section.
Update frontmatter description to reflect actual findings.
[~4 lines.]

## Phase 7: Self-Verify Claims (CoVe)

Extract claims into ## Claims table. Run CoVe WITHOUT the draft
document in context. See claim-verification.md for claim types,
table format, and procedure. Update document on disk.
[~4 lines. Restate the "without draft" constraint here — intentional
duplication for this fragile operation.]

## Phase 8: Citation Re-Verify

Re-fetch cited sources. Check each claim against fetched content.
Assign final statuses. See claim-verification.md for procedure and
statuses. Update document — no unverified claims remain.
[~3 lines.]

## Phase 9: Finalize

[Keep: restructure for lost-in-the-middle convention (summary top,
detail middle, takeaways bottom). Format search protocol as markdown
table. Remove DRAFT marker. Run reindex + audit. Include the quality
checklist updated for 9-phase numbering. ~15 lines.]
```

**Key rules for the rewrite:**
- Phases 3-8: skeleton only (3-5 lines each), point to references
- Phases 1, 2, 9: keep detail inline (no reference file owns this content)
- Every phase states its write-to-disk action
- Phase 7 restates the "no draft in context" constraint

**Target: ~55 instruction lines** (down from ~220).

**Step 2: Verify no content lost**

Cross-check: for every section in the OLD workflow, confirm content
exists in either the new workflow OR one of the 6 reference files.

---

## Task 10: Update `SKILL.md`

**Files:**
- Modify: `skills/research/SKILL.md`

**Step 1: Update frontmatter references**

Replace the references list:

```yaml
references:
  - references/research-workflow.md
  - references/source-quality.md
  - references/challenge.md
  - references/synthesis-guide.md
  - references/claim-verification.md
  - references/research-modes.md
  - references/python-utilities.md
```

(Was 8 entries, now 7.)

**Step 2: Update the phase gates table**

Replace the current table with:

```markdown
| Phase | Gate | How to Verify |
|-------|------|---------------|
| 1. Frame → 2. Gather | User confirmed sub-questions | User said "yes" or equivalent |
| 2. Gather → 3. Verify Sources | DRAFT file exists on disk with `<!-- DRAFT -->` marker | Read the file |
| 3. Verify Sources → 4. Evaluate Sources | URLs checked, unreachable removed from frontmatter | Read the file |
| 4. Evaluate Sources → 5. Challenge | Sources table has Tier + Status columns | Read the file |
| 5. Challenge → 6. Synthesize | `## Challenge` section exists on disk | Read the file |
| 6. Synthesize → 7. Self-Verify Claims | `## Findings` section exists on disk | Read the file |
| 7. Self-Verify Claims → 8. Citation Re-Verify | `## Claims` table populated, CoVe complete | Read the file |
| 8. Citation Re-Verify → 9. Finalize | No `unverified` claims in Claims Table | Read the file |
| 9. Finalize → Done | `<!-- DRAFT -->` removed, audit passes | Run audit |
```

**Step 3: Update Common Deviations**

- "Phase 2" reference — still correct
- "Phase 5 synthesis" → "Phase 6 synthesis"
- "Phase 2" for write-to-disk — still correct

**Step 4: Update Key Rules references**

- `references/sift-framework.md` → `references/source-quality.md`
- `references/source-evaluation.md` → `references/source-quality.md`
- `references/challenge-phase.md` → `references/challenge.md`
- `references/claim-verification.md` → unchanged (same name)
- `references/research-workflow.md` Phase 2 → Phase 2 (unchanged)
- `references/research-workflow.md` Phase 5 → Phase 6

**Step 5: Update examples**

- "Phase 3 (Verify & Evaluate)" → "Phase 4 (Evaluate Sources)"
- "Phase 5" findings excerpt → "Phase 6"
- "Phase 5.5" claims table → "Phase 7"

**Step 6: Trim Key Rules**

Review each rule in the Key Rules section. If a rule only restates
what a reference file already covers (e.g., "SIFT every source"
when source-quality.md defines the full SIFT process), compress to
a one-line pointer. Target: cut ~15 lines from this section.

---

## Task 11: Delete old reference files

**Files:**
- Delete: `skills/research/references/sift-framework.md`
- Delete: `skills/research/references/source-evaluation.md`
- Delete: `skills/research/references/source-verification.md`
- Delete: `skills/research/references/challenge-phase.md`

**Step 1: Verify no remaining references to old filenames**

```bash
grep -r "sift-framework\|source-evaluation\|source-verification\|challenge-phase" skills/research/
```

Expected: no matches. (Matches in CHANGELOG.md or docs/plans/ are
historical — do not update.)

**Step 2: Delete the files**

```bash
git rm skills/research/references/sift-framework.md
git rm skills/research/references/source-evaluation.md
git rm skills/research/references/source-verification.md
git rm skills/research/references/challenge-phase.md
```

Note: `claim-verification.md` is NOT deleted — it was rewritten in
place in Task 6.

---

## Task 12: Verify instruction density

**Files:**
- Read: all files in `skills/research/`

**Step 1: Measure new metrics**

```bash
python3 << 'PYEOF'
from pathlib import Path
from wos.skill_audit import check_skill_sizes, check_skill_meta

summaries, issues = check_skill_sizes(Path('skills'))
for s in summaries:
    if s['name'] == 'research':
        print(f"skill_lines={s['skill_lines']} ref_lines={s['ref_lines']} total={s['total_lines']} words={s['words']}")
        for f in s['files']:
            print(f"  {f}")
        break

meta_issues = check_skill_meta(Path('skills/research'))
for i in meta_issues:
    print(f"  [{i['severity']}] {i['issue']}")

for i in issues:
    if 'research' in i.get('issue', ''):
        print(f"  [{i['severity']}] {i['issue']}")

if not any('research' in i.get('issue', '') for i in issues):
    print("\nNo density warnings!")
PYEOF
```

Expected: total ≤ 250 instruction lines, 0 meta issues.

**If over 250:** Identify which files exceeded their budget. Consider
whether further splitting is needed (e.g., splitting a file that
serves 2 phases into two single-phase files) rather than compressing
content to the point of losing clarity.

**Step 2: Run full test suite**

```bash
uv run python -m pytest tests/ -v
```

Expected: all tests pass.

**Step 3: Run full audit**

```bash
uv run scripts/audit.py --root . --no-urls
```

Expected: no new issues introduced.

---

## Task 13: Commit and push

**Step 1: Stage all changes**

```bash
git add skills/research/
```

**Step 2: Review staged changes**

```bash
git diff --cached --stat
```

Expected: 4 deleted files, 3 new files, 4 modified files.

**Step 3: Commit**

```bash
git commit -m "refactor: consolidate research skill references (9-phase, 7 refs)

- Renumber to clean 9-phase workflow: split Verify & Evaluate into
  Phase 3 (Verify Sources) and Phase 4 (Evaluate Sources); promote
  5.5a/5.5b to Phase 7/8; Finalize becomes Phase 9
- Merge sift-framework + source-evaluation + source-verification
  into source-quality.md
- Rewrite challenge-phase.md as challenge.md (Phase 5 only)
- Extract synthesis-guide.md from workflow Phase 6
- Trim claim-verification.md (Phases 7-8 only)
- Deduplicate workflow to skeleton with resume detection and phase
  gates; detail in self-contained per-phase references
- Update SKILL.md phase gates, examples, and key rules"
```

**Step 4: Push and create PR**

```bash
git push -u origin feat/research-skill-consolidation
```

Create PR against `main`.
