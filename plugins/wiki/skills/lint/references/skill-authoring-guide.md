# Skill Authoring Guide

How to write effective skills for Claude Code. This guide covers
structure, conventions, and quality criteria. It also serves as the
rubric when `/wiki:lint` evaluates skill quality.

## The Loading Model

Skills load progressively in three levels:

| Level | When Loaded | Token Cost | Content |
|-------|------------|------------|---------|
| L1: Metadata | Always (startup) | ~100 tokens | `name` + `description` from frontmatter |
| L2: Instructions | When triggered | <5K tokens | SKILL.md body |
| L3: Resources | As needed | Unbounded | Reference files, scripts, assets |

Only L1 is always in context. L2 loads when Claude decides the skill
is relevant — based entirely on the description. L3 loads only when
SKILL.md references a file and the task needs it.

## Required Frontmatter

Every SKILL.md starts with YAML frontmatter:

```yaml
---
name: my-skill-name
description: >
  Performs specific actions on target artifacts. Use when the user
  wants to "do X", "run Y", or "check Z".
argument-hint: "[optional hint for slash command input]"
user-invocable: true
references:
  - references/detailed-guide.md
---
```

### `name` (required)

- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- Cannot contain "anthropic" or "claude"
- Should describe the action, not the target: `lint` not `lint-documents`

### `description` (required)

The most important field. Claude uses it to decide whether to load
the skill from 100+ available skills. Must include:

1. **What** the skill does (lead with this)
2. **When** to use it (trigger phrases)

Conventions:
- Third person voice: "Converts research into..." not "You can use this to..."
- Maximum 1024 characters
- No XML tags
- Be specific — vague descriptions prevent discovery

**Good:**
```yaml
description: >
  Converts research artifacts into focused context documents. Use when
  the user wants to "distill research", "extract findings", or "create
  context from research".
```

**Bad:**
```yaml
description: Helps with documents
```

### Optional Fields

Most skills need only `name` + `description`. Reach for these when the default behavior doesn't fit:

| Field | Reach for it when... | Example |
|-------|----------------------|---------|
| `argument-hint` | The skill takes a slash-command argument the user needs to know about | `"[issue-number]"` |
| `user-invocable: false` | The skill is background knowledge for agents, not a command users call directly — hides it from the `/` menu | A `library-conventions` skill preloaded into a review agent |
| `disable-model-invocation: true` | The skill is dangerous or consequential and should only fire when the user explicitly invokes it — prevents auto-triggering | A `deploy-production` skill |
| `model` | The skill should run on a different model than the session default — fast lookups warrant `haiku`; complex multi-step work warrants `opus` | `model: haiku` |
| `effort` | The skill needs more or less reasoning depth than the session default | `effort: low` for templating; `effort: high` for review |
| `context: fork` | The skill spawns an isolated subagent — the parent context only sees the final result, not intermediate tool calls | Batch operations, parallel eval runs |
| `agent` | The subagent type to use when `context: fork` is set | `agent: general-purpose` |
| `hooks` | The skill needs lifecycle automation scoped to its session — see [On-Demand Hooks](#on-demand-hooks) below | Block destructive ops while the skill runs |
| `paths` | The skill should only auto-activate when working with specific files — useful in monorepos to prevent a backend skill triggering in frontend code | `paths: "packages/backend/**"` |
| `shell` | The skill uses `` !`command` `` blocks on Windows | `shell: powershell` |
| `allowed-tools` | The skill uses specific tools repeatedly and you want to skip per-use confirmation prompts | `allowed-tools: "WebFetch, Bash(npm run *)"` |
| `references` | The skill has reference files or assets in the skill directory that should be available for progressive disclosure | `references: [references/api.md]` |

## SKILL.md Body

The body contains instructions Claude follows when the skill triggers.

### Size Limits

- **≤500 non-blank lines** in SKILL.md body
- **≤200 instruction lines** across SKILL.md + all references (configurable)
- If approaching either limit, split content into reference files

### Writing Style

- **Imperative voice:** "Read the document" not "The document should be read"
- **Consistent terminology:** Pick one term and use it throughout
- **No time-sensitive information**
- **Adapt to audience:** Consider the likely technical range of users.
  Briefly explain domain-specific terms (e.g., "assertion", "JSON")
  when context cues suggest the user may not know them. Don't
  over-explain for expert audiences.

### The Token-Earning Test

Every instruction should earn its place. Two questions to ask:

1. **"Does Claude already know this?"** — A paragraph explaining what
   PDFs are wastes tokens. A line showing which library to use earns
   its place.
2. **"Is this pulling its weight?"** — An instruction can be correct
   and still not help. If removing a section wouldn't change output
   quality, the section is dead weight. Lean skills outperform verbose
   ones because signal isn't diluted by noise.

### Freedom Matches Fragility

Match instruction specificity to how fragile the operation is:

| Fragility | Freedom | Example |
|-----------|---------|---------|
| High (exact sequence matters) | Low — exact commands | Database migrations, phase gates |
| Medium (preferred pattern) | Medium — pseudocode | Report generation with parameters |
| Low (many valid approaches) | High — general guidance | Code review, analysis |

### Dynamic Shell Injection (Claude Code only)

Embed a shell command directly in SKILL.md using the `` !`command` `` syntax.
Claude runs it at invocation time and the model sees only the result — not the
command itself. Useful for injecting live context the skill needs without asking
the user for it:

```markdown
Current branch: !`git branch --show-current`
Staged files: !`git diff --cached --name-only`
```

This is a Claude Code-only feature. On Copilot, Cursor, and other platforms,
`` !`command` `` blocks render as literal Markdown text — they are silently
ignored. Do not use in cross-platform skills.

### On-Demand Hooks

Skills can register lifecycle hooks that activate only when the skill runs and expire at session end. Use this when you want opinionated safety guardrails or automation that would be too aggressive to run globally.

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo 'blocked' && exit 1"
```

Classic examples from inside Anthropic:
- **`/careful`** — blocks `rm -rf`, `DROP TABLE`, force-push, `kubectl delete` via a `PreToolUse` Bash matcher. Invoke when doing risky refactors; leave off for normal work.
- **`/freeze`** — blocks any Edit/Write outside a specific directory. Invoke when you want Claude confined to one package.

The key design principle: hooks that are too opinionated for everyday use belong in skills, not global settings. The user opts in by invoking the skill.

### Agent Skills (`user-invocable: false`)

A skill with `user-invocable: false` is background knowledge, not a command. It's hidden from the `/` menu and designed to be preloaded into a subagent's context at startup via the `skills:` field in the agent definition.

Use this pattern when:
- The skill is domain knowledge a specialized agent should always have (e.g., `billing-api-conventions` for a billing agent)
- The skill should never be directly invoked — it's context, not a workflow
- You're building a `context: fork` agent and want to inject instructions without polluting the main session

```yaml
---
name: billing-api-conventions
description: Conventions for working with the internal billing API — error handling, retry patterns, rate limits
user-invocable: false
---
```

### Persistent State (`${CLAUDE_PLUGIN_DATA}`)

Data written to the skill directory may be deleted when the plugin upgrades. For state that should survive upgrades — usage logs, learned preferences, cached lookups — write to the `${CLAUDE_PLUGIN_DATA}` directory instead. Claude Code sets this to a stable per-plugin path outside the skill directory.

```markdown
Save state to: ${CLAUDE_PLUGIN_DATA}/history.json
```

Formats that work well: append-only text logs (simplest), JSON files, SQLite (for structured queries).

### Monorepo Skill Discovery

Skills in nested `.claude/skills/` directories are discovered **on-demand**, not at startup. A skill at `packages/frontend/.claude/skills/react-patterns/` only loads when Claude works with files in `packages/frontend/` — backend developers never see it.

This means:
- Root `.claude/skills/` → always available (project-wide conventions, shared workflows)
- Package `.claude/skills/` → available only when in that package

Skill descriptions count against a character budget (default 15,000 characters across all loaded skills). In large monorepos with many packages, use `paths` in frontmatter to further constrain activation, and use `SLASH_COMMAND_TOOL_CHAR_BUDGET` to raise the budget if needed.

Consider namespacing package-level skill names to avoid confusion: `frontend-review`, `backend-deploy`, `shared-utils` rather than bare `review`, `deploy`.

## Required Structural Sections

Every SKILL.md body must include these three sections. Their presence
and content are audited by `/build:check-skill`.

### `## Handoff`

Describes what the skill receives, what it produces, and what it chains
to. Use concrete, specific descriptors — not generic placeholders like
"document", "output", or "data" that leave scope ambiguous.

```markdown
## Handoff

**Receives:** Path to a SKILL.md, or no argument for all-skills audit
**Produces:** Structured findings table; optionally, targeted edits applied to audited skills
**Chainable to:** build-skill (to create a replacement), start-work (for bulk repair)
```

### `## Anti-Pattern Guards`

At least one explicit guard against predictable misuse or ordering errors.
Think: what's the most common way this skill goes wrong?

```markdown
## Anti-Pattern Guards

1. **Running LLM checks before lint** — static checks are deterministic and fast; always run them first
2. **Applying all fixes at once** — per-change confirmation is required; bulk application removes the user's ability to review individual changes
```

Treat this section as a **living section**: seed it with known failure modes when you write the skill, then add new guards as real failures emerge in use. Anti-Pattern Guards are the highest-signal content in a skill — they encode hard-won operational knowledge that instructions alone won't capture.

### `## Key Instructions`

The most consequential rules: irreversible actions, hard constraints, scope
limits. Critical instructions go **at the top**, not buried mid-list. Include
at least one explicit won't-do boundary — a statement that names what the
skill will not do, touch, or modify.

```markdown
## Key Instructions

- Won't modify files outside the project root
- Won't apply changes without user confirmation
- Read the existing skill before proposing edits
```

Won't-do scope is the most-skipped element in skill authoring and the most
impactful for preventing misuse. State it first.

### Behavioral Requirements

These patterns apply throughout the body — not only inside the three required
sections above:

**Gate checks.** Before any irreversible or shared-state step, require an
explicit confirmation or verifiable precondition. A user-approval prompt
counts; a lint check that must pass counts; a missing-input check that stops
the workflow counts.

**Routing guidance in `description`, not the body.** Do not add "When to Use
This Skill" or equivalent sections inside SKILL.md. The body loads only after
triggering — routing instructions there are never evaluated at routing time.

**Workflow step ordering.** Skills with ≥3 sequential steps must number them
explicitly and state any data-flow or ordering dependency. Don't imply
order — state it.

**Edge case handling.** Address at least one failure mode: missing input,
ambiguous input, a failed precondition, or a mid-workflow error. A gate that
blocks on missing input counts; a step that says "if X is unavailable, do Y"
counts. Silence on all failure modes is a gap.

## Reference Files

Additional files in `references/` that SKILL.md links to:

- **One level deep from SKILL.md** — Claude may partially read nested
  references. Never reference a file from another reference file.
- **Table of contents** for files >100 lines
- **Domain-organized** — split by topic, not by arbitrary size cuts
- File names should describe content: `source-evaluation.md` not `ref2.md`

## Skill Composition

Skills can invoke other skills by name — just reference the skill name in the instructions and the model will invoke it if installed. No explicit wiring is required.

```markdown
## Instructions

1. Run the `fetch-data` skill to get the latest metrics
2. Use the results to generate the report
```

Dependency management is not built into the runtime — if the referenced skill isn't installed, the model will try to proceed without it. Document required skills in `## Key Instructions` with a clear won't-work-without note:

```markdown
## Key Instructions

- Requires `fetch-data` skill to be installed — won't produce useful output without it
```

## Examples Beat Explanations

One concrete example often replaces a paragraph of description. When
steering output format or depth, show an input/output pair rather than
describing the expected result.

Use `<example>` tags for examples in skill instructions. 3-5 diverse
examples is the sweet spot for output-sensitive skills.

## Canonical Example: `distill`

The `distill` skill demonstrates these conventions:

**Frontmatter:** Third-person description with trigger phrases, 63
instruction lines total (well under threshold).

**Body:** 5 sequential workflow phases, each 3-6 lines. High-freedom
for judgment calls (what to distill), low-freedom for integration
steps (exact `python` commands).

**Reference:** One file (`distillation-guidelines.md`) at 41 lines,
covering splitting heuristics and word count rationale.

**What makes it effective:**
- Every instruction earns its tokens — no explaining what "distill" means
- Freedom varies: user controls granularity (high), but integration
  runs exact commands (low)
- Concise constraints section uses bold keywords for scannability

## Evaluation Criteria

When evaluating a skill, check these criteria:

### Automated (Python — checked by `lint.py`)

| Check | Severity | Standard |
|-------|----------|----------|
| `name` format | fail | lowercase, hyphens, ≤64 chars |
| `name` reserved words | fail | no "anthropic" or "claude" |
| `description` length | warn | ≤1024 characters |
| `description` XML tags | warn | none present |
| `description` voice | warn | third person (no "you can", "I can") |
| SKILL.md body size | warn | ≤500 non-blank lines |
| Instruction density | warn | ≤200 instruction lines (configurable) |

### Judgment (Claude — guided by this document)

**Structural sections** (checked by `/build:check-skill` criteria 3–7, 11, 13–16):

| Check | What to evaluate |
|-------|-----------------|
| Handoff section | Present? Receives/Produces/Chainable-to all populated with concrete descriptors — not generic placeholders like "document" or "output"? |
| Anti-Pattern Guards | Present with at least one guard? |
| Key Instructions | Won't-do scope present? Critical/irreversible rules listed first, not buried? |
| Gate checks | At least one explicit gate (user confirmation, lint pass, precondition check) before a consequential step? |
| Routing guidance | No "When to Use This Skill" or equivalent section in the body? All trigger conditions in `description` frontmatter? |
| Workflow ordering | If ≥3 sequential steps: numbered, explicitly ordered, dependencies stated — not implied? |
| Edge case handling | At least one failure mode addressed (missing input, ambiguous input, failed precondition, mid-workflow error)? |

**Content quality** (checked by `/build:check-skill` criteria 8–10, 12):

| Check | What to evaluate |
|-------|-----------------|
| Description triggers | Does it include both what + when? |
| Description breadth | Does it cast a wide enough net? Claude undertriggers — descriptions should be slightly "pushy", covering adjacent phrasings and contexts even when the user doesn't name the skill explicitly. |
| Freedom ↔ fragility | Do guardrail vs. guidance levels match the task? |
| Rationale over rigidity | Does the skill explain *why* behind instructions, or rely on rigid ALL-CAPS directives (MUST, NEVER, ALWAYS)? Explaining reasoning produces more intelligent adaptation than rigid commands. |
| Unnecessary context | Does the skill explain things Claude already knows? |
| Token-earning | Is every instruction pulling its weight, or could sections be removed without affecting output quality? |
| Generality | Is the skill written for broad use, or narrowly overfit to specific examples? Constraints should serve the general purpose, not patch individual test cases. |
| Examples quality | Are examples concrete and demonstrate expected depth? |
| Terminology consistency | Is vocabulary consistent throughout? |
| Reference depth | Are all references one level deep from SKILL.md? |
