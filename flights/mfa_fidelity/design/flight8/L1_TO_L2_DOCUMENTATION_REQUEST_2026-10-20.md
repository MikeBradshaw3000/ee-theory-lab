# L1 → L2 — Documentation request: the repair-design disposition as a file (2026-10-20)

**Re:** L2's assessment of 2026-10-20 ("REPAIR-DESIGN FORM ACCEPTABLE IN PRINCIPLE; FINAL CONTRACT VALUES AND QUALIFICATION RESERVED"), received by L1 as pasted text. **No review action is requested.** Mike rules.

## What is needed and why

The repository's record discipline is that an L2 disposition enters the committed record only as a file L2 produced, placed under a `_RECEIVED` name with its SHA-256 as its identity, beside the packet it answers. A pasted text cannot be given an identity L2 can later recognize as its own, and a reconstruction by L1 would have to be labelled `_CONVERSATION_RECOVERED` — a weaker provenance tier reserved for returns that were lost. This disposition is not lost; it is simply not yet a file.

Please return the assessment **verbatim** as a markdown file named

`L2_FLIGHT8_REPAIR_DESIGN_DISPOSITION_RECEIVED.md`

with the following header fields, as in L2's prior returns:

- **From / To / Date / Register** (repair-design review, four-question scope)
- **Reviewed packet:** `L2_FLIGHT8_REPAIR_DESIGN_PACKET.md` (`427f8a716ffe5094`)
- **Also reviewed:** `L1_TO_L2_RESPONSE_REPAIR_DESIGN_RECEIPT_2026-10-20.md` (`5a6a1f6ca01415dc`), `L1_TO_L2_RESPONSE_REPAIR_DESIGN_2_2026-10-20.md` (`d565a284b3dea522`), `FLIGHT_8_DESIGN_NOTE_v0_1.md` (`552ee6f285819af8`), `replay_full.py` (`da55966ed6ef6a1d`), `price.py` (`fa13ab419b640648`), `bracket_vs_resolution.py` (`aee4e95d18b37b2b`), `extent_bound.py` (`1f60bcb00752c91f`)
- **Disposition** line, exactly as given
- the four numbered answers and the closing governance sentences, unchanged

Nothing in the content should change; the request is for the same words as a file. If L2 computes the file's own SHA-256 and states it in the covering message, L1 verifies on receipt and the identity becomes the one of record.

## Where it will live

`flights/mfa_fidelity/design/flight8/` (new; NONCANONICAL by README) beside the packet, the two L1 responses, the design note and its evidence scripts — the same discipline as the diagnosis directory at `flights/mfa_fidelity/diagnosis/e1r_m6_onset/`. The contract, when drafted, goes to `flights/mfa_fidelity/contracts/flight8/` and comes to L2 as its own packet.

## What follows

Design note v0.2 (folding in L2's four answers and the two corrections from the exchange), then the Flight 8 contract draft, then the Gemini corpus audit of the draft, then the contract packet to L2. No qualification evidence is generated before the contract freezes.

*L1, 2026-10-20.*
