import importlib.util, sys, math, json, numpy as np
spec = importlib.util.spec_from_file_location("f9_probe", sys.argv[1]); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
L=100; Q=P.Q_DE; T_LO, T_HI = 0.3, 0.9
ii = np.arange(L, dtype=np.float64)
X = ii[:,None]*np.ones((1,L)); Y = np.ones((L,1))*ii[None,:]          # cell units
def delta_cells(centres, R):
    best = np.full((L,L), -np.inf)
    for cx, cy in centres:
        dx = np.abs(X-cx); dx = np.minimum(dx, L-dx); dy = np.abs(Y-cy); dy = np.minimum(dy, L-dy)
        best = np.maximum(best, R - np.sqrt(dx*dx+dy*dy))
    return best
def perim(core): return int((core != np.roll(core,1,0)).sum() + (core != np.roll(core,1,1)).sum())
V = {"1 disc": ([(49.5,49.5)], 25.3), "4 discs": ([(24.5,24.5),(24.5,74.5),(74.5,24.5),(74.5,74.5)], 12.65)}
rows=[]
for name,(cs,R) in V.items():
    d = delta_cells(cs,R); core = d >= 0
    mind = float(np.abs(d).min())
    for w in (1.0, 2.0, 4.0):
        S = 0.5*(1+np.tanh(d/w)); t = T_LO+(T_HI-T_LO)*S
        band = (S>0.1)&(S<0.9)
        r = dict(variant=name, R=R, w=w, core=int(core.sum()), nearest_cell_to_edge=round(mind,4), perim_cont=round(2*math.pi*R*len(cs),1), perim_lat=perim(core),
                 band=int(band.sum()), band_core=round(band.sum()/core.sum(),3), band_in=int((band&core).sum()), band_out=int((band&~core).sum()),
                 Smin=round(float(S.min()),4), Smax=round(float(S.max()),4), max_step=round(float(max(np.abs(t-np.roll(t,1,0)).max(), np.abs(t-np.roll(t,1,1)).max())),4))
        for c in "PH":
            lam = P.compose(c,t,t,t); spr = P.spectral_radius(lam)
            r[c] = (round(float(lam.min()),4), round(float(lam.max()),4), round(spr,5), round(Q/spr,5))
            tm=(T_LO+T_HI)/2; ref = tm**3 if c=="P" else tm
            r[c+"_core_ok"] = bool(np.array_equal(lam >= ref, core))
        rows.append(r); print(r)
json.dump(rows, open("td_final.json","w"), indent=1)
