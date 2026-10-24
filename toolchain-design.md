---
id: contractorcalc-toolchain
type: module-design
status: active
title: ContractorCalc — Pinned Toolchain and Platform Baseline
parent: contractorcalc-architecture
depends-on: [contractorcalc-architecture]
references: [contractorcalc-persistence]
tags: [toolchain, platforms, dependencies]
---

# Pinned toolchain and platform baseline

## Scope and evidence level

The source-grounded baseline was selected on **2026-10-24**. The application scaffold now declares these exact dependencies, retains the resolved `pubspec.lock`, and includes Android/iOS projects generated from the pinned SDK. Resolution is not native-build or device evidence. The selected baseline remains normative; changes require an explicit compatibility decision rather than silently following latest releases. [implementation-readiness.md](implementation-readiness.md) separates historical design evidence from the authorized foundation delivery.

## Flutter and platform pins

- **Flutter 3.47.8 stable**, framework commit `737ba8f885dc774b53b442759999a312c9461e4e`, with its bundled **Dart 3.13.7**. Do not separately upgrade Dart. Official Linux/macOS release manifests agree on this version/commit. This stable patch also carries the documented compromised-CA security update; do not start on the preceding patch merely to avoid toolchain changes.
- **Android:** minSdk **24** (Android 7.0), compileSdk **36**, targetSdk **36**, NDK **28.2.13676358**, Gradle wrapper **9.3.1**, Android Gradle Plugin **9.1.0**, Kotlin Gradle Plugin **2.4.0**. These match the selected Flutter commit's template constants; preserve the template's AGP/Kotlin integration rather than mixing unrelated tutorial versions. Use **Eclipse Temurin JDK 21.0.13+9**. Target API and deployment floor are different; compiling against 36 does not forbid running on newer supported Android versions.
- **iOS:** deployment target **15.0**; build baseline **Xcode 27.1 (27A9275)** with its bundled Apple SDK/Swift toolchain. Use a supported Mac build host; the published stable **macOS 27.0.1 (26A434)** is the selected host baseline. This is not a claim that such a Mac is available locally. Native package integration follows the selected Flutter template; lock any resulting SwiftPM/native resolutions during authorized bootstrap rather than installing an unrequested global CocoaPods version.
- **Artifacts:** Android release includes arm64-v8a and armeabi-v7a; x86_64 is a development/emulator target. iOS devices use arm64; simulator binaries must match the build host architecture. Validate each claimed release ABI and native SQLite packaging, including Android 16 KB page-size compatibility. A successful x86_64 emulator run alone does not prove either release ABI.

The app targets these mobile platforms only; Linux/macOS are development/test hosts, not additional product deliverables. Flutter's published platform floor and path_provider's published Android API 24+/iOS 13+ support are consistent with the selected product floor. Published constraints are not device-execution evidence.

## Exact package selections

Use exact versions (no caret/latest constraints for these direct selections) when an implementation task creates manifests. Keep Riverpod declarations handwritten initially; no Riverpod generator, hooks framework, generic units engine, separate rational package, remote service SDK, or legacy sqlite3_flutter_libs dependency is required.

| Role | Package | Selected version |
| --- | --- | --- |
| UI state/dependency wiring | flutter_riverpod | 3.4.3 |
| Typed SQLite repository | drift | 2.35.3 |
| Native SQLite/assets | sqlite3 | 3.8.0 |
| Application-support path | path_provider | 2.1.6 |
| Platform implementation constraint | path_provider_android | 2.3.1 |
| Platform implementation constraint | path_provider_foundation | 2.6.0 |
| Portable path handling | path | 1.9.1 |
| Current-command consistency hashes | crypto | 3.0.7 |
| Drift code generation | drift_dev | 2.35.2 |
| Build generation runner | build_runner | 2.17.1 |
| Static lint baseline | flutter_lints | 6.0.0 |
| Unit/widget/repository tests | flutter_test | selected Flutter SDK |
| Device workflows | integration_test | selected Flutter SDK |

Declare the endorsed path-provider implementations as exact dependency constraints, while application code imports path_provider rather than their internals. Do not use dependency_overrides to force incompatibilities. Flutter_riverpod 3.4.3 selects riverpod 3.4.3; the app does not need another independently versioned Riverpod dependency in the core.

The checked metadata permits Dart 3.13.7: Riverpod requires ^3.12.0; Drift/sqlite3/drift_dev require ≥3.10.0 <4.0.0; build_runner requires ^3.11.0; the selected foundation implementation requires ≥Flutter 3.38.4 / Dart ^3.10.3. Drift 2.35.3 requires sqlite3 ^3.4.0, which includes 3.8.0; drift_dev 2.35.2 permits drift ≥2.30.0 <2.36.0. Its analyzer range ≥13 <15 overlaps build_runner's ≥14.3 <15. This is a focused declared-constraint review, not a full transitive solve.

Do **not** add the latest standalone `test` package at the application root: test 1.33.0 requires test_api 0.7.15, while the pinned Flutter flutter_test source pins test_api 0.7.12 and matcher 0.12.20. Even test 1.31.1, which matches that test_api, caps analyzer below 14, conflicting with the selected build runner. Use SDK flutter_test to execute pure core tests as well as widget/repository tests; the production core itself remains pure Dart. A future separately published core package would need its own explicit package/test resolution decision, not a silent conflicting app dependency.

Sqlite3 3.8.0 uses build hooks/native assets. Development builds may fetch verified native assets; shipped offline calculations/storage must never fetch a SQLite library at application runtime or fall back to an OS library with unknown features. Its published archive and the two platform-provider archives were read in memory and their SHA-256 digests matched official Pub metadata. That source inspection ran no build hook, installation, or dependency resolver. The later foundation bootstrap resolved the graph and executes build hooks through normal tooling; this does not establish mobile native packaging. The first native build must record the actual packaged SQLite version/features rather than infer them from a Dart package version.

## Locking and bootstrap gates

Initial authorized bootstrap must resolve dependencies, inspect the actual graph/native packaging and retain pubspec.lock, generated native resolution locks, Gradle wrapper/checksum, SDK commit/version and code-generation outputs. Later reproduction enforces those locks; no automatic upgrades. Initial resolution may reveal a transitive or native-build incompatibility not evident in direct metadata. If it does, stop that gate and propose a version amendment; do not loosen requirements or add overrides to get green.

The designated initial app test directories are `test/core`, `test/interaction` and `test/persistence`; device acceptance suite is `integration_test/offline_workflows_test.dart`. The scaffold contains foundation tests under the first two normal-suite paths, with coverage notes reserving persistence/device locations. It deliberately does not create a passing placeholder `offline_workflows_test.dart`. Before a feature slice is accepted, its normal-suite fixtures and relevant device flows must exist and execute; discovery or compilation alone is insufficient.

The bootstrap verification target is an isolated, synthetic-data application checkout at this baseline. The foundation task authorized SDK installation, resolution, generation, analysis and normal-suite checks; native builds and device acceptance remain separate gates. The corresponding commands are:

- `flutter --version --machine`, `java -version`, and on the Mac `xcodebuild -version`: compare to the selected versions and record exact host/runtime identities.
- `flutter pub get`: establish the first reviewed lock; subsequent reproductions use `flutter pub get --enforce-lockfile`. Inspect the complete selected graph, SDK test_api/analyzer interactions, native asset hooks, minimum OS metadata and licenses.
- `dart run build_runner build`, `flutter analyze`, `flutter test`: generated schema/types are current, static checks pass, and all normally discovered contracts execute without disabling assertions/tests.
- `flutter build apk --debug` and on the Mac `flutter build ios --simulator --debug`: prove initial native integration. Separately inspect release AAB/IPA ABI/native-library contents and signing when authorized; debug builds do not establish release packaging.
- `flutter test integration_test/offline_workflows_test.dart -d <verified-device-id>`: bind the real target before execution; networking disabled in the app test environment, synthetic local data, no human development database. This is a required suite/target class; device IDs and execution authority are not invented here.

Minimum acceptance matrix: Android API 24 and current supported API 37 (plus a 16 KB page-size environment for native assets); iOS 15.x minimum-family device and a current iOS 27.0.1 device/simulator. Test both release Android ABIs before claiming both. Modern Xcode simulator/debug-device support need not include iOS 15 even though its deployment target does: obtain an actual iOS 15.x install/test route rather than claiming a current simulator proves the minimum. An unavailable minimum-family target blocks that platform-support acceptance, not independent pure-core development.

No package resolution, native build, minimum-device, offline, persistence or accessibility gate has passed merely because the metadata is compatible. This spec grants no installation, license acceptance, signing, Git operation, execution, or publication authority.

## Foundation reproduction contract

`tool/flutter-baseline.json` is the executable SDK identity/archive record. `tool/bootstrap_flutter.py` verifies the official manifest and archive SHA-256 before extracting to ignored `.toolchain/`; it never chooses latest or installs global tools. The supplied archives cover Linux x64 and macOS arm64 development hosts, not additional product platforms. An existing SDK directory must pass `tool/check_toolchain.py`; existence alone is not verification. `tool/env.sh` keeps Pub/Gradle/XDG cache/config paths checkout-local.

`bash tool/verify.sh` is shared by local setup and the least-privilege GitHub checks workflow. It enforces SDK identity and locked resolution, exercises tooling refusal cases, checks declared native configuration, runs generation/formatting/analysis and all normal tests, and refuses drift in retained locks/generated Dart. The static native checks are not native build/device acceptance. Core import guards protect the pure-Dart boundary but do not prove mathematical correctness. There is no schema, so generation currently creates no retained application schema outputs.

Native projects use `com.example.contractorcalc` as a development-only identity pending a separate production identity decision. Android app backup and device transfer are disabled by manifest and explicit exclusion rules; device verification remains mandatory. iOS directory backup exclusion is not implemented until storage creates the real directory. Release signing is intentionally unconfigured rather than silently using debug keys.

The pinned Flutter SDK bundles a legacy Gradle 2.10 wrapper JAR. The scaffold instead retains the official Gradle **9.3.1** wrapper and launchers from [Gradle v9.3.1](https://github.com/gradle/gradle/tree/v9.3.1), preserving Flutter's AGP/Kotlin integration while enabling distribution checksum enforcement. JAR SHA-256 is `b3a875ddc1f044746e1b1a55f645584505f4a10438c1afea9f15e92a7c42ec13`; the `gradle-9.3.1-all.zip` distribution SHA-256 is `17f277867f6914d61b1aa02efab1ba7bb439ad652ca485cd8ca6842fccec6e43`, both compared with the official [distribution checksum endpoints](https://services.gradle.org/distributions/). No Gradle launch or Android build is implied by these checksum checks.

## Source identities

- Official Flutter manifests: [Linux](https://storage.googleapis.com/flutter_infra_release/releases/releases_linux.json) / [macOS](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json), stable entries for the pinned commit above. Linux x64 SDK archive SHA-256: `baf7dcc5a3dbba60fe863bf493a6cf203195621f7786eaa5a1bba02cd0d87dd2`; macOS arm64: `6114edc2dae3636cfefb7e4456a4510399ee856e324149b34dbacb509e329d05`. SDK archives were not downloaded during source selection; the foundation bootstrap subsequently downloaded and checksum-verified the Linux x64 archive.
- Flutter commit-pinned [Android template constants](https://github.com/flutter/flutter/blob/737ba8f885dc774b53b442759999a312c9461e4e/packages/flutter_tools/lib/src/android/gradle_utils.dart), [FlutterExtension](https://github.com/flutter/flutter/blob/737ba8f885dc774b53b442759999a312c9461e4e/packages/flutter_tools/gradle/src/main/kotlin/FlutterExtension.kt), and [flutter_test dependencies](https://github.com/flutter/flutter/blob/737ba8f885dc774b53b442759999a312c9461e4e/packages/flutter_test/pubspec.yaml).
- [Flutter supported platforms](https://docs.flutter.dev/reference/supported-platforms); [path_provider 2.1.6 support matrix](https://pub.dev/documentation/path_provider/2.1.6/).
- Pub version metadata follows `https://pub.dev/api/packages/<package>/versions/<selected-version>` and includes environment/dependency constraints and the published archive SHA-256. Important inspected archives: sqlite3 `5340531ad17f386ae444873f643f281060b6238cc702edeee6b1e90bc4c6874e`; path_provider_android `69cbd515a62b94d32a7944f086b2f82b4ac40a1d45bebfc00813a430ab2dabcd`; path_provider_foundation `2a376b7d6392d80cd3705782d2caa734ca4727776db0b6ec36ef3f1855197699`.
- [Official Temurin JDK 21.0.13+9 release](https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.13%2B9); [Apple release history](https://developer.apple.com/news/releases/) identifies Xcode 27.1/macOS 27.0.1 and current/minimum-family iOS point releases. Apple download access and a Mac test host have not been established.
