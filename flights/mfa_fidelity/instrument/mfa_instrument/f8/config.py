"""mfa_instrument/f8/config.py — Flight 8 module M1: configuration, sweep identity, seed panel,
stream derivation, and the frozen-declaration preflight (Contract F8 v0.8.4 §2, §4.1, §4.5, §8;
freeze record §3; design note v0.3 §5 M1).

FROZEN OBJECTS (immutable literals bound to hardcoded digests, recomputed at every preflight):
  F8_LEVELS_MICRO   — the 24 pass-1 control values m in exact integer micro-units, endpoints
                      250000 and 2500000, interior by exact rational round-half-even (contract
                      §4.1); EQUAL BY LITERAL to the `levels_micro` list of APPENDIX_A_OF_RECORD.md
                      (`94d527624beafa7c…`), the object of record.
  F8_SEED_PANEL     — the 20 canonical seeds, drawn ONCE at build (2026-10-26) from a NEW declared
                      master by the E1 derivation rule and hardcoded; reused at every level and in
                      every canonical sweep (paired by seed). The E1 master 20260917 is retired.
  F8_CALIBRATION_SEED_PANEL — the 20 seeds of the two-part calibration census (contract §7.3 job 0),
                      drawn once from a SEPARATE declared master, never reused for a canonical job.
  Rule parameters   — mu = 0.2, g = 1 (not swept), eta0 = -ln(1 - 0.01) (RULED), grid 50, ticks
                      3000, tail 1000 in 10 windows of 100, rho0_low = 0.02, W_res = 3 spacings.

Both masters are BUILD DECLARATIONS (contract §8 marks the masters DERIVED@BUILD): they are of
record only when Flight 8's governance record names this module's identity. Nothing here runs a
sweep; `f8_run_spec` builds the immutable specification of one (level, seed, object) run and the
dynamics module executes it.

Stream derivation (contract §2.5, §4.11 independence basis). Every (seed, level, object) run gets its
own Generator: np.random.default_rng(SeedSequence([seed, OBJECT_CODE, level_micro])). The seed is a
panel member (derived from the master); the level is its exact micro-unit identity; the object code
separates the skeleton-high, skeleton-low, realization and null runs of one (seed, level) so that no
draw is shared across objects or levels. The skeleton-low initialization pattern is drawn from a
further declared stream (code INIT_LOW) so it is independent of the run's tick draws.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import types
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

import numpy as np

from ..config import MICRO_UNITS

F8_VERSION = "f8_stage1_v1"                       # freeze record §3 item 25
F8_CONTRACT_SHA256 = "e87277a2d11e948f3014210d56c4db2eaad15a3f8c86427d8086737ac435d182"      # FLIGHT_8_CONTRACT_v0_8_4.md
F8_APPENDIX_A_SHA256 = "94d527624beafa7c81decce4be21470d75dc31e232fc5277df41a5fd60f87653"    # APPENDIX_A_OF_RECORD.md
F8_FREEZE_RECORD_SHA256 = "16869692a043b139"                                                  # FLIGHT_8_FREEZE_RECORD.md (prefix; M7 binds the full file)

# ----------------------------------------------------------------------------- frozen sweep identity (contract §4.1, §8)
F8_GRID = 50
F8_TICKS = 3000
F8_TAIL_TICKS = 1000
F8_WINDOW = 100
F8_N_WINDOWS = 10
F8_M_MIN_MICRO, F8_M_MAX_MICRO = 250_000, 2_500_000
F8_PASS1_LEVELS = 24
F8_MU = 0.2                                       # deactivation rate (the Overview's lapse beta; NOT the Overview's mu(rho))
F8_G = 1.0                                        # feedback gain, not swept; m absorbs it
F8_ETA0 = -math.log(1.0 - 0.01)                   # realization floor hazard, RULED: -ln(1 - 0.01) ~ 0.0100503
F8_DT = 1
F8_RHO0_LOW_MICRO = 20_000                        # skeleton-low initialization fraction 0.02, in micro-units
F8_W_RES_SPACINGS = 3


def _round_half_even(fr: Fraction) -> int:
    q, r = divmod(fr.numerator, fr.denominator)
    twice = 2 * r
    if twice < fr.denominator: return q
    if twice > fr.denominator: return q + 1
    return q if q % 2 == 0 else q + 1


def generate_pass1_levels_micro() -> Tuple[int, ...]:
    """Exact-rational generation: level_j = 250000 + round_half_even(j · 2250000 / 23), j = 0..23
    (contract §4.1; Appendix A row 's')."""
    span = Fraction(F8_M_MAX_MICRO - F8_M_MIN_MICRO)
    return tuple(F8_M_MIN_MICRO + _round_half_even(Fraction(j) * span / (F8_PASS1_LEVELS - 1)) for j in range(F8_PASS1_LEVELS))


# FROZEN LITERAL — equal to APPENDIX_A_OF_RECORD.md `levels_micro` (object of record); verified against the rule at every preflight
F8_LEVELS_MICRO: Tuple[int, ...] = (
    250000, 347826, 445652, 543478, 641304, 739130, 836957, 934783, 1032609, 1130435, 1228261, 1326087,
    1423913, 1521739, 1619565, 1717391, 1815217, 1913043, 2010870, 2108696, 2206522, 2304348, 2402174, 2500000,
)
S_P1_MICRO = 97826                                # the pass-1 spacing s (21 gaps); 97827 at 2 gaps by rounding (Appendix A)
S_P1_MAX_MICRO = max(b - a for a, b in zip(F8_LEVELS_MICRO, F8_LEVELS_MICRO[1:]))
W_RES_MICRO = 293_478                             # declared resolution, 3 s (contract §4.5; freeze record §3 item 18)

# FROZEN SEED PANELS — BUILD DECLARATIONS (DERIVED@BUILD, contract §8): drawn once by the E1 rule from the masters below.
F8_SEED_PANEL_MASTER = 20261026                   # canonical panel master (build date); E1's 20260917 retired
F8_CALIBRATION_MASTER = 120261026                 # calibration-census master (contract §7.3 job 0), separate from all others
F8_SEED_PANEL: Tuple[int, ...] = (
    2601517389, 3379839832, 1589273066, 2703936042, 1530244675, 3901944897, 424388694, 2009899952,
    1635189879, 85538278, 49718904, 2287089062, 4211530381, 3340776081, 1475811144, 4160026138,
    2714859398, 3276505008, 4232330970, 1535487098,
)
F8_CALIBRATION_SEED_PANEL: Tuple[int, ...] = (
    3655077383, 2434248556, 295943332, 572059033, 1457873450, 2522627012, 2556733859, 3004017565,
    1323250378, 1987703677, 706797421, 455734318, 1709291720, 2972779286, 1557256973, 3770476374,
    2468903748, 3687455893, 1937104091, 938334236,
)


# E1's RETIRED panel (mfa_instrument/e1/config.py E1_SEED_PANEL, master 20260917), carried as a literal bound to E1's own
# frozen digest so the disjointness of the F8 panels is checked against the actual retired seeds (L2 M1 r1 D4), with no
# import of e1 at run time.
E1_RETIRED_SEED_PANEL: Tuple[int, ...] = (
    2117405799, 2804871216, 375183601, 701843324, 1075314870, 1719551416, 2685479494, 2666970591,
    632470092, 278031864, 2244203769, 3565777195, 1541399456, 2906227949, 4151989313, 2628184833,
    757868360, 872858888, 3907060348, 629405355,
)
E1_RETIRED_SEED_PANEL_SHA256 = "68309ed9f8be58088952675f2062afad2f59e3ebef10517ac43210b726a1c70d"   # = E1_SEED_PANEL_SHA256_LITERAL


def generate_seed_panel(master: int, n: int = 20) -> Tuple[int, ...]:
    """The E1 derivation rule, carried: SeedSequence(master) -> Generator -> n draws of uint32 without replacement."""
    g = np.random.default_rng(np.random.SeedSequence(int(master)))
    out: List[int] = []
    while len(out) < n:
        s = int(g.integers(1, 2**32 - 1))
        if s not in out: out.append(s)
    return tuple(out)


# ----------------------------------------------------------------------------- objects and streams (contract §2.6, §2.9, §4.11)
OBJECT_CODES: Dict[str, int] = {
    "skeleton_high": 1,       # eta_floor = 0, all cells active at t = 0 (deterministic; no init draw)
    "skeleton_low": 2,        # eta_floor = 0, fraction rho0 = 0.02 active, pattern from the INIT_LOW stream
    "realization": 3,         # eta_floor = eta0, stationary-null start drawn from the run stream
    "null": 4,                # g = 0 with eta_floor = eta0: independent two-state chains, stationary start
}
INIT_LOW_CODE = 10            # the declared stream for the skeleton-low initialization pattern


def stream_key(seed: int, obj: str, level_micro: int) -> Tuple[int, int, int]:
    return (int(seed), OBJECT_CODES[obj], int(level_micro))


def generator_from_key(key: Tuple[int, int, int]) -> np.random.Generator:
    """The run's one Generator from its recorded stream key: one uniform per cell per tick, plus the realization/null
    stationary-start draw."""
    return np.random.default_rng(np.random.SeedSequence([int(k) for k in key]))


def run_generator(seed: int, obj: str, level_micro: int) -> np.random.Generator:
    return generator_from_key(stream_key(seed, obj, level_micro))


def init_low_generator(seed: int, level_micro: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([int(seed), INIT_LOW_CODE, int(level_micro)]))


# ----------------------------------------------------------------------------- the control coordinate (contract §2.8, §3.1)
def q_deact(mu: float = F8_MU, dt: int = F8_DT) -> float:
    """q = 1 - exp(-mu dt): the single-tick deactivation probability."""
    return 1.0 - math.exp(-mu * dt)


def lambda_bar_from_level(level_micro: int, *, mu: float = F8_MU, g: float = F8_G, dt: int = F8_DT) -> float:
    """m := g·lambda_bar·dt / (1 - e^(-mu dt))  =>  lambda_bar = m·(1 - e^(-mu dt)) / (g dt), m = level_micro / 1e6 exactly."""
    return (float(Fraction(int(level_micro), MICRO_UNITS)) * q_deact(mu, dt)) / (g * dt)


def homogeneous_base_from_lambda(lam: float) -> float:
    """F_2_symmetric(v, u, r) = (v·u·r)·(w_v v + w_u u + w_r r) with w summing to 1.0; at v = u = r = b it is b^4,
    so the homogeneous base that reaches lambda_bar is b = lambda_bar^(1/4). F is inert under homogeneous bases
    (freeze record §3 item 2); the hazard consumes lambda_bar directly and b is recorded for the declaration."""
    if not (0.0 <= lam <= 1.0): raise F8ConfigError(f"lambda_bar {lam} outside [0, 1]: not reachable by bases in [0, 1]")
    return lam ** 0.25


# ----------------------------------------------------------------------------- the declaration
F8_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", F8_VERSION), ("contract_sha256", F8_CONTRACT_SHA256), ("appendix_a_sha256", F8_APPENDIX_A_SHA256),
    ("grid", F8_GRID), ("ticks", F8_TICKS), ("tail_ticks", F8_TAIL_TICKS), ("window", F8_WINDOW), ("n_windows", F8_N_WINDOWS),
    ("m_min_micro", F8_M_MIN_MICRO), ("m_max_micro", F8_M_MAX_MICRO), ("pass1_levels", F8_PASS1_LEVELS),
    ("levels_micro", F8_LEVELS_MICRO), ("s_p1_micro", S_P1_MICRO), ("s_p1_max_micro", S_P1_MAX_MICRO), ("w_res_micro", W_RES_MICRO),
    ("mu", F8_MU), ("g", F8_G), ("eta0", F8_ETA0), ("dt", F8_DT), ("rho0_low_micro", F8_RHO0_LOW_MICRO),
    ("f_dispatch", "F_2_symmetric"), ("bases", "homogeneous"), ("q", "off"), ("drive", 0.0), ("noise", 0.0),
    ("timing", "synchronous_two_phase"), ("neighbourhood", "moore_8_periodic"),
    ("object_codes", tuple(sorted(OBJECT_CODES.items()))), ("init_low_code", INIT_LOW_CODE),
    ("seed_panel_master", F8_SEED_PANEL_MASTER), ("seed_panel", F8_SEED_PANEL),
    ("calibration_master", F8_CALIBRATION_MASTER), ("calibration_seed_panel", F8_CALIBRATION_SEED_PANEL),
    ("e1_retired_panel_sha256", E1_RETIRED_SEED_PANEL_SHA256),
    ("reduced_shape_policy", ("grid>=3", "ticks>=window", "tail=min(1000,ticks)", "tail%window==0")),
)
F8_FROZEN = types.MappingProxyType(dict(F8_DECLARATION))


def frozen_digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


F8_LEVELS_SHA256_LITERAL = "7eefeea75a3d8012afec5ebc6ab7243c56aaa7cbc0c061d27476c1a2e40bdcac"
F8_SEED_PANEL_SHA256_LITERAL = "088c914cfb47682a06f68e8fdae895ad1c60b0f016a371d4c7c038c6f33a2cfe"
F8_CALIBRATION_PANEL_SHA256_LITERAL = "8c12e7c2a942f63db313458c4eb5f5b57b8b20df4b0bfde41f9d4e996dcb8fe9"
F8_DECLARATION_SHA256_LITERAL = "0d9657d79c8b1c63552db1e5b4e5859ebd6afecb8f77c44fca2f019ef60e0a55"


class F8ConfigError(ValueError):
    """A frozen F8 identity or admissibility rule is violated."""


def level_id(level_micro: int) -> str:
    """Canonical level identifier: the exact m value under the frozen '%.6f' format (contract §2.5)."""
    return "%.6f" % (Fraction(int(level_micro), MICRO_UNITS))


def verify_frozen_identity() -> Dict[str, str]:
    """Recompute every frozen identity from its rule and compare to the literals. Fail-closed."""
    if generate_pass1_levels_micro() != F8_LEVELS_MICRO:
        raise F8ConfigError("frozen level list differs from its generating rule")
    if len(set(F8_LEVELS_MICRO)) != F8_PASS1_LEVELS or list(F8_LEVELS_MICRO) != sorted(F8_LEVELS_MICRO):
        raise F8ConfigError("frozen level list is not injective and ascending")
    if len({level_id(m) for m in F8_LEVELS_MICRO}) != F8_PASS1_LEVELS:
        raise F8ConfigError("frozen level list is not injective under the '%.6f' identity format")
    if (F8_LEVELS_MICRO[0], F8_LEVELS_MICRO[-1]) != (F8_M_MIN_MICRO, F8_M_MAX_MICRO):
        raise F8ConfigError("frozen level list endpoints are not the contracted sweep range")
    gaps = sorted({b - a for a, b in zip(F8_LEVELS_MICRO, F8_LEVELS_MICRO[1:])})
    if gaps != [S_P1_MICRO, S_P1_MICRO + 1] or S_P1_MICRO != _round_half_even(Fraction(F8_M_MAX_MICRO - F8_M_MIN_MICRO, F8_PASS1_LEVELS - 1)):
        raise F8ConfigError("pass-1 spacing differs from round6(2.25/23) or the realized gaps are not {s, s+1}")
    if W_RES_MICRO != F8_W_RES_SPACINGS * S_P1_MICRO:
        raise F8ConfigError("W_res differs from 3 pass-1 spacings")
    if generate_seed_panel(F8_SEED_PANEL_MASTER) != F8_SEED_PANEL or len(set(F8_SEED_PANEL)) != 20:
        raise F8ConfigError("frozen seed panel differs from its generating rule or is not 20 distinct seeds")
    if generate_seed_panel(F8_CALIBRATION_MASTER) != F8_CALIBRATION_SEED_PANEL or len(set(F8_CALIBRATION_SEED_PANEL)) != 20:
        raise F8ConfigError("frozen calibration panel differs from its generating rule or is not 20 distinct seeds")
    if F8_SEED_PANEL_MASTER == F8_CALIBRATION_MASTER or 20260917 in (F8_SEED_PANEL_MASTER, F8_CALIBRATION_MASTER) or set(F8_SEED_PANEL) & set(F8_CALIBRATION_SEED_PANEL):
        raise F8ConfigError("masters not distinct from each other or from E1's retired master, or the panels overlap")
    if frozen_digest(E1_RETIRED_SEED_PANEL) != E1_RETIRED_SEED_PANEL_SHA256 or len(set(E1_RETIRED_SEED_PANEL)) != 20:
        raise F8ConfigError("E1 retired-panel literal differs from E1's frozen panel digest")
    if set(E1_RETIRED_SEED_PANEL) & (set(F8_SEED_PANEL) | set(F8_CALIBRATION_SEED_PANEL)):
        raise F8ConfigError("an F8 panel shares a seed with E1's retired panel")
    d_levels, d_panel, d_cal = frozen_digest(F8_LEVELS_MICRO), frozen_digest(F8_SEED_PANEL), frozen_digest(F8_CALIBRATION_SEED_PANEL)
    if d_levels != F8_LEVELS_SHA256_LITERAL or d_panel != F8_SEED_PANEL_SHA256_LITERAL or d_cal != F8_CALIBRATION_PANEL_SHA256_LITERAL:
        raise F8ConfigError("frozen literal digest mismatch (levels or a seed panel)")
    if frozen_digest(F8_DECLARATION) != F8_DECLARATION_SHA256_LITERAL:
        raise F8ConfigError("F8 declaration differs from its frozen literal digest")
    decl = dict(F8_DECLARATION)
    live = {"grid": F8_GRID, "ticks": F8_TICKS, "tail_ticks": F8_TAIL_TICKS, "window": F8_WINDOW, "n_windows": F8_N_WINDOWS,
            "m_min_micro": F8_M_MIN_MICRO, "m_max_micro": F8_M_MAX_MICRO, "pass1_levels": F8_PASS1_LEVELS, "levels_micro": F8_LEVELS_MICRO,
            "s_p1_micro": S_P1_MICRO, "s_p1_max_micro": S_P1_MAX_MICRO, "w_res_micro": W_RES_MICRO, "mu": F8_MU, "g": F8_G, "eta0": F8_ETA0,
            "dt": F8_DT, "rho0_low_micro": F8_RHO0_LOW_MICRO, "seed_panel": F8_SEED_PANEL, "calibration_seed_panel": F8_CALIBRATION_SEED_PANEL,
            "seed_panel_master": F8_SEED_PANEL_MASTER, "calibration_master": F8_CALIBRATION_MASTER, "version": F8_VERSION}
    for key, val in live.items():
        if decl[key] != val or type(decl[key]) is not type(val):
            raise F8ConfigError(f"F8 declaration field {key} differs from the live execution global")
    # HARD CONTRACT VALUES, stated independently of both the declaration and the globals (contract §8; freeze record §3)
    if (F8_M_MIN_MICRO, F8_M_MAX_MICRO, F8_PASS1_LEVELS, len(F8_SEED_PANEL), F8_GRID, F8_TICKS, F8_TAIL_TICKS, F8_WINDOW * F8_N_WINDOWS) != \
            (250000, 2500000, 24, 20, 50, 3000, 1000, 1000):
        raise F8ConfigError("live sweep/shape globals differ from the hard contract values")
    if F8_MU != 0.2 or F8_G != 1.0 or F8_ETA0 != -math.log(0.99) or F8_RHO0_LOW_MICRO != 20000 or W_RES_MICRO != 293478 or S_P1_MICRO != 97826:
        raise F8ConfigError("rule parameters differ from the ratified values (freeze record §3 items 3, 4, 16, 18; eta0 RULED)")
    if (decl["f_dispatch"], decl["bases"], decl["q"], decl["drive"], decl["noise"], decl["timing"], decl["neighbourhood"]) != \
            ("F_2_symmetric", "homogeneous", "off", 0.0, 0.0, "synchronous_two_phase", "moore_8_periodic"):
        raise F8ConfigError("F8 declaration configuration values are not the contracted values")
    if decl["contract_sha256"] != F8_CONTRACT_SHA256 or decl["appendix_a_sha256"] != F8_APPENDIX_A_SHA256:
        raise F8ConfigError("declaration does not name the frozen contract and Appendix A identities")
    for m in F8_LEVELS_MICRO:                       # every level's lambda_bar reachable by homogeneous bases in [0, 1]
        homogeneous_base_from_lambda(lambda_bar_from_level(m))
    return {"levels_sha256": d_levels, "seed_panel_sha256": d_panel, "calibration_panel_sha256": d_cal,
            "declaration_sha256": F8_DECLARATION_SHA256_LITERAL, "s_p1_max_micro": str(S_P1_MAX_MICRO)}


def verify_against_appendix_a(appendix_a_path: str) -> Dict[str, object]:
    """Bind M1 to the object of record: the committed APPENDIX_A_OF_RECORD.md must carry the declared identity and
    its JSON block must state exactly this module's levels, spacing, W_res, mu, g and eta0. Used by the preflight
    when the repository is present and by M7 when it binds the stage."""
    raw = open(appendix_a_path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != F8_APPENDIX_A_SHA256:
        raise F8ConfigError(f"APPENDIX_A_OF_RECORD.md identity {sha[:16]} is not the frozen {F8_APPENDIX_A_SHA256[:16]}")
    mt = re.search(r"```json\n(.*?)```", raw.decode("utf-8"), re.S)
    if not mt: raise F8ConfigError("Appendix A JSON block not found")
    j = json.loads(mt.group(1))
    if tuple(int(x) for x in j["levels_micro"]) != F8_LEVELS_MICRO: raise F8ConfigError("Appendix A levels differ from the frozen literal")
    if int(j["s_micro"]) != S_P1_MICRO or int(j["W_res_micro"]) != W_RES_MICRO: raise F8ConfigError("Appendix A s / W_res differ from M1")
    inp = j["inputs"]
    expected = {"L": F8_GRID, "N": F8_GRID * F8_GRID, "mu": F8_MU, "eta0": F8_ETA0, "Dt": float(F8_DT), "n1": F8_PASS1_LEVELS,
                "T": F8_TICKS, "tail": F8_TAIL_TICKS, "window": F8_WINDOW, "W_res_spacings": F8_W_RES_SPACINGS,
                "sweep": [float(Fraction(F8_M_MIN_MICRO, MICRO_UNITS)), float(Fraction(F8_M_MAX_MICRO, MICRO_UNITS))]}
    for k, v in expected.items():
        if k not in inp or inp[k] != v:
            raise F8ConfigError(f"Appendix A input {k} = {inp.get(k)!r} differs from M1's {v!r}")
    # Appendix A carries no g: m absorbs it (contract §2.8); g = 1 is ratified by name (freeze record §3 item 4), not by Appendix A
    return {"appendix_a_sha256": sha, "levels_match": True, "delta_m": j["delta_m"]["value"]}


# ----------------------------------------------------------------------------- run specification
@dataclass(frozen=True)
class F8RunSpec:
    """The immutable specification of one run. Grid/ticks are parameters ONLY so controls and smoke tests can run at
    reduced size; a production-shape run must use a panel seed (canonical or calibration) and a pass-1 level. A spec is
    trusted only after `validate_run_spec` has reconstructed it from its identity fields (L2 M1 r1 D2)."""
    level_micro: int
    level_id: str
    seed: int
    obj: str
    panel: str
    eta_floor: float
    g: float
    mu: float
    lambda_bar: float
    base_homogeneous: float
    grid: int
    ticks: int
    tail_ticks: int
    window: int
    stream_key: Tuple[int, int, int]
    declaration_sha256: str

    @property
    def n_cells(self) -> int: return self.grid * self.grid

    def canonical_json(self) -> str:
        from dataclasses import asdict
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), allow_nan=False)

    def spec_hash(self) -> str:
        return hashlib.sha256(self.canonical_json().encode()).hexdigest()


def _exact_int(x, name: str) -> int:
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)):
        raise F8ConfigError(f"{name} must be an exact non-Boolean integer, got {type(x).__name__}")
    return int(x)


def f8_run_spec(level_micro: int, seed: int, obj: str, *, grid: int = F8_GRID, ticks: int = F8_TICKS, panel: str = "canonical") -> F8RunSpec:
    """Build the run specification for one (level, seed, object). The frozen declaration is verified on every call."""
    verify_frozen_identity()
    level_micro = _exact_int(level_micro, "level"); seed = _exact_int(seed, "seed")
    grid = _exact_int(grid, "grid"); ticks = _exact_int(ticks, "ticks")
    if not isinstance(panel, str) or not isinstance(obj, str): raise F8ConfigError("panel and object must be strings")
    if obj not in OBJECT_CODES: raise F8ConfigError(f"unknown object {obj!r}; legal: {sorted(OBJECT_CODES)}")
    if level_micro <= 0: raise F8ConfigError("level must be a positive micro-unit value")
    # shape policy (L2 M1 r1 D3): fail closed before any record can be undefined
    if grid < 3: raise F8ConfigError("grid must be >= 3 (periodic Moore neighbours distinct)")
    if grid > F8_GRID or ticks > F8_TICKS: raise F8ConfigError("grid/ticks above the production shape are not defined")
    if ticks < F8_WINDOW: raise F8ConfigError("ticks must be >= one tail window")
    tail = min(F8_TAIL_TICKS, ticks)
    if tail % F8_WINDOW != 0: raise F8ConfigError("tail length must be a whole number of windows")
    production_shape = (grid, ticks) == (F8_GRID, F8_TICKS)
    if production_shape and level_micro not in F8_LEVELS_MICRO:
        raise F8ConfigError(f"a production-shape run must use a frozen pass-1 level; {level_micro} is not one (L2 M1 r1 D1)")
    allowed = F8_SEED_PANEL if panel == "canonical" else F8_CALIBRATION_SEED_PANEL if panel == "calibration" else None
    if allowed is None: raise F8ConfigError("panel must be 'canonical' or 'calibration'")
    if production_shape and seed not in allowed:
        raise F8ConfigError(f"a production-shape run must use a seed from the frozen {panel} panel")
    if production_shape and panel == "calibration" and obj not in ("realization", "skeleton_high"):
        raise F8ConfigError("the calibration census runs only the realization and skeleton-high objects (contract §7.3 job 0)")
    lam = lambda_bar_from_level(level_micro)
    g = 0.0 if obj == "null" else F8_G
    eta = 0.0 if obj.startswith("skeleton") else F8_ETA0
    return F8RunSpec(level_micro, level_id(level_micro), seed, obj, panel, eta, g, F8_MU, lam, homogeneous_base_from_lambda(lam),
                     grid, ticks, tail, F8_WINDOW, stream_key(seed, obj, level_micro), F8_DECLARATION_SHA256_LITERAL)


def validate_run_spec(spec) -> F8RunSpec:
    """Reconstruct the authorized spec from the supplied spec's identity fields (level, seed, object, panel, grid, ticks)
    and require every field equal in value AND exact type (L2 M1 r1 D2). A spec altered with dataclasses.replace, or
    built by hand, cannot execute a different mechanism under the frozen declaration."""
    if type(spec) is not F8RunSpec: raise F8ConfigError("run spec is not an F8RunSpec")
    ref = f8_run_spec(spec.level_micro, spec.seed, spec.obj, grid=spec.grid, ticks=spec.ticks, panel=spec.panel)
    from dataclasses import fields
    for f in fields(F8RunSpec):
        a, b = getattr(spec, f.name), getattr(ref, f.name)
        if type(a) is not type(b) or a != b:
            raise F8ConfigError(f"run spec field {f.name} = {a!r} differs from the reconstructed authorized value {b!r}")
    return ref
