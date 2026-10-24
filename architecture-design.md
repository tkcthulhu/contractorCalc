---
id: contractorcalc-architecture
type: architecture-design
status: active
title: ContractorCalc — Architecture and Tech Stack
parent: contractorcalc-goals
depends-on: [contractorcalc-goals]
tags: [offline, mobile, architecture, persistence]
---

# ContractorCalc architecture

This is the approved architecture and stack selection, not an implementation record or authorization to build. Product scope and capabilities are owned by `contractorcalc-goals` in [goal-and-requirements.md](goal-and-requirements.md).

## Drivers and stack decision

ContractorCalc is a single, self-contained mobile application with a shared Android/iOS interface. The team has no existing-stack constraint. A consistent custom measurement keypad and specialized forms take priority over separately implemented platform-native interfaces; accessibility and platform navigation conventions still apply.

The selected stack is:

- **Flutter and Dart** for the mobile application and shared presentation.
- **Riverpod** for dependency wiring and observable application/UI state, not durable storage or mathematical authority.
- **Drift with native SQLite** for preferences, paperless tape, memory, and user preset overrides. Use the native/FFI implementation rather than a platform-channel database adapter; database work runs outside the UI isolate.
- **Pure Dart calculation modules**, with exact rational arithmetic backed by `BigInt` where possible and finite binary64 approximations for operations requiring them.
- **Dart/Flutter test tooling and actual SQLite integration tests**, plus Android and iOS device/simulator workflows.

There is no backend requirement. Calculations, defaults, presets, and required assets are bundled and available on first launch without network access or sign-in. Remote configuration, downloaded formulas, and online initialization are not prerequisites for any required capability.

### Alternatives and consequences

**React Native with TypeScript/Expo** could meet the same offline requirements and would become more attractive with existing React expertise. It was not selected because that expertise is not a constraint and Flutter fits the shared custom interface well. JavaScript `Number` alone would not provide exact fraction arithmetic. The TypeScript calculator referenced by the goals is not an adopted dependency; any selective reuse would require separate compatibility, license, and mathematical review.

**Kotlin Multiplatform with Compose on Android and SwiftUI on iOS** could share the domain core and provide native interfaces, but would require two presentation implementations and their interaction coverage. That cost is not justified by the approved shared-interface preference.

**Built-in Flutter notifiers** would reduce dependencies. Riverpod is selected to make shared feature state and dependency substitution explicit; the domain remains independent of it. **Key-value files** would suffice for a few settings, but an ordered tape, versioned records, and atomic updates favor SQLite. Drift adds generated-code tooling in return for typed queries and migration tooling. One database avoids inconsistent cross-store updates.

## Ownership and dependency boundaries

The application is a modular monolith, not a collection of services or a generic rules engine. Boundaries are logical responsibilities, not a requirement to create a package for every solver.

### Presentation and input

Flutter widgets own rendering, accessible controls, layout, focus, and gestures. They contain no formulas or direct database writes. A keypad controller maintains structured entry/command state; specialized forms collect labeled task inputs. Both paths use shared parsing, quantity types, and owning calculations.

A quantity formatter owns fraction resolution, decimal precision, separators, unit rendering, and normalization of display artifacts such as negative zero. Formatting never mutates a quantity or becomes an input to chained calculations, tape serialization, or memory.

Blank input, entered zero, invalid input, an unavailable result, and a result with warnings are distinct states. Validation failures preserve editable input. A rejected calculation does not replace a prior valid result or overwrite memory.

### Application orchestration

Feature controllers coordinate parsing, resolved preferences/preset inputs, calls to the calculation core, formatting, and repository commands. They do not reconstruct solver formulas. Riverpod supplies dependencies and observable state, but an in-memory provider is never evidence that a durable write succeeded.

Repository contracts expose local settings, tape, memory, and material-preset data. Drift adapters implement those contracts. Cross-record durable operations use one transaction coordinator and connection, rather than independently saving from multiple controllers.

### Calculation core

The calculation core owns units, dimension compatibility, conversion factors, numerical policy, formula validation, and immutable typed results. It has no Flutter, Riverpod, database, filesystem, network, or platform dependency.

Cohesive solver families cover dimensional arithmetic and conversions; geometry/trigonometry; roofs and rafters; stairs; framing and cuts; and material estimation. Each formula has one owning implementation. Shared quantity and geometry operations are reused by solvers, not copied into forms or controllers.

The app supplies explicit assumption snapshots to the core, including resolved densities, yields, coverage, waste, and user stair limits. Results carry calculated quantities, relevant assumptions, and structured warnings. Material-estimate results distinguish the calculated requirement from the whole-unit purchase count. Presentation does not calculate purchase rounding or stair-limit conflicts.

Invalid dimensions, incomplete or contradictory solver inputs, impossible geometry, division by zero, non-finite results, and unsupported numeric ranges produce explicit failure outcomes rather than fabricated zero values. Stair warnings concern user-supplied limits, not safety certification or code compliance.

### Persistence and bundled definitions

A local repository is the authority for durable state; feature state is its projection or an explicitly temporary session value. A bundled, versioned material catalog supplies defaults. User preset overrides are stored separately and are not overwritten when bundled definitions change. Calculation inputs contain the actual resolved values, not merely a mutable preset name.

Dependencies point inward: presentation uses application controllers; controllers use domain operations and repository contracts; storage adapters implement repository contracts. The core does not import adapters or framework state. Shared quantity types are used by formatting and validated serialization without introducing database dependencies into the core.

## Numerical integrity

Fractional and decimal measurements are parsed directly to normalized rational values with arbitrary-precision integer numerator and denominator. Denominators are nonzero and normalized positive. Decimal input must not first pass through binary floating point. Canonical units and exact defined conversion factors permit exact dimensional conversions and rational arithmetic.

Use exact results where the operation supports them. Roots, trigonometry, and other inexact operations may produce binary64 approximations; subsequent calculations retain that approximation at computational precision without display rounding. This does not claim that irrational results are exact. Exact and approximate representations are distinguished explicitly.

Quantities carry dimensional meaning separately from their display unit. Length, area, volume, angles, unitless values, and other supported quantities cannot be interchanged by interpreting a label or dropping units. Memory and tape preserve quantity types and numerical representation.

Exact rationals are serialized as numerator/denominator decimal strings with a representation discriminator, not SQLite integer products or rounded display text. Finite approximate values use a tagged round-trip-safe representation. Deserialization validates the representation and quantity type; malformed data is not coerced to zero.

The 19.9-billion display requirement is not assumed to define every intermediate numeric bound. Arbitrary-precision integers also do not imply unlimited input complexity. Input/range limits, approximation tolerances, discontinuity handling, rounding ties, and display overflow behavior require numerical contracts before affected calculations are implemented.

## Durable local state

One schema-versioned SQLite database stores these categories:

- **Preferences:** typed settings, including display choices. Apply defaults for verified absent settings, not for failed reads.
- **Tape:** ordered operation snapshots with typed inputs/results, relevant assumption values, and a calculation-version identifier. App upgrades do not silently recompute historical results. Retain saved entries until explicit user clearing; paginate reads rather than loading the entire history. There is no automatic count- or age-based deletion.
- **Memory:** typed, unrounded quantities. Empty memory and a stored zero are distinct. Memory-key and register semantics are defined separately from storage.
- **Preset overrides:** user-supplied assumptions separate from bundled definitions.

Tape is review history, not a universal event store or an implied undo mechanism. Durable draft restoration and tape replay are not introduced by this architecture.

### Writes and lifecycle

Use a serialized write path with transactions for complete durable operations. A tape append is committed as a complete snapshot, never a partial result. If an operation changes multiple related records, they commit or roll back together. Persist durable actions when performed; do not rely on backgrounding or application-exit callbacks to flush state.

Explicit tape and memory clearing have independent scopes and preserve preferences and preset overrides. Clear commands are ordered with pending writes so previously queued state cannot reappear after a successful clear. A rejected or failed durable operation preserves existing committed state.

A storage failure does not disable pure calculations. Show a visible persistence warning and distinguish temporary results/session state from saved data. Do not claim that a preference change, memory write, tape entry, or clear was saved before transaction commit. Saved-state features with unavailable data remain explicitly unavailable rather than pretending that data is empty. Recovery must not silently replay non-idempotent operations or recreate entries the user cleared.

### Initialization and upgrades

Create the schema on a verified fresh installation. Database and variable-payload formats are versioned and validated. Preserve historical quantity representations, tape snapshots, and user customization through supported upgrades. Keep schema history and migration tests; do not replace migrations with reset-on-open behavior.

A migration failure, malformed saved state, or unsupported newer database is reported without silently deleting or resetting user data. Refuse unsupported downgrades rather than truncate data or advertise an unproven lossless rollback. Recovery and any destructive reset require their own explicit user-facing contract and authorization.

## Verification and platform obligations

Architecture selection does not authorize check execution. Implementation acceptance requires evidence for these precise suite categories against isolated synthetic data:

- **Core:** independent known-answer cases across required solver families; exact conversion round trips; supported dimension combinations and rejection paths; fraction/decimal parsing; chained-calculation invariance across display settings; material assumptions, waste, purchase rounding; user-limit warnings; numeric boundaries and approximation tolerances.
- **Input parity and presentation:** equivalent keypad/form inputs produce the same domain results; preference changes affect presentation only; invalid input remains editable; empty, zero, warning, and failure states are distinguishable.
- **Actual SQLite:** fresh creation and each supported upgrade path; exact/approximate serialization round trips; state across close/reopen; preserved custom presets/history; transaction rollback under deliberate failures; clear/write ordering; storage failure and unsupported-version refusal without reset. Mock repositories alone do not establish durability.
- **Android and iOS integration:** first launch and all required capability families with networking disabled; keypad and specialized-form workflows; preference, tape, and memory persistence across process restart; explicit clearing; visible unsaved state; accessibility labels, focus/navigation, text scaling, and screen-reader behavior.

The pure core uses normally discovered Dart tests; widgets and application controllers use Flutter tests; persistence checks run against SQLite; device workflows use Flutter integration testing and platform accessibility inspection. Exact commands and fixtures are bound when the application/tooling exists. Android evidence does not substitute for iOS evidence, and successful compilation does not establish offline workflows or persistence.

Flutter/dependency versions and minimum Android/iOS versions must be pinned after compatibility review, including SQLite native packaging. Building, signing, and running iOS simulator workflows requires macOS/Xcode access. This is a build/verification prerequisite, not a runtime internet requirement.

## Design boundary

This decision settles stack, ownership, numerical representation strategy, local persistence topology, tape retention, and degraded-storage behavior. It does not settle detailed keypad/operator behavior, memory register/key semantics, exact database schema, solver conventions, numeric bounds/tolerances, or dependency/OS version pins. Those contracts require approval before their implementation; no module may fill the gaps by silently inventing product behavior.

## Technical references

These explain selected mechanisms; project decisions above remain authoritative.

- [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide)
- [Dart number representation and BigInt](https://dart.dev/resources/language/number-representation)
- [Riverpod](https://riverpod.dev/)
- [Drift platform support](https://drift.simonbinder.eu/platforms/), [transactions](https://drift.simonbinder.eu/dart_api/transactions/), and [migrations](https://drift.simonbinder.eu/migrations/)
- [Flutter iOS development setup](https://docs.flutter.dev/platform-integration/ios/setup)
