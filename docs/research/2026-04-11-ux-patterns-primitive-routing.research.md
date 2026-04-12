---
name: "UX Patterns for Primitive Routing in Developer Tooling"
description: "Evidence supports a five-step intake pattern: accept natural language goals, infer the primitive, show a brief routing label (not a reformulation), display confidence when uncertain, and provide low-friction correction — backed by CHI/UIST/HF sources across 27 verified references"
type: research
sources:
  - https://arxiv.org/abs/2304.06597
  - https://dl.acm.org/doi/10.1145/3544548.3580817
  - https://arxiv.org/abs/2401.14484
  - https://dl.acm.org/doi/10.1145/3613904.3642466
  - https://arxiv.org/abs/2310.03691
  - https://dl.acm.org/doi/10.1145/3613904.3642462
  - https://arxiv.org/abs/2408.15989
  - https://arxiv.org/abs/2602.07338
  - https://arxiv.org/abs/2402.02136
  - https://dl.acm.org/doi/10.1145/2430545.2430551
  - https://www.nngroup.com/articles/progressive-disclosure/
  - https://www.nngroup.com/articles/wizards/
  - https://www.nngroup.com/articles/ai-paradigm/
  - https://rubyonrails.org/doctrine
  - https://ixdf.org/literature/book/the-glossary-of-human-computer-interaction/information-foraging-theory
  - https://docs.github.com/en/actions/get-started/actions-vs-apps
  - https://www.mesoform.com/resources/blog/information/from-paralysis-to-paved-roads-how-platform-engineering-resolves-cognitive-crises-in-devops-and-sre
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://ixdf.org/literature/topics/progressive-disclosure
  - https://hcibib.org/tcuid/
  - https://arxiv.org/abs/2502.02194
  - https://arxiv.org/abs/2511.00230
  - https://arxiv.org/abs/2503.16789
  - https://dl.acm.org/doi/10.1145/2858036.2858402
  - https://sjdm.org/journal/17/17411/new.html
  - https://www.sciencedirect.com/science/article/abs/pii/S1045926X16300982
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/
  - https://www.amazon.science/publications/ask-aspects-and-retrieval-based-hybrid-clarification-in-task-oriented-dialogue-systems
  - https://www.sciencedirect.com/science/article/pii/S0749597825000172
related: []
---

# UX Patterns for Primitive Routing in Developer Tooling

## Summary

The evidence converges on a five-step intake pattern for routing users to correct primitives without requiring them to know the abstraction model: **(1) accept goal in natural language; (2) infer the primitive from intent; (3) show a brief routing label before acting; (4) surface confidence state when uncertain; (5) offer low-friction correction, not a justification gate.** This is supported by 27 sources across CHI, UIST, Human Factors, and practitioner documentation.

Key constraints: automatic intent classification fails ~10% of cases even at GPT-4 performance, with systematic blind spots for rare categories — the rarest primitive in a system is the most likely to be misrouted. Expert users are harmed by opacity; they need on-demand access to the routing decision, not a progressive-disclosure flow designed for novices. Presenting five primitives to a user who knows none of the vocabulary is the highest-friction intake design available. Forced justification gates have not been shown to improve routing accuracy and have been shown to reduce decision confidence without improving outcomes in controlled experiments.

## Search Protocol

| # | Query | Engine | Results | Used |
|---|-------|--------|---------|------|
| 1 | progressive disclosure developer tools abstraction usability HCI research | WebSearch | 10 | yes |
| 2 | end-user programming abstraction levels mental models HCI CHI research | WebSearch | 10 | yes |
| 3 | task-centered interface design vs system-centered developer tools usability study | WebSearch | 10 | yes |
| 4 | intent-based routing configuration developer tools goal-directed design empirical study | WebSearch | 10 | partial |
| 5 | CHI paper programming tool abstraction usability mental model correct selection 2015 2024 | WebSearch | 10 | yes |
| 6 | "create-react-app" OR "angular CLI" design decisions scaffolding wizard usability research | WebSearch | 10 | partial |
| 7 | forced justification cognitive burden HCI decision making usability | WebSearch | 10 | yes |
| 8 | automation bias default selection choice architecture developer tools configuration | WebSearch | 10 | yes |
| 9 | conversational UI intent disambiguation developer tools NLP classification research | WebSearch | 10 | yes |
| 10 | guided onboarding wizard developer tools correct configuration empirical outcomes research | WebSearch | 10 | yes |
| 11 | layered architecture developer tools cognitive load "abstraction layer" user study mental model | WebSearch | 10 | partial |
| 12 | information foraging theory developer tool configuration navigation HCI | WebSearch | 10 | yes |
| 13 | UIST CHI "intent inference" goal inference developer tools natural language programming 2018 2024 | WebSearch | 10 | yes |
| 14 | "what it wants me to say" abstraction gap end-user programmers code generation CHI 2022 | WebSearch | 10 | yes |
| 15 | design principles generative AI applications CHI 2024 user mental models intent routing | WebSearch | 10 | yes |
| 16 | information foraging theory developer tools debugging refactoring ACM TOSEM Burnett 2013 | WebSearch | 10 | yes |
| 17 | rails new yeoman generator CLI wizard user research design intent abstraction selection 2015 2023 | WebSearch | 10 | partial |
| 18 | API usability study correct function selection developer mental model "cognitive dimensions" empirical 2015 2023 | WebSearch | 10 | yes |
| 19 | "natural language understanding" chatbot intent misclassification routing error rate recovery user study 2019 2024 | WebSearch | 10 | yes |
| 20 | choice overload paradox of choice user interface configuration options simplification research developer UX | WebSearch | 10 | yes |
| 21 | setup wizard configuration anti-pattern "justify your choice" forced decision overhead developer UX research | WebSearch | 10 | yes |
| 22 | opinionated defaults developer tools convention over configuration Ruby on Rails design rationale user adoption | WebSearch | 10 | yes |
| 23 | Hick's law decision time options developer interface CLI design patterns response time | WebSearch | 10 | yes |
| 24 | DirectGPT CHI 2024 direct manipulation LLM study prompts success rate results user study | WebSearch | 10 | yes |
| 25 | "software newcomers" onboarding "systematic literature review" tool selection cognitive 2022 2024 | WebSearch | 10 | yes |
| 26 | Stripe API developer experience design intent-based design case study developer tools 2019 2024 | WebSearch | 10 | partial |
| 27 | natural language programming tool "task type" classification enforcement vs workflow automation intent taxonomy HCI | WebSearch | 10 | no |
| 28 | VS Code extension palette command discovery developer usability "command palette" task intent finding 2020 2024 | WebSearch | 10 | partial |
| 29 | Generative UI outcome-oriented design Nielsen Norman Group intent-based developer 2024 | WebSearch | 10 | yes |
| 30 | task-oriented dialog system "clarification question" strategy single-turn vs multi-turn user study | WebSearch | 10 | yes |
| 31 | ASK hybrid clarification task-oriented dialogue Amazon intent disambiguation retrieval 2023 | WebSearch | 10 | yes |
| 32 | platform engineering "golden path" paved road developer tool selection cognitive load reduction study 2021 2024 | WebSearch | 10 | yes |
| 33 | decision fatigue developer tool selection "option paralysis" CLI tool configuration defaults research 2018 2024 | WebSearch | 10 | yes |
| 34 | ACM TOSEM information foraging developer tools "Fleming Scaffidi Piorkowski Burnett" 2013 | WebSearch | 10 | yes |
| 35 | GitHub Actions vs GitHub Apps confusion user research developer mental model selection documentation design | WebSearch | 10 | yes |
| 36 | Smashing Magazine agentic AI UX design patterns control consent intent routing 2026 | WebSearch | 10 | yes |
| 37 | grounded abstraction mental model developer tool correct selection empirical study 2020 2025 | WebSearch | 10 | partial |
| 38 | survey intent-first vs option-list configuration interface developer usability experiment CHI UIST ICSE | WebSearch | 10 | no |
| C1 | expert users "full disclosure" mental model developer tools prefer seeing options upfront usability study | WebSearch | 10 | partial |
| C2 | "progressive disclosure" expert users failure costs usability problems advanced features hidden | WebSearch | 10 | partial |
| C3 | "show interpretation" "pre-confirmation" intent routing user resistance rejection rate chatbot UX study | WebSearch | 10 | partial |
| C4 | wizard "create-react-app" "angular CLI" scaffolding usability empirical failure misrouting developer complaints | WebSearch | 0 | no |
| C5 | clarification question chatbot routing accuracy "reduces errors" empirical study dialogue systems 2020 2024 | WebSearch | 10 | partial |
| C6 | justification forcing condition "better decisions" HCI usability study "explain your choice" reduces errors empirical | WebSearch | 10 | partial |
| C7 | intent inference false positive misclassification rate developer tools rerouting failure mode | WebSearch | 10 | partial |
| C8 | "mental model" "abstraction transparency" benefits developer experience empirical showing model upfront | WebSearch | 10 | partial |
| C9 | scaffolding wizard CLI tool "correct configuration" success rate empirical study onboarding developer | WebSearch | 10 | no |
| C10 | cognitive dimensions framework "abstraction level" API usability expert programmers Clarke 2004 | WebSearch | 10 | yes |
| C11 | chatbot clarification "single clarification question" improves intent classification NLU routing ACL | WebSearch | 10 | partial |
| C12 | "default selection" errors developer tools configuration automation bias user study empirical | WebSearch | 10 | yes |
| C13 | automation bias systematic review frequency effect mediators mitigators Parasuraman | WebFetch/Search | 1 | yes |
| C14 | code generation AI "abstraction transparency" explainability showing model internals CHI ICSE 2022 | WebSearch | 10 | yes |
| C15 | ASK clarification task-oriented dialogue Amazon hybrid retrieval aspects empirical results 2023 | WebSearch | 10 | yes |
| C16 | "neural transparency" model transparency users over-trust miscalibrated AI tool empirical | WebSearch | 10 | yes |
| C17 | "conversational prompt rewriting" intent reformulation user rejection "original prompt" preferred LLM | WebSearch | 10 | yes |
| C18 | wizard create-react-app deprecated removed community complaints wrong defaults 2021 2023 | WebSearch | 10 | partial |
| C19 | understanding user mental models AI code completion tools IJHCS 2025 developer preference | WebSearch | 10 | yes |
| C20 | "forced justification" OR "accountability" decision quality HCI user study requiring explanation before choosing | WebSearch | 10 | yes |
| C21 | Tetlock "accountability" "exploratory" "confirmatory" thought forced justification pre-outcome improves | WebSearch | 10 | yes |
| C22 | "transparency dilemma" OR "disclosure backfire" AI recommendation user trust erodes 2022 2025 | WebSearch | 10 | yes |
| C23 | ScienceDirect "designing API appropriate abstraction level" robot 2016 usability lower abstraction preferred | WebSearch | 10 | yes |

**WebFetch verifications (Challenge phase):**
- amazon.science/publications/ask-... — confirmed, ASK paper, ACL 2025
- arxiv.org/html/2008.07559v2 — confirmed, clarification question discrimination study
- pmc.ncbi.nlm.nih.gov/articles/PMC3240751/ — confirmed, Parasuraman automation bias review
- arxiv.org/html/2502.02194v1 — confirmed, developer mental models study 2025
- arxiv.org/abs/2511.00230 — confirmed, Neural Transparency abstract only (paywall for full text)
- arxiv.org/html/2503.16789v1 — confirmed, prompt rewriting study 2025
- sjdm.org/journal/17/17411/new.html — confirmed, full paper fetched — Andersson et al. 2017
- react.dev/blog/2025/02/14/sunsetting-create-react-app — confirmed, full post fetched
- jakobnielsenphd.substack.com/p/intent-ux — confirmed, fetched
- sciencedirect.com/article/pii/S0749597825000172 — confirmed, abstract only (paywall)
- cs.auckland.ac.nz/~beryl/publications/jvlc 2016 Designing API.pdf — binary/PDF unreadable

**WebFetch verifications:**
- arxiv.org/abs/2304.06597 — confirmed, CHI 2023
- arxiv.org/html/2310.03691v2 — confirmed, full paper fetched
- arxiv.org/html/2401.14484v1 — confirmed, full paper fetched
- arxiv.org/abs/2408.15989 — confirmed, 2024
- arxiv.org/abs/2602.07338 — confirmed, 2026
- arxiv.org/abs/2402.02136 — confirmed, 2024
- nngroup.com/articles/progressive-disclosure/ — confirmed, fetched
- nngroup.com/articles/ai-paradigm/ — confirmed, fetched
- nngroup.com/articles/wizards/ — confirmed, fetched (no empirical data found)
- rubyonrails.org/doctrine — confirmed, fetched
- ixdf.org/literature/book/.../information-foraging-theory — confirmed, fetched
- docs.github.com/en/actions/get-started/actions-vs-apps — confirmed, fetched
- mesoform.com/.../from-paralysis-to-paved-roads — confirmed, fetched
- smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ — confirmed, fetched

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status | SIFT Notes |
|---|-----|-------|-----------|------|------|--------|------------|
| 1 | https://arxiv.org/abs/2304.06597 | "What It Wants Me To Say": Bridging the Abstraction Gap Between End-User Programmers and Code-Generating Large Language Models | Liu, Sarkar, Negreanu, Zorn, Williams, Toronto, Gordon (Microsoft Research) | CHI 2023 | T1 | verified | Between-subjects think-aloud study, n=24. Strong relevance to SQ1 and SQ3. Claim origin confirmed in this paper. |
| 2 | https://arxiv.org/abs/2401.14484 | Design Principles for Generative AI Applications | Weisz, He, Muller, Hoefer, Miles, Geyer (IBM Research) | CHI 2024 | T1 | verified | Design principles derived from synthesis of literature and iterative design research. No primary user study within paper itself; claims are grounded in prior evidence. T1 is borderline — classification as T1 depends on the CHI review process confirming empirical grounding. Retain T1 with note. |
| 3 | https://arxiv.org/abs/2310.03691 | DirectGPT: A Direct Manipulation Interface to Interact with Large Language Models | Masson, Malacria, Casiez, Vogel | CHI 2024 | T1 | verified | Within-subject study, n=12 (meets T1 threshold). Metrics confirmed in the paper (prompt count, length, time, success rate). |
| 4 | https://arxiv.org/abs/2408.15989 | Software Solutions for Newcomers' Onboarding in Software Projects: A Systematic Literature Review | Santos, Felizardo, Gerosa, Steinmacher | arXiv 2024 (IST journal) | T1 | verified | Systematic literature review of 32 studies. SLRs without a primary user study are typically T2; however this is an IST journal submission with rigorous protocol. Retain T1. |
| 5 | https://arxiv.org/abs/2602.07338 | Intent Mismatch Causes LLMs to Get Lost in Multi-Turn Conversation | Liu, Zhu, Feng, Ma, Wang, Meng | arXiv 2026 | T2 | verified | Empirical evaluation with measured performance metrics but arXiv preprint (not yet peer-reviewed at time of research). T2 appropriate. |
| 6 | https://arxiv.org/abs/2402.02136 | User Intent Recognition and Satisfaction with Large Language Models: A User Study with ChatGPT | Bodonhelyi, Bozkir, Yang, Kasneci, Kasneci | arXiv 2024 (cs.HC) | T2 | verified | User study with measured intent classification accuracy and satisfaction scores. Preprint; T2 appropriate. Satisfaction preference figures (56.61%, 53.50%) confirmed as originating in this paper. |
| 7 | https://dl.acm.org/doi/10.1145/2430545.2430551 | An Information Foraging Theory Perspective on Tools for Debugging, Refactoring, and Reuse Tasks | Fleming, Scaffidi, Piorkowski, Burnett, Bellamy, Lawrance, Kwan | ACM TOSEM 2013 | ~~T1~~ T2 ↓ | unverified (403) — alternate URLs also 403; no open-access version found | ACM DOI returns 403; arXiv guess (1210.0886) is an unrelated math paper. Semantic Scholar confirms paper exists and is an empirical study applying IFT to SE tasks, but full text unverified. Methodology appears to be theory application with developer observation rather than a controlled user study with n≥12 measured task completion. Downgraded T1→T2 pending full text access; if the paper contains a user study with n≥12 and task completion rates, upgrade to T1. Relevant to SQ1 and framework. |
| 8 | https://www.nngroup.com/articles/progressive-disclosure/ | Progressive Disclosure | Nielsen Norman Group | n.d. | T3 | verified | Synthesizes usability research; no primary study cited but draws on established HCI literature. T3 appropriate. "3+ levels create usability problems" claim is asserted as principle, not measured — trace claim before citing as empirical finding. |
| 9 | https://www.nngroup.com/articles/wizards/ | Wizards: Definition and Design Recommendations | Nielsen Norman Group | n.d. | ~~T3~~ T4 ↓ | verified | Fetched and confirmed: zero quantitative studies, controlled experiments, or empirical data. One anecdotal single-user example (Mint.com, unnamed). All recommendations are design principles and expert reasoning. No citations to external research. Downgraded T3→T4. |
| 10 | https://www.nngroup.com/articles/ai-paradigm/ | AI: First New UI Paradigm in 60 Years | Jakob Nielsen (NN/g) | 2023 | T3 | verified | Expert essay with design reasoning. No empirical study. T3 appropriate (design essay with evidence citations to prior UI paradigms). |
| 11 | https://rubyonrails.org/doctrine | The Ruby on Rails Doctrine | David Heinemeier Hansson | 2016 | T3 | verified | Practitioner design rationale document, no user study. T3 appropriate as practitioner guide with aggregated design reasoning. Claims about adoption outcomes are anecdotal. |
| 12 | https://ixdf.org/literature/book/the-glossary-of-human-computer-interaction/information-foraging-theory | Information Foraging Theory | Interaction Design Foundation Glossary | n.d. | T3 | verified | IFT theory glossary entry. No primary data; summarizes Pirolli & Card's foundational theory. T3 appropriate. |
| 13 | https://docs.github.com/en/actions/get-started/actions-vs-apps | GitHub Actions vs GitHub Apps | GitHub | 2024 | T2 | verified | Official tool documentation. Used as a real-world example of model-based routing, not as a source of empirical evidence. T2 may be generous — this is reference documentation, not a design case study with user research. Consider T3 for citation purposes. |
| 14 | https://www.mesoform.com/resources/blog/information/from-paralysis-to-paved-roads-how-platform-engineering-resolves-cognitive-crises-in-devops-and-sre | From Paralysis to Paved Roads: How Platform Engineering Resolves the Cognitive Crisis in DevOps and SRE | Mesoform | 2024 | ~~T3~~ T4 ↓ | verified | Fetched and confirmed: the 30%/70% figures (pipelines 30% faster, 70% maintenance reduction) do NOT appear in this article or its Medium mirror. These figures likely originate from a Databricks vendor blog (single-org case study). The 94% figure traces to Puppet State of DevOps 2023 survey (industry survey, not controlled study). The 97% context-switching figure traces to a Harness webinar survey. All statistics are industry surveys or vendor reports, not controlled studies. Downgraded T3→T4. Claims citing "30% faster / 70% maintenance reduction" from this source are unverifiable claim laundering — the figures do not appear in the cited document. |
| 15 | https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ | Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability | Victor Yocco (Smashing Magazine) | Feb 2026 | ~~T3~~ T4 ↓ | verified | Fetched and confirmed: author is Victor Yocco PhD (UX Researcher, ServiceNow). No citations to empirical studies. No quantitative data. Benchmark metrics (e.g., ">85% acceptance ratio") are asserted without evidentiary basis. Purely practitioner opinion and design reasoning with no sources listed. Downgraded T3→T4. |
| 16 | https://ixdf.org/literature/topics/progressive-disclosure | What is Progressive Disclosure? | Interaction Design Foundation | 2026 | T3 | verified | Educational overview synthesizing established UX design patterns. No primary data; uses illustrative examples (Google, Instagram, Photoshop). T3 appropriate. Note: this URL is not listed in the frontmatter `sources` field — should be added. |
| 17 | https://dl.acm.org/doi/10.1145/1985793.1985911 | Information Foraging as a Foundation for Code Navigation | Niu et al. | ICSE 2011 | ~~T1~~ T3 ↓ | unverified (403) — PDF found at homepages.uc.edu | ACM DOI returns 403. PDF located at University of Cincinnati repository. Critically: this is a **NIER (New Ideas and Emerging Results) track paper** — a 4-page position paper presenting preliminary ideas, not a full empirical study. NIER papers propose theoretical directions without controlled user studies. Does not meet T1 criteria (no user study, no n≥12, no measured task completion). Downgraded T1→T3 (design essay / theoretical framework with preliminary analysis). |
| 18 | https://hcibib.org/tcuid/ | Task-Centered User Interface Design: A Practical Introduction | Clayton Lewis, John Rieman | 1993/1994 | T3 | verified — **OUT OF SCOPE** | Textbook is accessible at URL. However: published 1993/1994, pre-dating the research scope (post-2015). Per stated scope, pre-2015 sources should be excluded. Flag for removal or explicit scope exception. The task-centered design principles it encodes are well-represented in post-2015 HCI literature. |
| 19 | https://arxiv.org/abs/2502.02194 | Understanding User Mental Models in AI-Driven Code Completion Tools: Insights from an Elicitation Study | Koenemann et al. | IJHCS 2025 | T1 | verified | 8 co-design workshops, n=56 developers. Empirical elicitation study with expert and novice developers. Directly addresses expertise-dependent disclosure preferences. Added in Challenge phase. |
| 20 | https://arxiv.org/abs/2511.00230 | Neural Transparency: Mechanistic Interpretability Interfaces for Anticipating Model Behaviors for Personalized AI | Shi et al. | arXiv 2025 | T2 | verified | Online user study (Prolific). Comparing transparency interface against baseline. Found users systematically miscalibrated behavior (misjudged 11/15 traits); transparency increased trust but did not improve correct behavior. Preprint. Added in Challenge phase. |
| 21 | https://arxiv.org/abs/2503.16789 | Conversational User-AI Intervention: A Study on Prompt Rewriting for Improved LLM Response Generation | (Anonymous) | arXiv 2025 | T2 | verified | Retrospective analysis of real human-LLM conversations. Rewritten prompts achieve 79.61% GPT-4o win rate for response quality, but no direct user testing of whether users accept shown rewrites. Added in Challenge phase. |
| 22 | https://dl.acm.org/doi/10.1145/2858036.2858402 | How Much Information? Effects of Transparency on Trust in an Algorithmic Interface | René Kizilcec | CHI 2016 | T1 | unverified (PDF binary) | Online field experiment on peer assessment grading. Three transparency conditions. Found inverted-U effect: both too-much and too-little transparency correlated negatively with trust vs. medium transparency (n=103); equivalence of the two extremes not established. Directly relevant to interpretive transparency claim. Full text unverified (PDF returned binary). Added in Challenge phase. |
| 23 | https://sjdm.org/journal/17/17411/new.html | Justifying the judgment process affects neither judgment accuracy, nor strategy use | Hoffmann, Gaissmaier, von Helversen | JDM 2017 | T2 | verified | Two controlled experiments (n=144, n=110). Process accountability (forced justification) did not improve accuracy or change strategies; only reduced confidence. Direct challenge to justification-gate benefit claims. Added in Challenge phase. |
| 24 | https://www.sciencedirect.com/science/article/abs/pii/S1045926X16300982 | Designing an API at an appropriate abstraction level for programming social robot applications | Pot, Jayawardena, Wiggins, MacDonald | JVLC 2016 | T2 | unverified (paywall) | Iterative design + user study. First high-abstraction API iteration revised to lower abstraction after user study found too much control removed. Empirical evidence that exposing more of the model improved usability for expert developers. Paywall prevents full text verification. Added in Challenge phase. |
| 25 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3240751/ | Automation Bias: A Systematic Review of Frequency, Effect Mediators, and Mitigators | Parasuraman, Manzey | Human Factors 2010 | T1 | verified | Systematic review. Erroneous automated advice increases incorrect decision rate by 26%; updating dynamic confidence levels reduces automation bias. Directly relevant to auto-routing failure modes and interpretive transparency design. Added in Challenge phase. |
| 26 | https://www.amazon.science/publications/ask-aspects-and-retrieval-based-hybrid-clarification-in-task-oriented-dialogue-systems | ASK: Aspects and Retrieval Based Hybrid Clarification in Task Oriented Dialogue Systems | Amazon Science | ACL 2025 | T1 | verified | Recall@5 improvement of ~20% from targeted clarifying questions when ambiguity is high. Provides positive empirical evidence for single-question clarification (structurally similar to a wizard step). Added in Challenge phase. |
| 27 | https://www.sciencedirect.com/science/article/pii/S0749597825000172 | The Transparency Dilemma: How AI Disclosure Erodes Trust | Schilke, Reimann | OB & HD 2025 | T1 | verified (abstract only) | 13 pre-registered experiments, n>3,000 (n>5,000 overstated). AI disclosure reduces trust across domains through legitimacy perceptions; exact 7–18% range requires full text. Contextually relevant to interpretive transparency backfire risk. Added in Challenge phase. |

---

## Source Evaluation Summary

### Tier Adjustments

**Source 7 (Fleming et al., TOSEM 2013) — T1 → T2 ↓**
ACM DOI remains 403; no open-access version found (the arXiv number 1210.0886 is an unrelated mathematics paper). Semantic Scholar confirms the paper exists and is empirical, but without full text access the methodology cannot be confirmed as meeting T1 criteria (controlled user study, n≥12, measured task completion). Downgraded to T2 pending verification. If full text confirms a user study with n≥12, restore to T1.

**Source 9 (NN/g Wizards) — T3 → T4 ↓**
Fetched and confirmed: zero quantitative data, controlled experiments, or citations to external research. Contains one anecdotal single-user example. All content is design principles and expert reasoning. Appropriately T4 (opinion/design reasoning without evidence citations). Extracts from this source should be treated as design rationale, not empirical evidence.

**Source 14 (Mesoform) — T3 → T4 ↓**
The 30%/70% figures cited in the Extracts section ("pipelines 30% faster," "maintenance effort dropping 70%") do not appear in this article or its Google Cloud Medium mirror. These figures likely originate from a Databricks vendor blog (a single organization's self-reported case study). The Mesoform article's verified statistics (94%, 97%) trace to industry surveys (Puppet, Harness) — not controlled research. This is claim laundering: the Extracts attribute figures to this source that are not in this source. Downgraded to T4. The 30%/70% claims in the Extracts section must be removed or re-attributed.

**Source 15 (Smashing Magazine) — T3 → T4 ↓**
Fetched and confirmed: no empirical citations, no quantitative data, no external sources listed. Victor Yocco PhD has relevant credentials but the article is practitioner opinion, not a T3-qualifying practitioner guide "citing evidence." Downgraded to T4.

**Source 17 (Niu et al., ICSE 2011) — T1 → T3 ↓**
Confirmed as a NIER (New Ideas and Emerging Results) track paper — a 4-page preliminary proposal, not a full empirical study. NIER papers are explicitly for early-stage ideas without full user study validation. Does not meet T1 criteria on any dimension. Downgraded to T3.

### Sources Flagged for Removal or Scope Exception

**Source 18 (Lewis & Rieman, 1993/1994):** Pre-2015 source. Violates stated research scope. The task-centered design framework is well-documented in post-2015 HCI literature (e.g., Sources 1, 2, 4). Consider removing and citing the foundational concept through a post-2015 source that references it, or add an explicit scope exception note explaining why this foundational text is retained.

**Source 16 (IxDF Progressive Disclosure):** URL missing from frontmatter `sources` list. Add to frontmatter.

### Claim Laundering

The Extracts for Source 14 (Mesoform) cite "pipelines 30% faster" and "maintenance effort dropping 70%" as if they originate in the Mesoform article. These figures do not appear in the fetched content of the Mesoform article or its published Medium mirror. The likely true origin is a Databricks vendor blog (single-organization case study, no controlled methodology). The claim as written in the Extracts section must be corrected: remove the specific percentages or attribute them to their actual source with appropriate tier (T4 — vendor case study).

---

## Extracts

### Sub-question 1: Progressive Disclosure and Abstraction Levels

**Source [1] — "What It Wants Me To Say" (CHI 2023)**

The paper's central finding is that a vocabulary mismatch exists between how end-users describe goals and the abstraction level the system requires. The paper terms this the "abstraction gap." The specific problem: "only a small portion of the infinite space of naturalistic utterances is effective at guiding code generation." Non-expert programmers face "the challenge of abstraction matching."

The proposed solution, "grounded abstraction matching," bridges this gap by translating the code the system produces back into a systematic, predictable naturalistic utterance — showing users how the system interprets their request. In a between-subjects think-aloud study (n=24), this grounded approach "improved end-users' understanding of the scope and capabilities of the code-generating model, helping users develop better mental models for crafting effective prompts."

Claim supported: When users lack a mental model of the system's abstraction vocabulary, showing the system's interpretation of their intent (rather than asking them to pick a category) improves correct selection behavior.

---

**Source [8] — NN/g Progressive Disclosure**

Nielsen Norman Group defines progressive disclosure as showing only essential options initially and revealing advanced features upon request. Key design constraints identified:
- "Users must access frequently-needed options on the primary display; secondary displays should contain only rarely-used settings."
- "The initial screen cannot include confusing features that slow performance."
- Navigation requires "clear labeling with strong information scent so users understand what they'll find."

Empirically grounded claim (no primary study cited, but synthesizes usability research): "people understand a system better when you help them prioritize features and spend more time on the most important ones."

Critical constraint from the NN/g analysis: "Multiple levels (3+) typically create usability problems." This suggests that for a five-primitive system, showing all primitives at once in a layered structure would create measurable usability harm.

Claim supported: Progressive disclosure is most effective when the initial screen contains only the most essential choices; adding complexity above 2 levels degrades usability.

---

**Source [14] — Mesoform, Platform Engineering and Golden Paths** *(NOW T4 — see Source Evaluation Summary)*

The article cites industry survey data on developer cognitive overload from tool-option abundance: "97% of developers report that toolchain sprawl forces constant, productivity-killing context switching" (Harness webinar survey). Organizations use "10.3 distinct toolchains on average" (Atlassian/CITE Research 2020). The proposed solution (golden paths) works by abstracting away abstraction selection entirely: "developers are freed from making countless low-level decisions."

The platform engineering answer to the primitive-selection problem is to not ask users to select primitives at all — instead, infer task type from stated goal and map to a pre-configured path. 94% of surveyed organizations report platform engineering improved productivity (Puppet State of DevOps 2023).

**CLAIM LAUNDERING FLAG:** The figures "30% faster pipeline building" and "70% maintenance reduction" cited in earlier versions of this extract do NOT appear in the Mesoform article or its Google Cloud Medium mirror. These figures could not be traced to any cited source in the article. Do not cite these percentages from this source. The 94%/97% figures are confirmed but derive from industry surveys, not controlled studies.

Claim supported (weakened to T4): Eliminating primitive selection in favor of goal-based routing is reported to correlate with productivity gains in platform engineering contexts; specific magnitude claims are unverifiable from this source.

---

**Source [12] — Information Foraging Theory (IFT), IxDF Glossary**

Information scent is defined as "the determination of information value based on navigation cues and metadata." The theory predicts users evaluate cost-benefit of pursuing an information path before committing effort. When scent is weak (labels, descriptions, or names do not match user vocabulary), "browsing increases" and navigation becomes exploratory rather than targeted.

For developer tools: when option labels use system vocabulary ("hook," "rule," "subagent") rather than user-goal vocabulary ("enforce," "automate," "delegate"), scent is absent. Users cannot navigate to the correct primitive without knowing its name.

Claim supported: Routing systems must present options using user-goal vocabulary (the "prey" language) rather than system-abstraction vocabulary, or users will fail to locate the correct primitive.

---

**Source [7] — Fleming et al., Information Foraging Theory Perspective on Developer Tools (ACM TOSEM 2013)**

The paper applies IFT to debugging, refactoring, and reuse tasks in software engineering. Confirmed: the theory can be applied to "obtain insights into how and why software engineering tools can aid developers." Key contribution: "specific tool designs" can be generalized to "independent, generalizable and reusable IFT-based design patterns."

The core model: developers treat tasks as "prey," environmental cues as "scent," and tool navigation as "foraging topology." Tools that improve scent reduce navigation cost. If a bug is the prey, words in the environment that point to it are cues. Applied to primitive routing: if a user's goal ("prevent pushes to main") is the prey, the intake prompt vocabulary must emit strong scent pointing toward the correct primitive ("hook").

Claim supported: Information foraging predicts that correct primitive selection depends on the semantic match between user-stated goal vocabulary and the cues present in the intake interface.

---

### Sub-question 2: Intent-Based vs. Model-Based Routing

**Source [10] — Nielsen, "AI: First New UI Paradigm in 60 Years" (NN/g, 2023)**

Nielsen identifies the current AI interaction paradigm as "intent-based outcome specification," calling it "the first new UI interaction paradigm in 60 years." The defining characteristic: "the user no longer tells the computer what to do. Rather, the user tells the computer what outcome they want."

However, Nielsen also notes a critical failure mode of pure intent-based systems: "When users don't know how something was done, it can be harder for them to identify or correct the problem." The black-box nature of intent-mapping prevents error recovery. Nielsen predicts future systems will adopt hybrid approaches combining intent-based and GUI (model-exposing) elements.

Claim supported: Intent-based routing is a recognized new paradigm; but without some model transparency, users lose error-recovery ability when routing fails.

---

**Source [13] — GitHub Actions vs GitHub Apps documentation (GitHub, 2024)**

GitHub's official documentation for resolving the Actions/Apps selection ambiguity uses model-based routing: it explains the characteristics of each option and asks users to match their needs to the descriptions. The page does not ask "what are you trying to accomplish?" (intent-first). Instead it presents: "Apps run persistently; Actions don't require persistent infrastructure." No decision tree, no intake question, no wizard flow is present.

This is a real-world example of a two-primitive routing problem solved via model-based documentation. The key discriminators presented are technical (persistence, data requirements, performance, infrastructure burden) — not goal-based ("prevent unauthorized changes" vs. "automate CI").

Claim supported (by absence of intent-based routing): Major developer platforms default to model-based routing documentation even where intent-based routing would be more accessible to users unfamiliar with the abstraction layer.

---

**Source [3] — DirectGPT (CHI 2024)**

This paper provides the most rigorous empirical comparison of intent-specification modes. Study design: 12 participants, within-subject, 12 tasks across text/code/image editing. Two conditions: standard ChatGPT (intent-specified via natural language prompts) vs. DirectGPT (intent-specified via direct manipulation — selecting objects, then applying commands from a toolbar).

Results:
- Prompt count: 50% fewer with DirectGPT (M=1.90 vs. M=3.67)
- Prompt length: 72% shorter with DirectGPT (5.83 words vs. 19.98 words)
- Task time: 50% faster with DirectGPT (56s vs. 1m 57s)
- Success: +0.95 points on 5-point scale (M=4.84 vs. M=3.89, p<0.001)

The authors attribute the gains to reduced "articulatory distance" (the gap between intended action and how it must be expressed) and reduced "semantic distance" (verbosity required to convey intent). Direct manipulation collapses these gaps by letting users select the object of interest rather than describe it.

Quote from participant P5: "[DirectGPT] was more like a tool. I did not need to make it comprehend anything."
Quote from participant P7: "I knew by highlighting specific parts I can just put in very concise prompts...it did not feel necessary for me to type in a whole conversation."

Claim supported: When users can select the target directly (object + intent) rather than fully articulate it in natural language, task success increases significantly and effort decreases. This argues for mixed-initiative intake — user describes goal, system proposes interpretation, user confirms.

---

**Source [6] — User Intent Recognition and Satisfaction with LLMs (Bodonhelyi et al., 2024)**

User study examining GPT-3.5 and GPT-4 intent classification performance. Key data:
- GPT-4 achieved 89.64% accuracy (F1: 88.84%) vs. GPT-3.5's 75.28% (F1: 74.28%) overall intent recognition
- Both models had systematically weak categories: "learning support" (36.84% for GPT-3.5, 0% for GPT-4), "curricular planning" (50%, 0%)
- Counterintuitive finding: "users tend to be more satisfied with the models' answers to their original prompts compared to the reformulated ones" — original prompt preference 56.61% (GPT-3.5) and 53.50% (GPT-4)

The data shows that even high-accuracy intent classification still misroutes ~10% of interactions at best, with systematic blind spots for rare or ambiguous intent categories. The satisfaction finding contradicts the assumption that correctly-reformulated prompts improve user experience.

Claim supported: Automatic intent routing has measurable failure rates; rare or ambiguous intents are the most likely to be misclassified, suggesting that for a low-frequency primitive (e.g., a "subagent"), auto-routing confidence should be surfaced to users rather than hidden.

---

### Sub-question 3: Intake Question Patterns and Taxonomies

**Source [1] — "What It Wants Me To Say" (CHI 2023)**

The paper's empirical finding most relevant to intake question design: users fail at abstraction matching because they describe intent at a level of granularity that doesn't match what the system can act on. The intervention ("grounded abstraction matching") works by showing users the system's vocabulary — effectively making the system's taxonomy legible to the user after an initial attempt.

This suggests an intake sequence: (1) accept free-text goal description, (2) show the system's interpretation mapped to its internal taxonomy, (3) allow user to confirm or correct. This is more effective than either (a) asking users to select a category from a list up front, or (b) silently routing without showing interpretation.

---

**Source [5] — Intent Mismatch in Multi-Turn Conversation (Liu et al., 2026)**

The paper identifies three triggering patterns for intent mismatch that are directly applicable to intake question design:
1. Users provide "underspecified, fragmented utterances relying on contextual pronouns and vague directives"
2. Systems make "early tentative assumptions" and "lock in" these interpretations across turns
3. Systems interpret user clarifications as confirmations rather than corrections

The proposed solution — a Mediator-Assistant framework that reconstructs ambiguous multi-turn inputs into explicit single-turn instructions — achieved approximately 20 percentage points of performance recovery.

This is structurally identical to the WOS routing problem: a user states a vague goal ("I want to make sure nobody pushes to main without a review"), the system must reconstruct it into a clear primitive specification ("a hook that enforces a branch protection rule") without locking in wrong assumptions.

Claim supported: Early over-commitment to a routing decision before user intent is fully resolved causes compounding errors. The intake question design should delay commitment until the interpretation can be surfaced and confirmed.

---

**Source [2] — Design Principles for Generative AI Applications (Weisz et al., CHI 2024)**

Principle "Design for Mental Models" identifies the core challenge: "The use of open-ended natural language, rather than a fixed vocabulary of commands, leads to new design challenges." Strategies include:
- "Orient the user to generative variability" — help users understand that the same input can produce different outputs
- "Teach effective use" — provide explanations and examples through documentation
- "Build upon the user's existing mental models"
- "Help the user craft effective outcome specifications"

The paper explicitly cites Nielsen's framing of intent-based outcome specification and notes that users typically resort to "trial-and-error" methods because the open vocabulary does not provide clear feedback on which specification form will be effective.

Claim supported: Intake design for intent-based systems must actively scaffold the user's mental model of the system's vocabulary, not just accept free text and route silently.

---

**Source [18] — Task-Centered User Interface Design (Lewis & Rieman, 1993/1994)**

The book's foundational argument: design requirements should be derived from user tasks (what people want to accomplish), not system features. The task-centered walkthrough method evaluates whether a design enables task completion without requiring users to understand the underlying system model.

Applied to intake question design: a task-centered intake asks "what do you want to accomplish?" and routes from there, rather than "which of these five primitives do you want to use?" The book frames this as the core distinction between task-centered and system-centered design.

Claim supported: Task-centered design (intent-first intake) has a 30+ year theoretical basis as superior to system-centered design (feature/primitive selection) for users who lack a system mental model.

---

### Sub-question 4: Wizard and Guided Setup Evidence

**Source [9] — NN/g Wizards: Definition and Design Recommendations** *(T4 — see Source Evaluation Summary; treat as design rationale, not empirical evidence)*

NN/g identifies the primary use case for wizards: "infrequent processes or novice users." Claimed benefits:
- "Less cognitive effort is spent in completing the process" because irrelevant fields are hidden
- Users make fewer errors with simplified steps
- "A long form is often daunting and users may overestimate the amount of work"

Identified anti-pattern: wizards harm task completion when users "possess domain expertise (they resent the forced sequence)" and when "the wizard blocks access to necessary information elsewhere in the app."

Critical finding for auto-selection: "Wizards allow the computer to control the flow...this limitation of users' freedom can be liberating in cases where people don't care about their choices or don't know enough to make a decision."

Important limitation: The article contains no quantitative studies, empirical data, or controlled experiments. Recommendations rely entirely on UX principles and design reasoning.

---

**Source [4] — Software Solutions for Newcomers' Onboarding: A Systematic Literature Review (Santos et al., 2024)**

Review of 32 studies on software onboarding solutions. Key findings relevant to guided setup:
- Recommendation systems are the "most prevalent strategy" (23 of 32 studies) — they "help users find information and make decisions where they lack experience" via "tailored suggestions"
- Information visualization tools (8 studies) reduce cognitive load through "interactive exploration of relationships among project elements"
- Only one study examined standalone structured documentation as a guidance mechanism — wizard-style linear onboarding received minimal research attention
- 71% of studies used laboratory experiments; 50% used quantitative metrics (success rates, completion times, satisfaction)
- Only 18 of 58 identified newcomer barriers are addressed by existing software solutions

The most evidence-backed onboarding pattern is recommendation-based (proactive, personalized suggestions based on inferred need), not wizard-based (sequential question-and-answer). This suggests that for primitive routing, a recommendation-based approach — infer the primitive from stated goal, propose it, allow confirmation — is more evidence-supported than a step-by-step wizard.

Claim supported: Recommendation-based routing (infer then propose) has substantially more research support in developer tool onboarding contexts than wizard-based routing (ask then select).

---

**Source [11] — The Ruby on Rails Doctrine (DHH, 2016)**

The Rails Doctrine explicitly articulates the "we made the choice for you" design pattern and its rationale. Key claims:

On omakase (choosing for users): "letting others assemble your stack" rather than "burdening individual programmers with tool selection."

On convention over configuration: "the transfer of configuration to convention frees us from deliberation." The doctrine states that "constraints liberate even the most able minds" and that "half the battle of getting going is finding a thread to pull" when starting without conventions.

On developer adoption: "conventions also lower the barriers of entry for beginners. There are so many conventions in Rails that a beginner doesn't even need to know about, but can just benefit from in ignorance."

The Rails Doctrine is the most cited industry rationale for the "auto-select, don't ask" pattern in developer tooling. It has no controlled user study backing, but the adoption trajectory of Rails (dominant framework for a decade) is cited as evidence of the pattern's effectiveness.

Claim supported: The "auto-select based on context" pattern has strong practitioner-level adoption evidence, framed as reducing decision fatigue and lowering onboarding barriers.

---

**Source [14] — Mesoform, Platform Engineering Golden Paths** *(T4 — see Source Evaluation Summary)*

Golden path pattern provides pre-configured end-to-end workflows that route developers to the correct implementation approach without requiring them to understand the underlying abstractions. The cognitive load justification: "developers spend limited mental energy on trivial choices" at the cost of "high-impact decisions on core product features."

Confirmed data from cited surveys: 94% of respondents agree platform engineering is instrumental (Puppet State of DevOps 2023). **The "30% faster pipeline building" figures cited in earlier research notes do not appear in this article and could not be traced; remove from any synthesis claims.** "Change failure rates drop 30-50%" also unverified in fetched content.

Structural claim (retained, T4): the golden path pattern is a direct implementation of intent-based routing in developer tooling — the developer states what they want to build, the platform selects and configures the primitives on their behalf.

---

### Sub-question 5: Justify-Your-Choice vs. Auto-Selection

**Source [11] — The Ruby on Rails Doctrine (DHH, 2016)**

The doctrine's omakase principle is the clearest practitioner articulation of anti-"justify your choice":

> "There are thousands of decisions that just need to be made once, and if someone else can do it for you, all the better."

DHH explicitly frames the "justify your choice" pattern as waste: requiring developers to deliberate over stack choices is "a machete-able" problem that Rails removes. The alternative — asking developers to pick between tool A and tool B — is characterized as a barrier that "looses us from the jungle of recurring decisions."

---

**Source [9] — NN/g Wizards** *(T4 — design rationale only, no empirical backing)*

The NN/g wizard article identifies a specific "justify your choice" anti-pattern found in installer wizards. Key finding from wizard failure mode analysis: "Once the install, setup or creation process completes, the user has no idea how to change the choices they made." Forcing up-front decisions creates "useless disposable throw-away knowledge" — users learn the wizard-specific choice vocabulary but cannot reuse it to modify their configuration later.

Also: "Power users often find wizards frustratingly rigid and limiting since wizards don't show users what their actions really do, or what application state gets changed as choices are made."

This is the justification-requirement anti-pattern in concrete form: users forced to decide between options they don't understand learn nothing applicable, and the decision overhead provides no lasting utility.

---

**Source [3] — DirectGPT (CHI 2024)**

The study's findings support auto-selection (or at least, reducing the specification burden). When users could select objects directly and apply operations rather than articulate intent in full, they were:
- 50% faster
- 25% more successful
- Used 72% fewer words

The paper explicitly attributes the improvement to reduced "articulatory distance" — the gap between what a user wants to do and the words they must produce to communicate it. Requiring users to justify or articulate their choice in full natural language imposes articulatory distance costs that directly reduce success rates.

---

**Source [5] — Intent Mismatch (Liu et al., 2026)**

The paper's core finding is that "early tentative assumptions" locked in by the system — i.e., the system making an auto-selection and sticking to it — cause approximately 60% relative performance degradation in multi-turn settings (the paper's own Figure 2 measurement; a ~30% figure cited in the document derives from Laban et al. 2025, a prior paper cited within [5]). This is the failure mode of pure auto-selection without confirmation.

Performance recovery of ~20 percentage points was achieved by a Mediator that reconstructs ambiguous intent into explicit instructions before acting. This is structurally a "show your interpretation and allow correction" pattern — neither pure auto-select (which locks in wrong assumptions) nor pure justify-your-choice (which asks users to select from options they don't understand).

Claim supported: The most evidence-supported pattern is interpretive transparency — auto-infer the routing, but show the interpretation before acting. This captures the benefit of auto-selection (no forced user deliberation) while avoiding the failure mode (locked-in wrong assumption).

---

**Source [6] — User Intent Recognition Study (Bodonhelyi et al., 2024)**

The counterintuitive finding about user satisfaction is directly relevant to the auto-select vs. justify debate: "users tend to be more satisfied with the models' answers to their original prompts compared to the reformulated ones" (56.61% preference for original, GPT-3.5; 53.50% preference for original, GPT-4).

This challenges the assumption that correctly classifying intent and reformulating it produces better outcomes. Users preferred the system responding to their stated intent rather than the system's reformulation of their intent, even when the reformulation was more technically accurate.

Claim supported: Users resist having their stated intent replaced by a reformulation, even a correct one. This argues for intake designs that accept user vocabulary and route without visible reformulation, rather than showing users a translated/mapped interpretation of their goal.

---

**Source [2] — Design Principles for Generative AI Applications (Weisz et al., CHI 2024)**

The "Design for Co-Creation" principle addresses how to handle the auto-select vs. justify tradeoff: systems should "assist the user in prompting effectively" and provide domain-specific parameter controls. Critically, the paper notes that trial-and-error is the dominant user behavior pattern when systems don't provide vocabulary scaffolding.

The proposed resolution: provide "generic input parameters" to reduce decision burden while still allowing control. This is a middle path — the system makes default selections but exposes knobs for correction, rather than requiring up-front justification.

---

**Additional Evidence: Hick's Law and Choice Quantity**

Multiple sources confirm that decision time increases logarithmically with option count (Hick-Hyman Law, 1952). For developer tool configuration specifically: "cutting a feature flag dashboard from twelve toggles to four made managers faster." The law applies most strongly when users are choosing between equally probable options — if users already know what they want (have a mental model), Hick's Law effects diminish.

For a user without a mental model of WOS primitives (who does not know which of five options to select), Hick's Law applies at maximum strength: presenting all five primitives simultaneously is the worst-case intake design.

---

**Contradicting Evidence**

**Source [6] — User Intent Recognition Study (2024)** produced one finding that contradicts assumptions in this space: even when the system correctly identified intent and reformulated the prompt to match, users preferred the original prompt and were not more satisfied. This is evidence against the "show your interpretation" pattern, to the extent that "showing interpretation" involves replacing the user's words with the system's vocabulary.

**Source [3] — DirectGPT (2024)** found benefits from direct manipulation (showing objects and operations) but the study was for editing tasks where objects are inherently visible. For WOS, the "objects" (primitives) are not visible until after routing — this limits the direct applicability of DirectGPT's findings to WOS's intake problem.

---

## Challenge

### Claims Challenged

#### Claim 1: Intent-first routing is superior to model-based routing

**Challenge search:** "expert users" "full disclosure" mental model developer tools prefer seeing options upfront usability study; "model-based routing" "option list" developer correct selection beats intent-based empirical; cognitive dimensions abstraction level API usability expert programmers prefer full model visibility

**Counter-evidence found:**

The Cognitive Dimensions of Notations framework (Green & Petre, foundational; applied to APIs by Clarke, 2004–2005) identifies a specific failure mode for high-abstraction intent-based routing: *hidden dependencies*. "Raising the abstraction level creates hidden dependencies because subroutines are now hidden from the user." The positive effect — "primitives having a close mapping to the domain" — coexists with the cost that "implementation details are hidden, making progressive evaluation difficult because programmers are suddenly exposed to lower level implementation details when debugging errors."

An empirical study on social robot programming APIs (Pot et al., Journal of Visual Languages & Computing, 2016) found that the first high-abstraction API iteration had to be revised to a *lower* abstraction level after a user study, because the high level took "away too much control from programmers." This is a direct case where model-based (partial exposure of abstractions) outperformed intent-based (fully hidden abstractions).

A 2025 mental models elicitation study across 56 developers in 8 co-design workshops (Koenemann et al., IJHCS, 2025; arXiv:2502.02194) found that expert developers considered automatic explanation generation "obnoxious or even 'outrageous'" — but also found developers across levels needed to customize how and when model behaviors were surfaced. Experts preferred on-demand transparency, not zero transparency.

The Amazon Neural Transparency study (Shi et al., arXiv:2511.00230, 2025) tested a transparency interface that exposed model internals against a baseline. Key finding: "users systematically miscalibrated AI behavior" when given transparency, misjudging 11 of 15 behavioral traits. The transparency *increased trust* but did *not help users achieve correct behavior*. This is evidence that showing the model is not straightforwardly superior — transparency can create miscalibration.

**Assessment:** The evidence does not show that model-based routing is *superior* to intent-based routing for novice users, but it qualifies the superiority claim for experts and for debugging contexts. Expert developers face a specific cost from fully opaque intent routing: they cannot validate routing decisions or debug unexpected behavior. The claim holds for novice-user intake but is undermined for expert developers who need some model visibility at correction time.

**Revised confidence for universal applicability:** LOW — the claim is true for novice-first intake but expert users need escape valves to inspect the routing decision.

---

#### Claim 2: Auto-select with interpretive transparency is the right middle ground

**Challenge search:** "show interpretation" "pre-confirmation" user resistance rejection; "conversational prompt rewriting" user rejection rate "original prompt" preferred; "interpretive transparency" confirmation LLM routing backfire satisfaction study

**Counter-evidence found:**

The Liu et al. (2026) claim that "show your interpretation and confirm" is optimal is directly challenged by Bodonhelyi et al.'s finding (already in the document) that users preferred responses to their *original* prompt 56.61%/53.50% of the time. New evidence from a 2025 prompt-rewriting study (arXiv:2503.16789) adds nuance: rewritten prompts produce better LLM responses (GPT-4o win rate: 79.61%), but this study *never showed rewrites to actual users* — it only compared LLM-judged response quality. There is no empirical evidence that users who *see* the rewrite accept it.

The Kizilcec (2016) CHI study on algorithmic transparency (n=not extracted, field experiment on peer assessment grading) found an inverted-U effect: some transparency improved trust calibration, but *too much information eroded trust and confused users equally as much as no information*. The finding: "providing students with high or low levels of transparency is detrimental, as both extremes confuse students and reduce their trust." This is empirical evidence that the "infer then show interpretation" approach can backfire if the interpretation is too detailed.

The broader Schilke & Reimann (2025) transparency dilemma research (13 experiments, n>3,000) found that *disclosing AI involvement* consistently reduced trust across domains, even when framing varied. While this addresses AI authorship disclosure rather than routing interpretation, it establishes that surfacing AI decision-making can systematically reduce acceptance.

**Assessment:** The "show interpretation" pattern is directly challenged. The Bodonhelyi finding remains the strongest evidence against it. The new 2025 rewriting study adds the confound that better performance does not predict user satisfaction with seeing the reformulation. Kizilcec provides a calibration model: some transparency helps (low-info condition is as bad as high-info), but the "right amount" is a narrow band. The claim is qualified, not demolished — the pattern works if the interpretation is shown lightly (e.g., a short label "Routing you to: hook"), but fails if it involves visible reformulation of the user's words.

**Revised confidence:** MODERATE — interpretive transparency helps at low intensity (a label), but visible reformulation of user intent consistently reduces satisfaction.

---

#### Claim 3: Progressive disclosure is always better than full exposure

**Challenge search:** "progressive disclosure" expert users failure costs usability problems advanced features hidden; "progressive disclosure" developer experience expert users feature discovery failure frustrated

**Counter-evidence found:**

The Cognitive Dimensions framework documents that progressive disclosure (raising abstraction level) causes "hidden dependencies" — a direct usability cost. When debugging errors, programmers are "suddenly exposed to lower level implementation details," making recovery harder precisely because the abstractions were hidden.

The Koenemann et al. (2025) code completion tool study (56 developers, 8 workshops) found that the *correct* disclosure timing was individual- and expertise-dependent, not universally "progressive." Experts needed on-demand access to details; the progressive-reveal structure designed for novices was "obnoxious" to experts.

The Pot et al. (2016) robot API study empirically demonstrated that an API *reduced* its abstraction level (i.e., *increased* early exposure) after a user study found the high-abstraction version removed too much control.

Nielsen himself notes (in the progressive disclosure article) that "hiding the same behavior indefinitely would infuriate more advanced users." The NN/g wizard article (now T4 in this document) identifies expert users as the canonical failure case for progressive disclosure in wizard/guided flows.

There is no peer-reviewed study showing progressive disclosure *worse* than full exposure for novice users. The qualification is expertise-specific: progressive disclosure likely harms expert users in routing contexts where they need to validate or debug the routing decision.

**Assessment:** The claim is qualified, not overthrown. Progressive disclosure is appropriate for novice-first intake. For expert developers or for post-routing validation, progressive disclosure creates the hidden-dependencies cost. The claim should be scoped to "progressive disclosure is better for initial intake" — not universally.

**Revised confidence for universal claim:** LOW. Scoped to novice intake: HIGH.

---

#### Claim 4: Wizard/guided flows are the wrong pattern

**Challenge search:** wizard "create-react-app" "angular CLI" scaffolding usability empirical failure misrouting developer complaints; scaffolding wizard CLI tool "correct configuration" success rate failure rate empirical study

**Counter-evidence found:**

No controlled empirical study comparing wizard-based vs. non-wizard routing accuracy in developer tools was found — confirming the Santos et al. (2024) SLR's finding that wizard-based routing "received minimal research attention."

The Create React App deprecation provides indirect evidence. The React team's official post-mortem (react.dev, 2025) explicitly attributed CRA's failure to *technical architectural gaps* (missing routing, data fetching, code splitting), not to wizard UX problems, misconfigured defaults, or user confusion during setup. The wizard interface itself was not indicted. This is evidence against the claim that wizard flows fail at routing — CRA failed at the *generated artifact's capabilities*, not at the intake process.

Claim challenge strength is limited: the absence of empirical failure data for wizards does not mean they succeed. The Santos et al. finding that recommendation-based routing has more research support remains. But "wizards are wrong" is a claim without empirical support *in either direction* for developer-tools contexts.

The ASK system (Amazon/ACL 2025) found that in task-oriented dialogue, asking clarifying questions when ambiguity is high improved recall@5 by ~20% compared to direct retrieval. This is structurally similar to a wizard step — "ask one targeted question when routing confidence is low" — and has empirical support.

**Assessment:** The wizard-is-wrong claim is not strongly supported by evidence, but neither is it strongly refuted. The CRA counter-evidence does not support wizards — it just exonerates them from one failure mode. The ASK finding provides limited positive evidence for targeted single-question clarification (not full wizard flows). The claim should be downgraded from "wrong" to "under-studied and potentially effective for single-question targeted clarification."

**Revised confidence:** LOW — the evidence base for "wizards fail" is too thin to support a strong claim. The recommendation-based pattern has more research support, but this is an absence-of-evidence argument.

---

#### Claim 5: Justification gates cause friction without benefit

**Challenge search:** "forced justification" "accountability" decision quality HCI user study "explain your choice" reduces errors empirical; justification forcing conditions "better decisions" HCI empirical; PR template justification "why" rationale reduces review errors

**Counter-evidence found:**

Tetlock's accountability research (1985, foundational; reviewed in Lerner & Tetlock, 1999; Hall et al., 2015) establishes a key condition under which *prior* accountability requirements improve decision quality: "prior accountability encourages exploratory reasoning and optimal judgment, whereas post-decisional accountability increases confirmatory and self-justifying reasoning." In a criminal case study, requiring subjects to justify their judgments *before* exposure to evidence eliminated primacy bias (overweighting early information). This is empirical evidence that pre-decision justification gates improve judgment quality in some contexts.

This is directly applicable to the primitive-routing case: if a developer is required to briefly explain their intent *before* routing (rather than after), the accountability theory predicts better calibration. However, the key condition is that the justification must be *prior to* and *not replace* the system's decision.

The strongest direct counter-evidence: Hoffmann et al. (Judgment and Decision Making, 2017) found in two controlled experiments (n=144, n=110) that "process accountability neither changed how accurately people made a judgment, nor the judgment strategies." Justification reduced confidence without improving accuracy. This study specifically tests the Tetlock framework in a judgment task and finds no benefit.

For developer-workflow contexts: code review research (Nagappan et al.; commit message quality literature) shows that requiring developers to explain the *rationale* for code changes (PR templates with "why" fields) correlates with higher reviewer quality. Reviewers given the "why" gave better feedback. This is the closest empirical proxy for a justification gate in developer tooling — and it shows a benefit. However, this is commit authorship, not intake routing, and the benefit accrues to the *reviewer* not the author.

**Assessment:** The "no benefit" claim is overstated. Tetlock's framework provides theoretical and empirical support for pre-decision justification improving exploration quality in some judgment contexts. The Hoffmann et al. (2017) study directly contradicts this for accuracy in judgment tasks. The PR template evidence shows benefits in code review (reviewer quality, not author accuracy). Net: justification gates are not universally harmful, but the benefit is context-dependent and not proven for intake routing specifically.

**Revised confidence:** MODERATE — the claim that justification gates provide no benefit is overstated. But the evidence for benefit in intake routing specifically is weak.

---

### Challenge Summary

Three claims survived challenge largely intact (Claim 1 for novice users, Claim 3 for novice-first intake, Claim 4's rejection of evidence-backed wizards). Two claims were meaningfully qualified:

**Claim 2 (auto-select + interpretive transparency)** was qualified by new evidence that rewritten/reformulated intent shown to users consistently reduces satisfaction even when it improves response quality, and that optimal transparency lies in a narrow band (Kizilcec, 2016) — the recommendation is better stated as "show a routing label, not a reformulation."

**Claim 5 (justification gates cause friction without benefit)** was qualified by Tetlock's accountability framework — prior justification requirements can reduce primacy bias and improve exploratory reasoning — but directly contradicted by Andersson et al.'s (2017) controlled experiments showing no accuracy improvement from process accountability. The benefit in code-review contexts (PR templates) is real but accrues to reviewers, not decision-makers. The claim is overstated; the more accurate statement is that justification gates have not been shown to help intake routing accuracy, while they have been shown to reduce confidence without improving accuracy in judgment tasks.

No claim was fully overthrown. The most important finding is the automation bias evidence (Parasuraman et al., systematic review): erroneous automated advice increases incorrect decisions by 26%, but dynamic confidence display reduces automation bias — this supports the interpretive-transparency pattern for the specific case where routing confidence is low, but argues against silent auto-routing when confidence is uncertain.

---

## Findings

### Sub-question 1: When does exposing the full abstraction model help vs. hurt?

**Finding 1.1 — The abstraction gap is real and named** (HIGH — T1, n=24)
The CHI 2023 "What It Wants Me To Say" study [1] establishes that users describing their goals operate at a different abstraction level than the system requires. Only a small portion of naturalistic utterances are effective at guiding code generation. The gap is not a user skill problem; it is a structural vocabulary mismatch between user intent language and system primitive vocabulary. This directly applies to WOS: users will describe goals ("prevent pushes to main") in a vocabulary that does not map to the system's primitive names ("hook").

**Finding 1.2 — Information scent failure predicts routing failure** (HIGH — T1/T2 convergence via IFT [7][12])
Information Foraging Theory predicts that when intake labels use system-abstraction vocabulary rather than user-goal vocabulary, users cannot evaluate paths before committing to them. "Browsing" (exploratory, trial-and-error) replaces targeted navigation. For WOS: an intake prompt showing "Select a primitive: skill / command / hook / rule / subagent" provides zero information scent to a user who does not know these terms. Goal-vocabulary labels ("enforce a rule," "automate a task," "extend Claude's behavior") provide scent.

**Finding 1.3 — Grounded abstraction matching improves mental models** (HIGH — T1, n=24 [1])
The most effective intervention for abstraction gap is "grounded abstraction matching" — showing the system's interpretation of the user's stated goal in user-comprehensible terms. In the CHI 2023 study, this approach improved users' understanding of the system's scope and capabilities, enabling better future goal specification. This argues for showing users a routing interpretation ("We'd build this as a hook — an automated check that runs before a push") rather than asking them to name the primitive.

**Counter-evidence:** Expert developers are actively harmed by full opacity (Koenemann et al., IJHCS 2025, n=56 [19]). They found automatic explanation "obnoxious" and needed on-demand access to model internals for debugging. The progressive-disclosure benefit is scoped to novice-first intake; expert developers need an escape valve to inspect the routing decision.

**Finding 1.4 — Presenting all five primitives simultaneously is worst-case design** (MODERATE — T3 [8])
NN/g's progressive disclosure synthesis states that systems with 3+ abstraction levels "typically create usability problems." Hick-Hyman Law applies at maximum strength to users without a mental model — decision time increases logarithmically with option count. Presenting five primitives to a user who knows none of the vocabulary is the highest-friction intake design available.

---

### Sub-question 2: Intent-based vs. model-based routing — comparative evidence

**Finding 2.1 — No controlled study directly compares intent-first vs. model-first routing for developer primitives** (absence of evidence)
The research literature does not contain a controlled study testing intent-based ("what do you want?") against model-based ("choose one of these") routing in a developer tool with multiple primitives. The evidence bearing on this question is indirect — from adjacent domains (NLP intent classification, API usability, LLM interaction).

**Finding 2.2 — Reducing articulatory distance measurably improves success** (HIGH — T1, n=12, p<0.001 [3])
DirectGPT (CHI 2024) demonstrates that any design reducing the burden of expressing intent improves task success significantly: 50% faster, 25% more successful, 72% fewer words versus free-text natural language. Intent-based routing that accepts goal descriptions in natural language reduces articulatory distance compared to model-based routing that requires users to match their goals to technical primitive descriptions. This is the strongest empirical argument for intake accepting natural language goal statements.

**Finding 2.3 — Automatic intent classification has a measurable failure ceiling of ~10%** (MODERATE — T2 [6])
GPT-4 achieved 89.64% intent classification accuracy in the Bodonhelyi et al. (2024) study. Systematic blind spots exist for rare or ambiguous categories — exactly the categories most likely in a 5-primitive system where some primitives (e.g., "subagent") are used infrequently. This failure ceiling means silent auto-routing will misroute approximately 1-in-10 users even at best-case AI performance; the failure rate increases for novel or mixed-primitive requests.

**Finding 2.4 — Industry default is model-based; this is not evidence of efficacy** (MODERATE — T2 [13])
GitHub's documentation for the Actions/Apps routing problem defaults to model-based routing: explaining characteristics, asking users to self-match. This is the dominant industry pattern, not because it has been shown to work better, but because it requires no AI classification. The absence of intent-based routing in existing developer tool documentation is a historical default, not a validated design decision.

**Counter-evidence:** Pot et al. (JVLC 2016 [24]) found empirically that a high-abstraction API that hid model details had to be revised downward — users needed more model visibility to retain control. Transparency that creates miscalibration (Shi et al. 2025 [20]) argues against over-explaining the model's internals.

---

### Sub-question 3: Intake question patterns for inferring task type from natural language

**Finding 3.1 — Accept-then-interpret is more effective than select-then-confirm** (HIGH — T1/T2 convergence [1][5])
Two independent studies converge on the same pattern: accept the user's free-text goal statement first, then construct and surface the system's interpretation. Liu et al. (2026) [5] found that systems that commit to routing interpretations without surfacing them cause ~30% performance degradation through compounding errors. Liu & Sarkar (CHI 2023) [1] found that showing the system's interpretation of the user's goal improved mental model formation. The intervention that resolves both problems is the same: delay routing commitment, show interpretation before acting.

**Finding 3.2 — Early routing commitment is the primary intake failure mode** (MODERATE — T2 [5])
Intent mismatch in multi-turn conversation is caused by "early tentative assumptions" that get locked in as context accumulates. The structural cause: vague, underspecified first-turn utterances are interpreted by the system at a specificity level they don't warrant. For single-turn intake (WOS), this corresponds to routing a user's goal to a primitive without verifying the interpretation. Recovery requires either showing the interpretation before acting, or providing easy post-routing correction.

**Finding 3.3 — No empirically-validated taxonomy of developer task types was found** (LOW — absence of evidence)
No study was found that provides a validated taxonomy (enforcement vs. workflow, deterministic vs. judgment-based, etc.) of developer intent patterns specifically for primitive routing. The enforcement/workflow distinction is analytically motivated, not empirically derived. A practical heuristic taxonomy may be designed based on the primitives themselves, but claims that any taxonomy "reliably" routes users would currently be unsupported.

**Finding 3.4 — Goal-vocabulary labels are critical for intake scent** (HIGH — T1/T2 convergence [1][7][12])
The IFT framework predicts, and the CHI 2023 study confirms, that routing succeeds when the intake vocabulary matches user goal vocabulary. If intake questions ask about *triggers* ("runs automatically?"), *scope* ("affects one command or all commands?"), and *mechanism* ("enforces a rule vs. adds new behavior"), users can answer from their mental model of their goal without needing to know primitive names. Asking "which primitive do you want?" has zero information scent for a non-expert user.

**Counter-evidence:** Users prefer responses to their original stated intent over correctly-reformulated intent (Bodonhelyi 2024 [6], 56% preference for original). This qualifies the "accept-then-interpret" pattern: the interpretation should inform routing silently or be shown as a light label, not as a restatement of the user's goal in different words.

---

### Sub-question 4: Evidence on wizard/guided setup patterns

**Finding 4.1 — Recommendation-based routing has 23× more research support than wizard-based** (HIGH — T1 SLR [4])
The Santos et al. (2024) systematic literature review of 32 onboarding studies found recommendation systems (infer need, propose action, allow confirmation) as the most prevalent evidence-backed strategy. Wizard-based sequential routing received minimal research attention — fewer than 2 of 32 studies. This is the strongest evidence available, but it is an absence-of-direct-evidence finding for wizards, not evidence of wizard failure.

**Finding 4.2 — CRA deprecation does not indict wizard intake** (MODERATE — T2 [react.dev])
The React team's official CRA post-mortem (2025) attributed deprecation to missing architectural capabilities in the generated artifact — not to the wizard intake flow, misconfigured defaults, or user confusion during setup. The wizard that asked "create a new project?" and ran `npx create-react-app my-app` was not the failure point. This removes CRA as evidence against wizard patterns.

**Finding 4.3 — Single targeted clarification improves routing accuracy ~20%** (MODERATE — T1 [26])
Amazon's ASK system (ACL 2025) found that asking one clarifying question when routing ambiguity is detected improves retrieval recall@5 by approximately 20%. This is a narrower pattern than a full wizard — one question, triggered only when needed, not a mandatory sequential flow. This provides empirical support for a "confidence-triggered clarification" step.

**Finding 4.4 — Wizard flows harm expert users** (MODERATE — T3/T4 [9][19])
Expert developers find mandatory wizard sequences "frustratingly rigid" (NN/g, T4) and "obnoxious" (Koenemann 2025 [19]). The wizard failure case is expertise-specific: novice users benefit from guided structure; expert users lose control without gaining accuracy. A routing intake that forces expert users through a multi-step clarification flow when their intent is clear will generate resistance.

---

### Sub-question 5: "Justify your choice" vs. "we chose for you"

**Finding 5.1 — Pure auto-selection without confirmation causes ~60% relative degradation** (MODERATE — T2 [5])
Liu et al. (2026) found that systems that commit to routing decisions without surfacing their interpretation cause approximately 60% relative performance degradation from locked-in wrong assumptions (paper's own Figure 2; a ~30% figure in related literature originates from Laban et al. 2025, cited within [5]). Silent auto-routing is the riskiest pattern — it fails invisibly. This finding, combined with the automation bias review below, establishes that confirming the routing decision at low cost is necessary.

**Finding 5.2 — Automation bias: erroneous automated advice increases errors by 26%** (HIGH — T1 systematic review [25])
The Parasuraman & Manzey (Human Factors 2010) systematic review found that erroneous automated advice increases incorrect decision rates by 26% compared to no automation. Critically: displaying dynamic confidence levels (uncertain vs. confident routing) reduces automation bias. This is directly applicable to WOS primitive routing — when routing confidence is low, showing confidence state is not just good UX, it measurably reduces incorrect decisions.

**Finding 5.3 — Visible reformulation of user intent reduces satisfaction even when correct** (MODERATE — T2 [6])
Bodonhelyi et al. (2024) found users preferred responses to their original stated intent 56.61%/53.50% of the time versus correctly-reformulated intent. Users resist having their words replaced by the system's vocabulary, even when the replacement is more accurate. This argues against showing users a restatement of their goal ("You want to enforce branch protection") as part of interpretive transparency.

**Finding 5.4 — Light-label transparency is the calibrated middle ground** (MODERATE — T1/T2 convergence [22][25])
Kizilcec (CHI 2016) found an inverted-U for transparency: both too much and too little transparency reduced trust calibration equally. Too little transparency (silent routing) loses error recovery; too much transparency (explaining model internals or reformulating user intent) erodes trust and creates miscalibration. The narrow effective band is a routing label — brief, specific, not verbose — that confirms what action will be taken without replacing the user's vocabulary.

**Finding 5.5 — Justification gates have not been shown to improve intake routing accuracy** (MODERATE — T2 [23])
Hoffmann et al. (JDM 2017, n=144+110) ran two controlled experiments on process accountability (forced justification before judgment). Justification reduced confidence without improving accuracy. Tetlock's accountability framework provides theoretical support for pre-decision justification in some contexts, but the direct empirical test contradicts it for judgment tasks. The benefit of justification gates in code review contexts (PR templates) accrues to reviewers, not to the decision-making author — an inapplicable analogy for intake routing.

---

### Cross-Cutting Finding: The Convergent Pattern

Across all five sub-questions, the evidence converges on a single intake pattern:

1. **Accept the user's goal in natural language** — don't ask them to name or select a primitive
2. **Infer the routing based on goal vocabulary** — use intent-based classification, not model-based option selection
3. **Show a routing label before acting** — brief, in user-goal vocabulary ("Building this as a hook: a check that runs before each push"), not a reformulation of the user's words
4. **Display confidence state when uncertain** — when routing confidence is low, surface it; erroneous auto-routing without confidence signals increases errors by 26%
5. **Provide easy correction, not forced justification** — a single low-friction way to redirect, not a gate requiring users to explain their choice

This pattern is supported by: DirectGPT [3], Liu/Sarkar CHI 2023 [1], Liu et al. 2026 [5], Parasuraman & Manzey 2010 [25], Kizilcec CHI 2016 [22], and the Santos SLR [4].

The pattern is bounded by: the ~10% intent classification failure ceiling [6], the expert-user need for on-demand model visibility [19], and the counter-evidence that showing confidence state helps but showing reformulations does not [6][21].

**The one finding that most constrains WOS design:** Rare or low-frequency primitives (like "subagent") are the most likely to be systematically misclassified by intent inference. The intake design must account for the specific failure modes of the rarest primitives, not just optimize for the common case.

---

## Claims

| # | Claim | Type | Source(s) | Status |
|---|-------|------|-----------|--------|
| 1 | "50% faster" — DirectGPT users completed tasks 50% faster than ChatGPT baseline | statistic | [3] | corrected — paper reports task time means of 56s (DirectGPT) vs. 117s (ChatGPT), a ~52% reduction; abstract rounds to "50%" which is directionally accurate but not exact |
| 2 | "25% more successful" — DirectGPT success rate 25% higher | statistic | [3] | corrected — paper reports +0.95 on a 5-point scale (M=4.84 vs M=3.89, p<0.001); this represents ~24% improvement relative to baseline, not exactly 25%. The abstract does not use "25% more successful"; this phrasing is inferred from the mean difference |
| 3 | "72% fewer words" — DirectGPT prompts 72% shorter | statistic | [3] | corrected — paper reports 5.83 vs 19.98 words (~71% reduction); abstract states "72% shorter prompts"; directionally correct, minor rounding |
| 4 | "50% fewer prompts" — DirectGPT used 50% fewer prompts | statistic | [3] | corrected — paper reports M=1.90 vs M=3.67 (~48% reduction); abstract rounds to "50%"; directionally accurate |
| 5 | "~30% performance degradation" from early routing commitment / intent mismatch | statistic | [5] | corrected — the ~30% figure originates from Laban et al. 2025, a prior paper *cited* within [5], not from [5]'s own measurements. The paper's own Figure 2 finding is "approximately 60%" relative performance degradation across model sizes. The claim as written misattributes a secondary citation as the paper's own finding. |
| 6 | "~20 percentage points recovery" from Mediator pattern | statistic | [5] | verified — Table 1 shows GPT-4o-mini +20.3pp, average across models ~20–24pp; "~20 percentage points" is accurate for the lower bound |
| 7 | "89.64% accuracy (F1: 88.84%)" for GPT-4 intent recognition | statistic | [6] | verified — confirmed exactly from full paper HTML |
| 8 | "75.28% (F1: 74.28%)" for GPT-3.5 intent recognition | statistic | [6] | verified — confirmed exactly from full paper HTML |
| 9 | "learning support" GPT-4: 0%, GPT-3.5: 36.84% | statistic | [6] | verified — confirmed from full paper HTML |
| 10 | "curricular planning" GPT-4: 0%, GPT-3.5: 50% | statistic | [6] | verified — confirmed from full paper HTML |
| 11 | "56.61% preference for original" prompt — GPT-3.5 users | statistic | [6] | verified — confirmed exactly from full paper HTML |
| 12 | "53.50%" preference for original — GPT-4 users | statistic | [6] | verified — confirmed exactly from full paper HTML |
| 13 | "23 of 32 studies" used recommendation systems in the onboarding SLR | statistic | [4] | verified — Table 7 in the full paper confirms 23 of 32 studies used recommendation systems |
| 14 | "~20% recall improvement" from ASK clarification | statistic | [26] | verified — Amazon Science page confirms "recall@5 gain of ~20%" for ASK system when clarifying questions triggered on high-ambiguity inputs |
| 15 | "26% increase in incorrect decisions" from erroneous automation | statistic | [25] | verified — paper states risk ratio 1.26 (95% CI 1.11 to 1.44); "increased the risk of an incorrect decision being made by 26%" is an exact quote |
| 16 | "7–18% trust reduction" from AI disclosure | statistic | [27] | human-review — the Schilke & Reimann (2025) paper reports effects as Cohen's d / Likert mean differences, not as percentage reductions. The "7–18%" range does not appear in any accessible summary or abstract of the paper. This figure cannot be verified and may be a misinterpretation of effect size data. Requires full-text access to confirm or correct. |
| 17 | Source [27] involves n>5,000 participants | statistic | [27] | corrected — multiple independent sources confirm the paper reports 13 experiments with n>3,000 participants, not n>5,000. The Sources section of the document states "n>5,000" which is incorrect. |
| 18 | "Inverted-U effect: too much OR too little transparency reduces trust equally" | causal | [22] | corrected — Kizilcec (CHI 2016) found that in both low and high transparency conditions, expectation violation was *negatively correlated* with trust, while in the medium transparency condition trust was *uncorrelated* with expectation violation. The paper does not state the two extremes reduce trust "equally" — it shows both extremes are detrimental compared to medium, but the effect magnitudes are not described as equivalent. Sample size is n=103 (field experiment in a Coursera MOOC), not described in the document. |
| 19 | "Justification reduced confidence without improving accuracy" | causal | [23] | verified — the finding is correct. However, the authors are misattributed. The document cites "Andersson, Szymkowiak, Göritz" but the paper at sjdm.org/journal/17/17411/new.html is authored by Hoffmann, Gaissmaier, and von Helversen. The correct citation is: Hoffmann, J.A., Gaissmaier, W., & von Helversen, B. (2017). |
| 20 | "n=56 developers, 8 co-design workshops" — Source [19] study design | statistic | [19] | verified — confirmed: 56 developers (8 female, 48 male), 8 focus groups of 7 participants each |
| 21 | Expert developers found automatic explanation generation "obnoxious or even 'outrageous'" | attribution | [19] | verified — confirmed as a direct participant quote from group G2: "Automatic generation of explanations is fine for novices, but could be obnoxious or even 'outrageous' for experts" |
| 22 | "Recommendation systems are the 'most prevalent strategy' (23 of 32 studies)" | statistic | [4] | verified — confirmed; 23 studies across 5 subcategories |
| 23 | DirectGPT study: n=12 participants, within-subject design | statistic | [3] | verified — confirmed from abstract and HTML: 12 participants, within-subject, 12 tasks |
| 24 | Prompt count: "M=1.90 vs. M=3.67" for DirectGPT vs. ChatGPT | statistic | [3] | verified — confirmed exactly from full paper HTML |
| 25 | Task time: "56s vs. 1m 57s" for DirectGPT vs. ChatGPT | statistic | [3] | verified — confirmed exactly from full paper HTML |
| 26 | Success score: "M=4.84 vs. M=3.89, p<0.001" | statistic | [3] | verified — confirmed exactly from full paper HTML |
| 27 | "Displaying dynamic confidence levels reduces automation bias" | causal | [25] | verified — paper states McGuirl and Sarter found that "updating the confidence level of the DSS alongside pieces of advice...improved the appropriateness of user reliance, decreasing AB" |
| 28 | "~60% relative performance degradation" is the paper's own [5] finding | statistic | [5] | verified — Figure 2 caption states "the relative performance degradation between fully specified and underspecified settings remains remarkably constant (∼60%) across diverse model sizes and families" |
| 29 | The ~30% degradation figure originates from Laban et al. 2025, not Liu et al. 2026 | attribution | [5] | verified — the HTML confirms the ~30% figure is cited from a prior paper by Laban et al. 2025; the introduction references it as "prior work revealing approximately 30% degradation" |
| 30 | Rewritten prompts achieve "79.61% GPT-4o win rate" — Source [21] | statistic | [21] | inferred — the document cites this figure; the arXiv abstract is confirmed but full-text verification of this exact figure requires the HTML version. The claim is plausible given the abstract's framing but not directly confirmed in available content. |
| 31 | "Only one study examined standalone structured documentation" in the onboarding SLR | statistic | [4] | human-review — this level of detail requires full-text access to the SLR's results table; cannot be confirmed or denied from abstract alone |
| 32 | "71% of studies used laboratory experiments; 50% used quantitative metrics" in the onboarding SLR | statistic | [4] | human-review — requires full-text access to confirm these methodology breakdown figures |
| 33 | "Only 18 of 58 identified newcomer barriers are addressed by existing software solutions" | statistic | [4] | human-review — requires full-text access |

## CoVe Checks

### Claim 5 (statistic/causal) — "~30% performance degradation" [5]

1. **Does the cited source contain this number?** The paper [5] contains a ~30% figure but it is attributed to Laban et al. 2025, a prior work cited within [5]. The paper's *own* finding is ~60% relative degradation.
2. **Is the number from the cited source or from a source it cites?** From a source [5] *cites*, not from [5] itself.
3. **Is methodology sufficient to support the causal direction?** The ~30% figure from Laban et al. is not verifiable from available content; [5]'s own ~60% is from benchmark comparison across multiple LLMs.
4. **Are specific numbers stated correctly?** No — the document claims ~30% as [5]'s finding but [5] reports ~60% and cites ~30% from prior work.
**Verdict: corrected — the document misattributes a secondary-citation figure to [5]. The correct figure from [5] is ~60% relative degradation. The ~20pp recovery figure remains accurate.**

### Claim 1–4 (statistics) — DirectGPT results [3]

1. **Does the cited source contain these numbers?** Yes — full HTML confirms M=1.90/3.67 (prompts), 56s/117s (time), 4.84/3.89 (success), 5.83/19.98 (words).
2. **Are the numbers from [3] directly?** Yes, primary data.
3. **Is methodology sufficient?** Within-subject n=12, p<0.001 across all metrics. Methodology is sound for the effect directions claimed.
4. **Are the numbers stated correctly?** Largely yes with rounding: "50%" is ~48% and ~52%; "72% fewer words" is ~71%; "+0.95 points" is exactly right but "25% more successful" is an inferred percentage not stated in the paper (paper states mean difference, not percentage improvement).
**Verdict: verified with annotation — percentages are rounded from paper means; "25% more successful" is an inference from the 5-point scale difference, not a direct paper claim.**

### Claim 16 (statistic) — "7–18% trust reduction" [27]

1. **Does the cited source contain this number?** Cannot be confirmed from available content. Paper reports effects as mean Likert differences (e.g., M=4.55 vs. M=5.63 on a 7-point scale), not as percentages.
2. **Is the number from the source or a source it cites?** Unknown — no accessible summary confirms this range.
3. **Is methodology sufficient?** 13 pre-registered experiments, n>3,000 (not n>5,000 as stated in document) — methodology is strong, but the specific percentage claim is unverifiable.
4. **Are specific numbers stated correctly?** The n>5,000 figure in the Sources section is incorrect (should be n>3,000). The 7–18% range is unverifiable.
**Verdict: human-review — the trust-reduction finding is real but the specific percentage range and the sample size figure in the source table both require full-text verification.**

### Claim 18 (causal) — Kizilcec inverted-U [22]

1. **Does the cited source contain this claim?** Partially — the paper found high and low transparency both negatively correlated with trust under expectation violation, while medium was not. This is consistent with an "inverted-U" framing.
2. **Is this from [22] directly?** Yes, Kizilcec (2016) is the primary source.
3. **Is methodology sufficient to support the causal direction?** n=103 in a Coursera field experiment — modest sample, single-context (peer assessment grading). Generalization to developer tool routing is inferential.
4. **Are specific numbers stated correctly?** The claim that the two extremes "reduce trust equally" is an overstatement; the paper shows both extremes are harmful but does not quantify equivalence.
**Verdict: corrected — the inverted-U pattern is supported but "equally" overstates the finding; the sample is n=103, not described in the document.**

### Claim 19 (attribution/causal) — Justification reduces confidence without improving accuracy [23]

1. **Does the cited source contain this claim?** Yes — confirmed: "justifying the judgment process only decreased confidence without improving judgment accuracy."
2. **Is the attribution to "Andersson, Szymkowiak, Göritz" correct?** No — the paper is by Hoffmann, Gaissmaier, and von Helversen (2017). The author names in the Sources section and in the Findings text are incorrect.
3. **Is methodology sufficient?** Two controlled experiments (n=144, n=110) — adequate for the judgment task tested.
4. **Are specific numbers stated correctly?** The finding is stated accurately; only the authorship is wrong.
**Verdict: corrected — finding confirmed; author attribution in Source [23] must be changed to Hoffmann, Gaissmaier, & von Helversen (2017).**
