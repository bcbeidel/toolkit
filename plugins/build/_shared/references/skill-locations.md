---
name: Skill Locations
description: Resolves the three target scopes — plugin, project, user — to the on-disk path prefixes that build-* and check-* skills use when reading or writing skill artifacts. Centralizes placement so all primitive-pair skills share one rule.
related:
  - plugins/build/skills/build-skill-pair/SKILL.md
  - plugins/build/skills/check-skill-pair/SKILL.md
  - plugins/build/_shared/references/skill-pair-best-practices.md
---

# Skill Locations

A `build-<primitive>` / `check-<primitive>` pair scaffolds the same five
artifacts regardless of where they live. What changes between scopes is
the path prefix. This doc names the three supported targets, defines the
prefix each one resolves to, and gives the inference rule build- and
check- skills use to pick a target when the user does not specify one.

## Targets

Three target values are supported. Skills accept them via a `--target`
flag or equivalent intake question.

| Target | When to use | `<SKILL_ROOT>` | `<SHARED_REF_DIR>` |
|--------|-------------|----------------|--------------------|
| `plugin` | Authoring inside a plugin source tree (e.g., this toolkit's `plugins/build/`) | `plugins/<plugin>/skills` | `plugins/<plugin>/_shared/references` |
| `project` | Skill is repo-specific — rubric depends on this repo's conventions | `.claude/skills` | `.claude/skills/_shared/references` |
| `user` | Skill is reusable across any project but not distributed as a marketplace plugin | `~/.claude/skills` | `~/.claude/skills/_shared/references` |

The five-artifact pair resolves as:

```
<SHARED_REF_DIR>/<primitive>-best-practices.md      ← principles doc
<SKILL_ROOT>/build-<primitive>/SKILL.md             ← scaffolder
<SKILL_ROOT>/check-<primitive>/SKILL.md             ← auditor
<SKILL_ROOT>/check-<primitive>/references/audit-dimensions.md
<SKILL_ROOT>/check-<primitive>/references/repair-playbook.md
```

The `references:` frontmatter inside each generated SKILL.md uses the
relative path `../../_shared/references/<primitive>-best-practices.md`
in all three targets — the structure mirrors across scopes by design,
so the relative reference is target-invariant.

## Routing-doc registration

`primitive-routing.md` is a plugin-scoped artifact. The toolkit's own
copy lives at `plugins/build/_shared/references/primitive-routing.md`.

- **`plugin`** — registration is required. Append the two route lines
  per the build-skill-pair Register step.
- **`project`** / **`user`** — registration is optional. If
  `<SHARED_REF_DIR>/primitive-routing.md` exists in the chosen scope,
  update it; otherwise note in the handoff that no routing doc was
  found and proceed.

A pair without a routing-doc entry is still discoverable in
project/user scope via Claude Code's normal skill-loading path —
routing docs are an authoring convention, not a runtime requirement.

## Inference rule

When a target is not specified, infer from CWD in this order. Stop at
the first match.

1. **`plugin`** — CWD is inside a plugin source tree. Detect by walking
   up from CWD until either (a) `<dir>/.claude-plugin/plugin.json`
   exists, or (b) `<dir>/plugins/<name>/.claude-plugin/plugin.json`
   exists for some `<name>`. The plugin root is the matching directory.
2. **`project`** — CWD is inside a repo with a `.claude/` directory.
   Detect by walking up from CWD until `<dir>/.claude/` exists and
   `<dir>` is a git repo (or contains `.claude/skills/`).
3. **`user`** — fallback when neither plugin nor project shape is
   detected.

If the inference produces an unexpected result, the skill must surface
the detected target to the user and ask for confirmation before
writing. Inference is a default, not a commitment.

## Why three targets

A primitive-pair builder that only writes to `plugins/build/...` works
when authoring the toolkit itself but fails for the toolkit's actual
audience: users who want pairs scoped to their repo or their personal
skill library. The three-target shape covers the realistic cases:

- **Plugin** — distributing the pair through the marketplace.
- **Project** — the rubric is repo-specific (file conventions, domain
  rules, layout) so the pair has no value outside this repo.
- **User** — reusable across projects but private to one workstation,
  so a marketplace plugin is overkill.

Anything beyond these three (enterprise-shared, monorepo-cross-package)
can compose: pick the closest target, then move artifacts post-write.
