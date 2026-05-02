---
name: Build Brief Best Practices
description: Authoring guide for `.briefs/<slug>.brief.md` — the per-build intent artifact written by multi-artifact build/* orchestrators (build-skill-pair, build-hook, build-resolver). Defines format, paste-excerpt convention, slug rules, update-don't-recreate semantics, and the anti-shortcut guard rationale. Referenced by the three orchestrators and their checker counterparts.
---

# Build Brief Best Practices

## What a Brief Is

A build brief is a small markdown file written at the very start of a multi-artifact build workflow that captures *why* the build is happening, *what* it will produce, *how* it will hand off to leaf skills, and a running decisions log. It exists because long linear orchestrators (five artifacts in `build-skill-pair`, three in `build-resolver`) lossy-compress the original ask away by the final draft step — the rubric reads generic, the audit dimensions feel inherited from defaults, and a session resumed days later requires reconstructing the intent from git history. The brief is also where checklists live: `Planned artifacts` and `Planned handoffs` are checked off as work proceeds, giving the Review Gate a concrete completeness signal. Briefs are intentionally short-lived and throw-away — they exist to keep the active build coherent, not to accumulate as a project log. They live at `.briefs/<slug>.brief.md`, are not tracked by `wiki:lint`, and may be deleted once the build lands.

## Anatomy

The canonical brief format:

```markdown
---
name: <primitive> build brief
description: Intent and scope for the build of <primitive>
type: brief
related:
  - <path to principles doc / produced artifacts>
---

## User ask (verbatim)
<quote from intake — paste the user's words, not a summary>

## So-what
<one paragraph: why this primitive matters, what problem it solves,
who benefits. Specific to this build — generic so-what is a smell.>

## Scope boundaries
- In: <what this build covers>
- Out: <what it explicitly does not>

## Planned artifacts
- [ ] <path/to/artifact-1>
- [ ] <path/to/artifact-2>

## Planned handoffs
- [ ] /build:build-bash-script — produce <name>.sh enforcing <dim>
- [ ] /build:check-skill — audit <name> SKILL.md

## Decisions log
<appended as the workflow proceeds — date-stamped one-liners are fine>
```

The five required H2 sections are *User ask*, *So-what*, *Scope boundaries*, *Planned artifacts*, *Planned handoffs*. *Decisions log* is appended-to throughout the build; it's not a Review-Gate gate. No `status:` field — briefs do not have a draft/complete/superseded lifecycle. They are either present (build active or recent) or absent (build hasn't happened, or the brief was deleted post-landing).

## Patterns That Work

**One brief per primitive — update, don't recreate.** Re-running an orchestrator on an existing primitive reads `.briefs/<slug>.brief.md`, asks the user whether to update it (default yes) or abandon and regenerate (default no), and proceeds. The Decisions log is appended-to; planned-artifact and planned-handoff checkboxes can be reset if the scope materially changes. The filename does not carry a date prefix — that would imply a per-session lifecycle, but the contract is per-primitive.

**Slug per orchestrator.** Each multi-artifact orchestrator owns a slug-derivation rule:

| Orchestrator | Slug source | Example |
|---|---|---|
| `build-skill-pair` | primitive name (Intake #1) | `.briefs/terraform-module.brief.md` |
| `build-hook` | hook name from enforcement goal | `.briefs/block-main-push.brief.md` |
| `build-resolver` | `resolver` for root-scoped, target dir slug for nested | `.briefs/resolver.brief.md` |

The slug is stable across re-runs so updates land in the same file. When an orchestrator can't derive a unique slug from intake (e.g., two hooks with the same enforcement goal), it asks the user to disambiguate before writing.

**Paste excerpts at handoff, not pointers.** When an orchestrator hands off to a leaf skill (`/build:build-bash-script`, `/build:build-python-script`), it pastes the brief's *So-what* paragraph and the relevant audit-dimension or constraint text directly into the leaf skill's invocation prompt — verbatim. Leaf skills are not modified; they do not know briefs exist. Pointers ("see `.briefs/foo.brief.md`") fail because the leaf skill won't navigate; excerpts succeed because the semantic frame travels with the prompt.

**Re-read the so-what before drafting.** Mid- and late-step instructions in each orchestrator say "re-read the brief's so-what before drafting the rubric" / "before writing the audit dimensions." This counters the lossy-compression failure mode where the rubric drifts toward generic by artifact 5 of 5.

**Check off as you go; verify at Review Gate.** The two checklists (planned artifacts, planned handoffs) are checked off as each is produced. The Review Gate verifies both checklists are complete before accepting the build — an unchecked box is a Review-Gate fail, surfacing forgotten artifacts or skipped handoffs.

## Anti-Patterns

**Inlining a chained skill instead of invoking it.** Observed failure mode: rather than invoking `/build:build-bash-script` via the Skill tool, an orchestrator reads that skill's SKILL.md and writes a partial implementation directly. The shortcut bypasses the chained skill's rubric and leaves no audit trail that the proper skill was used. The anti-shortcut guard is the canonical mitigation:

> "MUST invoke `/build:<chained-skill>` via the Skill tool. MUST NOT read its SKILL.md and inline a partial implementation. The shortcut bypasses the chained skill's rubric and leaves no audit trail."

This bullet appears in each affected orchestrator's Anti-Pattern Guards section.

**Generic so-what.** A so-what that could apply to any build of this primitive — "this codifies best practices for X" — fails the content-quality check. The so-what should name the actual reason this primitive is being built now: a specific gap, a specific user, a specific recurring problem. `check-*` skills audit this with LLM judgment.

**Abandoned checklists.** Boxes left unchecked at end-of-build, especially `Planned handoffs`, mean the orchestrator either skipped a handoff or finished without verifying its own scope. The Review-Gate completeness check catches this; if the user wants to drop a planned item, they uncheck it explicitly with a `Decisions log` entry, not by ignoring it.

**Pointer-only handoff.** "See `.briefs/foo.brief.md` for context" pasted into a leaf-skill invocation is treated by the leaf as ambient text it can ignore. Excerpts must be pasted verbatim — so-what + the specific dimension or constraint — for the semantic frame to actually arrive.

**Treating briefs as long-lived docs.** Briefs are not project context. They do not appear in `wiki:lint` checks, do not need cross-references, and may be deleted after the build lands. Treating them as durable artifacts inverts the throw-away contract.

## Safety & Maintenance

Briefs are gitignored at the project's discretion or committed at the project's discretion — neither is required. A committed brief gives PR reviewers traceability from the produced artifacts back to intent; a gitignored brief avoids accumulating one-shot context in history. Either choice is valid. What is *not* valid is auto-deleting briefs from a hook or script — the user owns the lifecycle.

When a brief becomes stale (the produced artifacts diverged from the planned-artifacts list, the so-what no longer matches the current build), the next orchestrator run that touches the same primitive will surface the drift at the "update or recreate?" prompt. There is no separate freshness check.

The format is intentionally light. Adding fields (timing data, metric thresholds, owner annotations) is out of scope — briefs earn their keep by being short enough to read in 30 seconds. A brief that grows past one screen has accreted scope that belongs in a design doc or plan, not a brief.
