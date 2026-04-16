---
name: Pull-Based GitOps Security Model and Tool Selection
description: "Pull-based GitOps (ArgoCD/Flux) is the preferred security model — cluster credentials are never exposed to external CI pipelines; ArgoCD wins for most teams, Flux for platform engineers."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.cncf.io/blog/2025/06/09/gitops-in-2025-from-old-school-updates-to-the-modern-way/
  - https://orthogonal.info/argocd-vs-flux-secure-gitops-kubernetes-2025/
  - https://www.aviator.co/blog/choosing-between-pull-vs-push-based-gitops/
  - https://spacelift.io/blog/flux-vs-argo-cd
related:
  - docs/context/iac-tool-selection-by-team-profile.context.md
  - docs/context/iac-testing-pyramid-and-adoption-gap.context.md
  - docs/context/cloud-native-security-identity-first-shift-left-runtime.context.md
---
# Pull-Based GitOps Security Model and Tool Selection

Pull-based GitOps is preferred over push-based deployment because cluster credentials never leave the cluster. The security boundary is fundamentally different — worth understanding before choosing a GitOps tool.

## Pull vs. Push: The Security Distinction

**Push-based** (Jenkins, GitHub Actions, GitLab CI): The CI/CD pipeline holds credentials to the Kubernetes cluster and actively pushes changes. The pipeline is an external actor with privileged access to the cluster. Push-based cannot automatically detect environment drift from the desired state.

**Pull-based** (ArgoCD, Flux): An agent running inside the cluster watches Git continuously. No external system needs credentials to the cluster. The cluster is autonomous — it reconciles itself to the Git state and self-heals when drift is detected. Authorization is handled by the cluster's own RBAC, not by credentials stored in a CI system.

"When possible, the pull-based approach should be preferred as it is considered the more secure and thus better practice to implement GitOps."

The security advantage is structural, not configurational. Push-based requires trust in the security of external CI credentials; pull-based eliminates that trust requirement.

## ArgoCD vs. Flux: Use-Case Split

Both are CNCF-graduated projects (ArgoCD: December 2022; Flux: November 2022). Neither is experimental in 2025. The choice is context-dependent:

**ArgoCD wins for most teams:**
- Built-in web UI with visual application topology
- Integrated RBAC system with role-based access
- ApplicationSet controller for multi-cluster management from a single instance
- All-in-one design with lower operational overhead to get started
- Direct integration with HashiCorp Vault, AWS Secrets Manager, and other external secret stores

**Flux wins for platform engineers:**
- Modular, composable CRD-native design — lighter footprint
- Tight coupling with the Kubernetes API; no separate UI layer
- Pure Kubernetes-native RBAC (no separate auth system)
- Better image automation capabilities
- Preferred when running resource-constrained clusters
- More resilient to control-plane failures (controllers deployed per cluster)

The "ArgoCD for most teams" framing is directionally correct for enterprises and teams who prioritize onboarding speed and UI observability. It overstates consensus — the preference is use-case-driven, not universal.

## Hybrid Push+Pull Is Emerging

The push/pull dichotomy is not absolute. Hybrid approaches are increasingly common: push-based pipelines handle CI velocity (build, test, validate) and pull-based operators handle deployment and drift correction. This combines event-driven speed with self-healing safety.

## Architectural Difference

ArgoCD bundles everything into one Application manifest — simple to reason about for most cases. Flux splits concerns into two resources: a GitRepository source and a HelmRelease that references it — more composable for platform engineering use cases.

ArgoCD multi-cluster: handled from a single instance via ApplicationSet. Flux multi-cluster: requires deploying controllers in each cluster — more operational overhead but can be more resilient when the central control plane fails.

**Takeaway**: Default to pull-based GitOps. Choose ArgoCD when your team values ease of onboarding, a UI, and multi-cluster management out of the box. Choose Flux when you want modular Kubernetes-native tooling and composability over convenience.
