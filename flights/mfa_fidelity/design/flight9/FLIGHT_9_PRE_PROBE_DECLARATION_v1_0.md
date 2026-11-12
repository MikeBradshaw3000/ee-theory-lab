# Flight 9 — Pre-probe declaration v1.0 (RATIFIED)

**Status.** Ratified by Mike, Theory Architect, 2026-11-12 ("ratify"), on L1 draft v0.1 (`ebca389a841e5f1c`, not committed), whose text this is apart from the title, this status line, the two sentences of §6 that record his identification, and §9. Required by Design Note v0.3 §10.4 (L2 design consultation Q8; Mike's ruling 8 of 2026-11-12). Repository `main` at `16e2a7607b88cd43ba33e324a671fbe5a1548a14`. **No probe run exists at ratification.** The probe starts only after this text and the two scripts are committed, pushed and verified from a fresh clone; the probe's manifest records this file's SHA-256.
**What this is.** A prospective declaration, fixed before any Flight 9 lattice output exists, of (i) the claim grammar the probe may not alter, (ii) the probe's exact menu, code and outputs, (iii) what the probe may and may not be used for, and (iv) the four items Interpretation 004 point 4 requires "before any data".
**What the probe is.** A noncanonical design probe run once by L1 in the Linux container. It is design evidence only: it enters no gate, tolerance, qualification or canonical record, and no Flight 9 result may be represented as independent of what it showed (compare Contract F8 §1.0).

## 1. The claim grammar, fixed before any output

Design Note v0.3 (`FLIGHT_9_DESIGN_NOTE_v0_3.md`, `8d82e319d79402f8…`, committed at `16e2a76`) §3.3, §3.4, §3.7, §3.8, §4 and §9 are incorporated here as fixed. In brief:

1. **Scientific target.** Two conditional tests: (a) conditional discriminability of the two prescribed rules in spatial output; (b) conditional boundary compatibility, the scored substantive endpoint: an independently defined observed boundary is or is not representable by a level set of the rule's own local λ at declared resolution. Whole-map contour constancy is reported only.
2. **Claim limits.** No lattice result selects which composition describes ecosystems. An uncoupled independent-response process passes (a) and (b); a pass does not establish collective reinforcement. Terrain TC is near-face feedback suppression, not literal zero-collapse.
3. **Structural against fidelity.** Orderings, contours and boundary representability are structural. Locations (onset level against the spectral crossing; local m_i on the edge; occupancy against the site closure) are fidelity: reported, never scored.
4. **Outcomes.** Follows own; follows rival; follows neither; not distinguished; not adjudicable here; apparatus unevaluable — with the meanings of v0.3 §3.7. "Follows rival" and "follows neither" are valid adverse outcomes. An adverse result seen in the probe does not become fidelity or ND afterwards.
5. **Control.** Bases frozen; g swept; spectral-relative gain κ = g/g_spec,X, computed from the terrain arrays alone.

## 2. The menu — run exactly once, nothing added

| Item | Declared value |
|---|---|
| Rule | Contract F8 §2.4 with a per-cell λ array; μ = 0.2, Δt = 1; synchronous Moore-8 periodic; bases frozen, Q off, drive 0, noise off |
| Objects | realization (η₀ = −ln 0.99, stationary floor-only start); skeleton (η_floor = 0, all cells active at t = 0) |
| Compositions | P = `F_canonical` = v·u·r; H = `F_baseline` = (v + u + r)/3 (rival only) |
| Terrains | T0 flat; TA concordant; TB cross-gradient; TC near-face. Closed-form on the unit torus, cell (i, j) at x = i/L, y = j/L; formulas in `f9_probe.py::terrain`. **TD (margin variants) is not in the probe**: its composition-independent definition is not settled. |
| Arms | T0·P; TA·P, TA·H; TB·P, TB·H; TC·P, TC·H (seven) |
| Lattice sizes | L = 50 and L = 100. L = 100 refines the same unit-torus terrain: patches double in lattice units. This is a pricing comparison, not a scaling study. |
| Levels | κ ∈ {0.75, 1.00, 1.25, 1.50, 1.75, 2.00, 2.50, 3.00}; g = κ·g_spec for the arm |
| Horizon | 3,000 ticks; tail = last 1,000 |
| Seeds | 4 per configuration, from the probe master 9920261112 through `numpy.random.SeedSequence([master, L, terrain, composition, object, κ in micro-units, seed index])` → PCG64. Every run has its own stream; nothing is paired. The master is never reused. |
| Runs | 2 sizes × 7 arms × 2 objects × 8 levels × 4 seeds = **896** |
| Where | L1's container, detached; one process; the menu is refused if the output directory already exists |

**Stopping rule.** The menu runs to completion or stops on an error. A stopped run is preserved as it stands and reported; it is not resumed, trimmed or extended. No configuration is added, repeated or dropped after any output exists. A further probe needs a further declaration.

**Identities (measured in the container, 2026-11-12; LF).**

| File | SHA-256 |
|---|---|
| `f9_probe.py` (rule, terrains, menu, record) | `da5fd84b00818fcdfceeddff57b6effc964f145d797011eef9c59fc67ecf6824` |
| `f9_probe_report.py` (the declared report, §5) | `1f2f8cfae79267fc3ddd63ea9984604d40780fb360e08a2ca3d1c63cf8103680` |
| `F9_PROBE_IDENTITIES.json` (terrain-array hashes, λ ranges, spectral radii, g_spec for all 14 size × arm cases) | `3a4e1399b935310f4b9828a101eb7d9595e92a55cfe17b496e3f7c5c7115b60f` |

Spectral crossings from that file (g_spec = q / spr; no dynamics):

| Arm | λ range | g_spec, L = 50 | g_spec, L = 100 |
|---|---|---|---|
| T0·P | 0.5120 (flat) | 0.354041 | 0.354041 |
| TA·P | 0.0270 – 0.7290 | 0.268651 | 0.258435 |
| TA·H | 0.3000 – 0.9000 | 0.210550 | 0.205933 |
| TB·P | 0.0960 – 0.5120 | 0.374622 | 0.364323 |
| TB·H | 0.5333 – 0.8000 | 0.231654 | 0.229112 |
| TC·P | 0.0405 – 0.7290 | 0.249309 | 0.248871 |
| TC·H | 0.6167 – 0.9000 | 0.201819 | 0.201551 |

On T0, spr = λ̄ and κ equals Flight 8's m.

## 3. What is retained

- `PROBE_MANIFEST.json`: this declaration's SHA-256 as ratified, the script's SHA-256, platform, Python and NumPy versions, the identities, and for every run its configuration, g, tail density, extinction tick, survival, wall seconds, and the SHA-256 of its array file.
- One array file per run: the per-cell records of §6 at W ∈ {1, 10, 100}.
- The report of §5.

Per-tick states are not retained. Every attempted configuration and its outcome is preserved, including runs that show no separation. The manifest and the report are committed; the array files are delivered to Mike as one zip whose SHA-256 is committed, and enter the repository only at his word.

## 4. What the probe may inform, and what it may not

**May inform:** run cost at each L; whether the κ range and spacing reach informative levels (neither floor-dominated nor saturated nor extinct everywhere); the seed-to-seed noise that sizes the canonical panel; whether terrains TB and TC, as specified, give the two rules different spatial output; whether the §6 record is produced correctly.

**May not adapt:** the tests and limits of §1; the outcome labels and their meanings; the normalization; any contour cut, edge-extraction rule, equivalence tolerance, minimum contrast or aggregation rule chosen because it rescues or improves a result seen in the probe.

**Not inspected before the contract's edge and tolerance rules are frozen:** no occupancy map is rendered or viewed; no statistic of occupancy against λ contours is computed; no edge is extracted. L1 computes only the report of §5. The boundary-compatibility endpoint is therefore not seen in the probe.

**If the probe prompts a change.** A change to terrain parameters, sizes or levels is recorded with what was seen and why it changed; terrains kept or altered because of probe output make later inference conditional on that selection. A change to anything in §1 is an outcome-informed scientific redesign: it is named as such, needs Mike's ruling, and needs a fresh validation boundary.

## 5. The report — the only quantities computed from probe output

| # | Quantity |
|---|---|
| R-1 | Wall seconds per run, by L and object |
| R-2 | Per arm, object and κ: mean tail density over the 4 seeds; for the skeleton, survivors of 4 |
| R-3 | Per realization arm and κ: 5th, 50th and 95th percentile across cells of the seed-mean W = 1 occupancy, beside the floor reference 0.0523 |
| R-4 | For TA, TB, TC at each L and κ (realization): correlation between the P-arm and H-arm seed-mean occupancy maps |
| R-5 | TB, each arm and κ (realization): the fraction of across-cell occupancy variance carried by the x-only means. Height varies with x only on TB. This is a whole-map quantity of the reported-only kind, not the scored boundary endpoint. |
| R-6 | TC, each arm and κ (realization): mean occupancy over cells inside the patch (bump ≥ 0.5) and outside it (bump ≤ 0.05), and their ratio. The two sets are defined by terrain geometry, the same for both compositions. |
| R-7 | Seed-to-seed standard deviation of tail density, per arm, object and κ |
| R-8 | Validity of the §6 record: range checks; counts of all-active and all-inactive cells at each W |

All eight are descriptive. None is a test, and none has a pass mark.

## 6. Interpretation 004, point 4 — declared before any data

This section binds Flight 9. By his ratification of 2026-11-12 Mike identifies its incorporation into the Flight 9 contract as satisfying Interpretation 004's requirement that the statistic, the window set, the levels and the persisted record be declared before any data. The contract may add to it; it may not change it after output exists without a recorded ruling.

1. **Windows.** W ∈ {1, 10, 100} ticks. Non-overlapping, equal-width, complete block windows aligned to the first tick of the recording tail (the last 1,000 ticks; n = 1,000, 100 and 10 windows). A window is active if the cell is active at any tick in it. These are observation windows; the participation window stays W = 1 tick (PD5).
2. **Persisted, per cell, per run, per W.** A, the number of active windows; R₀, the number of observed inactive segments; the first and last window states.
3. **Statistic.** The mean length of observed inactive segments clipped to the recording tail: W·(n − A)/R₀ ticks. An all-active record returns "undefined: no inactive segment". A segment touching either end of the tail is flagged as possibly censored. It is reported as its distribution over cells by occupancy band, with the W-specific floor reference (0.0523, 0.1342, 0.6496).
4. **Levels.** Every run at every level of every declared sweep. For the probe that is the menu of §2. The canonical level set is bound in the contract before any canonical data.
5. **Status.** Recorded, not tested. At stationarity the mean inactive spell is fixed by occupancy and q, so the statistic is descriptive and is not an independent signature. The PD record's held candidate (resolution-invariance across W) remains held and untested. No further design effort unless the theory gives it a prediction.

## 7. Done before ratification (disclosed)

- **Terrain identities and spectral values** were computed (`f9_probe.py --identities`). This uses the terrain arrays and adjacency only.
- **A reduction check** was run (`f9_probe.py --reduction`): with a constant λ array the probe's step returns exactly the placed Flight 8 scalar step's array (`f8/dynamics.py`, `cc663dd3c14197a8…`) at equal state and uniforms, over 1,200 ticks at L = 50 on flat arrays (three λ̄ values, both floors). Result: equal. This is a code check on flat arrays; no terrain was run.
- **The window record** was checked against brute force on random binary series, and the report script was exercised on synthetic random arrays. No lattice dynamics were involved.

No run of the rule on any Flight 9 terrain has been made.

## 8. After the probe

L1 reports R-1 to R-8 as they come out, states what was learned, and proposes what, if anything, changes, each change marked as cost, feasibility, terrain or (if it ever arises) scientific. Canonical work uses fresh masters. Probe output never becomes calibration, held-out qualification or canonical observation by relabeling.

## 9. Ratification

Ratified by Mike, Theory Architect, 2026-11-12 ("ratify"), as drafted.

*L1, v0.1 draft and v1.0, 2026-11-12.*
