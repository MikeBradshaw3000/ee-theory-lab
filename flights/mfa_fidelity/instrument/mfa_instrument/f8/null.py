"""mfa_instrument/f8/null.py — Flight 8 module M3: the Markov null and the threshold object
(Contract F8 v0.8.4 §2.9, §4.3; design note v0.3 §4; Mike/L2 ruling of 2026-10-20: route (a) for θ_T, route (b)
for θ_P, route (c) the named fallback).

THE NULL (§2.9): g = 0, η_floor = η₀, μ; each cell an independent two-state chain with a = 1 − e^(−η₀Δt),
q = 1 − e^(−μΔt), started in its stationary distribution π₁ = a/(a + q), no burn-in. The bases are inert, so the
null — and every threshold — is the same at every level; thresholds are still cached per level so the record
grammar carries unchanged (§4.3 note).

THE LAW. For one cell started stationary, the occupancy of any 100-tick window, O = Σ x_t, is a Markov-binomial on
0..100 whose pmf is computed EXACTLY by the two-state transfer-matrix dynamic programme (state = (x_t, count so far)).
By stationarity every window — the terminal window included — has the same marginal law. The window active-count
total over N = 2,500 independent cells is the N-fold convolution of that pmf, on 0..250,000; its CDF F_W is the law
of a single window's count. Then (§4.3):
  θ_T  = inf{x : F_W(x) ≥ 1 − α_T}            on the count grid /250,000, α_T = 0.001        [route (a), exact]
  θ_P  = inf{x : F_W(x) ≥ 1 − α_P/N_WINDOWS}   the per-window marginal at 1 − 0.0001           [route (b), familywise]
so that P_null(S_min > θ_P) ≤ P_null(some window > θ_P) ≤ N_WINDOWS·α_P/N_WINDOWS = α_P. The construction is
conservative by design; its realized conservatism is PRICED at qualification by the empirical null rejection rate
against α_P (`price_familywise`, run on the F8 stepper itself at g = 0, replicate master declared below).

TWO THINGS, KEPT SEPARATE (E1 M3's discipline, carried): the LAW is exact; its EVALUATION here is float64 — the
per-cell pmf by the DP (checked against an EXACT RATIONAL evaluation of the same DP: a and q are the float64 values
the stepper uses, so the rational DP on Fraction(a), Fraction(q) is exact for the law the instrument realizes), the
N-fold convolution by FFT power with a numerical certificate (imaginary residual, negative mass, normalisation,
clip correction) and an independent truncated direct-convolution path. A threshold is CERTIFIED only when the CDF
margins on both sides of its quantile crossing exceed a conservative error bound; otherwise the CONSERVATIVE
CERTIFIED COVERAGE THRESHOLD k_safe = min{k : F̂(k) − ε ≥ q} is selected and recorded as such (E1 M3 amendment
grammar carried). Monte Carlo validation runs the actual F8 stepper under the `null` object and checks the
empirical window-count CDF against F_W (DKW) and the exceedance rates against α_T and α_P/N_WINDOWS.
"""
from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import classify as K
from . import config as C
from . import dynamics as D
from .classify import N_CELLS, N_WINDOWS, WINDOW

ALPHA_T = 0.001                                    # [ratified: freeze record §3 item 8]
ALPHA_P = 0.001                                    # familywise (idem)
Q_T = 1.0 - ALPHA_T                                # 0.999
Q_P = 1.0 - ALPHA_P / N_WINDOWS                    # 0.9999: per-window marginal quantile, route (b)
WINDOW_DENOM = WINDOW * N_CELLS                    # 250,000: the count grid of a window mean
NULL_ERROR_BOUND_FACTOR = 1000.0                   # conservative multiplier on measured float64 residual indicators (E1 M3, carried)
NULL_ERROR_BOUND_FLOOR = 1e-9                      # never certify a crossing closer than this to the quantile (E1 M3, carried)
THRESHOLD_MODES_SET = ("exact_certified", "conservative_coverage")
VALIDATION_REPLICATE_MASTER = 220261026            # declared: the null-validation replicate master (separate from all panels)
VALIDATION_DKW_ALPHA = 0.05
VALIDATION_UNION_ALPHA = VALIDATION_DKW_ALPHA / N_WINDOWS   # per-window level of the dependence-valid union test over the ten windows
VALIDATION_TICKS = 1100                            # declared validation shape: full N, ten tail windows; the null is stationary from t = 0,
                                                   # so the pre-tail ticks do not enter the law; NOT the production shape (M1 panel policy)
DIRECT_TAIL_CUT = 1e-30
SCORING_OBJECT_VERSION = "f8_markov_null_v1"

NULL_DECLARATION: Tuple[Tuple[str, object], ...] = (
    ("scoring_object_version", SCORING_OBJECT_VERSION), ("mu", C.F8_MU), ("eta0", C.F8_ETA0), ("dt", C.F8_DT), ("n_cells", N_CELLS),
    ("window", WINDOW), ("n_windows", N_WINDOWS), ("window_denominator", WINDOW_DENOM), ("start", "stationary_no_burn_in"),
    ("alpha_T", ALPHA_T), ("alpha_P", ALPHA_P), ("q_T", Q_T), ("q_P", Q_P), ("theta_T_route", "a_exact_transfer_matrix"),
    ("theta_P_route", "b_familywise_per_window_marginal"), ("fallback", "c_qualified_simulation_threshold"),
    ("error_bound_factor", NULL_ERROR_BOUND_FACTOR), ("error_bound_floor", NULL_ERROR_BOUND_FLOOR), ("modes", THRESHOLD_MODES_SET),
    ("validation_replicate_master", VALIDATION_REPLICATE_MASTER), ("validation_ticks", VALIDATION_TICKS), ("direct_tail_cut", DIRECT_TAIL_CUT),
    ("validation_dkw_alpha", VALIDATION_DKW_ALPHA), ("validation_union_alpha", VALIDATION_UNION_ALPHA),
)
NULL_SHA256_LITERAL = "bfe0a5a0067cae7ca524cc2ba299219ce89007e794d8703a9872869388e9c05c"


class NullDomainError(ValueError):
    """The null object is asked for something outside its frozen domain, or an identity fails."""


def _digest(obj) -> str:
    return hashlib.sha256(repr(obj).encode()).hexdigest()


def verify_frozen_identity() -> None:
    if _digest(NULL_DECLARATION) != NULL_SHA256_LITERAL:
        raise NullDomainError("null declaration differs from its frozen literal digest")
    K.verify_frozen_identity()
    d = dict(NULL_DECLARATION)
    live = {"mu": C.F8_MU, "eta0": C.F8_ETA0, "dt": C.F8_DT, "n_cells": N_CELLS, "window": WINDOW, "n_windows": N_WINDOWS, "window_denominator": WINDOW_DENOM,
            "alpha_T": ALPHA_T, "alpha_P": ALPHA_P, "q_T": Q_T, "q_P": Q_P, "error_bound_factor": NULL_ERROR_BOUND_FACTOR, "error_bound_floor": NULL_ERROR_BOUND_FLOOR,
            "modes": THRESHOLD_MODES_SET, "validation_replicate_master": VALIDATION_REPLICATE_MASTER, "validation_ticks": VALIDATION_TICKS, "validation_dkw_alpha": VALIDATION_DKW_ALPHA, "validation_union_alpha": VALIDATION_UNION_ALPHA, "direct_tail_cut": DIRECT_TAIL_CUT, "scoring_object_version": SCORING_OBJECT_VERSION}
    for k_, v in live.items():
        if d[k_] != v or type(d[k_]) is not type(v):
            raise NullDomainError(f"null declaration field {k_} differs from the live global")
    if (ALPHA_T, ALPHA_P, N_WINDOWS, WINDOW_DENOM) != (0.001, 0.001, 10, 250000) or Q_T != 1.0 - 0.001 or Q_P != 1.0 - 0.001 / 10:
        raise NullDomainError("null constants differ from the contracted values (§4.3; freeze record §3 item 8)")
    if VALIDATION_REPLICATE_MASTER in (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER, 20260917):
        raise NullDomainError("validation replicate master collides with a panel master")


# ----------------------------------------------------------------------------- the chain
def chain_rates(eta_floor: float = C.F8_ETA0, mu: float = C.F8_MU, dt: int = C.F8_DT) -> Tuple[float, float, float]:
    """(a, q, π₁) exactly as the stepper evaluates them: a = 1 − exp(−η dt), q = 1 − exp(−μ dt) (f8.dynamics)."""
    a = float(D.activation_probability(eta_floor, 0.0, 0.0, np.zeros(1), dt)[0]); q = D.deactivation_probability(mu, dt)
    return a, q, D.stationary_pi1(eta_floor, mu, dt)


def cell_window_pmf(a: float, q: float, pi1: float, window: int = WINDOW) -> np.ndarray:
    """Occupancy pmf of one stationary two-state cell over `window` ticks, by the transfer-matrix DP (float64).
    State after t ticks: f[x][c] = P(x_t = x, Σ_{s≤t} x_s = c), with x_1 ~ (1 − π₁, π₁) counted."""
    f0 = np.zeros(window + 1); f1 = np.zeros(window + 1)
    f0[0] = 1.0 - pi1; f1[1] = pi1
    for _ in range(window - 1):
        n0 = f0 * (1.0 - a) + f1 * q
        n1 = np.zeros(window + 1); n1[1:] = f0[:-1] * a + f1[:-1] * (1.0 - q)
        f0, f1 = n0, n1
    return f0 + f1


def cell_window_pmf_exact(a: float, q: float, pi1: float, window: int = WINDOW) -> List[Fraction]:
    """INDEPENDENT second path: the same DP in exact rational arithmetic on Fraction(a), Fraction(q), Fraction(pi1)
    (the float64 inputs the stepper uses, taken as exact). Exact for the realized law; no rounding anywhere."""
    A, Qd, P1 = Fraction(a), Fraction(q), Fraction(pi1)
    f0 = [Fraction(0)] * (window + 1); f1 = [Fraction(0)] * (window + 1)
    f0[0] = 1 - P1; f1[1] = P1
    for _ in range(window - 1):
        n0 = [f0[c] * (1 - A) + f1[c] * Qd for c in range(window + 1)]
        n1 = [Fraction(0)] + [f0[c] * A + f1[c] * (1 - Qd) for c in range(window)]
        f0, f1 = n0, n1
    return [f0[c] + f1[c] for c in range(window + 1)]


def window_lag1_correlation(a: float, q: float, pi1: float, n_cells: int = N_CELLS, window: int = WINDOW) -> float:
    """EXACT correlation between the active-count totals of two CONSECUTIVE windows of the stationary null: with
    ρ = 1 − a − q the per-tick autocorrelation, Cov(x_s, x_t) = π₁(1 − π₁)ρ^|t−s|, summed over s in window j and t in
    window j+1, independent across cells. Consecutive windows are NOT independent (L2 M2/M3 r1 D1): the boundary ticks
    carry ρ¹ ≈ 0.81, and the sum is ≈ 0.025 at the frozen rates. This is why the inferential statistics use either one
    designated window per replicate or a union bound over windows, never the pooled sample as if independent."""
    r = 1.0 - a - q; v = pi1 * (1.0 - pi1)
    cov = n_cells * v * sum(r ** (t - s) for s in range(window) for t in range(window, 2 * window))
    var = n_cells * v * sum(r ** abs(t - s) for s in range(window) for t in range(window))
    return float(cov / var)


# ----------------------------------------------------------------------------- certificates (E1 M3 grammar, carried)
@dataclass(frozen=True)
class PmfCertificate:
    reps: int
    support: int
    max_imag_residual: float
    total_negative_mass: float
    most_negative_coefficient: float
    raw_normalisation_error: float
    clip_renorm_correction: float
    factor_l1_bound: float            # L1 error bound of the per-cell pmf this sum was built from
    sum_l1_bound: float               # reps·factor_l1_bound + own residual bound (convolution is L1-contractive)

    def __post_init__(self) -> None:
        validate_pmf_certificate(self)


def _own_bound(imag: float, total_neg: float, raw_norm_err: float, correction: float) -> float:
    return max(NULL_ERROR_BOUND_FLOOR, NULL_ERROR_BOUND_FACTOR * max(imag, total_neg, abs(raw_norm_err), correction))


def validate_pmf_certificate(c) -> None:
    if type(c) is not PmfCertificate:
        raise NullDomainError("validate_pmf_certificate requires an exact PmfCertificate")
    for name in ("reps", "support"):
        x = getattr(c, name)
        if isinstance(x, bool) or not isinstance(x, int) or x <= 0:
            raise NullDomainError(f"PMF certificate {name} must be an exact positive integer")
    vals = (c.max_imag_residual, c.total_negative_mass, c.most_negative_coefficient, c.raw_normalisation_error, c.clip_renorm_correction, c.factor_l1_bound, c.sum_l1_bound)
    if not all(isinstance(x, float) and math.isfinite(x) for x in vals):
        raise NullDomainError("PMF certificate fields must be finite floats")
    if c.max_imag_residual < 0.0 or c.total_negative_mass < 0.0 or c.most_negative_coefficient > 0.0 or c.clip_renorm_correction < 0.0 or c.factor_l1_bound <= 0.0 or c.sum_l1_bound <= 0.0:
        raise NullDomainError("PMF certificate fields have inadmissible signs")
    if c.support != c.reps * WINDOW:
        raise NullDomainError("PMF certificate support must be reps × WINDOW")
    own = _own_bound(c.max_imag_residual, c.total_negative_mass, c.raw_normalisation_error, c.clip_renorm_correction)
    if c.reps == 1:
        if not (c.factor_l1_bound == own and c.sum_l1_bound == own):
            raise NullDomainError("per-cell certificate must carry factor == sum == its own recomputed bound")
    elif c.sum_l1_bound != c.reps * c.factor_l1_bound + own:
        raise NullDomainError("convolution certificate must satisfy sum == reps × factor + own recomputed bound")


def _clean(raw: np.ndarray, reps: int, factor_l1_bound: float) -> Tuple[np.ndarray, PmfCertificate]:
    real = np.real(raw); imag = float(np.max(np.abs(np.imag(raw)))) if np.iscomplexobj(raw) else 0.0
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
    if reps == 1:
        return cleaned, PmfCertificate(1, real.size - 1, imag, total_neg, most_neg, raw_norm_err, correction, own, own)
    return cleaned, PmfCertificate(reps, real.size - 1, imag, total_neg, most_neg, raw_norm_err, correction, factor_l1_bound, reps * factor_l1_bound + own)


def certified_cell_pmf(a: float, q: float, pi1: float) -> Tuple[np.ndarray, PmfCertificate, float]:
    """The per-cell pmf (float64 DP) with its certificate; the factor bound is max(floor, factor × measured L1 distance
    to the EXACT rational DP), so the bound is measured against an exact path, never assumed. Returns the measured
    distance too."""
    f = cell_window_pmf(a, q, pi1); ex = cell_window_pmf_exact(a, q, pi1)
    dist = float(sum(abs(Fraction(float(x)) - e) for x, e in zip(f, ex)))
    cleaned, cert = _clean(f, 1, 0.0)
    bound = max(cert.factor_l1_bound, NULL_ERROR_BOUND_FACTOR * dist, NULL_ERROR_BOUND_FLOOR)
    cert = PmfCertificate(1, cert.support, cert.max_imag_residual, cert.total_negative_mass, cert.most_negative_coefficient,
                          cert.raw_normalisation_error, max(cert.clip_renorm_correction, bound / NULL_ERROR_BOUND_FACTOR), bound, bound)
    return cleaned, cert, dist


def window_count_pmf(cell_pmf: np.ndarray, cell_cert: PmfCertificate, n_cells: int = N_CELLS) -> Tuple[np.ndarray, PmfCertificate]:
    """The N-fold convolution by FFT power on the exact support 0..N·WINDOW; cleaned and certified."""
    size = n_cells * WINDOW + 1
    phi = np.fft.fft(cell_pmf, n=size)
    raw = np.fft.ifft(phi ** n_cells)
    return _clean(raw, n_cells, cell_cert.sum_l1_bound)


def direct_convolution_pmf_truncated(cell_pmf: np.ndarray, n_cells: int = N_CELLS, tail_cut: float = DIRECT_TAIL_CUT) -> Tuple[np.ndarray, int, float]:
    """INDEPENDENT second path (no FFT): binary-exponentiation direct convolution with support truncation at mass
    below tail_cut, tracking the discarded mass. Returns (pmf on 0..N·WINDOW, offset-free), offset, discarded mass."""
    def trunc(p: np.ndarray, off: int) -> Tuple[np.ndarray, int, float]:
        nz = np.nonzero(p > tail_cut)[0]
        lo, hi = int(nz[0]), int(nz[-1])
        disc = float(p[:lo].sum() + p[hi + 1:].sum())
        return p[lo:hi + 1], off + lo, disc
    base, boff, discarded = trunc(cell_pmf.copy(), 0)
    res, roff = np.array([1.0]), 0
    n = n_cells
    while n:
        if n & 1:
            res, roff, d = trunc(np.convolve(res, base), roff + boff); discarded += d
        n >>= 1
        if n:
            base, boff, d = trunc(np.convolve(base, base), 2 * boff); discarded += d
    full = np.zeros(n_cells * WINDOW + 1); full[roff:roff + res.size] = res
    return full, roff, discarded


# ----------------------------------------------------------------------------- quantile certification
@dataclass(frozen=True)
class QuantileCertificate:
    quantile: float
    index: int
    value: float
    cdf_below: float
    cdf_at: float
    margin_below: float
    margin_at: float
    error_bound: float
    certified: bool
    mode: str
    ordinary_index: int
    ordinary_certifiable: bool
    conservative_index: int
    displacement: int
    cdf_at_selected: float
    denominator: int

    def __post_init__(self) -> None:
        validate_quantile_certificate(self)


def validate_quantile_certificate(self) -> None:
    if type(self) is not QuantileCertificate:
        raise NullDomainError("validate_quantile_certificate requires an exact QuantileCertificate")
    q = self.quantile
    if not isinstance(q, float) or q not in (Q_T, Q_P):
        raise NullDomainError("certificate quantile must be the contracted q_T or q_P")
    if isinstance(self.denominator, bool) or not isinstance(self.denominator, int) or self.denominator != WINDOW_DENOM:
        raise NullDomainError("certificate denominator must be the window count grid")
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
        raise NullDomainError("the ordinary crossing must straddle q")
    ordinary_ok = bool(self.margin_below > self.error_bound and self.margin_at > self.error_bound)
    if self.ordinary_certifiable is not ordinary_ok:
        raise NullDomainError("ordinary_certifiable must equal the computed margin test")
    if self.mode == "exact_certified":
        if not (ordinary_ok and self.index == self.ordinary_index and self.cdf_at_selected == self.cdf_at):
            raise NullDomainError("exact mode must select the certified ordinary crossing")
    elif ordinary_ok or self.index != self.conservative_index or not (self.cdf_at_selected - self.error_bound >= q):
        raise NullDomainError("conservative mode requires an uncertifiable ordinary crossing and F_hat(k_safe) - eps >= q")
    if not self.certified:
        raise NullDomainError("a constructed certificate is certified by construction")


def _quantile(cdf: np.ndarray, q: float, eps: float) -> QuantileCertificate:
    k = int(np.searchsorted(cdf, q, side="left"))
    if k >= cdf.size: raise NullDomainError("quantile beyond the support")
    below = float(cdf[k - 1]) if k > 0 else 0.0; at = float(cdf[k])
    mb, ma = q - below, at - q
    ordinary_ok = bool(mb > eps and ma > eps)
    k_safe = int(np.searchsorted(cdf, q + eps, side="left"))
    if k_safe >= cdf.size or not (float(cdf[k_safe]) - eps >= q):
        raise NullDomainError("no support point clears the conservative coverage condition F_hat(k) - eps >= q")
    if ordinary_ok:
        return QuantileCertificate(q, k, float(np.float64(k) / np.float64(WINDOW_DENOM)), below, at, mb, ma, eps, True, "exact_certified", k, True, k_safe, k_safe - k, at, WINDOW_DENOM)
    return QuantileCertificate(q, k_safe, float(np.float64(k_safe) / np.float64(WINDOW_DENOM)), below, at, mb, ma, eps, True, "conservative_coverage", k, False, k_safe, k_safe - k, float(cdf[k_safe]), WINDOW_DENOM)


# ----------------------------------------------------------------------------- the threshold object
@dataclass(frozen=True)
class NullThresholds:
    level_micro: int
    level_id: str
    theta_p: float
    theta_t: float
    theta_p_certificate: QuantileCertificate
    theta_t_certificate: QuantileCertificate
    cell_pmf_certificate: PmfCertificate
    window_pmf_certificate: PmfCertificate
    cell_exact_l1_distance: float          # measured float-vs-exact-rational distance of the per-cell pmf
    direct_max_cdf_discrepancy: float      # max |F_fft − F_direct| over the support
    direct_discarded_mass: float
    direct_agrees: bool                    # both ordinary indices agree between the FFT and direct paths
    a: float
    q: float
    pi1: float
    null_mean_density: float
    scoring_object_version: str
    declaration_sha256: str

    def __post_init__(self) -> None:
        validate_null_thresholds(self)

    def payload_identity(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def validate_null_thresholds(th) -> None:
    if type(th) is not NullThresholds:
        raise NullDomainError("validate_null_thresholds requires an exact NullThresholds")
    for c in (th.theta_p_certificate, th.theta_t_certificate): validate_quantile_certificate(c)
    for pc in (th.cell_pmf_certificate, th.window_pmf_certificate): validate_pmf_certificate(pc)
    if th.cell_pmf_certificate.reps != 1 or th.window_pmf_certificate.reps != N_CELLS:
        raise NullDomainError("certificate reps must be 1 (cell) and N_CELLS (window)")
    if th.window_pmf_certificate.factor_l1_bound != th.cell_pmf_certificate.sum_l1_bound:
        raise NullDomainError("the window certificate must inherit the cell certificate's bound exactly")
    eps = th.window_pmf_certificate.sum_l1_bound
    if th.theta_p_certificate.error_bound != eps or th.theta_t_certificate.error_bound != eps:
        raise NullDomainError("both quantile certificates must carry the window pmf's final-CDF bound")
    if th.theta_p_certificate.quantile != Q_P or th.theta_t_certificate.quantile != Q_T:
        raise NullDomainError("certificate quantiles must be q_P (theta_P) and q_T (theta_T)")
    if th.theta_p != th.theta_p_certificate.value or th.theta_t != th.theta_t_certificate.value:
        raise NullDomainError("thresholds must equal their certificates' values")
    if th.theta_p < th.theta_t:
        raise NullDomainError("theta_P (quantile 0.9999) cannot lie below theta_T (quantile 0.999)")
    if th.level_id != C.level_id(th.level_micro) or th.level_micro not in C.F8_LEVELS_MICRO:
        raise NullDomainError("level identity is not a frozen pass-1 level")
    a, q, pi1 = chain_rates()
    if (th.a, th.q, th.pi1) != (a, q, pi1) or th.null_mean_density != pi1:
        raise NullDomainError("chain rates differ from the frozen rule's")
    if th.scoring_object_version != SCORING_OBJECT_VERSION or th.declaration_sha256 != NULL_SHA256_LITERAL:
        raise NullDomainError("scoring object version / declaration identity mismatch")
    if not th.direct_agrees:
        raise NullDomainError("the FFT and direct paths disagree on the ordinary crossings")
    if th.direct_max_cdf_discrepancy > eps:
        raise NullDomainError("FFT/direct CDF discrepancy exceeds the certified error bound")


_LAW_CACHE: Dict[Tuple[float, float, float], Tuple] = {}


def window_count_law() -> Tuple[np.ndarray, np.ndarray, PmfCertificate, PmfCertificate, float, float, float, bool]:
    """The window-count pmf and CDF with both certificates and the direct-path comparison. Level-independent; memoised."""
    verify_frozen_identity()
    a, q, pi1 = chain_rates()
    key = (a, q, pi1)
    if key in _LAW_CACHE: return _LAW_CACHE[key]
    cell, cell_cert, dist = certified_cell_pmf(a, q, pi1)
    pmf, w_cert = window_count_pmf(cell, cell_cert)
    cdf = np.cumsum(pmf); cdf[-1] = 1.0
    direct, _, disc = direct_convolution_pmf_truncated(cell)
    dcdf = np.cumsum(direct); dcdf = dcdf / dcdf[-1]
    disc_max = float(np.max(np.abs(cdf - dcdf)))
    agree = all(int(np.searchsorted(cdf, qq, side="left")) == int(np.searchsorted(dcdf, qq, side="left")) for qq in (Q_T, Q_P))
    _LAW_CACHE[key] = (pmf, cdf, cell_cert, w_cert, dist, disc_max, disc, agree)
    return _LAW_CACHE[key]


def null_thresholds(level_micro: int) -> NullThresholds:
    """θ_P, θ_T for a frozen pass-1 level (the law is level-independent; the record is per level, §4.3)."""
    verify_frozen_identity()
    if isinstance(level_micro, bool) or not isinstance(level_micro, (int, np.integer)) or int(level_micro) not in C.F8_LEVELS_MICRO:
        raise NullDomainError("thresholds are defined only at the frozen pass-1 levels")
    level_micro = int(level_micro)
    pmf, cdf, cell_cert, w_cert, dist, disc_max, disc, agree = window_count_law()
    eps = w_cert.sum_l1_bound
    a, q, pi1 = chain_rates()
    cp, ct = _quantile(cdf, Q_P, eps), _quantile(cdf, Q_T, eps)
    return NullThresholds(level_micro, C.level_id(level_micro), cp.value, ct.value, cp, ct, cell_cert, w_cert, dist, disc_max, disc, bool(agree),
                          a, q, pi1, pi1, SCORING_OBJECT_VERSION, NULL_SHA256_LITERAL)


def familywise_nominal_bound(th: NullThresholds) -> float:
    """P_null(S_min > θ_P) ≤ N_WINDOWS·(1 − F_W(θ_P)) — the Bonferroni-type bound the construction guarantees (≤ α_P)."""
    return float(N_WINDOWS * (1.0 - th.theta_p_certificate.cdf_at_selected))


# ----------------------------------------------------------------------------- the per-level cache record
@dataclass(frozen=True)
class ThresholdCache:
    role: str                                   # "production" | "slice"
    levels_micro: Tuple[int, ...]
    entries: Tuple[Tuple[str, float, float, str], ...]   # (level_id, theta_p, theta_t, payload identity)
    law_identity: str                           # identity of the (level-independent) window-count law object
    declaration_sha256: str
    n_levels: int


def build_threshold_cache(levels: Optional[Sequence[int]] = None, role: str = "production") -> ThresholdCache:
    verify_frozen_identity()
    if role not in ("production", "slice"): raise NullDomainError("cache role must be production or slice")
    lv = tuple(C.F8_LEVELS_MICRO) if levels is None else tuple(int(x) for x in levels)
    if role == "production" and lv != tuple(C.F8_LEVELS_MICRO): raise NullDomainError("a production cache covers exactly the frozen pass-1 levels")
    if len(set(lv)) != len(lv) or any(x not in C.F8_LEVELS_MICRO for x in lv): raise NullDomainError("cache levels must be distinct frozen pass-1 levels")
    ths = [null_thresholds(m) for m in lv]
    entries = tuple((t.level_id, t.theta_p, t.theta_t, t.payload_identity()) for t in ths)
    law = ths[0].payload_identity() if ths else ""
    return ThresholdCache(role, lv, entries, law, NULL_SHA256_LITERAL, len(lv))


def validate_threshold_cache(cache: ThresholdCache) -> None:
    """Validation is by REPLAY: every entry recomputed and compared, identity by identity."""
    if type(cache) is not ThresholdCache: raise NullDomainError("not a ThresholdCache")
    rebuilt = build_threshold_cache(cache.levels_micro, cache.role)
    if rebuilt != cache: raise NullDomainError("threshold cache does not replay to its recorded content")


def cache_to_json(cache: ThresholdCache) -> str:
    return json.dumps({"__type__": "F8ThresholdCache", "fields": asdict(cache)}, sort_keys=True, separators=(",", ":"), allow_nan=False)


def cache_from_json(text: str) -> ThresholdCache:
    doc = json.loads(text, parse_constant=lambda c: (_ for _ in ()).throw(NullDomainError(f"nonfinite constant {c}")))
    if doc.get("__type__") != "F8ThresholdCache": raise NullDomainError("not an F8ThresholdCache document")
    f = doc["fields"]
    cache = ThresholdCache(f["role"], tuple(int(x) for x in f["levels_micro"]), tuple((e[0], float(e[1]), float(e[2]), e[3]) for e in f["entries"]),
                           f["law_identity"], f["declaration_sha256"], int(f["n_levels"]))
    validate_threshold_cache(cache)
    return cache


# ----------------------------------------------------------------------------- validation on the stepper (Monte Carlo)
@dataclass(frozen=True)
class ValidationProtocol:
    """A PROSPECTIVELY REGISTERED null-validation protocol (L2 M2/M3 r2 H1): everything that decides pass/fail is fixed
    here, identified, and ratified by Mike BEFORE the run. A NullValidation names the protocol it was produced under and
    its `qualification_passed` is computed by that protocol's decision rule and nothing else. Attempt 1 (master 220261026,
    n = 400, designated-window FAIL) is retained as an immutable record and is never re-decided by a later protocol."""
    protocol_id: str                    # e.g. "f8_m3_null_validation_attempt2"
    attempt: int
    n_replicates: int
    replicate_master: int               # declared here; never a panel master; never a master already used by an earlier attempt
    grid: int
    ticks: int
    primary_statistic: str              # "designated_terminal_window_dkw"
    primary_alpha: float
    auxiliary_statistic: str            # "per_window_union_dkw"
    auxiliary_alpha: float              # the union's TOTAL level; each window at auxiliary_alpha / N_WINDOWS
    decision_rule: str                  # "primary_and_auxiliary" | "primary_only"
    joint_false_fail_bound: float       # the stated (union) bound on P(false fail) under the rule — never claimed smaller
    prior_attempts: Tuple[Tuple[int, int, int, str], ...]   # (attempt, master, n, outcome) retained, in order
    ratified_by: str                    # "Mike <date>" once ratified; "" = draft, cannot produce a qualification record

    def __post_init__(self) -> None:
        if self.primary_statistic != "designated_terminal_window_dkw" or self.auxiliary_statistic != "per_window_union_dkw":
            raise NullDomainError("protocol statistics must be the designated terminal-window DKW and the per-window union DKW")
        if self.decision_rule not in ("primary_and_auxiliary", "primary_only"):
            raise NullDomainError("unknown decision rule")
        if not (0.0 < self.primary_alpha < 1.0 and 0.0 < self.auxiliary_alpha < 1.0):
            raise NullDomainError("alphas must lie in (0, 1)")
        bound = self.primary_alpha + (self.auxiliary_alpha if self.decision_rule == "primary_and_auxiliary" else 0.0)
        if self.joint_false_fail_bound != bound:
            raise NullDomainError("joint_false_fail_bound must be the union bound of the levels the rule gates on")
        if self.replicate_master in (C.F8_SEED_PANEL_MASTER, C.F8_CALIBRATION_MASTER, 20260917) or any(self.replicate_master == m for _, m, _, _ in self.prior_attempts):
            raise NullDomainError("replicate master collides with a panel master or an earlier attempt's master")
        if (self.grid, self.ticks) == (C.F8_GRID, C.F8_TICKS) or self.ticks < C.F8_TAIL_TICKS + 1 or self.n_replicates < 10:
            raise NullDomainError("protocol shape must be a validation shape with the full tail and n ≥ 10")
        if self.attempt != len(self.prior_attempts) + 1:
            raise NullDomainError("attempt number must follow the retained prior attempts")

    def identity(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()

    def primary_bound(self) -> float: return math.sqrt(math.log(2.0 / self.primary_alpha) / (2.0 * self.n_replicates))
    def auxiliary_bound(self) -> float: return math.sqrt(math.log(2.0 / (self.auxiliary_alpha / N_WINDOWS)) / (2.0 * self.n_replicates))


# ATTEMPT 1 — retained, immutable, FAILED (L2 ruling 2026-10-27): master 220261026, n = 400, designated terminal-window DKW 0.0837 > 0.0679
ATTEMPT_1 = (1, VALIDATION_REPLICATE_MASTER, 400, "FAILED: designated terminal-window DKW 0.0837 > 0.0679 (alpha 0.05); union PASS not substitutable")

# ATTEMPT 2 — RATIFIED by Mike 2026-10-27 ("Ratify", as drafted) BEFORE any run under it; the ratification string is part of the identity
VALIDATION_PROTOCOL_ATTEMPT_2 = ValidationProtocol(
    protocol_id="f8_m3_null_validation_attempt2", attempt=2, n_replicates=1000, replicate_master=320261027, grid=C.F8_GRID, ticks=VALIDATION_TICKS,
    primary_statistic="designated_terminal_window_dkw", primary_alpha=0.025, auxiliary_statistic="per_window_union_dkw", auxiliary_alpha=0.025,
    decision_rule="primary_and_auxiliary", joint_false_fail_bound=0.05, prior_attempts=(ATTEMPT_1,), ratified_by="Mike 2026-10-27",
)
VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL = "20ae18f0a85d9b6ce3972acb2630529bd300a92fbc16e5f6f8b1a48a537abf2a"   # the registered identity; verified at every protocol run


def verify_protocol_registration(protocol: ValidationProtocol) -> None:
    if protocol.protocol_id == VALIDATION_PROTOCOL_ATTEMPT_2.protocol_id and protocol.identity() != VALIDATION_PROTOCOL_ATTEMPT_2_SHA256_LITERAL:
        raise NullDomainError("attempt-2 protocol differs from its registered identity")


@dataclass(frozen=True)
class NullValidation:
    """The validation record. INFERENTIAL fields (L2 M2/M3 r1 D1): `dkw_*` use ONE designated window per replicate — the
    terminal window, the one S_term is scored on — so the sample is independent across replicates (n = n_replicates)
    and the DKW bound applies. DESCRIPTIVE fields use all windows of all replicates; windows within a replicate are
    consecutive segments of one stationary trajectory and are not an independent sample, so `all_windows_sup_deviation`
    carries no coverage statement and must never be used as qualification evidence. SCOPE (D2): at a reduced grid the
    thresholds are the scaled-grid law's own quantiles (`thresholds_scope == "smoke_scaled_grid"`), smoke-only; the
    record of qualification has `thresholds_scope == "production_cache"` and grid 50."""
    n_replicates: int
    replicate_master: int
    grid: int
    ticks: int
    protocol_id: str                    # "" for an unregistered (diagnostic/smoke) run — such a record can never be qualification evidence
    protocol_sha256: str                # identity of the ratified ValidationProtocol the run was produced under ("" if none)
    qualification_passed: bool          # H3: computed ONLY by a ratified protocol's decision rule; False for every unregistered run
    production_scope_eligible: bool     # H3: grid 50 with the production cache's thresholds — eligibility, never passage
    thresholds_scope: str               # "production_cache" (grid 50) | "smoke_scaled_grid" (grid < 50; never qualification evidence)
    theta_p_used: float
    theta_t_used: float
    dkw_sup_deviation: float            # INFERENTIAL (designated test): sup |F̂ − F_W| over the terminal window, one per replicate
    dkw_bound: float                    # sqrt(ln(2/α)/(2 n_replicates)), α = VALIDATION_DKW_ALPHA
    dkw_passed: bool
    dkw_p_value: float                  # DKW tail bound 2·exp(−2 n D²) on the designated statistic (conservative p)
    per_window_sup_deviation: Tuple[float, ...]   # INFERENTIAL (union test): sup |F̂_j − F_W| for each window index j, n_replicates each
    union_bound: float                  # sqrt(ln(2/(α/N_WINDOWS))/(2 n_replicates)): each window at α/10, union valid under dependence
    union_passed: bool                  # every window's sup ≤ union_bound  ⇒  P(false fail) ≤ α whatever the dependence
    window_lag1_corr_exact: float       # exact consecutive-window correlation of the law (window_lag1_correlation)
    window_lag1_corr_empirical: float
    all_windows_sup_deviation: float    # DESCRIPTIVE: sup |F̂ − F_W| over all windows pooled (dependent sample; no bound)
    exceed_theta_t_rate: float          # DESCRIPTIVE: fraction of windows with mean > θ_T used (nominal ≤ α_T at scope)
    exceed_theta_p_rate: float          # DESCRIPTIVE: fraction of windows with mean > θ_P used (nominal ≤ α_P/N_WINDOWS at scope)
    s_min_rejection_rate: float         # DESCRIPTIVE price of route (b): fraction of replicates with S_min > θ_P (nominal ≤ α_P); independent across replicates
    s_term_false_no_sustained_rate: float   # fraction of replicates with S_term ≤ θ_T under the null (expected ≈ q_T)
    empirical_mean_density: float       # mean window-mean density over all windows (law: π₁)
    empirical_sd_density: float         # sd of window-mean density over all windows (law: σ_null)
    law_sd_density: float
    exceed_q99_rate: float              # fraction of windows above the scope law's 0.99 quantile (calibration diagnostic; ≈ 0.01)
    n_cells_scaled: bool                # True when grid < 50

    def __post_init__(self) -> None:
        if self.thresholds_scope not in ("production_cache", "smoke_scaled_grid") or self.n_cells_scaled != (self.thresholds_scope == "smoke_scaled_grid"):
            raise NullDomainError("validation scope must be production_cache at grid 50 or smoke_scaled_grid below it")
        if self.dkw_bound != math.sqrt(math.log(2.0 / VALIDATION_DKW_ALPHA) / (2.0 * self.n_replicates)) or self.dkw_passed != (self.dkw_sup_deviation <= self.dkw_bound):
            raise NullDomainError("DKW bound must be the one-designated-window bound at n_replicates, and dkw_passed its comparison")
        if self.union_bound != math.sqrt(math.log(2.0 / VALIDATION_UNION_ALPHA) / (2.0 * self.n_replicates)) or len(self.per_window_sup_deviation) != N_WINDOWS \
                or self.union_passed != all(d <= self.union_bound for d in self.per_window_sup_deviation) or self.per_window_sup_deviation[-1] != self.dkw_sup_deviation:
            raise NullDomainError("union test must use the per-window bound at alpha/N_WINDOWS over all ten windows, the last being the designated window")
        if self.dkw_p_value != min(1.0, 2.0 * math.exp(-2.0 * self.n_replicates * self.dkw_sup_deviation ** 2)):
            raise NullDomainError("dkw_p_value must be the DKW tail bound of the designated statistic")
        if self.production_scope_eligible != (self.thresholds_scope == "production_cache"):
            raise NullDomainError("production_scope_eligible must equal production scope")
        if self.protocol_id == "" and (self.protocol_sha256 != "" or self.qualification_passed):
            raise NullDomainError("an unregistered run carries no protocol identity and can never be qualification-passed")

    def is_qualification_evidence(self) -> bool:
        """DEPRECATED NAME kept for one round: eligibility only (H3). Use production_scope_eligible and qualification_passed."""
        return self.production_scope_eligible


def decide_under_protocol(v: "NullValidation", protocol: ValidationProtocol) -> bool:
    """The protocol's decision rule on a record produced under it (the only path to qualification_passed = True)."""
    if protocol.ratified_by == "": raise NullDomainError("a draft protocol cannot decide qualification")
    if (v.n_replicates, v.replicate_master, v.grid, v.ticks) != (protocol.n_replicates, protocol.replicate_master, protocol.grid, protocol.ticks) or not v.production_scope_eligible:
        raise NullDomainError("record does not match the protocol's registered shape, master and scope")
    primary = v.dkw_sup_deviation <= protocol.primary_bound()
    aux = all(d <= protocol.auxiliary_bound() for d in v.per_window_sup_deviation)
    return bool(primary and (aux if protocol.decision_rule == "primary_and_auxiliary" else True))


def validate_on_stepper(n_replicates: int, replicate_master: int = VALIDATION_REPLICATE_MASTER, *, grid: int = C.F8_GRID, ticks: int = VALIDATION_TICKS,
                        protocol: Optional[ValidationProtocol] = None) -> NullValidation:
    """Run the F8 stepper under the `null` object (g = 0) for n replicates with seeds derived from the declared replicate
    master, at a frozen level (inert), and compare the empirical window-count law with F_W. The shape is the declared
    validation shape (full N, VALIDATION_TICKS), never the production shape: replicate seeds are not panel seeds and
    claim no production identity. Below the production grid the law is rebuilt for N = grid² (same cell pmf) and the
    thresholds are THAT law's quantiles (smoke scope, D2); at grid 50 they are the production cache's."""
    verify_frozen_identity()
    if protocol is not None:
        if protocol.ratified_by == "": raise NullDomainError("a qualification run requires a RATIFIED protocol; a draft cannot produce a record of qualification")
        verify_protocol_registration(protocol)
        if (n_replicates, replicate_master, grid, ticks) != (protocol.n_replicates, protocol.replicate_master, protocol.grid, protocol.ticks):
            raise NullDomainError("run arguments must equal the registered protocol's values")
    if isinstance(n_replicates, bool) or not isinstance(n_replicates, int) or n_replicates < 10: raise NullDomainError("n_replicates must be an integer ≥ 10")
    if (grid, ticks) == (C.F8_GRID, C.F8_TICKS): raise NullDomainError("null validation never runs at the production shape (replicate seeds are not panel seeds)")
    if ticks < C.F8_TAIL_TICKS + 1: raise NullDomainError("validation needs the full ten-window tail")
    seeds = C.generate_seed_panel(replicate_master, n_replicates)
    a, q, pi1 = chain_rates()
    n = grid * grid
    if grid == C.F8_GRID:
        pmf, cdf, *_ = window_count_law()
        th = null_thresholds(C.F8_LEVELS_MICRO[0]); tp, tt = th.theta_p, th.theta_t; scope = "production_cache"
    else:
        cell, cert, _ = certified_cell_pmf(a, q, pi1); pmf, wc_ = window_count_pmf(cell, cert, n); cdf = np.cumsum(pmf); cdf[-1] = 1.0
        eps = wc_.sum_l1_bound; dn = WINDOW * n
        kp = int(np.searchsorted(cdf, Q_P + eps, side="left")); kt = int(np.searchsorted(cdf, Q_T + eps, side="left"))   # the scaled law's own conservative quantiles
        tp, tt = float(np.float64(kp) / np.float64(dn)), float(np.float64(kt) / np.float64(dn)); scope = "smoke_scaled_grid"
    denom = WINDOW * n
    counts: List[int] = []; designated: List[int] = []; smin_rej = 0; sterm_no = 0; nwin = min(C.F8_TAIL_TICKS, ticks) // WINDOW
    for s_ in seeds:
        r = D.run(C.f8_run_spec(C.F8_LEVELS_MICRO[0], int(s_), "null", grid=grid, ticks=ticks))
        tail = r.active_counts[ticks - nwin * WINDOW + 1:]
        wc = [int(tail[i * WINDOW:(i + 1) * WINDOW].sum()) for i in range(nwin)]
        counts.extend(wc); designated.append(wc[-1])
        means = [c / denom for c in wc]
        if min(means) > tp: smin_rej += 1
        if means[-1] <= tt: sterm_no += 1
    arr = np.array(counts); des = np.array(designated)
    grid_k = np.arange(denom + 1)
    Wm = arr.reshape(n_replicates, nwin)
    per_window = tuple(float(np.max(np.abs(np.searchsorted(np.sort(Wm[:, j]), grid_k, side="right") / n_replicates - cdf))) for j in range(nwin))
    emp_all = np.searchsorted(np.sort(arr), grid_k, side="right") / arr.size
    sup_des = per_window[-1]; sup_all = float(np.max(np.abs(emp_all - cdf)))
    bound = math.sqrt(math.log(2.0 / VALIDATION_DKW_ALPHA) / (2.0 * n_replicates))
    ubound = math.sqrt(math.log(2.0 / VALIDATION_UNION_ALPHA) / (2.0 * n_replicates))
    pval = min(1.0, 2.0 * math.exp(-2.0 * n_replicates * sup_des ** 2))
    lag_exact = window_lag1_correlation(a, q, pi1, n); lag_emp = float(np.corrcoef(Wm[:, :-1].ravel(), Wm[:, 1:].ravel())[0, 1]) if nwin > 1 else 0.0
    kk = np.arange(pmf.size); law_mean = float((kk * pmf).sum()); law_sd = float(np.sqrt(((kk - law_mean) ** 2 * pmf).sum()))
    k99 = int(np.searchsorted(cdf, 0.99, side="left"))
    rec = NullValidation(n_replicates, int(replicate_master), grid, ticks, "", "", False, scope == "production_cache", scope, tp, tt, sup_des, bound, bool(sup_des <= bound), pval,
                          per_window, ubound, bool(all(d <= ubound for d in per_window)), lag_exact, lag_emp, sup_all,
                          float(np.mean(arr / denom > tt)), float(np.mean(arr / denom > tp)),
                          smin_rej / n_replicates, sterm_no / n_replicates,
                          float(arr.mean() / denom), float(arr.std(ddof=1) / denom), law_sd / denom, float(np.mean(arr > k99)), grid != C.F8_GRID)
    if protocol is None:
        return rec
    import dataclasses as _dc
    return _dc.replace(rec, protocol_id=protocol.protocol_id, protocol_sha256=protocol.identity(), qualification_passed=decide_under_protocol(rec, protocol))
