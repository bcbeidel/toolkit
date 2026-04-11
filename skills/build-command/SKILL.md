---
name: build-command
description: >
  Scaffolds a Claude Code slash command file under .claude/commands/ with
  description, argument handling, and a prompt body. Use when the user
  wants to "create a command", "build a slash command", "scaffold a command",
  "add a custom /command", "make a slash command", or needs a reusable
  prompt template for a repeated task.
argument-hint: "[command name] [purpose description]"
user-invocable: true
---

# Build Command

Scaffold a `.claude/commands/<name>.md` — a reusable slash command that
loads a full prompt into Claude's context when invoked.

## Intake

Elicit three things, one question at a time:

1. **Command name** — lowercase, hyphens allowed, no spaces (e.g. `review-pr`, `summarize`)
2. **Purpose** — one sentence: what should this command do when invoked?
3. **Argument hint** (optional) — how will the user supply input? (e.g. `[PR number]`, `[file path]`, leave blank if no arguments needed)

If the user provided all three upfront, skip to Overlap Check.

## Overlap Check

Before drafting, check whether this command duplicates something that already exists:

1. Read frontmatter `name` fields from `skills/*/SKILL.md` — these are existing `/wos:<name>` skills
2. If `.claude/commands/` exists, list its files

If the proposed command name or purpose substantially duplicates an existing skill or command, surface the overlap:

> "There's already a `/wos:<name>` skill that does [X]. Do you want to build a command that wraps it, rename this command, or proceed anyway?"

Wait for the user's answer before drafting.

## Draft

Produce the command file content. A Claude Code command is a Markdown file
with YAML frontmatter and a prompt body:

```markdown
---
description: [one sentence — what this command does and when to use it]
argument-hint: "[hint or omit if no args]"
---

# [Command Name]

[Prompt body. This text becomes part of Claude's context when the command
is invoked. Write it as instructions Claude should follow.]

[If the command accepts arguments, reference them as $ARGUMENTS.]
```

**Draft guidelines:**
- `description` should be concise and specific — it appears in command pickers
- The prompt body should read like instructions, not documentation
- Include 1–2 inline examples if argument usage isn't obvious
- `$ARGUMENTS` is the only variable available; it contains everything the user typed after the command name

Present the full draft to the user.

## Review Gate

Present the draft in full and wait for explicit user approval before writing
any file to disk. Do not write anything before this gate passes.

If the user requests changes, revise and re-present. Repeat until approved.

## Save

Write the approved content to `.claude/commands/<name>.md`.

Confirm the path to the user:
> "Written to `.claude/commands/<name>.md`. Invoke it with `/<name>` or `/<name> [arguments]`."

## Handoff

**Receives:** Command name, purpose description, optional argument hint
**Produces:** `.claude/commands/<name>.md` ready for use as a Claude Code slash command
**Chainable to:** check-command (to review the command after creation)
