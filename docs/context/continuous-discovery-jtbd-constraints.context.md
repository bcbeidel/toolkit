---
name: Continuous Discovery and JTBD Constraints
description: Continuous discovery (OST, weekly touchpoints) is the gold standard for B2C/B2B-SMB product teams; JTBD has documented failure modes in multi-stakeholder B2B contexts.
type: context
sources:
  - https://arize.com/ai-product-manager-role
  - https://www.productboard.com/blog/ai-evals-for-product-managers/
related:
  - docs/context/design-systems-accessibility-false-confidence.context.md
  - docs/context/ai-pm-eval-lifecycle-and-ownership.context.md
---

# Continuous Discovery and JTBD Constraints

Continuous discovery — using Opportunity Solution Trees (OST) and weekly customer touchpoints — is the current gold standard for product teams with direct customer access. JTBD (Jobs-to-be-Done) is valuable for uncovering unmet needs in early discovery but has well-documented failure modes that disqualify it as a primary framework in multi-stakeholder B2B contexts.

## Continuous Discovery (OST)

Teresa Torres's nine-step OST workflow is the structured operationalization of continuous discovery:

1. Define outcome
2. Map the opportunity space
3. Select a target opportunity
4. Compare 3+ solutions
5. Identify and test the riskiest assumptions

The core cadence — weekly customer touchpoints rather than quarterly research sprints — produces higher-signal insights by keeping the opportunity space continuously mapped rather than periodically snapshoted.

Evidence suggests AI accelerates several synthesis tasks in this workflow: interview clustering, JTBD drafting, and hypothesis generation. However, human judgment on opportunity prioritization remains non-negotiable — AI cannot determine which opportunities matter most to the team's outcome.

**Confidence: MODERATE** — well-documented practitioner adoption. Adoption friction in enterprise B2B, regulated industries, and small teams without dedicated research capacity is real. The framework provides no principled alternative cadence for these constrained contexts.

## JTBD: Strengths and Failure Modes

Job stories ("When [situation], I want [motivation], so I can [outcome]") reframe product decisions away from feature requests toward motivations. This makes JTBD particularly useful for surfacing unmet needs during early discovery, where teams risk anchoring too quickly on requested solutions.

Documented failure modes in B2B contexts are well-established by multiple independent practitioner and analyst sources:

- **Multi-stakeholder divergence**: B2B purchasing involves stakeholders with divergent jobs — procurement, end-users, IT, executives — producing JTBD abstractions too broad to drive decisions. Whose job are you solving?
- **Roadmap disconnect**: JTBD insights routinely fail to connect to roadmaps or KPIs. The motivational framing ("help me feel confident") doesn't translate cleanly to prioritization or success metrics.
- **Over-abstraction**: Jobs articulated at the functional level ("help me get my work done faster") lose the specificity needed to compare or evaluate solutions.

**Confidence: HIGH** — supported by multiple independent practitioner and analyst sources.

## When to Apply Each

| Context | Recommended |
|---------|-------------|
| B2C product with direct user access | Continuous discovery (OST) |
| B2B-SMB with reachable decision-makers | Continuous discovery (OST) |
| Early discovery, unmet needs exploration | JTBD for insight framing |
| Enterprise B2B with procurement layers | JTBD unreliable alone; supplement with stakeholder mapping |
| Regulated industries, infrequent customer access | Neither framework as prescribed; adapt cadence to access reality |

## Takeaway

Continuous discovery is not a framework for all contexts — it requires direct, regular customer access to function as designed. For teams where that access is constrained, the framework provides no principled alternative. JTBD remains useful as a reframing tool in early discovery but should not be relied on as a primary prioritization mechanism in enterprise B2B, where stakeholder divergence produces abstractions that fail to drive decisions.
