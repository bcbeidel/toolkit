---
name: "Feedback Loop Design for Iterative Systems"
description: "Structured feedback formats, the supersede-don't-edit pattern, and operationalization mechanisms that close the loop between execution and design so systems improve through use"
metadata:
  type: reference
  sources:
    - https://en.wikipedia.org/wiki/PDCA
    - https://en.wikipedia.org/wiki/OODA_loop
    - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
    - https://arxiv.org/abs/2303.11366
    - https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
  related:
    - docs/research/feedback-loop-design.md
    - docs/context/agentic-planning-execution.md
    - docs/context/knowledge-synthesis-distillation.md
    - docs/context/agent-state-persistence.md
---

Feedback loops are the mechanism by which iterative systems learn from their own execution. Without them, every session starts from zero and mistakes repeat. Three traditions — continuous improvement (PDCA/OODA), software retrospectives, and architectural decision records — converge on the same core pattern: observe outcomes, capture structured observations, and feed them back into the process that produced them.

## Structured Feedback Over Free-Text

Categorical fields force completeness and enable machine parsing. The Infeasible/Why/Impact/Alternatives format answers four distinct questions: What failed? Why? What does it affect? What can we do instead? This outperforms narrative for both human and agent consumption because each field has a clear purpose and nothing is omitted.

The What/So What/Now What format provides a similar structure for retrospectives: observation, analysis, and action. Every effective retrospective format terminates in concrete action items — formats that stop at observation decay into venting sessions.

## Supersede, Don't Edit

Approved design artifacts are immutable records. When a design needs to change, a new document supersedes the original with an explicit link, rather than modifying it in place. This pattern originates in ADRs (Nygard, 2011), Kubernetes Enhancement Proposals, and IETF RFCs.

Immutability matters for three reasons. First, decision archaeology: when an execution problem traces back to a design decision, the original document explains why that choice was made. Second, feedback integrity: if feedback modifies the artifact it critiques, both become unreliable. Third, blame-free analysis: immutable records make it safe to examine past decisions.

The mutable/immutable boundary: records of decision (designs, ADRs, research) are immutable. Execution guides (plans, checklists) are mutable and updated in place.

## Minimize Feedback Latency

OODA's competitive advantage comes from faster loops, not better observation. Feedback captured during execution (inline annotations in plan documents) is more actionable than feedback captured in post-hoc retrospectives. For agent systems, this means writing feedback to disk at the moment of discovery, not buffering it in context.

## Route Feedback to Specific Artifacts

Every piece of feedback must name the artifact it targets. Without routing, feedback accumulates in an undifferentiated list and never reaches the artifact it should modify:

- **Design problem** — new design doc (supersede pattern)
- **Plan problem** — plan revision (in-place edit)
- **Process problem** — principle or convention update
- **Knowledge gap** — new context document or research

## Operationalize or Lose the Learning

Feedback that doesn't modify an upstream artifact will be lost on context reset. The PDCA Act phase — encoding the learning into the process — is the step that makes feedback loops actually loop. Five mechanisms support this:

1. **Target artifact identification** — every feedback entry names the specific file or process to change
2. **Act phase as gate** — the cycle doesn't restart until the learning is encoded
3. **Progressive distillation** — raw observation is compressed into the form factor of the target artifact
4. **Double-loop learning** — single-loop fixes the immediate issue; double-loop questions the process that produced it
5. **Deprecation with successor** — old guidance is explicitly deprecated with a pointer to the replacement

For agent systems specifically, Reflexion (Shinn et al., 2023) demonstrates that verbal self-reflection stored as persistent text enables agents to avoid repeating mistakes, achieving 91% pass@1 on HumanEval vs. GPT-4's 80%. Persistent feedback artifacts are not optional — they are the mechanism by which agent systems learn across session boundaries.
