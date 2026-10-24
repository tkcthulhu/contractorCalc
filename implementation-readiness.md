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
- Contract owners: `contractorcalc-interaction` / `interaction-design.md`; `contractorcalc-calculations` / `calculation-design.md`. Persistence and toolchain contracts follow before final reconciliation.
- Current action: finish numerical and specialized-solver definitions, then define storage schema and published toolchain compatibility. Consequential conventions not already approved require review before activation.
- This record owns progress/evidence. Durable contracts live only in their owning specs.

## Gates

| Gate | Target and due checkpoint | State |
| --- | --- | --- |
| Requirements correspondence | All listed capability families mapped to explicit owning contracts; before design acceptance | Pending |
| User design review | Draft module policies, schema and toolchain baseline; before specs become active | Pending |
| Document integrity | `spec_validate`, local Markdown links/frontmatter/whitespace assertions, scoped Git diff; final document snapshot | Pending |
| Mathematical review | Independent known-answer fixtures and cut-plane/geometry counterexamples defined in owning contracts; implementation acceptance | Not executed; design defines obligations only |
| Published compatibility | Exact Flutter/Dart/package releases and platform constraints from official metadata; before pin approval | Pending |
| Resolved/build compatibility | Dependency resolution, Android/iOS builds and native SQLite packaging; first implementation bootstrap gate | Not authorized/executed |
| Behavioral durability/accessibility | Core, SQLite, device/offline/restart and screen-reader suites; feature acceptance | Not authorized/executed |

## Resources and continuity

No application processes, test databases, installations, downloaded SDK archives, or task-owned bulk artifacts have been created. Source research is read-only. Repository Markdown and this record are the retained design evidence; no cleanup operation or blanket retention hold is implied. No independent agent review is claimed.

## Checkpoint history

- **2026-10-24:** inspected baseline and complete current specs; obtained the amendments above; created draft calculation/interaction graph nodes. Drafting and final design review remain in progress.
