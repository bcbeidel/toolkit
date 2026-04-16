---
name: How Asyncio Handles Concurrency in Python
description: Technical investigation of asyncio's concurrency model, event loop, and primitives
type: research
sources:
  - https://docs.python.org/3/library/asyncio.html
  - https://realpython.com/async-io-python/
---

## Summary

Asyncio uses a single-threaded event loop with cooperative multitasking.
Tasks yield control at `await` points. The primary primitives are coroutines,
tasks, and synchronization objects (locks, events, conditions, semaphores).

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://docs.python.org/3/library/asyncio.html | asyncio — Asynchronous I/O | Python Software Foundation | 2024 | T1 | verified |
| 2 | https://realpython.com/async-io-python/ | Async IO in Python | Real Python | 2023 | T3 | verified |

## Findings

### How does the event loop manage tasks?

Asyncio uses a single-threaded event loop with cooperative multitasking [1][2].
Tasks yield control at `await` points, allowing other tasks to run (HIGH —
T1 + T3 sources converge).

### What are the concurrency primitives?

The primary primitives are coroutines (`async def`), tasks (`asyncio.create_task`),
and futures (MODERATE — T3 source only for full taxonomy). Synchronization uses
locks, events, conditions, and semaphores [1] (HIGH).

## Challenge

### Assumptions Check

| Assumption | Evidence For | Evidence Against | Status |
|-----------|-------------|-----------------|--------|
| asyncio is single-threaded | T1 docs confirm event loop is single-threaded | run_in_executor uses threads | Qualified |

## Claims

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "single-threaded event loop" | attribution | [1] | verified |
| 2 | "tasks yield control at await points" | attribution | [1][2] | verified |
| 3 | "locks, events, conditions, and semaphores" | quote | [1] | verified |
| 4 | "coroutines, tasks, and futures" | attribution | [2] | corrected (futures are low-level, not primary) |

## Key Takeaways

- Asyncio is single-threaded by design; concurrency comes from cooperative yielding
- Use `run_in_executor` for CPU-bound work that would block the loop
- Synchronization primitives mirror threading but are coroutine-safe
