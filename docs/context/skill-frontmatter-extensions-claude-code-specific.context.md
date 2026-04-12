---
name: "Claude Code Frontmatter Extensions Are Outside the Agent Skills Spec"
description: "Claude Code proprietary frontmatter fields — context:fork, allowed-tools, model, hooks, and others — are not in the Agent Skills open standard and are silently dropped or rejected by other runtimes"
type: context
sources:
  - https://code.claude.com/docs/en/skills
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://elguerre.com/2026/03/30/ai-agents-vs-skills-commands-in-claude-code-codex-copilot-cli-gemini-cli-stop-mixing-them-up/
  - https://www.allaboutken.com/posts/20260408-mini-guide-claude-copilot-skills/
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/skill-loading-architecture-claude-specific.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
  - docs/context/agent-skills-governance-gap.context.md
---

# Claude Code Frontmatter Extensions Are Outside the Agent Skills Spec

Claude Code extends the Agent Skills standard with proprietary frontmatter fields that have no equivalent in the open spec. These extensions are what give WOS skills their execution power — subagent isolation, model overrides, tool pre-approval — but they make those skills Claude Code-specific. Other runtimes silently ignore them (safe but non-functional) or produce validation errors.

## The Extension Fields

Claude Code adds the following fields beyond the Agent Skills spec minimum:

| Field | Purpose | Portability |
|-------|---------|-------------|
| `context: fork` | Subagent isolation — run skill in separate context | Claude Code only; ignored elsewhere |
| `allowed-tools` | Pre-approved tool permissions for the skill | Claude Code only; experimental in spec |
| `model` / `effort` | Per-skill model and reasoning effort overrides | Claude Code only; no equivalent elsewhere |
| `hooks` | Pre/post execution lifecycle hooks | Claude Code only |
| `disable-model-invocation` | Bypass LLM invocation, run script directly | Claude Code only |
| `user-invocable` | Control whether skill appears in slash command list | Claude Code only |
| `argument-hint` | Hint text for skill argument intake | Claude Code only |
| `!<command>` | Dynamic context injection via shell command | Claude Code only |

The official skills-ref validator (GitHub issue #25380) flags these Claude Code extensions as non-standard. The `allowed-tools` field is marked "Experimental — support may vary between implementations" in the spec, confirming its non-portable status.

## What Happens on Other Runtimes

**Copilot CLI:** Silently ignores unrecognized frontmatter fields. A skill with `context: fork` will parse and load, but the fork isolation behavior does not occur — the skill runs in the main context instead.

**Gemini CLI:** Same silent-ignore behavior for unrecognized fields. `allowed-tools` is non-functional.

**Codex:** Child agent opt-in (`child_agents_md = true`) is required for any subagent behavior; `context: fork` provides none of the subagent dispatch semantics.

A confirmed cross-compatibility test (Hawkins, April 2026) showed that adding a `skills` field to `plugin.json` causes a Claude Code validation error, illustrating the fragility of the boundary — extensions go in both directions.

## WOS Implications

WOS's lint rules validate `context: fork`, `allowed-tools`, and `argument-hint` as correct practice. This is accurate for Claude Code but incorrectly implies these fields are standard. A WOS author following WOS guidance will produce skills that are functional on Claude Code and non-functional (or silently degraded) everywhere else.

Writing a portable WOS skill requires authoring to the spec minimum: `name`, `description`, and a markdown body — forgoing all of WOS's structural execution features. There is no middle ground. The features WOS adds value around (fork isolation, tool scoping, dynamic injection) are the same features that create runtime lock-in.

---

**Takeaway:** Claude Code's proprietary frontmatter fields (`context:fork`, `allowed-tools`, etc.) are not in the Agent Skills spec. WOS validates them as good practice, but they are Claude-locked. Other runtimes silently drop or reject them. Portable skills must forgo these fields entirely.
