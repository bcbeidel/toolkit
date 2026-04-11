---
name: "Mobile MVVM, MVI, and Clean Architecture Selection"
description: MVVM is the default for mobile; MVI is correct for complex state machines — both coexist within Clean Architecture and can be mixed per screen.
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://medium.com/@jyc.dev/architecture-patterns-in-mobile-development-2026-mvvm-mvi-and-clean-architecture-f26583f53522
  - https://nextnative.dev/blog/mobile-app-architecture-best-practices
  - https://medium.com/mobile-at-octopus-energy/architecture-in-jetpack-compose-mvp-mvvm-mvi-17d8170a13fd
related:
  - docs/context/mobile-framework-selection-decision-guide.context.md
  - docs/context/android-state-persistence-survival-matrix.context.md
  - docs/context/offline-first-read-write-strategy-model.context.md
---
# Mobile MVVM, MVI, and Clean Architecture Selection

MVVM is the dominant mobile architecture pattern and the correct default. MVI is preferred for screens with complex, interdependent state. Both fit cleanly inside Clean Architecture layers and can coexist within the same app. Start with MVVM; escalate individual screens to MVI as complexity demands.

## MVVM vs. MVI: The Decision Criteria

**MVVM (Model-View-ViewModel)**
- ViewModel exposes separate observable publishers per data piece (StateFlow, MutableState)
- View subscribes to individual state streams; updates are granular
- Lower boilerplate, lower entry barrier
- Correct default for most screens

**MVI (Model-View-Intent)**
- Single immutable UI state object published as a unit; all fields updated together
- Unidirectional data flow: View emits Intents → Reducer produces new State → View renders state
- Stronger consistency guarantees for screens with many interdependent UI fields
- Better predictability for complex async state transitions
- Higher boilerplate than MVVM

The practical heuristic: use MVVM for screens where state fields are independent; escalate to MVI when state fields have interdependencies that MVVM's per-field streams handle inconsistently. A screen showing a loading state, error state, and data that must all update together is a candidate for MVI.

## Platform Implementations

**Android (Jetpack Compose):**
- MVVM: ViewModel exposes `StateFlow` or `MutableState`; composables subscribe via `collectAsState()`
- MVI: ViewModel exposes a single `StateFlow<UiState>`; Intents flow to ViewModel via a channel
- Side effects (navigation, toasts, analytics): manage via `LaunchedEffect`, `SideEffect`, or MVI-style channel in ViewModel
- TCA (The Composable Architecture) is the dominant MVI-style library for complex SwiftUI apps on iOS

**iOS (SwiftUI):**
- MVVM: `@StateObject` / `@ObservableObject` maps to the ViewModel concept; Combine or Swift Concurrency handles reactive state
- MVI pattern: explicit state machine with Intents and reducers, commonly implemented via TCA

## Clean Architecture Layers

Clean Architecture decouples business logic from frameworks via concentric layers:

1. **Presentation Layer** — UI only (Composables, Views, ViewModels); MVVM or MVI lives here
2. **Domain Layer** — business rules and use cases; no framework dependencies; stable across platform changes
3. **Data Layer** — repositories, data sources (Room, Retrofit, Core Data, URLSession)

Each layer depends only inward (Presentation depends on Domain; Domain does not depend on Data or Presentation). UI changes cannot break data logic.

**Scale guidance:** The 4-layer model (adding an Infrastructure layer for networking, logging, device APIs) is appropriate for large teams enforcing strict boundaries. The Android team's own Guide to App Architecture recommends the 3-layer model for most apps. Use 4 layers only when multiple teams must maintain strict boundaries between domain logic and external infrastructure.

## State Management Principles (Applicable to Both)

- Single source of truth: state lives in ViewModel, not split between ViewModel and View
- Action-based changes: no direct state mutations from the View layer
- Pure transformation functions for predictable, testable state transitions
- Unidirectional data flow enabling time-travel debugging and isolated unit testing

## Takeaway

Default to MVVM. The lower boilerplate and well-understood pattern is correct for the majority of screens. Introduce MVI for specific screens where interdependent state fields cause inconsistency bugs under MVVM. Both patterns fit cleanly inside Clean Architecture layers and can coexist within the same app without architectural inconsistency.
