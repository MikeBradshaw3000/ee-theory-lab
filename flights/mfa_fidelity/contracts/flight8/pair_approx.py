"""Appendix B — pair approximation of the Flight 8 rule (synchronous, Moore z=8), derived from §2.4.
Variables: rho = P(cell active); pAA = P(Moore pair both active). Conditional neighbour probabilities under the
pair closure: qA_A = pAA/rho (neighbour active | cell active), qA_I = (rho - pAA)/(1 - rho) (neighbour active | cell inactive).
Per-cell rule: inactive with k of 8 active neighbours activates w.p. a_k = 1 - exp(-(eta + g*lam*k/8)); active deactivates w.p. qd = 1 - exp(-mu).
One tick (synchronous; given the state, all draws independent):
  rho' = rho*(1-qd) + (1-rho)*E[a_K],  K ~ Bin(8, qA_I)
  pAA' = pAA*(1-qd)^2 + 2*pAI*(1-qd)*E[a_{1+K7}] + pII*(E[a_{K7'}])^2,  K7 ~ Bin(7, qA_I)
     (A,A) both survive; (A,I): the active one survives and the inactive one, which has one known active neighbour
     (its partner) and 7 others ~ Bin(7, qA_I), activates; (I,I): both activate, each with 7 others ~ Bin(7, qA_I)
     and the partner inactive; their neighbour sets are treated as independent (the pair closure).
  pAI = rho - pAA, pII = 1 - 2 rho + pAA.
Control coordinate m = g*lam/qd (Delta t = 1), so g*lam = m*qd.
"""
import math, sys
from math import comb
def ak(k, eta, glam): return 1 - math.exp(-(eta + glam*k/8))
def E_a(n, p, eta, glam, offset=0):
    return sum(comb(n,k)*p**k*(1-p)**(n-k)*ak(k+offset, eta, glam) for k in range(n+1))
def step(rho, pAA, eta, m, mu):
    qd = 1 - math.exp(-mu); glam = m*qd
    if rho <= 0: return 0.0, 0.0
    qA_I = (rho - pAA)/(1 - rho) if rho < 1 else 0.0
    qA_I = min(max(qA_I, 0.0), 1.0)
    pAI = rho - pAA; pII = 1 - 2*rho + pAA
    rho2 = rho*(1-qd) + (1-rho)*E_a(8, qA_I, eta, glam)
    pAA2 = pAA*(1-qd)**2 + 2*pAI*(1-qd)*E_a(7, qA_I, eta, glam, offset=1) + pII*E_a(7, qA_I, eta, glam)**2
    return rho2, pAA2
def fixed_point(eta, m, mu, rho0=0.5, iters=20000):
    rho, pAA = rho0, rho0*rho0
    for _ in range(iters):
        r2, p2 = step(rho, pAA, eta, m, mu)
        if abs(r2-rho) < 1e-13 and abs(p2-pAA) < 1e-13: rho, pAA = r2, p2; break
        rho, pAA = r2, p2
    return rho, pAA
def leading_multiplier(m, mu):
    """Linearization of the eta=0 map at the absorbing state, in (rho, pAA):
       rho'  = (1-qd+8a1) rho - 8a1 pAA ;  pAA' = 2(1-qd)a1 rho + [(1-qd)^2 - 2(1-qd)a1] pAA,  a1 = 1-exp(-glam/8)."""
    qd = 1 - math.exp(-mu); glam = m*qd; a1 = 1 - math.exp(-glam/8)
    A = (1-qd+8*a1); B = -8*a1; C = 2*(1-qd)*a1; Dd = (1-qd)**2 - 2*(1-qd)*a1
    tr, det = A+Dd, A*Dd - B*C
    return (tr + math.sqrt(max(tr*tr - 4*det, 0)))/2
def m_lat(mu):
    lo, hi = 1.0, 5.0
    for _ in range(200):
        mid = (lo+hi)/2
        if leading_multiplier(mid, mu) < 1: lo = mid
        else: hi = mid
    return (lo+hi)/2
if __name__ == "__main__":
    mu = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
    eta0 = -math.log(0.99)
    ml = m_lat(mu); print(f"mu={mu}: mean-field crossing m=1; pair-approximation crossing m_lat = {ml:.4f}")
    print("  check: leading multiplier at m=1:", round(leading_multiplier(1.0, mu),4), " at m_lat:", round(leading_multiplier(ml, mu),6))
    print("  skeleton (eta=0) pair fixed point rho vs mean field:")
    for m in (1.0, 1.2, ml, 1.5, 2.0, 2.5):
        r, p = fixed_point(0.0, m, mu); print(f"    m={m:.3f}: pair rho*={r:.4f}  (qA_A={p/r if r>0 else 0:.3f})")
    print("  realization (eta0) pair fixed point:")
    for m in (0.25, 0.5, 1.0, ml, 1.5, 2.0, 2.5):
        r, p = fixed_point(eta0, m, mu); print(f"    m={m:.3f}: pair rho*={r:.4f}")
