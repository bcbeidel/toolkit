---
name: "Skill Chain Human Control and Interruption Design"
description: "HCI principles translate as motivating design goals not operational specs; never block the human; interrupt at skill boundaries not mid-skill; abort is insufficient — redirect without restart is required; wos sits at high-safety/low-autonomy end of the autonomy dial."
type: context
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/wizards/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11775001/
  - https://www.aiuxdesign.guide/patterns/mixed-initiative-control
  - https://www.spurnow.com/en/blogs/how-to-use-chatgpt-agent-mode
  - https://zapier.com/blog/human-in-the-loop-guide/
  - https://blog.n8n.io/human-in-the-loop-automation/
related:
  - docs/research/2026-04-10-skill-chaining-human-usability.research.md
  - docs/context/skill-chain-handoff-signaling-and-evidence-packs.context.md
  - docs/context/skill-chain-recovery-and-state-checkpointing.context.md
  - docs/context/skill-chain-hitl-patterns-and-cli-translation-gap.context.md
  - docs/context/hitl-oversight-as-tuned-policy-and-reversibility-gate.context.md
---

# Skill Chain Human Control and Interruption Design

**Classic HCI principles (Nielsen, Shneiderman) survive as motivating design goals but do not transfer operationally to LLM skill chains (MODERATE confidence).** They were designed for synchronous, deterministic GUI interactions; skill chains are asynchronous, probabilistic, and can execute irreversible side effects before a user reaches an "emergency exit." Use the heuristics to motivate design; expect that the implementations require original work.

## Two Principles That Translate Most Cleanly

**Visibility of system status** (Nielsen Heuristic 1): The human must always know which skill is running, what it has produced, and what comes next. Without this, chains are opaque state machines. This is non-negotiable.

**User control and freedom** (Nielsen Heuristic 3): Abort and redirect must be available at every skill boundary. Not just "stop" — also "continue from here with a different instruction." ChatGPT agent mode's model: users type "stop" to halt, then provide corrections and continue from there.

## The Wizard Pattern: Useful for Structure, Not Sequential Enforcement

Wizard UI patterns — sequential stages, named steps, closure at completion — are a useful structural analog for skill chains. What does not transfer: the core wizard constraint of "do not allow users to skip steps" is directly contraindicated for expert users and should not be applied universally. wos's target audience is developers who expect transparency and control, not protective scaffolding.

## Interruption: At Boundaries, Not Mid-Skill

HCI interruption research (Frontiers in Psychology, 2024) shows that interruptions at task chunk boundaries have lower resumption costs. For skill chains: offer interruption points after a skill completes, before the next is invoked. Mid-skill interruption is architecturally harder and leaves chain state in an ambiguous position.

The mixed-initiative control principle: the agent must never block the human from interacting. Human input always takes precedence — if there is a conflict between human actions and agent plans, the human's action wins.

## Abort Is Not Sufficient — Redirect Without Restart

Abort-only design forces users to restart the entire chain after a correction. The correct model provides both halt and redirect: "stop, provide corrections, continue from there." This requires the chain to preserve its prior stage outputs as re-entry points (see skill-chain-recovery-and-state-checkpointing.context.md).

## The Autonomy Dial

Smashing Magazine (2026) describes an autonomy dial from "Observe & Suggest" through "Act Autonomously." wos chains — human confirms at every gate — sit at the high-safety, low-autonomy end. This is appropriate for a developer tool where the human is also the author making consequential, often irreversible decisions.

The design task is not reducing gates. It is making each gate fast enough that it does not become friction — targeting 10–30 seconds per decision. Approval fatigue (gates without gate quality) is the failure mode, not the number of gates.

## Timeout Handling

Gates must not stall indefinitely. Production HITL systems (Zapier, n8n, Orkes) all implement timeout with explicit fallback: auto-escalate, shelve for later review, or default to the safest outcome. A stalled gate that eventually auto-executes after context has changed is worse than no gate.

**Bottom line:** Design for status visibility and user control above all else. Interrupt at skill boundaries. Build redirect-without-restart alongside abort. Set timeouts on every gate. Treat HCI heuristics as motivating principles — implementations require original work for a text-based, conversational interface.
