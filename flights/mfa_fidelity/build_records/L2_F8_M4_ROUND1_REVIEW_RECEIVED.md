# L2 — Flight 8 M4 Round-1 Source Review

**Date:** 2026-10-28  
**Register:** Instrument build review, frozen Contract F8 v0.8.4 (`e87277a2d11e948f`), §§4.4–4.7, 5.2, 6.2, Appendix A.  
**Packet:** `L2_F8_M4_BUILD_PACKET_2026-10-28.md` (`8b96d8dc292e7915`).  
**Reviewed source:** `f8/verdict.py` (`c79ce0d7c81e21d5`), `tests/test_f8_m4.py` (`8b8976b2c3602e0c`).  

## Verdict: SOUND (source-level and M4 scope)

No contract-relevant source defect identified in M4. **All three declarations M4-1, M4-2, M4-3 are accepted**, with the explicit integration boundary below. This is not authorization for placement or a production run; canonical full-suite verification and M7 integration remain separately controlled.

## Execution evidence and environment qualification

1. Literal requested command `python -m pytest tests/test_f8_m4.py -q`, from `flights/mfa_fidelity/instrument`, **did not collect**, because `pyarrow` is absent in this review environment. The import chain is `test_f8_m4` → `e1.verdict` → `e1.config` → `pyarrow.parquet`; installing `pyarrow` was unavailable owing to network/DNS restrictions.
2. Reran exactly the M4 test module with a **temporary, external import-only placeholder** for `pyarrow` and `pyarrow.parquet`, exposing version `0.0.0`. No repository files were changed. This placeholder implements **no Arrow or Parquet operations**, and so can support this verdict/router-focused module's import chain but **does not qualify Arrow integration or the canonical environment**. Command: `PYTHONPATH=/mnt/data/m4review_support:$PWD python -m pytest tests/test_f8_m4.py -q`. **Result: 17 passed in 5.52 s.**
3. Thus 17/17 M4 behavioral tests passed under an explicitly restricted import environment; do not describe this as an unqualified canonical-machine execution.

## Carried E1 components

Compared `f8/verdict.py` directly with the enclosed `e1/verdict.py`. The F8 module retains E1's rules 1, 2, 3, 4a, 4b, their precedence, two-off-band-U allowance with the isolation constraint, the seven router rows and their order, eight interior insertions for P2R-5/6 and four per interval for P2R-4, integer-micro-unit round-half-even arithmetic, and collision fallback by midpoint/move-or-drop with recorded actions. The live reachability remains P2R-5/6; multiple N→S intervals trigger rule 1 and P2R-2 before P2R-3/4; P2R-7 cannot be reached with confident dual phases in order. Arithmetic and routing outcomes were checked against E1's own implementation by the test module. The code is **not byte-for-byte identical** to E1: imports, grid constants, declarations, diagnostics, and width logic necessarily differ; the packet's “verbatim” characterization is supported at the **specified behavioral-rule level**, not whole-file textual identity. E1's `BOUNDARY_SPAN_LIMIT=3` remains in E1 and is absent from F8.

## Rule 4c and §4.7

F8's `evaluate` computes the unique band endpoints as the highest confident N and lowest confident S, then `width = levels[hi] - levels[lo]` and assigns 4c exactly when **`width > W_RES_MICRO`**. The declared resolution is exactly 293,478 micro-units, equal to 3 pass-1 spacings. Equality takes 4d (`LOCATED`), and 4c produces `NOT_DISTINGUISHED` with cause `boundary_unresolved_at_W_res`; both paths record width and resolution in the evidence. Rules 4a/4b take precedence. The 16,384-sequence exhaustive 7-level test agrees with an independently written rule transcription; strict boundary cases and a post-insertion narrower band are tested. Inspection finds no amplitude/jump/slope/monotonicity/separation condition in the verdict logic. The M4 output is a **secondary detection-morphology observation**, not an adjudication of P1, consistent with §4.7 and §4.9.

## Appendix A and §6.2

The implementation computes candidate insertions for bands on the frozen 24-level grid, uses exact round-half-even interpolation, **removes coincident candidates in the conservative Appendix A audit**, and measures twice the largest remaining final-level gap. The resulting Δ_route(B) for B=1…9 is **21,740; 43,480; 65,218; 86,958; 108,696; 130,436; 152,174; 173,914; 195,654**, agreeing with the committed Appendix A table and its parsed JSON, with `max_{B≤4} Δ_route(B)=86,958`. The reachable audit has 276 bands; 84 collision cases are reported, with collisions at B=3,6,9,12,15,18,21. Hence collision-free proof **does not close**, and the live fallback is appropriately retained and tested. The audit's collision-removal model and live router's move/drop fallback are deliberately distinct, as the contract specifies.

## Declarations

| Declaration | Ruling | Reason |
|---|---|---|
| **M4-1 — Cause token** | **ACCEPT** | `boundary_unresolved_at_W_res` distinguishes the new physical-width criterion from E1's count-based `boundary_unresolved`; the two affected §5.2 archetypes share it. |
| **M4-2 — “After pass 2”** | **ACCEPT, integration obligation** | A pure `evaluate(labels, levels)` correctly applies the same grammar at pass 1 to drive routing, then to the final combined level set for the verdict of record. **M7 must enforce and verify** that the recorded verdict uses the final level set and final labels; M4 alone cannot prove the downstream call site. |
| **M4-3 — Reachability unchanged** | **ACCEPT** | The router's precedence and confident-order rule leave only P2R-5/6 reachable for refinement on this grid; P2R-3/4/7 remain structurally dead. |

## Defects and repairs

**None found within the reviewed M4 scope.** The absence of installed `pyarrow` is a reviewer-environment qualification, **not an M4 source defect**. For placement, repeat the exact unmodified M4 test command and canonical suite on the authorized environment, and independently verify the M7 final-level-set obligation when M7 is reviewed.

**L2 disposition:** **SOUND**. No placement, run, or M6/M7 qualification authorized by this review.
