import numpy as np, sys, importlib.util
from scipy.spatial import cKDTree
L=100; ii=np.arange(L,dtype=float); X=ii[:,None]*np.ones((1,L)); Y=np.ones((L,1))*ii[None,:]
def delta(cs,R):
    b=np.full((L,L),-np.inf)
    for cx,cy in cs:
        dx=np.abs(X-cx); dx=np.minimum(dx,L-dx); dy=np.abs(Y-cy); dy=np.minimum(dy,L-dy); b=np.maximum(b,R-np.sqrt(dx*dx+dy*dy))
    return b
def box(a): return sum(np.roll(np.roll(a,i,0),j,1) for i in (-1,0,1) for j in (-1,0,1))/9
def bonds(h):
    a=h!=np.roll(h,-1,0); b=h!=np.roll(h,-1,1); i1,j1=np.nonzero(a); i2,j2=np.nonzero(b)
    return np.concatenate([np.stack([(i1+.5)%L,j1.astype(float)],1),np.stack([i2.astype(float),(j2+.5)%L],1)])
def D(E,C):
    d1=cKDTree(C,boxsize=L).query(E)[0]; d2=cKDTree(E,boxsize=L).query(C)[0]; return max(np.quantile(d1,.95),np.quantile(d2,.95)), max(d1.max(),d2.max())
C4=[(24.5,24.5),(24.5,74.5),(74.5,24.5),(74.5,74.5)]
for name,cs,R in (("4 discs",C4,12.65),("1 disc",[(49.5,49.5)],25.3)):
    d=delta(cs,R); core=d>=0
    ind=core.astype(float); print(name,"indicator: q95,max shift of the 0.5 contour after 3x3 mean:",D(bonds(box(ind)>=0.5),bonds(core)), "cells in smoothed set",int((box(ind)>=0.5).sum()))
    for w in (2.0,4.0):
        S=0.5*(1+np.tanh(d/w)); print("   w",w,"profile:",D(bonds(box(S)>=0.5),bonds(core)), int((box(S)>=0.5).sum()))
