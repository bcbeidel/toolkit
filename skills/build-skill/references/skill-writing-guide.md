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
