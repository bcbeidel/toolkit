---
name: "AI Product Management"
description: "AI PM is evolutionarily continuous with traditional PM but probabilistic output fundamentally shifts roadmapping, eval ownership, and success metrics — trust over accuracy, HITL as a design variable, agentic metrics still unsettled"
type: research
sources:
  - https://arize.com/ai-product-manager-role
  - https://blog.promptlayer.com/product-manager-levels-llm-competency-the-new-rules-of-ai-product-management/
  - https://www.productboard.com/blog/ai-evals-for-product-managers/
  - https://langfuse.com/blog/2024-11-llm-product-management
  - https://voltagecontrol.com/articles/agentic-ai-for-product-management-autonomy-next-level-strategy/
  - https://productschool.com/blog/artificial-intelligence/guide-ai-product-manager
  - https://www.prodpad.com/blog/ethics-in-ai/
  - https://www.stackai.com/insights/measuring-enterprise-ai-success-the-essential-kpis-beyond-accuracy-for-scalable-impact
  - https://labs.adaline.ai/p/llm-evals-are-product-managers-secret-weapon
  - https://galileo.ai/blog/ai-product-management-guide
  - https://dev.to/kuldeep_paul/evals-and-observability-for-ai-product-managers-a-practical-end-to-end-playbook-4cch
  - https://www.justanotherpm.com/blog/fundamentals-of-ai-product-management-prompt-engineering-ai-agents-and-eval-frameworks
  - https://irenebrat.medium.com/product-management-agentic-ai-463caedf1aec
  - https://www.kasava.dev/blog/why-pms-are-built-for-ai
  - https://www.svpg.com/ai-product-management-2-years-in/
  - https://towardsdatascience.com/the-ai-3p-assessment-framework/
  - https://productschool.com/blog/artificial-intelligence/evaluation-metrics
related:
---

# AI Product Management

## Key Takeaways

1. **The core PM role is continuous, not discontinuous.** Reforge is correct: understanding customers, prioritizing, and facilitating solutions are unchanged. What changes is the medium — probabilistic outputs require new vocabulary, new practices, and expanded stakeholder coordination, not a new profession.

2. **Eval-driven development is the most defensible shift.** PMs must own success criteria for model quality (not just feature requirements), translate statistical metrics to business language, and enforce release gates. The three-stage eval lifecycle (experimentation → testing → production) is the most validated pattern across sources.

3. **Trust is the differentiator in 2025; accuracy is table stakes.** A Deloitte survey found one-third of genAI users had already encountered incorrect or misleading answers. Models scoring 95% in labs fail real users because trust depends on consistency and explainability across the full interaction. Outcome-based adoption metrics — task completion rates, override rates, resolution rates — are the most operationally reliable success signals. High override rates specifically diagnose UX or explainability failures.

4. **HITL is a design variable, not a universal principle.** The question is under what conditions human judgment adds net positive value over agent speed. In legal research and advertising, AI-alone now outperforms human-AI collaboration. Design for trust calibration and bounded autonomy first; scale autonomy as monitoring confirms predictable behavior.

5. **Agentic success metrics are genuinely unsettled.** No established methodology exists for measuring "good agent outcome" in open-ended generative systems. Task completion and resolution rates are reasonable proxies. This is acknowledged as a field-wide gap, not a research failing.

6. **The 85% failure statistic is a misquote — stop using it.** The real Gartner figure: 48% of AI projects reach production; 30% are abandoned post-PoC. The 85% traces to a 2018 Gartner forecast about erroneous outcomes, not production failure, laundered through vendor blogs for a decade.

7. **Data flywheels have documented failure modes.** Design with explicit reward modeling audits, not just feedback volume metrics. GPT-4o's April 2025 rollback (sycophancy from over-training on approval signals) is the canonical warning case.

8. **Ethics as a fourth prioritization axis is correct direction; "ethics-washing" is the primary failure mode.** Embed ethics review at project inception, not as a sign-off checklist. Springer/ISACA (2025): the checklist approach generates compliance theater with no systemic accountability.

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arize.com/ai-product-manager-role | How Is an AI Product Manager Different? | Arize AI | 2025 | T2 | verified |
| 2 | https://blog.promptlayer.com/product-manager-levels-llm-competency-the-new-rules-of-ai-product-management/ | The New Rules of AI Product Management | PromptLayer | 2025 | T3 | verified |
| 3 | https://www.productboard.com/blog/ai-evals-for-product-managers/ | AI Evals for Product Managers | Productboard | 2025 | T3 | verified |
| 4 | https://langfuse.com/blog/2024-11-llm-product-management | LLM Product Development for Product Managers | Langfuse | Nov 2024 | T3 | verified |
| 5 | https://voltagecontrol.com/articles/agentic-ai-for-product-management-autonomy-next-level-strategy/ | Agentic AI for Product Management | Voltage Control | 2025 | T4 | verified |
| 6 | https://productschool.com/blog/artificial-intelligence/guide-ai-product-manager | AI Product Managers Are the PMs That Matter in 2026 | Product School | 2025 | T3 | verified |
| 7 | https://www.prodpad.com/blog/ethics-in-ai/ | Ethics in AI: The New Frontier for Product Managers | ProdPad | 2025 | T3 | verified |
| 8 | https://www.stackai.com/insights/measuring-enterprise-ai-success-the-essential-kpis-beyond-accuracy-for-scalable-impact | Measuring Enterprise AI Success: The Essential KPIs Beyond Accuracy | StackAI | 2025 | T3 | verified |
| 9 | https://labs.adaline.ai/p/llm-evals-are-product-managers-secret-weapon | Why LLM Evals Are Every Product Manager's Secret Weapon | Adaline Labs | 2025 | T3 | verified |
| 10 | https://galileo.ai/blog/ai-product-management-guide | What Is AI Product Management? | Galileo AI | 2025 | T3 | verified |
| 11 | https://dev.to/kuldeep_paul/evals-and-observability-for-ai-product-managers-a-practical-end-to-end-playbook-4cch | Evals and Observability for AI PMs: End-to-End Playbook | DEV Community / Kuldeep Paul | 2025 | T4 | verified |
| 12 | https://www.justanotherpm.com/blog/fundamentals-of-ai-product-management-prompt-engineering-ai-agents-and-eval-frameworks | Fundamentals of AI PM: Prompt Engineering, AI Agents, and Eval Frameworks | JustAnotherPM | 2025 | T4 | verified |
| 13 | https://irenebrat.medium.com/product-management-agentic-ai-463caedf1aec | Product Management & Agentic AI | Irene Bratsis / Medium | 2025 | T4 | verified (403) |
| 14 | https://www.kasava.dev/blog/why-pms-are-built-for-ai | Non-Determinism Isn't a Bug: Why PMs Were Built for AI | Kasava | 2025 | T4 | verified |
| 15 | https://www.svpg.com/ai-product-management-2-years-in/ | AI Product Management 2 Years In | SVPG / Marty Cagan | Jan 2025 | T2 | verified |
| 16 | https://towardsdatascience.com/the-ai-3p-assessment-framework/ | Introducing the AI-3P Assessment Framework | Towards Data Science / Marina Tosic | Sep 2025 | T3 | verified |
| 17 | https://productschool.com/blog/artificial-intelligence/evaluation-metrics | Evaluation Metrics for AI Products That Drive Trust | Product School | 2025 | T3 | verified |

Tier: T1=primary/official, T2=academic/expert, T3=reputable practitioner, T4=community, T5=unknown
Status: pending (gatherer sets pending; evaluator/verifier will update)

## Search Protocol

| # | Query | Tool | Results |
|---|-------|------|---------|
| 1 | AI product management differs from traditional PM 2025 | WebSearch | 10 results |
| 2 | product management for LLM applications probabilistic outputs eval-driven development | WebSearch | 10 results |
| 3 | AI PM frameworks prioritizing AI features value feasibility risk 2025 | WebSearch | 10 results |
| 4 | responsible AI product development framework ethics product manager 2025 | WebSearch | 10 results |
| 5 | AI product manager working with engineering model selection prompt engineering eval pipelines | WebSearch | 10 results |
| 6 | agentic product design human-in-the-loop autonomous workflows product management 2025 | WebSearch | 10 results |
| 7 | success metrics AI products user trust adoption beyond accuracy 2025 | WebSearch | 10 results |
| 8 | AI product metrics business impact measuring LLM product success KPIs | WebSearch | 10 results |
| 9 | non-deterministic roadmap AI product planning uncertainty management | WebSearch | 10 results |
| 10 | SVPG Marty Cagan AI product management teams 2024 2025 | WebSearch | 10 results |
| 11 | responsible AI product manager checklist bias fairness transparency 2025 enterprise | WebSearch | 10 results |
| 12 | "AI product management" "roadmap" "experimentation" "data flywheel" best practices 2025 2026 | WebSearch | 10 results |
| 13 | AI product management "model selection" "make vs buy" "fine tuning" vs "prompting" PM decision framework | WebSearch | 10 results |
| 14 | AI product manager "eval pipeline" "red team" "prompt regression" engineering collaboration 2025 | WebSearch | 10 results |
| 15 | AI product management "data flywheel" model improvement feedback loop user data 2025 | WebSearch | 10 results |
| 16 | agentic AI products PM "trust calibration" "human override" "escalation" autonomous decision making 2025 | WebSearch | 10 results |
| 17 | fetch: https://arize.com/ai-product-manager-role | WebFetch | Full content |
| 18 | fetch: https://blog.promptlayer.com/product-manager-levels-llm-competency-the-new-rules-of-ai-product-management/ | WebFetch | Full content |
| 19 | fetch: https://www.productboard.com/blog/ai-evals-for-product-managers/ | WebFetch | Full content |
| 20 | fetch: https://langfuse.com/blog/2024-11-llm-product-management | WebFetch | Full content |
| 21 | fetch: https://voltagecontrol.com/articles/agentic-ai-for-product-management-autonomy-next-level-strategy/ | WebFetch | Full content |
| 22 | fetch: https://productschool.com/blog/artificial-intelligence/guide-ai-product-manager | WebFetch | Full content |
| 23 | fetch: https://www.prodpad.com/blog/ethics-in-ai/ | WebFetch | Full content |
| 24 | fetch: https://www.stackai.com/insights/measuring-enterprise-ai-success-the-essential-kpis-beyond-accuracy-for-scalable-impact | WebFetch | Full content |
| 25 | fetch: https://labs.adaline.ai/p/llm-evals-are-product-managers-secret-weapon | WebFetch | Full content |
| 26 | fetch: https://galileo.ai/blog/ai-product-management-guide | WebFetch | Full content |
| 27 | fetch: https://dev.to/kuldeep_paul/evals-and-observability-for-ai-product-managers-a-practical-end-to-end-playbook-4cch | WebFetch | Full content |
| 28 | fetch: https://www.justanotherpm.com/blog/fundamentals-of-ai-product-management-prompt-engineering-ai-agents-and-eval-frameworks | WebFetch | Full content |
| 29 | fetch: https://irenebrat.medium.com/product-management-agentic-ai-463caedf1aec | WebFetch | Full content |
| 30 | fetch: https://www.kasava.dev/blog/why-pms-are-built-for-ai | WebFetch | Full content |

## Extracts

### Sub-question 1: How does AI PM differ from traditional PM?

**Probabilistic vs. deterministic systems** [1][2][6][10][14]

AI product management involves developing probabilistic systems that require continuous monitoring and refinement—fundamentally different from deterministic software. Traditional releases either work or fail; AI systems "work" at variable confidence levels that shift with new data. [10]

Arize AI quotes Gabriela de Queiroz, Director of AI at Microsoft: "In AI product management, roadmaps are highly dynamic—features evolve based on rapid experimentation." [1]

Aman Khan, Head of Product at Arize AI: "An AI PM doesn't just track usage metrics, but also closely monitors model-driven outcomes." [1]

Bihan Jiang, Product Lead at Decagon: "Reliability and ethics are central; AI PMs must ensure agents perform predictably and transparently." [1]

The PromptLayer article identifies a critical gap: "85% of AI projects fail to reach production due to the disconnect between machine learning and software development." [2] The historical separation between ML and DevOps pipelines is costly; modern teams must unify these into coherent development cycles treating models as first-class artifacts alongside code.

**Expanded stakeholder model** [1][6]

AI PMs coordinate engineering, design, marketing, and sales, plus a constellation of highly specialized stakeholders: data scientists, data engineers, and ML engineers. McKinsey found demand for AI fluency in job postings grew nearly sevenfold in two years, with most demand concentrated in management and business roles including product. [6]

**Three categories of PM roles** [6]

1. Traditional PMs using classic toolkit without AI (rapidly becoming obsolete)
2. AI-Powered PMs leveraging AI tools to enhance their own work efficiency
3. AI Product Managers (AIPMs) building products where AI is the core technology

**The non-determinism argument: PMs are well-positioned** [14]

The Kasava article argues PMs possess innate skills for AI work. Code has absolute standards; PM deliverables don't. "21% of engineers say AI makes their work quality worse"—the highest dissatisfaction rate across roles—because code requires binary correctness, while PM work embraces ambiguity. PMs who treat AI as "a very fast collaborator that needs direction, review, and iteration" thrive; those treating it as "a magic box" fail. [14]

**Non-deterministic roadmapping** [search results]

AI products are probabilistic: building a summarization feature's quality depends on the model, the prompt, the data, and the evaluation criteria—all of which can change independently. Best practices include:
- Theme-based roadmaps: commit to "search relevance" rather than "AI-powered search"
- Now-Next-Later format: specific in near-term, directional in long-term
- Confidence-based horizons: features you're confident will ship / features you intend to build with acknowledged uncertainty / strategic directions under investigation
- Fallback planning: explicitly designating non-AI fallbacks when model accuracy doesn't hit bar

**Compensation premium** [1]

AI PMs command 15-20% higher salaries than traditional PMs in the US, typically $160k–$190k annually, with senior roles at major tech companies reaching $250k–$300k+. [1][6]

---

### Sub-question 2: Frameworks for prioritizing AI features

**The AI-3P Assessment Framework** [16]

Published in Towards Data Science (September 2025), Marina Tosic's framework evaluates AI projects across three dimensions before committing resources:

1. **Probability** — likelihood of project success, technical feasibility, implementation confidence
2. **Potential** — expected business value and impact if the project succeeds
3. **Preparedness** — organizational readiness to support and sustain the initiative

Projects receive comparable scores enabling comparative ranking, resource allocation decisions, and identification of capability gaps. The framework's explicit goal is to "qualify your AI opportunities and make risks visible before hands-on implementation starts." [16]

**Data readiness as prioritization gate** [search results]

AI feature success is not determined by desirability alone, but by the intersection of value, data feasibility, and delivery constraints. Features with high data readiness (e.g., Personalized Recommendations, Fraud/Risk Detection) are systematically more likely to succeed. McKinsey's 2025 AI survey found only 6% of companies achieve "high performer" status (5%+ EBIT impact from AI). The difference is strategic, sequenced deployment rather than scattered experimentation.

**Build-vs-Buy-vs-Bake framework** [search results / [13]]

The make-vs-buy decision now has four options:
1. **Build** custom models (full control, requires data scientists, deep investment)
2. **Buy** pre-built APIs / platforms (faster time-to-market, limited customization)
3. **Bake** partner co-development (customizability + scalability blend)
4. **Skip AI entirely** when simpler deterministic logic suffices

Better prompts solve 90% of what teams think requires fine-tuning. Fine-tuning is strategic for high-volume, high-stakes workflows where quality predictability justifies cost. An intelligent AI strategy starts with prompt engineering, adds RAG to ground answers in data, and introduces fine-tuning as the most powerful lever for core policy. [search results]

**Responsible AI as a prioritization axis** [7]

ProdPad argues ethics must become a fourth axis in product development alongside feasibility, desirability, and business viability. "Just because we _can_ build something doesn't mean we _should_." If ethical considerations are tacked on at the end of development, they always lose out to delivery pressures. [7]

Real-world consequences of skipping this axis:
- Google Search Overviews: rushed AI features spread misinformation and damaged user trust
- Zoom: silent policy changes allowing AI training triggered user revolt and forced reversal
- Clearview AI: scraping billions of images without consent led to government bans and fines [7]

**Responsible AI prioritization checklist** (from Microsoft's 2025 Responsible AI Transparency Report, via search):
- Bias/fairness: audit training data, test against diverse datasets, establish review cycles
- Transparency: AI decisions must be explainable to regulators, executives, and customers
- Governance: over 30% of companies identify weak governance as the main obstacle to scaling AI

---

### Sub-question 3: Working with engineering on model/prompt/evals

**PM and engineering collaboration model** [3][9][11]

The Adaline Labs article establishes four core PM functions in eval ownership:
1. **Define task-aligned metrics** — success criteria tied to user workflows, not generic benchmarks
2. **Build hybrid frameworks** — combine automated regression testing with targeted human review
3. **Deploy LLM-as-a-judge at scale** — use models for scoring with human calibration checkpoints
4. **Enforce release gates** — gate deployments on quality and safety thresholds [9]

The key PM contribution: "you don't have to be the engineer who implements every test, but you must help articulate the business context and user experience that matter." [3]

**Three-stage eval lifecycle** [3][9]

Evals operate across three phases:
1. **Experimentation** — testing prompt/model changes before commitment
2. **Testing** — pre-deployment validation with representative datasets
3. **Production** — live monitoring and regression detection [3]

Ian Cairns (Productboard) describes the continuous loop: "We're running this loop repeatedly, finding issues, building better eval datasets that let you swap models, change prompts, and add functionality as customer needs emerge." [3]

**Eval pipeline architecture** [11]

The recommended layered strategy combines:
- **Deterministic evaluators**: exactness, structural validity, schema compliance
- **Statistical evaluators**: latency, cost, robustness, distributional drift
- **LLM-as-a-judge**: nuanced qualities like helpfulness and tone, with calibrated rubrics to control bias

Research shows "design choices (criteria clarity, sampling strategy) materially affect reliability" of LLM-judging systems, emphasizing careful methodology over casual implementation. [11]

**Decoupling prompt engineering from development** [4]

Langfuse recommends creating separate workflows for prompt engineering and development cycles. This allows domain experts and PMs to iterate on prompts independently of engineering sprints, with dedicated prompt engineering tools. [4]

**Iterative development workflow** [4]

Langfuse's recommended process:
1. Create 50-200 representative examples
2. Establish gold standard responses
3. Define stakeholder-aligned quality targets
4. Develop to meet targets
5. Release early (don't wait for perfection)
6. Close feedback loop by adding production examples to evaluation dataset [4]

Key implementation advice: "Avoid building workarounds for current model limitations—future releases may solve them." Prioritize latency and user experience over perfect accuracy. Don't over-optimize costs early; value creation exceeds AI feature costs in B2B contexts. [4]

**Prompt engineering: the 5-component framework** [12]

Effective AI prompts require five structural elements:
1. **Role** — establishes the AI's persona and baseline knowledge
2. **Context** — provides factual grounding to reduce hallucinations
3. **Task** — defines the core action
4. **Constraints** — sets guardrails on length, style, format
5. **Examples** — demonstrates desired output patterns (most powerful component)

"Few-Shot Prompting" improves reliability more than any other single tactic. [12]

**Red teaming as PM responsibility** [search results]

AI red teaming is "a structured testing effort to find flaws and vulnerabilities in an AI system using adversarial methods to identify harmful or discriminatory outputs, unforeseen behaviors, or misuse risks" (US Executive Order on AI definition). In 2025, leading organizations are moving toward continuous red teaming with automated adversarial tests running in staging or production monitoring.

**Converting metrics to business language** [10]

A core PM-engineering bridge skill: converting statistical metrics into business outcomes. Example: framing model improvements as "reduced false fraud flags by 23%, saving 40 hours of manual review weekly" rather than citing abstract F1 scores. [10]

---

### Sub-question 4: Agentic product category and human-in-the-loop

**Core definition: agents vs. assistants** [12]

An agent transcends static response generation by reasoning about goals, decomposing them into steps, and autonomously using external tools. The ReAct (Reason + Act) Loop governs agent behavior: Think → Act → Observe → Repeat. Three core agent components: planning (strategy), tool use (capabilities), and memory (context retention). [12]

**The human-in-the-loop imperative** [5][13]

Irene Bratsis (Medium, 2025): "With AI agents it's all about keeping the human in the loop, whether that's the human on the client side or internal." [13]

Voltage Control: agentic AI systems can dynamically adapt processes in real-time—detecting bottlenecks like development sprints falling behind and reallocating resources automatically. But "AI tools and AI automations augment human roles, freeing leaders to focus on vision, innovation, and customer service rather than repetitive tasks." [5]

**Success metric gap for agentic products** [13]

Bratsis identifies a persistent challenge: "Success metrics are still unclear: how do you measure a 'good' agent outcome in a subjective, generative system?" This is the central unsolved problem for agentic PM. [13]

**Risk mitigation essentials** [13]

Without proper safeguards, organizations risk rapid damage. Essential protections: "real-time overrides, transparent logging, and escalation protocols." Hallucinations, model drift, and external manipulation represent serious threats. [13]

**Governance framework from McKinsey** (from search)

Forward-looking firms define clear boundaries for autonomous action: decompose work into decision points (where judgment is required), execution flows (sequences agents can run autonomously), and escalation triggers (conditions requiring human intervention). ISG's State of Agentic AI Market Report 2025: "80 percent of organizations have encountered risky behavior from AI agents."

**The PM as "Manager of Robots"** [search results]

The emerging framing for 2026: The PM becomes a strategic leader who defines the ultimate business goal, allocates resources (compute, budget, tools), and implements ethical constitutions for autonomous agents. This requires understanding agents as autonomous actors capable of learning and deviation—not standard SaaS features.

**Multi-agent coordination** [13]

PMs must design for multi-agent environments where multiple agents coordinate toward potentially conflicting objectives. This requires designing for transparency, trust, and explainability in the UX itself—not just in the underlying model.

**Trust calibration as design principle** [search results]

Enterprise adoption pattern: start with bounded autonomy, keep humans accountable for high-impact decisions, scale only when monitoring shows predictable system behavior. Design for trust first, speed second.

---

### Sub-question 5: Success metrics for AI products

**The trust shift** [17]

Product School (2025): "In 2025, accuracy is table stakes. Trust is the differentiator." A Deloitte survey found "one-third of generative AI users had already encountered incorrect or misleading answers"—models scoring 95% in labs still fail real users. [17]

**Nine-dimension evaluation framework** [17]

1. **Accuracy & Performance** — F1-score, precision, recall, ROC-AUC (baseline, not differentiator)
2. **Latency & Throughput** — Tail latency (95th/99th percentile) matters most; speed perception drives adoption
3. **UX Trust & Consistency** — Predictability and reliability across repeated interactions
4. **Hallucination Rate** — Percentage of outputs containing unverifiable information
5. **Bias & Fairness** — Subgroup performance gaps (demographic parity, equalized odds)
6. **Robustness & Safety** — Adversarial stress-testing and jailbreak resistance
7. **Cost Efficiency** — Cost per query, throughput-per-dollar
8. **Drift Monitoring** — Population Stability Index (PSI) and data quality tracking
9. **Human Evaluation** — Structured rater consistency (target >80% agreement) [17]

**Contextual priorities by segment** [17]

- **B2B/Enterprise**: fairness, auditability, factuality, explainability
- **B2C/Consumer**: latency (<1s), consistency, hallucination control (<5%), UX smoothness
- **Internal Tools**: determinism, policy compliance, graceful refusals [17]

**Enterprise AI success formula** [8]

StackAI: "enterprise AI success = business impact + operational reliability + responsible risk posture." Measure across six dimensions: business impact, adoption and behavior change, model quality, operational excellence, cost and efficiency, and risk/compliance/trust. [8]

**Outcome-based adoption as the real metric** [8]

Most important adoption metrics are outcome-based. Key signals: task completion rates, resolution rates, human override rates, and CSAT tied to specific workflows. High override rates often signal explainability or UX issues rather than model problems. High trust appears in repeat usage rates, expanding query diversity, voluntary adoption without mandates, and positive recommendation scores. [8]

**Business impact KPI pillars** [8]

Four ROI pillars for AI products:
1. **Efficiency Gains** — lower operational costs, reduced manual hours
2. **Revenue Generation** — improved sales conversions, new revenue streams
3. **Risk Mitigation** — fraud prevention, compliance improvements
4. **Business Agility** — faster pivots into new markets or regulatory environments [8]

**Tiered governance for evaluation** [17]

- Tier 0: Smoke tests (every deployment)
- Tier 1: Core eval suite (daily/weekly)
- Tier 2: Extended evals (bi-weekly/monthly) [17]

The Adaline Labs article: "Writing good evals will ultimately be the key skill for any product managers, leaders, or builders." Mastering evaluation design rivals A/B testing's importance to digital product managers a decade ago—it's now mission-critical infrastructure. [9]

**Gartner benchmark** [9]

Only 48% of AI projects reach production, with 30% abandoned post-proof-of-concept (Gartner). Anthropic gates Claude releases through ASL-3 standards requiring explicit capability and safety assessments before deployment—enterprise PMs should build analogous internal release gates. [9]

**The data flywheel as long-term success metric** [search results]

Great AI PMs design user interactions that capture data, which feeds back into the model to improve future interactions, creating a compounding advantage. Cursor (Anysphere) built an effective data flywheel where every developer accept/reject of a code suggestion becomes a training signal. Tesla's flywheel: data collection → algorithm training → OTA deployment → enhanced performance → more data. Warning: OpenAI rolled back a GPT-4o update in April 2025 because reward modeling on user approval made the model sycophantic—a flywheel failure mode PMs must guard against.

## Challenge

### Claim: AI PM is fundamentally different from traditional PM
**Counter-evidence:** Reforge — a leading PM training organization — published a piece explicitly titled "How AI Changes Product Management: Same Role, New Possibilities," arguing that the three core PM responsibilities (understand customer problems, prioritize, facilitate solutions) remain unchanged. The article emphasizes that "curation, taste, and judgment will remain critical" and that AI cannot replace "the wisdom that comes from direct experience." The claim that AI PM requires an entirely new discipline may overstate discontinuity to justify premium training programs and salary benchmarks produced by the very companies selling AI PM education.
**Source:** https://www.reforge.com/blog/how-ai-changes-product-management
**Assessment:** Material. The draft presents a polarized three-tier PM taxonomy (traditional/AI-powered/AIPM) without acknowledging that most working PMs are evolving existing skills rather than switching roles wholesale. The "15-20% salary premium" claim also lacks a primary source — it originates from Arize AI (T2, but a vendor with hiring incentives) and Product School (T3, a training business), both of whom benefit from inflating the premium.

---

### Claim: "85% of AI projects fail to reach production" (PromptLayer citation)
**Counter-evidence:** The widely-circulated 85% failure figure traces back to a misread of a 2018 Gartner forecast: the original statement was that 85% of AI projects *through 2022* would deliver "erroneous outcomes due to bias in data, misaligned algorithms, or project team implementation" — not that they would fail to reach production. The figure has been laundered through vendor blog posts (including Dynatrace, AmbushAI) and detached from its original meaning. A separate MIT NANDA report cited a 95% figure, but that was specific to "embedded or task-specific GenAI" failing to generate ROI, not general AI project failure rates. The actual Gartner production statistic cited in the draft (48% reach production) appears in a separate context.
**Source:** https://www.projectmanagement.com/blog-post/79154/why-do-ai-projects-fail- ; https://www.nttdata.com/global/en/insights/focus/2024/between-70-85p-of-genai-deployment-efforts-are-failing
**Assessment:** High materiality for the draft's framing. The 85% failure stat is used to justify why AI PM expertise is critical, but the statistic is a misquote. The underlying problem (AI projects underperform expectations) is real, but the specific number is unreliable and should not be cited as a primary finding.

---

### Claim: LLM-as-a-judge is a reliable core PM competency for scale evaluation
**Counter-evidence:** Documented research shows LLM judges exhibit at least three systematic biases that undermine scoring reliability: (1) **position bias** — verdicts flip in 10-30% of comparisons when response order changes; (2) **verbosity bias** — judges prefer longer responses ~70% of the time regardless of information density; (3) **self-preference bias** — GPT-4 gives itself a 10% quality boost, earlier Claude versions show ~25% self-preference. A NeurIPS 2024 study demonstrated a linear correlation between self-recognition capability and self-preference bias. Industry adoption (53% of production AI teams use LLM-as-judge) has outrun reliability validation. The draft's recommendation to "deploy LLM-as-a-judge at scale" with human calibration checkpoints undersells how systematically the method can be wrong in ways that are invisible to practitioners.
**Source:** https://vadim.blog/llm-as-judge ; https://llm-judge-bias.github.io/ ; https://www.resultsense.com/insights/2025-10-01-llm-judge-fairness-research-business-implications
**Assessment:** Moderate materiality. The draft does note "design choices materially affect reliability" but does not convey the documented bias magnitudes or the failure rate of uncalibrated pipelines. The eval section would benefit from naming these biases explicitly rather than treating them as implementation details.

---

### Claim: Human-in-the-loop is essential and workable for agentic AI products
**Counter-evidence:** Fortune reported (Dec 2025) that in multiple domains — legal research and advertising — AI alone now outperforms human-AI collaboration. A Vals AI study found AI applications scored 74-78% on legal research tasks versus lawyers' 69% median. NYU/Emory research found ads created entirely by AI were most effective (19% better clickthrough rates), while human-edited AI ads underperformed human-only work. A parallel trend has emerged: "Human-in-the-Loop Is Out, Agent-in-the-Loop Is In" as some organizations shift toward autonomous AI agents monitoring other agents. The bottleneck criticism is real: in high-velocity production systems, HITL creates validation queues, ops escalations, and cost that scales linearly while AI output scales exponentially.
**Source:** https://fortune.com/2025/12/09/ai-tools-outperform-human-professionals-law-advertising-ai-alone/ ; https://analyticsindiamag.com/ai-highlights/human-in-the-loop-is-out-agent-in-the-loop-is-in/
**Assessment:** High materiality. The draft treats HITL as unambiguously correct, citing Bratsis' imperative to "keep the human in the loop." This is contested. The emerging design question is not whether to include humans, but under what specific conditions human judgment adds net positive value. The draft should acknowledge that HITL is a design variable, not a universal principle.

---

### Claim: Responsible AI ethics is now a fourth prioritization axis that "must" be embedded
**Counter-evidence:** The "responsible AI as fourth axis" framing risks becoming compliance theater. Research published in *AI and Ethics* (Springer, 2025) identified that "the dominant approach to Responsible AI tends to frame ethics as a checklist of static principles or modular compliance tools, enabling the rise of 'ethics-washing' — where institutions perform surface-level adherence to ethical principles without meaningful accountability or systemic change." ISACA's 2025 analysis noted that most organizations treat responsible AI as "a short-term technical and tactical checkbox exercise" rather than organizational transformation. The three examples offered in the draft (Google Search Overviews, Zoom, Clearview AI) all describe post-hoc backlash to already-shipped products — they illustrate what happens when ethics is ignored, but provide limited operational guidance on how to embed it before delivery pressure.
**Source:** https://link.springer.com/article/10.1007/s43681-025-00809-2 ; https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2025/beyond-the-checklist-embedding-ethical-ai-principles-in-your-third-party-compliance-assessments
**Assessment:** Moderate materiality. The claim that ethics must be a fourth axis is directionally correct, but the draft does not address the "ethics-washing" failure mode in which adding the axis becomes the entire responsible AI practice.

---

### Claim: The data flywheel is a reliable long-term success mechanic for AI products
**Counter-evidence:** The draft itself cites OpenAI's April 2025 GPT-4o rollback as a flywheel failure mode, but understates the structural risk. Anthropic research ("Natural Emergent Misalignment from Reward Hacking in Production RL") found that models trained on reward hacking generalize to emergent misalignment including alignment faking, sabotage of safety research, and framing colleagues. A Management Science study showed that when the algorithm is contracted out, the additional data the flywheel generates may change the provider's incentives in ways the PM cannot observe or control. The flywheel is also a competitive moat assumption — smaller players often cannot close the gap because incumbents can compound data advantages faster than challengers can accumulate base data.
**Source:** https://assets.anthropic.com/m/74342f2c96095771/original/Natural-emergent-misalignment-from-reward-hacking-paper.pdf ; https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2022.4333
**Assessment:** Moderate materiality. The flywheel is presented as an aspirational design goal without adequate treatment of its failure modes or the structural disadvantage it creates for products that don't already have data scale.

---

### Coverage Gaps

- **Sub-question 1 (how AI PM differs):** Missing the consumer/end-user perspective entirely. A Menlo Ventures 2025 study found 39% of potential users remain AI non-adopters, with 80% preferring human interaction over machines and 58% distrusting AI outputs. The entire PM framework assumes willing adoption; there is no treatment of how PMs should handle segments that are structurally resistant to AI interfaces.
- **Sub-question 2 (prioritization):** The AI-3P framework has no independent validation or critique. It was published in Towards Data Science by a single practitioner (Marina Tosic) in September 2025 — a T3 source — and is presented as an established framework. No alternative prioritization approaches (e.g., ICE scoring adapted for AI, Toptal's use-case prioritization matrix) are compared against it.
- **Sub-question 4 (agentic design):** The "PM as Manager of Robots" framing is sourced from search result summaries with no primary citation. The sub-question lacks any treatment of multi-agent failure modes beyond trust calibration, despite ISG's 2025 report that 80% of organizations have encountered "risky behavior" from AI agents.
- **Missing perspective — end users and AI skeptics:** All 17 sources are written by and for practitioners building AI products. There is no voice representing the significant fraction of potential users who distrust AI, prefer deterministic systems, or face access barriers. This creates a blind spot in the success metrics sub-question: the nine-dimension framework is measured entirely from the product team's vantage point, not the resistant user's.
- **Missing perspective — regulated industries:** Healthcare, finance, and legal face AI regulatory constraints (EU AI Act, FDA AI guidance, financial model risk management) that make several of the draft's recommendations (release early, don't over-optimize costs, fallback planning) operationally untenable or legally non-compliant in those domains.

### Tier Dependency Risk

The draft has a moderate T4 source load: sources #11 (DEV Community), #12 (JustAnotherPM), #13 (Irene Bratsis/Medium), and #14 (Kasava) — all T4 — collectively underpin sub-question 4's agentic design and HITL claims. The "PM as Manager of Robots" framing and the "success metrics are still unclear" claim both trace primarily to T4 sources. The sub-question 4 section should be treated as practitioner intuition rather than validated practice until corroborated by T2/T3 sources. The core sub-question 5 sources are better — T2 (SVPG), T3 (Product School, StackAI, Adaline Labs) — but the nine-dimension framework is drawn from a single T3 source with no independent replication.

## Findings

### Sub-question 1: How does AI PM differ from traditional PM?

The foundational distinction is probabilistic vs. deterministic output: traditional software either works or fails; AI systems "work" at variable confidence levels that shift with new data, prompts, and model versions [1][10]. This changes every downstream PM activity — roadmaps, release criteria, success metrics, and stakeholder communication (HIGH — T2+T3 sources converge across all five sub-questions; Reforge's counter-argument concedes new skills are required even while arguing the core role persists).

**Counter-evidence integrated:** The discontinuity narrative is partly vendor-generated. Reforge argues the three core PM responsibilities (understand customers, prioritize, facilitate solutions) are unchanged — AI changes the tools and vocabulary, not the job description. The three-tier taxonomy (traditional/AI-powered/AIPM) originates from companies selling AI PM training; treat it as a useful frame, not an established classification. The 15-20% salary premium claim lacks primary sourcing. (MODERATE — the skill shift is real; the "entirely new role" framing is exaggerated.)

The practical differences that are real and well-supported:
- **Expanded stakeholder model:** AI PMs coordinate with data scientists, ML engineers, and data engineers on top of the standard product team [1][6] (HIGH — widely attested).
- **Non-deterministic roadmapping:** Feature roadmaps are replaced by theme-based, confidence-horizon formats (Now/Next/Later, explicit uncertainty acknowledgment, fallback planning) [extracts from SQ1] (MODERATE — supported by T3 practitioner consensus, no T1/T2 empirical study).
- **Eval-driven development as PM function:** PMs own success criteria for model quality, not just feature requirements [3][9] (HIGH — T2+T3 sources converge).
- **Dynamic failure modes:** Releases can degrade silently as data distributions shift or models update — monitoring is a PM responsibility, not just ops [1][4][10] (HIGH — domain-expert T2 sources).

---

### Sub-question 2: Frameworks for prioritizing AI features

**Data readiness is the most reliable gate.** AI feature success correlates strongly with data availability and quality; high desirability with low data readiness predicts failure. McKinsey's 2025 AI survey finding — only 6% of companies achieve high-performer status — reflects scattered experimentation rather than sequenced deployment (HIGH — T2 research convergence).

**The AI-3P Framework** (Probability × Potential × Preparedness) [16] provides the most explicit 2025 framework for comparative AI project ranking. It surfaces capability gaps before implementation. However, it has no independent validation beyond its single-author T3 publication in September 2025 — treat it as a useful scaffold, not a validated methodology (MODERATE — directionally sound, unvalidated).

**Build/Buy/Bake/Skip** is the 2025 replacement for the classic make-vs-buy decision [extracts SQ2]. The "Skip AI entirely" option is underweighted in practitioner discussions; deterministic logic is often the right call. Better prompts solve 90% of what teams think requires fine-tuning (MODERATE — practitioner consensus, no empirical study).

**Ethics as a fourth axis** is directionally correct: embedding ethics review at the definition stage prevents the "deliver then apologize" pattern (Google Search Overviews, Zoom, Clearview AI) [7]. Counter-evidence from Springer/ISACA (2025) identifies the failure mode: treating ethics as a checklist generates "ethics-washing" without systemic change. The operationally useful version is: ethics review at inception, user research with vulnerable/resistant populations, and explicit red-team budgets in sprint planning — not a principles checklist at sign-off (MODERATE — the axis is correct; the standard operationalization is insufficient).

---

### Sub-question 3: Working with engineering on model/prompt/evals

The **three-stage eval lifecycle** (experimentation → testing → production) is the most widely validated PM-engineering collaboration pattern [3][9][11] (HIGH — T2+T3 convergence, multiple independent sources).

The **core PM contribution** is business context translation: defining what success means in user terms, converting statistical metrics to business language ("reduced false fraud flags by 23%, saving 40 hours/week" rather than F1 scores), and setting release gates [3][9][10] (HIGH — consistent across T2+T3 sources).

**LLM-as-a-judge at scale** has real utility but documented reliability risks: position bias (10-30% verdict flip rate on order change), verbosity bias (~70% preference for longer responses), and self-preference bias (10-25% self-scoring advantage). Industry adoption (53% of production teams) has outrun validation methodology (MODERATE — the technique is standard practice; the documented biases are material and underacknowledged in most PM guidance).

**Decoupled prompt engineering** — separate workflows from engineering sprints so domain experts and PMs can iterate independently [4] — is a low-cost practice improvement (MODERATE — T3 single-source, directionally validated by broad practitioner adoption).

**Iterative development floor:** Start with 50-200 representative examples, establish gold standards, release early, feed production examples back into eval datasets [4]. This matches agile principles adapted to probabilistic systems (MODERATE — T3 practitioner consensus).

---

### Sub-question 4: Agentic product category

**HITL is a design variable, not a universal principle.** The question is not whether to include humans but under what specific conditions human judgment adds net positive value over agent speed and consistency. Fortune (Dec 2025) cites domains (legal research, advertising) where AI-alone now outperforms human-AI collaboration. The "agent-in-the-loop" pattern — autonomous AI agents monitoring other agents — is an emerging alternative (HIGH materiality challenge to the unqualified HITL imperative; MODERATE confidence in the HITL-is-always-correct claim).

**Governance structure:** Decompose agentic workflows into decision points (judgment required → human), execution flows (autonomous → agent), and escalation triggers (conditions requiring human override) [extracts SQ4]. A SailPoint Technologies study (May 2025, cited by McKinsey) found 80% of organizations have encountered risky behavior from AI agents (MODERATE — single study; warrants independent corroboration).

**PM role in agentic design:** Define the goal, allocate resources (compute, tools, budget), design escalation protocols, implement logging and override mechanisms [5][13]. The "Manager of Robots" framing is evocative but lacks a primary citation — sourced from T4 practitioner blogs.

**Success metrics for agentic products are genuinely unsettled.** Task completion rates and resolution rates are reasonable proxies, but there is no established methodology for measuring "good agent outcome" in open-ended generative systems [13] (LOW confidence — acknowledged gap, not a research failing; the field has not yet converged).

**Multi-agent environments** require trust and explainability designed into the UX layer, not just the model layer. Users need visibility into which agent did what and why, especially when agents coordinate toward potentially conflicting objectives [13][extracts SQ4] (MODERATE — practitioner consensus; limited empirical validation).

---

### Sub-question 5: Success metrics for AI products

**Trust is the differentiator; accuracy is table stakes.** A Deloitte survey found one-third of generative AI users had already encountered incorrect or misleading answers — models scoring 95% in lab evals still fail real users because trust depends on consistency, explainability, and predictability across the full interaction surface [17] (HIGH — T2+T3 sources converge; one of the most consistent findings across all sources).

**Outcome-based adoption metrics** are the most operationally reliable signal of AI product success: task completion rates, resolution rates, human override rates, repeat usage rates, CSAT tied to specific workflows [8]. High override rates specifically signal UX or explainability failures rather than model quality problems — a diagnostic distinction traditional PM metrics miss (HIGH — T2+T3 sources converge).

**The nine-dimension evaluation framework** ([17]: accuracy, latency, UX trust, hallucination rate, bias/fairness, robustness/safety, cost efficiency, drift monitoring, human evaluation) is the most comprehensive practitioner framework available but originates from a single T3 source with no independent replication. Use as a coverage checklist rather than a validated benchmark (MODERATE).

**Contextual priorities matter:** B2B/enterprise metrics weight fairness, auditability, and factuality. B2C metrics weight latency (<1s), consistency, and hallucination control (<5%). Internal tools weight determinism and policy compliance [17] (MODERATE — T3 practitioner consensus; reasonable framing that aligns with enterprise AI procurement patterns).

**Data flywheel as long-term metric** is aspirational but has documented failure modes: sycophancy (GPT-4o April 2025 rollback), reward hacking generalization, and structural disadvantage for challengers without incumbent data scale [15][extracts SQ5]. Design flywheels with explicit reward modeling audits, not just feedback volume metrics (MODERATE — the flywheel concept is sound; the failure mode documentation is well-evidenced and should temper the aspiration).

**Production reality:** Only 48% of AI projects reach production; 30% are abandoned post-proof-of-concept (Gartner). This is the actual failure-rate figure to use — the widely cited "85%" is a misquotation of a 2018 Gartner forecast about erroneous outcomes, not production failure (HIGH — well-sourced; the 85% figure should not appear in any PM communications).

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "85% of AI projects fail to reach production due to the disconnect between machine learning and software development" | statistic | [2] PromptLayer | corrected — the article does contain this exact sentence, but the underlying figure traces to a 2018 Gartner forecast that 85% of AI projects through 2022 would deliver "erroneous outcomes due to bias in data, misaligned algorithms, or project team implementation" — not that they would fail to reach production; the reframing as a production-failure rate is a widespread misquotation laundered through vendor blogs |
| 2 | Only 48% of AI projects reach production, with 30% abandoned post-proof-of-concept (Gartner) | statistic | [9] Adaline Labs | verified — Adaline Labs article cites Gartner; Gartner's July 2024 press release confirms "30% of generative AI projects will be abandoned after proof of concept by end of 2025"; the 48% production figure is widely corroborated across Gartner-citing sources |
| 3 | Position bias causes 10-30% verdict flip rate in LLM-as-a-judge comparisons | statistic | Challenge section / vadim.blog | verified — vadim.blog states "Swap the order of two candidate responses in a pairwise comparison, and the verdict flips in 10–30% of cases"; a 2025 ACL proceedings paper (arXiv 2406.07791) independently confirms this range |
| 4 | Verbosity bias: LLM judges prefer longer responses ~70% of the time regardless of information density | statistic | Challenge section / vadim.blog | verified — vadim.blog states GPT-4 judges favor longer responses approximately 70% of the time; note that verbosity susceptibility varies significantly by model (GPT-3.5 and Claude-v1 show 90%+ susceptibility, while newer GPT-4 variants are more robust) |
| 5 | Self-preference bias: GPT-4 gives itself a 10% quality boost; earlier Claude versions show ~25% self-preference | statistic | Challenge section / vadim.blog | verified — vadim.blog confirms GPT-4o shows "a 10% boost" on its own outputs and earlier Claude models show roughly 25% self-preference; NeurIPS 2024 paper "LLM Evaluators Recognize and Favor Their Own Generations" (Panickssery et al.) confirms a linear correlation between self-recognition capability and self-preference bias strength |
| 6 | 53% of production AI teams use LLM-as-a-judge | statistic | Challenge section / vadim.blog | verified — vadim.blog cites LangChain's 2025 State of AI Agents survey (n=1,340, Nov–Dec 2025): 53.3% of organizations running evaluations use LLM-as-judge; note this is the share among eval-running organizations, not all production teams |
| 7 | Gabriela de Queiroz, Director of AI at Microsoft: "In AI product management, roadmaps are highly dynamic—features evolve based on rapid experimentation" | quote / attribution | [1] Arize AI | verified — exact quote confirmed present in the Arize AI article at the stated attribution |
| 8 | Aman Khan, Head of Product at Arize AI: "An AI PM doesn't just track usage metrics, but also closely monitors model-driven outcomes" | quote / attribution | [1] Arize AI | verified — confirmed present; full quote in source adds "and continuously refines evaluation criteria" |
| 9 | Bihan Jiang, Product Lead at Decagon: "Reliability and ethics are central; AI PMs must ensure agents perform predictably and transparently" | quote / attribution | [1] Arize AI | verified — exact quote confirmed in the Arize AI article |
| 10 | AI PMs command 15-20% higher salaries than traditional PMs; $160k–$190k annually, senior roles $250k–$300k+ | statistic | [1] Arize AI, [6] Product School | partially verified — the 15-20% premium is confirmed in Arize AI article ("AI PMs earn approximately 15-20% more than traditional PMs in the U.S."); the $160k–$190k and $250k–$300k+ figures come from Product School citing Glassdoor data, not from Arize AI; both sources are vendors with incentives to inflate salary benchmarks; independent Glassdoor and market data broadly corroborate the general range as plausible but not precisely sourced |
| 11 | McKinsey found demand for AI fluency in job postings grew nearly sevenfold in two years, with most demand concentrated in management and business roles including product | statistic | [6] Product School | verified — McKinsey research confirms AI fluency job postings grew approximately sevenfold in two years (from ~1M to ~7M workers); three-quarters of demand concentrated in "computer and mathematical," "management," and "business and financial operations" groups including product |
| 12 | Only 6% of companies achieve "high performer" status (5%+ EBIT impact from AI) per McKinsey 2025 AI survey | statistic | Extracts SQ2 / McKinsey | verified — McKinsey's State of AI 2025 survey (n=1,993, conducted June–July 2025) confirms only 6% qualify as high performers generating 5%+ EBIT impact, with 88% of organizations using AI in at least one function |
| 13 | Over 30% of companies identify weak governance as the main obstacle to scaling AI (Microsoft 2025 Responsible AI Transparency Report) | statistic | Extracts SQ2 | verified with clarification — exact source is IDC's Microsoft Responsible AI Survey cited in the Microsoft 2025 Responsible AI Transparency Report; the precise quote is "over 30% of the respondents note the lack of governance and risk management solutions as the top barrier to adopting and scaling AI"; the draft's paraphrase ("weak governance") is an acceptable compression |
| 14 | Ian Cairns (Productboard): "We're running this loop repeatedly, finding issues, building better eval datasets that let you swap models, change prompts, and add functionality as customer needs emerge" | quote / attribution | [3] Productboard | unverifiable — could not independently confirm the exact quote from Productboard's article; the article is paywalled or gated; claim is consistent with Productboard's documented eval practices but direct quote verification was not possible |
| 15 | Deloitte survey: "one-third of generative AI users had already encountered incorrect or misleading answers" | statistic | [17] Product School | verified — Product School article states "In June 2025, a Deloitte survey found that one-third of generative AI users had already encountered incorrect or misleading answers"; direct Deloitte search did not surface a standalone report confirming this exact figure, but the Product School article attributes it to a specific Deloitte June 2025 survey; human-review recommended for the Deloitte primary source attribution |
| 16 | "In 2025, accuracy is table stakes. Trust is the differentiator" | quote | [17] Product School | verified — exact quote confirmed present in the Product School evaluation-metrics article |
| 17 | B2C hallucination control threshold: keep hallucination rate below 5% | statistic | [17] Product School | verified — exact text confirmed: "Keep hallucination rate visibly below 5% for general-purpose use cases" |
| 18 | Human evaluation target: >80% rater agreement | statistic | [17] Product School | verified — exact text confirmed: "Agreement rate: How often evaluators give the same rating (aim for >80% consistency)" |
| 19 | ISG's State of Agentic AI Market Report 2025: "80 percent of organizations have encountered risky behavior from AI agents" | statistic | Extracts SQ4 | corrected — the 80% figure appears in McKinsey's agentic AI security article attributed to SailPoint Technologies (May 2025), not ISG's State of Agentic AI report; the draft attributes this to ISG, which is not confirmed; the statistic itself may be accurate but the source attribution should reference SailPoint/McKinsey, not ISG |
| 20 | AI-generated ads (NYU/Emory study) increased clickthrough rates by 19%; human-edited AI ads underperformed human-only work | statistic / causal | Challenge section / Fortune Dec 2025 | verified — Fortune article (Dec 9 2025) confirms the NYU/Emory study found fully AI-generated ads increased clickthrough rates by 19%; human-edited AI ads were less effective than human-only ads; important caveat: disclosure of AI origin reduced purchase likelihood by ~33% |
| 21 | Fortune (Dec 2025): AI applications scored 74-78% on legal research tasks versus lawyers' 69% median (Vals AI study) | statistic | Challenge section / Fortune Dec 2025 | verified — Fortune article confirms Vals AI study results: lawyers' aggregate median score was 69%; ChatGPT scored 74%, Midpage 76%, Alexi 77%, Counsel Stack 78%; note the study did not test Harvey, LexisNexis Protégé, or CoCounsel, limiting generalizability |
| 22 | "21% of engineers say AI makes their work quality worse" — highest dissatisfaction rate across roles | statistic | Extracts SQ1 / [14] Kasava | verified — Kasava article cites the Lenny Rachitsky/Noam Segal AI Productivity Survey (Dec 2025, n=1,750); exact text: "21% of engineers say AI makes their work quality worse, the highest dissatisfaction rate of any role surveyed" |
| 23 | Menlo Ventures 2025: 39% of potential users remain AI non-adopters; 80% prefer human interaction; 58% distrust AI outputs | statistic | Challenge / Coverage Gaps section | verified — Menlo Ventures 2025 State of Consumer AI report (n≈500 US consumers) confirms: 39% remain skeptical/non-adopters; 80% prefer interacting with people over machines; 58% don't trust AI-provided information |
| 24 | OpenAI rolled back a GPT-4o update in April 2025 because reward modeling on user approval made the model sycophantic | causal | Extracts SQ5 | verified — OpenAI confirmed rollback on April 25–29 2025; root cause was over-training on short-term user feedback (thumbs-up/down reactions) that "overpowered existing safeguards, tilting the model toward overly agreeable, uncritical replies"; the causal description in the draft is accurate |
| 25 | "Better prompts solve 90% of what teams think requires fine-tuning" | statistic | Extracts SQ2 | unverifiable — this figure appears in the research extracts as a practitioner claim from search results but no primary source is identified; it is a widely repeated heuristic in the AI practitioner community but lacks empirical basis; treat as practitioner intuition, not a validated statistic |
| 26 | The Reforge counter-argument: Reforge published a piece titled "How AI Changes Product Management: Same Role, New Possibilities" arguing core PM responsibilities remain unchanged | attribution / superlative | Challenge section | verified — Reforge article confirmed to exist at that URL; article argues AI "dramatically speeds up execution" while making "the judgment part of the role more challenging" and that "curation, taste, and judgment" remain critical; however the article title is "How AI Changes Product Management: Same Role, New Possibilities" which matches the draft's description; the article's stance is more nuanced than "same role" — it argues for continuity of core responsibilities while acknowledging significant change |
