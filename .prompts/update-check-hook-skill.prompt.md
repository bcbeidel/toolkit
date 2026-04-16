---
name: "Align check-hook skill with full research corpus"
description: "Full alignment pass on skills/check-hook/SKILL.md against the complete hook and shell-script context corpus — read all sources, identify gaps, make targeted additions to the audit rubric"
---

Read every source file listed below before touching anything. The goal is a
full alignment pass: after reading, compare the skill's current audit rubric
against what the context corpus says a high-quality hook looks like, then
make targeted additions for any meaningful gaps. Do not rewrite or restructure
existing content — insert only.

<context>
You are editing a skill file in the toolkit repo — a Claude Code plugin
marketplace at the working directory root. The skill audits existing hook
configurations and scripts. Its output is a findings report that surfaces
misconfigurations, gaps, and quality problems. Every gap in the skill is an
audit finding that gets missed.

Read all files below. Do not skip any. Read them fully, not just the
description lines.

**The skill being edited:**
- `plugins/check/skills/check-hook/SKILL.md`

**Hook domain — how hooks work in Claude Code:**
- `docs/context/hooks-deterministic-enforcement-vs-advisory.context.md`
- `docs/context/hook-event-payload-schemas.context.md`
- `docs/context/hook-matcher-syntax.context.md`
- `docs/context/hook-output-and-decision-control.context.md`
- `docs/context/hook-quality-criteria.context.md`
- `docs/context/hook-testing-and-debugging.context.md`

**Primitive routing — when hooks are the right primitive:**
- `docs/context/claude-code-primitive-routing-and-reliability.context.md`
- `docs/context/claude-code-wrong-primitive-failure-modes.context.md`
- `docs/context/claude-md-to-hook-conversion-signals.context.md`

**Hook script authoring — what a well-written script looks like:**
- `docs/context/hook-script-safety-preamble.context.md`
- `docs/context/hook-script-error-reporting.context.md`
- `docs/context/hook-script-injection-prevention.context.md`
- `docs/context/hook-script-json-payload-handling.context.md`
- `docs/context/hook-script-testing-strategies.context.md`
- `docs/context/hook-script-shellcheck-static-analysis.context.md`
- `docs/context/hook-script-bash-style-conventions.context.md`

**Research backing (skim for additional findings not yet in context files):**
- `docs/research/2026-04-13-hook-vs-primitives.research.md`
- `docs/research/2026-04-13-hook-quality-and-evaluation.research.md`
- `docs/research/2026-04-13-shell-script-best-practices.research.md`
</context>

<task>
After reading all sources:

1. **Identify gaps.** The check-hook skill currently audits configuration
   and structural issues (exit codes, async contradiction, loop guard, matcher
   casing, etc.). The hook-script authoring context files define what a
   well-written hook script looks like internally. Check whether the audit
   rubric covers script-quality issues surfaced by the new context:

   - `set -Eeuo pipefail` preamble presence
   - `|| true` guards on detection commands (grep, diff, test)
   - Injection safety: `eval` on payload-derived values, unquoted variable
     expansions, bare command names susceptible to PATH override
   - jq availability assumption (silent failure if jq not installed)
   - Variable quoting consistency — `"${var}"` form
   - `[[` vs `[` for conditionals
   - Errors going to STDERR vs stdout

   Also check whether the existing checks fully reflect the canonical rubric
   in `hook-quality-criteria.context.md`, including severities.

2. **List gaps before editing.** Output a brief gap list — one line per gap,
   noting which context file it comes from and where in the skill it slots.

3. **Make targeted additions only.** The skill's section order is:
   Input → Primitive Routing → Checks (10) → Report → Handoff.
   New script-quality checks should be added as numbered items within the
   Checks section (extending beyond 10 if needed) or integrated into existing
   checks where they are logically related. Keep check descriptions concise
   and scannable — one paragraph per check maximum.

4. **Prioritize HIGH-confidence findings.** MODERATE-confidence guidance
   should be included with qualification ("Evidence suggests..."). LOW-
   confidence findings should be omitted unless there is no alternative.

   Script-quality checks are inherently lighter-touch than configuration
   checks: the skill is reading scripts, not executing them. Flag issues as
   `warn` unless they are clearly broken (e.g., `eval` on payload fields is a
   `fail`; missing `|| true` guard is a `warn`).
</task>

<constraints>
- Edit only `skills/check-hook/SKILL.md`
- All additions are additive — no existing lines removed or reworded
- Keep additions concise: this file is read by an LLM as skill instructions
- Do not add external URLs
- Do not restructure the existing section order
- Keep check descriptions to one paragraph maximum
</constraints>

<output_format>
1. Output the gap list first.
2. Make all edits.
3. Run:
```
python plugins/wiki/scripts/lint.py plugins/check/skills/check-hook/SKILL.md --root . --no-urls
```
4. Report lint output. Acceptable: 0 fail. Pre-existing warn on `build-skill`
   density can be ignored. If lint shows fail on `check-hook`, fix it.
5. Confirm: "Gap list reviewed. Additions made. Lint: 0 fail."
</output_format>
