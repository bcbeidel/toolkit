---
name: audit-subagent
description: >
  Audits Claude Code custom subagent definitions in .claude/agents/.
  Detects over-permissioned tool sets, unclear routing descriptions,
  incomplete handoff contracts, missing termination conditions, and
  overlap with existing skills. Use when the user wants to "audit
  subagents", "check my agents", "review agent permissions", "validate
  my agents directory", or "are my agents well-formed".
argument-hint: "[path to agent file (optional; defaults to scanning .claude/agents/)]"
user-invocable: true
---

# Audit Subagent

Inspect Claude Code custom subagent definitions for structural quality,
tool set hygiene, description clarity, and handoff contract completeness.
Produces structured findings in the same format as `scripts/lint.py`.

**Announce at start:** "I'm using the audit-subagent skill to inspect these
agent definitions."

## Workflow

### 1. Discover

If a file path argument was provided, audit only that file.

Otherwise, scan `.claude/agents/` recursively for `.md` files.

If the directory does not exist or contains no `.md` files:

> "No subagent definitions found at `.claude/agents/`. Nothing to audit."

Exit after reporting.

### 2. Run Seven Checks

For each definition file, run all seven checks in order.

#### Check 1 — Tool Over-Permissioning

Does the tool set include capabilities the description does not support?

Flag when:
- `Bash` is listed but the description has no mention of command execution,
  shell operations, or running processes
- `Write` or `Edit` are listed but the description only involves reading
  or reporting
- `WebFetch` or `WebSearch` are listed but the agent is described as
  internal-only
- `Agent` is listed but the description shows no evidence of orchestrating
  sub-agents
- More than 6 tools are listed for a narrowly-scoped agent (description
  covers a single workflow step)

Severity: **warn**

#### Check 2 — Tool Under-Permissioning

Does the description imply capabilities not covered by the tool set?

Flag when:
- Description says "writes", "creates", or "generates files" but `Write`
  is absent
- Description says "reads" or "analyzes" files but `Read` is absent
- Description mentions "runs" or "executes" but `Bash` is absent
- Description mentions "searches the web" or "fetches" external content
  but `WebFetch`/`WebSearch` are absent

Severity: **warn**

#### Check 3 — Description Quality

A well-formed description covers four things: what the agent does, when
to invoke it, when NOT to invoke it, and what it returns.

Flag when the description:
- Is a single short phrase with no invocation conditions ("handles data
  tasks", "processes files")
- Contains no exclusion or "when not to use" boundary
- Does not mention what the agent returns or produces
- Could apply equally well to a skill (no parallelism, isolation, or
  permission benefit stated)

Severity: **warn**

#### Check 4 — Handoff Contract Completeness

Context loss at handoffs is the second-most common multi-agent production
failure mode.

Flag when:
- No `## Handoff` section is present — **warn**
- Section present but `**Receives:**`, `**Produces:**`, or `**Returns to:**`
  fields are missing or contain placeholder text (e.g., "TBD", `<inputs>`,
  empty values) — **fail**

Severity: **warn** (missing section) / **fail** (placeholder or empty fields)

#### Check 5 — Termination Conditions

Agents without explicit stopping conditions are a documented top cognitive
fault in production agentic systems.

Flag when the `## Workflow` section (or equivalent) has no step that
describes what "done" looks like, what the agent returns to the parent on
completion, or under what conditions the agent should stop.

Severity: **warn**

#### Check 6 — Context Cost Justified

Subagents are full context forks — high overhead compared to skills or
inline execution.

Flag when:
- The described workflow maps cleanly to an existing WOS skill
- No parallelism, permission isolation, or context-window pressure is
  mentioned or implied by the description
- The agent's scope is narrow enough for a single inline tool call

Severity: **warn**

#### Check 7 — Skill Overlap

Flag when the agent's described capability matches an existing skill
in `skills/` and the definition provides no rationale for why a
subagent is preferable (parallelism, tool isolation, or context pressure).

To check: list `skills/*/SKILL.md` names and compare against the agent's
described primary capability.

Severity: **warn**

### 3. Emit Findings

Output one line per issue, in `scripts/lint.py` format:

```
[severity] path/to/file.md — description of issue
```

Group findings by file. Within each file, sort `[fail]` before `[warn]`.
If a file has no issues, output:

```
[ok] path/to/file.md — well-formed
```

### 4. Summarize

After all findings, print:

```
Audited N agent(s): N ok, N warn, N fail
```

If any issues were found, add a one-sentence recommendation, e.g.:

> "3 agents have over-permissioned tool sets — run `/wos:build-subagent`
> to rebuild with least-privilege tool selection."

## Anti-Pattern Guards

- **Silent ok on placeholder handoffs** — `**Receives:** inputs` is not a
  complete handoff. Empty or generic fields are a fail, not a pass.
- **Skipping the context cost check** — a technically valid definition can
  still be the wrong primitive. Always assess whether a skill would suffice.
- **Flagging every broad tool set** — some agents genuinely need many tools.
  Anchor the over-permissioning check to the description, not an absolute
  tool count.

## Handoff

**Receives:** Path to a specific agent definition, or defaults to scanning
`.claude/agents/`
**Produces:** Structured audit findings (file, issue, severity) sorted by
severity; summary with agent count and issue totals
**Chainable to:** build-subagent (to scaffold replacements or new definitions)
