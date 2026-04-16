---
name: "Hook Blocking Reliability Across Platforms"
description: "Blocking semantics are documented on all six platforms but reliable enforcement across all tool types is confirmed on none as of Q1 2026; do not rely on hook blocking for security without per-tool-type verification"
type: context
sources:
  - https://code.claude.com/docs/en/hooks
  - https://cursor.com/docs/hooks
  - https://docs.windsurf.com/windsurf/cascade/hooks
  - https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-hooks
  - https://code.visualstudio.com/docs/copilot/customization/hooks
  - https://developers.openai.com/codex/hooks
  - https://docs.cline.bot/customization/hooks
  - https://forum.cursor.com/t/project-level-hooks-and-root-level-hooks-no-longer-work-in-cloud-agents/144932
related:
  - docs/research/2026-04-13-hooks-platform-comparison.research.md
  - docs/context/hooks-deterministic-enforcement-vs-advisory.context.md
  - docs/context/hook-platform-event-coverage-comparison.context.md
  - docs/context/hook-windsurf-model-and-constraints.context.md
  - docs/context/hook-github-copilot-blocking-gaps.context.md
  - docs/context/hook-cline-enforcement-anomalies.context.md
---

Every platform in the survey documents blocking semantics. None has confirmed reliable enforcement across all tool types as of Q1 2026. This is the most operationally important finding from the cross-platform comparison.

**Confirmed blocking failures**

- **Claude Code:** Exit code 2 confirmed non-blocking for Write and Edit tools (referenced GitHub issues #13744, #21988). Only Bash interception reliably verified. Note: these issue numbers require independent verification before use in architecture decisions.
- **Cursor:** `preToolUse` `permission: 'deny'` confirmed non-enforcing for file read operations (Cursor Forum, December 2025). The `ask` decision is schema-accepted but not enforced — when a `beforeShellExecution` hook returns `permission: 'ask'`, the command executes immediately. Note: the specific file-read denial failure references a forum report not independently traceable to the cited source; verify independently.
- **GitHub Copilot VS Code:** Hook deny decisions ignored by SDK (SDK version claim requires independent verification; February–March 2026 reports). Note: the SDK version number is not traceable to a cited source and requires independent verification.
- **Windsurf:** No confirmed blocking failures found. The simplest model (pre/post split, block/allow only, no input transformation) appears to have the fewest edge cases.

**Why Windsurf may be more reliable**

Windsurf's pre-hook model is architecturally simpler: five `pre_` events, one exit code 2 path, no `ask`, no `defer`, no `updatedInput`. Fewer decision branches may mean fewer implementation defects. This is an inference, not a confirmed guarantee.

**What each platform documents**

| Platform | Block mechanism | Input transform | `ask` outcome |
|----------|----------------|-----------------|---------------|
| Claude Code | Exit code 2 (PreToolUse, UserPromptSubmit, Stop, and others) | `updatedInput` | Yes — allow/deny/ask/defer |
| Cursor | Exit code 2 or `permission: 'deny'` | `updated_input` | Documented, not enforced |
| Windsurf | Exit code 2 (pre-hooks only) | None | No |
| Copilot cloud | Non-zero exit (preToolUse) | None | Documented, not processed |
| Copilot VS Code | Exit code 2 | None | `ask` requires confirmation |
| Codex CLI | Exit code 2 or `decision: block` JSON | None | No |
| Cline | `cancel: true` in JSON stdout | None | No |

**Operational guidance**

Do not rely on hook-based blocking for security enforcement without independent verification per tool type on the specific platform version you are targeting. Test each exit code path against each tool type you intend to gate. This is not a theoretical concern — confirmed failures exist on three of the six platforms.

All platforms are pre-stable (Experimental, Preview, or beta). Blocking failures may be fixed in future versions, and new ones may be introduced. The rankings and failure modes documented here are valid for Q1 2026 only.
