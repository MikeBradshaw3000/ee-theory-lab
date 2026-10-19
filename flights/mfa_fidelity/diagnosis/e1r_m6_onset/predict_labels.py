"""NONCANONICAL DIAGNOSIS — E1-R M6 onset failures. Not a result of record.

Arithmetic predictor: for every sweep of every class (both committed masters), reproduce the
frozen parameter draw and the per-seed regime-assignment uniforms EXACTLY (same SeedSequence
hierarchy as audit.run_sweep), assume M2/M3 classify every run's regime correctly (SUSTAINED ->
"SUSTAINED", NULL -> "NO_SUSTAINED", DIP -> "UNRESOLVED"), derive the pass-1 labels, route with
the frozen M4 router, derive the pass-2 labels at the inserted levels, and evaluate with the
frozen M4 verdict function.  No run is generated; no threshold is consulted.

If the predicted per-class error counts reproduce the committed audit records, the committed
failures are fully accounted for by the generator's regime geometry + M4 (router + verdict) with
zero contribution from M2/M3 misclassification.  Any residual is the M2/M3 contribution.
"""
import sys, json, collections
sys.path.insert(0, ".")
import numpy as np
from mfa_instrument.e1 import audit as A
from mfa_instrument.e1 import verdict as V
from mfa_instrument.e1 import classify as C
from mfa_instrument.e1.config import E1_LEVELS_MICRO, E1_SEED_PANEL

N = A.N_SEEDS


def label_at(archetype, m, prm, seed_us):
    statuses = []
    for s_idx in range(N):
        regime, _ = A.regime_at(archetype, m, prm, float(seed_us[s_idx]))
        statuses.append({"NULL": "NO_SUSTAINED", "SUSTAINED": "SUSTAINED", "DIP": "UNRESOLVED"}[regime])
    return C.level_label(C.level_counts(statuses))


def predict(archetype, sweep_index, master):
    ci = A.CLASSES.index(archetype)
    prm, attempts = A.draw_params(archetype, master, ci, sweep_index)
    g = np.random.default_rng(np.random.SeedSequence([int(master), ci, int(sweep_index)]))
    seed_us = g.random(N)
    lab1 = tuple(label_at(archetype, m, prm, seed_us) for m in E1_LEVELS_MICRO)
    v1 = V.evaluate(lab1, E1_LEVELS_MICRO)
    d = V.route(lab1, E1_LEVELS_MICRO)
    if d.insertions_micro:
        lab2 = tuple(label_at(archetype, m, prm, seed_us) for m in d.insertions_micro)
        merged = sorted(list(zip(E1_LEVELS_MICRO, lab1)) + list(zip(d.insertions_micro, lab2)))
        lv = tuple(m for m, _ in merged); lf = tuple(l for _, l in merged)
    else:
        lv, lf = tuple(E1_LEVELS_MICRO), lab1
    vf = V.evaluate(lf, lv)
    span1 = v1.evidence and dict(v1.evidence).get("boundary_span")
    spanf = dict(vf.evidence).get("boundary_span")
    return dict(sweep=sweep_index, width=prm.width_micro, onset=prm.onset_micro, temporal=prm.temporal,
                p1_verdict=v1.verdict, p1_rule=v1.rule, p1_span=span1, row=d.row, n_ins=len(d.insertions_micro),
                f_verdict=vf.verdict, f_cause=vf.cause, f_rule=vf.rule, f_span=spanf,
                p1=''.join(lab1), final=''.join(lf))


if __name__ == "__main__":
    masters = {"design": A.AUDIT_MASTER, "held_out": A.HELD_OUT_MASTER}
    out = {}
    for ens, master in masters.items():
        for cls in A.CLASSES:
            intended = A.INTENDED[cls][0]
            rows = [predict(cls, i, master) for i in range(A.SWEEPS_PER_CLASS)]
            if intended in ("LOCATED", "NOT_PRODUCED"):
                err = sum(r["f_verdict"] == "NOT_DISTINGUISHED" for r in rows)
            else:
                err = sum(r["f_verdict"] != "NOT_DISTINGUISHED" for r in rows)
            out[(ens, cls)] = rows
            vc = collections.Counter(r["f_verdict"] for r in rows)
            p1 = collections.Counter(r["p1_verdict"] for r in rows)
            print(f"{ens:8} {cls:34} pred_err={err:3}  final={dict(vc)}  pass1={dict(p1)}")
    json.dump({f"{e}:{c}": v for (e, c), v in out.items()}, open(sys.argv[1], "w"))
