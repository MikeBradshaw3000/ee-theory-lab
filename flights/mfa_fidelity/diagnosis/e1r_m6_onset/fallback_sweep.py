"""NONCANONICAL. For all 12,000 committed sweeps: router row, fallback move/drop counts, and whether the
final verdict is an error — to test whether fallback arithmetic is associated with the onset failures."""
import sys, json, collections
sys.path.insert(0, ".")
import numpy as np
from mfa_instrument.e1 import audit as A, verdict as V, classify as C
from mfa_instrument.e1.config import E1_LEVELS_MICRO
N = A.N_SEEDS
def lab(a, m, prm, u):
    return C.level_label(C.level_counts([{"NULL":"NO_SUSTAINED","SUSTAINED":"SUSTAINED","DIP":"UNRESOLVED"}[A.regime_at(a,m,prm,float(u[s]))[0]] for s in range(N)]))
rows = []
for ens, master in (("design", A.AUDIT_MASTER), ("held_out", A.HELD_OUT_MASTER)):
    for ci, cls in enumerate(A.CLASSES):
        intended = A.INTENDED[cls][0]
        for i in range(A.SWEEPS_PER_CLASS):
            prm, _ = A.draw_params(cls, master, ci, i)
            u = np.random.default_rng(np.random.SeedSequence([master, ci, i])).random(N)
            l1 = tuple(lab(cls, m, prm, u) for m in E1_LEVELS_MICRO)
            d = V.route(l1, E1_LEVELS_MICRO)
            if d.insertions_micro:
                l2 = tuple(lab(cls, m, prm, u) for m in d.insertions_micro)
                mg = sorted(list(zip(E1_LEVELS_MICRO, l1)) + list(zip(d.insertions_micro, l2)))
                vf = V.evaluate(tuple(x for _, x in mg), tuple(m for m, _ in mg))
            else:
                vf = V.evaluate(l1, E1_LEVELS_MICRO)
            err = (vf.verdict == "NOT_DISTINGUISHED") if intended != "NOT_DISTINGUISHED" else (vf.verdict != "NOT_DISTINGUISHED")
            rows.append(dict(ens=ens, cls=cls, sweep=i, row=d.row, n_ins=len(d.insertions_micro), moves=len(d.fallback_moves), drops=len(d.fallback_drops), err=int(err), rule=vf.rule))
json.dump(rows, open(sys.argv[1], "w"))
c = collections.defaultdict(lambda: [0, 0])
for r in rows:
    k = (r["cls"], r["row"], r["moves"] > 0); c[k][0] += 1; c[k][1] += r["err"]
print(f"{'class':34} {'row':6} fallback   n   err")
for k in sorted(c): print(f"{k[0]:34} {k[1]:6} {str(k[2]):8} {c[k][0]:4} {c[k][1]:4}")
print("drops total:", sum(r["drops"] for r in rows), "| n_ins distribution:", dict(collections.Counter(r["n_ins"] for r in rows)))
