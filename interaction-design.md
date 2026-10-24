---
id: contractorcalc-interaction
type: module-design
status: draft
title: ContractorCalc — Calculator and Interaction Contracts
parent: contractorcalc-architecture
depends-on: [contractorcalc-architecture, contractorcalc-calculations]
tags: [calculator, interaction]
references: [contractorcalc-persistence]
---

# Calculator and interaction contracts

## Responsibility and boundary

This module owns entry, expression editing, memory commands, presentation preferences, and user-visible save states. It invokes `contractorcalc-calculations` for arithmetic and solvers and the persistence contract for writes. It contains no duplicate formulas. The framework and offline boundaries in `contractorcalc-architecture` apply.

## First launch and preferences

First launch offers an offline **Imperial / Metric** choice without permission prompts, sign-in, downloads, or a building-code jurisdiction. Imperial starts in feet-inch-fraction at 1/16 inch; metric starts in millimeters. Both start with decimal precision **two places**, angles in degrees, thousands separators off, and waste zero. Tenths remains a selectable decimal preference. Fraction denominators are 2, 4, 8, 16, 32, or 64. Unit choice and individual display preferences remain editable after setup.

The platform locale supplies the decimal symbol and grouping presentation, not unit-system inference. Keypad tokens are structured. Forms accept the active locale's decimal symbol, an optional leading sign, and digits; reject grouping separators, alternate ambiguous separators, and mixed-locale text with a field-specific message. A displayed number is never reparsed for calculation. A storage failure during setup permits an explicitly temporary session choice; it does not mark setup durably complete or silently replace existing unreadable preferences.

Decimal output rounds to the selected one or two places, with two places the default, including trailing zeros. Fraction output rounds to the selected inch increment, reduces the fraction, and carries inches/feet correctly. Nearest rounding uses exact ties **away from zero**, applied to the signed quantity as a whole. Formatting a small negative value as zero removes the minus sign. Display rounding never changes calculations, memory, tape data, or purchase counts.

At absolute selected-unit magnitude above 19,900,000,000, use scientific notation with eight significant digits and an explicit unit. In compound feet-inch mode, use decimal feet for this fallback and label it. A nonzero value that would display as zero at the selected precision receives a visible smaller-than-one-display-increment indication and access to scientific notation; do not imply the stored quantity is zero.

## Expression model

The visible expression is a sequence of typed quantity, operator, grouping, and named-function tokens; never execute raw Dart text. Numeric and complexity limits are owned by `contractorcalc-calculations`.

Precedence is grouping/named functions, then unary sign, then multiplication/division, then addition/subtraction. Binary operators at the same level associate left. Multiplication is explicit: adjacent quantities or `2(3)` without a multiplication token are invalid. The sign key changes the current quantity's sign, not an arbitrary earlier term. A function has an explicit argument, e.g. `sin(30°)`; inverse trig takes a scalar and returns an angle. A root operation checks the resulting dimension. No context-dependent percent or undocumented repeated-operation semantics are implied.

- Plain numbers are unitless. Unit keys attach a compatible unit to the current numeric quantity; explicit conversion changes an existing quantity's display unit without changing its value. Do not relabel 2 feet as 2 meters.
- A feet-inch entry combines nonnegative feet, inches, and fraction components into one quantity. A leading sign applies to the whole measurement; reject embedded negative components. Nonnegative excess inches normalize by carrying. A zero fraction denominator is invalid. An entry such as `5 ft 2 1/2 in` is one length, not implicit expression multiplication.
- Fractions use a structured numerator/denominator entry; a binary divide token remains expression division. Fraction resolution limits output, not accepted exact fractions.
- The Length/Width/Height and Rise/Run/Diagonal/Pitch keys assign explicitly labeled quantity fields in their task panel. A scalar can acquire a field's visibly selected unit only through that assignment; core APIs never infer units from field names. Pitch explicitly distinguishes rise per 12 inches of run, rise/run ratio, percent grade, and degrees.
- `=` evaluates the complete expression. Missing operands, mismatched grouping, dimension errors, domain errors and range errors leave the expression editable and the previous valid result intact; the old result is visually distinguished from the failed expression.
- Successful `=` displays the new unrounded result and requests one tape append. Repeating `=` without an edit is a no-op and adds no tape entry. After a result, a binary operator starts a new expression with the unrounded result as its first quantity; a digit starts a new expression. Do not reuse a hidden earlier operand.
- Backspace edits the current input token or deletes the preceding operator/grouping token. AC clears transient expression/task-entry state, not tape, memory, saved presets, or preferences. Do not automatically restore unfinished drafts across process restart.

Required examples: `2 + 3 × 4 = 14`; `(2 + 3) × 4 = 20`; `8 ÷ 2 × 2 = 8`; `2 ft + 6 in = 2.50 ft` when formatted as decimal feet; `2 ft × 3 ft = 6 ft²`; `2 ft + 3 ft²` fails unchanged. At hundredths, displaying `1 ÷ 3` as `0.33` and then multiplying its result by 3 yields exactly 1.

## One typed memory register

A register is empty or contains one unrounded typed quantity. Display an M indicator for a populated register, including stored zero. Commands use the current valid result or a complete single-quantity entry; do not implicitly evaluate an incomplete/failed expression.

- **MS:** replace the register with that quantity after a successful durable write.
- **MR:** insert the stored quantity as one expression operand, replacing the active operand or starting a new expression after a result. Preserve its type/value and current display preferences. Empty MR is a visible empty-memory no-op, not insertion of zero.
- **M+:** if empty, store the quantity; otherwise add only a compatible quantity using core arithmetic.
- **M−:** if empty, store its negation; otherwise subtract only a compatible quantity using core arithmetic.
- **MC:** explicitly clear the register, independently of tape and preferences. Clearing already-empty memory is a successful no-op.

A dimensional/domain/range rejection leaves memory untouched. A storage failure reports that memory did not save; it does not promote a temporary replacement into the durable register. Disable mutation when saved memory could not be read; do not treat an unreadable register as empty. MR is unavailable when the saved register could not be read; a last-known display may remain labeled stale but is not silently inserted as current memory. Memory commands are not separate tape calculations; their persisted state is the register, not an implied memory event ledger.

## Forms, tape and failures

Specialized forms submit explicitly labeled typed inputs to their owning solver. Calculate validates all required fields before calling it, preserves user input on failure, and displays assumptions/warnings with successful results. Merely editing a field or changing presentation never writes a tape entry. Each deliberate successful Calculate action is a new tape operation even if its inputs match an earlier action.

Tape contains successful evaluated expressions and specialized calculations, with the entry order and snapshot contract owned by persistence. Failed calculations, partial keystrokes, preference changes, and memory commands do not append entries. A repeated `=` no-op adds nothing. Clearing tape requires explicit confirmation; cancellation changes nothing. MC acts only on memory and has a distinct accessible control. There is no implicit tape replay or undo feature.

Storage status is visibly separate from calculation status: saving, saved, not saved, and saved-state unavailable are not equivalent. Pure calculations continue during storage failures, but temporary tape rows are labeled not saved and are not silently backfilled after recovery. Preferences can be used temporarily with a warning; failed clears leave existing committed data present. User actions can retry explicitly after refreshing current state. Do not claim durable success on optimistic UI state alone.

Database cloud backup is excluded on Android and iOS, including SQLite journal/sidecar files and metadata. Android backup/data-extraction rules and the iOS backup-exclusion resource attribute must be tested; do not disable the entire app sandbox or security protections. Device transfer behavior is documented and tested separately from cloud backup. No manual export or sync is added here. Explain that uninstalling, clearing app data, or losing a device can lose local state; exclusion is not a secure-erasure guarantee for copies outside the app's control.

## Acceptance

Normal widget/controller tests cover all expression examples, editing transitions, signed fraction carry, both decimal precision options, locale ambiguity rejection, unit assignment versus conversion, memory empty/zero/type behavior, and failure preservation. Android/iOS workflows cover offline first launch, visible unit selection, accessible labels/focus, text scaling, saved/not-saved states, explicit clear confirmation, process restart, and backup exclusion. Calculation answers and durable transitions are also tested through their real owners, not only mocked providers.
