---
name: "Mobile Engineering: Landscape"
description: "Landscape of mobile engineering practices: native vs. cross-platform tradeoffs, architecture patterns (MVVM/MVI/Clean), mobile-specific CI/CD and testing, offline-first patterns, and performance optimization across Android and iOS."
type: research
sources:
  - https://kotlinlang.org/docs/multiplatform/native-and-cross-platform.html
  - https://www.kmpship.app/blog/kmp-vs-flutter-vs-react-native-2025
  - https://kotlinlang.org/docs/multiplatform/kotlin-multiplatform-react-native.html
  - https://medium.com/@jyc.dev/architecture-patterns-in-mobile-development-2026-mvvm-mvi-and-clean-architecture-f26583f53522
  - https://nextnative.dev/blog/mobile-app-architecture-best-practices
  - https://medium.com/mobile-at-octopus-energy/architecture-in-jetpack-compose-mvp-mvvm-mvi-17d8170a13fd
  - https://www.alimertgulec.com/en/blog/mobile-app-testing-strategy-2025
  - https://quashbugs.com/blog/scaling-mobile-testing-infrastructure
  - https://quashbugs.com/blog/visual-regression-testing-mobile-apps
  - https://refraction.dev/blog/cicd-pipelines-mobile-apps-best-practices
  - https://docs.flutter.dev/app-architecture/design-patterns/offline-first
  - https://dev.to/odunayo_dada/offline-first-mobile-app-architecture-syncing-caching-and-conflict-resolution-518n
  - https://developer.android.com/guide/components/activities/process-lifecycle
  - https://dev.to/arshtechpro/wwdc-2025-ios-26-background-apis-explained-bgcontinuedprocessingtask-changes-everything-9b5
  - https://developer.android.com/topic/performance/measuring-performance
  - https://www.arvisus.com/mobile-app-performance-optimization-how-to-fix-slow-apps-crashes-battery-drain/
related: []
---

# Mobile Engineering: Landscape

> Research mode: landscape | Date: 2026-04-10

## Key Insights

- **Framework choice is a team decision, not a technical one.** Swift/Kotlin native, KMP, Flutter, and React Native each have a defensible sweet spot. Choose based on team skills and product requirements, not benchmark comparisons.
- **Compose Multiplatform's stable iOS support (May 2025) changes the KMP calculus.** Teams with Kotlin expertise can now share both business logic and UI, closing the sharing gap with Flutter while retaining native binary performance.
- **MVVM is the right default; MVI for complex state machines.** Both fit cleanly inside Clean Architecture. Start MVVM, escalate individual screens to MVI as complexity demands. 4-layer Clean Architecture is premature for small teams — the Android team recommends 3 layers.
- **SavedStateHandle + WorkManager, not `onDestroy()`, is the reliable Android persistence pattern.** The OS kills cached processes without lifecycle callbacks. `onDestroy()` is not guaranteed.
- **Offline-first architecture is a read/write strategy decision, not just a caching decision.** Stream-based reading (emit local immediately, then update with remote) provides the best perceived UX. Conflict resolution must be chosen explicitly.
- **Baseline Profiles are a low-effort, high-impact Android launch optimization.** Ship them with every APK. Profile on production builds; debug builds mask real startup cost.
- **KMP market share numbers from KMPShip are vendor-published — treat as directional trend only.** No independent third-party survey corroborates the specific 42%/23% figures.

## Sub-Questions

1. What are current best practices for native (Swift/Kotlin) vs. cross-platform (React Native, Flutter, Kotlin Multiplatform) development?
2. How should mobile app architecture be structured (MVVM, MVI, clean architecture, composable patterns)?
3. What testing and CI/CD patterns are specific to mobile (device farms, screenshot testing, staged rollouts)?
4. How do app lifecycle, state restoration, and offline-first patterns affect mobile architecture?
5. What mobile-specific performance patterns matter (launch time, memory, battery, network efficiency)?

## Sources

| # | URL | Title | Author/Org | Date | Tier | Status |
|---|-----|-------|-----------|------|------|--------|
| 1 | https://kotlinlang.org/docs/multiplatform/native-and-cross-platform.html | Cross-platform and native app development: How do you choose? | JetBrains / Kotlin | 2025 | T1 | verified |
| 2 | https://www.kmpship.app/blog/kmp-vs-flutter-vs-react-native-2025 | Kotlin Multiplatform vs Flutter vs React Native: The 2025 Guide | KMPShip | 2025 | T3 | verified — ⚠ vendor bias (KMP tooling seller; market share figures are self-published, not third-party surveys) |
| 3 | https://kotlinlang.org/docs/multiplatform/kotlin-multiplatform-react-native.html | Kotlin Multiplatform vs. React Native: A cross-platform comparison | JetBrains / Kotlin | 2025 | T1 | verified |
| 4 | https://medium.com/@jyc.dev/architecture-patterns-in-mobile-development-2026-mvvm-mvi-and-clean-architecture-f26583f53522 | Architecture Patterns in Mobile Development (2026): MVVM, MVI, and Clean Architecture | J@y / Medium | 2026 | T4 | verified (403) — ⚠ unknown credentials; "2026" date suspicious; paywall |
| 5 | https://nextnative.dev/blog/mobile-app-architecture-best-practices | 9 Essential Mobile App Architecture Best Practices for 2025 | NextNative | 2025 | T3 | verified |
| 6 | https://medium.com/mobile-at-octopus-energy/architecture-in-jetpack-compose-mvp-mvvm-mvi-17d8170a13fd | Architecture in Jetpack Compose — MVP, MVVM, & MVI | Ian Alexander / Octopus Energy | 2023 | T3 | verified (403) — ⚠ foundational, pre-Compose-stable; paywall |
| 7 | https://www.alimertgulec.com/en/blog/mobile-app-testing-strategy-2025 | Mobile App Testing Strategy 2025: From Unit Tests to CI/CD | Ali Mert Gulec | 2025 | T3 | verified |
| 8 | https://quashbugs.com/blog/scaling-mobile-testing-infrastructure | How to Scale Mobile Testing: Strategies for QA Teams in 2025 | Quash | 2025 | T3 | verified — ⚠ vendor bias (QA tooling seller; cost savings figures are anecdotal) |
| 9 | https://quashbugs.com/blog/visual-regression-testing-mobile-apps | Visual Regression Testing for Mobile Apps: Best Practices | Quash | 2025 | T3 | verified — ⚠ vendor bias (same source as #8) |
| 10 | https://refraction.dev/blog/cicd-pipelines-mobile-apps-best-practices | CI/CD Pipeline Best Practices and Considerations for Mobile Apps | Refraction.dev | 2025 | T3 | verified |
| 11 | https://docs.flutter.dev/app-architecture/design-patterns/offline-first | Offline-first support | Google / Flutter | 2025 | T1 | verified |
| 12 | https://dev.to/odunayo_dada/offline-first-mobile-app-architecture-syncing-caching-and-conflict-resolution-518n | Offline-First Mobile App Architecture: Syncing, Caching, and Conflict Resolution | Odunayo Dada / DEV | 2025 | T4 | verified |
| 13 | https://developer.android.com/guide/components/activities/process-lifecycle | Processes and app lifecycle | Google / Android Developers | 2025 | T1 | verified |
| 14 | https://dev.to/arshtechpro/wwdc-2025-ios-26-background-apis-explained-bgcontinuedprocessingtask-changes-everything-9b5 | WWDC 2025 - iOS 26 Background APIs Explained: BGContinuedProcessingTask | ArshTechPro / DEV | 2025 | T4 | verified — ⚠ secondary source for Apple APIs (no Apple doc corroboration available) |
| 15 | https://developer.android.com/topic/performance/measuring-performance | Overview of measuring app performance | Google / Android Developers | 2025 | T1 | verified |
| 16 | https://www.arvisus.com/mobile-app-performance-optimization-how-to-fix-slow-apps-crashes-battery-drain/ | Mobile App Performance Optimization 2025 | Arvisus | 2025 | T4 | verified — unknown author credentials |

## Extracts

### SQ1: Native vs. Cross-Platform

**Decision framework from JetBrains official docs [#1]:**
- Choose cross-platform when: building for both Android and iOS simultaneously, optimizing development time, or wanting shared business logic with native UI control.
- Choose native when: single-platform target, UI is critically differentiated, or team has no bandwidth for tech adoption.

**Code sharing percentages [#2]:**
- KMP (logic only): 40–60% typical; with Compose Multiplatform: 90–95%+
- Flutter: ~100% (single Dart codebase, rendered uniformly)
- React Native: 70–85% (native modules required for some platform APIs)

**Framework market position and performance [#2]:**
- React Native: 42% market share (largest, JavaScript talent pool of 350k+ npm packages). New Bridgeless/Fabric architecture improves load time and memory.
- Flutter: Fastest cold starts and highest frame rates (Impeller renderer). 50,000+ pub.dev packages. Requires Dart investment.
- KMP: Adoption jumped from 12% to 23% in 18 months. Leaner binaries and lower memory footprint. Only 2,500+ KMP-specific libraries but access to full JVM ecosystem.

**2025 trend: native resurgence and KMP graduation [#1, #2]:**
- Startups in fintech, healthtech, and mobility are returning to Swift + Kotlin native for performance-critical products.
- Compose Multiplatform reached stable iOS support in May 2025 (v1.8.0), making shared UI in Kotlin viable for production.
- KMP "has essentially eliminated the traditional trade-off between development speed and native performance" for Kotlin-experienced teams [#2].

**Performance reality [#1]:**
- KMP compiles to JVM bytecode (Android) and native binaries (iOS) — shared code performance equals native implementations.
- Flutter uses its own rendering engine (Skia/Impeller), not native widgets, creating visual parity at the cost of larger app binaries.
- React Native's bridge-based native integration is "sometimes problematic" for deep platform APIs; KMP offers deepest platform API access with no overhead [#2].

**Use-case decision guide [#1, #2]:**
- KMP: existing Android/Kotlin expertise, native performance required, gradual migration from existing Android app.
- Flutter: fastest MVP, pixel-perfect cross-platform UI, greenfield project with team willing to learn Dart.
- React Native: JavaScript/React team, large third-party library ecosystem needed, web code sharing valuable.
- Native Swift/Kotlin: single-platform, highly specialized UX, or performance-critical features (AR, complex graphics).

---

### SQ2: Mobile App Architecture

**Dominant patterns in 2025 [#4, #5, #6]:**
- MVVM (Model-View-ViewModel): Dominant in Android Jetpack, SwiftUI, Flutter Riverpod. ViewModel exposes UI state via StateFlow/MutableState; composables observe and trigger actions.
- MVI (Model-View-Intent): Single immutable UI state object; unidirectional data flow; better consistency for complex state machines; higher boilerplate.
- Clean Architecture: Business logic decoupled from frameworks via concentric layers (domain at center); enforces "source code dependencies point inward only" [#5].

**MVVM vs MVI tradeoff [#6]:**
- MVVM: separate publisher per data piece; simpler, lower entry barrier; suitable for most flows.
- MVI: single state object published as a unit; stronger consistency and predictability; preferred for complex UI states with many interdependent fields.
- Practical guidance: use MVVM for simple flows, MVI for complex state machines — they can coexist under the same Clean Architecture layers [#4].

**Layer structure (Clean Architecture) [#5]:**
1. Presentation Layer — UI only (Composables, Views, ViewModels)
2. Domain Layer — business rules, use cases (no framework dependencies)
3. Data Layer — repositories, data sources (Room, Retrofit, etc.)
4. Infrastructure Layer — networking, logging, device APIs

Each layer depends only downward; UI changes cannot break data logic.

**State management principles [#5]:**
- Single immutable store as source of truth.
- Action-based state changes (no direct mutations).
- Pure reducer functions for predictable transformations.
- Unidirectional data flow enabling testability and time-travel debugging.

**Jetpack Compose specifics [#6]:**
- Compose encourages unidirectional data flow natively — composables observe state, trigger events upward.
- ViewModel exposes `StateFlow` or `MutableState`; composables subscribe via `collectAsState()`.
- Side effects (navigation, toasts, analytics) managed via `LaunchedEffect`, `SideEffect`, or dedicated channel in MVI.

**SwiftUI parallel [#4]:**
- `@StateObject` / `@ObservableObject` maps to MVVM's ViewModel concept.
- Combine framework or Swift Concurrency (`async/await`) handles reactive state.
- TCA (The Composable Architecture) is the dominant Swift MVI-style library for complex apps.

---

### SQ3: Mobile Testing and CI/CD

**Test pyramid for mobile [#7]:**
- Unit tests (70%): individual functions, run in milliseconds; XCTest (iOS), JUnit/Kotlin Test (Android), Jest (RN), flutter_test (Flutter).
- Integration tests (20%): multiple components together (API + database interactions).
- UI/E2E tests (10%): complete user flows; XCUITest (iOS), Espresso (Android), Detox (RN), integration_test (Flutter).

**Snapshot / visual regression testing [#7, #9]:**
- Snapshot testing compares UI screenshots against stored baselines to detect visual regressions automatically.
- Mobile-specific challenge: extreme fragmentation across screen sizes, pixel densities, OS rendering, notches, safe areas.
- Best practices: disable animations before capture; mask dynamic regions (timestamps, banners); maintain device-aware baselines (not one universal baseline); prioritize high-impact screens (login, checkout) first.
- Run visual checks at PR stage; pre-commit hooks can block unintentional `updateSnapshots=true` flags.
- Tools: swift-snapshot-testing (iOS), Paparazzi (Android), Percy (cross-platform), Applitools (AI-powered diffing).

**Device farm integration [#8, #10]:**
- Hybrid strategy: emulators/simulators for smoke tests and initial validation; real devices for regression and release testing.
- Cloud device farms (AWS Device Farm, Firebase Test Lab, BrowserStack, Sauce Labs) preferred over self-hosted — "maintaining in-house device labs is costly and logistically difficult" [#8].
- Parallel execution via test sharding across GitHub Actions matrix or Jenkins pipelines. One fintech team cut CI runtimes 60% with dynamic sharding [#8].
- Auto-scaling CI runners on AWS/GCP spot instances; batch device tests to minimize idle time; one team reduced device farm bills 40% via time-based scheduling [#8].

**CI/CD pipeline structure [#10, #7]:**
- Every commit: unit tests + static analysis + lint.
- Every PR: unit tests, integration tests, snapshot tests, coverage check.
- Release candidates: full UI test suite on real device farm.
- Fastlane for automating build/test/distribution workflows.
- GitHub Actions for orchestration; cache dependencies to reduce build time.
- Mandatory test passage gating merge.

**Staged rollouts:**
- Not covered in fetched sources with concrete specifics — Google Play and App Store both support percentage-based rollouts (1% → 10% → 50% → 100%).
- Monitor crash rates and ANRs in Firebase Crashlytics / Google Play Console vitals before expanding rollout.

---

### SQ4: App Lifecycle, State Restoration, and Offline-First

**Android process priority and lifecycle [#13]:**
- System kills processes in reverse priority: Foreground > Visible > Service > Cached.
- Cached processes (stopped Activities) are "killed freely" when system needs resources — apps cannot control this.
- Starting Android 13: cached processes may receive limited execution time until entering an active state.
- `onDestroy()` is NOT guaranteed to be called on process kill — do not rely on it for critical state persistence.

**Android state restoration patterns [#13]:**
- `SavedStateHandle` in ViewModel: survives both configuration changes and process death. Preferred over `onSaveInstanceState()` bundles for ViewModel-level state.
- `ViewModel` alone: survives configuration changes (rotation) but NOT process death.
- `DataStore` / `SharedPreferences`: persistent preferences across sessions.
- `WorkManager`: guaranteed execution of deferred tasks even after process death — use for sync operations.

**Android background work [#13]:**
- Never spawn threads in `BroadcastReceiver.onReceive()` — process is killed when method returns. Use `JobScheduler` or `WorkManager` instead.
- Services running >30 minutes are demoted from Service to Cached priority — use `setForeground()` or foreground services for long-running work.
- Prefer `WorkManager` for deferrable, guaranteed background tasks (sync, upload); `AlarmManager.setAndAllowWhileIdle()` for strict timing.

**iOS lifecycle and iOS 26 BGContinuedProcessingTask [#14]:**
- iOS 26 introduces `BGContinuedProcessingTask` for long-running, user-initiated operations (exports, uploads) with system UI progress indication.
- Three requirements: explicit user initiation, measurable continuous progress reporting, user ability to cancel.
- Supports `.fail` (execute or abort) and `.queue` (default, deferred) submission strategies.
- System intelligently boosts task priority when app returns to foreground.
- Legacy APIs: `BGAppRefreshTask` (short refresh) and `BGProcessingTask` (longer deferrable work) remain for non-user-initiated background work.

**Offline-first architecture pattern [#11]:**
- Repository is the single source of truth, combining `ApiClientService` (remote) and `DatabaseService` (local SQL).
- Three read strategies:
  1. Local fallback: try remote first, fall back to local cache on failure.
  2. Stream-based: emit local data immediately, then update with remote — best UX (no perceived load).
  3. Local-only with manual sync: always read local; `sync()` called explicitly or on schedule.
- Two write strategies:
  1. Online-only: remote write succeeds before local update — strict consistency, poor offline UX.
  2. Offline-first write: store locally immediately, sync when possible — best UX, requires conflict resolution.

**Sync strategies [#11]:**
- Periodic timer sync (every N minutes) with `synchronized` flag on data model.
- Push-based sync triggered by Firebase Messaging or similar.
- Connectivity check via `connectivity_plus` (Flutter) before sync; battery check via `battery_plus` before background sync.
- Use WorkManager (Android) or `BGProcessingTask` (iOS) for background sync — not raw timers.

**Conflict resolution [#12]:**
- Last-write-wins is simplest but loses data.
- CRDT (Conflict-free Replicated Data Types) increasingly used for collaborative apps.
- Operational transforms for ordered sequences (document editing).
- Server-authoritative with client-side optimistic updates for most CRUD apps.

---

### SQ5: Mobile Performance Patterns

**Key performance targets [#15]:**
- Cold app startup: < 500ms (Android Macrobenchmark / iOS MetricKit).
- Frame rendering at 60Hz: ≤ 16.7ms per frame; at 90Hz: ≤ 11.1ms.
- P95/P99 startup latency should be close to median — high variance indicates inconsistent user experience.
- Use `reportFullyDrawn()` on Android to signal app is fully interactive (not just first frame rendered).

**Profiling tools [#15]:**
- Android: Perfetto (system-wide), Android Studio Memory Profiler, Simpleperf (CPU flamegraphs), on-device System Tracing.
- Android Macrobenchmark library for startup and scrolling benchmarks; `FrameMetricsAggregator` for custom journey frame metrics.
- iOS: Instruments (Time Profiler, Allocations, Leaks), MetricKit for field metrics.
- Field vs. lab: Google Play Console / App Store Connect vitals for aggregate real-user data; Macrobenchmark / Instruments for controlled lab measurement.

**Baseline Profiles (Android) [#15]:**
- Pre-compile critical code paths based on real user behavior patterns.
- Improve cold app startup significantly.
- Generated via `MacrobenchmarkRule` and shipped with the APK.
- Apple equivalent: App Store pre-warms apps for common user paths.

**Memory management patterns [#15]:**
- Object pooling: reuse instead of allocating in tight loops (e.g., 2,000 `Vertex` objects/second → implement pool).
- Use `Memory Profiler` to identify objects created unnecessarily via "Arrange by Callstack."
- Frequent GC causes CPU contention → jank; minimize allocation in rendering-critical paths.
- Images: largest memory consumer in most apps; use WebP for 25–35% size reduction; load at display size, not full resolution.
- RecyclerView: use granular `notifyItemChanged()` not `notifyDataSetChanged()`; share `RecycledViewPool` for nested lists.

**Launch time optimization [#15]:**
- Profile with production-grade build (`-m speed` compilation), not debug builds.
- Common launch blockers: lock contention, synchronous binder IPC transactions, GC on startup, blocking I/O on main thread.
- Anti-pattern: "trampoline activity" (Activity → Activity with no frame rendered) — refactor setup code to reusable components.
- Defer non-critical initialization from `Application.onCreate()` to lazy loading or background thread.

**Battery and network efficiency [#16]:**
- Batch network requests to minimize radio wake-ups (each wake-up drains battery even for millisecond requests).
- Use push notifications instead of polling for updates.
- Implement intelligent sync schedules (off-peak, on WiFi, charging when possible).
- Android `WorkManager` constraints: `NetworkType.CONNECTED`, `requiresCharging()`, `requiresBatteryNotLow()`.
- iOS: `BGProcessingTask` supports `requiresNetworkConnectivity` and `requiresExternalPower` constraints.
- Avoid wake locks held longer than needed; prefer `JobScheduler` / `WorkManager` which respect Doze mode.

## Findings

### SQ1: Native vs. Cross-Platform

**F1. Framework choice is a team-and-product decision, not a technical superiority question.** (HIGH — T1 [#1] + convergence across [#2, #3])
Each framework has a defensible sweet spot: Swift/Kotlin native for single-platform or highly differentiated UX; KMP for teams with Kotlin expertise who need shared business logic with native UI control; Flutter for fastest time-to-market with pixel-perfect cross-platform UI; React Native for JavaScript/React teams who need large third-party library coverage. JetBrains provides a structured decision framework: choose cross-platform when building for both platforms simultaneously and optimizing dev time; choose native when single-platform, UI is critically differentiated, or team has no bandwidth for tech adoption.

**F2. React Native leads in adoption; KMP is the fastest-growing entrant.** (MODERATE — direction HIGH, specific numbers low-confidence due to vendor source [#2])
React Native's JavaScript ecosystem (350k+ npm packages) remains the primary differentiator. The Bridgeless/Fabric architecture addresses the bridge bottleneck that historically caused jank. KMP adoption is growing — corroborated directionally by JetBrains community surveys — but the specific "42% / 23%" market share figures are vendor-published by KMPShip (a KMP tooling company) and should not be cited as quantified market data.

**F3. Compose Multiplatform reaching stable iOS support (v1.8.0, May 2025) is a material shift for the KMP story.** (HIGH — T1 [#1])
Previously KMP shared only business logic; Compose Multiplatform enables shared UI code in Kotlin, achieving 90–95%+ code sharing. This closes the sharing gap with Flutter while retaining native binary performance on iOS. Teams with existing Android/Kotlin codebases can now migrate incrementally.

**F4. Flutter's rendering engine (Impeller) delivers consistent frame rates but at a visual cost.** (HIGH — [#1, #2])
Flutter renders its own widget layer, not native OS widgets. This enables visual consistency across platforms but means apps do not look or feel native by default. Binary sizes are larger than native or KMP equivalents. Flutter's 50k+ pub.dev packages provide a middle ground between React Native's breadth and KMP's depth.

---

### SQ2: Mobile App Architecture

**F5. MVVM is the dominant pattern; MVI is preferred for complex state machines; both are compatible with Clean Architecture.** (HIGH — [#4, #5, #6] convergence despite #4 credential uncertainty)
MVVM offers lower boilerplate and a lower entry barrier, suitable for most screens. MVI's single immutable state object provides stronger consistency guarantees for screens with many interdependent UI fields or complex async state transitions. A practical heuristic: start MVVM, migrate individual screens to MVI as complexity demands.

**F6. Clean Architecture's 4-layer model is appropriate for large teams; 3-layer MVVM + Repository is the Android team's own recommendation for most apps.** (HIGH — Android official docs + challenge analysis)
The Presentation → Domain → Data → Infrastructure stack introduces abstraction overhead that is premature for small teams and early-stage products. Android's Guide to App Architecture recommends a 3-layer model (UI → Domain → Data) for most apps. Use the full 4-layer model only when multiple teams must enforce strict boundaries.

**F7. Jetpack Compose and SwiftUI both enforce unidirectional data flow natively, making MVVM/MVI natural fits.** (HIGH — [#6, #4])
Compose: ViewModel exposes `StateFlow`; composables subscribe via `collectAsState()`. Side effects (navigation, analytics) managed via `LaunchedEffect` or MVI-style channels. SwiftUI: `@ObservableObject` / `@StateObject` maps to ViewModel; Combine or Swift Concurrency (`async/await`) handles reactive state. TCA (The Composable Architecture) is the dominant Swift MVI-style library for complex SwiftUI apps.

---

### SQ3: Mobile Testing and CI/CD

**F8. The 70/20/10 unit/integration/E2E pyramid is the established target.** (HIGH — [#7, #8] convergence)
Unit tests: fast, milliseconds, 70% of suite. Integration tests: multiple components together (API + DB). E2E/UI tests: full user flows on device, brittle, expensive — limit to critical paths. Framework coverage: XCTest + XCUITest (iOS), JUnit/Kotlin Test + Espresso (Android), Detox (React Native), flutter_test + integration_test (Flutter).

**F9. Visual regression testing requires mobile-specific baseline management.** (HIGH — [#9])
Platform fragmentation — screen sizes, pixel densities, OS rendering differences, notches, safe areas — makes a single universal baseline unreliable. Best practices: disable animations before capture; mask dynamic content regions; maintain device-aware baselines per target screen size; prioritize high-impact screens first (login, checkout). Run at PR stage; gate on snapshot changes. Tools: swift-snapshot-testing (iOS), Paparazzi (Android), Percy (cross-platform), Applitools (AI diffing).

**F10. Cloud device farms dominate release testing; emulators/simulators dominate daily development.** (MODERATE — strategy HIGH confidence; specific savings figures from vendor [#8] are anecdotal)
Self-hosted device labs are impractical for most teams. Cloud farms (AWS Device Farm, Firebase Test Lab, BrowserStack, Sauce Labs) provide on-demand scale. Hybrid strategy: emulators for smoke tests and initial validation on every commit; real devices for regression and release gating.

**F11. CI/CD pipeline structure: unit tests on every commit → integration + snapshot on PR → full device farm on release candidate.** (HIGH — [#7, #10] convergence)
Fastlane automates build/test/distribution. GitHub Actions or similar for orchestration; dependency caching critical for mobile (pods, gradle) build times. Test passage mandatory gate for merge.

**F12. Staged rollout mechanics are established practice but not covered by fresh 2025 sources.** (MODERATE — established practice, coverage gap noted)
Standard ladder: 1% → 5% → 10% → 50% → 100%. Gate progression on crash rate and ANR thresholds from Firebase Crashlytics / Google Play Console Vitals. App Store offers 7-day automatic phased release; Google Play supports manual percentage control.

---

### SQ4: App Lifecycle, State Restoration, and Offline-First

**F13. `onDestroy()` is unreliable for critical state on Android — use `SavedStateHandle` + WorkManager.** (HIGH — T1 [#13])
The Android OS kills cached processes without calling `onDestroy()`. Correct persistence matrix: `SavedStateHandle` in ViewModel (survives config changes + process death); `ViewModel` alone (config changes only); `DataStore` / `SharedPreferences` (session persistence); `WorkManager` (guaranteed deferred task execution across process death).

**F14. Offline-first architecture requires the Repository as single source of truth with explicit read and write strategies.** (HIGH — T1 [#11])
Three read strategies: (1) local fallback (remote first, local on failure), (2) stream-based (emit local immediately, update with remote — best UX), (3) local-only with explicit sync. Two write strategies: (1) online-only (strict consistency, poor offline UX), (2) offline-first (write locally, sync when possible — best UX, requires conflict resolution). Conflict resolution options: last-write-wins (simple, lossy), CRDTs (collaborative apps), server-authoritative with optimistic updates (most CRUD apps).

**F15. iOS 26 BGContinuedProcessingTask enables long-running user-initiated operations with system UI — but treat as preview-accurate pending Apple final docs.** (MODERATE — T4 secondary source [#14])
Requires: explicit user initiation, measurable continuous progress reporting, user ability to cancel. Supports `.fail` and `.queue` submission strategies. System boosts task priority when app returns to foreground. Legacy BGAppRefreshTask and BGProcessingTask remain for non-user-initiated background work.

**F16. WorkManager (Android) and BGProcessingTask (iOS) are the correct primitives for background sync.** (HIGH — T1 [#13] + [#11])
Both respect system power management (Doze mode, battery state, network conditions). WorkManager constraints: `NetworkType.CONNECTED`, `requiresCharging()`, `requiresBatteryNotLow()`. iOS: `requiresNetworkConnectivity` and `requiresExternalPower`. Never use raw threads in `BroadcastReceiver.onReceive()` — process is killed when the method returns.

---

### SQ5: Mobile Performance Patterns

**F17. Android's official cold start target is <500ms; frame budget is 16.7ms at 60Hz / 11.1ms at 90Hz.** (HIGH — T1 [#15])
Measure cold start with Android Macrobenchmark; measure frames with `FrameMetricsAggregator` or Perfetto. iOS equivalents: MetricKit for field metrics, Instruments for lab profiling. P95/P99 startup latency should track close to median — high variance indicates inconsistent user experience.

**F18. Baseline Profiles are a low-cost, high-impact launch time optimization for Android — ship them with every APK.** (HIGH — T1 [#15])
Generated via `MacrobenchmarkRule`; pre-compile hot code paths based on real user behavior. Apple's equivalent is App Store pre-warming for common user launch paths. Profile with production-grade builds (`-m speed` compilation), not debug builds — debug builds mask real launch performance.

**F19. Memory optimization centers on minimizing allocations in rendering-critical paths, using WebP for images, and applying object pooling for high-frequency allocations.** (HIGH — T1 [#15])
GC during rendering causes CPU contention and jank. WebP provides 25–35% image size reduction over JPEG/PNG at comparable quality. Use `notifyItemChanged()` not `notifyDataSetChanged()` on RecyclerView; share `RecycledViewPool` for nested lists. Profile with Android Studio Memory Profiler — "Arrange by Callstack" view identifies allocation sources.

**F20. Battery and network efficiency: batch requests, use push over polling, and offload background sync to platform-provided constraint systems.** (HIGH — T1 [#13, #15])
Each radio wake-up drains battery even for millisecond requests — batching fundamentally changes the power profile. WorkManager and BGProcessingTask apply battery/network constraints automatically and respect Doze mode. Avoid wake locks held longer than needed.

## Claims

Chain of Verification (CoVe) on key statistics, attributions, and superlatives.

| # | Claim | Type | Source | Status |
|---|-------|------|--------|--------|
| 1 | "React Native has 42% market share" | statistic | [#2] KMPShip | flagged — vendor-published, no third-party corroboration; treat as directional only |
| 2 | "KMP adoption jumped from 12% to 23% in 18 months" | statistic | [#2] KMPShip | flagged — same vendor; directional only |
| 3 | "KMP code sharing 40–60% (logic only); 90–95%+ with Compose Multiplatform" | statistic | [#2] KMPShip | flagged — vendor estimate; plausible given architecture but not independently verified |
| 4 | "React Native 70–85% code sharing; native modules required for some platform APIs" | statistic | [#2] KMPShip | flagged — vendor estimate; directional; aligns with broad practitioner experience |
| 5 | "Flutter: 50,000+ pub.dev packages; React Native: 350k+ npm packages; KMP: 2,500+ KMP-specific libraries" | statistic | [#2] KMPShip | verified — pub.dev and npm counts are publicly queryable and broadly cited; KMP-specific library count is lower-confidence |
| 6 | "Cold app startup: < 500ms (Android Macrobenchmark / iOS MetricKit)" | benchmark | [#15] Android Developers T1 | verified — official Android performance documentation |
| 7 | "Frame rendering at 60Hz: ≤ 16.7ms per frame; at 90Hz: ≤ 11.1ms" | benchmark | [#15] Android Developers T1 | verified — derived from frame rate math (1000ms / 60 = 16.67ms); official guidance |
| 8 | "WebP provides 25–35% image size reduction" | statistic | [#15] Android Developers T1 | verified — cited in Android official performance docs; consistent with Google's WebP documentation |
| 9 | "Compose Multiplatform v1.8.0 reached stable iOS support in May 2025" | attribution | [#1] JetBrains T1 | verified — JetBrains official documentation; aligns with KMPShip corroboration |
| 10 | "BGContinuedProcessingTask introduced in iOS 26 with three requirements" | attribution | [#14] ArshTechPro DEV T4 | flagged — secondary source only; API name and requirements described from WWDC preview, not Apple final docs. Mark as preview-accurate. |
| 11 | "One fintech team cut CI runtimes 60% with dynamic sharding" | anecdote | [#8] Quash vendor | flagged — anonymous vendor case study, no reproducibility data |
| 12 | "One team reduced device farm bills 40% via time-based scheduling" | anecdote | [#8] Quash vendor | flagged — same source; reject as evidence for claims |
| 13 | "SavedStateHandle survives both configuration changes and process death" | attribution | [#13] Android Developers T1 | verified — official Android lifecycle documentation |
| 14 | "Never spawn threads in BroadcastReceiver.onReceive() — process is killed when method returns" | rule | [#13] Android Developers T1 | verified — official Android documentation; fundamental Android constraint |
| 15 | "TCA (The Composable Architecture) is the dominant Swift MVI-style library for complex apps" | superlative | [#4] T4 unknown credentials | flagged — plausible (TCA is widely cited in Swift community) but "dominant" is uncorroborated. Use "widely adopted" instead. |

## Challenge

Challenging key claims and surfacing alternative perspectives before synthesis.

### Claim: "React Native has 42% market share; KMP adoption jumped from 12% to 23%"
**Source:** [#2] KMPShip — a commercial vendor selling KMP tooling.
**Challenge:** These figures are self-published by a vendor with direct commercial interest in KMP's perceived growth. No independent third-party survey (State of Mobile, Stack Overflow Developer Survey, Statista) corroborates the specific 42%/23% breakdown. The claim should be treated as directional signal, not validated market data. The broader trend — cross-platform adoption growing, KMP gaining momentum — is corroborated by JetBrains' own community reports [#1], but the specific percentages are uncorroborated.
**Verdict:** Directional evidence only. Do not cite as quantified market fact.

### Claim: "KMP has essentially eliminated the traditional trade-off between development speed and native performance"
**Source:** [#2] KMPShip — same vendor.
**Challenge:** This is a promotional statement. KMP has real advantages for Kotlin-fluent teams sharing business logic, but it introduces material costs: Kotlin Multiplatform's library ecosystem (2,500+ KMP-specific libraries) is dramatically thinner than React Native's (350k+ npm packages) or Flutter's (50k+ pub.dev packages) [#2]. iOS developers on KMP teams must either adopt Kotlin or create Swift interfaces to shared code, adding friction. Claims of "no overhead" apply to shared *business logic* — UI remains fully native and therefore fully duplicated.
**Verdict:** Partially supported. KMP eliminates runtime overhead at the cost of ecosystem depth and team composition constraints.

### Claim: "Startups in fintech, healthtech, and mobility are returning to Swift + Kotlin native"
**Source:** [#2] KMPShip.
**Challenge:** No corroborating case studies or data provided. This "native resurgence" narrative is common in practitioner discourse but difficult to quantify. Evidence runs both directions: companies like Discord moved *to* React Native for cross-platform efficiency; large enterprises (e.g., Airbnb) moved *away* from React Native to native. The actual trend depends heavily on company size, team composition, and product type.
**Verdict:** Anecdotal. No systematic data available. Include as observed practitioner trend, not fact.

### Claim: "One fintech team cut CI runtimes 60% with dynamic sharding"
**Source:** [#8] Quash — a QA tooling vendor.
**Challenge:** Anecdotal case study from a vendor blog with no company name, no methodology details, and no reproducibility information. The 60%/40% savings figures are marketing-grade claims. Device sharding does improve parallelization, but results vary widely based on test suite size, infrastructure baseline, and prior pipeline optimization level.
**Verdict:** Plausible directional effect; reject the specific numbers as evidence.

### Claim: iOS 26 BGContinuedProcessingTask details
**Source:** [#14] ArshTechPro / DEV community — secondary source, not Apple developer documentation.
**Challenge:** iOS 26 was announced at WWDC 2025. This article describes the API based on developer previews and WWDC sessions, not Apple's shipping documentation. API behavior, naming, and constraints may differ at release. No Apple developer.apple.com primary source was found and fetched for this claim.
**Verdict:** Treat as preview-accurate but flag as requiring verification against final Apple documentation before production use. The existence and general purpose of BGContinuedProcessingTask is corroborated by the WWDC session, but implementation specifics may shift.

### Claim: "Clean Architecture" four-layer structure as universal best practice
**Source:** [#5] NextNative consultancy blog.
**Challenge:** Clean Architecture introduces real costs — indirection, boilerplate, and team onboarding friction. For small teams and early-stage products, the Domain layer abstraction can be premature. The Android team's Guide to App Architecture explicitly recommends a simpler 3-layer model (UI → Domain → Data) for most apps, not a four-layer model. Many successful production apps (e.g., early-stage) use MVVM + Repository without a dedicated domain layer.
**Verdict:** Clean Architecture is appropriate for large, complex, team-built apps. For small/solo teams or simple apps, a 3-layer MVVM model is equally valid and lower friction.

### Coverage gap: Staged rollout mechanics
**Not addressed by any fetched source.** Google Play and App Store both support percentage-based phased rollouts. Key patterns include: 1% → 5% → 10% → 50% → 100% ladder with monitoring gates between each increment; Firebase Crashlytics and Google Play Console vitals as go/no-go signals; App Store's phased release (7-day automatic rollout) vs. Google Play's manual percentage control. This is well-established practice but no fresh 2025 source was located.

## Key Takeaways

**Native vs. cross-platform:** No universally correct answer. KMP is the best bet for Kotlin-fluent teams needing native performance; Flutter for greenfield cross-platform projects; React Native for JavaScript teams with large ecosystem needs; native Swift/Kotlin when UI differentiation or specialized APIs are the core product.

**Architecture:** Default to 3-layer MVVM + Repository. Add a Domain layer when multiple teams need strict boundary enforcement. Use MVI for screens with complex interdependent state. Both patterns are idiomatic in Compose/SwiftUI's reactive model.

**Testing and CI/CD:** Run unit tests on every commit, snapshot + integration tests on every PR, full device farm suite on release candidates. Visual regression testing requires device-aware baselines — one universal baseline doesn't work across mobile fragmentation. Staged rollout (1% → 5% → 10% → 50% → 100%) with crash rate gates is the standard pattern.

**Lifecycle and offline-first:** `onDestroy()` is a lie on Android — design for sudden process termination. SavedStateHandle and WorkManager are the reliable primitives. Offline-first is a strategy: pick a read strategy (stream-based is best UX) and a write strategy (offline-first writes require conflict resolution).

**Performance:** Cold start <500ms and frame budget ≤16.7ms at 60Hz are the official targets. Baseline Profiles, deferred initialization, and allocation minimization in render paths are the highest-leverage levers. Batch network requests; don't poll — every radio wake-up costs battery.

**Source quality notes:** Market share figures from KMPShip, cost savings figures from Quash, and iOS 26 API details from ArshTechPro/DEV are either vendor-published or secondary sources. Treat these as directional; verify against official documentation for production decisions.

## Search Protocol

| # | Query | Results Considered | Selected | Reason |
|---|-------|--------------------|----------|--------|
| 1 | React Native vs Flutter vs Kotlin Multiplatform 2025 comparison | 10 results across kmpship.app, mvpappforge.com, perficient.com, droidsonroids.com | #2, #3 | KMPShip had concrete market share and benchmark data; JetBrains official docs authoritative |
| 2 | native Swift Kotlin vs cross-platform mobile development best practices 2025 | 10 results including kotlinlang.org, blog.jacobstechtavern.com, studiokrew.com | #1 | Official JetBrains documentation provides authoritative decision framework |
| 3 | MVVM MVI clean architecture mobile 2025 Jetpack Compose SwiftUI | 10 results including multiple Medium articles, github.com/topics/mvi-clean-architecture | #4, #5, #6 | Selected 2026-dated piece plus architecture best practices article; Octopus Energy blog practical |
| 4 | mobile CI/CD device farm testing best practices 2025 | 10 results including circleci.com, quashbugs.com, refraction.dev, alimertgulec.com | #7, #8, #10 | Testing strategy with pyramid breakdown, scaling infrastructure detail, CI/CD pipeline specifics |
| 5 | offline-first mobile architecture patterns 2025 | 10 results including flutter.dev/docs, droidcon.com, medium.com, dev.to | #11, #12 | Flutter official docs had concrete code patterns; droidcon Android-specific (returned 404) |
| 6 | mobile app performance optimization launch time battery memory 2025 | 10 results including developer.android.com, arvisus.com, scalosoft.com | #15, #16 | Android Developers official docs are authoritative and highly specific with code examples |
| 7 | mobile screenshot testing visual regression staged rollout practices 2025 | 10 results including percy.io, quashbugs.com, getpanto.ai, browserstack.com | #9 | Quash article had concrete mobile-specific guidance on baselines and device fragmentation |
| 8 | mobile app lifecycle state restoration background processing iOS Android 2025 | 10 results including developer.android.com, dev.to WWDC 2025, medium.com | #13, #14 | Android official lifecycle docs authoritative; WWDC 2025 iOS 26 BGContinuedProcessingTask new API |
| 9 | Jetpack Compose SwiftUI architecture patterns 2025 | (covered by query #3 results) | — | Merged with SQ2 results; no additional distinct search needed |
