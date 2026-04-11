---
name: "Skill Chain HITL Patterns and CLI Translation Gap"
description: "Five convergent HITL patterns across all platforms: propose-before-commit, structured evidence packs, audit trail, timeout with explicit fallback, binary approve/reject as primary; all surveyed evidence is GUI-native and every pattern requires translation to text."
type: context
sources:
  - https://zapier.com/blog/human-in-the-loop-guide/
  - https://blog.n8n.io/human-in-the-loop-automation/
  - https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
  - https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-hand-off
  - https://orkes.io/blog/human-in-the-loop/
  - https://clig.dev/
related:
  - docs/research/2026-04-10-skill-chaining-human-usability.research.md
  - docs/context/skill-chain-handoff-signaling-and-evidence-packs.context.md
  - docs/context/skill-chain-human-control-and-interruption-design.context.md
  - docs/context/skill-chain-recovery-and-state-checkpointing.context.md
---

# Skill Chain HITL Patterns and CLI Translation Gap

**Five stable HITL patterns emerge across all surveyed platforms (HIGH confidence on the patterns; LOWER confidence that any specific implementation is a model of good UX).** The critical gap for wos: the entire evidence base is GUI-native. Every pattern requires translation to a conversational text interface — a translation the existing literature does not provide.

## The Five Convergent Patterns

**1. Propose before commit** — every platform separates action description from action execution. The human sees what will happen before it does. No platform surveyed (Zapier, n8n, Copilot Studio, Orkes, ChatGPT agent mode) executes consequential actions without first presenting a proposal.

**2. Structured evidence packs over raw output** — approval surfaces a context-rich, concise decision packet, not a raw data dump. Copilot Studio passes full conversation history and structured context variables. Zapier surfaces structured context for the approval decision. StackAI's formulation: action summary + reasoning + source data + policy flags + preconditions + rollback plan. Concise by default, expandable on request.

**3. Audit trail for every gate** — all decisions, timestamps, and decision-makers are logged. Zapier: every approval logged in the Zap's change history and account audit log, documenting "who reviewed what and when." This is both a compliance pattern and a debugging pattern.

**4. Timeout with explicit fallback** — no gate stalls indefinitely. Standard options: auto-escalate to backup owner, shelve for later review, or default to the safest outcome. Zapier, n8n, and Orkes all implement configurable timeout behavior. A gate that stalls and then auto-executes after context has changed is worse than no gate.

**5. Binary approve/reject as primary; data collection as secondary** — the simplest decision is the default. Zapier documents two action types: "Request Approval" (binary) and "Collect Data" (gather supplementary context). Binary is the primary path; structured data collection is an extension.

## The CLI/Conversational Interface Gap

The entire evidence base draws from GUI-native implementations: wizard UIs, visual progress panels, Outlook approval forms, Slack notification cards, n8n visual workflow canvas. wos operates through a conversational text interface — Claude Code's chat thread.

None of the wizard pattern literature, PatternFly design guidelines, or HITL approval form patterns have been tested in a pure-text, terminal-adjacent environment. The transfer is assumed by the literature, not evidenced.

**The closest applicable reference is CLIG (Command Line Interface Guidelines, clig.dev)** — a practical reference for CLI UX patterns that is entirely absent from the broader HITL literature. For wos, every GUI pattern requires translation:

| GUI pattern | Required text translation |
|-------------|--------------------------|
| Visual progress bar | Status line: "Research (3/8 sources indexed)..." |
| Approval form with fields | Structured text evidence pack |
| Step indicator sidebar | Named stage summary before each gate |
| "Approve" button | Explicit user response: "proceed" / "stop" / "adjust" |
| Audit log UI | Logged transition record in plan file |

## Implementation Guidance

These five patterns are worth adopting as design targets. The specific implementations from Copilot Studio and ChatGPT agent mode have documented production usability problems — treat them as examples of patterns being attempted, not as validated successes. n8n's explicit audit trail and Zapier's timeout configuration are the more mature reference implementations.

**Bottom line:** The five patterns are convergent and robust across platforms. The GUI-to-text translation is uncharted territory — CLIG is the right starting reference, but original design work is required. Do not assume that what works in a visual workflow tool transfers directly to a conversational CLI context.
