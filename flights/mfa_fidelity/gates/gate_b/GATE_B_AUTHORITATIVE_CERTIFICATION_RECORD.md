# Gate B — AUTHORITATIVE Certification Record
**Gate:** B (Lineage B fidelity: `become_survive`). **Specification:** Gate B v0.4, FROZEN 2026-09-04 (`e2f06bb1…`), never-relax-after-output in force. **Executed:** 2026-09-15/16, canonical machine (Windows; Python 3.14.4; NumPy 2.4.4; the frozen venv, twenty pins conforming). **Harness:** modules 1–4 placed at `b046456`, blob-identity repair at `9d1f75f`; L2 source-review SOUND throughout. **Recorded by:** L1. **Status:** RATIFIED by Mike, 2026-09-16; routed to L2 for AUTHORITATIVE acceptance review.

## 1. Result

**Gate B PASSES under AUTHORITATIVE conditions.** Formal qualification, B1, and B2 each completed with a persistent record owner, in FULL reference mode (the pinned module executed from its git object, its own import-time preflight satisfied), with the environment gate conforming and no candidate output consulted in any decision.

## 2. Run of record (three artifacts, sha256-16)

| act | artifact | identity | outcome |
|---|---|---|---|
| 1 — formal qualification | `qualification/gate_b_qualification_1789500596834674000_56304_a78fb59a.json` | `8F0FE639A62F4285` | PASS — manifest preflight; positive control (AUTHORITATIVE B1) PASS; witnesses (base invariance, alignment, FP, solved-offset) PASS; 32/32 mutants rejected, 32/32 attributed to their pre-declared checks; 31 per-mutant B1/schedule failure artifacts linked by path and digest |
| 2 — AUTHORITATIVE B1 | `b1/gate_b_b1_AUTHORITATIVE_report_1789500951423759000.json` | `9A258F37723789F9` | PASS — five frozen batteries (486 / 27 / 108 / 150 / 4,000), 4,771 case bundles, 7,085 comparator evaluations, allclose diagnostic 6,314 true / 0 false; reference blob `466455f2…` FULL; candidate `9d1f75f` (worktree dirty: untracked Stage-2 calibration outputs, recorded) |
| 3 — AUTHORITATIVE B2 | `b2/gate_b_b2_AUTHORITATIVE_report_1789503512233053500.json` | `62316661FACF8903` | PASS — wrapper verification 10/10 bit-identical (exact shape, dtype, bytes) against the pinned `execute_run`; eight cells, every Welch TOST interval inside ±0.003, no gross-divergence alarm; 769 s |

## 3. B2 cell results (terminal-window mean ρ, ticks 300–399; n = 20 per side)

| cell | reference | candidate | diff | 98.75% CI | Welch df | D_int | ties | p | TOST | alarm |
|---|---|---|---|---|---|---|---|---|---|---|
| cm0 u0.00 κ+0.0000 | 0.399658 | 0.399924 | +0.000265 | [−0.000472, +0.001003] | 36.9 | 6 | 0 | 0.3356 | pass | no |
| cm0 u0.25 κ+0.0000 | 0.434335 | 0.434407 | +0.000072 | [−0.000689, +0.000833] | 35.7 | 4 | 0 | 0.832 | pass | no |
| cm0 u0.00 κ+0.4221 | 0.385906 | 0.386252 | +0.000346 | [−0.000467, +0.001159] | 37.9 | 5 | 0 | 0.5713 | pass | no |
| cm0 u0.00 κ−0.4221 | 0.410718 | 0.410834 | +0.000117 | [−0.000569, +0.000803] | 36.3 | 5 | 0 | 0.5713 | pass | no |
| cm0 u0.25 κ+0.4221 | 0.426118 | 0.426380 | +0.000262 | [−0.000623, +0.001147] | 37.0 | 7 | 0 | 0.1745 | pass | no |
| cm0 u0.25 κ−0.4221 | 0.441098 | 0.441124 | +0.000026 | [−0.000616, +0.000669] | 33.8 | 5 | 1 | 0.5623 | pass | no |
| cm1 t0.25 κ+0.4221 | 0.401665 | 0.401802 | +0.000137 | [−0.000682, +0.000956] | 37.9 | 4 | 0 | 0.832 | pass | no |
| cm1 t0.25 κ−0.4221 | 0.422493 | 0.422487 | −0.000006 | [−0.000682, +0.000669] | 33.7 | 5 | 0 | 0.5713 | pass | no |

Every figure equals the PROVISIONAL container run (Python 3.12.3, Linux, EXTRACTION mode, 2026-09-12) to the last printed digit: the frozen grammar reproduced across environments and reference-load modes with nothing adjusted between them.

## 4. Certified claim (verbatim, Mike's Path-B ruling of 2026-08-26)

Gate B2 certifies terminal-window ensemble-mean equivalence plus the priced gross-divergence screen, and nothing more. It does not certify distributional equivalence; a genuine distributional-equivalence criterion is a named future object conditioned on an ensemble size that would give it real discriminating power.

Together with B1: the merged instrument's `become_survive` realization is **bit-identical to Lineage B at step level** (p_become, g_q, next state, survival threshold, schedule — 4,771 declared cases under raw float64 bit equality) and **equivalent to Lineage B at ensemble level** in the certified sense above, across the eight declared cells including both κ signs in both drive modes.

## 5. What this does not certify

Nothing about Ψ, Regime II, or the phenomenology of EE emergence. The instrument is certified fit to ask those questions under Lineage B's rule; it has asked none of them. The Q-disabled subset (N3 ruling) is the certified domain of `become_survive`; live Q under B remains a named, unbuilt object with its reopen conditions of record.

## 6. Provenance chain

Specification lineage v0.1 → v0.4 through four L2 rounds, frozen by Mike's word; canonical calibration and joint-forecast records at `32dd0ef`; harness modules 1–4 through twelve L2 rounds to SOUND, placed at `b046456`; platform-byte-identity finding caught by the harness on first canonical contact, repaired under a bounded reopening (reference identity moved to the git object), placed at `9d1f75f`; the formal qualification then run under AUTHORITATIVE conditions before either gate. Reference: `4d9a622:cycle3/wave_two/c3_w2_tcop.py`, blob sha256 `466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7`. Environment: `cycle3/requirements.lock.txt` at `4d9a622`, blob sha256 `c10e02c5db497570ffeb45dc92857fcc633cb38364858a35458096950d02de7c`, all twenty pins conforming.

## 7. Observations of record (no action implied)

- Four pairs of per-mutant failure artifacts are byte-identical (mutants 9/11, 13/14, 15/16, 22/23): each pair fails at the same first case with identical evidence. The qualification record binds each artifact to its mutant by path and digest; the B1 failure record itself carries no mutant identity.
- The candidate worktree was dirty at execution (untracked Stage-2 calibration JSON under `cycle3/calibration/stage2/`, unrelated to Gate B); recorded as `candidate_worktree_dirty: True` in all three artifacts.

## 8. Ratification

Ratified by Mike's word of 2026-09-16, given after reading this record in full. This record, the three run-of-record artifacts, and the per-mutant artifacts commit to `flights/mfa_fidelity/gates/gate_b/records/`, and the bundle routes to L2 for AUTHORITATIVE acceptance review.
