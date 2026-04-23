---
name: build-skill
description: Create a new Claude Code SKILL.md or improve an existing one. Use when the user wants to "create a skill", "add a skill", "build a skill", "scaffold a skill", "new skill for [X]", "write a skill that does X", or wants to capture a recurring workflow as a reusable skill.
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

## Workflow

### 0. Verify Primitive

Before proceeding, confirm a skill is the right mechanism. Full decision
matrix: [primitive-routing.md](../../_shared/references/primitive-routing.md).

A skill is right when:
- The user wants to invoke a reusable procedure on demand
- The workflow recurs across sessions and benefits from being captured once
- The steps are specific enough to execute without re-derivation at each invocation

Redirect when:
- Must fire at a lifecycle event regardless of LLM judgment → `/build:build-hook`
- Evaluates static file content against a path-scoped convention → `/build:build-rule`
- Needs context isolation or different tool permissions than the parent → `/build:build-subagent`
- Is advisory always-on context (not a procedure) → a CLAUDE.md section

Proceed without a gate if intent is unambiguous; ask one clarifying question if uncertain.

### 1. Intake

Read `$ARGUMENTS`. Parse one of:
- **Name + intent** (`/build:build-skill process-pdfs Use when the user pastes a PDF path…`) — propose the name, capture the trigger from the rest
- **Path to an existing SKILL.md** — load it and route to the Improve sub-workflow (Step 7)
- **No argument** — ask the user for the name and a one-sentence trigger phrase

If the current conversation already contains a workflow the user wants
to capture ("turn this into a skill"), extract the intent from the
conversation: the tools invoked, the step sequence, the corrections
made, the input/output shapes observed. Confirm with the user before
proceeding.

Ask for any missing:
1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases / file patterns / lifecycle events)
3. What's the expected output shape?

### 2. Scope

Pick where the skill lives before drafting — the write step needs the
full path, not a relative fragment:

| Scope | Path | When to use |
|---|---|---|
| **project** | `.claude/skills/<name>/SKILL.md` | Repo-specific; ships with the codebase |
| **personal** | `~/.claude/skills/<name>/SKILL.md` | Single-user, all projects |
| **plugin** | `<plugin-root>/skills/<name>/SKILL.md` | Contributing to a plugin marketplace |
| **enterprise** | org-defined | Managed deployment |

If the user hasn't named a scope, default to `project` when a `.claude/`
directory exists in the current repo; otherwise `personal`.

### 3. Conflict Check

Read existing skills at the chosen scope (and adjacent scopes where a
router would route across them). Look for:
- Existing skill with the same `name`
- Existing skill whose `description` triggers on the same user phrases

If overlap found, ask: "This overlaps with `[existing skill]`. Merge,
replace, or narrow the scope?" Routing ambiguity forces Claude to pick
arbitrarily.

### 4. Draft

Follow the anatomy from
[skills-best-practices.md](../../_shared/references/skills-best-practices.md).
Required frontmatter: `name`, `description`, `version`, `owner`.
Required body sections: `## When to use`, `## Prerequisites`, `## Steps`,
`## Failure modes`, `## Examples`.

Optional frontmatter fields — reach for them only when the use case calls:

- `argument-hint` — one-line CLI hint; when set, body must consume via `$ARGUMENTS`, `$ARGUMENTS[N]`, or `$N` substitution
- `when_to_use` — split for trigger phrases when `description` would exceed 1024 chars (combined cap 1536)
- `user-invocable: false` — background-knowledge skills preloaded into an agent rather than called directly
- `disable-model-invocation: true` — destructive or irreversible skills that should never auto-trigger
- `paths:` — glob patterns that scope auto-activation (useful in monorepos)
- `allowed-tools` — canonical forms: space-separated string **or** YAML list. Never comma-separated as a string — YAML parses it as one literal
- `context: fork` + `agent:` — run in an isolated subagent; declare the subagent's operational scope in `## Key Instructions`
- `model` / `effort` / `hooks` / `tested_with` — override session defaults; omit when default

Name reserved-token check: `anthropic` and `claude` in the `name` field
are platform-owned and rejected at load time.

First ~5K tokens of a skill are what survives Claude Code compaction —
lead with load-bearing content (frontmatter, `## When to use`, first
Steps). Reference material moves to `references/<topic>.md` and loads
on demand.

### 5. Present for Approval

Before writing, narrate the design choices in 3–6 bullets. Cover:
- **Frontmatter choices** — name the field and the reasoning ("set `disable-model-invocation: true` because this deploys to production")
- **Structure choices** — why the workflow is ordered as it is, where gates are placed
- **What was skipped and why** — patterns considered but rejected; often more educational than what was used

A reader who doesn't know skill authoring should be able to follow the
narration and disagree with any choice. If you can't explain a choice
clearly, revisit it.

Iterate on feedback. Hold the write until the user approves.

### 6. Write

- Create the skill directory if it doesn't exist
- Write `SKILL.md` to the full path from Step 2
- Copy any bundled files (scripts, references) the draft names
- Report the path

Claude Code picks up the new skill on next load.

After writing, invoke `/build:check-skill` on the new skill — surface
any findings and offer the repair loop before moving on.

### 7. Improve (alternate path from Step 1)

When Step 1 resolves to an existing SKILL.md, branch here:

1. Read the SKILL.md
2. Run `/build:check-skill` on it; collect findings
3. Ask the user which findings to address (y / n / comma-separated)
4. Apply canonical repairs from the playbook; show diffs; write on confirmation
5. Re-run `/build:check-skill` to verify

Generalize from feedback — narrow example-specific patches fail on the
next invocation. If a stubborn issue keeps appearing, try a different
framing or metaphor rather than tightening constraints with ALL-CAPS
directives.

## Platform-Specific Instructions

If you're on **Claude.ai**, **Copilot**, or **Cowork**, some mechanics
differ from the standard Claude Code workflow. Read
[platform-notes.md](references/platform-notes.md) for what to skip,
adapt, or substitute.

## Package and Present (only if `present_files` tool is available)

Check whether the `present_files` tool is available in the current
environment. If not, skip. If yes, package the written skill:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Direct the user to the resulting `.skill` file so they can install it.

## Key Instructions

- Run Step 0 (Verify Primitive) before drafting — redirect to `/build:build-hook`, `/build:build-rule`, `/build:build-subagent`, or CLAUDE.md when the ask fits a different primitive
- Draft against the anatomy template and principles from [skills-best-practices.md](../../_shared/references/skills-best-practices.md); don't invent frontmatter fields or required sections (`check-skill`'s Tier-1 flags unknown structural shapes)
- Lead with load-bearing content in the first ~5K tokens — that's the compaction-safe window
- Hold the write until the user approves the draft (Step 5 gate)
- After writing, run `/build:check-skill` — build-skill must produce skills that pass the deterministic checks

## Anti-Pattern Guards

1. **Capability-shaped description** — "Handles X" over "Use when the user asks to X" defeats routing. Principle: *Write the description as a retrieval signal.*
2. **Prose `## Steps` section** — paragraphs or unnumbered bullets degrade instruction-following. Principle: *Write Steps as a numbered sequence of atomic actions.*
3. **Commentary inside step body** — rationale in steps dilutes the imperative. Principle: *Write Steps as a numbered sequence of atomic actions.*
4. **Embedded secrets** — credentials in committed skill files are a breach. Principle: *No embedded secrets.*
5. **Unverified remote execution in steps** — `curl | bash` / `eval $(curl …)` are supply-chain vectors. Principle: *No unverified remote execution.*
6. **Destructive step without approval gate** — `rm -rf` / `DROP TABLE` / force-push / production deploy without a preceding confirmation. Principle: *Destructive operations gate on confirmation.*
7. **Writing before approval** — always show the draft and narrate design choices first; the user must explicitly approve before `SKILL.md` is written.
8. **Invented frontmatter keys** — unknown top-level frontmatter is silently ignored by Claude Code. Stick to the documented spec; cross-check against a peer toolkit skill when uncertain.
9. **Absolute paths in bundled references** — `/home/…` or drive-letter paths break portability. Principle: *(Anatomy — bundled assets referenced by relative path only.)*

## Example

<example>
User: `/build:build-skill process-pdfs Use when the user asks to extract text from a PDF`

Step 0 — Primitive confirmed (reusable on-demand workflow).

Step 1 — Intent: extract text from PDFs; trigger: user pastes a PDF path or asks "extract text from this PDF".

Step 2 — Scope: `.claude/` exists in the repo → project scope → `.claude/skills/process-pdfs/SKILL.md`.

Step 3 — No existing `process-pdfs` skill; no description collision found.

Step 4 — Drafts `SKILL.md` with required frontmatter (`name: process-pdfs`, `description: Use when…`, `version: 0.1.0`, `owner: <team>`) and required body sections.

Step 5 — Narrates:
> - `name: process-pdfs` — gerund form, improves trigger match for "processing PDFs"
> - Prerequisites names `pdftotext` (poppler) and a sample tests directory — cross-check against Steps
> - No `disable-model-invocation` — this is read-only; auto-triggering is safe
> - Skipped `context: fork` — you'll want to see tool calls while iterating

Step 6 — On approval, writes `.claude/skills/process-pdfs/SKILL.md`. Runs `/build:check-skill` — 0 findings. Reports the path.
</example>

## Handoff

**Receives:** Skill name + intent, or path to an existing SKILL.md (routes to Improve), or no argument (prompts for intake)
**Produces:** `SKILL.md` written to `<scope>/skills/<name>/SKILL.md`; optional `.skill` package when `present_files` is available
**Chainable to:** check-skill (to audit the just-built skill); verify-work (to validate against a broader plan)
