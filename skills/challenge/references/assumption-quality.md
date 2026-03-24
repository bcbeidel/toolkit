# Assumption Quality Guide

## What Makes a Good Assumption

A well-stated assumption is:

1. **Testable** — Can be checked against evidence. "We use OAuth" is testable.
   "The auth is fine" is not.
2. **Specific** — Names concrete things. "Rate limits are 500 req/min" is
   specific. "There are rate limits" is vague.
3. **Non-trivial** — Worth checking. "The code is written in Python" is
   trivially verifiable from the codebase. "Users will authenticate via
   OAuth 2.0 with PKCE" carries real design implications.
4. **Falsifiable** — Could be wrong. "We should use a database" is a
   recommendation, not an assumption. "The existing database supports
   JSON columns" is falsifiable.

## Common Assumption Categories

- **Architectural** — Technology choices, patterns, integration points
- **Behavioral** — How users/systems interact, expected workflows
- **Constraint** — Performance limits, compliance requirements, deadlines
- **Dependency** — What exists, what's available, what's compatible
- **Scope** — What's included/excluded, boundaries of the work

## Anti-Patterns

- **Opinions disguised as assumptions** — "React is the best framework" is
  not an assumption about the project.
- **Compound assumptions** — "Users authenticate via OAuth and sessions
  expire after 30 minutes" is two assumptions. Split them.
- **Tautologies** — "The system will work correctly" is not checkable.
- **Implementation details** — "We'll use a for loop" is too low-level to
  be worth challenging.
