# Skill Writing Guide

Reference for structuring and writing the SKILL.md body. Read this when drafting
a new skill or reviewing an existing one.

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

## Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

**Key patterns:**
- Keep SKILL.md under 500 lines; if approaching this limit, move detail to references/ with clear pointers about where to go next *(check-skill #1)*
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

## Lifecycle & Compaction

Skills aren't scripts — they're standing instructions that enter the
conversation once and persist.

**Normal lifecycle.** When a skill triggers, Claude Code renders the
SKILL.md body into a single message and inserts it into the
conversation. That message stays for the whole session. Every turn
after the trigger reads the same body. Nothing reloads unless the
user re-triggers.

**After compaction.** When the conversation is compacted (either
explicitly via `/compact` or automatically near the context limit),
skills are re-attached with two caps:

- **5,000 tokens per skill** — only the first 5K tokens of each
  re-attached SKILL.md survive. Content past that point is dropped.
- **25,000 tokens combined** — all re-attached skills share a single
  25K budget. Skills beyond the budget are dropped entirely.

**Practical implications:**

- **Put the load-bearing instructions first.** The trigger phrase lives
  in `description`, but the body's first 5K tokens are the only part
  guaranteed to survive compaction. Structure accordingly.
- **Write standing instructions, not one-time steps.** A body that
  says "First, introduce yourself" or "Start by asking three questions"
  goes stale after the first use and confuses the model on re-read.
  Write procedures that apply consistently throughout a task: "When
  processing a file, extract the header first." "Gate destructive ops
  on explicit user approval." These read correctly on every turn.
- **Use progressive disclosure for long content.** Move detail to
  `references/` instead of inlining it. Reference files load on
  demand and don't consume the 25K combined budget unless actually
  loaded.
- **The soft-cap of 500 lines in the body isn't arbitrary** — it
  approximates the post-compaction survival zone. Skills that blow
  past it risk losing their tail after a long conversation.

## Degrees of Freedom

Match instruction specificity to task fragility. Fragile tasks get
narrow, explicit instructions; routine tasks get broad prose. Over-
specifying a routine task produces brittle skills that break on edge
cases Claude could have handled; under-specifying a destructive task
produces skills that fail dangerously.

| Freedom | When to use | Form |
|---------|-------------|------|
| **Low** | Destructive / irreversible operations (deploy, rm -rf, DROP TABLE, force-push, external API writes). | Scripts or pseudocode with no parameters. Explicit gates. No variation allowed. |
| **Medium** | External effects where tool order matters (refactors, migrations, multi-step writes). | Parameterized steps that name specific tools and state data-flow between steps. |
| **High** | Reversible, low-stakes operations (file transforms, analysis, doc generation, reads). | Prose that describes the intent and lets Claude pick tools and order. |

Examples:

- **Low** — deploy script: "Run `./bin/deploy.sh --env=prod`. Do not
  substitute. Do not parameterize. If the script is missing, stop."
- **Medium** — migration workflow: "1. Run `alembic upgrade head`. 2. Verify
  `alembic current` matches expected head. 3. If mismatch, roll back via
  `alembic downgrade -1`."
- **High** — code review: "Review the diff for correctness, style, and
  security. Surface concerns proportional to severity. Skip nits unless
  asked."

Calibration heuristic: if you'd feel uneasy watching Claude improvise
the task, specify more. If you'd feel uneasy watching Claude follow a
script verbatim, specify less.

## Substitutions

When `argument-hint` is set in frontmatter, the body must consume the
user's argument explicitly. Otherwise Claude Code appends `ARGUMENTS:
<value>` at the end of the rendered skill — wrong position relative to
the workflow.

| Token | Meaning |
|-------|---------|
| `$ARGUMENTS` | The full argument string passed at invocation. |
| `$ARGUMENTS[N]` | The Nth whitespace-separated token (zero-indexed). |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g. `$0`, `$1`). |
| `${CLAUDE_SESSION_ID}` | Current session identifier. |
| `${CLAUDE_SKILL_DIR}` | Absolute path of the directory containing this SKILL.md — useful for referencing bundled scripts and references. |

Examples:

```
1. Read the file at $ARGUMENTS.
2. Compare $0 (current branch) against $1 (target branch).
3. Load the schema from ${CLAUDE_SKILL_DIR}/references/schema.yaml.
```

Insert substitutions at the workflow step that consumes the input — not
in a generic preamble. Position matters because Claude reads the body
top-to-bottom.

## Dynamic Context

Inline `` !`<command>` `` and fenced ` ```! ` blocks are evaluated by
Claude Code **before** the skill is sent to Claude. Their stdout is
substituted into the rendered text, so Claude sees the data as if it
were always there.

```
The current branch is !`git branch --show-current`.

Recent commits:
```!
git log --oneline -5
```
```

Use this for state Claude could have received pre-rendered — git
status, file lists, environment fingerprints — not as a substitute for
arbitrary tool calls during the workflow. Pre-rendering saves a tool
round-trip and lands the data in the right position; it's not a way to
hide side effects.

Note: any command that modifies state will execute on every
invocation. Reserve dynamic context for read-only commands.

## On-Demand Hooks

Skills can register lifecycle hooks that activate only when the skill runs and
expire at session end. Use this for safety guardrails or automation too
opinionated to run globally:

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "echo 'blocked' && exit 1"
```

Examples: `/careful` — blocks `rm -rf`, force-push, DROP TABLE; `/freeze` — blocks
edits outside a specific directory. The user opts in by invoking the skill; it
doesn't affect other sessions.

## Setup Configuration (`config.json`)

When a skill needs user-provided configuration (API keys, project IDs,
preferences), store it in a `config.json` file in the skill directory. Check for
it on invocation — if missing, ask the user for the values using
`AskUserQuestion`, then write the file. Subsequent runs skip the setup.

```markdown
## Instructions

1. Check if `${CLAUDE_SKILL_DIR}/config.json` exists
2. If missing, ask the user for [required fields] using AskUserQuestion, then write the file
3. Load config and proceed
```

## Skill Composition

Skills can invoke other skills by name — just reference the skill name in the
instructions and the model will invoke it if installed. Document required skills
as a won't-work-without dependency in `## Key Instructions`:

```markdown
## Key Instructions

- Requires the `fetch-data` skill to be installed — won't produce useful output without it
```

## Persistent State

Data written to the skill directory may be deleted on upgrade. For state that
should survive upgrades (logs, cached results, learned preferences), write to
`${CLAUDE_PLUGIN_DATA}` — a stable per-plugin path set by Claude Code.

## Principle of Lack of Surprise

Skills must not contain malware, exploit code, or any content that could
compromise system security. A skill's contents should not surprise the user in
their intent if described. Don't go along with requests to create misleading
skills or skills designed to facilitate unauthorized access, data exfiltration,
or other malicious activities. Roleplay-framing skills are fine.

## Writing Style

Explain *why* things are important rather than issuing heavy-handed MUSTs. Use
theory of mind — make the skill general and not narrowly overfit to specific
examples. Start with a draft, then read it fresh and improve it. *(check-skill #2)*

## Writing Patterns

Prefer imperative form in instructions.

**Defining output formats:**
```markdown
## Report structure
Use exactly this template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

## Quality Requirements

Every skill must satisfy these before the draft is final — `check-skill` will
flag any that are missing:

| # | Requirement |
|---|-------------|
| 3 | `## Handoff` present; Receives/Produces use specific descriptors (not "document", "output", "data") |
| 4 | `## Anti-Pattern Guards` present with at least one guard |
| 5 | At least one explicit gate (user approval, lint check, precondition) before a consequential step |
| 6 | At least one concrete example — invocation, sample output, or table row with a real case |
| 8 | Each rule produces a consistent decision; two developers reading it would make the same choice |
| 9 | Each rule would cause a mistake if removed — cut anything that restates model defaults |
| 10 | No "act as X" or "you are a senior X expert" persona framing — degrades task performance |
| 12 | No contradictions: if rule A says "always X" and rule B says "never X" for the same scenario, remove one |
| 14 | Multi-step workflows (≥3 steps): steps numbered, ordered, inter-step dependencies stated |
| 15 | Most consequential rules (irreversible actions, hard constraints) at the top of `## Key Instructions` |
| 16 | At least one failure mode addressed — missing input, unmet precondition, or mid-workflow failure |
| 22 | If workflow includes loops or retries: explicit termination condition stated |
