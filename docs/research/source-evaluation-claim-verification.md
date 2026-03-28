---
name: "Source Evaluation and Claim Verification Frameworks"
description: "SIFT framework, source tier hierarchies, claim verification types, and Chain-of-Verification (CoVe) applied to LLM-assisted research"
metadata:
  type: research
  sources:
    - https://hapgood.us/2019/06/19/sift-the-four-moves/
    - https://pressbooks.pub/webliteracy/chapter/four-strategies/
    - https://arxiv.org/abs/2309.11495
    - https://aclanthology.org/2024.findings-acl.212/
    - https://open.oregonstate.education/goodargument/chapter/four-tiers-of-sources/
    - https://libraryguides.csuniv.edu/tutorial_evaluating/hierarchy_of_credibility
    - https://datajournalism.com/read/handbook/verification-1/additional-materials/verification-and-fact-checking
    - https://researchguides.journalism.cuny.edu/factchecking-verification/fact-check-your-work
    - https://www.nature.com/articles/s41586-024-07421-0
    - https://www.coreprose.com/kb-incidents/why-llms-invent-academic-citations-and-how-to-stop-ghost-references
  related:
    - docs/research/prompt-engineering.md
    - docs/research/llm-capabilities-limitations.md
    - docs/context/source-evaluation-claim-verification.md
---

Source evaluation and claim verification are the difference between research that informs decisions and research that misleads them. When LLMs assist the research process, traditional verification becomes both more important and more difficult: models fabricate citations at rates of 14-95% depending on the model and task, generate plausible-sounding claims without epistemic grounding, and exhibit confirmation bias in their own outputs. Three frameworks address these challenges at different levels: SIFT for rapid source triage, source tier hierarchies for systematic credibility classification, and Chain-of-Verification for structured claim checking.

## The SIFT Framework

SIFT is a four-move evaluation strategy developed by Mike Caulfield, first published as "Four Moves and a Habit" in *Web Literacy for Student Fact-Checkers* (2017) and refined into the SIFT acronym in 2019. It replaced checklist-based approaches like the CRAAP test (Currency, Relevance, Authority, Accuracy, Purpose) with a lateral-reading methodology grounded in how professional fact-checkers actually work.

### The Four Moves

**Stop.** Before engaging with a source, pause. Ask whether you know and trust the author, publisher, or website. The goal is to interrupt the automatic tendency to read and absorb before evaluating. This is the habit component -- recognizing that your first reaction to a claim is not evaluation, it is consumption.

**Investigate the source.** Do not evaluate the source by reading it deeply. Instead, read *laterally*: open new tabs and see what others say about the source, its author, and its publisher. Professional fact-checkers spend seconds on a page itself and minutes checking what independent sources say about it. This technique, documented by Stanford researcher Sam Wineburg, consistently outperforms deep vertical reading for credibility assessment.

**Find better coverage.** If the claim is important, look for other sources covering the same topic. The goal is not to find agreement (that would be confirmation bias) but to find the best available coverage from the most authoritative sources. Multiple independent sources converging on the same claim increases confidence; a single source making a unique claim warrants skepticism.

**Trace claims, quotes, and media to the original context.** Much online content strips context from original sources. A statistic cited in a blog post may come from a study that says something different. A quote attributed to a public figure may be paraphrased, truncated, or fabricated. Tracing upstream to the original source reveals whether the claim was accurately represented.

### Why SIFT Replaced CRAAP

The CRAAP test asks evaluators to assess Currency, Relevance, Authority, Accuracy, and Purpose by examining the source itself. Research showed this approach fails in practice: students spent more time on less credible sources (engaging deeply with their "About Us" pages) and less time on credible ones. Checklists increase cognitive load without improving judgment.

SIFT addresses this by externalizing evaluation. Instead of asking "does this source *seem* credible?" it asks "what do *other credible sources* say about this source?" This lateral approach maps directly to how professional fact-checkers at organizations like Snopes and PolitiFact actually work.

### SIFT Applied to LLM-Assisted Research

When an LLM generates or recommends sources, SIFT becomes essential at every step:

- **Stop**: Do not assume an LLM-provided citation is real. Models fabricate citations at high rates (studies show 14-95% fabrication rates across models).
- **Investigate**: Verify the source exists. Check whether the URL resolves, the author exists, the publication is real.
- **Find better**: If the LLM cites a secondary summary, trace to the primary source. LLMs tend to cite the most statistically likely reference, not the most authoritative one.
- **Trace**: Confirm that the claim attributed to the source actually appears in that source. LLMs frequently attribute real claims to wrong sources or fabricate claims entirely.

## Source Tier Hierarchies

Source tier hierarchies classify sources by their epistemic authority -- how much weight a claim should carry based on where it comes from. While the traditional primary/secondary/tertiary classification describes a source's relationship to an event, tier hierarchies evaluate credibility and reliability for decision-making.

### The Five-Tier Model

**Tier 1 (T1): Primary/Official Sources.** Peer-reviewed academic papers, official documentation (API docs, RFCs, specifications), primary data from authoritative institutions, and original research. These sources have undergone formal review processes and represent the highest epistemic authority. When a T1 source contradicts lower tiers, the T1 source prevails absent compelling counter-evidence.

**Tier 2 (T2): Established Secondary Sources.** Reports from government agencies, major international organizations (World Bank, WHO), established reference works, and well-known technical publishers. These sources synthesize T1 material with editorial oversight. They are reliable for context and established facts but may lag behind T1 sources on recent developments.

**Tier 3 (T3): Quality Practitioner Sources.** Articles from recognized industry publications (Real Python, Martin Fowler's blog, CSS-Tricks), conference talks from established venues, and well-maintained community documentation. These offer practical interpretation of T1/T2 material. Claims unique to T3 sources warrant verification against higher tiers.

**Tier 4 (T4): General Web Sources.** News articles, magazine features, general-audience explainers, and Wikipedia. These provide breadth and accessibility but lack the review processes of higher tiers. Useful for orientation and discovering leads, but claims should be traced to higher-tier sources before being treated as established.

**Tier 5 (T5): Unvetted Sources.** Personal blogs without established reputation, forum posts, social media, anonymous content, and AI-generated text without human verification. These sources have no review process and unknown provenance. They may contain valuable signals but carry no epistemic weight on their own.

### Tier Application Rules

1. **Convergence increases confidence.** A claim supported by T1 and T3 sources independently is stronger than one supported by T1 alone (the T3 source confirms the claim is understood and applied correctly in practice).
2. **Higher tiers override lower tiers.** When sources conflict, defer to the higher tier unless the lower-tier source provides verifiable evidence the higher tier is wrong.
3. **Tier is not quality.** A well-written T4 source may be more useful than a poorly written T1 source. Tier measures epistemic authority, not prose quality or practical utility.
4. **Context shifts tiers.** An RFC is T1 for protocol behavior but T4 for deployment best practices. A practitioner blog post is T3 for implementation patterns but T5 for theoretical claims.

### Tier Hierarchies in LLM Context

LLM outputs are unvetted by default -- they are T5 sources. This has specific implications:

- LLM-generated claims require verification against T1-T3 sources before entering a research document.
- LLMs trained on internet-scale data reflect the statistical distribution of sources, which skews toward T3-T5 content. They are more likely to reproduce popular explanations than authoritative ones.
- When LLMs cite sources, the citation itself is T5 (it may be fabricated). The cited source, if verified to exist, carries its own tier.

## Claim Verification Types

Different types of claims require different verification methods. Professional fact-checkers categorize claims by type and apply targeted verification to each.

### Direct Quotes

**What to verify:** That the person said exactly what is attributed to them, in the context implied.

**Methods:**
- Trace to original transcript, recording, or primary document.
- Check for truncation that changes meaning (ellipsis abuse).
- Verify the speaker is correctly identified.
- Confirm the date and context of the statement.

**Common failures:** Paraphrases presented as direct quotes, quotes taken out of context, quotes from satirical sources treated as genuine, and composite quotes stitching together separate statements.

**LLM-specific risk:** Models frequently generate plausible-sounding quotes attributed to real people. These quotes may capture the person's general views but use words they never said. Every LLM-generated quote must be verified against primary sources.

### Statistics and Numerical Claims

**What to verify:** The number itself, its source, its context (methodology, sample size, time period), and whether it is presented accurately.

**Methods:**
- Trace to the original study or dataset.
- Check methodology: sample size, population, confidence intervals.
- Verify the number has not been rounded, converted, or recontextualized in ways that change its meaning.
- Watch for base rate neglect and misleading comparisons.

**Common failures:** Outdated statistics presented as current, percentages without base rates, cherry-picked data points, correlation presented as causation, and studies with small or unrepresentative samples.

**LLM-specific risk:** Models generate statistically plausible numbers that are not grounded in any real data. A model might state "studies show a 40% improvement" when no such study exists. Every statistic in LLM output should be treated as fabricated until verified.

### Attributions

**What to verify:** That the idea, invention, discovery, or action is correctly attributed to the named person or organization.

**Methods:**
- Check multiple independent sources for the attribution.
- Distinguish between originating an idea and popularizing it.
- Watch for "great man" attributions that oversimplify collaborative work.

**Common failures:** Misattribution of quotes (Einstein and Churchill are frequent targets), conflation of contribution and sole credit, and attribution to the most famous person associated with a topic rather than the actual originator.

**LLM-specific risk:** Models default to the most statistically associated name-concept pair in their training data, reinforcing popular misattributions.

### Superlatives and Absolute Claims

**What to verify:** Claims using "first," "only," "most," "best," "largest," "never," or "always."

**Methods:**
- Actively search for counter-examples.
- Check whether the superlative depends on a specific definition or scope.
- Verify the time frame and domain of the claim.

**Common failures:** Ignoring prior art, scope-dependent superlatives presented as absolute, and survivorship bias.

**LLM-specific risk:** Models are trained to produce confident, fluent text. Hedged claims ("one of the first") are less fluent than absolutes ("the first"), creating a systematic bias toward superlatives.

## Chain-of-Verification (CoVe)

Chain-of-Verification is a method introduced by Dhuliawala et al. (2023) at Meta AI that reduces hallucination in LLMs by separating generation from verification. Published at ACL 2024 Findings, it provides a structured approach to self-checking that directly addresses confirmation bias.

### The Four Stages

**1. Generate Baseline Response.** The model produces an initial response to the query. This response may contain hallucinations -- that is expected and acceptable at this stage.

**2. Plan Verification Questions.** The model examines its own response and generates specific, fact-checkable questions about the claims it made. These are not yes/no questions (which bias toward agreement) but open-ended questions that require specific factual answers.

**3. Execute Verification Independently.** Each verification question is answered independently, without access to the original response. This is the critical step that prevents confirmation bias: the model cannot see its own draft while answering the verification questions, so it cannot selectively seek confirming evidence.

**4. Generate Final Verified Response.** The model compares the verification answers against the original response, identifies inconsistencies, and produces a corrected final response.

### CoVe Variants

The paper investigates four execution strategies:

- **Joint:** All verification questions are answered in a single prompt alongside the original response. Fastest but most susceptible to confirmation bias since the model sees its own draft.
- **Two-Step:** Verification questions are answered in a separate prompt but all together. Reduces bias from the original response but verification answers can still bias each other.
- **Factored:** Each verification question is answered in a completely separate prompt. Maximum isolation, maximum bias reduction, but highest computational cost.
- **Factor+Revise:** Factored verification plus an explicit cross-checking step where the model compares verification answers against the original response and reasons about inconsistencies. This variant achieved the best results.

### Experimental Results

On biography generation, Factor+Revise improved FACTSCORE from 55.9 (few-shot baseline) to 71.4, a 28% improvement. The factored variants consistently outperformed joint variants, confirming that isolation during verification is the key mechanism. Overall, CoVe reduced factual hallucinations by 50-70% across list-based QA, closed-book MultiSpanQA, and long-form text generation tasks.

### Why Factored Verification Prevents Confirmation Bias

Confirmation bias in LLMs manifests as the tendency to agree with facts presented in context, regardless of their accuracy. When a model sees its own draft containing a false claim, it is more likely to verify that claim as true than if asked about the claim in isolation.

The factored approach eliminates this by ensuring each verification question is answered without any context from the original response. This functions like a double-blind study: the "verifier" does not know what answer the "generator" produced. Open-ended verification questions further reduce bias -- yes/no questions ("Is X true?") trigger agreement bias, while "What is X?" questions require the model to independently retrieve the answer.

### CoVe Applied to Research Workflows

CoVe maps directly to research verification practices:

1. **Draft findings** from gathered sources (Stage 1).
2. **Generate verification questions** for each claim: "What source supports this?" "What is the actual statistic?" "Who actually originated this concept?" (Stage 2).
3. **Answer each question independently** by searching for evidence without looking at the draft (Stage 3).
4. **Revise the draft** based on verification results, correcting or removing unsupported claims (Stage 4).

This is the machine-readable version of what human fact-checkers do when they re-verify claims before publication.

## Integrated Framework for LLM-Assisted Research

These four frameworks compose into a verification pipeline for LLM-assisted research:

**Layer 1 -- Source Triage (SIFT).** Every source encountered during research gets the four-move treatment. For LLM-suggested sources, this starts with verifying the source exists at all. Lateral reading confirms the source's reputation. Finding better coverage ensures you are working from the strongest available evidence.

**Layer 2 -- Source Classification (Tier Hierarchy).** Verified sources receive a tier classification. This tier determines how much weight the source's claims carry in synthesis. Conflicting claims are resolved by tier: T1 overrides T3 unless the T3 source provides verifiable counter-evidence.

**Layer 3 -- Claim Extraction and Typing.** Each claim in the research document is categorized: quote, statistic, attribution, or superlative. The category determines which verification method applies.

**Layer 4 -- Claim Verification (CoVe-Inspired).** Claims are verified using factored verification: each claim is checked independently, without reference to other claims or the draft document. The verifier asks open-ended questions ("What does source X actually say about Y?") rather than confirmation-seeking ones ("Does source X confirm Y?").

**Layer 5 -- Confidence Assignment.** Each finding receives a confidence level based on the verification results:
- **HIGH:** Multiple T1-T2 sources converge, claims verified, no credible counter-evidence.
- **MODERATE:** Single T1-T2 source or multiple T3 sources, claims verified, minor counter-evidence addressed.
- **LOW:** T3-T4 sources only, partial verification, or significant counter-evidence exists.

### LLM-Specific Failure Modes This Pipeline Addresses

| Failure Mode | Framework Response |
|---|---|
| Citation fabrication (14-95% of LLM citations) | SIFT: Verify source exists before evaluating |
| Plausible but groundless statistics | Claim typing: Trace every statistic to primary data |
| Popular misattributions reinforced | Claim typing: Check attributions against multiple sources |
| Confident superlatives without basis | Claim typing: Actively search for counter-examples |
| Confirmation bias in self-verification | CoVe: Factored verification prevents draft from biasing checks |
| Training data skew toward T4-T5 content | Tier hierarchy: Weight claims by source authority, not fluency |

## Challenge

**Counter-evidence and limitations:**

SIFT has been criticized for being too simplistic for advanced research contexts. It was designed for quick web literacy, not deep academic evaluation. For research purposes, SIFT serves as a rapid triage step but does not replace systematic literature review methodology.

Source tier hierarchies impose a rigid structure that may not capture all dimensions of credibility. A T5 blog post by a domain expert may contain more reliable information than a T1 peer-reviewed paper in a predatory journal. Tiers are heuristics, not guarantees.

CoVe's experimental results were obtained under controlled conditions with specific LLMs (primarily LLaMA 65B). The 50-70% hallucination reduction may not generalize to all models, tasks, or domains. Additionally, CoVe increases computational cost significantly (factored verification requires N+1 separate inference passes for N verification questions).

The integrated pipeline assumes human oversight at critical junctures. Fully automated verification pipelines risk circular validation, where the same model that generated a claim also verifies it. External grounding (human review, database lookups, URL verification) remains essential for high-stakes claims.

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | SIFT developed by Mike Caulfield, published 2019 | attribution | [1][2] | verified |
| 2 | SIFT originally "Four Moves and a Habit" in 2017 book | attribution | [2] | verified |
| 3 | Lateral reading concept from Sam Wineburg's research | attribution | [1] | verified |
| 4 | CRAAP test increases cognitive load without improving judgment | statistic | [1] | verified |
| 5 | CoVe reduces hallucinations by 50-70% | statistic | [3][4] | verified |
| 6 | CoVe Factor+Revise improves FACTSCORE from 55.9 to 71.4 | statistic | [3] | verified |
| 7 | CoVe by Dhuliawala et al. at Meta AI, 2023 | attribution | [3][4] | verified |
| 8 | CoVe published at ACL 2024 Findings | attribution | [4] | verified |
| 9 | LLMs fabricate 14-95% of citations | statistic | [10] | verified |
| 10 | 50+ ICLR 2026 submissions contained hallucinated citations | statistic | [10] | verified |
| 11 | Open-ended verification questions outperform yes/no | statistic | [3] | verified |

## Search Protocol

| # | Query | Source | Results | Useful |
|---|-------|--------|---------|--------|
| 1 | SIFT framework Mike Caulfield Stop Investigate Find better Trace lateral reading | WebSearch | 10 | 4 |
| 2 | source tier hierarchy research evaluation primary secondary tertiary | WebSearch | 10 | 3 |
| 3 | Chain-of-Verification CoVe LLM hallucination prevention confirmation bias | WebSearch | 10 | 5 |
| 4 | claim verification types quotes statistics attributions fact-checking methodology | WebSearch | 10 | 4 |
| 5 | LLM-assisted research source evaluation verification frameworks 2024 2025 | WebSearch | 10 | 2 |
| 6 | SIFT method vs CRAAP test Mike Caulfield lateral reading information literacy | WebSearch | 10 | 4 |
| 7 | Mike Caulfield "Web Literacy for Student Fact-Checkers" SIFT 2017 | WebSearch | 10 | 4 |
| 8 | source credibility evaluation tiers official documentation peer-reviewed | WebSearch | 10 | 3 |
| 9 | CoVe Factor+Revise two-step joint factored verification experimental results | WebSearch | 10 | 4 |
| 10 | fact-checking claim types quotes statistics attributions superlatives | WebSearch | 10 | 4 |
| 11 | LLM hallucination confabulation source fabrication verification strategies | WebSearch | 10 | 5 |
| 12 | LLM citation fabrication fake references AI-generated research source verification | WebSearch | 10 | 5 |
| 13 | CoVe paper arXiv 2309.11495 (WebFetch) | WebFetch | 1 | 1 |

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://hapgood.us/2019/06/19/sift-the-four-moves/ | SIFT (The Four Moves) | Mike Caulfield / Hapgood | 2019 | T1 | verified |
| 2 | https://pressbooks.pub/webliteracy/chapter/four-strategies/ | Four Moves - Web Literacy for Student Fact-Checkers | Mike Caulfield | 2017 | T1 | verified |
| 3 | https://arxiv.org/abs/2309.11495 | Chain-of-Verification Reduces Hallucination in Large Language Models | Dhuliawala et al. / Meta AI | 2023 | T1 | verified |
| 4 | https://aclanthology.org/2024.findings-acl.212/ | Chain-of-Verification Reduces Hallucination (ACL Findings) | Dhuliawala et al. | 2024 | T1 | verified |
| 5 | https://open.oregonstate.education/goodargument/chapter/four-tiers-of-sources/ | Four Tiers of Sources | Oregon State / A Dam Good Argument | 2022 | T3 | verified |
| 6 | https://libraryguides.csuniv.edu/tutorial_evaluating/hierarchy_of_credibility | Hierarchy of Credibility | Charleston Southern University Library | 2023 | T3 | verified |
| 7 | https://datajournalism.com/read/handbook/verification-1/additional-materials/verification-and-fact-checking | Verification and Fact Checking | DataJournalism.com | 2023 | T2 | verified |
| 8 | https://researchguides.journalism.cuny.edu/factchecking-verification/fact-check-your-work | Fact-Checking Your Reporting | CUNY Newmark J-School | 2023 | T2 | verified |
| 9 | https://www.nature.com/articles/s41586-024-07421-0 | Detecting hallucinations using semantic entropy | Farquhar et al. / Nature | 2024 | T1 | verified |
| 10 | https://www.coreprose.com/kb-incidents/why-llms-invent-academic-citations-and-how-to-stop-ghost-references | LLMs invent citations: 7 drivers, 6 fixes | CoreProse | 2025 | T3 | verified |

Key findings at bottom for agent retention: SIFT provides rapid source triage via lateral reading. Source tiers classify epistemic authority from T1 (peer-reviewed/official) through T5 (unvetted). Claim verification requires type-specific methods for quotes, statistics, attributions, and superlatives. CoVe's factored verification prevents confirmation bias by isolating verification from generation. LLM outputs are T5 by default and require external verification at every layer. The integrated pipeline composes these four frameworks into a practical verification workflow for LLM-assisted research.
