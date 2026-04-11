---
name: Coding Agent Compound Risk — Injection Plus Excessive Agency
description: LLM01 (Prompt Injection) and LLM06 (Excessive Agency) combine into a compound risk where successful injection reaches excessive permissions — least privilege is the last line of defense.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  - https://www.firetail.ai/blog/llm06-excessive-agency
  - https://www.trydeepteam.com/docs/frameworks-owasp-top-10-for-llms
  - https://iain.so/security-for-production-ai-agents-in-2026
related:
  - docs/context/prompt-injection-architectural-defense-patterns.context.md
  - docs/context/agent-generated-code-security-patterns.context.md
  - docs/context/llm-agent-sdl-maturity-and-best-practice-composite.context.md
  - docs/context/mcp-security-annotations-and-limitations.context.md
---
# Coding Agent Compound Risk — Injection Plus Excessive Agency

## Key Insight

LLM01 (Prompt Injection) and LLM06 (Excessive Agency) are individually dangerous. Together they form a compound risk: a successful injection that reaches an agent with excessive permissions can trigger unauthorized code execution, privilege escalation, and system access. Least privilege is the last line of defense when injection prevention fails (HIGH — OWASP T1, multiple T3 sources converge).

## LLM01: Prompt Injection

Prompt injection is ranked the most dangerous risk for coding agents. "LLM01 (Prompt Injection), LLM05 (Improper Output Handling), LLM06 (Excessive Agency), and LLM07 (System Prompt Leakage) pose the greatest risks to autonomous coding agents due to their potential for code execution, privilege escalation, and unauthorized system access."

Indirect injection is the dominant real-world vector: malicious instructions hidden in external content — code comments, commits, web pages, emails — that the agent processes as data but the model treats as instruction. Prompt injection found in "73% of audited deployments."

## LLM06: Excessive Agency

"Excessive Agency occurs when an AI agent performs inappropriate, damaging actions in response to unusual language model outputs, despite being granted necessary capabilities for legitimate purposes."

Three design flaws cause Excessive Agency:
1. **Excessive Functionality** — agents retain unnecessary tools or extensions from the development phase
2. **Excessive Permissions** — models have access to downstream systems beyond their intended scope
3. **Excessive Autonomy** — agents perform unapproved actions without constraints or confirmations

Each flaw independently increases blast radius. Together, they guarantee that a successful injection can cause maximum damage.

## The Compound Risk

When LLM01 and LLM06 combine:
- An injected instruction reaches a model with excessive functionality (more attack surface)
- The injected instruction executes with excessive permissions (larger blast radius)
- The injected instruction proceeds without human confirmation (no circuit breaker)

This is not a theoretical scenario. Real-world attacks have demonstrated: MCP tool poisoning where legitimate interfaces hide malicious directives; "Claudy Day" (March 2026) where invisible HTML tags enabled data exfiltration through permitted APIs; Invariant Labs' demonstration of a malicious MCP server silently exfiltrating a user's entire WhatsApp history.

## Least Privilege as Last Defense

When injection prevention fails (and evidence suggests it will sometimes fail), least privilege determines what the attacker can do. Mitigations:

- **Minimize functionality**: remove tools and extensions not required for current tasks; clean up development-phase permissions before production
- **Scope permissions to user's own level**: agents should not have access beyond what the human operator has
- **Require confirmation for irreversible operations**: emails, deployments, deletions, payments
- **Action sandboxing**: execute all tools in constrained containers with minimal granted permissions
- **Per-user rate limits**: slow iterative probe attacks

The "lethal trifecta" producing critical risk: access to private data + exposure to untrusted content + ability to communicate externally. Any two of the three is manageable; all three together with insufficient permission scoping creates catastrophic exposure.

## Industry Maturity Note

"The industry is quite literally where web security was in 2004. There is no equivalent to SAMM for AI agents, and organisations have no standardised way to assess or benchmark their agent security practices." Expect the OWASP LLM framework to evolve rapidly as attack patterns are documented.

## Takeaway

Design coding agents assuming injection will sometimes succeed. The question is not "will injection happen?" but "what can injection do?" Minimize functionality and permissions before deployment. Require confirmation for irreversible operations. Treat least privilege not as a courtesy but as the primary damage-containment mechanism.
