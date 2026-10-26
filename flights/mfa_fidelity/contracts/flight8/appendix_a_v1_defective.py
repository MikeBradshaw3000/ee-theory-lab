#!/usr/bin/env python3
"""
appendix_a.py — Contract F8 Appendix A: every DERIVED@FREEZE quantity computed by its
declared procedure from the contract's closed-form inputs. Pure-python, no dependencies,
deterministic. Run:  python3 -I appendix_a.py  → prints the Appendix A table (markdown)
and a JSON block; the JSON is the object of record, the table is its rendering.

Inputs (contract v0.8.2 §2, §3, §4.1, §4.5, §6, §8), PROPOSED unless marked RULED:
  L=50 (N=2500); mu=0.2; eta0=-ln(0.99) [RULED]; Dt=1; sweep [0.25,2.50], n1=24 levels
  in exact integer micro-units; T=3000, tail 1000 in 10 windows of 100 (T_pre=2000);
  QS survival N*rho_sk>=50; W_res = 3 pass-1 spacings; eps=0.01; 16/2/4 label rule;
  router: 8 round-half-even interior insertions per band, collided candidates removed;
  declared-range factors 0.9 (locatable) and 1.1 (unresolvable); off_band_mixture pi in [0.45,0.55].
"""
import json, math
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_EVEN

# ---------- inputs ----------
L = 50; N = L * L
MU = 0.2; DT = 1.0
ETA0 = -math.log(1 - 0.01)          # RULED
M_MIN, M_MAX, N1 = 0.25, 2.50, 24
T, TAIL, WIN = 3000, 1000, 100
T_PRE = T - TAIL
QS_MIN_ACTIVE = 50
WRES_SPACINGS = 3
EPS = 0.01
ALPHA_P = 0.001
INSERTIONS = 8
LOC_FACTOR, UNRES_FACTOR = 0.9, 1.1
PI_RANGE = (0.45, 0.55)
MICRO = 1_000_000

q = 1 - math.exp(-MU * DT)           # deactivation prob per tick

# ---------- 1. grid in micro-units ----------
m_min_u, m_max_u = int(round(M_MIN * MICRO)), int(round(M_MAX * MICRO))
# levels: exact integer micro-units, evenly spaced, round-half-even on the division
def rhe(x: Fraction) -> int:
    return int(Decimal(x.numerator) / Decimal(x.denominator)).__class__(
        (Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1), rounding=ROUND_HALF_EVEN))
levels_u = [rhe(Fraction(m_min_u) + Fraction((m_max_u - m_min_u) * i, N1 - 1)) for i in range(N1)]
spacings = [b - a for a, b in zip(levels_u, levels_u[1:])]
s_u = min(spacings); s_u_max = max(spacings)
W_res_u = WRES_SPACINGS * s_u

# ---------- 2. mean-field map and fixed points ----------
def fmap(rho, m, eta):
    glam = m * q / DT                 # m = g*lam*Dt/(1-e^-mu*Dt)
    return (1 - rho) * (1 - math.exp(-(eta + glam * rho) * DT)) + rho * math.exp(-MU * DT)

def fixed_point(m, eta, rho0=0.5, iters=400000, tol=1e-15):
    rho = rho0
    for _ in range(iters):
        r2 = fmap(rho, m, eta)
        if abs(r2 - rho) < tol:
            return r2
        rho = r2
    return rho

def rho_sk(m):                        # skeleton: eta=0; 0 for m<=1 (stable absorbing)
    if m <= 1.0:
        return 0.0
    return fixed_point(m, 0.0)

def rho_re(m):
    return fixed_point(m, ETA0)

levels_m = [u / MICRO for u in levels_u]
table_sk = {f"{m:.6f}": rho_sk(m) for m in levels_m}
table_re = {f"{m:.6f}": rho_re(m) for m in levels_m}

# ---------- 3. null stationary density, sigma_null, theta_P (Gaussian provisional) ----------
a = 1 - math.exp(-ETA0 * DT)
pi1 = a / (a + q)
# exact per-cell window-mean variance for a 2-state chain: Var(mean of W ticks) with
# stationary start; autocorrelation lambda = 1-a-q.
lam = 1 - a - q
var_x = pi1 * (1 - pi1)
# sum_{i,j} lam^|i-j| / W^2
W = WIN
sum_corr = W + 2 * sum((W - k) * lam ** k for k in range(1, W))
var_cell_winmean = var_x * sum_corr / (W * W)
sigma_null = math.sqrt(var_cell_winmean / N)
# theta_P familywise: per-window quantile 1 - alpha_P/10, provisional Gaussian
from statistics import NormalDist
z = NormalDist().inv_cdf(1 - ALPHA_P / 10)
theta_P_gauss = pi1 + z * sigma_null
# m at which rho_re = theta_P (bisection below sweep)
def m_at(target):
    lo, hi = 1e-6, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if rho_re(mid) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2
m_feedback_onset = m_at(theta_P_gauss)

# ---------- 4. Delta m ----------
lower = math.log(N) / (q * T_PRE)                  # 1 - m >= ln N / (q T_pre)
# upper: smallest m-1 with N*rho_sk(m) >= 50, by bisection on m>1
lo, hi = 1.0, 2.5
for _ in range(200):
    mid = (lo + hi) / 2
    if N * rho_sk(mid) < QS_MIN_ACTIVE: lo = mid
    else: hi = mid
upper = hi - 1.0
s_m = s_u / MICRO
delta_m = max(lower, upper) + s_m

# ---------- 5. Beta(15,6) quantiles at eps ----------
def beta_cdf_15_6(x):
    # I_x(15,6) = sum_{j=15}^{20} C(20,j) x^j (1-x)^(20-j)
    return sum(math.comb(20, j) * x ** j * (1 - x) ** (20 - j) for j in range(15, 21))
def beta_quantile(p):
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if beta_cdf_15_6(mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2
q_eps, q_1meps = beta_quantile(EPS), beta_quantile(1 - EPS)
beta_mean = 15 / 21

# ---------- 6. Delta_route(B): exhaustive over all bands of the pass-1 grid ----------
def insertions(lo_u, hi_u, k=INSERTIONS):
    """k round-half-even interior insertions between lo and hi (exclusive)."""
    out = []
    for i in range(1, k + 1):
        x = Fraction(lo_u) + Fraction((hi_u - lo_u) * i, k + 1)
        out.append(rhe(x))
    return out

level_set = set(levels_u)
delta_route = {}
collision_B = set()
n_bands = 0
for i in range(N1):
    for j in range(i + 1, N1):
        n_bands += 1
        lo_u, hi_u = levels_u[i], levels_u[j]
        B = j - i
        cands = insertions(lo_u, hi_u)
        kept = [c for c in cands if c not in level_set]      # collided candidates removed (worst case)
        if len(kept) < len(cands): collision_B.add(B)
        final = sorted(set([lo_u, hi_u] + kept))
        gap = max(b_ - a_ for a_, b_ in zip(final, final[1:]))
        delta_route[B] = max(delta_route.get(B, 0), 2 * gap)
B_LOC = 4
Delta_route = delta_route[B_LOC]

# ---------- 7. gap widths, declared ranges, margins ----------
w_L = (W_res_u - Delta_route) / q_1meps
w_U = W_res_u / q_eps
w_A = s_u / q_1meps
gentle_max = LOC_FACTOR * w_L
wide_min = UNRES_FACTOR * w_U
M_L = W_res_u - q_1meps * gentle_max - Delta_route
M_U = q_eps * wide_min - W_res_u
check_63 = (M_L > 0) and (M_U > 0) and (w_A < gentle_max) and (wide_min > W_res_u)

# ---------- 8. off_band_mixture risk ----------
def binom_tail(p):
    return sum(math.comb(20, k) * p ** k * (1 - p) ** (20 - k) for k in list(range(0, 4)) + list(range(17, 21)))
risk = max(binom_tail(PI_RANGE[0]), binom_tail(PI_RANGE[1]), binom_tail(0.5))

# ---------- 9. m_infl: argmax d rho_re / dm (fine grid + central differences) ----------
grid = [0.5 + i * 0.0005 for i in range(int((2.0 - 0.5) / 0.0005) + 1)]
vals = [rho_re(m) for m in grid]
best, best_m = -1, None
for k in range(1, len(grid) - 1):
    d = (vals[k + 1] - vals[k - 1]) / (grid[k + 1] - grid[k - 1])
    if d > best: best, best_m = d, grid[k]
m_infl = best_m

# ---------- 10. m_lat: pair approximation (Appendix B.2 linearization) ----------
def leading_multiplier(m):
    glam = m * q
    a1 = 1 - math.exp(-glam / 8)
    # 2x2 map on (rho, pAA): rho' = (1-q+8a1)rho - 8a1 pAA ; pAA' = 2(1-q)a1 rho + [(1-q)^2 - 2(1-q)a1] pAA
    A = [[1 - q + 8 * a1, -8 * a1], [2 * (1 - q) * a1, (1 - q) ** 2 - 2 * (1 - q) * a1]]
    tr = A[0][0] + A[1][1]; det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    disc = tr * tr - 4 * det
    if disc >= 0:
        return max(abs((tr + math.sqrt(disc)) / 2), abs((tr - math.sqrt(disc)) / 2))
    return math.sqrt(det)
lo, hi = 1.0, 2.0
for _ in range(200):
    mid = (lo + hi) / 2
    if leading_multiplier(mid) < 1: lo = mid
    else: hi = mid
m_lat = (lo + hi) / 2

# ---------- output ----------
A = {
  "inputs": {"L": L, "N": N, "mu": MU, "eta0": ETA0, "Dt": DT, "sweep": [M_MIN, M_MAX], "n1": N1,
             "T": T, "tail": TAIL, "window": WIN, "T_pre": T_PRE, "QS_min_active": QS_MIN_ACTIVE,
             "W_res_spacings": WRES_SPACINGS, "eps": EPS, "alpha_P": ALPHA_P, "insertions": INSERTIONS,
             "locatable_factor": LOC_FACTOR, "unresolvable_factor": UNRES_FACTOR, "pi_range": PI_RANGE},
  "levels_micro": levels_u, "s_micro": s_u, "s_micro_max": s_u_max, "W_res_micro": W_res_u,
  "rho_sk": table_sk, "rho_re": table_re,
  "null": {"pi1": pi1, "sigma_null_winmean": sigma_null, "theta_P_gaussian_provisional": theta_P_gauss,
           "m_feedback_onset": m_feedback_onset},
  "delta_m": {"lower": lower, "upper": upper, "s": s_m, "value": delta_m},
  "beta_15_6": {"q_eps": q_eps, "q_1meps": q_1meps, "mean": beta_mean},
  "delta_route": {str(k): v for k, v in sorted(delta_route.items())}, "collision_B": sorted(collision_B),
  "n_bands": n_bands, "Delta_route_B4": Delta_route,
  "widths": {"w_L": w_L, "w_A": w_A, "w_U": w_U, "gentle_max": gentle_max, "wide_min": wide_min,
             "M_L": M_L, "M_U": M_U, "check_6_3_passes": check_63},
  "off_band_mixture_risk_max": risk,
  "m_infl": m_infl, "m_lat": m_lat,
}

def f6(x): return f"{x:.6f}"
print("## Appendix A — DERIVED@FREEZE table (computed by appendix_a.py; values of record)\n")
print("| Quantity | Procedure | Value |\n|---|---|---|")
print(f"| s (pass-1 spacing) | (2.50 − 0.25)/23 in micro-units, round-half-even | {s_u:,} (max gap {s_u_max:,}) |")
print(f"| W_res | 3 s | {W_res_u:,} |")
sk = ", ".join(f"{table_sk[f'{m:.6f}']:.3f} ({m:.4g})" for m in levels_m if m > 1.0 and abs(m*4-round(m*4))<1e-6 or m in (levels_m[-1],))
print(f"| ρ*_sk(m) | fixed point of §3.1 at η_floor = 0 | 0 for m ≤ 1; full 24-level table in JSON; e.g. {table_sk[f'{levels_m[-1]:.6f}']:.4f} at m = {levels_m[-1]:.4f} |")
print(f"| ρ*(m; η₀) | fixed point at η₀ | full 24-level table in JSON; e.g. {table_re[f'{levels_m[0]:.6f}']:.4f} ({levels_m[0]:.4f}), {rho_re(1.0):.4f} (1.0), {table_re[f'{levels_m[-1]:.6f}']:.4f} ({levels_m[-1]:.4f}) |")
print(f"| null stationary density, σ_null | a/(a+q); exact 2-state window-mean variance, N = {N}, window {WIN} | {pi1:.4f}; {sigma_null:.5f} |")
print(f"| θ_P (familywise, α_P = {ALPHA_P}) | per-window Gaussian quantile 1 − α_P/10 (provisional; exact at build) | {theta_P_gauss:.4f} |")
print(f"| m at which ρ*(m; η₀) = θ_P | bisection | {m_feedback_onset:.3f} (below the sweep) |")
print(f"| Δm | max({lower:.4f}, {upper:.4f}) + s | **{delta_m:.4f}** |")
print(f"| Beta(15, 6) quantiles, ε = {EPS} | closed-form CDF, bisection | {q_eps:.6f} / {q_1meps:.6f} (mean {beta_mean:.4f}) |")
print(f"| Δ_route(B), B = 1…9 | exhaustive over all {n_bands} bands, collided candidates removed | " + "; ".join(f"{delta_route[b]:,}" for b in range(1, 10)) + f" (collisions at B ∈ {sorted(collision_B)}) |")
print(f"| Δ_route (B = {B_LOC}) | — | **{Delta_route:,}** |")
print(f"| m_infl | argmax dρ*/dm, central differences on a 0.0005 grid | {m_infl:.4f} |")
print(f"| m_lat | Appendix B.2 linearized pair map, leading multiplier = 1 by bisection | {m_lat:.4f} |")
print(f"| off_band_mixture risk | max P(K ≤ 3 or K ≥ 17) over π ∈ [{PI_RANGE[0]}, {PI_RANGE[1]}] | {risk:.4f} |")
print(f"| rule-1 class grid coverage | by construction of draw ranges | 1 |")
print(f"| w_L, w_A, w_U | §6.2 with exact quantiles | {w_L:,.0f}; {w_A:,.0f}; {w_U:,.0f} |")
print(f"| declared ranges | gentle ≤ 0.9 w_L; wide ≥ 1.1 w_U | ≤ {gentle_max:,.0f}; ≥ {wide_min:,.0f} |")
print(f"| margins M_L, M_U (§6.3) | W_res − q₁₋ε·0.9w_L − Δ_route; q_ε·1.1w_U − W_res | {M_L:,.0f}; {M_U:,.0f} — **§6.3 check {'PASSES' if check_63 else 'FAILS'}** |")
print("\n```json")
print(json.dumps(A, indent=1, default=float))
print("```")
