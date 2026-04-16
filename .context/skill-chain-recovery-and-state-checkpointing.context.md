---
name: "Skill Chain Recovery and State Checkpointing"
description: "Checkpointing is necessary but not sufficient — LLM non-determinism means replay restores outputs not the reasoning chain; irreversible side effects require compensation not rollback; language-based re-entry is the right model for conversational interfaces."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://developers.cloudflare.com/agents/concepts/human-in-the-loop/
  - https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents
  - https://medium.com/@mayankbohra.dev/the-agentic-ops-headache-when-rollback-means-complex-compensation-adcafd9f6754
  - https://blog.n8n.io/human-in-the-loop-automation/
  - https://www.aiuxdesign.guide/patterns/mixed-initiative-control
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/research/2026-04-10-skill-chaining-human-usability.research.md
  - docs/context/skill-chain-human-control-and-interruption-design.context.md
  - docs/context/skill-handoff-contracts-and-state-design.context.md
---
# Skill Chain Recovery and State Checkpointing

**Checkpointing is necessary but not sufficient for human re-entry into a failed chain (HIGH confidence on "necessary"; MODERATE confidence on sufficiency).** LLMs are non-deterministic. Replay-based durability (Temporal's model, database-style rollback) restores intermediate outputs but cannot reproduce the reasoning that produced them — re-entry is an approximation, not a restoration.

## Why Full Rollback Is Not Achievable

Database transaction semantics do not apply to LLM-based skill chains. Three distinct problems:

1. **Non-determinism**: If a skill is re-executed from a checkpoint, it produces a different response. The output may be structurally equivalent but semantically different. The reasoning chain is not preserved.

2. **Irreversible side effects**: File writes, external API calls, emails sent, database records created — these cannot be rolled back through state restoration. They require compensation patterns: redo (re-execute with corrected parameters), overwrite (replace the output with a corrected version), or flag (mark as needing manual review).

3. **Partial execution**: A skill that partially executed before failure may have produced outputs that cannot be cleanly undone. Compensation, not rollback, is the correct framing.

The documented "Agentic Ops Headache": "You can't treat AI agent context like database transactions that simply roll back to a clean state."

## What Checkpointing Provides

Checkpointing enables re-entry at the last successful stage, not reconstruction of the reasoning chain. This is still highly valuable — it prevents full chain restarts when a late-stage skill fails.

Cloudflare's HITL pattern: checkpoint requires "persistent storage of original requests, intermediate decisions, and partial progress." Each skill's output must be persisted before the next skill runs. If the chain fails, the human re-enters at the last persisted output — not from scratch.

**Distinguish reversible from irreversible before execution**: skills should signal whether their action can be undone. The human at the approval gate needs to know if "reject" means "this didn't happen" or "this already happened and we need to compensate."

## Language-Based Re-Entry

For a conversational interface, the right re-entry model is language-based, not UI-based. Mixed-initiative control pattern: "I've adjusted this section. Continue from here." The human names where to resume; the chain picks up from that named point.

This is preferable to UI checkboxes or form-based recovery for wos's text-based interface. The agent receives a natural language instruction naming the re-entry point, locates the corresponding checkpoint, and resumes from persisted state.

## Log Human Recovery Decisions as Data

n8n's HITL pattern: "Log every human decision — timestamps, verdicts, override reasons, outcome data. These records reveal patterns enabling progressive automation — reducing unnecessary approvals as the system proves reliable." Recovery decisions are not just events; they are the signal for future automation calibration.

## Practical Implications for wos

For wos's interactive chains (human at every gate, short 4–5 skill sequences): the plan file with task checkboxes provides reasonable chain-level checkpointing. The gap is at the sub-skill level. Full rollback should not be promised to users — communicate honestly that recovery means compensation, not restoration.

**Bottom line:** Checkpoint every stage output before invoking the next skill. Surface the checkpoint explicitly at each gate so the human knows they can re-enter there. Design re-entry as a language interaction. Never represent checkpointing as full rollback — communicate that irreversible side effects require compensation, not restoration.
