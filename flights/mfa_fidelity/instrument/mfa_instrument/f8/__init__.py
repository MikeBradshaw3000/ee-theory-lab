"""mfa_instrument.f8 — Flight 8 instrument package (Contract F8 v0.8.4, FROZEN 2026-10-23).

A new package beside `e1/`. Nothing in `e1/` is imported for its scientific values, modified, or
re-declared; E1's frozen identities stay what they are. Shared substrate helpers from the frozen
package root (`mfa_instrument.dynamics._moore_sum_a`, `mfa_instrument.config.MICRO_UNITS`) are
imported, never copied, so the Moore accumulation order of record is the one the specification
froze. Instrument version string: `f8_stage1_v1` (freeze record §3 item 25).
"""
