---
name: "Align build-hook skill with full research corpus"
description: "Full alignment pass on skills/build-hook/SKILL.md against the complete hook and shell-script context corpus — read all sources, identify gaps, make targeted additions"
---

Read every source file listed below before touching anything. The goal is a
full alignment pass: after reading, compare the skill's current guidance
against what the context corpus says, then make targeted additions for any
meaningful gaps. Do not rewrite or restructure existing content — insert only.

<context>
You are editing a skill file in the toolkit repo — a Claude Code plugin
marketplace at the working directory root. The skill generates hook scripts
and settings.json entries. Its output is what an LLM will produce when a
user asks to build a hook. Every gap in the skill is a gap in the generated
output.

Read all files below. Do not skip any. Read them fully, not just the
description lines.

**The skill being edited:**
- `plugins/build/skills/build-hook/SKILL.md`

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

**Hook script authoring — how to write the bash scripts themselves:**
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

1. **Identify gaps.** For each piece of actionable guidance in the context
   corpus, check whether the skill already covers it. A gap is guidance that
   is absent or materially weaker in the skill than in the context files.

2. **List gaps before editing.** Output a brief gap list — one line per gap,
   noting which context file it comes from and which section of the skill it
   should slot into. This makes the edit plan visible.

3. **Make targeted additions only.** Insert new content into the appropriate
   sections. Do not rewrite, reorder, or remove existing content. Every
   addition must fit the existing section structure. The sections are:
   Route → Elicit → Draft → Safety Check → Stop Hook Guard → Security Note →
   Known Limitations → Rule Overlap → Review Gate → Save → Test → Handoff.

4. **Prioritize HIGH-confidence findings.** MODERATE-confidence guidance from
   the shell-script context files should be included with appropriate
   qualification (e.g., "Evidence suggests..."). LOW-confidence findings
   should be omitted unless there is no alternative guidance.

Focus areas likely to have remaining gaps:
- **Draft:** Does the script template reflect all safety-preamble requirements
  (`-E` flag, `|| true` guards for detection commands, ERR trap pattern)?
- **Draft:** Is the JSON payload extraction guidance complete (jq --arg, field
  quoting, jq availability fallback)?
- **Safety Check:** Are injection prevention rules present (no eval, quote
  all vars, absolute paths)?
- **Test:** Is the testing section present and does it cover stdin simulation
  and ShellCheck?
- **Style:** Are `[[` over `[`, STDERR for errors, and function naming
  conventions mentioned somewhere actionable?
</task>

<constraints>
- Edit only `skills/build-hook/SKILL.md`
- All additions are additive — no existing lines removed or reworded
- Keep additions concise: this file is read by an LLM as skill instructions
- Do not add external URLs
- Do not restructure the existing section order
</constraints>

<output_format>
1. Output the gap list first.
2. Make all edits.
3. Run:
```
python plugins/wiki/scripts/lint.py plugins/build/skills/build-hook/SKILL.md --root . --no-urls
```
4. Report lint output. Acceptable: 0 fail. Pre-existing warn on `build-skill`
   density can be ignored. If lint shows fail on `build-hook`, fix it.
5. Confirm: "Gap list reviewed. Additions made. Lint: 0 fail."
</output_format>
