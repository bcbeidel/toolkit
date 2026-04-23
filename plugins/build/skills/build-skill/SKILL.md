---
name: build-skill
description: >-
  Use when the user wants to "create a skill", "add a skill", "build a
  skill", "scaffold a skill", "new skill for [X]", "write a skill that
  does X", or wants to capture a recurring workflow as a reusable
  Claude Code skill. Also use to improve an existing SKILL.md.
argument-hint: "[skill name and intent, or path to an existing SKILL.md]"
user-invocable: true
version: 1.0.0
owner: build-plugin
references:
  - ../../_shared/references/skills-best-practices.md
  - ../../_shared/references/primitive-routing.md
  - references/platform-notes.md
---

# /build:build-skill

Create a Claude Code skill. Skills are markdown files at
`<scope>/skills/<name>/SKILL.md` that Claude loads on demand — the
router reads the `description` and decides whether to invoke.

Authoring principles — what makes a skill load-bearing, the anatomy
template, patterns that work — live in
[skills-best-practices.md](../../_shared/references/skills-best-practices.md).
This skill is the workflow; the principles doc is the rubric.

## When to use

- The user says "create/build/add/scaffold a skill" or "new skill for [X]"
- The user wants to capture a recurring workflow as a reusable skill
- The user passes an existing `SKILL.md` path and wants it improved
- The conversation contains a workflow the user asks to "turn into a skill"

## Prerequisites

- Working directory is (or contains) the target scope: a repo with
  `.claude/` for project scope, `~/.claude/` for personal, a plugin
  root for plugin scope
- Write access to `<scope>/skills/<name>/`
- `$ARGUMENTS` may carry a name + intent, or a `SKILL.md` path, or be
  empty (in which case the skill prompts the user for intake)
- `/build:check-skill` available for the post-write audit step
- Optional: `present_files` tool available when running on
  Claude.ai / Copilot / Cowork (drives the Package-and-Present step)

## Steps

1. **Verify the primitive.** Confirm a skill is the right mechanism
   before drafting. Full decision matrix in
   [primitive-routing.md](../../_shared/references/primitive-routing.md).
   Redirect to `/build:build-hook` when the ask must fire at a
   lifecycle event regardless of LLM judgment; to `/build:build-rule`
   when it evaluates static file content against a path-scoped
   convention; to `/build:build-subagent` when it needs context
   isolation or different tool permissions; to a CLAUDE.md section
   when it's advisory always-on context. Proceed without a gate if
   intent is unambiguous; ask one clarifying question if uncertain.

2. **Capture intent.** Read `$ARGUMENTS`. Parse one of: a name + intent
   phrase (use the name, capture the trigger from the rest); a path to
   an existing `SKILL.md` (route to the Improve sub-step at Step 8);
   or empty (prompt the user). If the current conversation already
   contains a workflow the user wants to capture, extract the intent
   from the conversation — the tools invoked, the step sequence, the
   corrections, the I/O shapes observed. Confirm before proceeding.
   Ask for any missing pieces: what the skill should enable Claude to
   do, when it should trigger, and the expected output shape.

3. **Pick the scope.** Choose where the skill lives before drafting —
   the write step needs the full path, not a relative fragment.
   **project** → `.claude/skills/<name>/SKILL.md` (default when a
   `.claude/` directory exists in the repo). **personal** →
   `~/.claude/skills/<name>/SKILL.md`. **plugin** →
   `<plugin-root>/skills/<name>/SKILL.md`. **enterprise** →
   org-defined path.

4. **Check for conflicts.** Read existing skills at the chosen scope
   (and adjacent scopes where a router would route across them). Flag
   an existing skill with the same `name` or a `description` whose
   triggers overlap with the new skill. Ask: "This overlaps with
   `[existing skill]`. Merge, replace, or narrow the scope?" Routing
   ambiguity forces Claude to pick arbitrarily.

5. **Draft the skill.** Follow the anatomy in
   [skills-best-practices.md](../../_shared/references/skills-best-practices.md).
   Required frontmatter: `name`, `description`, `version`, `owner`.
   Required body sections: `## When to use`, `## Prerequisites`,
   `## Steps`, `## Failure modes`, `## Examples`. Optional frontmatter
   fields — `argument-hint`, `when_to_use`, `user-invocable: false`,
   `disable-model-invocation: true`, `paths:`, `allowed-tools`,
   `context: fork` + `agent:`, `model`, `effort`, `hooks`,
   `tested_with` — reach for only when the use case calls.
   `allowed-tools` takes canonical forms: space-separated string
   **or** YAML list. Never comma-separated as a string — YAML parses
   it as one literal. Name tokens `anthropic` and `claude` are
   platform-owned and rejected at load time. First ~5K tokens survive
   Claude Code compaction — lead with load-bearing content.

6. **Present for approval.** Before writing, narrate the design
   choices in 3–6 bullets. Cover the frontmatter choices and why any
   non-default field is set; the structure choices (ordering, where
   gates sit); and what was skipped and why (often more educational
   than what was used). A reader who doesn't know skill authoring
   should be able to follow the narration and disagree with any
   choice. Iterate on feedback. Hold the write until the user
   approves.

7. **Write.** Create the skill directory if it doesn't exist. Write
   `SKILL.md` to the full path from Step 3. Copy any bundled files
   (scripts, references) the draft names. Report the path. Claude
   Code picks up the new skill on next load. Then invoke
   `/build:check-skill` on the new skill — surface any findings and
   offer the repair loop before moving on.

8. **Improve (alternate path from Step 2).** When Step 2 resolves to
   an existing `SKILL.md`, read it; run `/build:check-skill`; collect
   findings; ask the user which to address (y / n /
   comma-separated); apply canonical repairs from the playbook; show
   diffs; write on confirmation; re-run `/build:check-skill` to
   verify. Generalize from feedback — narrow example-specific
   patches fail on the next invocation. If a stubborn issue keeps
   appearing, try a different framing rather than tightening
   constraints with ALL-CAPS directives.

9. **Package and present (optional).** Only when the `present_files`
   tool is available (Claude.ai / Copilot / Cowork — see
   [platform-notes.md](references/platform-notes.md)), package the
   skill with `python -m scripts.package_skill <path/to/skill-folder>`
   and direct the user to the resulting `.skill` file.

## Failure modes

- **Primitive mismatch.** If Step 1 is skipped and the ask is really
  a hook / rule / subagent / CLAUDE.md section, the resulting skill
  never triggers at the right moment. Recovery: redirect and stop;
  do not write a skill that papers over the wrong primitive.
- **Overlapping description with an existing skill.** The router
  picks one arbitrarily, so neither skill fires reliably. Recovery:
  resolve in Step 4 by narrowing one description, merging the
  workflows, or deleting the stale overlap.
- **User declines the draft at the approval gate.** Expected.
  Recovery: capture the specific objection, revise the draft, and
  re-present; do not write until the objection is addressed.
- **check-skill findings block the write.** After Step 7, if
  `/build:check-skill` surfaces FAIL findings on the new skill,
  apply the canonical repair from `repair-playbook.md` and re-audit
  until only WARNs remain (or until the user explicitly accepts a
  FAIL).
- **Destructive-intent skill without `disable-model-invocation`.**
  The skill can auto-fire during routing, triggering the destructive
  workflow without the user's intent. Recovery: set
  `disable-model-invocation: true` on any skill whose auto-invocation
  is dangerous.

## Examples

<example>
Invocation:

```bash
/build:build-skill process-pdfs Use when the user asks to extract text from a PDF
```

Step 1 — Primitive confirmed (reusable on-demand workflow).

Step 2 — Intent: extract text from PDFs. Trigger: user pastes a PDF
path or asks "extract text from this PDF".

Step 3 — Scope: `.claude/` exists in the repo → project scope →
`.claude/skills/process-pdfs/SKILL.md`.

Step 4 — No existing `process-pdfs` skill; no description collision.

Step 5 — Drafts `SKILL.md` with required frontmatter (`name: process-pdfs`,
`description: Use when…`, `version: 0.1.0`, `owner: <team>`) and
required body sections.

Step 6 — Narrates:
> - `name: process-pdfs` — gerund form, improves trigger match for "processing PDFs"
> - Prerequisites names `pdftotext` (poppler) and a sample tests directory — cross-checked against Steps
> - No `disable-model-invocation` — this is read-only; auto-triggering is safe
> - Skipped `context: fork` — the user will want to see tool calls while iterating

Step 7 — On approval, writes `.claude/skills/process-pdfs/SKILL.md`.
Runs `/build:check-skill` — 0 findings. Reports the path.
</example>

## Key Instructions

- Run Step 1 (Verify Primitive) before drafting — redirect to
  `/build:build-hook`, `/build:build-rule`, `/build:build-subagent`,
  or CLAUDE.md when the ask fits a different primitive
- Draft against the anatomy and principles from
  [skills-best-practices.md](../../_shared/references/skills-best-practices.md);
  don't invent frontmatter fields or required sections
  (`/build:check-skill`'s Tier-1 flags unknown structural shapes)
- Lead with load-bearing content in the first ~5K tokens —
  compaction-safe window
- Hold the write until the user approves the draft (Step 6 gate)
- After writing, run `/build:check-skill` — this skill must produce
  skills that pass the deterministic checks

## Anti-Pattern Guards

1. **Capability-shaped description.** "Handles X" over "Use when the
   user asks to X" defeats routing. Principle: *Write the description
   as a retrieval signal.*
2. **Prose `## Steps` section.** Paragraphs or unnumbered bullets
   degrade instruction-following. Principle: *Write Steps as a
   numbered sequence of atomic actions.*
3. **Commentary inside step body.** Rationale in steps dilutes the
   imperative. Principle: *Write Steps as a numbered sequence of
   atomic actions.*
4. **Embedded secrets.** Credentials in committed skill files are a
   breach. Principle: *No embedded secrets.*
5. **Unverified remote execution in steps.** `curl | bash` /
   `eval $(curl …)` are supply-chain vectors. Principle: *No
   unverified remote execution.*
6. **Destructive step without approval gate.** `rm -rf`, `DROP TABLE`,
   force-push, production deploy without a preceding confirmation.
   Principle: *Destructive operations gate on confirmation.*
7. **Writing before approval.** Always show the draft and narrate
   design choices first; the user must explicitly approve before
   `SKILL.md` is written.
8. **Invented frontmatter keys.** Unknown top-level frontmatter is
   silently ignored by Claude Code. Stick to the documented spec;
   cross-check against a peer toolkit skill when uncertain.
9. **Absolute paths in bundled references.** `/home/…` or
   drive-letter paths break portability. Principle:
   *(Anatomy — bundled assets referenced by relative path only.)*

## Handoff

**Receives:** Skill name + intent, or path to an existing SKILL.md
(routes to Improve), or no argument (prompts for intake).

**Produces:** `SKILL.md` written to `<scope>/skills/<name>/SKILL.md`;
optional `.skill` package when `present_files` is available.

**Chainable to:** `/build:check-skill` (to audit the just-built
skill); `/work:verify-work` (to validate against a broader plan).
