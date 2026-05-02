---
name: Repair Playbook — Help-Skill
description: One repair recipe per Tier-1 finding type plus one per Tier-2 dimension plus one per Tier-3 collision. Each recipe is Signal → CHANGE → FROM → TO → REASON. Applied during the check-help-skill opt-in repair loop with per-finding confirmation.
---

# Repair Playbook

Per-finding repair recipes for check-help-skill. Every Tier-1 finding
ID, every Tier-2 dimension, and the Tier-3 collision finding has a
recipe here. Apply one at a time, with explicit user confirmation,
re-running the producing check after each fix.

## Format

- **Signal** — the finding ID or dimension name
- **CHANGE** — what to modify, in one sentence
- **FROM** — concrete non-compliant example
- **TO** — compliant replacement
- **REASON** — why, tied to source principle

---

## Tier-1 — Slug & Frontmatter

### Signal: `slug-mismatch`

**CHANGE** Set frontmatter `name` to the literal string `help` and
ensure the directory basename is also `help`. Move the file if the
directory is named anything else.

**FROM**
```yaml
---
name: build-index
---
```
**TO**
```yaml
---
name: help
---
```
**REASON** `/<plugin>:help` resolves on the literal slug `help`.
Renaming defeats discoverable invocation.

### Signal: `frontmatter-shape`

**CHANGE** Add the missing required frontmatter keys: `name`,
`description`, `version`, `owner`, `license`, `references:`.

**FROM**
```yaml
---
name: help
description: Plugin index
---
```
**TO**
```yaml
---
name: help
description: Use when the caller asks "what's in the build plugin"…
version: 1.0.0
owner: build-plugin
license: MIT
references:
  - ../../_shared/references/help-skill-best-practices.md
---
```
**REASON** Required frontmatter is the cache-busting and ownership
signal consumers rely on.

### Signal: `frontmatter-invented-key`

**CHANGE** Remove the unsanctioned frontmatter key. If the
information is load-bearing, move it to the body.

**FROM**
```yaml
---
plugin-tier: core
---
```
**TO** *(remove the key entirely)*

**REASON** Unknown frontmatter keys are silently ignored by Claude
Code; including them implies a contract that does not exist.

---

## Tier-1 — Body Structure

### Signal: `body-line-count`

**CHANGE** Trim the body. Move long-form rationale to AGENTS.md or
the plugin README; tighten workflow descriptions to one sentence
each.

**FROM** *body length 280 lines, with multi-paragraph workflow
narratives*

**TO** *body length under 150 lines, one-sentence workflow
qualifiers*

**REASON** A help-skill is an index, not documentation. Length
dilutes the orientation.

### Signal: `synopsis-present`

**CHANGE** Add a single-sentence synopsis below the H1, before the
first H2.

**FROM**
```markdown
# /build:help

## Skills in this plugin
```
**TO**
```markdown
# /build:help

Author and audit Claude Code primitives — skills, hooks, rules,
subagents, and scripts.

## Skills in this plugin
```
**REASON** The synopsis is the most-read line. Skipping it forces
the caller to translate the skill table into a value proposition.

---

## Tier-1 — Skill Index

### Signal: `managed-region-present`

**CHANGE** Wrap the skill table in
`<!-- generated: do not edit by hand; regenerate from disk -->` and
`<!-- /generated -->` markers.

**FROM**
```markdown
## Skills in this plugin

| Skill | Triggers on |
|---|---|
| build-skill | … |
```
**TO**
```markdown
## Skills in this plugin

<!-- generated: do not edit by hand; regenerate from disk -->
| Skill | Triggers on |
|---|---|
| build-skill | … |
<!-- /generated -->
```
**REASON** The marker is what the auditor uses to detect hand edits;
without it, drift becomes invisible.

### Signal: `managed-region-tampered`

**CHANGE** Regenerate the table inside the managed region from
sibling SKILL.md frontmatter; discard hand edits.

**FROM** *manually polished trigger column with prose embellishment*

**TO** *table regenerated from each sibling's `description` first
~12 words, no embellishment*

**REASON** Hand-editing the managed region is what the marker
exists to forbid. Drift is structurally impossible only when the
generator is the source of truth.

### Signal: `skill-index-coverage`

**CHANGE** Regenerate the table from `plugins/<plugin>/skills/*/`
directory listing. Add rows for any sibling skill missing from the
table; remove rows for skills that no longer exist on disk.

**FROM** *table missing the recently added `check-skill-pair` row;
table contains a row for `build-deprecated` that no longer exists*

**TO** *table includes `check-skill-pair`; row for `build-
deprecated` removed*

**REASON** The skill table is the most-read and most-drift-prone
part of the document. Coverage drift is what the help-skill is
specifically supposed to prevent.

### Signal: `skill-index-no-self`

**CHANGE** Remove the `help` row from the skill-index table.

**FROM**
```
| help | Use when the caller asks… |
```
**TO** *(row removed)*

**REASON** Listing the help-skill in its own table is recursive and
confusing; the generator must exclude `name == "help"`.

### Signal: `description-fidelity`

**CHANGE** Regenerate the trigger column for the affected row from
the sibling skill's current `description` (first ~12 words). Do not
hand-polish.

**FROM**
```
| plan-work | Plan a multi-step task |
```
*(but `plan-work`'s current description starts: "Use when the user
has a spec or requirements for a multi-step task…")*

**TO**
```
| plan-work | Use when the user has a spec or requirements for… |
```
**REASON** The table is the disk-derived view of sibling
descriptions. Drift means the index lies about what siblings do.

---

## Tier-1 — Workflows & Pointers

### Signal: `workflow-section-present`

**CHANGE** Add a `## Common workflows` section with at least one
curated chain. Do not auto-generate; ask the user.

**FROM** *no workflows section*

**TO**
```markdown
## Common workflows

- **Build new feature** — `scope-work` → `plan-work` → `start-work`
  → `verify-work`. *Use when starting from requirements.*
```
**REASON** A help-skill without curated workflows is a flat index;
triage scaffolding is what differentiates it from the directory
listing.

### Signal: `workflow-freshness`

**CHANGE** Either remove the broken skill reference from the
workflow chain, or update the chain to use a current sibling.

**FROM**
```
- **X** — `scope-work` → `plan-work` → `legacy-runner`.
```
*(but `legacy-runner` no longer exists at
`plugins/work/skills/legacy-runner/`)*

**TO**
```
- **X** — `scope-work` → `plan-work` → `start-work`.
```
**REASON** A workflow chain that references a removed skill is a
broken pointer — followers land on nothing.

### Signal: `workflow-chain-cross-plugin`

**CHANGE** Either narrow the chain to in-plugin skills or move the
cross-plugin chain to AGENTS.md's plugin-composition section.

**FROM**
```
- **X** — `scope-work` (work) → `build-skill` (build).
```
**TO**
```
- **X** — `scope-work` → `plan-work` → `start-work`.
```
*(and add the cross-plugin chain to AGENTS.md if useful)*

**REASON** Per-plugin scoping is intentional. Cross-plugin
discovery lives in AGENTS.md; mixing it into a help-skill blurs the
boundary.

### Signal: `pointer-resolution`

**CHANGE** Fix the broken relative link.

**FROM**
```markdown
- [AGENTS.md](../../AGENTS.md)
```
*(file is actually 4 directories up, not 2)*

**TO**
```markdown
- [AGENTS.md](../../../../AGENTS.md)
```
**REASON** From `plugins/<plugin>/skills/help/SKILL.md`, the repo
root is four directories up.

### Signal: `pointer-broken-fail`

**CHANGE** Same as `pointer-resolution`. The FAIL severity reflects
that AGENTS.md / RESOLVER.md / the plugin README are load-bearing
navigation.

**REASON** A help-skill whose pointer to AGENTS.md is broken sends
callers nowhere; the pointer's job is to be the off-ramp to broader
context.

---

## Tier-1 — Description Shape

### Signal: `description-trigger-shape`

**CHANGE** Rewrite the `description` to lead with "Use when" and
include concrete trigger phrases.

**FROM**
```yaml
description: Plugin index for the build plugin.
```
**TO**
```yaml
description: >-
  Use when the caller asks "what's in the build plugin", "list
  build skills", "how do I use build", or wants to see which build
  skill fits a task.
```
**REASON** Capability-shaped descriptions do not retrieve. The
router reads the description as a trigger condition.

---

## Tier-1 — Safety

### Signal: `secret`

**CHANGE** Remove the secret. Help-skills should not contain
credentials of any kind.

**FROM**
```
api_key: sk-proj-abc123def456
```
**TO** *(removed; replace with reference to env var if context
requires)*

**REASON** A help-skill is committed and trusted by Claude as
instructions; embedded secrets are a breach.

### Signal: `tls-disable`

**CHANGE** Remove the security-weakening instruction. Document the
real fix or file a bug.

**REASON** Security-weakening guidance outlives the issue that
prompted it.

### Signal: `pipe-to-shell`

**CHANGE** Remove the `curl … | bash` invocation. If installer
guidance is needed, link to a workflow skill instead.

**REASON** Help-skills are orientation surfaces; supply-chain
installers belong inside workflow skills with explicit safety
gates.

---

## Tier-2 — Judgment Dimensions

### Signal: D1 Workflow Curation (FAIL)

**CHANGE** Replace the flat list with at least one composed chain
showing how skills compose. Add a one-sentence "when this chain
applies" qualifier per chain.

**FROM**
```markdown
## Common workflows
- scope-work
- plan-work
- start-work
```
**TO**
```markdown
## Common workflows
- **Build new feature** — `scope-work` → `plan-work` → `start-work`
  → `verify-work`. *Use when starting from requirements.*
```
**REASON** A help-skill without composed chains is just a re-
listing of the skill table.

### Signal: D2 Triage Scaffolding (WARN)

**CHANGE** Add a "task → skill" mapping cue per workflow chain.
Name the user task, not just the skill name.

**FROM**
```
- **scope-work** — explores requirements
```
**TO**
```
- **When you have requirements but don't know how to break them
  down** — start with `scope-work`, then `plan-work`.
```
**REASON** Triage scaffolds the choice; description echo doesn't.

### Signal: D3 Dual Audience (WARN)

**CHANGE** Add scannable structure (bullets, tables) for human
readers and concrete trigger phrases for agent routing. Trim
narrative prose; keep imperatives.

**REASON** A help-skill that reads as a marketing page fails the
agent; one that reads as token-optimized telegraph fails the
human. Both audiences must scan it cleanly.

### Signal: D4 Scope Discipline (WARN)

**CHANGE** Move architectural / install / contributing prose out
of the help-skill. Replace with a pointer to AGENTS.md / README /
CONTRIBUTING.

**FROM**
```markdown
## Why this plugin exists
This plugin codifies the conventions we've evolved over…
```
**TO**
```markdown
## Where to look next
- [AGENTS.md](../../../../AGENTS.md) — plugin composition rationale
```
**REASON** Pointers, not duplications. Two copies drift.

### Signal: D5 Trigger Quality (WARN)

**CHANGE** Rewrite the description to fire on meta-questions about
the plugin, not on the plugin's own workflows.

**FROM**
```yaml
description: Use when the user wants to build, audit, or work with
  Claude Code primitives.
```
**TO**
```yaml
description: >-
  Use when the caller asks "what's in the build plugin", "list
  build skills", or "which build skill fits this task".
```
**REASON** A description shaped like sibling triggers competes for
routing. The help-skill's distinct trigger is meta-questions about
the plugin.

---

## Tier-3 — Cross-Entity Collision

### Signal: trigger-collision

**CHANGE** Narrow either the help-skill description or the
colliding sibling description so the trigger sets are disjoint.
Choose based on which side is "wider" — the help-skill's trigger
should be meta-questions only; siblings' triggers should be the
specific tasks they perform.

**FROM**
- help-skill description: *"Use when the user wants to use the
  build plugin."*
- sibling `build-skill` description: *"Use when the user wants to
  build, scaffold, or create a skill."*
- shared trigger phrase: "use the build plugin" overlaps with
  "build" tasks.

**TO**
- help-skill description: *"Use when the caller asks 'what's in the
  build plugin' or 'list build skills'."*
- sibling description unchanged.

**REASON** The router picks one arbitrarily when two skills match
the same trigger. The help-skill is the one to narrow because its
distinct value is meta-trigger; siblings own their workflow
triggers.
