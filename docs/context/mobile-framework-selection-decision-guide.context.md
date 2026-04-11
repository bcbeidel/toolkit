---
name: Mobile Framework Selection Decision Guide
description: "Swift/Kotlin native, KMP, Flutter, and React Native each have a defensible sweet spot — framework selection is a team-and-product decision, not a technical superiority question."
type: concept
confidence: high
created: 2026-04-10
updated: 2026-04-10
sources:
  - https://kotlinlang.org/docs/multiplatform/native-and-cross-platform.html
  - https://www.kmpship.app/blog/kmp-vs-flutter-vs-react-native-2025
  - https://kotlinlang.org/docs/multiplatform/kotlin-multiplatform-react-native.html
related:
  - docs/context/mobile-mvvm-mvi-clean-architecture-selection.context.md
  - docs/context/android-state-persistence-survival-matrix.context.md
  - docs/context/offline-first-read-write-strategy-model.context.md
---
# Mobile Framework Selection Decision Guide

Mobile framework selection is a team-and-product decision, not a technical superiority question. Swift/Kotlin native, Kotlin Multiplatform (KMP), Flutter, and React Native each have a defensible sweet spot with real tradeoffs. Benchmark comparisons between frameworks are less useful than matching a framework to team expertise and product requirements.

## Decision Framework (JetBrains Official)

**Choose cross-platform when:** building for both Android and iOS simultaneously, optimizing development time, or wanting shared business logic while retaining native UI control.

**Choose native (Swift/Kotlin) when:** single-platform target, UI is critically differentiated (AR, complex graphics, platform-specific UX), team has no bandwidth for new tech adoption, or performance is the primary constraint.

## Framework Sweet Spots

**Swift/Kotlin native**
- Full platform API access, no abstraction layer overhead
- Required for AR, complex graphics, or deep platform integration (HealthKit, CoreML, Android hardware APIs)
- Single-platform commitment; choosing both platforms means two separate codebases
- Highest initial investment, lowest runtime overhead

**Kotlin Multiplatform (KMP)**
- Best for: existing Android/Kotlin teams, gradual migration from Android-only app, native performance required
- Compiles to JVM bytecode (Android) and native binaries (iOS) — shared code performance equals native
- Compose Multiplatform reached stable iOS support in May 2025 (v1.8.0), enabling shared UI code in Kotlin and 90–95%+ code sharing, closing the gap with Flutter while retaining native binary performance
- Smaller library ecosystem than Flutter or React Native, but full JVM ecosystem access; 2,500+ KMP-specific libraries
- Market adoption is growing (KMPShip reports direction, though specific percentages are vendor-published and should not be cited as market data)

**Flutter**
- Best for: fastest MVP, pixel-perfect cross-platform UI, greenfield project with team willing to learn Dart
- Uses own rendering engine (Impeller), not native OS widgets — visual consistency across platforms at the cost of larger binary sizes and non-native appearance by default
- 50,000+ pub.dev packages; strong third-party library coverage
- Requires Dart investment — teams without Dart experience should factor in ramp-up time

**React Native**
- Best for: JavaScript/React teams, large npm package ecosystem needed, web code sharing valuable
- 350,000+ npm packages is the primary differentiator
- Bridgeless/Fabric architecture improves load time and memory usage over older bridge-based integration
- Bridge-based native module integration is still "sometimes problematic" for deep platform APIs; KMP has deeper access with less overhead

## 2025 Context

Startups in fintech, healthtech, and mobility are returning to Swift + Kotlin native for performance-critical products. KMP is the fastest-growing cross-platform entrant following Compose Multiplatform's stable iOS release. Flutter remains competitive for greenfield projects requiring fast time-to-market.

The "React Native vs Flutter" comparison that dominated earlier years has been superseded by KMP's graduation into a viable third option, particularly for teams with existing Kotlin codebases.

## Takeaway

Match framework to team, not to benchmarks. For cross-platform: KMP if you have Kotlin expertise, Flutter for fastest cross-platform MVP, React Native for JavaScript teams. For single-platform or performance-critical products: native Swift/Kotlin. Evaluate KMP seriously for any new Android project, given that Compose Multiplatform stable iOS support now enables full code sharing without sacrificing native performance.
