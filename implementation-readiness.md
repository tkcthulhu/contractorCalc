# ContractorCalc design-readiness record

The design-only task below is historical. The subsequent separately authorized foundation delivery is recorded at the end of this file; it does not retroactively expand design-task authority or establish complete feature/platform acceptance.

## Task and authority

- **Request:** resolve the implementation-design blockers identified after the architecture selection, before branch closeout. The preceding design-only boundary remains in force.
- **Mode:** DESIGN, under registered agentic-engineering guidance v1.2.0-rc.4. Documentation deliverables describe Behavior and Persistence/integrity risks; these profiles do not authorize implementation or execution.
- **Baseline:** inspected clean worktree at `3b006b0` (approved architecture). Existing approved requirements and stack choices are protected except for explicit user amendments recorded below.
- **Allowed:** read repository and official/public technical sources; draft/revise Markdown design contracts; perform standalone document/spec checks. No source code, dependency installation, app/database execution, Git mutations, PR/branch closure, agent delegation, or remote tracker mutation is authorized.
- **Repository:** `https://github.com/tkcthulhu/contractorCalc`; no tracker/task issue has been inspected or synchronized and no remote mutation grant is present. The assistant owns this local record; the user owns design acceptance and future implementation authorization. Tracker reconciliation is pending future project/implementation planning, not represented as done.
- **Stop:** deliver reviewed design contracts and honest readiness gates. Do not start implementation or close/ship the branch.

## Approved amendments — 2026-10-24

These are user decisions, not proof of implementation:

- Algebraic precedence; explicit multiplication, parentheses and units; repeated equals is a no-op; an operator chains from an unrounded result and a digit starts a new expression.
- One persistent typed register with MS/MR/M+/M−/MC; scientific notation above the normal display range.
- Android API 24 / iOS 15 minimums, subject to the pinned dependency review.
- Entirely offline first-launch imperial/metric selection; database excluded from automatic OS cloud backup.
- Display rounding is nearest with exact ties away from zero. Decimal precision defaults to hundredths; tenths remains selectable.
- Stair counting uses the upper floor as landing: N risers and N−1 treads.
- The polygon capability means convex regular polygons (equal sides and equal angles).
- Bundled material presets are labeled editable estimates, not universal supplier specifications.

The earlier approved decisions remain: Flutter/Dart, Riverpod, Drift/native SQLite, pure shared calculation authority, retain tape until explicitly cleared, and continue pure calculations with visible unsaved-state warnings during storage failures.

## Current checkpoint

- **Design readiness: READY; user-approved.** The user approved the four complete module contracts and pinned baseline on 2026-10-24, explicitly retaining execution gates and the no-implementation/no-closeout boundary. All four module specs are active. Implementation has not started.
- Active contract owners: `contractorcalc-interaction` / `interaction-design.md`; `contractorcalc-calculations` / `calculation-design.md`; `contractorcalc-persistence` / `persistence-design.md`; `contractorcalc-toolchain` / `toolchain-design.md`.
- The goals spec reflects approved product amendments; architecture links detailed owners rather than leaving the old design gaps open. The review target was these four complete module specs plus the corresponding goals/architecture reconciliation presented in chat, not a runnable application. Only lifecycle/acceptance-record updates follow that approval.
- Next action belongs to the user: separately authorize a bounded implementation/bootstrap task or branch closeout. Neither is authorized by design acceptance. Dependency/build, mathematical and device acceptance gates below remain mandatory before their respective acceptance units.
- This record owns progress/evidence. Durable contracts live only in their owning specs.

## Requirements correspondence

| Active goals surface | Owning contract sections |
| --- | --- |
| Imperial/metric dimensional math, exact conversions, fractions/decimal modes, DMS, density, board feet, cost and display range | calculation-design.md: Owner/API/units, Representation/limits, Dimensional/angular operations, Materials; interaction-design.md: First launch/preferences, Expression model |
| Rise/run/diagonal/pitch, common/regular/irregular hip/valley/jack rafters, cut angles, flat/pitched roof area/squares/bundles/sheathing | calculation-design.md: Right angles, roofs and rafters; Materials |
| Riser/tread counts, supplied riser limits, stringer/incline modes, stairwell opening/headroom/floor thickness | calculation-design.md: Straight stairs |
| Stud counts, linear/arched rake walls, compound miter and crown | calculation-design.md: Framing, rake walls and compound cuts |
| Length/width/height area/volume, sheets, blocks/footings, columns/cones, circle/arcs/segments and regular polygons | calculation-design.md: Dimensional/basic geometry; Materials |
| Trig and inverse trig | calculation-design.md: Dimensional, angular and basic geometry operations |
| Gravel type/density, bag mass/yield, editable coverage, explicit waste and ceiling purchase counts | calculation-design.md: Materials; persistence-design.md: Preset overrides and snapshots |
| Keypad/forms, preferences, persistent tape/memory and explicit clearing | interaction-design.md; persistence-design.md: Schema v1 and transaction contracts |
| Android/iOS, offline first launch/use, local persistence and data-loss/backup boundary | architecture-design.md; interaction-design.md: First launch/forms/failures; toolchain-design.md; persistence-design.md |

Coverage is a source-correspondence assessment, not executed mathematical or device evidence. No capability family was dropped or implementation silently authorized. The newly explicit regular-polygon and upper-floor-landing conventions follow user decisions.

## Gates

| Gate | Target and due checkpoint | State |
| --- | --- | --- |
| Requirements correspondence | All listed capability families mapped to explicit owning contracts; before design acceptance | Complete; self-review correspondence above, user-approved design |
| User design review | Four module contracts, schema, limits and pinned toolchain baseline; before specs become active | User approved 2026-10-24; modules activated |
| Document integrity | `spec_validate`, standalone Markdown structure/local-link/whitespace assertions, `git diff --check`, scoped Git inventory; final document snapshot | Passed: valid six-node graph, six active specs, local links/headings/frontmatter/whitespace consistent, no placeholders, Markdown-only changed-file inventory and no app/test/native/build artifacts |
| Mathematical review | Independent known-answer fixtures and cut-plane/geometry counterexamples defined in owning contracts; implementation acceptance | Not executed; design defines obligations only |
| Published compatibility | Exact Flutter/Dart/package releases and platform constraints from official metadata; before pin approval | Focused declared-constraint review complete; selected Flutter 3.47.8/Dart 3.13.7 and exact packages in toolchain-design.md. Full solve/build not executed |
| Resolved/build compatibility | Dependency resolution, Android/iOS builds and native SQLite packaging; first implementation bootstrap gate | Not authorized/executed |
| Behavioral durability/accessibility | Core, SQLite, device/offline/restart and screen-reader suites; feature acceptance | Not authorized/executed |

## Resources and continuity

No application processes, test databases, installations, downloaded SDK archives, or task-owned bulk artifacts have been created. Source research is read-only. Published sqlite3/path-provider package archives were read in memory only, with SHA-256 verification; no files were extracted or hooks executed. Source identities/digests are retained in toolchain-design.md. Repository Markdown and this record are the retained design evidence; no cleanup operation or blanket retention hold is implied. No independent agent review is claimed.

## Checkpoint history

- **2026-10-24:** inspected baseline and complete current specs; obtained the amendments above; created draft calculation/interaction graph nodes.
- **2026-10-24:** drafted all required calculation families and expression/memory behavior. Spec graph and draft whitespace/local-link checks passed. Source browsing supports definitions; no mathematical/application tests were executed.
- **2026-10-24:** drafted schema v1, strict quantity codecs, generation/revision barriers, current-operation receipts, transaction/refusal rules and SQLite acceptance cases.
- **2026-10-24:** the legacy Flutter manifest URL containing `/flutter/releases/` returned HTTP 404, aborting the first metadata script before Pub checks. Located the current official `/releases/releases_linux.json` and macOS URLs; both identify the selected stable commit. This was a source retrieval failure, not an application test failure.
- **2026-10-24:** Adoptium's assets API returned HTTP 403; the official public Temurin GitHub release API independently supplied JDK 21.0.13+9. Apple/Android readable pages did not expose all current compatibility-table rows; no complete native host/build compatibility claim is made from them.
- **2026-10-24:** direct Pub/Flutter source inspection exposed standalone test/test_api/analyzer conflicts. Selected SDK flutter_test instead of an incompatible latest standalone test package. Current toolchain/package source identities and limits are recorded; no resolver/build was run.
- **2026-10-24:** read all four resulting module specs and reconciled cross-contract details: typed codec ownership, empty-memory clear barriers, unavailable generation, square-area exactness, stair opening reference span, compound face-tilt reference, numeric-field parsing limits and canonical receipt hashing. Updated only approved goal amendments and architecture navigation. All capability families map to owning contracts above. Spec graph and six-spec Markdown/design-only checks passed.
- **2026-10-24:** user approved the complete module contracts and pinned baseline, retaining all execution gates and explicitly not authorizing implementation/closeout. Activated the four module specs. Inspected preceding draft checkpoints at commits `10b3188`, `659c0b5`, and `5021809`; final documentation/lifecycle changes are a separate worktree delta, not claimed to exist in those commits.

- **2026-10-24:** final `spec_validate` reported no issues and the goals-rooted graph contained all six specs. Standalone Python assertions passed for all Markdown structure/local links/whitespace, six active specs, absence of placeholders and absence of application/test/native/build artifacts. `git diff --check` passed; the final changed-file inventory contains only the seven intended Markdown documents. These checks do not validate solver execution or native compatibility.

## Delivery boundary

There are no unresolved product/architecture contract decisions from this design task. This is a design-readiness conclusion, not proof of mathematical correctness, a solved package graph, supported-device execution, or release readiness. No application code, manifests, lockfiles, native projects, tests, installed dependencies or running services were created. No independent review, hosted CI, signing, deployment, tracker synchronization, or branch/PR closure is claimed.

Execution prerequisites remain explicit: a scoped implementation grant, safe isolated bootstrap targets, the selected SDK/native toolchain, a Mac/Xcode/signing route when applicable, and real minimum-family/device environments. Their unavailable or unexecuted state blocks only the corresponding bootstrap/platform/feature acceptance. Future project planning should reconcile the actual GitHub tracker under a separately scoped remote-write grant; this local design record does not grant it.

## Subsequent authorized foundation delivery — 2026-10-24

The user separately requested implementation of project scaffolding, confirmed a clearly labeled unfinished app shell with no calculator/storage functionality, selected task-local SDK bootstrap, development identity `com.example.contractorcalc`, and GitHub checks without remote mutations, then explicitly approved the bounded design. Baseline was the clean `f0fe518` checkout. This grant superseded the preceding no-implementation boundary only for the foundation slice; no global installs, license acceptance, signing, device actions, or branch/PR closeout were authorized.

The root Flutter application now has generated Android/iOS projects, the exact approved direct dependencies and resolved lockfile, a Riverpod composition root, an unfinished foundation screen, module boundaries, normal-suite foundation tests, and shared local/CI verification. Architecture/toolchain owners describe the lasting decisions; [README.md](README.md) describes setup. No solver, schema, repository, onboarding, tape, memory, or preset behavior was added. iOS backup exclusion, native resolution locks and device suites remain storage/native implementation obligations rather than fabricated artifacts.

Observed local evidence on Linux x64:

- Official SDK metadata and installed identity agree on Flutter 3.47.8, commit `737ba8f885dc774b53b442759999a312c9461e4e`, Dart 3.13.7; Linux archive SHA-256 matched.
- Initial exact resolution and subsequent `flutter pub get --enforce-lockfile` passed without overrides; resolved analyzer 14.6.0 and SDK test_api 0.7.12 coexist. Full graph and dependency license-file inventory were inspected. SDK test packages inherit Flutter's root license; an inventory is not a complete redistribution/legal review.
- `bash tool/verify.sh` passed end to end: seven tooling tests, static native configuration checks, locked resolution, generation, formatting, analysis, five Flutter tests, and lock/generated-output drift checks. The core guard protects imports, not mathematical behavior; widget layout checks are not device accessibility acceptance.
- Flutter's template bundled a Gradle 2.10 wrapper; its comparison with the published 9.3.1 checksum failed. The official 9.3.1 JAR/launchers replaced it and the published JAR/distribution checksums matched. No version override or AGP/Kotlin integration change was needed.
- Original failed constructor analysis and widget semantics-resource-lifetime runs were corrected without removing assertions. A newly written static checker initially assumed an obsolete framework-plist key; it now checks iOS's actual project deployment declarations rather than imposing a nonexistent template field. Failed and final logs are retained under ignored `.local/evidence/`; source/locks and checks remain in Git-managed files.

Native Android/iOS builds, mobile SQLite version/features and packaging, both Android release ABIs, 16 KB environments, minimum/current-device installs, offline/restart/backup workflows, and screen-reader verification were not executed. Android/JDK and Mac/Xcode/device targets are unavailable here. No release, hosted-CI success, publication, independent review, tracker synchronization, or human implementation acceptance is claimed. The workflow file is configured, not remotely executed. These missing gates block their corresponding acceptance units, not the independently verified foundation.

Task-local retained resources at handoff: approximately 4.0 GiB `.toolchain/` (SDK/archive), 307 MiB `.local/` (caches and compact evidence), 79 MiB `.dart_tool/`, and 51 MiB `build/`. Bulk is reconstructible from the baseline/locks; original logs and unique diagnostics are compact evidence. No project byte threshold or automatic cleanup grant exists. The workspace owner decides SDK/cache reuse or release at the next handoff; no global/shared caches or human databases were changed or deleted. GitHub coordination remains pending a separately scoped grant. The next authorized stop is handoff for human review, not a subsequent feature slice or PR operation.
