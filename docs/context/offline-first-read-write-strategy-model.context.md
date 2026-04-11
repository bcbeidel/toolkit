---
name: Offline-First Read/Write Strategy Model
description: Offline-first architecture requires explicit selection of read strategy (3 options) and write strategy (2 options) — conflict resolution must be chosen explicitly, not deferred.
type: context
sources:
  - https://docs.flutter.dev/app-architecture/design-patterns/offline-first
  - https://dev.to/odunayo_dada/offline-first-mobile-app-architecture-syncing-caching-and-conflict-resolution-518n
related:
  - docs/context/mobile-framework-selection-decision-guide.context.md
  - docs/context/mobile-mvvm-mvi-clean-architecture-selection.context.md
  - docs/context/android-state-persistence-survival-matrix.context.md
---

# Offline-First Read/Write Strategy Model

Offline-first is not just a caching decision — it is an architecture decision about read behavior, write behavior, and conflict resolution. Each strategy has distinct UX and consistency tradeoffs. Conflict resolution must be chosen explicitly before implementation; it cannot be added as an afterthought without restructuring the sync layer.

## Repository as Single Source of Truth

The offline-first Repository pattern combines two data sources:
- `ApiClientService` — remote data source (REST API, GraphQL endpoint)
- `DatabaseService` — local data source (Room on Android, Core Data/SQLite on iOS, SQLite on Flutter)

The Repository is the only component consumers interact with. It arbitrates between local and remote data according to the selected strategy. Consumers never call the API or database directly.

## Three Read Strategies

**1. Local fallback (remote-first)**
Try remote first; fall back to local cache on failure. Provides current data when online; stale data when offline. Correct for: data where freshness is primary and offline access is a fallback, not a feature.

**2. Stream-based (emit local immediately, update with remote)**
Emit local data immediately to the UI, then update with remote data when available. This is the best perceived UX — no loading state on initial render. The UI may briefly show stale data, then update. Correct for: most user-facing data in apps where offline is a first-class experience.

**3. Local-only with explicit sync**
Always read from local storage; call `sync()` explicitly or on schedule. No automatic remote fetch on read. Correct for: heavily offline-first apps (field work, low-connectivity environments) where sync is a deliberate user action.

## Two Write Strategies

**1. Online-only writes**
Remote write must succeed before local data is updated. If offline, write fails immediately. Guarantees consistency; provides poor offline UX. Correct for: financial transactions, critical business records where eventual consistency is not acceptable.

**2. Offline-first writes**
Write to local storage immediately; sync to remote when connectivity is available. Best UX — no failed operations when offline. Requires conflict resolution when sync occurs. Correct for: most CRUD apps where eventual consistency is acceptable.

## Conflict Resolution (Choose Before Implementing)

Conflict resolution strategy must be selected at architecture time, not as a patch when conflicts appear:

**Last-write-wins** — simpler implementation; data loss is possible when concurrent writes conflict. Accept this tradeoff explicitly if choosing it.

**Server-authoritative with client-side optimistic updates** — client writes locally as if the write succeeded (optimistic), then reconciles with server truth on sync. Correct for: most CRUD applications. The server is the authority; client reverts if the server rejects.

**CRDTs (Conflict-free Replicated Data Types)** — mathematical guarantees of convergence without coordination for specific data types (counters, sets, sequences). Used in collaborative applications (document editing, presence). Requires deep understanding of CRDT semantics; not appropriate for business logic with domain-specific invariants (e.g., account balances).

**Operational transforms** — for ordered sequences where operation ordering matters (collaborative text editing). Complex to implement correctly; use only when CRDTs cannot express the required semantics.

## Sync Primitives

Use platform-provided sync primitives that respect battery and network constraints:
- Android: `WorkManager` with `NetworkType.CONNECTED` and optional `requiresBatteryNotLow()` constraints
- iOS: `BGProcessingTask` with `requiresNetworkConnectivity` and `requiresExternalPower` constraints

Do not use raw timers or `BroadcastReceiver` threads for background sync — they are not reliable across process death and do not respect Doze mode.

## Takeaway

Offline-first requires three explicit decisions: which read strategy, which write strategy, and which conflict resolution mechanism. Stream-based reading + offline-first writing + server-authoritative conflict resolution is the recommended default for most CRUD mobile apps. Select conflict resolution at architecture time; it shapes the entire sync layer.
