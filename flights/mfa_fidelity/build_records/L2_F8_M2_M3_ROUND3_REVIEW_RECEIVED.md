# L2 — Flight 8 M2/M3 Round-3 Adversarial Review

**Date:** 2026-10-28  
**Register:** Flight 8 instrument build; M2 and M3 jointly, including M1-r3 change  
**Verdict: DEFECT-WITH-REPAIR (verification hold only; no newly demonstrated H1/H3 source defect)**  
**Placement:** NOT CLEARED on the evidence independently verified in this review.

## Receipt and provenance

Examined the 45-file archive, including the round-3 response (`043cb2e1f1b23080`), `null.py` (`4ee3f239b27f772b`), `test_f8_m2_m3.py` (`d0d26e75280dffef`), runner (`126a0be4684f4975`), and three attempt/protocol records (`a95509d3e809d70b`, `834a788bd39ee771`, `b10a9d5a89e43978`). Local source hashes for the three executable files match the declarations.

## Test execution — incomplete

From `flights/mfa_fidelity/instrument`:

- `python -m pytest tests/test_f8_m2_m3.py -q`: interrupted by execution timeout after 14 displayed passing dots; **not** a 34-test pass.
- `python -m pytest tests/test_f8_m2_m3.py -q -p no:cacheprovider`: likewise interrupted after 14 displayed dots; **not** a completed pass.
- `python -m pytest tests/test_f8_m2_m3.py -q -k 'h1 or h3' -p no:cacheprovider`: **4 passed, 30 deselected** in 5.27 seconds.

These partial results cannot substantiate a claimed independent 34/34 run. In particular, the full M2/M3 suite's computationally costly law/cache/stepper checks were not completed in this review environment.

## H1 — registered protocol, ratification, attempt 2, and alpha disclosure

**Statistical rule: acceptable as a prospective decision rule, conditional on the asserted chronology.** The record encodes 1,000 independent replicate trajectories with one designated terminal window per replicate. The ratified protocol names the new master 320261027, shape 50 × 1,100 ticks, primary designated-window DKW at alpha 0.025, auxiliary 10-window union DKW at total alpha 0.025, and a requirement that **both** pass. Its advertised joint false-rejection union bound is 0.05, not 0.025. The registered protocol identity (`20ae18f0a85d9b6c…`) matches the record and the source literal; the runner checks the `null.py` identity, and source checks require ratification and registered run arguments. The prior failed 400-replicate attempt is retained in the protocol history and separate record.

**Observed result, as recorded:** designated sup deviation 0.0445029166 < registered primary bound 0.0468082612; maximum per-window deviation 0.0445029166 < auxiliary bound 0.0578126791. Therefore the recorded protocol decision, `qualification_passed = true`, is arithmetically correct. The ordinary module-default DKW at alpha 0.05 instead has bound 0.0429469408 and **fails** (`dkw_passed = false`; DKW tail upper bound 0.0380874). Both statements must remain visible in any clearance or reporting. This is not a conventional alpha-0.05 designated-window DKW pass. Lowering the test alpha raises its non-rejection boundary; the protocol's pass does not erase the default failure.

The archive asserts Mike ratified the protocol on 2026-10-27 before the attempt-2 run on 2026-10-28. The string `ratified_by` and dated file corroborate that registration was represented in the artifacts, but neither by itself provides independently time-stamped proof that ratification preceded draws. This is a provenance qualification, **not** a demonstrated contradiction. The registered rule's statistical legitimacy also does not turn the first attempt into a pass; its FAILED status remains binding.

**H1 ruling:** rule and recorded decision SOUND within the expressly registered protocol; chronological precedence is supported by submitted attestations, not independently audited timestamps. The alpha-0.05 default failure must always be disclosed.

## H2 — canonical regression

L1 reports `678 passed, 2 skipped` at HEAD `0f30400`, pinned repository root and canonical Windows environment, with output digest `8603cbaf338588e0…`. This is a specific, auditable **reported** regression result, not a locally reproduced result: the present 45-file archive does not recreate the entire canonical repository, pinned root, or canonical Windows environment, and L2 did not execute the complete regression. The locally attempted 34-test module also did not finish. Accordingly **H2 remains a verification hold**, rather than an identified failure in the canonical suite.

## H3 — qualification grammar

`production_scope_eligible` is distinct from `qualification_passed`, with protocol identifier and SHA-256 recorded. The `NullValidation` constructor disallows unregistered `qualification_passed = true`; `decide_under_protocol` gates decisions on a ratified protocol, its registered shape/master and eligible scope, and primary/auxiliary rule. The local H1/H3 targeted tests passed (4/4). The deprecated `is_qualification_evidence()` still returns *eligibility*, not passage, and must not be used as an affirmative qualification predicate. The promised M7 removal should remain a tracked obligation.

**H3 ruling:** SOUND for the explicitly documented transitional grammar, subject to the required deprecation warning and M7 removal. The available record is not a cryptographic proof that a `NullValidation` was generated by the stepper: protocol fields and `qualification_passed` are not authenticated signatures, and an informed caller can instantiate consistent records. Do not claim stronger provenance guarantees than the checks actually supply.

## Defect and exact repair

**V1 — Independent completion of the required 34-test run remains unverified.** The two attempted runs timed out after 14 dots; the targeted 4-test success does not discharge the full-module gate. **Repair:** Execute `python -m pytest tests/test_f8_m2_m3.py -q` to completion from the specified instrument directory in an environment sufficient for the full law/cache computation, capture the exit code, 34-test summary and environment information, and return the immutable output/digest for verification. If the suite fails, repair the specific source defects and resubmit changed-source identities and tests. Corroborate the canonical 678/2 regression by supplying its captured output and digest, or by a reproducible full canonical run on the pinned root. This is a verification/evidence repair, not authorization to alter the frozen contract or selectively respecify the qualification test.

## Disposition

**DEFECT-WITH-REPAIR — V1 verification hold.** No new source defect was established in the H1 decision arithmetic or H3 grammar. The H1 protocol is statistically coherent and the disclosed default-alpha failure is material. The claimed canonical regression and required 34-test completion remain L1 evidence rather than completed independent L2 checks; **do not place M2/M3 with M1-r3 under this review** until V1 is discharged.
