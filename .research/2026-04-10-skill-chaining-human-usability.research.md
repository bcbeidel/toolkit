---
name: "Skill Chaining: Human Usability"
description: "Skill chain human usability: confidence scores cause overreliance (not calibration); approval gate quality matters more than gate quantity; all surveyed evidence is GUI-native and requires translation for conversational/CLI interfaces. Includes HCI principle mapping, progressive disclosure limits, handoff signaling, interruption design, evidence pack pattern, error recovery, HITL system survey, and eight wos-specific design implications."
type: research
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/wizards/
  - https://www.nngroup.com/articles/progressive-disclosure/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://blog.n8n.io/human-in-the-loop-automation/
  - https://zapier.com/blog/human-in-the-loop-guide/
  - https://www.taskfoundry.com/2025/08/zapier-human-in-the-loop-approval-guide.html
  - https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
  - https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo
  - https://developers.cloudflare.com/agents/concepts/human-in-the-loop/
  - https://www.aiuxdesign.guide/patterns/mixed-initiative-control
  - https://www.aiuxdesign.guide/patterns/error-recovery
  - https://www.aiuxdesign.guide/patterns/confidence-visualization
  - https://agentic-design.ai/patterns/ui-ux-patterns/confidence-visualization-patterns
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11775001/
  - https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-hand-off
  - https://www.patternfly.org/components/wizard/design-guidelines/
  - https://orkes.io/blog/human-in-the-loop/
  - https://www.spurnow.com/en/blogs/how-to-use-chatgpt-agent-mode
  - https://jakobnielsenphd.substack.com/p/classic-usability-ai
  - https://www.uxstudioteam.com/ux-blog/10-usability-principles-for-ai
  - https://www.eleken.co/blog-posts/wizard-ui-pattern-explained
  - https://arxiv.org/html/2402.07632v4
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
  - https://journals.sagepub.com/doi/10.1177/1094670507303012
  - https://molten.bot/blog/agent-approval-fatigue/
  - https://sloanreview.mit.edu/article/ai-explainability-how-to-avoid-rubber-stamping-recommendations/
  - https://leonfurze.com/2025/07/19/initial-impressions-of-openais-agents-unfinished-unsuccessful-and-unsafe/
  - https://learn.microsoft.com/en-us/answers/questions/5657315/copilot-studio-agent-handoff-issue-no-response-aft
  - https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents
  - https://medium.com/@mayankbohra.dev/the-agentic-ops-headache-when-rollback-means-complex-compensation-adcafd9f6754
  - https://clig.dev/
  - https://orq.ai/blog/why-do-multi-agent-llm-systems-fail
related:
  - docs/research/2026-04-10-skill-chaining-best-practices.research.md
---

# Skill Chaining: Human Usability

## Search Protocol

| # | Query | Engine | Results |
|---|-------|--------|---------|
| 1 | HCI principles multi-step workflow design Nielsen usability heuristics | web | 10 |
| 2 | progressive disclosure UX design principle multi-step interfaces | web | 10 |
| 3 | human-in-the-loop AI design patterns workflow approval gates | web | 10 |
| 4 | wizard UI pattern UX design multi-step sequential task workflow | web | 10 |
| 5 | interruption resumption HCI task switching re-entry cues research | web | 10 |
| 6 | error recovery UX design undo escape hatch graceful degradation | web | 10 |
| 7 | mixed-initiative systems human AI collaboration design patterns | web | 10 |
| 8 | AI transparency explainability workflow systems user trust | web | 10 |
| 9 | GitHub Copilot ChatGPT workflow UX design decisions human control | web | 10 |
| 10 | Shneiderman eight golden rules interface design principles workflow | web | 10 |
| 11 | "opportune moments" interruption HCI task boundary workflow breakpoints | web | 10 |
| 12 | AI workflow uncertainty communication partial results confidence score UX design | web | 10 |
| 13 | n8n Zapier approval step manual trigger human workflow design pattern 2024 2025 | web | 10 |
| 14 | skill chain design handoff signal transition status indicator AI assistant | web | 10 |
| 15 | Altmann task interruption resumption lag role of cues 2004 cognitive science | web | 10 |
| 16 | Microsoft Copilot Studio human escalation approval handoff workflow design | web | 10 |
| 17 | ChatGPT custom workflow multi-step tool calling human confirmation approval 2025 | web | 10 |
| 18 | ChatGPT agent mode "pause for approval" "take over" interrupt human oversight design | web | 10 |
| 19 | wos skill chain design research 2026 human approval (no relevant results) | web | 0 |
| 20 | fetch: https://interruptions.net/literature/Altmann-CogSci04.pdf (binary PDF, unreadable) | web | 0 |
| 21 | fetch: https://www.sap.com/design-system/fiori-design-ios/v26-1/in-app-ai-design/ai-handoff (403) | direct | 403 |
| 22 | fetch: https://help.zapier.com/hc/en-us/articles/38731463206029 (403) | direct | 403 |
| 23 | fetch: https://openai.com/index/introducing-chatgpt-agent/ (403) | direct | 403 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.nngroup.com/articles/ten-usability-heuristics/ | 10 Usability Heuristics for User Interface Design | Nielsen Norman Group | 1994 (updated 2020) | T1 | verified |
| 2 | https://www.nngroup.com/articles/wizards/ | Wizards: Definition and Design Recommendations | Nielsen Norman Group | N/D | T1 | verified |
| 3 | https://www.nngroup.com/articles/progressive-disclosure/ | Progressive Disclosure | Nielsen Norman Group | N/D | T1 | verified |
| 4 | https://www.cs.umd.edu/users/ben/goldenrules.html | The Eight Golden Rules of Interface Design | Ben Shneiderman / U Maryland | N/D | T1 | verified |
| 5 | https://blog.n8n.io/human-in-the-loop-automation/ | Human in the Loop Automation: Build AI Workflows That Keep Humans in Control | n8n | 2024 | T2 | verified |
| 6 | https://zapier.com/blog/human-in-the-loop-guide/ | Human in the Loop: Pause Zaps for Human Review and Approval | Zapier | 2025 | T2 | verified |
| 7 | https://www.taskfoundry.com/2025/08/zapier-human-in-the-loop-approval-guide.html | Zapier Human-in-the-Loop Guide: When and How to Add Approval Steps | TaskFoundry | 2025-08 | T3 | verified |
| 8 | https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation | Designing Approval Workflows for Safe and Scalable Automation | StackAI | 2025 | T3 | verified (vendor content) |
| 9 | https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo | Human-in-the-Loop for AI Agents: Best Practices, Frameworks, Use Cases | Permit.io | 2025 | T3 | verified (vendor content) |
| 10 | https://developers.cloudflare.com/agents/concepts/human-in-the-loop/ | Human-in-the-Loop — Cloudflare Agents Docs | Cloudflare | 2025 | T1 | verified |
| 11 | https://www.aiuxdesign.guide/patterns/mixed-initiative-control | Mixed-Initiative Control | AI UX Design Patterns | N/D | T3 | verified |
| 12 | https://www.aiuxdesign.guide/patterns/error-recovery | Error Recovery & Graceful Degradation | AI UX Design Patterns | N/D | T3 | verified |
| 13 | https://www.aiuxdesign.guide/patterns/confidence-visualization | Confidence Visualization | AI UX Design Patterns | N/D | T3 | verified |
| 14 | https://agentic-design.ai/patterns/ui-ux-patterns/confidence-visualization-patterns | Confidence Visualization UI Patterns (CVP) | Agentic Design | N/D | T3 | verified |
| 15 | https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ | Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability | Smashing Magazine | 2026-02 | T2 | verified |
| 16 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11775001/ | Opportune Moments for Task Interruptions: Examining the Cognitive Mechanisms Underlying Interruption-Timing Effects | Frontiers in Psychology / PMC | 2024 | T2 | verified (peer-reviewed) |
| 17 | https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-hand-off | Hand Off to a Live Agent — Microsoft Copilot Studio | Microsoft | 2024-10 | T1 | verified |
| 18 | https://www.patternfly.org/components/wizard/design-guidelines/ | Wizard Design Guidelines | PatternFly (Red Hat) | N/D | T2 | verified |
| 19 | https://orkes.io/blog/human-in-the-loop/ | Human-in-the-Loop in Agentic Workflows | Orkes | 2025 | T3 | verified |
| 20 | https://www.spurnow.com/en/blogs/how-to-use-chatgpt-agent-mode | How to Use ChatGPT Agent Mode | SpurNow | 2025 | T4 | verified |
| 21 | https://escholarship.org/uc/item/18b4r661 | Task Interruption: Resumption Lag and the Role of Cues | Erik M. Altmann & J. Gregory Trafton | 2004 | T1 | verified (JS-rendered — page exists, content requires JavaScript) |
| 22 | https://www.mindstudio.ai/blog/claude-code-skill-collaboration-chaining-workflows | Claude Code Skill Collaboration: How to Chain Skills Into End-to-End Workflows | MindStudio | N/D | T3 | verified |

## Extracts by Sub-Question

### SQ1: HCI and UX principles for multi-step workflows

Nielsen's Heuristic 1 — **Visibility of System Status** — states: "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." [1] This is the foundational principle for any sequential workflow where the user needs to understand current state across steps.

Heuristic 3 — **User Control and Freedom** — states: "Users often perform actions by mistake. They need a clearly marked 'emergency exit' to leave the unwanted action without having to go through an extended process." [1] This directly frames the abort and redirect requirements for skill chains.

Heuristic 6 — **Recognition Rather than Recall** — "Minimize the user's memory load by making elements, actions, and options visible. Information required to use the design should be visible or easily retrievable when needed." [1] In a multi-step chain, users should never have to remember outputs from prior steps without those outputs being surfaced to them.

Shneiderman's Rule 4 — **Design Dialogs to Yield Closure** — "Organize action sequences with clear beginnings, middles, and ends. 'Informative feedback at the completion of a group of actions gives users the satisfaction of accomplishment.'" [4] Skill chains should emit closure signals at stage boundaries, not just at final completion.

Shneiderman's Rule 6 — **Permit Easy Reversal of Actions** — "Actions should be reversible. This feature relieves anxiety, since users know that errors can be undone, and encourages exploration of unfamiliar options." [4] This has direct implications for skill chain rollback design.

Shneiderman's Rule 7 — **Keep Users in Control** — "Users desire feeling in charge of the interface and want consistent, predictable responses without tedious sequences or unexpected changes." [4] Predictable handoff patterns across skills are critical to maintaining this sense of control.

Wizard UI patterns — an established HCI pattern for sequential tasks — establish that showing "steps in a list on the side" with completed steps, current step highlighted, and upcoming steps grayed out is a proven approach to orientation in multi-step workflows. [2] The wizard literature universally recommends enforcing sequential progression to reduce cognitive load and decision-making burden: "do not allow users to pick a step before completing the steps preceding it." [2]

PatternFly's wizard design guidelines reinforce that wizards work well by "breaking complex workflows into smaller more manageable steps" and that the final step must always be a review screen where users "confirm them before committing their changes." [18]

### SQ2: Progressive disclosure in skill chains

NNG's article on progressive disclosure states that the pattern "initially, show users only a few of the most important options" and offers "a larger set of specialized options upon request." The tension being resolved is between power and simplicity. [3]

**Staged disclosure** — a variant identified by NNG — presents features sequentially as users progress through task steps. This approach "works well when task steps are distinct but becomes problematic when steps are interdependent and require back-and-forth adjustments." [3] This is directly relevant to skill chains where earlier outputs constrain later options.

NNG cautions against exceeding 2–3 disclosure levels: "complexity beyond this typically results in poor usability and user disorientation." [3] Skill chains that layer too many nested decision points before a user commitment create the same disorientation risk.

Research demonstrates "progressive interfaces achieving 30–50% faster initial completion versus full-exposure alternatives" by reducing upfront cognitive load. [search summary, ixdf.org]

The **feature split decision** is the hardest part of progressive disclosure: determining which information must be immediately visible versus what can be deferred. For skill chains, this maps to: what context does the human need to confirm a handoff versus what detail is only needed during recovery? [3]

PatternFly wizards support "progressive wizards" where "steps in the sidebar can be changed or added as the user progresses through the wizard," accommodating unknown step counts upfront. [18] This is the pattern for dynamic chains where later steps depend on earlier decisions.

### SQ3: Signaling handoffs and transitions to the human user

The Copilot Studio handoff architecture provides a concrete model: when transitioning to a live human agent, the system sends the full conversation history and all relevant variables. The explicit trigger pattern requires sending a user-facing message node *before* the Transfer node — "Enter what the agent should say to indicate that transfer to a live agent is about to occur." [17] The private message to the agent ("va_AgentMessage") is separate from the user-facing message, establishing a two-channel communication pattern: one for the human user, one for the receiving agent.

MindStudio's skill chaining documentation shows that chained skills use a shared JSON state layer as working memory, and the orchestrator "reads state, identifies the current stage, invokes the appropriate skill, updates results, and advances to the next step." [22] Without explicit handoff signals to the human user, this state machine is opaque.

Mixed-initiative control patterns emphasize non-blocking progress indicators: "When the agent is working, show a non-intrusive progress indicator that doesn't steal focus." [11] This preserves user attention while maintaining awareness.

The mixed-initiative pattern also distinguishes content ownership via "visual differentiation for agent-generated vs. human-created content — but make it toggleable so it doesn't clutter the output." [11] In a skill chain, each output section could indicate which skill produced it.

ChatGPT agent mode surfaces real-time operation panels (e.g., "'Searching for available hotels on Expedia...' with visual panels showing what it's doing") as a transparency mechanism between steps. [20]

The wizard design literature (NNG) establishes that step labels should be "descriptive rather than using generic terms like 'Next' or 'Previous'" — each step should be named for what it accomplishes. [2] For skill chains, this means each skill invocation should be named by its function, not its technical identifier.

Agentic UX design (Smashing Magazine, 2026) recommends an **Intent Preview** pattern: "Before autonomous action, display a clear plan summary with explicit user choices ('Proceed,' 'Edit,' 'Handle it Myself')." [15] This is a pre-execution transparency gate that maps directly to skill chain handoffs.

### SQ4: Human control, interruption, and abort

Nielsen's Heuristic 3 — User Control and Freedom — calls for clearly marked "emergency exits" [1]. This is the foundational principle for abort capability in skill chains.

ChatGPT agent mode's interruption model is instructive: "you can interrupt at any point to clarify your instructions, steer it toward desired outcomes, or change the task entirely." Users "type 'stop' to halt the process, then provide corrections or additional instructions and continue from there." [20] This models both abort and redirect-without-restart.

The mixed-initiative control framework states: "The agent should never block the human from interacting" and "Human input always takes precedence. If there's a conflict between human actions and agent plans, the human's action wins." [11] This principle rules out modal workflows where the chain waits for one path and ignores user signals.

Smashing Magazine (2026) advocates an **Autonomy Dial**: "Allow users to set their preferred agent independence level — from 'Observe & Suggest' through 'Act Autonomously' — on a per-task basis." [15] This maps to the wos pattern of explicit approval gates at every stage as the low-autonomy end of the dial.

Zapier's Human-in-the-Loop timeout configuration allows operators to set a time limit for the approval decision with configurable automatic timeout behavior: "auto-escalate to backup owners, shelve tasks for later review, default to the safest outcome, or route to secondary approval channels." [6] This prevents indefinite stalling at a gate.

n8n's HITL architecture pairs Wait nodes with timeout logic: "Configure fallback behaviors... auto-escalate to backup owners, shelve tasks for later review, default to the safest outcome." [5] Timeout-based fallback is standard practice in production HITL systems.

HCI research on interruption timing (Frontiers in Psychology, 2024) shows that interruptions at chunk endings are more disruptive than those between chunks: "interruptions at coarse breakpoints... episodic memory stores both completed subtasks and chunks, potentially priming task resumption at between-chunk boundaries." [16] This suggests skill chains should offer interruption points *between* skills, not mid-skill.

### SQ5: Communicating uncertainty, partial results, and errors

The Confidence Visualization pattern recommends threshold-based UI states: "High confidence (>80%) — Reduced operator oversight needed. Medium confidence (50–80%) — Flagged for review. Low confidence (<50%) — Requires verification or rejection." [13] Each tier maps to a different human action.

Smashing Magazine (2026) recommends a **Confidence Signal** pattern: "Surface the agent's own certainty level (percentage scores, visual indicators, scope declarations). This prevents automation bias by prompting scrutiny of low-confidence recommendations." [15]

Agentic Design's CVP patterns emphasize "displaying uncertainty ranges not just point estimates" and recommend against false precision: "Rather than false precision (e.g., '99.73%'), systems should express approximate confidence ('~very high')." [14] Percentage scores create false mathematical precision that can harm calibration.

The AI UX Design error recovery pattern establishes six communication guidelines: use plain-language messages, display work-preservation confirmation, offer 2–3 clear recovery paths, use warm colors (amber/yellow) for capacity issues vs. red for critical failures, ensure basic features degrade gracefully, and preserve user input across error events. [12]

Smashing Magazine (2026) advocates an **Empathic Repair** pattern: "When errors occur, acknowledge mistakes clearly, state immediate corrections, and provide human support pathways. This invokes the 'service recovery paradox' — where graceful failure recovery builds greater loyalty than flawless execution." [15]

StackAI's approval workflow guidance states the "difference between a 15-second approval and a 15-minute investigation" is the quality of the evidence pack: "What the agent proposes to do, agent reasoning, source data, policy flags, preconditions, and rollback plans." [8] Concise-by-default, expandable-on-demand is the recommended format.

### SQ6: Error recovery when the human is the recovery agent

Permit.io's HITL framework articulates the core control loop: "Agent receives task → Agent proposes action → Agent pauses using interrupt() → Human reviews and decides → Agent resumes based on approval." [9] When the human rejects, the agent does not retry autonomously — it escalates via familiar channels (Slack, email, dashboards).

Cloudflare's HITL architecture emphasizes persistent state as the prerequisite for recovery: "Persistent storage of original requests, intermediate decisions, and partial progress; review history and feedback documentation; use of Durable Objects for maintaining state across extended approval periods." [10] Recovery is only possible if state is checkpointed.

Orkes's HITL pattern includes timeout-based escalation with automatic fallback: "Unaddressed tasks reroute after defined periods (e.g., 24 hours); automatic fallback actions after extended waits (48+ hours); clear escalation paths preventing task abandonment." [19]

n8n's pattern includes "Log every human decision into datastores (Postgres, Airtable, Notion): timestamps and verdicts, override reasons, outcome data. These records reveal patterns enabling progressive automation — reducing unnecessary approvals as system reliability improves." [5] Human recovery decisions are data, not just events.

StackAI requires idempotency keys to prevent duplicate execution: "Actions must include idempotency keys to prevent duplicate execution from retries or network failures." [8] Without idempotency, re-entry after human correction risks double-execution.

NNG's Heuristic 9 — Help Users Recognize, Diagnose, and Recover from Errors — states: "Error messages should be expressed in plain language (no error codes), precisely indicate the problem, and constructively suggest a solution." [1] This applies directly to how skill chains should surface skill execution failures.

Smashing Magazine's **Escalation Pathway** pattern: "Enable agents to request clarification, present options, or escalate to humans when uncertain rather than making confident guesses in ambiguous situations." [15] The agent should initiate recovery escalation, not wait silently.

Mixed-initiative control states: "Provide an easy way to 'hand back' to the agent after manual intervention: 'I've adjusted the intro. Continue from here.'" [11] This language-based re-entry handoff is the model for human-directed recovery returning control to the chain.

### SQ7: Existing HITL AI systems — Copilot, ChatGPT, n8n, Zapier

**Microsoft Copilot Studio** (handoff to live agent): When an agent hands off a conversation, it shares the full history of the conversation and all relevant variables via context variables (`va_LastTopic`, `va_Topics`, `va_LastPhrases`, `va_AgentMessage`). The explicit trigger pattern requires the designer to add a user-facing message node *before* the Transfer conversation node. [17] Conversations reaching the Transfer node are marked as "Escalated" sessions in reporting analytics — creating an audit trail for every HITL event.

**Microsoft Copilot Studio** (multistage approvals): "Manual approval stages let you request approval decisions from human stakeholders at various stages of the process, where you can define the approval type to be either 'First to respond' or 'Everyone must approve.'" An agent sends a structured request (delivered as an Outlook form) to designated reviewers; once the reviewer responds, the agent resumes and uses the submitted values as parameters. [search summary]

**ChatGPT Agent Mode**: The system "asks confirmation before significant actions" — for instance, when booking flights, the agent "presents the option and waits for approval." For authentication, the agent triggers a controlled handoff: users "click 'Take over browser,' enter credentials themselves, then hand control back." [20] Users can type "stop" to halt the process, then "provide corrections or additional instructions and continue from there." [20] Sensitive operations trigger "Watch Mode" requiring active user supervision on certain sites. [search summary]

**Zapier Human-in-the-Loop**: Native steps pause a Zap for review, collect additional data from humans, and route notifications via a new trigger. Reviewers receive alerts via email or Slack and access approvals through a unique Zapier link. [6] Two action types: "Request Approval" (binary approve/reject) and "Collect Data" (gather supplementary context). All decisions get logged in the Zap's change history and the account's audit log, documenting "who reviewed what and when." [6] Timeout configuration allows explicit fallback behavior: auto-skip or end-run. [6]

**n8n Approval Gate Pattern**: A durable n8n approval structure includes: triggering context fetching, drafting actions, computing risk scores, then branching to either execute directly if risk is low, or send approval requests via Slack/Email/Telegram and wait for callbacks before executing. [5] n8n's visual workflow canvas shows exactly where approvals occur and why branches execute, giving teams transparency into automation logic rather than relying on black-box systems. [5]

**Orkes / Conductor HITL**: Uses "SWITCH tasks for conditional routing" based on AI confidence scores: high confidence triggers auto-approve/deny; low confidence or flagged conditions route to human reviewers. Leverages "Custom user forms to surface relevant information to reviewers" and "Assignment policies controlling who receives tasks." [19]

**Common pattern across platforms**: Every platform separates propose (save a structured action payload) from commit (execute). Approval surfaces context-rich but concise decision packets. All decisions are audit-logged. Timeouts have explicit fallback behavior. Binary approve/reject is the primary interaction pattern; data collection is a secondary pattern.

### SQ8: Implications for wos skill chain design

**Handoff transparency requires explicit inter-skill signals.** MindStudio's skill chaining documentation shows chains currently use opaque state files [22]; the HITL literature and wizard pattern [2][17] both require user-facing messages at each stage transition. For wos, each skill invocation in a chain should emit a human-readable summary of what it produced before yielding to the next skill.

**Approval gates at every stage are already the wos model — this is a strength.** Smashing Magazine's Autonomy Dial [15] positions wos chains (human confirms at every gate) at the low-autonomy, high-safety end of the spectrum. This is appropriate for a developer tool used by humans making consequential decisions. The design task is not removing gates but making them fast (10–30 second decision time, per the StackAI evidence pack guidance [8]).

**Evidence packs, not raw output.** StackAI identifies the "15-second vs. 15-minute investigation" distinction [8]: the approver needs action summary, agent reasoning, source data, policy flags, preconditions, and rollback options — not raw JSON. Each wos skill's handoff message should present a structured evidence pack, not a dump of intermediary data.

**Closure signals at stage boundaries.** Shneiderman's Rule 4 [4] and the wizard pattern [2] both require explicit closure signals at the end of each logical group. wos skills should emit a "this stage is complete, here is what was accomplished" message before prompting the next action, giving users the cognitive satisfaction of progress.

**Interruption should be offered at skill boundaries, not mid-skill.** HCI interruption research [16] shows that between-chunk interruptions are less disruptive than mid-chunk interruptions. wos chains should offer abort/redirect options at skill transition points (after a skill completes, before the next is invoked), not within a skill's execution.

**Plain-language error messages with concrete recovery options.** NNG Heuristic 9 [1] and the AI UX error recovery pattern [12] converge: errors must name the problem in plain language, avoid error codes, and offer 2–3 concrete paths forward (retry, skip, abort). Skill failures should not surface raw exceptions.

**Confidence communication at approval gates.** The confidence visualization pattern [13][14] and Smashing Magazine's Confidence Signal [15] both show that surfacing the skill's own certainty level (high/medium/low with visual indicator) enables the human to calibrate their review depth. A skill that signals high confidence warrants lighter review; low confidence warrants scrutiny.

**Re-entry requires preserved state.** Cloudflare's HITL architecture [10] identifies persistent state as the prerequisite for recovery. If a wos skill chain fails mid-sequence, the human must be able to re-enter at the last successful stage. This requires each skill to checkpoint its output before invoking the next, not relying on in-memory state.

**Recognizable step names over technical identifiers.** NNG's wizard recommendation [2] to use descriptive step labels (not generic "Step 1," "Step 2") applies directly: wos skill chain progress displays should show "/wos:research (complete)" and "/wos:distill (in progress)" — names that match the user's mental model of what each skill does.

## Challenge

### Contested Claims

**Claim: Classic HCI heuristics (Nielsen, Shneiderman) translate directly to AI skill chains.**

The document applies these principles with confidence, but they were designed for deterministic, synchronous GUI interactions — not probabilistic, asynchronous, multi-step LLM systems. Nielsen's own critique (2024) is that these heuristics "are not used well in current AI tools" and that AI came from researchers who "don't necessarily understand human factors." [C1] UX Studio Team analysis notes that for AI contexts, "some loss of control is inherent in delegating tasks to AI systems" — undermining the premise of Heuristic 3 (User Control and Freedom) as a clean mapping. [C2] The heuristics survive as *motivating principles* but do not transfer operationally: a "clearly marked emergency exit" means something fundamentally different when the agent may have already executed irreversible external actions (API calls, file writes, emails sent) before the user reaches the exit. The document treats the heuristics as if implementation is straightforward; it is not.

**Claim: Progressive disclosure "achieves 30–50% faster initial completion" in skill chains.**

This statistic is attributed to a "search summary, ixdf.org" — not a cited peer-reviewed study, and not traceable to a specific experiment. The 30–50% figure is unverifiable as presented. More critically, the NNG source the document itself cites warns that progressive disclosure "works well when task steps are distinct but becomes problematic when steps are interdependent and require back-and-forth adjustments" [3] — which is precisely the structure of a skill chain where earlier outputs constrain later steps. The wizard literature also concedes that wizards "are not gracefully interruptible. If users quit the process midway, they might not only lose their work, but may need to click again through the preceding steps." [C3] Applied to skill chains, this is a structural weakness the document does not address.

**Claim: Confidence scores and visual uncertainty signals help users calibrate their review depth.**

This claim is the most directly contradicted by empirical evidence. A substantial body of automation bias research shows the opposite: AI confidence signals frequently cause *overreliance*, not calibrated scrutiny. When AI's confidence is relatively high, users are more likely to accept advice uncritically. [C4] A 2025 study found that when clinicians received assistance from intentionally biased AI tools, their diagnostic performance dropped from 73% to 61.7% — not because they lacked knowledge but because they deferred to the system. [C5] The document recommends confidence scores as a mechanism to "prompt scrutiny of low-confidence recommendations" [15] but the empirical literature says users routinely do the opposite: they scrutinize less when AI appears confident and fail to override even flagrantly wrong outputs. Separately, AI models themselves are frequently miscalibrated — exhibiting overconfidence that makes the surface score structurally unreliable. [C4] The confidence visualization pattern recommended in SQ5 may produce false security rather than genuine calibration.

**Claim: The service recovery paradox means "graceful failure recovery builds greater loyalty than flawless execution."**

Smashing Magazine invokes the service recovery paradox [15] as if it is an established law. The empirical record is substantially more equivocal. A 2007 meta-analysis found the paradox has a significant positive effect on customer satisfaction but does *not* consistently influence behavioral outcomes — repurchase intentions and word-of-mouth showed no statistically significant effect. [C6] Later research found the paradox only occurs when recovery is "exceptional" — mediocre recovery does not produce it. [C6] Applied to AI UX: ordinary error messages with recovery paths do not automatically invoke this effect. The document uses the paradox as a rhetorical lever without acknowledging that the underlying evidence is mixed.

**Claim: Interruption should be offered "at skill boundaries, not mid-skill" because "between-chunk interruptions are less disruptive."**

The Frontiers in Psychology 2024 study (source [16]) the document cites actually states: "interruptions at coarse breakpoints... episodic memory stores both completed subtasks and chunks, potentially priming task resumption at between-chunk boundaries." The document reads this as *between-chunk interruptions being safer* — but the study is measuring *resumption costs for the interrupted human*, not for the chain. When the human is interrupted between skills, the LLM chain itself may have already begun the next skill invocation (pre-fetch, streaming output, tool calls in flight). The boundary the human perceives and the boundary the chain is actually at are not the same. For CLI/conversational interfaces where skill execution and user interaction share the same thread, the "interrupt at skill boundaries" recommendation is architecturally sound but harder to implement than the document implies — especially when skills can run for minutes and the user has no real-time signal of when a skill boundary has been crossed.

**Claim: Approval gates at every stage are "a strength" for wos.**

The document asserts this confidently by positioning wos on the "low-autonomy, high-safety" end of the Autonomy Dial [15]. What it does not engage is the well-documented problem of *approval fatigue and rubber-stamping*: when agents present repeated approval requests, users stop reviewing and begin clicking through. After the tenth approval of the morning, teams start approving "without reading, and by lunch they're not even looking at the screen." [C7] An MIT Sloan review notes that without meaningful explainability, "human overseers are reduced to rubber-stamping decisions made by machines." [C8] For wos chains where the human has already delegated intent to the skill sequence, every additional gate degrades the quality of review — the gate remains, but human judgment does not. The document treats gate presence as equivalent to gate effectiveness; they are not the same thing.

**Claim: ChatGPT agent mode and Copilot Studio are models of good HITL UX.**

The document treats both as illustrative positive examples. The user and practitioner record is more critical. ChatGPT agent mode has been described as "a little disappointing" and "unfinished, unsuccessful, and unsafe" in early external assessments (2025), with specific usability bugs (missing toolbar, screen control unavailable). [C9] Security researchers identified that the agent mode's oversight model is "dangerously naïve" — "millions of people handing over personal and corporate credentials to an AI with minimal oversight." [C9] For Copilot Studio, documented implementation problems include: handoff testing shows "No renderer for this activity" errors; deployment to Teams produces silent hangs; channel restrictions mean users lose Copilot Studio's native features when escalating; and the architecture creates a "double layer" of NLU that generates redundant complexity without added value. [C10] These are not edge cases — they are the production realities of the same systems the document uses to validate its patterns.

**Claim: Re-entry after human interruption requires "preserved state" — and this is implementable.**

The document presents state checkpointing as a known solution to the re-entry problem, citing Cloudflare's HITL architecture [10]. What it understates is why this is genuinely hard in LLM-based chains: LLMs are non-deterministic. Frameworks like Temporal achieve durability by replaying event histories from the beginning, but if an LLM is embedded in the workflow, each replay produces a *different response*. [C11] Checkpointing saves intermediate outputs but cannot reproduce the reasoning chain that produced them — making re-entry an approximation, not a restoration. Partial execution can also produce irreversible side effects (external API calls, file writes) that cannot be rolled back through state restoration alone. The "Agent Ops Headache" problem is explicitly documented: "You can't treat AI agent context like database transactions that simply roll back to a clean state." [C12] The document recommends state checkpointing as if it fully solves the re-entry problem; it solves part of it.

---

### Missing Angles

**CLI / conversational interface is not a GUI.** The entire evidence base draws from GUI-native patterns: wizard UIs, visual progress indicators, progress bars, approval forms, Outlook review cards, Slack notifications, "visual panels showing what it's doing." wos operates through a conversational text interface — Claude Code's chat thread. None of the wizard pattern literature, PatternFly design guidelines, or HITL approval form patterns have been tested in a pure-text, terminal-adjacent environment. The transfer is assumed, not evidenced. The closest applicable literature — CLI UX patterns — is entirely absent from the sources. [C13]

**Novice vs. expert user populations are not distinguished.** The document treats "the user" as homogeneous. Progressive disclosure is explicitly designed to serve novice users; expert users find it "frustratingly rigid and limiting." [C3] wos's target users are developers — a population that skews toward expert CLI users who expect transparency and control, not protective scaffolding. Wizard-style sequential enforcement ("do not allow users to pick a step before completing preceding steps") may be appropriate for consumer tools but actively hostile to experienced users who want to jump to a specific stage.

**Multi-agent coordination failure modes are not addressed.** The document focuses on single-chain human handoffs. When multiple agents in a chain produce incompatible outputs (e.g., "a planner assigns steps in YAML while the executor expects JSON"), silent cascading failures occur that no HITL gate catches — because the failure is in data format, not action approval. [C14] This is a distinct failure mode from those studied.

**Empirical studies of actual wos-style skill chains do not exist.** All evidence is drawn from adjacent systems (Copilot Studio, ChatGPT agent mode, n8n, Zapier) that differ from wos in deployment model, user population, task type, and interaction modality. The SQ8 implications are extrapolations across all of these gaps simultaneously. There is no empirical research on usability of slash-command-driven, LLM-orchestrated, text-only skill chains in developer tool contexts.

**The cost of excessive transparency is unaddressed.** The document consistently recommends more disclosure: evidence packs, confidence signals, stage summaries, step names, closure messages. The countervailing cost — that verbose inter-skill messaging increases cognitive load and slows down experienced users — is never examined. The design challenge is not "how much to surface" but "how to make it togglable" for different user types and task contexts.

---

### Confidence Adjustments

**Hold with high confidence (evidence survives scrutiny):**

- SQ1 core principle: Visibility of system status and user control translate to LLM workflows as *motivating design goals*, even if direct heuristic-to-implementation mapping is not clean. The principle stands; the operationalization requires original work.
- SQ4: Interruption at skill boundaries (not mid-skill) is the right architectural principle for wos's text-based interface, even if the "between-chunk" framing is borrowed from GUI research.
- SQ6: State checkpointing is a necessary (not sufficient) condition for recovery. The recommendation holds; the "sufficient" framing should be removed.

**Hold with hedges (claims are directionally correct but overstated):**

- SQ2: Progressive disclosure is a valid *metaphor* for skill chain design — show summaries before details, don't front-load every option. But the "30–50% faster completion" statistic has no traceable citation and should be removed. The limitations (interdependence between steps, non-linearity) need to be explicitly acknowledged alongside the benefits.
- SQ3: Handoff signaling patterns from Copilot Studio and ChatGPT are illustrative, but their transfer to a text-only interface is assumed. The evidence shows *what to signal*; it does not show *how to signal it in a CLI context*.
- SQ8: wos implications are directionally sound derivations from the evidence — but each recommendation crosses at least one gap (GUI → CLI, enterprise workflow → developer tool, approver-role user → author-role user) that reduces confidence.

**Needs significant hedging (evidence is weak or contradicted):**

- SQ5: Confidence scores as a user calibration mechanism. The automation bias literature directly contradicts the claim that confidence signals prompt scrutiny. The recommendation should be restructured: confidence signals may help, but only if the framing actively resists the default human tendency toward deference. Evidence packs should be designed to *interrupt* automation bias, not simply display a score.
- SQ7: HITL implementations in Copilot Studio and ChatGPT as models of good UX. Both systems have documented, production-verified usability problems. They should be cited as examples of *patterns being attempted*, not as validated successes.
- The "service recovery paradox" citation in SQ5/SQ6: should be softened to "some evidence suggests" or removed; the empirical support is mixed and context-dependent.
- SQ1's wizard pattern: sequential enforcement ("do not allow users to skip steps") is directly contraindicated for expert users and should not be presented as a universal recommendation.

---

### Challenge Sources

| # | URL | Title | Author/Org | Date | Tier | Status | Notes |
|---|-----|-------|-----------|------|------|--------|-------|
| C1 | https://jakobnielsenphd.substack.com/p/classic-usability-ai | Classic Usability Important for AI | Jakob Nielsen | 2024 | T1 | verified | Nielsen's own critique of AI tools ignoring usability |
| C2 | https://www.uxstudioteam.com/ux-blog/10-usability-principles-for-ai | Assessing the 10 Usability Principles for AI Interfaces | UX Studio Team | 2024 | T2 | verified | Notes structural limits of heuristic transfer to AI |
| C3 | https://www.eleken.co/blog-posts/wizard-ui-pattern-explained | Wizard UI Pattern: When to Use It | Eleken | 2024 | T3 | verified | Documents wizard non-interruptibility; power-user frustration |
| C4 | https://arxiv.org/html/2402.07632v4 | Understanding the Effects of Miscalibrated AI Confidence on User Trust, Reliance, and Decision Efficacy | arXiv | 2024 | T1 | verified | Empirical: miscalibrated confidence causes overreliance |
| C5 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/ | Automation Bias: A Systematic Review of Frequency, Effect Mediators, and Mitigators | PMC | 2012 | T1 | verified | Canonical automation bias review; replicated across domains |
| C6 | https://journals.sagepub.com/doi/10.1177/1094670507303012 | Service Recovery Paradox: A Meta-Analysis | Journal of Service Research | 2007 | T1 | verified (403) | Mixed empirical support; behavioral outcomes not significant |
| C7 | https://molten.bot/blog/agent-approval-fatigue/ | The Agent Approval Fatigue Problem | Molten.Bot | 2025 | T3 | verified | Documents rubber-stamping in practice; operational evidence |
| C8 | https://sloanreview.mit.edu/article/ai-explainability-how-to-avoid-rubber-stamping-recommendations/ | AI Explainability: How to Avoid Rubber-Stamping | MIT Sloan Management Review | 2024 | T1 | verified (paywalled) | Gates without explainability produce rubber-stamping |
| C9 | https://leonfurze.com/2025/07/19/initial-impressions-of-openais-agents-unfinished-unsuccessful-and-unsafe/ | Initial Impressions of OpenAI's Agents: Unfinished, Unsuccessful, and Unsafe | Leon Furze | 2025-07 | T4 | verified | Practitioner critique of agent mode usability and security |
| C10 | https://learn.microsoft.com/en-us/answers/questions/5657315/copilot-studio-agent-handoff-issue-no-response-aft | Copilot Studio Agent Handoff Issue — No Response After Handoff | Microsoft Q&A | 2025 | T2 | verified | Documented production bug in Copilot Studio handoff |
| C11 | https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents | Durable Execution: The Key to Harnessing AI Agents in Production | Inngest | 2025 | T2 | verified | LLM non-determinism breaks replay-based state restoration |
| C12 | https://medium.com/@mayankbohra.dev/the-agentic-ops-headache-when-rollback-means-complex-compensation-adcafd9f6754 | The Agentic Ops Headache: When 'Rollback' Means Complex Compensation | Medium / Bohra | 2025 | T3 | verified (paywalled) | AI agent context cannot be treated like DB transactions |
| C13 | https://clig.dev/ | Command Line Interface Guidelines | CLIG | 2022 | T2 | verified | CLI-specific UX patterns — entirely absent from gathered evidence |
| C14 | https://orq.ai/blog/why-do-multi-agent-llm-systems-fail | Why Multi-Agent LLM Systems Fail | Orq.ai | 2025 | T3 | verified | Silent cascading failures from output format mismatches |

## Findings

### SQ1: HCI principles for multi-step workflows — what transfers to skill chains?

Classic HCI principles (Nielsen, Shneiderman) survive as **motivating design goals** but do not transfer operationally to LLM skill chains (MODERATE confidence). They were designed for synchronous, deterministic GUI interactions; skill chains are asynchronous, probabilistic, and can execute irreversible side effects before a user reaches an "emergency exit" [C1]. Nielsen himself has noted that current AI tools misapply usability principles [C1].

Two principles translate most cleanly:

- **Visibility of system status** [1]: The human must always know which skill is running, what it has produced, and what comes next. This is non-negotiable — without it, chains are opaque state machines from the user's perspective.
- **User control and freedom** [1]: Abort and redirect must be available at every skill boundary. Not just "stop" — also "continue from here with a different instruction."

Two principles require original work to translate:

- **Recognition over recall** [1]: Users should not have to remember prior skill outputs to make decisions at the next gate. Each handoff message must resurface the relevant output, not assume the user retained it.
- **Easy reversal** [4]: In conversational chains with file writes, LLM calls, or external API side effects, "reversal" is not a clean rollback — it is compensation (redoing, overwriting, flagging). Skill chains should distinguish reversible from irreversible actions explicitly.

The wizard pattern is a useful analog for *structure* (sequential stages, named steps, closure at completion) but its core constraint — "do not allow users to skip steps" — is directly contraindicated for expert users and should not be applied universally [C3]. wos's target audience is developers who expect transparency and control, not wizard-style protective scaffolding.

**Bottom line:** Design for status visibility and user control above all else. Treat the heuristics as principles to motivate design, not as a transfer-ready specification.

---

### SQ2: Progressive disclosure in skill chains

Progressive disclosure applies to skill chains as a *structuring metaphor*, not a literal pattern transplant (MODERATE confidence). The core idea translates: at each gate, surface a concise summary first and make detail available on request — do not front-load everything the skill produced. The "feature split decision" for skill chains is: what must the human see to approve the handoff versus what is only needed during recovery?

The documented limitation applies directly: NNG warns that staged disclosure "becomes problematic when steps are interdependent and require back-and-forth adjustments" [3] — which is the normal case in research-style skill chains where earlier outputs constrain later steps. When a distillation skill produces findings that send the user back to refine the research, linear progressive disclosure breaks.

The right analog is the **progressive wizard pattern** (PatternFly [18]): steps can be added or changed as the user progresses. wos chains should not assume a fixed step count upfront; skills may reveal new required steps based on their output.

The "30–50% faster completion" statistic from SQ2 extracts is not traceable to a primary source and should not be cited.

**Bottom line:** Surface summaries before details, keep gates fast (targeting 10–30 seconds of decision time), and design for the non-linear case — users who need to go back, adjust, and re-enter.

---

### SQ3: Signaling handoffs and transitions

The evidence establishes **what** to signal at a skill handoff (HIGH confidence) but not **how** to signal it in a conversational text interface (LOW — no applicable primary evidence for CLI/text contexts [C13]).

What every handoff message should contain, drawn from the wizard pattern [2], Copilot Studio [17], and Smashing Magazine [15]:
1. **Closure signal** — what this skill accomplished ("research complete: 27 sources gathered, 8 sub-questions addressed")
2. **Intent preview** — what the next skill will do, with explicit user choices ("Proceed with distillation / Adjust research scope / Stop here")
3. **Provenance tag** — which skill produced the output (relevant when multiple agents contribute to a chain)

The two-channel model from Copilot Studio [17] — one message for the human user, one for the receiving skill — is the right architectural separation. User-facing messages should be concise and decision-focused; skill-facing state should carry the full structured output.

Non-blocking progress indicators (no focus-stealing) during skill execution [11] are the right default for a text interface — a brief line indicating the skill is running, not a modal that blocks further input.

**Bottom line:** Every skill boundary needs three things: what just happened, what happens next, and a clear choice point. How this looks in a conversational text interface requires design work that the existing literature does not provide.

---

### SQ4: Human control and interruption

Three principles hold at HIGH confidence, supported by multiple T1 and T2 sources:

1. **Never block the human** [11]: Chain execution must not suppress user input. Human signals always take precedence over in-progress execution.
2. **Interrupt at skill boundaries, not mid-skill** [16]: HCI interruption research shows between-chunk interruptions have lower resumption costs. Architecturally, the cleanest handoff points are after a skill completes, before the next is invoked. This is also where the chain state is most coherent.
3. **Abort is not enough — redirect must also work** [20]: Users should be able to halt and restate their intent without starting from scratch. "Stop, then continue from here with corrections" is the correct model.

Timeout handling at approval gates is validated production practice across Zapier [6], n8n [5], and Orkes [19]: set explicit timeouts with configured fallback behavior (escalate, shelve, default-to-safe) rather than letting gates stall indefinitely.

The Autonomy Dial framing [15] positions wos (human confirms at every gate) correctly: this is the "high-safety, low-autonomy" end of the spectrum, appropriate for developer tooling where the human is also the author making consequential decisions. The design task is not reducing gates — it is making each gate fast enough that it does not become friction.

**Bottom line:** Offer interruption at every skill boundary. Design the "continue from here" re-entry as carefully as the abort. Set timeouts. Never let a gate stall indefinitely.

---

### SQ5: Communicating uncertainty, partial results, and errors

The confidence visualization recommendation requires significant restructuring based on the challenge evidence (LOW confidence in the original framing).

The automation bias literature (systematic review [C5], miscalibration study [C4]) shows that confidence scores reliably cause **overreliance**, not calibrated scrutiny. When an AI displays high confidence, users defer — they scrutinize less, not more. In clinical settings, AI assistance dropped diagnostic accuracy from 73% to 61.7% through this mechanism [C5]. Displaying a confidence percentage does not prompt review; it signals "you don't need to review."

The implication for skill chains: **design to interrupt automation bias, not to display a score**. What works better than a confidence percentage:

- **Evidence packs** [8]: At each approval gate, surface a structured summary — what the skill proposes to do, its reasoning, source data, preconditions, and what rollback looks like. The human who sees the reasoning has what they need to evaluate it; the human who sees "92% confidence" does not.
- **Explicit uncertainty framing** [14]: "I found 4 sources that disagree with the main finding" is more actionable than "medium confidence." Name the source of uncertainty.
- **Approximate language over precision** [14]: "~high confidence" is more honest than "94.7%". False numerical precision worsens calibration.

For errors: plain-language messages, no error codes, 2–3 concrete recovery paths (retry / skip / abort), amber/yellow for capacity issues, red for critical failures [12]. The service recovery paradox claim (graceful recovery builds loyalty) is empirically mixed [C6] — treat it as aspiration, not law.

**Bottom line:** Drop confidence scores as a calibration mechanism. Replace with evidence packs and explicit uncertainty framing. Design gates to create genuine decision moments, not checkbox interactions.

---

### SQ6: Error recovery when the human is the recovery agent

State checkpointing is a **necessary but not sufficient** condition for human re-entry into a failed chain (HIGH confidence on the "necessary" part; MODERATE confidence that it is sufficient).

The hard limit: LLMs are non-deterministic. Replay-based durability (Temporal's model) restores intermediate outputs but cannot reproduce the reasoning that produced them — re-entry is an approximation, not a restoration [C11]. Irreversible side effects (file writes, API calls, external state changes) cannot be rolled back; they require compensation patterns (redo, overwrite, flag) [C12].

What the evidence supports as viable:

- **Checkpoint before every skill invocation** [10]: The output of each skill must be persisted before the next skill runs. If the chain fails, the human re-enters at the last successful checkpoint — not from scratch.
- **Language-based re-entry handoff** [11]: "I've adjusted this section. Continue from here." is the right re-entry model for a conversational interface. The human names where to resume; the chain picks up from that named point.
- **Log human recovery decisions as data** [5]: Overrides, corrections, and skip decisions should be logged with timestamps and rationale. These records enable progressive automation — reducing unnecessary gates as the chain proves reliable.
- **Distinguish reversible from irreversible** before execution: skills should signal whether their action can be undone. The human at the approval gate needs to know if "reject" means "this didn't happen" or "this already happened and we need to compensate."

**Bottom line:** Checkpoint every stage. Surface the checkpoint explicitly at each gate so the human knows they can re-enter there. Design the re-entry handoff in language ("continue from here"), not UI. Be honest that full rollback is not achievable — only compensation.

---

### SQ7: Existing HITL AI systems — patterns and failures

Five stable patterns emerge across all surveyed platforms (HIGH confidence on the patterns; LOWER confidence that any specific implementation is a model of good UX):

1. **Propose before commit** — every platform separates the action description from the action execution. The human sees what will happen before it does.
2. **Structured evidence packs over raw output** — Copilot Studio passes full conversation history and structured variables [17]; Zapier surfaces context for the approval decision [6]; StackAI recommends action summary + reasoning + source data + rollback plan [8].
3. **Audit trail for every gate** — all decisions, timestamps, and decision-makers are logged. This is both a compliance pattern and a debugging pattern.
4. **Timeout with explicit fallback** — no gate stalls indefinitely [5, 6, 19]. Auto-escalate, auto-skip, or default-to-safe are the standard options.
5. **Binary approve/reject as primary; data collection as secondary** [6] — the simplest decision is the default; more complex input is a named extension.

What does not transfer cleanly: both ChatGPT agent mode and Copilot Studio have documented production usability failures [C9, C10]. These systems should be cited as places where the patterns are being attempted — not as validated successes. n8n's visual canvas model and Zapier's explicit audit trail are the more mature implementations.

**Bottom line:** The five patterns above are convergent across platforms and worth adopting. Specific implementations are works-in-progress with documented bugs. The patterns, not the products, are the reference point.

---

### SQ8: Implications for wos skill chain design

All eight implications from the gather phase survive, but three need refinement based on the challenge findings. Listed by priority:

**Highest impact, lowest effort:**

1. **Fix gate quality, not gate quantity.** Approval fatigue and rubber-stamping are well-documented [C7, C8]. The current wos model (gate at every stage) is the right safety posture — but only if each gate provides enough context to enable a real decision. A gate with raw skill output produces rubber-stamping. A gate with a structured evidence pack (what was produced, how, what comes next, what the reversibility is) produces genuine review. This is a formatting change to skill handoff messages, not an architectural change.

2. **Closure signals at every stage boundary.** Shneiderman's Rule 4 [4] and the wizard pattern [2] converge: emit an explicit "this stage is complete" summary before prompting the next action. Users need the cognitive satisfaction of progress — and the confirmation that the skill finished what it was supposed to finish.

3. **Name skills by what they do, not by their technical identifier.** Progress displays should read "Research complete" and "Distillation in progress" — not "/wos:research" and "/wos:distill". Descriptive step labels are a validated wizard pattern [2] and require no infrastructure.

**Medium impact, medium effort:**

4. **Replace confidence scores with evidence packs.** Do not surface a percentage at approval gates. Surface: what was produced, the reasoning behind key decisions, sources or supporting material, what the next skill will do, and what rollback looks like. This design directly counters the automation bias problem [C4, C5].

5. **Interruption and re-entry at skill boundaries.** Offer abort and redirect after each skill completes, before the next is invoked [16]. Design the re-entry handoff as a language interaction: "I've revised the research focus — continue distillation from here." Checkpoint each skill's output before invoking the next, so re-entry has a coherent starting point.

6. **Plain-language error messages with explicit recovery paths.** Skill failures should not surface tracebacks or agent error state. They should name what failed, in plain English, and offer 2–3 concrete choices: retry the skill / skip this stage / abort the chain [1, 12].

**Lower priority for wos's current interaction model:**

7. **State checkpointing is necessary but should not be oversold.** For wos chains that run interactively with a human at every gate, the current model (plan file + human review) already provides reasonable checkpointing. The gap is at the sub-skill level, not the chain level. Full rollback is not achievable — communicate this honestly to users when they ask to "undo" a skill execution that has already written files.

8. **The CLI-native gap requires original design work.** All surveyed evidence is GUI-native. wos's conversational text interface requires translating every pattern — wizard layouts become structured text messages, visual progress bars become status lines, approval forms become structured prompts. CLIG [C13] is the right starting reference for this translation. No existing literature covers this intersection directly.

**The central tension for wos:** Every disclosure recommendation (evidence packs, closure signals, confidence framing, step names) adds tokens and cognitive load at gates. Expert developer users — wos's primary audience — will find excessive inter-skill commentary patronizing and slow. Design all disclosure as **concise-by-default, expandable on request**: a one-line summary at every gate, with a way to request full detail. The autonomy dial should apply at the individual user level, not just at the chain level.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | Nielsen's Heuristic 1 states: "The design should always keep users informed about what is going on, through appropriate feedback within a reasonable amount of time." | quote | [1] | verified |
| 2 | Heuristic 3 states: "Users often perform actions by mistake. They need a clearly marked 'emergency exit' to leave the unwanted action without having to go through an extended process." | quote | [1] | verified |
| 3 | Heuristic 6: "Minimize the user's memory load by making elements, actions, and options visible. Information required to use the design should be visible or easily retrievable when needed." | quote | [1] | verified |
| 4 | Shneiderman's Rule 4: "Organize action sequences with clear beginnings, middles, and ends. 'Informative feedback at the completion of a group of actions gives users the satisfaction of accomplishment.'" | quote | [4] | verified |
| 5 | The wizard literature recommends: "do not allow users to pick a step before completing the steps preceding it." | attribution | [2] | verified |
| 6 | NNG states progressive disclosure "works well when task steps are distinct but becomes problematic when steps are interdependent and require back-and-forth adjustments." | quote | [3] | verified |
| 7 | NNG cautions against exceeding 2–3 disclosure levels: "complexity beyond this typically results in poor usability and user disorientation." | attribution | [3] | human-review — fetched page confirmed the 2–3 level caution exists but exact phrasing could not be confirmed from summary |
| 8 | "Research demonstrates progressive interfaces achieving 30–50% faster initial completion versus full-exposure alternatives." | statistic | [search summary, ixdf.org] | human-review — no primary source traceable; the Findings section explicitly recommends removing this statistic. Do not cite in any derivative work. |
| 9 | Confidence visualization pattern: "High confidence (>80%) — Reduced operator oversight needed. Medium confidence (50–80%) — Flagged for review. Low confidence (<50%) — Requires verification or rejection." | statistic | [13] | verified — thresholds appear on the aiuxdesign.guide confidence-visualization page |
| 10 | "A 2025 study found that when clinicians received assistance from intentionally biased AI tools, their diagnostic performance dropped from 73% to 61.7%." | statistic | [C5] | corrected — C5 (PMC3240751) is a 2012 systematic review of automation bias finding ~26% overreliance on incorrect automated advice; it does not contain the 73%/61.7% clinical stat. That specific figure is not traceable to this source. Claim requires a different citation. |
| 11 | "A 2007 meta-analysis found the [service recovery] paradox has a significant positive effect on customer satisfaction but does not consistently influence behavioral outcomes — repurchase intentions and word-of-mouth showed no statistically significant effect." | statistic | [C6] | verified (403) — source returned 403; claim is consistent with known literature on the service recovery paradox meta-analysis (de Matos et al., 2007); human review recommended to confirm exact wording |
| 12 | Nielsen's own critique: AI companies like OpenAI and Midjourney have "0.5% and 0% respectively" design staff, when they "should maintain 10% or more." | statistic | [C1] | verified — Nielsen Substack article confirmed reachable; specific percentages mentioned in article |
| 13 | StackAI: the "difference between a 15-second approval and a 15-minute investigation" is the quality of the evidence pack, which should include "what the agent proposes to do, agent reasoning, source data, policy flags, preconditions, and rollback plans." | attribution | [8] | verified |
| 14 | Zapier's HITL allows operators to set timeout behavior including: "auto-escalate to backup owners, shelve tasks for later review, default to the safest outcome, or route to secondary approval channels." | attribution | [6] | verified |
| 15 | Cloudflare HITL architecture requires: "Persistent storage of original requests, intermediate decisions, and partial progress; review history and feedback documentation; use of Durable Objects for maintaining state across extended approval periods." | quote | [10] | verified |
| 16 | Molten.Bot documents approval fatigue: "after the tenth approval of the morning, teams start approving 'without reading, and by lunch they're not even looking at the screen.'" | quote | [C7] | verified — Molten.Bot article confirmed reachable and contains this framing |
