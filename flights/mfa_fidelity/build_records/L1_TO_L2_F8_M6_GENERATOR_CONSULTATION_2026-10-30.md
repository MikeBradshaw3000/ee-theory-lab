# L1 → L2 — Flight 8 M6: bounded consultation on one contract reading, before the M6 build

**Register:** consultation on a contract reading (the F8_INTERPRETATION_001 pattern, 2026-10-29). **Not** a module review; no code is proposed here. **Pinned to:** `ee-theory-lab` HEAD `5dd1afa` (M-P1 placed 2026-10-30). Contract F8 v0.8.4 is FROZEN (`e87277a2d11e948f…`); its bytes do not change under any outcome of this consultation. Mike rules; this packet asks L2 for a disposition he can rule on.

**Packet contents (at repository paths):** this document; `flights/mfa_fidelity/contracts/flight8/` — the frozen contract, the freeze record, Appendix A of record; `flights/mfa_fidelity/rulings/F8_INTERPRETATION_001_EXTINCT_RUN_TAIL_DENSITY.md` (the pattern this follows); `flights/mfa_fidelity/instrument/mfa_instrument/` — the whole placed package (`f8/` M1–M5, M-P1; `e1/` for the carried M6 grammar, `e1/audit.py`); `tools/time_one_run.py` (reproduces §1's cost figure); `MANIFEST.txt` (SHA-256 of every file). First reply requested: the receipt table (file count and hashes against the manifest), then the disposition.

## 1. The reading that cannot be executed

Contract §5.1 (frozen): runs under each regime of an M6 archetype sweep are generated from "the Markov null (NULL), the realization's own rule at the level's m (SUSTAINED), or the DIP construction (UNRESOLVED)". E1's generator drew SUSTAINED runs as Binomial(N, p_high), p_high ∈ [0.30, 0.60] (`e1/audit.py`, `gen_sustained_run`, `P_HIGH_RANGE`). §5.1 replaced that with "the realization's own rule".

Read literally — one execution of the lattice rule per SUSTAINED (level, seed) — the ratified audit is not executable:

| Quantity | Value | Source |
|---|---|---|
| One production-shape run (50×50, 3,000 ticks), realization or null | **1.0–1.3 s** (container; `tools/time_one_run.py`) | measured |
| Runs per audit: 12 classes × 500 sweeps × (24 pass-1 + up to 8 insertions) levels × 20 seeds | ≈ **3.84 M** | §5.1, §5.2, §4.4 |
| One audit at that cost | ≈ **1,400 h**; the SUSTAINED-only share still ≈ 700 h | arithmetic |
| E1's M6 audit under the binomial generator | 1.3 h on the canonical machine | E1-R record |
| Sweeps per class | 500, ratified by name (freeze record §3 item 23) | not relaxable |

An independent second obstacle: `f8/config.py` line 345 refuses any production-shape run at a level that is not a frozen pass-1 level (L2 M1 round-1 D1, accepted and placed). The pass-2 insertion levels — where every ramp class's band is decided — are not pass-1 levels. The lattice rule therefore has no authorized execution at the levels M6 most needs, independent of cost.

L1's conclusion: §5.1's phrase needs an identified interpretation recorded beside the frozen contract (bytes unchanged; M7 carries its identity), ruled by Mike. This packet asks L2 which reading is sound.

## 2. Candidate readings

| | Reading | Cost per audit | Defined at pass-2 levels | Known shortfall |
|---|---|---|---|---|
| **A** | **The realization's rule under the contract's own §3.1 closure.** Each cell an independent two-state chain: activation hazard η₀ + g·λ̄·ρ*(m; η₀) (the §2.4 hazard with d_i replaced by the map's fixed point at that m), deactivation μ (§2.4), stationary start. Its stationary density is exactly ρ*(m; η₀), the §3.1 fixed point. Modulated classes act on the target density; the hazard is re-solved from the stationary relation a = qρ/(1 − ρ). | ≈ E1's (milliseconds per run; the chain is vectorised over cells and ticks) | Yes — ρ*(m; η₀) is solvable at any m by M5's fixed-point solver | No spatial correlation: window-mean variance below the lattice's. Disclosed; priced after job 0 by reporting ŝ(m) beside the surrogate's per-level sd (descriptive, never a pass criterion). |
| B | Lattice pools: pre-simulated realization runs at each pass-1 level under a dedicated master, sampled with replacement per sweep | pool ≈ 24 × k × 1.3 s | **No** (config refuses) | Runs reused across sweeps; undefined off-grid |
| C | E1's construction with the F8 amplitude: Binomial(N, ρ*(m; η₀)) per tick | ≈ E1's | Yes | No temporal correlation at all; farthest from "the realization's own rule" |
| D | Literal lattice per run | ≈ 1,400 h | No (config refuses) | Infeasible; 500/class is ratified |

**L1 recommends A**, on three grounds: (1) it is the contract's own closure (§3.1) applied to the contract's own rule (§2.4) — the same object the flight's predictions are stated in; (2) it is exactly M3's null construction with g restored — §2.9 defines the null as "the same rule with the feedback term removed", so under A one generator with one parameter produces both NULL and SUSTAINED regimes, and the §4.3 familywise price runs on it at g = 0; (3) it is defined at every level the router can reach. Its shortfall is the closure's shortfall everywhere else in this flight (§3.2's design evidence, §1.2′), stated the same way.

Two consequences A carries into the generator declaration (all PROPOSED; nothing pre-approved):

1. **Amplitude is tied to m, not drawn.** From Appendix A: ρ*(0.25; η₀) = 0.0669 at the lowest level against θ_P = 0.057364 (M3 of record; null per-window sd ≈ 0.0013). A SUSTAINED chain run at m = 0.25 is still confidently SUSTAINED (~7 sd above θ_P on every window), but the margin is small compared with E1's absolute 0.30–0.60. The modulated classes (`persistent_nonstationary_high_m` drift/oscillation, `nonmonotone_amplitude` attenuation) must therefore be declared on the **excess over the null density** (ρ − π₁), so no modulation can carry a sustained run under θ_P; the per-draw preflight proves it.
2. `no_null_consistent_anywhere` reads as §5.2 writes it: a realization chain at every level, the absorbing state never reached.

## 3. Three adjacent items for the same ruling

- The phrase "two-part generator (skeleton + realization)" appears in L1's session handoffs of 2026-10-23 and 2026-10-30 but **nowhere in the contract**. §5.1 names three regime sources; the only two-part object in the contract is job 0's calibration census (§7.3). L1 treats it as a handoff gloss unless L2 or Mike reads otherwise.
- §5.3: the design, held-out and pricing masters are drawn "after the table, W_res and the generator are frozen". Table and W_res are frozen; the generator is not until this ruling, so the masters are drawn at the end of the M6 build and committed with its identity (DERIVED@BUILD, as M1's panel masters).
- §4.3: θ_P's familywise conservatism is priced in the M6 record by the empirical null rejection rate against α_P. Under A that price runs on the chain at g = 0; the stepper-level price M3 already carries (`price_familywise`) stays beside it.

## 4. What L1 asks of L2

1. Is reading A sound as the identified interpretation of §5.1 for M6? If not, which row, or what else?
2. Is the disclosure form of A's shortfall adequate — descriptive comparison of the lattice's ŝ(m) (job 0) with the surrogate's per-level sd, in the M6 record, never a pass criterion — or does L2 require a different pricing?
3. Does the "modulations on the excess over the null density" rule (§2 item 1) satisfy the generator constraint, or should the amplitude margin be declared another way?
4. Anything in A that L2 would mark DEFECT at the build review, so it is designed out now.

After L2's disposition Mike rules; L1 then records `F8_INTERPRETATION_002` beside the contract (bytes unchanged), builds M6 on it, and routes the build for review in a fresh chat with a receipt table first.

*L1, 2026-10-30. No file placed; no master drawn; nothing in `e1` modified; HEAD `5dd1afa`.*
