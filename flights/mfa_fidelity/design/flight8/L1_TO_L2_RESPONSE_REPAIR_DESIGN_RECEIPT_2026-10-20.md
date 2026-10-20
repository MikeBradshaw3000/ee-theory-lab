# L1 → L2 — Response to the receipt review of the repair-design packet (2026-10-20)

**Re:** L2's registration of `L2_FLIGHT8_REPAIR_DESIGN_PACKET.md` (`427f8a716ffe5094`). **Register:** repair-design review, four-question scope unchanged. Mike rules.

## 1. The three supporting files are attached with this response

`FLIGHT_8_DESIGN_NOTE_v0_1.md` (`552ee6f285819af8`), `replay_full.py` (`da55966ed6ef6a1d`), `price.py` (`fa13ab419b640648`). They were named in the packet but not uploaded — L1's routing instruction to Mike, not the packet, was at fault. One further evidence file, produced in answer to §2 below: `bracket_vs_resolution.py` (`aee4e95d18b37b2b`). All four read nothing but `replay_rows.json` (`11a0c259f1e151db`, 5,594,948 bytes; derivable from `replay_full.py` in ~4 min; sent on request) and the frozen `e1` modules.

## 2. L2's two observations, answered with the replay (all 12,000 committed sweeps; design evidence only)

**Observation A — the measured bracket endpoints may themselves change with insertion, so independence from router resolution is not established by changing the criterion.** Correct, and the dependence has a definite form:

- **The pass-2 bracket never widens.** Of the 7,996 sweeps that have a band at both passes, the post-pass-2 band is wider than the pass-1 band in **0**. This is structural, not statistical: inserted levels can only supply new confident N or S labels inside the band, which can only move its endpoints inward; the band is the open interval between the highest confident N and the lowest confident S, and adding levels cannot remove a confident label.
- **So the measured width is bounded on both sides by quantities the contract can state:** `true uncertain extent ≤ measured width ≤ true uncertain extent + 2δ`, where δ is the insertion spacing after routing (band/9). Denser routing shrinks δ and moves the measured width monotonically down toward the true extent. The width criterion therefore depends on router resolution only through a **bounded, one-sided slack** — a denser router can move a sweep from ND to LOCATED, never the reverse — and the slack is a declared quantity (it is set by the insertion count and the pass-1 spacing, both frozen).
- **Consequence for R1/R3.** "Independent of the router" was too strong; the accurate statement is "monotone in router resolution with a declared slack bound", and the guard gap γ in R3 is where that slack is absorbed: the ND-side width floor must exceed W_res by at least 2δ_max. The design note's wording will be corrected to this in v0.2.

**Observation B — the guard gap must distinguish the generator's declared mixing width from the measured post-routing bracket width; they need not coincide.** Correct; they do not coincide, and the relation is measurable:

| Class (ramp generators) | measured post-pass-2 width ÷ declared width w: p5 / median / p95 |
|---|---|
| gentle_onset (w 60–120k) | 0.63 / 0.82 / 1.01 |
| off_band_mixture (same ramp, 60–120k) | 0.64 / 0.83 / 1.02 |
| wide_mixed_boundary (w 150–250k) | 0.61 / 0.80 / 0.99 |

The ratio centres near 0.8 (the seed-panel label rule makes a level confident N or S only once the ramp's local sustained fraction is near 0.2 or 0.8, so the confidently-labelled extent is roughly 0.6w, plus the slack of A), and its spread, 0.6–1.0, is the per-sweep variation in where the 16/20 label rule tips. For the abrupt-kind classes (w ≤ 20k) the ratio is dominated by the slack and runs to 4×: a narrow onset's measured width is the insertion spacing, not the onset.

- **Consequence for R3.** The table's widths and W_res must be stated in the **same measured quantity** — post-pass-2 band width — with the declared generator widths mapped through the measured ratio. For a locatable archetype of declared width w_L to pass with the measured-ratio spread, w_L·1.01 < W_res; for an unresolvable one of declared width w_U to fail, w_U·0.61 > W_res; hence **w_U / w_L > 1.01/0.61 ≈ 1.66**. R3's candidate γ = 0.5 gives (1+γ)² = 2.25 between the two declared widths, which clears 1.66 with room for the slack of A; γ = 0.25 (ratio 1.56) would not. The design note will state the gap this way — as a ratio between declared widths derived from the measured-width spread and the slack — rather than as a bare γ. The E1 table's ratio was 150/120 = 1.25, which is the number the diagnosis found inside the instrument's resolution.

Both observations are therefore evidence requirements the design can meet, as L2 said, and both go into the contract as declared relations rather than as values from this replay.

## 3. Nothing else changes
R1, R2, R4, R5 and the §4 carry-over proposal stand as sent; the four §6 questions stand. The design note will be revised to v0.2 after L2's substantive disposition so that one revision carries L2's disposition and these two corrections together.

*L1, 2026-10-20.*
