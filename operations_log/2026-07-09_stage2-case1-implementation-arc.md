# Operations log - Stage 2 Case 1 implementation arc (spec freeze, Amendment 1, harness build to acceptance)

**Date:** 2026-07-09
**Session type:** continuation of the 2026-07-08 session (third arc; prior arcs committed at c5896b3 and d7d38ea with their own ops logs)
**HEAD at arc open:** d7d38ea (origin current)
**Arbiter:** Mike (sole execution channel)
**Drafting partner:** Claude (Layer 1)

## Arc summary

Mike opened the implementation-spec arc in-session. Source ingestion ran on the COMMIT-PINNED CLONE CHANNEL after Mike flagged manual-transit risk: L1 cloned the public repo at d7d38ea in its own container, extracted the six (later eight) permitted files, digest-verified tcop_read.py (d60da1d9...399f7c) and c3_w2_tcop.py (466455f2...b7e7, matching the committed build record) against committed digests, confirmed the held-out files were never copied, and destroyed the clone. Adopted as the standing L1 source-ingestion convention.

Sequence: implementation spec v1 (with proposed morphology menu) -> L2 hostile review (two verdicts; menu conditionally valid; build design reject-as-build-ready; conditioned two-arm budget accepted as genuinely joint) -> v2 full-acceptance merge (D1 tolerance 0.03; D2 N4 non-scoring) -> Mike froze ("draft"). Build blocker surfaced honestly: the F3-analog gate unbuildable without the committed RNG discipline -> Mike approved AMENDMENT 1 (two construction-only permitted inputs) -> L2 accepted with fences. Harness: v1 (ten L1-self-flagged defects in the routing packet) -> L2 reject-18 -> v2 full rebuild on frozen-source-verified semantics -> L2 reject-7 -> v3 -> L2 reject-2, no conceptual blocker -> v4 -> **L2 ACCEPT, execution-ready, gated on Mike**.

## Defects owned

The frozen-source verification corrected three wrong-values-under-right-names defects in L1's initial gate reading: WINDOW_LEN was 100 not 75; the onset rule uses abs(raw); the meanI control shuffle is per-cell along time (axis=0) - L1's v1 had a spatial shuffle under the time-shuffle name, which would have corrupted every residue. The P3 amplitude placeholder (0.06) was ~3x below the frozen derivation (~0.21). All caught pre-execution by the review structure working as designed.

## Files placed this commit

1. cycle3/wave_two/STAGE2_CASE1_IMPLEMENTATION_SPEC.md (canonical, frozen)
2. cycle3/wave_two/STAGE2_MINI_CONTRACT_AMENDMENT_1.md (Mike-approved, L2-accepted)
3. cycle3/wave_two/STAGE2_CASE1_REVIEW_RECORD.md (full lineage)
4. cycle3/calibration/stage2/stage2_case1_harness.py (v4, L2-accepted)
5. cycle3/RESUME_2026-05-30.md (anchor refresh, 2026-07-09 header)
6. operations_log/2026-07-09_stage2-case1-implementation-arc.md (this file)

Digests published pre-placement, verified at destination. Transit artifacts (v1-v3 of spec and harness, all routing packets) superseded, not committed.

## State at arc close

Harness execution NOT authorized; opens on Mike's explicit call, stage by stage. L2 scope reminder carried: Case-1 success does not complete Stage 2 (fold path + speaking case or recorded waiver still required). Amendment RATIFIED-PENDING-CALIBRATION. TCOP result permanent. All holds carried; Move B pending Mike's materials.

Drafting partner: Claude (Layer 1)
