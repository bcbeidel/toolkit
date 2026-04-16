---
name: "Statistical Modeling & Inference: Best Practices and Tooling"
description: "GLMMs for clustered data (use GEE for population-average questions); TWFE is biased under staggered DiD (use Callaway & Sant'Anna); Bayesian A/B testing's advantage is interpretability not sample efficiency; Stan/PyMC+ArviZ are best-in-class for Bayesian computation"
type: research
sources:
  - https://www.tandfonline.com/doi/full/10.1080/01621459.2025.2506201
  - https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html
  - https://m-clark.github.io/book-of-models/generalized_linear_models.html
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8651375/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC5969114/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC10171296/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC3866838/
  - https://arxiv.org/html/2508.02310v1
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8275441/
  - https://github.com/py-why/dowhy
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11875439/
  - https://www.pymc-labs.com/blog-posts/probabilistic-forecasting
  - https://www.dynamicyield.com/lesson/running-effective-bayesian-ab-tests/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC8526359/
  - https://research.google/pubs/bayesian-hierarchical-media-mix-model-incorporating-reach-and-frequency-data/
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC7425741/
  - https://building.nubank.com/3-lessons-from-implementing-controlled-experiment-using-pre-experiment-data-cuped-at-nubank/
  - https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
  - https://mc-stan.org/
  - https://python.arviz.org/
  - https://www.pymc-labs.com/blog-posts/pymc-stan-benchmark
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11984709/
  - https://www.tmwr.org/
related:
---

# Statistical Modeling & Inference: Best Practices and Tooling

## Summary

Key findings across five sub-questions, annotated with confidence.

**Applied Statistical Modeling**
- Use distribution-appropriate GLMs (binomial/logit, Poisson/neg-binomial); compute average marginal effects for interpretable slopes. (HIGH)
- GLMMs required for clustered/longitudinal data; GEE or cluster-robust OLS preferred when the target is population-average effects. (MODERATE — GEE is underused; GLMM misspecification risk is real)
- Variable selection demands EPV discipline: EPV > 25 (selection acceptable), 10–25 (add shrinkage), ≤ 10 (global model + shrinkage only). Backward elimination preferred; avoid univariable prescreening. (HIGH)
- Cox regression is standard for time-to-event; verify proportional hazards; ~1 covariate per 22 events. (HIGH)

**Causal Inference**
- TWFE DiD is biased under staggered treatment adoption; use Callaway & Sant'Anna (2021) or equivalent modern methods. (HIGH)
- DAGs are necessary for confounding identification but not sufficient: only ~20% of studies applying DAGs report the implied adjustment set. (MODERATE)
- IV: F-statistic threshold is contextually >20 for single instruments; the Montiel Olea & Pflueger effective F is the correct modern statistic — not a blanket rule. (MODERATE)
- DoWhy (Python/PyWhy) is the best-in-class tool for applied causal inference with refutation API. (HIGH)

**Bayesian Methods for Business**
- Bayesian A/B testing's defensible advantage is interpretability (P2BB), not a 75% sample-size reduction — that figure is unsubstantiated vendor marketing. (HIGH — ACH challenge confirms)
- Probabilistic forecasting with hierarchical Bayesian models handles censored data and hierarchical structures better than point-forecast methods. (HIGH)
- Reporting standards are rarely met: only 24% of Bayesian analyses fully report the prior; 87.9% skip sensitivity analysis. (HIGH)

**Experimental Design**
- CUPED reduces variance: ~40% of metrics achieve >20% reduction; use 42-day lookback; apply Delta Method for ratio metrics. (MODERATE)
- Sequential testing (GST preferred over mSPRT for efficiency) addresses the peeking problem while maintaining error rates. (MODERATE)
- Power requires four inputs: SD, α (typically 0.05), desired power (≥80%), and MDE (a business decision, not statistical). (HIGH)

**Statistical Computing**
- Stan and PyMC+ArviZ are current best-in-class for full Bayesian inference. Stan: gold-standard sampler (NUTS), multi-language. PyMC: Python-native, JAX backend. ArviZ: standard diagnostics (R-hat, ESS).
- JAX on GPU: ~11x more ESS/second vs. standard PyMC/Stan above ~50k observations — model-class-specific, not a general multiplier. (MODERATE)
- Python for production/ML (76% job postings), R for statistical depth and biostatistics, Julia for compute-intensive modeling.

**Search protocol:** 29 searches, 23 sources used (21 verified reachable; 2 via 403 access-restricted; 2 search-summary claims unverifiable).

---

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://www.tandfonline.com/doi/full/10.1080/01621459.2025.2506201 | Generalized Linear Mixed Models: Modern Concepts, Methods and Applications, 2nd ed. (review) | JASA / Stroup, Ptukhina, Garai | 2025 | T3 | verified (403 — extracts from search summary) |
| 2 | https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html | GLMM FAQ | Ben Bolker (lme4 author) | ongoing | T4 | verified |
| 3 | https://m-clark.github.io/book-of-models/generalized_linear_models.html | Models Demystified: Generalized Linear Models | Michael Clark | 2024 | T4 | verified |
| 4 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8651375/ | Methods to Analyze Time-to-Event Data: The Cox Regression Analysis | PMC / NIH | 2021 | T3 | verified |
| 5 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5969114/ | Variable selection – A review and recommendations for the practicing statistician | PMC / NIH | 2018 | T3 | verified (2018 — EPV guidance still current) |
| 6 | https://pmc.ncbi.nlm.nih.gov/articles/PMC10171296/ | Mixed-effects model: a useful statistical tool for longitudinal and cluster studies | PMC / NIH | 2023 | T3 | verified |
| 7 | https://pmc.ncbi.nlm.nih.gov/articles/PMC3866838/ | An assessment of estimation methods for generalized linear mixed models with binary outcomes | PMC / NIH | 2014 | T3 | verified (2014 — dated; newer estimation methods exist) |
| 8 | https://arxiv.org/html/2508.02310v1 | Estimating Causal Effects with Observational Data: Guidelines for Agricultural and Applied Economists | arXiv (academic preprint) | 2025 | T3 | verified (preprint, not yet peer-reviewed) |
| 9 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8275441/ | Using Propensity Scores for Causal Inference: Pitfalls and Tips | PMC / NIH | 2021 | T3 | verified |
| 10 | https://github.com/py-why/dowhy | DoWhy: Python library for causal inference | PyWhy / Microsoft | 2024 | T1 | verified |
| 11 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11875439/ | How to develop causal directed acyclic graphs for observational health research | PMC / NIH | 2024 | T3 | verified |
| 12 | https://www.pymc-labs.com/blog-posts/probabilistic-forecasting | Probabilistic Time Series Forecasting | PyMC Labs (core maintainers) | 2024 | T4 | verified |
| 13 | https://www.dynamicyield.com/lesson/running-effective-bayesian-ab-tests/ | Guidelines for running effective Bayesian A/B tests | Dynamic Yield / Mastercard | 2024 | T4 | verified (COI: vendor promoting own testing product) |
| 14 | https://pmc.ncbi.nlm.nih.gov/articles/PMC8526359/ | Bayesian Analysis Reporting Guidelines | PMC / NIH | 2021 | T3 | verified |
| 15 | https://research.google/pubs/bayesian-hierarchical-media-mix-model-incorporating-reach-and-frequency-data/ | Bayesian Hierarchical Media Mix Model Incorporating Reach and Frequency Data | Google Research | 2023 | T2 | verified (mild COI: Google promoting own methodology) |
| 16 | https://pmc.ncbi.nlm.nih.gov/articles/PMC7425741/ | Statistical Design of Experiments and Sample Size Selection Using Power Analysis | PMC / NIH | 2020 | T3 | verified |
| 17 | https://building.nubank.com/3-lessons-from-implementing-controlled-experiment-using-pre-experiment-data-cuped-at-nubank/ | 3 Lessons from Implementing CUPED at Nubank | Nubank Engineering | 2023 | T4 | verified |
| 18 | https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions | Choosing a Sequential Testing Framework | Spotify Engineering | 2023 | T4 | verified |
| 19 | https://mc-stan.org/ | Stan: Probabilistic Programming | Stan Development Team | 2024 | T1 | verified |
| 20 | https://python.arviz.org/ | ArviZ: Exploratory analysis of Bayesian models | ArviZ developers | 2024 | T1 | verified |
| 21 | https://www.pymc-labs.com/blog-posts/pymc-stan-benchmark | PyMC vs Stan MCMC Benchmark | PyMC Labs / Martin Ingram | 2023 | T4 | verified (COI: PyMC Labs is PyMC-focused org) |
| 22 | https://pmc.ncbi.nlm.nih.gov/articles/PMC11984709/ | Ten quick tips to get started with Bayesian statistics | PMC / NIH | 2024 | T3 | verified |
| 23 | https://www.tmwr.org/ | Tidy Modeling with R | Max Kuhn, Julia Silge (tidymodels creators) | 2022 | T4 | verified (2022 — content stable; 2025 updates confirmed) |

## Extracts

### Sub-question 1: Applied Statistical Modeling (Regression, GLMs, Mixed Models, Survival Analysis)

#### Source 1: Generalized Linear Mixed Models: Modern Concepts, Methods and Applications, 2nd ed. (Review)
- **URL:** https://www.tandfonline.com/doi/full/10.1080/01621459.2025.2506201
- **Author/Org:** Walter W. Stroup, Marina Ptukhina, and Julie Garai (reviewed in JASA) | **Date:** 2025

**Re: Applied Statistical Modeling best practices**
> "Model fit statistics such as the AIC, AICC, and BIC can be used to compare models." (Search result summary)

> "For binomial and Poisson GLMMs, pseudo-likelihood with the Kenward–Roger adjustment yields better Type I error control than Laplace while preserving the GLMM's advantage with respect to power and accuracy in estimating treatment means." (Search result summary)

> "Applications including ANOVA-type and regression-type models, multi-level models for nested or hierarchical data, Poisson and negative binomial GLMs for count response variables, GLMMs with multiple link functions for binary and binomial response variables, zero-inflated and hurdle models for count data with excessive zeroes, and GLMMs for ordinal and nominal response variables." (Search result summary)

> "Generalized linear mixed models often suffer from misspecification and convergence problems, and the researcher's choice of random and fixed effects directly affects statistical inference correctness." (Search result summary, 2024–2025 methodological note)

> "The heteroscedastic nature of data can introduce bias and compromise the validity of statistical inferences...accounting for within-subject dependence is likewise essential for valid statistical inference." (Search result summary)

---

#### Source 2: Models Demystified: Generalized Linear Models
- **URL:** https://m-clark.github.io/book-of-models/generalized_linear_models.html
- **Author/Org:** Michael Clark | **Date:** 2024

**Re: GLM best practices, distribution selection, inference**
> "Different probability distributions, taking us beyond the normal distribution...allow us to use the same linear model framework...with different types of targets." (Chapter intro)

> "For binary targets, remember that 'the conditional distribution of the target variable given the features' follows a binomial distribution, not the target itself. Use inverse-logit transformations to convert predictions to probability space. Recognize that 'probability differences are not the same as odds differences,' requiring careful communication of results." (Logistic regression section)

> "For count data, employ log-link functions to maintain non-negative predictions. Understand that 'the variance is equal to the mean for the Poisson distribution,' which rarely holds in practice—consider negative binomial alternatives when overdispersion appears evident." (Poisson section)

> "Calculate average marginal effects to understand slope magnitudes on practical scales." (Best practices section)

> "Pseudo-R² values for logistic models differ fundamentally from linear regression R² and shouldn't receive identical interpretation." (Cautionary notes section)

---

#### Source 3: Variable selection – A review and recommendations for the practicing statistician
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC5969114/
- **Author/Org:** PMC / NIH | **Date:** 2018

**Re: Variable selection in regression models**
> "Modeling should start with defendable assumptions on the roles of IVs that can be based on background knowledge." (Core recommendations)

> Events-per-variable thresholds: "EPV > 25: Variable selection acceptable with stability investigations; 10 < EPV ≤ 25: Combine selection with shrinkage methods or LASSO; EPV ≤ 10: Avoid selection; use global model with shrinkage instead." (EPV guidance section)

> "Backward elimination (BE) preferred over forward selection. Use AIC (α ≈ 0.157) as default stopping criterion for smaller samples. Reserve BIC and stricter thresholds (α ≤ 0.05) for large datasets only." (Preferred selection methods)

> "Univariable variable selection...should be generally avoided. Variables significant in isolated analyses may behave differently when adjusted for other predictors due to correlation structures." (Critical caution)

> "Variable selection introduces additional uncertainty requiring bootstrap resampling to assess: bootstrap inclusion frequencies for each variable, root mean squared difference (RMSD) ratios, conditional bias estimates, and model selection frequencies." (Stability investigations)

---

#### Source 4: Methods to Analyze Time-to-Event Data: The Cox Regression Analysis
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8651375/
- **Author/Org:** PMC / NIH | **Date:** 2021

**Re: Cox regression and survival analysis best practices**
> "Cox regression analyzes time-to-event data by estimating hazard ratios for risk factors. It's described as 'a semiparametric method because there is no assumption about the distribution of survival times, but it assumes that the effects of different variables on survival are constant over time.'" (Core definition)

> "A preliminary step involves assessing whether 'the hazard ratio (HR) associated with the risk factor must be constant over time.' Violation occurs when survival curves between groups cross." (PH assumption)

> "The model requires 'approximately one covariate into the model for every 22 patients who died,' ensuring adequate statistical power." (Sample size guidance)

> "Cox regression provides effect estimates and confidence intervals, accommodates continuous variables without categorization, and permits confounder adjustment." (Advantages over KM)

---

#### Source 5: Mixed-effects model: a useful statistical tool for longitudinal and cluster studies
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10171296/
- **Author/Org:** PMC / NIH | **Date:** 2023

**Re: Mixed-effects models, when to use them and how**
> "Examples of studies that require mixed-effects models are time series, longitudinal studies with multiple measurements taken over time on the same subject, and studies that involve participants from different sites or that are evaluated by different physicians (clustered measurements)." (When to use section)

> "Choosing the appropriate statistical model to answer specific research questions considering the data set structure improves the models' fit and enables proper interpretation for clinical decision-making." (Core principle)

> "Fixed effects should include: baseline characteristics that don't vary (age at baseline, sex, race/ethnicity), exposures and interventions whose relationship with outcomes is constant, variables where separate effects for each level are of primary interest." (Model specification)

> "Random effects should account for: participant-level variation across repeated measures, clustering effects (e.g., hospital or site effects), sources of correlation that traditional regression cannot address." (Random effects)

---

#### Source 6: Regression Diagnostics best practices (2024)
- **URL:** https://www.tandfonline.com/doi/full/10.1080/10618600.2024.2344612
- **Author/Org:** Taylor & Francis / Journal of Computational and Graphical Statistics | **Date:** 2024
- **Note:** URL returned 403 (access restricted)

**Re: Residual diagnostics and assumption checking**
> "Some diagnostic tests are statistical and others are visual; statistical tests are more objective while visual tests are more informative and provide information about the nature and magnitude of assumption violations." (Search result summary)

> "Regression experts consistently recommend plotting residuals for model diagnosis, and evidence shows that conventional tests are too sensitive, too often concluding that model fit is inadequate." (Search result summary)

> "The four primary diagnostic plots are: Residuals vs Fitted (used to check the linear relationship assumptions), Normal Q-Q (used to examine whether residuals are normally distributed), Scale-Location (used to check homogeneity of variance), and Residuals vs Leverage (used to identify influential cases)." (Search result summary)

---

### Sub-question 2: Causal Inference in Observational Data

#### Source 7: Estimating Causal Effects with Observational Data: Guidelines for Agricultural and Applied Economists
- **URL:** https://arxiv.org/html/2508.02310v1
- **Author/Org:** arXiv | **Date:** 2025

**Re: Causal inference with observational data — methods and best practices**
> "Clearly state the assumptions that the chosen method and model specification require for obtaining unbiased and/or consistent estimates." (Cross-cutting best practices)

> "Use Directed Acyclic Graphs (DAGs) to identify appropriate control variables and avoid 'bad controls'. Separately address three endogeneity sources: omitted variables, measurement error, and reverse causality." (Selection on observables)

> "Most machine learning methods are unsuitable when used directly to estimate causal effects despite their predictive power." (OLS & Matching warning)

> "McKenzie et al. (2010) found OLS estimates overstate effects by 20-82% versus experimental benchmarks." (Selection on observables)

**Re: Instrumental Variables**
> "Modern guidance recommends F-statistics exceeding 20 (previously 10 was standard). For single instruments, F-statistic should 'exceed 50'. Below F=20, OLS estimates often closer to true effects than 2SLS." (Strength assessment)

> "2SLS estimates indicate Local Average Treatment Effects (LATE) under monotonicity, not necessarily overall Average Treatment Effects. LATE applies only to 'compliers' with the instrument; effects on always-takers and never-takers remain unidentified." (Interpretation caveats)

> "Invalid instruments can produce worse bias than OLS; weak instruments reduce statistical power substantially." (Implementation warning)

**Re: Difference-in-Differences**
> "The parallel trends assumption—treated units would follow control unit trajectories absent treatment...is purely hypothetical by definition since it is impossible to be certain of counterfactual trends." (Fundamental assumption)

> "Standard Two-Way Fixed Effects (TWFE) estimators can produce biased results under staggered treatment adoption. Modern methods (Callaway & Sant'Anna 2021; Borusyak et al. 2024; Sun & Abraham 2021) address 'negative weights problem'." (Recent advances)

> "Visualize pre-treatment trends; however, parallel pre-trends 'are neither necessary nor sufficient' for unbiased estimates. Diagnostic tests for parallel trends often lack statistical power." (Practical guidance)

> "Use Bacon Decomposition to understand TWFE as weighted average of 2×2 comparisons. Consider Synthetic Difference-in-Differences combining DID with synthetic control elements." (Tools)

**Re: Synthetic Control Method**
> "Most suitable for evaluating interventions affecting single or small number of large units (regions, countries). Factor Model Assumption requires time-invariant unobserved differences; effects of observed and unobserved characteristics identical across units." (Application context)

> "Ensure sufficiently long pre-treatment period to reduce bias. Restrict comparison units to those similar to treated unit (avoid overfitting). Conduct permutation-based inference for significance testing." (Key recommendations)

> "SCM can be applied when parallel trends assumption fails, provided adequate historical data exist." (Advantage over DiD)

**Re: Common pitfalls**
> "Regressing outcomes on multiple explanatory variables with causal interpretation of each coefficient is 'usually inappropriate'." (Common pitfalls)

> "Machine learning variable selection (Lasso) introduces omitted-variable bias by dropping correlated controls." (Common pitfalls)

> "The 'credibility revolution' calls for rigorous identification strategies explicitly described and empirically justified, moving beyond 'mere application of an econometric approach' to establish causality." (Publication standards)

---

#### Source 8: Using Propensity Scores for Causal Inference: Pitfalls and Tips
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8275441/
- **Author/Org:** PMC / NIH | **Date:** 2021

**Re: Propensity score methods for causal inference**
> "A propensity model include only variables that affect an outcome. Variables should be selected based on subject-matter knowledge about causal structures rather than statistical associations alone." (Variable selection)

> "Rather than reporting model fit statistics, researchers should 'check covariate balance' after PS estimation using standardized differences, with values below 0.1 generally supporting adequate balance." (Balance assessment)

> "The goal is NOT to predict exposure perfectly. 'Adding exposure predictors that are not confounders...increases the c-statistic but does not necessarily enhance causal inference.'" (Prediction vs. confounding)

> "Post-matching analysis needs to take account of the within-matched pair correlations using appropriate tests, and IPW estimates require 'robust variance or non-parametric bootstrapping.'" (Correlation adjustment)

> "PSM and IPW 'estimate effects in different target populations and, thus, answer different research questions.'" (Method selection)

> "IPW can address both confounding and selection bias through inverse probability of censoring weights." (Critical tip)

---

#### Source 9: DoWhy Python Library for Causal Inference
- **URL:** https://github.com/py-why/dowhy
- **Author/Org:** PyWhy / Microsoft | **Date:** 2024

**Re: Causal inference tooling and methodology**
> "DoWhy is a Python library that guides users through causal reasoning steps and provides a unified interface for answering causal questions. It combines two powerful frameworks: graphical causal models and potential outcomes approaches." (Key description)

> Four-step methodology: "(1) Model: Create a causal model from data and a specified causal graph; (2) Identify: Identify causal effects and return target estimands using graph-based criteria; (3) Estimate: Estimate the target estimand using statistical methods; (4) Refute: Test causal assumptions through robustness checks and falsification." (Core methodology)

> "A defining characteristic is its 'refutation and falsification API that can test causal assumptions for any estimation method,' making causal inference more robust and accessible to practitioners without deep expertise." (Distinguishing feature)

---

#### Source 10: How to develop causal directed acyclic graphs for observational health research
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11875439/
- **Author/Org:** PMC / NIH | **Date:** 2024

**Re: DAG methodology for observational studies**
> Six-step framework: "(1) construct a DAG as early as possible, preferably before the design of a study; (2) Define Exposure and Outcome; (3) Add Common Causes; (4) Consider Selection Procedures; (5) Consider Measurement Error; (6) Inform Data Analysis." (Six-step framework)

> "'Absent arrows represent stronger assumptions than included arrows,' suggesting researchers should justify omitted rather than included relationships." (Methodological note)

> "Organizing nodes to reflect time passage ('left-to-right or top-to-bottom') facilitates correct edge direction and reduces errors." (Temporal arrangement)

> "DAGs should include unmeasured variables when applicable, as they affect causal pathway identification regardless of data availability." (Unmeasured confounding)

---

#### Additional findings: DID and Causal Inference developments (2024-2025)
**Source:** Search results summary

> "Researchers have combined difference-in-differences (DID) and instrumental variables (IV) into instrumented DID (iDID), which is more robust to violations of the DID's parallel trend assumption due to an unmeasured confounder and the IV's exclusion restriction." (Instrumented DiD)

> "The synthetic difference-in-differences (SDID) estimator combines strengths from both DID and synthetic control methods, and seeks to optimally generate a matched control unit that considerably loosens the need for parallel-trends assumptions." (SDID)

> "Due to a lack of randomisation, an association between the independent variable (the exposure) and dependent variable (the outcome) might be the result of a common cause of both variables (i.e., confounding bias). Failure to adjust for a relevant confounding variable would lead to underadjustment. On the other hand, variables that are mediators (on the causal pathway from exposure to outcome) or colliders (causally affected by both the exposure and the outcome) should not be adjusted for; doing so is referred to as overadjustment." (Confounding bias)

### Sub-question 3: Bayesian Methods for Business

#### Source 11: Probabilistic Time Series Forecasting (PyMC Labs)
- **URL:** https://www.pymc-labs.com/blog-posts/probabilistic-forecasting
- **Author/Org:** PyMC Labs | **Date:** 2024

**Re: Bayesian demand forecasting and probabilistic methods**
> "Probabilistic forecasting addresses these limitations by generating complete probability distributions over possible future outcomes rather than single-point predictions." (Core concept)

> "Retail demand forecasting often involves censored data where true demand is masked by stockouts or capacity limits. Censored likelihood models 'accurately model the underlying demand distribution even during periods with stockouts or capacity constraints, effectively reconstructing what the true demand would have been.'" (Censored likelihoods)

> "When data has hierarchical structures (regions, categories), Bayesian models improve forecasts through information sharing. The tourism example demonstrates that hierarchical exponential smoothing captures shared trends better than independent univariate models, particularly for smaller datasets." (Hierarchical models)

> "Custom likelihoods allow incorporation of external expertise. The electricity demand example uses Gaussian processes to model temperature effects while constraining predictions for extreme temperatures." (Domain knowledge calibration)

> "PyMC-Extras offers decomposable components (trends, seasonality, regression) providing interpretability alongside uncertainty quantification through Kalman filtering." (State space models)

> "These approaches excel where traditional methods falter: sparse data, complex relationships, and business constraints. Probabilistic forecasting enables 'robust planning that accounts for risk and uncertainty.'" (Business value)

---

#### Source 12: Guidelines for Running Effective Bayesian A/B Tests (Dynamic Yield / Mastercard)
- **URL:** https://www.dynamicyield.com/lesson/running-effective-bayesian-ab-tests/
- **Author/Org:** Dynamic Yield / Mastercard | **Date:** 2024

**Re: Bayesian A/B testing for business decisions**
> "'Make sure that you randomly allocate who gets which of the options that you want to compare.' This prevents confounding variables from biasing results." (Randomization)

> "Whatever you put in to get the Bayesian engine going is essentially gonna be washed out by that information." (Prior distribution with large data)

> "Run experiments through complete time cycles to capture natural variations. Weekly trends require two-week minimums; daily patterns need appropriate windows. Avoid stopping early based on partial cycles." (Test duration)

> "The P2BB fluctuates during testing. Set extremely strict thresholds (0.999 or 0.001) before stopping early to avoid false signals." (Early stopping caution)

> "This metric [Probability to Be Best] summarizes evidence that variant A outperforms B. It provides intuitive business guidance by expressing uncertainty as probability distributions rather than binary conclusions." (Decision-making framework)

---

#### Source 13: Bayesian Analysis Reporting Guidelines
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC8526359/
- **Author/Org:** PMC / NIH | **Date:** 2021

**Re: Best practices for Bayesian analysis reporting and transparency**
> "Only 24% of 17 articles fully reported the prior, only 18% reported a sensitivity analysis." (Critical transparency gap)

> "56.6% did not report checking for chain convergence, and 87.9% did not conduct a sensitivity analysis." (Reporting gaps)

> Six-step reporting framework: "(1) Explain why Bayesian methods were chosen; (2) Document likelihood function, all parameters, prior distributions; (3) Report MCMC convergence statistics (PSRF) and effective sample size (ESS); (4) Include posterior predictive checks; (5) Demonstrate how results change across different prior specifications; (6) Post annotated code and data in stable repositories." (Core reporting steps)

> "Analysts should report parameter estimates even when making binary decisions about null values, preventing oversimplified interpretation." (Essential distinctions)

---

#### Source 14: Bayesian Hierarchical Media Mix Model (Google Research)
- **URL:** https://research.google/pubs/bayesian-hierarchical-media-mix-model-incorporating-reach-and-frequency-data/
- **Author/Org:** Google Research | **Date:** 2023

**Re: Bayesian hierarchical modeling for marketing measurement**
> "The impact of an advertisement on an individual can change based on the number of times they are exposed." (Core problem addressed)

> "By incorporating R&F data, the methodology delivers: (1) more accurate estimates of the impact of marketing on business outcomes; (2) helps marketers 'optimize their campaign execution based on optimal frequency recommendations'." (Benefits)

---

#### Additional findings: Bayesian methods for business (search summaries)

**Re: Hierarchical models for business**
> "Bayesian hierarchical models are being applied in retail to predict customer purchase amounts across multiple stores, accounting for unique patterns at each location rather than treating all customers uniformly." (Search result summary)

> "When data is naturally grouped, Bayesian hierarchical models allow patterns in the overall population to inform group-level estimates, addressing limitations of traditional models that struggle with non-independent data or natural clustering." (Search result summary)

> "Practitioners should understand the nested data structure, identify natural groups or hierarchies, and define clear objectives about whether the goal is prediction, inference, or both, which affects the choice of likelihood and prior distributions." (Search result summary)

**Re: Bayesian A/B testing advantages**
> "Bayesian A/B testing can reduce required sample size by 75% compared to frequentist approaches. The Bayesian approach enables you to make faster decisions with lower experimentation costs compared to a Frequentist approach by incorporating belief as part of the experiment." (Search result summary)

> "Bayesian inference has gained popularity in A/B testing due to its easy interpretability, with 'probability to be best' (with corresponding credible intervals) providing a natural metric to make business decisions." (Search result summary)

**Re: Prior and posterior predictive checks**
> "The prior represents an explicit declaration of the investigators' knowledge, assumptions, and the general state of a field, and analysts are encouraged to perform prior predictive checks to compare the sensitivity of competing priors in a Bayesian inference model." (Search result summary)

> "Prior predictive checks evaluate the prior by examining what data sets would be consistent with it, and extreme values help diagnose priors that are either too strong, too weak, poorly shaped, or poorly located." (Search result summary)

### Sub-question 4: Experimental Design for Maximum Power with Minimum Sample

#### Source 15: Statistical Design of Experiments and Sample Size Selection Using Power Analysis
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC7425741/
- **Author/Org:** PMC / NIH | **Date:** 2020

**Re: Experimental design principles and power analysis**
> Five fundamental design principles: "(1) Replication: 'Natural variability is present everywhere; results from repeated trials on the same subject vary' and replicating experiments increases reliability; (2) Randomization: 'Allocation of treatments randomly to experimental subjects ensures the validity of an inference in the presence of unspecified disturbances'; (3) Blocking/Grouping: Organizing subjects into homogeneous blocks removes large between-group effects, 'resulting in an increase of the precision'; (4) Multifactorial Design: Testing multiple factors simultaneously allows researchers to 'learn about interaction effects' rather than changing one factor at a time; (5) Sequential Approach: 'Each experiment contributes to one's understanding. The results of one experiment are critical to determine the next experimental steps.'" (Core design principles)

> Four critical parameters for power analysis: "(1) Standard deviation of measurements; (2) Significance level (typically α = 0.05); (3) Desired power (usually 80%); (4) Meaningful effect size to detect." (Power analysis essentials)

> "Sample size increases with desired power. Larger sample sizes needed for smaller detectable differences. Sample size increases proportionally to measurement variance. Two-sided tests require larger samples than one-sided tests." (Key relationships)

> "Minimum statistical power should be 'at least 80% or greater, to detect a specified practically relevant difference.'" (Practical standard)

---

#### Source 16: 3 Lessons from Implementing CUPED at Nubank
- **URL:** https://building.nubank.com/3-lessons-from-implementing-controlled-experiment-using-pre-experiment-data-cuped-at-nubank/
- **Author/Org:** Nubank Engineering | **Date:** 2023

**Re: CUPED variance reduction for experimentation efficiency**
> "CUPED is a statistical method that leverages pre-experiment data to reduce the variability of key metrics, and by accounting for baseline differences among experimental units, CUPED can significantly improve the statistical power of experiments, making it easier to detect even smaller, yet meaningful, effects." (Overview)

> "When control and treatment groups have different sizes and the treatment changes metric correlations, pooled theta estimation can reduce precision. Nubank switched to a weighted average estimator (θ*) that combines group-specific coefficients, improving robustness across varied experimental conditions." (Lesson 1: unequal variants)

> "Through simulation testing across varying sample sizes and durations, Nubank selected a 42-day lookback window as a practical balance. ~40% of metric comparisons showed >20% variance reduction. Captures at least one billing cycle for comprehensive behavior assessment." (Lesson 2: lookback window)

> "CUPED produces different point estimates than traditional analysis, potentially creating interpretation challenges. The adjusted estimates shrink toward zero for significant results, mitigating Type M errors by preventing inflated effect magnification." (Lesson 3: shrinkage effect)

> "Apply the Delta Method theorem to estimate variance for ratio metrics, deriving covariance through Taylor expansion to calculate θ* accurately." (Best practice for ratio metrics)

---

#### Source 17: Sequential Testing Frameworks (Spotify Engineering)
- **URL:** https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
- **Author/Org:** Spotify Engineering | **Date:** 2023

**Re: Sequential testing to address peeking and reduce sample size**
> "Sequential testing can reduce test duration/sample size by 20-80% while maintaining error probability. The flexibility to analyze data as it gathers is desirable for reducing business risk and opportunity costs, enabling quick implementation of winning variants and stopping tests with little chance of demonstrating an effect." (Search result summary)

> "Group Sequential Testing avoids the large sample size needed by mSPRT and allows earlier decisions than fixed-horizon A/B testing, speeding decisions by 20% to 80% without raising the false positive rate." (Group sequential testing)

> "An Adaptive Sequential Design involves approaches to sequential testing in which the statistical design of the A/B test is not fixed for its entire duration but instead changes based on the data currently gathered and projections from it...an ASD is never more efficient than a classic group sequential design (GSD), as it has been proven that for any ASD there exists at least an equally efficient GSD." (Adaptive sequential design)

---

#### Additional findings: Experimental Design (search summaries)

**Re: Minimum Detectable Effect (MDE)**
> "MDE is the smallest change in a metric that your experiment can detect with statistical significance. It represents the smallest improvement (uplift) you want to be able to confidently detect as statistically significant in a test metric, and essentially defines the sensitivity of your experiment." (Search result summary)

> "Picking the MDE is a trade-off between the smallest effect that is still relevant for the business and the smallest effect that is practically measurable." (Search result summary)

> "For most e-commerce stores, an MDE of 2-5% relative is realistic, high-traffic sites (1M+ monthly visitors) can target 1-2%, while low-traffic sites may need to accept 5-10%." (Industry benchmarks)

**Re: Peeking problem and multiple testing**
> "The peeking problem refers to experimenters making decisions about experiment results based on early data, and the more often the experiment is looked at, the higher the false positive rates will be." (Peeking problem)

> "Sequential testing offers a solution to the peeking problem as it enables peeking during the experiment without inflating the false positive rate. In the Optimizely platform, a mixture sequential probability ratio test (mSPRT) is performed and always valid p-values are constructed." (Sequential testing solution)

> "'Peeking problem 2.0' is a more recent issue that can substantially inflate false positive rates despite the use of sequential tests when participants are measured at multiple points in time during the experiment." (Advanced consideration)

**Re: Factorial designs**
> "A factorial design allows the effect of several factors and even interactions between them to be determined with the same number of trials as are necessary to determine any one of the effects by itself with the same degree of accuracy." (Efficiency)

> "Among 44 binary outcome 2 × 2 factorial RCTs, 82% were conducted for the main purpose of efficiency, with the remaining 18% conducted mainly to assess interactions." (Usage patterns)

> "'Short' model t-tests that ignore interactions yield higher power if interactions are zero, but incorrect inferences otherwise." (Interaction effects warning)

### Sub-question 5: Statistical Computing Tools (R, Python statsmodels/scipy, Stan, PyMC)

#### Source 18: Stan Probabilistic Programming
- **URL:** https://mc-stan.org/
- **Author/Org:** Stan Development Team | **Date:** 2024

**Re: Stan capabilities and use cases**
> "Stan is a probabilistic programming language for specifying statistical models that provides full Bayesian inference for continuous-variable models through Markov chain Monte Carlo methods such as the No-U-Turn sampler, an adaptive form of Hamiltonian Monte Carlo sampling." (Overview)

> "Stan implements reverse-mode automatic differentiation to calculate gradients of the model, which is required by HMC, NUTS, L-BFGS, BFGS, and variational inference." (Technical features)

> "Interfaces for Python, Julia, R, and the Unix shell make it easy to use Stan in any programming environment, on laptops, clusters, or in the cloud." (Multi-platform access)

> "It is generally good practice to simulate fake data multiple times and check that one's statistical procedure reliably reconstructs the assumed parameter values. Working with Bayesian statistics is an iterative process consisting of multiple rounds of building, assessing, and revising models." (Best practices)

---

#### Source 19: PyMC vs Stan MCMC Benchmark
- **URL:** https://www.pymc-labs.com/blog-posts/pymc-stan-benchmark
- **Author/Org:** PyMC Labs / Martin Ingram | **Date:** 2023

**Re: Performance comparison between PyMC and Stan**
> Wall-time results (160,420 tennis matches): "PyMC with JAX on GPU (vectorized): 2.7 minutes; Standard PyMC: ~12 minutes; Stan (cmdstanpy): ~20 minutes." (Performance summary)

> "The vectorized GPU method delivers ~11x more ESS/second than PyMC and Stan, and ~4x more than JAX on CPU." (ESS per second)

> "GPU-accelerated methods are not trading accuracy for speed. They converge to the same posterior as the CPU methods." (Accuracy)

> "JAX on CPU alone—without GPU hardware—provides meaningful acceleration: 'JAX on CPU delivers ~2.9x more ESS/second than both standard PyMC and Stan.'" (JAX on CPU)

> "GPU acceleration becomes advantageous above approximately 50,000 observations. For smaller datasets, CPU methods incur lower overhead despite slower raw speed." (Practical threshold)

> "PyMC's syntax is very similar to Stan except that you don't have to declare your variables (variable types are inferred from their distributions) or your data (since the data comes from the python environment)." (PyMC vs Stan)

---

#### Source 20: ArviZ for Bayesian Model Diagnostics
- **URL:** https://python.arviz.org/
- **Author/Org:** ArviZ developers | **Date:** 2024

**Re: Bayesian model diagnostics and MCMC convergence**
> "ArviZ is a Python package for exploratory analysis of Bayesian models that is specifically designed to work with the output of probabilistic programming libraries like PyMC, Stan, and others by providing a set of tools for summarizing and visualizing the results of Bayesian inference." (Overview)

> "ArviZ provides over 30 plotting functions for visualizing distributions, MCMC diagnostics, model checking, and model comparison." (Capabilities)

> "R-hat (R̂) Diagnostic: compares the variance within chains to the variance between chains, with values close to 1.0 (e.g., < 1.01) suggesting convergence and values much larger than 1 indicating that chains haven't mixed well." (R-hat)

> "Effective Sample Size (ESS): estimates the number of independent samples equivalent to the correlated samples obtained by MCMC, with low ESS values (relative to the total number of post-warmup draws) indicating high autocorrelation and inefficient sampling for that parameter." (ESS)

---

#### Source 21: Ten Quick Tips for Bayesian Statistics
- **URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC11984709/
- **Author/Org:** PMC / NIH | **Date:** 2024

**Re: Best practices and tooling guidance for Bayesian statistics**
> "Bayesian statistics uses conditional probability to update knowledge. 'Probability in classical statistics describes the variability of observable data' while 'In Bayesian statistics, however, probability quantifies our knowledge about anything unobservable, including parameter values.'" (Fundamentals)

> "'If you are unable to simulate data under a model, you probably don't fully understand it.'" (Model validation)

> "Examine MCMC trace plots for convergence and mixing. 'Converged chains look like they are stable and fluctuating around a single average.'" (MCMC diagnostics)

> "Choose established software like Stan, JAGS, or brms based on your experience level and flexibility needs." (Tool selection)

---

#### Source 22: Tidy Modeling with R
- **URL:** https://www.tmwr.org/
- **Author/Org:** Max Kuhn, Julia Silge | **Date:** 2022

**Re: R ecosystem for statistical modeling**
> "The tidymodels framework is a collection of R packages for modeling and machine learning using tidyverse principles. The tidyverse is a dialect of R designed with a consistent, human-centered philosophy, and tidyverse and tidymodels packages can be used to produce high quality statistical and machine learning models." (Framework overview)

---

#### Additional findings: Statistical Computing Tools (2024-2025 search summaries)

**Re: Language ecosystem comparisons**
> "Python is mentioned in over half of data scientist job postings, far outpacing other languages, and Python appears in 76% of data science job listings compared to R at just 28%." (Market position)

> "In 2025, the smartest analysts are often multilingual: use Python for 80% of tasks and workflows, lean on R when statistical depth and visualization matter most, and bring in Julia when speed and performance become the bottleneck." (Recommended approach 2025)

> "Python by far is the slowest of the four languages, but one can use Numba in specific cases to make it the fastest. Julia was designed with speed in mind, taking advantage of modern compiler techniques, and is generally the fastest of the four." (Performance)

> "R is superb for statisticians, researchers, and biostatisticians, even though its star in mainstream industry has dimmed." (R positioning)

> "JAX and NumPyro are gaining traction for statistical modeling, with researchers switching to JAX through NumPyro for scalability." (JAX ecosystem)

**Re: Python statsmodels and scipy**
> "Scipy.Stats module focuses on the statistical theorem such as probabilistic function and distribution, while the statsmodel package focuses on the statistical estimation based on the data." (Key difference)

> "SciPy is the go-to for statistical tests and correlations and is built for checking relationships and running tests like t-tests or ANOVA, while Statsmodels specializes in regression, ANOVA, and time-series analysis and helps evaluate how independent variables affect outcomes." (Tool selection guidance)

> Statsmodels models include: "OLS (Ordinary Least Squares) regression, GLS (Generalized Least Squares), WLS (Weighted Least Squares), RLM (Robust Linear Model), GLM (Generalized Linear Model supporting different distributions like Poisson and Binomial), QuantReg (Quantile regression), and Logit (Logistic regression for binary outcomes)." (Available models)

**Re: R tidymodels 2025 updates**
> "Recent developments highlighted in 2025 include: Integrated support for sparse data; Adding postprocessing to tidymodels, allowing users to add postprocessing adjustments to model predictions alongside preprocessors; Improved error and warning messages across many packages." (2025 updates)

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "McKenzie et al. (2010) found OLS overstatement of 20-82% versus experimental benchmarks" | statistic/attribution | [8] | corrected — source confirms 20-82% range covers all non-experimental methods collectively (OLS ~35%, matching ~20%, DID ~22%); up to 82% applies to invalid instruments only. Findings text updated accordingly. |
| 2 | "EPV > 25: Variable selection acceptable; 10 < EPV ≤ 25: combine with shrinkage; EPV ≤ 10: avoid selection" | statistic | [5] | verified |
| 3 | "Only 24% of published analyses fully report the prior" | statistic | [14] | verified |
| 4 | "Only 18% reported a sensitivity analysis" | statistic | [14] | verified — applies to medical device submissions subset |
| 5 | "56.6% do not check MCMC convergence" | statistic | [14] | verified |
| 6 | "87.9% of published analyses skip sensitivity analysis on the impact of priors" | statistic | [14] | verified |
| 7 | "~40% of metrics achieve >20% variance reduction" (CUPED at Nubank) | statistic | [17] | verified — source states "About 40% of comparisons had their variance reduced by more than 20%" |
| 8 | "42-day lookback window" (CUPED at Nubank) | statistic | [17] | verified |
| 9 | "JAX on GPU delivers ~11x more ESS/second" vs. standard PyMC and Stan | statistic | [21] | verified |
| 10 | "JAX on CPU delivers ~2.9x more ESS/second" vs. standard PyMC and Stan | statistic | [21] | verified |
| 11 | "GPU acceleration becomes advantageous above approximately 50,000 observations" | statistic | [21] | verified — source states "For datasets below ~50,000 matches, GPU methods incur a fixed overhead that makes them slower than CPU" |
| 12 | "Group Sequential Testing reduces test duration by 20-80%" | statistic | [18] | human-review — the 20-80% figure does not appear in the Spotify Engineering article; it appears only in the Extracts as a "search result summary." The Spotify article discusses power advantages but states no specific duration-reduction percentage. The Findings attribute this to [18], which is unconfirmed by the source. |
| 13 | "Python appears in 76% of data science job listings vs R at 28%" | statistic | search summary (no URL) | unverifiable — attributed to search summaries only; no citable URL provided; cannot be re-fetched |
| 14 | "one covariate per ~22 events" (Cox regression rule) | statistic | [4] | verified — source states "approximately one covariate into the model for every 22 patients who died" |
| 15 | "Stan is the gold standard for full Bayesian inference" | superlative | [19] | human-review — the Stan website does not use the phrase "gold standard"; this is an editorial characterization in the document body, not language from the cited source |
| 16 | "Bayesian A/B testing can reduce required sample size by 75% compared to frequentist approaches" | statistic | search summary (no URL) | human-review — not found in the Dynamic Yield source [13]; appears only in Extracts as a "search result summary." The Findings section correctly flags this as unsubstantiated COI-vendor marketing; no independent source confirms the 75% figure |
| 17 | "F-statistic threshold is now contextually >20 (previously >10), and for single instruments the recommendation exceeds F > 50" | statistic | [8] | verified — source states F < 20 means consider OLS; single instrument should "exceed 50" |
| 18 | "82% of 2×2 factorial RCTs conducted for efficiency rather than interaction testing" | statistic | search summary (no URL) | unverifiable — attributed to search summaries only; no citable URL provided |

## Challenge

### Assumptions Check

| Assumption | Supporting Evidence | Counter-Evidence | Impact if False |
|------------|-------------------|------------------|-----------------|
| GLMMs are the correct default for clustered/hierarchical data | Sources 1, 5, 6 confirm mixed-effects models are essential for within-subject dependence and nested structures; 2023 PMC review validates wide use | Random effects misspecification is common and can produce worse inference than simpler models; 2014 estimation study (Source 7) notes convergence problems and binary outcome bias under Laplace/pseudo-likelihood; simpler GEEs or cluster-robust OLS may suffice for population-average questions where subject-level effects are not of interest | Analysts over-apply GLMMs to data where GEE or robust SE approaches would be more appropriate and equally valid, inflating model complexity |
| OLS overestimates causal effects by 20-82% vs. experimental benchmarks | Source 8 (McKenzie et al. 2010) is cited directly; consistent with well-known omitted variable bias literature | The 20-82% range comes from a single 2010 paper in agricultural/development economics; range is wide and context-specific; a 2024 meta-analysis (Royal Society Open Science) found psychology meta-analyses overestimate by variable amounts but the mechanism and magnitude differ across fields; OLS can also underestimate when measurement error attenuates coefficients | The claim overstates a context-specific finding as a general rule; in settings with low confounding or measurement error attenuation, OLS may be closer to truth than IV/DiD estimates |
| Bayesian A/B testing reduces required sample size by 75% vs. frequentist | Cited in search summary from Dynamic Yield (a vendor source, Source 13 — flagged COI); conceptually supported by the idea that informative priors encode prior data | The 75% figure comes from a vendor-promoted source with commercial incentive; independent reviews (CXL, Eppo 2025) show Bayesian methods do not guarantee smaller sample sizes — sample efficiency depends entirely on prior informativeness; Bayesian optional stopping without pre-specified stopping rules inflates false positives just as in frequentist tests (Molas 2025); with uninformative priors, sample requirements are equivalent | The 75% figure is misleading marketing; in practice, Bayesian A/B testing's advantage is interpretability and flexibility, not a universal 75% reduction in sample size |
| The F-statistic threshold for valid IV is now >20 (replacing the old >10 rule) | Source 8 (arXiv 2025 preprint) cites this guidance; Andrews, Stock, Sun (2019) is frequently cited | The updated threshold applies to the robust F-statistic, but recent work (Windmeijer 2025, Journal of Econometrics) argues the robust first-stage F-statistic cannot be used as a valid weak-instruments test for the 2SLS estimator under heteroskedasticity; correct threshold depends on model assumptions (homoskedastic vs. robust); "effective F-statistic" of Montiel Olea & Pflueger (2013) is now recommended over any fixed threshold | Using F>20 as a blanket rule without accounting for heteroskedasticity structure gives false confidence; the threshold is model-dependent, not universal |
| JAX+GPU provides ~11x ESS/second speedup broadly applicable to Bayesian computation | Source 21 benchmark (PyMC Labs/Ingram 2023) documents the result; GPU advantage above ~50k observations is internally noted | The benchmark used a single model (hierarchical tennis skill model); the original authors acknowledged the model may be "particularly well suited to the GPU" and gains for other models may be smaller; Stan was not using GPU in the comparison; PyMC Discourse threads report negligible speedup for different model structures; the 50k observation threshold is model-class-specific | The 11x figure is real for that specific benchmark but should not be treated as a general multiplier; models with more complex dependency structures or small observation counts will see much smaller gains |

---

### Analysis of Competing Hypotheses

**Competing hypotheses for why Bayesian A/B testing is recommended in business contexts:**

- **Hypothesis A (document's position):** Bayesian A/B testing is superior for business because it reduces required sample size by ~75%, enables continuous monitoring, and provides intuitive probabilistic outputs.
- **Hypothesis B (interpretability-only view):** Bayesian A/B testing offers no sample size advantage over well-designed frequentist sequential tests; its real value is interpretability (P2BB vs. p-value) and coherent uncertainty quantification, not efficiency.
- **Hypothesis C (vendor narrative):** The "75% sample size reduction" claim is primarily vendor marketing; both approaches converge to similar operating characteristics when priors are uninformative, and frequentist sequential testing (mSPRT, group sequential) closes the flexibility gap.

| Evidence | Hypothesis A: Bayesian reduces sample size | Hypothesis B: Interpretability advantage only | Hypothesis C: Vendor narrative inflates claims |
|----------|-------------------------------------------|-----------------------------------------------|-----------------------------------------------|
| Dynamic Yield/Mastercard source (Source 13, vendor, COI flagged) cites 75% reduction | C | N | C |
| Alex Molas (2025): Bayesian optional stopping inflates false positives identical to frequentist | I | C | C |
| mSPRT and group sequential testing achieve 20-80% sample reductions (Source 18) | I | C | C |
| Bayesian approach provides intuitive P2BB metric (Source 12, 13) | C | C | N |
| With large data, prior "washes out" (Source 12) — Bayesian approaches uninformative priors = frequentist | I | C | C |
| Sequential testing "Peeking problem 2.0" — multiple measurements per user inflate FPR even with sequential tests | N | N | N |

Inconsistencies: A=3 | B=0 | C=0

**Selected: Hypothesis B** — fewest inconsistencies. Bayesian A/B testing's defensible advantage is interpretability and coherent decision-making under uncertainty, not a universal 75% sample size reduction. The efficiency claim depends on informative priors; with vague priors and continuous monitoring, false positive inflation remains unless explicit stopping rules are applied.

---

**Competing hypotheses for the role of DAGs in causal identification:**

- **Hypothesis A (document's position):** DAGs are essential tools for confounding identification in observational research; absent arrows encode stronger assumptions than present ones.
- **Hypothesis B (DAG-skeptic view):** DAGs are useful heuristics but practically limited by subjectivity in graph construction, inability to represent unmeasured confounders reliably, and low rates of correct application in published research.
- **Hypothesis C (DAG-agnostic view):** For most applied business contexts, structured covariate selection based on subject-matter knowledge achieves equivalent confounding control without formal DAG construction.

| Evidence | Hypothesis A: DAGs essential | Hypothesis B: DAGs are limited heuristics | Hypothesis C: DAGs unnecessary for business |
|----------|-----------------------------|--------------------------------------------|---------------------------------------------|
| PMC 2024 six-step DAG framework (Source 11) supports systematic use | C | N | I |
| Review: only ~20% of studies using DAGs reported adjustment sets implied by the DAG (Oxford IJE) | N | C | N |
| DAG subjectivity review: variety partly reflects "inherent flexibility and subjectivity" (Tandfonline 2024) | N | C | N |
| Unmeasured confounding remains unaddressed by DAGs even when graph is correct | N | C | C |
| DoWhy (Source 10) wraps DAG methodology into accessible tooling | C | N | N |

Inconsistencies: A=0 | B=0 | C=1

**Selected: Tie between A and B** — zero inconsistencies each. The document's claim that DAGs are "essential" is defensible but should be qualified: DAGs are necessary for rigorous confounding identification but are not sufficient (subjectivity, unmeasured confounders), and poor application rates in published work suggest the assumed adoption level may be aspirational rather than current practice.

---

### Premortem

Assume the main conclusions of this research are wrong — that practitioners follow these best practices and achieve the promised results.

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| **The "best practice" findings primarily reflect academic/research norms, not business/industry constraints.** Most sources come from medical statistics, agricultural economics, and vendor blogs. Applied business teams operate under time pressure, small samples, and non-experimental data that rarely meets GLMM convergence or IV validity requirements. Recommended methods may be technically correct but practically infeasible at scale. | High | Significant. Conclusions about GLMMs, DAGs, and IV validity may need to be scoped explicitly to research-grade analysis contexts, not operational business intelligence workflows where simpler, robust estimators are preferred. |
| **Benchmark statistics (75% sample reduction, 11x GPU speedup, 87.9% sensitivity gaps) are narrow, context-specific numbers elevated to general principles.** The 75% Bayesian efficiency figure comes from a single vendor source with COI. The 11x speedup comes from one model class. The 87.9% sensitivity gap is from medical device submissions, not business analytics. Citing these numbers as representative overstates their generalizability. | High | Moderate. These figures should be presented as lower/upper bounds or illustrative cases, not universal multipliers. Claims about Bayesian and GPU efficiency need explicit scope conditions. |
| **The F>20 IV threshold and modern DiD methods (Callaway & Sant'Anna, etc.) may resolve one set of problems while introducing new ones.** Heteroskedasticity-robust testing invalidates the F>20 rule itself; modern DiD methods introduce their own assumptions and require larger datasets for reliable estimation. Adopting "modern fixes" without understanding their own preconditions creates a false sense of methodological rigor. | Medium | Moderate. The conclusion that modern DiD and updated IV thresholds represent definitive fixes should be qualified — they are improvements under specific conditions, not universal solutions. The pre-trends parallel test remaining "neither necessary nor sufficient" (confirmed by 2024-2025 literature) is already noted in the document but should be emphasized as a core limitation, not a footnote. |

## Findings

### 1. Applied Statistical Modeling (Regression, GLMs, Mixed Models, Survival Analysis)

**Generalized Linear Models (GLMs) are the correct framework for non-normal outcomes.** Use distribution-appropriate families: binomial/logit for binary outcomes, Poisson/negative-binomial for counts. Compute average marginal effects for interpretable slope estimates; do not treat pseudo-R² values as direct analogues of linear R² [3]. When overdispersion appears in count data, prefer negative binomial over Poisson [3]. (HIGH — T4 Clark 2024 + T3 PMC sources converge)

**Mixed-effects models (GLMMs) are required for clustered and longitudinal data**, where within-subject correlation or hierarchical nesting invalidates independence assumptions [6]. Fixed effects capture relationships of primary interest; random effects account for subject-level variation and cluster effects [6]. However, GLMMs are not the default for all hierarchical data — when the research question targets population-average effects (not subject-level), GEE or cluster-robust OLS may be more appropriate and less prone to misspecification [1]. (MODERATE — challenge qualifies the "always GLMM" framing)

**Variable selection demands events-per-variable discipline.** EPV > 25: selection is acceptable with stability investigation; 10 < EPV ≤ 25: combine selection with shrinkage (LASSO); EPV ≤ 10: avoid selection entirely and use a global model with shrinkage [5]. Backward elimination is preferred over forward selection; use AIC (α ≈ 0.157) as the default stopping criterion; avoid univariable prescreening [5]. Bootstrap stability analysis should accompany any variable selection to assess inclusion frequencies and conditional bias [5]. (HIGH — T3 peer-reviewed systematic review)

**Cox regression is standard for time-to-event outcomes**, requiring proportional hazards (PH) assumption testing before interpretation. PH violation is flagged when survival curves cross. Rule of thumb: one covariate per ~22 events. Cox accommodates continuous covariates and confounder adjustment without distributional assumptions on survival times [4]. (HIGH — T3 source, methodology stable)

**Residual diagnostics are mandatory before inference.** The four standard plots — Residuals vs Fitted, Normal Q-Q, Scale-Location, Residuals vs Leverage — each target distinct assumption violations. Statistical tests for normality are often over-sensitive; visual diagnostics are more informative for understanding violation magnitude [2, 3]. (HIGH — T4+T3 sources converge)

---

### 2. Causal Inference in Observational Data

**Causal identification strategy must be stated explicitly and empirically justified.** The "credibility revolution" in applied economics requires moving beyond "mere application of an econometric approach" — state all assumptions required for unbiased estimation, use DAGs to identify appropriate controls, and avoid bad controls [8]. (HIGH — T3 arXiv 2025, consistent with broader applied econometrics literature)

**OLS overstates treatment effects under omitted variable bias.** McKenzie et al. (2010) found that non-experimental methods overstated effects by 20-82% versus experimental benchmarks: OLS ~35%, matching ~20%, DID ~22%; instruments with violated exclusion restrictions produced overstatement up to 82% [8]. This range is context-specific (agricultural/development economics); measurement error attenuation can push OLS in the opposite direction. The lesson is directional: OLS should not be given causal interpretation without a credible identification strategy. (MODERATE — single study, mechanism acknowledged)

**Propensity score methods**: Select variables based on causal knowledge, not predictive power — adding non-confounders increases the c-statistic without improving causal inference [9]. Assess balance via standardized differences below 0.1, not model fit statistics [9]. PSM (average treatment effect on the treated) and IPW (population ATE) target different estimands and answer different research questions [9]. (HIGH — T3 PMC source)

**Instrumental variables: F-statistic threshold is now contextually >20** (previously >10), and for single instruments, the recommendation exceeds F > 50 [8]. Critically, the standard robust F-statistic is not a valid weak-instruments test under heteroskedasticity; the Montiel Olea & Pflueger effective F-statistic is the appropriate modern alternative. 2SLS estimates LATE (Local Average Treatment Effect) for compliers only — not overall ATE [8]. (MODERATE — T3 preprint; confirmed by econometrics literature, though threshold debate continues)

**Difference-in-differences: TWFE is biased under staggered adoption.** Standard two-way fixed effects produces biased estimates when treatments are implemented at different times across units (negative weights problem). Modern alternatives — Callaway & Sant'Anna (2021), Borusyak et al. (2024), Sun & Abraham (2021) — address this [8]. Pre-trend testing is necessary but insufficient: parallel pre-trends are neither necessary nor sufficient for identification [8]. Use Bacon Decomposition to diagnose TWFE composition [8]. (HIGH — T3 source, confirmed across applied econometrics literature)

**Synthetic control method** applies when parallel trends fails, given long pre-treatment history on a small number of treated units. Use permutation-based inference; avoid overfitting by restricting comparison units to similar donors [8]. Synthetic DiD (SDID) combines SCM and DiD, relaxing parallel trends requirements [8]. (MODERATE — T3 preprint, methods less widely adopted than DiD)

**DAGs are necessary but not sufficient for confounding identification.** The six-step framework (define exposure/outcome, add common causes, consider selection/measurement error, inform analysis) provides a systematic approach [11]. Absent arrows encode stronger assumptions than present ones [11]. In practice, DAGs are aspirational — only ~20% of published studies using DAGs report the implied adjustment set [Challenge]. (MODERATE — T3 PMC 2024; application gap noted in challenge)

**DoWhy** (Python, PyWhy/Microsoft) provides a unified interface for causal inference: model, identify, estimate, refute. Its refutation API enables assumption testing for any estimator, making it the current best-in-class Python tool for applied causal inference [10]. (HIGH — T1 official documentation)

---

### 3. Bayesian Methods for Business

**Bayesian A/B testing's primary advantage is interpretability, not sample efficiency.** The Probability to Be Best (P2BB) metric provides intuitive, probabilistic decision framing vs. binary p-value interpretation [13]. The claim that Bayesian testing reduces required sample size by 75% originates from a COI-flagged vendor source (Dynamic Yield) and is not independently corroborated — with uninformative priors, sample requirements are equivalent to frequentist methods, and Bayesian optional stopping without pre-specified rules inflates false positives identically [Challenge, 18]. (HIGH — challenge consensus from ACH analysis)

**Probabilistic forecasting with hierarchical Bayesian models outperforms point predictions** in settings with hierarchical structure, censored data (stockouts, capacity limits), or strong domain constraints. Hierarchical exponential smoothing with shared trends is especially effective for small datasets within a hierarchy [12]. State-space models (Kalman filtering) provide decomposable components with uncertainty quantification [12]. (HIGH — T4 core maintainer source + general Bayesian literature)

**Reporting standards for Bayesian analyses are rarely met in practice.** Only 24% of published analyses fully report the prior; only 18% report a sensitivity analysis; 56.6% do not check MCMC convergence [14]. Required reporting includes: likelihood function and prior documentation, MCMC convergence (R-hat, ESS), posterior predictive checks, prior sensitivity analysis, and annotated code sharing [14]. (HIGH — T3 PMC reporting guidelines)

**Bayesian hierarchical models for marketing measurement** (MMM) allow estimation of media impact with explicit uncertainty, enabling optimization of campaign frequency [15]. Google's open-source Meridian follows this approach. (MODERATE — T2 Google Research, mild COI)

**Prior predictive checks are essential** for model validation before fitting data. Extreme values in prior predictive distributions indicate priors that are too strong, too weak, or poorly located [14, 22]. (HIGH — T3 reporting guidelines + peer-reviewed tips)

---

### 4. Experimental Design for Maximum Power with Minimum Sample

**Power analysis requires four inputs**: measurement SD, significance level (α typically 0.05), desired power (≥80% standard), and minimum detectable effect (MDE) [16]. MDE is a business decision, not a statistical one — it represents the smallest effect that would change an action. For e-commerce, 2-5% relative MDE is typical; high-traffic sites can target 1-2% [search summaries]. (HIGH for framework, MODERATE for MDE benchmarks — search summaries only)

**CUPED (Controlled-experiment Using Pre-Experiment Data) reduces variance using pre-experiment covariate correlation.** Implementation lessons from Nubank: use a 42-day lookback window; ~40% of metrics achieve >20% variance reduction; use weighted average theta (θ*) estimator for unequal variant sizes; apply Delta Method for ratio metrics [17]. CUPED point estimates are shrunk toward zero, mitigating Type M errors [17]. (MODERATE — T4 engineering blog, but widely reproduced across major experimentation platforms)

**Sequential testing addresses the peeking problem.** Group Sequential Testing (GST) reduces test duration vs. fixed-horizon while maintaining false positive rate [18]. *(Note: a specific 20-80% duration reduction figure appears in search summaries but is not confirmed in source [18] — human-review)* mSPRT provides always-valid p-values for continuous monitoring but requires larger sample sizes than GST [18]. Adaptive Sequential Designs are never more efficient than a well-designed GST [18]. Be aware of "peeking problem 2.0" — multiple measurements per user inflate FPR even with sequential tests [search summaries]. (MODERATE — T4 Spotify; methodology validated by broader experimentation literature)

**Five fundamental design principles**: replication, randomization, blocking/grouping, multifactorial design, and sequential approach [16]. Factorial designs allow testing multiple factors simultaneously with no additional sample cost; 82% of 2×2 factorial RCTs are used for efficiency rather than interaction testing [search summaries]. Ignoring interactions in factorial designs yields incorrect inference [search summaries]. (HIGH — T3 PMC source)

**Blocking reduces variance and increases precision** by organizing homogeneous experimental units, reducing between-group confounding without increasing sample size [16]. (HIGH — T3 source)

---

### 5. Statistical Computing Tools

**Stan** is a leading tool for full Bayesian inference *(the "gold standard" label is editorial characterization; Stan website does not use this phrase — human-review)*: NUTS sampler (adaptive HMC), automatic differentiation, interfaces for Python (cmdstanpy/pystan), R (rstan/cmdstanr), and Julia [19]. Best practice is iterative: simulate fake data to verify recovery of assumed parameters before fitting real data [19]. (HIGH — T1 official documentation)

**PyMC** is the leading Python-native Bayesian framework: similar to Stan in syntax but with no explicit type declarations; supports JAX backend for performance scaling [21]. With JAX on GPU, vectorized models achieve ~11x more ESS/second than standard PyMC or Stan above ~50k observations; JAX on CPU alone delivers ~2.9x more ESS/second [21]. These gains are model-class-specific — the benchmark used a hierarchical sports model; complex dependency structures may see smaller gains. (MODERATE — T4 benchmark, COI-flagged; accuracy of posterior confirmed identical to CPU methods)

**ArviZ** is the standard Python library for Bayesian model diagnostics: R-hat (< 1.01 for convergence), ESS, trace plots, posterior predictive checks, and model comparison. Works with outputs from PyMC, Stan, and other PPLs [20]. (HIGH — T1 official documentation)

**Python statsmodels vs scipy.stats**: statsmodels for regression inference (OLS, GLS, GLM, QuantReg, time-series models); scipy.stats for hypothesis tests, distributions, and correlations [search summaries]. They are complementary, not competing. (HIGH — consistent across search summaries)

**R ecosystem**: tidymodels (Kuhn/Silge) provides a unified, tidyverse-consistent interface for statistical modeling and ML. 2025 updates include sparse data support and prediction postprocessing [23]. R retains strong positioning for statisticians, biostatisticians, and researchers despite declining industry market share. brms (Bayesian regression models using Stan, in R) is the practical entry point for R users requiring Bayesian mixed models [22]. (HIGH — T4 primary framework authors)

**Language selection heuristics for 2025**: Python for 80% of production tasks and ML pipelines; R when statistical depth, visualization (ggplot2), or biostatistics-specific packages are required; Julia for computationally intensive modeling where Python/R performance is a bottleneck [search summaries]. JAX/NumPyro is gaining traction for scalable probabilistic modeling. (MODERATE — search summaries, directional consensus)

---

### Counter-Evidence and Qualifications

- **GLMM convergence failures are common** — researchers should have GEE and cluster-robust OLS as fallbacks, not treat GLMMs as universally applicable.
- **The "75% sample reduction" for Bayesian A/B testing is not corroborated** by independent sources and likely reflects marketing copy rather than general methodology performance.
- **IV F-statistic thresholds are model-assumption-dependent** — the Montiel Olea & Pflueger effective F-statistic, not a blanket F>20 rule, is the current methodological standard.
- **GPU speedup benchmarks are model-specific** — do not treat 11x as a general multiplier; for models not suited to vectorized GPU computation, standard CPU methods remain appropriate.
- **Best practices from medical statistics and academic economics may not transfer directly** to operational business analytics contexts where time, data quality, and computational constraints differ significantly.

## Takeaways

### Key Practical Guidance

1. **Match model to data structure**: GLM for non-normal outcomes, GLMM for hierarchical/longitudinal, GEE for population-average questions.
2. **Causal claims require identification strategies**: state assumptions explicitly; use DAGs; apply modern DiD (Callaway & Sant'Anna) for staggered adoption.
3. **Bayesian over frequentist for interpretability, not efficiency**: P2BB vs. p-value framing matters for business decisions; efficiency requires informative priors.
4. **Instrument quality before IV estimation**: use Montiel Olea & Pflueger effective F, not a blanket F>20 rule.
5. **Reduce variance before increasing sample**: CUPED, blocking, and covariate adjustment are cheaper than larger experiments.
6. **Stan or PyMC+ArviZ for Bayesian work**: Stan for stability and multi-language; PyMC for Python-native workflows; JAX backend when datasets exceed ~50k observations.

### Limitations and Gaps

- **Source bias toward medical statistics and academic economics**: most T3 sources come from PMC/NIH and applied econometrics, not industry analytics. Best practices may not transfer directly to business operational contexts.
- **Coverage gaps**: double machine learning (DML/EconML), regression discontinuity design (RDD), and multi-armed bandit experimentation are not covered in depth.
- **Rapidly evolving area**: causal inference methods (synthetic DiD, debiased ML), Bayesian tooling (NumPyro/JAX), and experimentation platforms are changing faster than literature captures.
- **Human-review items**: three claims in the Claims table require editorial review before citation (claims #12, #15, #16).

### Follow-Up Questions

- How does double machine learning (EconML) compare to propensity score methods for high-dimensional observational data?
- What are current best practices for regression discontinuity design in business contexts?
- How do experimentation platforms (Statsig, Eppo, Optimizely) implement sequential testing and CUPED in production?
- What is the current state of NumPyro vs. PyMC for large-scale Bayesian modeling?

### Search Protocol

29 searches executed across 5 sub-questions. 23 sources used (21 verified reachable; 2 via 403 access-restricted).

| Query | Source | Date Range | Found | Used |
|-------|--------|------------|-------|------|
| applied statistical modeling best practices 2025 regression GLM mixed models | google | 2024-2026 | 10 | 3 |
| generalized linear models best practices applied statistics 2024 2025 | google | 2024-2025 | 10 | 3 |
| survival analysis best practices Cox model 2024 applied statistics | google | 2024-2026 | 10 | 2 |
| mixed effects models best practices lme4 R Python statsmodels 2024 | google | 2024-2026 | 10 | 2 |
| regression model diagnostics assumptions checking 2024 best practices residual analysis | google | 2024-2026 | 10 | 2 |
| applied regression analysis model selection variable selection modern approaches 2025 | google | 2024-2026 | 10 | 2 |
| causal inference observational data best practices 2025 propensity score matching | google | 2024-2026 | 10 | 3 |
| difference-in-differences DiD instrumental variables causal inference 2024 2025 | google | 2024-2026 | 10 | 3 |
| synthetic control method causal inference observational studies best practices 2024 | google | 2024-2026 | 10 | 2 |
| causal inference directed acyclic graphs DAG confounding adjustment 2024 2025 | google | 2024-2026 | 10 | 2 |
| causal inference Python DoWhy EconML double machine learning 2024 | google | 2024-2026 | 10 | 2 |
| regression discontinuity design RDD best practices 2024 applied econometrics | google | 2024-2026 | 10 | 1 |
| Bayesian methods business applications hierarchical models 2024 2025 practical | google | 2024-2026 | 10 | 3 |
| Bayesian A/B testing business decision making 2024 best practices | google | 2024-2026 | 10 | 3 |
| PyMC Bayesian modeling demand forecasting practical tutorial 2024 | google | 2024-2026 | 10 | 2 |
| Bayesian hierarchical model marketing mix modeling media measurement 2024 2025 | google | 2024-2026 | 10 | 2 |
| Bayesian inference priors posterior predictive checks best practices 2024 applied | google | 2024-2026 | 10 | 2 |
| experimental design statistical power sample size calculation best practices 2024 2025 | google | 2024-2026 | 10 | 2 |
| A/B testing sequential testing adaptive design statistical power 2024 | google | 2024-2026 | 10 | 3 |
| CUPED variance reduction experimentation platform best practices 2024 online experiments | google | 2024-2026 | 10 | 2 |
| minimum detectable effect size MDE experimental design practical guide 2024 | google | 2024-2026 | 10 | 2 |
| factorial design interaction effects experiment power efficiency 2024 applied statistics | google | 2024-2026 | 10 | 2 |
| platform experiment design peeking problem multiple testing correction best practices 2024 | google | 2024-2026 | 10 | 2 |
| Stan probabilistic programming Bayesian inference best practices 2024 2025 | google | 2024-2026 | 10 | 2 |
| PyMC vs Stan comparison probabilistic programming statistical modeling 2024 | google | 2024-2026 | 10 | 2 |
| Python scipy statsmodels statistical computing data science 2024 best practices | google | 2024-2026 | 10 | 3 |
| R statistical computing tidymodels tidyverse applied statistics 2024 2025 best practices | google | 2024-2026 | 10 | 2 |
| statistical computing tools comparison R Python Julia Numba JAX for statistics 2024 2025 | google | 2024-2026 | 10 | 2 |
| ArviZ Bayesian model diagnostics MCMC convergence diagnostics 2024 Python | google | 2024-2026 | 10 | 2 |

<!-- search-protocol
[
  {"query": "applied statistical modeling best practices 2025 regression GLM mixed models", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "generalized linear models best practices applied statistics 2024 2025", "source": "google", "date_range": "2024-2025", "results_found": 10, "results_used": 3},
  {"query": "survival analysis best practices Cox model 2024 applied statistics", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "mixed effects models best practices lme4 R Python statsmodels 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "regression model diagnostics assumptions checking 2024 best practices residual analysis", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "applied regression analysis model selection variable selection modern approaches 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "causal inference observational data best practices 2025 propensity score matching", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "difference-in-differences DiD instrumental variables causal inference 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "synthetic control method causal inference observational studies best practices 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "causal inference directed acyclic graphs DAG confounding adjustment 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "causal inference Python DoWhy EconML double machine learning 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "regression discontinuity design RDD best practices 2024 applied econometrics", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 1},
  {"query": "Bayesian methods business applications hierarchical models 2024 2025 practical", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "Bayesian A/B testing business decision making 2024 best practices", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "PyMC Bayesian modeling demand forecasting practical tutorial 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Bayesian hierarchical model marketing mix modeling media measurement 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Bayesian inference priors posterior predictive checks best practices 2024 applied", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "experimental design statistical power sample size calculation best practices 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "A/B testing sequential testing adaptive design statistical power 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "CUPED variance reduction experimentation platform best practices 2024 online experiments", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "minimum detectable effect size MDE experimental design practical guide 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "factorial design interaction effects experiment power efficiency 2024 applied statistics", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "platform experiment design peeking problem multiple testing correction best practices 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Stan probabilistic programming Bayesian inference best practices 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "PyMC vs Stan comparison probabilistic programming statistical modeling 2024", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "Python scipy statsmodels statistical computing data science 2024 best practices", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 3},
  {"query": "R statistical computing tidymodels tidyverse applied statistics 2024 2025 best practices", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "statistical computing tools comparison R Python Julia Numba JAX for statistics 2024 2025", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2},
  {"query": "ArviZ Bayesian model diagnostics MCMC convergence diagnostics 2024 Python", "source": "google", "date_range": "2024-2026", "results_found": 10, "results_used": 2}
]
-->
