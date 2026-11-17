"""mfa_instrument.f9 — Flight 9 instrument package (Contract F9 v0.7, FROZEN 2026-11-15 by the freeze
record placed at 595ddc8).

A new package beside `e1/` and `f8/`. Nothing in `e1/` or `f8/` is modified or re-declared. The shared
substrate helper of the frozen package root (`mfa_instrument.dynamics._moore_sum_a`) and
`mfa_instrument.config.MICRO_UNITS` are imported, never copied. Instrument version string:
`f9_stage1_v1` (freeze record §3.2 item 18).

Module M1 (this placement): `config` (frozen declarations), `terrain` (bases, compositions, comparison
arrays, serialization), `geometry` (edge bonds and traced components, contract §5.5 step 3), `family`
(the registered contour family, §5.5 step 5), `spectral` (spectral-relative gain, §2.8) and
`identities` (the build of contract §3.4 step 4). M1 holds no seed, no master and no dynamics.
"""
