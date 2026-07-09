# Stage 2 mini-contract - Amendment 1: permitted-input additions (Mike-approved 2026-07-09)

**Status: amendment to the frozen STAGE2_MINI_CONTRACT.md, blocker-driven, Mike-approved 2026-07-09; L2 rules on it as a named item inside the Case-1 harness build review. On any discrepancy the mini-contract as amended governs; nothing else in the mini-contract changes (unchanged-and-unweakened).**

## The blocker

The frozen implementation spec requires Engine A to pass an F3-analog gate: bit-exact reproduction of the committed null-extension NPZs. tcop_read.py (permitted) RECONSTRUCTS propensity fields but never SIMULATES; the committed RNG discipline (legacy global seeding, init shuffle, one shared rand_grid per tick) exists only in the committed run scripts. Additionally, the frozen pipeline's own byte-for-byte enforcement (verify_byte_for_byte) reads both committed sources at runtime. The Case-1 harness is unbuildable to spec without them.

## The amendment

Add to the Section 3 PERMITTED INPUTS for Case 1:
- cycle3/wave_two/c3_w2_tcop.py (sha256 466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7 - matches the committed build digest recorded at seeding)
- cycle3/wave_two/c3_w2_rule_c_m2.py (sha256 8f1f6ab9f188abe35dd257cb46e9ce7c9e51ad9ee1744c5945c10830d030ef59)

## Why this is safe

Both are pre-execution instrument scripts, committed BEFORE any probe run existed; they contain construction and machinery only, zero realized quantities. They are the same artifact class as the already-permitted tcop_read.py, whose own enforcement consumes them. The held-out record is unchanged. Blocker-driven per the parent amendment's Section 4 pattern; never budget-seeking; F1/F4 provenance discipline applies to their contents identically.

Drafting partner: Claude (Layer 1); arbitration: Mike (2026-07-09).
