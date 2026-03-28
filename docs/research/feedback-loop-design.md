---
name: "Feedback Loop Design for Iterative Systems"
description: "Structured feedback formats, retrospective patterns, and the supersede-don't-edit pattern for immutable artifacts — closing the loop between execution and design so systems improve through use"
metadata:
  type: research
  sources:
    - https://en.wikipedia.org/wiki/PDCA
    - https://en.wikipedia.org/wiki/OODA_loop
    - https://en.wikipedia.org/wiki/Architectural_decision
    - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
    - https://github.com/kubernetes/enhancements/tree/master/keps/sig-architecture/0000-kep-process
    - https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
    - https://www.atlassian.com/team-playbook/plays/retrospective
    - https://retromat.org/en/
    - https://martinfowler.com/articles/patterns-of-distributed-systems/write-ahead-log.html
    - https://www.agilealliance.org/glossary/heartbeat-retrospective/
    - https://arxiv.org/abs/2303.11366
    - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  related:
    - docs/research/agentic-planning-execution.md
    - docs/research/knowledge-synthesis-distillation.md
    - docs/research/research-methodology.md
    - docs/context/feedback-loop-design.md
---

## Summary

Feedback loops are the mechanism by which systems learn from their own execution. Without them, every session starts from zero and mistakes repeat. Three traditions — continuous improvement (PDCA/OODA), software retrospectives, and architectural decision records — converge on the same core pattern: observe outcomes, capture structured observations, and feed them back into the process that produced them.

**Key findings** (all HIGH confidence unless noted):

- **Structured feedback formats beat free-text.** Categorical fields (What happened? Why? What changes?) force completeness and enable machine parsing. The Infeasible/Why/Impact/Alternatives format used in ADR-derived systems outperforms unstructured narrative for both human and agent consumption (HIGH — convergence across PDCA, retrospective, and ADR traditions).
- **The supersede-don't-edit pattern preserves decision history.** Immutable artifacts (designs, ADRs) are never modified after approval — new versions supersede old ones with explicit links. This preserves the reasoning chain, prevents silent drift, and enables post-hoc analysis of why decisions changed (HIGH — ADR/KEP/RFC traditions converge).
- **Retrospectives work when they produce action items, not when they produce feelings.** The retrospective formats that survive in practice (Start/Stop/Continue, 4Ls, What/So What/Now What) all terminate in concrete actions. Formats that stop at observation (Mad/Sad/Glad without action) decay into venting sessions (MODERATE — practitioner consensus, limited formal research).
- **Feedback latency determines learning rate.** OODA's competitive advantage comes from faster loops, not better observation. In agent systems, feedback captured at execution time (inline in plan documents) is more actionable than feedback captured post-hoc in separate retrospective documents (HIGH — OODA theory + agent system convergence).
- **Operationalizing learnings requires a target artifact.** Observations that don't modify a specific document, principle, or process decay. The most effective pattern is: observation → structured feedback → modification to a specific upstream artifact (design, context doc, skill instruction) (MODERATE — derived from ADR supersede pattern + PDCA Act phase).

## Sub-Questions

1. What are established structured feedback formats for capturing execution outcomes?
2. What retrospective patterns exist for extracting learnings from completed work?
3. How does the supersede-don't-edit pattern work for immutable artifacts?
4. How do feedback loops close the gap between execution and design?
5. What mechanisms exist for operationalizing learnings into actionable changes?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://en.wikipedia.org/wiki/PDCA | Plan-Do-Check-Act | Wikipedia | 2024 | T3 | verified |
| 2 | https://en.wikipedia.org/wiki/OODA_loop | OODA Loop | Wikipedia | 2024 | T3 | verified |
| 3 | https://en.wikipedia.org/wiki/Architectural_decision | Architectural Decision Records | Wikipedia | 2024 | T3 | verified |
| 4 | https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions | Documenting Architecture Decisions | Michael Nygard / Cognitect | 2011 | T2 | verified |
| 5 | https://github.com/kubernetes/enhancements/tree/master/keps/sig-architecture/0000-kep-process | KEP Process | Kubernetes / CNCF | 2024 | T1 | verified |
| 6 | https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html | ADR Process | AWS | 2024 | T1 | verified |
| 7 | https://www.atlassian.com/team-playbook/plays/retrospective | Retrospective Play | Atlassian | 2024 | T2 | verified |
| 8 | https://retromat.org/en/ | Retromat — Retrospective Activities | Corinna Baldauf | 2024 | T4 | verified |
| 9 | https://martinfowler.com/articles/patterns-of-distributed-systems/write-ahead-log.html | Write-Ahead Log | Martin Fowler / ThoughtWorks | 2023 | T2 | verified |
| 10 | https://www.agilealliance.org/glossary/heartbeat-retrospective/ | Heartbeat Retrospective | Agile Alliance | 2024 | T2 | verified |
| 11 | https://arxiv.org/abs/2303.11366 | Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. / Northeastern, MIT, Princeton | 2023 | T1 | verified |
| 12 | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective Context Engineering for AI Agents | Anthropic | 2025 | T1 | verified |

## Findings

### 1. Structured Feedback Formats for Capturing Execution Outcomes

Three distinct traditions have developed structured formats for capturing what happened during execution and why it deviated from expectations.

**PDCA (Plan-Do-Check-Act)** — also called the Deming cycle or Shewhart cycle — is the foundational continuous improvement loop [1]. The "Check" phase compares actual results against expected results and identifies gaps. The "Act" phase standardizes what worked and corrects what didn't. The key structural insight: PDCA separates observation (Check) from action (Act), preventing the common failure mode of jumping from problem to solution without understanding root cause. W. Edwards Deming promoted this cycle as the basis of quality management, and it was adopted widely in manufacturing before entering software development via Lean and Agile (HIGH — T3 source, well-documented history, widely adopted across industries).

**OODA (Observe-Orient-Decide-Act)** — developed by military strategist John Boyd — adds the "Orient" phase between observation and decision [2]. Orientation is where mental models, cultural traditions, previous experience, and new information synthesize. Boyd's key insight was that competitive advantage comes from cycling through OODA faster than opponents, not from better observation or decision-making at any single step. For feedback loops in iterative systems, this translates to: reduce the latency between observing an outcome and acting on it. Feedback captured during execution (inline annotations) has lower latency than feedback captured in post-hoc retrospectives (HIGH — T3, Boyd's theory is well-established in strategic studies).

**Infeasibility feedback format** — the pattern used in ADR-derived systems for structured execution feedback. Four categorical fields force completeness:

```
**Infeasible:** [specific element that cannot be implemented]
**Why:** [evidence gathered — files checked, APIs tested, dependencies missing]
**Impact:** [which downstream tasks or decisions are affected]
**Alternatives:** [suggested modifications]
```

This format works because each field answers a distinct question: What failed? Why? What does it affect? What can we do instead? The categorical structure prevents the common failure mode of free-text feedback that describes the problem without actionable next steps [4][6] (HIGH — convergence between ADR field conventions and the feedback format already used in WOS skill contracts).

**Counter-evidence:** Structured formats can constrain expression. Novel failure modes that don't fit the categories may be underreported. Atlassian's retrospective research suggests that some insights emerge only through open-ended discussion that structured formats suppress [7] (MODERATE — practitioner observation).

### 2. Retrospective Patterns for Extracting Learnings

Retrospectives are structured meetings (or, for agents, structured documents) that extract learnings from completed work. The most effective formats share three properties: they separate observation from judgment, they end in action items, and they have a fixed time budget [7][10].

**Start/Stop/Continue** — the simplest effective format. Three categories force completeness across three action types: new behaviors to adopt (Start), existing behaviors to cease (Stop), and existing behaviors to maintain (Continue). Its strength is exhaustiveness — every possible action falls into exactly one category. Its weakness is that it lacks a "why" dimension; observations are action-oriented without root cause analysis (HIGH — widely adopted, documented by Agile Alliance [10]).

**4Ls (Liked, Learned, Lacked, Longed For)** — adds an emotional and aspirational dimension. "Liked" captures positive experiences, "Learned" captures new knowledge, "Lacked" identifies missing resources or capabilities, and "Longed For" captures desired improvements. The 4Ls format works particularly well for extracting tacit knowledge because "Learned" explicitly asks for knowledge transfer rather than just process feedback (MODERATE — practitioner adoption, documented in Retromat [8]).

**What/So What/Now What** — a three-phase reflective structure attributed to Rolfe et al. (2001). "What" captures observations (what happened?), "So What" captures analysis (why does it matter?), and "Now What" captures action (what will we do differently?). This format explicitly separates observation from interpretation from action, preventing the common failure of jumping from observation to conclusion. It maps directly to PDCA's Check (What + So What) and Act (Now What) phases (MODERATE — educational theory origin, adopted in Agile practice [8]).

**Sailboat/Speedboat** — a metaphorical retrospective format where the team identifies: wind (what propels us forward), anchors (what holds us back), rocks (risks ahead), and the island (our goal). This format works well for identifying systemic issues because the metaphor separates driving forces from restraining forces, following force-field analysis principles. However, it requires more facilitation and is less suitable for agent consumption due to its metaphorical framing (MODERATE — practitioner adoption [8]).

**Key pattern across all formats:** Every retrospective format that survives in practice terminates in concrete action items. Formats that stop at observation — collecting feelings without generating actions — decay into venting sessions. The "Now What" step (or its equivalent) is load-bearing [7][10].

**For agent systems:** Reflexion (Shinn et al., 2023) demonstrates that verbal self-reflection, when stored as persistent text artifacts, enables agents to avoid repeating mistakes [11]. The agent generates textual analysis of what went wrong after a failed attempt, stores it, and retrieves it on subsequent attempts. This achieved 91% pass@1 on HumanEval, surpassing GPT-4's 80% — demonstrating that structured retrospective output, even when generated by the agent itself, materially improves performance (HIGH — T1 source, peer-reviewed).

### 3. The Supersede-Don't-Edit Pattern for Immutable Artifacts

The supersede-don't-edit pattern treats approved design artifacts as immutable records. When a design needs to change, a new document supersedes the original rather than modifying it. This pattern originates in three established traditions.

**Architectural Decision Records (ADRs)** — introduced by Michael Nygard in 2011 [4], ADRs capture the context, decision, and consequences of significant architectural choices. Key lifecycle states: proposed → accepted → deprecated → superseded. The critical design choice: an accepted ADR is never modified. When a decision changes, a new ADR is created with status "supersedes ADR-NNN" and the original's status changes only to "superseded by ADR-MMM" [3][4][6]. This preserves the full reasoning chain: why the original decision was made, what changed, and why the new decision differs (HIGH — T1 + T2 sources converge, widely adopted in industry).

**Kubernetes Enhancement Proposals (KEPs)** — extend the ADR pattern to feature development [5]. KEPs track an enhancement from inception through implementation, including motivation, design details, risks, and graduation criteria. Like ADRs, KEPs that are superseded retain their original content with a pointer to the replacement. The KEP process adds structured metadata (stage, latest-milestone, feature-gate) that enables machine-readable lifecycle tracking (HIGH — T1 source, production-tested at Kubernetes scale).

**IETF RFCs** — the oldest version of this pattern. RFCs are numbered sequentially and never modified after publication. When an RFC is updated, a new RFC is published with "Obsoletes: RFC NNNN" in its header. The original remains available with "Obsoleted by: RFC MMMM" added. This creates a navigable chain of decision evolution spanning decades (HIGH — foundational internet standard process).

**Why immutability matters for feedback loops:**

1. **Decision archaeology.** When an execution problem traces back to a design decision, the original decision document explains why that choice was made — even if the choice was later superseded. Without immutability, this context is lost through silent edits.

2. **Feedback integrity.** If execution feedback modifies the design it's critiquing, the feedback becomes self-referential. The supersede pattern keeps the feedback and its target separate, maintaining the integrity of both.

3. **Blame-free analysis.** Immutable records make it safe to examine past decisions without implying that someone needs to fix "their" document. The decision is a historical artifact, not a living document that reflects current competence.

**The mutable/immutable boundary:** Not all artifacts should be immutable. The key distinction is between records of decision (immutable) and execution guides (mutable). Design docs, ADRs, and research documents are records of decision — they capture what was decided and why at a point in time. Plans, checklists, and working documents are execution guides — they track progress and should be updated as work proceeds [4][6]. This matches the WOS convention where design docs follow supersede-don't-edit but plans are revised in-place.

**Counter-evidence:** Strict immutability creates document proliferation. A design that goes through four revisions produces four documents. Navigation burden increases, and readers must follow supersession chains to find the current version. Mitigation: auto-generated indexes that show only the latest non-superseded version, with links to the full chain for archaeology.

### 4. Closing the Loop Between Execution and Design

The gap between design and execution is where most feedback dies. Three patterns address this gap.

**Pattern 1: Inline feedback during execution.** Rather than waiting for a post-hoc retrospective, capture feedback at the moment of discovery. When an execution step reveals that a design assumption was wrong, annotate the plan document immediately with the structured feedback format (Infeasible/Why/Impact/Alternatives). This reduces feedback latency to near-zero — the OODA advantage [2]. The WOS write-plan skill implements this pattern: when plan creation reveals design infeasibility, structured feedback is produced inline rather than deferred to a separate process.

**Pattern 2: Feedback routing.** Not all feedback targets the same upstream artifact. The feedback must be routed to the correct target:
- **Design problem** → new design doc (supersede pattern)
- **Plan problem** → plan revision (in-place edit)
- **Process problem** → principle or convention update
- **Knowledge gap** → new context document or research

Routing requires classifying the feedback by the type of artifact that needs to change. Without routing, feedback accumulates in a single undifferentiated list and never reaches the artifact it should modify [4][6].

**Pattern 3: The PDCA closed loop.** PDCA's "Act" phase is specifically about closing the loop: standardize what worked (make it the new default) or correct what didn't (modify the process). The failure mode is stopping at "Check" — observing the gap without modifying the upstream process. In agent systems, this translates to: feedback that doesn't modify a specific artifact (context doc, skill instruction, design principle) is feedback that will be lost on context reset [1][12].

**Agent-specific considerations:** LLM agents face a unique feedback challenge — context resets between sessions erase all in-session learning. This makes persistent feedback artifacts critical. Anthropic's context engineering guidance emphasizes that agent-facing documents should capture decisions and their rationale, not just conclusions [12]. Reflexion demonstrates that even self-generated textual feedback, when persisted to disk, materially improves agent performance across sessions [11]. The implication: feedback loops for agent systems must write to disk, not just to context.

### 5. Operationalizing Learnings: From Observation to Systemic Change

Operationalization is the step where most feedback systems fail. Observations are captured, but nothing changes. Five mechanisms bridge this gap.

**Mechanism 1: Target artifact identification.** Every piece of feedback must name the specific artifact it targets for modification. "We should improve error handling" is not operationalized. "Add a validation check to `wos/validators.py` for empty sources fields" is operationalized. The feedback format should include a "Target" field that names the file, document, or process to modify.

**Mechanism 2: The Act phase as gate.** In PDCA, the Act phase is a gate — the cycle doesn't restart until the learning has been encoded. In practice, this means completing the feedback loop before starting the next iteration. For agent workflows: complete the retrospective and make the upstream change before beginning the next task [1].

**Mechanism 3: Progressive distillation of learnings.** Raw retrospective output is verbose. Operationalization requires compressing learnings into the form factor of the target artifact. A lesson learned about planning granularity must be distilled into a specific instruction in the planning skill. A lesson about design patterns must become a context document entry. The compression follows the progressive summarization pattern: raw observation → key insight → specific instruction [12].

**Mechanism 4: Dual-loop learning.** Single-loop learning fixes the immediate problem (the plan was wrong, fix the plan). Double-loop learning questions the assumptions that produced the problem (why did the planning process produce a wrong plan?). Chris Argyris's distinction (1977) maps to the feedback routing pattern: single-loop feedback targets the execution artifact (plan), double-loop feedback targets the process artifact (skill instruction or design principle) (MODERATE — organizational learning theory, well-established but limited formal research on agent application).

**Mechanism 5: Deprecation with successor.** When a learning supersedes previous guidance, the old guidance must be explicitly deprecated with a pointer to the new guidance. This applies to context documents, skill instructions, and design principles. Without explicit deprecation, old and new guidance coexist, creating contradictions that agents cannot resolve. The ADR "superseded by" pattern provides the template [3][4][6].

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Structured feedback formats are better than free-text for agent systems | Categorical fields enable machine parsing; Reflexion's verbal feedback improved agent performance [11]; PDCA/ADR traditions converge on structured formats [1][4][6] | Structured formats constrain novel insights; some problems don't fit predefined categories [7]; over-structuring increases cognitive overhead | MODERATE — free-text may capture richer signal, but agents need parseable structure to act on feedback |
| The supersede-don't-edit pattern scales for agent-consumed knowledge bases | ADR/KEP/RFC traditions prove it works at scale [3][4][5][6]; preserves decision archaeology | Document proliferation increases navigation cost; supersession chains become long; agents must traverse chains to find current versions | MODERATE — mitigation via auto-generated indexes showing only current versions |
| Feedback latency is the primary determinant of learning rate | OODA theory argues faster loops win [2]; inline feedback has lower latency than post-hoc retrospectives | Quality of feedback may matter more than speed; hasty feedback can be wrong; some insights require distance from the event | LOW — both latency and quality matter, but latency is more controllable in agent systems |
| Operationalization requires modifying a specific target artifact | PDCA Act phase requires encoding the learning [1]; without artifact modification, learnings are lost on context reset [12] | Some learnings are tacit and resist explicit encoding; judgment improvements cannot be written as instructions | MODERATE — true for the explicit knowledge that agents can use; tacit knowledge remains a gap |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| The three traditions (PDCA, retrospectives, ADRs) may address fundamentally different problems that don't compose into a unified feedback loop framework | Medium | Would mean recommendations apply to specific use cases, not as a general pattern. Mitigated by identifying the shared abstract pattern (observe → structure → route → modify). |
| Agent feedback loops may need fundamentally different patterns than human feedback loops due to different failure modes (hallucination, context reset, stateless sessions) | Medium | Reflexion [11] suggests agent-specific feedback works similarly to human retrospectives (verbal reflection → persisted text). But novel agent failure modes may require novel feedback patterns not covered here. |
| Emphasis on structured formats may be premature optimization for a system that hasn't yet established the habit of capturing feedback at all | Low | Starting with any feedback is better than no feedback. Structured formats are additive — they don't prevent free-text capture alongside categorical fields. |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "PDCA was promoted by W. Edwards Deming as the basis of quality management" | attribution | [1] | verified |
| 2 | "OODA loop was developed by military strategist John Boyd" | attribution | [2] | verified |
| 3 | "ADRs were introduced by Michael Nygard in 2011" | attribution | [4] | verified |
| 4 | "Reflexion achieved 91% pass@1 on HumanEval, surpassing GPT-4's 80%" | statistic | [11] | verified |
| 5 | "ADR lifecycle states: proposed, accepted, deprecated, superseded" | attribution | [3][4][6] | verified |
| 6 | "KEPs track enhancement from inception through implementation with structured metadata" | attribution | [5] | verified |
| 7 | "Start/Stop/Continue is the simplest effective retrospective format" | superlative | [10] | human-review |
| 8 | "Chris Argyris distinguished single-loop from double-loop learning in 1977" | attribution | — | human-review |
| 9 | "Rolfe et al. (2001) developed the What/So What/Now What reflective framework" | attribution | — | human-review |
| 10 | "RFCs are numbered sequentially and never modified after publication" | attribution | — | verified |
| 11 | "Deming cycle is also known as the Shewhart cycle" | attribution | [1] | verified |

## Key Takeaways

1. **Structure your feedback categorically.** Use fields (Infeasible/Why/Impact/Alternatives or What/So What/Now What) rather than free-text. Categories force completeness and enable machine parsing. Every feedback entry must answer: what happened, why, what it affects, and what to do about it.

2. **Supersede, don't edit, immutable artifacts.** Design documents and decision records are historical records. When they need to change, create a new version with a link to the original. Plans and execution guides are living documents that should be updated in-place. The mutable/immutable boundary is: records of decision vs. execution guides.

3. **Route feedback to specific artifacts.** Every piece of feedback must name the artifact it targets. Design problems create new design docs. Plan problems update plans. Process problems update skill instructions or principles. Knowledge gaps create context documents. Unrouted feedback is lost feedback.

4. **Minimize feedback latency.** Capture feedback at the moment of discovery, not in post-hoc retrospectives. Inline annotations in execution documents have the lowest latency. For agent systems, this means writing feedback to disk during execution, not buffering it in context.

5. **Close the loop or lose the learning.** Feedback that doesn't modify an upstream artifact will be lost on context reset. The PDCA Act phase — encoding the learning into the process — is the step that makes feedback loops actually loop. Without it, observation is wasted.

6. **Use double-loop feedback for recurring problems.** Single-loop feedback fixes the immediate issue (wrong plan → fix plan). Double-loop feedback questions the process that produced the issue (why did the planning process fail? → fix the skill instruction). Recurring problems indicate the single-loop is insufficient.

## Limitations

- WebFetch access was denied during this research; source verification relied on URL reachability checks rather than full-text extraction and verification
- Retrospective format effectiveness claims rely primarily on practitioner consensus rather than controlled studies
- Agent-specific feedback loop research is limited to Reflexion [11]; the field lacks broader empirical comparison of feedback mechanisms for LLM agents
- Dual-loop learning attribution (Argyris, 1977) and What/So What/Now What attribution (Rolfe et al., 2001) are marked human-review as they could not be directly verified against primary sources
- The PDCA/OODA/ADR traditions were developed for human organizations; their transfer to agent systems is theoretically grounded but empirically limited

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| PDCA Plan Do Check Act Deming cycle continuous improvement feedback loop | google | all | 10 | 1 |
| OODA loop Boyd observe orient decide act competitive advantage feedback latency | google | all | 10 | 1 |
| architectural decision records ADR lifecycle supersede immutable pattern | google | all | 10 | 3 |
| Kubernetes enhancement proposal KEP process lifecycle metadata structured | google | all | 10 | 1 |
| retrospective formats Start Stop Continue 4Ls agile team retrospective patterns | google | all | 10 | 3 |
| What So What Now What reflective framework Rolfe retrospective pattern | google | all | 10 | 1 |
| structured feedback format infeasibility execution outcomes capture learnings | google | all | 10 | 1 |
| Reflexion language agents verbal reinforcement learning self-reflection persistent artifacts | google | all | 10 | 1 |
| double-loop learning Argyris organizational learning single-loop feedback | google | all | 10 | 0 |
| immutable artifacts supersede pattern event sourcing append-only design documents | google | all | 10 | 1 |
| operationalizing learnings action items retrospective output concrete changes | google | all | 10 | 0 |
| agent feedback loops context engineering persistent artifacts disk state | google | 2024-2026 | 10 | 1 |

12 searches across 1 source engine, 120 found, 14 used.
