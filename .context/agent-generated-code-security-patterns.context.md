---
name: Agent-Generated Code Security Patterns
description: "LLM-generated code has 12–65% vulnerability rates — secure-by-default prompting, supply chain verification, and layered sandboxing are the three primary defensive patterns."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.emergentmind.com/topics/security-of-llm-generated-code
  - https://socket.dev/blog/slopsquatting-how-ai-hallucinations-are-fueling-a-new-class-of-supply-chain-attacks
  - https://safedep.io/ai-native-sdlc-supply-chain-threat-model/
  - https://www.sonarsource.com/resources/library/owasp-llm-code-generation/
  - https://www.innoq.com/en/blog/2025/12/dev-sandbox/
  - https://amirmalik.net/2025/03/07/code-sandboxes-for-llm-ai-agents
related:
  - docs/context/coding-agent-compound-risk-injection-plus-agency.context.md
  - docs/context/prompt-injection-architectural-defense-patterns.context.md
  - docs/context/ci-validation-for-llm-generated-code.context.md
  - docs/context/llm-agent-sdl-maturity-and-best-practice-composite.context.md
---
# Agent-Generated Code Security Patterns

## Key Insight

LLM-generated code has 12–65% non-compliance rates with basic secure coding standards. GPT-4o achieved 90.7% functional correctness but only 65.3% secure-functional correctness — a 25% gap between code that works and code that works securely. Three patterns address this: secure-by-default prompting, supply chain verification, and layered sandboxing.

## Pattern 1: Secure-by-Default Prompting

Security-focused instructions reduce vulnerability rates by up to 75% on specific tasks. Zero-shot security accuracy averages 37.4%; with safety instructions and few-shot examples, it can be raised by 20–25%.

**Techniques:**
- Structured reasoning prompts (GRASP) raise Security Rate from ~0.6 to ≥0.8 across tested LLMs
- ProSec secure fine-tuning achieved up to 35% vulnerability reduction with negligible utility loss
- Automated patching (FDSP) reduced residual vulnerability rate from 40.2% to 7.4% for GPT-4

Vulnerable CWE categories prevalent in LLM output: unchecked return values (CWE-252/253), buffer copy without bounds checking (CWE-120), SQL injection (CWE-89), hard-coded credentials (CWE-259/798), improper input validation (CWE-20).

## Pattern 2: Supply Chain Verification

**Slopsquatting** is the dominant supply chain attack vector: 19.7% of recommended packages across 576,000 code samples from 16 LLMs didn't exist. Open-source models hallucinated at 21.7% vs. 5.2% for commercial models. 43% of fake packages appeared consistently on every request — making them viable attack targets that can be pre-registered by attackers.

Nine supply chain threat categories for AI-native development:
- Package hallucination and slopsquatting
- Dependency confusion (agents lack knowledge distinguishing internal from public packages)
- Prompt injection via package metadata (malicious README files)
- MCP server and tool poisoning (untrusted MCP servers steering toward malicious packages)
- Compromised agent skills (26.1% of analyzed skills contained at least one vulnerability per one study; cross-reference against other findings before applying universally)

**Controls:** Socket.dev scanning for real-time threat detection; package verification before installation; LLM self-refinement to validate package existence before recommending.

## Pattern 3: Layered Sandboxing

Container isolation alone is insufficient for untrusted AI-generated code. Defense-in-depth combining OS primitives, hardware virtualization, and network segmentation is mandatory.

**Isolation technologies (in order of isolation strength):**
- Linux Containers (LXC/Docker): OS-level isolation, no performance penalty
- gVisor (User-Mode Kernel): intercepts system calls; "perfect middle ground for running untrusted code"
- Firecracker/Kata Containers (VMs): hardware virtualization; slight performance penalty
- WebAssembly/JVM: virtual stack machines; limited to compatible code

**"Lethal trifecta" — maximum risk when all three apply simultaneously:**
1. Access to private data
2. Exposure to untrusted content
3. Ability to communicate externally

Mitigation: mount only necessary project directories from host to VM; perform all Git operations on the host; provide only minimal, purpose-specific credentials (read-only tokens, never push credentials in sandbox).

## The Security-Performance Trade-off

Prompting LLMs to optimize for security degrades performance, and vice versa. CI gates for agent-generated code should evaluate all three dimensions — security, performance, and functional correctness — simultaneously rather than optimizing for any one dimension. Sequential single-dimension gates will optimize away the others.

## Takeaway

Treat agent-generated code as untrusted input: prompt for security explicitly, verify all package recommendations before installing, and execute in layered sandboxes. The 25% gap between functional and secure-functional output is not a model limitation to wait out — it is the current baseline that defensive patterns can close.
