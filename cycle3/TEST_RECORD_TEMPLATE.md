# TEST RECORD — `C3-<area>-<nnn>` <Test name>

> Copy this file per test. Fill the **pre-execution** block before running; fill the **post-execution** block after. Both halves are required — a record with only one half is incomplete. Execution channel is **Mike only**; no layer executes.

---

## Pre-execution (write before running)

**Test ID:** `C3-<area>-<nnn>`
**Test name:**
**Registry status at open:** planned → ready
**Date opened:**

**Purpose — the question this test answers:**
> One sentence. If it cannot be stated as a question with a possible "no," it is not yet a test.

**Theoretical target — which part of Regime-II-as-structural this bears on:**
> Name the specific claim. If it bears on the co-equal observable pair, state explicitly that it does **not** presuppose which candidate is Ψ.

**Level this test is designed to address:** L1 / L2 / L3 / L4
> Most tests target one level. A test claiming to reach L4 must show it has already cleared L1–L3, by record reference.

**Inputs and parameters:**
> Substrate / run, grid size, seed(s), Λ setting, ρ regime, window bounds if any, all tunable parameters with values. Enough that the run is reproducible from this block alone.

**Script name and version:**
> Path + version tag or SHA. If the script is new to Cycle 3, say so. Never overwrite a canonical disk file with a reconstruction; reference reconstructions explicitly and never treat them as canonical.

**Expected data produced:**
> Which output files, what columns/shape, where they land.

**Expected output / pass criterion — stated per level:**
- L1 (implementation): _e.g. runs without error, output finite and well-formed_
- L2 (measurement validity): _e.g. value is state-based and density-adjusted; passes the permutation-null z separator against the uniformity degeneracy_
- L3 (steady-state eligibility): _e.g. window earns the label — relative drift < 5%, ρ CV < 10–15%, range/mean < 25–30%_
- L4 (interpretation): _what reading would and would not be licensed — but note L4 is settled by Mike / Layer 1, not by this criterion alone_

**Positive control:**
> The synthetic case that SHOULD produce a clear signal. Required before any output is interpreted. If absent, this test cannot clear past L1 — say so here.

**Negative control:**
> The case that should produce ≈ no signal (e.g. near-uniform persistence → degeneracy check; ρ-matched scramble). Required to distinguish "no coherence" from a measurement artifact.

**Interpretation boundary — declared in advance:**
> What a pass establishes and, explicitly, what it does NOT establish. State the seam: implementation/measurement (Layer 3/2) vs meaning (Mike/Layer 1). Naming a boundary before the result is what stops a clean L1 pass from being read as theory support after the fact.

---

## Execution (Mike only)

**Date run:**
**Machine / environment:** _(confirm venv interpreter path per MESA_ENVIRONMENT_REPRODUCTION §7)_
**Actual command run:**
```
<paste verbatim>
```

**Output files generated:**
> Paths + brief note that each is well-formed. SHA or size if provenance matters.

---

## Post-execution (write after running)

**Highest level cleared:** L1 / L2 / L3 / L4
> The single most important field. "Script ran" = L1 only. Do not advance a level on the strength of a lower one.

**Result summary:**
> What the run produced, in vocabulary-disciplined terms. Candidates **produce** or **fail to produce**; they do not "confirm" or "demonstrate." Report the value AND its controls together — a value without its control is not a result.

**Control outcomes:**
- Positive control:
- Negative control:
> If controls were not run, interpretation stops at the level the controls would have unlocked. Say so plainly.

**Steady-state eligibility outcome (if applicable):**
> Did the window earn the label, on which diagnostics, with what numbers. "Near-zero slope" is not eligibility on its own — report drift, range/mean, and CV.

**Interpretation (L4 — Mike / Layer 1 only):**
> May be left as "withheld" with stacked reasons, exactly as a Cycle 2 smoke test was. Withholding is a legitimate, recorded outcome. If interpreted, Mike arbitrates and signs.

**Divergence note (if the co-equal pair was involved):**
> If the two candidate observables disagreed, record the disagreement as data. Do not collapse it to one reading. Flag whether this is a case (e.g. transient wave) where divergence is expected.

**Follow-up decision:**
> Next action: re-run with controls / advance to next level / route a revision to Layer 3 / open a new test (give its ID) / retire / hand the open ontological question to Mike. Update the registry row to match.

**Registry status at close:**
