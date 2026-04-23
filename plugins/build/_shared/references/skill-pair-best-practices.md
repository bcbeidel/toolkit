---
name: Skill-Pair Best Practices
description: Authoring guide for a primitive-pair — a matched `build-<primitive>` + `check-<primitive>` pair that shares a distilled principles doc, a scoreable audit-dimensions rubric, and a repair-playbook. Referenced by build-skill-pair and check-skill-pair.
related:
  - plugins/build/skills/build-bash-script/SKILL.md
  - plugins/build/skills/check-bash-script/SKILL.md
  - plugins/build/skills/build-python-script/SKILL.md
  - plugins/build/skills/check-python-script/SKILL.md
  - plugins/build/skills/build-skill-pair/SKILL.md
---

# Skill-Pair Best Practices

## What a Good Skill-Pair Does

A skill-pair is two skills authored as a unit: a scaffolder
(`build-<primitive>`) and an auditor (`check-<primitive>`) that share
a single distilled rubric. Its value is that creation and review
never drift — both halves read from the same principles doc, so the
patterns the scaffolder produces are the patterns the auditor
enforces. A pair earns its place when a primitive class is
introduced that (a) benefits from a scaffolding workflow, (b)
benefits from an audit workflow, and (c) carries enough convention
to distill into a rubric worth citing.

The pair is the unit. Either half alone is incomplete: a scaffold
without an audit produces artifacts nothing validates; an audit
without a scaffold enforces a rubric nothing produces. The
`build-skill-pair` meta-skill refuses to scaffold only one side for
this reason.

## Anatomy

Six artifact slots form the pair. All six are load-bearing — missing
any one breaks a contract some other slot relies on.

The principles doc carries four required H2 sections — *What a Good
\<primitive\> Does*, *Anatomy*, *Patterns That Work*, and *Safety*
(or the longer *Safety & Maintenance*; both pass via prefix match).
A separate *Anti-Patterns* section is encouraged but not required —
existing pairs fold negative patterns inline into Patterns or Safety,
and that organization is acceptable. The audit checks structural
presence, not the breakdown.

Inside `audit-dimensions.md` and `repair-playbook.md`, each check
gets its own H3 entry with a short canonical identifier (e.g.,
`### secret`, `### shebang`, `### SC2086`). Pre-existing pairs
document Tier-1 checks compactly as a markdown table under
`## Tier-1 — Deterministic Checks` instead — `audit_pair.py` extracts
table rows AND H3s from `audit-dimensions.md` and normalizes both
to canonical IDs (stripping backticks, "Signal:" prefix, "*(FAIL)*"
suffix) before comparing against the playbook H3 set. New pairs
should prefer per-signal H3s in both files; the table form is
grandfathered.

```
plugins/build/
├── _shared/
│   └── references/
│       ├── <primitive>-best-practices.md        ← principles doc (rubric)
│       └── primitive-routing.md                 ← registration lives here
└── skills/
    ├── build-<primitive>/
    │   └── SKILL.md                             ← scaffolder; references principles
    └── check-<primitive>/
        ├── SKILL.md                             ← auditor; references principles + rubric files
        └── references/
            ├── audit-dimensions.md              ← scoreable rubric derived from principles
            └── repair-playbook.md               ← one fix recipe per dimension
```

The principles doc lives in `_shared/`, not inside either skill, so
both halves cite the same absolute path. The audit rubric and repair
playbook live with the check half because that is where they are
applied. The routing-doc registration is the pair's public handle —
without it, discovery is grep-only.

## Patterns That Work

- **Single shared principles doc.** Both halves' frontmatter
  `references:` resolve to the same path. Two docs (one per skill)
  guarantee drift; one doc makes drift impossible by construction.
- **Three-tier audit structure.** The check half organizes work as
  Tier-1 deterministic / Tier-2 judgment / Tier-3 cross-entity.
  Tier-1 short-circuits missing inputs so Tier-2/3 read nothing that
  is absent. The bash-script and python-script check skills both use
  this structure; it generalizes.
- **Per-finding Repair Loop.** The audit always offers an opt-in
  repair with per-item confirmation. Bulk application overwrites
  mid-refactor intent; per-finding keeps the user in control.
- **Scope Gate in the build half.** A scaffolder that forgets its
  scope produces out-of-bounds artifacts. Explicit refusal signals
  (wrong primitive, wrong language, setuid intent, etc.) at the top
  of the build workflow keep the pair honest.
- **audit-dimensions parallels repair-playbook.** Each dimension in
  the audit rubric has a matching entry in the repair playbook.
  Drift between them produces either findings with no fix recipe or
  fix recipes for findings the audit cannot surface.
- **Pair registered in `primitive-routing.md`.** Both route lines
  (`/build:build-<primitive>` and `/build:check-<primitive>`)
  appear, and the primitive class is described under *What Each
  Primitive Was Designed For* (new class) or *Language Selection*
  (variant).

## Anti-Patterns

- **Principles doc duplicated inside each skill.** The duplication
  creates two rubrics that diverge silently. Audit findings cite one
  copy while the scaffolder reads the other, and users discover the
  drift only when a pattern flagged in review was never in the
  scaffold template.
- **audit-dimensions without corresponding repair-playbook entries.**
  The audit surfaces findings with no remediation path. Users triage
  into "file an issue" and the finding lives forever as a warn.
- **Unregistered pair.** Pairs absent from `primitive-routing.md`
  are discoverable only by grep. Other skills and future authors do
  not find them; the pair sits on disk but is invisible to the
  routing layer that is supposed to catalog it.
- **Build without check (or vice versa) using this pattern.**
  Single-skill authoring has a home — `/build:build-skill` — and the
  pair pattern does not replace it. Scaffolding one half alone with
  the pair meta-skill produces a dangling rubric nothing references.
- **Scope Gate as a comment, not a refusal.** A build skill that
  documents wrong-primitive cases but does not *refuse* them lets
  misrouted scaffolds through. The Gate's authority is in the
  refuse; the language is secondary.

## Safety & Maintenance

**Evolving a pair.** Update the principles doc first, then
audit-dimensions and repair-playbook to reflect any new or changed
pattern, then both SKILL bodies to cite any newly-named workflow
step. Landing these in reverse order — SKILLs first — produces a
window where the body claims patterns the rubric does not yet carry.

**Retiring a pair.** Delete in reverse-dependency order: SKILL
bodies first, then rubric files, then the principles doc, then the
routing-doc lines. Running `/build:check-skill-pair <name>` after
deletion should return `No pair found for <name>` cleanly.

**Version discipline.** A pair is a single shipping unit; both
halves ship together or neither does. The build plugin's version
bump covers the whole pair — no partial-pair releases.

**Auditing the pair's own integrity.** `/build:check-skill-pair
<name>` walks all six slots and surfaces drift — missing principles
doc, orphan dimensions, unregistered pair, divergent principles
paths between halves. Run it after any pair-spanning change.

