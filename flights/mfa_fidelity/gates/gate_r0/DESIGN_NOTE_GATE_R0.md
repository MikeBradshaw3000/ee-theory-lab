# Design Note — Gate R0: Projection-Bridge Implementation Correctness
**Author:** L1, 2026-09-16. **Status:** §4 departure-statistic set DECLARED by Mike, 2026-09-16 (of record); build proceeds on the working branch; L2 source-review of the built modules follows. **Governing text:** Merge Specification v0.4 FROZEN §8.3 (R0), §3.2, §4.1, §4.5, §7.2; MFP Registration v1.1 (the mean-field operation, the recovery standard, the asymmetry); D2 ruling (exposure surface); D5 ruling (state family committed secondary); E1 contract lineage §6 (R1a targets, tolerances, declared residuals). **Standing:** Gates A and B AUTHORITATIVE and closed; R0 is the sole remaining E1 §8 gate.

## 1. What R0 is, and is not

R0 is *instrument validation*: the implementation proves it correctly computes the four projection quantities against constructed cases with answers known in advance. It precedes all scientific evaluation and asks no recovery question. R1 — recovery against pre-declared targets — is E1 §6's business and does not begin until R0 has passed; the MFP asymmetry binds at R1 only afterwards. R0's pass therefore carries exactly one meaning: *when R1 later reports agreement or departure, the numbers it reports are the numbers the frozen definitions name.*

## 2. The four quantities (frozen definitions, with source)

| # | quantity | frozen definition | source |
|---|---|---|---|
| Q1 | **the local quantity Q reads** | `Local_Density`: Moore-neighborhood active fraction, count/8, toroidal (symmetric_chain's read); under `Q_read = global`, `rho_global` | §3.2, §4.1 |
| Q2 | **aggregate ρ(t)** | `rho_global`: the pre-update grid mean, persisted per tick (tick table) whenever Gate R is exercised, including local-primary runs | §4.1, §7.2 |
| Q3 | **the population-aggregated Q response** | per base: `delta_b = Γ_Ψ·Ψ_local + Γ_ρ·activation_input`, clipped to [0,1] with per-base clip counters; telemetry decomposed as `Delta_from_Psi`, `Delta_from_rho`; the population aggregate is the mean over agents of each decomposed term, per base, per tick | §4.1, §4.5 |
| Q4 | **the declared departure statistics** | measurements of the run's distance from each of MFP's three mean-field moves (§4 below) | MFP v1.1 §4; E1 §6 (residuals) |

Q3 is identically zero in E1 (Γ_Ψ = Γ_ρ = 0 by the threshold-object ruling); R0 nonetheless proves it on constructed nonzero-Γ cases, because the bridge is one instrument and E4 will exercise the channel.

## 3. Constructed cases with known answers

Every expected value is computed *from the frozen definition on constructed inputs*, never from the instrument. Float expectations are compared by **raw float64 bit equality**; integer counts exactly. Cases are declared in a frozen case map the harness cannot narrow (the Gate B discipline, carried over whole).

**Q1 — local read.** The stencil motifs (counts 0–8 at an interior center and at the (0,0) and (0,25) wrap centers, from Gate B's battery), checkerboard (every cell reads exactly 4/8), full stripes (every cell reads 2/8 or 6/8 by row parity), all-inactive (0), all-active (8/8). Global read: the same grids' means as exact fractions.

**Q2 — aggregate ρ(t).** Deterministic trajectories forced by the counted frozen-sequence stub: all draws 0 (every activation passes) and all draws 1 (none does) from declared initial grids, so ρ(t) is a known sequence; the persisted tick table must carry the pre-update mean at every tick, bit-exact, in both `Q_read` modes, with the tick index verified against the frozen post-step/pre-update semantics.

**Q3 — aggregated Q response.** Constructed `Ψ_local` fields (ds patterns with known Moore sums: isolated activation, a full row, a checkerboard flip) and constructed `activation_input` (a fixed grid under local read; a known scalar under global read) with declared (Γ_Ψ, Γ_ρ): expected `Delta_from_Psi`, `Delta_from_rho`, the clipped base, and the clip counters computed by hand; population aggregates as exact means. Both `Q_read` modes; both clip edges exercised (a case that clips high, one that clips low, one that does not clip).

**Q4 — departure statistics** (the declared set, §4): checkerboard — local-read dispersion exactly 0 and Moran's I exactly 0 under Moore weights (four same-colour diagonal neighbours, four opposite cardinals); full stripes — dispersion and Moran's I in closed form; a single active cell — closed form; all-active and all-inactive — dispersion 0, Moran's I undefined and *refused, not returned as 0* (a domain guard, as in Gate B); constructed base fields with known population mean/variance; a constructed configuration–neighbourhood correlation of exactly +1 (Λ_i set equal to Local_Density_i), exactly −1, and exactly 0 (a symmetric construction).

## 4. The declared departure-statistic set (DECLARED by Mike, 2026-09-16)

"Declared" means declared before data. R0 fixes the computations; E1 §6 already names heterogeneity and spatial correlation as the residuals R1a measures. Proposed frozen set, one statistic per mean-field move, all measurement-side, none feeding Q:

1. **Local-read dispersion** (move 1, *local conditions replaced by population averages*): the population variance of `Local_Density` about `rho_global` per tick.
2. **Configuration–neighbourhood correlation** (move 2, *correlations set to zero*): the Pearson correlation across cells between the agent's configuration quantity (Λ_i under symmetric_chain; `is_active` as the state proxy) and its `Local_Density`, per tick; and **Moran's I** of `is_active` under toroidal Moore weights, per tick — the D5 state family's committed spatial observable.
3. **Configuration-distribution dispersion** (move 3, *distribution collapsed to representative values*): per-base population mean and variance of (v, u, r) per tick — trivial while bases are fixed (E1), load-bearing once Q writes (E4).

Mike's word of 2026-09-16 fixes this set as the declared departure surface for R1's attribution telemetry. Nothing in it is a target or a tolerance — those remain E1 §6's, frozen at contract freeze.

## 5. Construction

- **`mfa_instrument/bridge.py`** (new; the Phase-2 observables rebuild, scoped to the projection bridge): pure functions computing Q1–Q4 from grids and fields; never imported by `dynamics.py`; no Q feedback path exists by construction (a test asserts `dynamics.py` does not import it).
- **`mfa_instrument/gates/gate_r0.py`** (new): the constructed-case harness — frozen case map with expected values computed from definitions inside the harness's own expectation module (not from `bridge.py`), raw-bit comparators from `gates/gate_b/comparators.py`, fail-fast with the atomic failure record and the same failure grammar, environment check and label discipline reused from Gate B, `newline="\n"` on every writer from day one.
- **Qualification:** a mutant battery for the bridge (wrong stencil, wrong normalization, post- instead of pre-update ρ, decomposition terms swapped, clip counters off by one, Moran's I with self-weight, correlation with population instead of sample normalization, undefined case returning 0) with pre-declared attribution against an independent frozen manifest — the Gate B pattern.
- **Tests** in the instrument suite; **L2 source review** before placement; **AUTHORITATIVE R0** on the canonical machine with a record owner.

## 6. What R0 leaves untouched

`dynamics.py`, `telemetry.py`, `verify.py`, both cleared gates. R0 reads emitted telemetry and grids; it writes nothing into the dynamics. E1's §6 targets, tolerances, and departure *zone* are not R0's — they freeze with the contract, from the reference object, before any E1 data.
