---
name: "Confirmation Gates Cannot Prevent Primitive Selection Errors"
description: "Why 'confirm your choice' gates structurally fail to prevent wrong primitive selection — the error class mismatch between slips and mistakes"
type: context
sources:
  - https://www.nngroup.com/articles/confirmation-dialog/
  - https://www.nngroup.com/articles/user-mistakes/
  - https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
  - https://github.com/kristw/yeoman-easily
related:
  - docs/research/2026-04-11-primitive-selection-routing.research.md
  - docs/context/skill-chain-hitl-patterns-and-cli-translation-gap.context.md
---

Confirmation gates prevent slips, not mistakes. NN/G's practitioner consensus defines slips as correct-intent, wrong-execution errors — the user knows what they want, but presses the wrong button. Mistakes are wrong-intent errors — the user's mental model is incorrect, so they form a goal that doesn't suit the situation. Primitive selection errors are mistakes: the user chooses `skill` when they need a `hook` because they don't know the difference, not because they executed their intent incorrectly. A "confirm your skill choice" gate cannot prevent this. The user will confirm `skill` confidently.

The NN/G heuristic applies directly: confirmation dialogs are effective for reversible, high-stakes slips (deleting a file, submitting a form). They are ineffective — and harmful through automation bias — when the user cannot distinguish the correct from incorrect answer. Overuse causes users to click through without reading. The gate becomes noise.

The closest pattern in agentic AI UX is the Intent Preview (plan summary before action) described in the Smashing Magazine 2026 agentic UX patterns article. It is designed to prevent agent execution errors, not primitive selection errors: the user has already selected their action, and the gate shows them what will happen before it does. The article's >85% acceptance rate is a design target, not an empirical finding — the article explicitly calls it a representative benchmark, not a validated result from a controlled study.

No production framework implements a semantic "justify your primitive choice" gate at creation time. After surveying 14 frameworks, the only gate-like patterns found were:

- **Yeoman `confirmBeforeStart`**: the `yeoman-easily` library provides an opt-in pre-generation confirmation gate. This is a third-party helper, not a Yeoman platform default. It demonstrates technical feasibility, not ecosystem adoption.
- **Rails 7 generator validation**: raises an error if an attribute type is invalid (e.g., `reference` vs `references`). This is a type-form gate — it catches typos, not semantic mismatches.
- **JetBrains "alternative solutions" link**: a pre-selection redirect, but passive — a documentation link, not an interactive gate.

The absence is explained by the error class mismatch, not by a gap waiting to be filled. Designing a gate for this problem would require the system to know the user's intent better than the user does — at which point the gate itself is the routing mechanism, not a confirmation layer on top of one.

AWS CLI preview-before-commit (showing the resulting CloudFormation template before execution) is the strongest gate analog found. It prevents correct-intent slips — the user sees what their correct choices will produce — not wrong-intent mistakes.

**Takeaway:** If a user doesn't know whether they need a skill or a hook, asking them to confirm their skill choice will not prevent the error. The intervention must operate earlier, at routing, not confirmation.
