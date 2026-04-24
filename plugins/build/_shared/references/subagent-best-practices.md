---
name: Subagents Best Practices
description: Authoring guide for Claude Code custom subagent definitions — what makes a `.claude/agents/<name>.md` file load-bearing, how to shape its frontmatter and prompt body, the positive patterns that work, and the safety and maintenance posture a durable subagent library needs. Referenced by build-subagent and check-subagent.
---

# Subagents Best Practices

## What a Good Subagent Does

A subagent is a single-responsibility worker the routing agent can delegate to with confidence. It carries a routing contract (its `description`), a bounded tool set, and a prompt body that tells a fresh context how to do one job and finish. A good subagent is easy to invoke correctly, hard to invoke by accident, produces machine-parsable output, and fails clearly when blocked.

## Anatomy

```markdown
---
name: typescript-linter
description: Lints staged TypeScript files, reports findings as JSON. Use after editing `.ts` or `.tsx` files when the user wants to check lint status before committing.
tools:
  - Read
  - Glob
  - Grep
---

# TypeScript Linter

You are a TypeScript lint reviewer. Your single job is to surface lint
failures in staged files and return them as a parsable report.

## Scope

In scope: `.ts` / `.tsx` files currently staged.
Out of scope: formatting, type errors, unstaged files.

## Process

1. List staged TypeScript files.
2. Read each file and surface lint violations.
3. Return findings as JSON: `[{file, line, rule, message}]`.
4. If no findings, return `[]`. Stop.

## Failure behavior

If a file cannot be read, emit `{file, error: "<reason>"}` and continue.
Do not attempt workarounds.
```

## Authoring Principles

**Location and file format.** Subagents live under `.claude/agents/` (project) or `~/.claude/agents/` (user), with a `.md` extension. Claude Code only discovers definitions in those directories; files elsewhere are invisible.

**Frontmatter shape.** Begin each file with a YAML frontmatter block delimited by `---`. Frontmatter is where machine-readable metadata lives; the prompt body goes in the markdown that follows. Two keys are mandatory: `name` (the agent's identifier) and `description` (the routing contract). Everything else is optional.

**Naming.** The `name` is kebab-case and matches the filename stem. Filenames describe the primary role (`typescript-linter.md`, not `agent.md` or `helper.md`). The filename is the first signal of purpose; a stable stem-matching identifier prevents confusion between what the file is called and what the agent is called.

**Single responsibility.** Each subagent does one thing. A subagent that covers two unrelated workflows has ambiguous routing — the router can't decide when to pick it, and the prompt body has to juggle modes. Split into two subagents whenever the alternative is an "and/or" in the description.

**Description is a router prompt, not human documentation.** The main agent reads the `description` to decide whether to delegate. Write it as routing instructions: start with a verb phrase naming the capability, state trigger conditions ("use after editing Python files…", "when the user asks to…"), and name at least one exclusion ("not for …"). A description that reads as a capability summary produces unreliable delegation.

**Bounded description length.** Descriptions are consumed by the router in-context; the router has a finite attention budget and a hard character ceiling. Short, specific descriptions route more reliably than long, vague ones.

**Distinct trigger vocabulary.** Sibling subagents should not share the same trigger phrases. Overlapping descriptions produce coin-flip routing — the router has no way to pick between two agents that claim the same surface. Scan the directory when authoring a new agent and adjust vocabulary until each agent owns a distinct slice.

**Declare `tools` explicitly; no wildcards.** The `tools` field is the primary safety mechanism. Declare it as an explicit list. Omitting it grants the full tool set by default; wildcards (`*`, `all`) are the same failure in a different wrapper. Either defeats least privilege before the subagent runs.

**Least privilege.** Grant the tools the workflow genuinely uses, and nothing else. A reviewing agent needs `Read`, `Grep`, `Glob` — not `Write` or `Edit`. A reporting agent needs no shell. Narrow tool access limits blast radius on misinterpretation or prompt injection.

**Scope dangerous tools.** `Bash`, `Write`, and `Edit` carry the most risk. When `Bash` is granted, enumerate the allowed commands in the prompt body rather than relying on the tool grant alone. When `Write` or `Edit` is granted, declare path constraints so the agent modifies only the intended slice of the tree.

**Prompt length is bounded.** The system prompt competes for the subagent's own context budget. A bounded prompt stays focused, runs faster, costs less, and leaves more room for the work itself. Long prompts dilute attention and often hurt accuracy rather than help it.

**Output format is explicit.** Downstream callers parse the response. Mandate a specific, machine-parsable format (JSON, structured markdown, a named schema). Conversational prose breaks automation; unstructured output forces every consumer to write its own parser.

**Direct voice.** Instructions are imperative and consistent in tone. "Run the tests" beats "you should probably run the tests." Hedging ("try your best", "if possible") and apologies license mediocre output. Terminology is consistent across the prompt — the same concept keeps the same name.

**One concrete example when the task is ambiguous.** Few-shot examples outperform abstract instructions when the task surface is genuinely unclear. They cost tokens, so use them sparingly — once, at the point of maximum ambiguity, rather than as decoration.

**Scope and out-of-scope stated explicitly.** A dedicated section (or equivalent) names what the agent handles and what it refuses. Out-of-scope is as load-bearing as in-scope: it tells the agent when to stop rather than improvise.

**Consistent section structure.** Use markdown headings within the prompt body, and keep the set of headings consistent across the library. Pattern recognition shortens review time — reviewers find the same information in the same place across agents.

## Patterns That Work

- **Router-facing descriptions over capability summaries.** The audience is the main agent's routing decision, not a human reader.
- **Explicit allowlists over implicit inheritance.** List the tools the subagent needs; don't leave the grant implicit.
- **Bounded prompts over exhaustive prompts.** A prompt that fits in the focus window beats a prompt that covers every edge case.
- **Mandated output schema over free-form prose.** Parsable output beats parseable output.
- **Imperative voice over suggestive voice.** Name the action; don't hedge.
- **Single clear scope over mixed scopes.** Two subagents beat one that does both.
- **Explicit failure handling over silent flailing.** State what the agent does on blocker; don't let it invent workarounds.

## Safety

Subagent definitions commit to version control and live alongside production code. The safety posture follows from that.

- **No embedded secrets.** API keys, tokens, credentials, and private-key headers never belong in `.claude/agents/` files. Version-controlled secrets are hard to purge once leaked.
- **No interpolation of untrusted input.** Raw user input concatenated into a prompt is a prompt-injection surface. Treat external text as data, not as instructions.
- **Explicit failure behavior.** State how the agent reports blockers — bad input, missing access, ambiguous request. Deterministic exits prevent loops, hallucinated workarounds, and unsafe flailing.

## Review and Decay

Subagents are infrastructure. When their scope or tool set changes in a way consumers depend on, bump a version and document the change in a changelog block (in the file or a sibling `CHANGELOG.md`). Mark deprecated subagents rather than deleting them silently — downstream consumers need to know where to go next. Revisit a subagent when its description stops matching the work it actually does; descriptions drift faster than tool grants.

---

A good subagent reads like a contract: the description tells the router when to pick it, the tool set says what it's allowed to touch, the prompt says what it does and when it stops. When any of those pieces is vague, the agent either fails to get invoked or gets invoked for work it can't finish. The principles above are the ones the panel agreed on across families; when a subagent violates them, it usually violates several at once.
