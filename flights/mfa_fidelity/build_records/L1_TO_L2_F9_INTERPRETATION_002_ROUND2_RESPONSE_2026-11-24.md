# L1 → L2 — Flight 9 Interpretation 002, draft 2: response to your round-1 review

**Date:** 2026-11-24. **Register:** review of a draft ruling record (receipt first). No code for these summaries exists.
**Responds to:** your round-1 review of draft 1 (`review/L2_F9_INTERPRETATION_002_DRAFT1_ROUND1_REVIEW_2026-11-23_RECEIVED.md`, `3d892d6ebbbbcecbb3c9241c7acd0d510232a806a22cef445a9684b895efa2d9`, in this packet as received; archive `b489e5d703d592343f319ff164b19ddd27d3e37a4a27168026ffa7033490224b`; FINAL VERDICT: NOT SOUND).
**Repository pin:** `ee-theory-lab` `main` at `c6c21c497366d3ca71e0487127c774aacfd14ba1`, checked against the remote before this packet was built. Files under `flights/` other than `rulings_draft/` are byte copies of the pin (the evaluator among them is the placed one; its precedence repair is cleared and awaiting placement, and this record depends on no ordering it changed).
**Contract:** FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`. **Decision authority:** Mike.

## 0. Receipt first

As before: a receipt table (archive SHA-256 against the value Mike gives you, file count as the manifest lists it, every file's digest against `MANIFEST.txt`), then wait for Mike's "execute". Return one `.md` upload that cites this archive's SHA-256 and ends with exactly one plain line at column 0, `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND`.

## 1. Under review

`flights/mfa_fidelity/rulings_draft/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_2.md` (`c7d8b54901f021dcdbcaf69b5aa17abee2ae2e7d98c921259e80c6f910cbdb63`). Draft 1 is under `packet_only/draft1/`; `draft1_to_draft2.diff` is the plain `diff` between them.

## 2. Mike's decision since round 1

You confirmed one inclusion was his: the closure's own fit to the registered family and the fitted-level difference. L1 put it to him with a recommendation to keep them. **Mike, 2026-11-24: "yes".** Draft 2 keeps them and removes the confirmation paragraph and the strike recipe.

## 3. Your findings, one by one

| Your point | Draft 2 |
|---|---|
| **D1** — the draw trigger | Accepted; the sentence was L1's and ambiguous. L1 ran your witness (0 observed region cells; 324 cells, 72 bonds, 68 and 72 edge cells on the draw). Point 8 now has "When the draws are made": for complete valid inputs, 1,000 draws for every summary that applies under the coverage table, whether or not its observed value exists; your non-T0 case is named. "Fixed dependencies": a summary blocked on every draw by an unavailable closure or T0 reference is recorded "not assessed on the draws" with the fixed cause, distinct from "assessed on 1,000, defined on none"; a blocked summary does not stop the draws for the others. No fit is made on a draw for these summaries and none is added to the evaluator's. |
| §3.1 — regional counts | Zero is a defined count (Points 5 and 8). **L1 chose the lattice-only reading you left open:** the two counts do not depend on the closure and are reported, with ranges, when the closure is unavailable (Point 5; Point 9 has a row for it). The draft says this was L1's choice between your two. |
| §3.2 — fit gates and the signed quantity | Point 6: a closure λ* needs the closure map to pass step 4, a non-empty family and a fit within ε, with a note that the low-level fit applies no step-4 test itself. Point 7: d_Y = λ*_lattice,Y − λ*_closure,Y; each label on its own map. Point 8: the range [L_Y − c_Y, U_Y − c_Y] with the same count, which can exist without an observed d_Y. |
| Point 9 — point versus draw | A sentence at the head of Point 9; two rows separating "defined on none" from "blocked by a fixed dependency". |
| §6.1 — the stream dependency | Your wording, in Point 8 and in Consequences; "follows it" is gone. |
| §6.3 — bounds on build declarations; §5.9 | Consequences: the interpolation inside S is not reopened; the encoding of causes replaces no named cause; a build declaration cannot choose another availability domain or uncertainty target; every §5.9 binding that exists at the stage applies and the list is not a replacement. |
| §6.2 — cost | "No additional family search per draw for these summaries; the evaluator's own step-9 work stands; nothing here is a timing result." |
| Editorial 1 | §5.7 row 4 is now quoted in full and exactly. |
| Editorial 2 | "the least S among the contours examined …, which need not be the family minimum and is not λ*" (Point 10). |
| Editorial 3 | "where the summary needs them" (Point 8); "zeros after extinction" (constraint 3). |
| The strike recipe's missing Point 8 sentence | Moot: the fits are kept. |

## 4. Questions

**Q1.** Is D1 closed: would two builders now make the same draws and the same accounting in your witness state, and in the state where the closure edge exists and fails step 4?
**Q2.** Is the lattice-only reading of the regional counts stated consistently everywhere (Points 5, 8 and 9)? If you think it is Mike's to choose, say so.
**Q3.** Are the fit gates and the signed difference as you asked, and is anything about the kept fits still undetermined?
**Q4.** Did any repair change a point you accepted in round 1? `draft1_to_draft2.diff` is the whole change.
**Q5.** With the inclusion decided, does the draft still need any further word from Mike other than his acceptance of the record?
**Q6.** Anything else.
