---
name: "Skill Format Portability Floor vs. WOS Extensions"
description: "The Agent Skills spec minimum (name + description + markdown body) is portable across Claude Code and Copilot CLI; WOS-idiomatic patterns exceed that floor and are Claude Code-specific"
type: context
sources:
  - https://www.allaboutken.com/posts/20260408-mini-guide-claude-copilot-skills/
  - https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://www.mindstudio.ai/blog/agent-skills-open-standard-claude-openai-google
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/agent-skills-governance-gap.context.md
  - docs/context/skill-portability-empirical-testing-gap.context.md
---

# Skill Format Portability Floor vs. WOS Extensions

There is a genuine portability floor in the Agent Skills standard: `name` + `description` frontmatter + a markdown instruction body. This minimum has been empirically confirmed to work across Claude Code and Copilot CLI. WOS-idiomatic patterns go beyond this floor, and everything above it is Claude Code-specific.

## The Confirmed Portable Floor

Ken Hawkins (April 2026) confirmed that a single minimal `SKILL.md` with `name`, `description`, and a markdown body runs on both Claude Code and GitHub Copilot CLI without modification. The Agent Skills standard published by Anthropic in December 2025 defines this minimum and has been adopted by multiple tools including Copilot CLI, Gemini CLI, Cursor, and Codex (exact adopter count not confirmed from directly fetched sources; named tools are verified).

The spec minimum is sufficient for: basic skill selection via description-driven dispatch, delivery of instruction text to the model, and slash command invocation.

## Where the Portability Ends

Known cross-runtime behavioral differences even at the spec minimum:

- **Copilot CLI:** Subagents cannot inherit repo-level skills. A WOS skill using subagent delegation will not port this behavior.
- **Codex:** Child agent access to skills requires explicit opt-in (`child_agents_md = true`). Subagent dispatch works differently.
- **All non-Claude runtimes:** L2/L3 loading (reference files, dynamic injection) does not occur. Skill content must fit within the initial system prompt.
- **Claude Code validation:** Adding a `skills` field to `plugin.json` — a test of extension syntax — causes a Claude Code validation error, illustrating that the boundary is strict even for well-intentioned extensions.

## WOS Patterns Above the Floor

WOS-idiomatic skill authoring uses:
- `context: fork` — subagent isolation
- `allowed-tools` — pre-approved tool permissions
- `argument-hint` — argument intake hint text
- `model` / `effort` — per-skill model configuration
- `!<command>` — dynamic context injection from shell commands
- `references/` directory — L3 resource loading
- Multi-file skill structures (SKILL.md + scripts/) — L2/L3 loading dependency

None of these elements are in the Agent Skills spec minimum. All are Claude Code extensions. WOS validates them as correct practice without flagging them as Claude-locked.

## The Portability Tradeoff

Writing a portable WOS skill means authoring to the spec minimum: a single `SKILL.md` with `name`, `description`, and a flat markdown instruction body that fits within the initial context window. This forfeits:
- Dynamic context injection (no `!<command>`)
- Fork isolation (no `context: fork`)
- Pre-approved tool scoping (no `allowed-tools`)
- Progressive reference loading (no `references/` directory)
- Per-skill model configuration

These are exactly the features that make WOS skills structurally powerful. A skill authored for portability is a content-level skill (text instructions only) with none of the WOS execution architecture.

There is no middle ground: the features WOS adds value around are the same features that create runtime lock-in.

---

**Takeaway:** The Agent Skills spec minimum (`name` + `description` + markdown body) is confirmed portable across Claude Code and Copilot CLI. Every WOS-idiomatic extension above that floor — `context:fork`, `allowed-tools`, L2/L3 loading, dynamic injection — is Claude Code-specific. Writing for portability requires forgoing WOS's execution architecture.
