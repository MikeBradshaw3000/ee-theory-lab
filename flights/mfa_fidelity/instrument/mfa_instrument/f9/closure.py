"""mfa_instrument/f9/closure.py — Flight 9 module M5, part 1: the comparators of Contract F9 v0.7 §4 (N5, §5.3).

FIDELITY ONLY. Nothing here is scored, nothing here enters B or D, and no value computed here retunes a
scored tolerance (§4, §4.3). A poor comparison is published as such (§1.2′).

SITE CLOSURE (§4.2; freeze record item 15). The map, per cell i, in the contract's written form:

    p_i′ = (1 − p_i)·[1 − exp(−Δt·(η_floor + g·λ_i·Σ_j A_ij·p_j/8))] + (1 − q)·p_i

with A the periodic Moore adjacency, q = 1 − exp(−μ·Δt), and the same λ, g, η_floor, μ and Δt the lattice
rule uses (the activation term is `dynamics.activation_probability` on `dynamics.local_density`, the
placed functions, applied to probabilities instead of states). It is iterated from p = 1 at every cell
(skeleton, η_floor = 0) or p = π₁ at every cell (realization, η_floor = η₀) until the largest absolute
change of one application is at most 1e-12, for at most 200,000 applications.
  STOP RULE AS BUILT. After the k-th application, r_k = max_i |p_i′ − p_i|. If r_k ≤ 1e-12 the closure has
  converged at k and the map of record is p′ (the later iterate). If k reaches 200,000 with r_k > 1e-12 the
  comparator is `comparator unavailable` for that arm, object and level: the record carries the count and
  the last change and NO map, so nothing downstream can use an iterate that is not a fixed point. This
  affects no endpoint (§4.2, §7).
  WHAT "CONVERGED" MEANS. A change of at most 1e-12 in one application. It is not a bound on the distance
  to the fixed point: near the crossing the map contracts slowly and the distance can be many times the
  change. In the skeleton below the crossing the fixed point is p = 0 and the converged map is a small
  positive array, not zero.
  ACROSS MACHINES. exp comes from the platform's library and can differ in the last place, so the number
  of applications and the map's last digits can differ between machines. The map's SHA-256 in a record
  identifies that computation on that machine; it is not claimed equal elsewhere. The canonical machine's
  records are the records.

SPECTRAL CROSSING (§4.1). κ = g/g_spec, so the crossing at κ = 1 is true by construction (§2.8); g_spec is
M1's (`spectral.g_spec`), carried by the arm context. The linearization of the zero-floor map at p = 0 is
(1 − q)·I + g·Δt·diag(λ)·A/8, whose spectral radius is 1 at κ = 1 (to the accuracy of M1's spectral
routine): that is the sense in which κ = 1 is the zero-floor site-closure comparator. Its lattice counterpart is the skeleton's finite-horizon
persistence threshold κ̂_c (§5.4, M4's `persistence_record`). The realization has activity at g = 0 and
no absorbing-state onset; nothing here locates one.

THRESHOLD AGAINST THE CROSSING AND AGAINST T0 (§1.2′ (i), §4.3). For an arm's skeleton sweep:
  normalized shift  κ̂_c − 1, in integer micro-units of κ;
  raw-g shift       g(κ̂_c) − g_spec = (κ̂_c − 1)·g_spec, a float, with g(κ̂_c) and g_spec beside it (§2.8);
  against T0        κ̂_c − κ̂_c,T0 in micro-units, where κ̂_c,T0 is T0's own threshold from its own
                    skeleton-high sweep on the same grid (§4.3), with both raw gains beside it.
κ̂_c and its bracket are §5.4's and are computed here from the survivor counts by M4's
`persistence_record`; no persistence record is accepted on its own word. The uncertainty of κ̂_c is its
§5.4 bracket (§5.7), so the lower bracket level's shift is recorded beside each shift where a bracket
exists. If the arm has no κ̂_c the shifts are unavailable with §5.4's cause. If κ̂_c,T0 is unavailable
(T0's profile has no κ̂_c, or T0's survivor counts are not supplied) every T0-referenced item is recorded
`reference unavailable` (§5.8, §7). A non-monotone profile has no κ̂_c: its descriptive suffix statistic
is carried in the persistence record and is never used as a threshold here. Flight 8's 1.521739 is not
used. m_i = 1 is a local homogeneous benchmark (`spectral.local_m`), not the closure's edge.

NOT IN THIS MODULE: the comparison of occupancy maps and edges with the closure's map (§1.2′ (iii)), the
local m_i on the observed edge (§1.2′ (ii)) and the resampling ranges of §5.7. They need the evaluator's
maps and belong to the reports.
"""
from __future__ import annotations

import hashlib
import math
from typing import Dict, Optional

import numpy as np

from ..config import MICRO_UNITS
from . import config as C
from . import dynamics as D
from . import outcomes as O
from . import spectral as S
from . import terrain as T
from .config import F9ConfigError

SOLVER_TOL = 1e-12                                # §4.2; freeze record item 15
SOLVER_MAX_ITER = 200_000                         # §4.2; freeze record item 15
CLOSURE_OBJECTS = ("skeleton", "realization")
START_RULE = (("skeleton", "p = 1 at every cell"), ("realization", "p = pi_1 = a/(a + q) at every cell"))
CAUSE_UNAVAILABLE = "comparator unavailable"      # §4.2, §7
CAUSE_REFERENCE = "reference unavailable"         # §5.8, §7

CLOSURE_DECLARATION = (
    ("module", "f9.closure"), ("version", C.F9_VERSION), ("contract", C.F9_CONTRACT_SHA256),
    ("map", "p' = (1 - p)*(1 - exp(-dt*(eta_floor + g*lam*moore_sum(p)/8))) + (1 - q)*p"),
    ("solver_tol", repr(SOLVER_TOL)), ("solver_max_iter", SOLVER_MAX_ITER), ("norm", "max absolute change of one application"),
    ("stop", "converged at the first k with change <= tol, map of record the later iterate; unavailable if change > tol at k = max_iter"),
    ("objects", CLOSURE_OBJECTS), ("start", START_RULE), ("cause_unavailable", CAUSE_UNAVAILABLE), ("cause_reference", CAUSE_REFERENCE),
    ("threshold", "kappa_c and bracket by outcomes.persistence_record from survivor counts"),
    ("shifts", "normalized: kappa_c - 1 (micro); raw: (kappa_c - 1)*g_spec; against T0: kappa_c - kappa_c_T0 (micro)"),
    ("reference", "T0's kappa_c from its own skeleton-high sweep; unavailable when T0 has no kappa_c or no counts"),
    ("kind", "fidelity; never scored"),
)
CLOSURE_DECLARATION_SHA256_LITERAL = "d4196f0ecee6a55204ec8f42f7a9465c453498e4b2f85a80fe64ed963d6fcf9e"


class F9ClosureError(F9ConfigError):
    """An input outside the closure's domain, or a declaration that differs from its frozen digest."""


def verify_closure_declaration() -> str:
    C.verify_frozen_identity()
    digest = C.frozen_digest(CLOSURE_DECLARATION)
    if digest != CLOSURE_DECLARATION_SHA256_LITERAL:
        raise F9ClosureError("the closure declaration differs from its frozen digest")
    d = dict(CLOSURE_DECLARATION)
    if (d["solver_tol"], d["solver_max_iter"], d["objects"], d["start"]) != (repr(SOLVER_TOL), SOLVER_MAX_ITER, CLOSURE_OBJECTS, START_RULE) \
            or (SOLVER_TOL, SOLVER_MAX_ITER) != (1e-12, 200_000):
        raise F9ClosureError("the solver's constants differ from the registered values (freeze record item 15)")
    return digest


# ======================= the map =======================
def closure_step(p: np.ndarray, *, eta_floor: float, g: float, lam: np.ndarray) -> np.ndarray:
    """One application of the §4.2 map."""
    return (1.0 - p) * D.activation_probability(eta_floor, g, lam, D.local_density(p)) + (1.0 - C.q_deact()) * p


def _check_field(lam, g, eta_floor, p0) -> np.ndarray:
    lam = np.asarray(lam)
    if lam.dtype != np.float64 or lam.ndim != 2 or min(lam.shape) < 3 or not np.all(np.isfinite(lam)) or float(lam.min()) < 0.0:
        raise F9ClosureError("the index is a finite, non-negative float64 array on a lattice of at least 3 by 3")
    for name, z in (("g", g), ("eta_floor", eta_floor), ("p0", p0)):
        if type(z) is not float or not math.isfinite(z) or z < 0.0: raise F9ClosureError(f"{name} is a finite, non-negative float")
    if p0 > 1.0: raise F9ClosureError("p0 is a probability")
    return lam


def iterate(lam: np.ndarray, g: float, eta_floor: float, p0: float) -> Dict[str, object]:
    """Iterate the map from the constant start p0 by the stop rule of the module docstring. Returns
    {"converged", "iterations", "last_change", "map"}; "map" is None when the rule did not converge."""
    lam = _check_field(lam, g, eta_floor, p0)
    p = np.full(lam.shape, p0, dtype=np.float64)
    change = math.inf
    for k in range(1, SOLVER_MAX_ITER + 1):
        nxt = closure_step(p, eta_floor=eta_floor, g=g, lam=lam)
        change = float(np.max(np.abs(nxt - p)))
        if not math.isfinite(change): raise F9ClosureError("the closure map left the finite numbers")
        p = nxt
        if change <= SOLVER_TOL:
            return {"converged": True, "iterations": k, "last_change": change, "map": p}
    return {"converged": False, "iterations": SOLVER_MAX_ITER, "last_change": change, "map": None}


def start_value(obj: str) -> float:
    if obj == "skeleton": return 1.0
    if obj == "realization": return D.stationary_pi1(C.F9_ETA0)
    raise F9ClosureError(f"not a closure object: {obj!r}")


def site_closure(arm: D.ArmContext, level_micro: int, obj: str) -> Dict[str, object]:
    """The §4.2 comparator for one arm, object and registered level. Returns {"record", "map"}: the record is plain
    data; the map is the float64 array of record, or None with `comparator unavailable`."""
    verify_closure_declaration()
    if not isinstance(arm, D.ArmContext) or (arm.terrain, arm.composition) not in C.F9_ARMS: raise F9ClosureError("not an arm context")
    if obj not in CLOSURE_OBJECTS: raise F9ClosureError(f"not a closure object: {obj!r}")
    g = S.gain(level_micro, arm.g_spec)                                   # refuses an undeclared level
    eta = C.F9_ETA0 if obj == "realization" else 0.0
    res = iterate(arm.lam, g, eta, start_value(obj))
    p = res["map"]
    rec: Dict[str, object] = {
        "record": "F9SiteClosure", "kind": "fidelity; never scored", "terrain": arm.terrain, "composition": arm.composition, "object": obj,
        "level_micro": level_micro, "g": g, "g_spec": arm.g_spec, "eta_floor": eta, "start": start_value(obj),
        "index_sha256": arm.index_sha256, "identity_record_sha256": arm.identity_record_sha256,
        "solver": {"tol": SOLVER_TOL, "max_iter": SOLVER_MAX_ITER}, "iterations": res["iterations"], "last_change": res["last_change"],
        "available": bool(res["converged"]), "cause": None if res["converged"] else CAUSE_UNAVAILABLE,
        "declaration_sha256": CLOSURE_DECLARATION_SHA256_LITERAL,
    }
    if p is None:
        rec.update(map_sha256=None, map_min=None, map_max=None, map_mean=None)
    else:
        rec.update(map_sha256=hashlib.sha256(T.serialize(p)).hexdigest(), map_min=float(p.min()), map_max=float(p.max()), map_mean=float(p.mean()))
    return {"record": rec, "map": p}


# ======================= the threshold against the crossing and against T0 =======================
def _g_spec(x, what: str) -> float:
    if type(x) is not float or not math.isfinite(x) or not x > 0.0: raise F9ClosureError(f"{what} is a finite, positive float")
    return x


def threshold_fidelity(terrain: str, composition: str, survivors: Dict[int, Optional[int]], g_spec: float,
                       t0_survivors: Optional[Dict[int, Optional[int]]] = None, t0_g_spec: Optional[float] = None) -> Dict[str, object]:
    """§1.2′ (i) for one arm: the skeleton threshold against κ = 1 and against T0's own threshold (see module docstring).
    `survivors[κ micro]` and `t0_survivors[κ micro]` are survivor counts of 40 from skeleton-high sweeps; both persistence
    records are computed here. For T0's own arm, pass T0's counts and gain in both roles (as `survivors`, `g_spec` and as
    `t0_survivors`, `t0_g_spec`); the comparison with itself is then zero by construction and is recorded as such. Without
    the reference arguments the T0 comparison is `reference unavailable`."""
    verify_closure_declaration()
    if (terrain, composition) not in C.F9_ARMS: raise F9ClosureError(f"not a declared arm: {terrain!r}.{composition!r}")
    g_spec = _g_spec(g_spec, "g_spec")
    own = O.persistence_record(survivors)
    one = MICRO_UNITS

    def shift_block(rec, gs):
        k = rec["kappa_c_micro"]
        if k is None:
            return {"available": False, "cause": rec.get("kappa_c_cause") or rec["cause"], "profile": rec["profile"]}
        low = rec["bracket_micro"][0] if rec["bracket_micro"] is not None else None
        return {"available": True, "cause": None, "profile": rec["profile"], "kappa_c_micro": k, "bracket_lower_micro": low,
                "bracketed": low is not None, "normalized_shift_micro": k - one, "bracket_lower_normalized_shift_micro": None if low is None else low - one,
                "g_spec": gs, "g_at_kappa_c": S.gain(k, gs), "raw_g_shift": S.gain(k, gs) - gs,
                "bracket_lower_raw_g_shift": None if low is None else S.gain(low, gs) - gs}

    out: Dict[str, object] = {"record": "F9ThresholdFidelity", "kind": "fidelity; never scored", "terrain": terrain, "composition": composition,
                              "crossing_micro": one, "persistence": own, "against_crossing": shift_block(own, g_spec),
                              "declaration_sha256": CLOSURE_DECLARATION_SHA256_LITERAL}
    if t0_survivors is None or t0_g_spec is None:
        if not (t0_survivors is None and t0_g_spec is None): raise F9ClosureError("T0's counts and T0's g_spec are supplied together or not at all")
        out.update(t0_persistence=None, against_t0={"available": False, "cause": CAUSE_REFERENCE, "reference_cause": "T0's skeleton-high counts were not supplied"})
        return out
    t0_g_spec = _g_spec(t0_g_spec, "T0's g_spec")
    ref = O.persistence_record(t0_survivors)
    out["t0_persistence"] = ref
    if ref["kappa_c_micro"] is None:
        out["against_t0"] = {"available": False, "cause": CAUSE_REFERENCE, "reference_cause": ref.get("kappa_c_cause") or ref["cause"], "reference_profile": ref["profile"]}
    elif own["kappa_c_micro"] is None:
        out["against_t0"] = {"available": False, "cause": own.get("kappa_c_cause") or own["cause"], "reference_kappa_c_micro": ref["kappa_c_micro"],
                             "reference_profile": ref["profile"]}
    else:
        out["against_t0"] = {"available": True, "cause": None, "kappa_c_micro": own["kappa_c_micro"], "reference_kappa_c_micro": ref["kappa_c_micro"],
                             "difference_micro": own["kappa_c_micro"] - ref["kappa_c_micro"], "profile": own["profile"], "reference_profile": ref["profile"],
                             "bracketed": own["bracket_micro"] is not None, "reference_bracketed": ref["bracket_micro"] is not None,
                             "g_at_kappa_c": S.gain(own["kappa_c_micro"], g_spec), "reference_g_at_kappa_c": S.gain(ref["kappa_c_micro"], t0_g_spec)}
    return out
