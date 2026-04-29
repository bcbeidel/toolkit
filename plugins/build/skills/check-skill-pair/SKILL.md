---
name: check-skill-pair
description: >
  Audits pair-level integrity of a primitive-pair (the artifact
  `/build:build-skill-pair` produces) by walking the six artifact
  slots together — principles doc, `build-<primitive>/SKILL.md`,
  `check-<primitive>/SKILL.md`, `audit-dimensions.md`,
  `repair-playbook.md`, and the `primitive-routing.md` registration
  — and reports cross-artifact issues a per-SKILL.md checker cannot
  see: missing principles doc, drifted audit/playbook dimension
  coverage, both halves referencing different principles paths,
  absent routing registration, drifted audit/playbook dimensions.
  Use when the
  user wants to "audit a skill pair", "check pair integrity",
  "review a primitive pair", "is this pair consistent", or
  "validate the skill pair for X". Not for auditing a single
  SKILL.md — route to `/build:check-skill`. Not for re-distilling
  a stale principles doc — route to `/build:build-skill-pair`.
argument-hint: "[primitive-name]"
references:
  - ../../_shared/references/skill-best-practices.md
  - ../../_shared/references/primitive-routing.md
  - ../../_shared/references/skill-pair-best-practices.md
  - ../../_shared/references/skill-locations.md
  - references/audit-dimensions.md
  - references/repair-playbook.md
---

# Check Skill Pair

Audit a primitive-pair for cross-artifact integrity. Per-SKILL.md
concerns (description quality, frontmatter shape, body length) are
covered by `/build:check-skill`; this skill catches the issues that
only surface when you look at the six artifacts *together*.

The deterministic audit runs in one step via
[`scripts/audit_pair.py`](scripts/audit_pair.py). It emits Tier-1
existence findings (six artifact slots), Tier-2 content findings
(required H2 sections in the principles doc, audit-dimensions vs
repair-playbook coverage), and Tier-3
cross-reference findings (shared principles path, check-half
frontmatter refs, build→check handoff, routing registration, dogfood
script info). A second pass layers one LLM-judgment check on top:
**audit-dimensions required-fields** — each dimension entry should
carry six fields (name, what, pass, fail, severity, principles-doc
section), accepted either labeled (`**Pass:**`) or inferred
("Passes when…"). This check is prose-heuristic and stays out of the
script.

**Workflow sequence:** 1. Scope → 2. Target → 3. Run audit_pair.py →
4. Required-Fields Pass → 5. Report → 6. Opt-In Repair Loop

`<SKILL_ROOT>` and `<SHARED_REF_DIR>` resolve from the chosen target
— see [skill-locations.md](../../_shared/references/skill-locations.md)
for the prefix table.

## 1. Scope

Parse `$ARGUMENTS` as the primitive name (kebab-case, no path
prefix). Refuse on empty input — this skill operates on a named
primitive, not a configuration. Confirm scope aloud in one line:
`Auditing skill-pair for primitive: <name>`.

The six artifact slots `audit_pair.py` inspects:

- Principles doc: `<SHARED_REF_DIR>/<name>-best-practices.md`
- Build skill: `<SKILL_ROOT>/build-<name>/SKILL.md`
- Check skill: `<SKILL_ROOT>/check-<name>/SKILL.md`
- Audit dimensions: `<SKILL_ROOT>/check-<name>/references/audit-dimensions.md`
- Repair playbook: `<SKILL_ROOT>/check-<name>/references/repair-playbook.md`
- Routing registration: `<SHARED_REF_DIR>/primitive-routing.md` (both route lines; required for `plugin` target, optional otherwise)

## 2. Target

Pick the placement scope before invoking the script. If `$ARGUMENTS`
includes `--target <plugin|project|user>`, use it. Otherwise apply
the inference rule from
[skill-locations.md](../../_shared/references/skill-locations.md):
walk up CWD for a plugin source tree, then for a project `.claude/`
directory, falling back to `user`. Surface the inferred target in
one line and confirm before invoking the script.

## 3. Run audit_pair.py

Execute the deterministic audit, passing the resolved target:

```bash
python3 plugins/build/skills/check-skill-pair/scripts/audit_pair.py \
  --target <plugin|project|user> <name>
```

The default target is `plugin` (back-compat). Project- and
user-target audits resolve artifacts under `.claude/skills/` or
`~/.claude/skills/` respectively.

The script emits a findings table, a summary line, and an exit code
(non-zero if any `fail` findings). If the script prints `No pair
found for <name>`, stop — recommend `/build:build-skill-pair <name>`
to create one. There is nothing to audit into existence.

Parse the findings table. The script covers: all six Tier-1
existence checks, Tier-2 principles-doc structure + dimension
coverage, and Tier-3 shared principles path + check-half frontmatter
refs + build→check handoff + routing registration + dogfood-script
info.

## 4. Required-Fields Pass

The one check the script leaves to judgment: each dimension entry
in `audit-dimensions.md` should carry six fields — *name*, *what it
checks*, *pass criteria*, *fail criteria*, *severity*, and a
*principles-doc section reference*. Accept labeled form
(`**Pass:**`, `**Severity:**`) or inferred form (a sentence
beginning "Passes when…", "Severity is fail because…"). A dimension
missing three or more fields is `warn`.

Skip this pass if Tier-1 flagged `audit-dimensions.md` as missing —
there is nothing to read.

Read the file once, iterate dimension entries (H3 headings), and
append any findings to the Tier-1/2/3 set the script produced.

## 5. Report

The script already emits a findings table and summary line. If the
Required-Fields Pass added any findings, merge them into the
existing table (append as `T2` rows with the
`audit-dimensions-required-fields` check name) and recompute the
summary line. Preserve the script's sort order: `fail` → `warn` →
`info`; within severity, Tier-1 before Tier-2 before Tier-3.

Example script output (shape):

```
0 fail, 1 warn, 1 info across 6 artifact slots

| Tier | Check | Artifact | Issue | Severity |
|------|-------|----------|-------|----------|
| T3 | build-to-check-handoff | plugins/build/skills/build-foo/SKILL.md | body does not mention /build:check-foo | warn |
| T3 | dogfood-script-audit | plugins/build/skills/check-foo/scripts | 1 Python script(s) — run /build:check-python-script | info |

0 fail, 1 warn, 1 info across 6 artifact slots
```

## 6. Opt-In Repair Loop

Ask exactly once:

> "Apply fixes? Enter `y` (all), `n` (skip), or comma-separated
> numbers."

For each selected finding, route to the appropriate fix:

- **Direct edit** — routing-doc registration (write missing route
  lines), check half's frontmatter references (add
  `audit-dimensions.md` / `repair-playbook.md` to `references:`),
  build→check handoff wording. Show the diff; write on confirmation.
- **Routed to another skill** — missing principles doc or large-scale
  pair damage → recommend `/build:build-skill-pair <name>` to
  rebuild from input material; orphan dimensions → ask whether the audit or
  the playbook is authoritative (`add to audit` or `remove from
  playbook`, vice versa); never auto-pick. Tier-1 scripts dogfood
  info → recommend `/build:check-bash-script` or
  `/build:check-python-script` per Language Selection.

After each applied fix, re-run Tier-1 existence checks on the
affected artifact so subsequent findings reflect the new state.

Terminate the loop when the user selects no further findings, enters
`n`, or confirms `done`. The loop does not re-prompt once findings
are exhausted.

## Example

Invocation: `/build:check-skill-pair skill-pair` (self-audit).

Runs `scripts/audit_pair.py skill-pair`. Tier-1 confirms all six
artifacts exist (principles doc, both SKILLs, audit-dimensions,
repair-playbook, routing registration). Tier-2 dimension coverage
matches. Tier-3 confirms both halves reference the same principles
path, check SKILL frontmatter carries both rubric refs, build SKILL
Handoff mentions `/build:check-skill-pair`, routing doc has both
route lines. Emits `info`: 1 Python script exists under
`check-skill-pair/scripts/` — recommends `/build:check-python-script`.

Required-Fields Pass reads `audit-dimensions.md` and confirms each
of the 14 dimensions carries the six required fields.

Report: `0 fail, 0 warn, 1 info across 6 artifact slots`.

Repair loop: user declines (info is advisory); chainable handoff
offers `/build:check-python-script
plugins/build/skills/check-skill-pair/scripts/audit_pair.py`.

## Anti-Pattern Guards

1. **Auditing a single SKILL.md.** The pair is the unit of work
   here. Per-SKILL.md concerns — description routing quality,
   frontmatter shape, body length, ALL-CAPS density — belong to
   `/build:check-skill`. Running this skill on a single SKILL.md
   misses five of the six artifact slots and wastes the audit.
2. **Auto-resolving orphan dimensions.** When `audit-dimensions.md`
   and `repair-playbook.md` drift, the user picks the authoritative
   side — sometimes the audit is right and the playbook has dead
   entries; sometimes the playbook is right and the audit missed a
   new dimension. The skill asks; it does not guess.
3. **Bulk-applying fixes.** Per-finding confirmation is required.
   Pair-integrity findings are often intentional mid-refactor states
   (a dimension in flight, a principles doc being rewritten), and
   bulk-applying "fixes" overwrites deliberate work.
4. **Auditing principles-doc prose quality.** The rubric's *content*
   is whatever the user distilled. This skill checks *structural*
   integrity — required sections present, dimensions aligned —
   not pattern-level critique. Quality concerns about the distilled
   rubric are a `/build:build-skill-pair` re-run, not an audit task.
5. **Skipping Tier-1 when Tier-2/3 look juicy.** Missing artifacts
   are the load-bearing finding. Running Tier-2/3 against a missing
   principles doc produces cascading failures that all reduce to
   "rebuild the pair"; surfacing the Tier-1 `fail` first keeps the
   report readable.

## Key Instructions

- Won't audit a single SKILL.md — the pair is the unit. Route to
  `/build:check-skill` for per-SKILL.md quality.
- Won't auto-resolve orphan dimensions — the user picks the
  authoritative side (audit or playbook).
- Won't apply fixes without per-finding confirmation. The Repair
  Loop is opt-in and per-item.
- Delegates all deterministic checks to `scripts/audit_pair.py` —
  the script covers Tier-1 (existence), Tier-2 (principles
  structure, dimension coverage), and Tier-3
  (shared principles path, check frontmatter refs, build→check
  handoff, routing registration, dogfood-script info). The SKILL
  body only adds the required-fields judgment pass on top. Keeping
  determinism in Python and judgment in the LLM lets CI run the
  script standalone without LLM involvement.
- When the primitive has no artifacts at all, refuses with `No pair
  found for <name>` and recommends `/build:build-skill-pair <name>`.
  There is nothing to audit into existence.
- Tier-1 scripts under `check-<name>/scripts/` get an `info` finding
  — not a direct audit — recommending
  `/build:check-bash-script` or `/build:check-python-script` per
  *Language Selection* in `primitive-routing.md`. This skill does
  not audit scripts; that would duplicate the script-checkers.
- Recovery: this skill is read-only outside the Repair Loop, which
  requires confirmation per finding. Any edits produced can be
  reverted via `git diff` / `git checkout`; the skill itself performs
  no destructive actions.

## Handoff

**Receives:** primitive name — kebab-case, no path prefix (e.g.,
`bash-script`, not `<SKILL_ROOT>/build-bash-script/`); optional
`--target` flag selecting `plugin` (default), `project`, or `user`.

**Produces:** a findings table with one row per audit-dimension /
slot, each row carrying the check name, the artifact path, the
specific issue, and a severity (`fail` / `warn` / `info`). Optionally
— per user confirmation in the Repair Loop — targeted edits to the
check half's frontmatter, the routing doc, or the build half's
handoff wording.

**Chainable to:** `/build:check-skill` (to audit each half's
per-SKILL.md quality once structural integrity is clean);
`/build:build-skill-pair` (to rebuild when the principles doc is
missing or structurally incomplete);
`/build:check-bash-script` or `/build:check-python-script` (to audit
any Tier-1 deterministic scripts the check half carries under its
own `scripts/` directory).
