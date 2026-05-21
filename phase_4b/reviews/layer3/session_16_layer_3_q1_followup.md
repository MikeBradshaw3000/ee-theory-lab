# Layer 3 Follow-Up — Session 16, Q1 Primary-Source Verification

**From:** Mike Bradshaw, on behalf of Layer 1 (Claude)
**To:** Gemini (Layer 3)
**Context:** Follow-up on your Q1 return regarding shadow-copy structure scope across F-forms. Your structural claim (F_LR probe-distinct; F_2_symmetric probe1-only-genuine) is load-bearing for the item 6a pre-registration data-validity mask. Layer 1 is grounding that claim against primary source before downstream commitment, per Rule 1.

## Requested return

Two specific primary-source artifacts:

### 1. SHA-256 hash values

For the following six files, return the SHA-256 hash:

- `flight6_probe1_overcrowding_FLR_20x20.parquet`
- `flight6_probe2_starvation_FLR_20x20.parquet`
- `flight6_probe3_fusion_FLR_20x20.parquet`
- `flight6_probe1_overcrowding_F2sym_20x20.parquet`
- `flight6_probe2_starvation_F2sym_20x20.parquet`
- `flight6_probe3_fusion_F2sym_20x20.parquet`

(Adjust filenames if the canonical names differ from what I've written here. The 40x40 counterparts are not required for this verification — the 20x20 set is sufficient to ground the structural claim.)

The substrate-state test: the three F_LR files should produce three distinct hashes; the three F_2_symmetric files should produce two identical hashes (probe2 and probe3 matching probe1) and confirm the shadow-copy structure for F_2_symmetric.

### 2. flight2_production.py code excerpt

The `make_shadow_copies` invocation logic from `flight2_production.py` — specifically, the section that determines which F-form triggers shadow-copy generation and which probes receive shadow copies. A code excerpt (with surrounding context as needed for the logic to be intelligible) is what's needed; full-file is not required.

## What this is not asking

- Not asking for design-rationale interpretation (that was quarantined from your prior return as borderline architectural inference; the substrate facts are what's needed here)
- Not asking for any new implementation
- Not asking for any architectural commitment

## Return scope

Hashes + code excerpt. Brief.

— Routing drafted by Claude as Layer 1 central node, session 16 Q1 follow-up, for relay to Layer 3 via Mike.
