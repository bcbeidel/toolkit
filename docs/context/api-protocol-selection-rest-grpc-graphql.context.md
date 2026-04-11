---
name: API Protocol Selection — REST, gRPC, GraphQL
description: REST is the default for public APIs; gRPC for internal service communication; GraphQL only where UI teams need flexible projections — each additional protocol adds real operational cost.
type: context
sources:
  - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
  - https://dasroot.net/posts/2026/04/graphql-vs-rest-vs-grpc-api-architecture-comparison-2026/
  - https://markaicode.com/grpc-vs-rest-benchmarks-2025/
  - https://trpc.io/
  - https://betterstack.com/community/guides/scaling-nodejs/trpc-explained/
  - https://www.openapis.org/
related:
  - docs/context/api-backwards-compatibility-and-deprecation-protocol.context.md
  - docs/context/oauth-2-1-pkce-and-rbac-abac-layering.context.md
  - docs/context/microservices-sizing-ddd-boundaries-and-default-monolith.context.md
---

# API Protocol Selection — REST, gRPC, GraphQL

REST, gRPC, and GraphQL solve different problems. Using the wrong protocol for a use case creates operational cost without architectural benefit. The 2025 consensus: REST + gRPC (internal) is the dominant hybrid pattern; GraphQL is added only where UI flexibility justifies the additional investment.

## REST: Default for Public APIs

REST is the baseline for any externally-consumed API. Its advantages are universal tooling, HTTP caching support, and the mature OpenAPI 3.1 ecosystem. No credible 2025 alternative challenges REST's dominance for public APIs.

Canonical design rules (Microsoft Azure Architecture Center):
- Noun-based resource URIs, not verb-based (`/orders`, not `/create-order`)
- Plural collections (`/customers`, `/customers/5`)
- HTTP verb semantics: GET (idempotent), POST (create), PUT (full replace), PATCH (partial update), DELETE
- Standard status codes: 201+Location on create, 204 for empty, 404 for not found, 400 for validation
- OpenAPI 3.1 as the contract format; contract-first approach (spec before code) enables parallel frontend/backend development

**Use REST when:** building public or external APIs, clients are heterogeneous (browsers, mobile, third parties), or HTTP caching and ecosystem breadth matter.

## gRPC: Default for Internal Services

gRPC (HTTP/2 + Protocol Buffers) is significantly faster than REST+JSON for internal service-to-service communication. The performance advantage comes from smaller binary payloads, HTTP/2 connection multiplexing, and native streaming. Specific benchmark multipliers (5–10x throughput) from T5 sources have methodology concerns — the directional advantage is real and well-established, but precise figures are workload-dependent.

Additional gRPC benefits: strong contract enforcement via `.proto` schemas, bidirectional streaming, built-in code generation across languages.

Limitations: no native browser support (requires gRPC-Web proxy), binary format complicates manual debugging, all parties must maintain `.proto` files. Note: gRPC-Web and the Connect Protocol soften the "not for public APIs" absolutism in browser-facing contexts.

**Use gRPC when:** latency-sensitive internal service-to-service calls, high-throughput data pipelines, or real-time streaming between services under your control.

## GraphQL: Only for Flexible UI Projections

GraphQL eliminates over-fetching and under-fetching for applications with many surfaces needing different data shapes from the same backend. Its field-level deprecation and schema evolution avoids the REST versioning problem — a meaningful advantage for frontend-heavy teams.

Median latency overhead vs REST is small (~3ms) and accepted for the flexibility gained. GraphQL is not appropriate for inter-service calls or public APIs without controlled consumer access.

**Use GraphQL when:** frontend teams need query flexibility, multiple clients need different projections from the same backend, or bandwidth is constrained (mobile). Not for public APIs or when consumers are third parties without contractual guarantees.

## tRPC: TypeScript Monorepo Niche

tRPC provides end-to-end type safety in full-stack TypeScript monorepos (Next.js + Node.js). The constraint is absolute: TypeScript-only, tight client-server coupling, unsuitable for external APIs. The 2025 pattern is tRPC for product-facing BFFs (Backend for Frontend) + OpenAPI at gateway boundaries for external stability.

## The Operational Cost Ceiling

Each additional protocol in a stack adds tooling investment, training burden, and debugging complexity. REST + gRPC is the dominant baseline. GraphQL is added when UI flexibility genuinely demands it — not as a default alongside REST. The hybrid approach has a ceiling; teams that add all three without clear justification pay operational cost without proportional benefit.

## Takeaway

Start with REST for public-facing APIs and gRPC for internal service communication. Add GraphQL only when UI teams have a demonstrable need for flexible projections that REST cannot serve. Treat each protocol addition as a cost-benefit decision, not a default.
