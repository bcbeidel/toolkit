---
name: build-help-skill
description: >-
  Use when the user wants to "create a help skill", "scaffold a help
  skill for the X plugin", "add a /<plugin>:help command", "build a
  plugin index skill", or wants to give a plugin an orientation
  surface that lists its skills and common workflows. Produces a
  SKILL.md at plugins/<plugin>/skills/help/SKILL.md.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
argument-hint: "[plugin name]"
user-invocable: true
version: 1.0.0
owner: build-plugin
license: MIT
references:
  - ../../_shared/references/help-skill-best-practices.md
  - ../../_shared/references/primitive-routing.md
  - ../../_shared/references/skill-best-practices.md
  - scripts/render_skill_table.py
---

# /build:build-help-skill

Scaffold a `help` skill for a Claude Code plugin — the SKILL.md a
caller loads when they ask "what's in this plugin / which skill
fits". A help-skill is a specialized SKILL.md whose subject is the
plugin itself: a one-sentence synopsis, a disk-derived index of
sibling skills, two or three curated workflow chains, and pointers
to `AGENTS.md` / `RESOLVER.md` / the plugin README.

Authoring principles — what makes a help-skill load-bearing, the
canonical anatomy, the patterns that keep the index honest — live in
[help-skill-best-practices.md](../../_shared/references/help-skill-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

## When to use

- The user says "create/build/scaffold a help skill" or "add a
  `/<plugin>:help` command"
- A plugin has grown to 5+ sibling skills and discovery by grep is
  slow
- The user wants a plugin to have an orientation surface that lists
  its skills and shows how they compose
- The user passes a plugin name (e.g., `build`, `wiki`, `work`) and
  wants its help-skill scaffolded

## Prerequisites

- Working directory is a toolkit checkout (or a repo with the same
  `plugins/<plugin>/skills/<name>/SKILL.md` shape)
- Write access to `plugins/<plugin>/skills/help/`
- The target plugin already exists at `plugins/<plugin>/` with at
  least 2 sibling skills (a help-skill for a plugin with one skill
  is more cost than benefit)
- `/build:check-help-skill` available for the post-write audit step

## Steps

1. **Verify the primitive.** Confirm the user wants a *help-skill* —
   a plugin-orientation SKILL.md — and not a generic skill (route to
   `/build:build-skill`), a top-level README (route to
   `/build:build-readme`), or a global router skill (out of scope —
   per-plugin scoping is intentional). Full decision matrix in
   [primitive-routing.md](../../_shared/references/primitive-routing.md).

2. **Resolve the plugin.** Read `$ARGUMENTS`. If it names a plugin
   (e.g., `build`, `wiki`, `work`, `consider`), confirm
   `plugins/<plugin>/.claude-plugin/plugin.json` exists. If empty or
   ambiguous, list the plugins in `plugins/` and ask which one. If
   the named plugin does not exist, stop — do not scaffold a help-
   skill for a plugin that hasn't been created.

3. **Scope-gate.**
   - **Existing help-skill.** If `plugins/<plugin>/skills/help/`
     already exists, stop. Offer to revise the existing help-skill
     instead — run `/build:check-help-skill` and iterate from
     findings.
   - **Plugin too small.** If the plugin has fewer than 2 sibling
     skills, surface the threshold and ask the user to confirm. A
     help-skill for a one-skill plugin is overhead with no payoff.
   - **Slug collision.** If a sibling skill is already named `help`
     anywhere in the plugin, stop — the slug is fixed and a
     collision is a configuration error to resolve before
     scaffolding.

4. **Elicit the synopsis and workflows.** Ask, one question at a
   time, three things:
   - **Synopsis** — one sentence answering "what does this plugin
     do" (e.g., for `work`: *"Plan, execute, and verify multi-step
     coding work."*).
   - **Common workflows** — two to three curated chains of skill
     composition. Each chain is a bulleted entry: workflow name →
     `skill-a` → `skill-b` → `skill-c`, plus one sentence on when
     the chain applies. Pre-fill suggestions by reading sibling
     skill descriptions and proposing chains the user can accept,
     edit, or reject. Do not auto-generate without confirmation —
     workflow curation is judgment.
   - **Where-to-look-next pointers** — confirm the three default
     pointers (`AGENTS.md`, `RESOLVER.md`, plugin `README.md`) and
     ask if any plugin-specific docs (e.g., a design doc, a
     research note) belong there too.

5. **Read sibling skills via the renderer script.** Run
   `scripts/render_skill_table.py <plugin> --format json` to parse
   each sibling SKILL.md's frontmatter (name + description) into a
   structured list. The script excludes `help` and `_shared/`
   automatically. The LLM reasons over the script's JSON output, not
   raw SKILL.md files — this is the deterministic substrate that
   the rest of the workflow composes against. The same script
   renders the markdown table in Step 7.

6. **Pick the trigger discipline.** Draft the description with the
   help-skill's distinguishing trigger shape: *"Use when the caller
   asks 'what's in the `<plugin>` plugin', 'list `<plugin>` skills',
   'how do I use `<plugin>`', or wants to see which `<plugin>` skill
   fits a task."* Then check it against every sibling skill's
   description for trigger collision. If any sibling fires on
   "what's in this plugin" or "list skills" — flag the collision,
   show both descriptions, and ask the user which to narrow. The
   router cannot disambiguate two skills that match the same trigger.

7. **Draft the SKILL.md.** Follow the anatomy in
   [help-skill-best-practices.md](../../_shared/references/help-skill-best-practices.md).
   Required frontmatter: `name: help` (literal — the slug is fixed),
   `description` (from Step 6), `version: 1.0.0`, `owner:
   <plugin>-plugin`, `license: MIT`, `references:` pointing at
   `../../_shared/references/help-skill-best-practices.md`. Required
   body: H1 `# /<plugin>:help`, the one-sentence synopsis from Step 4,
   a `## Skills in this plugin` section wrapping a managed-region
   marker pair (`<!-- generated: do not edit by hand; regenerate
   from disk -->` and `<!-- /generated -->`) around the table
   produced by `scripts/render_skill_table.py <plugin>` (re-run for
   the markdown form), a `## Common workflows` section with the
   curated chains from Step 4, and a `## Where to look next`
   section with the pointers from Step 4. Body length under 150
   lines.

8. **Present for approval.** Before writing, narrate the design
   choices in 3–6 bullets. Cover the synopsis (and why it differs
   from `AGENTS.md`'s framing of the plugin), the trigger-collision
   check from Step 6 (which sibling descriptions were closest, and
   how the help-skill description was differentiated), the curated
   workflows (which chains were chosen and why), and any pointers
   beyond the three defaults. The reader should be able to disagree
   with any choice. Iterate on feedback. Hold the write until the
   user approves.

9. **Write.** Create
   `plugins/<plugin>/skills/help/` if it doesn't exist. Write
   `SKILL.md` to that directory. Then invoke
   `/build:check-help-skill` on the newly written file — surface any
   findings and offer the repair loop before moving on.

10. **Update plugin manifest.** If
    `plugins/<plugin>/.claude-plugin/plugin.json` enumerates skills
    (some plugins do, some don't), add `help` to the list. If the
    plugin's `AGENTS.md` table or top-level `AGENTS.md` "Plugin
    Structure" table lists skills per plugin, add `help` there too.
    Surface the diff before writing — table edits are easy to get
    wrong.

## Failure modes

- **Plugin does not exist.** Step 2 stops the workflow. Recovery:
  ask the user to scaffold the plugin first, or to pick a different
  plugin.
- **Trigger collision with a sibling skill.** Step 6 surfaces the
  collision. Recovery: narrow either the help-skill description or
  the sibling description before drafting; do not write a help-
  skill that will fight its own siblings for routing.
- **Existing help-skill at scope.** Step 3 stops the workflow.
  Recovery: offer to revise the existing help-skill via
  `/build:check-help-skill` and the repair loop, not to scaffold
  over it.
- **User declines the draft at the approval gate.** Expected.
  Recovery: capture the specific objection, revise the draft, and
  re-present.
- **`check-help-skill` findings block the write.** After Step 9, if
  `/build:check-help-skill` surfaces FAIL findings, apply the
  canonical repair from `repair-playbook.md` and re-audit until
  only WARNs remain (or until the user explicitly accepts a FAIL).

## Examples

<example>
Invocation:

```bash
/build:build-help-skill work
```

Step 1 — Primitive confirmed (plugin orientation surface).

Step 2 — Plugin resolves to `plugins/work/`. Confirmed via
`plugin.json`.

Step 3 — No existing `plugins/work/skills/help/`. Plugin has 5
sibling skills (above the 2-skill threshold). No `help` slug
collision.

Step 4 — Elicits:
- Synopsis: *"Plan, execute, and verify multi-step coding work."*
- Workflows:
  - **Build new feature** — `scope-work` → `plan-work` →
    `start-work` → `verify-work`. *Use when starting from
    requirements; produces a design doc, plan, and validated code.*
  - **Fix a bug** — `scope-work` → `start-work` → `verify-work`.
    *Use when the bug is well-understood and a full plan is
    overkill; skips planning to keep the loop tight.*
- Pointers: defaults plus `plugins/work/CONTRIBUTING.md`.

Step 5 — Reads 5 sibling SKILL.mds; extracts name + description for
each.

Step 6 — Trigger description drafted: *"Use when the caller asks
'what's in the work plugin', 'list work skills', 'how do I use
work', or wants to see which work skill fits a task."* Cross-checked
against siblings — no collision (siblings fire on "scope/plan/start/
verify work", not on meta-questions about the plugin).

Step 7 — Drafts SKILL.md with the managed-region table built from
sibling frontmatter.

Step 8 — Narrates the synopsis choice (concise, action-oriented; not
a duplicate of AGENTS.md's framing), the trigger differentiation,
the workflow curation. User approves.

Step 9 — Writes `plugins/work/skills/help/SKILL.md`. Invokes
`/build:check-help-skill plugins/work/skills/help/SKILL.md` — 0
findings.

Step 10 — Updates `plugins/work/.claude-plugin/plugin.json` and the
top-level `AGENTS.md` "Plugin Structure" table to list `help`.
Surfaces both diffs before writing.
</example>

## Key Instructions

- Use the literal slug `help` — directory `help/`, frontmatter `name:
  help`, slash command `/<plugin>:help`. The slug is not negotiable;
  Claude Code's invocation depends on it.
- Generate the skill-index table from sibling SKILL.md frontmatter,
  inside a managed region. Hand-curated tables drift; the
  managed-region marker is what `check-help-skill` audits for hand
  edits.
- Curate workflow chains — do not auto-generate. The chains carry
  judgment about how skills compose; the user must confirm each one.
- Run the trigger-collision check (Step 6) before drafting. A
  help-skill that fights its siblings for routing is worse than no
  help-skill at all.
- Hold the write until the user approves the draft (Step 8 gate).
- After writing, run `/build:check-help-skill` — this skill must
  produce help-skills that pass the deterministic checks.

## Anti-Pattern Guards

1. **Hand-curated skill table.** A table without managed-region
   markers, or content edited inside the markers, drifts on every
   sibling change. Principle: *Generate the skill table from sibling
   frontmatter.*
2. **Slug other than `help`.** `index`, `overview`, `menu`, or
   `<plugin>-help` all break `/<plugin>:help` as a discoverable
   invocation. Principle: *Use `name: help` literally — the slug is
   fixed.*
3. **Capability-shaped description.** "Surfaces an index of plugin
   skills" does not retrieve. Lead with "Use when the caller
   asks…". Principle: *Lead the description with the caller's
   situation.*
4. **Trigger collision with sibling skills.** The Step 6 check
   exists for this — running it after the draft is too late.
   Principle: *Trigger description must not collide with sibling-
   skill triggers.*
5. **Architectural prose in the body.** Long-form rationale belongs
   in `AGENTS.md`. Principle: *Pointers, not duplications.*
6. **Cross-plugin workflow chains.** Chains spanning two plugins
   belong in `AGENTS.md`. Principle: *Workflow chains scoped to
   this plugin only.*
7. **Listing the help-skill in its own table.** Recursive and
   useless. The generator must exclude `name == "help"`.
8. **Writing before approval.** Always present the draft and narrate
   choices first; the user must explicitly approve before SKILL.md
   is written.
9. **Inlining a chained skill instead of invoking it.** MUST invoke
   `/build:check-help-skill` via the Skill tool after the write.
   MUST NOT read its SKILL.md and inline a partial audit. The
   shortcut bypasses the chained skill's rubric and leaves no audit
   trail that the proper skill was used.

## Handoff

**Receives:** Plugin name (resolves to `plugins/<plugin>/`), or no
argument (prompts for intake).

**Produces:** `plugins/<plugin>/skills/help/SKILL.md`, plus optional
edits to `plugin.json` and the top-level `AGENTS.md` plugin table.

**Chainable to:** `/build:check-help-skill <path>` (audits the
just-built help-skill against the rubric — coverage, freshness,
fidelity, trigger quality, dual audience, scope discipline);
`/build:check-skill <path>` (catches generic SKILL.md structural
issues this skill's draft step missed).
