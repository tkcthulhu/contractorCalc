# ContractorCalc

An offline Android/iOS construction calculator for contractors and tradespeople.

**Current implementation: project foundation only.** The app opens a clearly
labeled unfinished screen. It does not yet calculate, collect preferences, or
store tape, memory, or material presets. The approved product contracts describe
the intended application, not completed features.

## Developer setup

The exact approved baseline is owned by
[`contractorcalc-toolchain`](toolchain-design.md). Do not substitute a newer SDK,
loosen package constraints, or add dependency overrides to bypass a failed gate.

Prerequisites for the local bootstrap: Python 3.10+, Git, HTTPS access to Google's
Flutter release storage, Pub, and dependency build-time assets on GitHub, `tar`
with xz support on Linux or `unzip` on
macOS, and several GiB of free space. The bootstrap supports Linux x64 and macOS
arm64; other hosts need a separately verified SDK archive decision.

From this checkout, in Bash:

```bash
python3 tool/bootstrap_flutter.py
source tool/env.sh
python3 tool/check_toolchain.py
flutter pub get --enforce-lockfile
bash tool/verify.sh
```

The bootstrap verifies the official release metadata and archive SHA-256 before
extracting Flutter **3.47.8**, commit
`737ba8f885dc774b53b442759999a312c9461e4e`, with bundled **Dart 3.13.7**.
It installs into `.toolchain/`, not globally. `tool/env.sh` sets checkout-local
Pub, Gradle and XDG cache/config paths and suppresses analytics for the shell.
It does not install Java, Android SDKs, Xcode, or accept licenses. Re-sourcing is
needed in each new shell. An existing SDK directory is never treated as version
proof: the explicit identity check and verification script must pass.

Keep `pubspec.lock`, the Gradle wrapper and checksum, and native resolution locks
when a real native build creates them. Initial dependency resolution has already
been performed; normal setup must use `--enforce-lockfile`, not `pub upgrade`.
Storage and generation dependencies are intentionally declared at the approved
baseline even though their product features are not implemented yet.

### Verification

`bash tool/verify.sh` is the shared local/GitHub CI command. It checks:

- Exact Flutter/Dart/revision identity and bootstrap refusal tests.
- Static Android/iOS deployment, identity, backup and wrapper configuration.
- Locked package resolution and `build_runner` generation.
- Dart formatting, Flutter analysis and all normally discovered `test/` tests.
- No lockfile drift or changed/untracked generated `*.g.dart` output.

It resolves packages and may execute dependency build hooks, generate outputs and
populate ignored caches. It does not launch a native app, open a database, build
mobile artifacts, sign, or deploy. No Drift schema exists, so successful generation does
not establish schema correctness. Hosted CI has not been run merely because its
workflow exists.

Core tests currently guard import boundaries, **not calculator correctness**.
Widget tests cover the real composition root and small-screen/large-text shell.
`test/persistence/` and `integration_test/` contain coverage notes, not passing
placeholder acceptance tests.

### Running on mobile

After independently provisioning the exact native toolchain from the toolchain
spec and verifying a target device:

```bash
source tool/env.sh
python3 tool/check_toolchain.py
flutter devices
flutter run -d <verified-device-id>
```

The development identity is `com.example.contractorcalc` on both platforms; it
is not a production domain/store identity. Android minimum API is **24**; iOS
minimum is **15.0**. Only Android/iOS projects are generated—desktop hosts are not
product platforms.

Native builds are not yet verified. Android needs the pinned JDK/SDK/NDK;
iOS needs the selected macOS/Xcode host. The release configuration has no signing
setup and does not silently sign with debug keys. Native SQLite packaging,
Android 16 KB compatibility, both release ABIs, minimum-platform installation,
offline workflows, restart durability, and screen-reader testing remain required
acceptance gates in the owning specs. A Linux widget run proves none of them.

Android cloud backup and device transfer are disabled by manifest and explicit
exclusion rules, pending device verification. No database exists. The storage
slice must set and test iOS's backup-exclusion resource attribute on the actual
`CCData` directory **before** creating local data. No cloud recovery is promised.

### Local resources

`.toolchain/` holds the verified archive and SDK. `.local/` holds package/build
caches and task-local command evidence; both are ignored by Git. These are not
application user data. No automatic cleanup is installed. Before removing bulk,
ensure no commands use it and preserve any needed evidence; the SDK/cache can be
recreated from the retained baseline and lockfile. Losing the only SDK copy
requires another download, not a global fallback.

## Architecture and contracts

The root is one Flutter application, not a separate package per solver. Dependency
boundaries and their rationale are owned by
[`contractorcalc-architecture`](architecture-design.md):

- `lib/core/`: pure Dart quantities and calculations (not implemented yet).
- `lib/application/`: orchestration and repository contracts (not implemented yet).
- `lib/features/`: Flutter presentation; currently only the foundation screen.
- `lib/data/`: storage adapters (not implemented yet).
- `lib/main.dart` and `lib/app.dart`: application composition and shell.

Other approved owners:

- [Goals and requirements](goal-and-requirements.md)
- [Interaction contract](interaction-design.md)
- [Calculation contract](calculation-design.md)
- [Persistence contract](persistence-design.md)
- [Pinned toolchain and platform baseline](toolchain-design.md)
- [Historical design-readiness record](implementation-readiness.md)

Scaffolding verification is not feature, persistence, device, or release
acceptance. Those gates remain in force for the corresponding implementation
slices.
