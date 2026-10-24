# Device acceptance coverage

The foundation has no device acceptance tests. Do not add a passing placeholder
at `offline_workflows_test.dart`: that path is reserved for the genuine offline
workflows required by [`contractorcalc-toolchain`](../toolchain-design.md).

The feature slices must add and run the required Android/iOS workflows on verified
targets using synthetic local data. Widget tests and compilation do not establish
first-launch behavior, process-restart durability, backup exclusion, screen-reader
behavior, minimum-platform support, or SQLite release packaging.
