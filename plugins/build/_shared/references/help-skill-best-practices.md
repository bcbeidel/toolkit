---
name: Help-Skill Best Practices
description: Authoring guide for help-skills — a SKILL.md at plugins/<plugin>/skills/help/ that orients agents and humans to a plugin's contents, reachable as /<plugin>:help and as auto-triggered context. Covers what a help-skill is for, the canonical anatomy, patterns that keep the index honest, anti-patterns that fail dual audience, and the safety posture. Referenced by build-help-skill and check-help-skill.
---

# Help-Skill Best Practices

## What a Good Help-Skill Does

A help-skill is the **front door of a plugin** — the markdown a caller
loads when they want to know what a plugin contains and which of its
skills fits the task in hand. It is not a generic skill; it is a
specialized SKILL.md whose subject is *the plugin itself*. Two
audiences read it: a human typing `/<plugin>:help` who wants a readable
index, and an agent that has matched the trigger "what's in this
plugin / which skill fits" and needs triage scaffolding to route into
the right sibling skill.

A help-skill earns its place when a plugin contains enough skills that
discovery by grep or by skimming `<plugin>/skills/` is slow, and the
skill descriptions alone don't communicate *how the skills compose*.
Five or more sibling skills is the rough threshold; below that, the
caller can read the directory directly. A help-skill is the *pull*
alternative to a `UserPromptSubmit` hook that injects a global routing
table on every prompt — on-demand, no token tax, scoped to one plugin,
generated from disk so the index can't drift.

A help-skill is not a top-level repository README (that is for a
stranger arriving from a search result; the help-skill caller has
already chosen the plugin), not a CLI tool's `--help` output (it is
markdown for an LLM, not text for a terminal), not a global
cross-plugin router (per-plugin scoping is intentional), and not a
substitute for `AGENTS.md` (which carries cross-plugin context).

## Anatomy

```markdown
---
name: help                          ← always literal "help" — directory and slug
description: Use when the caller asks "what's in the <plugin> plugin",
  "list <plugin> skills", "how do I use <plugin>", or wants to see
  which <plugin> skill fits a task.
version: 1.0.0
owner: <plugin>-plugin
license: MIT
references:
  - ../../_shared/references/help-skill-best-practices.md
---

# /<plugin>:help

One-sentence synopsis of what the plugin does.

## Skills in this plugin

<!-- generated: do not edit by hand; regenerate from disk -->
| Skill | Triggers on |
|---|---|
| `<sibling-1>` | <description first ~12 words> |
| `<sibling-2>` | <description first ~12 words> |
<!-- /generated -->

## Common workflows

- **<Workflow name>** — `<skill-a>` → `<skill-b>` → `<skill-c>`.
  <One sentence: when this chain applies.>

## Where to look next

- [AGENTS.md](../../../../AGENTS.md) — cross-plugin context
- [RESOLVER.md](../../../../RESOLVER.md) — filing and context routing
- [`<plugin>/README.md`](../../README.md) — plugin install / contributing
```

Load-bearing pieces: the literal `name: help` (the slug is fixed —
Claude Code's `/<plugin>:<slug>` invocation depends on it); the
description tuned to "what's in the plugin" / "list skills" / "how do I
use it" triggers; a one-sentence plugin synopsis; a disk-derived skill
table inside a generated-region marker; one or more curated workflow
chains; pointers to `AGENTS.md`, `RESOLVER.md`, and the plugin README.

## Patterns That Work

**Generate the skill table from sibling frontmatter.** The table is
the most-read part of the document and the most likely to drift. A
small generator that walks `<plugin>/skills/*/SKILL.md`, reads each
`name` and `description`, and emits the table inside a managed region
makes drift structurally impossible. Hand-editing the table inside the
managed region is the failure mode the marker exists to flag.

**Use `name: help` literally — the slug is fixed.** Claude Code
resolves `/<plugin>:help` by looking for a skill named `help` inside
the plugin's `skills/` directory. Renaming the slug breaks the
discoverable invocation. The directory basename, the frontmatter
`name`, and the slash-command suffix all carry the same string.

**Lead the description with the caller's situation, not the skill's
function.** *"Use when the caller asks 'what's in the build plugin' or
'list build skills'"* retrieves; *"Surfaces an index of plugin skills"*
does not. The router reads the description; the description must read
like a trigger condition.

**One-sentence synopsis below the H1 is the most-read line.** It
answers *what does this plugin do* in one breath. Same role as a
README's one-sentence description — but scoped to the plugin, not the
project.

**Curate workflow chains; do not auto-generate them.** A workflow
chain like `scope-work → plan-work → start-work → verify-work` carries
judgment about how skills compose. That judgment cannot be derived
from frontmatter. List two or three chains the plugin's authors
actually expect callers to follow; resist the urge to enumerate every
permutation.

**Trigger description must not collide with sibling-skill triggers.**
The help-skill fires on "what's in this plugin / list skills / how do
I use it" — meta-questions about the plugin. If its description
overlaps with a sibling skill's description (e.g., both fire on "build
a skill"), the router picks one arbitrarily and the caller gets the
wrong skill half the time. The help-skill description must read
unambiguously as *a question about the plugin*, not *a task the plugin
performs*.

**Keep the body short.** Under 150 lines is the target — a help-skill
is an index, not documentation. If the curated workflows or the
"where to look next" section grow past a screen, the content belongs
in `AGENTS.md` or a docs site, not in the help-skill.

**Pointers, not duplications.** The "where to look next" section links
to `AGENTS.md`, `RESOLVER.md`, and the plugin README. It does not
duplicate their content. Two copies drift; one canonical source plus a
link does not.

**Relative paths, parents-up to repo root.** From
`plugins/<plugin>/skills/help/SKILL.md`, the repo root is four
directories up. Use `../../../../AGENTS.md`, `../../../../RESOLVER.md`,
and `../../README.md` for the plugin README. Absolute paths break
under fork or relocation; relative paths survive.

## Anti-Patterns

**Hand-curated skill table.** A table that lives inside the help-skill
as authored prose drifts the moment a sibling skill is added,
removed, or renamed. The next caller sees an incorrect index and
either follows it (and lands on a missing skill) or ignores it (and
the help-skill provides no value). Use a generated region; never
hand-edit between the markers.

**Description that fires on the plugin's own workflows.** A
help-skill whose description says *"Use when the user wants to build,
check, or audit a skill"* (in the `build` plugin) competes with every
sibling skill in the same plugin. The router has no way to choose
correctly and the help-skill effectively replaces routing with chaos.

**Architectural prose in the help-skill body.** Sections explaining
"why this plugin exists", "design philosophy", or "how plugins
compose" belong in `AGENTS.md` or a project-level design doc. The
help-skill is an index; long-form rationale dilutes the orientation.

**Workflow chains that include skills not in this plugin.** Cross-
plugin chains (e.g., `scope-work` → `build-skill` spanning `work` and
`build`) belong in `AGENTS.md`'s plugin-composition section, not in a
single plugin's help-skill. The per-plugin scoping is what keeps the
help-skill bounded.

**Skipping the synopsis.** A help-skill that opens with "## Skills in
this plugin" with no one-sentence synopsis above it skips the
most-read line. The caller reads the H1 and then needs to translate
"how does this plugin's skill set add up to a value proposition?"
themselves — exactly the question the synopsis exists to answer.

**Slug other than `help`.** Renaming to `index`, `overview`, `menu`,
or `<plugin>-help` defeats `/<plugin>:help` as a discoverable
invocation. Callers and `AGENTS.md`'s "Plugin Structure" table both
key on the literal slug.

**Including the help-skill in its own table.** The generator must
exclude `help` from the rendered table — listing the help-skill in its
own index is recursive, useless, and confuses callers about whether
to invoke the help-skill from itself.

**Embedded executable content.** Help-skills are pure orientation
markdown; they do not need scripts or destructive commands. A
help-skill with `## Steps` running `rm` or `curl` is the wrong
primitive — that's a workflow skill misnamed as help.

## Safety & Maintenance

A help-skill is version-controlled, auto-loaded, and trusted by Claude
as instructions — same trust posture as any other SKILL.md. The
blast-radius surface is smaller (no destructive operations) but the
information-leak surface is the same.

- **No embedded secrets, internal hostnames, or credentials** —
  audited deterministically, same rule as every SKILL.md.
- **No instructions to disable security posture** — TLS, SELinux,
  firewall.
- **No `curl … | bash` invitations** — help-skills should not be
  pointing callers at supply-chain installers; if a workflow needs an
  installer, that workflow's own skill is where it lives.

**Maintenance posture.** The skill-table managed region must
regenerate every time a sibling skill is added, removed, or has its
description changed. The generator is the contract; manual edits are
a bug. Curated workflow chains do *not* auto-update — they are
human-maintained judgment, and a sibling skill added without
revisiting them produces a stale chain. Plugin maintainers re-read
the workflows section on every plugin version bump and confirm it
still reflects how skills are expected to compose.

When a sibling skill is removed, the generator re-emits the table
without it — but a curated workflow chain that referenced the removed
skill becomes a broken pointer. Tier-1 freshness checks catch this:
every skill name in `## Common workflows` must resolve to a sibling
SKILL.md on disk.

---

**Diagnostic when a help-skill underperforms.** Not invoked when a
caller asks "what's in this plugin"? The description is capability-
shaped instead of trigger-shaped — rewrite leading with "Use when the
caller asks…". Invoked but caller still picks the wrong sibling
skill? The triage scaffolding is too sparse — add a "common
workflows" entry that names the skill chain for the caller's task.
Skill table out of date? The managed region was hand-edited or the
generator wasn't re-run — re-run the generator and audit for manual
edits inside the markers.
