---
name: Primitive Routing Guide
description: Decision framework for choosing the right Claude Code primitive — rules, skills, hooks, subagents, CLAUDE.md, or permissions.deny. Referenced by all build-* skills as a shared routing gate.
---

# Primitive Routing Guide

## The Right Question

When someone wants to enforce a convention, the instinct is to ask "which primitive can express this?" All of them are expressive — most rules can be written as a CLAUDE.md entry, a hook, a skill, or a semantic rule. The question that actually matters is: **what guarantee do you need?**

Some goals need to happen every single time, regardless of what Claude thinks. Others benefit from Claude's judgment — knowing when the convention applies, how it interacts with other context, when an exception is warranted. Building a mandatory enforcement mechanism on the probabilistic tier, or burying a nuanced convention in a deterministic one, produces the same outcome: technically correct, behaviorally wrong.

## The Two Tiers

**Deterministic tier — fires regardless of LLM judgment:**

These primitives don't consult Claude. They run because an event happened, a user typed a command, or a setting says never. Use this tier when "usually" isn't good enough.

- **Hooks** — shell scripts at lifecycle events (before a tool call, after a commit, at session start). Claude never decides whether to run them.
- **User-invoked skills** — fires exactly when the user types `/skill-name`. No ambiguity about whether Claude matched the right trigger.
- **`permissions.deny`** — a static firewall in `settings.json`. No logic, no exceptions, no override path.

**Probabilistic tier — Claude decides whether and when to apply:**

These primitives benefit from judgment. Claude reads context, assesses relevance, adapts. Use this tier when you want Claude's interpretation, not unconditional execution.

- **CLAUDE.md** — always loaded, but Claude weighs each instruction against the situation. Advisory, not mandatory.
- **Model-invoked skills** — Claude matches the task to the skill description. May skip if the match is uncertain.
- **Subagents** — Claude decides when to fork context. Judgment-driven delegation.
- **Rules** — Claude evaluates file content against the criterion. The LLM judgment is the entire mechanism.

## What Each Primitive Was Designed For

**Rules** exist for conventions that are semantically nuanced — the kind where two files could look identical to grep but mean different things to a careful developer. The LLM judgment isn't a limitation; it's the point. Rules are the wrong choice when the check is mechanical (use a linter instead) or when it must fire unconditionally at a lifecycle event (use a hook instead).

**Hooks** exist for invariants. Things that must happen at a specific moment, without exception, regardless of what Claude thinks about the situation. A hook that enforces a preference instead of an invariant spends its authority on false positives — one bypass event normalizes the pattern, and once bypass is cultural, the hook provides no protection.

**Skills** exist for repeatable procedures that benefit from Claude's judgment about when and how to apply them. A skill is a procedure you invoke; CLAUDE.md is context you carry. If you find yourself writing "always follow these conventions" inside a skill body, that content belongs in CLAUDE.md instead. If the procedure must fire at a specific lifecycle event, it belongs in a hook.

**Subagents** exist for work that would pollute the main context — broad searches, large file reads, parallel workstreams with independent outputs. The isolation is the feature. For sequential work where step N+1 needs full step N output, the isolation becomes a liability: you're paying the context fork cost without getting the benefit.

**CLAUDE.md** exists for background knowledge — the architectural context Claude needs to make good decisions across all tasks. It degrades under load: every line you add reduces the compliance probability of every other line equally. Rules that are shell-expressible don't belong here; moving them to hooks removes them from the advisory budget and improves compliance for everything that remains.

**`permissions.deny`** exists for unconditional blocks with no exceptions, ever. If the block is sometimes legitimate, use a hook with conditional logic instead.

## Routing Test

Two questions route most decisions:

1. **Must this fire at a specific lifecycle event, regardless of LLM judgment?** → Hook
2. **Should Claude decide whether this applies to the current situation?** → Skill or CLAUDE.md

If neither resolves it:
- Static file content evaluated for semantic compliance → **Rule**
- Task needs context isolation or different tool permissions → **Subagent**
- Unconditional, no exceptions, no override path → **`permissions.deny`**

## When You've Chosen the Wrong Primitive

Wrong-primitive failures don't announce themselves as configuration errors. They look like behavioral inconsistency — a convention that mostly works, sometimes doesn't.

**CLAUDE.md for enforcement** — Claude follows the rule most of the time, then violates it in long sessions or under context pressure. This isn't a rule quality problem; CLAUDE.md is advisory by design. Convert to a PreToolUse hook and the problem disappears.

**Hooks for advisory guidance** — One false positive per session is enough to generate bypass culture. Once users normalize running with `--no-verify`, the hook provides zero protection. Reserve exit-2 blocks for genuine invariants. Advisory output (exit 1 = warning) is more durable than blocking for preferences.

**Skills for always-on context** — Skill content enters the conversation as a message when invoked and stays in a shared token budget. After auto-compaction, early-invoked skills are candidates for eviction. If behavior changes mid-session, the content belongs in CLAUDE.md, not a skill.

**CLAUDE.md past ~150–200 lines** — Instruction density degrades uniformly. Adding a new rule reduces compliance for every existing rule by roughly the same amount, with no way to prioritize. Shell-expressible rules moved to hooks free up advisory budget for the conventions that genuinely need judgment.

**Subagents for sequential dependent work** — Each step requires a new context fork, round-trip latency accumulates, and the isolation benefit (discarding intermediate work) doesn't apply when the next step needs the full previous output. Sequential work belongs in the main conversation or a skill.

---

**Diagnostic for existing failures:** Paste the failing rule as the first message (outside CLAUDE.md). If Claude follows it there but not in CLAUDE.md — the issue is primitive delivery, change the primitive. If Claude still doesn't follow it — the issue is the rule itself, rewrite it. This isolates whether you have a delivery problem or a quality problem.

## Language Selection — when the answer is "a script"

When the routing test lands on "a script" (glue code, a CLI tool, a hook body), one more decision follows: shell or Python? Both are scripts; they fail in different directions.

**Pick shell when:**
- The task is *glue* — stitching CLI tools (`git`, `curl`, `jq`, `find`, `xargs`) through pipelines
- The task is genuinely one-shot and will not acquire business logic
- The work operates on text streams, not structured records
- The execution environment cannot be relied on to ship Python (bare containers, minimal CI images)

**Pick Python when:**
- The task manipulates structured data — arrays of typed records, nested JSON, schema-validated payloads
- Projected logic exceeds ~100 LOC of business code (not counting help or boilerplate)
- The script needs testable seams — `pytest` against `main()`
- Real error recovery is required — typed exceptions, retry with backoff, context managers
- Cross-platform correctness matters — Windows compatibility, path normalization
- The work needs concurrency, or calls HTTP APIs with JSON and retry semantics
- The argument surface has subcommands or interdependent flags

**Cost axes.** Shell scripts are genuinely painful to unit-test; if the script lives past a quarter, Python's testing story pays back. Pure-POSIX shell runs anywhere; a Python script with third-party deps needs a virtualenv, a PEP 723 runner, or `pipx`. Shell fails silently (unquoted variables, `set -e` surprises, broken pipes ignored); Python fails loudly (`ImportError`, typed exceptions). Pick based on which failure mode your environment catches better.

**Tiebreaker.** When the decision is genuinely balanced — 20–100 LOC of mixed glue and light logic, no strong environment constraint — **pick Python**. Interpretability wins: `subprocess.run([...], check=True)` reads more clearly than `cmd1 | while IFS= read -r line; do ...`, and the next maintainer will thank you.

**Escalation — start as a script, graduate to a package.** Either language: when the script grows a second entry point, acquires shared state across invocations, runs as a long-lived service, or its test coverage exceeds its code, convert to a proper package. Both Scope Gates flag these signals explicitly.

Route: `/build:build-bash-script` + `/build:check-bash-script` for Bash 4.0+; `/build:build-python-script` + `/build:check-python-script` for Python. POSIX `sh` is out of scope for both — when genuine portability to `dash`/BusyBox/Alpine is required, choose a different language.

## Meta-Primitives — patterns that create other primitives

Some primitives are *about* primitives. A skill-pair is the canonical case: a matched `build-<primitive>` scaffolder and `check-<primitive>` auditor that share a single distilled principles doc under `_shared/references/`, plus a scoreable `audit-dimensions.md` and a `repair-playbook.md`. The pair exists so creation and review never drift — both halves read from the same rubric, so the patterns the scaffolder produces are the patterns the auditor enforces. Either half alone is incomplete; `/build:build-skill-pair` refuses to scaffold only one side.

Reach for a skill-pair when a new primitive class carries enough convention to distill into a rubric worth citing — Bash scripts, Python scripts, and future additions (e.g., Terraform modules, Dockerfiles, SQL migrations) fit this mold. Do *not* reach for a pair when the primitive has no convention beyond what already appears in CLAUDE.md or a rule — the distilled rubric would be thin and the pair would dilute the meta-skill's usefulness.

Route: `/build:build-skill-pair <primitive>` to author the pair (six artifacts: principles doc + two SKILLs + audit-dimensions + repair-playbook + routing-doc registration). `/build:check-skill-pair <primitive>` to audit pair-level integrity — missing principles doc, drifted audit/playbook coverage, unregistered pair, divergent principles paths. Full authoring guidance lives in [skill-pair-best-practices.md](skill-pair-best-practices.md).
