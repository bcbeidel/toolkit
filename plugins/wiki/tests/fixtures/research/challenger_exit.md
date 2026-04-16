---
name: Test Research — Challenger Exit
description: Fixture representing state after challenger completes
type: research
sources:
  - https://docs.python.org/3/library/asyncio.html
  - https://realpython.com/async-io-python/
---

<!-- DRAFT -->

## Research Brief

**Question:** How does asyncio handle concurrency in Python?

**Mode:** technical
**SIFT Rigor:** High

### Sub-questions

1. How does the event loop manage tasks?
2. What are the concurrency primitives?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://docs.python.org/3/library/asyncio.html | asyncio — Asynchronous I/O | Python Software Foundation | 2024 | T1 | verified |
| 2 | https://realpython.com/async-io-python/ | Async IO in Python | Real Python | 2023 | T3 | verified |

### How does the event loop manage tasks?

> The event loop is the core of every asyncio application. Event loops run
> asynchronous tasks and callbacks, perform network IO operations, and run
> subprocesses. — Python docs

> asyncio uses cooperative multitasking: tasks voluntarily yield control at
> await points, allowing other tasks to run. — Real Python

### What are the concurrency primitives?

> asyncio provides locks, events, conditions, and semaphores as
> synchronization primitives. — Python docs

> The key primitives are coroutines (async def), tasks (asyncio.create_task),
> and futures (low-level). — Real Python

## Challenge

### Assumptions Check

| Assumption | Evidence For | Evidence Against | Status |
|-----------|-------------|-----------------|--------|
| asyncio is single-threaded | T1 docs confirm event loop is single-threaded | run_in_executor uses threads | Qualified |

### Premortem

| Failure Reason | Plausibility | Impact on Conclusion |
|----------------|-------------|---------------------|
| Overlooking multi-process use cases | medium | Qualifies finding about single-threaded nature |
