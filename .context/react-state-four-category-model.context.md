---
name: React State Four-Category Model
description: "React state falls into four distinct categories — local UI, shared cross-component, server/remote, and URL — each with a distinct recommended tool; conflating them is the primary source of over-engineering."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://www.developerway.com/posts/react-state-management-2025
  - https://strapi.io/blog/react-and-nextjs-in-2025-modern-best-practices
  - https://makersden.io/blog/react-state-management-in-2025
related:
  - docs/context/react-server-components-adoption-scope.context.md
  - docs/context/vite-rolldown-vs-turbopack-framework-alignment.context.md
  - docs/context/design-tokens-and-headless-component-tradeoffs.context.md
---
# React State Four-Category Model

Conflating different types of state is the most common source of over-engineering in React applications. State falls into four categories with non-overlapping characteristics, and each category has an appropriate tool. Using the wrong tool for a category adds complexity without benefit.

## The Four Categories

| Category | Recommended Approach |
|----------|---------------------|
| Local UI state | `useState` / `useReducer` — no library |
| Shared cross-component state | React Context for 1–2 concerns; Zustand for larger scope |
| Server/remote state | TanStack Query or SWR |
| URL state | `useSearchParams` (React Router) or the `nuqs` library |

**Local UI state** is owned by a single component: open/closed toggles, form input values, hover states. The rule is colocation: keep state as close as possible to the component that uses it; lift only when sharing is required. No library is warranted.

**Shared cross-component state** is client-side state that multiple components read from or write to. React Context is appropriate for 1–2 concerns with low update frequency (theme, auth user, locale). Zustand is the default for broader shared client state: minimal boilerplate, hook-based API, no provider nesting required. Jotai offers fine-grained atomic reactivity for limiting re-renders. Redux Toolkit remains appropriate for large enterprise codebases with existing Redux investment and teams that need DevTools-heavy debugging workflows.

**Server/remote state** is asynchronous data fetched from an API: users, products, orders. TanStack Query handles caching, deduplication, background refetching, retries, pagination, and optimistic updates natively. It eliminates roughly 80% of traditional Redux patterns used for data fetching. SWR is a viable alternative with a significantly smaller bundle (5.3 KB vs 16.2 KB) for teams where bundle size is constrained.

**URL state** is state that should survive page reload or be shareable via URL: search query, active tab, filters, sort order. Storing this in component state creates inconsistency between what the user sees and what the URL represents. Use `useSearchParams` from React Router or the `nuqs` library for type-safe URL state management.

## The RSC Qualification

In React Server Components (RSC) architectures, server-side data fetching partially replaces the need for client-side server-state libraries. TanStack Query's own documentation notes that if you use Next.js or Remix, "you probably don't need React Query." This qualification applies when server components handle data fetching and streaming — the four-category model remains accurate for SPA and hybrid architectures.

## Common Misapplications

- Putting server/remote state in a Zustand store (replicates what TanStack Query does better)
- Using Redux for local UI state that never leaves the component
- Storing URL-representable state in component state (breaks bookmarkability)
- Using Context for high-frequency updates (causes unnecessary re-renders)

## Takeaway

Identify which category a piece of state belongs to before choosing a tool. The overhead of the wrong tool — boilerplate, mental model mismatch, unnecessary re-renders — is proportional to the mismatch between state category and tool choice.
