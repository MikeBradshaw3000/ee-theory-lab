"""mfa_instrument/e1/projection.py — E1 stage-1 module M5, ROUND 2: the projection object and R1a (Contract E1 v0.3 §6;
v0.4 §6; v0.5 C; v0.6 A–D; v0.7 A–B; v0.8 A–C; L2 M5 first-pass review, blockers M5-1..M5-7).

THE CLOSURE (R1a). The frozen rule drives each cell by drive_i = α·Λ_i + β·d_i − δ·d_i² − γ_offset, p_base = σ(drive),
p_act = p_base + η_floor·(1 − p_base), Λ_i = v·u_base·r, d_i the Moore-neighbourhood density. The independence /
mean-neighbourhood closure replaces d_i by the global density ρ and averages over Λ ~ D_m (triple product of three
independent uniforms on (m − w/2, m + w/2)):
    ρ_{t+1} = G_m(ρ_t) = E_{Λ~D_m}[ η_floor + (1 − η_floor)·σ(αΛ + βρ_t − δρ_t² − γ_offset) ],
evaluated by a FROZEN 16-node Gauss–Legendre product rule (converged; validated three ways), iterated directly.

OUTCOME HYGIENE (L2 M5 ruling §3): this instrument carries NO reference result. The T2-S table and every branch
consequence are frozen here BEFORE the result; the result — the reference structure of record — is created only by
the canonical 701-point job and lives in a separate result record, never in the declaration that measures it. What the
sampled closure has shown so far (every sampled level S, bottom point S with positive margin, projection-side sweep 0
returning the matching adverse category) is a PROVISIONAL SAMPLED CLOSURE FINDING / EXPECTED REFERENCE BRANCH, stated
in the packet, not in the source.

CANONICAL VERSUS ANALYSIS (L2 M5-1): every result type carries a ROLE and identities. Only `dense_reference()` on the
exact frozen 701-point grid with zero precision halts issues `reference_of_record`; only the exact declared tolerance
program issues `canonical` tolerances; only the exact declared 200-sweep ensemble with zero halts can complete a design-
stability gate; T2-L requires a COMPLETE design-stability object; only the exact dense grid can issue a canonical stability
verdict. Analysis-subset objects keep their own role and can never issue a freeze-facing status.

HALTS FAIL CLOSED (L2 M5-2): in design stability and T2-L, halts are never removed before estimating design success —
the policy frozen here is: exact attempted count required, every halt recorded, ANY halt → the gate is NOT EVALUABLE
(incomplete), and the matching rate is reported over the ATTEMPTED denominator. Apparatus failures (production-cache
defects) RAISE and halt the stage; only predeclared evaluability events (uncertified conditional thresholds) enter the
accounting, categorized.

[PROPOSED] values remain Mike-level and are ratified only at freeze.
"""
from __future__ import annotations

import hashlib
import math
import types
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..config import DynamicsConstants, MICRO_UNITS
from . import audit as _A
from . import classify as _K
from . import config as _C
from . import null as _N
from . import verdict as _V
from .classify import N_CELLS, RUN_LEN, TAIL_START, TAIL_END, TAIL_LEN, WINDOW, N_WINDOWS, TERMINAL_WINDOWS, level_counts, level_label, run_status
from .config import E1_BASE_WIDTH_MICRO, E1_LEVELS_MICRO, E1_SEED_PANEL, S_P1_MAX_MICRO, DELTA_M_R_MICRO, level_id
from .verdict import evaluate, route

PROJECTION_VERSION = "e1_stage1_m5_v4 / R1a discrete closure; all records derived; content-bound caches"


class ProjectionDomainError(ValueError):
    """Frozen identity violated, input outside the projection's domain, or an apparatus defect."""


class ProjectionApparatusError(RuntimeError):
    """A production-cache or environment defect during a projection job: halts the STAGE, never a replicate."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def _frozen_mapping(decl, name):
    keys = [k for k, _ in decl]
    if len(set(keys)) != len(keys): raise ProjectionDomainError(f"{name}: duplicate declaration field names")
    return dict(decl)


def _exact_int(x, name, lo=None):
    if isinstance(x, bool) or not isinstance(x, int): raise ProjectionDomainError(f"{name} must be an exact non-Boolean integer")
    if lo is not None and x < lo: raise ProjectionDomainError(f"{name} must be >= {lo}")
    return x


def _level(x, name="level") -> int:
    m = _exact_int(x, name)
    if m - E1_BASE_WIDTH_MICRO // 2 < 0 or m + E1_BASE_WIDTH_MICRO // 2 > MICRO_UNITS: raise ProjectionDomainError(f"{name} {m} inadmissible")
    return m


# ----------------------------------------------------------------------------- frozen declaration
GL_NODES = 16
RHO_0 = 0.5
HORIZON = RUN_LEN
DENSE_START_MICRO, DENSE_END_MICRO, DENSE_STEP_MICRO = 150_000, 850_000, 1_000
DENSE_POINTS = (DENSE_END_MICRO - DENSE_START_MICRO) // DENSE_STEP_MICRO + 1     # 701
OFF_BAND_U_TOTAL = 7                                 # [PROPOSED]
OFF_BAND_U_RUN = 3                                   # [PROPOSED]
DELTA_M_R = DELTA_M_R_MICRO                          # 3382: the reference-side departure-zone width (its ONE role)
DELTA_M_STAB = 3382                                  # [PROPOSED]
DELTA_M_EST = 3382                                   # [PROPOSED]
DELTA_M_LOC = S_P1_MAX_MICRO                         # [PROPOSED] = s_P1^max
ENVELOPE_QUANTILES = (2.5, 97.5)                     # [PROPOSED], linear
DESIGN_STABILITY_SWEEPS = 200                        # [PROPOSED] exact declared ensemble
T2L_FAILURE_CAP = 0.20                               # [PROPOSED]
TOLERANCE_REPLICATES = 1000                          # [PROPOSED] exact declared program
TOLERANCE_QUANTILE = 0.95                            # [PROPOSED]
TOLERANCE_QUANTILE_METHOD = "linear"
TOLERANCE_CI_RESAMPLES = 2000                        # bootstrap of the 0.95 quantile: reports its sampling uncertainty (never certifies coverage by itself)
T1_MIN_SETTLED = 8                                   # [PROPOSED]
T1_SEED_COUNT = len(E1_SEED_PANEL)                   # 20: the cross-seed range statistic is calibrated at this count
T3_DISTANCE = "mean absolute deviation over ticks 0..1999"          # [PROPOSED]
T2L_FAILURE_DISPOSITION = "NOT EVALUABLE (design-location resolution insufficient)"   # [PROPOSED] v0.7 B, Mike's choice
HALT_POLICY = "any halt in a canonical ensemble -> gate NOT EVALUABLE (incomplete); rates reported over the attempted denominator"
STABILITY_ALT_TEMPLATES = 3                          # [PROPOSED] v0.6 B axis 1: alternative base templates
STABILITY_ALT_SEED_SETS = 2                          # [PROPOSED] v0.6 B axis 2 — SEE NOTE: under M3's exact null law replicate draws no longer
                                                     # exist, so this axis is implemented as independent template-draw FAMILIES (each seed set
                                                     # draws its own 3 templates); the retained meaning is flagged for Mike's ruling
PROJECTION_MASTER = 202609301
TOLERANCE_MASTER = 202609302
STABILITY_MASTER = 202609303
BOOTSTRAP_MASTER = 202609304
BOOTSTRAP_RESAMPLES = 10_000

STRUCTURE_CLASSES = ("ORDER-VIOLATING/MULTIPLE", "NO-SUSTAINED-PHASE", "NO-NULL-PHASE", "REFERENCE-UNRESOLVED", "UNIQUE-THRESHOLD")
T2S_STATUSES = ("RECOVERED", "NOT RECOVERED", "NOT EVALUABLE")
T2S_TABLE: Tuple[Tuple[str, str, str, str, str], ...] = (
    ("*",                          "NOT_DISTINGUISHED", "*",                        "NOT EVALUABLE", "production instrument limit"),
    ("REFERENCE-UNRESOLVED",       "*",                 "*",                        "NOT EVALUABLE", "reference cannot speak; reference-structure finding"),
    ("UNIQUE-THRESHOLD",           "LOCATED",           "*",                        "RECOVERED",     "proceed to T2-L"),
    ("UNIQUE-THRESHOLD",           "NOT_PRODUCED",      "*",                        "NOT RECOVERED", "projection threshold not produced by the stream-level realization"),
    ("NO-SUSTAINED-PHASE",         "LOCATED",           "*",                        "NOT RECOVERED", "structural mismatch"),
    ("NO-NULL-PHASE",              "LOCATED",           "*",                        "NOT RECOVERED", "structural mismatch"),
    ("ORDER-VIOLATING/MULTIPLE",   "LOCATED",           "*",                        "NOT RECOVERED", "structural mismatch"),
    ("NO-SUSTAINED-PHASE",         "NOT_PRODUCED",      "no_sustained_phase",       "RECOVERED",     "adverse-structure agreement (P1 adverse in both systems; nothing supported)"),
    ("NO-NULL-PHASE",              "NOT_PRODUCED",      "no_null_consistent_phase", "RECOVERED",     "adverse-structure agreement (P1 adverse in both systems; nothing supported)"),
    ("ORDER-VIOLATING/MULTIPLE",   "NOT_PRODUCED",      "order_violation",          "RECOVERED",     "adverse-structure agreement (P1 adverse in both systems; nothing supported)"),
    ("NO-SUSTAINED-PHASE",         "NOT_PRODUCED",      "*",                        "NOT RECOVERED", "mismatched adverse structures"),
    ("NO-NULL-PHASE",              "NOT_PRODUCED",      "*",                        "NOT RECOVERED", "mismatched adverse structures"),
    ("ORDER-VIOLATING/MULTIPLE",   "NOT_PRODUCED",      "*",                        "NOT RECOVERED", "mismatched adverse structures"),
)
MATCHING_E1_CATEGORY: Tuple[Tuple[str, str, str], ...] = (
    ("UNIQUE-THRESHOLD", "LOCATED", "*"), ("NO-SUSTAINED-PHASE", "NOT_PRODUCED", "no_sustained_phase"),
    ("NO-NULL-PHASE", "NOT_PRODUCED", "no_null_consistent_phase"), ("ORDER-VIOLATING/MULTIPLE", "NOT_PRODUCED", "order_violation"),
)

PROJECTION_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", PROJECTION_VERSION), ("closure", "rho_{t+1} = E_{Lambda~D_m}[eta + (1-eta)*sigmoid(alpha*Lambda + beta*rho - delta*rho^2 - gamma_offset)]"),
    ("lambda_distribution", "triple product of three independent uniforms on (m - w/2, m + w/2)"), ("quadrature", "Gauss-Legendre product rule, fixed nodes"),
    ("gl_nodes", GL_NODES), ("iteration", "direct map iteration; no ODE; no RK4"), ("rho_0", RHO_0), ("horizon", HORIZON),
    ("constants", _C.E1_CONSTANTS_EXPECTED), ("base_width_micro", E1_BASE_WIDTH_MICRO),
    ("dense_grid_micro", (DENSE_START_MICRO, DENSE_END_MICRO, DENSE_STEP_MICRO)), ("dense_points", DENSE_POINTS),
    ("reference_null", "M3 reference_thresholds (frozen common-rank template; conservative coverage mode where ambiguous)"),
    ("projected_tail_geometry", "projection transcription of M2's windows and precedence on the continuous orbit (not M2's production tail_stats)"),
    ("structure_classes", STRUCTURE_CLASSES), ("off_band_u_total", OFF_BAND_U_TOTAL), ("off_band_u_run", OFF_BAND_U_RUN),
    ("delta_m_r_micro", DELTA_M_R), ("delta_m_stab_micro", DELTA_M_STAB), ("delta_m_est_micro", DELTA_M_EST), ("delta_m_loc_micro", DELTA_M_LOC),
    ("envelope_quantiles", ENVELOPE_QUANTILES), ("design_stability_sweeps", DESIGN_STABILITY_SWEEPS), ("t2l_failure_cap", T2L_FAILURE_CAP),
    ("t2l_failure_disposition", T2L_FAILURE_DISPOSITION), ("halt_policy", HALT_POLICY),
    ("tolerance_replicates", TOLERANCE_REPLICATES), ("tolerance_quantile", TOLERANCE_QUANTILE), ("tolerance_quantile_method", TOLERANCE_QUANTILE_METHOD),
    ("tolerance_ci_resamples", TOLERANCE_CI_RESAMPLES), ("t1_min_settled", T1_MIN_SETTLED), ("t1_seed_count", T1_SEED_COUNT),
    ("t1_dispersion", "tau_disp = TOLERANCE_QUANTILE of the finite-N distribution of the exact cross-seed RANGE (max-min) over groups of T1_SEED_COUNT replicates"),
    ("t3_distance", T3_DISTANCE), ("stability_alt_templates", STABILITY_ALT_TEMPLATES), ("stability_alt_seed_sets", STABILITY_ALT_SEED_SETS),
    ("stability_axis_2", "independent template-draw families: template (k, j) ~ SeedSequence([STABILITY_MASTER, k, j]); retained meaning flagged for Mike"),
    ("masters", (PROJECTION_MASTER, TOLERANCE_MASTER, STABILITY_MASTER, BOOTSTRAP_MASTER)), ("bootstrap_resamples", BOOTSTRAP_RESAMPLES),
    ("t2s_table", T2S_TABLE), ("matching_e1_category", MATCHING_E1_CATEGORY),
    ("reference_result", "NONE IN THE INSTRUMENT: the reference of record is created only by the canonical 701-point job (separate result record)"),
)
PROJECTION_DECLARATION_SHA256_LITERAL = "e9a109a505433fa42fea08ac4ee1830dde9b418fb35f1740c7453a4ad0cf4fc0"   # established 2026-10-01 (round 4)

_GL_X, _GL_W = np.polynomial.legendre.leggauss(GL_NODES)
_GL_X.setflags(write=False); _GL_W.setflags(write=False)
GL_BASIS_SHA256_LITERAL = "cfbec389e51be570a7c11d417e51ddf7452b650090e96ceae2c5a91a93020864"      # independently established identity of the exact Gauss-Legendre basis bytes


def verify_frozen_identity() -> None:
    _C.verify_frozen_identity(); _K.verify_frozen_identity(); _N.verify_frozen_identity(); _V.verify_frozen_identity()
    if _digest(PROJECTION_DECLARATION) != PROJECTION_DECLARATION_SHA256_LITERAL:
        raise ProjectionDomainError("projection declaration differs from its frozen literal digest")
    d = _frozen_mapping(PROJECTION_DECLARATION, "PROJECTION_DECLARATION")
    live = {"version": PROJECTION_VERSION, "gl_nodes": GL_NODES, "rho_0": RHO_0, "horizon": HORIZON, "constants": _C.E1_CONSTANTS_EXPECTED,
            "base_width_micro": E1_BASE_WIDTH_MICRO, "dense_grid_micro": (DENSE_START_MICRO, DENSE_END_MICRO, DENSE_STEP_MICRO), "dense_points": DENSE_POINTS,
            "structure_classes": STRUCTURE_CLASSES, "off_band_u_total": OFF_BAND_U_TOTAL, "off_band_u_run": OFF_BAND_U_RUN,
            "delta_m_r_micro": DELTA_M_R, "delta_m_stab_micro": DELTA_M_STAB, "delta_m_est_micro": DELTA_M_EST, "delta_m_loc_micro": DELTA_M_LOC,
            "envelope_quantiles": ENVELOPE_QUANTILES, "design_stability_sweeps": DESIGN_STABILITY_SWEEPS, "t2l_failure_cap": T2L_FAILURE_CAP,
            "t2l_failure_disposition": T2L_FAILURE_DISPOSITION, "halt_policy": HALT_POLICY, "tolerance_replicates": TOLERANCE_REPLICATES,
            "tolerance_quantile": TOLERANCE_QUANTILE, "tolerance_quantile_method": TOLERANCE_QUANTILE_METHOD, "tolerance_ci_resamples": TOLERANCE_CI_RESAMPLES,
            "t1_min_settled": T1_MIN_SETTLED, "t1_seed_count": T1_SEED_COUNT, "t3_distance": T3_DISTANCE,
            "stability_alt_templates": STABILITY_ALT_TEMPLATES, "stability_alt_seed_sets": STABILITY_ALT_SEED_SETS,
            "masters": (PROJECTION_MASTER, TOLERANCE_MASTER, STABILITY_MASTER, BOOTSTRAP_MASTER), "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "t2s_table": T2S_TABLE, "matching_e1_category": MATCHING_E1_CATEGORY}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v): raise ProjectionDomainError(f"projection declaration field {k} differs from the live global")
    for k, v in d.items():
        if k == "reference_result" and ("NO-NULL" in str(v) or "UNIQUE" in str(v) or "NO-SUSTAINED" in str(v)):
            raise ProjectionDomainError("the instrument declaration must not carry a reference result")
    if (GL_NODES, DENSE_POINTS, DELTA_M_R, DELTA_M_LOC, HORIZON, RHO_0, TOLERANCE_REPLICATES, DESIGN_STABILITY_SWEEPS, T1_SEED_COUNT) != (16, 701, 3382, 30435, 3000, 0.5, 1000, 200, 20) \
            or DELTA_M_R != DELTA_M_R_MICRO or DELTA_M_LOC != S_P1_MAX_MICRO:
        raise ProjectionDomainError("projection hard values differ from the contract")
    if len({PROJECTION_MASTER, TOLERANCE_MASTER, STABILITY_MASTER, BOOTSTRAP_MASTER}) != 4: raise ProjectionDomainError("masters not independent")
    if not (0.0 < T2L_FAILURE_CAP < 1.0 and 0.0 < TOLERANCE_QUANTILE < 1.0 and 0.0 < ENVELOPE_QUANTILES[0] < ENVELOPE_QUANTILES[1] < 100.0): raise ProjectionDomainError("gate values out of range")
    k = DynamicsConstants()
    for name, val in _C.E1_CONSTANTS_EXPECTED:
        if getattr(k, name) != val: raise ProjectionDomainError(f"committed constant {name} differs from the E1 declaration")
    # quadrature preflight: the basis is read-only, equals a fresh regeneration byte-for-byte, and equals its established identity
    gx, gw = np.polynomial.legendre.leggauss(GL_NODES)
    if _GL_X.flags.writeable or _GL_W.flags.writeable or _GL_X.tobytes() != gx.tobytes() or _GL_W.tobytes() != gw.tobytes() \
            or hashlib.sha256(_GL_X.tobytes() + _GL_W.tobytes()).hexdigest() != GL_BASIS_SHA256_LITERAL:
        raise ProjectionDomainError("Gauss-Legendre basis differs from its established content identity or is writable")


def m3_reference_identity() -> str:
    return _digest(("m3", _N.NULL_DECLARATION_SHA256_LITERAL, _N.NULL_TEMPLATE_SHA256_LITERAL, _N.SCORING_OBJECT_VERSION))


# ----------------------------------------------------------------------------- the closure (content-bound caches)
def _cube_nodes(m_micro: int) -> Tuple[np.ndarray, np.ndarray]:
    w = E1_BASE_WIDTH_MICRO / MICRO_UNITS; m = m_micro / MICRO_UNITS; a, b = m - w / 2.0, m + w / 2.0
    xs = 0.5 * (b - a) * _GL_X + 0.5 * (a + b); ws = 0.5 * (b - a) * _GL_W
    V, U, R = np.meshgrid(xs, xs, xs, indexing="ij")
    lam = (V * U * R).reshape(-1); wt = np.einsum("i,j,k->ijk", ws, ws, ws).reshape(-1) / (b - a) ** 3
    if not (abs(float(wt.sum()) - 1.0) < 1e-12 and np.all(lam >= a ** 3 - 1e-15) and np.all(lam <= b ** 3 + 1e-15)): raise ProjectionDomainError("cube nodes/weights failed normalisation")
    lam.setflags(write=False); wt.setflags(write=False)
    return lam, wt


def _content(*arrs: np.ndarray) -> str:
    return hashlib.sha256(b"".join(a.tobytes() for a in arrs)).hexdigest()


_NODE_CACHE: Dict[int, Tuple[np.ndarray, np.ndarray, str]] = {}


def _nodes(m_micro: int) -> Tuple[np.ndarray, np.ndarray]:
    """Cached nodes whose CONTENT is verified on every retrieval against a fresh regeneration (a replaced read-only
    entry with the right sums is refused — L2 r2 §10)."""
    if m_micro not in _NODE_CACHE:
        lam, wt = _cube_nodes(m_micro); _NODE_CACHE[m_micro] = (lam, wt, _content(lam, wt))
    lam, wt, sha = _NODE_CACHE[m_micro]
    f_lam, f_wt = _cube_nodes(m_micro)
    if lam.flags.writeable or wt.flags.writeable or _content(lam, wt) != sha or sha != _content(f_lam, f_wt):
        raise ProjectionDomainError("cached quadrature nodes differ from their regenerated content")
    return lam, wt


def _g(rho: np.ndarray, m: int) -> np.ndarray:
    lam, wt = _nodes(m); k = DynamicsConstants()
    drive = k.alpha * lam[None, :] + (k.beta * rho - k.delta * rho * rho - k.gamma_offset)[:, None]
    pb = 1.0 / (1.0 + np.exp(-drive)); p = np.clip(pb + k.eta_floor * (1.0 - pb), 0.0, 1.0)
    return p @ wt


def g_map(rho, m_micro: int) -> np.ndarray:
    verify_frozen_identity(); m = _level(m_micro)
    r = np.atleast_1d(np.asarray(rho, dtype=np.float64))
    if not np.isfinite(r).all() or (r < 0.0).any() or (r > 1.0).any(): raise ProjectionDomainError("rho must be finite in [0, 1]")
    out = _g(r, m)
    return out if np.ndim(rho) else out[0]


def closure_validation(m_micro: int, mc_samples: int = 2_000_000, seed: int = 1) -> Dict[str, float]:
    verify_frozen_identity(); m = _level(m_micro); k = DynamicsConstants(); w = E1_BASE_WIDTH_MICRO / MICRO_UNITS; mm = m / MICRO_UNITS
    g = np.random.default_rng(seed); b = g.uniform(mm - w / 2, mm + w / 2, size=(mc_samples, 3)); lam = b[:, 0] * b[:, 1] * b[:, 2]
    def gl(n, rho):
        x, wt = np.polynomial.legendre.leggauss(n); a, bb = mm - w / 2, mm + w / 2
        xs = 0.5 * (bb - a) * x + 0.5 * (a + bb); ws = 0.5 * (bb - a) * wt
        V, U, R = np.meshgrid(xs, xs, xs, indexing="ij"); W = np.einsum("i,j,k->ijk", ws, ws, ws)
        pb = 1 / (1 + np.exp(-(k.alpha * V * U * R + k.beta * rho - k.delta * rho ** 2 - k.gamma_offset)))
        return float(np.sum(W * (pb + k.eta_floor * (1 - pb))) / (bb - a) ** 3)
    out = {}
    for rho in (0.0, 0.5):
        pb = 1 / (1 + np.exp(-(k.alpha * lam + k.beta * rho - k.delta * rho ** 2 - k.gamma_offset))); mc = float(np.mean(pb + k.eta_floor * (1 - pb)))
        q = float(_g(np.array([rho]), m)[0])
        out[f"gl16_rho{rho}"] = q; out[f"mc_rho{rho}"] = mc; out[f"abs_gl16_minus_mc_rho{rho}"] = abs(q - mc)
        out[f"abs_gl16_minus_gl8_rho{rho}"] = abs(q - gl(8, rho)); out[f"abs_gl16_minus_gl32_rho{rho}"] = abs(q - gl(32, rho))
    out["template_mean_p_act_rho0"] = float(np.mean(_N.null_p_act(m))); out["abs_template_minus_gl16_rho0"] = abs(out["template_mean_p_act_rho0"] - out["gl16_rho0.0"])
    return out


_ORBIT_CACHE: Dict[int, Tuple[np.ndarray, str]] = {}


def _compute_orbit(m: int) -> np.ndarray:
    r = np.empty(HORIZON); r[0] = RHO_0
    for t in range(1, HORIZON): r[t] = float(_g(np.array([r[t - 1]]), m)[0])
    r.setflags(write=False); return r


def orbit(m_micro: int) -> np.ndarray:
    """The deterministic orbit; cached CONTENT verified against a fresh recomputation on every retrieval."""
    verify_frozen_identity(); m = _level(m_micro)
    if m not in _ORBIT_CACHE:
        o = _compute_orbit(m); _ORBIT_CACHE[m] = (o, _content(o))
    o, sha = _ORBIT_CACHE[m]
    if o.flags.writeable or _content(o) != sha or sha != _content(_compute_orbit(m)): raise ProjectionDomainError("cached orbit differs from its recomputed content")
    return o


@dataclass(frozen=True)
class ProjectedTail:
    window_means: Tuple[float, ...]
    s_min: float
    s_term: float
    orbit_tail_mean: float


def projected_tail_stats(series: np.ndarray) -> ProjectedTail:
    if not isinstance(series, np.ndarray) or series.dtype != np.float64 or series.shape != (RUN_LEN,) or not np.isfinite(series).all() or (series < 0).any() or (series > 1).any():
        raise ProjectionDomainError("series must be a finite float64 vector of RUN_LEN in [0, 1]")
    tail = series[TAIL_START:TAIL_END + 1]
    wm = tuple(float(np.mean(tail[i * WINDOW:(i + 1) * WINDOW])) for i in range(N_WINDOWS))
    term = tail[TERMINAL_WINDOWS[0] * WINDOW:(TERMINAL_WINDOWS[-1] + 1) * WINDOW]
    return ProjectedTail(wm, float(min(wm)), float(np.mean(term)), float(np.mean(tail)))


def projected_label(m_micro: int) -> Tuple[str, ProjectedTail, _N.NullThresholds]:
    th = _N.reference_thresholds(_level(m_micro)); pt = projected_tail_stats(orbit(m_micro))
    return ("S" if pt.s_min > th.theta_p else ("N" if pt.s_term <= th.theta_t else "U")), pt, th


# ----------------------------------------------------------------------------- reference structure (every scientific field DERIVED)
def dense_grid_micro() -> Tuple[int, ...]:
    return tuple(range(DENSE_START_MICRO, DENSE_END_MICRO + 1, DENSE_STEP_MICRO))


REFERENCE_ROLES = ("analysis_subset", "reference_of_record")
LEGAL_MODES = ("exact_certified", "conservative_coverage")
HALT_MODE = ("halt", "halt")
UNRECORDED_MODE = ("unrecorded", "unrecorded")        # analysis_subset built from synthetic labels only; never on a record


def _is_hex64(s) -> bool: return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)


def _classify(labels: Sequence[str], levels: Sequence[int], halts: Sequence[str]) -> Tuple[str, Optional[Tuple[int, int]], int, int, str]:
    lab = tuple(labels); lv = tuple(levels)
    n_idx = [i for i, x in enumerate(lab) if x == "N"]; s_idx = [i for i, x in enumerate(lab) if x == "S"]
    if halts: return "REFERENCE-UNRESOLVED", None, 0, 0, "reference null failed its precision requirement at grid instantiation"
    if n_idx and s_idx and min(s_idx) < max(n_idx): return "ORDER-VIOLATING/MULTIPLE", None, 0, 0, "an S lies strictly below an N"
    if not n_idx and not s_idx: return "REFERENCE-UNRESOLVED", None, 0, 0, "all U"
    if not s_idx: return ("NO-SUSTAINED-PHASE", None, 0, 0, "no S; hard top point N") if lab[-1] == "N" else ("REFERENCE-UNRESOLVED", None, 0, 0, "no S but the hard top point is U: phase could be hidden")
    if not n_idx: return ("NO-NULL-PHASE", None, 0, 0, "no N; hard bottom point S") if lab[0] == "S" else ("REFERENCE-UNRESOLVED", None, 0, 0, "no N but the hard bottom point is U: phase could be hidden")
    lo, hi = max(n_idx), min(s_idx)
    off = [i for i, x in enumerate(lab) if x == "U" and not (lo < i < hi)]
    max_run = 0; cur = 0; prev = None
    for i in off:
        cur = cur + 1 if prev is not None and i == prev + 1 else 1; prev = i; max_run = max(max_run, cur)
    if len(off) > OFF_BAND_U_TOTAL or max_run > OFF_BAND_U_RUN: return "REFERENCE-UNRESOLVED", None, len(off), max_run, "off-band unresolved (allowance exceeded)"
    return "UNIQUE-THRESHOLD", (lv[lo], lv[hi]), len(off), max_run, "both phases, order respected"


@dataclass(frozen=True)
class ReferenceStructure:
    role: str
    structure_class: str
    labels: Tuple[str, ...]
    levels_micro: Tuple[int, ...]
    grid_sha256: str
    expected_points: int
    realized_points: int
    precision_halt_count: int
    precision_halts: Tuple[str, ...]
    modes: Tuple[Tuple[str, str], ...]
    bracket_micro: Optional[Tuple[int, int]]
    midpoint_micro: Optional[int]
    off_band_u_total: int
    off_band_u_max_run: int
    reason: str
    m3_reference_sha256: str
    m5_declaration_sha256: str
    result_sha256: str

    def __post_init__(self) -> None: validate_reference_structure(self)


def _reference_result_identity(r) -> str:
    return _digest((r.role, r.structure_class, r.labels, r.levels_micro, r.expected_points, r.precision_halts, r.modes, r.bracket_micro, r.off_band_u_total, r.off_band_u_max_run, r.reason, r.m3_reference_sha256, r.m5_declaration_sha256))


def validate_reference_structure(r) -> None:
    """EVERY scientific field re-derived from (labels, levels, halts, modes) (L2 r2 §3); identity computed only after."""
    if type(r) is not ReferenceStructure: raise ProjectionDomainError("exact ReferenceStructure required")
    if r.role not in REFERENCE_ROLES: raise ProjectionDomainError("unknown role")
    lab, lv = r.labels, r.levels_micro
    if type(lab) is not tuple or type(lv) is not tuple or not lab or len(lab) != len(lv): raise ProjectionDomainError("labels/levels must be non-empty tuples of equal length")
    if any(x not in ("S", "N", "U") for x in lab): raise ProjectionDomainError("labels must be S/N/U")
    if any(type(m) is not int for m in lv) or list(lv) != sorted(lv) or len(set(lv)) != len(lv): raise ProjectionDomainError("levels must be strictly ascending exact ints")
    for m in lv: _level(m)
    if r.grid_sha256 != _digest(lv) or r.realized_points != len(lv) or type(r.expected_points) is not int: raise ProjectionDomainError("grid identity/counts inconsistent")
    if type(r.precision_halts) is not tuple or r.precision_halt_count != len(r.precision_halts) or len(set(r.precision_halts)) != len(r.precision_halts): raise ProjectionDomainError("halt list inconsistent")
    if type(r.modes) is not tuple or len(r.modes) != len(lv): raise ProjectionDomainError("one mode pair per level required")
    ids = [level_id(m) for m in lv]
    for i, (md, x) in enumerate(zip(r.modes, lab)):
        if type(md) is not tuple or len(md) != 2: raise ProjectionDomainError("mode pair malformed")
        if md == HALT_MODE:
            if ids[i] not in r.precision_halts or x != "U": raise ProjectionDomainError("halt mode must coincide with a listed halt and a U label")
        elif md == UNRECORDED_MODE:
            if r.role == "reference_of_record": raise ProjectionDomainError("reference_of_record requires recorded threshold modes")
        elif not (md[0] in LEGAL_MODES and md[1] in LEGAL_MODES): raise ProjectionDomainError("mode pair not in M3's legal modes")
    for h in r.precision_halts:
        if h not in ids or r.modes[ids.index(h)] != HALT_MODE: raise ProjectionDomainError("listed halt without a halt mode at that level")
    cls, br, tot, run, why = _classify(lab, lv, r.precision_halts)
    if (r.structure_class, r.bracket_micro, r.off_band_u_total, r.off_band_u_max_run, r.reason) != (cls, br, tot, run, why): raise ProjectionDomainError("structure fields do not re-derive from the labels")
    if r.midpoint_micro != ((br[0] + br[1]) // 2 if br else None): raise ProjectionDomainError("midpoint does not derive from the bracket")
    if r.role == "reference_of_record":
        if lv != dense_grid_micro() or r.expected_points != DENSE_POINTS or r.precision_halt_count != 0: raise ProjectionDomainError("reference_of_record requires the exact 701-point grid, all points, and zero precision halts")
        if r.m3_reference_sha256 != m3_reference_identity() or r.m5_declaration_sha256 != PROJECTION_DECLARATION_SHA256_LITERAL: raise ProjectionDomainError("reference_of_record identities differ from the current instrument")
    else:
        if r.expected_points != len(lv): raise ProjectionDomainError("analysis subset expected points must equal its levels")
    if not (_is_hex64(r.m3_reference_sha256) and _is_hex64(r.m5_declaration_sha256)): raise ProjectionDomainError("identities must be sha256")
    if r.result_sha256 != _reference_result_identity(r): raise ProjectionDomainError("reference result identity does not recompute")


def structure_class(labels: Sequence[str], levels: Sequence[int], precision_halts: Sequence[str] = (), modes: Sequence[Tuple[str, str]] = (), role: str = "analysis_subset") -> ReferenceStructure:
    lab = tuple(labels); lv = tuple(levels)
    if len(lab) != len(lv) or not lab or any(x not in ("S", "N", "U") for x in lab): raise ProjectionDomainError("labels must be S/N/U, one per level")
    if list(lv) != sorted(lv) or len(set(lv)) != len(lv): raise ProjectionDomainError("levels must be strictly ascending")
    cls, br, tot, run, why = _classify(lab, lv, precision_halts)
    if role == "reference_of_record" and (lv != dense_grid_micro() or precision_halts): raise ProjectionDomainError("reference_of_record requires the exact dense grid and zero halts")
    md = tuple(modes) if modes else tuple(UNRECORDED_MODE for _ in lv)
    fields = (role, cls, lab, lv, _digest(lv), DENSE_POINTS if role == "reference_of_record" else len(lv), len(lv), len(precision_halts), tuple(precision_halts), md, br,
              (br[0] + br[1]) // 2 if br else None, tot, run, why, m3_reference_identity(), PROJECTION_DECLARATION_SHA256_LITERAL)
    probe = object.__new__(ReferenceStructure)
    for name, val in zip(ReferenceStructure.__dataclass_fields__, fields + ("",)): object.__setattr__(probe, name, val)
    return ReferenceStructure(*fields, _reference_result_identity(probe))


def classify_grid(levels: Sequence[int], role: str = "analysis_subset") -> ReferenceStructure:
    verify_frozen_identity(); lv = tuple(_level(x) for x in levels)
    if list(lv) != sorted(lv) or len(set(lv)) != len(lv): raise ProjectionDomainError("levels must be strictly ascending and unique")
    labels: List[str] = []; halts: List[str] = []; modes: List[Tuple[str, str]] = []
    for m in lv:
        try:
            lab, pt, th = projected_label(m); labels.append(lab); modes.append(tuple(th.threshold_modes))
        except _N.NullDomainError as e:
            if "no support point" in str(e) or "not certified" in str(e): halts.append(level_id(m)); labels.append("U"); modes.append(HALT_MODE)
            else: raise
    return structure_class(labels, lv, halts, modes, role)


def dense_reference() -> ReferenceStructure:
    r = classify_grid(dense_grid_micro(), role="analysis_subset")
    if r.precision_halt_count: raise ProjectionDomainError(f"dense reference has {r.precision_halt_count} precision halt(s): no reference of record")
    return structure_class(r.labels, r.levels_micro, (), r.modes, role="reference_of_record")


def departure_zone(ref: ReferenceStructure) -> Optional[Tuple[int, int]]:
    validate_reference_structure(ref)
    if ref.structure_class != "UNIQUE-THRESHOLD" or ref.midpoint_micro is None: return None
    return (ref.midpoint_micro - DELTA_M_R, ref.midpoint_micro + DELTA_M_R)


# ----------------------------------------------------------------------------- fixed-point census (diagnostic only)
@dataclass(frozen=True)
class FixedPointCensus:
    levels_micro: Tuple[int, ...]
    fixed_points: Tuple[Tuple[float, ...], ...]
    counts: Tuple[int, ...]
    structure_changes: int
    character: str


def fixed_points(m_micro: int, grid: int = 4001, refine: int = 60) -> Tuple[float, ...]:
    verify_frozen_identity(); m = _level(m_micro); rs = np.linspace(0.0, 1.0, grid); f = _g(rs, m) - rs; out = []
    for i in range(grid - 1):
        if f[i] == 0.0: out.append(float(rs[i]))
        elif np.sign(f[i]) != np.sign(f[i + 1]):
            a, b = rs[i], rs[i + 1]
            for _ in range(refine):
                c = 0.5 * (a + b); fc = float(_g(np.array([c]), m)[0] - c)
                if np.sign(fc) == np.sign(float(_g(np.array([a]), m)[0] - a)): a = c
                else: b = c
            out.append(0.5 * (a + b))
    return tuple(out)


def fixed_point_census(levels: Sequence[int]) -> FixedPointCensus:
    lv = tuple(_level(x) for x in levels); fps = tuple(fixed_points(m) for m in lv); counts = tuple(len(f) for f in fps)
    changes = sum(1 for a, b in zip(counts, counts[1:]) if a != b)
    char = f"over the {len(lv)} evaluated levels: " + ("one root at each; no count change" if all(c == 1 for c in counts) and changes == 0 else f"{changes} count change(s); counts {counts}")
    return FixedPointCensus(lv, fps, counts, changes, char)


# ----------------------------------------------------------------------------- T2-S (M4 grammar enforced)
@dataclass(frozen=True)
class T2S:
    reference_class: str
    e1_verdict: str
    e1_cause: Optional[str]
    status: str
    note: str
    proceed_to_t2l: bool


def validate_e1_result(e1_verdict: str, e1_cause: Optional[str]) -> None:
    if e1_verdict not in _V.VERDICTS: raise ProjectionDomainError(f"unknown E1 verdict {e1_verdict!r}")
    legal = {"LOCATED": (None,), "NOT_PRODUCED": tuple(_V.NP_CAUSES), "NOT_DISTINGUISHED": tuple(_V.ND_CAUSES)}[e1_verdict]
    if e1_cause not in legal: raise ProjectionDomainError(f"cause {e1_cause!r} is not legal for verdict {e1_verdict}")


def t2s(reference_class: str, e1_verdict: str, e1_cause: Optional[str]) -> T2S:
    if reference_class not in STRUCTURE_CLASSES: raise ProjectionDomainError(f"unknown reference class {reference_class!r}")
    validate_e1_result(e1_verdict, e1_cause)
    for rc, ev, ec, status, note in T2S_TABLE:
        if (rc == "*" or rc == reference_class) and (ev == "*" or ev == e1_verdict) and (ec == "*" or ec == e1_cause):
            return T2S(reference_class, e1_verdict, e1_cause, status, note, note == "proceed to T2-L")
    raise ProjectionDomainError("T2-S table is not total for this input")


def matching_e1_category(reference_class: str) -> Optional[Tuple[str, str]]:
    for rc, ev, ec in MATCHING_E1_CATEGORY:
        if rc == reference_class: return (ev, ec)
    return None


# ----------------------------------------------------------------------------- finite-N realizations
def finite_n_homogeneous(m_micro: int, n_replicates: int, master: int, level_key: int) -> np.ndarray:
    verify_frozen_identity(); m = _level(m_micro); n = _exact_int(n_replicates, "n_replicates", 1)
    g = np.random.default_rng(np.random.SeedSequence([int(master), int(level_key), m]))
    rho = np.full(n, RHO_0); out = np.empty((n, HORIZON)); out[:, 0] = rho
    for t in range(1, HORIZON):
        c = g.binomial(N_CELLS, _g(rho, m)); rho = c / N_CELLS; out[:, t] = rho
    return out


def finite_n_per_seed(m_micro: int, seed: int, g: np.random.Generator) -> np.ndarray:
    m = _level(m_micro); ch, v, u, r = _N._replay_initialization(m, seed); k = DynamicsConstants()
    lam = (v * u * r).reshape(-1); rho = RHO_0; counts = np.empty(TAIL_LEN, dtype=np.int64)
    for t in range(HORIZON):
        pb = 1.0 / (1.0 + np.exp(-(k.alpha * lam + k.beta * rho - k.delta * rho * rho - k.gamma_offset)))
        p = np.clip(pb + k.eta_floor * (1.0 - pb), 0.0, 1.0)
        c = int(np.sum(g.random(N_CELLS) < p))
        if t >= TAIL_START: counts[t - TAIL_START] = int(round(rho * N_CELLS))
        rho = c / N_CELLS
    return _A._series_from_counts(counts)


# ----------------------------------------------------------------------------- tolerances (derived by replay), T1, T3
TOLERANCE_ROLES = ("canonical", "smoke")


@dataclass(frozen=True)
class Tolerances:
    role: str
    level_micro: int
    master: int
    n_replicates: int
    quantile: float
    method: str
    orbit_tail_mean: float
    tau_eq: float
    tau_eq_ci_half_width: float
    tau_traj: float
    tau_traj_ci_half_width: float
    tau_disp: float
    tau_disp_ci_half_width: float
    deviation_sha256: str
    result_sha256: str

    def __post_init__(self) -> None: validate_tolerances(self, replay=False)


def _tolerance_identity(t) -> str:
    return _digest((t.role, t.level_micro, t.master, t.n_replicates, t.quantile, t.method, t.orbit_tail_mean, t.tau_eq, t.tau_eq_ci_half_width, t.tau_traj, t.tau_traj_ci_half_width, t.tau_disp, t.tau_disp_ci_half_width, t.deviation_sha256))


def _q(x: np.ndarray) -> float: return float(np.quantile(x, TOLERANCE_QUANTILE, method=TOLERANCE_QUANTILE_METHOD))


def _q_ci_half(x: np.ndarray, g: np.random.Generator) -> float:
    idx = g.integers(0, x.size, size=(TOLERANCE_CI_RESAMPLES, x.size)); qs = np.quantile(x[idx], TOLERANCE_QUANTILE, axis=1, method=TOLERANCE_QUANTILE_METHOD)
    return float((np.percentile(qs, 97.5) - np.percentile(qs, 2.5)) / 2.0)


def _derive_tolerance_values(m: int, n: int, master: int) -> Tuple[float, float, float, float, float, float, float, str]:
    """THE derivation: (orbit tail mean, τ_eq, ci, τ_traj, ci, τ_disp, ci, deviation identity) from the frozen orbit and the replayed ensemble."""
    o = orbit(m); reps = finite_n_homogeneous(m, n, master, 1); otm = float(np.mean(o[TAIL_START:]))
    tails = reps[:, TAIL_START:].mean(axis=1)
    dev_eq = np.abs(tails - otm); dev_traj = np.abs(reps[:, :TAIL_START] - o[None, :TAIL_START]).mean(axis=1)
    groups = tails[: (n // T1_SEED_COUNT) * T1_SEED_COUNT].reshape(-1, T1_SEED_COUNT); rng_stat = groups.max(axis=1) - groups.min(axis=1)
    g = np.random.default_rng(np.random.SeedSequence([master, 7, m]))
    return otm, _q(dev_eq), _q_ci_half(dev_eq, g), _q(dev_traj), _q_ci_half(dev_traj, g), _q(rng_stat), _q_ci_half(rng_stat, g), _content(dev_eq, dev_traj, rng_stat)


def validate_tolerances(t, replay: bool = True) -> None:
    """Formatting at construction; with replay=True (every scientific use) the complete value set is RE-DERIVED from the
    frozen orbit and the replayed finite-N ensemble and must reproduce exactly (L2 r2 §4.1)."""
    if type(t) is not Tolerances or t.role not in TOLERANCE_ROLES: raise ProjectionDomainError("exact Tolerances with a known role required")
    m = _level(t.level_micro); _exact_int(t.master, "master", 1); _exact_int(t.n_replicates, "n_replicates", T1_SEED_COUNT)
    if t.role == "canonical" and (t.master, t.n_replicates, t.quantile, t.method) != (TOLERANCE_MASTER, TOLERANCE_REPLICATES, TOLERANCE_QUANTILE, TOLERANCE_QUANTILE_METHOD):
        raise ProjectionDomainError("canonical tolerances require the frozen master, replicate count, quantile, and method")
    if t.role == "smoke" and (t.master, t.n_replicates) == (TOLERANCE_MASTER, TOLERANCE_REPLICATES): raise ProjectionDomainError("the exact canonical program must carry the canonical role")
    if (t.quantile, t.method) != (TOLERANCE_QUANTILE, TOLERANCE_QUANTILE_METHOD): raise ProjectionDomainError("quantile/method are frozen")
    vals = (t.orbit_tail_mean, t.tau_eq, t.tau_traj, t.tau_disp, t.tau_eq_ci_half_width, t.tau_traj_ci_half_width, t.tau_disp_ci_half_width)
    if not all(type(x) is float and math.isfinite(x) and x >= 0.0 for x in vals) or not 0.0 <= t.orbit_tail_mean <= 1.0: raise ProjectionDomainError("tolerance values must be finite non-negative floats; orbit mean in [0, 1]")
    if not _is_hex64(t.deviation_sha256): raise ProjectionDomainError("deviation identity must be sha256")
    if t.result_sha256 != _tolerance_identity(t): raise ProjectionDomainError("tolerance result identity does not recompute")
    if replay:
        derived = _derive_tolerance_values(m, t.n_replicates, t.master)
        if derived != (t.orbit_tail_mean, t.tau_eq, t.tau_eq_ci_half_width, t.tau_traj, t.tau_traj_ci_half_width, t.tau_disp, t.tau_disp_ci_half_width, t.deviation_sha256):
            raise ProjectionDomainError("tolerance values do not re-derive by replay of the declared program")


def tolerances(m_micro: int, n_replicates: int = TOLERANCE_REPLICATES, master: int = TOLERANCE_MASTER) -> Tolerances:
    verify_frozen_identity(); m = _level(m_micro); n = _exact_int(n_replicates, "n_replicates", T1_SEED_COUNT); _exact_int(master, "master", 1)
    role = "canonical" if (master, n) == (TOLERANCE_MASTER, TOLERANCE_REPLICATES) else "smoke"
    otm, teq, teqc, ttr, ttrc, tdp, tdpc, dsha = _derive_tolerance_values(m, n, master)
    fields = (role, m, master, n, TOLERANCE_QUANTILE, TOLERANCE_QUANTILE_METHOD, otm, teq, teqc, ttr, ttrc, tdp, tdpc, dsha)
    probe = object.__new__(Tolerances)
    for name, val in zip(Tolerances.__dataclass_fields__, fields + ("",)): object.__setattr__(probe, name, val)
    return Tolerances(*fields, _tolerance_identity(probe))


@dataclass(frozen=True)
class T1Result:
    level_micro: int
    status: str
    reason: str
    n_settled: int
    mean_settled_rho: Optional[float]
    orbit_tail_mean: float
    deviation: Optional[float]
    tau_eq: float
    tau_disp: float
    in_departure_zone: bool
    tolerance_role: str
    tolerance_sha256: str
    reference_sha256: str


def t1_orbit_tail_agreement(m_micro: int, settled_rho_bars: Sequence[float], tol: Tolerances, ref: ReferenceStructure) -> T1Result:
    m = _level(m_micro); validate_tolerances(tol, replay=True); validate_reference_structure(ref)
    if tol.level_micro != m: raise ProjectionDomainError("tolerances belong to a different level")
    vals = [float(x) for x in settled_rho_bars]
    if any(not math.isfinite(x) or not 0.0 <= x <= 1.0 for x in vals): raise ProjectionDomainError("settled rho values must be finite in [0, 1]")
    zone = departure_zone(ref); inz = zone is not None and zone[0] <= m <= zone[1]
    base = dict(level_micro=m, n_settled=len(vals), orbit_tail_mean=tol.orbit_tail_mean, tau_eq=tol.tau_eq, tau_disp=tol.tau_disp, in_departure_zone=inz, tolerance_role=tol.role, tolerance_sha256=tol.result_sha256, reference_sha256=ref.result_sha256)
    if tol.role != "canonical" or ref.role != "reference_of_record": return T1Result(status="NOT EVALUABLE", reason="noncanonical tolerances or reference: no scientific status", mean_settled_rho=None, deviation=None, **base)
    if len(vals) < T1_MIN_SETTLED: return T1Result(status="NOT EVALUABLE", reason=f"settled runs {len(vals)} < {T1_MIN_SETTLED}", mean_settled_rho=None, deviation=None, **base)
    if max(vals) - min(vals) > tol.tau_disp: return T1Result(status="NOT EVALUABLE", reason="cross-seed settled estimates disagree beyond tau_disp", mean_settled_rho=float(np.mean(vals)), deviation=None, **base)
    dev = abs(float(np.mean(vals)) - tol.orbit_tail_mean)
    if inz: return T1Result(status="NOT EVALUABLE", reason="level inside the reference-side departure zone (T1/T3 exemption)", mean_settled_rho=float(np.mean(vals)), deviation=dev, **base)
    return T1Result(status="RECOVERED" if dev <= tol.tau_eq else "NOT RECOVERED", reason="within tau_eq" if dev <= tol.tau_eq else "exceeds tau_eq", mean_settled_rho=float(np.mean(vals)), deviation=dev, **base)


@dataclass(frozen=True)
class T3Result:
    level_micro: int
    status: str
    reason: str
    distance: Optional[float]
    tau_traj: float
    in_departure_zone: bool
    tolerance_role: str
    tolerance_sha256: str
    reference_sha256: str


def t3_trajectory_distance(m_micro: int, mean_production_trajectory: np.ndarray, tol: Tolerances, ref: ReferenceStructure) -> T3Result:
    m = _level(m_micro); validate_tolerances(tol, replay=True); validate_reference_structure(ref)
    if tol.level_micro != m: raise ProjectionDomainError("tolerances belong to a different level")
    tr = np.asarray(mean_production_trajectory, dtype=np.float64)
    if tr.shape != (RUN_LEN,) or not np.isfinite(tr).all() or (tr < 0).any() or (tr > 1).any(): raise ProjectionDomainError("trajectory must be a finite RUN_LEN vector in [0, 1]")
    zone = departure_zone(ref); inz = zone is not None and zone[0] <= m <= zone[1]
    d = float(np.mean(np.abs(tr[:TAIL_START] - orbit(m)[:TAIL_START])))
    if tol.role != "canonical" or ref.role != "reference_of_record": return T3Result(m, "NOT EVALUABLE", "noncanonical tolerances or reference: no scientific status", d, tol.tau_traj, inz, tol.role, tol.result_sha256, ref.result_sha256)
    if inz: return T3Result(m, "NOT EVALUABLE", "level inside the reference-side departure zone", d, tol.tau_traj, True, tol.role, tol.result_sha256, ref.result_sha256)
    return T3Result(m, "RECOVERED" if d <= tol.tau_traj else "NOT RECOVERED", "within tau_traj" if d <= tol.tau_traj else "exceeds tau_traj", d, tol.tau_traj, False, tol.role, tol.result_sha256, ref.result_sha256)


# ----------------------------------------------------------------------------- projection sweeps (derived records)
HALT_CATEGORIES = ("evaluability:uncertified_threshold",)


@dataclass(frozen=True)
class ProjectionSweep:
    sweep_index: int
    master: int
    pass1_labels: Tuple[str, ...]
    pass1_verdict: str
    pass1_cause: Optional[str]
    router_row: str
    nominal_insertions: int
    realized_insertions: int
    insertions_micro: Tuple[int, ...]
    fallback_moves: Tuple[Tuple[int, int], ...]
    fallback_drops: Tuple[int, ...]
    final_levels_micro: Tuple[int, ...]
    final_labels: Tuple[str, ...]
    verdict: str
    cause: Optional[str]
    rule: str
    bracket_micro: Optional[Tuple[int, int]]
    cache_body_sha256: str
    cache_file_sha256: str
    cache_qualification_sha256: str
    m5_declaration_sha256: str
    halt_category: Optional[str]
    halt_detail: Optional[str]
    sweep_sha256: str = ""

    def __post_init__(self) -> None: validate_projection_sweep(self)


def _sweep_identity(s) -> str:
    return _digest((s.sweep_index, s.master, s.pass1_labels, s.insertions_micro, s.fallback_moves, s.fallback_drops, s.final_levels_micro, s.final_labels, s.verdict, s.cause, s.rule, s.bracket_micro,
                    s.cache_body_sha256, s.cache_file_sha256, s.cache_qualification_sha256, s.m5_declaration_sha256, s.halt_category, s.halt_detail))


def validate_projection_sweep(s) -> None:
    """Every M4/router-derived field RE-DERIVED from the carried profiles (L2 r2 §11); provenance surface exact."""
    if type(s) is not ProjectionSweep: raise ProjectionDomainError("exact ProjectionSweep required")
    _exact_int(s.sweep_index, "sweep_index", 0)
    if s.master != PROJECTION_MASTER: raise ProjectionDomainError("sweep master must be PROJECTION_MASTER")
    if s.m5_declaration_sha256 != PROJECTION_DECLARATION_SHA256_LITERAL: raise ProjectionDomainError("sweep declaration identity differs from the current M5 declaration")
    if (s.cache_body_sha256, s.cache_file_sha256, s.cache_qualification_sha256) != (_A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, _A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL):
        raise ProjectionDomainError("sweep cache bundle must equal the source-literal production identities (a projection sweep can only run on the production cache)")
    if type(s.pass1_labels) is not tuple or len(s.pass1_labels) != len(E1_LEVELS_MICRO) or any(x not in _K.LEVEL_LABELS for x in s.pass1_labels): raise ProjectionDomainError("pass-1 labels malformed")
    v1 = evaluate(s.pass1_labels, E1_LEVELS_MICRO); d = route(s.pass1_labels, E1_LEVELS_MICRO)
    if (s.pass1_verdict, s.pass1_cause) != (v1.verdict, v1.cause): raise ProjectionDomainError("pass-1 verdict does not re-derive from the pass-1 labels")
    nominal = _V.P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else (2 * _V.P2R_PER_INTERVAL_INSERTIONS if d.row == "P2R-4" else 0)
    if (s.router_row, s.nominal_insertions, s.realized_insertions, s.insertions_micro, s.fallback_moves, s.fallback_drops) != (d.row, nominal, len(d.insertions_micro), tuple(d.insertions_micro), tuple(d.fallback_moves), tuple(d.fallback_drops)):
        raise ProjectionDomainError("router fields do not re-derive from the pass-1 labels")
    if s.halt_category is not None:
        if s.halt_category not in HALT_CATEGORIES or type(s.halt_detail) is not str: raise ProjectionDomainError("illegal halt category/detail")
        if (s.final_levels_micro, s.final_labels, s.verdict, s.cause, s.rule, s.bracket_micro) != ((), (), "HALTED", None, "", None): raise ProjectionDomainError("a halted sweep carries no final profile")
    else:
        if s.halt_detail is not None: raise ProjectionDomainError("halt detail without a halt category")
        exp_levels = tuple(sorted(tuple(E1_LEVELS_MICRO) + tuple(d.insertions_micro)))
        if s.final_levels_micro != exp_levels or len(s.final_labels) != len(exp_levels) or any(x not in _K.LEVEL_LABELS for x in s.final_labels): raise ProjectionDomainError("final grid does not re-derive from pass-1 plus accepted insertions")
        pos = {m: i for i, m in enumerate(exp_levels)}
        if any(s.final_labels[pos[m]] != s.pass1_labels[i] for i, m in enumerate(E1_LEVELS_MICRO)): raise ProjectionDomainError("pass-1 labels not preserved in the final profile")
        vf = evaluate(s.final_labels, s.final_levels_micro)
        if (s.verdict, s.cause, s.rule, s.bracket_micro) != (vf.verdict, vf.cause, vf.rule, vf.bracket_micro): raise ProjectionDomainError("final verdict/cause/rule/bracket do not re-derive from the final profile")
    if s.sweep_sha256 != _sweep_identity(s): raise ProjectionDomainError("sweep identity does not recompute")


def projection_sweep(sweep_index: int, cache) -> ProjectionSweep:
    verify_frozen_identity(); i = _exact_int(sweep_index, "sweep_index", 0)
    if not _A.is_production_cache(cache): raise ProjectionDomainError("projection sweeps require the production_frozen threshold cache")
    ident = (cache.body_sha256, cache.file_sha256, cache.qualification_sha256, PROJECTION_DECLARATION_SHA256_LITERAL)
    def labels_at(levels: Sequence[int]) -> Tuple[str, ...]:
        out = []
        for m in levels:
            statuses = []
            for seed in E1_SEED_PANEL:
                g = np.random.default_rng(np.random.SeedSequence([PROJECTION_MASTER, i, int(m), int(seed)]))
                try: th = cache.get(m, seed)
                except _A.AuditDomainError as e: raise ProjectionApparatusError(f"production cache lacks reachable key level {level_id(m)} seed {seed}: {e}")
                statuses.append(run_status(finite_n_per_seed(m, seed, g), th.theta_p, th.theta_t)[0])
            out.append(level_label(level_counts(statuses)))
        return tuple(out)
    lab1 = labels_at(E1_LEVELS_MICRO); v1 = evaluate(lab1, E1_LEVELS_MICRO); d = route(lab1, E1_LEVELS_MICRO)
    nominal = _V.P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else (2 * _V.P2R_PER_INTERVAL_INSERTIONS if d.row == "P2R-4" else 0)
    if d.insertions_micro:
        lab2 = labels_at(d.insertions_micro); merged = sorted(list(zip(E1_LEVELS_MICRO, lab1)) + list(zip(d.insertions_micro, lab2)))
        levels_f = tuple(m for m, _ in merged); lab_f = tuple(l for _, l in merged)
    else: levels_f, lab_f = tuple(E1_LEVELS_MICRO), lab1
    vf = evaluate(lab_f, levels_f)
    fields = (i, PROJECTION_MASTER, lab1, v1.verdict, v1.cause, d.row, nominal, len(d.insertions_micro), tuple(d.insertions_micro), tuple(d.fallback_moves), tuple(d.fallback_drops),
              levels_f, lab_f, vf.verdict, vf.cause, vf.rule, vf.bracket_micro, *ident, None, None)
    probe = object.__new__(ProjectionSweep)
    for name, val in zip(ProjectionSweep.__dataclass_fields__, fields + ("",)): object.__setattr__(probe, name, val)
    return ProjectionSweep(*fields, _sweep_identity(probe))


# ----------------------------------------------------------------------------- design stability (exact ensemble, derived)
@dataclass(frozen=True)
class DesignStability:
    reference_class: str
    reference_role: str
    reference_sha256: str
    matching_category: Optional[Tuple[str, str]]
    declared_sweeps: int
    attempted: int
    scored: int
    halted: int
    n_matching: int
    match_rate_over_attempted: float
    cp_lower_95: float
    complete: bool
    design_stable: bool
    status: str
    ensemble_sha256: str
    cache_body_sha256: str
    cache_file_sha256: str
    cache_qualification_sha256: str
    m5_declaration_sha256: str
    result_sha256: str = ""


def _cp_lower(k: int, n: int) -> float: return 1.0 - _A.clopper_pearson_upper(n - k, n)


def _ds_identity(d) -> str:
    return _digest((d.reference_class, d.reference_role, d.reference_sha256, d.matching_category, d.declared_sweeps, d.attempted, d.scored, d.halted, d.n_matching, d.match_rate_over_attempted, d.cp_lower_95,
                    d.complete, d.design_stable, d.status, d.ensemble_sha256, d.cache_body_sha256, d.cache_file_sha256, d.cache_qualification_sha256, d.m5_declaration_sha256))


def _ensemble_facts(ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep]):
    """Validate every sweep; derive the ensemble surface and the design-stability fields. Shared by constructor and validator."""
    if any(type(s) is not ProjectionSweep for s in sweeps): raise ProjectionDomainError("sweeps must be exact ProjectionSweep records")
    for s in sweeps: validate_projection_sweep(s)
    att = len(sweeps); idx = tuple(s.sweep_index for s in sweeps)
    exact_set = idx == tuple(range(DESIGN_STABILITY_SWEEPS))
    bundles = {(s.cache_body_sha256, s.cache_file_sha256, s.cache_qualification_sha256) for s in sweeps}; decls = {s.m5_declaration_sha256 for s in sweeps}
    if len(bundles) > 1 or len(decls) > 1: raise ProjectionDomainError("sweeps span more than one cache bundle or declaration")
    bundle = next(iter(bundles)) if bundles else ("", "", "")
    canonical_bundle = bundle == (_A.PRODUCTION_CACHE_BODY_SHA256_LITERAL, _A.PRODUCTION_CACHE_FILE_SHA256_LITERAL, _A.PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)
    halted = sum(1 for s in sweeps if s.halt_category is not None); cat = matching_e1_category(ref.structure_class)
    match = 0 if cat is None else sum(1 for s in sweeps if s.halt_category is None and s.verdict == cat[0] and (cat[1] == "*" or s.cause == cat[1]))
    rate = match / att if att else 0.0; lower = _cp_lower(match, att) if att else 0.0
    complete = exact_set and halted == 0 and ref.role == "reference_of_record" and cat is not None and canonical_bundle
    stable = complete and lower >= 1.0 - T2L_FAILURE_CAP
    status = "NOT EVALUABLE (incomplete)" if not complete else ("DESIGN-STABLE" if stable else "NOT DESIGN-STABLE")
    ens = _digest(tuple(s.sweep_sha256 for s in sweeps))
    return cat, att, att - halted, halted, match, rate, lower, complete, stable, status, ens, bundle


def design_stability(ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep]) -> DesignStability:
    validate_reference_structure(ref)
    cat, att, scored, halted, match, rate, lower, complete, stable, status, ens, bundle = _ensemble_facts(ref, sweeps)
    fields = (ref.structure_class, ref.role, ref.result_sha256, cat, DESIGN_STABILITY_SWEEPS, att, scored, halted, match, rate, lower, complete, stable, status, ens, *bundle, PROJECTION_DECLARATION_SHA256_LITERAL)
    probe = object.__new__(DesignStability)
    for name, val in zip(DesignStability.__dataclass_fields__, fields + ("",)): object.__setattr__(probe, name, val)
    return DesignStability(*fields, _ds_identity(probe))


def validate_design_stability(d: DesignStability, ref: ReferenceStructure, sweeps: Sequence[ProjectionSweep]) -> None:
    """Re-derive the complete gate from the reference and the supplied sweeps (L2 r2 §4.2)."""
    if type(d) is not DesignStability: raise ProjectionDomainError("exact DesignStability required")
    validate_reference_structure(ref)
    if (d.reference_class, d.reference_role, d.reference_sha256) != (ref.structure_class, ref.role, ref.result_sha256): raise ProjectionDomainError("gate reference identity differs")
    cat, att, scored, halted, match, rate, lower, complete, stable, status, ens, bundle = _ensemble_facts(ref, sweeps)
    if (d.matching_category, d.declared_sweeps, d.attempted, d.scored, d.halted, d.n_matching, d.match_rate_over_attempted, d.cp_lower_95, d.complete, d.design_stable, d.status, d.ensemble_sha256) != \
       (cat, DESIGN_STABILITY_SWEEPS, att, scored, halted, match, rate, lower, complete, stable, status, ens): raise ProjectionDomainError("design-stability fields do not re-derive from the ensemble")
    if (d.cache_body_sha256, d.cache_file_sha256, d.cache_qualification_sha256, d.m5_declaration_sha256) != (*bundle, PROJECTION_DECLARATION_SHA256_LITERAL): raise ProjectionDomainError("gate identity bundle differs")
    if d.result_sha256 != _ds_identity(d): raise ProjectionDomainError("design-stability identity does not recompute")


# ----------------------------------------------------------------------------- T2-L (validates the gate and every sweep first)
@dataclass(frozen=True)
class T2L:
    status: str
    reason: str
    envelope_micro: Optional[Tuple[int, int]]
    reference_bracket_micro: Optional[Tuple[int, int]]
    production_bracket_micro: Optional[Tuple[int, int]]
    attempted: int
    halted: int
    n_conditioned: int
    fail_fraction_over_attempted: float
    ci_half_widths_micro: Optional[Tuple[float, float]]
    e_l_micro: Optional[int]
    e_u_micro: Optional[int]
    gates: Tuple[Tuple[str, bool], ...]
    conditioned_sha256: str
    bootstrap_sha256: str
    design_stability_status: str
    design_stability_sha256: str
    reference_sha256: str
    result_sha256: str = ""


def _t2l_identity(r) -> str:
    return _digest((r.status, r.reason, r.envelope_micro, r.reference_bracket_micro, r.production_bracket_micro, r.attempted, r.halted, r.n_conditioned, r.fail_fraction_over_attempted, r.ci_half_widths_micro,
                    r.e_l_micro, r.e_u_micro, r.gates, r.conditioned_sha256, r.bootstrap_sha256, r.design_stability_status, r.design_stability_sha256, r.reference_sha256))


def _t2l_facts(ref: ReferenceStructure, ds: DesignStability, sweeps: Sequence[ProjectionSweep], production_bracket_micro) -> Dict[str, object]:
    """THE T2-L derivation, shared by constructor and validator (L2 r3 §7): validates the reference, the gate against the
    supplied sweeps (hence every sweep and the exact ensemble), the production bracket; then derives every scientific field."""
    validate_reference_structure(ref)
    if type(ds) is not DesignStability: raise ProjectionDomainError("exact DesignStability required")
    validate_design_stability(ds, ref, sweeps)
    att = len(sweeps); halted = sum(1 for s in sweeps if s.halt_category is not None)
    cond = [s for s in sweeps if s.halt_category is None and s.verdict == "LOCATED" and s.bracket_micro is not None]
    fail_frac = (1.0 - len(cond) / att) if att else 1.0
    f: Dict[str, object] = dict(reference_bracket_micro=ref.bracket_micro, production_bracket_micro=production_bracket_micro, attempted=att, halted=halted, n_conditioned=len(cond),
                                fail_fraction_over_attempted=fail_frac, design_stability_status=ds.status, design_stability_sha256=ds.result_sha256, reference_sha256=ref.result_sha256,
                                envelope_micro=None, ci_half_widths_micro=None, e_l_micro=None, e_u_micro=None, gates=(), conditioned_sha256="", bootstrap_sha256="")
    if production_bracket_micro is not None:
        pb = production_bracket_micro
        if not (isinstance(pb, tuple) and len(pb) == 2 and all(type(x) is int for x in pb) and pb[0] < pb[1]): raise ProjectionDomainError("production bracket must be an ascending pair of exact ints")
        _level(pb[0]); _level(pb[1])
    if ref.role != "reference_of_record" or ref.structure_class != "UNIQUE-THRESHOLD" or ref.bracket_micro is None:
        return {**f, "status": "NOT EVALUABLE", "reason": "reference is not a reference_of_record UNIQUE-THRESHOLD"}
    if not (ds.complete and ds.design_stable): return {**f, "status": "NOT EVALUABLE", "reason": "design-stability gate not complete/stable for this ensemble"}
    if production_bracket_micro is None: return {**f, "status": "NOT EVALUABLE", "reason": "E1 verdict is not LOCATED"}
    gates: List[Tuple[str, bool]] = [("unique_bracket_failure_fraction_within_cap", fail_frac <= T2L_FAILURE_CAP)]
    csha = _digest(tuple(s.sweep_sha256 for s in cond)); f["conditioned_sha256"] = csha
    if fail_frac > T2L_FAILURE_CAP or len(cond) < 2:
        return {**f, "gates": tuple(gates), "status": "NOT EVALUABLE", "reason": "design-resolution limit: too many replicate sweeps fail to yield a unique bracket"}
    lo = np.array([s.bracket_micro[0] for s in cond], dtype=np.float64); hi = np.array([s.bracket_micro[1] for s in cond], dtype=np.float64)
    L_env = int(round(float(np.percentile(lo, ENVELOPE_QUANTILES[0], method="linear")))); U_env = int(round(float(np.percentile(hi, ENVELOPE_QUANTILES[1], method="linear"))))
    g = np.random.default_rng(np.random.SeedSequence([BOOTSTRAP_MASTER, len(cond)])); idx = g.integers(0, len(cond), size=(BOOTSTRAP_RESAMPLES, len(cond)))
    bl = np.percentile(lo[idx], ENVELOPE_QUANTILES[0], axis=1, method="linear"); bu = np.percentile(hi[idx], ENVELOPE_QUANTILES[1], axis=1, method="linear")
    hw = (float((np.percentile(bl, 97.5) - np.percentile(bl, 2.5)) / 2.0), float((np.percentile(bu, 97.5) - np.percentile(bu, 2.5)) / 2.0))
    gates.append(("endpoint_ci_half_widths_within_delta_m_est", hw[0] <= DELTA_M_EST and hw[1] <= DELTA_M_EST))
    e_l = max(0, ref.bracket_micro[0] - L_env); e_u = max(0, U_env - ref.bracket_micro[1])
    gates.append(("informativeness_e_L_and_e_U_within_delta_m_loc", e_l <= DELTA_M_LOC and e_u <= DELTA_M_LOC))
    f.update(envelope_micro=(L_env, U_env), ci_half_widths_micro=hw, e_l_micro=e_l, e_u_micro=e_u, gates=tuple(gates), bootstrap_sha256=_digest((BOOTSTRAP_MASTER, BOOTSTRAP_RESAMPLES, len(cond), hw)))
    if not all(ok for _, ok in gates): return {**f, "status": "NOT EVALUABLE", "reason": T2L_FAILURE_DISPOSITION if not gates[-1][1] else "endpoint estimation precision insufficient"}
    overlap = production_bracket_micro[0] <= U_env and L_env <= production_bracket_micro[1]
    return {**f, "status": "RECOVERED" if overlap else "NOT RECOVERED", "reason": "production bracket overlaps the envelope" if overlap else "no overlap"}


def t2l(ref: ReferenceStructure, ds: DesignStability, sweeps: Sequence[ProjectionSweep], production_bracket_micro: Optional[Tuple[int, int]]) -> T2L:
    """T2-L: the record is the shared derivation's output with its identity computed last."""
    f = _t2l_facts(ref, ds, sweeps, production_bracket_micro)
    probe = object.__new__(T2L)
    for name in T2L.__dataclass_fields__: object.__setattr__(probe, name, f.get(name, ""))
    return T2L(**f, result_sha256=_t2l_identity(probe))


def validate_t2l(result, ref: ReferenceStructure, ds: DesignStability, sweeps: Sequence[ProjectionSweep], production_bracket_micro) -> None:
    """A persisted T2-L record proves it came from the honest derivation: every carried field must equal the re-derived
    value from the supplied reference, gate, exact ensemble and production bracket; identity recomputed last."""
    if type(result) is not T2L: raise ProjectionDomainError("exact T2L required")
    f = _t2l_facts(ref, ds, sweeps, production_bracket_micro)
    for k, v in f.items():
        if getattr(result, k) != v: raise ProjectionDomainError(f"T2-L field {k} does not re-derive")
    if result.result_sha256 != _t2l_identity(result): raise ProjectionDomainError("T2-L identity does not recompute")


# ----------------------------------------------------------------------------- reference stability audit (both axes; halts carried; derived)
STABILITY_ROLES = ("analysis_subset", "canonical")


def classify_grid_under_template(levels: Sequence[int], template: np.ndarray) -> ReferenceStructure:
    verify_frozen_identity(); lv = tuple(_level(x) for x in levels); labels = []; halts = []; modes = []
    w = E1_BASE_WIDTH_MICRO / MICRO_UNITS; t = _N.validate_template(template)
    for m in lv:
        b = (m / MICRO_UNITS - w / 2.0) + w * t
        try:
            th = _N.conditional_thresholds_for_analysis(m, b[:, 0].reshape(-1), b[:, 1].reshape(-1), b[:, 2].reshape(-1))
            pt = projected_tail_stats(orbit(m)); labels.append("S" if pt.s_min > th.theta_p else ("N" if pt.s_term <= th.theta_t else "U")); modes.append(tuple(th.threshold_modes))
        except _N.NullDomainError as e:
            if "no support point" in str(e) or "not certified" in str(e): halts.append(level_id(m)); labels.append("U"); modes.append(HALT_MODE)
            else: raise
    return structure_class(labels, lv, halts, modes, role="analysis_subset")


@dataclass(frozen=True)
class StabilityAudit:
    role: str
    primary_class: str
    primary_sha256: str
    grid_sha256: str
    alternative_records: Tuple[Tuple[int, int, ReferenceStructure], ...]      # (seed_set k, template j, the COMPLETE alternative reference record)
    alternatives: Tuple[Tuple[int, int, str, Optional[Tuple[int, int]], Optional[int], Optional[int], int, Tuple[str, ...], str], ...]   # DERIVED summary rows
    n_expected: int
    n_realized: int
    class_reproduced_by_all: bool
    any_alternative_halted: bool
    max_displacement_micro: Optional[int]
    complete: bool
    within_delta_m_stab: bool
    result_sha256: str = ""


def _sa_identity(s) -> str:
    recs = tuple((e[0], e[1], getattr(e[2], "result_sha256", repr(e[2]))) if isinstance(e, tuple) and len(e) == 3 else repr(e) for e in s.alternative_records)   # robust: malformed input reaches the validator
    return _digest((s.role, s.primary_class, s.primary_sha256, s.grid_sha256, recs, s.alternatives, s.n_expected, s.n_realized,
                    s.class_reproduced_by_all, s.any_alternative_halted, s.max_displacement_micro, s.complete, s.within_delta_m_stab))


def _sa_rows(primary: ReferenceStructure, records) -> Tuple:
    """Summary rows DERIVED from validated alternative records (never accepted as carried)."""
    rows = []
    for k, j, r in records:
        validate_reference_structure(r)
        if r.levels_micro != primary.levels_micro or r.role != "analysis_subset": raise ProjectionDomainError("alternative record must be an analysis_subset on the primary's exact grid")
        d0 = d1 = None
        if primary.bracket_micro and r.bracket_micro: d0, d1 = abs(r.bracket_micro[0] - primary.bracket_micro[0]), abs(r.bracket_micro[1] - primary.bracket_micro[1])
        rows.append((k, j, r.structure_class, r.bracket_micro, d0, d1, r.precision_halt_count, r.precision_halts, r.result_sha256))
    return tuple(rows)


def _sa_facts(primary: ReferenceStructure, rows):
    n_exp = STABILITY_ALT_SEED_SETS * STABILITY_ALT_TEMPLATES
    cells = [(a[0], a[1]) for a in rows]
    same = all(a[2] == primary.structure_class for a in rows); any_halt = any(a[6] > 0 for a in rows)
    disp = [x for a in rows for x in (a[4], a[5]) if x is not None]; mx = max(disp) if disp else None
    role = "canonical" if (primary.role == "reference_of_record" and primary.levels_micro == dense_grid_micro()) else "analysis_subset"
    complete = len(rows) == n_exp and len(set(cells)) == n_exp and set(cells) == {(k, j) for k in range(STABILITY_ALT_SEED_SETS) for j in range(STABILITY_ALT_TEMPLATES)} and role == "canonical" and not any_halt
    within = complete and same and (mx is None or mx <= DELTA_M_STAB)
    return role, n_exp, same, any_halt, mx, complete, within


def _alternative_template(k: int, j: int) -> np.ndarray:
    return np.random.default_rng(np.random.SeedSequence([STABILITY_MASTER, k, j])).random((N_CELLS, 3))


def stability_audit(levels: Sequence[int], primary: ReferenceStructure) -> StabilityAudit:
    validate_reference_structure(primary); lv = tuple(_level(x) for x in levels)
    if primary.levels_micro != lv: raise ProjectionDomainError("stability audit levels must equal the primary reference's levels")
    records = tuple((k, j, classify_grid_under_template(lv, _alternative_template(k, j))) for k in range(STABILITY_ALT_SEED_SETS) for j in range(STABILITY_ALT_TEMPLATES))
    rows = _sa_rows(primary, records); role, n_exp, same, any_halt, mx, complete, within = _sa_facts(primary, rows)
    fields = (role, primary.structure_class, primary.result_sha256, _digest(lv), records, rows, n_exp, len(rows), same, any_halt, mx, complete, within)
    probe = object.__new__(StabilityAudit)
    for name, val in zip(StabilityAudit.__dataclass_fields__, fields + ("",)): object.__setattr__(probe, name, val)
    return StabilityAudit(*fields, _sa_identity(probe))


def validate_stability_audit(s: StabilityAudit, primary: ReferenceStructure, replay: bool = False) -> None:
    """Every alternative record validated (class/bracket/halts/modes re-derived from its own labels); summary rows re-derived
    from the records; opaque identities impossible (each row's identity is the validated record's own); with replay=True each
    alternative is regenerated from (STABILITY_MASTER, k, j) and reclassified and must reproduce exactly."""
    if type(s) is not StabilityAudit: raise ProjectionDomainError("exact StabilityAudit required")
    validate_reference_structure(primary)
    if (s.primary_class, s.primary_sha256, s.grid_sha256) != (primary.structure_class, primary.result_sha256, _digest(primary.levels_micro)): raise ProjectionDomainError("audit primary identity differs")
    if type(s.alternative_records) is not tuple or any(type(e) is not tuple or len(e) != 3 or type(e[0]) is not int or type(e[1]) is not int or type(e[2]) is not ReferenceStructure for e in s.alternative_records):
        raise ProjectionDomainError("alternative records malformed")
    rows = _sa_rows(primary, s.alternative_records)
    if s.alternatives != rows: raise ProjectionDomainError("alternative summary rows do not derive from the alternative records")
    role, n_exp, same, any_halt, mx, complete, within = _sa_facts(primary, rows)
    if (s.role, s.n_expected, s.n_realized, s.class_reproduced_by_all, s.any_alternative_halted, s.max_displacement_micro, s.complete, s.within_delta_m_stab) != (role, n_exp, len(rows), same, any_halt, mx, complete, within):
        raise ProjectionDomainError("stability fields do not re-derive from the alternatives")
    if replay:
        for k, j, r in s.alternative_records:
            if classify_grid_under_template(primary.levels_micro, _alternative_template(k, j)).result_sha256 != r.result_sha256: raise ProjectionDomainError(f"alternative ({k}, {j}) does not reproduce by replay")
    if s.result_sha256 != _sa_identity(s): raise ProjectionDomainError("stability identity does not recompute")
