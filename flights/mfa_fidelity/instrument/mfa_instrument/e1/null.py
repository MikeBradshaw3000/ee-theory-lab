"""mfa_instrument/e1/null.py — E1 stage-1 module M3: the null object (Contract E1 §4.2 v0.3, v0.4
§4.2 amendments, v0.5 B, v0.6 B, v0.7 A; design note §2 M3; L2 first-review repairs M3-1..M3-7).

THE NULL OBJECT (a no-interaction reference, named only as that): per level m, the frozen common
rank template gives 2500 base triples (v, u_base, r) = (m − w/2) + w·rank; Λ_i = v·u_base·r
(F_canonical); the per-cell no-neighbour chain is p_base_i = σ(α·Λ_i − γ_offset), p_act_i =
p_base_i + η_floor·(1 − p_base_i), zero density terms. Under the frozen symmetric rule the next
state is `draw < p_act` for EVERY cell regardless of its current state (dynamics.py Step 6 — see
memorylessness_witness), so with neighbours zeroed each null cell is Bernoulli(p_act_i)
INDEPENDENTLY ACROSS TICKS and the tail statistics have EXACT laws:

  per-tick count K ~ PoissonBinomial(p_1..p_2500)                          (i.i.d. across ticks)
  window count W_100 = Σ_{100 ticks} K ;  window mean = W_100 / 250000
  terminal count W_300 ;  S_term = W_300 / 750000
  S_min = min of 10 i.i.d. window means (disjoint tick sets):  F_min(x) = 1 − (1 − F_W(x))^10

TWO THINGS, KEPT SEPARATE (L2 M3-3): the LAW is exact; its EVALUATION here is float64 — a per-tick
pmf by characteristic-function DFT and reps-fold convolution by FFT power. Every pmf carries a
NUMERICAL CERTIFICATE (max imaginary residual, total negative mass, most negative coefficient, raw
normalisation error, clip/renormalisation correction) and every threshold carries the CDF on both
sides of its quantile crossing; a quantile is CERTIFIED only when both crossing margins exceed a
conservative numerical error bound whose conservativeness is validated against an independent
direct-convolution path at the declared validation levels. `sampling_ci_half_width = 0.0` records
that no Monte Carlo error exists; the certificates record what float64 evaluation cost.

Thresholds: θ_P, θ_T = inf{x : F(x) ≥ 0.99} on the exact count grid — the same grid M2 computes
production statistics on (integer counts recovered from rho; one sum; one division).

AMENDMENT OF RECORD (2026-09-21; Mike's authorization on L2's M6 rulings, Findings 1 and 2):
  PRIMARY SCORING OBJECT = the CONDITIONAL PER-SEED NULL. A production run's initialized bases
  (v, u_base, r) are known exactly; its own no-neighbour p_act_i follow from them under the frozen
  rule; its own θ_P/θ_T are certified by the same law. `conditional_thresholds` builds that object,
  bound to the bases' identity and the seed. The frozen common-rank template survives ONLY as a
  reference/stability object, an alternative-null sensitivity axis, and the numerical-validation
  template (`reference_thresholds`) — it is NOT a production scoring threshold: the one-template
  threshold prices only within-realization variation, and at high m between-base-draw variation of
  the mean null activity exceeds it (M6 pricing, L2 ruling).
  CONSERVATIVE CERTIFIED COVERAGE THRESHOLD. When the ordinary crossing k* = min{k : F̂(k) ≥ q}
  cannot be certified (its margins lie inside the certified final-CDF error bound ε), the object is
  k_safe = min{k : F̂(k) − ε ≥ q}, which guarantees the TRUE CDF at the selected grid point is ≥ q.
  It is recorded with its ordinary index, uncertifiable status, displacement, and mode — it is not
  called the exact quantile. If no support point clears the condition, the call halts.
  The one-grid-step displacement observed on scanned levels is reported, never asserted globally.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import asdict, dataclass
from itertools import product
from typing import Dict, Optional, Sequence, Tuple

import numpy as np

from ..config import DynamicsConstants, MICRO_UNITS
from . import classify as _K
from . import config as _C
from .classify import WINDOW, N_WINDOWS, TERMINAL_WINDOWS, tail_stats
from .config import E1_BASE_WIDTH_MICRO, E1_GRID, E1_CONSTANTS_EXPECTED, level_id

N_CELLS = E1_GRID * E1_GRID                  # 2500
NULL_QUANTILE = 0.99                         # [PROPOSED] design choice, named as such
TERM_TICKS = len(TERMINAL_WINDOWS) * WINDOW  # 300


class NullDomainError(ValueError):
    """Input outside the null object's executable domain, or a frozen identity violated."""


# ----------------------------------------------------------------------------- frozen declaration
NULL_TEMPLATE_MASTER = 202609171                 # dedicated null-generation seed material (declared)
NULL_TEMPLATE_ROLE = 0xE10000
NULL_TEMPLATE_SHA256_LITERAL = "a7411439c549776f26f4dc293d93c82b4c6feb488c06676007c71c960df15efc"   # established 2026-09-17
NULL_ERROR_BOUND_FACTOR = 1000.0                 # conservative multiplier on measured float64 residual indicators
NULL_ERROR_BOUND_FLOOR = 1e-9                    # never certify a crossing closer than this to the quantile
SCORING_OBJECT_VERSION = "e1_conditional_null_v1"   # participates in the composite scoring identity; frozen in the declaration
THRESHOLD_MODES_SET = ("exact_certified", "conservative_coverage")

NULL_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("n_cells", N_CELLS), ("grid", E1_GRID), ("base_width_micro", E1_BASE_WIDTH_MICRO), ("f_dispatch", "F_canonical"),
    ("constants", E1_CONSTANTS_EXPECTED), ("density_terms", "zero"), ("quantile", NULL_QUANTILE),
    ("window", WINDOW), ("n_windows", N_WINDOWS), ("terminal_windows", TERMINAL_WINDOWS), ("term_ticks", TERM_TICKS),
    ("template_master", NULL_TEMPLATE_MASTER), ("template_rng_role", NULL_TEMPLATE_ROLE), ("template_sha256", NULL_TEMPLATE_SHA256_LITERAL),
    ("law", "exact_poisson_binomial"), ("evaluation", "float64_fft"),
    ("error_bound_factor", NULL_ERROR_BOUND_FACTOR), ("error_bound_floor", NULL_ERROR_BOUND_FLOOR),
    ("primary_scoring_object", "conditional_per_seed"), ("reference_template_use", "reference/sensitivity/validation only"),
    ("quantile_modes", ("exact_certified", "conservative_coverage")), ("conservative_rule", "k_safe = min{k : F_hat(k) - eps >= q}"),
    ("scoring_object_version", SCORING_OBJECT_VERSION), ("payload_identity", "sha256 of the canonical complete threshold payload, excluding the digest itself"),
)
NULL_DECLARATION_SHA256_LITERAL = "5304efb26ad4d15103e859a2ffb58af3ac3f57c7447052aca270e3ec36aa52d0"   # established 2026-09-21 (reopening round 3: scoring version + payload identity)


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def _frozen_mapping(decl: Tuple[Tuple[str, object], ...], name: str) -> Dict[str, object]:
    """Tuple-to-mapping conversion that REFUSES duplicate field names (L2 C1): a duplicate key would
    silently drop a field from field-by-field verification."""
    keys = [k for k, _ in decl]
    if len(set(keys)) != len(keys):
        raise NullDomainError(f"{name}: duplicate declaration field names {sorted(k for k in keys if keys.count(k) > 1)}")
    return dict(decl)


def verify_frozen_identity() -> None:
    """Fail-closed (L2 M3-1): the M1 and M2 identities; every declaration field equal to its live
    global; the declared constants equal to the committed E1 constants; the template, quantile,
    support, and method identities."""
    _C.verify_frozen_identity(); _K.verify_frozen_identity()
    if _digest(NULL_DECLARATION) != NULL_DECLARATION_SHA256_LITERAL:
        raise NullDomainError("null declaration differs from its frozen literal digest")
    d = _frozen_mapping(NULL_DECLARATION, "NULL_DECLARATION")
    if len(d) != len(NULL_DECLARATION):
        raise NullDomainError("null declaration lost a field in mapping")
    live = {"n_cells": N_CELLS, "grid": E1_GRID, "base_width_micro": E1_BASE_WIDTH_MICRO, "f_dispatch": "F_canonical",
            "constants": E1_CONSTANTS_EXPECTED, "density_terms": "zero", "quantile": NULL_QUANTILE, "window": WINDOW, "n_windows": N_WINDOWS,
            "terminal_windows": TERMINAL_WINDOWS, "term_ticks": TERM_TICKS, "template_master": NULL_TEMPLATE_MASTER,
            "template_rng_role": NULL_TEMPLATE_ROLE, "template_sha256": NULL_TEMPLATE_SHA256_LITERAL, "law": "exact_poisson_binomial",
            "evaluation": "float64_fft", "error_bound_factor": NULL_ERROR_BOUND_FACTOR, "error_bound_floor": NULL_ERROR_BOUND_FLOOR,
            "primary_scoring_object": "conditional_per_seed", "reference_template_use": "reference/sensitivity/validation only",
            "quantile_modes": ("exact_certified", "conservative_coverage"), "conservative_rule": "k_safe = min{k : F_hat(k) - eps >= q}",
            "scoring_object_version": SCORING_OBJECT_VERSION, "payload_identity": "sha256 of the canonical complete threshold payload, excluding the digest itself"}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v):
            raise NullDomainError(f"null declaration field {k} differs from the live global")
    if N_CELLS != E1_GRID * E1_GRID or N_CELLS != _K.N_CELLS or TERM_TICKS != 300 or NULL_QUANTILE != 0.99 or N_WINDOWS != 10:
        raise NullDomainError("null support/quantile/window count inconsistent with M1/M2 or the hard values")
    if NULL_TEMPLATE_ROLE != 0xE10000 or NULL_TEMPLATE_MASTER != 202609171:          # the established template RNG identity, hard
        raise NullDomainError("template RNG role/master differ from the established values")
    if SCORING_OBJECT_VERSION != "e1_conditional_null_v1" or THRESHOLD_MODES_SET != ("exact_certified", "conservative_coverage"):
        raise NullDomainError("scoring object version or mode set differs from the established values")
    if len(live) != len(d):
        raise NullDomainError("declaration and live verification sets differ in size")
    k = DynamicsConstants()
    for name, val in E1_CONSTANTS_EXPECTED:
        if getattr(k, name) != val:
            raise NullDomainError(f"committed constant {name} differs from the E1 declaration")


# ----------------------------------------------------------------------------- template
def generate_rank_template(master: int = NULL_TEMPLATE_MASTER) -> np.ndarray:
    g = np.random.default_rng(np.random.SeedSequence([int(master), NULL_TEMPLATE_ROLE]))
    return g.random((N_CELLS, 3))


def validate_template(t) -> np.ndarray:
    if not isinstance(t, np.ndarray) or t.dtype != np.float64 or t.shape != (N_CELLS, 3):
        raise NullDomainError("template must be a float64 ndarray of shape (2500, 3)")
    if not np.isfinite(t).all() or (t < 0.0).any() or (t >= 1.0).any():
        raise NullDomainError("template values must be finite in [0, 1)")
    return t


_TEMPLATE_CACHE: Optional[np.ndarray] = None


def rank_template() -> np.ndarray:
    """The frozen REFERENCE template (never a production scoring object): regenerated once, digest-verified at EVERY call (L2 M3-2),
    returned as a read-only copy so the cache can never be mutated through a returned reference."""
    global _TEMPLATE_CACHE
    if _TEMPLATE_CACHE is None:
        _TEMPLATE_CACHE = validate_template(generate_rank_template()); _TEMPLATE_CACHE.setflags(write=False)
    if hashlib.sha256(_TEMPLATE_CACHE.tobytes()).hexdigest() != NULL_TEMPLATE_SHA256_LITERAL:
        raise NullDomainError("rank template differs from its frozen literal digest")
    out = _TEMPLATE_CACHE.copy(); out.setflags(write=False)
    return out


# ----------------------------------------------------------------------------- per-level chain
def _level(level_micro) -> int:
    if isinstance(level_micro, bool) or not isinstance(level_micro, (int, np.integer)):
        raise NullDomainError("level must be an exact integer micro-unit value")
    m = int(level_micro)
    if m - E1_BASE_WIDTH_MICRO // 2 < 0 or m + E1_BASE_WIDTH_MICRO // 2 > MICRO_UNITS:
        raise NullDomainError("inadmissible level (base interval leaves [0,1])")
    return m


def _exact_pos_int(x, name: str) -> int:
    if isinstance(x, bool) or not isinstance(x, (int, np.integer)) or int(x) <= 0:
        raise NullDomainError(f"{name} must be an exact positive non-Boolean integer")
    return int(x)


def _p_act_with(level_micro: int, k: DynamicsConstants, template: np.ndarray) -> np.ndarray:
    """PRIVATE: the chain under explicit constants and template (validation only; never production)."""
    m = _level(level_micro); w = E1_BASE_WIDTH_MICRO / MICRO_UNITS
    b = (m / MICRO_UNITS - w / 2.0) + w * validate_template(template)
    lam = b[:, 0] * b[:, 1] * b[:, 2]                       # F_canonical
    p_base = 1.0 / (1.0 + np.exp(-(k.alpha * lam - k.gamma_offset)))
    p = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)
    if not np.isfinite(p).all():
        raise NullDomainError("nonfinite null probability")
    return p


def null_bases(level_micro: int) -> np.ndarray:
    verify_frozen_identity(); m = _level(level_micro); w = E1_BASE_WIDTH_MICRO / MICRO_UNITS
    return (m / MICRO_UNITS - w / 2.0) + w * rank_template()


def null_p_act(level_micro: int) -> np.ndarray:
    """REFERENCE chain: the frozen template and the declared E1 constants only (no override parameters). Not production."""
    verify_frozen_identity()
    return _p_act_with(level_micro, DynamicsConstants(), rank_template())


# ----------------------------------------------------------------------------- exact law, float64 evaluation, certified
@dataclass(frozen=True)
class PmfCertificate:
    reps: int
    support: int
    max_imag_residual: float
    total_negative_mass: float
    most_negative_coefficient: float
    raw_normalisation_error: float
    clip_renorm_correction: float      # L1 distance between the raw real pmf and the cleaned pmf
    tick_l1_bound: float               # conservative L1 error bound of the per-tick pmf this sum was built from
    sum_l1_bound: float                # final L1 bound of THIS pmf: reps·tick_l1_bound + own residual bound (convolution is L1-contractive)

    def __post_init__(self) -> None:
        validate_pmf_certificate(self)


def validate_pmf_certificate(c) -> None:
    """PMF-certificate semantic validator (L2 r5 §6.1): exact type; exact non-Boolean integral reps and support;
    finite residual/bound fields with admissible signs; the certificate's OWN residual bound recomputed through
    `_own_bound`; the reps-1 identity (tick == sum == own); the repeated-convolution identity
    (sum == reps × tick + own, exact float). Called at construction, by the complete object validator for every
    carried PMF certificate, and therefore at the production guard."""
    if type(c) is not PmfCertificate:
        raise NullDomainError("validate_pmf_certificate requires an exact PmfCertificate")
    for name in ("reps", "support"):
        x = getattr(c, name)
        if isinstance(x, bool) or not isinstance(x, int) or x <= 0:
            raise NullDomainError(f"PMF certificate {name} must be an exact positive non-Boolean integer")
    vals = (c.max_imag_residual, c.total_negative_mass, c.most_negative_coefficient, c.raw_normalisation_error, c.clip_renorm_correction, c.tick_l1_bound, c.sum_l1_bound)
    if not all(isinstance(x, float) and math.isfinite(x) for x in vals):
        raise NullDomainError("PMF certificate residual/bound fields must be finite floats")
    if c.max_imag_residual < 0.0 or c.total_negative_mass < 0.0 or c.most_negative_coefficient > 0.0 or c.clip_renorm_correction < 0.0 or c.tick_l1_bound <= 0.0 or c.sum_l1_bound <= 0.0:
        raise NullDomainError("PMF certificate residual/bound fields have inadmissible signs")
    if c.support % c.reps != 0:
        raise NullDomainError("PMF certificate support must be a multiple of reps")
    own = _own_bound(c.max_imag_residual, c.total_negative_mass, c.raw_normalisation_error, c.clip_renorm_correction)
    if c.reps == 1:
        if not (c.tick_l1_bound == own and c.sum_l1_bound == own):
            raise NullDomainError("per-tick PMF certificate must carry tick == sum == its own recomputed residual bound")
    else:
        if c.sum_l1_bound != c.reps * c.tick_l1_bound + own:
            raise NullDomainError("repeated-convolution PMF certificate must satisfy sum == reps x tick + own recomputed residual bound")


def _validate_p(p) -> np.ndarray:
    if not isinstance(p, np.ndarray) or p.dtype != np.float64 or p.ndim != 1 or p.size == 0 or not np.isfinite(p).all() or (p < 0).any() or (p > 1).any():
        raise NullDomainError("probabilities must be a finite float64 1-D vector in [0,1]")
    return p


def _own_bound(imag: float, total_neg: float, raw_norm_err: float, correction: float) -> float:
    return max(NULL_ERROR_BOUND_FLOOR, NULL_ERROR_BOUND_FACTOR * max(imag, total_neg, abs(raw_norm_err), correction))


def _clean(raw: np.ndarray, reps: int, tick_l1_bound: float = 0.0) -> Tuple[np.ndarray, PmfCertificate]:
    real = np.real(raw); imag = float(np.max(np.abs(np.imag(raw))))
    neg = real[real < 0.0]
    total_neg = float(-np.sum(neg)) if neg.size else 0.0
    most_neg = float(np.min(real)) if neg.size else 0.0
    raw_norm_err = float(np.sum(real) - 1.0)
    cleaned = np.where(real < 0.0, 0.0, real)
    tot = float(np.sum(cleaned))
    if not np.isfinite(tot) or abs(tot - 1.0) > 1e-6:
        raise NullDomainError(f"pmf evaluation failed to normalise (sum {tot!r})")
    cleaned = cleaned / tot
    correction = float(np.sum(np.abs(cleaned - real)))
    own = _own_bound(imag, total_neg, raw_norm_err, correction)
    # L1 error of a reps-fold convolution ≤ reps × L1 error of the factor (convolution is L1-contractive), plus this evaluation's own residual
    sum_l1 = reps * tick_l1_bound + own if reps > 1 else own
    return cleaned, PmfCertificate(reps, real.size - 1, imag, total_neg, most_neg, raw_norm_err, correction, tick_l1_bound if reps > 1 else own, sum_l1)


def per_tick_count_pmf(p) -> Tuple[np.ndarray, PmfCertificate]:
    """Per-tick count pmf over 0..n: characteristic function on θ_k = 2πk/(n+1), inverted by the DFT with
    the matching sign (fft(φ)/(n+1)). Returns (cleaned pmf, certificate)."""
    p = _validate_p(p); n = p.size
    theta = 2.0 * np.pi * np.arange(n + 1) / (n + 1)
    logphi = np.zeros(n + 1, dtype=np.complex128)
    for s in range(0, n + 1, 512):
        th = theta[s:s + 512][:, None]
        logphi[s:s + 512] = np.sum(np.log1p(p[None, :] * (np.exp(1j * th) - 1.0)), axis=1)
    return _clean(np.fft.fft(np.exp(logphi)) / (n + 1), 1)


def per_tick_count_pmf_dp(p) -> np.ndarray:
    """INDEPENDENT second path (no FFT): the O(n²) recursive convolution in float64."""
    p = _validate_p(p); pmf = np.zeros(p.size + 1); pmf[0] = 1.0
    for i, pi in enumerate(p):
        pmf[1:i + 2] = pmf[1:i + 2] * (1.0 - pi) + pmf[0:i + 1] * pi
        pmf[0] *= (1.0 - pi)
    return pmf


def poisson_binomial_pmf(p, reps) -> Tuple[np.ndarray, PmfCertificate]:
    """Sum over `reps` i.i.d. per-tick counts: reps-fold convolution via FFT power on the zero-padded
    per-tick pmf (support 0..reps·n). Returns (cleaned pmf, certificate)."""
    pmf, cert, _ = poisson_binomial_pmf_with_tick(p, reps)
    return pmf, cert


def poisson_binomial_pmf_with_tick(p, reps) -> Tuple[np.ndarray, PmfCertificate, PmfCertificate]:
    """As `poisson_binomial_pmf`, also returning the per-tick certificate the sum's bound inherits from."""
    reps = _exact_pos_int(reps, "reps")
    base, cert_base = per_tick_count_pmf(p)
    n = reps * (base.size - 1)
    padded = np.zeros(n + 1); padded[:base.size] = base
    pmf, cert = _clean(np.fft.ifft(np.fft.fft(padded) ** reps), reps, tick_l1_bound=cert_base.sum_l1_bound)
    return pmf, cert, cert_base


def direct_convolution_pmf(p, reps) -> np.ndarray:
    """INDEPENDENT second path for small reps: sequential full-support direct convolution
    (numpy.convolve is a direct product sum, not an FFT) of the DP per-tick pmf."""
    reps = _exact_pos_int(reps, "reps")
    base = per_tick_count_pmf_dp(p); out = base.copy()
    for _ in range(reps - 1):
        out = np.convolve(out, base)
    return out


def direct_convolution_pmf_truncated(p, reps, tail_cut: float = 1e-30) -> Tuple[np.ndarray, float]:
    """INDEPENDENT second path that reaches 300 ticks: sequential direct convolution on a TRUNCATED
    support — after each step, leading/trailing coefficients below tail_cut are dropped and the total
    discarded mass is accumulated and RETURNED as part of this path's own error. Deterministic, no FFT.
    Returns (full-length pmf with zeros outside the kept support, discarded_mass)."""
    reps = _exact_pos_int(reps, "reps")
    base = per_tick_count_pmf_dp(p); n_tick = base.size - 1
    cur = base.copy(); lo = 0; discarded = 0.0
    for _ in range(reps - 1):
        cur = np.convolve(cur, base)
        keep = np.nonzero(cur >= tail_cut)[0]
        a, b = int(keep[0]), int(keep[-1]) + 1
        discarded += float(np.sum(cur[:a]) + np.sum(cur[b:]))
        cur = cur[a:b]; lo += a
    out = np.zeros(reps * n_tick + 1); out[lo:lo + cur.size] = cur
    return out, discarded


def error_bound(cert: PmfCertificate) -> float:
    """CDF error bound of the pmf's OWN cumulative sum: a CDF value is a partial sum of the pmf, so its
    absolute error is ≤ the pmf's L1 error (sum_l1_bound, which already inherits the per-tick error)."""
    return cert.sum_l1_bound


def f_min_derivative_bound() -> float:
    """d/dF [1 − (1 − F)^n] = n(1 − F)^(n−1) ≤ n on [0,1]. DERIVED from the frozen N_WINDOWS at call time
    (L2 r4: no independent mutable constant may weaken the θ_P certificate); the frozen identity
    verifier requires N_WINDOWS == 10 and the declaration's n_windows to agree."""
    if N_WINDOWS != 10 or _frozen_mapping(NULL_DECLARATION, "NULL_DECLARATION")["n_windows"] != N_WINDOWS:
        raise NullDomainError("N_WINDOWS differs from the frozen value 10")
    return float(N_WINDOWS)


def final_cdf_bounds(cert_w: PmfCertificate, cert_t: PmfCertificate) -> Tuple[float, float]:
    """The bounds on the TWO FINAL CDFs that select the thresholds (L2 r3 M3-3): F_min through the
    min-of-N_WINDOWS map (derivative ≤ N_WINDOWS, derived, never a free constant) and F_term directly."""
    return f_min_derivative_bound() * error_bound(cert_w), error_bound(cert_t)


@dataclass(frozen=True)
class QuantileCertificate:
    index: int                       # the SELECTED index: k* in exact mode, k_safe in conservative mode
    value: float                     # float64 of index/denominator (the grid value)
    cdf_below: float                 # F̂(k*−1) at the ORDINARY crossing
    cdf_at: float                    # F̂(k*)
    margin_below: float              # q − F̂(k*−1)
    margin_at: float                 # F̂(k*) − q
    error_bound: float               # ε: the certified final-CDF error bound
    certified: bool                  # True in either mode once a certified object exists
    mode: str = "exact_certified"    # "exact_certified" | "conservative_coverage"
    ordinary_index: int = -1         # k* = min{k : F̂(k) ≥ q}
    ordinary_certifiable: bool = True
    conservative_index: int = -1     # k_safe = min{k : F̂(k) − ε ≥ q}
    displacement: int = 0            # conservative_index − ordinary_index (reported; never a global claim)
    cdf_at_selected: float = 0.0     # F̂(selected index)
    denominator: int = 0             # the count-grid denominator; value == float64(index / denominator)

    def __post_init__(self) -> None:
        validate_quantile_certificate(self)


def validate_quantile_certificate(self) -> None:
    """Certificate-level fail-closed invariants (L2 r2 §7; r4 §5): a reusable validator called at
    construction, by the parent object's validator for BOTH certificates, and by the production guard —
    so a nested post-construction mutation cannot hide behind mutually consistent parent fields."""
    if type(self) is not QuantileCertificate:
        raise NullDomainError("validate_quantile_certificate requires an exact QuantileCertificate")
    if True:
        q = NULL_QUANTILE
        if isinstance(self.denominator, bool) or not isinstance(self.denominator, int) or self.denominator <= 0:
            raise NullDomainError("certificate denominator must be a positive integer")
        if self.value != float(np.float64(self.index) / np.float64(self.denominator)):
            raise NullDomainError("certificate value must equal float64(index / denominator)")
        vals = (self.value, self.cdf_below, self.cdf_at, self.margin_below, self.margin_at, self.error_bound, self.cdf_at_selected)
        if not all(isinstance(x, float) and math.isfinite(x) for x in vals):
            raise NullDomainError("certificate fields must be finite floats")
        if not (0.0 <= self.value <= 1.0 and 0.0 <= self.cdf_below <= 1.0 and 0.0 <= self.cdf_at <= 1.0 and 0.0 <= self.cdf_at_selected <= 1.0 and self.error_bound > 0.0):
            raise NullDomainError("certificate values out of range")
        if self.mode not in THRESHOLD_MODES_SET:
            raise NullDomainError(f"unknown certificate mode {self.mode!r}")
        if any(isinstance(i, bool) or not isinstance(i, int) for i in (self.index, self.ordinary_index, self.conservative_index, self.displacement)):
            raise NullDomainError("certificate indices must be exact integers")
        if self.displacement != self.conservative_index - self.ordinary_index:
            raise NullDomainError("displacement must equal conservative_index - ordinary_index")
        if self.margin_below != q - self.cdf_below or self.margin_at != self.cdf_at - q:
            raise NullDomainError("margins must be derived from the ordinary crossing's CDF values")
        if not (self.cdf_below < q <= self.cdf_at):
            raise NullDomainError("the ordinary crossing must straddle q: cdf_below < q <= cdf_at")
        # ordinary certifiability is a COMPUTED semantic fact (L2 r3 §6.1), never a trusted Boolean
        ordinary_ok = bool(self.margin_below > self.error_bound and self.margin_at > self.error_bound)
        if self.ordinary_certifiable is not ordinary_ok:
            raise NullDomainError("ordinary_certifiable must equal the computed margin test")
        if self.mode == "exact_certified":
            if not (ordinary_ok and self.index == self.ordinary_index and self.cdf_at_selected == self.cdf_at):
                raise NullDomainError("exact mode must select the certified ordinary crossing")
        else:
            if ordinary_ok or self.index != self.conservative_index or not (self.cdf_at_selected - self.error_bound >= q):
                raise NullDomainError("conservative mode requires an uncertifiable ordinary crossing and F_hat(k_safe) - eps >= q")
        if not self.certified:
            raise NullDomainError("a constructed certificate is certified by construction")


def validate_null_thresholds(th) -> None:
    """THE COMPLETE OBJECT VALIDATOR: exact types; both nested certificates re-validated; the object's own
    invariants; the statistic geometry. Called by NullThresholds.__post_init__ and by the production guard."""
    if type(th) is not NullThresholds:
        raise NullDomainError("validate_null_thresholds requires an exact NullThresholds")
    for c in (th.theta_p_certificate, th.theta_t_certificate):
        validate_quantile_certificate(c)
    if th.tick_pmf_certificate is None:
        raise NullDomainError("the per-tick PMF certificate must be carried")
    for pc in (th.tick_pmf_certificate, th.window_pmf_certificate, th.terminal_pmf_certificate):
        validate_pmf_certificate(pc)
    tk = th.tick_pmf_certificate
    if tk.reps != 1 or tk.support != N_CELLS:
        raise NullDomainError("the carried per-tick certificate must have reps 1 and support N_CELLS")
    # the inherited per-tick bound is bound by IDENTITY to the carried per-tick certificate (never an inequality)
    for pc in (th.window_pmf_certificate, th.terminal_pmf_certificate):
        if pc.tick_l1_bound != tk.sum_l1_bound:
            raise NullDomainError("window/terminal certificates must inherit the carried per-tick certificate's bound exactly")
    th._validate_own_invariants()
    validate_threshold_geometry(th)


def _quantile(cdf: np.ndarray, denom: int, final_cdf_bound: float) -> QuantileCertificate:
    """The threshold of a FINAL CDF with the FINAL-CDF error bound ε (never a component pmf's).
    EXACT mode when the ordinary crossing k* certifies (both margins > ε). Otherwise the CONSERVATIVE
    CERTIFIED COVERAGE THRESHOLD k_safe = min{k : F̂(k) − ε ≥ q} (L2 M6 Finding-2 formulation), which
    guarantees true F(k_safe) ≥ q; if no support point satisfies it, HALT."""
    q = NULL_QUANTILE
    k = int(np.searchsorted(cdf, q, side="left"))
    below = float(cdf[k - 1]) if k > 0 else 0.0; at = float(cdf[k])
    mb, ma = q - below, at - q
    ordinary_ok = bool(mb > final_cdf_bound and ma > final_cdf_bound)
    k_safe = int(np.searchsorted(cdf, q + final_cdf_bound, side="left"))
    if k_safe >= cdf.size or not (float(cdf[k_safe]) - final_cdf_bound >= q):
        raise NullDomainError("no support point clears the conservative coverage condition F_hat(k) - eps >= q")
    if ordinary_ok:
        return QuantileCertificate(k, float(np.float64(k) / np.float64(denom)), below, at, mb, ma, final_cdf_bound, True,
                                   "exact_certified", k, True, k_safe, k_safe - k, at, int(denom))
    return QuantileCertificate(k_safe, float(np.float64(k_safe) / np.float64(denom)), below, at, mb, ma, final_cdf_bound, True,
                               "conservative_coverage", k, False, k_safe, k_safe - k, float(cdf[k_safe]), int(denom))


@dataclass(frozen=True)
class NullThresholds:
    level_micro: int
    level_id: str
    theta_p: float
    theta_t: float
    theta_p_certificate: QuantileCertificate
    theta_t_certificate: QuantileCertificate
    window_pmf_certificate: PmfCertificate
    terminal_pmf_certificate: PmfCertificate
    p_act_mean: float
    law: str
    evaluation: str
    sampling_ci_half_width: float    # 0.0: no Monte Carlo error exists
    numerically_certified: bool
    role: str = "reference_template"         # "conditional_per_seed" (PRODUCTION SCORING) | "reference_template" (never production scoring)
    seed: Optional[int] = None               # the production seed the conditional object belongs to
    bases_sha256: Optional[str] = None       # component-array identity of the exact initialized (v, u_base, r)
    threshold_modes: Tuple[str, str] = ("exact_certified", "exact_certified")
    config_hash: Optional[str] = None        # the frozen production RunConfig hash the bases were replayed from
    scoring_identity: Optional[str] = None   # composite CONTEXT identity: version | level | seed | components | dtype/shape | bases | config
    payload_sha256: Optional[str] = None     # identity of the canonical complete THRESHOLD PAYLOAD (every scoring-relevant field, nested certificates included)
    tick_pmf_certificate: Optional[PmfCertificate] = None   # the per-tick certificate the window/terminal bounds INHERIT from (L2 r5 §6.2, preferred)

    def __post_init__(self) -> None:
        validate_null_thresholds(self)
        if self.payload_sha256 != threshold_payload_identity(self):
            raise NullDomainError("threshold payload identity does not match the object's payload")

    def _validate_own_invariants(self) -> None:
        """Fail-closed internal invariants (L2 §11, r2 §5/§7): semantic agreement between the object and its
        certificates; frozen law/evaluation fields; role-specific metadata; the context identity recomputes.
        (Nested certificate validation and geometry are applied by validate_null_thresholds.)"""
        if self.role not in ("reference_template", "conditional_per_seed", "analysis_bases"):
            raise NullDomainError(f"unknown threshold role {self.role!r}")
        if self.level_id != level_id(self.level_micro):
            raise NullDomainError("level_id does not match level_micro")
        if self.theta_p != self.theta_p_certificate.value or self.theta_t != self.theta_t_certificate.value:
            raise NullDomainError("theta values differ from their certificates")
        if self.threshold_modes != (self.theta_p_certificate.mode, self.theta_t_certificate.mode):
            raise NullDomainError("threshold_modes differ from the certificates' modes")
        if self.numerically_certified != (self.theta_p_certificate.certified and self.theta_t_certificate.certified):
            raise NullDomainError("numerically_certified differs from the certificates")
        if (self.law, self.evaluation, self.sampling_ci_half_width) != ("exact_poisson_binomial", "float64_fft", 0.0):
            raise NullDomainError("law/evaluation/sampling fields differ from the frozen definitions")
        if not (isinstance(self.p_act_mean, float) and math.isfinite(self.p_act_mean) and 0.0 <= self.p_act_mean <= 1.0):
            raise NullDomainError("p_act_mean must be a finite float in [0, 1]")
        if self.role in ("reference_template", "analysis_bases") and not (self.seed is None and self.bases_sha256 is None and self.config_hash is None and self.scoring_identity is None):
            raise NullDomainError("non-production object must carry no seed, bases, config, or scoring identity")
        if self.role == "conditional_per_seed":
            if self.seed not in _C.E1_SEED_PANEL or not self.bases_sha256 or not self.config_hash or not self.scoring_identity:
                raise NullDomainError("conditional object requires a frozen production seed, bases identity, config hash, and scoring identity")
            if self.scoring_identity != composite_scoring_identity(self.level_micro, self.seed, self.bases_sha256, self.config_hash):
                raise NullDomainError("scoring identity does not match the object's level/seed/bases/config")

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def validate_threshold_geometry(th) -> None:
    """Bind the certificates to E1's statistic geometry (L2 r3 §6.2): θ_P on the window count grid, θ_T on
    the terminal count grid; PMF certificates with the window/terminal reps and supports; certificate error
    bounds EQUAL to final_cdf_bounds of the carried PMF certificates (exact float equality). Called by
    __post_init__ AND by the production guard, so a mutation cannot bypass it by recomputing the digest."""
    if th.theta_p_certificate.denominator != WINDOW * N_CELLS or th.theta_t_certificate.denominator != TERM_TICKS * N_CELLS:
        raise NullDomainError("certificate denominators must be the E1 window and terminal count grids (250000 / 750000)")
    w, tm = th.window_pmf_certificate, th.terminal_pmf_certificate
    if (w.reps, w.support, tm.reps, tm.support) != (WINDOW, WINDOW * N_CELLS, TERM_TICKS, TERM_TICKS * N_CELLS):
        raise NullDomainError("PMF certificate reps/support must be the window (100/250000) and terminal (300/750000) constructions")
    b_min, b_term = final_cdf_bounds(w, tm)
    if (th.theta_p_certificate.error_bound, th.theta_t_certificate.error_bound) != (b_min, b_term):
        raise NullDomainError("certificate error bounds must equal final_cdf_bounds of the carried PMF certificates")


def threshold_payload_identity(th) -> str:
    """sha256 of the canonical complete threshold payload — every scoring-relevant output and every nested
    certificate field — excluding only the payload digest itself (L2 r2 §5)."""
    d = asdict(th); d.pop("payload_sha256", None)
    canon = repr(sorted(d.items()))
    return hashlib.sha256(canon.encode()).hexdigest()


def composite_scoring_identity(level_micro: int, seed: int, bases_sha256: str, config_hash: str) -> str:
    """The composite scoring identity carried into the run record (L2 C2/C3): version | level | seed |
    component names | dtype/shape | base bytes identity | production config hash."""
    canon = "|".join([SCORING_OBJECT_VERSION, level_id(level_micro), str(int(seed)), "v,u_base,r", f"float64/({E1_GRID},{E1_GRID})", bases_sha256, config_hash])
    return hashlib.sha256(canon.encode()).hexdigest()


def _thresholds_from_p(p: np.ndarray, level_micro: int, role: str, seed: Optional[int], bases_sha: Optional[str],
                       config_hash: Optional[str] = None) -> NullThresholds:
    pmf_w, cert_w, cert_tick = poisson_binomial_pmf_with_tick(p, WINDOW)
    pmf_t, cert_t, cert_tick2 = poisson_binomial_pmf_with_tick(p, TERM_TICKS)
    if cert_tick != cert_tick2:
        raise NullDomainError("per-tick certificate differs between the window and terminal constructions")
    b_min, b_term = final_cdf_bounds(cert_w, cert_t)
    cdf_min = 1.0 - (1.0 - np.cumsum(pmf_w)) ** N_WINDOWS
    qp = _quantile(cdf_min, WINDOW * N_CELLS, b_min)
    qt = _quantile(np.cumsum(pmf_t), TERM_TICKS * N_CELLS, b_term)
    if not (qp.certified and qt.certified):
        raise NullDomainError(f"threshold not certified at level {level_id(level_micro)}: theta_P {qp}, theta_T {qt}")
    sid = composite_scoring_identity(level_micro, seed, bases_sha, config_hash) if role == "conditional_per_seed" else None
    fields = (int(level_micro), level_id(level_micro), qp.value, qt.value, qp, qt, cert_w, cert_t, float(np.mean(p)),
              "exact_poisson_binomial", "float64_fft", 0.0, True, role, seed, bases_sha, (qp.mode, qt.mode), config_hash, sid)
    probe = object.__new__(NullThresholds)                    # compute the payload digest on the same field values, then construct fail-closed
    for name, val in zip(NullThresholds.__dataclass_fields__, fields + (None, cert_tick)):
        object.__setattr__(probe, name, val)
    return NullThresholds(*fields, threshold_payload_identity(probe), cert_tick)


def reference_thresholds(level_micro: int) -> NullThresholds:
    """REFERENCE thresholds from the frozen common-rank template — a reference/stability object, an
    alternative-null sensitivity axis, and the numerical-validation template. NEVER a production
    scoring threshold (amendment of record). Role is marked on the object."""
    verify_frozen_identity()
    return _thresholds_from_p(null_p_act(level_micro), level_micro, "reference_template", None, None)


def null_thresholds(level_micro: int) -> NullThresholds:
    """RETIRED (L2 §10). The generic name preserved the historical misuse the amendment eliminates.
    Call `reference_thresholds` (reference/sensitivity/validation) or `conditional_thresholds` (production)."""
    raise NullDomainError("null_thresholds is retired: use reference_thresholds (reference) or conditional_thresholds (production)")


def validate_bases(v, u_base, r, production_shape: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Production bases must have the exact grid shape (E1_GRID, E1_GRID) (L2 §7); the reference/analysis
    path may accept flat vectors when `production_shape=False`."""
    out = []
    for name, a in (("v", v), ("u_base", u_base), ("r", r)):
        if not isinstance(a, np.ndarray) or a.dtype != np.float64:
            raise NullDomainError(f"{name}: float64 ndarray required")
        if production_shape and a.shape != (E1_GRID, E1_GRID):
            raise NullDomainError(f"{name}: production bases must have shape ({E1_GRID}, {E1_GRID}), got {a.shape}")
        if a.size != N_CELLS:
            raise NullDomainError(f"{name}: {N_CELLS} cells required")
        if not np.isfinite(a).all() or (a < 0.0).any() or (a > 1.0).any():
            raise NullDomainError(f"{name}: values must be finite in [0, 1]")
        out.append(np.ascontiguousarray(a.reshape(-1)))
    return out[0], out[1], out[2]


def bases_identity(v, u_base, r, production_shape: bool = True) -> str:
    """Component-array identity only: NOT proof of the seed/level relationship (that is `_replay_initialization`)."""
    v, u, r = validate_bases(v, u_base, r, production_shape)
    return hashlib.sha256(v.tobytes() + u.tobytes() + r.tobytes()).hexdigest()


def _replay_initialization(level_micro: int, seed: int):
    """Initialization ONLY, from the frozen production RunConfig for (level, seed), on the ancestor-faithful
    stream, stopping before any dynamics draw. Returns (config_hash, v, u_base, r)."""
    from ..init import initialize
    from ..rng import SeedRegistry
    cfg = _C.e1_run_config(int(level_micro), int(seed))            # production shape; refuses off-panel seeds
    st = initialize(cfg.init, cfg.grid_scale, SeedRegistry(cfg.seed).dynamics())
    return cfg.config_hash(), st.v, st.u_base, st.r


def _p_act_from_bases(v: np.ndarray, u: np.ndarray, r: np.ndarray) -> np.ndarray:
    k = DynamicsConstants()
    lam = v * u * r                                          # F_canonical
    p_base = 1.0 / (1.0 + np.exp(-(k.alpha * lam - k.gamma_offset)))
    p = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)
    if not np.isfinite(p).all():
        raise NullDomainError("nonfinite conditional probability")
    return p


def conditional_p_act(v, u_base, r) -> np.ndarray:
    """The run's OWN no-neighbour chain from its exact initialized bases under the frozen rule.
    Verifies the frozen identity itself (L2 §7)."""
    verify_frozen_identity()
    v, u, r = validate_bases(v, u_base, r)
    return _p_act_from_bases(v, u, r)


def conditional_thresholds(level_micro: int, seed: int, v, u_base, r) -> NullThresholds:
    """THE PRIMARY PRODUCTION SCORING OBJECT (amendment of record), PROVEN to belong to its run (L2 C2):
    the seed must be a frozen production seed; the frozen production RunConfig for (level, seed) is
    rebuilt; initialization is replayed on the ancestor-faithful stream; the supplied (v, u_base, r) —
    exact (50, 50) float64 — must equal the replayed arrays RAW-BIT; only then are the run's own θ_P/θ_T
    certified (exact or conservative coverage mode, recorded) and bound to a composite scoring identity."""
    verify_frozen_identity()
    m = _level(level_micro)
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
        raise NullDomainError("seed must be an exact non-Boolean integer")
    if int(seed) not in _C.E1_SEED_PANEL:
        raise NullDomainError("seed is not one of the frozen E1 production seeds")
    v_, u_, r_ = validate_bases(v, u_base, r, production_shape=True)
    chash, rv, ru, rr = _replay_initialization(m, int(seed))
    for name, got, want in (("v", v_, rv), ("u_base", u_, ru), ("r", r_, rr)):
        w = np.ascontiguousarray(want.reshape(-1))
        if got.dtype != w.dtype or got.view(np.uint64).tobytes() != w.view(np.uint64).tobytes():
            raise NullDomainError(f"{name}: supplied bases are not the replayed initialization for level {level_id(m)} seed {int(seed)}")
    p = _p_act_from_bases(v_, u_, r_)
    return _thresholds_from_p(p, m, "conditional_per_seed", int(seed), bases_identity(v, u_base, r), chash)


def conditional_thresholds_for_analysis(level_micro: int, v, u_base, r) -> NullThresholds:
    """NON-PRODUCTION constructor for audit/qualification code needing arbitrary base arrays (L2 C2).
    Returns an object with the DISTINCT non-production role "analysis_bases" (seed None, no bases identity,
    not the frozen template): it can never pass the production guard and is never mistaken for a reference object."""
    verify_frozen_identity()
    m = _level(level_micro)
    v_, u_, r_ = validate_bases(v, u_base, r, production_shape=False)
    return _thresholds_from_p(_p_act_from_bases(v_, u_, r_), m, "analysis_bases", None, None)


def require_production_scoring_object(th, expected_level_micro: int, expected_seed: int, expected_bases_sha256: str,
                                      expected_config_hash: str) -> NullThresholds:
    """Context-aware production guard (L2 C3): the object must be a NullThresholds, conditional, certified,
    internally consistent, and must agree EXACTLY with the run being scored on level, seed, bases identity,
    config hash, and composite scoring identity. Consumers scoring production runs call THIS, never a
    role check alone."""
    verify_frozen_identity()
    if not isinstance(th, NullThresholds):
        raise NullDomainError("production scoring requires a NullThresholds object")
    lvl = _level(expected_level_micro)
    if isinstance(expected_seed, bool) or not isinstance(expected_seed, (int, np.integer)) or int(expected_seed) not in _C.E1_SEED_PANEL:
        raise NullDomainError("expected seed must be an exact non-Boolean frozen production seed")
    for name, h in (("expected_bases_sha256", expected_bases_sha256), ("expected_config_hash", expected_config_hash)):
        if not isinstance(h, str) or len(h) != 64 or any(c not in "0123456789abcdef" for c in h):
            raise NullDomainError(f"{name} must be a 64-hex-character sha256 string")
    validate_null_thresholds(th)                                # the COMPLETE semantic surface incl. nested certificates and exact types, FIRST
    if th.payload_sha256 != threshold_payload_identity(th):
        raise NullDomainError("production scoring object payload identity does not recompute")
    if th.role != "conditional_per_seed":
        raise NullDomainError("production scoring requires the conditional per-seed null (reference-template thresholds refused)")
    if not (th.numerically_certified and th.theta_p_certificate.certified and th.theta_t_certificate.certified):
        raise NullDomainError("production scoring object is not certified")
    if th.threshold_modes != (th.theta_p_certificate.mode, th.theta_t_certificate.mode):
        raise NullDomainError("production scoring object modes inconsistent with its certificates")
    expected = composite_scoring_identity(lvl, int(expected_seed), expected_bases_sha256, expected_config_hash)
    if (th.level_micro, th.seed, th.bases_sha256, th.config_hash, th.scoring_identity) != \
            (lvl, int(expected_seed), expected_bases_sha256, expected_config_hash, expected):
        raise NullDomainError("production scoring object does not belong to the run being scored (level/seed/bases/config identity mismatch)")
    return th


# ----------------------------------------------------------------------------- validation program (frozen)
VALIDATION_LEVELS_MICRO: Tuple[int, ...] = (150000, 515217, 850000)      # low, middle, high pass-1 levels
CONSERVATIVE_MODE_LEVELS_MICRO: Tuple[int, ...] = (508454,)             # declared ambiguous-crossing surface (L2 Q1): θ_P conservative
DIRECT_ALLOWANCE_RULE = ("direct allowance = primary final-CDF bound + max absolute FFT/direct CDF discrepancy + discarded mass; "
                         "direct path re-selects under it; ordinary index, selected index, mode, and coverage condition must agree")
DIRECT_ALLOWANCE_RULE_SHA256_LITERAL = "e69a87dc6398112dcb0f7978e139a0a3381b63e42eaaa2e70e0c6500745b7170"       # independent hardcoded identity of the EXACT rule string (L2 r4 §6)
DIRECT_ALLOWANCE_TERMS = ("primary final-CDF bound", "max absolute FFT/direct CDF discrepancy", "discarded mass")
DIRECT_AGREEMENTS = ("ordinary index", "selected index", "mode", "coverage condition")
VALIDATION_REPLICATES = 400
VALIDATION_REPLICATE_MASTER = 202609172
VALIDATION_DKW_ALPHA = 0.05
VALIDATION_QUANTILE_ALLOWANCE = 5e-4             # |θ_mc − θ_exact| < allowance (strict)
VALIDATION_EXCEEDANCE_CAP = 0.03                 # MC exceedance fraction <= cap (inclusive)
VALIDATION_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("levels_micro", VALIDATION_LEVELS_MICRO), ("replicates", VALIDATION_REPLICATES), ("replicate_master", VALIDATION_REPLICATE_MASTER),
    ("dkw_alpha", VALIDATION_DKW_ALPHA), ("statistics", ("S_min", "S_term")), ("comparisons", ("empirical_cdf_sup", "quantile", "exceedance", "direct_path")),
    ("dkw_rule", "sup_dev <= dkw_bound"), ("quantile_allowance", VALIDATION_QUANTILE_ALLOWANCE), ("quantile_rule", "abs(mc - exact) < allowance"),
    ("exceedance_cap", VALIDATION_EXCEEDANCE_CAP), ("exceedance_rule", "frac <= cap"),
    ("direct_path_rule", "final-CDF max abs diff (+ discarded mass) <= final-CDF bound; identical selected indices AND modes under the direct path's own selection"),
    ("conservative_mode_levels_micro", CONSERVATIVE_MODE_LEVELS_MICRO), ("conservative_mode_rule", DIRECT_ALLOWANCE_RULE),
    ("completion", "all three declared levels, both statistics, every comparison"),
)
VALIDATION_SHA256_LITERAL = "5a430205c033e4c47497d6eab33b5b087375da7746a70a222b5f0900b1970c55"   # established 2026-09-21 (round 4: full triangle allowance declared)


def brute_force_pmf(p, reps: int) -> np.ndarray:
    """Exact enumeration for tiny cases."""
    p = np.asarray(p, dtype=np.float64); n = reps * p.size; out = np.zeros(n + 1); q = np.repeat(p, reps)
    for bits in product((0, 1), repeat=n):
        pr = 1.0
        for b, pi in zip(bits, q): pr *= pi if b else (1 - pi)
        out[sum(bits)] += pr
    return out


def simulate_null_rho(level_micro: int, replicate, replicate_master, p: Optional[np.ndarray] = None) -> np.ndarray:
    """One replicate's PRODUCTION-SHAPED rho(t) (3000 ticks; only the tail is drawn — pre-tail ticks
    are zero and touch no tail statistic): per-tick counts from 2500 Bernoulli draws against p_act;
    rho_t = count/2500 in float64 exactly as rho_global is formed. COMMON RANDOM NUMBERS: replicate
    j's uniforms come from SeedSequence([master, j]) and are identical at every level."""
    p = null_p_act(level_micro) if p is None else _validate_p(p)
    if isinstance(replicate, bool) or not isinstance(replicate, (int, np.integer)) or int(replicate) < 0:
        raise NullDomainError("replicate must be an exact non-negative non-Boolean integer")
    master = _exact_pos_int(replicate_master, "replicate_master")
    g = np.random.default_rng(np.random.SeedSequence([master, int(replicate)]))
    rho = np.zeros(_K.RUN_LEN, dtype=np.float64)
    for w in range(N_WINDOWS):
        u = g.random((WINDOW, N_CELLS))
        counts = np.sum(u < p[None, :], axis=1)
        rho[_K.TAIL_START + w * WINDOW:_K.TAIL_START + (w + 1) * WINDOW] = counts.astype(np.float64) / np.float64(N_CELLS)
    return rho


def monte_carlo_tail_statistics(level_micro: int, n_replicates, replicate_master) -> Tuple[np.ndarray, np.ndarray]:
    """The contract's MC path: production-shaped series through M2's OWN tail_stats (bit-consistent
    by construction, L2 M3-5). Returns (S_min, S_term) per replicate."""
    verify_frozen_identity()
    n = _exact_pos_int(n_replicates, "n_replicates"); p = null_p_act(level_micro)
    s_min = np.empty(n); s_term = np.empty(n)
    for j in range(n):
        st = tail_stats(simulate_null_rho(level_micro, j, replicate_master, p))
        s_min[j] = st.s_min; s_term[j] = st.s_term
    return s_min, s_term


def _sup_dev(sample: np.ndarray, cdf_grid: np.ndarray, denom: int) -> float:
    ks = np.arange(cdf_grid.size)
    emp = np.searchsorted(np.sort(sample), ks / denom, side="right") / sample.size
    return float(np.max(np.abs(emp - cdf_grid)))


def validate_level(level_micro: int, n_replicates: int, replicate_master: int) -> Dict[str, float]:
    thr = reference_thresholds(level_micro); p = null_p_act(level_micro)
    pmf_w, _ = poisson_binomial_pmf(p, WINDOW); cdf_min = 1.0 - (1.0 - np.cumsum(pmf_w)) ** N_WINDOWS
    pmf_t, _ = poisson_binomial_pmf(p, TERM_TICKS); cdf_t = np.cumsum(pmf_t)
    s_min, s_term = monte_carlo_tail_statistics(level_micro, n_replicates, replicate_master)
    dkw = float(np.sqrt(np.log(2 / VALIDATION_DKW_ALPHA) / (2 * n_replicates)))
    return {"level_id": thr.level_id, "n": n_replicates, "dkw_bound": dkw,
            "sup_dev_term": _sup_dev(s_term, cdf_t, TERM_TICKS * N_CELLS), "sup_dev_min": _sup_dev(s_min, cdf_min, WINDOW * N_CELLS),
            "theta_t_exact": thr.theta_t, "theta_t_mc": float(np.quantile(s_term, NULL_QUANTILE, method="linear")),
            "theta_p_exact": thr.theta_p, "theta_p_mc": float(np.quantile(s_min, NULL_QUANTILE, method="linear")),
            "frac_term_exceeding": float(np.mean(s_term > thr.theta_t)), "frac_min_exceeding": float(np.mean(s_min > thr.theta_p))}


def validate_numerics(level_micro: int) -> Dict[str, float]:
    """The independent direct path against the FFT path at one level, on the TWO FINAL CDFs (L2 r3
    M3-3): F_min (through the min-of-ten map) and the 300-tick F_term; the direct path's own
    discarded mass is added to the comparison; both paths must select the SAME quantile indices."""
    thr = reference_thresholds(level_micro); p = null_p_act(level_micro)
    fft_tick, cert_tick = per_tick_count_pmf(p); dp_tick = per_tick_count_pmf_dp(p)
    fft_w, cert_w = poisson_binomial_pmf(p, WINDOW); fft_t, cert_t = poisson_binomial_pmf(p, TERM_TICKS)
    dir_w, disc_w = direct_convolution_pmf_truncated(p, WINDOW); dir_t, disc_t = direct_convolution_pmf_truncated(p, TERM_TICKS)
    cdf_min_fft = 1.0 - (1.0 - np.cumsum(fft_w)) ** N_WINDOWS; cdf_min_dir = 1.0 - (1.0 - np.cumsum(dir_w)) ** N_WINDOWS
    cdf_t_fft = np.cumsum(fft_t); cdf_t_dir = np.cumsum(dir_t)
    b_min, b_term = final_cdf_bounds(cert_w, cert_t)
    # INDEPENDENT selection on the direct path (L2 Q1): the direct path applies the SAME selection rule under a
    # prospectively stated allowance — the FFT path's certified final-CDF bound plus the direct path's own
    # discarded mass — and reports its own mode, ordinary index, and selected index. A conservative selected
    # index is compared only with the direct path's conservative selection, never with an ordinary crossing.
    delta_p = float(np.max(np.abs(cdf_min_fft - cdf_min_dir))); delta_t = float(np.max(np.abs(cdf_t_fft - cdf_t_dir)))
    # FULL TRIANGLE ALLOWANCE (L2 r2 §11.1): |F − F̂_dir| ≤ ε_FFT + ‖F̂_dir − F̂_FFT‖∞ + discarded mass
    dsel_p = _direct_selection(cdf_min_dir, b_min + delta_p + disc_w); dsel_t = _direct_selection(cdf_t_dir, b_term + delta_t + disc_t)
    return {"tick_max_abs_diff": float(np.max(np.abs(fft_tick - dp_tick))), "tick_error_bound": error_bound(cert_tick),
            "fmin_cdf_max_abs_diff": float(np.max(np.abs(cdf_min_fft - cdf_min_dir))) + disc_w, "fmin_final_bound": b_min,
            "fterm_cdf_max_abs_diff": float(np.max(np.abs(cdf_t_fft - cdf_t_dir))) + disc_t, "fterm_final_bound": b_term,
            "direct_discarded_mass_w": disc_w, "direct_discarded_mass_t": disc_t,
            "theta_p_index_fft": float(thr.theta_p_certificate.index), "theta_p_index_direct": float(dsel_p["selected"]),
            "theta_t_index_fft": float(thr.theta_t_certificate.index), "theta_t_index_direct": float(dsel_t["selected"]),
            "theta_p_mode_fft": thr.theta_p_certificate.mode, "theta_p_mode_direct": dsel_p["mode"],
            "theta_t_mode_fft": thr.theta_t_certificate.mode, "theta_t_mode_direct": dsel_t["mode"],
            "theta_p_ordinary_direct": float(dsel_p["ordinary"]), "theta_t_ordinary_direct": float(dsel_t["ordinary"]),
            "theta_p_ordinary_fft": float(thr.theta_p_certificate.ordinary_index), "theta_t_ordinary_fft": float(thr.theta_t_certificate.ordinary_index),
            "direct_allowance_p": b_min + delta_p + disc_w, "direct_allowance_t": b_term + delta_t + disc_t,
            "theta_p_coverage_ok_direct": bool(dsel_p["coverage_ok"]), "theta_t_coverage_ok_direct": bool(dsel_t["coverage_ok"])}


def _direct_selection(cdf: np.ndarray, allowance: float) -> Dict[str, object]:
    """The selection rule re-implemented on the direct path: ordinary crossing; certifiable iff both margins
    exceed the allowance; else the conservative selection min{k : F(k) − allowance ≥ q}; halt if none."""
    q = NULL_QUANTILE
    k = int(np.searchsorted(cdf, q, side="left"))
    below = float(cdf[k - 1]) if k > 0 else 0.0; at = float(cdf[k])
    ordinary_ok = (q - below > allowance) and (at - q > allowance)
    k_safe = int(np.searchsorted(cdf, q + allowance, side="left"))
    if k_safe >= cdf.size or not (float(cdf[k_safe]) - allowance >= q):
        raise NullDomainError("direct path: no support point clears the conservative coverage condition")
    sel = k if ordinary_ok else k_safe
    return {"ordinary": k, "selected": sel, "mode": "exact_certified" if ordinary_ok else "conservative_coverage",
            "coverage_ok": float(cdf[sel]) - allowance >= q if not ordinary_ok else True}


@dataclass
class ValidationRecord:
    passed: bool
    levels: Tuple[Dict[str, float], ...]
    numerics: Tuple[Dict[str, float], ...]
    declaration_sha256: str


def run_validation(execution_levels: Optional[Sequence[int]] = None) -> ValidationRecord:
    """The declared three-level, two-statistic validation with EXACT completion against the frozen
    validation declaration; per level: DKW agreement for BOTH statistics, MC quantiles near the exact
    ones, MC exceedance near 1%, and the independent direct path inside the error bound."""
    verify_frozen_identity()
    if _digest(VALIDATION_DECLARATION) != VALIDATION_SHA256_LITERAL:
        raise NullDomainError("validation declaration differs from its frozen literal digest")
    levels = tuple(VALIDATION_LEVELS_MICRO) if execution_levels is None else tuple(execution_levels)
    if len(set(levels)) != len(levels) or set(levels) != set(VALIDATION_LEVELS_MICRO):
        raise NullDomainError("validation execution set is not exactly the declared level set")
    out, nums = [], []
    for m in levels:
        out.append(validate_level(m, VALIDATION_REPLICATES, VALIDATION_REPLICATE_MASTER)); nums.append(validate_numerics(m))
    d = _frozen_mapping(VALIDATION_DECLARATION, "VALIDATION_DECLARATION")
    if d["conservative_mode_rule"] != DIRECT_ALLOWANCE_RULE:
        raise NullDomainError("declared direct-allowance rule differs from the live rule (full triangle)")
    if hashlib.sha256(DIRECT_ALLOWANCE_RULE.encode()).hexdigest() != DIRECT_ALLOWANCE_RULE_SHA256_LITERAL:
        raise NullDomainError("direct-allowance rule differs from its independent exact identity (full triangle)")
    if not all(term in DIRECT_ALLOWANCE_RULE for term in DIRECT_ALLOWANCE_TERMS + DIRECT_AGREEMENTS) or \
            DIRECT_ALLOWANCE_TERMS != ("primary final-CDF bound", "max absolute FFT/direct CDF discrepancy", "discarded mass") or \
            DIRECT_AGREEMENTS != ("ordinary index", "selected index", "mode", "coverage condition"):
        raise NullDomainError("direct-allowance rule terms differ from the established full triangle (three terms, four agreements)")
    if (d["quantile_allowance"], d["exceedance_cap"], d["dkw_alpha"], d["replicates"]) != (VALIDATION_QUANTILE_ALLOWANCE, VALIDATION_EXCEEDANCE_CAP, VALIDATION_DKW_ALPHA, VALIDATION_REPLICATES) \
            or (VALIDATION_QUANTILE_ALLOWANCE, VALIDATION_EXCEEDANCE_CAP, VALIDATION_DKW_ALPHA, VALIDATION_REPLICATES) != (5e-4, 0.03, 0.05, 400):
        raise NullDomainError("validation acceptance values differ from the frozen declaration or the hard contract values")
    ok = all(v["sup_dev_term"] <= v["dkw_bound"] and v["sup_dev_min"] <= v["dkw_bound"]
             and abs(v["theta_t_mc"] - v["theta_t_exact"]) < d["quantile_allowance"] and abs(v["theta_p_mc"] - v["theta_p_exact"]) < d["quantile_allowance"]
             and v["frac_term_exceeding"] <= d["exceedance_cap"] and v["frac_min_exceeding"] <= d["exceedance_cap"] for v in out)
    ok = ok and all(n["tick_max_abs_diff"] <= n["tick_error_bound"] and n["fmin_cdf_max_abs_diff"] <= n["fmin_final_bound"]
                    and n["fterm_cdf_max_abs_diff"] <= n["fterm_final_bound"]
                    and n["theta_p_index_fft"] == n["theta_p_index_direct"] and n["theta_t_index_fft"] == n["theta_t_index_direct"]
                    and n["theta_p_mode_fft"] == n["theta_p_mode_direct"] and n["theta_t_mode_fft"] == n["theta_t_mode_direct"]
                    and n["theta_p_ordinary_fft"] == n["theta_p_ordinary_direct"] and n["theta_t_ordinary_fft"] == n["theta_t_ordinary_direct"]
                    and n["theta_p_coverage_ok_direct"] and n["theta_t_coverage_ok_direct"] for n in nums)
    # the declared conservative-mode surface: at least one final CDF must actually be in conservative mode on BOTH paths
    if d.get("conservative_mode_levels_micro") != CONSERVATIVE_MODE_LEVELS_MICRO:
        raise NullDomainError("conservative-mode validation surface differs from the declaration")
    cons = [validate_numerics(m) for m in CONSERVATIVE_MODE_LEVELS_MICRO]
    ok = ok and all(("conservative_coverage" in (c["theta_p_mode_fft"], c["theta_t_mode_fft"]))
                    and c["theta_p_mode_fft"] == c["theta_p_mode_direct"] and c["theta_t_mode_fft"] == c["theta_t_mode_direct"]
                    and c["theta_p_index_fft"] == c["theta_p_index_direct"] and c["theta_t_index_fft"] == c["theta_t_index_direct"]
                    and c["theta_p_ordinary_fft"] == c["theta_p_ordinary_direct"] and c["theta_t_ordinary_fft"] == c["theta_t_ordinary_direct"]
                    and c["theta_p_coverage_ok_direct"] and c["theta_t_coverage_ok_direct"] for c in cons)
    nums = list(nums) + cons
    return ValidationRecord(bool(ok), tuple(out), tuple(nums), VALIDATION_SHA256_LITERAL)


# ----------------------------------------------------------------------------- witnesses
def common_random_numbers_witness(replicate: int = 0) -> Dict[str, object]:
    """Cross-level CRN (L2 M3-6): the SAME captured uniforms drive two DISTINCT levels; every cell
    active under the lower-p level is active under the higher-p level with the same draw (drawwise
    dominance under one shared stream)."""
    lo, hi = VALIDATION_LEVELS_MICRO[0], VALIDATION_LEVELS_MICRO[-1]
    p_lo, p_hi = null_p_act(lo), null_p_act(hi)
    g1 = np.random.default_rng(np.random.SeedSequence([VALIDATION_REPLICATE_MASTER, replicate])); u1 = g1.random((WINDOW, N_CELLS))
    g2 = np.random.default_rng(np.random.SeedSequence([VALIDATION_REPLICATE_MASTER, replicate])); u2 = g2.random((WINDOW, N_CELLS))
    act_lo = u1 < p_lo[None, :]; act_hi = u2 < p_hi[None, :]
    return {"p_hi_dominates_p_lo": bool((p_hi >= p_lo).all()), "same_uniforms_across_levels": bool(np.array_equal(u1, u2)),
            "drawwise_dominance_hi_over_lo": bool(np.all(act_hi | ~act_lo)),
            "counts_lo_first_tick": int(act_lo[0].sum()), "counts_hi_first_tick": int(act_hi[0].sum())}


def memorylessness_witness() -> Dict[str, object]:
    """Public-path witness (L2 M3-7): through the cleared Dynamics.step, an ACTIVE and an INACTIVE
    centre cell with identical bases, zero active neighbours, and the same declared draws receive the
    same p_act and the same next states, with one fresh full-grid draw consumed per tick."""
    from ..dynamics import Dynamics
    from ..init import GridState
    from ..rng import DynamicsStream
    from ..gates.gate_b.stub import FrozenSequenceGenerator
    cfg = _C.e1_run_config(_C.E1_LEVELS_MICRO[12], 7, grid=8, ticks=2)
    out = {}
    for start_active in (False, True):
        grid = np.zeros((8, 8), bool); grid[4, 4] = start_active
        fill = np.full((8, 8), 0.5)
        state = GridState(v=fill.copy(), u_base=fill.copy(), r=fill.copy(), is_active=grid)
        stub = FrozenSequenceGenerator([np.full((8, 8), 0.5), np.full((8, 8), 0.02)], 8)
        model = Dynamics(cfg, state, DynamicsStream(generator=stub), emit_rho_global=True)
        caps = []
        for _ in range(2):
            cap = {}; model.step(lambda t, fl: cap.update({k: np.asarray(v) if hasattr(v, "shape") else v for k, v in fl.items()})); caps.append(cap); stub.next_tick()
        stub.assert_consumed()
        out[start_active] = (float(caps[0]["p_act"][4, 4]), bool(caps[0]["is_active"][4, 4]), bool(caps[1]["is_active"][4, 4]))
    return {"p_act_active_start": out[True][0], "p_act_inactive_start": out[False][0], "same_p_act": out[False][0] == out[True][0],
            "same_next_states": out[False][1:] == out[True][1:], "tick0_next": out[False][1], "tick1_next": out[False][2], "fresh_draw_each_tick": True}
