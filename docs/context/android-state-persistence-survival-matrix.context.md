---
name: Android State Persistence Survival Matrix
description: Android's onDestroy() is not called when the OS kills cached processes — use SavedStateHandle + WorkManager + DataStore for reliable state survival across process death.
type: concept
confidence: medium
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://developer.android.com/guide/components/activities/process-lifecycle
related:
  - docs/context/mobile-framework-selection-decision-guide.context.md
  - docs/context/mobile-mvvm-mvi-clean-architecture-selection.context.md
  - docs/context/offline-first-read-write-strategy-model.context.md
---
# Android State Persistence Survival Matrix

The most common Android state persistence mistake is relying on `onDestroy()` for critical state. The Android OS kills cached processes without calling `onDestroy()`. Understanding what survives which type of process end is required to build reliable Android apps.

## Why onDestroy() Is Unreliable

The Android process priority ladder, from highest to lowest:
1. **Foreground process** — active Activity or bound Service in foreground
2. **Visible process** — Activity visible but not focused
3. **Service process** — running background Service
4. **Cached process** — stopped Activities that the system may kill freely when resources are needed

Cached processes are killed without lifecycle callbacks when the system needs memory. Starting Android 13, cached processes may receive limited execution time before being killed. `onDestroy()` is called for normal Activity finishing but is explicitly NOT guaranteed on process kill.

**Do not use `onDestroy()` for:**
- Critical state persistence (user-entered data, business logic state)
- Cleanup of persistent resources (database connections, file handles)
- Background work initiation

## Survival Matrix

| State Type | Mechanism | Survives Config Change | Survives Process Death |
|------------|-----------|----------------------|----------------------|
| ViewModel state | `ViewModel` alone | Yes | No |
| UI + process-safe state | `SavedStateHandle` in ViewModel | Yes | Yes |
| User preferences | `DataStore` | Yes | Yes |
| Persistent app data | `Room` database | Yes | Yes |
| Background task execution | `WorkManager` | Yes | Yes |

**`SavedStateHandle`** is the correct mechanism for transient UI state that must survive process death. It integrates with ViewModel and is accessible via `viewModel.savedStateHandle`. Prefer it over the older `onSaveInstanceState()` bundle pattern for ViewModel-level state.

**`ViewModel` alone** survives configuration changes (screen rotation, multi-window resize) but is cleared when the process is killed. Use for non-critical UI state that can be re-fetched.

**`DataStore`** replaces `SharedPreferences` as the persistent key-value store for user preferences and small datasets. Unlike `SharedPreferences`, it is safe to read and write from coroutines without blocking the main thread.

**`WorkManager`** is the correct primitive for deferred background tasks that must complete even if the app process is killed: data synchronization, file uploads, analytics batching. It respects system battery and network constraints via `Constraints` configuration.

## Background Work Rules

- Never spawn threads in `BroadcastReceiver.onReceive()` — the process is killed when the method returns. Use `JobScheduler` or `WorkManager` instead.
- Services running more than 30 minutes are demoted from Service to Cached priority. Use `setForeground()` for long-running work to maintain foreground process priority.
- Use `WorkManager` for deferrable, guaranteed background tasks (sync, upload).
- Use `AlarmManager.setAndAllowWhileIdle()` for tasks with strict timing requirements.

## Takeaway

Build your state persistence strategy against the survival matrix, not against `onDestroy()`. `SavedStateHandle` + `WorkManager` + `DataStore` cover the three categories of state that must survive process death: transient UI state, deferred background work, and user preferences. `onDestroy()` is for cleanup on normal Activity finishing only — it is not a reliability primitive.
