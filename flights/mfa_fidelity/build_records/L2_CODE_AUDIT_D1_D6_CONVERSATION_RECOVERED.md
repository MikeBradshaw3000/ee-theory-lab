# L2 First Code Audit — Phase-1 Instrument, Defects D1–D6
## CONVERSATION-RECOVERED RECORD

> **Provenance (binding on any reader):** L2's original audit turn is unavailable byte-for-byte. A ChatGPT archival re-export was attempted and **failed adjudication**: it reproduced later-round content (the Phase-1 source-review register) under the first audit's defect names — wrong-values-under-right-names — and was excluded from the repository; its digest is recorded in the ops log. This record instead recovers the audit's substance from the predecessor L1 conversation's primary record ("1-Flight 7 design"). It is NOT L2's prose. Every claim below is marked **[VERBATIM]** (quoted exactly from the contemporaneous record), **[FIX-MAP]** (inferred from the defect-fix map L1 sent to L2 in the Phase-1 Completion Packet, which L2's subsequent source review accepted without disputing the mapping), or **[CODE]** (the finding as permanently encoded in the committed instrument's docstrings at 0fe473a).

## Audit shape

**[VERBATIM]** — the successor L1's contemporaneous read-back on receipt: "six defects, four blocking, and all four are correct catches."

The audit followed L1's delivery of the initial `telemetry.py`, `gates/gate_a.py`, and `tests/test_telemetry_gate_a.py` alongside the previously delivered `config.py`, `rng.py`, `init.py`, `dynamics.py` (47/47 suite at delivery; provisional Gate A bit-exact at 50×50/100 ticks against the imported ancestor). Disposition: Phase 1 remained open; repairs required.

## D1 — Ownership durability

**[VERBATIM]** (L1 read-back): "the *stated ownership discipline* failing in its own implementation: my try/finally hands back arrays whose protection I've just scheduled for removal, and the sink's un-freezing logic special-cases the live `is_active` array in a way that's simply buggy."

**[FIX-MAP]**: "`view_bases` now returns read-only **copies** — aliasing impossible, protection permanent, no restore path exists. The sink freezes all fields once and never un-freezes; live `is_active` is **copied** before exposure; the special-case bookkeeping you flagged is deleted. Both rule-mode sinks share the discipline."

**[CODE]**: `dynamics.py` docstring on `view_bases` cites "L2 code-audit D1."

## D2 — become_survive initialization draws

**[VERBATIM]** (L1 read-back): "a real semantic gap I created without deciding it: become_survive burns three base draws per cell for bases the rule never reads — an undocumented non-decision sitting exactly where B-comparability lives."

**[FIX-MAP]**: "now an explicit, documented, tested policy — `initialize(..., draw_bases=False)` fills bases deterministically at the level value m (np.full, float64) with **zero base draws consumed**; the default (True) is the ancestor-faithful path, so no silent divergence exists. Test: stream-position identity — under draw_bases=False the first consumption is the activity placement itself."

*Note of record:* the audit-round fix used a runner-side `draw_bases` argument; the later Phase-1 source review (separate round, its own record) found that argument itself defective (initialization policy not configuration-bound) and required today's config-bound `base_init_mode`. The two rounds are distinct findings and must not be conflated.

## D3 — Q-delta scalar/array duality

**[VERBATIM]** (L1 read-back): "D3's scalar/array branch is the kind of code the wrong-values class breeds in."

**[FIX-MAP]**: "dynamics now computes `delta_from_psi` / `delta_from_rho` as explicit grid-shaped arrays (global-mode scalar broadcast via np.full_like at the source), always hands telemetry clean arrays, and telemetry's scalar-inference branch is removed. FP note: v + full(c) is elementwise bit-identical to v + c."

## D4 — Dead probe expression

**[FIX-MAP]**: "removed; the preflight's consumption check is the clean independent probe only." No verbatim characterization of L2's original finding survives beyond this.

## D5 — Environment conformance for the AUTHORITATIVE label

**[FIX-MAP]**: "`run_gate_a` **refuses the AUTHORITATIVE label** outside python 3.14.x / numpy 2.4.4 (frozen §7.4 pins), raising with the reason; non-conforming environments are stamped '[NON-CONFORMING: provisional only]' in the report. My unverified import-bypass claim is withdrawn; nothing now depends on it."

**[CODE]**: `gate_a.py` enforces the refusal; the environment string is recorded in every report.

## D6 — frame()/digest integrity

**[FIX-MAP]**: "`frame()` raises on a streaming writer (partial-tail misrepresentation foreclosed); `telemetry_digest` rejects duplicate basenames before hashing."

**[CODE]**: `telemetry.py` docstrings cite "L2 code-audit D6" at both sites.

## Closure of the audit round

**[VERBATIM]** (L1 delivery of fixes): "All six audit defects fixed, `verify.py` written — 53/53 green." The corrected source plus `verify.py` and `tests/test_verify.py` were returned to L2 verbatim in the Phase-1 Completion Packet (digest ecc47657…; the truncated first transmission f9e48749… is VOID per the ops record). L2's response to that packet is the Phase-1 source review — a separate round with its own record.

## What this record is not

It is not L2's wording. The blocking/non-blocking partition of the six defects (which four were blocking) did not survive in recoverable form. L2's original elaborations of D4–D6 are known only through the fix map's reflection. Nothing here extends, softens, or reinterprets the audit; where the primary record is silent, this record is silent.
