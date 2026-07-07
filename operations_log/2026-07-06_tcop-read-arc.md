# Ops log — 2026-07-06: TCOP read arc (spec → Amendment 1 → script → execution → findings)

**Session scope: Mike's explicit open of the read-spec stage through canonical findings. One arc, deferred-commit cluster. HEAD at open: a4fb946 (origin current, tree clean, cold-start confirmed from disk).**

## Grounding (primary source, not anchor summary)

Contract (8c94d8c), THRESHOLDING_ADDENDUM (8a777e6), design resolution, THRESHOLD_FIXING_READ_SPEC v2.1, threshold_fixing_read_results.json (v3, verified digit-for-digit vs addendum), TCOP_SEEDING_IMPLEMENTATION_SPEC, c3_w2_tcop_preflight.json (solved offsets verified: 0.04977134874876729 / 0.12339551870278656 / 0.24248438819907564, solved-always, u/2 gap within tol at every tier — diagnostic only), both CSV headers read from disk (the schedule column is `u_t`; handoff's "u_t_for" resolved to the build's function name), committed apparatus sources read in full (c3_w2_rule_c_m2.py, threshold_fixing_read.py, c3_w2_tcop.py), anchor 2026-07-06 supersession header confirmed current.

## Read spec

L1 draft v1 (four flagged arbitration items A1–A4) → L2 attack: reject-as-ratification-ready (5 major defects; replacement texts for G2 trend/c=0 handling, G3 bin grid + comparison universe, onset sentinel layer, exhaustive consistency audit, operational outcome rules) → L1 full-acceptance merge v2 with five disclosed refinements D1–D5 (max(0,·) dominance well-definedness; c=0 as sign-neutral path-(b) endpoint; lexicographic tracking burden → new A5; no-attenuation-allowance record; sentinel non-halting) → L2 fidelity pass CLEAN, D1–D5 accepted, A5 lexicographic preferred by L2 over its own either-or → **Mike arbitrated A1–A5 as jointly recommended (2026-07-06)** → CANONICAL, placed at cycle3/wave_two/TCOP_READ_SPEC.md, placement digest 56AAD2CFBFAFAA8ECDB997350C9A8A859E961BBF273314C4F50955A8E90693C0.

## Script + Amendment 1

tcop_read.py v1 L1-drafted (six disclosed determinations N1–N6). Mike routed to L2 for hostile pre-execution build review (safety step beyond the spec's required sequence). L2: reject-as-execution-ready — **one blocker (B1: path-(a) failure not bin/gate-qualified; exposed an internal tension in the ratified spec text)** + six amendments (D1 full global bin reporting; D2 exact index-set/identifier verification; D3 masked-prop cross-check; D4 full frozen-constant startup verification; D5 counts-only console; D6 named zero-mode diagnostics) + claims hardening (C1 wording; C7 runtime byte-for-byte enforcement). B1 routed to Mike as a clarifying spec amendment with joint L1+L2 recommendation; **Mike arbitrated option (i), bin-qualified** → TCOP_READ_SPEC_AMENDMENT_1.md CANONICAL, placed (digest 283E3D69BA7C524F815A98CD26B2B39781666E760EA5DC2F3EA0A8CCF1BD733F). tcop_read.py v2 folded everything; transit digest published before placement and **verified identical at destination: d60da1d92d72ddeb15353da301ea4e6161b9961e769936e42779170d8b399f7c** (repo root).

## Execution (Mike, 2026-07-06)

Clean completion, no halts, no .HALT.json. Console legible in-session (binding rule satisfied). Byte-for-byte enforcement PASS; structural verification PASS (315 runs, 5040/4095 rows, index sets exact, identifiers verified); **56,805 recorded-vs-reconstructed checks, worst |d| = 9.996e-17** (atol 1e-9); CM-0 comparator sets digest-frozen (9d68c551…) before any CM-1 processing; invariance self-check True. Output: cycle3/data_out/tcop_read_results.json (READ_RNG_SEED 20260706, frozen, no rerun).

## Result (candidate language; the JSON evidence table governs)

**UNDER-DETERMINED on both co-equal axes — no evaluable eligible comparison family. Apparatus limits, not evidence. The ordering hypothesis remains open; no produces claim, no risky-form failure claim, no evaluated path-(b) test.** Gate record: G1 135/135 incl. dominance (verified common-mode lift all tiers, strict-all); G4 176/180 (four (u=0, c=+0.35) rows fenced — floor-boundary effect, zero outcome bearing); G2 3/6 (negative sign passed all tiers; positive sign failed all tiers, monotone-in-tier near-miss deficits — compatibility with attenuation noted, mechanism NOT established, competing explanations open); path-(b) bin census for evaluable families 76 out-of-support / 6 count-failed / 4 phase-confounded / 0 eligible (the feasibility audit's predeclared necessary-not-sufficient contingency); c=0 record: zero flags, 3 single-window sentinels (two negative-signed), all G3_eligible=false; _amendment1_withheld empty.

Findings: v1 L1-authored from JSON → L2 interpretation-creep attack (amend-before-canonical: path-(a) partial-support leak removed; sentinel wording narrowed; 4a rewritten compatibility-only; 4c quantification corrected; top-line tightened) → v2 full-acceptance, all replacements verbatim → **Mike CONCUR** → CANONICAL at cycle3/wave_two/TCOP_READ_FINDINGS.md.

## Named open items (new this arc, both Mike's, both named-not-triggered)

1. **Attenuation-allowance design question:** the contract's "predeclared G4 slope attenuation allowance" was never emitted at thresholding; none was applied at read time; whether one should ever exist is a design question, not a finding.
2. **Matched-ρ geometry design question:** realized drive-induced ρ-stratification exceeded the frozen bin width; any evaluable ordering comparison requires a new design resolution (comparison-family geometry, tier placement, or matching unit) — never a relaxation of this read's frozen rules.

Carried unchanged: 9-window earned-window rule UNVERIFIED; CM-2 held; Rule E B/C held; L4 untouched; Comparator 0 unreclassified; Λ=0.20 named-not-triggered; no density-stability claim.

## Process notes

Attachment channel failed once mid-arc (my own merge document echoed back in place of L2's fidelity response) — caught by the no-verification-without-legible-evidence rule; re-send resolved it. All placements digest-gated; script transit digest published before placement and matched at destination. L2 build review (Mike's added safety step) caught a real blocker pre-execution — the third consecutive arc in which the interpretive-stage hostile review earned its cost.
