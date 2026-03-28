---
name: "Research Methodology for Agent-Driven Workflows"
description: "Layered evaluation, breadth-before-depth discovery, disagreement-as-signal, and three-layer confidence — convergent principles from academic, intelligence, and agent-driven research traditions"
metadata:
  type: reference
  sources:
    - https://www.prisma-statement.org/
    - https://pressbooks.pub/introtocollegeresearch/chapter/the-sift-method/
    - https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html
    - https://arxiv.org/html/2508.12752v1
    - https://arxiv.org/abs/2309.11495
    - https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses
  related:
    - docs/research/research-methodology.md
    - docs/context/llm-capabilities-limitations.md
    - docs/context/tool-design-for-llms.md
---

Three traditions — academic systematic review, intelligence analysis, and agent-driven AI research — developed independently but converge on the same core principles for systematic information gathering. These principles apply directly to agent workflows that gather, evaluate, and synthesize information.

## Breadth Before Depth

All three traditions agree: start with systematic coverage, then narrow. PRISMA requires multiple databases plus supplementary methods. Intelligence methodology demands diverse collection sources. Agent architectures use iterative multi-query pipelines with sequential or tree-based decomposition. The common pattern is casting a wide net first, then pursuing targeted depth based on what the initial sweep reveals.

Citation chaining — recursively following references backward and forward — complements initial search in all traditions. For agents, this translates to iterative query refinement: search, read results, formulate the next query based on gaps.

## Two-Level Evaluation

Source evaluation operates at two distinct levels, and both are necessary.

**Source-level filtering** asks "is this source trustworthy?" Frameworks include SIFT (Stop, Investigate, Find better, Trace) for rapid assessment, CRAAP (Currency, Relevance, Authority, Accuracy, Purpose) for thorough evaluation, and evidence hierarchies that rank research designs by rigor. Agent equivalents include CRAG reflection tokens that score document relevance and quality.

**Claim-level verification** asks "does this source actually say this, and is it correct?" Chain-of-Verification (CoVe) drafts a response, generates verification questions, answers them independently to prevent confirmation bias, then produces a verified output. This catches errors even within trusted sources.

Source filtering reduces noise. Claim verification catches errors that survive filtering. Skipping either level creates blind spots.

## Disagreement as Signal

When sources conflict, the instinct to resolve the conflict quickly is counterproductive. Three approaches handle disagreement:

- **Triangulation** (Denzin) seeks convergence across data sources, methods, investigators, or theories. Convergence from independent sources strengthens confidence.
- **Analysis of Competing Hypotheses** (ACH) works across rather than down — evaluating each piece of evidence against every hypothesis, selecting the one with fewest inconsistencies. This directly counters confirmation bias.
- **Agent conflict resolution** uses fact-level conflict modeling and multi-agent debate to detect contradictions programmatically.

The key principle: surface conflicts for review rather than silently resolving them. Disagreement between independent sources is informative.

## Three-Layer Confidence

No single confidence framework covers all levels of uncertainty. Effective assessment requires three layers:

1. **Source-level** — Is this a reliable source? GRADE assesses certainty across five domains (risk of bias, inconsistency, indirectness, imprecision, publication bias) using four levels (high, moderate, low, very low). Adopted by 110+ organizations.
2. **Claim-level** — Does this source actually support this claim? CoVe-style self-verification and CRAG reflection tokens operate here.
3. **Output-level** — How certain is the synthesized finding? Intelligence analysis contributes explicit uncertainty annotation using calibrated language.

## Circular Sourcing Risk

Triangulation assumes source independence. Web-based research — whether human or agent-driven — risks correlated sources that appear independent but trace to a common origin. Multiple sources citing the same upstream authority do not constitute independent confirmation. Provenance tracking is necessary to detect this failure mode, especially for agents searching the same web index.
