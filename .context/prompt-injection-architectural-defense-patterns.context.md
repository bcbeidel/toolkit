---
name: Prompt Injection Architectural Defense Patterns
description: "Prompt injection is inevitable at the model level — effective defense requires architectural control/data separation via Dual LLM, Plan-Then-Execute, and Context-Minimization patterns."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html
  - https://github.com/tldrsec/prompt-injection-defenses
  - https://www.anthropic.com/research/prompt-injection-defenses
  - https://labs.reversec.com/posts/2025/08/design-patterns-to-secure-llm-agents-in-action
related:
  - docs/context/coding-agent-compound-risk-injection-plus-agency.context.md
  - docs/context/agent-generated-code-security-patterns.context.md
  - docs/context/mcp-security-annotations-and-limitations.context.md
  - docs/context/llm-context-credential-leakage-and-sanitization.context.md
---
# Prompt Injection Architectural Defense Patterns

## Key Insight

Model-level defenses against prompt injection are insufficient — Anthropic's best-in-class effort reduced attacks to 1%, which "still represents meaningful risk." No browser agent is immune. The only reliable defense is architectural: separate control flow from untrusted data flow before the LLM processes either. Three architectural patterns achieve this.

## The Root Cause

"The root causes of indirect prompt injection attacks are twofold: the inability of LLMs to effectively differentiate between informational context and actionable instructions, and the lack of awareness in LLMs to avoid executing instructions embedded in content."

Attack variants include: encoding obfuscation (Base64, Unicode), typoglycemia (scrambled words), HTML/Markdown injection, multi-turn attacks, RAG poisoning (five carefully crafted documents can manipulate AI responses 90% of the time), and MCP tool poisoning (hidden directives in tool documentation).

Research evaluated eight defenses and bypassed all of them using adaptive attacks at >50% success rate. Instructional defenses alone are not a security boundary.

## Pattern 1: Dual LLM

Separate privileged orchestrator from quarantined processor. The quarantined model handles untrusted external content with no tool access. Results from the quarantined model are stored as symbolic references (e.g., `$abc123`). The privileged orchestrator manipulates variables without dereferencing actual content.

Effect: the privileged model never sees the injected content; it only sees symbolic pointers to outputs. An injection in external content can corrupt the data but cannot reach the control flow.

## Pattern 2: Plan-Then-Execute

The LLM creates an immutable action plan upfront. A non-LLM orchestrator supervises execution of the plan. "An injection can corrupt data flowing between steps but cannot alter the control flow." The plan is locked before any untrusted content is processed.

This pattern is architecturally compatible with human-in-the-loop: the plan can be reviewed and approved before execution begins, providing a natural oversight gate.

## Pattern 3: Context-Minimization

Two-phase processing: a Request Parser extracts intent into structured data; a Response Generator receives only the trusted extracted content. "The original malicious prompt is discarded." The generator never sees the raw untrusted input.

Related: LLM Map-Reduce isolates each document in its own LLM call forced into a strict JSON schema. Schema validation catches injections that produce invalid JSON. This is particularly effective for batch document processing.

## Layered Defense Stack

No single architectural pattern eliminates all injection risk. Effective programs combine:
1. Architectural control/data separation (Dual LLM, Plan-Then-Execute, or Context-Minimization)
2. Input pre-processing (paraphrasing, retokenization)
3. Blast radius reduction (least-privilege access, assume compromise will occur)
4. Output monitoring (validate for prompt leakage, API key exposure)
5. Human-in-the-loop for high-risk operations

The ordering matters: architecture first, then monitoring, then instructs. Relying primarily on instructional defenses while omitting architectural separation creates a defense-in-depth gap.

## Anthropic's Empirical Results

Three defense layers: (1) RL training exposing Claude to injections in simulated web content; (2) improved classifiers detecting adversarial commands in hidden text and manipulated images; (3) human red teaming. Claude Opus 4.5 reduced injection success to 1% in browser-based operations.

"Despite progress, no browser agent is immune to prompt injection." The 1% success rate "still represents meaningful risk" at operational scale.

## Takeaway

Assume injection attempts will occur and will sometimes succeed at the model level. Design architectures where a successful injection cannot reach high-privilege control flow — separate the instruction-following model from untrusted content processing. Dual LLM, Plan-Then-Execute, and Context-Minimization are the three evidence-backed architectural patterns.
