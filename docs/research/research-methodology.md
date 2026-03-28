---
name: "Research Methodology for Systematic Information Gathering"
description: "Landscape survey of source discovery strategies, evaluation frameworks, cross-referencing techniques, and confidence assessment — three traditions (academic, intelligence, agent-driven) converge on layered approaches combining source-level filtering with claim-level verification"
metadata:
  type: research
  sources:
    - https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/
    - https://www.prisma-statement.org/
    - https://arxiv.org/html/2508.12752v1
    - https://arxiv.org/html/2503.24047v1
    - https://pressbooks.pub/introtocollegeresearch/chapter/the-sift-method/
    - https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses
    - https://www.cisecurity.org/ms-isac/services/words-of-estimative-probability-analytic-confidences-and-structured-analytic-techniques
    - https://arxiv.org/abs/2309.11495
    - https://pmc.ncbi.nlm.nih.gov/articles/PMC9714985/
    - https://www.scribbr.com/methodology/triangulation/
    - https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html
    - https://arxiv.org/html/2506.18096v1
    - https://pmc.ncbi.nlm.nih.gov/articles/PMC8474097/
  related:
    - docs/research/prompt-engineering.md
    - docs/research/llm-capabilities-limitations.md
    - docs/research/tool-design-for-llms.md
    - docs/context/research-methodology.md
---

## Summary

Three distinct traditions address systematic research methodology — academic information science, intelligence analysis, and agent-driven AI — and they converge on remarkably similar principles despite independent development. This landscape survey identifies the key techniques, frameworks, and patterns across all three.

**Key findings (all HIGH confidence unless noted):**

- **Source discovery** requires systematic breadth followed by targeted depth. PRISMA mandates multiple databases plus supplementary methods [1][2]; agent architectures use iterative multi-query pipelines with sequential or tree-based decomposition [3][12]; citation chaining complements both approaches [13].
- **Source evaluation** operates at two levels: source-level (SIFT, CRAAP, evidence hierarchies) and claim-level (CRAG reflection tokens, CoVe verification). Both are necessary — source filtering reduces noise, claim verification catches errors even in trusted sources [3][5][8].
- **Cross-referencing** addresses source disagreement through convergence-seeking (Denzin triangulation [9][10]), structured divergence analysis (ACH [6][7]), and programmatic conflict detection (FaithfulRAG [3]). Disagreement is a signal, not a problem to suppress.
- **Confidence assessment** needs a layered approach: source-level confidence (GRADE-like criteria [11]), claim-level confidence (CoVe-style verification [8]), and output-level confidence (explicit uncertainty annotation [7]). No single framework covers all three levels.

16 searches across 1 source engine, 160 results found, 18 used. 13 sources verified (all reachable). Source tiers: 2 T1, 1 T2, 7 T3, 1 T4, 2 T5.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7839230/ | PRISMA-S: Reporting Literature Searches in Systematic Reviews | Rethlefsen et al. / Systematic Reviews | 2021 | T3 | verified |
| 2 | https://www.prisma-statement.org/ | PRISMA Statement | PRISMA Group | 2020 | T1 | verified |
| 3 | https://arxiv.org/html/2508.12752v1 | Deep Research: A Survey of Autonomous Research Agents | Multiple authors / arXiv | 2025 | T3 | verified |
| 4 | https://arxiv.org/html/2503.24047v1 | Towards Scientific Intelligence: LLM-based Scientific Agents | Multiple authors / arXiv | 2025 | T3 | verified |
| 5 | https://pressbooks.pub/introtocollegeresearch/chapter/the-sift-method/ | The SIFT Method | Caulfield / Pressbooks | 2024 | T4 | verified |
| 6 | https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses | Analysis of Competing Hypotheses | Wikipedia | 2024 | T5 | verified |
| 7 | https://www.cisecurity.org/ms-isac/services/words-of-estimative-probability-analytic-confidences-and-structured-analytic-techniques | Words of Estimative Probability and SATs | CIS / MS-ISAC | 2023 | T2 | verified |
| 8 | https://arxiv.org/abs/2309.11495 | Chain-of-Verification Reduces Hallucination in LLMs | Dhuliawala et al. / Meta AI | 2023 | T3 | verified |
| 9 | https://pmc.ncbi.nlm.nih.gov/articles/PMC9714985/ | Principles, Scope, and Limitations of Methodological Triangulation | Fusch et al. / PMC | 2022 | T3 | verified |
| 10 | https://www.scribbr.com/methodology/triangulation/ | Triangulation in Research: Guide, Types, Examples | Scribbr | 2023 | T5 | verified |
| 11 | https://www.cdc.gov/acip-grade-handbook/hcp/chapter-7-grade-criteria-determining-certainty-of-evidence/index.html | GRADE Criteria Determining Certainty of Evidence | CDC / ACIP | 2024 | T1 | verified |
| 12 | https://arxiv.org/html/2506.18096v1 | Deep Research Agents: A Systematic Examination And Roadmap | Multiple authors / arXiv | 2025 | T3 | verified |
| 13 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8474097/ | Using citation tracking for systematic literature searching | Haddaway et al. / PMC | 2021 | T3 | verified |

## Findings

### Source Discovery Strategies

Three distinct traditions converge on systematic source discovery, each contributing techniques applicable to agent-driven research.

**Academic systematic review methodology** provides the most rigorous framework. PRISMA-S specifies 16 reporting items for search strategy transparency, requiring documentation of all databases searched, complete search syntax, and reproducibility [1][2]. The dual-column approach — databases/registers plus "other methods" — explicitly acknowledges that formal database search alone is insufficient (HIGH — T1+T3 sources converge). Citation chaining (snowballing) complements database search by recursively following references backward (checking cited works) and forward (finding citing works), and is considered best practice in systematic reviews [13] (HIGH — T3 peer-reviewed).

**Intelligence and OSINT methodology** emphasizes source diversity and collection planning. The intelligence cycle — preparation, collection, processing, analysis — structures the discovery process similarly to PRISMA but adds explicit threat modeling around source contamination and deliberate disinformation (MODERATE — T2 source, not directly confirmed by T1 academic sources).

**Agent-driven approaches** decompose discovery into pipeline stages: planning (question decomposition), query development, web exploration, and synthesis [3][12]. Key innovations include iterative query refinement (searching, reading results, then formulating next query based on what was learned), tree-based planning using MCTS for search space exploration, and entity-centric knowledge stores that capture cross-domain relationships [4] (HIGH — multiple T3 survey papers converge). Sequential and tree-based decomposition strategies represent the primary architectural divide: sequential builds each query on prior results, while tree-based explores multiple paths simultaneously [12].

**Synthesis across traditions:** All three traditions share the principle that a single search strategy is insufficient. PRISMA requires multiple databases plus supplementary methods; intelligence methodology demands diverse collection sources; agent architectures use iterative multi-query pipelines. The common pattern is systematic breadth followed by targeted depth (HIGH — converges across T1, T2, T3 sources).

### Evaluation Frameworks

Four major evaluation frameworks span the spectrum from rapid heuristic to formal systematic assessment.

**SIFT (Stop, Investigate, Find better, Trace)** — developed by Mike Caulfield — provides the fastest evaluation cycle. Lateral reading (going outside the source to check what others say about it) is the core innovation, distinguishing expert fact-checkers from novices who read vertically within a single source [5] (HIGH — T4, Caulfield is the framework originator). SIFT is designed for speed: the "Stop" step prevents reflexive trust, and the whole process can execute in under a minute.

**CRAAP (Currency, Relevance, Authority, Accuracy, Purpose)** — developed by CSU Chico librarians [human-review: attribution uncited] — provides a checklist-based evaluation. Each criterion addresses a different dimension of source quality. CRAAP is more thorough than SIFT but slower and better suited for deliberate evaluation of sources already identified as candidates (MODERATE — no T1-T3 source directly compared SIFT vs CRAAP; assessment based on framework structure).

**Evidence hierarchies** rank research designs by methodological rigor: meta-analyses and systematic reviews at the top, through RCTs and observational studies, down to expert opinion and laboratory studies. This pyramid is well established in medical and health sciences research (HIGH — T1 CDC source confirms, widely adopted). The hierarchy is less directly applicable to non-empirical domains like software engineering or policy analysis.

**Agent-specific evaluation** introduces programmatic source assessment. CRAG (Corrective RAG) uses a lightweight retrieval evaluator to assess document quality and adaptively handle incorrect or irrelevant information [3]. Reflection tokens (ISREL for relevance, ISSUP for evidence support) provide per-document quality signals that parallel human evaluation criteria but execute at machine speed (MODERATE — T3 survey source, specific systems described but not independently validated).

**Synthesis across frameworks:** Traditional frameworks assess the source as a unit; agent evaluation increasingly operates at the claim level. The SIFT/CRAAP tradition asks "is this source trustworthy?" while CRAG and reflection-token approaches ask "does this specific retrieved passage support this specific claim?" Both levels are necessary — source-level filtering reduces noise, claim-level verification catches errors even in trusted sources.

### Cross-Referencing and Triangulation

**Denzin's four types of triangulation** (1978) remain the foundational taxonomy: data triangulation (multiple sources), investigator triangulation (multiple researchers), theory triangulation (multiple interpretive frameworks), and methodological triangulation (multiple methods) [9][10] (HIGH — T3 peer-reviewed, widely cited across research methodology literature). For agent-driven research, data source triangulation is the most directly applicable — seeking the same information from independent sources and checking for convergence.

**Analysis of Competing Hypotheses (ACH)** — developed by Richards Heuer at the CIA — provides a structured cross-referencing technique that works across rather than down a matrix. Instead of gathering evidence for a preferred hypothesis, ACH requires listing all hypotheses and evaluating each piece of evidence against every hypothesis, selecting the one with fewest inconsistencies [6] (MODERATE — T5 Wikipedia source, but well-documented CIA methodology with T2 institutional confirmation from CIS [7]). This approach directly counters confirmation bias by forcing consideration of disconfirming evidence.

**Agent-specific conflict resolution** addresses the challenge of contradictory sources programmatically. FaithfulRAG employs fact-level conflict modeling to detect and resolve contradictions between retrieved documents [3]. Entropy-based decoding adapts generation based on evidence uncertainty. Multi-agent debate architectures assign different agents to generate hypotheses, perform critical reflection, and rank ideas [4] (MODERATE — T3 survey sources, specific systems described).

**Synthesis across approaches:** Triangulation, ACH, and agent conflict resolution all address the same core problem — what to do when sources disagree. Traditional triangulation seeks convergence; ACH systematically evaluates divergence; agent systems attempt automated conflict detection. The key insight for agent pipelines is that disagreement between sources is a signal, not a problem to suppress. Systems should surface conflicts for human review rather than silently resolving them.

### Confidence Assessment

**GRADE (Grading of Recommendations, Assessment, Development, and Evaluation)** is the most widely adopted formal confidence framework, used by 110+ organizations including WHO and CDC [11]. It assesses certainty across five downgrading domains: risk of bias, inconsistency, indirectness, imprecision, and publication bias. Four certainty levels (high, moderate, low, very low) replace earlier numeric scales. GRADE-CERQual extends this to qualitative evidence with components for methodological limitations, coherence, adequacy, and relevance (HIGH — T1 official CDC source).

**Intelligence community confidence levels** map to three tiers: high (high-quality information, solid judgment possible), moderate (credibly sourced and plausible but insufficient quality/corroboration), low (scant, questionable, fragmented, or poorly corroborated information) [7]. Key determinants include: use of structured method, source reliability, source corroboration, level of expertise, peer collaboration, task complexity, and time pressure (HIGH — T2 institutional source).

**Chain-of-Verification (CoVe)** provides an LLM-specific confidence mechanism: draft a response, generate verification questions, answer them independently (preventing confirmation bias), then produce a verified final response [8]. CoVe decreases hallucinations across a variety of tasks [unverifiable: full paper comparison details not accessible via abstract page] but cannot fully eliminate them, particularly in reasoning steps (HIGH — T3 peer-reviewed, ACL 2024).

**Scientific agent validation** uses domain-specific mechanisms: statistical error bounds, process supervision (quantum-chemical feedback in ChemReasoner), multi-agent peer review, and simulation-based validation with gradient feedback [4] (MODERATE — T3 survey, describes multiple specific systems).

**Synthesis across approaches:** GRADE and intelligence confidence levels converge on similar scales (high/moderate/low) but derive them differently — GRADE from formal evidence quality criteria, intelligence analysis from source reliability and corroboration. CoVe adds a self-verification layer specific to LLM outputs. For agent-driven research, a layered approach is indicated: source-level confidence (via GRADE-like criteria), claim-level confidence (via CoVe-style verification), and output-level confidence (annotating findings with explicit uncertainty). No single framework covers all three levels adequately.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "PRISMA-S specifies 16 reporting items for search strategy transparency" | statistic | [1] | verified |
| 2 | "SIFT developed by Mike Caulfield" | attribution | [5] | verified |
| 3 | "CRAAP developed by librarians at CSU Chico" | attribution | — | human-review |
| 4 | "Denzin's four types of triangulation (1978)" | attribution | [9][10] | verified |
| 5 | "ACH developed by Richards Heuer at the CIA in the 1970s" | attribution | [6] | verified |
| 6 | "GRADE adopted by 110+ organizations including WHO and CDC" | statistic | [11] | verified |
| 7 | "CoVe outperforms zero-shot, few-shot, and chain-of-thought approaches" | superlative | [8] | unverifiable |
| 8 | "GRADE assesses certainty across five downgrading domains" | attribution | [11] | verified |
| 9 | "GRADE uses four certainty levels: high, moderate, low, very low" | attribution | [11] | verified |

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| Traditional research frameworks (PRISMA, SIFT, GRADE) transfer meaningfully to agent-driven workflows | Deep research agents use analogous phases: query decomposition parallels systematic search strategy [3][12]; CRAG evaluation mirrors SIFT-style source assessment [3] | These frameworks were designed for human cognitive limitations (anchoring bias, confirmation bias); agents have different failure modes (hallucination, context window limits) | HIGH — would mean agent pipelines need fundamentally different methodology rather than adapted human frameworks |
| Source tiering is the primary quality signal | GRADE, evidence hierarchies, and SIFT all converge on source classification as central [1][2][5][11] | Agent systems increasingly use content-level verification (CRAG reflection tokens, CoVe fact-checking) rather than source-level trust [3][8]; source tier says nothing about whether a specific claim within that source is accurate | MODERATE — tiering remains useful for prioritization but insufficient as sole quality measure for agents |
| Cross-referencing via triangulation produces reliable validation | Denzin's framework widely adopted [9][10]; intelligence analysis emphasizes corroboration [7] | Circular sourcing — multiple sources may trace to a single origin; corroboration count can be inflated by shared misinformation; agents searching the same web index get correlated results | MODERATE — triangulation needs augmentation with provenance tracking to detect circular sourcing |
| Confidence scales (HIGH/MODERATE/LOW) meaningfully communicate uncertainty | GRADE and intelligence community both use similar scales, adopted by 110+ organizations [7][11] | Three-level scales collapse rich uncertainty distributions; "moderate confidence" spans a wide range of actual certainty; LLM-generated confidence labels may not calibrate to actual reliability | LOW — scales are useful communication tools but should not be confused with calibrated probabilities |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| The landscape omits non-Western research methodology traditions (e.g., participatory action research, indigenous knowledge validation) that may offer techniques not captured by PRISMA/SIFT/GRADE | Medium | Qualifies breadth claim — findings reflect English-language, Western institutional approaches primarily |
| Agent-driven research is evolving so rapidly that the 2025 survey papers may not reflect production practices by the time this document is referenced | High | Qualifies currency of agent-specific findings; the traditional frameworks (PRISMA, GRADE, Denzin) remain stable |
| Overemphasis on formal frameworks may miss that effective research in practice relies heavily on tacit expertise and heuristic judgment that resists formalization | Medium | Qualifies applicability — formalized frameworks are necessary but not sufficient; agent pipelines need to account for judgment gaps |

## Key Takeaways

1. **Layer your evaluation.** Source-level filtering (SIFT/tiering) and claim-level verification (CoVe/CRAG) address different failure modes. Use both.

2. **Treat disagreement as signal.** When sources conflict, surface it rather than suppress it. ACH's "work across" approach — evaluating each piece of evidence against all hypotheses — is directly implementable in agent workflows.

3. **Breadth before depth.** All three traditions agree: start with systematic coverage, then narrow. PRISMA's dual-column approach, OSINT's diverse collection, and agent iterative decomposition all embody this principle.

4. **Confidence needs three layers.** Source-level (is this a reliable source?), claim-level (does this source actually say this?), and output-level (how certain is the synthesized finding?). GRADE addresses the first, CoVe the second, intelligence analysis the third — but no single framework spans all three.

5. **Watch for circular sourcing.** Triangulation assumes source independence. Web-based research — whether human or agent-driven — risks correlated sources that appear independent but trace to a common origin.

## Limitations

- Coverage limited to English-language, Western institutional methodology traditions
- Agent-specific findings based on 2025 survey papers; the field is evolving rapidly
- CRAAP test attribution uncited (human-review); CoVe baseline comparison details inaccessible (unverifiable)
- WebFetch access was intermittently denied during this research; some source extracts relied on search result summaries rather than direct full-text extraction
- Not searched: Scopus, Web of Science, Google Scholar, Semantic Scholar, ACM Digital Library, IEEE Xplore

## Follow-ups

- Investigate calibration research: do LLM-generated confidence labels correlate with actual accuracy?
- Survey non-Western research methodology traditions for techniques absent from this landscape
- Evaluate CRAG and reflection token approaches in practice — how do they perform outside controlled benchmarks?
- Research provenance tracking techniques that detect circular sourcing in web-based triangulation

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| systematic information gathering source discovery strategies research methodology | google | all | 10 | 1 |
| PRISMA systematic review search strategy source identification methods | google | all | 10 | 2 |
| LLM agent research automation source discovery techniques 2024 2025 | google | 2024-2025 | 10 | 3 |
| SIFT framework source evaluation Mike Caulfield lateral reading methodology | google | all | 10 | 1 |
| CRAAP test source evaluation framework criteria academic research | google | all | 10 | 1 |
| information triangulation cross-referencing techniques research validation multiple sources | google | all | 10 | 2 |
| confidence assessment framework research findings certainty grading evidence quality GRADE | google | all | 10 | 1 |
| intelligence analysis structured analytic techniques confidence levels assessment | google | all | 10 | 2 |
| OSINT open source intelligence methodology source verification collection techniques | google | all | 10 | 0 |
| evidence hierarchy levels of evidence research pyramid primary secondary sources | google | all | 10 | 0 |
| retrieval augmented generation RAG source quality evaluation verification techniques 2024 2025 | google | 2024-2025 | 10 | 0 |
| Denzin triangulation types data source methodological investigator theory 1978 | google | all | 10 | 1 |
| analysis of competing hypotheses ACH Heuer intelligence structured analytic technique | google | all | 10 | 1 |
| chain of verification LLM hallucination detection factual accuracy self-verification | google | all | 10 | 1 |
| snowball sampling citation chaining reference tracking academic literature search technique | google | all | 10 | 1 |
| deep research AI agent iterative search refinement query decomposition 2025 | google | 2025 | 10 | 1 |

16 searches across 1 source engine, 160 found, 18 used.
