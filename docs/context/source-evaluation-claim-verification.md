---
name: "Source Evaluation and Claim Verification"
description: "SIFT framework, source tier hierarchies, claim verification types, and Chain-of-Verification composed into a verification pipeline for LLM-assisted research"
metadata:
  type: reference
  sources:
    - https://hapgood.us/2019/06/19/sift-the-four-moves/
    - https://pressbooks.pub/webliteracy/chapter/four-strategies/
    - https://arxiv.org/abs/2309.11495
    - https://aclanthology.org/2024.findings-acl.212/
    - https://open.oregonstate.education/goodargument/chapter/four-tiers-of-sources/
  related:
    - docs/research/source-evaluation-claim-verification.md
    - docs/context/llm-capabilities-limitations.md
    - docs/context/prompt-engineering.md
---

Four frameworks compose into a practical verification pipeline for LLM-assisted research: SIFT for rapid source triage, source tier hierarchies for credibility classification, claim typing for targeted verification, and Chain-of-Verification (CoVe) for bias-resistant fact-checking. LLM outputs are unvetted by default and require external verification at every layer.

## SIFT: Rapid Source Triage

SIFT (Stop, Investigate, Find better coverage, Trace to original) is a lateral-reading methodology developed by Mike Caulfield (2017/2019) that replaced checklist-based approaches like the CRAAP test. Instead of evaluating a source by reading it deeply, SIFT externalizes evaluation: check what other credible sources say about this source.

For LLM-assisted research, SIFT is non-negotiable at every step. Models fabricate citations at rates of 14-95% depending on model and task. Before evaluating any LLM-provided source: verify it exists, check the URL resolves, confirm the author and publication are real, and trace claims to what the source actually says.

## Source Tier Hierarchies

Sources are classified by epistemic authority across five tiers:

- **T1 (Primary/Official):** Peer-reviewed papers, official documentation, RFCs, specifications. Highest authority; overrides lower tiers absent compelling counter-evidence.
- **T2 (Established Secondary):** Government agencies, major international organizations, established reference works. Reliable for context and established facts.
- **T3 (Quality Practitioner):** Recognized industry publications, conference talks, well-maintained community docs. Claims unique to T3 warrant verification against higher tiers.
- **T4 (General Web):** News articles, Wikipedia, general explainers. Useful for orientation; trace claims to higher tiers before treating as established.
- **T5 (Unvetted):** Personal blogs without reputation, forum posts, social media, AI-generated text. No epistemic weight on their own.

LLM outputs are T5 by default. LLMs trained on internet-scale data skew toward T3-T5 content, reproducing popular explanations over authoritative ones. When an LLM cites a source, the citation itself is T5 until verified; the cited source carries its own tier only after confirmation it exists.

Key application rules: convergence across tiers increases confidence, higher tiers override lower when sources conflict, and context shifts tiers (an RFC is T1 for protocol behavior but T4 for deployment best practices).

## Claim Verification by Type

Different claims require different verification methods:

- **Direct quotes:** Trace to original transcript or document. LLMs frequently generate plausible quotes using words the person never said.
- **Statistics:** Trace to original study or dataset. Check methodology, sample size, time period. LLMs generate statistically plausible numbers not grounded in real data.
- **Attributions:** Check multiple independent sources. LLMs default to the most statistically associated name-concept pair, reinforcing popular misattributions.
- **Superlatives:** Actively search for counter-examples. Models bias toward confident absolutes ("the first") over accurate hedges ("one of the first").

## Chain-of-Verification (CoVe)

CoVe (Dhuliawala et al., 2023; ACL 2024 Findings) reduces LLM hallucination by separating generation from verification in four stages: generate a baseline response, plan verification questions about its claims, answer each question independently without seeing the original response, then revise based on verification results.

The critical mechanism is isolation: factored verification (each question answered in a separate context) prevents the model from exhibiting confirmation bias toward its own draft. The Factor+Revise variant achieved a 28% improvement in FACTSCORE and 50-70% hallucination reduction across tasks.

For research workflows: draft findings, generate open-ended verification questions ("What does source X actually say about Y?" not "Does source X confirm Y?"), answer each independently, then revise.

## The Integrated Pipeline

These frameworks layer: SIFT triages sources, tier hierarchies classify their authority, claim typing determines verification method, and CoVe-style factored checking prevents confirmation bias. Confidence levels follow from verification results — HIGH requires converging T1-T2 sources with verified claims, MODERATE needs a single T1-T2 or multiple T3 sources, LOW indicates T3-T4 sources with partial verification.

The pipeline assumes human oversight at critical junctures. Fully automated verification risks circular validation where the same model generates and verifies claims.
