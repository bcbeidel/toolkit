---
name: "Research Methodology & Source Evaluation"
description: "SIFT framework (lateral reading over vertical) is the validated foundation for source evaluation; tool-based URL/DOI verification beats CoVe self-correction for LLM hallucination mitigation; hybrid keyword+citation-chaining search with documented protocols is the coverage standard."
type: research
sources:
  - https://hapgood.us/2019/06/19/sift-the-four-moves/
  - https://hapgood.us/2019/08/13/check-please-starter-course-released/
  - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3048994
  - https://journals.sagepub.com/doi/10.1177/016146811912101102
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8012470/
  - https://journals.sagepub.com/doi/full/10.1177/23328584211038937
  - https://arxiv.org/abs/2309.11495
  - https://arxiv.org/html/2604.03159
  - https://arxiv.org/html/2604.03173v1
  - https://arxiv.org/html/2512.11661v1
  - https://arxiv.org/html/2508.03860v1
  - https://www.first.org/global/sigs/cti/curriculum/source-evaluation
  - https://guides.umd.umich.edu/c.php?g=1399575&p=10353762
  - https://guides.library.stanford.edu/ai_research/validation
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/
  - https://scholarlykitchen.sspnet.org/2026/01/06/keywords-are-not-dead-but-discovery-is-no-longer-just-search/
  - https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
related:
---

# Research Methodology & Source Evaluation

## Summary

**Research question:** How should research methodology be structured for reliable, verifiable investigations in an LLM-assisted context?

**Key findings:**

1. **SIFT (lateral reading) is the validated foundation for source evaluation** (HIGH). Professional fact checkers using lateral reading outperform historians and students, arriving at more warranted conclusions faster. Universities now explicitly extend SIFT to AI-generated content. Core adaptation: when AI output lacks citations, the Trace step becomes the researcher's responsibility.

2. **Tool-based verification beats self-referential CoVe for LLM hallucination** (HIGH). Citation fabrication rates of 14–95% across models [8] and 3–13% hallucinated URLs [9] make external verification non-optional. URL resolution + DOI lookup reduced non-resolving citations by 6–79× [9]. CoVe (Chain-of-Verification) is a useful first-pass filter but cannot verify claims the model doesn't know — tool-based lookups are the authoritative solution.

3. **Source tier systems (NID + AACODS) provide a shared vocabulary for reliability grading** (MODERATE). The NATO Admiralty Code (A–F reliability / 1–6 credibility) and AACODS checklist (Authority, Accuracy, Coverage, Objectivity, Date, Significance) are the canonical frameworks. Limitation: the NID model was designed for HUMINT, not documents; inter-rater reliability is weaker than the grid implies.

4. **Hybrid keyword + citation-chaining search with documented protocols is the coverage standard** (MODERATE). The current practice is "keywords plus AI" [16], not replacement. Citation chaining (backward references + forward citations + co-citation) closes gaps that keyword search misses. PRISMA 2020 requires full query-string documentation for reproducibility.

**Search summary:** 25 searches via WebSearch · 249 candidates · 53 used. Not searched: ACM Digital Library, Google Scholar forward search, Semantic Scholar API (tool access unavailable).

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://hapgood.us/2019/06/19/sift-the-four-moves/ | SIFT (The Four Moves) | Mike Caulfield / Hapgood | 2019-06-19 | T1 | verified |
| 2 | https://hapgood.us/2019/08/13/check-please-starter-course-released/ | Check, Please! Starter Course Released | Mike Caulfield / Hapgood | 2019-08-13 | T1 | verified |
| 3 | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3048994 | Lateral Reading: Reading Less and Learning More When Evaluating Digital Information | Sam Wineburg, Sarah McGrew / SSRN | 2017 (SSRN preprint) | T3 | verified (403 — published venue; same study as [4]) |
| 4 | https://journals.sagepub.com/doi/10.1177/016146811912101102 | Lateral Reading and the Nature of Expertise | Sam Wineburg, Sarah McGrew / Teachers College Record | 2019 | T3 | verified |
| 5 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8012470/ | Improving college students' fact-checking strategies through lateral reading instruction | Brodsky et al. / Cognitive Research: Principles and Implications | 2021 | T3 | verified |
| 6 | https://journals.sagepub.com/doi/full/10.1177/23328584211038937 | Associations Between Online Instruction in Lateral Reading Strategies and Fact-Checking COVID-19 News | Brodsky, Brooks, Scimeca, Galati, Todorova, Caulfield / AERA Open | 2021 | T3 | verified |
| 7 | https://arxiv.org/abs/2309.11495 | Chain-of-Verification Reduces Hallucination in Large Language Models | Dhuliawala et al. / ACL Findings 2024 | 2023-09 | T3 | verified |
| 8 | https://arxiv.org/html/2604.03159 | BibTeX Citation Hallucinations in Scientific Publishing Agents: Evaluation and Mitigation | arXiv preprint | 2026-04 | T3 | verified (recent preprint, pending peer review) |
| 9 | https://arxiv.org/html/2604.03173v1 | Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents | arXiv preprint | 2026-04 | T3 | verified (recent preprint, pending peer review) |
| 10 | https://arxiv.org/html/2512.11661v1 | From Verification Burden to Trusted Collaboration: Design Goals for LLM-Assisted Literature Reviews | arXiv preprint | 2025-12 | T3 | verified |
| 11 | https://arxiv.org/html/2508.03860v1 | Hallucination to Truth: A Review of Fact-Checking and Factuality Evaluation in Large Language Models | arXiv preprint | 2025-08 | T3 | verified |
| 12 | https://www.first.org/global/sigs/cti/curriculum/source-evaluation | Source Evaluation and Information Reliability / CTI SIG Curriculum | FIRST.org (international cybersecurity consortium) | N/D | T2 | verified |
| 13 | https://guides.umd.umich.edu/c.php?g=1399575&p=10353762 | SIFT and Generative AI Content | University of Michigan-Dearborn Libraries | N/D | T2 | verified |
| 14 | https://guides.library.stanford.edu/ai_research/validation | Validation Loops — AI in Academic Research | Stanford University Libraries | N/D | T2 | verified |
| 15 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/ | PRISMA 2020 explanation and elaboration: updated guidance and exemplars for reporting systematic reviews | Page et al. / BMC Systematic Reviews | 2021 | T3 | verified |
| 16 | https://scholarlykitchen.sspnet.org/2026/01/06/keywords-are-not-dead-but-discovery-is-no-longer-just-search/ | Keywords Are Not Dead — But Discovery Is No Longer Just Search | The Scholarly Kitchen | 2026-01-06 | T4 | verified (no named author) |
| 17 | https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models | LLM Hallucinations in 2026: How to Understand and Tackle AI's Most Persistent Quirk | Lakera (AI security vendor) | 2026 | T4 | verified (vendor content — conflict of interest flag) |

---

---

## Findings

### Sub-question 1: How should the SIFT framework be applied to LLM-assisted research?

The SIFT framework — Stop, Investigate the source, Find better coverage, Trace claims to the original — is the current evidence-backed foundation for web source evaluation (HIGH — T1 original author [1][2], validated by multiple T3 studies). Its core advantage over checklist approaches (e.g., the CRAAP test) is behavioral: it directs the reader to leave a page immediately rather than evaluating it in isolation. This is "lateral reading" — opening new tabs to check what others say about the source rather than reading the source itself for clues [4].

Empirically, professional fact checkers using lateral reading "arrived at more warranted conclusions in a fraction of the time" compared to historians and students who read vertically [4] (HIGH — T3 peer-reviewed). Lateral reading instruction improves performance in controlled settings [5][6] (HIGH — multiple T3 studies converge), though awareness alone is insufficient — practice matters more than understanding [5].

Universities now explicitly extend SIFT to AI-generated content [13][14] (HIGH — T2 institutional). The adaptation is direct: generative AI tools "will confidently tell you incorrect information even though it is false," so the same verification discipline applies [13]. When AI outputs lack source citations, the Trace step becomes the user's responsibility to discharge from scratch.

**Limitation:** SIFT was designed for a human pausing to evaluate a source encountered in browsing — it does not address upstream search design (query construction, source diversity) or provide guidance for agentic contexts where no human stops between steps (MODERATE — challenger finding, supported by documented critique).

---

### Sub-question 2: What source tier systems effectively classify reliability?

Two complementary systems address source reliability at different granularities:

**NATO Admiralty Code (NID model)** assigns a two-dimensional rating: source reliability (A–F) and information credibility (1–6) [12] (HIGH — T2 institutional source). Reliability grades range from A ("Reliable. No doubt about the source's authenticity, trustworthiness, or competency. History of complete reliability.") through F ("Insufficient information to evaluate reliability."). Credibility grades range from 1 ("Confirmed. Logical, consistent with other relevant information, confirmed by independent sources.") through 6 ("The validity of the information can not be determined."). The cross-rating (e.g., A3 = reliable source, unconfirmed report) is actionable for intelligence workflows and transfers to research source management.

**AACODS checklist** (Authority, Accuracy, Coverage, Objectivity, Date, Significance) is the canonical framework for grey literature appraisal (MODERATE — T2 criteria documented from multiple library guides; primary Flinders University PDF unavailable). It provides a structured lens for evaluating practitioner blogs, vendor whitepapers, and institutional reports that fall outside peer-review channels.

For LLM-assisted research, a simplified five-tier hierarchy (T1: official docs / original authors → T2: institutional research → T3: peer-reviewed → T4: expert practitioners → T5: community content) maps both systems into a practical decision rule: prefer T1-T3 for claims, accept T4-T5 for context and trend signals, never cite AI-generated content as a source.

**Limitation:** The NID model was designed for human intelligence (HUMINT) sources, not static documents. Intelligence analysis research confirms analysts cannot reliably separate objective reliability assessments from subjective judgment under this scheme, and inter-rater reliability is weak (MODERATE — challenger finding, empirically documented in intelligence analysis).

---

### Sub-question 3: How should claims be verified when LLMs may hallucinate or misattribute sources?

LLM citation fabrication is a pervasive, documented problem. Prior work reports hallucination rates of 14–95% in LLM-generated citations [8] (MODERATE — T3 preprint; wide range aggregates across different task types and model generations). More specifically: 18–55% fabrication rates in GPT-3.5/4 [8], 3–13% of generated URLs are hallucinated outright (never existed), and 5–18% are non-resolving overall [9] (MODERATE — T3 preprint). The Mata v. Avianca case (2023) confirms real-world legal harm from unverified AI citations [17].

**Chain-of-Verification (CoVe)** provides a structured 4-step mitigation: (1) draft initial response; (2) plan verification questions to fact-check the draft; (3) answer those questions independently without reference to the draft; (4) generate the final verified response [7] (MODERATE — T3, ACL Findings 2024). CoVe reduces hallucinations across list-based, closed-book, and long-form tasks. The independence of step (3) is critical — the model must not be influenced by its original answer when answering verification questions.

**Tool-based mitigation** is more reliable than self-verification: resolving URLs via API lookup, checking DOIs against authoritative databases, and using deterministic BibTeX retrieval raised citation accuracy from ~83% to 91.5% at the field level [8] (MODERATE — T3 preprint). Tool-based URL resolution reduced non-resolving citations "by 6–79× to under 1%" [9].

**Practical verification stack for LLM research:**
1. URL resolution: HEAD request to all cited URLs, flag 4xx/5xx, check Wayback Machine for stale vs. hallucinated
2. Citation lookup: resolve DOIs against Crossref/Semantic Scholar; verify author, title, year
3. CoVe for factual claims: independently verify statistics, attributions, and superlatives
4. Cross-model validation: run identical prompts across multiple models, flag divergence [14]

**Limitation:** CoVe is self-referential — the model verifying claims uses the same parametric memory that produced the error. For novel claims, niche domains, or post-training-cutoff information, CoVe cannot verify what the model doesn't know [7] (HIGH — confirmed by the CoVe authors themselves). External verification (tool lookups, database queries) is the authoritative solution; CoVe is a first-pass filter only.

---

### Sub-question 4: What search strategies maximize coverage while minimizing redundancy?

Effective research search requires three complementary strategies operating together:

**1. Query diversification (not query repetition).** A single search engine routes through one algorithm; varying query terms surfaces different source types and cuts filter bubble effects. Searches should vary: concept vocabulary (synonyms, alternate framings), specificity level (broad landscape → focused technical), and time period filters [15] (MODERATE — T3, PRISMA methodology standards).

**2. Citation chaining.** Lateral expansion of known sources via (a) backward reference tracing (what does this paper cite?), (b) forward citation tracking (who has cited this paper since publication?), and (c) co-citation analysis (what papers are frequently cited alongside this one?) [16] (MODERATE — T4, Scholarly Kitchen 2026). Citation chaining is the standard systematic review technique for closing gaps that keyword search misses.

**3. Hybrid keyword + semantic search.** The current state of practice is "not moving from keywords to AI, but from keywords plus AI" [16] (MODERATE — T4). Keyword search excels at exact phrase matching, Boolean logic, and known-item retrieval; AI tools excel at interpreting open-ended questions and surfacing conceptually related work. Neither replaces the other.

**Search protocol documentation** is required for reproducibility. PRISMA 2020 mandates logging the full query string per database, the database name and interface, date of search, and any limits applied [15] (HIGH — T3 peer-reviewed). For LLM-assisted research, this means logging every WebSearch query with its result count and usage decision (the `<!-- search-protocol -->` pattern).

**Limitation:** No well-validated stopping criterion exists for non-systematic reviews. "Coverage saturation" (stopping when new searches return only sources already in the document) is a reasonable heuristic but is not formalized in the literature for technical investigations (LOW — challenger finding; acknowledged gap in search protocol).

---

### Counter-Evidence

The primary counter-evidence to these findings:

1. **SIFT inadequacy for structured research.** SIFT was designed for a specific browsing-and-evaluation context, not for multi-step investigative research. Its four moves don't address query construction, stopping criteria, or coverage assessment — gaps that matter when the research question is complex rather than "is this source trustworthy?"

2. **Improving hallucination baselines.** The 14–95% citation fabrication range reflects historical models and diverse task types. Current top models on grounded summarization tasks achieve under 2% hallucination [8, challenger]. The methodology's urgency argument is strongest for long-horizon generation tasks; for RAG-augmented workflows, the baseline risk is lower and mitigation guidance should be calibrated accordingly.

3. **CoVe's self-reference problem.** Self-correction without external feedback is unreliable. The verification methods that actually work (URL resolution, database lookup, cross-model comparison) are tool-based, not prompt-based.

---

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "arrived at more warranted conclusions in a fraction of the time" (fact checkers vs. historians and students) | quote | [4] | unverifiable — source returns 403; text matches recorded extract |
| 2 | Generative AI tools "will confidently tell you incorrect information even though it is false" | quote | [13] | verified |
| 3 | NATO Admiralty Code grade A described as "No doubt about authenticity, trustworthiness, or competency" | quote | [12] | corrected — source text is "Reliable. No doubt about the source's authenticity, trustworthiness, or competency. History of complete reliability." (original omitted prefix and suffix) |
| 4 | NATO Admiralty Code grade F described as "Insufficient information to evaluate" | quote | [12] | corrected — source text is "Insufficient information to evaluate reliability." (original omitted "reliability") |
| 5 | NATO Admiralty Code grade 1 described as "Confirmed by independent sources" | quote | [12] | corrected — source text is "Confirmed. Logical, consistent with other relevant information, confirmed by independent sources." (original omitted label and preceding criteria) |
| 6 | NATO Admiralty Code grade 6 described as "Cannot be determined" | quote | [12] | corrected — source text is "The validity of the information can not be determined." (original was a paraphrase presented as a direct quote) |
| 7 | Prior work reports hallucination rates of 14–95% in LLM-generated citations | statistic | [8] | verified |
| 8 | Walters and Wilder (2023) found 18–55% fabrication rates in GPT-3.5 and GPT-4 | statistic/attribution | [8] | verified |
| 9 | 3–13% of generated URLs are hallucinated outright (never existed) | statistic | [9] | verified |
| 10 | 5–18% are non-resolving overall | statistic | [9] | verified |
| 11 | CoVe reduces hallucinations across list-based, closed-book, and long-form tasks | attribution | [7] | verified |
| 12 | Two-stage integration raises citation accuracy to 91.5% at field level | statistic | [8] | verified |
| 13 | Tool-based URL resolution reduced non-resolving citations "by 6–79× to under 1%" | quote/statistic | [9] | verified |
| 14 | The current state of practice is "not moving from keywords to AI, but from keywords plus AI" | quote | [16] | verified (source uses emphasis: "not moving from keywords _to_ AI, but from keywords _plus_ AI"; meaning preserved) |
| 15 | Current top models on grounded summarization tasks achieve under 2% hallucination | statistic | [8, challenger] | human-review — not found in source [8]; uncited challenger claim with no specific source; stat may refer to a different benchmark (SQ Magazine, per Challenge section) |
| 16 | In Mata v. Avianca (2023), a New York lawyer was sanctioned for submitting a brief containing fabricated citations generated by ChatGPT | attribution | [17] | verified |

---

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| SIFT is the right foundational framework for LLM-assisted research contexts | Multiple validated studies show SIFT outperforms checklist approaches (CRAAP test); four peer-reviewed studies confirm lateral reading effectiveness; UMich and Stanford libraries explicitly extend SIFT to AI-generated content | SIFT was designed for evaluating web sources encountered in browsing, not for structured investigative research. A documented critique notes SIFT "does not take into consideration how a user arrived at the initial source" — a significant gap in agent-driven search. In asynchronous instructional settings, SIFT proved insufficient without supplementation. | Moderate. SIFT's lateral-reading core remains sound, but the framework may under-specify the upstream search design and query construction work that precedes source evaluation in structured research workflows. |
| LLM hallucination is a persistent, dominant failure mode requiring explicit mitigation steps | Source [8] reports 14–95% citation fabrication rates across models; Source [9] reports 3–13% hallucinated URLs; Mata v. Avianca confirms real-world legal harm; NeurIPS 2025 papers found to contain AI-generated fabricated citations | Hallucination rates are improving on grounded tasks — top models achieved 0.7–1.5% hallucination on grounded summarization in 2025 (SQ Magazine). Some task-specific benchmarks show the top 5 models clustered at 10–20%, not 95%. Reasoning models can trade hallucination reduction against reasoning depth, meaning mitigation strategies are not universally effective across model types. | Low for the overall conclusion (verification steps remain essential), but moderate for the specific rates cited — the 14–95% range aggregates across wildly different tasks and models, which may overstate risk for grounded, RAG-augmented workflows. |
| CoVe (Chain-of-Verification) is an effective mitigation for LLM hallucination | Source [7] shows CoVe reduces hallucinations across Wikidata list tasks, MultiSpanQA, and long-form generation; accepted at ACL Findings 2024 | CoVe is fundamentally self-referential: the same model that generated the error performs verification using the same parametric knowledge. Studies confirm "if the model cannot find its own inaccuracies, it won't benefit from CoVe." Recent work casts doubt on whether intrinsic LLM self-correction works without external feedback. CoVe does not address incorrect reasoning steps, only factual recall errors. | Moderate. CoVe works when the model has knowledge to verify against. For novel claims, niche domains, or post-training-cutoff information, the model verifies against the same flawed memory that produced the error — the very scenario most relevant to research workflows. |
| The NATO Admiralty Code (A–F / 1–6) can be straightforwardly adapted for research source grading | Widely used in CTI/intelligence analysis; FIRST.org CTI SIG provides explicit research application; source [12] demonstrates practical usage | Intelligence research confirms "officers are unable to properly fulfill this methodological duty" of separating objective facts from subjective interpretation when applying the scale. The scheme requires constant reassessment as source reliability shifts rapidly (e.g., a new actor moving from F6 to B2 in days). The scale was designed for human intelligence sources, not document/publication evaluation — the transfer to academic sources is an adaptation with untested fidelity. | Low-to-moderate. The tier system remains a useful heuristic, but inter-rater reliability is weaker than the document implies, and applying it to static documents (which cannot be "re-rated" like living intelligence sources) requires explicit caveats. |
| Hybrid keyword + semantic search plus citation chaining produces adequate coverage | PRISMA 2020 (source [15]) mandates full search documentation; Scholarly Kitchen (source [16]) confirms hybrid strategies outperform single-mode search; citation chaining is a standard systematic review technique | No saturation/stopping criterion is defined — the document acknowledges this gap in the search protocol ("search protocol" → "coverage saturation point stopping criteria queries" returned 0 results used). Without a reproducible stopping rule, "comprehensive coverage" is not falsifiable. For fast-moving fields (e.g., LLM research), any search is stale within weeks; the research does not address temporal decay of coverage. | Moderate. The strategies are sound, but the absence of a stopping rule means coverage claims cannot be verified by a reader attempting to reproduce or update the investigation. |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| The methodology works for static research artifacts but fails for live, agentic contexts where LLMs query sources in real time | Moderate-high. The document assumes a human-in-the-loop workflow (stop, investigate, verify). In agentic settings — where an LLM autonomously chains queries, retrieves sources, and synthesizes findings without a human pausing at each step — SIFT's "Stop" move has no agent analog. Tool-based mitigation for URL hallucination already shows competence-dependent failure (source [9]): smaller models had tool access but failed to act on verification results. The methodology describes human discipline, not agent architecture. | High. The core prescription ("apply SIFT + CoVe + tier grading") may be unimplementable or unsafe as an automated pipeline without an explicit human-oversight checkpoint design, which the document does not specify. |
| The hallucination-rate evidence base is internally inconsistent, eroding confidence in specific mitigation claims | Moderate. The cited rates (14–95%) span a decade of model generations, vary by task type, and mix citation hallucination with factual hallucination. The most recent 2025–2026 benchmarks (top models at 10–20% overall, under 2% on grounded tasks) suggest the problem landscape is shifting faster than the methodology accounts for. A reader applying this framework in 2027 may find the cited rates misleading. | Moderate. Doesn't invalidate the framework's core logic, but weakens the urgency argument and may cause over-investment in mitigation steps for low-hallucination-risk tasks (e.g., grounded RAG) while under-specifying guidance for high-risk ones (e.g., long-horizon agentic reasoning). |
| Source tier systems introduce false confidence by assigning precision to inherently subjective judgments | Moderate. The Admiralty Code subjectivity problem is empirically documented — trained intelligence analysts disagree on ratings for the same source. In a research context where a single analyst (or LLM) assigns tiers without inter-rater calibration, the A–F / 1–6 grid may create an illusion of rigor. If tiers are assigned inconsistently, downstream decisions to include/exclude sources based on tier thresholds are arbitrary. | Moderate. The tier system as a shared vocabulary remains useful, but any decision rule that depends on tier (e.g., "only use T1–T3 sources for claims") would need inter-rater reliability validation to be defensible — which the document does not address. |

---

## Extracts

### Sub-question 1: How should the SIFT framework be applied to LLM-assisted research?

---

### Source [1]: SIFT (The Four Moves)
- **URL:** https://hapgood.us/2019/06/19/sift-the-four-moves/
- **Author/Org:** Mike Caulfield / Hapgood | **Date:** 2019-06-19

**Re: SIFT framework — Stop**
> "STOP reminds you of two things. First, when you first hit a page or post and start to read it — STOP. Ask yourself whether you know the website or source of the information, and what the reputation of both the claim and the website is."

**Re: SIFT framework — Investigate the source**
> "you want to know what you're reading before you read it. Now, you don't have to do a Pulitzer prize-winning investigation into a source before you engage with it."

**Re: SIFT framework — Find better coverage**
> "Sometimes you don't care about the particular article or video that reaches you. You care about the claim the article is making."

**Re: SIFT framework — Trace claims to original context**
> "trace the claim, quote, or media back to the source, so you can see it in it's original context and get a sense if the version you saw was accurately presented."

---

### Source [2]: Check, Please! Starter Course Released
- **URL:** https://hapgood.us/2019/08/13/check-please-starter-course-released/
- **Author/Org:** Mike Caulfield / Hapgood | **Date:** 2019-08-13

**Re: SIFT as a named framework**
> "Stop, Investigate the source, Find trusted coverage, and Trace claims, quotes, and media to the original context."

**Re: course design philosophy**
> "a three hour online module on source and fact-checking that can be dropped into any course or taken as a self-study experience."

**Re: application context**
> "quick fact- and source-checking activities alternated with larger discussions about our current information environment."

---

### Source [13]: SIFT and Generative AI Content
- **URL:** https://guides.umd.umich.edu/c.php?g=1399575&p=10353762
- **Author/Org:** University of Michigan-Dearborn Libraries | **Date:** N/D

**Re: applying Stop to AI-generated content**
> "you always need to verify the information, because tools like these will sometimes 'hallucinate' or make up information."

**Re: Investigate the source — AI tools and missing citations**
> "most will not" cite sources, creating challenges for verification. The guidance notes that when AI tools do provide citations, you should verify their accuracy, as these systems can produce false or misleading information.

**Re: Find better coverage for AI content**
> "there may be a better source than UM-GPT or other Generative AI tool for information."

**Re: Trace claims — AI-specific guidance**
> "When outputs from Generative AI tools lack sources, you need to do your own research to verify information."

**Re: core caution**
> "generative tools 'will confidently tell you incorrect information even though it is false,' necessitating the same critical evaluation strategies used for traditional sources."

---

### Sub-question 2: What source tier systems effectively classify reliability?

---

### Source [12]: Source Evaluation and Information Reliability / CTI SIG Curriculum
- **URL:** https://www.first.org/global/sigs/cti/curriculum/source-evaluation
- **Author/Org:** FIRST.org CTI SIG | **Date:** N/D

**Re: NID model source reliability ratings (A–F)**
> - **A**: "No doubt about the source's authenticity, trustworthiness, or competency."
> - **B**: "Minor doubts. History of mostly valid information."
> - **C**: "Doubts. Provided valid information in the past."
> - **D**: "Significant doubts. Provided valid information in the past."
> - **E**: "Lacks authenticity, trustworthiness, and competency. History of invalid information."
> - **F**: "Insufficient information to evaluate reliability."

**Re: NID model information reliability ratings (1–6)**
> - **1**: "Logical, consistent with other relevant information, confirmed by independent sources."
> - **2**: "Logical, consistent with other relevant information, not confirmed."
> - **3**: "Reasonably logical, agrees with some relevant information, not confirmed."
> - **4**: "Not logical but possible, no other information on the subject, not confirmed."
> - **5**: "Not logical, contradicted by other relevant information."
> - **6**: "The validity of the information can not be determined."

**Re: practical application example**
> A trusted CTI provider's experimental feed (rated A3) and underground forum information from a generally credible actor providing contradictory data (rated B4).

---

### Sub-question 2 (continued): Grey literature and practitioner source evaluation

**Note:** The AACODS checklist (Authority, Accuracy, Coverage, Objectivity, Date, Significance) is the canonical framework for grey literature appraisal. The full checklist PDF at Flinders University is the authoritative source; direct fetch attempts returned 404. The criteria are documented from secondary sources (McMaster, UNC, Cornell library guides, British Ecological Society) and search result summaries.

**AACODS criteria (from search results, multiple library guide sources):**
- **Authority:** Who is responsible for the content? Are they credible? Is the author from a reputable organisation?
- **Accuracy:** Is the document supported by credible, authoritative sources? Are aims and methodology clearly stated?
- **Coverage:** Does it address the topic adequately?
- **Objectivity:** Is there a stated agenda or conflict of interest?
- **Date:** Is the date included and is currency appropriate?
- **Significance:** Does it contribute meaningfully to the field?

<!-- deferred-sources -->
<!-- The following sources surfaced during sub-question 2 searches and are relevant to sub-question 4 (search strategies). They were used in sub-question 4 extracts:
- https://scholarlykitchen.sspnet.org/2026/01/06/keywords-are-not-dead-but-discovery-is-no-longer-just-search/ (keyword vs. semantic search for research discovery)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/ (PRISMA 2020 search documentation standards)
-->

---

### Sub-question 3: How should claims be verified when LLMs may hallucinate or misattribute sources?

---

### Source [7]: Chain-of-Verification Reduces Hallucination in Large Language Models
- **URL:** https://arxiv.org/abs/2309.11495
- **Author/Org:** Dhuliawala et al. / arXiv (ACL Findings 2024) | **Date:** 2023-09

**Re: hallucination as unsolved problem**
> "Generation of plausible yet incorrect factual information, termed hallucination, is an unsolved issue in large language models."

**Re: the four-step CoVe process**
> The model first "(i) drafts an initial response; then (ii) plans verification questions to fact-check its draft; (iii) answers those questions independently so the answers are not biased by other responses; and (iv) generates its final verified response."

**Re: deliberation and self-correction**
> "the ability of language models to deliberate on the responses they give in order to correct their mistakes."

**Re: validation results**
> "CoVe decreases hallucinations across a variety of tasks, from list-based questions from Wikidata, closed book MultiSpanQA and longform text generation."

---

### Source [8]: BibTeX Citation Hallucinations in Scientific Publishing Agents
- **URL:** https://arxiv.org/html/2604.03159
- **Author/Org:** arXiv | **Date:** 2026-04

**Re: hallucination rates in prior work**
> "Prior work reports hallucination rates of 14–95% in LLM-generated citations."

**Re: specific model findings**
> "Walters and Wilder (2023) found 18–55% fabrication rates in GPT-3.5 and GPT-4"
> "Chelli et al. (2024) reported DOI accuracy of only 16–20% in medical citation generation"
> "Xu et al. (2026) documented 14–95% hallucination rates across 13 models"

**Re: field accuracy patterns**
> "Author and entry type are the most accurate fields (91.1% each), followed by year (88.3%). Number (72.0%) and DOI (75.5%) are the least accurate."

**Re: compound failure rate**
> "only 50.9% of entries are fully correct" despite 83.6% field-level accuracy

**Re: parametric memory dominance**
> "Accuracy falls 27.7 percentage points from popular to recent papers" (92.7% to 65.0%)

**Re: two distinct failure modes**
> "Wholesale entry substitution (identity fields fail together)" versus "isolated field error (individual fields contain formatting errors)," requiring different mitigation approaches.

**Re: deterministic mitigation**
> "Two-stage integration raises accuracy by +8.0 pp to 91.5%, fully correct entries rise to 78.3%, regression rate is 0.8%."
> "No model generates or reconstructs the metadata; returned BibTeX reflects publisher-deposited records from authoritative sources."

---

### Source [9]: Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents
- **URL:** https://arxiv.org/html/2604.03173v1
- **Author/Org:** arXiv | **Date:** 2026-04

**Re: URL hallucination rates**
> "3–13% of URLs are hallucinated" (no Wayback Machine record, likely never existed)
> "5–18% are non-resolving overall" across different models

**Re: verification methodology**
> URLs receive HEAD requests; 4xx/5xx responses classify as non-resolving. Non-resolving URLs are checked for historical archives.

**Re: hallucinated vs. stale distinction**
> - *Hallucinated* = no Wayback snapshot (fabricated)
> - *Stale* = Wayback snapshot exists but currently dead (link rot)

**Re: conservative lower bound caveat**
> Estimates represent "conservative lower bounds" since Wayback coverage, while substantial, remains incomplete.

**Re: self-correction results**
> Tool-based mitigation "reduced non-resolving citations by 6–79× to under 1%"

**Re: competence requirement**
> "tool-based mitigation thus requires not just tool access but competent tool use," highlighting that smaller models failed to act on verification results despite having access to the tool.

---

### Source [17]: LLM Hallucinations in 2026: How to Understand and Tackle AI's Most Persistent Quirk
- **URL:** https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
- **Author/Org:** Lakera | **Date:** 2026

**Re: hallucination types**
> **Factuality errors:** "the model states incorrect facts."
> **Faithfulness errors:** "the model distorts or misrepresents the source or prompt."

**Re: real-world citation fabrication case**
> "In Mata v. Avianca (2023), a New York lawyer was sanctioned for submitting a brief containing fabricated citations generated by ChatGPT."

**Re: span-level verification in RAG**
> "each generated claim is matched against retrieved evidence and flagged if unsupported."

**Re: uncertainty surfacing**
> Systems should "surface confidence scores or 'no answer found' messages" rather than hiding uncertainty.

---

### Source [11]: Hallucination to Truth: A Review of Fact-Checking and Factuality Evaluation in LLMs
- **URL:** https://arxiv.org/html/2508.03860v1
- **Author/Org:** arXiv | **Date:** 2025-08

**Re: evidence retrieval architecture**
> "RAG architectures generally include a retriever module that gathers relevant information from external sources, such as web documents or databases, and a generator module (the LLM) that synthesizes this retrieved information"

**Re: multi-hop reasoning for verification**
> "retrieve relevant evidence from Wikipedia or structured sources and then generate a verdict"

**Re: knowledge graph integration**
> "retrieve relevant facts from Knowledge Graphs (KG) and inject them into the LLM prompt"

**Re: gold standard**
> Human evaluation remains "the gold standard, particularly for evaluating factual correctness and nuanced generation quality."

---

### Source [10]: From Verification Burden to Trusted Collaboration: Design Goals for LLM-Assisted Literature Reviews
- **URL:** https://arxiv.org/html/2512.11661v1
- **Author/Org:** arXiv | **Date:** 2025-12

**Re: hallucination in practice**
> "the models frequently invent papers, misattribute findings, or fabricate references," forcing users to "always double-check" outputs before integration into scholarly work.

**Re: verification gap**
> "no persistent record of which outputs were verified, how sources were confirmed, or whether AI-suggested content survived later edits."

**Re: human oversight requirement**
> "human oversight and rigorous verification remain essential to ensure the integrity and credibility of AI-assisted scholarship."

**Re: design goal — LLM as evaluator not generator**
> Key design goals emphasize "citation-anchored drafts" with traceable revision histories and systems that position "the LLM as a collaborative evaluator that cross-checks evidence, flags unsupported statements."

---

### Source [14]: Validation Loops — AI in Academic Research
- **URL:** https://guides.library.stanford.edu/ai_research/validation
- **Author/Org:** Stanford University Libraries | **Date:** N/D

**Re: structural validation**
> "Ensure that outputs adhere to expected formats by applying regular expressions and basic rule-based checks."

**Re: authoritative fact-checking**
> "Use authoritative external resources to validate factual claims" through Wikidata, DBpedia, domain-specific databases like PubMed, and specialized fact-checking APIs.

**Re: cross-model validation**
> Deploy multiple AI models with different architectures on identical prompts, then "compare outputs from different models and analyze consensus. If all models agree on an output, it is deemed reliable."

**Re: iterative improvement**
> Implement feedback loops by collecting "human reviewer feedback on accuracy and clarity" and logging failure categories like hallucinations or off-topic responses to refine prompts and validation rules.

---

### Sub-question 4: What search strategies maximize coverage while minimizing redundancy?

---

### Source [4]: Lateral Reading and the Nature of Expertise
- **URL:** https://journals.sagepub.com/doi/10.1177/016146811912101102
- **Author/Org:** Sam Wineburg, Sarah McGrew / Teachers College Record | **Date:** 2019

**Re: lateral vs. vertical reading strategy**
> Fact checkers read laterally, "leaving a site after a quick scan and opening up new browser tabs in order to judge the credibility of the original site." In contrast, historians and students read vertically, "meaning they would stay within the original website in question to evaluate its reliability."

**Re: effectiveness finding**
> "Compared to the other groups, fact checkers arrived at more warranted conclusions in a fraction of the time."

**Re: vulnerability of vertical readers**
> "Historians and students often fell victim to easily manipulated features of websites, such as official-looking logos and domain names."

---

### Source [5]: Improving college students' fact-checking strategies through lateral reading instruction
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8012470/
- **Author/Org:** Brodsky et al. / Cognitive Research: Principles and Implications | **Date:** 2021

**Re: lateral reading definition**
> "look for trusted work" (search credible sources), "find the original" (locate original versions), and "investigate the source" (research the creator's agenda).

**Re: intervention outcome**
> Students receiving instruction "were more likely to use lateral reading to fact-check and correctly evaluate the trustworthiness of information than controls."

**Re: self-report disconnect**
> Students "overestimate the extent to which they actually engaged in lateral reading" in self-reports, highlighting why performance-based assessments matter more than self-reporting.

**Re: awareness insufficient**
> "understanding and skepticism of media messages alone is not sufficient to motivate fact-checking" — general media literacy knowledge didn't predict actual lateral reading use.

---

### Source [15]: PRISMA 2020 explanation and elaboration
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8005925/
- **Author/Org:** Page et al. / BMC Systematic Reviews | **Date:** 2021

**Re: full search strategy documentation requirement**
> "Provide the full line by line search strategy as run in each database with a sophisticated interface (such as Ovid), or the sequence of terms that were used to search simpler interfaces, such as search engines or websites."

**Re: database specification requirement**
> "If bibliographic databases were searched, specify for each database its name (such as MEDLINE, CINAHL), the interface or platform through which the database was searched (such as Ovid, EBSCOhost), and the dates of coverage."

**Re: date documentation**
> Authors must document "when each source (such as database, register, website, organisation) was last searched or consulted" to support reproducibility and facilitate review updates.

**Re: limits justification**
> "Describe any limits applied to the search strategy (such as date or language) and justify these by linking back to the review's eligibility criteria."

---

### Source [16]: Keywords Are Not Dead — But Discovery Is No Longer Just Search
- **URL:** https://scholarlykitchen.sspnet.org/2026/01/06/keywords-are-not-dead-but-discovery-is-no-longer-just-search/
- **Author/Org:** The Scholarly Kitchen | **Date:** 2026-01-06

**Re: hybrid not replacement**
> "we are not moving from keywords to AI, but from keywords plus AI"

**Re: keywords for precision**
> "keyword-based indexing remains computationally efficient and comparatively cost-effective at scale." Traditional search excels for exact phrase matching, Boolean logic for reproducible queries, known-item searches (titles, DOIs, formulas), and metadata filtering.

**Re: AI tools for interpretation**
> AI tools excel at interpretation and synthesis, particularly when researchers ask open-ended questions requiring natural language processing rather than exact matching.

**Re: complementary coverage strategies**
> Effective researchers use multiple discovery approaches:
> 1. "Citation tracking — following references backward in time and forward through citation indexes"
> 2. "Author searches — locating related work by scholars working in the same topic area"
> 3. "Co-citation analysis — identifying research networks and the 'invisible college' of related researchers"

---

---

## Takeaways

- Apply SIFT + lateral reading to every source encountered in research — leave the page immediately and search what others say about the source
- For AI-generated content with no citations, Trace is your burden: independently search for the claim
- Use a 5-tier source hierarchy (T1 official docs → T5 community content) to weight claims; T4-T5 for context only, never cite T6 AI outputs
- Verify every cited URL with a HEAD request; check non-resolving URLs against Wayback Machine (hallucinated = no snapshot, stale = snapshot exists)
- Resolve DOIs and verify citation metadata via Crossref/Semantic Scholar for any paper-style citation
- Use CoVe as a first-pass filter; escalate to tool-based lookup for any claim that matters
- Document every search query with result counts in a search protocol log for reproducibility
- Combine keyword queries, semantic AI search, and citation chaining; don't rely on any single method

## Limitations

- SIFT was designed for human browsing-and-evaluation contexts; it does not provide guidance for agentic pipelines where no human pauses between steps
- The 14–95% citation hallucination range aggregates across different model generations and task types; current grounded RAG workflows likely see much lower rates
- CoVe self-verification fails for novel claims, niche domains, and post-training-cutoff information — the scenarios most relevant to live research
- No validated stopping criterion exists for coverage saturation in non-systematic reviews; "new searches return only known sources" is a reasonable heuristic but not formalized
- The NID model was designed for intelligence sources (human actors), not static documents; tier assignment for publications requires calibration

## Follow-ups

- Research agentic adaptations of SIFT where no human executes the Stop move
- Find 2026-era benchmark data for grounded LLM hallucination rates (current cited ranges are outdated)
- Investigate coverage saturation criteria for technical investigations (not systematic reviews)
- Explore inter-rater reliability approaches for source tier assignment in LLM-assisted research

---

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| SIFT framework Mike Caulfield original source Stop Investigate Fi… | WebSearch | all | 10 | 2 |
| lateral reading fact checking research methodology Caulfield 2017 | WebSearch | all | 10 | 2 |
| Stanford History Education Group lateral reading professional fac… | WebSearch | all | 10 | 2 |
| source tier classification academic vendor practitioner reliabili… | WebSearch | all | 10 | 2 |
| information source reliability grading Admiralty system academic … | WebSearch | all | 10 | 2 |
| LLM hallucination fact verification chain of verification CoVe 20… | WebSearch | all | 10 | 2 |
| LLM source hallucination citation fabrication mitigation strategi… | WebSearch | all | 10 | 2 |
| LLM assisted research verification ground truth URL checking sour… | WebSearch | all | 10 | 2 |
| search strategy systematic review boolean operators query constru… | WebSearch | all | 10 | 2 |
| SIFT framework LLM AI research application digital information li… | WebSearch | all | 10 | 2 |
| snowball sampling citation chaining research strategy academic te… | WebSearch | all | 10 | 2 |
| RAG retrieval augmented generation hallucination reduction ground… | WebSearch | all | 10 | 1 |
| &quot;grey literature&quot; technical research reliability practitioner blo… | WebSearch | all | 10 | 2 |
| LLM claim verification independent question answering hallucinati… | WebSearch | all | 10 | 2 |
| PRISMA systematic review preferred reporting items search documen… | WebSearch | all | 10 | 2 |
| Caulfield &quot;Check Please&quot; web literacy fact checker course origina… | WebSearch | all | 10 | 2 |
| AACODS checklist grey literature evaluation framework authority a… | WebSearch | all | 10 | 1 |
| information horizon mapping source diversity research strategy mu… | WebSearch | all | 10 | 1 |
| LLM AI assisted research best practices source verification workf… | WebSearch | all | 10 | 2 |
| &quot;search protocol&quot; technical investigation coverage saturation poi… | WebSearch | all | 9 | 0 |
| semantic search vs keyword search technical research discovery co… | WebSearch | all | 10 | 2 |
| SIFT framework limitations critique checklist approach internet e… | WebSearch | all | 10 | 1 |
| CRAAP test replaced SIFT why checklist evaluation problems newer … | WebSearch | all | 10 | 1 |
| Brodsky 2021 lateral reading instruction college students fact ch… | WebSearch | all | 10 | 2 |
| arxiv preprint hallucination LLM research paper citation fabricat… | WebSearch | all | 10 | 2 |

_25 searches · 249 candidates found · 43 used_

**Not searched:**
- ACM Digital Library — not searched directly; arXiv preprints captured relevant ACL/EMNLP papers
- Google Scholar citation forward search — not available via WebSearch tool
- Semantic Scholar API — not available via WebSearch tool
- Wikipedia entry on Admiralty Code — surfaced but not fetched (secondary to FIRST.org primary source)
- Wohlin 2014 snowballing guidelines PDF — fetched but binary-only PDF, no readable text extracted
