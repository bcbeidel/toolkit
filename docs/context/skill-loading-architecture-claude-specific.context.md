---
name: "Skill Loading Architecture Is Claude Code-Specific"
description: "The L1/L2/L3 progressive loading model relies on Claude's VM and Bash environment and cannot be replicated on GPT, Gemini, or open-source runtimes"
type: context
sources:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  - https://code.claude.com/docs/en/skills
  - https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills
  - https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
related:
  - docs/research/2026-04-11-wos-skill-portability-runtime-comparison.research.md
  - docs/context/skill-frontmatter-extensions-claude-code-specific.context.md
  - docs/context/skill-format-portability-floor-vs-wos-extensions.context.md
  - docs/context/skill-progressive-loading-and-routing.context.md
---

# Skill Loading Architecture Is Claude Code-Specific

Claude Code implements a three-tier progressive loading system that is architecturally dependent on Claude's VM environment and Bash tool access. This design has no equivalent on any other model runtime. WOS skills that rely on L2 or L3 loading — which includes all skills using reference files — are Claude Code-specific and will not function the same elsewhere.

## How the Architecture Works

- **Level 1 (L1):** Skill metadata (`name`, `description`) is injected into the system prompt at startup. All runtimes supporting the Agent Skills spec handle this tier.
- **Level 2 (L2):** Full skill instructions are loaded on-demand via Bash filesystem reads when a skill is triggered. Claude autonomously issues `Bash` tool calls to read `SKILL.md` from disk at the moment the skill activates.
- **Level 3 (L3):** Reference files and scripts inside `references/` or `scripts/` subdirectories are accessed via additional Bash commands, only when referenced within the skill body.

The entire L2/L3 mechanism depends on Claude having access to a VM with a real filesystem and the ability to invoke Bash tool calls autonomously. This is a runtime environment capability, not a skill file format feature.

## Why It Cannot Be Replicated

On GPT-4o (Assistants API), Gemini CLI, and open-source runtimes (Ollama, vLLM), there is no mechanism for on-demand file loading via shell commands during execution. These runtimes require skill content to be pre-embedded in the system prompt or tool definitions at session start. The progressive disclosure model — loading only what is needed, when it is needed — is structurally unavailable.

Copilot CLI and Gemini CLI parse `SKILL.md` frontmatter and present metadata to the model, but they do not replicate the dynamic file-read dispatch that defines L2/L3 behavior in Claude Code.

The character budget for L1 metadata is dynamic in Claude Code: it scales at 1% of the context window, with a fallback of 8,000 characters. This dynamic allocation is a Claude Code implementation detail, not a cross-runtime behavior.

## Practical Implications

Any WOS skill that uses `references/` directories, inline `!<command>` injection, or depends on L3 script access is Claude-locked by architecture, not just by frontmatter syntax. Moving such a skill to another runtime requires restructuring: flattening all referenced content into a single system prompt blob, which eliminates the token efficiency and progressive disclosure benefits WOS's architecture was designed to provide.

The portability floor — what works across all Agent Skills adopters — is L1 only: `name`, `description`, and a markdown body that fits within the system prompt. WOS skills are designed around L2/L3 loading and gain their value from it. Portable WOS skills would need to be re-authored from scratch, not merely reformatted.
---

**Takeaway:** The L1/L2/L3 progressive loading model is a Claude Code architectural feature enabled by VM+Bash access. No other runtime replicates it. WOS skills using reference files or dynamic injection are Claude-locked by design, not just by frontmatter choices.
