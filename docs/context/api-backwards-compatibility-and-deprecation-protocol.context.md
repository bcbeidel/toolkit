---
name: API Backwards Compatibility and Deprecation Protocol
description: Backwards compatibility is a hard API design constraint — extend, never break; announce deprecations 6–12 months ahead using machine-readable Deprecation and Sunset headers.
type: context
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
  - https://stripe.com/blog/api-versioning
  - https://zuplo.com/blog/2025/04/11/api-versioning-backward-compatibility-best-practices
  - https://www.gravitee.io/blog/api-versioning-best-practices
related:
  - docs/context/api-protocol-selection-rest-grpc-graphql.context.md
  - docs/context/oauth-2-1-pkce-and-rbac-abac-layering.context.md
  - docs/context/schema-evolution-expand-contract-pattern.context.md
---

# API Backwards Compatibility and Deprecation Protocol

Backwards compatibility is a first-class API design constraint, not an afterthought. The cost of a breaking change — client breakage, migration effort, trust erosion — far exceeds the cost of early design iteration. The rule: extend, never break. When breaking is unavoidable, announce 6–12 months ahead with machine-readable signals.

## The Extend-Never-Break Rule

Every change to a public API must preserve existing behavior:
- Add optional fields and new endpoints; never remove or rename existing ones
- Never change the semantic meaning of an existing field (even if the new meaning seems equivalent)
- Create new endpoints for new semantics rather than modifying existing ones
- Use feature flags for gradual rollouts without version proliferation

When a field must be removed, deprecate it: document the replacement, add the `Deprecation` header, run both old and new in parallel during the transition window. Only remove after the transition period ends.

## Versioning Strategies

| Strategy | Approach | Best For |
|----------|----------|----------|
| URI versioning | `/v1/resources` | Public APIs — cacheable, routeable, legible |
| Custom header | `API-Version: 1` | Enterprise/internal APIs — keeps URLs clean |
| Query parameter | `?version=1.0` | Testing convenience; less REST-aligned |
| Date-based (Stripe model) | `Stripe-Version: 2024-10-01` | APIs with frequent incremental changes |

URI versioning is the standard for public APIs. Never serve a default version when the version parameter is omitted — require clients to specify it explicitly. Serving a default silently upgrades clients to new behavior they didn't opt into.

**Semantic versioning applied to API changes:**
- MAJOR: breaking changes (remove fields, change semantics)
- MINOR: additive non-breaking changes (new optional fields, new endpoints)
- PATCH: bug fixes without interface changes

## Deprecation Protocol

Deprecation is not an event — it is a process with a defined timeline:
1. **Announce 6–12 months in advance.** Clients operating in production pipelines need time to migrate; shorter windows cause breakage.
2. **Add RFC 8594 `Deprecation` and `Sunset` response headers** to all deprecated endpoint responses. These are machine-readable: client tooling, API gateways, and monitoring systems can detect and alert on them.
3. **Add a `Link` header** pointing to the successor endpoint or documentation.
4. **Provide migration guides** alongside the deprecation notice — clients should know what to do, not just that something is changing.
5. **Run both versions in parallel** throughout the transition window. Remove the deprecated endpoint only after the Sunset date.

Implement deprecation headers as a reusable gateway-level policy, not per-endpoint boilerplate.

## Stripe as a Production Reference

Stripe has maintained compatibility with every API version since 2011. Their architecture uses "version change modules": self-contained transformation functions that encapsulate backwards-incompatible changes, applied in reverse chronological order during response generation. Old behavior is isolated in modules, not scattered throughout the codebase — this gives fixed-cost maintenance rather than exponentially growing compatibility shims.

The lesson: long-term compatibility maintenance is achievable at scale with the right internal architecture, but it requires deliberate design from the beginning.

## Takeaway

Design APIs right the first time. The cost of a backward-incompatible change compounds over the API's lifetime. When changes are unavoidable, follow the extend-never-break principle, version explicitly, deprecate with 6–12 months notice and machine-readable headers, and run both versions in parallel during the transition. Treat backwards compatibility as an engineering constraint, not a courtesy.
