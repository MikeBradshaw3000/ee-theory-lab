# L1 → L2 — Flight 9 Interpretation 002 (fidelity summaries), draft 1: governance-record review, round 1

**Date:** 2026-11-23. **Register:** review of a draft ruling record (receipt first). Not a build review and not a run authorization. No code for these summaries exists.
**Repository pin:** `ee-theory-lab` `main` at `c6c21c497366d3ca71e0487127c774aacfd14ba1`, checked against the remote before this packet was built. Files under `flights/` other than `rulings_draft/` are byte copies of the pin. The draft is not committed.
**Contract:** `FLIGHT_9_CONTRACT_v0_7.md`, FROZEN, `60cf50fc8936abef7f92ef20ad3ab7f6d12e6e1dbdbd2d8f963058c09e73d168`.
**Decision authority:** Mike.

## 0. Receipt first

Reply with a receipt table before any review content: the archive's SHA-256 against the value Mike gives you, the file count as the manifest lists it, and every file's full digest against `MANIFEST.txt`. Then wait for Mike's "execute". Return the review as one `.md` upload that cites the archive's SHA-256 and ends with exactly one plain line at column 0, either `FINAL VERDICT: SOUND` or `FINAL VERDICT: NOT SOUND` (no bold, no backticks, nothing after it).

## 1. What is under review

`flights/mfa_fidelity/rulings_draft/F9_INTERPRETATION_002_FIDELITY_SUMMARIES_DRAFT_1.md` (`b2efdeda1d063ccb6d46d66e0c8d0881d5131015221d1e4f20fb6bed943d1a07`): L1's draft of an interpretation beside the frozen contract, fixing the reductions of §1.2′ (ii) and (iii) and their uncertainty before any output exists. When accepted it would be placed in `rulings/` without `DRAFT_1` in its name and with its authority statement brought up to date.

## 2. How it came about

- L1's consultation (`consultation/L1_TO_L2_…`, `5811f97b…`) put eight open points and a proposal for each.
- Your advice (`consultation/L2_…_RECEIVED.md`, `c9df277a8d38449b2c37417e167a1aa6971f2fd8081a4283cac0f9cdf8b0156b`, in this packet as received) corrected four things in L1's proposal (T0's edge exclusion; λ*'s own range recipe; §2.8's persistence of local m; the absence of any component correspondence across draws), recommended differently on two (m on under-resolved edges; rebuilding the region on each draw), offered a six-point package, and named one supported smaller alternative (occupancy only).
- L1 accepted all six and recommended to Mike: adopt the package; include the direct edge comparison; record it as an interpretation reviewed by you before any code.
- **Mike, 2026-11-23: "Adopt, include, l2 review".**

## 3. Where the draft goes beyond those three words (say if any of this is not L1's to write)

1. **The closure's own fit to the family and the fitted-level difference** (Point 6, last paragraph; Point 7, "Fitted levels"). L1's original proposal F had them; you called them optional; Mike's "include" answered the question about the direct edge comparison. The draft includes them and marks them "For Mike's confirmation", with the text to strike if he prefers the smaller report.
2. **Skeleton coverage of Points 6 and 7.** Your coverage table gives the skeleton "Item (iii)"; the draft reads that as occupancy and edges both, with the skeleton closure.
3. **The regional cell counts get ranges** (Point 8), since the region is rebuilt on each draw and its size is then a numeric scalar of the draw.
4. **"The draws are made whenever any summary of the level is defined."** On T0 that means 1,000 draws per level for whole-lattice Point 5 alone.
5. **The list left to build declarations** (Consequences, second bullet).

## 4. Questions

**Q1.** Does each point state your advice accurately where it says it follows it? Is anything you advised missing, weakened or strengthened?
**Q2.** For each of Points 1 to 10: is the interpretation determinate enough to build from, so that two builders would compute the same numbers up to the conventions the draft leaves to build declarations? Name any point where they could not.
**Q3.** Does any point change, or appear to change, something the frozen contract fixes? Check the seven constraints as restated against the contract's own words.
**Q4.** The five items of §3 above: for each, acceptable in the record, to be struck, or a separate ruling for Mike?
**Q5.** The authority statement: does it say exactly what has and has not been ruled? Is the confirmation in Point 6 the only place where the draft needs a further word from Mike?
**Q6.** Is anything in the Consequences section wrong or overstated, in particular the dependency on the second reports module's skeleton stream (that module's source, in review and not placed, is under `packet_only/m6b_in_review/` for reference only and is not under review here)?
**Q7.** Anything else.
