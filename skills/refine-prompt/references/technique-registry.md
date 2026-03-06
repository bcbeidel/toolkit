# Technique Registry

7 techniques in Pareto priority order. Walk this list top-to-bottom during
Stage 2 (Refine). For each technique, check the **when-to-apply** condition.
If met, apply. If not, skip.

**Key principle:** Apply only techniques whose conditions are clearly met.
More techniques does not mean a better prompt.

---

## 1. Clarity Rewrite

**Impact:** HIGH
**When to apply:** Clarity score < 5 (intentionally broad — even prompts
scoring 4 benefit from minor directness improvements)
**When to skip:** Clarity already 5/5

Rewrite for directness and specificity:
- Replace vague verbs ("handle", "process", "manage") with specific actions
- Define ambiguous terms inline
- Remove hedging language ("try to", "maybe", "if possible")
- Use second person ("You are..." / "Your task is...")

**Evidence:** Bsharat et al. "Principled Instructions Are All You Need"
(arXiv:2312.16171) — 26 principles for prompting, +57% accuracy on LLaMA-2,
+67% on GPT-4.

---

## 2. Structured Sectioning

**Impact:** HIGH
**When to apply:** Multi-section prompt OR prompt has 3+ distinct components
(context, task, format, constraints, examples)
**When to skip:** Single-purpose prompt under ~50 words

Wrap distinct sections in XML tags:
- `<context>` for background information
- `<task>` for the main instruction
- `<output_format>` for expected output structure
- `<constraints>` for rules and limitations
- `<examples>` for few-shot examples

Use descriptive tag names. Nest when hierarchy is natural.

**Evidence:** Anthropic Tier 1 documentation — XML tags provide up to 40%
quality improvement on complex prompts. Claude uses tags as parsing boundaries.

**Format selection by target model:**

| Target model | Recommended format | Rationale |
|-------------|-------------------|-----------|
| Claude (Anthropic) | XML tags | Trained on XML as parsing boundaries; up to 40% quality gain |
| GPT (OpenAI) | Markdown headers | OpenAI recommends Markdown; XML acceptable; JSON poor for docs |
| Gemini (Google) | XML or Markdown | Format-agnostic; consistency within prompt matters most |
| Llama (Meta) | Markdown + XML | Hybrid approach per Meta docs; minimal format sensitivity |
| Multi-model / unknown | Markdown headers | Broadest compatibility; XML underperforms on non-Claude models |

When the target model is not specified, default to Markdown headers for
broadest compatibility. Note the format choice and rationale in the change
log.

**Research:** [LLM Format Preferences](../../../docs/research/2026-03-05-llm-format-preferences.md)

---

## 3. Completeness Fill

**Impact:** MEDIUM
**When to apply:** Missing any of: output format specification, success
criteria, or edge case handling
**When to skip:** All three are present

Add the missing elements:
- **Output format:** What shape should the response take? (list, table,
  prose, code, JSON)
- **Success criteria:** How will the user judge if the output is good?
- **Edge cases:** What should happen with unusual inputs? (empty, too large,
  malformed)

Only add what's missing. Don't over-specify what's already clear from context.

**Evidence:** Anthropic Tier 1 documentation — "Be explicit about what you
want. Claude works best when instructions are specific rather than implicit."

---

## 4. Prompt Repetition

**Impact:** HIGH (conditional)
**When to apply:** Non-reasoning context AND the prompt contains a critical
instruction that must not be ignored (e.g., format constraints, safety rules)
**When to skip:** Reasoning/thinking tasks, short prompts, or when the
critical instruction is already emphasized

Repeat the most important instruction at both the beginning and end of the
prompt. Use slight rephrasing to avoid appearing redundant.

**Evidence:** Leviathan et al. "Repeat After Me" (Google Research, Dec 2025)
— won 47/70 benchmarks, lost 0. Addresses lost-in-the-middle attention
patterns.

---

## 5. Few-Shot Examples

**Impact:** MEDIUM (conditional)
**When to apply:** The prompt requires a specific output format or tone AND
will be reused (template, skill instruction, recurring task)
**When to skip:** One-off tasks, obvious format, or when examples would make
the prompt too long for its purpose

Add 1-3 input/output examples that demonstrate the expected behavior. Choose
examples that cover:
- The typical case
- An edge case (if relevant)

Keep examples concise. Label clearly with "Example:" or `<example>` tags.

**Evidence:** Anthropic Tier 1 documentation — "Examples are the single most
reliable way to steer Claude's output format and style."

---

## 6. Self-Check Instruction

**Impact:** LOW (conditional)
**When to apply:** The output is objectively verifiable (code that should
compile, math that should be correct, facts that can be checked)
**When to skip:** Creative tasks, subjective outputs, or tasks where
self-checking would add unhelpful second-guessing

Add an instruction to verify the output before presenting it:
- "Before responding, verify that [specific check]"
- "Double-check that [constraint] is satisfied"

Be specific about what to check. Generic "review your work" adds nothing.

**Evidence:** Schulhoff et al. "The Prompt Report" (arXiv:2406.06608) —
TACL survey finds self-check works only with specific, verifiable criteria.

---

## 7. Role Assignment

**Impact:** LOW
**When to apply:** The task requires specialized domain knowledge (legal,
medical, security, specific framework expertise)
**When to skip:** General-purpose tasks, tasks where domain framing would
narrow the response unhelpfully

Assign a specific role at the start of the prompt:
- "You are a senior security engineer reviewing..."
- "You are a database performance specialist..."

Use roles that invoke specific expertise, not generic authority ("You are an
expert" adds nothing).

**Evidence:** Anthropic Tier 1 documentation — "Even a single sentence of
role context makes a measurable difference on domain-specific tasks."

