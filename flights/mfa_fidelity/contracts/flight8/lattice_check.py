"""NONCANONICAL design evidence (own seeds; pre-freeze). Skeleton (eta=0) of the F8 rule on a 50x50 periodic Moore
lattice, synchronous, high initialization; tail-window (last 1000 of 3000 ticks) mean density and survival, for a
grid of m. Purpose: is the pair-approximation m_lat in the right place relative to the lattice?"""
import sys, math, numpy as np
L=50; T=3000; TAIL=1000; mu=0.2; qd=1-math.exp(-mu)
def run(m, seed, eta=0.0, init="high"):
    rng=np.random.default_rng(seed); glam=m*qd
    x = np.ones((L,L),bool) if init=="high" else (rng.random((L,L))<0.02)
    dens=[]
    for t in range(T):
        k = sum(np.roll(np.roll(x,di,0),dj,1) for di in (-1,0,1) for dj in (-1,0,1) if (di,dj)!=(0,0)).astype(float)
        pa = 1-np.exp(-(eta+glam*k/8)); pd = qd
        u = rng.random((L,L))
        x = np.where(x, u>=pd, u<pa)
        if t>=T-TAIL: dens.append(x.mean())
        if not x.any() and eta==0: dens += [0.0]*(T-t-1 if t<T-TAIL else T-1-t); break
    d=np.array(dens[:TAIL]) if dens else np.zeros(TAIL)
    return d.mean(), float((d>0).all())
ms=[float(a) for a in sys.argv[1:]] or [1.0,1.1,1.15,1.2,1.3,1.5]
for m in ms:
    res=[run(m,s) for s in range(6)]
    print(f"m={m:.2f}: tail density per seed {[round(r[0],4) for r in res]}  survived {sum(r[1] for r in res)}/6")
