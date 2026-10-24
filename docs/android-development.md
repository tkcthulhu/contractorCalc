# Local Android development (Linux x64)

This checkout uses command-line tools, not Android Studio or global packages.
The baseline is in [`toolchain-design.md`](../toolchain-design.md) and
[`tool/android-baseline.json`](../tool/android-baseline.json). macOS/iOS setup
is separate. These commands build the unfinished foundation, not a calculator.

## Use the already installed tools

Run from the checkout in Bash, re-sourcing in each new terminal:

```bash
source tool/android_env.sh
python3 tool/check_toolchain.py
python3 tool/check_android.py
```

Java, Android SDK/preferences/AVD, Pub and Gradle caches are checkout-local.
The shell selects dedicated ADB port **5038**, not the normal server/device list.
If a port is already occupied, inspect its ownership; do not kill another task's
server or emulator. A different ADB port can be selected with
`CONTRACTORCALC_ADB_PORT` before sourcing. Never target an arbitrary connected
phone or use an unqualified install command.

To build without starting a device:

```bash
flutter pub get --enforce-lockfile
flutter build apk --debug --target-platform android-x64 --no-pub
```

The ordinary output is `build/app/outputs/flutter-apk/app-debug.apk`. Android
integration tests overwrite that output with a test-harness build. The original
verified standalone APK from setup is separately retained, when available, at
`build/android-bootstrap/contractorcalc-x64-debug.apk`; ignored build artifacts
are not present in a fresh clone. The development package is
`com.example.contractorcalc`. Never distribute this debug build as a release.

## Start the dedicated emulator

The synthetic AVD `contractorcalc_api36_x64` has already been created locally.
Check that ports 5038, 5556 and 5557 are free before starting. Do not start a second
instance if this task's AVD/server is already running. Use separate terminals so
servers stay foreground, visible and easy to stop.

Terminal 1:

```bash
source tool/android_env.sh
export HOME="$CONTRACTORCALC_ROOT/.local/android-home"
adb -L "tcp:$ANDROID_ADB_SERVER_PORT" nodaemon server
```

Terminal 2 (the verified headless configuration):

```bash
source tool/android_env.sh
export HOME="$CONTRACTORCALC_ROOT/.local/android-home"
export TMPDIR="$CONTRACTORCALC_ROOT/.local/android-tmp"
mkdir -p "$HOME" "$TMPDIR"
emulator -avd contractorcalc_api36_x64 -port 5556 \
  -no-window -no-audio -no-snapshot -no-boot-anim -no-metrics \
  -gpu swiftshader -memory 2048 -cores 2 \
  -camera-back none -camera-front none
```

The image raises RAM to its 2560 MiB minimum. KVM must be usable; do not change
host virtualization/security settings to bypass a failure. **Do not add `-grpc`:**
ADB is sufficient and the initial explicit gRPC listener was not safe. Inspect
listeners after startup (`ss -ltnp`); emulator/ADB listeners must be loopback-only.
A visible window can be requested by omitting `-no-window`, but desktop rendering
and any additional GUI host libraries have not been verified here.

Terminal 3:

```bash
source tool/android_env.sh
adb -P "$ANDROID_ADB_SERVER_PORT" devices -l
adb -P "$ANDROID_ADB_SERVER_PORT" -s emulator-5556 shell getprop sys.boot_completed
adb -P "$ANDROID_ADB_SERVER_PORT" -s emulator-5556 shell getprop ro.boot.qemu.avd_name
adb -P "$ANDROID_ADB_SERVER_PORT" -s emulator-5556 shell getprop ro.build.version.sdk
adb -P "$ANDROID_ADB_SERVER_PORT" -s emulator-5556 shell getprop ro.product.cpu.abi
adb -P "$ANDROID_ADB_SERVER_PORT" -s emulator-5556 shell getprop ro.kernel.qemu
```

Require, respectively: boot completed **1**, AVD **contractorcalc_api36_x64**,
API **36**, ABI **x86_64**, emulator **1**, and the checkout-owned emulator process.
An arbitrary device with a similar serial is not sufficient. Allow boot to
complete and inspect the actual UI for blocking system dialogs before testing;
do not suppress ANRs or loosen assertions to force a pass.

Then run the app, or the bounded native bootstrap test:

```bash
flutter run -d emulator-5556
# Stop flutter run before starting the separate test:
flutter test integration_test/android_bootstrap_test.dart \
  -d emulator-5556 --no-pub --reporter expanded
```

The test checks the real shell, executes SQLite in memory, and prints
`ANDROID_BOOTSTRAP_SQLITE` with the runtime source identity/compile options.
It creates no durable application database. It is **not** the reserved full
`offline_workflows_test.dart` acceptance suite. For offline smoke context, use
only this verified synthetic guest: `adb ... shell cmd connectivity airplane-mode
enable`, `adb ... shell svc wifi disable`, then inspect guest connectivity. This
is not full offline/persistence/backup acceptance.

Stop the foreground emulator and ADB with Ctrl-C in their own terminals; inspect
processes/listeners afterward. After an interrupted parent session, verify exact
owned executable paths, command lines and ports before stopping survivors. Do
not use blanket `killall`/`pkill` or accidentally start a new server while checking
whether the old one stopped. Retain the AVD unless its owner approves removal.

## Recreate tools in a fresh checkout

Prerequisites: the pinned Flutter setup, Python 3.10+, Bash, Git, HTTPS, `tar`,
`unzip`, `ss`, usable KVM, and sufficient disk/RAM. The completed local setup
retained roughly 11 GiB in `.toolchain/`, 3.6 GiB in `.local/`, plus build outputs;
these sizes are observations, not quotas or automatic cleanup thresholds.

First review the Android SDK License Agreement dated January 16, 2019.
`tool/android-baseline.json` records its source and exact-text SHA-256
`1f8729233617b193fd619213792ae16a41b95d2bbbf525dfe66998252ba68b16`.
Only if you accept that exact agreement:

```bash
python3 tool/bootstrap_android.py --accept-sdk-license
source tool/android_env.sh
export HOME="$CONTRACTORCALC_ROOT/.local/android-home"
mkdir -p "$HOME"
sdkmanager --sdk_root="$ANDROID_HOME" --channel=0 \
  'platform-tools' 'platforms;android-36' 'platforms;android-35' \
  'build-tools;36.0.0' 'ndk;28.2.13676358' 'cmake;3.22.1' \
  'emulator' 'system-images;android-36;default;x86_64'
python3 tool/check_android.py
```

The bootstrap checks the license text and JDK/CLI archive checksums; it does not
record a package-license receipt or accept terms by default. Review sdkmanager's
prompt and accept only the same agreement. Different/additional terms require a
new decision. **Never pipe `yes` into `sdkmanager --licenses`.**

The package command is for fresh provisioning, not routine updates. Some SDK
package IDs are unversioned: sdkmanager is not a revision lock. The checker
compares every installed identity/revision to the baseline and must pass before
building. If upstream serves different revisions, stop and review archival
reproduction or an explicit baseline amendment; do not silently update the pins.
API 35 is required by the selected JNI plugin; the app still compiles/targets 36.
CMake 3.22.1 is the native plugin build tool, not an app dependency upgrade.

Create a **new dedicated synthetic** AVD only if it does not already exist:

```bash
mkdir -p "$ANDROID_AVD_HOME" "$ANDROID_USER_HOME" \
  "$CONTRACTORCALC_ROOT/.local/android-home" \
  "$CONTRACTORCALC_ROOT/.local/android-tmp"
printf 'no\n' | avdmanager create avd --name contractorcalc_api36_x64 \
  --package 'system-images;android-36;default;x86_64' --device pixel_2
```

Here `no` declines a custom hardware profile; it is not license acceptance. Do
not use `--force` to overwrite an existing AVD. Before building on a fresh
checkout, review/create suitable limits in the ignored
`$GRADLE_USER_HOME/gradle.properties` (do not overwrite existing preferences).
The observed build used these settings:

```properties
org.gradle.daemon=false
org.gradle.workers.max=2
org.gradle.jvmargs=-Xmx2G -XX:MaxMetaspaceSize=768m -XX:ReservedCodeCacheSize=256m -XX:+HeapDumpOnOutOfMemoryError
```

These are local resource choices, not committed preferences or a diagnosis of
the ThinkRail crashes. The template's larger defaults are not the limits used
for the verified build.

## Evidence and limits

[`implementation-readiness.md`](../implementation-readiness.md) records the
observed result and caveats. Compact original/recovery logs, SQLite identity,
APK inspection and screenshots are retained under ignored
`.local/evidence/android-setup/`. The first test was interrupted by the ThinkRail
crash; its separate recovery run passed. Android startup-system ANRs, CLI/SDK XML
warnings and a final ActivityManager wait timeout followed by a verified visible
shell were not erased or treated as a stability/performance pass.

Native Android x86_64 debug smoke is verified, not release signing/ABIs, 16 KB
compatibility, minimum/current acceptance targets, durable storage, accessibility,
full offline workflows, hosted CI or iOS. No automatic SDK/cache/AVD cleanup is
installed; preserve unique evidence and obtain owner direction for bulk reuse or
removal.
