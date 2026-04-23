---
name: Skill-Pair Repair Playbook
description: One entry per audit dimension — how to fix a finding. Routes to other skills when the fix is better handled there.
---

# Skill-Pair Repair Playbook

Each entry corresponds to a dimension in
[audit-dimensions.md](audit-dimensions.md). Structure:
*Finding* → *Diagnosis* → *Fix*. Where the fix is better handled by
another skill, the entry routes there rather than writing the edit
inline.

## Tier-1: Existence

### principles-doc-presence

**Finding:** `_shared/references/<primitive>-best-practices.md` is
missing or empty.
**Diagnosis:** the pair was scaffolded partially, or the principles
doc was deleted without removing the pair. The rubric is absent; both
halves reference a broken path.
**Fix:** run `/build:build-skill-pair <primitive>` to re-run the
Distill step against the pair's input material. Do not hand-author
the principles doc — the meta-skill's Intake / Distill contract
ensures the rubric is internally consistent with the input.

### build-skill-presence

**Finding:** `plugins/build/skills/build-<primitive>/SKILL.md` is
missing.
**Diagnosis:** the scaffold half was deleted or never created.
**Fix:** run `/build:build-skill-pair <primitive>` — the Save step
writes the build half. If the principles doc is still intact, the
Distill step passes through and only the missing SKILL.md is
written.

### check-skill-presence

**Finding:** `plugins/build/skills/check-<primitive>/SKILL.md` is
missing.
**Diagnosis:** the audit half was deleted or never created.
**Fix:** run `/build:build-skill-pair <primitive>`. Same rationale
as `build-skill-presence`.

### audit-dimensions-presence

**Finding:** `check-<primitive>/references/audit-dimensions.md` is
missing or empty.
**Diagnosis:** the scoreable rubric is absent; the check half has
nothing to audit against.
**Fix:** run `/build:build-skill-pair <primitive>` to regenerate
the rubric files from the principles doc.

### repair-playbook-presence

**Finding:** `check-<primitive>/references/repair-playbook.md` is
missing or empty.
**Diagnosis:** findings have no fix recipes.
**Fix:** run `/build:build-skill-pair <primitive>` to regenerate
the rubric files from the principles doc.

### routing-registration-presence

**Finding:** one or both route lines (`/build:build-<primitive>`,
`/build:check-<primitive>`) are missing from
`_shared/references/primitive-routing.md`.
**Diagnosis:** the pair was scaffolded but the Register step did not
run, or the routing doc was edited after the fact.
**Fix:** append the missing route line(s) to the appropriate section
of `primitive-routing.md`. If the primitive is a new top-level class,
add a one-paragraph entry under *What Each Primitive Was Designed
For*; if it is a variant of an existing class, extend the relevant
sub-section (most commonly *Language Selection*). Show the diff and
write on confirmation.

## Tier-2: Content

### principles-doc-structure

**Finding:** the principles doc is missing one or more required H2
sections (`What a Good`, `Anatomy`, `Patterns That Work`,
`Anti-Patterns`, `Safety & Maintenance`).
**Diagnosis:** the Distill step produced an incomplete rubric, or
later hand-edits removed a section.
**Fix:** add the missing section with a stub heading and offer to
populate from the pair's input material, or route to
`/build:build-skill-pair <primitive>` for a full rebuild.

### dimension-coverage-alignment

**Finding:** `audit-dimensions.md` and `repair-playbook.md` cover
different dimension sets — orphans on one or both sides.
**Diagnosis:** a dimension was added or removed on one side
without the other, or the two files have drifted through
independent edits.
**Fix:** ask the user which side is authoritative. Two options:
(a) the audit is correct — add missing entries to the repair
playbook (route to `/build:build-skill-pair <primitive>` if the
principles doc has grown); (b) the playbook is correct — remove
dead dimensions from the audit. Never auto-pick — orphan dimensions
are often intentional mid-refactor states.

### audit-dimensions-required-fields

**Finding:** one or more dimensions in `audit-dimensions.md` lack
the required fields (name, what, pass, fail, severity,
principles-doc section).
**Diagnosis:** shorthand or partial entries that skipped fields
during authoring.
**Fix:** flag each dimension and offer to fill in the missing
fields from the principles doc. If three or more fields are
missing, route to `/build:build-skill-pair <primitive>` — the
Draft step rebuilds the rubric from the principles doc.

## Tier-3: Cross-Reference

### shared-principles-path

**Finding:** the two halves' frontmatter `references:` point at
different principles-doc paths.
**Diagnosis:** a file was renamed or moved without updating both
halves' frontmatters. The pair has silently split.
**Fix:** identify the authoritative path (usually the one that
exists on disk), then update the other half's `references:` field
to match. Show the diff and write on confirmation. If *neither*
path exists, escalate to `principles-doc-presence` fix.

### check-frontmatter-references

**Finding:** `check-<primitive>/SKILL.md` frontmatter does not list
`audit-dimensions.md` and/or `repair-playbook.md` in `references:`.
**Diagnosis:** the references field was not updated when the rubric
files were added, or was edited away.
**Fix:** add the missing file(s) to the `references:` list. Paths
are relative to the check half's own directory
(`references/audit-dimensions.md`,
`references/repair-playbook.md`). Show the diff and write on
confirmation.

### build-to-check-handoff

**Finding:** `build-<primitive>/SKILL.md` does not mention
`/build:check-<primitive>` in its Handoff Chainable-to field or
its final workflow step.
**Diagnosis:** the build half was authored without naming its
chainability to the check half, or the reference was removed.
**Fix:** add `/build:check-<primitive>` to the `Chainable-to:`
line in the Handoff section, and — if the build half has a "Test"
workflow step — cite the check command there as the canonical
follow-on. Show the diff and write on confirmation.

### dogfood-script-audit

**Finding:** `check-<primitive>/scripts/` exists; its scripts have
not been audited by the appropriate script-checker.
**Diagnosis:** advisory — the meta-skill's *Language Selection*
routing rule suggests Tier-1 scripts get audited by
`/build:check-bash-script` or `/build:check-python-script`. This is
not an integrity failure; it is a consistency recommendation.
**Fix:** recommend running `/build:check-bash-script
check-<primitive>/scripts/` (for bash) or
`/build:check-python-script check-<primitive>/scripts/` (for
Python) per *Language Selection* in `primitive-routing.md`. This
playbook does not apply the fix — it routes to the script-checker
whose job this is.
