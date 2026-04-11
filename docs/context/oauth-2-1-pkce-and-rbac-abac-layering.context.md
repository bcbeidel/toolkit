---
name: "OAuth 2.1, PKCE, and RBAC/ABAC Layering"
description: OAuth 2.1 requires PKCE for all Authorization Code flows and deprecates Implicit and Password grants; use RBAC at the gateway for coarse checks and ABAC at the resource level for fine-grained policy.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://datatracker.ietf.org/doc/rfc9700/
  - https://microservices.io/post/architecture/2025/04/25/microservices-authn-authz-part-1-introduction.html
  - https://www.osohq.com/learn/rbac-vs-abac
related:
  - docs/context/api-protocol-selection-rest-grpc-graphql.context.md
  - docs/context/api-backwards-compatibility-and-deprecation-protocol.context.md
  - docs/context/microservices-sizing-ddd-boundaries-and-default-monolith.context.md
---
# OAuth 2.1, PKCE, and RBAC/ABAC Layering

RFC 9700 (IETF, 2025) formalizes current OAuth security best practices. PKCE is now required for all Authorization Code flows. The Implicit and Password grant flows are deprecated entirely. Access tokens should expire in 15 minutes or less.

## OAuth 2.1 / RFC 9700 Requirements

**PKCE (Proof Key for Code Exchange)** is required for public clients and recommended for confidential clients in Authorization Code flows. PKCE prevents authorization code injection attacks by binding the code challenge to the client that initiated the request. There is no longer a class of "public clients only" exemption.

**Deprecated grant flows:**
- Implicit grant: deprecated due to access token leakage risk in URL fragments
- Resource Owner Password Credentials: deprecated because it exposes user credentials directly to the client application

**Additional normative requirements:**
- Redirect URI validation: exact string matching required; no wildcards
- Sender-constrained tokens: use mutual TLS (mTLS) or DPoP to bind tokens to clients, preventing stolen token replay
- State parameter: required in all OAuth transactions for CSRF protection

## JWT Token Hygiene

- Access tokens: ≤15 minute expiry is the standard
- Include claims: `iss`, `aud`, `jti`, `iat`, `nbf`, `exp`
- Signing: asymmetric (RS256 or ES256) in multi-service environments — services verify tokens without sharing secrets
- Storage for web clients: HttpOnly, Secure, SameSite cookies — never localStorage (XSS-vulnerable)
- Refresh token rotation: required to limit refresh token lifetime exposure

## Authentication in Microservices: BFF Pattern

The Backend for Frontend (BFF) pattern handles authentication at the edge. The BFF terminates user sessions after login, issues JWTs for downstream services, and prevents services from sharing a session store. Services verify tokens directly (stateless). User identity does not propagate automatically — the BFF must explicitly pass it downstream.

At larger scale, service mesh (Istio, Linkerd) provides mutual TLS between internal services as an alternative to per-service token propagation.

## RBAC + ABAC: The Authorization Layering Pattern

Neither RBAC nor ABAC alone serves production authorization requirements. The recommended pattern layers both:

**RBAC (Role-Based Access Control) at the gateway:**
- Groups permissions into roles (Admin, Editor, Viewer)
- Simple to implement and audit for stable organizational structures
- Appropriate for coarse-grained checks: is this user authenticated? does their role permit this endpoint category?
- Suffers "role explosion" at scale as organizational edge cases multiply

**ABAC (Attribute-Based Access Control) at the resource level:**
- Access decisions based on attributes: user attributes, resource attributes, environmental context (time, location, IP)
- Enables fine-grained dynamic policies: "can edit if user is author AND document is in draft state"
- Required under HIPAA/GDPR compliance scenarios where access must be contextual, not just role-based
- Use Policy as Code (Open Policy Agent, AWS Cedar) to manage ABAC complexity

**For relationship-heavy access control** (collaborative features, shared documents): ReBAC (Relationship-Based Access Control) — the Zanzibar/Google Docs model — is appropriate. Access is determined by explicit user-to-resource relationship graphs rather than static roles or attribute evaluations.

Authorization logic fragments over time when left in individual services. Centralizing policy definitions with a policy engine reduces drift and enables auditing.

## Takeaway

OAuth 2.1 / RFC 9700 is the current normative baseline — PKCE required, Implicit and Password deprecated, tokens ≤15 min, sender-constrained tokens recommended. Layer authorization: RBAC at the gateway for coarse endpoint-level checks, ABAC at the resource level for context-sensitive policy decisions. Centralize policy definitions to prevent fragmentation across services.
