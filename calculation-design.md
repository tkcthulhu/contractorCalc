---
id: contractorcalc-calculations
type: module-design
status: active
title: ContractorCalc — Numerical and Solver Contracts
parent: contractorcalc-architecture
depends-on: [contractorcalc-architecture]
tags: [calculation, numerical-integrity]
---

# Numerical and solver contracts

## Owner, API and units

This pure Dart module is the only mathematical authority for `contractorcalc-goals`. It accepts validated typed requests and returns immutable results, assumptions and warning codes, or a typed failure. UI parsing is owned by `contractorcalc-interaction`; repositories supply snapshots, never formulas. No Flutter, storage, network or clock dependency is allowed.

Each public solver has a named request mode, explicit units and only the independent inputs for that mode. Missing, zero and invalid are distinct. Reject booleans, numeric strings, non-integral counts, unknown enums, incompatible dimensions and non-finite inputs at the core boundary; the UI parser converts valid text first. Reject overspecified or incomplete modes rather than silently choosing which input wins. A successful warning result is distinct from a failure; failures never mutate input, memory or tape.

Canonical quantity kind identifiers are `scalar`, `length` (m), `area` (m²), `volume` (m³), `mass` (kg), `density` (kg/m³), `cost` (currency units), `price_per_length`, `price_per_area`, `price_per_volume`, `price_per_mass`, and `angle` (degrees). A per-item/scalar price has kind `cost`, with its pricing basis explicit in the request; do not introduce a second incompatible kind for identical currency units. Supported products/quotients must resolve to one of those kinds; otherwise return `dimension_mismatch`. Same-kind division produces a scalar. Add/subtract require matching kinds. Angles scale by scalars, but are not interchangeable with scalars; trig functions consume angles and inverse trig consumes scalars. Cost uses the entered currency-unit label, with no exchange, tax or jurisdictional assumptions; incompatible currency labels cannot be combined.

Exact definitions: inch = 0.0254 m; foot = 12 inches = 0.3048 m; yard = 3 feet; centimeter = 0.01 m; millimeter = 0.001 m. Derive square/cubic factors from these definitions, not rounded tables. Pound = 0.45359237 kg; US short ton = 2000 pounds; metric tonne = 1000 kg. Do not label the last two ambiguously as interchangeable tons. A board foot is 144 in³ = 1/12 ft³; a roofing square is 100 ft². Survey feet are not used.

## Representation and technical limits

- Decimal and fraction literals become normalized `BigInt` rationals directly. Zero is 0/1; denominators are positive; reduce by gcd. Retain exact results through rational arithmetic and square roots whose reduced numerator and denominator are perfect squares.
- Other roots/trig and π-based geometry produce a tagged finite binary64 approximation. Mixed arithmetic converts at that explicit boundary. Conversion overflow or a nonzero value underflowing to zero is `numeric_range`, not a fabricated valid zero.
- Maximum literal: 64 significant decimal digits and a scientific exponent in −100…100; maximum expression: 256 tokens and 32 nested groups/functions. Maximum normalized rational numerator and denominator: 4096 bits each. Bound unreduced intermediates before allocating products (8192 bits), then require normalized results within the limit. Arithmetic exceeding a limit fails without changing prior state.
- Absolute canonical magnitude is at most 10^100, independently of the smaller normal display range. Exact nonzero values may be smaller than binary64 can represent; an operation requiring an unrepresentable approximation refuses. Exact degree angles reduce modulo 360 before trig conversion; approximate input angles above 10^9 degrees refuse because argument reduction is unreliable.
- Generated schedules have at most 10,000 rows; regular polygon side counts are integers 3…10,000. Refuse `complexity_limit` before generating oversized schedules. Aggregate material counts remain exact integers within the rational limit; they are not truncated to a SQLite integer.
- `division_by_zero`, `dimension_mismatch`, `invalid_input`, `incomplete_input`, `contradictory_input`, `geometry_domain`, `numeric_range`, and `complexity_limit` are distinct failure categories. Internal implementation faults are not converted to successful results.

The domain owns purchase ceiling and discrete geometry decisions. Presentation-only nearest/tie rounding is owned by interaction. For approximate positive purchase ratios, apply ceiling to the unrounded computational ratio; do not snap down to a nearby integer. If within 10^-10 × max(1, |ratio|) of an integer, return `near_purchase_boundary` so the displayed estimate does not imply unjustified certainty. Exact rational ratios use exact ceiling without this warning.

Do not use one epsilon to excuse invalid user inputs. Supplied negatives and out-of-domain values fail exactly. Only derived binary64 inverse-trig arguments may be clamped to [−1,1] within 32 machine epsilons; larger excursions fail. Derived negative squared lengths may be clamped to zero only within 32 epsilons of their operands' scale. Reject tan when |cos(angle)| ≤ 10^-12. Near-singular plane intersections likewise refuse with `ill_conditioned_geometry` rather than emit unstable cuts.

Known-answer approximation tests use |actual−expected| ≤ max(10^-12 in the output's canonical unit, 10^-10 × |expected|); tiny nonzero and boundary fixtures also require appropriate relative/sign/domain assertions. This is an acceptance-fixture tolerance, not a universal error guarantee for arbitrarily ill-conditioned inputs. Exact fixtures require exact rational equality.

## Dimensional, angular and basic geometry operations

Length/Width/Height give rectangle area LW and box volume LWH. Square and cube apply repeated multiplication with dimension checks. Nonnegative geometric sizes are accepted where zero denotes no material; divisors and dimensions needed to define an angle/radius must be positive. Negative signed quantities remain valid for general arithmetic but are rejected where a physical size cannot be negative.

DMS is one leading sign with nonnegative degree/minute/second components, minutes < 60 and seconds < 60; decimal degrees = sign × (degrees + minutes/60 + seconds/3600). Preserve rational degrees; output rounding carries seconds into minutes/degrees. Sine/cosine/tangent use degrees converted internally to radians. Inverse ranges are asin [−90°,90°], acos [0°,180°], atan (−90°,90°). Reject user asin/acos inputs outside [−1,1].

Circle radius r gives diameter 2r, circumference 2πr, area πr². Accept diameter as an alternate independent mode; reject negative r. A circular arc uses r > 0 and sweep θ in [0,360°], converted to radians t: length rt, chord 2r sin(t/2), sector area r²t/2, segment area r²(t−sin t)/2, sagitta r(1−cos(t/2)), and segment perimeter arc+chord. A chord/radius mode must choose minor or major: t_minor = 2 asin(c/(2r)), t_major = 2π−t_minor, with 0 ≤ c ≤ 2r. Chord c > 0 and sagitta h > 0 determine r = c²/(8h)+h/2 and t = 4 atan2(2h,c), supporting minor and major segments without silently selecting one. Zero sagitta cannot define a finite radius in that inverse mode. Use stable small-angle evaluation or refuse if the contracted residual cannot be met; do not substitute an approximate field formula without validation.

A right circular column/cylinder uses r,h ≥ 0: base πr², lateral area 2πrh, total closed surface 2πr(h+r), volume πr²h. A right circular cone uses r,h ≥ 0: slant √(r²+h²), lateral area πr×slant, closed surface lateral+πr², volume πr²h/3. Label base/lateral/total area separately; no hidden choice about including end caps.

A convex regular polygon uses integer n and exactly one of side a > 0, apothem q > 0 or circumradius R > 0. Let u = π/n. Convert by q = a/(2 tan u), R = a/(2 sin u), a = 2q tan u = 2R sin u. Return perimeter na, area naq/2, central angle 360°/n and interior angle 180°−360°/n. For n=4, compute area directly as a², 4q² or 2R² from the selected input so an avoidable trig approximation does not contaminate an exact square area. This is not an arbitrary equilateral-polygon solver.

## Right angles, roofs and rafters

### Right-angle solver

Rise H ≥ 0, run R > 0, diagonal D and pitch p = H/R obey D² = H²+R². Supported independent modes: H+R; H+D with D > H; R+D with D ≥ R; R+pitch; H+pitch with H,p > 0; D+pitch with D > 0 and p ≥ 0. Derive R = D/√(1+p²), H = pR as needed. Pitch input is explicitly ratio p, rise per 12 inches (12p inches), grade 100p%, or angle atan(p) in [0°,90°). H=0 with pitch=0 alone is underdetermined, not a zero-size triangle. Return missing/contradictory modes explicitly.

### Common rafter and roof area

A common rafter takes the wall-to-ridge horizontal run R > 0, rise H ≥ 0 (or pitch), and horizontal eave overhang o ≥ 0. Pitch p = H/R, gross centerline length (R+o)√(1+p²). Explicit along-centerline end deductions d1,d2 ≥ 0 yield net length gross−d1−d2; reject a negative net length. Defaults are zero deductions, not guessed ridge thickness, birdsmouth depth, or stock-length allowance. Label gross theoretical and adjusted lengths separately.

A roof is a list of non-overlapping horizontal-plan facet areas Ai ≥ 0 with pitch pi ≥ 0: plan area ΣAi, surface area ΣAi√(1+pi²). Flat roofs have p=0. A rectangular mono-pitch facet has plan area (length+two explicitly supplied end overhangs) × (wall-to-wall width+two explicitly supplied eave overhangs). A gable has common wall-to-ridge rise H, separate positive wall-to-ridge runs R1,R2, pitches H/Ri and facet plan areas (length+two end overhangs) × (Ri+that side's eave overhang). Set overhang inputs to zero when dimensions already include them; never add one twice. General facet mode accepts explicit already-adjusted Ai values and does not infer overhang geometry. The app does not infer intersecting roof layouts or subtract openings that were never supplied. Surface area feeds roofing squares, bundles and 4×8 sheathing through the common material estimator.

### Regular/irregular hip or valley centerlines and jacks

Use a horizontal eave corner at the origin, two eave rays enclosing angle φ in (0°,180°), common reference eave elevation 0, positive pitches p1,p2, and a common target rise H > 0. Ray 1 is the +x axis; its inward normal is n1=(0,1). Ray 2 has direction (cos φ,sin φ) and inward normal n2=(sin φ,−cos φ). Roof planes are z=pi(ni·r). Solve y=H/p1 and x=(H/p2 + y cos φ)/sin φ. The intersection runs from (0,0,0) to (x,y,H); length √(x²+y²+H²). The endpoint must satisfy n1·r > 0 and n2·r > 0 inside the chosen wedge; x need not be positive for an obtuse wedge. Refuse normalized intersection determinants with absolute value ≤ 10^-12. φ=90° and p1=p2 is the regular case; unequal pitches are not replaced by a 45° assumption.

Hip/valley selection identifies convex/concave roof orientation and mirrors the joint diagram; it does not change the centerline metric. This model uses equal eave elevations and explicit endpoints. For nonzero extension/deduction, use labeled distances along the centerline, not an assumed equal horizontal overhang for unequal pitches. Do not claim a rough timber cut length or structural roof layout from this centerline model.

Jack schedules are computed separately for each roof face. A side supplies first offset f > 0, on-center spacing s > 0 and eave-span limit E ≥ f, measured from the corner along that face's ray. For each e=f+k s ≤ E, intersect the ray from that eave point in the face's inward-normal direction with the hip/valley plan line. Retain only intersections strictly between corner and the target endpoint; exact endpoint jacks are reported separately as common/end rafters, not duplicated. Height is pi times that jack's horizontal run; length is run√(1+pi²), followed by explicit along-line deductions. Return station, run, rise, gross/net length and cut references. Validate list size before generation; reversing the input origin must not silently reverse station meaning.

### Cut-angle reference model

Every cut result includes an oriented diagram/reference frame, not an unlabeled degree. For a board, +X runs toward its upper/end joint, +Y lies in its broad side face toward its top edge, and +Z=X×Y is the face normal. For a rafter, X follows the rising centerline, Y is in its vertical plane, and Z is horizontal. A cut plane has a unit normal N in world coordinates; transform to local (nx,ny,nz) by dotting with this basis and select the sign with nx ≥ 0. The canonical saw-plane convention is miter M=atan2(ny,nx), bevel B=atan2(nz,√(nx²+ny²)); reconstruction is (cos B cos M, cos B sin M, sin B). Refuse a cut parallel to board length, where this convention is singular. These are reference-plane angles, not a promise that every saw's scales/signs match.

For a common rafter with incline α, a plumb plane has horizontal normal along its plan run; a level plane has vertical normal. Thus plumb line angle to the rafter edge is 90°−α (from square α); level line angle to the edge is α (from square 90°−α). A jack cheek plane is vertical through the hip/valley plan line; use its horizontal perpendicular as N, then transform in the jack's frame. Hip/valley double-cheek faces use the corresponding explicitly selected adjoining member's side-plane normal. Do not collapse all unequal-pitch cheek angles to 45°. Return each face's plane/reference and distinguish line-mark angles from canonical miter/bevel.

## Straight stairs

The upper floor is the landing. Total finished-floor rise H > 0 and a supplied integer riser count N in 2…10,000 give riser h=H/N and tread count T=N−1. Alternatively a supplied maximum riser hmax > 0 chooses N=max(2,ceil(H/hmax)), refusing a count above 10,000; no code-derived hmax is assumed. Explicit N is never silently changed to satisfy hmax; return `riser_limit_conflict` if h exceeds it.

After N is selected, exactly one independent going mode is supplied: tread going g > 0; total going G > 0, giving g=G/T; incline θ in (0°,90°), giving g=h/tan θ; or theoretical pitch-line stringer L > H, giving g=√(L²−H²)/N. Return G=Tg, virtual pitch-line run P=Ng, incline atan(h/g), and theoretical stringer L=√(H²+P²). The distinction between G and P is explicit. Theoretical stringer length excludes fastening, bearing, tread/riser thickness, nosing and stock trimming allowances; it is not a finished cut length. An optional user maximum stringer length flags a conflict without changing the chosen layout.

Headroom is vertical clearance from the straight nosing pitch line to the underside of the finished upper floor. Let floor thickness F ≥ 0, opening O ≥ 0 measured horizontally back from the upper landing nosing, and pitch θ. Clearance at the opening edge is O tan θ−F. A required clearance C > 0 needs O_required=(C+F)/tan θ. Exactly one of supplied opening or target headroom determines the other. A negative achieved clearance or an opening O > P beyond the modeled pitch-line span is a conflict warning, not a clamped success. Show this reference geometry and state that it is a straight-line estimate, not a jurisdictional compliance decision. Never substitute slope-normal clearance for vertical headroom.

## Framing, rake walls and compound cuts

A straight wall of length L > 0 and on-center spacing s > 0 places studs at x=0, each k s strictly inside the span, and x=L. Count is ceil(L/s)+1. Endpoints are not duplicated when L is an exact multiple. Optional extra studs are an explicit nonnegative integer addition; do not infer corners, openings, king/jack studs, headers or load-bearing adequacy.

Linear rake top profile is h(x)=h0+(h1−h0)x/L, with nonnegative endpoint heights. For an arched rake, the profile is an explicitly chosen upper/lower circular branch h(x)=cy ± √(r²−(x−cx)²), with r > 0, center (cx,cy) and span contained within the branch domain. The form offers a symmetric arch using span L and sagitta a in (0,L/2], radius r=L²/(8a)+a/2, cx=L/2, cy=h_end+a−r, upper branch; advanced center/branch inputs permit unequal endpoint heights. A signed concave counterpart uses the lower branch and explicit center. This is a circular arch, not an inferred ellipse or parabola. Validate that the entire chosen profile is defined and nonnegative over the span, including interior extrema. At each stud station, cut height is h(x) minus an explicit vertical plate deduction d ≥ 0. Reject negative heights rather than discarding the stud. Return stations and heights, not guessed joinery allowances.

Compound miter is a symmetric pair of straight members meeting at plan interior angle C in (0°,180°), with the same installed broad-face tilt β above horizontal, measured about each member's longitudinal axis. This is cross-sectional face tilt, not longitudinal incline; for cutting, each broad face is laid flat on the saw table. In the canonical board frame above, one face normal is (sin(C/2), cos β cos(C/2), sin β cos(C/2)); the mirrored member reverses the last two components. Derive canonical M/B from those vectors. Thus |M|=atan2(cos β cos(C/2),sin(C/2)) and |B|=asin(sin β cos(C/2)). Require β in [0°,90°]; label inside/outside retained faces and mirrored orientation, rather than guessing a saw-specific sign.

For crown molding laid flat, spring S in (0°,90°) is measured from the wall; β=90°−S. Return the same canonical plane angles. For a nested crown, distinguish the setup: |M|=(180°−C)/2, B=0. A 38° spring at a 90° corner laid flat gives approximately |M|=31.619° and |B|=33.859°; nested gives 45°/0°. The diagram must specify material face and retained side; do not interchange wall angle with turning angle (180°−C), or spring angle with its complement. These calculations are geometric, not manufacturer-specific tool instructions.

## Materials, concrete, gravel and cost

Every estimate starts from supplied nonnegative net area or volume. Rectangular slabs/footings use LWH; circular footings/columns use πr²h. Multiple components sum explicitly; no overlap, opening, compaction or waste is inferred. Waste w is supplied in percent, defaults to zero and lies in [0,1000]; multiply the raw requirement once by 1+w/100. Negative inputs reject. Coverage/yield and density must be positive. Zero target yields zero purchase units.

- Drywall/siding/paneling: area divided by selected 4×8, 4×9 or 4×12 foot sheet area. Roof sheathing uses 4×8. Return raw count, waste-adjusted count and ceil(adjusted count). These are area-coverage estimates, not sheet nesting or cut-layout optimization.
- Concrete blocks: net wall area divided by user-confirmed nominal face coverage, initially 16×8 inches including the stated joint allowance. Report raw and purchase count; no grout/rebar/header requirements are inferred.
- Roofing: surface area/100 ft² gives roofing squares. Bundles use actual editable area per bundle, not rounded roofing squares; never round squares before deriving bundles. The example preset is 100/3 ft² per bundle, explicitly labeled a three-bundles-per-square assumption, not universal product coverage.
- Concrete bags: adjusted volume divided by selected mix yield per bag. Bag mass is metadata; never infer yield from weight alone. Example presets: 40 lb → 0.30 ft³, 60 lb → 0.45 ft³, 80 lb → 0.60 ft³, all labeled illustrative normal-weight mix yields, editable and not manufacturer certification.
- Density conversion modes accept exactly two of mass M ≥ 0, volume V > 0, and density ρ > 0: M=ρV, V=M/ρ, or ρ=M/V. A supplied zero mass can produce zero volume, but cannot establish a positive material density; report the invalid density rather than divide by zero.
- Gravel: adjusted volume × selected bulk density gives mass. Initial density estimates are dry gravel 1680 kg/m³ and wet gravel 2000 kg/m³, with moisture/compaction variation disclosed and supplier replacement encouraged. Select US short tons or metric tonnes explicitly. No extra compaction multiplier is added.
- Board feet: volume/(144 in³), equivalently thickness_inches × width_inches × length_feet /12. Dimensions are actual entered values, not inferred dressed/nominal lumber sizes.
- Total cost: supplied nonnegative quantity or purchase count × nonnegative entered price per the same explicit unit basis. Distinguish theoretical-quantity cost from whole-unit-purchase cost; do not apply waste or ceiling twice. Currency labels are metadata, not an exchange-rate service; cost display uses the selected decimal precision without rounding intermediate arithmetic.

Preset identity, catalog version, source/estimate label, resolved numerical values, units and any user override are included in the calculation's assumption snapshot. Defaults are estimates and cannot be presented as supplier-verified facts. Resetting an override changes future calculations only, never past tape results.

## Independent acceptance examples

These are required expected results for future normal-suite tests, not executed verification:

- 1 inch = exactly 25.4 mm; 1 yard = exactly 914.4 mm; 1 ft³ = exactly 0.028316846592 m³; 1 US short ton = exactly 907.18474 kg. Round-trip exact fractions with no drift across display changes.
- 1/3 × 3 = exactly 1; at hundredths ±1.235 displays ±1.24; 11 63/64 inches at 1/16 resolution carries to 1 foot. Nonzero tiny quantities do not falsely become stored zero.
- Rise 3 ft/run 4 ft → diagonal exactly 5 ft, pitch 0.75, grade 75%. A diagonal shorter than its supplied leg rejects.
- A 90° equal-pitch hip at rise 6 ft and each pitch 0.5 ends at (12,12,6) ft with length exactly 18 ft. At first-side eave station 2 ft, its jack has run 2 ft, rise 1 ft and length √5 ft. Unequal-pitch and non-90° cases must satisfy both plane equations, not only an expected length.
- H=112 in, hmax=7 in and g=10 in → N=16, T=15, h=7 in, G=150 in, P=160 in, L=√38144 in and θ=atan(0.7). With F=12 in and C=80 in, required opening is 920/7 in. Explicit N=15 warns because 112/15 > 7.
- A 10 ft wall at 16 in spacing has 9 studs including endpoints. Linear heights from 8 ft to 10 ft yield 8 ft at x=0 and 10 ft at x=10 ft; a symmetric span-10 ft, sagitta-2 ft arch at end height 8 ft has radius 7.25 ft, circle-center height 2.75 ft and midspan top height 10 ft.
- Circle r=1 m → area π m²; a 180° sweep gives segment area π/2 m², chord 2 m and arc π m. Cone r=3 m/h=4 m → slant 5 m, volume 12π m³, closed surface 24π m². Regular square side 2 m → perimeter 8 m and area 4 m².
- 100 ft² / 4×8 sheet = 3.125 sheets, purchase 4; at 10% waste = 3.4375, purchase 4. 1 ft³ / 0.6 ft³ bag = 5/3 bags, purchase 2. 1 m³ dry gravel → 1680 kg = 1.68 metric tonnes. 100 ft² of roof with example bundle coverage → exactly 3 bundles before waste.
- Invalid signs/counts, zero divisors/yields, incomplete/contradictory modes, tangent singularities, circle branch ambiguity, unsupported dimensions, out-of-range AST/schedules and near-boundary purchase warnings have independent negative fixtures. Invalid operations preserve protected state through the application entry points.

Cut-plane tests reconstruct normals from M/B, verify the plane contains the intended joint, check mirrored/inside/outside orientation, and compare equal/unequal-pitch cases. The canonical definitions and independent geometry must agree before cut-output acceptance; one rounded chart value alone is insufficient.

## Source grounding

Definitions above settle ContractorCalc's conventions; sources support mechanisms, not safety/compliance claims. References are read-only and not runtime dependencies or copied implementations.

- [NIST SI conversion factors](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors) and [international-foot definitions](https://www.nist.gov/pml/us-surveyfoot/revised-unit-conversion-factors): exact unit definitions, distinguishing rounded published factors from exact derived conversions. NIST's measurement-uncertainty display guidance does not override the approved retain-unrounded-values contract.
- MathWorld [circular segment](https://mathworld.wolfram.com/CircularSegment.html), [cone](https://mathworld.wolfram.com/Cone.html), and [regular polygon](https://mathworld.wolfram.com/RegularPolygon.html): geometric definitions and formulas.
- [Blocklayer stair reference](https://www.blocklayer.com/stairs/straighteng) and [crown setups](https://www.blocklayer.com/crown-molding): confirm that top-tread, headroom and tool-setup conventions must be explicit. Their defaults, code statements and interaction model are not adopted.
- [Engineering ToolBox bulk densities](https://www.engineeringtoolbox.com/dirt-mud-densities-d_1727.html): approximate dry/wet gravel estimates. Example bag and roofing yields above are explicitly product assumptions, not values claimed to be verified from a manufacturer data sheet.
- Hip/jack intersections, pitch-line stair relationships and cut normals are analytic definitions/derivations stated here. They require the independent fixtures and plane-residual review above; source browsing is not proof that an implementation is correct.
