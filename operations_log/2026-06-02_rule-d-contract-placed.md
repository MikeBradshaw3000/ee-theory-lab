# Operations log — 2026-06-02 Rule D design contract placed

**Session:** Cycle 3 wave two. New mechanism-class design target opened: Rule D, turnover-limited activation. Design contract drafted, routed to Layer 2 for mean-field review, amended per Layer 2's required precision amendments, and placed canonical at cycle3/wave_two/rule_d/RULE_D_DESIGN_CONTRACT.md. NO probe seeded; downstream opens D-1/D-2/D-3 not resolved.
**Layer:** Layer 1 (Claude) drafting/routing; Layer 2 (ChatGPT) mean-field review; Mike sole execution channel, arbiter, and router. Layer 3 not yet engaged.
**Opened from:** HEAD 6c14b48 (first-pass-rest ops log).
**Closed at:** HEAD 4a8a688, origin current.
**Outcome:** Rule D design contract canonical (1 file, 143 lines, new rule_d/ subdirectory). Fourth 2026-06-02 ops entry.

---

## Sequence

After the wave-two first-pass rest on A-prime, Mike proposed a new mechanism-class target rather than a Rule C second pass: Rule D, turnover-limited activation. Layer 1 pushed back before any spec on three points (fence, discrimination, scope), confirmed the three pillars with Mike via Layer 2, drafted the contract, routed it to Layer 2 for mean-field review, incorporated Layer 2's amendments, and placed it canonical at Mike's call.

## The mechanism target

Rule D tests whether lifted, non-degenerate near-null observables can be produced at RESPONSIVE local coupling because independent active-cell turnover prevents apparatus-level spatial / persistence organization from accumulating. A time-scale-mismatch claim, distinct from the floor-adjacent (coupling-absent) near-null Rule C and the comparators established. NOT a LowLow search; a named mechanism with a causal bet.

Distinct from object (c): object (c) had no named theoretical target and the M2 map pointed away from all four Section 5 patterns; Rule D supplies a named mechanism and reason, so it is a legitimate new arc rather than open-ended search.

## Three pillars (Layer 2-confirmed before drafting)

1. Turnover = independent stochastic Bernoulli deactivation hazard theta_turnover on active cells, fixed per setting, blind to neighbors / global rho / observables / SS diagnostics. Deterministic fixed lifetime rejected as canonical (age-cohort/periodicity confound), reserved as later audit. Survival is neighbor-BLIND churn, which keeps Rule D distinct from Rule B (whose issue was neighbor-conditioned survival).
2. Coupling = Rule C's centered logit-linear signed kappa on becoming-active, reused UNCHANGED. Turnover is the single new axis. Avoids two confounds (new-coupling artifact; Rule-B survival collapse).
3. Bracketing criterion (mandatory, pessimistic-on-passing): near-null counts as turnover-limited only if, at matched Lambda and matched responsive kappa, lower turnover is signed and intermediate turnover goes near-null while rho stays lifted and non-degenerate. Otherwise floor-adjacent / rule-forced / degenerate.

Symbol discipline: theta (theta_turnover in ASCII for code/CSV/filenames). NOT eta — eta(t) is the project's existing shared noise term (HKB/Haken lineage, Lake Vision genealogy); reuse would collide. Flagged to Mike and Layer 2, ratified.

## Layer 2 mean-field review (cleared with required amendments)

Layer 2 cleared order-parameter coherence: a density mean-field rho_{t+1} = (1-theta)rho_t + (1-rho_t)*sigma(logit(p_Lambda)+kappa(2rho_t-1)) shows lifted rho can coexist with nonzero turnover, and at the correlation level local coupling can inject correlations while independent turnover erases them — so responsive-coupling + near-null is not forced to be trivial. The mechanism is scientifically live. Accepted WITH required precision amendments (not place-as-is). All incorporated:

1. Section 2.3 update-order fence (new): synchronous update from t-state; turned-over cells do not re-enter same tick. Without it theta is not a clean lifetime hazard. (Load-bearing — would have silently changed the rule at implementation.)
2. Section 4.3 density-confound guard (new): turnover changes rho; a near-null row could be near-null from density displacement, not turnover suppression. Record rho_mean, rho_range_over_mean, bracket-level delta_rho_mean; audit, do not control (controlling would violate the fence).
3. Section 4.4 live-coupling exposure guard (new): realized endpoint contrast proves capability, not realized sampling; as theta changes rho the q_i distribution shifts. Record observed q_i distribution and mean absolute neighbor-induced perturbation; "responsive coupling" must be realized, not nominal.
4. Section 8 metrics for guards 2-3.
5. Wording: "coherent structure" -> "apparatus-level observable organization" (avoids implying L4 Psi assigned); "REFUTES" -> "fails to produce / negative result" (restores produce-or-fail-to-produce vocabulary — Layer 1's own quarantine slip, caught by Layer 2).

Convergence read: genuine. Layer 2 caught two confounds Layer 1 had not fenced (density, live-exposure) and one implementation hole (update order), and corrected a vocabulary slip. Substantive independent engagement, not ratification. The mean-field coherence answer was the load-bearing check — had it come back "fast churn re-reaches the floor, kappa irrelevant," the contract would have been revised or not placed; it did not.

## Edits and placement

Six str_replace amendments to the draft (Section 2.3, 4.3, 4.4, 8 metrics, two wording fixes, status header). Verified byte-state no BOM / single trailing LF / zero CRLF / size 15008; vocabulary-quarantine scan clean (only hit was the Regime_II prohibition statement itself). New subdirectory cycle3/wave_two/rule_d/ created. Delivered via create -> present_files -> Mike Copy-Item. Downloads held three same-named files; the bare name and (1) were the 11682-byte PRE-AMENDMENT draft, the amended canonical-ready file was (2) at 15008 — copied by SIZE (placing the bare name would have canonical-placed a contract missing the update-order fence and both guards). Destination verified first3=35,32,82 / last2=46,10 / size=15008. Staged by explicit pathspec; diff --cached one entry. Commit 4a8a688 (1 file, 143 lines, create-mode). Push confirmed `6c14b48..4a8a688  main -> main`.

## State at close

- HEAD 4a8a688, origin current, tree otherwise clean (untracked read_obs001_nearnull_scale.py at root unchanged).
- Rule D design contract CANONICAL at cycle3/wave_two/rule_d/RULE_D_DESIGN_CONTRACT.md. Mechanism, fences (incl. update order), coupling reuse, bracketing criterion, density + live-coupling guards, and interpretive role fixed. NOT seeded.
- Downstream opens UNRESOLVED (next design step, not a seed): D-1 theta grid range/density; D-2 responsive kappa settings; D-3 Lambda-anchor promotion (0.20/0.40 only vs promote reserved 0.30/0.50). All to be set against the realized scale after placement, never silently inside the mechanism definition; never justified by LowLow search.
- Rule C first pass still rests on A-prime; Comparator 0 / epsilon floor findings unchanged; weak-form Rule B prior untouched; L4 ontological question rides forward unsettled.
- Anchor not yet updated to point at the Rule D arc — flagged to Mike as the next housekeeping touch.

Drafting partner: Layer 1 (Claude).
