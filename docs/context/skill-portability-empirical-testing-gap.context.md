---
name: "No Empirical Cross-Runtime Test of a WOS Skill Exists"
description: "All WOS skill portability claims derive from vendor documentation or T4 practitioner reports — no independent empirical cross-runtime test of a WOS skill has been published"
type: context
sources:
  - https://gorilla.cs.berkeley.edu/leaderboard.html
  - https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google
  - https://www.allaboutken.com/posts/20260408-mini-guide-claude-copilot-skills/
  - https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
---

# No Empirical Cross-Runtime Test of a WOS Skill Exists

The research corpus contains no independent empirical test of a WOS skill — or any Agent Skills-format skill — running unchanged across multiple runtimes. All portability claims derive from vendor documentation (with inherent COI) or T4 practitioner blog posts. This is a material evidentiary gap that qualifies the confidence level of all cross-runtime portability conclusions.

## What Exists (and Its Limitations)

**Hawkins (T4, April 2026):** Confirmed that a minimal `SKILL.md` with `name`, `description`, and markdown body works on both Claude Code and Copilot CLI. This is a practitioner report, not a systematic test. It covers the happy path (minimal skill, two runtimes) and does not test WOS-idiomatic patterns.

**ElGuerre (T4, March 2026):** Compared the agent/skill/command vocabulary across Claude Code, Codex, Copilot CLI, and Gemini CLI. Identified behavioral differences (subagent inheritance, opt-in requirements). This is documentation analysis, not execution testing.

**Berkeley Function Calling Leaderboard (BFCL V4):** Evaluates function-calling accuracy across models. Does not test SKILL.md-format skill portability. Function-calling performance is a different measurement than skill file format compatibility.

**MindStudio compatibility report:** Addresses API-level tool definition adaptation (described as "minutes of work"). This covers the provider API layer, not skill file format portability. MindStudio has a COI — it built products on the Agent Skills standard and may understate lock-in.

**Vendor documentation (Anthropic, Google, Microsoft, GitHub):** T1 sources for runtime-specific behavior. All have COI on portability claims — each vendor benefits from portraying their platform as compatible with the open standard.

## What Is Missing

An independent test would:
1. Take a WOS skill with representative features (reference files, `context: fork`, `allowed-tools`, dynamic injection)
2. Deploy it unchanged on Claude Code, Copilot CLI, Gemini CLI, and at least one open-source runtime
3. Measure: Does it load? Does description-based dispatch work? Do reference files load? Does fork isolation work? Does dynamic injection work?
4. Document behavioral differences without vendor motivation

No such test was found in the research corpus across 25 searches and 42 sources used.

## Implication for Confidence Levels

All portability claims in the source research document are classified as documentation-derived or practitioner-reported. The finding that "the spec minimum is portable" is HIGH confidence because it derives from a practitioner test and is consistent across all vendor documentation. The finding that "WOS-idiomatic extensions are Claude-locked" is also HIGH confidence, but rests on documentation analysis — not on observing those extensions fail on another runtime.

Confirming the full scope of portability degradation (not just which fields are absent from the spec, but what actually breaks in practice) requires running a real WOS skill across runtimes.

---

**Takeaway:** No published independent empirical test of a WOS skill running across multiple runtimes exists. Portability claims rest on vendor docs (COI) and T4 practitioner reports. Confirming the practical scope of portability degradation requires deploying a representative WOS skill across Claude Code, Copilot CLI, and Gemini CLI and measuring behavioral differences directly.
