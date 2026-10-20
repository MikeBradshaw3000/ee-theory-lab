"""Price candidate rule-4c definitions on the stored replay. Rules 1-3, 4a, 4b are kept frozen; only
the 4c criterion is replaced. Candidate families:
  COUNT k       : frozen form, span = number of interior levels after pass 2, ND iff span > k
  WIDTH W       : ND iff physical width of the band after pass 2 (lv[hi]-lv[lo], micro) > W
  P1COUNT k     : span counted on the PASS-1 sequence only (interior pass-1 levels), ND iff > k
"""
import sys, json, collections
sys.path.insert(0, ".")
from mfa_instrument.e1 import audit as A, verdict as V
rows = json.load(open(sys.argv[1]))
INTENDED = {c: v for c, v, _ in V.ARCHETYPE_TABLE}
CAP = A.CAP
def cp_ok(k, n=500): return A.clopper_pearson_upper(k, n) <= CAP
def verdict(r, mode, x):
    lab, lv = r["lf"], r["lv"]
    n_idx=[i for i,c in enumerate(lab) if c=="N"]; s_idx=[i for i,c in enumerate(lab) if c=="S"]
    if n_idx and s_idx and min(s_idx)<max(n_idx): return "NOT_PRODUCED"
    if not n_idx: return "NOT_PRODUCED" if lab[0]=="S" else "NOT_DISTINGUISHED"
    if not s_idx: return "NOT_PRODUCED" if lab[-1]=="N" else "NOT_DISTINGUISHED"
    lo,hi=max(n_idx),min(s_idx)
    if any(c=="M" and not (lo<i<hi) for i,c in enumerate(lab)): return "NOT_DISTINGUISHED"
    u_out=[i for i,c in enumerate(lab) if c=="U" and not (lo<i<hi)]
    spans=V._contiguous_spans(u_out)
    if len(u_out)>V.OFF_BAND_U_ALLOWANCE or any(len(s)>1 for s in spans): return "NOT_DISTINGUISHED"
    if mode=="COUNT": return "NOT_DISTINGUISHED" if (hi-lo-1)>x else "LOCATED"
    if mode=="WIDTH": return "NOT_DISTINGUISHED" if (lv[hi]-lv[lo])>x else "LOCATED"
    if mode=="P1COUNT":
        p=r["p1"]; n1=[i for i,c in enumerate(p) if c=="N"]; s1=[i for i,c in enumerate(p) if c=="S"]
        lo1,hi1=max(n1),min(s1); return "NOT_DISTINGUISHED" if (hi1-lo1-1)>x else "LOCATED"
def price(mode, x):
    err=collections.Counter()
    for r in rows:
        v=verdict(r,mode,x); intended=INTENDED[r["cls"]]
        e = (v=="NOT_DISTINGUISHED") if intended!="NOT_DISTINGUISHED" else (v!="NOT_DISTINGUISHED")
        err[(r["ens"],r["cls"])]+=e
    return err
def report(mode, x):
    err=price(mode,x); worst=max(err.values()); fails=[k for k,v in err.items() if not cp_ok(v)]
    cells=" ".join(f"{err[('design',c)]:3}/{err[('held_out',c)]:3}" for c in A.CLASSES)
    print(f"{mode:8}{str(x):>8}  pass={'YES' if not fails else 'no ':3} worst={worst:3}  {cells}")
print("classes:", " | ".join(c[:10] for c in A.CLASSES))
print("sanity: frozen COUNT 3 should reproduce the committed counts (gentle 500, abrupt 59/54...)")
report("COUNT",3)
for k in (4,5,6,8,10,12,16,20): report("COUNT",k)
for k in (2,3,4): report("P1COUNT",k)
for W in (60_000,70_000,80_000,90_000,100_000,110_000,120_000,130_000,140_000,150_000,160_000,180_000): report("WIDTH",W)
# physical band-width distributions per class (final), to see the separation
import statistics as st
print("\nfinal band physical width (micro) by class, both ensembles pooled: min / p5 / median / p95 / max  (sweeps with a band)")
for c in A.CLASSES:
    ws=[]
    for r in rows:
        if r["cls"]!=c: continue
        lab,lv=r["lf"],r["lv"]; n=[i for i,ch in enumerate(lab) if ch=="N"]; s=[i for i,ch in enumerate(lab) if ch=="S"]
        if n and s and max(n)<min(s): ws.append(lv[min(s)]-lv[max(n)])
    if ws:
        ws.sort(); q=lambda p: ws[int(p*(len(ws)-1))]
        print(f"  {c:34} n={len(ws):4} {ws[0]:7} {q(.05):7} {q(.5):7} {q(.95):7} {ws[-1]:7}")
    else: print(f"  {c:34} no band")
