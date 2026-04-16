---
name: "Skill Chain Handoff Signaling and Evidence Packs"
description: "Every skill boundary needs three elements: closure signal, intent preview, and provenance tag; confidence scores cause overreliance not calibration; evidence packs beat confidence scores; approximate language beats numerical precision."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows
  - https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-hand-off
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
  - https://arxiv.org/html/2402.07632v4
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
  - https://agentic-design.ai/patterns/ui-ux-patterns/confidence-visualization-patterns
  - https://www.nngroup.com/articles/wizards/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
  - docs/research/2026-04-10-skill-chaining-human-usability.research.md
  - docs/context/skill-handoff-contracts-and-state-design.context.md
  - docs/context/skill-chain-human-control-and-interruption-design.context.md
  - docs/context/skill-chain-hitl-patterns-and-cli-translation-gap.context.md
---
# Skill Chain Handoff Signaling and Evidence Packs

**Do not surface a confidence percentage at approval gates. Evidence packs beat confidence scores.** Automation bias research shows that confidence signals cause overreliance — users scrutinize less when AI appears confident, not more. The goal at a skill handoff is a genuine decision moment, not a checkbox interaction.

## Three Required Elements at Every Skill Boundary

The evidence from the wizard pattern (NNG), Copilot Studio (Microsoft), and Smashing Magazine (2026) converges on three elements that every handoff message must contain:

1. **Closure signal** — what this skill accomplished ("Research complete: 27 sources gathered, 8 sub-questions addressed"). Shneiderman's Rule 4: "Informative feedback at the completion of a group of actions gives users the satisfaction of accomplishment." Without this, users have no cognitive confirmation that a stage finished correctly.

2. **Intent preview** — what the next skill will do, with explicit user choices ("Proceed with distillation / Adjust research scope / Stop here"). Smashing Magazine's Intent Preview pattern: "Before autonomous action, display a clear plan summary with explicit user choices." This is a pre-execution transparency gate.

3. **Provenance tag** — which skill produced the output. In chains where multiple agents contribute, the human needs to know where each piece of the output came from. NNG's wizard recommendation: use descriptive step labels ("Research complete," "Distillation in progress") not technical identifiers ("/wos:research," "/wos:distill").

## Evidence Packs Over Confidence Scores

The automation bias literature directly contradicts confidence scores as a calibration mechanism:

- A systematic review (PMC) found approximately 26% overreliance on incorrect automated advice across domains.
- A controlled study (arXiv 2402.07632) found that miscalibrated AI confidence causes users to defer to the system even when it is wrong.
- When an AI displays high confidence, users scrutinize less, not more.

What works instead:

**Evidence packs**: At each approval gate, surface a structured summary — what the skill proposes to do, its reasoning behind key decisions, source data, preconditions, and what rollback looks like. StackAI identifies the "difference between a 15-second approval and a 15-minute investigation" as the evidence pack quality. Components: action summary, agent reasoning, source data, policy flags, preconditions, rollback options.

**Explicit uncertainty framing**: "I found 4 sources that disagree with the main finding" is more actionable than "medium confidence." Name the source of uncertainty rather than abstracting it into a score.

**Approximate language over precision**: "~high confidence" is more honest than "94.7%." False numerical precision worsens calibration rather than improving it. Agentic Design (CVP patterns): "Rather than false precision (e.g., '99.73%'), systems should express approximate confidence ('~very high')."

## Concise by Default, Expandable on Request

Expert developer users — wos's primary audience — will find excessive inter-skill commentary slow and patronizing. Design all disclosure as concise-by-default, expandable on demand: a one-line closure summary at every gate, with a way to request full detail. The goal is a 10–30 second decision time at each gate, not a 15-minute investigation.

The two-channel model (Copilot Studio): user-facing messages should be concise and decision-focused; skill-facing state should carry the full structured output. These are separate channels with separate audiences.

**Bottom line:** Replace confidence percentages with evidence packs. Every handoff needs a closure signal, an intent preview, and a provenance tag. Approximate language beats numerical precision. Design for 10–30 second decisions, not investigations.
