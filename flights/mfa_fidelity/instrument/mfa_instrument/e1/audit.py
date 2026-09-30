"""mfa_instrument/e1/audit.py — E1 stage-1 module M6, ROUND 2 of the rebuild on the conditional per-seed
interface (Contract E1 v0.3 §7 items 3–4; v0.4 §7; v0.5 D; L2 M6-rebuild review items A1–A6, §10–§13).

CLAIM BOUNDARY (L2 §13, enforced in every record label): a passing audit establishes ONLY that a class is
DISTINGUISHED AS SCIENTIFIC VERSUS NOT_DISTINGUISHED at the declared bound — the applicable-error question.
It does NOT establish that the machinery recognizes the exact archetype verdict and cause. Exact-agreement
figures are carried as DESCRIPTIVE ONLY and never enter any pass.

SCORING OBJECT: each production seed's OWN conditional null (M3 amendment). A run is scored against its own
certified (θ_P, θ_T); a level label aggregates twenty per-seed status calls.

THE PRODUCTION CACHE BOUNDARY (L2 A3): a `ThresholdCache` carries a ROLE. Only `production_frozen` may feed
a freeze-qualifying audit, and that role is granted only by `load_production_cache`, which requires: the
committed body digest (a source literal), the committed file digest, exact audit/M3/M4/reachable-surface
identities embedded in the artifact, the exact 7,580-row count, exact noncoercive row schema, duplicate-key
refusal, exact declared counts, exact key coverage, canonical row order, and a QUALIFICATION RECORD stating
replay verification COMPLETE (the one-time canonical-machine pass `qualify_threshold_cache`, which replays
every row, adds M3's threshold payload identity to each, and rewrites the artifact). The mapping is immutable.
A production audit never derives a threshold on demand: a missing reachable key is an apparatus defect and
HALTS the audit. Smoke/slice caches keep a distinct role and can never produce an ensemble pass.

COMPLETION (L2 A1): a class is COMPLETE only when attempted == scored == 500 and halted == 0 AND the cap
clears; `ensemble_pass` requires every class complete. The nonhalted bound is descriptive when halts occur.
QUALIFICATION (L2 A2): `qualify_audit` mechanically joins a design record and a held-out record — exact
distinct masters, the same production cache identity, exact class sets, 500/500/0 per class, every cap in
both, distinct record identities. M6's `ensemble_pass` is NOT a freeze pass; only the qualification is.

GENERATOR (L2 A4/A5): a deeply immutable GENERATOR_DECLARATION freezes every load-bearing rule (class widths,
temporal modes, offsets, index ranges, attenuation, RNG hierarchy and draw order, the exact intended map) and
is compared field-by-field to the live implementation at preflight. Every parameter draw passes an
`archetype_preflight` that proves the named morphology is actually instantiated inside the frozen sweep;
failures are REDRAWN deterministically from a dedicated stream up to MAX_REDRAWS with the attempt count
recorded; exhaustion is a GENERATOR HALT (apparatus failure, never a classifier error). `run_sweep` asserts
the preflight again before generating any series.

PAIRING (narrowed, L2 §14.5): common per-seed REGIME-ASSIGNMENT uniforms across levels; time-series
realization noise is NOT a full common-random-number pairing.
"""
from __future__ import annotations

import hashlib
import json
import math
import types
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from ..config import MICRO_UNITS
from . import classify as _K
from . import config as _C
from . import null as _N
from . import verdict as _V
from .classify import COUNTS, N_CELLS, RUN_LEN, TAIL_START, TAIL_LEN, WINDOW, N_WINDOWS, level_counts, level_label, run_status
from .config import E1_LEVELS_MICRO, E1_SEED_PANEL, level_id
from .verdict import ARCHETYPE_TABLE, evaluate, route

AUDIT_VERSION = "e1_stage1_m6_v3_conditional / Contract E1 v0.3 §7 + v0.4 §7 + v0.5 D + M3 amendment"
N_SEEDS = COUNTS["n_runs"]


class AuditDomainError(ValueError):
    """Frozen identity violated, input outside the audit's domain, or an apparatus defect."""


class ThresholdUncertifiable(RuntimeError):
    def __init__(self, level_micro: int, seed: int, detail: str) -> None:
        super().__init__(detail); self.level_micro = level_micro; self.seed = seed


class GeneratorHalt(RuntimeError):
    """Archetype preflight exhausted its frozen redraw budget: an apparatus failure, never a classifier error."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def _frozen_mapping(decl, name):
    keys = [k for k, _ in decl]
    if len(set(keys)) != len(keys):
        raise AuditDomainError(f"{name}: duplicate declaration field names")
    return dict(decl)


def _exact_int(x, name, lo=None):
    if isinstance(x, bool) or not isinstance(x, int):
        raise AuditDomainError(f"{name} must be an exact non-Boolean integer")
    if lo is not None and x < lo:
        raise AuditDomainError(f"{name} must be >= {lo}")
    return x


def _exact_float(x, name, lo=None, hi=None):
    if isinstance(x, bool) or not isinstance(x, float) or not math.isfinite(x):
        raise AuditDomainError(f"{name} must be a finite float")
    if (lo is not None and x < lo) or (hi is not None and x > hi):
        raise AuditDomainError(f"{name} out of range")
    return x


def _level(x, name="level"):
    m = _exact_int(x, name)
    if m - _C.E1_BASE_WIDTH_MICRO // 2 < 0 or m + _C.E1_BASE_WIDTH_MICRO // 2 > MICRO_UNITS:
        raise AuditDomainError(f"{name} {m} inadmissible")
    return m


def _seed(x, name="seed"):
    s = _exact_int(x, name)
    if s not in E1_SEED_PANEL:
        raise AuditDomainError(f"{name} is not a frozen production seed")
    return s


# ----------------------------------------------------------------------------- audit declaration
SWEEPS_PER_CLASS = 500                           # [PROPOSED]
CAP = 0.10                                       # [PROPOSED]
CP_CONFIDENCE = 0.95
AUDIT_MASTER = 202609221
HELD_OUT_MASTER = 202609222
PRICING_MASTER = 202609223
PRICING_REPLICATES = 400
MAX_REDRAWS = 64                                 # frozen generator redraw budget per sweep

INTENDED_MAP: Tuple[Tuple[str, str, Optional[str]], ...] = ARCHETYPE_TABLE     # the exact known-answer mapping, frozen by identity below
SCIENTIFIC_CLASSES = tuple(n for n, v, _ in INTENDED_MAP if v in ("LOCATED", "NOT_PRODUCED"))
ND_CLASSES = tuple(n for n, v, _ in INTENDED_MAP if v == "NOT_DISTINGUISHED")
CLASSES = tuple(n for n, _, _ in INTENDED_MAP)

AUDIT_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("version", AUDIT_VERSION), ("scoring_object", "conditional_per_seed"), ("sweeps_per_class", SWEEPS_PER_CLASS),
    ("cap", CAP), ("cp_confidence", CP_CONFIDENCE), ("cp_side", "one-sided upper"),
    ("audit_master", AUDIT_MASTER), ("held_out_master", HELD_OUT_MASTER), ("pricing_master", PRICING_MASTER),
    ("pricing_replicates", PRICING_REPLICATES), ("n_seeds", N_SEEDS), ("max_redraws", MAX_REDRAWS),
    ("classes", CLASSES), ("scientific_classes", SCIENTIFIC_CLASSES), ("nd_classes", ND_CLASSES),
    ("applicable_error", "scientific-intent classes: final NOT_DISTINGUISHED; ND-intent classes: final LOCATED or NOT_PRODUCED"),
    ("claim_boundary", "a pass establishes distinguished-as-scientific-vs-ND at the bound; exact archetype recognition is descriptive only"),
    ("completion", "attempted == scored == 500 and halted == 0 and cap clears; ensemble_pass requires every class complete"),
    ("qualification", "design AND held-out records mechanically joined; ensemble_pass alone is never a freeze pass"),
    ("pairing", "common per-seed regime-assignment uniforms across levels; realization noise not fully paired"),
    ("production_cache", "role production_frozen only via load_production_cache with a qualification record; no on-demand thresholds"),
)
AUDIT_DECLARATION_SHA256_LITERAL = "60eb65d4e28c6bdd1f62f8183b29d944e8d9476bc5e986c1412a0cd76b9441f2"   # established 2026-09-26

# ----------------------------------------------------------------------------- generator declaration (complete, frozen)
P_HIGH_RANGE = (0.30, 0.60)
DRIFT_RANGE = (-0.10, 0.10)
OSC_AMP_RANGE = (0.05, 0.25)
OSC_PERIOD_RANGE = (50, 400)
DIP_WINDOWS = (0, N_WINDOWS - 1)
GENTLE_WIDTH_MICRO = (60_000, 120_000)
ABRUPT_WIDTH_MICRO = (0, 20_000)
WIDE_WIDTH_MICRO = (150_000, 250_000)
ONSET_RANGE_MICRO = (300_000, 700_000)
MIXTURE_PI_RANGE = (0.30, 0.70)
SECOND_ONSET_INCREMENT_MICRO = (120_000, 200_000)      # exclusive upper (integers 120000..199999)
TWO_CROSSING_OFFSETS_MICRO = (110_000, 220_000)
EXTRA_LEVEL_INDEX_RANGE = (0, 4)                       # exclusive upper (0..3)
NONMONOTONE_ATTENUATION = 0.5
NONMONOTONE_SCALE_MICRO = 400_000
CLASS_WIDTH: Tuple[Tuple[str, str], ...] = (("gentle_onset", "gentle"), ("off_band_mixture", "gentle"), ("wide_mixed_boundary", "wide"),
                                            ("unresolved_heavy_boundary", "wide"))          # all others: abrupt
TEMPORAL_CLASSES: Tuple[str, ...] = ("persistent_nonstationary_high_m",)                     # choose drift|oscillation; all others constant
TEMPORAL_MODES = ("constant", "drift", "oscillation")
RNG_HIERARCHY = "SeedSequence([master, class_index, sweep_index]); draws: params (redraw stream: SeedSequence([master, class_index, sweep_index, attempt])) then seed_us"
PARAM_DRAW_ORDER = ("onset", "width", "p_high", "temporal", "drift", "amp", "period", "pi", "second_onset_increment", "extra_level_index")

GENERATOR_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("regimes", ("NULL", "SUSTAINED", "DIP")), ("p_high_range", P_HIGH_RANGE), ("drift_range", DRIFT_RANGE),
    ("osc_amp_range", OSC_AMP_RANGE), ("osc_period_range", OSC_PERIOD_RANGE), ("dip_windows", DIP_WINDOWS), ("dip_window_ticks", WINDOW),
    ("gentle_width_micro", GENTLE_WIDTH_MICRO), ("abrupt_width_micro", ABRUPT_WIDTH_MICRO), ("wide_width_micro", WIDE_WIDTH_MICRO),
    ("onset_range_micro", ONSET_RANGE_MICRO), ("mixture_pi_range", MIXTURE_PI_RANGE),
    ("second_onset_increment_micro", SECOND_ONSET_INCREMENT_MICRO), ("two_crossing_offsets_micro", TWO_CROSSING_OFFSETS_MICRO),
    ("extra_level_index_range", EXTRA_LEVEL_INDEX_RANGE), ("nonmonotone_attenuation", NONMONOTONE_ATTENUATION),
    ("nonmonotone_scale_micro", NONMONOTONE_SCALE_MICRO), ("class_width", CLASS_WIDTH), ("temporal_classes", TEMPORAL_CLASSES),
    ("temporal_modes", TEMPORAL_MODES), ("rng_hierarchy", RNG_HIERARCHY), ("param_draw_order", PARAM_DRAW_ORDER),
    ("max_redraws", MAX_REDRAWS), ("preflight", "archetype_preflight: named morphology instantiated inside the frozen sweep (see function)"),
    ("intended_map", INTENDED_MAP),
)
GENERATOR_DECLARATION_SHA256_LITERAL = "527cc5f8de300546d1b9f8f53ad1bdccf782accda37ed5a9f97fca277d804dd8"   # established 2026-09-26


def verify_frozen_identity() -> None:
    _C.verify_frozen_identity(); _K.verify_frozen_identity(); _N.verify_frozen_identity(); _V.verify_frozen_identity()
    if _digest(AUDIT_DECLARATION) != AUDIT_DECLARATION_SHA256_LITERAL:
        raise AuditDomainError("audit declaration differs from its frozen literal digest")
    if _digest(GENERATOR_DECLARATION) != GENERATOR_DECLARATION_SHA256_LITERAL:
        raise AuditDomainError("generator declaration differs from its frozen literal digest")
    d = _frozen_mapping(AUDIT_DECLARATION, "AUDIT_DECLARATION"); g = _frozen_mapping(GENERATOR_DECLARATION, "GENERATOR_DECLARATION")
    live_a = {"version": AUDIT_VERSION, "scoring_object": "conditional_per_seed", "sweeps_per_class": SWEEPS_PER_CLASS, "cap": CAP,
              "cp_confidence": CP_CONFIDENCE, "audit_master": AUDIT_MASTER, "held_out_master": HELD_OUT_MASTER, "pricing_master": PRICING_MASTER,
              "pricing_replicates": PRICING_REPLICATES, "n_seeds": N_SEEDS, "max_redraws": MAX_REDRAWS, "classes": CLASSES,
              "scientific_classes": SCIENTIFIC_CLASSES, "nd_classes": ND_CLASSES}
    live_g = {"regimes": ("NULL", "SUSTAINED", "DIP"), "p_high_range": P_HIGH_RANGE, "drift_range": DRIFT_RANGE, "osc_amp_range": OSC_AMP_RANGE,
              "osc_period_range": OSC_PERIOD_RANGE, "dip_windows": DIP_WINDOWS, "dip_window_ticks": WINDOW, "gentle_width_micro": GENTLE_WIDTH_MICRO,
              "abrupt_width_micro": ABRUPT_WIDTH_MICRO, "wide_width_micro": WIDE_WIDTH_MICRO, "onset_range_micro": ONSET_RANGE_MICRO,
              "mixture_pi_range": MIXTURE_PI_RANGE, "second_onset_increment_micro": SECOND_ONSET_INCREMENT_MICRO,
              "two_crossing_offsets_micro": TWO_CROSSING_OFFSETS_MICRO, "extra_level_index_range": EXTRA_LEVEL_INDEX_RANGE,
              "nonmonotone_attenuation": NONMONOTONE_ATTENUATION, "nonmonotone_scale_micro": NONMONOTONE_SCALE_MICRO, "class_width": CLASS_WIDTH,
              "temporal_classes": TEMPORAL_CLASSES, "temporal_modes": TEMPORAL_MODES, "rng_hierarchy": RNG_HIERARCHY, "param_draw_order": PARAM_DRAW_ORDER,
              "max_redraws": MAX_REDRAWS, "intended_map": INTENDED_MAP}
    for src, live in ((d, live_a), (g, live_g)):
        for k, v in live.items():
            if src[k] != v or type(src[k]) is not type(v):
                raise AuditDomainError(f"declaration field {k} differs from the live global")
    if (SWEEPS_PER_CLASS, CAP, CP_CONFIDENCE, N_SEEDS, PRICING_REPLICATES, MAX_REDRAWS) != (500, 0.10, 0.95, 20, 400, 64) or len({AUDIT_MASTER, HELD_OUT_MASTER, PRICING_MASTER}) != 3:
        raise AuditDomainError("audit hard values differ from the contract or ensembles are not independent")
    if INTENDED_MAP != ARCHETYPE_TABLE or _digest(INTENDED_MAP) != _V.ARCHETYPE_TABLE_SHA256_LITERAL:
        raise AuditDomainError("intended map differs from M4's frozen archetype table")
    if set(SCIENTIFIC_CLASSES) | set(ND_CLASSES) != set(CLASSES) or set(SCIENTIFIC_CLASSES) & set(ND_CLASSES):
        raise AuditDomainError("class partition inconsistent with the intended map")
    if DIP_WINDOWS != (0, N_WINDOWS - 1) or WINDOW != 100:
        raise AuditDomainError("DIP geometry inconsistent with M2's window constants")


INTENDED = types.MappingProxyType({n: (v, c) for n, v, c in INTENDED_MAP})


# ----------------------------------------------------------------------------- Clopper–Pearson (fail-closed)
def _betacf(x: float, a: float, b: float) -> Tuple[float, bool]:
    MAXIT, EPS, FPMIN = 300, 3e-14, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = FPMIN if abs(d) < FPMIN else d; d = 1.0 / d; h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = FPMIN if abs(d) < FPMIN else d; c = 1.0 + aa / c; c = FPMIN if abs(c) < FPMIN else c; d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = FPMIN if abs(d) < FPMIN else d; c = 1.0 + aa / c; c = FPMIN if abs(c) < FPMIN else c; d = 1.0 / d
        de = d * c; h *= de
        if abs(de - 1.0) < EPS:
            return h, True
    return h, False


def _beta_cdf(x: float, a: float, b: float) -> float:
    if x <= 0.0: return 0.0
    if x >= 1.0: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        h, ok = _betacf(x, a, b); val = front * h / a
    else:
        h, ok = _betacf(1.0 - x, b, a); val = 1.0 - front * h / b
    if not ok or not math.isfinite(val):
        raise AuditDomainError("regularized incomplete beta did not converge or is nonfinite")
    return val


def _beta_ppf(q: float, a: float, b: float) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _beta_cdf(mid, a, b) < q: lo = mid
        else: hi = mid
    out = 0.5 * (lo + hi)
    if not math.isfinite(out): raise AuditDomainError("beta quantile nonfinite")
    return out


def clopper_pearson_upper(k, n, confidence=CP_CONFIDENCE) -> float:
    k = _exact_int(k, "k"); n = _exact_int(n, "n", 1); _exact_float(confidence, "confidence")
    if not (0.0 < confidence < 1.0): raise AuditDomainError("confidence must lie in (0, 1)")
    if not 0 <= k <= n: raise AuditDomainError("Clopper–Pearson requires 0 <= k <= n")
    if k == n: return 1.0
    return _beta_ppf(confidence, float(k + 1), float(n - k))


# ----------------------------------------------------------------------------- threshold cache and the production boundary
CACHE_ROLES = ("production_frozen", "slice")
PRODUCTION_CACHE_BODY_SHA256_LITERAL = "4659b062414f7b77680cb9c2df3bdb967675376b9908ed10f5fefd843b8e9feb"   # canonical-machine qualification 2026-09-28: 7580/7580 replayed, 13221 s
PRODUCTION_CACHE_FILE_SHA256_LITERAL = "608844ff7bd636d59faed391398524879806abdddd3c0bfc92b3396e7c93932e"
PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL = "5c933778c0a8f1056ace4bf14fd27e496b4ce7446ddd156f7d17a485e6d153ab"   # committed qualification-record FILE bytes, commit 790f73e, read from a fresh clone 2026-09-29
ROW_SCHEMA: Tuple[Tuple[str, type], ...] = (("level_micro", int), ("seed", int), ("theta_p", float), ("theta_t", float),
                                            ("modes", list), ("bases_sha256", str), ("config_hash", str), ("scoring_identity", str),
                                            ("payload_sha256", str))


@dataclass(frozen=True)
class SeedThreshold:
    level_micro: int
    seed: int
    theta_p: float
    theta_t: float
    modes: Tuple[str, str]
    bases_sha256: str
    config_hash: str
    scoring_identity: str
    payload_sha256: str


def _conditional_for(level_micro: int, seed: int) -> Tuple[SeedThreshold, _N.NullThresholds]:
    m = _level(level_micro); s = _seed(seed)
    ch, v, u, r = _N._replay_initialization(m, s)
    th = _N.conditional_thresholds(m, s, v, u, r)
    _N.require_production_scoring_object(th, m, s, _N.bases_identity(v, u, r), ch)
    return SeedThreshold(m, s, th.theta_p, th.theta_t, tuple(th.threshold_modes), th.bases_sha256, th.config_hash, th.scoring_identity, th.payload_sha256), th


def reachable_pass2_levels() -> Tuple[int, ...]:
    """Pass-2 insertion levels the router can produce on the frozen grid, from route() POST-FALLBACK over the
    canonical band witnesses (M4's reachable surface) — never the raw evenly-spaced union."""
    verify_frozen_identity()
    n = len(E1_LEVELS_MICRO); levels: set = set()
    for i in range(n):
        for j in range(i + 1, n):
            lab = ["U"] * n
            for k in range(0, i + 1): lab[k] = "N"
            for k in range(j, n): lab[k] = "S"
            levels |= {int(x) for x in route(tuple(lab), E1_LEVELS_MICRO).insertions_micro}
    levels -= set(E1_LEVELS_MICRO)
    return tuple(sorted(levels))


def reachable_surface_identity() -> str:
    return _digest(("m4", _V.VERDICT_DECLARATION_SHA256_LITERAL, reachable_pass2_levels()))


def artifact_header() -> Dict[str, object]:
    p2 = reachable_pass2_levels()
    return {"version": AUDIT_VERSION, "m3_declaration_sha256": _N.NULL_DECLARATION_SHA256_LITERAL, "m3_scoring_object_version": _N.SCORING_OBJECT_VERSION,
            "m4_declaration_sha256": _V.VERDICT_DECLARATION_SHA256_LITERAL, "reachable_surface_sha256": reachable_surface_identity(),
            "n_levels": len(E1_LEVELS_MICRO), "n_pass2_levels": len(p2), "pass2_levels": list(p2), "n_seeds": N_SEEDS,
            "n_rows": (len(E1_LEVELS_MICRO) + len(p2)) * N_SEEDS}


def _canon(body) -> str:
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


def write_artifact(path: str, rows: List[Dict[str, object]]) -> Tuple[str, str]:
    """Write the artifact with the frozen header; returns (body digest, file digest)."""
    body = dict(artifact_header()); body["rows"] = sorted(rows, key=lambda r: (r["level_micro"], r["seed"]))
    bd = hashlib.sha256(_canon(body).encode()).hexdigest()
    text = _canon({"sha256": bd, "body": body})
    with open(path, "w", newline="\n") as f:
        f.write(text)
    return bd, hashlib.sha256(text.encode()).hexdigest()


class ThresholdCache:
    """Immutable per-(level,seed) conditional thresholds with a ROLE. Only `production_frozen` may feed a
    freeze-qualifying audit; it is granted only by `load_production_cache`."""
    __slots__ = ("_by", "role", "body_sha256", "file_sha256", "qualification", "qualification_sha256")

    def __init__(self, by: Dict[Tuple[int, int], SeedThreshold], role: str, body_sha256: str, file_sha256: Optional[str] = None,
                 qualification=None, qualification_sha256: Optional[str] = None) -> None:
        if role not in CACHE_ROLES: raise AuditDomainError("unknown cache role")
        for k, v in by.items():
            if type(v) is not SeedThreshold or (type(k[0]) is not int) or (type(k[1]) is not int) or (v.level_micro, v.seed) != k:
                raise AuditDomainError("cache mapping values must be exact SeedThreshold objects keyed by their own (level, seed)")
        object.__setattr__(self, "_by", types.MappingProxyType(dict(by)))
        object.__setattr__(self, "role", role); object.__setattr__(self, "body_sha256", body_sha256)
        object.__setattr__(self, "file_sha256", file_sha256); object.__setattr__(self, "qualification", qualification)
        object.__setattr__(self, "qualification_sha256", qualification_sha256)

    def __setattr__(self, k, v): raise AuditDomainError("ThresholdCache is immutable")

    def get(self, level_micro, seed) -> SeedThreshold:
        m = _level(level_micro); s = _seed(seed)
        try: return self._by[(m, s)]
        except KeyError: raise AuditDomainError(f"threshold cache has no entry for level {level_id(m)} seed {s}")

    def __len__(self): return len(self._by)


def _parse_rows(body) -> Dict[Tuple[int, int], SeedThreshold]:
    hdr = artifact_header()
    for k in ("version", "m3_declaration_sha256", "m3_scoring_object_version", "m4_declaration_sha256", "reachable_surface_sha256",
              "n_levels", "n_pass2_levels", "pass2_levels", "n_seeds", "n_rows"):
        if body.get(k) != hdr[k]:
            raise AuditDomainError(f"artifact header field {k} differs from the frozen expectation")
    rows = body.get("rows")
    if not isinstance(rows, list) or len(rows) != hdr["n_rows"]:
        raise AuditDomainError(f"artifact must carry exactly {hdr['n_rows']} rows")
    by: Dict[Tuple[int, int], SeedThreshold] = {}; prev = None
    for r in rows:
        if not isinstance(r, dict) or set(r.keys()) != {k for k, _ in ROW_SCHEMA} or len(r) != len(ROW_SCHEMA):
            raise AuditDomainError("artifact row keys differ from the exact schema")            # exact SET (canonical JSON sorts keys)
        for k, typ in ROW_SCHEMA:
            if type(r[k]) is not typ: raise AuditDomainError(f"artifact row field {k} has type {type(r[k]).__name__}, expected {typ.__name__}")
        st = SeedThreshold(r["level_micro"], r["seed"], r["theta_p"], r["theta_t"], tuple(r["modes"]), r["bases_sha256"], r["config_hash"], r["scoring_identity"], r["payload_sha256"])
        _level(st.level_micro); _seed(st.seed)
        key = (st.level_micro, st.seed)
        if key in by: raise AuditDomainError(f"duplicate artifact row for {key}")
        if prev is not None and key <= prev: raise AuditDomainError("artifact rows are not in canonical (level, seed) order")
        prev = key; by[key] = st
    expected = {(m, s) for m in tuple(E1_LEVELS_MICRO) + tuple(hdr["pass2_levels"]) for s in E1_SEED_PANEL}
    if set(by) != expected: raise AuditDomainError("artifact rows do not cover exactly the pass-1 and reachable pass-2 grid")
    return by


def load_artifact_rows(path: str) -> Tuple[Dict[Tuple[int, int], SeedThreshold], str, str]:
    raw = open(path, "rb").read()
    file_sha = hashlib.sha256(raw).hexdigest()
    doc = json.loads(raw.decode("utf-8"))
    body = doc["body"]
    if hashlib.sha256(_canon(body).encode()).hexdigest() != doc["sha256"]:
        raise AuditDomainError("artifact body digest does not match its embedded digest")
    return _parse_rows(body), doc["sha256"], file_sha


def load_slice_cache(path: str) -> ThresholdCache:
    """Any well-formed artifact, digest-checked only: role `slice` — never a production input."""
    verify_frozen_identity()
    by, bd, fs = load_artifact_rows(path)
    return ThresholdCache(by, "slice", bd, fs)


QUAL_SCHEMA: Tuple[Tuple[str, type], ...] = (("audit_version", str), ("body_sha256", str), ("file_sha256", str), ("n_rows", int), ("n_unique_keys", int),
                                             ("n_pass1_levels", int), ("n_pass2_levels", int), ("replay_verification_complete", bool),
                                             ("m3_declaration_sha256", str), ("m3_scoring_object_version", str), ("m4_declaration_sha256", str),
                                             ("reachable_surface_sha256", str))


def _is_hex64(s) -> bool:
    return isinstance(s, str) and len(s) == 64 and all(c in "0123456789abcdef" for c in s)


@dataclass(frozen=True)
class CacheQualification:
    audit_version: str
    body_sha256: str
    file_sha256: str
    n_rows: int
    n_unique_keys: int
    n_pass1_levels: int
    n_pass2_levels: int
    replay_verification_complete: bool
    m3_declaration_sha256: str
    m3_scoring_object_version: str
    m4_declaration_sha256: str
    reachable_surface_sha256: str

    def __post_init__(self) -> None:
        validate_cache_qualification(self)

    def canonical(self) -> str:
        return _canon(asdict(self))

    def record_sha256(self) -> str:
        return hashlib.sha256(self.canonical().encode()).hexdigest()


def validate_cache_qualification(q) -> None:
    """Exact type; exact field types (bool is bool — 1 is refused; ints non-Boolean); hex identities; the
    frozen header identities; replay COMPLETE required to be the literal True."""
    if type(q) is not CacheQualification: raise AuditDomainError("validate_cache_qualification requires an exact CacheQualification")
    for k, typ in QUAL_SCHEMA:
        v = getattr(q, k)
        if type(v) is not typ: raise AuditDomainError(f"qualification field {k} has type {type(v).__name__}, expected {typ.__name__}")
    for k in ("body_sha256", "file_sha256", "m3_declaration_sha256", "m4_declaration_sha256", "reachable_surface_sha256"):
        if not _is_hex64(getattr(q, k)): raise AuditDomainError(f"qualification field {k} is not a 64-hex sha256")
    hdr = artifact_header()
    if (q.audit_version, q.n_rows, q.n_unique_keys, q.n_pass1_levels, q.n_pass2_levels) != (AUDIT_VERSION, hdr["n_rows"], hdr["n_rows"], hdr["n_levels"], hdr["n_pass2_levels"]):
        raise AuditDomainError("qualification counts/version differ from the frozen expectation")
    if (q.m3_declaration_sha256, q.m3_scoring_object_version, q.m4_declaration_sha256, q.reachable_surface_sha256) != \
       (hdr["m3_declaration_sha256"], hdr["m3_scoring_object_version"], hdr["m4_declaration_sha256"], hdr["reachable_surface_sha256"]):
        raise AuditDomainError("qualification identities differ from the frozen header identities")
    if q.replay_verification_complete is not True: raise AuditDomainError("replay verification must be exactly True")


def qualify_threshold_cache(in_path: str, out_path: str, record_path: str) -> CacheQualification:
    """THE ONE-TIME CANONICAL-MACHINE QUALIFICATION: replay EVERY row (hours), require exact reproduction of
    every carried field, attach M3's threshold payload identity per row, rewrite the artifact, and write the
    qualification record. Only its outputs can become `production_frozen`."""
    verify_frozen_identity()
    raw = json.loads(open(in_path, "rb").read().decode("utf-8")); body = raw["body"]
    rows_out: List[Dict[str, object]] = []; seen = set()
    for r in body["rows"]:
        st, th = _conditional_for(r["level_micro"], r["seed"])
        for k in ("theta_p", "theta_t", "bases_sha256", "config_hash", "scoring_identity"):
            if getattr(st, k) != r[k]: raise AuditDomainError(f"row {(st.level_micro, st.seed)} field {k} does not reproduce by replay")
        if tuple(r["modes"]) != st.modes: raise AuditDomainError(f"row {(st.level_micro, st.seed)} modes do not reproduce")
        key = (st.level_micro, st.seed)
        if key in seen: raise AuditDomainError(f"duplicate input row {key}")
        seen.add(key); rows_out.append(asdict(st) | {"modes": list(st.modes)})
    bd, fs = write_artifact(out_path, rows_out)
    by, bd2, fs2 = load_artifact_rows(out_path)
    if (bd, fs) != (bd2, fs2): raise AuditDomainError("rewritten artifact does not reload to its own identities")
    hdr = artifact_header()
    q = CacheQualification(AUDIT_VERSION, bd, fs, len(by), len(set(by)), hdr["n_levels"], hdr["n_pass2_levels"], True,
                           hdr["m3_declaration_sha256"], hdr["m3_scoring_object_version"], hdr["m4_declaration_sha256"], hdr["reachable_surface_sha256"])
    with open(record_path, "w", newline="\n") as f:
        f.write(_canon(asdict(q)))
    return q


def load_production_cache(path: str, record_path: str) -> ThresholdCache:
    """The ONLY way to obtain role `production_frozen`: exact committed body and file digests (source
    literals), exact header identities, exact schema/coverage/order, and a qualification record that
    reproduces those identities and states replay verification COMPLETE."""
    verify_frozen_identity()
    if any("PENDING" in x for x in (PRODUCTION_CACHE_BODY_SHA256_LITERAL, PRODUCTION_CACHE_FILE_SHA256_LITERAL, PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)):
        raise AuditDomainError("production identities not yet established in source (artifact and/or qualification record)")
    by, bd, fs = load_artifact_rows(path)
    if bd != PRODUCTION_CACHE_BODY_SHA256_LITERAL or fs != PRODUCTION_CACHE_FILE_SHA256_LITERAL:
        raise AuditDomainError("artifact identities differ from the committed production identities")
    raw = open(record_path, "rb").read()
    qs = hashlib.sha256(raw).hexdigest()
    if qs != PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL:
        raise AuditDomainError("qualification record file identity differs from the committed identity")
    rec = json.loads(raw.decode("utf-8"))
    if not isinstance(rec, dict) or set(rec) != {k for k, _ in QUAL_SCHEMA}: raise AuditDomainError("qualification record keys differ from the exact schema")
    q = CacheQualification(**rec)                              # exact typing enforced at construction (1 for True is refused)
    if _canon(rec) != q.canonical() or raw.decode("utf-8") != q.canonical():
        raise AuditDomainError("qualification record is not canonical")
    if not (q.record_sha256() == qs == PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL):
        raise AuditDomainError("qualification object digest must equal the file digest and the committed literal")
    if (q.body_sha256, q.file_sha256) != (bd, fs):
        raise AuditDomainError("qualification record does not reproduce the artifact's identities")
    cache = ThresholdCache(by, "production_frozen", bd, fs, q, qs)
    if cache_semantic_identity(cache) != (bd, fs):
        raise AuditDomainError("mapping re-derivation does not reproduce the artifact identities")
    return cache


def cache_semantic_identity(cache) -> Tuple[str, str]:
    """RE-DERIVE the artifact identities from the immutable mapping itself (L2 r2 §5): rebuild the canonical
    body (frozen header + rows in canonical order, exact schema) and the canonical file text, and hash both.
    Carried strings are never trusted; only what the mapping recomputes to."""
    if type(cache) is not ThresholdCache: raise AuditDomainError("cache_semantic_identity requires an exact ThresholdCache")
    hdr = artifact_header()
    expected = {(m, s) for m in tuple(E1_LEVELS_MICRO) + tuple(hdr["pass2_levels"]) for s in E1_SEED_PANEL}
    if set(cache._by) != expected: raise AuditDomainError("cache mapping does not cover exactly the pass-1 and reachable pass-2 grid")
    rows = []
    for key in sorted(cache._by):
        st = cache._by[key]
        r = asdict(st); r["modes"] = list(st.modes)
        for k, typ in ROW_SCHEMA:
            if type(r[k]) is not typ: raise AuditDomainError(f"cache row field {k} has type {type(r[k]).__name__}")
        rows.append(r)
    body = dict(hdr); body["rows"] = rows
    bd = hashlib.sha256(_canon(body).encode()).hexdigest()
    fs = hashlib.sha256(_canon({"sha256": bd, "body": body}).encode()).hexdigest()
    return bd, fs


def is_production_cache(cache) -> bool:
    """Production status is DERIVED: exact type and role; a validated qualification whose record digest equals
    the committed literal; the mapping's RE-DERIVED body/file identities equal the source literals AND the
    qualification's; no pending literal."""
    try:
        if type(cache) is not ThresholdCache or cache.role != "production_frozen": return False
        if any("PENDING" in x for x in (PRODUCTION_CACHE_BODY_SHA256_LITERAL, PRODUCTION_CACHE_FILE_SHA256_LITERAL, PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)): return False
        q = cache.qualification; validate_cache_qualification(q)
        if not (q.record_sha256() == cache.qualification_sha256 == PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL): return False   # DERIVED from the object
        bd, fs = cache_semantic_identity(cache)
        return (bd == PRODUCTION_CACHE_BODY_SHA256_LITERAL == q.body_sha256 == cache.body_sha256
                and fs == PRODUCTION_CACHE_FILE_SHA256_LITERAL == q.file_sha256 == cache.file_sha256)
    except AuditDomainError:
        return False


def slice_cache(levels: Sequence[int]) -> ThresholdCache:
    """In-memory replay-built slice over given pass-1 levels (tests/smoke). Role `slice`."""
    verify_frozen_identity()
    by = {}
    for m in levels:
        for s in E1_SEED_PANEL:
            st, _ = _conditional_for(m, s); by[(m, s)] = st
    return ThresholdCache(by, "slice", "slice:" + _digest(tuple(sorted(by))))


# ----------------------------------------------------------------------------- regimes (validated)
_COND_CDF: Dict[Tuple[int, int], np.ndarray] = {}


def _validated_cdf(cdf: np.ndarray) -> np.ndarray:
    if not isinstance(cdf, np.ndarray) or cdf.dtype != np.float64 or cdf.ndim != 1 or cdf.shape[0] != N_CELLS + 1:
        raise AuditDomainError("conditional CDF must be a float64 vector of length N_CELLS + 1")
    if not np.isfinite(cdf).all() or (np.diff(cdf) < 0.0).any() or cdf[0] < 0.0 or abs(cdf[-1] - 1.0) > 1e-9:
        raise AuditDomainError("conditional CDF must be finite, nondecreasing, and normalised")
    out = cdf.copy(); out[-1] = 1.0                       # exact top cell: searchsorted can never exceed N_CELLS
    out.setflags(write=False)
    return out


def _conditional_null_cdf(level_micro: int, seed: int) -> np.ndarray:
    key = (_level(level_micro), _seed(seed))
    if key not in _COND_CDF:
        ch, v, u, r = _N._replay_initialization(*key)
        _COND_CDF[key] = _validated_cdf(np.cumsum(_N.per_tick_count_pmf(_N.conditional_p_act(v, u, r))[0]))
    return _COND_CDF[key]


def _series_from_counts(counts: np.ndarray) -> np.ndarray:
    if not isinstance(counts, np.ndarray) or counts.ndim != 1 or counts.shape[0] != TAIL_LEN or not np.issubdtype(counts.dtype, np.integer):
        raise AuditDomainError("counts must be an integer vector of TAIL_LEN")
    if (counts < 0).any() or (counts > N_CELLS).any():
        raise AuditDomainError("counts must lie in [0, N_CELLS]")
    rho = np.zeros(RUN_LEN, dtype=np.float64)
    rho[TAIL_START:] = counts.astype(np.float64) / np.float64(N_CELLS)
    return rho


def gen_null_run(level_micro: int, seed: int, g: np.random.Generator) -> np.ndarray:
    return _series_from_counts(np.searchsorted(_conditional_null_cdf(level_micro, seed), g.random(TAIL_LEN), side="left").astype(np.int64))


def gen_sustained_run(p_high, temporal, drift, amp, period, g: np.random.Generator) -> np.ndarray:
    _exact_float(p_high, "p_high", 0.0, 1.0); _exact_float(drift, "drift"); _exact_float(amp, "amp", 0.0); _exact_int(period, "period", 1)
    if temporal not in TEMPORAL_MODES: raise AuditDomainError(f"temporal must be one of {TEMPORAL_MODES}")
    t = np.arange(TAIL_LEN, dtype=np.float64)
    if temporal == "constant": p = np.full(TAIL_LEN, p_high)
    elif temporal == "drift":  p = p_high * (1.0 + drift * (t / TAIL_LEN - 0.5))
    else:                      p = p_high * (1.0 + amp * np.sin(2.0 * np.pi * t / period))
    return _series_from_counts(g.binomial(N_CELLS, np.clip(p, 0.0, 1.0)).astype(np.int64))


def gen_dip_run(p_high, g: np.random.Generator) -> np.ndarray:
    _exact_float(p_high, "p_high", 0.0, 1.0)
    counts = g.binomial(N_CELLS, p_high, size=TAIL_LEN).astype(np.int64)
    w = int(g.integers(DIP_WINDOWS[0], DIP_WINDOWS[1] + 1))
    counts[w * WINDOW:(w + 1) * WINDOW] = 0
    return _series_from_counts(counts)


# ----------------------------------------------------------------------------- generator: params, preflight, redraw
@dataclass(frozen=True)
class SweepParams:
    archetype: str
    onset_micro: int
    width_micro: int
    p_high: float
    temporal: str
    drift: float
    amp: float
    period: int
    pi: float
    second_onset_micro: int
    extra_level_index: int


def _width_kind(archetype: str) -> str:
    return dict(CLASS_WIDTH).get(archetype, "abrupt")


def _draw_once(archetype: str, g: np.random.Generator) -> SweepParams:
    """One parameter draw in the frozen PARAM_DRAW_ORDER."""
    u = lambda lo, hi: float(g.uniform(lo, hi))
    kind = _width_kind(archetype); w = {"gentle": GENTLE_WIDTH_MICRO, "abrupt": ABRUPT_WIDTH_MICRO, "wide": WIDE_WIDTH_MICRO}[kind]
    onset = int(g.integers(ONSET_RANGE_MICRO[0], ONSET_RANGE_MICRO[1] + 1))
    width = int(g.integers(w[0], w[1] + 1))
    p_high = u(*P_HIGH_RANGE)
    temporal = str(g.choice(["drift", "oscillation"])) if archetype in TEMPORAL_CLASSES else "constant"
    drift = u(*DRIFT_RANGE); amp = u(*OSC_AMP_RANGE); period = int(g.integers(OSC_PERIOD_RANGE[0], OSC_PERIOD_RANGE[1] + 1))
    pi = u(*MIXTURE_PI_RANGE)
    second = onset + int(g.integers(SECOND_ONSET_INCREMENT_MICRO[0], SECOND_ONSET_INCREMENT_MICRO[1]))
    extra = int(g.integers(EXTRA_LEVEL_INDEX_RANGE[0], EXTRA_LEVEL_INDEX_RANGE[1]))
    return SweepParams(archetype, onset, width, p_high, temporal, drift, amp, period, pi, second, extra)


def archetype_preflight(prm: SweepParams) -> Tuple[bool, str]:
    """Does this parameter object INSTANTIATE its named morphology inside the frozen sweep? (L2 A4: the four
    counterexamples are refused here.) Returns (ok, reason)."""
    L = E1_LEVELS_MICRO; a = prm.archetype
    lo, hi = prm.onset_micro - prm.width_micro // 2, prm.onset_micro + prm.width_micro // 2
    n_below = sum(1 for m in L if m < lo); n_above = sum(1 for m in L if m >= hi)
    if a in ("gentle_onset", "abrupt_onset", "persistent_nonstationary_high_m", "nonmonotone_amplitude", "wide_mixed_boundary", "unresolved_heavy_boundary",
             "off_band_mixture", "off_band_unresolved"):
        if n_below < 1 or n_above < 1: return False, "onset window leaves no confident level on one side"
    if a == "reentrant":
        if not any(m >= prm.second_onset_micro for m in L): return False, "second onset beyond the sweep: activity never returns to NULL"
        if not any(prm.onset_micro <= m < prm.second_onset_micro for m in L): return False, "no level inside the sustained region"
        if not any(m < prm.onset_micro for m in L): return False, "no NULL level below the onset"
    if a == "two_resolved_crossings":
        b, c = prm.onset_micro + TWO_CROSSING_OFFSETS_MICRO[0], prm.onset_micro + TWO_CROSSING_OFFSETS_MICRO[1]
        regions = (lambda m: m < prm.onset_micro, lambda m: prm.onset_micro <= m < b, lambda m: b <= m < c, lambda m: m >= c)
        if not all(any(f(m) for m in L) for f in regions):
            return False, "N-S-N-S requires at least one level in each of the four regions inside the sweep"
    if a == "off_band_mixture":
        extra = L[prm.extra_level_index]
        if not extra < lo: return False, "extra level is not below the band"
    if a == "off_band_unresolved":
        extras = L[prm.extra_level_index:prm.extra_level_index + 3]
        if len(extras) != 3 or not max(extras) < lo: return False, "the three extra levels are not all below the band"
    if a == "no_sustained_anywhere" or a == "no_null_consistent_anywhere":
        return True, "unconditional"
    return True, "ok"


def draw_params(archetype: str, master: int, class_index: int, sweep_index: int) -> Tuple[SweepParams, int]:
    """Deterministic redraw from a dedicated stream SeedSequence([master, class_index, sweep_index, attempt])
    until the frozen preflight passes, up to MAX_REDRAWS; exhaustion raises GeneratorHalt. Returns (params, attempts)."""
    if archetype not in CLASSES: raise AuditDomainError(f"unknown archetype {archetype!r}")
    for attempt in range(MAX_REDRAWS):
        g = np.random.default_rng(np.random.SeedSequence([int(master), int(class_index), int(sweep_index), attempt]))
        prm = _draw_once(archetype, g)
        ok, _ = archetype_preflight(prm)
        if ok: return prm, attempt + 1
    raise GeneratorHalt(f"{archetype}: preflight failed {MAX_REDRAWS} times for sweep {sweep_index}")


def regime_at(archetype: str, m_micro: int, prm: SweepParams, seed_u: float) -> Tuple[str, float]:
    L = E1_LEVELS_MICRO
    lo, hi = prm.onset_micro - prm.width_micro // 2, prm.onset_micro + prm.width_micro // 2
    frac = 0.0 if m_micro < lo else (1.0 if m_micro >= hi or hi == lo else (m_micro - lo) / (hi - lo))
    p_high = prm.p_high
    if archetype == "nonmonotone_amplitude":
        p_high = float(np.clip(prm.p_high * (1.0 - NONMONOTONE_ATTENUATION * max(0.0, (m_micro - prm.onset_micro) / NONMONOTONE_SCALE_MICRO)), P_HIGH_RANGE[0], 1.0))
    if archetype in ("gentle_onset", "abrupt_onset", "persistent_nonstationary_high_m", "nonmonotone_amplitude", "wide_mixed_boundary"):
        return ("SUSTAINED" if seed_u < frac else "NULL"), p_high
    if archetype == "no_sustained_anywhere": return "NULL", p_high
    if archetype == "no_null_consistent_anywhere": return "SUSTAINED", p_high
    if archetype == "two_resolved_crossings":
        b, c = prm.onset_micro + TWO_CROSSING_OFFSETS_MICRO[0], prm.onset_micro + TWO_CROSSING_OFFSETS_MICRO[1]
        return ("SUSTAINED" if (prm.onset_micro <= m_micro < b) or m_micro >= c else "NULL"), p_high
    if archetype == "reentrant":
        return ("SUSTAINED" if prm.onset_micro <= m_micro < prm.second_onset_micro else "NULL"), p_high
    if archetype == "off_band_mixture":
        if m_micro == L[prm.extra_level_index]: return ("SUSTAINED" if seed_u < prm.pi else "NULL"), p_high
        return ("SUSTAINED" if seed_u < frac else "NULL"), p_high
    if archetype == "off_band_unresolved":
        if m_micro in L[prm.extra_level_index:prm.extra_level_index + 3]: return "DIP", p_high
        return ("SUSTAINED" if seed_u < frac else "NULL"), p_high
    if archetype == "unresolved_heavy_boundary":
        if lo <= m_micro < hi: return "DIP", p_high
        return ("SUSTAINED" if m_micro >= hi else "NULL"), p_high
    raise AuditDomainError(f"unknown archetype {archetype!r}")


# ----------------------------------------------------------------------------- one sweep (complete record)
@dataclass(frozen=True)
class SweepResult:
    archetype: str
    sweep_index: int
    params: SweepParams
    preflight_attempts: int
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
    final_verdict: str
    final_cause: Optional[str]
    final_rule: str
    cache_role: str
    cache_body_sha256: str
    declaration_sha256: str
    generator_sha256: str
    evaluability_halt: Optional[str] = None
    generator_halt: Optional[str] = None


def _label_at(archetype: str, m: int, prm: SweepParams, seed_us: np.ndarray, cache: ThresholdCache, g: np.random.Generator, production: bool) -> str:
    statuses = []
    for s_idx, seed in enumerate(E1_SEED_PANEL):
        try:
            th = cache.get(m, seed)
        except AuditDomainError:
            if production:
                raise AuditDomainError(f"production cache lacks reachable key level {level_id(m)} seed {seed}: apparatus defect, audit halts")
            th = _slice_inserted(m, seed)                      # slice/smoke only: derive on demand, never in production
        regime, p_high = regime_at(archetype, m, prm, float(seed_us[s_idx]))
        if regime == "NULL": rho = gen_null_run(m, seed, g)
        elif regime == "SUSTAINED": rho = gen_sustained_run(p_high, prm.temporal, prm.drift, prm.amp, prm.period, g)
        else: rho = gen_dip_run(p_high, g)
        statuses.append(run_status(rho, th.theta_p, th.theta_t)[0])
    return level_label(level_counts(statuses))


_SLICE_INSERTED: Dict[Tuple[int, int], SeedThreshold] = {}


def _slice_inserted(m: int, seed: int) -> SeedThreshold:
    key = (m, seed)
    if key not in _SLICE_INSERTED:
        try: _SLICE_INSERTED[key] = _conditional_for(m, seed)[0]
        except _N.NullDomainError as e:
            if "not numerically certified" in str(e) or "no support point" in str(e): raise ThresholdUncertifiable(m, seed, str(e))
            raise
    return _SLICE_INSERTED[key]


def run_sweep(archetype: str, sweep_index: int, master: int, cache: ThresholdCache) -> SweepResult:
    if not isinstance(cache, ThresholdCache): raise AuditDomainError("cache must be a ThresholdCache")
    production = cache.role == "production_frozen"
    ci = CLASSES.index(archetype) if archetype in CLASSES else None
    if ci is None: raise AuditDomainError(f"unknown archetype {archetype!r}")
    _exact_int(sweep_index, "sweep_index", 0); _exact_int(master, "master", 1)
    ident = dict(cache_role=cache.role, cache_body_sha256=cache.body_sha256, declaration_sha256=AUDIT_DECLARATION_SHA256_LITERAL, generator_sha256=GENERATOR_DECLARATION_SHA256_LITERAL)
    try:
        prm, attempts = draw_params(archetype, master, ci, sweep_index)
    except GeneratorHalt as e:
        empty = SweepParams(archetype, 0, 0, 0.0, "constant", 0.0, 0.0, 1, 0.0, 0, 0)
        return SweepResult(archetype, sweep_index, empty, MAX_REDRAWS, (), "", None, "", 0, 0, (), (), (), (), (), "GENERATOR_HALT", None, "", **ident, generator_halt=str(e))
    ok, why = archetype_preflight(prm)
    if not ok: raise AuditDomainError(f"preflight re-assertion failed after draw: {why}")       # cannot happen; asserted anyway (L2 A4)
    g = np.random.default_rng(np.random.SeedSequence([int(master), ci, int(sweep_index)]))
    seed_us = g.random(N_SEEDS)                                # common per-seed regime-assignment uniforms
    try:
        lab1 = tuple(_label_at(archetype, m, prm, seed_us, cache, g, production) for m in E1_LEVELS_MICRO)
        v1 = evaluate(lab1, E1_LEVELS_MICRO); d = route(lab1, E1_LEVELS_MICRO)
        nominal = _V.P2R_SINGLE_BAND_INSERTIONS if d.row in ("P2R-5", "P2R-6") else (2 * _V.P2R_PER_INTERVAL_INSERTIONS if d.row == "P2R-4" else 0)
        router = dict(router_row=d.row, nominal_insertions=nominal, realized_insertions=len(d.insertions_micro), insertions_micro=tuple(d.insertions_micro),
                      fallback_moves=tuple(d.fallback_moves), fallback_drops=tuple(d.fallback_drops))
        if d.insertions_micro:
            lab2 = tuple(_label_at(archetype, m, prm, seed_us, cache, g, production) for m in d.insertions_micro)
            merged = sorted(list(zip(E1_LEVELS_MICRO, lab1)) + list(zip(d.insertions_micro, lab2)))
            levels_f = tuple(m for m, _ in merged); lab_f = tuple(l for _, l in merged)
        else:
            levels_f, lab_f = tuple(E1_LEVELS_MICRO), lab1
        vf = evaluate(lab_f, levels_f)
    except ThresholdUncertifiable as e:
        r = locals().get("router") or dict(router_row="", nominal_insertions=0, realized_insertions=0, insertions_micro=(), fallback_moves=(), fallback_drops=())
        return SweepResult(archetype, sweep_index, prm, attempts, locals().get("lab1", ()), getattr(locals().get("v1"), "verdict", ""), getattr(locals().get("v1"), "cause", None),
                           r["router_row"], r["nominal_insertions"], r["realized_insertions"], r["insertions_micro"], r["fallback_moves"], r["fallback_drops"],
                           (), (), "HALTED", None, "", **ident, evaluability_halt=f"uncertified_threshold@{level_id(e.level_micro)}#seed{e.seed}")
    return SweepResult(archetype, sweep_index, prm, attempts, lab1, v1.verdict, v1.cause, **router, final_levels_micro=levels_f, final_labels=lab_f,
                       final_verdict=vf.verdict, final_cause=vf.cause, final_rule=vf.rule, **ident)


# ----------------------------------------------------------------------------- scoring, completion, qualification
@dataclass(frozen=True)
class ClassScore:
    archetype: str
    intended_verdict: str
    intended_cause: Optional[str]
    attempted: int
    scored: int
    halted: int
    generator_halted: int
    applicable_error: str
    errors: int
    cp_upper_95: float              # DESCRIPTIVE when halted > 0
    statistical_cap_pass: bool      # cap on scored sweeps only — descriptive when halts occur
    complete_pass: bool             # attempted == scored == 500, halted == 0, generator_halted == 0, cap clears
    exact_agreement_descriptive: float   # verdict AND cause equal the intended map — DESCRIPTIVE ONLY, never enters a pass; derived from the count
    exact_agreement_count: int
    verdict_counts: Tuple[Tuple[str, int], ...]
    yield_distribution: Tuple[Tuple[int, int], ...]
    halt_keys: Tuple[str, ...]


def score_class(results: Sequence[SweepResult], requested: int) -> ClassScore:
    a = results[0].archetype; iv, ic = INTENDED[a]
    ghalt = [r for r in results if r.generator_halt]; ehalt = [r for r in results if r.evaluability_halt]
    scored = [r for r in results if not r.generator_halt and not r.evaluability_halt]
    kind = "false_nd" if a in SCIENTIFIC_CLASSES else "false_scientific"
    n = len(scored)
    if n == 0:
        return ClassScore(a, iv, ic, len(results), 0, len(ehalt), len(ghalt), kind, 0, 1.0, False, False, 0.0, 0, (), (), tuple(sorted({str(r.evaluability_halt) for r in ehalt})))
    errors = sum(1 for r in scored if r.final_verdict == "NOT_DISTINGUISHED") if kind == "false_nd" else sum(1 for r in scored if r.final_verdict in ("LOCATED", "NOT_PRODUCED"))
    ub = clopper_pearson_upper(errors, n); cap_ok = ub <= CAP
    complete = (len(results) == requested == SWEEPS_PER_CLASS) and n == SWEEPS_PER_CLASS and not ehalt and not ghalt and cap_ok
    vc: Dict[str, int] = {}; yd: Dict[int, int] = {}
    for r in scored:
        vc[r.final_verdict] = vc.get(r.final_verdict, 0) + 1
        if r.router_row in ("P2R-5", "P2R-6", "P2R-4"): yd[r.realized_insertions] = yd.get(r.realized_insertions, 0) + 1
    agree_n = sum(1 for r in scored if r.final_verdict == iv and r.final_cause == ic)
    return ClassScore(a, iv, ic, len(results), n, len(ehalt), len(ghalt), kind, errors, ub, cap_ok, complete, agree_n / n, agree_n,
                      tuple(sorted(vc.items())), tuple(sorted(yd.items())), tuple(sorted({str(r.evaluability_halt) for r in ehalt})))


def validate_class_score(s, requested: int) -> None:
    """Re-derive every semantic field of a ClassScore from its carried counts (L2 r2 §4.2): intended verdict/cause
    from the frozen map, applicable-error family from the partition, errors from the verdict counts, the CP bound
    from (errors, scored), cap pass, completion. Refuse any mismatch or type hole."""
    if type(s) is not ClassScore: raise AuditDomainError("validate_class_score requires an exact ClassScore")
    if s.archetype not in INTENDED: raise AuditDomainError(f"unknown archetype {s.archetype!r}")
    iv, ic = INTENDED[s.archetype]
    if (s.intended_verdict, s.intended_cause) != (iv, ic): raise AuditDomainError("intended verdict/cause differ from the frozen map")
    for k in ("attempted", "scored", "halted", "generator_halted", "errors"):
        v = getattr(s, k)
        if type(v) is not int or v < 0: raise AuditDomainError(f"ClassScore.{k} must be a non-negative exact int")
    for k in ("statistical_cap_pass", "complete_pass"):
        if type(getattr(s, k)) is not bool: raise AuditDomainError(f"ClassScore.{k} must be an exact bool")
    if s.scored + s.halted + s.generator_halted != s.attempted: raise AuditDomainError("scored + halted + generator_halted must equal attempted")
    kind = "false_nd" if s.archetype in SCIENTIFIC_CLASSES else "false_scientific"
    if s.applicable_error != kind: raise AuditDomainError("applicable error differs from the class partition")
    # verdict_counts: exact tuple of exact 2-tuples; keys in M4's frozen VERDICTS; unique (checked BEFORE any dict
    # conversion); canonically ordered; positive exact non-Boolean ints; summing to scored; empty iff scored == 0 (R3-C1)
    vcs = s.verdict_counts
    if type(vcs) is not tuple or any(type(e) is not tuple or len(e) != 2 for e in vcs):
        raise AuditDomainError("verdict_counts must be an exact tuple of exact 2-tuples")
    keys = [e[0] for e in vcs]
    if any(type(k) is not str or k not in _V.VERDICTS for k in keys): raise AuditDomainError("verdict_counts keys must be M4 verdicts")
    if len(set(keys)) != len(keys): raise AuditDomainError("verdict_counts keys must be unique")
    if keys != sorted(keys): raise AuditDomainError("verdict_counts must be canonically ordered")
    if any(type(v) is not int or isinstance(v, bool) or v <= 0 for _, v in vcs): raise AuditDomainError("verdict_counts values must be positive exact ints")
    if sum(v for _, v in vcs) != s.scored: raise AuditDomainError("verdict_counts must sum to scored")
    if s.scored == 0 and vcs != (): raise AuditDomainError("unscored class must carry empty verdict_counts")
    vc = dict(vcs)
    errs = vc.get("NOT_DISTINGUISHED", 0) if kind == "false_nd" else vc.get("LOCATED", 0) + vc.get("NOT_PRODUCED", 0)
    if s.errors != errs: raise AuditDomainError("errors differ from the verdict counts")
    # descriptive aggregates re-derived (3.3): exact-agreement COUNT carried, ratio derived; yield keys/counts; halt keys
    if type(s.exact_agreement_count) is not int or isinstance(s.exact_agreement_count, bool) or not 0 <= s.exact_agreement_count <= s.scored:
        raise AuditDomainError("exact_agreement_count must be an exact int in [0, scored]")
    if s.exact_agreement_count > vc.get(iv, 0): raise AuditDomainError("exact agreement cannot exceed the intended-verdict count")
    expected_ratio = (s.exact_agreement_count / s.scored) if s.scored else 0.0
    if s.exact_agreement_descriptive != expected_ratio: raise AuditDomainError("exact_agreement_descriptive must derive from the count")
    yd = s.yield_distribution
    if type(yd) is not tuple or any(type(e) is not tuple or len(e) != 2 for e in yd): raise AuditDomainError("yield_distribution must be an exact tuple of 2-tuples")
    ykeys = [e[0] for e in yd]
    if any(type(k) is not int or isinstance(k, bool) or k < 0 for k in ykeys) or len(set(ykeys)) != len(ykeys) or ykeys != sorted(ykeys):
        raise AuditDomainError("yield keys must be unique canonically ordered non-negative exact ints")
    if any(type(v) is not int or isinstance(v, bool) or v <= 0 for _, v in yd) or sum(v for _, v in yd) > s.scored:
        raise AuditDomainError("yield counts must be positive exact ints totalling at most scored")
    hk = s.halt_keys
    if type(hk) is not tuple or any(type(k) is not str or not k.startswith("uncertified_threshold@") for k in hk) or list(hk) != sorted(set(hk)):
        raise AuditDomainError("halt_keys must be a canonical tuple of unique uncertified_threshold@ strings")
    if (s.halted == 0) != (hk == ()): raise AuditDomainError("halt_keys must be empty iff halted == 0")
    if s.scored == 0:
        if (s.cp_upper_95, s.statistical_cap_pass, s.complete_pass) != (1.0, False, False): raise AuditDomainError("unscored class must carry cp 1.0 and no passes")
    else:
        if s.cp_upper_95 != clopper_pearson_upper(s.errors, s.scored): raise AuditDomainError("cp_upper_95 differs from the recomputed bound")
        if s.statistical_cap_pass is not (s.cp_upper_95 <= CAP): raise AuditDomainError("statistical_cap_pass differs from the recomputed cap test")
        comp = (s.attempted == requested == SWEEPS_PER_CLASS) and s.scored == SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 and s.statistical_cap_pass
        if s.complete_pass is not comp: raise AuditDomainError("complete_pass differs from the recomputed completion rule")
        if not (isinstance(s.exact_agreement_descriptive, float) and 0.0 <= s.exact_agreement_descriptive <= 1.0): raise AuditDomainError("exact agreement out of range")


@dataclass(frozen=True)
class AuditRecord:
    version: str
    ensemble: str
    master: int
    requested_sweeps_per_class: int
    cache_role: str
    cache_body_sha256: str
    cache_file_sha256: str
    cache_qualification_sha256: str
    audit_declaration_sha256: str
    generator_declaration_sha256: str
    scores: Tuple[ClassScore, ...]
    ensemble_pass: bool             # every class complete_pass on a derived production cache — NOT a freeze pass
    record_sha256: str

    def identity_body(self):
        return (self.version, self.ensemble, self.master, self.requested_sweeps_per_class, self.cache_role, self.cache_body_sha256,
                self.cache_file_sha256, self.cache_qualification_sha256, self.audit_declaration_sha256, self.generator_declaration_sha256,
                tuple(asdict(s) for s in self.scores), self.ensemble_pass)

    def summary(self) -> str:
        return " | ".join(f"{s.archetype}:{s.applicable_error}={s.errors}/{s.scored} ub={s.cp_upper_95:.3f} {'C' if s.complete_pass else '-'}" for s in self.scores) \
               + f" => ensemble_pass={self.ensemble_pass}"


def validate_audit_record(rec, expect_production: bool = True) -> None:
    """The complete record validator (L2 r2 §4): exact type; M6 frozen identity re-run; current declaration
    identities; the source-literal production-cache identity bundle (when expect_production); every ClassScore
    semantically re-derived; ensemble_pass recomputed; record identity recomputed."""
    if type(rec) is not AuditRecord: raise AuditDomainError("validate_audit_record requires an exact AuditRecord")
    verify_frozen_identity()
    if rec.version != AUDIT_VERSION: raise AuditDomainError("record version differs from the audit version")
    if rec.ensemble not in ("design", "held_out") or rec.master != (AUDIT_MASTER if rec.ensemble == "design" else HELD_OUT_MASTER):
        raise AuditDomainError("record ensemble/master differ from the frozen masters")
    if (rec.audit_declaration_sha256, rec.generator_declaration_sha256) != (AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL):
        raise AuditDomainError("record declaration identities differ from the current M6 declarations")
    if type(rec.requested_sweeps_per_class) is not int or rec.requested_sweeps_per_class < 1 or type(rec.ensemble_pass) is not bool:
        raise AuditDomainError("record count/flag types")
    if rec.cache_role not in CACHE_ROLES: raise AuditDomainError("record cache role unknown")
    if expect_production:
        if rec.cache_role != "production_frozen" or (rec.cache_body_sha256, rec.cache_file_sha256, rec.cache_qualification_sha256) != \
           (PRODUCTION_CACHE_BODY_SHA256_LITERAL, PRODUCTION_CACHE_FILE_SHA256_LITERAL, PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL):
            raise AuditDomainError("record cache identity bundle differs from the source-literal production identities")
    if tuple(s.archetype for s in rec.scores) != CLASSES: raise AuditDomainError("record class set/order differs from the frozen classes")
    for s in rec.scores: validate_class_score(s, rec.requested_sweeps_per_class)
    ens = all(s.complete_pass for s in rec.scores) and rec.cache_role == "production_frozen" and expect_production
    if rec.ensemble_pass is not ens: raise AuditDomainError("ensemble_pass differs from the recomputed value")
    if rec.record_sha256 != _digest(rec.identity_body()): raise AuditDomainError("record identity does not recompute")


def run_audit(ensemble: str, cache: ThresholdCache, sweeps_per_class: Optional[int] = None) -> AuditRecord:
    verify_frozen_identity()
    if ensemble not in ("design", "held_out"): raise AuditDomainError("ensemble must be 'design' or 'held_out'")
    if type(cache) is not ThresholdCache: raise AuditDomainError("cache must be a ThresholdCache")
    n = SWEEPS_PER_CLASS if sweeps_per_class is None else _exact_int(sweeps_per_class, "sweeps_per_class", 1)
    prod = is_production_cache(cache)
    if n == SWEEPS_PER_CLASS and not prod:
        raise AuditDomainError("a 500-sweep audit requires the production_frozen cache (identities re-derived, not the role label)")
    master = AUDIT_MASTER if ensemble == "design" else HELD_OUT_MASTER
    scores = tuple(score_class([run_sweep(name, i, master, cache) for i in range(n)], n) for name in CLASSES)
    ens = all(s.complete_pass for s in scores) and prod
    fields = (AUDIT_VERSION, ensemble, master, n, cache.role, cache.body_sha256, cache.file_sha256 or "", cache.qualification_sha256 or "",
              AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL, scores, ens)
    probe = AuditRecord(*fields, "")
    return AuditRecord(*fields, _digest(probe.identity_body()))


@dataclass(frozen=True)
class AuditQualification:
    design_record_sha256: str
    held_out_record_sha256: str
    cache_body_sha256: str
    cache_file_sha256: str
    cache_qualification_sha256: str
    audit_declaration_sha256: str
    generator_declaration_sha256: str
    qualified: bool
    reasons: Tuple[str, ...]
    qualification_sha256: str = ""

    def identity_body(self):
        return (self.design_record_sha256, self.held_out_record_sha256, self.cache_body_sha256, self.cache_file_sha256, self.cache_qualification_sha256,
                self.audit_declaration_sha256, self.generator_declaration_sha256, self.qualified, self.reasons)


def _qualification_reasons(design, held_out) -> List[str]:
    """The complete reasons tuple, in the one frozen order used by qualify_audit and its validator."""
    reasons: List[str] = []
    for rec, name in ((design, "design"), (held_out, "held_out")):
        try: validate_audit_record(rec, expect_production=True)
        except AuditDomainError as e: reasons.append(f"{name}: invalid record — {e}")
    for rec, name, master in ((design, "design", AUDIT_MASTER), (held_out, "held_out", HELD_OUT_MASTER)):
        if type(rec) is not AuditRecord: reasons.append(f"{name}: not an AuditRecord"); continue
        if rec.ensemble != name: reasons.append(f"{name}: wrong ensemble label")
        if rec.master != master: reasons.append(f"{name}: wrong master")
        if rec.requested_sweeps_per_class != SWEEPS_PER_CLASS: reasons.append(f"{name}: not 500 requested")
        if rec.cache_role != "production_frozen": reasons.append(f"{name}: cache not production_frozen")
        if tuple(s.archetype for s in rec.scores) != CLASSES: reasons.append(f"{name}: class set differs")
        for s in rec.scores:
            if not (s.attempted == s.scored == SWEEPS_PER_CLASS and s.halted == 0 and s.generator_halted == 0 and s.statistical_cap_pass and s.complete_pass):
                reasons.append(f"{name}:{s.archetype}: not complete")
        if not rec.ensemble_pass: reasons.append(f"{name}: ensemble_pass False")
    if type(design) is AuditRecord and type(held_out) is AuditRecord:
        if design.master == held_out.master: reasons.append("masters not distinct")
        if design.cache_body_sha256 != held_out.cache_body_sha256: reasons.append("cache identities differ")
        if design.record_sha256 == held_out.record_sha256: reasons.append("record identities not distinct")
    return reasons


def validate_audit_qualification(q, design, held_out) -> None:
    """THE FREEZE-QUALIFYING OBJECT'S VALIDATOR (L2 r3 §5): exact type; both records validated; the complete reasons
    tuple recomputed in the frozen order; the two record identities and the source-literal cache/declaration bundle;
    qualified is (not reasons); every hash field 64-hex; qualification_sha256 recomputed. Refuses every mismatch."""
    if type(q) is not AuditQualification: raise AuditDomainError("validate_audit_qualification requires an exact AuditQualification")
    reasons = tuple(_qualification_reasons(design, held_out))
    if type(q.reasons) is not tuple or any(type(r) is not str for r in q.reasons) or q.reasons != reasons:
        raise AuditDomainError("qualification reasons differ from the recomputed reasons")
    if type(q.qualified) is not bool or q.qualified is not (not reasons): raise AuditDomainError("qualified must equal (reasons == ())")
    d_id = design.record_sha256 if type(design) is AuditRecord else ""; h_id = held_out.record_sha256 if type(held_out) is AuditRecord else ""
    if (q.design_record_sha256, q.held_out_record_sha256) != (d_id, h_id): raise AuditDomainError("qualification record identities differ from the records")
    bundle = (PRODUCTION_CACHE_BODY_SHA256_LITERAL, PRODUCTION_CACHE_FILE_SHA256_LITERAL, PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)
    if (q.cache_body_sha256, q.cache_file_sha256, q.cache_qualification_sha256) != bundle: raise AuditDomainError("qualification cache bundle differs from the source literals")
    if (q.audit_declaration_sha256, q.generator_declaration_sha256) != (AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL):
        raise AuditDomainError("qualification declaration identities differ from the current declarations")
    for k in ("cache_body_sha256", "cache_file_sha256", "cache_qualification_sha256", "audit_declaration_sha256", "generator_declaration_sha256", "qualification_sha256"):
        if not _is_hex64(getattr(q, k)): raise AuditDomainError(f"qualification field {k} is not a 64-hex sha256")
    if q.qualified and not (_is_hex64(q.design_record_sha256) and _is_hex64(q.held_out_record_sha256)): raise AuditDomainError("a qualified object must carry two 64-hex record identities")
    if q.qualification_sha256 != _digest(q.identity_body()): raise AuditDomainError("qualification identity does not recompute")


def qualify_audit(design, held_out) -> AuditQualification:
    """THE FREEZE-QUALIFYING ACT for the audit (L2 A2, r2 §4, r3 §5): both records VALIDATED before being joined; the
    reasons computed by the one frozen procedure; the returned object validated against both records before return."""
    reasons = tuple(_qualification_reasons(design, held_out))
    bundle = (PRODUCTION_CACHE_BODY_SHA256_LITERAL, PRODUCTION_CACHE_FILE_SHA256_LITERAL, PRODUCTION_CACHE_QUALIFICATION_SHA256_LITERAL)
    fields = (design.record_sha256 if type(design) is AuditRecord else "", held_out.record_sha256 if type(held_out) is AuditRecord else "",
              *bundle, AUDIT_DECLARATION_SHA256_LITERAL, GENERATOR_DECLARATION_SHA256_LITERAL, not reasons, reasons)
    q = AuditQualification(*fields); q = AuditQualification(*fields, _digest(q.identity_body()))
    validate_audit_qualification(q, design, held_out)
    return q


# ----------------------------------------------------------------------------- pricing (per-seed bounds; pooled descriptive)
@dataclass(frozen=True)
class PricingRecord:
    replicates_per_seed: int
    levels: Tuple[str, ...]
    per_seed_exceed_reference: Tuple[Tuple[str, Tuple[int, ...]], ...]      # per level: 20 per-seed counts vs the one-template reference
    per_seed_exceed_conditional: Tuple[Tuple[str, Tuple[int, ...]], ...]    # per level: 20 per-seed counts vs each seed's own conditional
    worst_seed_cp_upper_reference: float      # exact CP: max over seeds of CP(k_seed, replicates)
    worst_seed_cp_upper_conditional: float
    pooled_rate_reference_descriptive: float  # pooled counts / (20 x replicates) — DESCRIPTIVE ONLY (Poisson-binomial design)
    pooled_rate_conditional_descriptive: float

    def summary(self) -> str:
        return (f"PRICING {self.replicates_per_seed}/seed: worst-seed CP-95 upper θ_T exceedance — one-template reference {self.worst_seed_cp_upper_reference:.4f} "
                f"vs conditional per-seed {self.worst_seed_cp_upper_conditional:.4f} | pooled rates (descriptive) {self.pooled_rate_reference_descriptive:.4f} / {self.pooled_rate_conditional_descriptive:.4f}")


def run_pricing(levels: Optional[Sequence[int]] = None, replicates: int = PRICING_REPLICATES) -> PricingRecord:
    verify_frozen_identity()
    reps = _exact_int(replicates, "replicates", 1)
    lv = tuple(E1_LEVELS_MICRO) if levels is None else tuple(_level(x) for x in levels)
    if not lv: raise AuditDomainError("levels must be nonempty")
    if len(set(lv)) != len(lv): raise AuditDomainError("levels must be unique")
    per_r: List[Tuple[str, Tuple[int, ...]]] = []; per_c: List[Tuple[str, Tuple[int, ...]]] = []
    worst_r = worst_c = 0.0; pool_r = pool_c = 0
    for m in lv:
        ref = _N.reference_thresholds(m); kr: List[int] = []; kc: List[int] = []
        for seed in E1_SEED_PANEL:
            ch, v, u, r = _N._replay_initialization(m, seed)
            cond = _N.conditional_thresholds(m, seed, v, u, r)
            cdf = _validated_cdf(np.cumsum(_N.per_tick_count_pmf(_N.conditional_p_act(v, u, r))[0]))
            g = np.random.default_rng(np.random.SeedSequence([PRICING_MASTER, int(m), int(seed)]))
            cr = cc = 0
            for _ in range(reps):
                st = _K.tail_stats(_series_from_counts(np.searchsorted(cdf, g.random(TAIL_LEN), side="left").astype(np.int64)))
                cr += st.s_term > ref.theta_t; cc += st.s_term > cond.theta_t
            kr.append(cr); kc.append(cc)
            worst_r = max(worst_r, clopper_pearson_upper(cr, reps)); worst_c = max(worst_c, clopper_pearson_upper(cc, reps))
        per_r.append((level_id(m), tuple(kr))); per_c.append((level_id(m), tuple(kc))); pool_r += sum(kr); pool_c += sum(kc)
    tot = N_SEEDS * reps * len(lv)
    return PricingRecord(reps, tuple(level_id(m) for m in lv), tuple(per_r), tuple(per_c), worst_r, worst_c, pool_r / tot, pool_c / tot)
