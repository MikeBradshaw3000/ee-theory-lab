"""NONCANONICAL design evidence. Tests both sides of
    true uncertain extent  <=  measured post-pass-2 band width  <=  true uncertain extent + slack
on every committed ramp-generator sweep, with 'true uncertain extent' defined exactly.

Definition. For a sweep, the ideal label at a control value m (same 20 seeds, same regime rule, same
frozen M2 label rule) is a step function of m: seed s is SUSTAINED at m iff u_s < frac(m), frac linear
from 0 at onset-w/2 to 1 at onset+w/2.  The TRUE UNCERTAIN EXTENT is  E = m_S - m_N  where
  m_N = sup{ m : label(m) == 'N' }   (last m at which the level would be confident N)
  m_S = inf{ m : label(m) == 'S' }   (first m at which the level would be confident S).
Both are breakpoints m_s = lo + u_s*(hi-lo) of the seed thresholds; computed exactly from the sorted
breakpoints, no grid.  SLACK = (m_N - lv[lo]) + (lv[hi] - m_S), i.e. the two one-sided gaps between the
true endpoints and the nearest confident grid level outside them; its bound is the sum of the two
final-level spacings straddling m_N and m_S (after fallback), which the script also measures.
Classes: the five pure-ramp generators (no extra inserted levels, no DIP): gentle_onset, abrupt_onset,
persistent_nonstationary_high_m, nonmonotone_amplitude, wide_mixed_boundary."""
import sys, json
sys.path.insert(0, ".")
import numpy as np
from mfa_instrument.e1 import audit as A, classify as C
N = A.N_SEEDS
rows = json.load(open(sys.argv[1]))
RAMP = ("gentle_onset","abrupt_onset","persistent_nonstationary_high_m","nonmonotone_amplitude","wide_mixed_boundary")
def label_from_count(k):          # k seeds sustained, N-k null, no unresolved
    return C.level_label(C.LevelCounts(k, N-k, 0))
def band(lab, lv):
    n=[i for i,c in enumerate(lab) if c=="N"]; s=[i for i,c in enumerate(lab) if c=="S"]
    return (max(n), min(s)) if n and s and max(n)<min(s) else None
stats = {c: dict(n=0, lower_ok=0, upper_ok=0, max_viol=0.0, slack=[], spac=[]) for c in RAMP}
for r in rows:
    cls = r["cls"]
    if cls not in RAMP: continue
    b = band(r["lf"], r["lv"])
    if not b: continue
    ci = A.CLASSES.index(cls); master = A.AUDIT_MASTER if r["ens"]=="design" else A.HELD_OUT_MASTER
    prm, _ = A.draw_params(cls, master, ci, r["sweep"])
    u = np.random.default_rng(np.random.SeedSequence([master, ci, r["sweep"]])).random(N)
    lo, hi = prm.onset_micro - prm.width_micro//2, prm.onset_micro + prm.width_micro//2
    bp = sorted(lo + us*(hi-lo) for us in u)          # seed s becomes sustained just above bp[s]
    # label as a function of m: k(m) = #{bp < m}; label(m) = label_from_count(k)
    # m_N = sup{m: label N}: the breakpoint at which k first exceeds the N-allowed count
    kN = max(k for k in range(N+1) if label_from_count(k)=="N")      # largest k still labelled N
    kS = min(k for k in range(N+1) if label_from_count(k)=="S")      # smallest k labelled S
    m_N = bp[kN]            # for m in (bp[kN-1], bp[kN]] count is kN -> N; above bp[kN] count kN+1
    m_S = bp[kS-1]          # for m > bp[kS-1] count >= kS -> S
    if prm.width_micro == 0: m_N = m_S = float(lo)
    E = m_S - m_N
    lv = r["lv"]; meas = lv[b[1]] - lv[b[0]]
    s = stats[cls]; s["n"] += 1
    s["lower_ok"] += meas >= E - 1e-9
    gapN = m_N - lv[b[0]]; gapS = lv[b[1]] - m_S
    # straddling spacings: the final-level spacing containing m_N and the one containing m_S
    def spacing_at(x):
        for a, c in zip(lv, lv[1:]):
            if a <= x < c: return c - a
        return float("nan")
    bound = spacing_at(m_N) + spacing_at(m_S)
    ok = meas <= E + bound + 1e-9
    s["upper_ok"] += ok
    if not ok: s["max_viol"] = max(s["max_viol"], meas - E - bound)
    s["slack"].append(gapN + gapS); s["spac"].append(bound)
print(f"{'class':34} {'n':>5} {'measured>=E':>12} {'measured<=E+straddle':>22} {'slack med/max':>16} {'straddle med/max':>18}")
for c in RAMP:
    s = stats[c]; sl = sorted(s["slack"]); sp = sorted(s["spac"])
    print(f"{c:34} {s['n']:5} {s['lower_ok']:12} {s['upper_ok']:22} {sl[len(sl)//2]:7.0f}/{sl[-1]:7.0f} {sp[len(sp)//2]:8.0f}/{sp[-1]:8.0f}")
