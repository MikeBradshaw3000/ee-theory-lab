#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cycle 3, Wave Two: Two-Channel Ordering Probe (TCOP) — Seeding Apparatus (BUILD 3)
Governed by: TCOP_SEEDING_IMPLEMENTATION_SPEC.md (CANONICAL), contract 8c94d8c, addendum 8a777e6.
Stages: preflight | stageA | stageB | stageC (strict CLI whitelist; execution is Mike's
bounded seed authorization). The run script evaluates NOTHING (no G1-G4, no onset,
no classification); it produces states and diagnostics for the later read.
Dynamical core: minimal-diff from committed c3_w2_rule_c_m2.py (apparatus functions
byte-for-byte). Harness (manifest/digests/staging/atomic promotion/F3 gates): new code.
"""

import sys
import os
import json
import hashlib
import random

# ==========================================
# Pre-flight Verification (Fail Fast) — committed block
# ==========================================
if sys.prefix == sys.base_prefix:
    raise RuntimeError("PRE-FLIGHT FAIL: Virtual environment is not active.")

if sys.version_info[:2] != (3, 14):
    raise RuntimeError(f"PRE-FLIGHT FAIL: Python 3.14.x required. Found: {sys.version_info[:2]}")

try:
    import numpy as np
    import pandas as pd
    import mesa
except ImportError as e:
    raise RuntimeError(f"PRE-FLIGHT FAIL: Critical import missing. {e}")

if np.__version__ != "2.4.4":
    raise RuntimeError(f"PRE-FLIGHT FAIL: numpy 2.4.4 required. Found: {np.__version__}")

if not os.path.exists(os.path.join("cycle3", "c3_ctl_001_battery.py")):
    raise RuntimeError("PRE-FLIGHT FAIL: cycle3 directory or c3_ctl_001_battery.py unreachable.")

# ==========================================
# Locked Apparatus Parameters
# ==========================================
GRID_SIZE = 50
N_CELLS = GRID_SIZE * GRID_SIZE
TICKS_PER_RUN = 400
BLOCK_LENGTH = 25
N_BLOCKS = TICKS_PER_RUN // BLOCK_LENGTH
WINDOW_LENGTH = 100
WINDOW_STEP = 25
SEEDS = [42, 137, 256, 1024, 31415]
TARGET_RHO_INIT = 0.10
INIT_ACTIVE_CELLS = round(TARGET_RHO_INIT * N_CELLS)

# SS-001 & Degeneracy Thresholds (committed)
THRESH_RELATIVE_DRIFT = 0.10
THRESH_RHO_CV = 0.10
THRESH_RHO_RANGE_OVER_MEAN = 0.25
LIFTED_THRESHOLD = 0.05
VAR_EPSILON = 1e-3

# Null Convention Parameters (committed)
PERMUTATIONS = 199
LOW_Z_THRESH = 2.0

# TCOP frozen inputs
LAMBDA = 0.40
S_SURV = 0.40
LOGIT_L = float(np.log(LAMBDA / (1.0 - LAMBDA)))
U_TIERS = [0.10, 0.25, 0.50]
DELTA_RHO_MATCH = 0.00283
TOL_U2 = DELTA_RHO_MATCH / 2.0
CONTRACT_COMMIT = "8c94d8c"
ADDENDUM_COMMIT = "8a777e6"

# COMMITTED c -> kappa map at Lambda = 0.40 (frozen input; NEVER re-derived)
KAPPA_MAP = [
    ( 0.00,  0.0000),
    (+0.05, +0.1042), (-0.05, -0.1042),
    (+0.10, +0.2090), (-0.10, -0.2090),
    (+0.20, +0.4221), (-0.20, -0.4221),
    (+0.35, +0.7599), (-0.35, -0.7599),
]

DATA_DIR = os.path.join("cycle3", "data_out")
MANIFEST_PATH = os.path.join(DATA_DIR, "c3_w2_tcop_preflight.json")
BLOCK_CSV = os.path.join(DATA_DIR, "c3_w2_tcop_blocks.csv")
WINDOW_CSV = os.path.join(DATA_DIR, "c3_w2_tcop_windows.csv")
STAGE_MARKER = os.path.join(DATA_DIR, "c3_w2_tcop_stage_{stage}.done")
DRIVEN_CHECK_ATOL = 1e-12
FIXED_CHECK_SEED = 777

# ==========================================
# Apparatus Functions (byte-for-byte, committed c3_w2_rule_c_m2.py)
# ==========================================

def calculate_morans_i_toroidal_8(grid):
    grid_mean = np.mean(grid)
    grid_var = np.var(grid)
    if grid_var < 1e-9:
        return 0.0
    centered = grid - grid_mean
    w_sum = (
        np.roll(centered, 1, axis=0) + np.roll(centered, -1, axis=0) +
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(centered, -1, axis=0), -1, axis=1)
    )
    numerator = np.sum(centered * w_sum)
    denominator = np.sum(centered**2)
    return (1.0 / 8.0) * (numerator / denominator)

def batch_morans_i_toroidal_8(grids):
    grid_mean = np.mean(grids, axis=(1, 2), keepdims=True)
    grid_var = np.var(grids, axis=(1, 2), keepdims=True)
    valid_mask = np.squeeze(grid_var) > 1e-9
    if not np.any(valid_mask):
        return np.zeros(grids.shape[0])
    centered = grids - grid_mean
    w_sum = (
        np.roll(centered, 1, axis=1) + np.roll(centered, -1, axis=1) +
        np.roll(centered, 1, axis=2) + np.roll(centered, -1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, 1, axis=1), -1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), 1, axis=2) +
        np.roll(np.roll(centered, -1, axis=1), -1, axis=2)
    )
    numerator = np.sum(centered * w_sum, axis=(1, 2))
    denominator = np.sum(centered**2, axis=(1, 2))
    I_vals = np.zeros(grids.shape[0])
    np.divide(numerator, denominator, out=I_vals, where=valid_mask)
    return (1.0 / 8.0) * I_vals

def compute_persistence_null(grid, actual_I, num_permutations=PERMUTATIONS):
    if np.var(grid) < 1e-9:
        return 0.0
    flat_grid = grid.flatten()
    null_Is = np.zeros(num_permutations)
    for i in range(num_permutations):
        shuffled = np.random.permutation(flat_grid).reshape((GRID_SIZE, GRID_SIZE))
        null_Is[i] = calculate_morans_i_toroidal_8(shuffled)
    null_std = np.std(null_Is)
    return (actual_I - np.mean(null_Is)) / null_std if null_std > 1e-9 else 0.0

def compute_meanI_state_null(actual_grids, actual_meanI, num_permutations=PERMUTATIONS):
    null_meanIs = np.zeros(num_permutations)
    ticks, h, w = actual_grids.shape
    flat_grids = actual_grids.reshape(ticks, -1)
    for p in range(num_permutations):
        rand_idx = np.random.rand(ticks, h * w).argsort(axis=1)
        shuffled_flat = np.take_along_axis(flat_grids, rand_idx, axis=1)
        tick_Is = batch_morans_i_toroidal_8(shuffled_flat.reshape(ticks, h, w))
        null_meanIs[p] = np.mean(tick_Is)
    null_std = np.std(null_meanIs)
    return (actual_meanI - np.mean(null_meanIs)) / null_std if null_std > 1e-9 else 0.0

def evaluate_window_ss(rho_window):
    mean_rho = np.mean(rho_window)
    epsilon = 1e-9
    t = np.arange(WINDOW_LENGTH)
    slope, _ = np.polyfit(t, rho_window, 1)
    relative_drift = (abs(slope) * WINDOW_LENGTH) / (mean_rho + epsilon)
    rho_cv = np.std(rho_window) / (mean_rho + epsilon)
    rho_range_over_mean = (np.max(rho_window) - np.min(rho_window)) / (mean_rho + epsilon)

    steady = (relative_drift < THRESH_RELATIVE_DRIFT) and \
             (rho_cv < THRESH_RHO_CV) and \
             (rho_range_over_mean < THRESH_RHO_RANGE_OVER_MEAN)
    lifted = mean_rho > LIFTED_THRESHOLD

    return relative_drift, rho_cv, rho_range_over_mean, mean_rho, steady, lifted

def run_parity_check():
    sys.path.insert(0, os.path.abspath("cycle3"))
    try:
        import c3_ctl_001_battery as ctl
        import c3_ss_001_battery as ss

        PARITY_SEED = 7
        np.random.seed(PARITY_SEED)

        test_grids = np.random.randint(0, 2, size=(100, 50, 50))
        test_rho = np.mean(test_grids, axis=(1, 2))

        assert np.isclose(calculate_morans_i_toroidal_8(test_grids[0]),
                          ctl.calculate_morans_i_toroidal_8(test_grids[0]))

        assert np.allclose(batch_morans_i_toroidal_8(test_grids),
                           ctl.batch_morans_i_toroidal_8(test_grids))

        loc_res = evaluate_window_ss(test_rho)
        ext_res = ss.evaluate_window(test_rho)
        assert np.isclose(loc_res[0], ext_res["Relative_Drift"])
        assert np.isclose(loc_res[1], ext_res["Rho_CV"])
        assert loc_res[4] == ext_res["Steady_State_Candidate"]

        np.random.seed(PARITY_SEED)
        test_grid_2d = np.random.randint(0, 2, size=(50, 50))
        actual_I_persist = calculate_morans_i_toroidal_8(test_grid_2d)

        np.random.seed(PARITY_SEED)
        local_z_persist = compute_persistence_null(test_grid_2d, actual_I_persist)
        np.random.seed(PARITY_SEED)
        ctl_z_persist, _ = ctl.compute_persistence_null(test_grid_2d, actual_I_persist)
        assert np.isclose(local_z_persist, ctl_z_persist), \
            "PRE-FLIGHT FAIL: persistence null parity broken."

        np.random.seed(PARITY_SEED)
        test_grids_3d = np.random.randint(0, 2, size=(100, 50, 50))
        actual_meanI = np.mean(batch_morans_i_toroidal_8(test_grids_3d))

        np.random.seed(PARITY_SEED)
        local_z_meanI = compute_meanI_state_null(test_grids_3d, actual_meanI)
        np.random.seed(PARITY_SEED)
        ctl_z_meanI, _ = ctl.compute_meanI_state_null(test_grids_3d, actual_meanI)
        assert np.isclose(local_z_meanI, ctl_z_meanI), \
            "PRE-FLIGHT FAIL: meanI_state null parity broken."

    except AssertionError as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check broken. Reimplementation diverges from apparatus. {e}")
    except Exception as e:
        raise RuntimeError(f"PRE-FLIGHT FAIL: Parity check execution error: {e}")
    finally:
        sys.path.pop(0)

def get_neighbor_count(grid):
    return (
        np.roll(grid, 1, axis=0) + np.roll(grid, -1, axis=0) +
        np.roll(grid, 1, axis=1) + np.roll(grid, -1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, 1, axis=0), -1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), 1, axis=1) +
        np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
    )

# ==========================================
# TCOP helpers
# ==========================================

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sanitize_float(v):
    return f"{v:+.4f}".replace("-", "m").replace("+", "p").replace(".", "_")

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def u_t_for(mode, tier, u_const, block_idx):
    """Single source of truth for the common-mode input at a block."""
    if mode == "cm0":
        return u_const
    if tier == 0.0:
        return 0.0
    return [0.0, tier / 2.0, tier][block_idx % 3]

def step_tcop_core(grid, u_t, kappa, rand_grid):
    """CM-1/CM-0 update. u_t enters the becoming-active logit ONLY; survival bare p_Lambda.
    One shared rand_grid for both branches (committed discipline)."""
    neighbors = get_neighbor_count(grid)
    q_i = neighbors / 8.0
    g_q = 2.0 * q_i - 1.0
    p_become = sigmoid(LOGIT_L + u_t + kappa * g_q)
    become_active = (grid == 0) & (rand_grid < p_become)
    stay_active = (grid == 1) & (rand_grid < LAMBDA)
    return (become_active | stay_active).astype(int), p_become

# ==========================================
# Static-offset preflight solve (finite-block periodic orbit; solved-always)
# ==========================================

def scalar_periodic_orbit_mean(u_tier, n_cycles=400):
    """Iterate rho_{t+1} = s*rho + (1-rho)*sigma(logit+L_t) over the frozen 3-block schedule
    to the periodic orbit; return mean rho over one converged period (exact for E[rho] at kappa=0)."""
    rho = TARGET_RHO_INIT
    levels = [0.0, u_tier / 2.0, u_tier]
    trace = []
    for cyc in range(n_cycles):
        cycle_rhos = []
        for lvl in levels:
            p = sigmoid(LOGIT_L + lvl)
            for _ in range(BLOCK_LENGTH):
                rho = S_SURV * rho + (1.0 - rho) * p
                cycle_rhos.append(rho)
        if cyc >= n_cycles - 2:
            trace.append(np.mean(cycle_rhos))
    if abs(trace[-1] - trace[-2]) > 1e-12:
        raise RuntimeError("PREFLIGHT FAIL: periodic orbit did not converge.")
    return float(trace[-1])

def scalar_static_equilibrium(u_const):
    p = sigmoid(LOGIT_L + u_const)
    return float(p / (1.0 - S_SURV + p))

def solve_static_offsets():
    """Bisection: u_const s.t. static equilibrium == periodic-orbit mean. Solved-always."""
    offsets = {}
    for u in U_TIERS:
        target = scalar_periodic_orbit_mean(u)
        lo, hi = 0.0, u
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if scalar_static_equilibrium(mid) < target:
                lo = mid
            else:
                hi = mid
        u_c = 0.5 * (lo + hi)
        rho_u2 = scalar_static_equilibrium(u / 2.0)
        gap = abs(rho_u2 - target)
        offsets[str(u)] = {
            "u_const_solved": float(u_c),
            "rho_bar_sched": target,
            "rho_static_u_half": rho_u2,
            "u_half_gap": float(gap),
            "u_half_gap_within_tol_diagnostic": bool(gap <= TOL_U2),
            "tolerance": TOL_U2,
            "selected": float(u_c),
            "rule": "solved-always (Mike-ratified primary)",
        }
    return offsets

# ==========================================
# Driven-path construction check (hard pre-data gate)
# ==========================================

def verify_driven_path_construction(offsets):
    rng = np.random.default_rng(FIXED_CHECK_SEED)
    for trial in range(3):
        grid = (rng.random((GRID_SIZE, GRID_SIZE)) < 0.4).astype(int)
        rand_grid = rng.random((GRID_SIZE, GRID_SIZE))
        neighbors = get_neighbor_count(grid)
        q = neighbors / 8.0
        u_levels = {0.0}
        for u in U_TIERS:
            u_levels |= {u / 2.0, u, offsets[str(u)]["selected"]}
        for u_t in sorted(u_levels):
            for kappa in [0.0, +0.7599, -0.7599]:
                _, p_impl = step_tcop_core(grid, u_t, kappa, rand_grid)
                p_ref = sigmoid(LOGIT_L + u_t + kappa * (2.0 * q - 1.0))
                if not np.allclose(p_impl, p_ref, rtol=0.0, atol=DRIVEN_CHECK_ATOL):
                    raise RuntimeError(f"PREFLIGHT FAIL: driven-path p_become mismatch at u_t={u_t}, kappa={kappa}")
                # survival invariance: the stay branch uses bare LAMBDA regardless of u_t/kappa
                new_a, _ = step_tcop_core(np.ones_like(grid), u_t, kappa, rand_grid)
                new_b, _ = step_tcop_core(np.ones_like(grid), 0.0, 0.0, rand_grid)
                if not np.array_equal(new_a, new_b):
                    raise RuntimeError(f"PREFLIGHT FAIL: survival not invariant to u_t={u_t}, kappa={kappa}")

def verify_u_t_for(offsets):
    for u in U_TIERS:
        u_c = offsets[str(u)]["selected"]
        for b in range(N_BLOCKS):
            if u_t_for("cm0", u, u_c, b) != u_c:
                raise RuntimeError("PREFLIGHT FAIL: cm0 path does not feed constant u_const.")
            expect = [0.0, u / 2.0, u][b % 3]
            if u_t_for("cm1", u, None, b) != expect:
                raise RuntimeError("PREFLIGHT FAIL: cm1 schedule ramp incorrect.")
    for b in range(N_BLOCKS):
        if u_t_for("cm1", 0.0, None, b) != 0.0:
            raise RuntimeError("PREFLIGHT FAIL: u=0 tier not identically zero.")

def verify_save_promote_selftest():
    dummy_tmp = os.path.join(DATA_DIR, "c3_w2_tcop_selftest_tmp.npz")
    dummy_fin = os.path.join(DATA_DIR, "c3_w2_tcop_selftest.npz")
    arr = np.zeros((2, 2, 2), dtype=int)
    np.savez_compressed(dummy_tmp, states=arr)
    if not os.path.exists(dummy_tmp):
        raise RuntimeError("PREFLIGHT FAIL: staging save did not produce the expected tmp filename.")
    os.replace(dummy_tmp, dummy_fin)
    chk = np.load(dummy_fin)["states"]
    if chk.shape != (2, 2, 2):
        raise RuntimeError("PREFLIGHT FAIL: save/promote self-test shape mismatch.")
    os.remove(dummy_fin)

# ==========================================
# Naming, manifests, staging
# ==========================================

def npz_final_path(mode, kappa, tier, u_const, seed):
    kstr = sanitize_float(kappa)
    if mode == "cm1":
        ustr = sanitize_float(tier)
        return os.path.join(DATA_DIR, f"c3_w2_tcop_cm1_states_L0.4_k{kstr}_u{ustr}_s{seed}.npz")
    ucstr = sanitize_float(u_const)
    return os.path.join(DATA_DIR, f"c3_w2_tcop_cm0_states_L0.4_k{kstr}_uc{ucstr}_s{seed}.npz")

def npz_tmp_path(final_path):
    return final_path[:-4] + "_tmp.npz"

def build_row_manifest(offsets):
    rows = []
    for (c, kappa) in KAPPA_MAP:
        for seed in SEEDS:
            rows.append({"mode": "cm1", "stage": "stageA", "c_label": c, "kappa": kappa,
                         "tier": 0.0, "u_const": None, "seed": seed})
    for (c, kappa) in KAPPA_MAP:
        for u in U_TIERS:
            for seed in SEEDS:
                rows.append({"mode": "cm1", "stage": "stageB", "c_label": c, "kappa": kappa,
                             "tier": u, "u_const": None, "seed": seed})
    for (c, kappa) in KAPPA_MAP:
        for u in U_TIERS:
            u_c = offsets[str(u)]["selected"]
            for seed in SEEDS:
                rows.append({"mode": "cm0", "stage": "stageC", "c_label": c, "kappa": kappa,
                             "tier": u, "u_const": u_c, "seed": seed})
    for r in rows:
        r["npz"] = npz_final_path(r["mode"], r["kappa"], r["tier"], r["u_const"] or 0.0, r["seed"]) \
            if r["mode"] == "cm0" else npz_final_path(r["mode"], r["kappa"], r["tier"], None, r["seed"])
        r["expected_shape"] = [TICKS_PER_RUN, GRID_SIZE, GRID_SIZE]
    return rows

def committed_parity_inputs():
    files = {}
    for (c, kappa) in KAPPA_MAP:
        kstr = sanitize_float(kappa)
        for seed in SEEDS:
            p = os.path.join(DATA_DIR, f"c3_w2_rule_c_m2_states_L0.4_k{kstr}_s{seed}.npz")
            files[p] = "m2"
    for seed in SEEDS:
        p = os.path.join(DATA_DIR, f"c3_w2_null_extension_states_L0.4_kp0_0000_s{seed}.npz")
        files[p] = "ne"
    return files

def do_preflight():
    run_parity_check()
    os.makedirs(DATA_DIR, exist_ok=True)
    offsets = solve_static_offsets()
    verify_driven_path_construction(offsets)
    verify_u_t_for(offsets)
    verify_save_promote_selftest()

    inputs = {}
    for path, fam in committed_parity_inputs().items():
        if not os.path.exists(path):
            raise RuntimeError(f"PREFLIGHT FAIL (fail closed): missing parity input {path}")
        inputs[path] = {"family": fam, "sha256": sha256_file(path)}

    rows = build_row_manifest(offsets)
    manifest = {
        "contract_commit": CONTRACT_COMMIT,
        "addendum_commit": ADDENDUM_COMMIT,
        "delta_rho_match": DELTA_RHO_MATCH,
        "kappa_map": KAPPA_MAP,
        "seeds": SEEDS,
        "u_tiers": U_TIERS,
        "static_offsets": offsets,
        "inputs": inputs,
        "row_manifest": rows,
        "expected_outputs": [r["npz"] for r in rows] + [BLOCK_CSV, WINDOW_CSV, MANIFEST_PATH],
        "expected_shapes": {"npz": [TICKS_PER_RUN, GRID_SIZE, GRID_SIZE]},
        "script_sha256": sha256_file(os.path.abspath(__file__)),
    }
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=1)
    print("PREFLIGHT OK")
    print(f"  parity check: PASS (committed apparatus, incl. both null machines)")
    print(f"  driven-path construction check: PASS (atol={DRIVEN_CHECK_ATOL})")
    print(f"  u_t_for assertions: PASS (all {N_BLOCKS} blocks, all tiers, both modes)")
    print(f"  save/promote self-test: PASS")
    for u in U_TIERS:
        o = offsets[str(u)]
        print(f"  tier u={u}: rho_bar_sched={o['rho_bar_sched']:.6f}  u_const={o['selected']:.6f}  "
              f"u/2 gap={o['u_half_gap']:.6f} (tol {TOL_U2:.6f}; diagnostic only; solved-always)")
    print(f"  inputs digested: {len(inputs)} files; rows planned: {len(rows)}")
    print(f"  manifest: {MANIFEST_PATH}")

# ==========================================
# Run execution
# ==========================================

def load_manifest_or_die():
    if not os.path.exists(MANIFEST_PATH):
        raise RuntimeError("STAGE FAIL: preflight manifest missing. Run preflight first.")
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)
    here = sha256_file(os.path.abspath(__file__))
    if here != manifest["script_sha256"]:
        raise RuntimeError("STAGE FAIL (fail closed): script digest does not match preflight manifest.")
    return manifest

def execute_run(mode, c_label, kappa, tier, u_const, seed, stage):
    np.random.seed(seed)
    random.seed(seed)

    flat_grid = np.zeros(N_CELLS, dtype=int)
    flat_grid[:INIT_ACTIVE_CELLS] = 1
    np.random.shuffle(flat_grid)
    grid = flat_grid.reshape((GRID_SIZE, GRID_SIZE))

    states = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE), dtype=int)
    rhos = np.zeros(TICKS_PER_RUN)
    p_becomes = np.zeros((TICKS_PER_RUN, GRID_SIZE, GRID_SIZE))

    for t in range(TICKS_PER_RUN):
        states[t] = grid
        rhos[t] = np.mean(grid)
        block_idx = t // BLOCK_LENGTH
        u_t = u_t_for(mode, tier, u_const, block_idx)
        rand_grid = np.random.rand(GRID_SIZE, GRID_SIZE)
        grid, p_b = step_tcop_core(grid, u_t, kappa, rand_grid)
        p_becomes[t] = p_b

    run_id = os.path.basename(npz_final_path(mode, kappa, tier, u_const if mode == "cm0" else None, seed))[:-4]

    block_rows = []
    for b in range(N_BLOCKS):
        b_states = states[b*BLOCK_LENGTH:(b+1)*BLOCK_LENGTH]
        b_p = p_becomes[b*BLOCK_LENGTH:(b+1)*BLOCK_LENGTH]
        b_rho = rhos[b*BLOCK_LENGTH:(b+1)*BLOCK_LENGTH]
        u_t = u_t_for(mode, tier, u_const, b)

        tick_Is, tick_Is_masked = [], []
        for i in range(BLOCK_LENGTH):
            tick_Is.append(calculate_morans_i_toroidal_8(b_p[i]))
            inact = (b_states[i] == 0)
            if inact.any() and (~inact).any():
                pm = b_p[i].copy()
                pm[~inact] = b_p[i][inact].mean()
                tick_Is_masked.append(calculate_morans_i_toroidal_8(pm))
            else:
                tick_Is_masked.append(0.0)

        cell_slope = b_p * (1.0 - b_p)
        in_primary = (3 <= b <= 14)
        if b <= 2:
            reason = "" if in_primary else "PRE_PRIMARY_INCOMPLETE_CYCLE"
        elif b == 15:
            reason = "BLOCK_15_PARTIAL_CYCLE"
        else:
            reason = ""

        block_rows.append({
            "run_id": run_id, "mode": mode, "stage": stage, "c_label": c_label, "kappa": kappa,
            "tier": tier, "u_const": u_const if mode == "cm0" else "",
            "seed": seed, "block_idx": b, "u_t": u_t, "schedule_phase": b % 3,
            "block_in_primary_set": in_primary, "primary_exclusion_reason": reason,
            "block_rho": float(np.mean(b_rho)),
            "raw_Psi_meanI_state": float(np.mean(batch_morans_i_toroidal_8(b_states))),
            "raw_Psi_persistence_I": float(calculate_morans_i_toroidal_8(np.mean(b_states, axis=0))),
            "analytic_realized_delta_p_driven": float(sigmoid(LOGIT_L + u_t + kappa) - sigmoid(LOGIT_L + u_t - kappa)),
            "mean_p_become": float(np.mean(b_p)),
            "mean_slope": float(np.mean(cell_slope)),
            "q05_slope": float(np.percentile(cell_slope, 5)),
            "tail_mass": float(np.mean((b_p < 0.05) | (b_p > 0.95))),
            "p_min": float(np.min(b_p)), "p_max": float(np.max(b_p)),
            "prop_I_full_surface": float(np.mean(tick_Is)),
            "prop_I_masked_diagnostic": float(np.mean(tick_Is_masked)),
        })

    window_rows = []
    for w_start in range(0, TICKS_PER_RUN - WINDOW_LENGTH + 1, WINDOW_STEP):
        w_end = w_start + WINDOW_LENGTH
        w_states = states[w_start:w_end]
        w_rhos = rhos[w_start:w_end]
        w_start_block = w_start // BLOCK_LENGTH

        drift, cv, range_over, mean_rho, steady_cand, lifted_cand = evaluate_window_ss(w_rhos)

        tick_Is = batch_morans_i_toroidal_8(w_states)
        psi_meanI = float(np.mean(tick_Is))
        psi_meanI_z = compute_meanI_state_null(w_states, psi_meanI)
        pgrid = np.mean(w_states, axis=0)
        psi_pers = float(calculate_morans_i_toroidal_8(pgrid))
        psi_pers_z = compute_persistence_null(pgrid, psi_pers)

        mean_active_state_variance = float(np.mean([np.var(g) for g in w_states]))
        persistence_std = float(np.std(pgrid))
        extinction_deg = bool(mean_rho <= LIFTED_THRESHOLD)
        saturation_deg = bool((mean_rho >= 0.95) or (mean_active_state_variance < VAR_EPSILON))
        low_low = bool(lifted_cand and (not extinction_deg) and (not saturation_deg) and
                       (abs(psi_meanI_z) < LOW_Z_THRESH) and (abs(psi_pers_z) < LOW_Z_THRESH) and
                       (mean_active_state_variance >= VAR_EPSILON))

        in_primary = (3 <= w_start_block <= 11)
        if w_start_block <= 2:
            w_reason = "PRE_PRIMARY_PHASE_IMBALANCE"
        elif w_start_block >= 12:
            w_reason = "EXITS_PRIMARY_BLOCK_SET"
        else:
            w_reason = ""

        w_blocks = [block_rows[w_start_block + i] for i in range(4)]
        dp_vals = [br["analytic_realized_delta_p_driven"] for br in w_blocks]
        comp = {}
        for br in w_blocks:
            key = f"{br['u_t']:.4f}"
            comp[key] = comp.get(key, 0) + 1

        window_rows.append({
            "run_id": run_id, "mode": mode, "stage": stage, "c_label": c_label, "kappa": kappa,
            "tier": tier, "u_const": u_const if mode == "cm0" else "", "seed": seed,
            "window_start_tick": w_start, "window_start_block": w_start_block,
            "window_start_schedule_phase": w_start_block % 3,
            "window_in_primary_family": in_primary, "primary_exclusion_reason": w_reason,
            "window_mean_rho": float(mean_rho),
            "raw_Psi_meanI_state": psi_meanI, "Psi_meanI_state_z": float(psi_meanI_z),
            "raw_Psi_persistence_I": psi_pers, "Psi_persistence_I_z": float(psi_pers_z),
            "relative_drift": float(drift), "rho_cv": float(cv),
            "rho_range_over_mean": float(range_over),
            "mean_active_state_variance": mean_active_state_variance,
            "persistence_std": persistence_std,
            "Steady_State_Candidate_APPARATUS_ONLY": str(steady_cand),
            "Lifted_Activation_Candidate_APPARATUS_ONLY": str(lifted_cand),
            "extinction_degenerate_APPARATUS_ONLY": str(extinction_deg),
            "saturation_degenerate_APPARATUS_ONLY": str(saturation_deg),
            "LowLow_Nondegenerate_Candidate_APPARATUS_ONLY": str(low_low),
            "analytic_realized_delta_p_u0_convention": float(sigmoid(LOGIT_L + kappa) - sigmoid(LOGIT_L - kappa)),
            "driven_realized_contrast_mean": float(np.mean(dp_vals)),
            "driven_realized_contrast_range": float(np.max(dp_vals) - np.min(dp_vals)),
            "window_schedule_composition": json.dumps(comp, sort_keys=True),
        })

    return states, block_rows, window_rows

def run_stage(stage):
    manifest = load_manifest_or_die()
    marker = STAGE_MARKER.format(stage=stage)
    if os.path.exists(marker):
        raise RuntimeError(f"STAGE FAIL: {stage} already marked complete. No resume; route to Mike.")

    rows = [r for r in manifest["row_manifest"] if r["stage"] == stage]
    if not rows:
        raise RuntimeError(f"STAGE FAIL: no rows for stage {stage}.")

    # Pre-write collision halt (R3)
    for r in rows:
        if os.path.exists(r["npz"]):
            raise RuntimeError(f"STAGE FAIL (collision, pre-write): {r['npz']} exists. Route to Mike.")
        tmp = npz_tmp_path(r["npz"])
        if os.path.exists(tmp):
            os.remove(tmp)

    staged = []
    block_rows_all, window_rows_all = [], []
    for i, r in enumerate(rows):
        u_c = r["u_const"]
        states, b_rows, w_rows = execute_run(r["mode"], r["c_label"], r["kappa"], r["tier"], u_c, r["seed"], stage)

        if stage == "stageA":
            kstr = sanitize_float(r["kappa"])
            m2_path = os.path.join(DATA_DIR, f"c3_w2_rule_c_m2_states_L0.4_k{kstr}_s{r['seed']}.npz")
            m2 = np.load(m2_path)["states"]
            assert np.array_equal(states[:200], m2), \
                f"F3-A FAIL: c={r['c_label']} seed={r['seed']} not bit-exact vs committed M2 (ticks 0-199). HALT."
            if r["kappa"] == 0.0:
                ne_path = os.path.join(DATA_DIR, f"c3_w2_null_extension_states_L0.4_kp0_0000_s{r['seed']}.npz")
                ne = np.load(ne_path)["states"]
                assert np.array_equal(states, ne), \
                    f"F3-B FAIL: (u=0,c=0) seed={r['seed']} not bit-exact vs null-extension (400 ticks). HALT."

        tmp = npz_tmp_path(r["npz"])
        np.savez_compressed(tmp, states=states)
        staged.append((tmp, r["npz"]))
        block_rows_all.extend(b_rows)
        window_rows_all.extend(w_rows)
        print(f"[{stage}] {i+1}/{len(rows)} staged: {os.path.basename(r['npz'])}")

    # Atomic promotion after all runs + gates pass
    for tmp, fin in staged:
        chk = np.load(tmp)["states"]
        if chk.shape != (TICKS_PER_RUN, GRID_SIZE, GRID_SIZE):
            raise RuntimeError(f"STAGE FAIL: staged shape mismatch {tmp}.")
        if os.path.exists(fin):
            raise RuntimeError(f"STAGE FAIL (collision at promotion): {fin} exists.")
        os.replace(tmp, fin)

    # Per-stage CSVs concatenated at promotion (M2 fix)
    bdf = pd.DataFrame(block_rows_all)
    wdf = pd.DataFrame(window_rows_all)
    for path, df in [(BLOCK_CSV, bdf), (WINDOW_CSV, wdf)]:
        stage_part = path[:-4] + f"_{stage}.csv"
        df.to_csv(stage_part, index=False)
        if os.path.exists(path):
            existing = pd.read_csv(path)
            pd.concat([existing, df], ignore_index=True).to_csv(path, index=False)
        else:
            df.to_csv(path, index=False)

    with open(marker, "w") as f:
        f.write("complete\n")
    print(f"{stage} COMPLETE: {len(rows)} runs promoted; CSVs written; marker set.")

# ==========================================
# CLI dispatch (strict whitelist)
# ==========================================

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("preflight", "stageA", "stageB", "stageC"):
        raise SystemExit("Usage: c3_w2_tcop.py {preflight|stageA|stageB|stageC}")
    cmd = sys.argv[1]
    if cmd == "preflight":
        do_preflight()
    else:
        run_stage(cmd)
