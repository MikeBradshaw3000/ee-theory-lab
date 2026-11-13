import importlib.util, sys, numpy as np
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L=100; x=(np.arange(L)/L)[:,None]*np.ones((1,L)); y=np.ones((L,1))*(np.arange(L)/L)[None,:]
for (s0,a,d0,b) in ((0.55,0.07,0.19,0.19),(0.55,0.07,0.0,0.38)):
  for r0 in (0.8,0.5,0.3):
    s=s0+a*P._c(x); d=d0+b*P._c(y); v=s+d; u=s-d; r=np.full((L,L),r0)
    for c in "PH":
        lam=P.compose(c,v,u,r); tot=lam.var(); spr=P.spectral_radius(lam)
        print((s0,a,d0,b),r0,c,"sx=%.5f sy=%.5f ratio=%.4f cv=%.4f min=%.4f max=%.4f spr=%.5f gspec=%.5f"%(lam.mean(1).var()/tot,lam.mean(0).var()/tot,lam.max()/lam.min(),lam.std()/lam.mean(),lam.min(),lam.max(),spr,P.Q_DE/spr))
