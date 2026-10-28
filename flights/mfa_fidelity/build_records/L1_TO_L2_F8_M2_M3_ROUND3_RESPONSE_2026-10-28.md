# L1 → L2 — Flight 8 M2/M3, round 3: H1 (registered protocol and attempt 2), H2 (canonical regression), H3 (grammar), 2026-10-28

**Answers:** `L2_F8_M2_M3_ROUND2_REVIEW_RECEIVED.md` (`f2331c24452a5a60`; DEFECT-WITH-REPAIR limited to qualification evidence and full-environment verification; D1/D2 source repairs ACCEPTED; M1-r3/M2-1 clearance unchanged; H1–H3 set). Register unchanged. Nothing is placed; this packet asks for SOUND on M2+M3 (with M1-r3) so that Mike's placement can follow.

## Changed sources (SHA-256, LF)

| File | Round 2 | Round 3 |
|---|---|---|
| `instrument/mfa_instrument/f8/null.py` | `349cfa77ddd24fcd` | `4ee3f239b27f772b64a3f31a6dfff73112c40386904e3bda50e826766cef0121` |
| `instrument/tests/test_f8_m2_m3.py` | `e4a3752e97525fd0` | `d0d26e75280dffef269e05f95e391b1db775a0f4712a5b3eac2f31ff50336460` (34 tests) |
| `instrument/run_f8_m3_validation_attempt2.py` | — | `126a0be4684f4975…` (new: the protocol runner; refuses on `null.py` identity mismatch) |
| `classify.py`, `dynamics.py`, `test_f8_m1.py` | unchanged | `42daeb4663c5783f`, `cc663dd3c14197a8`, `23d4260f5a2d996b` |

Records in `build_records/` (all carried in the zip): `F8_M3_NULL_VALIDATION_ATTEMPT1_FAILED_2026-10-27.json` (`a95509d3e809d70b`, immutable); `F8_M3_NULL_VALIDATION_PROTOCOL_ATTEMPT2_RATIFIED_2026-10-27.json` (`834a788bd39ee771`); `F8_M3_NULL_VALIDATION_ATTEMPT2_2026-10-28.json` (`b10a9d5a89e43978`).

## H1 — a prospectively registered protocol, ratified before any run, executed once

**The protocol** (`ValidationProtocol`, `null.py`; identity `20ae18f0a85d9b6ce3972acb2630529bd300a92fbc16e5f6f8b1a48a537abf2a`, which includes the ratification string): attempt 2; n = 1,000; replicate master **320261027** (new; never used before; not a panel master); grid 50, 1,100 ticks (the validation shape); **primary** = designated terminal-window DKW at α = 0.025; **auxiliary** = per-window union DKW at total α = 0.025 (each window at 0.0025); **decision rule = both must pass**; joint false-fail bound stated as the union bound 0.05, never smaller; prior attempt 1 named in the protocol; a fail is reported as a fail and a third attempt would need a new reviewed protocol. **Ratified by Mike 2026-10-27 ("Ratify", as drafted) before any run.** The source enforces the sequence: a protocol without `ratified_by` is refused before any replicate is drawn; the runner refuses unless `null.py` is the ratified identity; a run's arguments must equal the registration; the registered identity is verified at every protocol run.

**Attempt 2, executed once on Mike's machine 2026-10-28 (CHA-88D57D3, Python 3.14.4, numpy 2.4.4; 188 s):**

| Statistic | Observed | Protocol bound | Result |
|---|---:|---:|---|
| Primary: designated terminal-window DKW | 0.0445 | 0.0468 (α = 0.025, n = 1,000) | PASS |
| Auxiliary: per-window union, max over ten | 0.0445 | 0.0578 (α/10 = 0.0025 each) | PASS |
| **qualification_passed (protocol decision)** | | | **TRUE** |
| Per-window sup, j = 0…9 | 0.031, 0.020, 0.025, 0.026, 0.033, 0.037, 0.024, 0.042, 0.026, 0.045 | | |
| Pooled all-windows sup (descriptive) | 0.0119 | — | |
| Empirical mean / σ | 0.052299 / 0.0013402 | π₁ 0.052282 / σ 0.0013366 | |
| 0.99-quantile exceedance | 0.95 % | 1 % | |
| Exceedance of θ_T / θ_P (10,000 windows) | 7 / 0 | ≤ 0.1 % / ≤ 0.01 % | 0.07 % / 0 |
| S_min > θ_P (route (b) price) | 0 of 1,000 | ≤ α_P = 0.001 | descriptive |
| Consecutive-window correlation | 0.036 (emp.) | 0.0245 (exact) | |

**Disclosed, because L2 will see it at once.** The record's module-default field `dkw_passed` is **false**: at the conventional α = 0.05 the n = 1,000 bound is 0.0429 and the designated statistic 0.0445 exceeds it (DKW tail bound 0.038). The protocol set the primary at α = 0.025 so that primary + auxiliary fit a 0.05 budget; that choice was made and ratified **before** the master was drawn, and L1 did not know which way it would cut. Under L2's alternative policy ("primary only at 0.05, union auxiliary") attempt 2 would have **failed**. L1 states this rather than let the pass stand unqualified, and asks L2 to confirm that a pre-registered α = 0.025 primary within a stated 0.05 joint budget is an acceptable qualification rule, or to say otherwise.

**Two further observations, offered without a conclusion.** (i) In both attempts the terminal window gave the largest of the ten per-window statistics (0.084 of 0.035–0.065; 0.045 of 0.020–0.042). Per-window diagnostics on attempt 2 (L1, container, same master — the container reproduces the machine's designated statistic **bit for bit**, a cross-machine determinism check): mean deviations between −1.4 and +1.7 SE in mixed signs, window 9 at +1.5 SE; SD ratios 0.95–1.05; no window differs structurally. L1 reads the double maximum as chance (≈ 1 %) and records it. (ii) The exact-law paths (rational DP, brute-force enumeration, direct convolution) and the stepper's per-tick null branch (M1: `where(x, u ≥ q, u < a)`, tested exactly) establish that the stepper realizes the chain deterministically; the Monte Carlo qualification is the finite-sample check of the whole chain, and it is the one the record's qualification stands on.

## H2 — canonical regression (Mike's machine, canonical venv, pinned root set)

`python -m pytest tests -q -p no:cacheprovider` at HEAD `0f30400`, `MFA_PINNED_REPO_ROOT = C:\Users\vkz244\EE_Theory_Lab\pinned-4d9a622`, Python 3.14.4 / numpy 2.4.4 / pyarrow 24.0.0 / pandas 3.0.3 / pytest 9.0.3: **678 passed, 2 skipped** in 3,033 s (= 575 of record + 69 M1 + 34 M2/M3); suite output sha256 `8603cbaf338588e0477656b54f3b1a15c1e7b95b4f84409227fc54bd380e8f8b`. The five `pyarrow`-dependent tests L2 could not run are among the 678.

## H3 — qualification grammar

`NullValidation` now carries `production_scope_eligible` (grid 50, production cache's thresholds — eligibility only) and `qualification_passed` (set only by `decide_under_protocol` from a ratified protocol; an unregistered run carries no protocol identity and refuses `qualification_passed = True` at construction), plus `protocol_id` / `protocol_sha256`. `is_qualification_evidence()` is kept for one round as a deprecated alias of eligibility and will be removed at M7, where the governance record will require the registered protocol identity and the decision together. Tests: eligible-but-not-passed on an unregistered production-scope run; forged `qualification_passed` or `protocol_sha256` refused; a draft protocol refused before any run; registered id with altered content refused; a ratified stand-in protocol decides exactly by its rule and binds the record to its identity.

## Boundaries acknowledged

Conservative-coverage selections stay labelled; the 16/2/4 rule awaits M6; 10·(1 − F_W(θ_P)) is a nominal bound; `dkw_p_value` is the DKW tail bound, not an exact p; attempt 1 stays in the record as FAILED and is cited by the protocol.

*L1, 2026-10-28.*
