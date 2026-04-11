---
name: check-command
description: >
  Audits Claude Code slash commands for description clarity, argument
  handling, scope creep, and overlap with existing skills. Use when the
  user wants to "audit commands", "review a command", "check commands",
  "improve a command", "find redundant commands", or "what's wrong with
  my commands".
argument-hint: "[command name | path to command file]"
user-invocable: true
---

# Check Command

Inspect `.claude/commands/` files for quality and redundancy. Read-only —
reports findings but does not modify any files.

## Input

Accept one of:
- A command name — reads `.claude/commands/<name>.md`
- A file path — reads the file directly
- No argument — scans all files in `.claude/commands/`

If `.claude/commands/` does not exist and no file path was given, report:
> "No `.claude/commands/` directory found. Nothing to audit."

## Checks

Run four checks against each command file.

### 1. Description clarity

Read the `description` field in the frontmatter.

Signals of a weak description:
- Vague verb ("handle", "do", "manage") with no object
- Missing "when to use" — the description should indicate what prompts
  invoke this command, not just what it does
- Over-long (paragraph-length) descriptions better suited to a README

Flag as `warn` if description is empty, missing, or does not clearly state
what the command does and when to use it.

### 2. Argument handling

Check whether the command body uses `$ARGUMENTS`.

Signals of poor argument handling:
- `$ARGUMENTS` is referenced but no `argument-hint` appears in frontmatter
  (user has no guidance on what to supply)
- `$ARGUMENTS` appears multiple times in ways that suggest different values
  are expected (they all receive the same string)
- The command clearly expects input but `$ARGUMENTS` is never referenced
  (input will silently be ignored)

Flag as `warn` per signal found.

### 3. Scope creep

Check whether the command does multiple unrelated things.

Signals:
- Conjunctions in the description ("and also", "then") suggesting
  multiple distinct outcomes
- Multiple independent workflow phases with no clear connection
- The command is longer than ~50 lines and covers more than one subject

A command should do one thing well. If it does more, suggest splitting.
Flag as `warn` if scope appears broader than a single coherent action.

### 4. Skill overlap

Check whether this command duplicates a capability already provided by a
WOS skill or another command.

1. Read frontmatter `name` fields from all `skills/*/SKILL.md` files
2. Compare the command's purpose against each skill's description
3. Check for other files in `.claude/commands/` with similar purposes

Flag as `warn` if substantive overlap is found, noting which skill or
command the duplication involves. Overlap is not always a problem —
a command may be an intentional thin wrapper around a skill — but the
redundancy should be surfaced.

## Report

Present findings as a table with a summary count at the top:

```
N issues across M commands (X warn)

command          | check               | finding
-----------------+---------------------+---------------------------------
review-pr        | Argument handling   | $ARGUMENTS used but no argument-hint set
summarize        | Skill overlap       | Duplicates /wos:distill (description match)
```

If no issues are found, confirm:
> "All commands look well-formed."

## Handoff

**Receives:** Command name, file path, or no argument (scans all)
**Produces:** Findings table per command; read-only — no files modified
**Chainable to:** build-command (to create or revise a command based on findings)
