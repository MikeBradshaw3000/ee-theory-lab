"""NONCANONICAL design evidence. Ideal-M2/M3 replay of all 12,000 committed sweeps, storing the final
(pass-1 + pass-2) label/level sequence so candidate verdict rules can be priced offline."""
import sys, json
sys.path.insert(0, ".")
import numpy as np
from mfa_instrument.e1 import audit as A, verdict as V, classify as C
from mfa_instrument.e1.config import E1_LEVELS_MICRO
N = A.N_SEEDS
MAP = {"NULL":"NO_SUSTAINED","SUSTAINED":"SUSTAINED","DIP":"UNRESOLVED"}
def lab(a, m, prm, u):
    return C.level_label(C.level_counts([MAP[A.regime_at(a,m,prm,float(u[s]))[0]] for s in range(N)]))
rows = []
for ens, master in (("design", A.AUDIT_MASTER), ("held_out", A.HELD_OUT_MASTER)):
    for ci, cls in enumerate(A.CLASSES):
        for i in range(A.SWEEPS_PER_CLASS):
            prm, _ = A.draw_params(cls, master, ci, i)
            u = np.random.default_rng(np.random.SeedSequence([master, ci, i])).random(N)
            l1 = tuple(lab(cls, m, prm, u) for m in E1_LEVELS_MICRO)
            d = V.route(l1, E1_LEVELS_MICRO)
            if d.insertions_micro:
                l2 = tuple(lab(cls, m, prm, u) for m in d.insertions_micro)
                mg = sorted(list(zip(E1_LEVELS_MICRO, l1)) + list(zip(d.insertions_micro, l2)))
                lv = [m for m, _ in mg]; lf = "".join(x for _, x in mg)
            else:
                lv = list(E1_LEVELS_MICRO); lf = "".join(l1)
            vf = V.evaluate(lf, lv)
            rows.append(dict(ens=ens, cls=cls, sweep=i, w=prm.width_micro, onset=prm.onset_micro, row=d.row,
                             p1="".join(l1), lf=lf, lv=lv, verdict=vf.verdict, rule=vf.rule))
json.dump(rows, open(sys.argv[1], "w"))
print(len(rows))
