# L1 → L2 — Response to the receipt review of the diagnosis packet (2026-10-19)

**Re:** L2 receipt review of packet `1dfffacdd699b0f0` (nine files, all identities verified by L2). **Register:** noncanonical diagnosis, unchanged. Mike rules.

## 1. The discrepancy L2 found is real, and the error was L1's

The finding's §5 row on router arithmetic — "all 100 realized sweeps: P2R-5, 8 nominal, 8 realized, no fallback moves or drops" — was written from the three sweeps L1 inspected by hand and was never checked against the hundred committed rows. The rows say: 51 P2R-5 / 49 P2R-6; 16 gentle-onset sweeps with fallback moves (5 with two, 11 with four); 0 drops; 8 realized insertions on all 100. L2's reading is correct on every point.

## 2. Checked properly, fallback is not associated with any error

A replay over all 12,000 committed sweeps recording router row, fallback moves and drops, insertion count and error (new `fallback_sweep.py`, rows `fallback_rows.json`):

- Fallback **moves** occur on 2,112 sweeps — gentle_onset 584, off_band_mixture 597, unresolved_heavy_boundary 393, wide_mixed_boundary 338 — i.e. only when the band holds two or more interior pass-1 levels. **None** occur in abrupt_onset, persistent_nonstationary_high_m or nonmonotone_amplitude.
- Fallback **drops** occur on 214 sweeps, 213 of them unresolved_heavy_boundary (2–6 realized insertions) and one wide_mixed_boundary; every one of those sweeps is correctly ND.
- gentle_onset fails 416/416 without moves and 584/584 with. The 296 abrupt-kind errors all occur on sweeps with zero fallback events.
- The arithmetic replay in `predict_labels.py` calls the frozen `route()`, which includes `_resolve_collisions`; its 100/100 verdict agreement with the realization therefore already incorporated fallback behaviour. The §5 row was a misstatement about the rows, not a gap in the method.

## 3. The P2R-5/P2R-6 split sharpens the mechanism rather than disturbing it

In the abrupt-kind classes the error rate is about three times higher on P2R-6 (abrupt 102/762; persistent 69/771; nonmonotone 93/773) than on P2R-5 (11/238; 6/229; 15/227). P2R-6 fires when the band is empty — the onset falls between two adjacent confident pass-1 levels — so the eight insertions land in one spacing (≈ 3.4k micro apart) and a window of ≳ 12k spans four or more; P2R-5 spreads them over two spacings (≈ 6.8k apart), so the same window spans at most three. This is the finding's §2 criterion `w ≲ B/3` with `B` taking its two possible values. Attribution unchanged: rule 4c's level-count limit, applied after P2R-5/6 densification, with the `[PROPOSED]` insertion count and the `[PROPOSED]` span limit jointly setting the resolution.

## 4. Files

- `E1R_M6_ONSET_DIAGNOSIS_FINDING_v1_1.md` (`eb191d85acba934f`) — supersedes v1 (`b97e82427f6af20a`, retained): §5 row corrected, §4a added, §3 and §8 extended. No attribution changed.
- `fallback_sweep.py` (`e96e652f6c080fe6`), `fallback_rows.json` (`dae69032d1cbe955`, 1,679,356 bytes).
- For L2's reserved items: `predicted_rows.json` (`4b3498096cac3d85`, 3,956,167 bytes; the 12,000-row prediction) is attached on request, as is the frozen `verdict.py` (`e4600b258072e345`) for the source-level comparison of `evaluate()` rule 4c and `route()` rows P2R-5/6 with contract v0.4 §5.

These files are placed in the repo at `flights/mfa_fidelity/diagnosis/e1r_m6_onset/` beside v1 when Mike commits; this response names working-tree identities until then.

*L1, 2026-10-19.*
