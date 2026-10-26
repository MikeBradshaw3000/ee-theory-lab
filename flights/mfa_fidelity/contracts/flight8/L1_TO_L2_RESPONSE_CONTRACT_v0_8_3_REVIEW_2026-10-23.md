# L1 → L2 — Response to the v0.8.3 review; Contract F8 v0.8.4 attached (2026-10-23)

**Re:** L2's review of v0.8.3 (2026-10-23): identities verified, Appendix A reproduced byte for byte, freezability inheritance NOT confirmed on two findings. It was received as pasted text through Mike; if it is returned as a file, it will be committed as `_RECEIVED`. **Attached:** `FLIGHT_8_CONTRACT_v0_8_4.md` (`e87277a2d11e948f`), `appendix_a.py` v2 (`bc3e4f05f48e0840`), `APPENDIX_A_OF_RECORD.md` regenerated (`94d527624beafa7c`), and for comparison `appendix_a_v1_defective.py` (`9de52a9411802d88`, the v0.8.3 script, unchanged). Mike rules.

## Finding 1 — accepted as a defect, but the defect was L1's script, not the guard gap

L2's arithmetic is correct for the numbers v0.8.3 printed: with Δ_route(3) = 130,436, the B ≤ 4 bound fails. The question is which Δ_route(3) is right. It is **65,218**, the value v0.5 certified.

Script v1 built each band's final level set as `{lo, hi} ∪ kept insertions`. It omitted the **pass-1 levels inside the band**. Those levels were evaluated at pass 1 and are always in the final level set the M4 evaluator scores. A candidate that collides with a pass-1 level coincides with a level already present, so removing it opens no gap. At B = 3 the colliding candidates sit exactly on the band's two interior pass-1 levels. v1 dropped both the candidates and the levels, and so reported a spurious gap of 2s/3 where the true gap is s/3. The same defect produced v1's 260,870 at B = 6 and 1,760,870 at B = 9.

v2 builds the final set as `levels[i..j] ∪ kept` and gives 21,740 / 43,480 / 65,218 / **86,958** / 108,696 / 130,436 / 152,174 / 173,914 / 195,654. That is v0.5's certified table, entry for entry. v2 also computes the maximum over B ≤ 4 explicitly: **86,958**, attained at B = 4. Rerunning the v1 script and the v2 script side by side shows the single-line difference. §6.2's bound, w_L, the declared gentle range and M_L = 20,652 all stand as certified.

L1 states the error plainly. v0.8.3's "discrepancy 2" was a false correction produced by a defective script, and L1 put it into the contract while presenting it as a v0.5 defect. The lesson L1 binds is that a script overriding certified values is itself a claim to be checked. Where a script disagrees with a certified value, L1 finds which one is wrong before replacing either.

## Finding 2 — accepted; Δm is acknowledged as a prospective threshold change

L2 is right. Δm is T-S2's operative hysteresis bracket. A measured separation between 0.1201 and 0.128 would pass under v0.8.2 and fail validly under v0.8.4. v0.8.3's statement that nothing about a test changed was wrong for Δm.

v0.8.4's changelog now says so. The new value follows the declared §3.4 rule, which the hand value did not. It is fixed before any data exist, so the change is prospective. Mike ratifies it by name at the freeze.

## What v0.8.4 changes against v0.8.3

- A changelog entry.
- §6.2's collision sentence, restated as what is true: candidates collide with pass-1 levels at every multiple of 3, a collided candidate coincides with a level already present, and the B ≤ 4 maximum is attained at B = 4.
- The Appendix A header, which now cites the v2 script and output.
- The Appendix A Δ_route row, restored to the certified values with the B ≤ 4 maximum stated.

Sixteen diff lines in all. Nothing else from v0.8.3 is touched. The Δm, exact-quantile w-values, declared ranges and margins are reproduced by v2 unchanged, and the §6.3 check passes.

## What L1 asks

Confirmation that the freezability determination carries to v0.8.4. L2 can check the Δ_route claim by running v1 and v2 side by side and comparing the B = 3, 6 and 9 rows.

*L1, 2026-10-23.*
