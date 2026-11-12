#!/usr/bin/env python3
"""Flight 9 pre-contract terrain probe -- NONCANONICAL design evidence only.

Governed by FLIGHT_9_PRE_PROBE_DECLARATION (design/flight9/). This script is not an instrument module: it has
no governance record, no qualification and no canonical master, and nothing it writes may be represented as a
Flight 9 result. It implements the carried hazard rule of Contract F8 s2.4 with a per-cell lambda array:

    inactive -> active:   P_i = 1 - exp(-[eta_floor + g*lambda_i*d_i(t)]*dt)
    active   -> inactive: P   = 1 - exp(-mu*dt)

synchronous, Moore-8 periodic, one full-grid uniform per tick; bases frozen; Q off; drive 0; noise off.

Modes
  --identities            terrain arrays, their SHA-256, lambda ranges, spectral radius and g_spec. NO dynamics.
  --reduction REPO_ROOT   the constant-lambda step equals the placed f8 scalar step (exact array equality).
  --run DECLARATION OUT   the declared menu, exactly once. Refuses if OUT exists.
"""
from __future__ import annotations

import argparse, hashlib, json, math, os, platform, sys, time
import numpy as np

# ------------------------------------------------------------------ carried constants (Contract F8 v0.8.4)
MU = 0.2
DT = 1
ETA0 = -math.log(1.0 - 0.01)
TICKS = 3000
TAIL = 1000
Q_DE = 1.0 - math.exp(-MU * DT)

# ------------------------------------------------------------------ the declared menu
PROBE_MASTER = 9920261112            # noncanonical; never reused for any canonical or qualification purpose
GRIDS = (50, 100)                    # L = 100 refines the same unit-torus terrain (patches double in lattice units)
KAPPA_MICRO = (750000, 1000000, 1250000, 1500000, 1750000, 2000000, 2500000, 3000000)
N_SEEDS = 4
WINDOWS = (1, 10, 100)
OBJECTS = ("realization", "skeleton_high")
ARMS = (("T0", "P"), ("TA", "P"), ("TA", "H"), ("TB", "P"), ("TB", "H"), ("TC", "P"), ("TC", "H"))
TERRAIN_CODE = {"T0": 0, "TA": 1, "TB": 2, "TC": 3}
COMP_CODE = {"P": 0, "H": 1}
OBJECT_CODE = {"realization": 0, "skeleton_high": 1}


def _c(z: np.ndarray) -> np.ndarray:
    return np.cos(2.0 * np.pi * z)


def terrain(name: str, L: int):
    """Bases (v, u, r) on the unit torus, cell (i, j) at x = i/L, y = j/L. Closed-form; no random draw."""
    x = (np.arange(L, dtype=np.float64) / L)[:, None] * np.ones((1, L))
    y = np.ones((L, 1)) * (np.arange(L, dtype=np.float64) / L)[None, :]
    if name == "T0":                                   # flat
        v = np.full((L, L), 0.8); u = v.copy(); r = v.copy()
    elif name == "TA":                                 # concordant: all three bases equal
        t = 0.6 + 0.15 * (_c(x) + _c(y))               # in [0.3, 0.9]
        v = t.copy(); u = t.copy(); r = t.copy()
    elif name == "TB":                                 # cross-gradient: height varies with x only
        s = 0.6 + 0.2 * _c(x)                          # (v + u)/2 in [0.4, 0.8]
        d = 0.2 * _c(y)                                # (v - u)/2 in [-0.2, 0.2]
        v = s + d; u = s - d; r = np.full((L, L), 0.8)
    elif name == "TC":                                 # near-face: u falls to 0.05 at the patch centre
        bump = (((1.0 + _c(x - 0.5)) / 2.0) ** 4) * (((1.0 + _c(y - 0.5)) / 2.0) ** 4)
        v = np.full((L, L), 0.9); r = v.copy(); u = 0.9 - 0.85 * bump
    else:
        raise ValueError(name)
    for b in (v, u, r):
        if not (b.min() >= 0.0 and b.max() <= 1.0): raise ValueError(f"{name}: base outside [0, 1]")
    return v, u, r


def tc_bump(L: int) -> np.ndarray:
    x = (np.arange(L, dtype=np.float64) / L)[:, None] * np.ones((1, L))
    y = np.ones((L, 1)) * (np.arange(L, dtype=np.float64) / L)[None, :]
    return (((1.0 + _c(x - 0.5)) / 2.0) ** 4) * (((1.0 + _c(y - 0.5)) / 2.0) ** 4)


def compose(comp: str, v, u, r) -> np.ndarray:
    if comp == "P": return v * u * r                   # F_canonical
    if comp == "H": return (v + u + r) / 3.0           # F_baseline (rival only)
    raise ValueError(comp)


def moore_sum(a: np.ndarray) -> np.ndarray:
    out = np.zeros_like(a, dtype=np.float64)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0: continue
            out += np.roll(np.roll(a, di, axis=0), dj, axis=1)
    return out


def spectral_radius(lam: np.ndarray, tol: float = 1e-14, max_iter: int = 200000) -> float:
    """spr(diag(lam) A / 8) by power iteration on the similar symmetric operator D^(1/2) (A/8) D^(1/2)."""
    if float(lam.max()) <= 0.0: return 0.0
    s = np.sqrt(lam)
    w = np.ones_like(lam) / math.sqrt(lam.size)
    last = 0.0
    for _ in range(max_iter):
        z = s * moore_sum(s * w) / 8.0
        ray = float(np.sum(w * z))
        n = float(np.linalg.norm(z))
        if n == 0.0: return 0.0
        w = z / n
        if abs(ray - last) <= tol * max(1.0, abs(ray)): return ray
        last = ray
    raise RuntimeError("spectral_radius: no convergence")


def sha(a: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.float64).tobytes()).hexdigest()


def identities() -> dict:
    out = {"mu": MU, "dt": DT, "eta0": ETA0, "q": Q_DE, "arms": []}
    for L in GRIDS:
        for name, comp in ARMS:
            v, u, r = terrain(name, L)
            lam = compose(comp, v, u, r)
            spr = spectral_radius(lam)
            out["arms"].append({
                "L": L, "terrain": name, "composition": comp,
                "bases_sha256": hashlib.sha256(b"".join(np.ascontiguousarray(b).tobytes() for b in (v, u, r))).hexdigest(),
                "lambda_sha256": sha(lam), "lambda_min": float(lam.min()), "lambda_max": float(lam.max()),
                "lambda_mean": float(lam.mean()), "spectral_radius": spr,
                "g_spec": (Q_DE / (DT * spr)) if spr > 0 else None,
            })
    return out


def step(x: np.ndarray, u: np.ndarray, *, eta_floor: float, g: float, lam: np.ndarray) -> np.ndarray:
    d = moore_sum(x.astype(np.float64)) / 8.0
    p_act = 1.0 - np.exp(-(eta_floor + g * lam * d) * DT)
    return np.where(x, u >= Q_DE, u < p_act)


def generator(L, name, comp, obj, kappa_micro, seed_index) -> np.random.Generator:
    ss = np.random.SeedSequence([PROBE_MASTER, L, TERRAIN_CODE[name], COMP_CODE[comp], OBJECT_CODE[obj], kappa_micro, seed_index])
    return np.random.Generator(np.random.PCG64(ss))


def window_summaries(tail_states: np.ndarray, W: int):
    """Per cell: A = active windows, R0 = observed inactive segments, first and last window states.
    Windows are non-overlapping, equal-width, complete, aligned to the tail's first tick; a window is active if
    the cell is active at any tick in it."""
    n = tail_states.shape[0] // W
    yw = tail_states[: n * W].reshape(n, W, *tail_states.shape[1:]).any(axis=1)
    A = yw.sum(axis=0).astype(np.int32)
    K = (yw[1:] != yw[:-1]).sum(axis=0).astype(np.int32)
    first = yw[0].astype(np.int8); last = yw[-1].astype(np.int8)
    R0 = ((K + 2 - first - last) // 2).astype(np.int32)
    R0 = np.where(A == n, 0, R0).astype(np.int32)
    return n, A, R0, first, last


def run_one(L, name, comp, obj, kappa_micro, seed_index, lam, g) -> dict:
    eta = ETA0 if obj == "realization" else 0.0
    gen = generator(L, name, comp, obj, kappa_micro, seed_index)
    if obj == "realization":
        a = 1.0 - math.exp(-eta * DT); x = gen.random((L, L)) < (a / (a + Q_DE))
    else:
        x = np.ones((L, L), dtype=bool)
    tail_states = np.zeros((TAIL, L, L), dtype=bool)
    counts = np.zeros(TICKS + 1, dtype=np.int64); counts[0] = int(x.sum())
    extinction = None
    for t in range(1, TICKS + 1):
        if extinction is None:
            x = step(x, gen.random((L, L)), eta_floor=eta, g=g, lam=lam)
            counts[t] = int(x.sum())
            if eta == 0.0 and counts[t] == 0: extinction = t
        if t > TICKS - TAIL: tail_states[t - (TICKS - TAIL) - 1] = x if extinction is None else False
    res = {"tail_density": float(counts[TICKS - TAIL + 1:].mean() / (L * L)), "extinction_tick": extinction,
           "survival": bool((counts[TICKS - TAIL + 1:] > 0).all())}
    arrays = {}
    for W in WINDOWS:
        n, A, R0, first, last = window_summaries(tail_states, W)
        arrays[f"A_W{W}"] = A; arrays[f"R0_W{W}"] = R0; arrays[f"first_W{W}"] = first; arrays[f"last_W{W}"] = last
        res[f"n_windows_W{W}"] = int(n)
    return res, arrays


def reduction_check(repo_root: str) -> dict:
    sys.path.insert(0, os.path.join(repo_root, "flights", "mfa_fidelity", "instrument"))
    from mfa_instrument.f8 import dynamics as F8D          # the placed scalar step
    L = 50; ok = True; ticks = 0
    for eta in (0.0, ETA0):
        for lam_bar in (0.05, 0.2758, 0.45):
            gen = np.random.Generator(np.random.PCG64(np.random.SeedSequence([PROBE_MASTER, 777, int(lam_bar * 1e6), int(eta > 0)])))
            x = gen.random((L, L)) < 0.4
            lam = np.full((L, L), lam_bar)
            for _ in range(200):
                u = gen.random((L, L))
                a = F8D.step(x, u, eta_floor=eta, g=1.0, lambda_bar=lam_bar, mu=MU)
                b = step(x, u, eta_floor=eta, g=1.0, lam=lam)
                ok = ok and bool(np.array_equal(a, b)); ticks += 1
                x = a
    return {"reduction_equal": ok, "ticks_compared": ticks, "f8_dynamics_sha256": hashlib.sha256(open(F8D.__file__, "rb").read()).hexdigest()}


def run_menu(declaration_path: str, out_dir: str) -> None:
    if os.path.exists(out_dir): raise SystemExit(f"refusing: {out_dir} exists (the menu runs exactly once)")
    decl = hashlib.sha256(open(declaration_path, "rb").read()).hexdigest()
    os.makedirs(out_dir)
    ident = identities()
    gspec = {(a["L"], a["terrain"], a["composition"]): a["g_spec"] for a in ident["arms"]}
    manifest = {"declaration_sha256": decl, "script_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                "probe_master": PROBE_MASTER, "platform": platform.platform(), "python": sys.version.split()[0],
                "numpy": np.__version__, "identities": ident, "runs": []}
    for L in GRIDS:
        for name, comp in ARMS:
            v, u, r = terrain(name, L); lam = compose(comp, v, u, r)
            for obj in OBJECTS:
                for km in KAPPA_MICRO:
                    g = (km / 1e6) * gspec[(L, name, comp)]
                    for si in range(N_SEEDS):
                        t0 = time.time()
                        res, arrays = run_one(L, name, comp, obj, km, si, lam, g)
                        fn = f"L{L}_{name}_{comp}_{obj}_k{km}_s{si}.npz"
                        np.savez_compressed(os.path.join(out_dir, fn), **arrays)
                        res.update({"L": L, "terrain": name, "composition": comp, "object": obj, "kappa_micro": km,
                                    "g": g, "seed_index": si, "seconds": time.time() - t0, "file": fn,
                                    "file_sha256": hashlib.sha256(open(os.path.join(out_dir, fn), "rb").read()).hexdigest()})
                        manifest["runs"].append(res)
                        with open(os.path.join(out_dir, "PROBE_MANIFEST.json"), "w", newline="\n") as f:
                            json.dump(manifest, f, indent=1, sort_keys=True)
    with open(os.path.join(out_dir, "COMPLETE"), "w", newline="\n") as f:
        f.write(f"{len(manifest['runs'])} runs\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--identities", action="store_true")
    ap.add_argument("--reduction", metavar="REPO_ROOT")
    ap.add_argument("--run", nargs=2, metavar=("DECLARATION", "OUT"))
    a = ap.parse_args()
    if a.identities: print(json.dumps(identities(), indent=1, sort_keys=True))
    elif a.reduction: print(json.dumps(reduction_check(a.reduction), indent=1, sort_keys=True))
    elif a.run: run_menu(a.run[0], a.run[1])
    else: ap.print_help()
