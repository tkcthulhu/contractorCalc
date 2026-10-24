---
id: contractorcalc-goals
type: goal-and-requirements
status: active
title: ContractorCalc — Goal and Requirements
---

# ContractorCalc

Construction material estimates and common measurement calculations on the job.

## Overview

ContractorCalc is a mobile app for estimating construction materials and solving common construction measurement calculations.

## Problem

Repeated manual math and unit conversions during construction work create opportunities for mistakes. ContractorCalc reduces this repeated work and the associated conversion errors.

## Target Users

Contractors and tradespeople performing job-site calculations.

## Non-Goals

- Structural safety certification or jurisdiction-specific building-code compliance. Stair limits are user-specified constraints, not a claim of compliance.

## Capabilities

### Dimensional math and conversions

- Feet-inch-fraction, inch-fraction, and yard modes; decimal feet and decimal inches in tenths and hundredths.
- Preset fraction resolution from 1/2 inch through 1/64 inch. Fraction resolution and decimal display precision affect presentation only; chained calculations retain unrounded values.
- Metric measurements in meters, centimeters, and millimeters, with imperial–metric conversion.
- Length, area, and volume conversion between supported formats.
- Degrees:minutes:seconds ↔ decimal degrees.
- Weight-per-volume conversions, board feet, and total cost from a unit price.
- Display values up to 19.9 billion, with an optional thousands separator and a unitless decimal display.

### Right angles, roofs, and rafters

- Right-angle solver with Rise, Run, Diagonal, and Pitch keys; pitch expressed as slope, percent grade, or degrees.
- Common rafters, regular and irregular hip and valley rafters, and jack rafters with jack spacing.
- Plumb, level, and cheek cutting angles.
- Flat and pitched roof calculations: roof area, plan area, roofing squares, shingle bundles, and 4×8 sheathing count.

### Stairs

- Riser and tread counts, riser height, and tread width.
- User-specified riser height limit, stringer length, and stair incline angle. Flag conflicts with user-supplied stair limits.
- Stairwell opening, headroom, and floor thickness.

### Framing and walls

- Stud count for a given on-center spacing.
- Rake walls, including arched rake walls.
- Compound miter cuts and crown molding angles.

### Area, volume, and materials

- Square and cubic calculations using Length, Width, and Height keys.
- Drywall, siding, and paneling sheet counts for 4×8, 4×9, and 4×12 sheets.
- Concrete blocks and footings.
- Column and cone area and volume.
- Circle area, circumference, arcs, and segments, from basic to advanced calculations.
- Polygons with equal sides.

### Trigonometry

- Sine, cosine, tangent, and their inverses: arcsine, arccosine, and arctangent.

### Concrete and gravel

- Tons of gravel needed to fill a volume, based on gravel type.
- Bags of concrete needed to fill a volume, based on bag weight and mix yield.

### Material estimate assumptions

- Labeled, editable presets for gravel density, concrete bag yield, and roofing coverage; users can substitute supplier or manufacturer values.
- Sheet, bag, block, and shingle-bundle estimates show the calculated requirement and a whole-unit purchase count rounded up.
- An explicit waste percentage is available for these estimates and defaults to zero.

### Usability

- A calculator keypad for fast dimensional entry, plus labeled input forms and results for specialized tasks such as stairs and rafters.
- Paperless tape for reviewing recent entries.
- User-configurable preferences, including fraction resolution and display formats.
- Memory functions.
- Preferences, tape, and memory persist locally across app restarts. Users can explicitly clear tape and memory.

## Non-Functional Requirements

- Support Android and iOS.
- Every listed calculation, preferences, paperless tape, and memory must work locally without internet access or sign-in.

## Alternatives Considered

These references inform the product comparison; none is selected as a dependency. Undocumented features are not assumed absent.

- [Construction Master Pro](https://www.constructionmasterpro.com/): close commercial reference for dimensional math, imperial–metric conversions, roofs, and stairs with a handheld-calculator-style interface. No specific feature gap is established by this comparison.
- [BuildCalc](https://www.buildcalc.com/more-features-and-functions/): extensive documented overlap in stairs, rafters, rake walls, materials, and conversions; also documents input forms, contextual help, and layout drawings. No specific feature gap is established by this comparison.
- [Tradesman’s Field Calculator](https://github.com/alexneil/tradesmans-field-calculator): MIT-licensed React/TypeScript component and calculation engine with documented dimensional math and geometry solvers. Its documented scope is narrower than ContractorCalc’s full feature set.
