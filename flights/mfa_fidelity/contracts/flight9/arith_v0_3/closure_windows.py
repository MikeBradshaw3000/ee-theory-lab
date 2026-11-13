#!/usr/bin/env python3
"""Site-closure estimate of informative levels at theta. NO lattice run; NO probe output read.
Closure of contract s4.2 (realization: eta0, start pi1), 3x3 mean, region {p >= theta}; informative iff
both sides >= 100 cells and >= 40 edge bonds. The closure is a mean-field object and is known to be biased."""
import importlib.util, sys, math, json, numpy as np
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L=100; Q=P.Q_DE; ETA0=P.ETA0; A0=1-math.exp(-ETA0); PI1=A0/(A0+Q)
ii=np.arange(L,dtype=np.float64); x=(ii/L)[:,None]*np.ones((1,L)); y=np.ones((L,1))*(ii/L)[None,:]; X=ii[:,None]*np.ones((1,L)); Y=np.ones((L,1))*ii[None,:]
def tb():
    s=0.55+0.07*P._c(x); d=0.19+0.19*P._c(y); return s+d,s-d,np.full((L,L),0.8)
def td(cs,R,w):
    b=np.full((L,L),-np.inf)
    for cx,cy in cs:
        dx=np.abs(X-cx);dx=np.minimum(dx,L-dx);dy=np.abs(Y-cy);dy=np.minimum(dy,L-dy);b=np.maximum(b,R-np.sqrt(dx*dx+dy*dy))
    t=0.3+0.6*0.5*(1+np.tanh(b/w)); return t,t.copy(),t.copy()
C1=[(49.5,49.5)];C4=[(24.5,24.5),(24.5,74.5),(74.5,24.5),(74.5,74.5)]
T={"T0":P.terrain("T0",L),"TA":P.terrain("TA",L),"TB":tb(),"TC":P.terrain("TC",L),"TD-1-2":td(C1,25.3,2.),"TD-1-4":td(C1,25.3,4.),"TD-4-2":td(C4,12.65,2.),"TD-4-4":td(C4,12.65,4.)}
KAP=[0.75]+[round(1.0+0.1*k,2) for k in range(11)]+[2.25,2.5,3.0]
def closure(lam,g):
    p=np.full((L,L),PI1)
    for it in range(200000):
        d=P.moore_sum(p)/8.0
        new=(1-p)*(1-np.exp(-(ETA0+g*lam*d)))+(1-Q)*p
        if np.abs(new-p).max()<1e-12: return new,it
        p=new
    return None,None
def box(a): return sum(np.roll(np.roll(a,i,0),j,1) for i in (-1,0,1) for j in (-1,0,1))/9
def nb(h): return int((h!=np.roll(h,-1,0)).sum()+(h!=np.roll(h,-1,1)).sum())
out={}
for name,(v,u,r) in T.items():
    for c in ("P","H"):
        if name=="T0" and c=="H": continue
        lam=P.compose(c,v,u,r); gs=Q/P.spectral_radius(lam); rows=[]
        for k in KAP:
            p,it=closure(lam,k*gs)
            if p is None: rows.append(dict(kappa=k,converged=False)); continue
            pt=box(p); row=dict(kappa=k,mean=float(p.mean()),lo=float(pt.min()),hi=float(pt.max()),iters=it)
            for th in (0.10,0.20,0.30):
                h=pt>=th; n=int(h.sum()); row["inf_%.2f"%th]=bool(n>=100 and L*L-n>=100 and nb(h)>=40); row["n_%.2f"%th]=n
            rows.append(row)
        out[name+"."+c]=rows
json.dump(out,open(sys.argv[2],"w"),indent=1)
for a,rows in out.items():
    print(a)
    print("   kappa  "+" ".join("%5.2f"%r["kappa"] for r in rows))
    print("   mean   "+" ".join("%5.3f"%r["mean"] for r in rows))
    print("   min    "+" ".join("%5.3f"%r["lo"] for r in rows))
    print("   max    "+" ".join("%5.3f"%r["hi"] for r in rows))
    for th in ("0.10","0.20","0.30"):
        print("   th"+th+"  "+" ".join("    Y" if r["inf_"+th] else "    ." for r in rows), " count",sum(r["inf_"+th] for r in rows))
