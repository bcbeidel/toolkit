---
name: Audit Dimensions — Subagents
description: The complete check inventory for check-subagent — Tier-1 deterministic check table (seven scripts), Tier-2 judgment dimension specifications (seven dimensions, each citing its source principle), and the Tier-3 description-collision check. Referenced by the check-subagent workflow.
---

# Audit Dimensions

The check-subagent audit runs in three tiers. This document is the
inventory: every deterministic check Tier-1 emits, every judgment
dimension Tier-2 evaluates, and the cross-entity Tier-3 check. Every
dimension cites the source principle it audits from
[subagents-best-practices.md](../../../_shared/references/subagents-best-practices.md).

## Tier-1 — Deterministic Checks

Seven scripts, ~18 atomic checks. Each script emits findings in the
fixed lint format (`SEVERITY  <path> — <check>: <detail>` +
`Recommendation:`). Exit codes: `0` clean / WARN / INFO / HINT-only;
`1` on FAIL; `64` arg error; `69` missing optional dependency
(`gitleaks` is optional and degrades gracefully to a regex fallback).

| Script | Check ID | What | Severity | Source principle |
|---|---|---|---|---|
| `check_secrets.sh` | `secret` | API keys, tokens, private-key headers via regex pattern list (or `gitleaks` when available) | FAIL | No embedded secrets |
| `check_location.sh` | `location-dir` | File is under `.claude/agents/`, `~/.claude/agents/`, or `plugins/<plugin>/agents/` | FAIL | Location and file format |
| `check_location.sh` | `location-ext` | File extension is `.md` | FAIL | Location and file format |
| `check_frontmatter.sh` | `fm-delimiter` | `---`-delimited YAML frontmatter block at file head | FAIL | Frontmatter shape |
| `check_frontmatter.sh` | `fm-name` | `name` key present and non-empty | FAIL | Frontmatter shape |
| `check_frontmatter.sh` | `fm-description` | `description` key present and non-empty | FAIL | Frontmatter shape |
| `check_frontmatter.sh` | `fm-description-length` | `description` ≤1,024 characters | FAIL | Bounded description length |
| `check_frontmatter.sh` | `plugin-noop` | For files under `plugins/<plugin>/agents/`, flag `permissionMode`, `hooks`, or `mcpServers` — silently ignored by Claude Code in plugin scope | WARN | Frontmatter shape (toolkit project-fact) |
| `check_frontmatter.sh` | `memory-expansion` | `memory:` set alongside a `tools:` allowlist that omits Read, Write, or Edit — runtime auto-enables all three regardless | WARN | Tools declared explicitly (toolkit project-fact) |
| `check_naming.sh` | `name-kebab` | `name` matches `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` | WARN | Naming |
| `check_naming.sh` | `name-stem-match` | Filename stem equals `name` | FAIL | Naming |
| `check_naming.sh` | `generic-filename` | Filename is not a generic placeholder (`agent.md`, `helper.md`, `default.md`) | HINT | Naming |
| `check_tools.sh` | `tools-omitted` | `tools` key absent — defaults to full tool grant | WARN | Declare `tools` explicitly; no wildcards |
| `check_tools.sh` | `tools-wildcard` | `tools` contains `*`, `all`, or `all_tools` | FAIL | Declare `tools` explicitly; no wildcards |
| `check_tools.sh` | `agent-listed` | `Agent` listed in `tools` for a subagent-scope definition — filtered at the platform level, has no effect | WARN | Declare `tools` explicitly (toolkit project-fact) |
| `check_tools.sh` | `parallel-write-risk` | `background: true` + effective tools include `Write` or `Edit` + `isolation: worktree` absent | WARN | Scope dangerous tools (toolkit project-fact) |
| `check_size.sh` | `size-soft` | Body character count ≥6,000 (~1,500 tokens) | WARN | Prompt length bounded |
| `check_size.sh` | `size-hard` | Body character count ≥12,000 (~3,000 tokens) | FAIL | Prompt length bounded |
| `check_structure.sh` | `no-headings` | Body has no `##` heading | WARN | Consistent section structure |
| `check_structure.sh` | `scope-absent` | No heading matching `Scope`, `In scope`, or `Out of scope` | INFO | Scope/out-of-scope stated |

**FAIL exclusions from Tier-2.** Any `secret`, `location-dir`,
`location-ext`, `fm-delimiter`, `fm-name`, `fm-description`, or
`tools-wildcard` finding excludes the file from Tier-2 — the routing
contract or the tool-scope contract is unresolvable, so judgment
evaluation is premature. Other FAILs (`fm-description-length`,
`name-stem-match`, `size-hard`) leave a parseable definition that
judgment can still evaluate productively.

**Missing-tool degradation.** `check_secrets.sh` emits an INFO
finding (`tool-missing: gitleaks`) and falls back to inline regex
patterns when `gitleaks` is absent. Exit stays `0` (or `1` if the
regex fallback finds a secret). Coverage is reduced but not zero —
surfacing the INFO is the user's signal to install `gitleaks` for
full coverage.

## Tier-2 — Judgment Dimensions

One LLM call per file. All seven dimensions run every time; a
dimension that doesn't apply returns PASS silently. Findings carry
WARN severity unless a dimension explicitly marks otherwise —
judgment-level drift is coaching, not blocking.

### D1 Scope Discipline

**Source principles:** *Single responsibility.* *Scope and out-of-scope
stated explicitly.*

**Judges:** Does the subagent do one well-defined thing? Is its scope
(what it handles) named, and is its out-of-scope (what it refuses or
escalates) named alongside? A subagent that mixes unrelated workflows
— "lint TypeScript and also generate migrations" — fails this
dimension, as does one that names only what it does without naming
what it refuses.

**Signals of failure:**
- Description or body contains an "and/or" joining distinct
  workflows.
- No Scope / Out-of-scope section (or equivalent) in the body.
- Workflow covers multiple distinct artifacts (produces both a
  report and a migration, for example).

**PASS silently when:** the subagent covers a single workflow and
states its boundaries.

### D2 Description as Router Prompt

**Source principles:** *Description is a router prompt, not human
documentation.*

**Judges:** Is the `description` written as a routing instruction for
the main agent? A well-formed description opens with a verb phrase
naming the capability, states explicit trigger conditions (when to
invoke), names at least one exclusion (when not to invoke), and
mentions what the agent returns. If the subagent should self-invoke
without explicit request, the description includes "use proactively"
or equivalent routing language.

**Signals of failure:**
- Opens with a noun phrase ("Agent that handles…") or a capability
  summary ("Helper for data tasks") rather than a verb-led action.
- No trigger conditions — nothing tells the router *when* to pick
  this agent.
- No exclusion — nothing distinguishes it from adjacent routing
  targets.
- No statement of what the agent returns (format, location,
  artifact).
- Agent is intended for proactive use but no routing language
  signals this.

**PASS silently when:** the description reads as a routing rule the
main agent can classify against.

### D3 Tool Proportionality

**Source principles:** *Least privilege.* *Scope dangerous tools.*

**Judges:** Does the effective tool set match the described workflow?
The assessment anchors to the description — an allowlist of eight
tools is appropriate for a workflow that needs eight tools, and
suspicious only when the workflow implies fewer. `Bash`, `Write`,
and `Edit` are high-risk; when granted, the body should scope them
(enumerated allowed commands for `Bash`, path constraints for
`Write` / `Edit`).

**Signals of failure:**
- `Bash` granted without any body-level mention of command execution,
  shell operations, or running processes.
- `Write` / `Edit` granted to a read-only / review / reporting agent.
- `WebFetch` / `WebSearch` granted for an explicitly internal-only
  workflow.
- Effective tool set substantially wider than the described workflow
  (a narrow single-verb workflow with >6 tools in the allowlist).
- High-risk tool granted with no body-level scoping or path
  constraints.

**PASS silently when:** the effective tool set matches the workflow
and high-risk grants carry body-level scoping.

### D4 Output Contract

**Source principles:** *Output format is explicit.* *One concrete
example when the task is ambiguous.*

**Judges:** Is the output format mandated (JSON schema, named
markdown structure, specific artifact path)? Does a concrete
input/output example appear at the point of maximum ambiguity? Free-
form prose output breaks downstream parsing.

**Signals of failure:**
- Body mentions "report findings" or "return results" without
  naming the format.
- Format is named but the structure is not described (no field list,
  no schema reference, no example).
- Task is ambiguous (multiple reasonable output shapes exist) and no
  example is supplied.
- Example supplied is synthetic (`<placeholder>`, `foo`, `bar`) rather
  than a realistic case.

**PASS silently when:** output format is explicit and any ambiguity
carries a concrete example.

### D5 Voice & Framing

**Source principles:** *Direct voice.*

**Judges:** Are instructions in imperative mood? Is terminology
consistent across the body? The body should not hedge ("try your
best", "if possible", "might want to") or apologize ("sorry",
"unfortunately"); hedging licenses mediocre output and weakens the
instruction surface.

**Signals of failure:**
- Hedging phrases: "try your best", "might want to", "if possible",
  "perhaps", "sorry", "unfortunately".
- Tentative modal verbs where imperative is appropriate ("you
  should", "you may want to", "consider running" in place of "run").
- The same concept referred to by multiple names across the body
  (e.g., "finding" vs. "issue" vs. "violation" used interchangeably).

**PASS silently when:** instructions are imperative and tone is
consistent.

### D6 Failure Behavior

**Source principles:** *Explicit failure behavior.*

**Judges:** Does the body state how the agent behaves on blockers —
bad input, missing access, ambiguous request? Deterministic exits
prevent the agent from improvising workarounds or flailing into
unsafe actions.

**Signals of failure:**
- No Failure / Errors / Exceptions / On-blocker section (or
  equivalent).
- The section exists but describes only the happy path.
- Instructions authorize open-ended recovery ("try other approaches
  until something works").
- No statement of what the agent reports to the parent on failure.

**PASS silently when:** failure paths are named and the agent's
reporting behavior on blockers is stated.

### D7 Injection Surface

**Source principles:** *No interpolation of untrusted input.*

**Judges:** Does the body interpolate user-supplied text into the
prompt without escaping or treating it as data? Raw interpolation is
a prompt-injection surface — the model reads untrusted text as
instruction unless the body explicitly frames it as data.

**Signals of failure:**
- Template placeholders (`{user_input}`, `$USER_MESSAGE`, `<<<
  input >>>`) appearing in instruction position in the body.
- Body instructs the agent to "follow the instructions in the user's
  input" or equivalent.
- No framing language distinguishing user-supplied content from
  instruction content.

**PASS silently when:** user input is not interpolated, or is framed
as data (enclosed in context tags, explicitly named as user content
to inspect, etc.).

## Tier-3 — Description Collision

Pairwise description similarity across every `.md` file in the
audited scope. Token-set Jaccard similarity ≥0.6 is flagged as WARN —
two subagents sharing the same trigger vocabulary produce non-
deterministic routing, because the main agent has no basis to pick
between them.

| Check ID | What | Severity | Source principle |
|---|---|---|---|
| `description-collision` | Pairwise `description` token-set Jaccard ≥0.6 | WARN | Distinct trigger vocabulary across siblings |

Single-file scope skips this tier. Multi-file scope emits one finding
per colliding pair (not per file), with the pair names and similarity
score.

## Severity semantics

| Severity | Meaning | Exit behavior |
|---|---|---|
| FAIL | Spec violation or unrecoverable structural issue; file may exclude from Tier-2 | Contributes to exit 1 |
| WARN | Principle violation; repair recommended | Exit 0 |
| INFO | Informational — missing optional tool, scope section absent, etc. | Exit 0 |
| HINT | Feed-forward context for Tier-2; not a finding requiring repair | Exit 0 |

## How this document stays honest

Every Tier-2 dimension cites its source principle by name. Every
Tier-1 check cites its source principle (with a note when it's a
toolkit project-fact beyond cross-family consensus). When the
principles doc changes, this inventory updates alongside it; dimension
names and source-principle citations are the link. If a dimension ever
drifts from its principle, the check-subagent audit itself will
surface the inconsistency.
