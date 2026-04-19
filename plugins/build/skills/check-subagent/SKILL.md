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

If `$ARGUMENTS` is non-empty, treat it as a file path and audit only that
file. Otherwise, scan `.claude/agents/` recursively for `.md` files.

If the directory does not exist or contains no `.md` files:

> "No subagent definitions found at `.claude/agents/`. Nothing to audit."

Exit after reporting.

### 2. Run Eleven Checks

For each definition file, run all eleven checks in order.

**Category key:** **canonical** = enforces a spec-documented requirement.
**best-practice** = recommended by Anthropic best-practices, not binding.
**toolkit-opinion** = house style with no spec backing; flagged only when a
trigger condition elevates the finding. Each check is tagged with its
category so authors can weigh findings appropriately.

#### Check 1 — Tool Over-Permissioning

**Category:** best-practice (anchored to spec's least-privilege guidance but
flagged on judgment, not fixed thresholds).

Does the effective tool set include capabilities the description does not
support? Anchor the assessment to the description — omission of `tools` is
the spec-documented default (inherit all tools), not inherently suspicious.
Flag only when the inherited or listed set exceeds what the described
workflow needs.

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
- `Agent` is listed in `tools` for a definition that runs as a
  subagent (via Agent tool or `@`-mention) — subagents cannot spawn
  other subagents; the Agent tool is filtered out at the platform level;
  listing it has no effect. Exception: `Agent` or `Agent(<type>, ...)` is
  legitimate syntax for definitions intended to run as the *main thread*
  via `claude --agent <name>` (spec documents this path). Flag only when
  the definition's description does not indicate main-thread use
- Only `disallowedTools` is set for a narrowly-scoped agent — the agent
  inherits all tools except the denylisted ones; verify the inherited set
  is not broader than the workflow requires
- An effective tool set substantially wider than the described workflow
  needs. A "narrow scope" here means the description covers a single
  workflow step (one verb, one artifact produced); an allowlist of >6 tools
  for that scope warrants review. For multi-step agents, anchor to the
  workflow steps, not a fixed tool count

Severity: **warn**

#### Check 2 — Tool Under-Permissioning

**Category:** best-practice.

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

**Category:** canonical for `description`-field rules (spec-documented
1024-char cap, routing signal); toolkit-opinion for the `## When to invoke`
body section (house convention to disambiguate ambiguous descriptions).

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
- The `description` is ambiguous or risks over/undertriggering AND the
  body has no `## When to invoke` section with disambiguating examples —
  **Otherwise (description is already a clear routing rule): not flagged.**
  This is a toolkit-opinion check; the body section is recommended, not
  spec-required.
- The section exists but contains no negative example (a request type
  that should NOT route to this agent) when the agent's capability
  overlaps with a sibling skill or agent — a negative case is what
  disambiguates overlapping routing targets.

**Trigger-evaluation fallback:** When routing behavior is uncertain after
the static checks above, generate 8–10 should-trigger queries and 8–10
should-NOT-trigger queries (near-miss cases that test the exclusion
boundary), evaluate each against the subagent's `description`, and report
the hit rate. Pass when both rates exceed 80%; otherwise recommend
description tightening.

Severity: **warn** (description-field failures) / **info**
(trigger-evaluation recommendation).

#### Check 4 — Handoff Contract Completeness

**Category:** toolkit-opinion. The `## Handoff` section is not spec-required;
it's a WOS convention for skill-chain composition and `check-skill-chain`
verification. Context loss at handoffs is the second-most common multi-agent
production failure mode per Anthropic's engineering writeups — the section is
strongly recommended when the agent's output is consumed by another agent,
skill, or workflow step.

**Trigger:** the agent's description or workflow implies the output flows
into another agent/skill/step (chainable, callable, or produces a structured
artifact a downstream consumer reads), OR the agent writes files a parent
workflow will act on.

**When triggered, flag when:**
- No `## Handoff` section is present — **warn**
- Section present but `**Receives:**`, `**Produces:**`, or `**Returns to:**`
  fields are missing or contain placeholder text (e.g., "TBD", `<inputs>`,
  empty values) — **fail**
- Fields use generic category descriptors ("data", "output", "results")
  rather than concrete descriptors ("list of failing test names and their
  error messages") — **warn**. Concrete descriptors prevent context-loss
  failures at handoff; generic ones hide what state is actually conveyed.

**Otherwise (self-contained agent whose output the user reads directly):
not flagged.**

Severity: **warn** / **fail** (as noted above).

#### Check 5 — Termination Conditions

**Category:** best-practice. Spec documents `maxTurns` as a safety net but
does not require termination language in the body. Agents without explicit
stopping conditions are a documented top cognitive fault ("context anxiety",
premature wrap-up, runaway loops) per Anthropic's engineering writeups.

Flag when the `## Workflow` section (or equivalent) has no step that
describes what "done" looks like, what the agent returns to the parent on
completion, or under what conditions the agent should stop, AND `maxTurns`
is not set in the frontmatter. A workflow completion condition and a
`maxTurns` limit serve as complementary guardrails — agents with neither
are runaway risks.

Severity: **warn**

#### Check 6 — Context Cost Justified

**Category:** toolkit-opinion. Not spec-required. Multi-agent workflows use
4–7× more tokens than single-agent sessions (Anthropic *Multi-Agent Research
System*); a subagent that buys no isolation, parallelism, or tool-scope
benefit is a cost multiplier without upside.

Subagents are full context forks — high overhead compared to skills or
inline execution.

Flag when:
- The described workflow maps cleanly to an existing toolkit skill
- No parallelism, permission isolation, or context-window pressure is
  mentioned or implied by the description
- The agent's scope is narrow enough for a single inline tool call

Severity: **warn**

#### Check 7 — Skill Overlap

**Category:** toolkit-opinion. Related to Check 6 but focused on a specific
signal: exact capability duplication with an existing skill.

Flag when the agent's described capability matches an existing skill
in `skills/` and the definition provides no rationale for why a
subagent is preferable (parallelism, tool isolation, or context pressure).

To check: list `skills/*/SKILL.md` names and compare against the agent's
described primary capability.

Severity: **warn**

#### Check 8 — Skills Inheritance Gap

**Category:** canonical (spec: "Subagents don't inherit skills from the
parent conversation").

Parent session skills are NOT inherited by subagents. Skills must be listed
explicitly in the `skills` frontmatter field.

Flag when:
- The description or workflow implies the agent needs project-specific
  procedures or plugin skill behavior, but the `skills` field is absent
  or empty

Severity: **warn**

#### Check 9 — Permission Mode and Parent Propagation

**Category:** canonical (enforces spec-documented plugin restrictions).

Flag when:
- `permissionMode: bypassPermissions` is set — this grants the subagent
  unrestricted access regardless of the user's session settings. Flag
  for explicit justification review.
- **Any of `permissionMode`, `hooks`, or `mcpServers` is set on an agent
  loaded from a plugin** (`agents/` in a plugin directory). Spec: "For
  security reasons, plugin subagents do not support the `hooks`,
  `mcpServers`, or `permissionMode` frontmatter fields. These fields are
  ignored when loading agents from a plugin." Any of the three in a plugin
  definition is a no-op and misleading.
- Parent-precedence mismatch: `permissionMode` is set on the subagent but
  the expected parent context uses `bypassPermissions`, `acceptEdits`, or
  `auto` — all three override the subagent's choice. Informational flag
  only; the static definition can't know the runtime parent.

Severity: **warn** (bypassPermissions) / **warn** (plugin no-op) / **info**
(parent-precedence mismatch).

#### Check 10 — Memory Field Implicit Tool Grant

**Category:** canonical (spec-documented side-effect).

When `memory` is set (`user`, `project`, or `local`), the spec auto-enables
Read, Write, and Edit so the subagent can manage its memory files. This
silently expands a narrow `tools` allowlist.

Flag when:
- `memory` is set AND `tools` is also set AND the `tools` allowlist does
  not include Read, Write, **and** Edit — the runtime will enable all three
  regardless, so the allowlist is misleading about the agent's actual
  capability surface.

Severity: **warn**

#### Check 11 — Parallel Write Conflict Risk

**Category:** best-practice (quotes Anthropic blog; not spec-required).

Flag when:
- `background: true` is set AND the effective tool set includes `Write`
  or `Edit`, AND `isolation: worktree` is absent — background agents with
  write access running concurrently will conflict on shared files. From the
  official blog: "Two subagents editing the same file in parallel is a
  recipe for conflict." `isolation: worktree` gives each subagent a clean
  working copy.

Severity: **warn**

### 3. Emit Findings

Print the summary line at the **top** of the report so reviewers see the
headline before the detail:

```
Audited N agent(s): N fail, N warn, N info
```

Then one line per issue, in `scripts/lint.py` format:

```
[severity] path/to/file.md — description of issue
```

Group findings by file. Within each file, sort by severity (`[fail]` before
`[warn]` before `[info]`), then by category (canonical before best-practice
before toolkit-opinion), then by check number. This ordering surfaces the
spec-binding failures before house-style warnings.

If a file has no issues, output:

```
[ok] path/to/file.md — well-formed
```

### 4. Summarize

Repeat the summary line at the **bottom** of the report (same format as the
top). If any issues were found, add a one-sentence recommendation, e.g.:

> "3 agents have over-permissioned tool sets — run `/build:build-subagent`
> to rebuild with least-privilege tool selection."

### 5. Opt-In Repair Loop

After presenting findings, ask:

> "Apply fixes? Enter y (all), n (skip), or comma-separated numbers."

For each selected finding:

1. Read the relevant section of the agent definition
2. Propose a minimal specific edit — fix the finding without restructuring
   surrounding content
3. Show the diff
4. Write the change only on user confirmation
5. Re-run the relevant check (and any adjacent checks whose inputs the edit
   touched) to verify the fix before moving to the next selection

Canonical-category findings should be applied first; toolkit-opinion findings
are user-judgment calls and may be skipped without regret.

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

## Key Instructions

- Won't auto-fix findings — audit produces a report; fixes require explicit user action or invocation of `build-subagent`
- Won't flag broad tool sets without anchoring the assessment to the agent's stated description — over-permissioning is relative to purpose, not an absolute count
- Won't pass generic or placeholder handoff fields — placeholder text (`<inputs>`, "TBD", empty values) fails Check 4; generic category descriptors ("data", "output", "results") warn on Check 4; concrete descriptors ("list of failing test names with stack traces") pass

## Handoff

**Receives:** Path to a specific agent definition, or defaults to scanning
`.claude/agents/`
**Produces:** Structured audit findings (file, issue, severity) sorted by
severity; summary with agent count and issue totals
**Chainable to:** build-subagent (to scaffold replacements or new definitions)
