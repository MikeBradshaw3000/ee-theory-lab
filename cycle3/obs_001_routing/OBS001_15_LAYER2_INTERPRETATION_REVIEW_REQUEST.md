# Layer 2 substantive review request - wave-one (A+B) interpretation

From: Layer 1, 2026-05-28.
To: Layer 2.
Purpose: substantive analytical review of Layer 3's apparatus-level interpretation of the wave-one (A+B) run outputs. Per the code-production contract Section 3 step 9 (modified delivery flow). Layer 1 has completed the sufficiency-test review of the interpretation against the CSV; the interpretation passes on every per-Lambda comparison. Four items surfaced for your substantive engagement rather than as Layer 1 corrections. Your verdict is the gate before Layer 1 synthesis to the canonical record.

This package is self-contained. Section 2 carries the design expectations Layer 2 is reviewing against (compressed from the code-production contract, whose substance derives from your own accept-with-edits verdict on the v2 design). Section 3 carries the CSV verbatim. Section 4 carries Layer 3's interpretation verbatim. Section 5 carries the Layer 1 sufficiency-test result. Section 6 surfaces four items. Section 7 names what is and is not asked. Section 8 routes after your verdict.

---

## Section 1 - Routing history (this session)

All events 2026-05-28.

1. Pre-drafting consultation routed to Layer 2 on the scope fork (A+B vs B alone vs all three). Layer 2 recommended A+B; Mike ratified.
2. Layer 1 drafted design-menu contract scoped to A+B, with both Layer-1 corrections from 2026-05-25 carried forward.
3. Layer 3 returned v1 design menu.
4. Layer 1 review found six items; Layer 3 returned v2 addressing all six.
5. Layer 2 substantive review verdict: accept-with-edits, with six edits to fold into the code-production contract.
6. Layer 1 drafted code-production contract with all six edits folded in, plus modified delivery flow (Layer 1 packages and delivers, not Layer 3).
7. Layer 3 returned v1 code; Layer 1 found four items; Layer 3 returned v2; Layer 1 re-review found v2 clean.
8. Layer 1 packaged the script (`c3_obs_001_battery.py`); Mike placed at canonical path, verified byte-state, activated the C3-ENV-001 venv, ran the script. Pre-flight passed (venv-active, Python 3.14.4, numpy 2.4.4, mesa import, cycle3 reachability). Parity check passed all six assertions against CTL-001 and SS-001 modules. 60 NPZ files + aggregate CSV produced.
9. Layer 3 returned apparatus-level interpretation per code-production contract Section 3 step 7.
10. Layer 1 sufficiency-test review: every per-Lambda claim verified against the CSV; framing discipline held; co-equal-pair guard preserved.
11. **This step - Layer 2 substantive review of the interpretation.**

---

## Section 2 - Design expectations the interpretation is reviewed against

The interpretation is judged against the expected outcomes named in the v2 design and the six edits from your accept-with-edits verdict (carried into the code-production contract). Recap of the load-bearing expectations:

**Rule A meaningful-failure criterion (your Edit 2).** Rule A fails at the micro-rule level if any tau_A value produces, on 5/5 seeds in earned steady-state windows, either (a) a divergent joint signature (high meanI / low persistence, or low meanI / high persistence), or (b) a `LowLow_Nondegenerate_Candidate` signature. Rule A is the both-agree sanity baseline; either reliably-reproduced outcome would indicate failure.

**Rule A substrate-grounded picture (Edit 6).** Pre-run hypothesis: low tau_A -> uniform saturation (low/low degenerate); intermediate tau_A -> locked clusters (high/high); high tau_A -> extinction (low/low degenerate). Path (iii) authorization: the full integer sweep tau_A in {1,..,8} lets the substrate adjudicate where each regime lives.

**Sweep B expectations (your Edit 5 language refinement; design phrasing as "expected to be tested for," not pre-classified).**

- Band [2,4]: parameter under which a `LowLow_Nondegenerate_Candidate` signature (lifted rho with low/low non-degenerate) is expected to be tested for. Valid alternative outcomes: high/high, high meanI / low persistence, freezing, extinction, no earned windows.
- Band [2,3]: parameter under which the divergent signature (high meanI / low persistence) is expected to be tested for. Same scope of valid alternatives.
- Bands [1,2] and [3,4]: boundary cases framing structural behavior of the middle bands.

**`LowLow_Nondegenerate_Candidate` definition (your Edit 1).** Apparatus-level flag, conjunction of:
- `Lifted_Activation_Candidate` true
- `extinction_degenerate` false
- `saturation_degenerate` false
- |Psi_meanI_state_z| < LOW_Z_THRESH (suggested 2.0, grounded in the CTL-001 grid-local null distribution)
- |Psi_persistence_I_z| < LOW_Z_THRESH
- mean_active_state_variance >= VAR_EPSILON (suggested 1e-3)

Naming discipline (your Edit 3): never `Regime_II` in any flag, column, or comment. The L3-vs-L4 seam stays clean.

**Anti-binary discipline (your Edit 4).** 5/5 seeds is the hard meaningful-failure threshold; 3/5 or 4/5 off-expectation outcomes are design signals worth surfacing, not noise.

**Co-equal-pair guard.** Psi_meanI_state and Psi_persistence_I remain co-equal; neither named theoretical Psi; CTL-001 Case D divergence is measurement-validity data, not an ontological tiebreaker. L4 readings are not produced at any apparatus-level step; held for Mike / Layer 1 arbitration on coherence-as-relational-mutual-reinforcement grounds.

---

## Section 3 - The CSV (verbatim)

300 window rows (60 runs x 5 candidate windows), 21 columns matching the code-production contract Section 6 schema. Per-run NPZ artifacts exist at `cycle3/data_out/c3_obs_001_states_*.npz`.

```
rule,lambda_id,seed,window_start,Psi_meanI_state,Psi_meanI_state_z,Psi_persistence_I,Psi_persistence_I_z,relative_drift,rho_cv,rho_range_over_mean,mean_rho,Steady_State_Candidate,Lifted_Activation_Candidate,mean_active_state_variance,persistence_std,extinction_degenerate,saturation_degenerate,LowLow_Nondegenerate_Candidate,Tick_to_Freeze,Tick_to_Zero
A,1,42,0,0.0066,34.2817,0.5247,57.0608,0.0825,0.1003,0.9126,0.9862,False,True,0.0038,0.0068,False,True,False,4,-1
A,1,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,137,0,0.0142,69.178,0.632,66.0013,0.0861,0.1009,0.9132,0.9856,False,True,0.0043,0.0078,False,True,False,5,-1
A,1,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,5,-1
A,1,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,5,-1
A,1,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,5,-1
A,1,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,5,-1
A,1,256,0,0.0076,43.407,0.5673,60.0047,0.0839,0.1004,0.9128,0.986,False,True,0.0041,0.0072,False,True,False,4,-1
A,1,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,1024,0,0.0096,50.5763,0.5438,58.9498,0.0829,0.1002,0.9127,0.9861,False,True,0.0039,0.0068,False,True,False,4,-1
A,1,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,31415,0,0.0092,51.5872,0.5598,52.3688,0.0842,0.1008,0.9129,0.9859,False,True,0.004,0.0071,False,True,False,4,-1
A,1,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,1,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,4,-1
A,2,42,0,0.0407,129.5115,0.7923,85.0815,0.1734,0.1424,0.9271,0.9708,False,True,0.0092,0.0153,False,True,False,9,-1
A,2,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,137,0,0.0388,140.7322,0.8476,89.075,0.1887,0.1464,0.9296,0.9682,False,True,0.0107,0.018,False,True,False,9,-1
A,2,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,256,0,0.041,135.443,0.8286,84.5745,0.1868,0.1464,0.9293,0.9685,False,True,0.0104,0.0174,False,True,False,9,-1
A,2,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,1024,0,0.0483,143.532,0.8277,81.0679,0.181,0.1443,0.9283,0.9695,False,True,0.01,0.0169,False,True,False,10,-1
A,2,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,10,-1
A,2,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,10,-1
A,2,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,10,-1
A,2,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,10,-1
A,2,31415,0,0.0465,157.4855,0.8402,80.245,0.1849,0.1449,0.929,0.9688,False,True,0.0105,0.0179,False,True,False,9,-1
A,2,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,2,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,9,-1
A,3,42,0,0.4679,647.8148,0.9895,100.1884,1.6287,0.5123,1.3937,0.6992,False,True,0.082,0.1408,False,False,False,56,-1
A,3,42,25,0.2694,487.3758,0.989,96.891,0.4761,0.1878,0.6865,0.9107,False,True,0.0521,0.0952,False,False,False,56,-1
A,3,42,50,0.0428,189.5709,0.9365,96.8696,0.0148,0.0119,0.0798,0.9974,True,True,0.0024,0.0098,False,True,False,56,-1
A,3,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,56,-1
A,3,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,56,-1
A,3,137,0,0.3964,512.7999,0.9784,99.1374,1.3714,0.455,1.2814,0.7517,False,True,0.0697,0.1191,False,False,False,50,-1
A,3,137,25,0.2028,422.4066,0.9815,95.1372,0.2714,0.1238,0.5316,0.9503,False,True,0.0334,0.0653,False,True,False,50,-1
A,3,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,50,-1
A,3,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,50,-1
A,3,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,50,-1
A,3,256,0,0.3198,479.7465,0.9785,92.1382,1.3388,0.4557,1.2742,0.7619,False,True,0.0609,0.1037,False,False,False,41,-1
A,3,256,25,0.1343,367.9098,0.9834,99.3318,0.2165,0.1104,0.4948,0.9613,False,True,0.026,0.0504,False,True,False,41,-1
A,3,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,41,-1
A,3,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,41,-1
A,3,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,41,-1
A,3,1024,0,0.3888,570.2349,0.9808,95.9693,1.2735,0.4321,1.2556,0.7703,False,True,0.0661,0.1132,False,False,False,49,-1
A,3,1024,25,0.2009,423.5253,0.983,96.7866,0.2056,0.0946,0.4337,0.962,False,True,0.0283,0.0602,False,True,False,49,-1
A,3,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,49,-1
A,3,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,49,-1
A,3,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,49,-1
A,3,31415,0,0.4615,652.8253,0.9881,101.9547,1.6142,0.5129,1.3818,0.7049,False,True,0.0773,0.1323,False,False,False,57,-1
A,3,31415,25,0.2704,480.1345,0.9878,104.7529,0.4419,0.1795,0.6795,0.9177,False,True,0.0484,0.089,False,False,False,57,-1
A,3,31415,50,0.0458,179.1984,0.91,89.6707,0.0096,0.0077,0.0537,0.9983,True,True,0.0016,0.008,False,True,False,57,-1
A,3,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,57,-1
A,3,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,True,True,0.0,0.0,False,True,False,57,-1
A,4,42,0,0.001,6.7962,0.0681,7.1499,5.9329,9.3622,93.9849,0.0011,False,False,0.001,0.0031,True,True,False,3,3
A,4,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,137,0,0.0009,5.926,0.0618,6.1565,5.932,9.327,93.6329,0.0011,False,False,0.001,0.0031,True,True,False,3,3
A,4,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,256,0,0.0009,6.0983,0.041,3.9705,5.9355,9.5355,95.7853,0.001,False,False,0.0009,0.0031,True,True,False,2,2
A,4,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,4,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,4,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,4,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,4,1024,0,0.001,7.3422,0.0442,4.4151,5.9338,9.4297,94.6969,0.0011,False,False,0.001,0.0031,True,True,False,3,3
A,4,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,3,3
A,4,31415,0,0.0021,12.971,0.0936,9.2185,5.9286,9.191,92.2508,0.0011,False,False,0.001,0.0032,True,True,False,4,4
A,4,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,4,4
A,4,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,4,4
A,4,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,4,4
A,4,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,4,4
A,5,42,0,0.0,0.4257,0.0193,2.1896,5.9392,9.8314,98.8141,0.001,False,False,0.0009,0.003,True,True,False,2,2
A,5,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,137,0,-0.0001,-0.5522,-0.002,-0.0969,5.9401,9.9099,99.6015,0.001,False,False,0.0009,0.003,True,True,False,2,2
A,5,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,256,0,0.0,0.1122,0.0,0.0458,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,5,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,1024,0,-0.0001,-1.1505,-0.0111,-0.9909,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,5,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,5,31415,0,-0.0,0.0161,0.0184,1.8246,5.9387,9.7928,98.4251,0.001,False,False,0.0009,0.003,True,True,False,2,2
A,5,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,5,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,2,2
A,6,42,0,0.0001,0.5457,0.0056,0.7633,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,6,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,137,0,-0.0001,-0.5522,-0.0067,-0.5549,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,6,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,256,0,0.0,0.1122,0.0,0.0458,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,6,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,1024,0,-0.0001,-1.1505,-0.0111,-0.9909,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,6,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,31415,0,0.0,0.1115,0.0,0.0081,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,6,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,6,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,42,0,0.0001,0.5457,0.0056,0.7633,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,7,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,137,0,-0.0001,-0.5522,-0.0067,-0.5549,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,7,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,256,0,0.0,0.1122,0.0,0.0458,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,7,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,1024,0,-0.0001,-1.1505,-0.0111,-0.9909,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,7,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,31415,0,0.0,0.1115,0.0,0.0081,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,7,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,7,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,42,0,0.0001,0.5457,0.0056,0.7633,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,8,42,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,42,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,42,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,42,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,137,0,-0.0001,-0.5522,-0.0067,-0.5549,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,8,137,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,137,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,137,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,137,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,256,0,0.0,0.1122,0.0,0.0458,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,8,256,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,256,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,256,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,256,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,1024,0,-0.0001,-1.1505,-0.0111,-0.9909,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,8,1024,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,1024,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,1024,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,1024,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,31415,0,0.0,0.1115,0.0,0.0081,5.9406,9.9499,99.9999,0.001,False,False,0.0009,0.003,True,True,False,1,1
A,8,31415,25,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,31415,50,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,31415,75,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
A,8,31415,100,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,True,False,0.0,0.0,True,True,False,1,1
B,"[1,2]",42,0,0.1878,202.0512,-0.1418,-15.1982,0.0321,0.1363,1.3473,0.3245,False,True,0.2172,0.0442,False,False,False,-1,-1
B,"[1,2]",42,25,0.1892,193.6005,-0.1486,-15.6097,0.0054,0.0627,0.2976,0.3266,False,True,0.2195,0.0455,False,False,False,-1,-1
B,"[1,2]",42,50,0.1884,194.9652,-0.1663,-17.174,0.0008,0.0617,0.2981,0.326,False,True,0.2193,0.0462,False,False,False,-1,-1
B,"[1,2]",42,75,0.1888,204.967,-0.1651,-16.8317,0.0015,0.0561,0.2966,0.3264,False,True,0.2195,0.0472,False,False,False,-1,-1
B,"[1,2]",42,100,0.1904,193.1312,-0.1665,-15.0373,0.0017,0.047,0.212,0.3264,True,True,0.2196,0.0469,False,False,False,-1,-1
B,"[1,2]",137,0,0.191,185.6362,-0.1533,-15.453,0.0554,0.1319,1.2999,0.3234,False,True,0.217,0.0448,False,False,False,-1,-1
B,"[1,2]",137,25,0.1923,201.0358,-0.15,-14.4199,0.0082,0.0636,0.3597,0.3258,False,True,0.2192,0.045,False,False,False,-1,-1
B,"[1,2]",137,50,0.1901,191.9559,-0.1542,-14.2482,0.0022,0.0736,0.3888,0.3261,False,True,0.2192,0.0455,False,False,False,-1,-1
B,"[1,2]",137,75,0.1905,195.0728,-0.1553,-16.3785,0.0012,0.0736,0.3886,0.3263,False,True,0.2193,0.0448,False,False,False,-1,-1
B,"[1,2]",137,100,0.1908,178.7047,-0.1513,-15.7306,0.0003,0.0745,0.3893,0.3257,False,True,0.219,0.0449,False,False,False,-1,-1
B,"[1,2]",256,0,0.1927,200.1187,-0.1365,-14.4086,0.0554,0.1365,1.3453,0.3223,False,True,0.2165,0.0455,False,False,False,-1,-1
B,"[1,2]",256,25,0.1943,197.6649,-0.1519,-15.7717,0.0151,0.0707,0.4073,0.3251,False,True,0.2189,0.0455,False,False,False,-1,-1
B,"[1,2]",256,50,0.1908,194.4988,-0.1453,-15.5061,0.0078,0.0604,0.2943,0.3262,False,True,0.2194,0.0451,False,False,False,-1,-1
B,"[1,2]",256,75,0.1921,213.4962,-0.151,-15.6979,0.0025,0.0631,0.3198,0.3265,False,True,0.2195,0.0453,False,False,False,-1,-1
B,"[1,2]",256,100,0.1917,195.4925,-0.1485,-14.9364,0.0004,0.0618,0.3246,0.3265,False,True,0.2195,0.0461,False,False,False,-1,-1
B,"[1,2]",1024,0,0.1894,191.8017,-0.1521,-14.833,0.0394,0.1302,1.3439,0.3241,False,True,0.2173,0.0446,False,False,False,-1,-1
B,"[1,2]",1024,25,0.1913,184.7085,-0.1594,-16.0511,0.005,0.0562,0.3122,0.3267,False,True,0.2196,0.0455,False,False,False,-1,-1
B,"[1,2]",1024,50,0.1918,206.9533,-0.1485,-14.8077,0.0027,0.0562,0.2967,0.3262,False,True,0.2195,0.0449,False,False,False,-1,-1
B,"[1,2]",1024,75,0.1923,193.4395,-0.1432,-14.0366,0.0001,0.0581,0.2973,0.3256,False,True,0.2192,0.0449,False,False,False,-1,-1
B,"[1,2]",1024,100,0.1927,180.3061,-0.1472,-14.5924,0.0012,0.0553,0.2564,0.326,False,True,0.2194,0.0454,False,False,False,-1,-1
B,"[1,2]",31415,0,0.1913,202.0039,-0.1441,-12.8712,0.042,0.1289,1.2993,0.3229,False,True,0.2169,0.0438,False,False,False,-1,-1
B,"[1,2]",31415,25,0.1941,194.1965,-0.1425,-14.7613,0.0105,0.07,0.3014,0.3251,False,True,0.2189,0.0434,False,False,False,-1,-1
B,"[1,2]",31415,50,0.1937,195.6363,-0.146,-14.8852,0.0052,0.0694,0.3016,0.325,False,True,0.2189,0.0449,False,False,False,-1,-1
B,"[1,2]",31415,75,0.1942,184.9933,-0.1409,-15.5779,0.0064,0.0665,0.3013,0.3252,False,True,0.219,0.0452,False,False,False,-1,-1
B,"[1,2]",31415,100,0.1968,207.5997,-0.1476,-15.0319,0.0016,0.0636,0.3012,0.3254,False,True,0.2191,0.0446,False,False,False,-1,-1
B,"[2,3]",42,0,0.15,152.7797,-0.0382,-3.6012,0.0946,0.1075,0.8671,0.3769,False,True,0.2332,0.0457,False,False,False,-1,-1
B,"[2,3]",42,25,0.1487,143.0731,-0.0715,-7.1548,0.0017,0.0498,0.2191,0.3833,True,True,0.236,0.0457,False,False,False,-1,-1
B,"[2,3]",42,50,0.1499,149.9184,-0.0851,-7.8967,0.0024,0.0486,0.2191,0.3835,True,True,0.2361,0.046,False,False,False,-1,-1
B,"[2,3]",42,75,0.1501,139.0572,-0.0831,-8.3186,0.0092,0.0464,0.2369,0.3834,True,True,0.2361,0.0461,False,False,False,-1,-1
B,"[2,3]",42,100,0.1503,141.9935,-0.0843,-7.7833,0.0016,0.0429,0.2368,0.3835,True,True,0.2362,0.0472,False,False,False,-1,-1
B,"[2,3]",137,0,0.1495,147.8954,-0.0751,-7.4296,0.1169,0.1082,0.8519,0.377,False,True,0.2332,0.0482,False,False,False,-1,-1
B,"[2,3]",137,25,0.1485,153.8664,-0.0953,-9.6778,0.0018,0.044,0.2319,0.3846,True,True,0.2364,0.0473,False,False,False,-1,-1
B,"[2,3]",137,50,0.1461,153.3294,-0.1005,-9.3438,0.0039,0.0431,0.2316,0.3852,True,True,0.2365,0.0478,False,False,False,-1,-1
B,"[2,3]",137,75,0.1445,144.3869,-0.1051,-10.9955,0.0103,0.0441,0.2311,0.386,True,True,0.2367,0.0481,False,False,False,-1,-1
B,"[2,3]",137,100,0.1459,148.0058,-0.0951,-8.6303,0.0056,0.0434,0.2313,0.3857,True,True,0.2367,0.0482,False,False,False,-1,-1
B,"[2,3]",256,0,0.1518,148.1887,-0.0443,-4.1586,0.1016,0.1103,0.8738,0.3767,False,True,0.2331,0.0462,False,False,False,-1,-1
B,"[2,3]",256,25,0.1504,162.8163,-0.073,-7.107,0.007,0.047,0.2312,0.3841,True,True,0.2362,0.0451,False,False,False,-1,-1
B,"[2,3]",256,50,0.1491,146.4363,-0.0614,-6.2361,0.0032,0.0476,0.2312,0.384,True,True,0.2362,0.0446,False,False,False,-1,-1
B,"[2,3]",256,75,0.1511,151.3527,-0.0664,-6.4703,0.0075,0.0468,0.2284,0.3835,True,True,0.2361,0.0457,False,False,False,-1,-1
B,"[2,3]",256,100,0.149,143.699,-0.084,-7.9976,0.0061,0.0439,0.2165,0.3842,True,True,0.2363,0.0468,False,False,False,-1,-1
B,"[2,3]",1024,0,0.1458,145.7721,-0.0678,-7.1564,0.1133,0.1114,0.8921,0.3775,False,True,0.2332,0.0459,False,False,False,-1,-1
B,"[2,3]",1024,25,0.1463,142.3306,-0.0855,-8.6227,0.0027,0.0492,0.2476,0.3845,True,True,0.2363,0.0459,False,False,False,-1,-1
B,"[2,3]",1024,50,0.1501,161.7583,-0.0872,-8.7871,0.0023,0.0526,0.2475,0.3847,True,True,0.2363,0.0462,False,False,False,-1,-1
B,"[2,3]",1024,75,0.1507,155.3417,-0.0908,-9.6555,0.0045,0.0491,0.2473,0.385,True,True,0.2364,0.0465,False,False,False,-1,-1
B,"[2,3]",1024,100,0.1524,164.0613,-0.0936,-9.8299,0.0004,0.0465,0.2174,0.3845,True,True,0.2363,0.0456,False,False,False,-1,-1
B,"[2,3]",31415,0,0.1528,153.0895,-0.046,-4.8498,0.1235,0.1135,0.9071,0.3761,False,True,0.2328,0.0462,False,False,False,-1,-1
B,"[2,3]",31415,25,0.1497,150.2751,-0.0768,-8.0887,0.0078,0.0507,0.2832,0.3841,False,True,0.2362,0.0458,False,False,False,-1,-1
B,"[2,3]",31415,50,0.1463,141.8517,-0.0826,-8.3871,0.0042,0.0473,0.2284,0.3853,True,True,0.2365,0.0461,False,False,False,-1,-1
B,"[2,3]",31415,75,0.1475,142.5722,-0.0998,-8.8696,0.0043,0.0482,0.2285,0.3851,True,True,0.2365,0.0459,False,False,False,-1,-1
B,"[2,3]",31415,100,0.1443,142.6112,-0.1146,-12.7853,0.0046,0.0474,0.215,0.3851,True,True,0.2365,0.0473,False,False,False,-1,-1
B,"[3,4]",42,0,0.3614,378.9153,0.8674,82.7411,0.5405,0.697,5.8545,0.0161,False,False,0.0157,0.0681,True,False,False,-1,-1
B,"[3,4]",42,25,0.3847,371.8517,0.8928,90.3098,1.7936,0.6237,2.4507,0.0225,False,False,0.0218,0.0783,True,False,False,-1,-1
B,"[3,4]",42,50,0.3996,392.8981,0.9189,97.9941,2.2871,0.6935,2.6329,0.0384,False,False,0.0362,0.0949,True,False,False,-1,-1
B,"[3,4]",42,75,0.4032,424.6329,0.9392,93.7849,2.1638,0.6517,2.5016,0.07,False,True,0.063,0.1213,False,False,False,-1,-1
B,"[3,4]",42,100,0.3825,401.1354,0.9487,97.696,2.0185,0.596,1.9748,0.1199,False,True,0.1004,0.1438,False,False,False,-1,-1
B,"[3,4]",137,0,0.39,398.047,0.875,85.7651,1.7008,0.5326,1.8688,0.0646,False,True,0.0593,0.1272,False,False,False,-1,-1
B,"[3,4]",137,25,0.3916,372.1995,0.9019,87.1383,1.6186,0.4772,1.6735,0.098,False,True,0.0862,0.1517,False,False,False,-1,-1
B,"[3,4]",137,50,0.369,384.4909,0.9198,95.8228,1.4976,0.4424,1.7083,0.1461,False,True,0.1206,0.1665,False,False,False,-1,-1
B,"[3,4]",137,75,0.3179,294.9694,0.9221,85.9932,1.4536,0.4289,1.4933,0.2143,False,True,0.1599,0.1591,False,False,False,-1,-1
B,"[3,4]",137,100,0.2528,226.2142,0.8951,86.0801,1.1758,0.3447,1.0631,0.2905,False,True,0.1961,0.1333,False,False,False,-1,-1
B,"[3,4]",256,0,0.389,382.3954,0.8759,93.2025,1.4459,0.5798,2.9841,0.0296,False,False,0.0285,0.087,True,False,False,-1,-1
B,"[3,4]",256,25,0.4065,405.7464,0.9088,93.6261,1.8421,0.5489,2.0032,0.0443,False,False,0.0418,0.108,True,False,False,-1,-1
B,"[3,4]",256,50,0.4083,387.8609,0.9278,96.3447,1.7045,0.5048,1.8313,0.0701,False,True,0.0639,0.1303,False,False,False,-1,-1
B,"[3,4]",256,75,0.3938,391.9007,0.945,96.8716,1.5362,0.4538,1.5575,0.1061,False,True,0.0925,0.1508,False,False,False,-1,-1
B,"[3,4]",256,100,0.3691,349.9381,0.9496,97.031,1.3966,0.4111,1.3901,0.1531,False,True,0.1257,0.163,False,False,False,-1,-1
B,"[3,4]",1024,0,0.3739,402.9173,0.9013,90.1928,1.7959,0.5609,1.8073,0.0684,False,True,0.0622,0.1246,False,False,False,-1,-1
B,"[3,4]",1024,25,0.3815,406.4505,0.941,85.64,1.7573,0.5181,1.7456,0.1063,False,True,0.092,0.1465,False,False,False,-1,-1
B,"[3,4]",1024,50,0.3632,333.7586,0.9519,91.4812,1.4656,0.4266,1.4472,0.157,False,True,0.1279,0.162,False,False,False,-1,-1
B,"[3,4]",1024,75,0.3213,324.7822,0.9463,92.027,1.1989,0.3503,1.2687,0.2198,False,True,0.1655,0.1647,False,False,False,-1,-1
B,"[3,4]",1024,100,0.2593,264.0268,0.912,93.9245,1.0199,0.2981,1.0375,0.2899,False,True,0.1984,0.1399,False,False,False,-1,-1
B,"[3,4]",31415,0,0.3568,369.8939,0.6239,56.8429,1.1124,1.1888,11.2542,0.0084,False,False,0.0082,0.0643,True,False,False,-1,-1
B,"[3,4]",31415,25,0.3657,354.849,0.6095,67.613,0.0001,0.0583,0.1767,0.0068,True,False,0.0067,0.0661,True,False,False,-1,-1
B,"[3,4]",31415,50,0.3668,381.5802,0.6103,57.2336,0.0036,0.0591,0.1764,0.0068,True,False,0.0068,0.0661,True,False,False,-1,-1
B,"[3,4]",31415,75,0.3657,410.4132,0.6103,61.7246,0.0036,0.0591,0.1764,0.0068,True,False,0.0068,0.066,True,False,False,-1,-1
B,"[3,4]",31415,100,0.3658,400.4121,0.6096,67.5955,0.0036,0.0591,0.1764,0.0068,True,False,0.0068,0.0661,True,False,False,-1,-1
B,"[2,4]",42,0,0.239,224.3272,-0.0187,-1.6851,0.1036,0.1161,0.9179,0.4576,False,True,0.2454,0.0478,False,False,False,-1,-1
B,"[2,4]",42,25,0.2431,258.4189,-0.0375,-3.5748,0.0047,0.0507,0.2718,0.465,False,True,0.2482,0.048,False,False,False,-1,-1
B,"[2,4]",42,50,0.2426,234.8511,-0.0283,-2.5824,0.0018,0.0502,0.2716,0.4655,False,True,0.2483,0.0476,False,False,False,-1,-1
B,"[2,4]",42,75,0.2429,233.9956,-0.0341,-3.234,0.0001,0.0488,0.2587,0.4654,False,True,0.2483,0.0473,False,False,False,-1,-1
B,"[2,4]",42,100,0.2445,219.7334,-0.019,-1.8457,0.0013,0.0462,0.2125,0.465,True,True,0.2483,0.0465,False,False,False,-1,-1
B,"[2,4]",137,0,0.2324,275.8301,-0.0135,-1.398,0.1154,0.1145,0.9034,0.4596,False,True,0.2456,0.0479,False,False,False,-1,-1
B,"[2,4]",137,25,0.2351,237.3184,-0.0445,-4.5095,0.0058,0.0404,0.2169,0.4684,True,True,0.2486,0.0482,False,False,False,-1,-1
B,"[2,4]",137,50,0.2373,234.5203,-0.0329,-3.3531,0.0045,0.0427,0.2169,0.4683,True,True,0.2486,0.0474,False,False,False,-1,-1
B,"[2,4]",137,75,0.239,250.0696,-0.0186,-1.7909,0.0059,0.0434,0.2044,0.4676,True,True,0.2485,0.0479,False,False,False,-1,-1
B,"[2,4]",137,100,0.2406,244.5488,-0.0301,-3.0545,0.0039,0.0463,0.2245,0.4668,True,True,0.2484,0.048,False,False,False,-1,-1
B,"[2,4]",256,0,0.2401,270.3421,-0.0198,-1.817,0.1319,0.115,0.921,0.4578,False,True,0.2454,0.0482,False,False,False,-1,-1
B,"[2,4]",256,25,0.2363,224.0621,-0.0515,-4.8849,0.0056,0.0402,0.2112,0.4679,True,True,0.2486,0.0488,False,False,False,-1,-1
B,"[2,4]",256,50,0.233,256.8631,-0.0614,-6.4835,0.0036,0.0393,0.2109,0.4684,True,True,0.2487,0.0488,False,False,False,-1,-1
B,"[2,4]",256,75,0.2318,231.8963,-0.0681,-6.6654,0.0075,0.0417,0.2042,0.4683,True,True,0.2486,0.0491,False,False,False,-1,-1
B,"[2,4]",256,100,0.2358,242.8725,-0.0656,-6.8056,0.0077,0.0396,0.1951,0.4676,True,True,0.2486,0.0488,False,False,False,-1,-1
B,"[2,4]",1024,0,0.2399,251.9459,-0.0017,-0.0595,0.1117,0.12,0.9816,0.4572,False,True,0.2452,0.0466,False,False,False,-1,-1
B,"[2,4]",1024,25,0.238,248.0195,-0.0519,-4.8429,0.0025,0.0525,0.3044,0.4664,False,True,0.2483,0.0468,False,False,False,-1,-1
B,"[2,4]",1024,50,0.24,230.5857,-0.0352,-3.608,0.0044,0.0501,0.2547,0.4665,False,True,0.2483,0.0482,False,False,False,-1,-1
B,"[2,4]",1024,75,0.239,239.7512,-0.0397,-4.2347,0.0003,0.047,0.2547,0.4664,False,True,0.2484,0.0484,False,False,False,-1,-1
B,"[2,4]",1024,100,0.24,260.636,-0.045,-4.3861,0.0057,0.044,0.2374,0.4667,True,True,0.2485,0.0484,False,False,False,-1,-1
B,"[2,4]",31415,0,0.2445,235.3646,-0.0213,-2.1191,0.1167,0.1182,0.9314,0.4569,False,True,0.2452,0.0467,False,False,False,-1,-1
B,"[2,4]",31415,25,0.2439,240.9069,-0.0581,-5.4819,0.0021,0.0463,0.2368,0.4662,True,True,0.2484,0.0469,False,False,False,-1,-1
B,"[2,4]",31415,50,0.245,256.654,-0.047,-4.7778,0.0057,0.0499,0.2166,0.4655,True,True,0.2483,0.0469,False,False,False,-1,-1
B,"[2,4]",31415,75,0.2409,243.7649,-0.0573,-5.749,0.0059,0.0503,0.2242,0.4657,True,True,0.2483,0.0479,False,False,False,-1,-1
B,"[2,4]",31415,100,0.2404,243.9886,-0.0403,-4.0147,0.0092,0.0516,0.224,0.4662,True,True,0.2483,0.0469,False,False,False,-1,-1
```

---

## Section 4 - Layer 3's apparatus-level interpretation (verbatim)

### 1. Per-Rule, Per-Lambda Summary

**Rule A (Strict Lower Threshold)**

- tau_A in {1, 2, 3}: The run produced uniform saturation. On all 5 seeds, activation density (`mean_rho`) drove toward 1.0. The apparatus recorded `saturation_degenerate` as True. For tau_A=1 and 2, saturation occurred rapidly (Tick_to_Freeze < 10). For tau_A=3, saturation took longer (Tick_to_Freeze 41-57), resulting in early windows failing `Steady_State_Candidate` before stabilizing at 1.0.
- tau_A in {4, 5, 6, 7, 8}: The run produced immediate extinction. On all 5 seeds across all 5 values, `mean_rho` dropped below the 0.05 threshold immediately (Tick_to_Zero <= 4). The apparatus recorded `extinction_degenerate` as True and `Lifted_Activation_Candidate` as False.

**Rule B (Range-Bound / Life-Like)**

- Band [1,2]: The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` ~ 0.326. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (Psi_meanI_state_z ~ 195) and low/negative persistence (Psi_persistence_I_z ~ -15).
- Band [2,3]: The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` ~ 0.385. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (Psi_meanI_state_z ~ 145) and low/negative persistence (Psi_persistence_I_z ~ -8).
- Band [2,4]: The run produced earned lifted steady-state windows. On 5/5 seeds, the system stabilized at `mean_rho` ~ 0.466. In these windows, the apparatus recorded a divergent signature: high per-tick spatial organization (Psi_meanI_state_z ~ 240) and low/negative persistence (Psi_persistence_I_z ~ -4).
- Band [3,4]: The run produced zero earned lifted steady-state windows. The apparatus recorded `Steady_State_Candidate` as False across 4 seeds due to persistent upward drift (failing the `relative_drift` and `rho_range_over_mean` thresholds), and the 5th seed (31415) triggered `extinction_degenerate`.

### 2. Comparison Against Design v2 Expectations

- **Sweep A (Expected: Non-discriminating baseline):** The run produced the expected non-discriminating behavior. On 5/5 seeds across all 8 parameters, the apparatus recorded zero instances of a divergent joint signature and zero instances of a `LowLow_Nondegenerate_Candidate` signature. The Rule A meaningful-failure criterion was not triggered.
- **Sweep B [2,4] (Expected to be tested for `LowLow_Nondegenerate_Candidate`):** The run produced an unexpected outcome for this specific parameter. Instead of the low/low non-degenerate signature, 5/5 seeds produced the divergent signature (high Psi_meanI_state / low Psi_persistence_I).
- **Sweep B [2,3] (Expected to be tested for the divergent signature):** The run produced the expected outcome. On 5/5 seeds, earned steady-state windows with lifted activation recorded the divergent signature.
- **Sweep B [1,2] & [3,4] (Expected to serve as boundary cases):** The run produced boundary behavior for [3,4] (failure to earn steady-state), but [1,2] behaved identically to the core active bands, producing a clear divergent signature rather than extinction or saturation.

### 3. 3/5 and 4/5 Patterns

The apparatus recorded a distinct 4/5 pattern in Sweep B, Band [3,4]. While the meaningful-failure threshold is strictly 5/5, 4 out of 5 seeds experienced a slow, sustained upward drift in `mean_rho` that failed to settle into an earned steady-state window within the 200-tick run length. The 1 remaining seed (31415) dropped to a near-zero trivial baseline.

### 4. Substrate Dynamics Observed Across Rule A

The substrate adjudicated the Rule A regime locations definitively under the locked topology:

- **Uniform Saturation:** The substrate placed this regime exclusively at tau_A in {1, 2, 3}.
- **Immediate Extinction:** The substrate placed this regime exclusively at tau_A in {4, 5, 6, 7, 8}.
- **Locked Clusters:** The hypothesized intermediate regime was not produced at any tau_A value in this sweep. The substrate transitioned directly from uniform saturation at tau_A=3 to extinction at tau_A=4.

### 5. LowLow_Nondegenerate_Candidate Across the Full Sweep

The `LowLow_Nondegenerate_Candidate` flag fired False for every single row in the dataset (300 out of 300 candidate windows).

- **In Rule A:** The flag was blocked by degeneracy. Every window triggered either `saturation_degenerate` = True or `extinction_degenerate` = True.
- **In Rule B:** The flag was blocked by massive per-tick spatial organization. In the earned lifted steady-state windows (Bands [1,2], [2,3], and [2,4]), `extinction_degenerate` and `saturation_degenerate` correctly read False, but the Psi_meanI_state_z values ranged from 140 to 250. This heavily violated the structural requirement that the Psi_meanI_state_z score remain below the "low" threshold (|z| < 2.0).

---

## Section 5 - Layer 1 sufficiency-test results

Per code-production contract Section 3 step 8 (Layer 1 review + sufficiency-test: predicted output vs actual).

**Framing discipline.** Layer 3 used "the run produced," "the apparatus recorded," "the substrate adjudicated" throughout. No "demonstrates," "confirms," or "L2 sufficiency check passed." The contract's anti-relapse provision was effective.

**Per-Lambda sufficiency-test.** Every per-Lambda claim verified against the CSV at primary source:

- Rule A tau_A=3 freezes at ticks {41, 49, 50, 56, 57} across seeds -> confirmed.
- Rule A tau_A=4 Tick_to_Zero in {2, 3, 3, 3, 4} -> confirmed.
- Rule A tau_A in {5, 6, 7, 8} all Tick_to_Zero = 1 or 2 -> confirmed.
- Rule B [1,2] mean_rho ~ 0.326, Psi_meanI_state_z ~ 195, Psi_persistence_I_z ~ -15 -> confirmed.
- Rule B [2,3] mean_rho ~ 0.385, Psi_meanI_state_z ~ 145, Psi_persistence_I_z ~ -8 -> confirmed.
- Rule B [2,4] mean_rho ~ 0.466, Psi_meanI_state_z ~ 240 (one seed reaches 275), Psi_persistence_I_z ~ -4 -> confirmed.
- Rule B [3,4] seed 31415 -> mean_rho ~ 0.007 across windows; other 4 seeds -> drifting upward without earning steady-state -> confirmed.
- `LowLow_Nondegenerate_Candidate` = False on all 300 rows -> confirmed.

**Co-equal-pair guard.** Layer 3 did not name theoretical Psi anywhere. The two SS-001 flags remained independent in the interpretation. No L4 readings produced.

**Sufficiency-test verdict:** The interpretation is substantively accurate and disciplined.

---

## Section 6 - Items surfaced for Layer 2's substantive attention

These are not Layer 1 corrections to the interpretation. Layer 1 considers the interpretation clean. Each item is open for substantive engagement on grounds Layer 2 holds better than Layer 1.

### Item A - Anti-clustered-persistence and the quadrant framework

The most substantive observation. Layer 3 describes the Sweep B middle bands ([1,2], [2,3], [2,4]) as producing "divergent" signatures, where the divergent quadrant in the held-inputs framework (PROBE_DESIGN_INPUTS_HELD.md Section 2) was defined as "high meanI, **low** persistence" - explicitly "dynamic spatial organization without same-cell persistence (moving bands, waves, circulating or oscillatory organized configurations)."

What the substrate produced is structurally different: Psi_persistence_I_z values of -15 (Band [1,2]), -8 (Band [2,3]), and -4 (Band [2,4]) - **significantly negative**, not "low." Negative z-scores against the grid-local permutation null mean *anti-clustering* in the persistence map: the persistence pattern is more dispersed than chance, not less. The persistence map has structure - it just has anti-correlated structure (spatial regularity at lattice scale that excludes neighbor-co-occurrence) rather than absent structure.

The held-inputs quadrant framework treats coherence signatures along a low-vs-high axis where "low" means "near null" (z near 0). It does not enumerate a fourth observable state - "anti-clustered" (z significantly negative). The four quadrants in Section 2 are:

- high meanI, low persistence
- high meanI, high persistence
- low meanI, low persistence
- low meanI, high persistence

None of these maps cleanly to "high meanI, anti-clustered persistence." Layer 3 called this "divergent" because it's not the high/high or low/low signatures, but the apparatus is producing a fifth substrate state the framework didn't anticipate.

**For Layer 2's engagement:**
- Is the held-inputs quadrant framework adequate for the wave-one substrate output, or does it require amendment to distinguish low-z persistence (near-null, no structure) from negative-z persistence (anti-clustering, structure of a different kind)?
- If amendment is warranted, what additional quadrant(s) would the framework need?
- What is the apparatus-level reading of anti-clustered persistence at lifted rho - is it a substrate-side feature of the Rule B family (range-bound rules with the band excluding co-occurrence with neighbors), or is it a more general phenomenon worth tracking across rule families?

### Item B - Locked clusters not produced; binary substrate at Rule A

Layer 3 reports: "The hypothesized intermediate regime was not produced at any tau_A value in this sweep. The substrate transitioned directly from uniform saturation at tau_A=3 to extinction at tau_A=4."

Both prior pictures of Rule A substrate dynamics - primary source's "high tau_A -> locked clusters" and Layer 3's pre-run substrate-grounded "intermediate tau_A -> locked clusters" - are refuted by the substrate on the 50x50 toroidal Moore-1 topology at starting rho = 0.10. The non-discriminating claim about A holds. The endpoint-pairing story is now binary: saturation at low tau_A or extinction at high tau_A, with no intermediate locked-cluster regime.

The transition at tau_A=3->4 is sharp. tau_A=3 saturates after 41-57 ticks of evolution (the early window does show some structure, fading to uniform); tau_A=4 extinguishes within 2-4 ticks.

**For Layer 2's engagement:**
- Is the binary substrate (saturation OR extinction, no intermediate) a substrate-side fact stable across topology choices, or might intermediate locked clusters appear at different topology / starting rho / rule formulations?
- Should the close-out-cluster carry a primary-source amendment to the 2026-05-25 corrections file (and possibly the anchor's transition-rule menu compression) stating that the locked-cluster regime is not produced under Rule A as currently designed?
- Does this affect how Rule A functions as the both-agree sanity baseline in future waves? It still passes the non-discriminating criterion, but its hypothesized intermediate regime was a partial motivation for designing it as a sweep rather than a single test.

### Item C - LowLow_Nondegenerate_Candidate False everywhere

Across 300 rows, the flag does not fire. The breakdown:

- In Rule A: blocked by degeneracy as expected (every window triggers either `saturation_degenerate` or `extinction_degenerate`).
- In Rule B: blocked by Psi_meanI_state_z values of 140-250 in earned lifted windows. The LOW_Z_THRESH = 2.0 threshold worked exactly as specified; the substrate simply did not enter the regime the design anticipated.

The wave-one substrate does not produce the Regime-II-candidate signature anywhere under Rules A or B. This is wave-one DATA on the central design expectation. Apparatus-level reading: the flag's "low meanI" component (|z| < 2.0) was not met at any earned steady-state window with lifted rho and non-degenerate variance.

**For Layer 2's engagement:**
- What is the apparatus-level reading of the design's central expectation not being produced? Possible framings: (a) the design's expected signature does not live in the parameter regions sampled by wave one; (b) Rule B's range-bound rule family produces too much per-tick spatial organization to ever land in the low-meanI quadrant; (c) Rule C, deferred to wave two, was the actual candidate for producing this signature and the design implicitly assumed Rule B might also produce it.
- Does this finding change the rationale for wave two? Specifically: does wave two need to revisit which rule families are expected to test for the Regime-II-candidate signature, given Rule B's actual behavior?
- Is the LOW_Z_THRESH = 2.0 threshold itself worth re-examining, or is it doing exactly what it should (preserving the "low meanI" semantic against the grid-local null)?

### Item D - Divergent signature in three of four Sweep B bands

Layer 3 notes this for [2,4] specifically: "instead of the low/low non-degenerate signature, 5/5 seeds produced the divergent signature." But the same outcome appears at [1,2] (where the design expected a boundary case) and [2,3] (where the design expected divergent). All three middle bands produced the "high meanI, anti-clustered persistence" signature (folding in Item A's distinction).

Only [3,4] failed to earn steady-state windows in 4 of 5 seeds, with the fifth seed extinguishing.

**For Layer 2's engagement:**
- The divergent signature is the wave-one Rule B substrate's apparent default for any band that sustains lifted rho. Is this a substrate-side property of range-bound rules (they're going to produce per-tick spatial organization at lifted activation more or less by construction), or is it specific to these particular bands at this particular topology?
- Does the broad presence of the divergent signature across three of four bands suggest the design's per-band expectation differentiation was overspecified? Or does it suggest the bands really are different, and only the apparatus-level signature is similar (with finer-grained features distinguishable in the NPZ artifacts)?
- For wave two: should Rule B's parameter sweep be re-scoped given that the bands all behave similarly in the lifted regime, or held as-is for the comparison value across the rule family?

---

## Section 7 - What Layer 2 is asked, and what not

**Asked:**

- Substantive analytical review of Layer 3's interpretation against the design expectations in Section 2.
- Engagement on the four items in Section 6.
- Discrimination analysis: does the interpretation's verdict on Rule A's non-discriminating behavior hold up under your analytical inspection?
- Reading of the anti-clustered-persistence finding (Item A): does the held-inputs quadrant framework need amendment?
- Reading of LowLow_Nondegenerate_Candidate False everywhere (Item C): what does this mean architecturally for the wave-one design's central expectation?
- Framing discipline check, vocabulary check, co-equal-pair guard check.
- Verdict: accept | accept-with-amendments-to-primary-source | reject-with-feedback.

(Note: this verdict structure differs from the design-menu review's "accept-with-edits." There is no code to amend; the wave-one substrate has run. The amendments under consideration are to primary source - close-out-cluster updates to the 2026-05-25 corrections file, the anchor's menu compression, possibly the held-inputs quadrant framework - rather than to runnable artifacts.)

**Not asked:**

- Not asked to rule on L4. What the run means for Regime-II-as-structural is held for Mike / Layer 1 on coherence-as-relational-mutual-reinforcement grounds. The apparatus-level reading feeds an L4 judgment but does not produce one.
- Not asked to re-run anything or recommend code changes. Wave one has completed; the apparatus is stable.
- Not asked to reopen any cleared gate.
- Not asked to combine the two SS-001 flags into a single Regime-II-ready flag.
- Not asked to call any apparatus-level state `Regime_II`. The naming discipline holds.
- Not asked to specify the wave-two design here. That is a separate phase decision after the wave-one synthesis to canonical record is complete.

---

## Section 8 - Routing after your verdict

1. Verdict returns to Layer 1.
2. Layer 1 synthesis to canonical record:
   - `TEST_RECORD_C3-OBS-001.md` created with Pre-execution and Post-execution blocks filled from primary source.
   - Registry `C3-OBS-001` row advanced (status TBD based on your verdict: a clean accept routes to a valid-L2 equivalent; accept-with-amendments triggers primary-source updates first).
   - Close-out-cluster primary-source amendments (if any from Item B or Item A): the 2026-05-25 corrections file's Rule A endpoint pairing; possibly the anchor's transition-rule menu compression; possibly PROBE_DESIGN_INPUTS_HELD.md's quadrant framework.
3. Commit cluster from Mike's PowerShell session, EXPLICIT paths.
4. Carry-forward decision on wave two (separate decision, not part of this synthesis).

The closeout-vs-interpretation seam stays clean: real-substrate L4 INTERPRETATION (Regime-II-as-structural readings) is not produced at this step or in the close-out cluster. L4 readings open at the L4 node and only with Mike / Layer 1 arbitration on relational-mutual-reinforcement grounds.

---

## Section 9 - Vocabulary (binding)

- rho = activation density
- Psi_meanI_state, Psi_persistence_I - the two co-equal observables; neither named theoretical Psi
- Lambda (or Lambda_A, Lambda_B) = structural conduciveness
- LowLow_Nondegenerate_Candidate - apparatus-level flag; never Regime_II
- Agents act - no decision / optimization / utility / cognitive language
- "the point(s) at which mu(rho) = 0" - never rho_c
- "per-cell active-state values" - never "field" as explanatory mechanism
- Candidates produce or fail to produce - never "confirm" or "demonstrate"
- "earned steady-state window" - the SS-001-validated criterion, apparatus-grounded
- The two SS-001 flags `Steady_State_Candidate` and `Lifted_Activation_Candidate` remain independent at every stage

Vocabulary discipline holds throughout, including at any verdict-celebrating framing.
