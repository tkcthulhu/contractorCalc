# ContractorCalc design-readiness record

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

- Implementation has not started. Module contracts are being drafted for user review; draft status is not approval.
- Draft contract owners: `contractorcalc-interaction` / `interaction-design.md`; `contractorcalc-calculations` / `calculation-design.md`; `contractorcalc-persistence` / `persistence-design.md`.
- Interaction, numerical/solver, schema/transition and toolchain drafts are present. Toolchain owner: `contractorcalc-toolchain` / `toolchain-design.md`. Current action: cross-spec correspondence review, then obtain final user design approval. Consequential draft policies not already approved are not active contracts.
- This record owns progress/evidence. Durable contracts live only in their owning specs.

## Gates

| Gate | Target and due checkpoint | State |
| --- | --- | --- |
| Requirements correspondence | All listed capability families mapped to explicit owning contracts; before design acceptance | Pending |
| User design review | Draft module policies, schema and toolchain baseline; before specs become active | Pending |
| Document integrity | `spec_validate`, local Markdown links/frontmatter/whitespace assertions, scoped Git diff; final document snapshot | Pending |
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
- **2026-10-24:** direct Pub/Flutter source inspection exposed standalone test/test_api/analyzer conflicts. Selected SDK flutter_test instead of an incompatible latest standalone test package. Current toolchain/package source identities and limits are recorded; no resolver/build was run. Final cross-spec and user design review remain pending.
