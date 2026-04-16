---
name: "Hook Platform Stability Status Q1 2026"
description: "All six hook systems are pre-stable (Experimental, Preview, or beta) as of Q1 2026; rankings and behavior will shift within 1–2 release cycles"
type: context
sources:
  - https://code.claude.com/docs/en/hooks
  - https://cursor.com/changelog/1-7
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://developers.openai.com/codex/hooks
  - https://code.visualstudio.com/docs/copilot/customization/hooks
  - https://docs.cline.bot/customization/hooks
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-blocking-reliability-cross-platform.context.md
---

No platform in the survey has reached a stable, production-grade stability designation for its hook system as of Q1 2026. All six are in varying stages of pre-release labeling, and all are actively adding events, fixing enforcement bugs, and changing schemas.

**Stability designations by platform**

| Platform | Status label | Hook system launched |
|----------|-------------|---------------------|
| Claude Code | No explicit stability label; two CVEs patched Oct 2025 and Jan 2026 | Before Oct 2025 |
| Cursor | Beta; Hooks launched v1.7, September 29, 2025 | September 2025 |
| Windsurf | No explicit stability label; adding events monthly | Before November 2025 |
| Codex CLI | Experimental; Windows support temporarily disabled | 2025 |
| GitHub Copilot VS Code | Preview | 2025 |
| Cline | No explicit stability label; Windows toggle not yet supported | v3.36, 2025 |

**What pre-stable means operationally**

- Schemas change without backward compatibility guarantees (Windsurf explicitly warns of this for transcripts)
- Enforcement bugs exist and are known but unfixed (Cursor cloud agent hooks, Copilot VS Code deny decisions)
- Features are removed, renamed, or split across events (Cline deprecated `shouldContinue`)
- Platform rankings based on event count or capability surface may invert within months

**When to reassess**

Any architecture decision based on hook capability comparisons from this document should be re-evaluated before implementation. Cursor launched hooks in September 2025 and added multiple capabilities within two months. Windsurf added `pre_user_prompt` blocking in December 2025 and `post_setup_worktree` in January 2026. A platform ranked lower today may be ranked higher within one or two major version cycles.

The core constraint documented here is not which platform is best — it is that the entire hook ecosystem is too young to treat any current ranking as stable input to long-term architecture decisions.
