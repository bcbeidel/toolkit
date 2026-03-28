---
name: "Preview Before Execute"
description: "The universal safety pattern of generating a reviewable artifact between observation and mutation — drawn from infrastructure automation, Kubernetes admission control, and agent system design"
metadata:
  type: reference
  sources:
    - https://developer.hashicorp.com/terraform/cli/commands/plan
    - https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform
    - https://docs.ansible.com/projects/ansible/2.9/user_guide/playbooks_checkmode.html
    - https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/
    - https://noma.security/blog/the-risk-of-destructive-capabilities-in-agentic-ai/
    - https://cleanlab.ai/blog/ai-agent-safety/
  related:
    - docs/research/reads-vs-writes-separation.md
    - docs/context/reads-writes-separation.md
    - docs/context/human-in-the-loop-design.md
    - docs/context/idempotency-convergent-operations.md
    - docs/context/escalation-circuit-breakers.md
---

Every mature infrastructure tool enforces the same pattern: observe proposed changes, produce a reviewable artifact, require explicit approval, then mutate. This is not optional ergonomics — it is safety architecture. Agent systems that skip preview execute incorrect mutations at machine speed.

## The Pattern Across Infrastructure

Three independently developed tools converge on identical architecture:

**Terraform plan/apply.** `terraform plan` reads current state, compares against desired configuration, and produces a change set without modifying anything. `terraform apply` executes. For automation pipelines, plans are saved to files (`-out=FILE`), reviewed and approved, then applied exactly as approved. The plan file ensures that even if state drifts between planning and applying, the exact approved changes execute — no silent recomputation.

**Ansible check mode.** The `--check` flag connects to target hosts, gathers facts, evaluates conditions, and reports what would change without making modifications. Combined with `--diff`, it shows exact line-level changes. The limitation is revealing: modules that execute arbitrary commands (`shell`, `command`, `raw`) cannot support check mode because Ansible cannot predict what a shell command will do without running it. Observation requires predictability.

**Puppet noop.** Shows proposed changes before applying them, following the same pattern. The convergence across three independently developed tools is strong evidence that preview-then-execute is necessary safety architecture, not a convenience feature.

The common steps: (1) declare desired state, (2) compare desired vs. actual, (3) display the diff, (4) require explicit approval, (5) apply. Steps 1-3 are pure observation. Step 4 is the human gate. Step 5 is mutation. Conflating any step degrades safety.

## Kubernetes Admission Control

Kubernetes embodies this pattern precisely in its API request processing:

1. **Mutating admission webhooks** run first. They modify objects (inject sidecars, set defaults, add labels). They run sequentially — each sees the output of the previous one.
2. **Validating admission webhooks** run second. They inspect the final object and can only accept or reject — no modification. They run in parallel.

The ordering is deliberate: validators see the object in its final form, after all mutations. If validation ran before mutation, policies would enforce against a state that does not match what gets stored. This is CQS applied to a request pipeline — mutating webhooks are commands, validating webhooks are queries.

## Six Recurring Safety Patterns

Across every domain examined, six patterns recur:

1. **Preview before execute.** A human-reviewable artifact between observation and mutation (Terraform plan files, Ansible diff output, git diff before commit).

2. **Read-only by default.** Write access is an explicit, audited escalation from the default observation mode.

3. **Separate the models.** Different concerns use different interfaces optimized for their respective purposes (CQRS read/write models, validating vs. mutating webhooks).

4. **Validate the final state.** Policy enforcement targets the state as it will actually exist, not a pre-mutation projection (Kubernetes validates after mutation, Terraform validates plans against policy before apply).

5. **Make trade-offs explicit.** Database replication lag is monitored. Terraform plan files capture point-in-time snapshots. CQRS eventual consistency is an architectural choice. Silent trade-offs — an agent acting on stale state without awareness — are the dangerous case.

6. **Idempotent observation, gated mutation.** Observation operations should be safe to run any number of times. Mutation operations require explicit gates (approval workflows, plan files, elevated permissions).

## Applying to Agent Systems

Agent systems need the equivalent of a plan file — a structured "here is what I intend to do" artifact that humans or policy engines can approve or reject. The implementation priorities:

- Separate read-only tools (observe, diagnose, analyze) from write tools (modify, create, delete) at the API level.
- Generate a reviewable diff or change summary before any write operation.
- Gate mutations on consequence magnitude — low-risk, reversible operations can auto-approve; high-risk, irreversible operations require human review.
- Bind plans to state snapshots so drift between observation and mutation is detectable.

The speed of agents makes this more important, not less. Humans naturally preview because they are slow. Agents that skip preview execute at machine speed without the built-in pause that human cognition provides.
