---
name: LLM Agent SDL Maturity and Best-Practice Composite
description: "No mature SDL standard exists for LLM agents — best practice composites NIST 800-218A, OWASP LLM Top 10, and MITRE ATLAS with evaluation-driven development and adaptive red teaming."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://iain.so/security-for-production-ai-agents-in-2026
  - https://www.giskard.ai/knowledge/risk-assessment-for-llms-and-ai-agents-owasp-mitre-atlas-and-nist-ai-rmf-explained
  - https://csrc.nist.gov/pubs/sp/800/218/a/final
  - https://www.promptfoo.dev/docs/red-team/owasp-llm-top-10/
  - https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents
related:
  - docs/context/coding-agent-compound-risk-injection-plus-agency.context.md
  - docs/context/prompt-injection-architectural-defense-patterns.context.md
  - docs/context/agent-generated-code-security-patterns.context.md
  - docs/context/llm-context-credential-leakage-and-sanitization.context.md
---
# LLM Agent SDL Maturity and Best-Practice Composite

## Key Insight

"The industry is quite literally where web security was in 2004. There is no equivalent to SAMM for AI agents, and organisations have no standardised way to assess or benchmark their agent security practices." No single SDL framework covers the full scope. Best practice is a composite of NIST 800-218A + OWASP LLM Top 10 + MITRE ATLAS, implemented through evaluation-driven development and adaptive red teaming.

## Framework Roles

Three frameworks address complementary questions:
- **OWASP LLM Top 10**: "What are the most common AI vulnerabilities?" (vulnerability enumeration)
- **MITRE ATLAS**: "How can we classify and prevent threats?" (threat taxonomy, technique mapping)
- **NIST AI RMF**: "How do we govern and manage AI risk at scale?" (organizational governance)

No single framework is sufficient. Use OWASP for specific vulnerability guidance and red teaming targets; ATLAS for attack technique mapping and mitigation selection; NIST AI RMF for governance, accountability, and continuous improvement processes.

## NIST SP 800-218A

Published July 2024 by NIST. Augments the base Secure Software Development Framework (SSDF) v1.1 with AI-model-specific practices covering generative AI and dual-use foundation models. Mandated by Executive Order 14110. Targets: AI model producers, producers of AI systems using those models, and system acquirers.

NIST is developing specific overlays for single and multi-agent AI systems; draft expected Q3 2026.

## MITRE ATLAS (v5.4.0, February 2026)

16 tactics, 84 techniques, 56 sub-techniques, 32 mitigations, 42 case studies. October 2025 update added 14 new techniques specifically for AI agents: Modify AI Agent Configuration, RAG Database Retrieval manipulation, LLM Plugin Compromise.

Key tactic-to-mitigation mappings:
- Direct Prompt Injection → AI telemetry logging
- Indirect Prompt Injection → monitoring and logging
- LLM Jailbreak → guardrails and model alignment

## NIST AI RMF Four Core Functions

1. **Map** — identify and assess AI risks across system lifecycle
2. **Measure** — quantify risks using quantitative and qualitative methods
3. **Manage** — implement controls and continuous improvement
4. **Govern** — establish accountability, policies, and organizational culture

## Evaluation-Driven SDL

Traditional regression testing is "necessary but not sufficient" for AI components. The evaluation-driven development cycle:
1. Build evaluation suites before implementation
2. Instrument comprehensive telemetry from day one
3. Monitor actual production behavior
4. Analyze failure root causes
5. Expand tests for discovered failure modes
6. Iterate guardrails continuously

AI components require: behavioral testing, adversarial evaluation, and continuous monitoring — in addition to standard code review, static analysis, dependency scanning, and threat modeling for the non-AI components they interact with.

## Red Teaming as SDL Gate

Promptfoo provides `owasp:llm:01` through `owasp:llm:10` shorthand configurations; `owasp:llm` tests all vulnerabilities simultaneously. PII leakage has four specialized plugins (`pii:direct`, `pii:session`, `pii:social`, `pii:api-db`). Excessive Agency testing includes `excessive-agency`, `overreliance`, `imitation`, `hijacking`, and RBAC plugins.

Red teaming should be adaptive — not a one-time gate but a continuous process that expands test coverage as new attack patterns are discovered.

## Model Versioning and Observability

Pin explicit model versions (e.g., `claude-3-opus-20240229` rather than floating aliases). Stage rollouts: 10% → 100% while monitoring. Shadow testing: run new versions in parallel. Define rollback triggers: automatic if eval scores drop or guardrail triggers increase.

OpenTelemetry captures: model identifiers and versions, token consumption, generation completion reasons, request parameters. "LLMs are inherently opaque systems — even creators don't fully understand internal reasoning." Chain-of-thought prompting makes models "show working," providing rationalization (not genuine insight) that is still useful for debugging.

## Takeaway

There is no mature SDL for LLM agents. Implement a composite: NIST 800-218A for AI-specific secure development practices, OWASP LLM Top 10 for vulnerability coverage, MITRE ATLAS for attack taxonomy and mitigation mapping. Add evaluation-driven development (build evals before building features) and adaptive red teaming as continuous gates rather than point-in-time checks.
