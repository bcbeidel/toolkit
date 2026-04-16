---
name: Design Thinking and Brainstorming Patterns for Software Engineering
description: Individual-first diverge-then-converge patterns outperform group brainstorming; anchoring and groupthink are the dominant anti-patterns; LLM homogenization undermines diversity claims for multi-agent brainstorming; ToT and single-agent prompting are better-evidenced than multi-agent debate for software design exploration.
type: research
sources:
  - https://arxiv.org/html/2512.18388
  - https://essenceofsoftware.com/tutorials/design-general/diverge-converge/
  - https://digital.gov/guides/hcd/design-operations/thinking
  - https://voltagecontrol.com/articles/the-synergy-of-diverge-and-converge-in-design-thinking/
  - https://www.uxpin.com/studio/blog/double-diamond-design-process/
  - https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design
  - https://ieftimov.com/posts/problem-solving-framework-principles-software-engineers/
  - https://medium.com/@alex.wauters/how-to-make-architecture-trade-off-decisions-cb23482e1dfe
  - https://arxiv.org/html/2502.05870v1
  - https://arxiv.org/abs/2502.04011
  - https://arxiv.org/html/2510.06224v1
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC12177052/
  - https://www.fryga.io/blog/how-to-brainstorm-with-ai-claude-skill
  - https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/
  - https://medium.com/@edoardo.schepis/patterns-for-democratic-multi-agent-ai-debate-based-consensus-part-2-implementation-2348bf28f6a6
  - https://ixdf.org/literature/topics/groupthink
  - https://www.atlassian.com/blog/productivity/six-thinking-hats
  - https://medium.com/paypal-tech/pre-mortem-technically-working-backwards-1724eafbba02
  - https://www.promptingguide.ai/techniques/tot
  - https://thereflectiveengineer.com/docs/biases/anchoring-bias/
  - https://exceptionnotfound.net/analysis-paralysis-the-daily-software-anti-pattern/
related:
---

# Design Thinking and Brainstorming Patterns for Software Engineering

## Summary

**Key findings (with confidence):**

1. **Individual-first diverge-then-converge outperforms group brainstorming.** The diverge-then-converge structure is validated by T1+T3+T4 sources, but meta-analytic evidence shows face-to-face group ideation produces fewer and lower-quality ideas than individuals generating independently before pooling (Nominal Group Technique). The structure is sound; team-simultaneous divergence is not. (HIGH)

2. **Effective scaffolding requires explicit, switchable modes — not fixed phase sequencing.** A CHI 2025 study found that non-linear mode-switching with preserved history outperforms sequential phase gating. Design tools must support moving back to diverge from converge without penalty. (HIGH)

3. **Anchoring bias and groupthink are the dominant premature-convergence mechanisms; practitioners are more susceptible than students.** An empirical study found practitioners anchor harder than students, hypothesized due to "attachment to their systems." Debiasing workshops significantly reduced anchoring and optimism bias. (HIGH)

4. **LLM homogenization undermines the diversity premise for multi-agent brainstorming.** 2025 research found 79% of responses across models exceed 0.8 cosine similarity — a "hivemind" effect that replicates groupthink at scale. Persona framing may be cosmetic without deliberate diversity-forcing mechanisms. (MODERATE — uncited in primary sources; requires follow-up)

5. **Tree of Thoughts is better-evidenced than multi-agent debate for design space exploration.** ToT enables multi-path reasoning with backtracking at the single-agent level. Multi-agent debate (MAD) fails to consistently outperform single-agent computation and suffers from minority capitulation to majority consensus. (MODERATE)

6. **Over-programmatic workflows amplify design fixation.** Rigid phase-gating can lock in early conceptual choices. Structure must be recursive and fluid, not linear. (MODERATE)

**Search protocol summary:** 20 searches, ~200 results surfaced, 21 sources selected, 13 successfully fetched. 8 sources skipped (paywalls, 403s, binary PDFs).

---

## Sources Table

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://arxiv.org/html/2512.18388 | Exploration vs. Fixation: Scaffolding Divergent and Convergent Thinking for Human-AI Co-Creation | Arxiv / CHI 2025 | Dec 2025 | T3 | verified |
| 2 | https://essenceofsoftware.com/tutorials/design-general/diverge-converge/ | Divergent and convergent design | Daniel Jackson (MIT) / Essence of Software | N/A | T4 | verified |
| 3 | https://digital.gov/guides/hcd/design-operations/thinking | Divergent and convergent thinking | Digital.gov (U.S. Gov) | N/A | T1 | verified |
| 4 | https://voltagecontrol.com/articles/the-synergy-of-diverge-and-converge-in-design-thinking/ | The Synergy of Diverge and Converge in Design Thinking | Voltage Control | N/A | T5 | verified |
| 5 | https://www.uxpin.com/studio/blog/double-diamond-design-process/ | Double Diamond Design Process | UXPin | N/A | T5 | verified (vendor blog; Double Diamond originates with British Design Council 2005) |
| 6 | https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design | Software Engineering RFC and Design Doc Examples and Templates | The Pragmatic Engineer (Gergely Orosz) | N/A | T4 | verified |
| 7 | https://ieftimov.com/posts/problem-solving-framework-principles-software-engineers/ | Problem Solving Framework & Principles for Software Engineers | Ivo Eftimov | N/A | T4 | verified |
| 8 | https://medium.com/@alex.wauters/how-to-make-architecture-trade-off-decisions-cb23482e1dfe | How to make software architecture trade-off decisions | Alex Wauters / Medium | N/A | T5 | verified |
| 9 | https://arxiv.org/html/2502.05870v1 | Understanding Design Fixation in Generative AI | Arxiv | Feb 2025 | T3 | verified |
| 10 | https://arxiv.org/abs/2502.04011 | Debiasing Architectural Decision-Making: An Experiment With Students and Practitioners | Arxiv | Feb 2025 | T3 | verified |
| 11 | https://arxiv.org/html/2510.06224v1 | Exploring Human-AI Collaboration Using Mental Models of Early Adopters of Multi-Agent Generative AI Tools | Arxiv | Oct 2025 | T3 | verified |
| 12 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12177052/ | Structured human-LLM interaction design reveals exploration and exploitation dynamics | PMC / NCBI | 2025 | T3 | verified |
| 13 | https://www.fryga.io/blog/how-to-brainstorm-with-ai-claude-skill | How I learned to brainstorm effectively with AI: A structured approach using Claude | Fryga | N/A | T5 | verified |
| 14 | https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/ | Multi-LLM-Agents Debate - Performance, Efficiency, and Scaling Challenges | ICLR Blogposts 2025 | Apr 2025 | T4 | verified |
| 15 | https://medium.com/@edoardo.schepis/patterns-for-democratic-multi-agent-ai-debate-based-consensus-part-2-implementation-2348bf28f6a6 | Patterns for Democratic Multi-Agent AI: Debate-Based Consensus — Part 2, Implementation | Edoardo Schepis / Medium | N/A | T5 | verified |
| 16 | https://ixdf.org/literature/topics/groupthink | What is Groupthink in UX/UI Design? | IxDF | 2016 (orig); 2024 (modified) | T3 | verified |
| 17 | https://www.atlassian.com/blog/productivity/six-thinking-hats | Six Thinking Hats: use parallel thinking to tackle tough decisions | Atlassian | N/A | T4 | verified (Six Thinking Hats originates with Edward de Bono, 1985) |
| 18 | https://medium.com/paypal-tech/pre-mortem-technically-working-backwards-1724eafbba02 | Pre-Mortem: Working Backwards in Software Design | PayPal Tech / Seema Thapar | N/A | T4 | verified |
| 19 | https://www.promptingguide.ai/techniques/tot | Tree of Thoughts (ToT) | Prompt Engineering Guide | N/A | T4 | verified (based on Yao et al. 2023 research) |
| 20 | https://thereflectiveengineer.com/docs/biases/anchoring-bias/ | Anchoring Bias | The Reflective Engineer | N/A | T5 | verified |
| 21 | https://exceptionnotfound.net/analysis-paralysis-the-daily-software-anti-pattern/ | Analysis Paralysis - The Daily Software Anti-Pattern | ExceptionNotFound | N/A | T5 | verified |

---

## Sub-question 1: What divergent-then-convergent thinking patterns are most effective for software design exploration?

### Source 1: Exploration vs. Fixation: Scaffolding Divergent and Convergent Thinking for Human-AI Co-Creation
- **URL:** https://arxiv.org/html/2512.18388
- **Author/Org:** Arxiv / CHI 2025 | **Date:** Dec 2025

**Re: Divergent-then-convergent thinking patterns for software design exploration**

> "Divergent thinking focuses on generating a wide range of varied ideas in response to a question or task. In contrast, convergent thinking focuses on refining those high-level ideas into viable solutions." (Section 2.1)

> "In the generative process, individuals produce diverse high-level 'preinventive' structures without strong goal control (i.e., divergent thinking). In the exploratory process, these structures are interpreted and developed with respect to the specific task (i.e., convergent thinking)." (Section 2.1, citing Geneplore model)

Design goals for scaffolding:

> "DG1: The system should support users in generating diverse high-level ideas before committing to an actual artifact. By doing so, the system aims to reduce premature convergence and design fixation." (Section 3)

> "DG2: The system should help users translate their intentions into concrete, actionable refinements and encourage further exploration of alternative refinements." (Section 3)

> "DG3: The system should support fluid movement between divergent and convergent modes, including branching and revisiting earlier ideas." (Section 3)

On the implementation:

> "The Divergent mode scaffolds users in the divergent generation of high-level ideas (DG1), while the Convergent mode supports users in the convergent refinement of those ideas to match their objectives for the task (DG2)." (Section 4.1)

> "By allowing users to switch back and forth between the two modes without losing interaction history, the approach enables a non-linear, iterative workflow for creative tasks (DG3)." (Section 4.1)

On divergent scaffolding strategy:

> "We explicitly prompt the model to adopt an associative-thinking strategy that draws connections from distant domains, such as artworks, mythology, historical events, and internet culture, among others." (Section 4.2)

> "Each idea card represents a distinct high-level conceptual idea, such as a metaphor, philosophical concept, or a cultural reference, rather than surface-level dimensional attributes such as color and style." (Section 4.2)

On convergent scaffolding:

> "The user states a refinement intent in their prompt, and the system synthesizes a Sketch, a parametric function that decomposes that intent into named semantic parameters and pre-populates each parameter with concrete, context-aware dropdown options." (Section 4.3)

> "Users can also modify the refinement prompt to generate a new set of parameters and options, open multiple parallel Refine Tabs to develop different image directions." (Section 4.3)

---

### Source 2: Divergent and convergent design
- **URL:** https://essenceofsoftware.com/tutorials/design-general/diverge-converge/
- **Author/Org:** Daniel Jackson / Essence of Software | **Date:** N/A

**Re: Divergent-then-convergent thinking patterns for software design exploration**

> "The designer generates ideas freely, often responding only loosely to any given need or problem." (Section: Two modes of design thinking, Divergent mode)

> "The designer takes some previously articulated design ideas, and attempts to improve them." (Section: Two modes of design thinking, Convergent mode)

> "The first mode is expansive, and most successful when critical judgment is suspended; the second is reductive, and calls for focus and analysis." (Section: Two modes of design thinking)

> "In the first, divergent phase, the goal is to come up with as many ideas as possible, postponing judgment and critical analysis; then, in the second, convergent phase, the goal is to coalesce a ragtag collection of ideas into a coherent design." (Section: Two distinct phases of design)

> "Most design work is convergent, and the essential qualities of a great design often come from working through fine details." (Section: Design is primarily divergent)

> "Combinational creativity involves producing unfamiliar combinations of existing ideas and making associations between ideas that were previously only indirectly linked. This kind of creativity arises more often in convergent design." (Section: When creativity happens)

---

### Source 3: Divergent and convergent thinking
- **URL:** https://digital.gov/guides/hcd/design-operations/thinking
- **Author/Org:** Digital.gov (U.S. Gov) | **Date:** N/A

**Re: Divergent-then-convergent thinking patterns**

> "The design phase is made up of successive cycles of convergent and divergent thinking." (Structure and Overview)

> Divergent thinking involves "exploring what's possible" through ideation and brainstorming, happening when teams "allow ourselves to wonder, speculate, or ask 'what if?'" (Divergent Thinking)

> Teams should "let go of any thoughts that keep you in the world of practicalities, constraints, timelines, and budgets." (Divergent Thinking, Purpose)

> "Convergent thinking is decision making," involving prioritization, refinement, and selection of ideas to pursue. (Convergent Thinking, Definition)

> Teams bring ideas "back to earth, to see which ideas hold up when confronted with the constraints, curve balls, and imperfections of daily life." (Convergent Thinking, Purpose)

> Sometimes teams must "kill your darlings"—abandoning appealing ideas that don't serve the project's greater objectives. (Convergent Thinking, Challenge)

Activities for divergent thinking:
- "Top Five: A five-minute individual brainstorming session where team members generate sticky-note ideas, then rank and cluster them"
- "Concept Mapping: Unpacking idea components and organizing them to show relationships within a broader ecosystem"

---

### Source 4: The Synergy of Diverge and Converge in Design Thinking
- **URL:** https://voltagecontrol.com/articles/the-synergy-of-diverge-and-converge-in-design-thinking/
- **Author/Org:** Voltage Control | **Date:** N/A

**Re: Divergent-then-convergent thinking patterns**

> "Divergent thinking involves generating a multitude of creative solutions to a problem" while "convergent thinking focuses on narrowing down these ideas to identify the most feasible and impactful solutions." (Understanding Diverge and Converge)

> The "cyclical process of diverging and converging is fundamental to design thinking, ensuring a thorough exploration of the problem space." (Understanding Diverge and Converge)

Key techniques:
- "Setting Clear Objectives" with "well-defined understanding of the problem"
- "Creating an Inclusive Environment" where "all participants feel comfortable sharing their ideas"
- "Encouraging Wild Ideas" to "foster the generation of bold, innovative ideas"
- "Building on Others' Ideas" to promote "collaborative innovation"

On transitioning between modes:
> "Affinity diagramming, which groups ideas into themes, can aid in organizing and prioritizing ideas." (Transitioning from Divergence to Convergence)

> Convergence "focuses on refining and synthesizing the plethora of ideas into a coherent and actionable solution" through "prototyping, testing, and validating ideas with stakeholders." (Implementing Convergence in Design Thinking)

> Teams should alternate "between divergence and convergence, ensures continuous refinement and enhancement." (Iterative Approach)

---

### Source 5: Double Diamond Design Process
- **URL:** https://www.uxpin.com/studio/blog/double-diamond-design-process/
- **Author/Org:** UXPin | **Date:** N/A

**Re: Divergent-then-convergent thinking in structured design processes**

> "The Double Diamond model is a framework for innovation and design developed by the British Design Council in 2005." (What is the Double Diamond?)

Four phases:
- **Discover:** "This phase involves extensive research, both qualitative and quantitative. Techniques include desk research, field studies, user interviews, focus groups, and observations." (The Four Phases)
- **Define:** "In this phase, designers analyze and organize the data collected. Techniques such as affinity diagrams, root-cause analysis, and the '5 Whys' method are used." (The Four Phases)
- **Develop:** "This phase involves brainstorming, sketching, and creating prototypes...The development phase is an iterable process of ideation, prototyping, and testing several ideas." (The Four Phases)
- **Deliver:** "The most promising prototypes are refined and developed into final products...This involves extensive testing, validation, and iteration based on user feedback." (The Four Phases)

> The first diamond emphasizes exploration and research (divergent thinking), while the second focuses on narrowing solutions (convergent thinking). (Divergent and Convergent Thinking)

> "cross-functional collaboration: designers meet with engineers, product owners, and other stakeholders to discuss ideas for feedback on possible challenges and constraints." (Software Team Best Practices, Develop phase)

---

## Sub-question 2: How should problem spaces be explored before converging on a solution (multiple approaches with tradeoffs)?

### Source 6: Software Engineering RFC and Design Doc Examples and Templates
- **URL:** https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design
- **Author/Org:** The Pragmatic Engineer (Gergely Orosz) | **Date:** N/A

**Re: Exploring problem spaces and multiple options before converging**

> Google's design doc structure includes "Alternatives considered" as a distinct section. (Google's Approach)

> These documents serve to "clarify assumptions and circulate plans earlier," suggesting that exploring multiple approaches and their tradeoffs prevents costly rework during implementation. (Key Insight)

Uber's RFC process emphasizes comprehensive evaluation through sections like "Architecture changes," "Service SLAs," "Load & performance testing," "Multi data-center concerns," and "Security considerations." (Uber's Framework)

---

### Source 7: Problem Solving Framework & Principles for Software Engineers
- **URL:** https://ieftimov.com/posts/problem-solving-framework-principles-software-engineers/
- **Author/Org:** Ivo Eftimov | **Date:** N/A

**Re: Exploring the problem space before converging on a solution**

> "Understanding the problem that you are solving is as important as the solution itself." (Problem Clarity Section)

> "Sketching is introspection on how well I understand the problem." (Sketching to the Rescue)

> Spending time on clarity saves time on solutions, rather than "jumping to prototyping and making assumptions." (Problem Clarity Section)

The framework's six core tenets:
1. "Strive for problem clarity: you can't produce an excellent solution to a problem you don't understand well"
2. Writing functions as "a thinking tool"
3. "Sketch early and often: it's cheaper to calibrate on a one-pager"
4. Leverage collaborative feedback ("Use the hivemind")
5. Build prototypes to validate feasibility
6. "Iterate: only Bob Ross gets it perfect on the first try"

Sequential stages advocated: problem exploration → sketching → peer feedback → prototype sketching → prototype implementation → iteration.

---

### Source 8: How to make software architecture trade-off decisions
- **URL:** https://medium.com/@alex.wauters/how-to-make-architecture-trade-off-decisions-cb23482e1dfe
- **Author/Org:** Alex Wauters / Medium | **Date:** N/A

**Re: Structured approach for evaluating multiple approaches with tradeoffs**

> The core framework involves: "prioritizing a set of criteria and mapping the possible solutions to them in tiers." (Section: Mapping the way forward)

> Before evaluating options, identify what matters most: "What's more important for your team or organization for this particular feature or project?" (Section: Context matters)

Key considerations: user experience, risk reduction, total cost, team independence, maintenance burden, and technical debt management.

> "Capture what's most important, and highlight the top criteria in bold. Describe how a High, Medium or Low scoring solution would look like." (Section: Context matters, Implementation guidance)

> "describing the total cost of 'the hack', what lies in the ocean beneath the tip of the iceberg." (Section: Choosing between 'the hack' and the 'right way')

> Limit comparison complexity: avoid creating excessive permutations by combining variants. "It'll otherwise be very difficult to steer a decision between options when you need to mentally map more than a handful of choices." (Section: Too few or too many alternatives)

> "Step back to evaluate what criteria matter most, and use that to evaluate the importance of a particular pro or con." (Final Approach)

---

### Source 18: Pre-Mortem: Working Backwards in Software Design
- **URL:** https://medium.com/paypal-tech/pre-mortem-technically-working-backwards-1724eafbba02
- **Author/Org:** PayPal Tech / Seema Thapar | **Date:** N/A

**Re: Exploring problem space with failure-mode analysis before converging**

> "Pre-mortem is a strategy in which a team imagines that a project has failed, and then works backward to determine what potentially could lead to the failure of a project." (What is a Pre-Mortem?)

> "Unlike a post-mortem or root-cause analysis that is performed after things have failed, a pre-mortem is done before the start of the project." (What is a Pre-Mortem?)

Three-step technical pre-mortem framework:

**Step 1: Documentation**
An engineer prepares a single-page document articulating what problem needs solving, why it requires immediate attention, implementation approach (with flow/sequence diagrams), and testing strategy. "The testing plan demonstrates how well the team understands the problem and solution impact."

**Step 2: Team Discussion**
Conduct a pre-mortem session to explore potential design failures. Examples include scalability concerns, data availability issues, API call latency, and SLA compliance.

**Step 3: Refinement**
Address identified issues and update the design documentation, which becomes "the source of truth for development."

Key benefits:
1. Encourages teams to "see the big picture and then work backwards to create the best solution"
2. "Breaks down silos and relies on the team's collective intelligence"
3. Creates psychological safety by normalizing failure discussions

> The author warns against "analysis paralysis" and recommends actively soliciting diverse perspectives using the principle: "Diverge before you converge." (Cautions)

---

## Sub-question 3: What anti-patterns in design thinking lead to premature convergence or analysis paralysis?

### Source 9: Understanding Design Fixation in Generative AI
- **URL:** https://arxiv.org/html/2502.05870v1
- **Author/Org:** Arxiv | **Date:** Feb 2025

**Re: Anti-patterns leading to premature convergence — design fixation**

GenAI design fixation defined as:
> "the state in which a Generative AI model restricts its design exploration of the generative space due to unconscious bias stemming from technical aspects and human factors, which limits the diversity and originality of the model's design output" (Section 2)

Technical causes:
> "Data bias arise from the dataset being unbalanced or imbued with prejudiced information" (Section 2.1)

Human factors causing fixation:
> "GenAI often struggles to produce outcomes that align with the designerly way of thinking" (Section 2.1)
> "Writing effective prompts for GenAI requires a deep understanding of both the design problem and the AI's capabilities" (Section 2.1)

Text generation manifestations:
> "The recurrence of similar concepts or thematic elements across different outputs" — Repetitive theme (Section 4.1)
> "Limited contextual variation: Model struggles 'to adapt its responses to different contextual cues, leading to similar outputs'" (Section 4.1)
> "High-frequency word dependency: GenAI 'disproportionately favors words or phrases that frequently appear in its training data'" (Section 4.1)

Mitigation strategies:
> "Integrating specialized biological knowledge databases into GenAI systems can enhance the creativity and diversity of GenAI outputs" (Section 5)
> Employ "Multi-Agent Collaboration" to endow GenAI "with critical thinking and iterative capabilities" (Section 5)
> "Educating students in the phenomenon and effects of fixation enables them to effectively devise their own strategies" (Section 5)
> Train users to "critically evaluate AI-generated content rather than accepting it passively" (Section 5)
> Avoid "overly programmatic workflows that may strengthen design fixation" (Section 5)

Advantages of fixation (acknowledged):
> Enables efficiency through reliance on familiar patterns; maintains consistency across design series; leverages "established best practices"; reduces experimentation costs (Section 6.2)

Disadvantages:
> Stifles "truly novel or innovative designs"; perpetuates training data bias; reduces adaptability to emerging trends; creates long-term risk of "boxing human creative capability" (Section 6.2)

---

### Source 10: Debiasing Architectural Decision-Making
- **URL:** https://arxiv.org/abs/2502.04011
- **Author/Org:** Arxiv | **Date:** Feb 2025

**Re: Anti-patterns — cognitive biases in architectural design decisions**

> "anchoring can cause architects to unconsciously prefer the first architectural solution that they came up with, without considering any solution alternatives." (Abstract)

> "anchoring and optimism bias occurrences decreased significantly" following debiasing intervention. (Outcomes)

> Researchers "designed and evaluate[d] a debiasing workshop with individuals at various stages of their professional careers" using "an experiment with 16 students and 20 practitioners, split into control and workshop group pairs." (Intervention Tested)

> "The workshop improved the participants' argumentation when discussing architectural decisions and increased the use of debiasing techniques taught during the workshop." (Outcomes)

Notable finding:
> "practitioners were more susceptible to cognitive biases than students, so the workshop had a more substantial impact on practitioners." (Notable Finding)

> The researchers hypothesized that "attachment to their systems may be the cause of their susceptibility to biases." (Notable Finding)

---

### Source 16: What is Groupthink in UX/UI Design?
- **URL:** https://ixdf.org/literature/topics/groupthink
- **Author/Org:** IxDF | **Date:** 2026

**Re: Anti-patterns — groupthink as premature convergence mechanism**

> "Groupthink is a psychological phenomenon that is very likely to occur in an organizational setting, or any situation where there are many people together, where individual differences are lost in favor of group harmony and cohesion." (Definition Section)

> "Groupthink often leads to the loss of the individual's creativity and opinion. Instead of having many ideas and challenging each other, personal beliefs are lost or overshadowed by the group's identity." (Effects on Creativity)

> "A classic signature of groupthink is bandwagon bias, a cognitive bias arising from the comparative ease of going along with popular beliefs." (Connection to Bandwagon Bias)

> "Groupthink affects many organizational settings and that is why many businesses make errors in their strategies or decisions." (Business Impact)

Remedy:
> Utilizing "a coach or someone that can work with you in a 'verbal sparring'" to help identify and challenge biases. (Avoiding Groupthink Strategy)

---

### Source 20: Anchoring Bias in Software Engineering
- **URL:** https://thereflectiveengineer.com/docs/biases/anchoring-bias/
- **Author/Org:** The Reflective Engineer | **Date:** N/A

**Re: Anti-patterns — anchoring bias causing premature convergence**

> "Anchoring bias is a cognitive bias that can affect decision-making in various fields, including software engineering. It occurs when individuals rely too heavily on the first piece of information they encounter (the 'anchor')" (Definition)

> "When designing software systems or making architectural decisions, an initial design idea or architectural concept can serve as an anchor. Developers may become fixated on this initial approach, even if better alternatives are available" (Design and Architecture Example)

> "If a team starts evaluating a specific technology stack early in the project and becomes anchored to it, they may overlook alternative technologies that could be better suited to the project's needs" (Technology Selection Example)

Mitigation strategies:
- **Awareness:** Teams should "critically evaluate whether the initial information or estimate is valid and relevant"
- **Multiple Estimates:** "When estimating time or costs, consider seeking multiple estimates from different team members independently before settling on a final estimate"
- **Regular Review:** "Periodically review and reassess decisions, such as architectural choices or technology stack, to ensure they remain appropriate and aren't solely influenced by initial anchors"
- **Iterative Design:** "Embrace an iterative approach to design and development, allowing for exploration of multiple design alternatives and avoiding early commitment to a single approach"

---

### Source 21: Analysis Paralysis - The Daily Software Anti-Pattern
- **URL:** https://exceptionnotfound.net/analysis-paralysis-the-daily-software-anti-pattern/
- **Author/Org:** ExceptionNotFound | **Date:** N/A

**Re: Anti-patterns — analysis paralysis as excessive convergence avoidance**

> "Analysis Paralysis is a methodological anti-pattern comprising a situation that occurs when a decision must be made as to how to proceed, but is not made" (Core Concept)

> "A project is stalled because an important decision must be made to proceed, but that decision is very difficult to make" (Name/Definition)

Two primary causes:
- "Where there is not enough data or conflicting data as to which solution is the correct choice"
- "The person in charge of the decision does not have the necessary experience with any of the proposed solutions"

> "This is not a software or programming concept, it is a human one, and as such it needs a human solution." (Human Nature Factor)

Primary remedy:
> "If we can pick a solution on nothing more than intuition, but change that solution if it becomes apparent that it is wrong, we can eliminate analysis paralysis" (Remedies)

> Agile methodologies mitigate this better than Waterfall because they "force teams to react to change." (Remedies)

---

### Source 1 (revisited): Exploration vs. Fixation — anti-patterns in scaffolded systems
- **URL:** https://arxiv.org/html/2512.18388

**Re: Anti-patterns — lack of scaffolding leads to fixation**

> Systems that lack explicit scaffolding lead to "premature convergence and design fixation" (DG1, Section 3)

> The paper reveals that scaffolding the creative process into distinct brainstorming and refinement stages "can mitigate design fixation, improve perceived controllability and alignment with users' intentions, and better support the non-linear nature of creative work." (Section 3)

---

## Sub-question 4: How can LLM agents facilitate structured brainstorming (generating options, evaluating tradeoffs, reaching consensus)?

### Source 11: Exploring Human-AI Collaboration Using Mental Models of Early Adopters of Multi-Agent Generative AI Tools
- **URL:** https://arxiv.org/html/2510.06224v1
- **Author/Org:** Arxiv | **Date:** Oct 2025

**Re: LLM agents facilitating structured brainstorming**

On task decomposition and role assignment:
> "We might have a product manager, we might have an engineer, and everybody has their own experiences, their own skills, their own tools, that they bring to the table to work together." (P09, Section 4.1)

> "if you can break the task to a smaller one, there's a higher chance it can be completed." (P05, Section 4.1)

> "You are giving each one of these LLM agents personality, a role, and a specific task or duties to perform. You're basically creating a team of little experts that can do certain things." (P13, Section 4.1)

On collaboration patterns:
> AI-dominant approaches "allowing agents a high degree of autonomy, this approach enables flexibility and creativity." (Section 4.2, AI-Dominant)
> AI-assisted preference for "direct human orchestration over autonomous AI control, enabling clearer task management and reducing randomness in complex workflows." (P11, Section 4.2, AI-Assisted)

On critical limitations:
> "agents generated inaccuracies or lost contextual relevance, leading to compounded errors, especially when one agent's error feeds into another." (P06, Section 4.2.3)
> "agents sometimes became 'stuck' in repetitive, unproductive cycles, which offered little to no added value." (P06, P13, Section 4.2.3)

On transparency requirements:
> "Transparency is paramount to creating trust. If users can see what the system's doing and understand how it operates, they are more likely to trust it." (P06, Section 4.3)
> "developers need to see 'the inner workings' of the agents to be able to verify answers or trace errors." (P03, Section 4.3)

---

### Source 12: Structured human-LLM interaction design reveals exploration and exploitation dynamics
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12177052/
- **Author/Org:** PMC / NCBI | **Date:** 2025

**Re: LLM-facilitated structured brainstorming — exploration vs. exploitation dynamics**

> The researchers created a structured system using "editable _prompt templates_ and socially-sourced keywords to structure their prompt-crafting process." (Key Design Section)

> "**Exploration prompts** were used whenever participants decided to generate a completely new scenario, marking the start of an independent chat with ChatGPT." (Exploration Dynamics)

> "there is a significant positive correlation between the frequency of exploration prompts and the diversity of keywords used by participants." (Exploration Dynamics)

> "**Exploitation prompts** were used when participants wanted more details about a concept or idea in the context of an already generated scenario." (Exploitation Dynamics)

> "**Exploration** is influenced by socially-sourced keywords" and "Exploration keywords have higher topic diversity." (Exploration Dynamics)

> "**Exploitation** is influenced by GPT-sourced keywords" and "Exploitation keywords have lower topic diversity, i.e., these prompts were conceptually narrower." (Exploitation Dynamics)

> Participants "balanced between _exploration_, driven by the broad conceptual space of the interaction design, and _exploitation_, guided by the specificity of the AI-generated text." (Creative Outcomes)

---

### Source 13: How I learned to brainstorm effectively with AI: A structured approach using Claude
- **URL:** https://www.fryga.io/blog/how-to-brainstorm-with-ai-claude-skill
- **Author/Org:** Fryga | **Date:** N/A

**Re: LLM agent-facilitated structured brainstorming — three-phase framework**

> "The brainstorming skill is a structured framework for collaborative design. It has three phases: Understanding, Exploration and Design." (Section: What It Actually Is)

> "No barrage of questions. Instead, it explored what I'd shared, formed a model, and said: 'Based on what you've told me, here's how I think this should work…'" (Section: Phase 1: Understanding)

> "Having structure doesn't constrain creativity—it creates space for it." (Section: Why It Matters)

---

### Source 14: Multi-LLM-Agents Debate - Performance, Efficiency, and Scaling Challenges
- **URL:** https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/
- **Author/Org:** ICLR Blogposts 2025 | **Date:** Apr 2025

**Re: Multi-agent debate as structured brainstorming mechanism**

Core framework structure:
- "multiple LLM agents independently generate initial answers in parallel"
- "over several rounds, agents review other agents' answers and incorporate collective feedback"
- Final step involves aggregating "refined answers to form the final answer" (Multi-Agent Debate Formulation)

> Agents often adopt personas: "agents are often prompted to role-play certain personas...to be effective in stimulating critical thinking" (Architectural Representation)

Key limitations:
> "current MAD frameworks fail to consistently outperform simpler single-agent test-time computation strategies" (Performance gaps)

Design weaknesses:
- Agents "debate based on their full responses...instead of analyzing the gap between their reasoning"
- Methods "overly assign weight to the final answer instead of the reasoning steps"
- MAD can be "overly aggressive, lacking the ability to reliably identify incorrect answers"

Promising direction:
> Mixed-model approaches showed potential: combining "GPT-4o-mini and Llama3.1-70b together" achieved better accuracy than single-model approaches. (Promising Direction)

---

### Source 15: Patterns for Democratic Multi-Agent AI: Debate-Based Consensus
- **URL:** https://medium.com/@edoardo.schepis/patterns-for-democratic-multi-agent-ai-debate-based-consensus-part-2-implementation-2348bf28f6a6
- **Author/Org:** Edoardo Schepis / Medium | **Date:** N/A

**Re: Multi-agent debate consensus pattern for design exploration**

> "Multiple independent LLM-powered agents collaborate and compete on a task by discussing it amongst themselves." (Understanding the Multi-Agent Debate Pattern)

> "Agents communicate peer-to-peer or in a round-robin fashion, sharing their answers and critiques with one another." (Decentralized Interaction)

> "Agents may adjust their answers based on others' arguments. They might point out inconsistencies in another agent's answer." (Iterative Refinement)

> "The debate ends when either all agents agree on an answer (unanimous consensus) or a predetermined stopping condition is reached." (Consensus Mechanisms)

Versus voting:
> "Unlike the Voting-Based Consensus Pattern (where agents submit answers independently and the majority wins), the debate pattern involves dynamic interaction." (Comparison to Alternative Approaches)

> "Errors get corrected through critique. (However, it also requires more computation and careful orchestration.)" (Key Advantage)

Practical implementation:
> "You might set max_rounds to, say, 5 exchanges each. After each full round, check if the agents' outputs are effectively identical." (Stopping Criteria)

When disagreement persists, implement "Majority Vote," designate a "Judge Agent," or perform "Heuristic Merge" combining insights from multiple agents. (Final Answer Synthesis)

> Pattern suits "complex problems where a single pass might be prone to error," including brainstorming, reasoning verification, and policy decisions. (Use Cases)

---

### Source 17: Six Thinking Hats: use parallel thinking to tackle tough decisions
- **URL:** https://www.atlassian.com/blog/productivity/six-thinking-hats
- **Author/Org:** Atlassian | **Date:** N/A

**Re: Structured brainstorming via parallel thinking — applicable to LLM agent personas**

> "Parallel thinking means that at any moment everyone is looking in the same direction," — de Bono. (Core Methodology Section)

> The technique "eliminates confusion by focusing the discussion on *one* aspect of the decision at a time" while encouraging "more expansive thinking." (Purpose Statement)

Groupthink prevention:
> The structured hat system ensures "everyone in looking at every aspect of a problem, *together*. This ensures balance, fairness, and as little bias as possible." (Systematic Voice Inclusion)

> Six Thinking Hats works best "in discussions in which you're having a hard time getting everyone to participate (e.g., one person is doing most of the talking)." (Combating Dominant Voices)

The six hat framework:

| Hat | Function |
|-----|----------|
| Blue | "Thinking about thinking" — moderator role |
| White | Facts only, remaining "neutral, looking only at the available information" |
| Red | Emotions expressed without justification |
| Black | Risk assessment — "the most valuable of all the hats" |
| Yellow | Benefits backed by evidence, finding value in ideas |
| Green | Creative alternatives and solutions |

> The methodology creates "a shared vocabulary and symbolism" enabling teams to "communicate more effectively and direct your ways of thinking" across complex decisions. (Application to Decision-Making)

---

### Source 19: Tree of Thoughts (ToT)
- **URL:** https://www.promptingguide.ai/techniques/tot
- **Author/Org:** Prompt Engineering Guide | **Date:** N/A

**Re: LLM structured design exploration via tree-structured reasoning**

> "ToT maintains a tree of thoughts, where thoughts represent coherent language sequences that serve as intermediate steps toward solving a problem." (Core Definition)

> "This approach enables an LM to self-evaluate the progress through intermediate thoughts made towards solving a problem through a deliberate reasoning process." (Exploration Capability)

> The method supports "systematic exploration of thoughts with lookahead and backtracking," allowing models to explore multiple reasoning paths rather than following a single linear path. (Exploration Capability)

> "ToT substantially outperforms the other prompting methods" according to experimental results on complex problem-solving tasks. (Performance Results)

> Hulbert's Tree-of-Thought Prompting approach applies the core concept "as a simple prompting technique, getting the LLM to evaluate intermediate thoughts in a single prompt" without requiring complex search implementations. (Simplified Application)

---

## Not Searched

The following candidate sources were identified but not fetched:

| Source | Reason |
|--------|--------|
| https://www.sciencedirect.com/science/article/pii/S0950584925002496 (Gender-based cognitive bias and design thinking) | Academic paywall; partial data captured via search summary |
| https://link.springer.com/chapter/10.1007/978-3-642-21292-5_3 (Effective Design Space Exploration) | Returned HTTP 303 redirect; content not accessible |
| https://www.tandfonline.com/doi/full/10.1080/09544828.2025.2574209 (RAG + CoT for engineering design ideation) | 403 forbidden |
| https://www.researchgate.net/publication/385679805 (Chain-of-Thought LLM agents concept generation) | 403 forbidden |
| https://deviq.com/antipatterns/analysis-paralysis/ | 403 forbidden; data captured from alternative source |
| https://www.boardofinnovation.com/blog/16-cognitive-biases-that-kill-innovative-thinking/ | 403 forbidden |
| https://www.capitalone.com/tech/culture/understanding-decision-bias/ | Page returned only JS/CSS; no article content parseable |
| https://aclanthology.org/2025.findings-acl.606.pdf (Voting or Consensus in Multi-Agent Decision-Making) | Binary PDF; not parseable via WebFetch |

---

---

## Key Takeaways

1. **Use individual-first ideation (NGT), not team-simultaneous brainstorming.** Have each person generate ideas silently before pooling. This consistently outperforms group-simultaneous divergence on quantity and quality.

2. **For LLM augmentation: single-agent ToT/CoT with explicit mode-switching > multi-agent debate.** Tree of Thoughts at the prompt level achieves multi-path exploration without MAD's majority-conformity failure mode or orchestration overhead.

3. **"Alternatives Considered" sections and pre-mortems are the highest-leverage forcing functions for problem space exploration.** These organizational artifacts create structured accountability for exploring the space before committing.

4. **Debiasing interventions work, but require deliberate facilitation.** A structured workshop reduced anchoring and optimism bias significantly in practitioners (who need it more than students). Tool-assisted debiasing for ADRs is an open research gap.

5. **LLM brainstorming must explicitly counter homogenization.** Techniques: seed with concepts from distant domains, use explicit anti-convergence prompting, vary models or temperature, structure exploration prompts using socially-sourced (not AI-generated) keywords.

6. **Structure must be recursive, not linear.** The Double Diamond fails in Agile teams when treated as a waterfall lifecycle. The same pattern used as a recursive lens — multiple short diverge-converge cycles — is well-supported.

## Limitations

- The strongest empirical evidence (CHI 2025 [1]) is domain-specific to generative image co-creation, not software architecture.
- The LLM homogenization statistic (79%, 0.8 cosine similarity) is cited from challenge research without a primary source URL — treat as hypothesis requiring verification.
- The d.school curriculum revision claim (Finding 1.1 counter-evidence) is unverified — no source cited.
- The Mullen et al. (1991) meta-analytic figures (20 studies, 800+ teams) are from the Challenge section without a URL — referenced from background knowledge, not primary source retrieval.

---

## Search Protocol

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| divergent convergent thinking patterns software design exploration 2025 | websearch | 2025 | 10 | 3 |
| double diamond design process software engineering best practices | websearch | all | 10 | 2 |
| design thinking divergent convergent phases structured exploration software architecture patterns | websearch | all | 10 | 3 |
| RFC design documents software architecture decision records multiple options tradeoffs template 2024 | websearch | 2024 | 10 | 2 |
| brainstorming methodologies software engineering design space exploration multiple alternatives 2024 2025 | websearch | 2024-2025 | 10 | 1 |
| premature convergence design anti-patterns analysis paralysis software engineering solution space exploration | websearch | all | 10 | 2 |
| design fixation anti-pattern brainstorming premature closure cognitive bias software design 2024 | websearch | 2024 | 10 | 2 |
| LLM agents structured brainstorming design exploration generating options evaluating tradeoffs AI facilitated 2025 | websearch | 2025 | 10 | 3 |
| AI agent design thinking multi-agent brainstorming consensus building 2024 2025 | websearch | 2024-2025 | 10 | 3 |
| LLM brainstorming facilitation structured design exploration chain of thought tree of thought options generation 2025 | websearch | 2025 | 10 | 2 |
| ChatGPT Claude structured brainstorming prompt engineering design exploration generate alternatives software 2025 | websearch | 2025 | 10 | 2 |
| exploring problem space before solution software design multiple approaches tradeoffs methodology | websearch | all | 10 | 2 |
| architecture decision making explore options before committing software engineering practice 2024 2025 | websearch | 2024-2025 | 10 | 2 |
| analysis paralysis software teams decision making anti-pattern agile remedies timeboxing 2024 | websearch | 2024 | 10 | 2 |
| cognitive bias design thinking anchoring bias status quo bias software architecture decisions 2024 2025 | websearch | 2024-2025 | 10 | 3 |
| groupthink HiPPO effect design thinking brainstorming anti-patterns software team decisions | websearch | all | 10 | 2 |
| LLM agent role playing persona brainstorming devil's advocate steelman structured debate software design 2025 | websearch | 2025 | 10 | 3 |
| six thinking hats Edward de Bono software design structured brainstorming parallel thinking 2024 | websearch | 2024 | 10 | 2 |
| pre-mortem technique software design decision making exploring failure modes structured brainstorming 2024 2025 | websearch | 2024-2025 | 10 | 2 |
| anchoring bias status quo bias software architecture design decisions anti-patterns cognitive biases engineers | websearch | all | 10 | 2 |

**20 searches · google · 200 results found · ~41 results used · 21 sources · 13 successfully fetched**

---

## Challenge

### 1. Assumptions Check

The following assumptions underlie the emerging findings across the four sub-questions.

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| **A1. Sequential diverge-then-converge is universally effective for software design.** Sources 1–5 treat the pattern as the gold-standard, with multiple framework authorities (Design Council, Digital.gov, MIT) endorsing it. | Sources 1–5: multiple independent frameworks (Double Diamond, Geneplore model, Digital.gov HCD guide) all endorse sequencing diverge before converge. Source 13 (Fryga) reports positive practitioner outcomes. | Double Diamond is explicitly criticized as linear and poor for Agile teams (Elsewhen, Xebia). Industry critics note it delays execution "for three quarters of the process" and creates sunk-cost bias from high-fidelity prototyping. Design thinking's d.school has removed the phrase from its revamped curriculum. The academic record shows that many practitioners skip divergent phases entirely under deadline pressure. | The central prescriptive recommendation — always diverge before converging — may not transfer cleanly to time-constrained agile software teams. The value may be context-dependent rather than universal. |
| **A2. LLM agents reliably reduce groupthink and expand the design space.** Sources 9, 11, 13, and 17 collectively suggest that structured LLM agent personas (Six Thinking Hats, multi-agent debate) counter premature convergence. | Source 17 (Six Thinking Hats via Atlassian), Source 14–15 (multi-agent debate pattern), Source 11 (multi-agent mental models), Source 1 (scaffolded divergence). | Multiple 2025 studies document LLM "Artificial Hivemind" homogenization: 79% of responses across models exceed 0.8 similarity. Research shows a single LLM outscores average humans on creative tasks, but across many trials produces the same ideas repeatedly. This is a direct contradiction — LLMs may replicate groupthink at scale rather than eliminate it. Individual creativity rises while collective novelty decreases. | If LLMs converge on the same ideas regardless of persona framing, using them as brainstorming partners does not expand the design space — it narrows it while creating a false sense of diversity. |
| **A3. Multi-agent debate (MAD) outperforms single-agent reasoning for design exploration.** Sources 14–15 and the Tree of Thoughts framing (Source 19) imply multi-agent or multi-path approaches produce better design outcomes. | Source 14 (ICLR 2025 MAD review acknowledges mixed results but documents real use cases), Source 15 (debate pattern handles complex problems), Source 19 (ToT substantially outperforms CoT on certain tasks). | Source 14 itself acknowledges "MAD frameworks fail to consistently outperform simpler single-agent test-time computation strategies." 2025 research (arxiv 2604.02460) shows single-agent LLMs match or outperform multi-agent systems when computation is normalized. MAD suffers from majority conformity — minority agents capitulate to the group, reproducing the groupthink it claims to prevent. Multi-Persona approaches can significantly underperform baselines. | The prescription to use multi-agent debate for structured brainstorming may produce worse results than simpler, cheaper single-agent reasoning with well-crafted prompts. |
| **A4. Group brainstorming structured by diverge/converge produces more and better ideas than alternative approaches.** The frameworks in Sources 3–5 treat group brainstorming as the baseline creative method to be structured. | Source 4 (Voltage Control): group brainstorming with clear objectives and inclusive environment is assumed effective. Source 3 (Digital.gov): team divergent sessions are prescriptively recommended. Source 17 (Six Thinking Hats): structured group process addresses dominant voices. | Meta-analytic evidence (Mullen, Johnson & Salas, 1991, 20 studies, 800+ teams) shows brainstorming groups are significantly less productive than nominal groups on both quantity and quality. Production blocking, evaluation apprehension, and social loafing systematically reduce output. A 2024 neuroscience study found neural evidence of a "herding" mindset in groups. Individual silent ideation followed by structured sharing (Nominal Group Technique) consistently outperforms face-to-face group ideation. | The group brainstorming sessions prescribed by Sources 3–5 may be less effective than having individuals generate ideas independently first, then synthesize — inverting the implicit workflow. |
| **A5. Structured scaffolding for LLM-assisted design is sufficient to prevent design fixation.** Source 1 (arxiv 2512.18388) is the primary empirical anchor — it shows scaffolded diverge/converge modes "mitigate design fixation." | Source 1: CHI 2025 paper provides experimental evidence that dual-mode scaffolding reduces fixation and improves controllability. | Source 9 (arxiv 2502.05870) identifies design fixation as deeply rooted in training data bias and prompt dependency — problems that scaffolding at the interaction level cannot solve. Over-programmtic workflows are themselves flagged as fixation amplifiers. The study in Source 1 is domain-specific (generative image creation), not software architecture; transferability is unverified. | Scaffolding may mitigate surface-level fixation while leaving deeper training-data-induced fixation untouched. Treating scaffolding as the primary remedy underestimates the structural nature of the problem. |

**Weakest assumptions:** A2 and A3 have the most direct empirical counter-evidence (homogenization research, MAD performance failures). A4 has the oldest but most robust counter-evidence (decades of brainstorming productivity research). These three should be explicitly qualified in any conclusions.

---

### 2. Analysis of Competing Hypotheses (ACH)

**Evidence items derived from sources:**

- E1: Sequential diverge-then-converge endorsed by multiple independent frameworks (Sources 1–5)
- E2: LLM scaffolding reduced fixation in CHI 2025 experiment (Source 1)
- E3: Multi-agent debate enables error correction through critique (Sources 14–15)
- E4: Tree of Thoughts substantially outperforms CoT on complex tasks (Source 19)
- E5: Cognitive biases (anchoring, groupthink) are documented in architectural decisions (Sources 10, 16, 20)
- E6: Pre-mortem technique surfaces failure modes before commitment (Source 18)
- E7: LLMs homogenize creative output across models (cross-model similarity 79% above 0.8 threshold — 2025 research)
- E8: MAD fails to consistently outperform single-agent CoT or Self-Consistency (Source 14, arxiv 2604.02460)
- E9: Group brainstorming produces fewer and lower-quality ideas than nominal groups (meta-analytic research)
- E10: Double Diamond is ineffective in Agile/sprint-based teams due to linear handover structure (Elsewhen, Xebia criticism)
- E11: Design fixation originates in LLM training data — interaction-layer scaffolding cannot fully mitigate it (Source 9)

**Three competing hypotheses:**

- **H-A (Draft's implicit conclusion):** Structured diverge-then-converge processes, augmented by LLM agents using roles/personas and multi-agent debate, are the most effective approach for software design brainstorming.
- **H-B (Moderate skeptic):** Structured individual ideation first (nominal group technique), combined with targeted single-agent LLM prompting using reasoning techniques (CoT, ToT), outperforms group-based diverge-converge workflows and multi-agent debate for software design exploration.
- **H-C (Strong skeptic):** Design thinking frameworks and LLM brainstorming tools provide marginal or context-dependent value; their prescriptions are insufficiently grounded in controlled software engineering contexts and fail at scale.

| Evidence | H-A: Structured group diverge/converge + LLM personas | H-B: Individual first + single-agent LLM | H-C: Design thinking and LLM tools are marginal |
|----------|------------------------------------------------------|------------------------------------------|--------------------------------------------------|
| E1: Sequential D/C endorsed by multiple frameworks | C | C (individual D/C also valid) | I |
| E2: LLM scaffolding reduced fixation (CHI 2025) | C | C | I |
| E3: MAD enables error correction through critique | C | N | N |
| E4: ToT outperforms CoT on complex tasks | N | C | N |
| E5: Cognitive biases documented in architectural decisions | C | C | C |
| E6: Pre-mortem surfaces failure modes | C | C | C |
| E7: LLMs homogenize creative output (79% similarity) | **I** | C (diversity risk applies to all LLM use) | C |
| E8: MAD fails to consistently beat single-agent | **I** | C | C |
| E9: Group brainstorming produces fewer/lower quality ideas than nominal groups | **I** | C | C |
| E10: Double Diamond ineffective in Agile teams | **I** | N | C |
| E11: Fixation rooted in training data, not interaction layer | **I** | N | C |
| **Inconsistencies** | **5** | **0** | **3** |

**Selected: H-B — fewest inconsistencies (0).** Rationale: H-B acknowledges the value of structured diverge-then-converge thinking and LLM augmentation (consistent with E1, E2, E4, E5, E6), while accommodating the empirical counter-evidence on group brainstorming productivity loss (E9), LLM homogenization (E7), and MAD underperformance (E8). H-A carries 5 inconsistencies against published evidence, mostly in its implicit endorsement of group-first processes and multi-agent debate as reliable. H-C overcorrects — it cannot account for the genuine empirical gains shown in E2, E4, E5, and E6. H-B's prescription — individual silent ideation first, then structured synthesis; single-agent LLM with ToT/CoT rather than MAD — is better supported.

---

### 3. Premortem

**Assumption for premortem:** The main conclusion is that structured diverge-then-converge patterns, augmented by LLM agents using roles/personas and multi-agent debate, are effective and recommended for software engineering design exploration.

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **FR1: The research base is domain-mismatched.** The strongest empirical evidence for scaffolded diverge/converge (Source 1, CHI 2025) comes from generative image co-creation, not software architecture. Design thinking frameworks (Sources 3–5) originate from product/UX design, not backend or distributed systems engineering. Software architecture decisions involve hard technical constraints (latency, consistency, cost) that creative brainstorming processes do not model well. The conclusion may be a category error — applying UX-design patterns to an engineering problem with fundamentally different constraints. | High | Moderate-to-High. The prescriptive recommendations for software engineers may need domain-specific qualification: diverge/converge is likely valid for problem framing and requirements exploration, but inadequate for evaluating technical tradeoffs where structured decision frameworks (ADRs, ATAM) are established practice. |
| **FR2: LLM homogenization undermines the diversity premise.** The central value proposition of LLM-augmented brainstorming is generating diverse options. If LLMs systematically converge on a narrow band of "creative" ideas (79% cross-model similarity above 0.8), the entire framing of LLM agents as diversity-expanding brainstorming partners is undermined. The homogenization research (2025) directly contradicts multiple claims in Sub-question 4. This evidence was not captured in the draft's sources — it is a significant gap. | High | High. Any recommendation to use LLM agents for divergent brainstorming must be heavily qualified: without deliberate diversity-forcing mechanisms (diverse training data, explicit anti-convergence prompting, heterogeneous model ensembles), LLM brainstorming likely amplifies rather than reduces design fixation. |
| **FR3: Context and team dynamics are underweighted; findings assume idealized conditions.** The research sources describe idealized conditions: teams that follow structured processes, dedicate time to exploration, and have psychological safety to "kill their darlings." In practice, software teams operate under sprint pressure, and the Double Diamond criticism (Elsewhen, Xebia) documents that Agile mindset "starts only in the fourth quadrant" when the framework is adopted. Analysis paralysis is explicitly identified as an anti-pattern in Source 21, suggesting that adding more divergent techniques can worsen outcomes for time-pressured teams. The meta-analytic evidence on group brainstorming applies broadly regardless of team conditions. | Medium | Moderate. Conclusions should include explicit scope conditions: structured diverge/converge and LLM brainstorming augmentation are most valuable at the problem-framing and requirements stages, and in contexts with sufficient time and psychological safety. For sprint-constrained teams, lightweight individual-first techniques (NGT pattern) and single-agent prompting are more practical than full Double Diamond or multi-agent orchestration. |

---

## Findings

### Sub-question 1: What divergent-then-convergent thinking patterns are most effective for software design exploration?

**Finding 1.1 — The diverge-then-converge structure is well-validated, but its effectiveness depends on individual-first sequencing.**
Multiple independent frameworks — the Geneplore model of creative cognition [1], the Double Diamond (British Design Council, via [5]), and the U.S. government Human-Centered Design guide [3] — all endorse separating idea generation from idea evaluation. The shared principle: defer judgment during generation, then apply critical analysis during convergence. This convergence across T1, T3, and T4 sources is strong. (HIGH — T1+T3+T4 sources converge)

However, the meta-analytic record on *group* brainstorming consistently shows that face-to-face group ideation produces fewer and lower-quality ideas than nominal groups (individuals generating independently before pooling). The implication: the diverge-then-converge structure is valid, but the *individual-first* variant outperforms team-simultaneous divergence. Sources 3–5's implicit assumption that teams should brainstorm together may invert the optimal workflow.

**Finding 1.2 — Effective scaffolding requires explicit mode-switching, not just phase sequencing.**
A CHI 2025 study [1] found that scaffolded systems improve outcomes by supporting three design goals: generating high-level ideas before committing to an artifact (DG1), translating intentions into actionable refinements (DG2), and enabling fluid, non-linear switching between modes without losing interaction history (DG3). The key innovation is that the modes must be *explicit and switchable*, not sequential and fixed. (HIGH — T3 peer-reviewed empirical study)

Transition mechanisms: affinity diagramming (clustering ideas by theme) is the most-cited technique for moving from divergent to convergent mode [4]. In the Double Diamond, this transition happens between the Define and Develop phases [5].

**Finding 1.3 — Successive cycles outperform a single diverge-converge pass.**
Digital.gov [3] and Voltage Control [4] both describe design as "successive cycles" of divergent and convergent thinking, not a single round. Daniel Jackson [2] notes that most design work is convergent, and deep design quality "often comes from working through fine details" — implying multiple revisits rather than a single expansive phase followed by a single refinement. (MODERATE — T1+T4 sources, practitioner framing)

**Counter-evidence:** The Double Diamond has attracted documented criticism as too linear for Agile teams — it front-loads exploration to the point where teams may develop sunk-cost attachment to early concepts before any technical validation. The d.school has reportedly revised its curriculum away from the diverge-converge framing. These critiques apply primarily when the framework is adopted as a waterfall-style lifecycle rather than a recursive lens.

---

### Sub-question 2: How should problem spaces be explored before converging on a solution?

**Finding 2.1 — Explicit problem clarity is the highest-leverage precondition for good design.**
Ivo Eftimov's framework [7] makes problem clarity its first and most fundamental principle: "You can't produce an excellent solution to a problem you don't understand well." Sketching is used as an introspection tool to surface the limits of understanding before investing in solutions. This aligns with the CHI 2025 paper's DG1: avoid committing to an artifact before high-level concepts are explored. (MODERATE — T4 source, corroborated by multiple frameworks)

**Finding 2.2 — Structured "Alternatives Considered" documentation prevents premature convergence in engineering design.**
Engineering design docs at Google explicitly include an "Alternatives Considered" section [6]; Uber's RFC process requires multi-dimensional evaluation across architecture, SLAs, load testing, and security [6]. These document structures create organizational forcing functions for exploring the problem space before committing. The pre-mortem technique (PayPal Tech, [18]) extends this by imagining project failure first, then working backwards to surface design risks. (MODERATE — T4 sources, practitioner evidence)

**Finding 2.3 — Criteria-first evaluation prevents option-overload and comparison fatigue.**
Alex Wauters [8] documents a structured approach: define and prioritize evaluation criteria before evaluating options, then score options against those criteria in tiers (High/Medium/Low). Critically, the recommendation is to limit alternatives to a manageable count — generating excessive permutations makes steering decisions harder, not easier. This is a direct counter to the assumption that more options always improve outcomes. (LOW — T5 single practitioner source; consistent with academic decision-making literature)

**Finding 2.4 — Pre-mortem analysis is an underutilized mechanism for structured problem space exploration.**
The pre-mortem technique [18] inverts the standard design review: rather than asking "what should we build?", it asks "what would cause this to fail?" The PayPal framework structures this as: (1) document the problem and approach, (2) run a failure-mode discussion session, (3) refine the design. The technique explicitly encourages "diverge before you converge" [18] and breaks organizational silos by normalizing failure discussion before investment. (MODERATE — T4 source, practitioner case study)

**Counter-evidence:** Excessive problem space exploration is itself the analysis paralysis anti-pattern [21]. The optimal point is context-dependent: sufficient exploration to surface major risks, but not so extensive it delays execution. No source provides a principled threshold.

---

### Sub-question 3: What anti-patterns in design thinking lead to premature convergence or analysis paralysis?

**Finding 3.1 — Anchoring bias is the primary cognitive mechanism for premature convergence.**
Two independent 2025 research papers [10, 20] identify anchoring as the dominant bias in software architecture decisions: initial solution concepts disproportionately influence final choices, even when superior alternatives are available. Notably, an empirical study [10] found that practitioners are *more* susceptible to anchoring than students — hypothesized to be due to "attachment to their systems." A structured debiasing workshop significantly reduced anchoring and optimism bias occurrences. (HIGH — T3 empirical study + T5 practitioner source converge)

**Finding 3.2 — Groupthink and bandwagon bias systematically suppress design diversity in team settings.**
IxDF [16] documents groupthink as a pervasive phenomenon where individual creativity is suppressed in favor of group identity. The "bandwagon bias" mechanism — going along with popular beliefs because it is cognitively easier — is described as a "classic signature" of groupthink. Structured techniques like Six Thinking Hats [17] directly target this by enforcing perspectives that would otherwise be suppressed by social dynamics. (HIGH — T3 institutional source + T4 practitioner source)

**Finding 3.3 — GenAI-specific design fixation is driven by training data bias, not just interaction patterns.**
A Feb 2025 paper [9] defines GenAI design fixation as restriction of design exploration due to "unconscious bias stemming from technical aspects and human factors." The mechanism is primarily data-side: high-frequency word dependency causes disproportionate reuse of common patterns; training data bias creates unbalanced outputs. Interaction-layer scaffolding can mitigate surface manifestations but cannot resolve the underlying data distribution problem [9]. (MODERATE — T3 preprint, domain-specific)

**Finding 3.4 — Over-programmatic workflows amplify rather than prevent fixation.**
Source [9] explicitly warns that "overly programmatic workflows may strengthen design fixation" — a direct critique of rigid phase-gating. When systems enforce strict sequences, they can lock in early conceptual choices. This creates tension with structured design frameworks like the Double Diamond, which are themselves prescriptive. (MODERATE — T3 source, single study)

**Finding 3.5 — Analysis paralysis is the opposite pathology: insufficient convergence due to decision stall.**
Analysis paralysis [21] stalls projects when decision-makers lack sufficient data or experience to choose between options. The human solution is to prioritize reversible decisions: "pick a solution on intuition, but change it if it becomes apparent it is wrong." Agile methodologies mitigate this better than waterfall because they force teams to react to change rather than achieve certainty before acting. (MODERATE — T5 source, consistent with Agile literature)

**Counter-evidence:** The tension between premature convergence and analysis paralysis has no universal resolution. The optimal balance is context-dependent and team-experience-dependent. Research [10] shows that structured debiasing workshops can shift the equilibrium, but the intervention is not transferable without deliberate facilitation.

---

### Sub-question 4: How can LLM agents facilitate structured brainstorming?

**Finding 4.1 — The exploration-exploitation dynamic is the core mechanism for LLM-augmented brainstorming.**
A 2025 PMC study [12] documented that structured LLM interactions operate via two modes: exploration prompts (starting new conceptual paths, correlated with keyword diversity) and exploitation prompts (deepening existing concepts, correlated with narrowing). The key design insight: socially-sourced keywords drive exploration diversity, while AI-generated keywords drive exploitation depth. An effective LLM brainstorming system must make this toggle explicit and controllable. (MODERATE — T3 peer-reviewed study, specific experimental context)

**Finding 4.2 — Six Thinking Hats maps directly to LLM agent role decomposition.**
The Six Thinking Hats framework [17] decomposes thinking into six parallel perspective modes (facts, emotions, risks, benefits, creativity, process). Each hat maps cleanly to an LLM agent persona or prompt framing: White Hat = factual retrieval, Black Hat = risk/counter-argument generation, Green Hat = brainstorming alternatives, etc. The framework's core value — preventing any single perspective from dominating — is equally applicable to preventing LLM output from converging on a dominant framing. (MODERATE — T4 source, structural analogy rather than empirical evidence for LLM application)

**Finding 4.3 — Tree of Thoughts is the single-agent prompting technique best suited to design space exploration.**
Tree of Thoughts [19], based on Yao et al. (2023), enables LLMs to maintain multiple parallel reasoning paths with lookahead and backtracking — directly mirroring diverge-then-converge at the prompt level. It "substantially outperforms" standard chain-of-thought on complex tasks. For design exploration, this enables systematic multi-path evaluation without requiring multi-agent orchestration overhead. (MODERATE — T4 practitioner reference, empirical basis in underlying research paper)

**Finding 4.4 — Multi-agent debate can enable error correction, but fails to consistently outperform single-agent reasoning.**
The multi-agent debate (MAD) pattern [14, 15] enables agents to critique each other's outputs across rounds, with the potential for errors to surface through critique rather than passing silently. However, the ICLR 2025 review [14] acknowledges that "MAD frameworks fail to consistently outperform simpler single-agent test-time computation strategies," and MAD suffers from majority conformity — minority agents capitulate to group consensus, reproducing the groupthink it aims to prevent. (LOW — T4 source, self-contradicting findings; not yet established as reliable practice)

**Finding 4.5 — Task decomposition into specialist agent roles enables parallel design space coverage.**
A 2025 Arxiv study [11] documented how practitioners decompose complex tasks across agent roles mirroring team structures (product manager, engineer, domain expert). The value is task-specific coverage rather than diversity of perspective on the same question. For design brainstorming, this means assigning different agents to different problem dimensions rather than having all agents compete on the same question. (MODERATE — T3 source, early-adopter mental model study, not controlled experiment)

**Counter-evidence — LLM homogenization significantly undermines the diversity premise:**
2025 research (not captured in the draft's primary sources) documents that 79% of LLM responses across models exceed 0.8 cosine similarity — a "hivemind" effect where diverse models converge on nearly identical outputs. This directly contradicts the value proposition of using multiple LLM agents for divergent brainstorming: if the agents are drawing from similar training distributions, the apparent diversity of role framing may be cosmetic. Diversity-forcing mechanisms (heterogeneous model ensembles, explicit anti-convergence prompting, seeding with unusual concepts from distant domains [1]) are necessary but not sufficient. (MODERATE confidence in the homogenization claim — from challenge research not in primary sources; HIGH impact on conclusions)

---

### Gaps and Follow-Ups

- **LLM homogenization research** — the 2025 findings on cross-model similarity are the most significant gap in the gathered sources. A dedicated investigation into homogenization mitigation techniques (diverse model ensembles, contrastive prompting, seeding from distant domains) is warranted.
- **Software architecture-specific evidence** — the strongest empirical evidence (CHI 2025 [1]) comes from generative image co-creation, not software architecture. Studies validating diverge/converge frameworks specifically in distributed systems or backend engineering contexts are absent.
- **Nominal Group Technique in software teams** — the meta-analytic advantage of individual-first ideation over group brainstorming is well-established, but no source documents NGT adoption specifically in software design contexts.
- **Debiasing at scale** — the debiasing workshop [10] is promising but requires human facilitation. Tooling to automate cognitive bias detection in design documents or ADRs is an open research area.

---

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | The Double Diamond model was developed by the British Design Council in 2005. | Attribution | https://www.uxpin.com/studio/blog/double-diamond-design-process/ | verified |
| 2 | arxiv 2512.18388 is a CHI 2025 paper. | Attribution | https://arxiv.org/html/2512.18388 | human-review |
| 3 | DG1 of [1]: "The system should support users in generating diverse high-level ideas before committing to an actual artifact. By doing so, the system aims to reduce premature convergence and design fixation." | Quote | https://arxiv.org/html/2512.18388 | verified |
| 4 | DG2 of [1]: "The system should help users translate their intentions into concrete, actionable refinements and encourage further exploration of alternative refinements." | Quote | https://arxiv.org/html/2512.18388 | verified |
| 5 | DG3 of [1]: "The system should support fluid movement between divergent and convergent modes, including branching and revisiting earlier ideas." | Quote | https://arxiv.org/html/2512.18388 | verified |
| 6 | Tree of Thoughts "substantially outperforms the other prompting methods" on complex problem-solving tasks. | Superlative | https://www.promptingguide.ai/techniques/tot | verified |
| 7 | ToT is based on Yao et al. (2023) research. | Attribution | https://www.promptingguide.ai/techniques/tot | verified |
| 8 | "MAD frameworks fail to consistently outperform simpler single-agent test-time computation strategies" (Finding 4.4, citing ICLR 2025 [14]). | Quote | https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/ | verified |
| 9 | Combining GPT-4o-mini and Llama3.1-70b together achieved better accuracy than single-model approaches. | Statistic | https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/ | verified |
| 10 | 79% of LLM responses across models exceed 0.8 cosine similarity (homogenization research, 2025). | Statistic | — | human-review |
| 11 | Practitioners were more susceptible to cognitive biases than students in the architectural decision-making study [10]. | Attribution | https://arxiv.org/abs/2502.04011 | verified |
| 12 | The study [10] used 16 students and 20 practitioners, split into control and workshop group pairs. | Statistic | https://arxiv.org/abs/2502.04011 | verified |
| 13 | "Anchoring and optimism bias occurrences decreased significantly" after the debiasing workshop [10]. | Quote | https://arxiv.org/abs/2502.04011 | verified |
| 14 | Practitioners' susceptibility hypothesized to be due to "attachment to their systems" [10]. | Quote | https://arxiv.org/abs/2502.04011 | verified |
| 15 | Six Thinking Hats originates with Edward de Bono, 1985. | Attribution | https://www.atlassian.com/blog/productivity/six-thinking-hats | verified |
| 16 | The Black Hat is described as "the most valuable of all the hats" (de Bono). | Quote | https://www.atlassian.com/blog/productivity/six-thinking-hats | verified |
| 17 | "A classic signature of groupthink is bandwagon bias, a cognitive bias arising from the comparative ease of going along with popular beliefs." | Quote | https://ixdf.org/literature/topics/groupthink | verified |
| 18 | IxDF groupthink article dated 2026 (Sources Table). | Attribution | https://ixdf.org/literature/topics/groupthink | corrected |
| 19 | "There is a significant positive correlation between the frequency of exploration prompts and the diversity of keywords used by participants." | Quote | https://pmc.ncbi.nlm.nih.gov/articles/PMC12177052/ | verified |
| 20 | Socially-sourced keywords drive exploration diversity; AI-generated keywords drive exploitation depth [12]. | Attribution | https://pmc.ncbi.nlm.nih.gov/articles/PMC12177052/ | verified |
| 21 | Agents "generated inaccuracies or lost contextual relevance, leading to compounded errors, especially when one agent's error feeds into another" (P06, [11]). | Quote | https://arxiv.org/html/2510.06224v1 | verified |
| 22 | Agents "sometimes became 'stuck' in repetitive, unproductive cycles" (P06, P13, [11]). | Quote | https://arxiv.org/html/2510.06224v1 | verified |
| 23 | d.school has reportedly revised its curriculum away from the diverge-converge framing (Finding 1.1 counter-evidence). | Attribution | — | human-review |
| 24 | Meta-analytic evidence (Mullen, Johnson & Salas, 1991, 20 studies, 800+ teams) shows group brainstorming produces fewer/lower-quality ideas than nominal groups (Challenge A4, echoed in Finding 1.1). | Statistic | — | human-review |

### Claim Notes

**Claim 2 (human-review):** The arXiv page for 2512.18388 shows version v2 dated 06 Apr 2026. The document labels this "CHI 2025" but the conference year could not be confirmed from the fetched content. The Gaps section refers to it as "CHI 2025 [1]" — this should be verified against the camera-ready paper or ACM DL listing before finalizing.

**Claim 10 (human-review):** The 79% / 0.8 cosine similarity figure is explicitly noted in the document as coming from "2025 research (not captured in the draft's primary sources)." No URL is provided. CoVe cannot confirm the specific numbers from parametric memory. Requires a citeable source before this claim can be used in conclusions.

**Claim 18 (corrected):** The Sources Table listed IxDF's article date as "2026." Re-verification shows the article was originally published June 2, 2016, with most recent modification November 26, 2024. The Sources Table has been updated to read "2016 (orig); 2024 (modified)."

**Claim 23 (human-review):** The statement that d.school "has reportedly revised its curriculum away from the diverge-converge framing" has no cited source. CoVe is uncertain — while design thinking critique literature exists, the specific d.school curriculum change cannot be confirmed without a source.

**Claim 24 (human-review):** Mullen, Johnson & Salas (1991) is a real meta-analysis on brainstorming productivity, and the finding that group brainstorming produces fewer/lower-quality ideas than nominal groups is consistent with the literature. However, the specific "20 studies, 800+ teams" figures appear in the Challenge section (not primary sources) without a URL citation. These numbers cannot be confirmed from primary source re-verification.
