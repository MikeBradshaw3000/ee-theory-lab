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
"""
from __future__ import annotations

import hashlib
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

NULL_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("n_cells", N_CELLS), ("grid", E1_GRID), ("base_width_micro", E1_BASE_WIDTH_MICRO), ("f_dispatch", "F_canonical"),
    ("constants", E1_CONSTANTS_EXPECTED), ("density_terms", "zero"), ("quantile", NULL_QUANTILE),
    ("window", WINDOW), ("n_windows", N_WINDOWS), ("terminal_windows", TERMINAL_WINDOWS), ("term_ticks", TERM_TICKS),
    ("template_master", NULL_TEMPLATE_MASTER), ("template_role", NULL_TEMPLATE_ROLE), ("template_sha256", NULL_TEMPLATE_SHA256_LITERAL),
    ("law", "exact_poisson_binomial"), ("evaluation", "float64_fft"),
    ("error_bound_factor", NULL_ERROR_BOUND_FACTOR), ("error_bound_floor", NULL_ERROR_BOUND_FLOOR),
)
NULL_DECLARATION_SHA256_LITERAL = "8aac1ef282b4bef4baa210124021729e863bb1e1f2fe94e1b64ee5fd7ac59ee0"   # established 2026-09-17; verified at every entry point


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def verify_frozen_identity() -> None:
    """Fail-closed (L2 M3-1): the M1 and M2 identities; every declaration field equal to its live
    global; the declared constants equal to the committed E1 constants; the template, quantile,
    support, and method identities."""
    _C.verify_frozen_identity(); _K.verify_frozen_identity()
    if _digest(NULL_DECLARATION) != NULL_DECLARATION_SHA256_LITERAL:
        raise NullDomainError("null declaration differs from its frozen literal digest")
    d = dict(NULL_DECLARATION)
    live = {"n_cells": N_CELLS, "grid": E1_GRID, "base_width_micro": E1_BASE_WIDTH_MICRO, "f_dispatch": "F_canonical",
            "constants": E1_CONSTANTS_EXPECTED, "density_terms": "zero", "quantile": NULL_QUANTILE, "window": WINDOW, "n_windows": N_WINDOWS,
            "terminal_windows": TERMINAL_WINDOWS, "term_ticks": TERM_TICKS, "template_master": NULL_TEMPLATE_MASTER,
            "template_role": NULL_TEMPLATE_ROLE, "template_sha256": NULL_TEMPLATE_SHA256_LITERAL, "law": "exact_poisson_binomial",
            "evaluation": "float64_fft", "error_bound_factor": NULL_ERROR_BOUND_FACTOR, "error_bound_floor": NULL_ERROR_BOUND_FLOOR}
    for k, v in live.items():
        if d[k] != v or type(d[k]) is not type(v):
            raise NullDomainError(f"null declaration field {k} differs from the live global")
    if N_CELLS != E1_GRID * E1_GRID or N_CELLS != _K.N_CELLS or TERM_TICKS != 300 or NULL_QUANTILE != 0.99 or N_WINDOWS != 10:
        raise NullDomainError("null support/quantile/window count inconsistent with M1/M2 or the hard values")
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
    """The frozen production template: regenerated once, digest-verified at EVERY call (L2 M3-2),
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
    """PRODUCTION: the frozen template and the declared E1 constants only (no override parameters)."""
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
    reps = _exact_pos_int(reps, "reps")
    base, cert_base = per_tick_count_pmf(p)
    n = reps * (base.size - 1)
    padded = np.zeros(n + 1); padded[:base.size] = base
    return _clean(np.fft.ifft(np.fft.fft(padded) ** reps), reps, tick_l1_bound=cert_base.sum_l1_bound)


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
    if N_WINDOWS != 10 or dict(NULL_DECLARATION)["n_windows"] != N_WINDOWS:
        raise NullDomainError("N_WINDOWS differs from the frozen value 10")
    return float(N_WINDOWS)


def final_cdf_bounds(cert_w: PmfCertificate, cert_t: PmfCertificate) -> Tuple[float, float]:
    """The bounds on the TWO FINAL CDFs that select the thresholds (L2 r3 M3-3): F_min through the
    min-of-N_WINDOWS map (derivative ≤ N_WINDOWS, derived, never a free constant) and F_term directly."""
    return f_min_derivative_bound() * error_bound(cert_w), error_bound(cert_t)


@dataclass(frozen=True)
class QuantileCertificate:
    index: int                       # k* = inf{k : F(k) ≥ q}
    value: float                     # float64 of k*/denominator (the grid value)
    cdf_below: float                 # F(k*−1)
    cdf_at: float                    # F(k*)
    margin_below: float              # q − F(k*−1)
    margin_at: float                 # F(k*) − q
    error_bound: float
    certified: bool                  # both margins exceed the error bound


def _quantile(cdf: np.ndarray, denom: int, final_cdf_bound: float) -> QuantileCertificate:
    """The quantile of a FINAL CDF with the FINAL-CDF error bound (never a component pmf's)."""
    k = int(np.searchsorted(cdf, NULL_QUANTILE, side="left"))
    below = float(cdf[k - 1]) if k > 0 else 0.0; at = float(cdf[k])
    mb, ma = NULL_QUANTILE - below, at - NULL_QUANTILE
    return QuantileCertificate(k, float(np.float64(k) / np.float64(denom)), below, at, mb, ma, final_cdf_bound, bool(mb > final_cdf_bound and ma > final_cdf_bound))


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

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


def null_thresholds(level_micro: int) -> NullThresholds:
    """PRODUCTION thresholds for one level: identity verified; frozen template and declared constants
    only; both quantiles certified or the call is REFUSED."""
    verify_frozen_identity()
    p = null_p_act(level_micro)
    pmf_w, cert_w = poisson_binomial_pmf(p, WINDOW)
    pmf_t, cert_t = poisson_binomial_pmf(p, TERM_TICKS)
    b_min, b_term = final_cdf_bounds(cert_w, cert_t)
    cdf_min = 1.0 - (1.0 - np.cumsum(pmf_w)) ** N_WINDOWS
    qp = _quantile(cdf_min, WINDOW * N_CELLS, b_min)
    qt = _quantile(np.cumsum(pmf_t), TERM_TICKS * N_CELLS, b_term)
    if not (qp.certified and qt.certified):
        raise NullDomainError(f"quantile not numerically certified at level {level_id(level_micro)}: theta_P {qp}, theta_T {qt}")
    return NullThresholds(int(level_micro), level_id(level_micro), qp.value, qt.value, qp, qt, cert_w, cert_t, float(np.mean(p)),
                          "exact_poisson_binomial", "float64_fft", 0.0, True)


# ----------------------------------------------------------------------------- validation program (frozen)
VALIDATION_LEVELS_MICRO: Tuple[int, ...] = (150000, 515217, 850000)      # low, middle, high pass-1 levels
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
    ("direct_path_rule", "final-CDF max abs diff (+ discarded mass) <= final-CDF bound; identical quantile indices"),
    ("completion", "all three declared levels, both statistics, every comparison"),
)
VALIDATION_SHA256_LITERAL = "3cf3da8003ed73328c02b45af42a2ebe920d92bc866bef35ed42715a57fa5445"   # established 2026-09-18 (amended: frozen acceptance values)


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
    thr = null_thresholds(level_micro); p = null_p_act(level_micro)
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
    thr = null_thresholds(level_micro); p = null_p_act(level_micro)
    fft_tick, cert_tick = per_tick_count_pmf(p); dp_tick = per_tick_count_pmf_dp(p)
    fft_w, cert_w = poisson_binomial_pmf(p, WINDOW); fft_t, cert_t = poisson_binomial_pmf(p, TERM_TICKS)
    dir_w, disc_w = direct_convolution_pmf_truncated(p, WINDOW); dir_t, disc_t = direct_convolution_pmf_truncated(p, TERM_TICKS)
    cdf_min_fft = 1.0 - (1.0 - np.cumsum(fft_w)) ** N_WINDOWS; cdf_min_dir = 1.0 - (1.0 - np.cumsum(dir_w)) ** N_WINDOWS
    cdf_t_fft = np.cumsum(fft_t); cdf_t_dir = np.cumsum(dir_t)
    b_min, b_term = final_cdf_bounds(cert_w, cert_t)
    k_min_dir = int(np.searchsorted(cdf_min_dir, NULL_QUANTILE, side="left")); k_t_dir = int(np.searchsorted(cdf_t_dir, NULL_QUANTILE, side="left"))
    return {"tick_max_abs_diff": float(np.max(np.abs(fft_tick - dp_tick))), "tick_error_bound": error_bound(cert_tick),
            "fmin_cdf_max_abs_diff": float(np.max(np.abs(cdf_min_fft - cdf_min_dir))) + disc_w, "fmin_final_bound": b_min,
            "fterm_cdf_max_abs_diff": float(np.max(np.abs(cdf_t_fft - cdf_t_dir))) + disc_t, "fterm_final_bound": b_term,
            "direct_discarded_mass_w": disc_w, "direct_discarded_mass_t": disc_t,
            "theta_p_index_fft": float(thr.theta_p_certificate.index), "theta_p_index_direct": float(k_min_dir),
            "theta_t_index_fft": float(thr.theta_t_certificate.index), "theta_t_index_direct": float(k_t_dir)}


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
    d = dict(VALIDATION_DECLARATION)
    if (d["quantile_allowance"], d["exceedance_cap"], d["dkw_alpha"], d["replicates"]) != (VALIDATION_QUANTILE_ALLOWANCE, VALIDATION_EXCEEDANCE_CAP, VALIDATION_DKW_ALPHA, VALIDATION_REPLICATES) \
            or (VALIDATION_QUANTILE_ALLOWANCE, VALIDATION_EXCEEDANCE_CAP, VALIDATION_DKW_ALPHA, VALIDATION_REPLICATES) != (5e-4, 0.03, 0.05, 400):
        raise NullDomainError("validation acceptance values differ from the frozen declaration or the hard contract values")
    ok = all(v["sup_dev_term"] <= v["dkw_bound"] and v["sup_dev_min"] <= v["dkw_bound"]
             and abs(v["theta_t_mc"] - v["theta_t_exact"]) < d["quantile_allowance"] and abs(v["theta_p_mc"] - v["theta_p_exact"]) < d["quantile_allowance"]
             and v["frac_term_exceeding"] <= d["exceedance_cap"] and v["frac_min_exceeding"] <= d["exceedance_cap"] for v in out)
    ok = ok and all(n["tick_max_abs_diff"] <= n["tick_error_bound"] and n["fmin_cdf_max_abs_diff"] <= n["fmin_final_bound"]
                    and n["fterm_cdf_max_abs_diff"] <= n["fterm_final_bound"]
                    and n["theta_p_index_fft"] == n["theta_p_index_direct"] and n["theta_t_index_fft"] == n["theta_t_index_direct"] for n in nums)
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
