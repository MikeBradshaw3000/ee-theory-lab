#!/usr/bin/env python3
"""Closure-estimated width in kappa of the window in which an arm has an edge at theta. NO lattice run; NO probe output."""
import importlib.util, sys, math, json, numpy as np
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L=100; Q=P.Q_DE; ETA0=P.ETA0; A0=1-math.exp(-ETA0); PI1=A0/(A0+Q)
ii=np.arange(L,dtype=np.float64); x=(ii/L)[:,None]*np.ones((1,L)); y=np.ones((L,1))*(ii/L)[None,:]
def tb(s0,a,d0,b,r0):
    s=s0+a*P._c(x); d=d0+b*P._c(y); return s+d,s-d,np.full((L,L),r0)
def closure(lam,g,p0=None):
    p=np.full((L,L),PI1) if p0 is None else p0
    for it in range(200000):
        new=(1-p)*(1-np.exp(-(ETA0+g*lam*P.moore_sum(p)/8.0)))+(1-Q)*p
        if np.abs(new-p).max()<1e-12: return new
        p=new
def box(a): return sum(np.roll(np.roll(a,i,0),j,1) for i in (-1,0,1) for j in (-1,0,1))/9
def nb(h): return int((h!=np.roll(h,-1,0)).sum()+(h!=np.roll(h,-1,1)).sum())
def inf(pt,th):
    h=pt>=th; n=int(h.sum()); return n>=100 and L*L-n>=100 and nb(h)>=40
fine=[round(0.75+0.01*k,2) for k in range(226)]
g10=[0.75]+[round(1.0+0.1*k,2) for k in range(11)]+[2.25,2.5,3.0]
g05=[0.75]+[round(1.0+0.05*k,2) for k in range(21)]+[2.25,2.5,3.0]
res={}
cases={"TB.H r0=0.8":(tb(0.55,0.07,0.19,0.19,0.8),"H"),"TB.H r0=0.5":(tb(0.55,0.07,0.19,0.19,0.5),"H"),"TB.H r0=0.3":(tb(0.55,0.07,0.19,0.19,0.3),"H"),"TB.H r0=0.1":(tb(0.55,0.07,0.19,0.19,0.1),"H"),
       "TB.P (any r0)":(tb(0.55,0.07,0.19,0.19,0.8),"P")}
v,u,r=P.terrain("TC",L); cases["TC.H"]=((v,u,r),"H")
for name,((v,u,r),c) in cases.items():
    lam=P.compose(c,v,u,r); gs=Q/P.spectral_radius(lam); p=None; flags={}
    for th in (0.10,0.20,0.30): flags[th]=[]
    for k in fine:
        p=closure(lam,k*gs,p); pt=box(p)
        for th in flags: flags[th].append(inf(pt,th))
    row={"ratio":float(lam.max()/lam.min())}
    for th,f in flags.items():
        ks=[k for k,ok in zip(fine,f) if ok]
        row[th]=dict(lo=min(ks) if ks else None,hi=max(ks) if ks else None,width=round(max(ks)-min(ks)+0.01,2) if ks else 0,
                     n_grid10=sum(1 for k in g10 if k in ks),n_grid05=sum(1 for k in g05 if k in ks))
    res[name]=row; print(name,"ratio %.3f"%row["ratio"]); [print("    theta",th,row[th]) for th in (0.10,0.20,0.30)]
json.dump({k:{str(a):b for a,b in v.items()} for k,v in res.items()},open(sys.argv[2],"w"),indent=1)
