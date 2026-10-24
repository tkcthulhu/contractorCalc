---
id: contractorcalc-persistence
type: module-design
status: active
title: ContractorCalc — Local Schema and State Transitions
parent: contractorcalc-architecture
depends-on: [contractorcalc-architecture, contractorcalc-calculations]
references: [contractorcalc-interaction]
tags: [sqlite, persistence, integrity]
---

# Local schema and state transitions

## Owner and initialization

One background-isolate Drift/native SQLite owner serializes durable commands. Widgets/controllers use repository contracts, never direct SQL or parallel database connections for app writes. Pure quantity validation/arithmetic is owned by `contractorcalc-calculations`; interaction semantics are owned by `contractorcalc-interaction`.

Use one database, `CCData/contractorcalc.sqlite`, beneath the platform application-support directory. Exclude the entire CCData directory, database sidecars and metadata from automatic OS cloud backup. Resolve the actual platform path and verify Android backup/data-extraction rules and the iOS directory backup-exclusion attribute before data creation; do not assume an API's Dart name identifies an Android backup domain. If a platform cannot separate cloud and device-transfer exclusion, protect this directory from both and document the restriction. Do not promise automatic device-to-device portability or secure deletion of uncontrolled copies.

Initial schema version is **1**, owned by Drift/SQLite `user_version`. Create state/settings rows and the complete schema in a single fresh-install transaction; memory, tape and overrides start empty. A versioned existing database with missing singleton rows is corrupt/unavailable, not a fresh installation. Use SQLite transactions with WAL journaling, synchronous=FULL, foreign_keys=ON, and verified STRICT-table/JSON-function support; configure connection pragmas before schema transactions. SQLite commit is the acknowledgment boundary, not an absolute guarantee against broken hardware. No fallback disables constraints when packaging lacks a feature. No account or sign-in state exists.

## Scalar and serialization contracts

SQLite `INTEGER` scalars are signed 64-bit. Revisions/generations/timestamps range from 0 through 9,223,372,036,854,775,807; check increment capacity before any write. A full counter refuses with `storage_limit`; never wrap or reset. IDs are 128 random bits encoded as exactly 32 lowercase hexadecimal characters, generated locally from a cryptographic random source. IDs establish operation identity, not time or authentication.

Quantity codec version **1** is a validated tagged JSON object:

- `v`: integer 1; `kind`: one calculation-kind enum; `repr`: `rational` or `binary64`.
- Rational: `n` signed canonical decimal integer string and `d` positive canonical decimal integer string; gcd=1, zero 0/1, and core bit/range limits apply. No leading plus, leading zeros or negative zero.
- Binary64: `bits` exactly 16 lowercase hexadecimal digits encoding IEEE-754 bits in big-endian order; reject NaN/infinity, normalize negative zero to positive zero, and validate numerical bounds. Decode bits, not locale-dependent decimal text.
- Cost/price kinds additionally require `currency_label`, a nonempty plain-text label of at most 16 Unicode scalar values, default `currency units`; reject it on other kinds. There is no exchange operation.

Command-hash envelope v1 has exactly `v` (1), `action`, `expected_counter` (canonical nonnegative decimal string), and `payload` (validated object). Actions are `tape.clear`, `memory.store`, `memory.add`, `memory.subtract`, `memory.clear`, `config.update`, `preset.replace`, or `preset.reset`. Empty-action payloads are empty objects; values/targets are explicit in nonempty payloads. Canonical encoding sorts ASCII schema keys ascending at every level, preserves array order and Unicode scalar values, emits compact UTF-8 JSON with no whitespace, escapes quote/backslash/control characters only (controls as lowercase four-digit Unicode escapes), and emits small integer settings in minimal decimal notation. No binary floating-point JSON numbers occur: quantity values use the codec above, and counters use strings. Freeze the envelope for a retry; a new expected counter is a new explicit operation, not an automatic reassertion.

Canonical units follow `contractorcalc-calculations`; a quantity does not carry a second conflicting numeric display-unit value. The UI can request another compatible display unit without changing serialization. Codecs reject unknown discriminators, missing/extra fields, invalid strings/types and unsupported versions, rather than coercing them. Exact quantities never pass through JSON floating-point numbers or SQLite REAL.

## Schema v1

All v1 tables use SQLite STRICT mode. All columns are NOT NULL unless explicitly nullable. SQL CHECK constraints enforce scalar enums, length/range and JSON-object validity; validated adapters enforce strict pre-coercion inputs, typed payload shapes and domain invariants. SQLite affinity/STRICT mode is not a substitute for domain rejection of booleans or numeric strings. Use bound parameters. No user content is executable SQL or an expression-language program.

### `app_state` — singleton durable command barriers

`id INTEGER PRIMARY KEY CHECK(id=1)`; `tape_generation INTEGER DEFAULT 0 CHECK(>=0)`; `memory_revision INTEGER DEFAULT 0 CHECK(>=0)`; `config_revision INTEGER DEFAULT 0 CHECK(>=0)`; nullable TEXT `last_tape_clear_id`, `last_memory_operation_id`, `last_config_operation_id`, each constrained to the 32-character ID format when present. Each ID has a paired nullable TEXT `last_tape_clear_command_hash`, `last_memory_command_hash`, or `last_config_command_hash`, exactly 64 lowercase hex characters when present; a CHECK requires each ID/hash pair to be jointly NULL or non-NULL. Hash the versioned canonical JSON command envelope (action, expected counter and typed payload) with SHA-256. A matching ID with a different hash is an integrity error. Hashes detect conflicting operation reuse, not authenticity. The row is inserted on fresh creation and never deleted by application commands.

This table owns generations/revisions; do not duplicate competing counters in UI or child rows. Last-operation fields are bounded current receipts for ambiguous acknowledgments, not a permanent event ledger. They do not establish the outcome of arbitrary older operations.

### `preferences` — singleton validated display configuration

`id INTEGER PRIMARY KEY CHECK(id=1)`; nullable TEXT `unit_system` in `imperial|metric`; nullable TEXT `length_format` in `feet_inch|inch_fraction|yards|decimal_feet|decimal_inches|meters|centimeters|millimeters|unitless_decimal`; nullable TEXT `mass_unit` in `short_ton|tonne`; `fraction_denominator INTEGER DEFAULT 16` in `2,4,8,16,32,64`; `decimal_places INTEGER DEFAULT 2` in `1,2`; `angle_format TEXT DEFAULT 'decimal_degrees'` in `decimal_degrees|dms`; `thousands_separator INTEGER DEFAULT 0` in `0,1`.

An explicit SQL CHECK requires either all three nullable fields to be NULL (first-launch choice not saved) or all to be non-NULL valid enums; include explicit IS NULL/IS NOT NULL guards so SQLite's three-valued CHECK semantics cannot admit partial setup. Setup completion is derived from this shape, not a redundant flag. The default row has all three NULL. Choosing imperial sets feet_inch/short_ton; choosing metric sets millimeters/tonne, atomically with the user choice. Later individual format selections can differ from those initial defaults.

No per-row revision is duplicated here; configuration writes compare/increment `app_state.config_revision`. Waste is a calculation input with a zero default, not a hidden global multiplier. Locale is resolved for presentation, not used to reinterpret saved quantities.

### `memory` — independent one-slot quantity

`slot TEXT PRIMARY KEY CHECK(slot='M')`; `quantity_json TEXT` constrained to a JSON object and at most 16,384 UTF-8 bytes. An absent row is empty memory; a present zero quantity is populated memory. There is no FK to tape: clearing history cannot delete memory. The persistence codec delegates numerical/kind validation and compatibility to core value objects; it does not own another arithmetic implementation. Memory row contents are mutable only through the register coordinator and are governed by `app_state.memory_revision`.

### `tape_entries` — immutable variable calculation snapshots

- `seq INTEGER PRIMARY KEY AUTOINCREMENT`, strictly positive, is the stable ordering/cursor identity. SQLite's sequence is never manually reset when clearing. Exhaustion is a storage failure, not ID reuse.
- `operation_id TEXT UNIQUE`, constrained to the ID format; `generation INTEGER CHECK(>=0)`; `created_at_utc_ms INTEGER CHECK(>=0)`; `payload_version INTEGER CHECK(=1)`; `engine_version TEXT`, initially `calc-contract-1`.
- `operation_type TEXT` is one of `expression|right_angle|common_rafter|hip_valley|jack_schedule|roof|stairs|studs|rake_wall|compound_miter|crown|rectangle_box|circle_arc|column_cone|regular_polygon|material|board_feet|density|cost|dms|trig`.
- `request_json`, `result_json`, `assumptions_json`, `presentation_json`: TEXT JSON objects. Require `json_valid(column)=1`, object type, and combined UTF-8 payload length at most 1,048,576 bytes. Oversized snapshots produce a visible not-saved storage outcome; never truncate data to make a save pass.

The unique operation ID index plus the INTEGER primary key are sufficient initial indexes. Read descending by seq with a `seq < cursor` keyset and at most 100 rows per page; timestamps are informational, not unique/order authorities. No age/count retention index or background deletion exists.

Payload envelope fields are versioned:

- Request: `v=1`, stable solver `mode`, and normalized typed `inputs`; expression requests contain the typed token sequence, not source code. Mode-specific field sets/units are validated by the owning solver request type.
- Result: `v=1`, mode-specific typed `outputs`, and ordered structured `warnings` with code and typed details. Only successful results are stored; no error row is fabricated as a zero result.
- Assumptions: `v=1`, resolved `values`, and `presets` containing stable preset ID, catalog version, estimate/source label, original numerical values and override status. Store the values required to explain a result independently of future preset edits.
- Presentation: `v=1`, resolved format settings, locale tag, display units, and the original plain-text `summary`. It supports historical read-only display, never arithmetic or recall by parsing text.

Each mode uses a sealed/validated payload type, not a free-form Map accepted from widgets. Variable solver snapshots are appropriate JSON; identities, ordering, state and settings remain explicit columns. Unsupported historical payloads may show their stored summary with an unsupported-format warning, but must not be re-evaluated. Malformed payloads are isolated/reported without deleting the row or interpreting it as current valid numerical state.

Tape rows are immutable after insertion except explicit whole-tape deletion. Changing preferences affects future rendering/results, not saved historical presentation. Engine version changes when calculation behavior changes; old rows retain their recorded version/result rather than being recomputed on upgrade.

### `preset_overrides` — owned customization of bundled definitions

`preset_id TEXT PRIMARY KEY` (1…80 lowercase ASCII letters/digits/dot/underscore/hyphen); `category TEXT` in `gravel|concrete|roofing`; `label TEXT` (1…80 Unicode scalar values, at most 320 UTF-8 bytes); `payload_version INTEGER CHECK(=1)`; `definition_json TEXT`, JSON object at most 16,384 UTF-8 bytes.

The bundled catalog remains a versioned application asset, not mutable rows reseeded over user data. IDs are stable: `gravel.dry`, `gravel.wet`, `concrete.40lb`, `concrete.60lb`, `concrete.80lb`, `roofing.example_three_bundle`. Initial values and estimate labels are owned by the calculation contract. The adapter validates the ID/category against the known catalog and validates these complete override shapes:

- Gravel: `v=1`, positive density quantity, `source_label` plain text up to 256 Unicode scalar values.
- Concrete: `v=1`, positive bag-mass and per-bag-volume-yield quantities, and source label.
- Roofing: `v=1`, positive area-per-bundle quantity and source label.

Overrides are labeled user-provided/unverified, regardless of a supplier name typed into the source label. An override replaces that preset's entire validated definition; no half-updated mass/yield pair. Unknown IDs from newer catalogs are preserved but unavailable, not silently deleted/reassigned. Resetting an override deletes only that row and affects future calculations. Configuration revision governs override writes as well as display settings. No tape FK points at mutable definitions; snapshots carry their own resolved assumptions.

## Transaction and failure contracts

### Save a calculation

At evaluation start, capture current tape generation and a coherent resolved configuration/preset snapshot from a successful saved-state read. If that read is unavailable, do not substitute generation zero: calculate with explicit temporary choices and do not queue an automatic save. The pure calculation can finish without storage. Encode and validate the complete successful snapshot before entering the write transaction. Under the single writer:

1. Check the operation ID for a prior matching saved snapshot. Return its saved seq for the same operation; a conflicting reuse is an integrity error, not replacement.
2. Require the captured generation to equal current `app_state.tape_generation`; otherwise return `history_cleared`, without appending a late pre-clear calculation.
3. Insert the complete row and commit. A lost acknowledgment is reconciled by the same operation ID and generation, never by creating a new ID and replaying automatically. If the generation changed after a clear, refuse resurrection even if the old row is gone.

A new explicit Calculate action receives a new identity even for identical inputs. No semantic deduplication by content, timestamp or display text. On storage failure the valid calculation remains available as not saved; persistence failure is not a calculation failure. An automatic recovery refresh does not backfill temporary tape rows.

### Clear tape

First reconcile an identical current ID/hash receipt without clearing again. Otherwise, with the expected current generation and a fresh clear operation ID, check generation capacity, delete all tape rows, increment generation, and set the current clear ID/hash receipt in one transaction. Reject stale clear expectations after another clear. Repeated receipt acknowledgment does not perform a second clear; a new deliberate confirmed clear does. No preferences, memory, overrides or sequences are reset. Cancellation sends no durable command. An empty clear still advances the barrier to invalidate pending pre-clear results.

### Mutate memory

MS/M+/M−/MC carry an expected current memory revision. Inside one transaction, first reconcile an identical current ID/hash receipt, then for a new operation verify its revision, load/validate the current register, compute through the owning core if needed, update/delete the slot, increment revision and record the current operation ID/hash. Reject stale or incompatible requests without writes. Even an already-empty MC advances the clear barrier while leaving memory contents empty. Failed reads never initialize an implicit empty register. MR is read-only and unavailable when current saved state could not be loaded.

Do not retry a non-idempotent M+/M− blindly after an uncertain commit. If the current receipt matches, report that committed result; otherwise refresh current memory/revision and require a new explicit user action. A receipt for an older operation is not invented from the present register value.

### Change configuration or an override

First reconcile an identical current ID/hash receipt without reapplying. For a new operation compare expected configuration revision; validate the complete final settings/definition; update the intended row(s), increment configuration revision, and store the current operation ID/hash atomically. Reject stale edits rather than overwrite newer choices. An explicitly temporary UI preference during storage failure is not promoted to committed settings. Restoring persistence re-reads saved state; the user may deliberately save a new choice afterward. Past tape snapshots remain untouched.

### Initialization, migration and corruption

Only fresh creation inserts defaults. Schema migration is ordered, transactional and non-destructive; known payload versions have explicit decoders/upgraders. Version 1 has no fictitious older upgrade path. Every subsequent schema version must test all supported historical fixtures and preserve raw quantities, empty-versus-zero memory, overrides, tape order/presentation and barriers.

A migration or startup-integrity failure preserves the database and exposes saved-state unavailable while pure calculations can use explicitly temporary choices. Refuse unsupported newer schemas and lossy downgrade; do not reset, drop tables, replace malformed values with defaults, or automatically delete corrupt tape rows. Backup files or repair/export features require separate contracts; this design authorizes none.

The application coordinator enforces singleton existence, current generation/revision, codec validity and whole-operation invariants. SQL enforces structural constraints and uniqueness but does not by itself prove these cross-row/domain properties. No triggers or model hooks claim to secure arbitrary raw SQL. Tests must exercise both layers and deliberately malformed raw rows.

## Acceptance gates

Use the actual packaged SQLite engine with isolated synthetic database files. Required suites exercise fresh schema/defaults, raw valid/invalid inserts for CHECKs/uniqueness/JSON shape, strict codec round trips including exact rationals and binary64 bits, positive/negative/zero/malformed data, singleton loss detection, and integer/UTF-8 payload limits.

Through real repository/coordinator entry points test every command, repeated IDs versus new identical operations, empty clears, stale revisions, delayed pre-clear calculations, each ordering of a write and clear, lost-acknowledgment reconciliation, deliberate exception after an early write, and enclosing rollback. Verify raw rows/counters and protected categories, not only UI projections. Close and reopen real files to prove persistence. Device tests verify backup exclusion of the resolved directory and sidecars, first launch offline, process termination/restart, storage-unavailable warnings, and no reset on unsupported schema. No such tests have been executed by authoring this spec.
