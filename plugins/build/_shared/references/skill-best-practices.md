---
name: Skills Best Practices
description: Authoring guide for Claude Code skills — what makes a SKILL.md load-bearing, how to shape its frontmatter and body, the positive patterns that work, and the safety and maintenance posture a durable skill library needs. Referenced by build-skill and check-skill.
---

# Skills Best Practices

## What a Good Skill Does

A skill is a reusable, model-invocable workflow packaged as a markdown file that Claude loads on demand. A skill earns its place when the same workflow recurs, the steps are specific enough to execute without re-derivation, and the cost of getting them wrong is higher than the cost of writing them down. Primitive selection — rule vs. hook vs. skill vs. CLAUDE.md — is covered in `primitive-routing.md`.

## Anatomy

```markdown
---
name: kebab-case-slug
description: Use when <concrete trigger>. <One sentence of purpose.>
version: 1.0.0
owner: team-or-person
license: MIT
---

# <Human-readable title>

## When to use
- <Concrete trigger condition>

## Prerequisites
- <Tool, env var, or state assumption>

## Steps
1. <Atomic imperative action.>
2. <Atomic imperative action.>

## Failure modes
- <Likely failure> → <recovery action>

## Examples
<worked example with inputs, outputs, and side effects>
```

Load-bearing elements: the frontmatter identity (`name`, `description`, `version`, `owner`), the invocation triggers, the numbered step sequence, and the failure contract. Bundled assets sit alongside `SKILL.md` in the skill directory, referenced by **relative path** only.

## Authoring Principles

**Name for discovery.** The file is `SKILL.md`; the directory basename equals `name`; `name` is lowercase kebab-case matching `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 characters, unique across the collection. Names are stable identifiers that routing depends on.

**Write the description as a retrieval signal.** Lead with "Use when…" and enumerate concrete invocation triggers — user phrases, file extensions, error strings, event types. Keep it short; long descriptions dilute the signal.

**Declare identity in frontmatter.** Ship `name`, `description`, `version` (semver), and `owner`. Version bumps are the cache-busting signal consumers rely on; owner is who gets pinged when the skill rots. Add `license` (SPDX identifier such as `MIT`, or a short reference to a bundled `LICENSE` file) so reusers know the redistribution terms — match the host repo's license unless the skill ships under different terms. Invent no keys the skill spec does not sanction.

**Keep the body short.** Under 300 lines, hard ceiling 400; lines under 120 characters. Move long scripts and reference material to sibling files. Every line is paid for in context tokens.

**Declare triggers as scannable conditions.** A dedicated `## When to use` section with concrete bullets confirms the skill applies to the situation in hand — the description retrieves, the section confirms.

**Write Steps as a numbered sequence of atomic actions.** Ordered list starting at 1, one action per step, imperative voice addressed to the agent. Keep conditional nesting shallow; deeper branching usually means a second skill. No commentary or rationale inside the step body — reasoning lives in surrounding prose.

**State preconditions once, check them early.** List tools, env vars, versions, and assumed state in `## Prerequisites`, and verify the critical ones in step 1. Assumed state is the biggest source of silent failure.

**Declare inputs, outputs, and their shapes.** Name parameters the skill consumes, artifacts it produces, and environment variables it reads. Implicit contracts invite guessing.

**Speak in plain, direct English.** Define domain terms on first use; avoid undefined jargon and abbreviations. Keep terminology consistent — if one step names `service_name`, don't later call it `svc`. Prefer definite phrasing over hedges like *etc.*, *maybe*, *probably*, *somehow*, *TBD*, *???*; ambiguity propagates directly into model behavior.

**Anchor with a concrete example.** At least one `## Examples` entry with inputs, outputs, and observable side effects. Abstract rules alone drift.

**Write a failure contract.** A `## Failure modes` section naming the three most likely failures and their recovery actions beats letting the agent invent recovery. Where a step polls, retries, or waits, name the timeout and the backoff — "poll every 10s for up to 5 minutes" executes; "poll until done" hangs.

## Patterns That Work

**Trigger-shaped descriptions over capability-shaped ones.** Route on the situation that invokes, not the function performed.

**Imperative numbered steps over prose paragraphs.** Sequences are followed more reliably.

**Relative paths over absolute ones.** Portable; absolute paths break on relocation.

**Explicit failure contracts over silent success.** Name the recoveries.

**Single-purpose skills over kitchen sinks.** Split when the description covers two workflows.

**Definite phrasing over hedges.** State the action; leave no re-derivation.

## Safety

Skills are version-controlled, auto-loaded, and trusted by Claude as instructions — a leak surface and a blast-radius amplifier.

- **No embedded secrets.** Reference env vars or vault paths by name only. Deterministically audited.
- **Destructive operations gate on confirmation.** Deletes, force-pushes, drops, truncates, production deploys, and secret rotations are preceded by an approval step or a dry-run. Destructive-command patterns without safety flags or approval context are flagged deterministically.
- **No unverified remote execution.** `curl | bash`, `eval $(curl …)`, `source <(curl …)` are supply-chain vectors. Pin and verify. Deterministically audited.
- **Declare privilege and blast radius.** Skills touching elevated systems name the privilege tier and required IAM/RBAC roles in `## Prerequisites`.

## Review and Decay

Retire a skill when the workflow no longer recurs, when a better-scoped skill supersedes it, or when its triggers no longer match how users ask. Bump `version` on any material change to description, steps, or bundled executables — consumers and caches key on it. A skill whose steps stop matching reality trains the model to treat the whole library as noise.

---

**Diagnostic when a skill isn't working.** Not invoked? The description is usually the problem — rewrite it as a list of concrete triggers. Invoked but wrong output? The step sequence has prose, hedges, or branches deeper than two levels. Silent failure? The skill is missing its verification contract — add a final step that confirms the desired outcome.
