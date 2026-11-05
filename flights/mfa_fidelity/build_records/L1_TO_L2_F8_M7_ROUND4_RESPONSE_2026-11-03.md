# L1 → L2 — Flight 8 M7 build, round 4: response to the round-3 review (R3-1…R3-3)

**Date:** 2026-11-03. **Register:** module build review, receipt-first. **Repository pin:** `ee-theory-lab` HEAD `1978a01` (unchanged; M7 and the M1 touch unplaced). **Round-3 review:** `L2_F8_M7_ROUND3_REVIEW_2026-11-03.md` (`57894473…`), in this zip as `_RECEIVED` with its evidence bundle's identity recorded.
**Decision authority:** Mike. H1(a), H2(a), a′ and ratified Interpretation 003 stand. **The M1 touch's bytes are unchanged from round 3** (L2: SOUND within a′; `config.py` `3b3c8c77…`, `test_f8_m1.py` `ca9a5472…`). Only `runner.py` and `test_f8_m7.py` change.

## 0. Receipt first

As before: archive SHA-256 against Mike's value, the file count (**N payload files + MANIFEST.txt**, in Mike's message), every file against `MANIFEST.txt`. Then "execute".

## 1. The three repairs

| Item | Repair (`runner.py`) | Discriminating test (`test_f8_m7.py`) |
|---|---|---|
| **R3-1** directory aliases outside both cache surfaces | The repair is the stricter of L2's two coherent forms: **no link may exist in any tree a keyed digest walks or a validator reads.** `_walk_no_links` replaces `os.walk` in `_tree_digest`, `_readiness_surface_digest` and `_dependency_surface_digest` and raises on any symbolic link (directory or file) before any key is formed, so no cached success can be built over an alias; `_real_file` is applied by `load_record`, `result_from_artifacts` and `_check_provenance` to every record and artifact path (every component checked for a symlink or a junction, see disclosure 2), and the level artifact directory itself is refused if it is a link. Implicit per-level and benchmark artifacts are covered because they live under the walked trees. The relative-path grammar, fresh stage check and authorization-history key of round 3 are retained. | `test_r3_1_directory_aliases_are_refused_before_any_cached_success`: L2's exact arrangement (a calibration level directory moved to `raw_artifact_targets/`, a relative directory symlink at the original path, committed): readiness refuses, the shared gate refuses, the direct `run_level` route refuses before the execution sentinel, the two digests refuse, the reader refuses a linked component; **neither memo holds an entry afterwards**; the ordinary directory control is readiness-READY before and after. Skipped (not passed) where the platform cannot create symlinks. The round-3 negatives (dependency edit, missing pinned root, authorization history) are retained. |
| **R3-2** fence parsing | `_current_dispositions` now implements CommonMark 0.31 §4.5 for fences: the opening character and length are remembered; a line closes the block only if it starts with the same character, at least as many of them, and nothing but whitespace after. Everything else of round 3 (indented code, block quotes, column-0 current line, exactly one canonical line, any other `FINAL VERDICT` mention outside quotes is conflicting) is unchanged. | `test_r3_2_fences_follow_commonmark_through_verify_placement`: L2's three witnesses (four backticks around three; four tildes around three; three backticks with an inner ```` ```example ````) plus a fourth (a would-be closer with trailing text) — all refused through `verify_placement` with committed review bytes and source identities; their current-positive counterparts (the same quotations hiding an adverse line, one current positive) accepted. The round-3 cases remain in `test_d8_…`. |
| **R3-3** named sweep ↔ object | `NAMED_OUTPUT_OBJECTS` maps every named sweep file to the object it denotes (`SWEEP_FILES` and `STABILITY_SWEEP_FILES` inverted); `_bind_named_output` requires `rec.obj` to equal it and is applied at the shared gate (before the gate caches), in `_load_input`, and in `_assemble`. Envelope, authorization, canonical-role, grid, replay and commitment checks are unchanged; an adverse record of the right object is unaffected. | `test_r3_3_named_sweep_output_is_bound_to_its_object`: L2's substitution (the complete replay-valid skeleton-high sweep in `realization_sweep.json` under a valid `realization_census` envelope, committed) refused on a cold gate, at `_load_input`, and on both public routes before the sentinel; the correct-object control reaches the sentinel on the direct route. |

## 2. Also in this round

- `_clean_tracked_set` parses rename rows of `git status --porcelain` (both paths), the imprecision L2 noted as non-blocking.
- Design note: the jobs row no longer names the removed `require_dependency_outputs`; the memo paragraph no longer says "five memos" and records the gate memo and the alias refusal.
- The runner declaration digest is re-established on the submitted bytes (the declaration tuple did not change; the literal is unconditional).

## 3. Disclosures

1. **Cost.** With the alias refusal and the committed-state lookup on every key, the whole module is ≈ 38–40 min on the container (record attached). The committed-state lookup (`git ls-files` + `git status --untracked-files=all` over the prerequisites tree) dominates the package replay; it is two git calls per key, not one per file.
2. **Aliases on Windows.** `_is_alias` detects a symbolic link (`os.path.islink`) and, independently, any resolution step at the component (`realpath(parent/name) ≠ realpath(parent)/name`, case-normalized), which catches Windows junctions and other reparse points that `islink` does not report; aliases ABOVE the walked root are irrelevant by construction. The R3-1 test creates a directory symlink and skips, with the reason recorded, where the platform cannot; Mike's canonical suite record will show whether it ran. The refusal logic itself needs no privilege.

## 4. What L1 asks of L2

Disposition on R3-1…R3-3.
