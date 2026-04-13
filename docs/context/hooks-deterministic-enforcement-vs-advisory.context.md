---
name: "Hooks: Deterministic Enforcement vs Advisory Guidance"
description: "Hooks enforce deterministic behavior via exit code 2 (non-negotiable); CLAUDE.md is advisory and subject to context dilution; PreToolUse is the highest-leverage event; hooks config is attack surface (CVE-2025-59536)"
type: comparison
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/best-practices
  - https://claude.com/blog/how-to-configure-hooks
  - https://paddo.dev/blog/claude-code-hooks-guardrails/
  - https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
related:
  - docs/context/instruction-file-hierarchy-and-path-scoping.context.md
  - docs/context/instruction-file-fragmentation-and-convergence.context.md
  - docs/context/llm-failure-modes-and-mitigations.context.md
  - docs/context/production-reliability-gap-and-multi-agent-failures.context.md
  - docs/context/hook-event-payload-schemas.context.md
  - docs/context/hook-matcher-syntax.context.md
  - docs/context/hook-output-and-decision-control.context.md
  - docs/context/hook-quality-criteria.context.md
---
CLAUDE.md instructions are advisory. Hooks are deterministic. This distinction is not a nuance — it is the architectural boundary between what Claude is asked to do and what Claude is physically prevented from doing.

**Why advisory instructions fail as enforcement.** Three failure modes documented in production:
1. Context dilution — important rules buried in CLAUDE.md get lost as context fills in long sessions; the model stops attending to them
2. Probabilistic compliance — instructions are weighed against other signals; a sufficiently urgent user request can override a soft instruction
3. LLM interpretation — Claude processes CLAUDE.md as context, not as a rule engine; it exercises judgment about when rules apply

Documented incidents where CLAUDE.md instructions failed: "NEVER edit .env files" → Claude loaded `.env` and replicated credentials to committed files; `rm -rf` with a home path → executed after user intended only a limited directory removal.

**Exit code 2 is non-negotiable.** A `PreToolUse` hook that returns exit code 2 blocks the tool call. No LLM interpretation, no context pressure, no urgent user request overrides this. Exit code 1 is non-blocking (shown in transcript but execution continues). Only exit code 2 blocks.

**PreToolUse is the highest-leverage hook event.** It fires before a tool executes and can return four outcomes: allow, deny, ask, or defer. When multiple PreToolUse hooks conflict, priority order is: deny > defer > ask > allow. It can also modify tool input before execution via `updatedInput`. This is the correct place for security rules, file protection, and command blocking.

**What belongs where:**

| CLAUDE.md (Advisory) | Hooks (Deterministic) |
|---|---|
| Architectural decisions, engineering philosophy | Running linters and formatters |
| Naming conventions, preferences | Blocking dangerous commands |
| Technology stack context | Protecting sensitive files (.env, credentials) |
| Guidance with legitimate edge cases | Pre-commit validation gates |

The operational rule: if a CLAUDE.md rule is one Claude "keeps violating," convert it to a hook. If it can be expressed as a shell one-liner, it belongs in a hook.

**CVE-2025-59536 (Check Point Research, 2026).** `.claude/settings.json` is a repository file. Any collaborator with commit access can inject malicious hooks that execute arbitrary commands on the developer's machine. Anthropic's fix: enhanced warning dialog before trusting a project's hooks. The operational implication: treat hook changes in `.claude/settings.json` with the same code review scrutiny as executable source files, not as configuration metadata.

**Async hooks cannot enforce.** Setting `"async": true` runs the hook in the background without blocking. Async hooks cannot block via exit code 2 — the action has already proceeded. Async is for logging, notifications, and non-critical follow-up. Gating requires synchronous hooks.

**Loop prevention for Stop hooks.** Stop hooks that block without checking `stop_hook_active` will trap Claude in an infinite loop. Mandatory pattern: check `stop_hook_active` in input, exit 0 if already true.
