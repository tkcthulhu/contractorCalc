# Device acceptance coverage

`android_bootstrap_test.dart` is a bounded Android foundation smoke test: it
checks the real shell, opens in-memory bundled SQLite, executes a query and
reports the runtime version/source identity/compile options. It closes that
database and creates no durable user data. Run it only on the verified synthetic
target described in [the Android guide](../docs/android-development.md).

The foundation still has no full device acceptance suite. Do not add a passing
placeholder at `offline_workflows_test.dart`: that path is reserved for the real
offline workflows required by [`contractorcalc-toolchain`](../toolchain-design.md).

The feature slices must add and run the required Android/iOS workflows on verified
targets using synthetic local data. Widget tests and compilation do not establish
first-launch behavior, process-restart durability, backup exclusion, screen-reader
behavior, minimum-platform support, or SQLite release packaging.
