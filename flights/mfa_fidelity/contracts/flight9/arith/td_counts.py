import numpy as np, math, json
L=100
def counts(center_half):
    # achievable cell counts of a disc {dist<=R} centred on a lattice point (False) or a cell corner (True); returns {count: (Rmin, Rmax)} 
    off = 0.5 if center_half else 0.0
    i = np.arange(-40,41)+off
    d2 = np.sort((i[:,None]**2 + i[None,:]**2).ravel())
    u, c = np.unique(np.round(d2,9), return_counts=True); cum = np.cumsum(c)
    return {int(cum[k]): (math.sqrt(u[k]), math.sqrt(u[k+1])) for k in range(len(u)-1) if u[k] < 900}
A = {False: counts(False), True: counts(True)}
sol=[]
for h1 in (False, True):
  for h4 in (False, True):
    for h16 in (False, True):
      for c16,(r16a,r16b) in A[h16].items():
        T = 16*c16
        if not 1800 <= T <= 2200: continue
        if T in A[h1] and T//4 in A[h4]:
          sol.append((T, h1, h4, h16, A[h1][T], A[h4][T//4], (r16a,r16b)))
for s in sorted(sol): print(s)
print("pairs n=1,4 only:")
for h1 in (False, True):
  for h4 in (False, True):
    for c4,(a,b) in A[h4].items():
      T=4*c4
      if 1900<=T<=2100 and T in A[h1]: print(T,h1,h4,A[h1][T],(a,b))
