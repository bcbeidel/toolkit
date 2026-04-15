---
name: check-subagent
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

# Check Subagent

Inspect Claude Code custom subagent definitions for structural quality,
tool set hygiene, description clarity, and handoff contract completeness.
Produces structured findings in the same format as `scripts/lint.py`.

**Announce at start:** "I'm using the check-subagent skill to inspect these
agent definitions."

## Workflow

### 1. Discover

If a file path argument was provided, audit only that file.

Otherwise, scan `.claude/agents/` recursively for `.md` files.

If the directory does not exist or contains no `.md` files:

> "No subagent definitions found at `.claude/agents/`. Nothing to audit."

Exit after reporting.

### 2. Run Ten Checks

For each definition file, run all ten checks in order.

#### Check 1 — Tool Over-Permissioning

Does the effective tool set include capabilities the description does not
support?

**Determining the effective tool set:**
- If `tools` is set: effective set = listed tools only
- If only `disallowedTools` is set: effective set = all tools minus the
  denylist (potentially broad — check against workflow scope)
- If both are set: `disallowedTools` applied first, then `tools` resolves
  against the remainder
- If neither is set: effective set = all tools (flag unless workflow
  genuinely requires unrestricted access)

Flag when:
- `Bash` is in the effective set but the description has no mention of
  command execution, shell operations, or running processes
- `Write` or `Edit` are in the effective set but the description only
  involves reading or reporting
- `WebFetch` or `WebSearch` are in the effective set but the agent is
  described as internal-only
- `Agent` is listed in `tools` — subagents cannot spawn other subagents;
  the Agent tool is filtered out at the platform level; listing it has
  no effect and is misleading
- Only `disallowedTools` is set for a narrowly-scoped agent — the agent
  inherits all tools except the denylisted ones; verify the inherited set
  is not broader than the workflow requires
- More than 6 tools in the effective set for a narrowly-scoped agent
  (description covers a single workflow step)

Severity: **warn**

#### Check 2 — Tool Under-Permissioning

Does the description imply capabilities not covered by the effective tool
set? Apply the same effective-set logic as Check 1 — a tool removed via
`disallowedTools` is absent even if not explicitly missing from `tools`.

Flag when:
- Description says "writes", "creates", or "generates files" but `Write`
  is absent from the effective set (not listed in `tools`, or listed in
  `disallowedTools`)
- Description says "reads" or "analyzes" files but `Read` is absent from
  the effective set
- Description mentions "runs" or "executes" but `Bash` is absent from
  the effective set
- Description mentions "searches the web" or "fetches" external content
  but `WebFetch`/`WebSearch` are absent from the effective set

Severity: **warn**

#### Check 3 — Description Quality and Invocation Guidance

A well-formed definition has two routing artifacts: a `description`
frontmatter field that reads as a routing rule, and a `## When to invoke`
body section with concrete examples including at least one negative case.

**On the `description` field — flag when:**
- Is a single short phrase with no invocation conditions ("handles data
  tasks", "processes files")
- Contains no exclusion or "when not to use" boundary
- Does not mention what the agent returns or produces
- Could apply equally well to a skill (no parallelism, isolation, or
  permission benefit stated)
- Reads as a capability list rather than a routing rule — no specific
  trigger phrases, no problem patterns named
- Is intended for proactive use but contains no "use proactively" signal
  or equivalent routing language (auto-delegation by description matching
  is unreliable; without explicit routing language, the agent will rarely
  be invoked automatically)
- Exceeds 1,024 characters — descriptions over this limit are silently
  truncated without warning

**On the `## When to invoke` body section — flag when:**
- The section is absent entirely — this section is required; it should
  contain at least one positive trigger example and one negative example
- The section exists but contains no negative example (a request type
  that should NOT route to this agent and should go to a skill instead)

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
completion, or under what conditions the agent should stop, AND `maxTurns`
is not set in the frontmatter. A workflow completion condition and a
`maxTurns` limit serve as complementary guardrails — agents with neither
are runaway risks.

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

#### Check 8 — Skills Inheritance Gap

Parent session skills are NOT inherited by subagents. Skills must be listed
explicitly in the `skills` frontmatter field.

Flag when:
- The description or workflow implies the agent needs project-specific
  procedures or plugin skill behavior, but the `skills` field is absent
  or empty

Severity: **warn**

#### Check 9 — Permission Mode and Parent Propagation

Flag when:
- `permissionMode: bypassPermissions` is set — this grants the subagent
  unrestricted access regardless of the user's session settings. Flag
  for explicit justification review.
- `permissionMode` is set to any value but the agent is loaded from a
  plugin (`agents/` in a plugin directory) — plugin subagents have
  `permissionMode` silently ignored; the field is a no-op and misleading.

Severity: **warn** (bypassPermissions) / **warn** (plugin no-op)

#### Check 10 — Parallel Write Conflict Risk

Flag when:
- `background: true` is set AND the effective tool set includes `Write`
  or `Edit`, AND `isolation: worktree` is absent — background agents with
  write access running concurrently will conflict on shared files. From the
  official blog: "Two subagents editing the same file in parallel is a
  recipe for conflict." `isolation: worktree` gives each subagent a clean
  working copy.

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
- **Missing the `Agent` tool trap** — `Agent` in a subagent's tools list
  is always a warn; it cannot work. Do not skip this even if the rest of
  the tool set looks reasonable.
- **Skipping Check 8 for short definitions** — a one-page agent definition
  with no `skills` field is not automatically clean; if the description
  implies project context, the omission is a gap regardless of file length.

## Handoff

**Receives:** Path to a specific agent definition, or defaults to scanning
`.claude/agents/`
**Produces:** Structured audit findings (file, issue, severity) sorted by
severity; summary with agent count and issue totals
**Chainable to:** build-subagent (to scaffold replacements or new definitions)
